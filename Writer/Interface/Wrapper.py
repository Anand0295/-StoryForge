"""Interface Wrapper Module - Safe model loading and management.

This module provides a safe interface for loading and managing multiple AI models
with proper input validation, subprocess safety, and error handling.

Key Features:
- Safe subprocess execution without shell injection (CWE-77/78/88)
- Input validation for package names and model identifiers
- Path traversal protection (CWE-22)
- Comprehensive error handling with logging
- Support for multiple model providers (Ollama, external APIs)
"""

import os
import sys
import json
import logging
import importlib
import subprocess
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from urllib.parse import parse_qs, urlparse

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security constants
ALLOWED_PACKAGE_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
ALLOWED_MODEL_PATTERN = re.compile(r'^[a-zA-Z0-9:._-]+$')
ALLOWED_PROVIDERS = {'ollama', 'gemini', 'openai', 'local'}
MAX_PACKAGE_NAME_LENGTH = 100
MAX_MODEL_NAME_LENGTH = 200


def validate_package_name(package_name: str) -> bool:
    """Validate package name to prevent injection attacks (CWE-77/78/88).
    
    Args:
        package_name: Package name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(package_name, str):
        return False
    
    if len(package_name) > MAX_PACKAGE_NAME_LENGTH:
        logger.warning(f"Package name too long: {len(package_name)} characters")
        return False
    
    if not ALLOWED_PACKAGE_PATTERN.match(package_name):
        logger.warning(f"Package name contains invalid characters: {package_name}")
        return False
    
    return True


def validate_model_name(model_name: str) -> bool:
    """Validate model name format.
    
    Args:
        model_name: Model name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(model_name, str):
        return False
    
    if len(model_name) > MAX_MODEL_NAME_LENGTH:
        logger.warning(f"Model name too long: {len(model_name)} characters")
        return False
    
    if not ALLOWED_MODEL_PATTERN.match(model_name):
        logger.warning(f"Model name contains invalid characters: {model_name}")
        return False
    
    return True


def validate_provider(provider: str) -> bool:
    """Validate provider name.
    
    Args:
        provider: Provider name to validate
        
    Returns:
        True if valid, False otherwise
    """
    return provider.lower() in ALLOWED_PROVIDERS


def execute_pip_install_safely(package_name: str) -> bool:
    """Execute pip install safely without shell injection (CWE-77/78/88).
    
    Args:
        package_name: Package name to install (will be validated)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate package name
        if not validate_package_name(package_name):
            logger.error(f"Invalid package name: {package_name}")
            return False
        
        logger.info(f"Installing package: {package_name}")
        
        # Use subprocess with list (no shell=True to prevent injection)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                package_name
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Failed to install {package_name}: {result.stderr}")
            return False
        
        logger.info(f"Successfully installed {package_name}")
        return True
    except subprocess.TimeoutExpired:
        logger.error(f"Installation of {package_name} timed out")
        return False
    except Exception as e:
        logger.error(f"Error installing {package_name}: {e}")
        return False


def safe_import_package(package_name: str) -> Optional[Any]:
    """Safely import a package or install it if missing.
    
    Args:
        package_name: Package name to import
        
    Returns:
        Imported module or None if failed
    """
    try:
        if not validate_package_name(package_name):
            logger.error(f"Invalid package name format: {package_name}")
            return None
        
        # Try to import
        return importlib.import_module(package_name)
    except ImportError:
        logger.warning(f"Package {package_name} not found. Attempting installation...")
        if execute_pip_install_safely(package_name):
            try:
                return importlib.import_module(package_name)
            except ImportError as e:
                logger.error(f"Failed to import {package_name} after installation: {e}")
                return None
        return None
    except Exception as e:
        logger.error(f"Unexpected error importing {package_name}: {e}")
        return None


def safe_load_json_file(file_path: str, base_dir: str = '.') -> Optional[Dict]:
    """Safely load JSON file with path traversal protection (CWE-22).
    
    Args:
        file_path: Path to JSON file
        base_dir: Base directory for file access
        
    Returns:
        Loaded JSON data or None if failed
    """
    try:
        # Validate path to prevent traversal attacks
        base_path = Path(base_dir).resolve()
        target_path = (base_path / file_path).resolve()
        
        # Ensure target is within base directory
        if not str(target_path).startswith(str(base_path)):
            logger.error(f"Path traversal attempt detected: {file_path}")
            return None
        
        if not target_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        
        if not target_path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            return None
        
        # Read and parse JSON
        with open(target_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Successfully loaded JSON from {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        return None


class Interface:
    """Safe model interface with proper error handling and input validation."""
    
    def __init__(self, models: Optional[List[str]] = None):
        """Initialize interface with optional list of models to load.
        
        Args:
            models: Optional list of model identifiers to load
        """
        try:
            self.clients: Dict[str, Any] = {}
            self.history: List[Dict] = []
            self.model_configs: Dict[str, Dict] = {}
            
            if models:
                self.load_models(models)
        except Exception as e:
            logger.error(f"Error initializing Interface: {e}")
            self.clients = {}
            self.history = []
            self.model_configs = {}
    
    def load_models(self, models: List[str]) -> bool:
        """Load multiple models safely with validation.
        
        Args:
            models: List of model identifiers
            
        Returns:
            True if all models loaded successfully, False otherwise
        """
        try:
            if not isinstance(models, list):
                logger.error("Models must be a list")
                return False
            
            success = True
            for model in models:
                if not validate_model_name(model):
                    logger.error(f"Invalid model name: {model}")
                    success = False
                    continue
                
                try:
                    self._load_single_model(model)
                except Exception as e:
                    logger.error(f"Failed to load model {model}: {e}")
                    success = False
            
            return success
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    def _load_single_model(self, model: str) -> None:
        """Load a single model with proper error handling.
        
        Args:
            model: Model identifier
            
        Raises:
            ValueError: If model format is invalid
            ImportError: If required packages cannot be loaded
        """
        if model in self.clients:
            logger.debug(f"Model {model} already loaded")
            return
        
        try:
            # Parse model string (format: "provider:model" or "provider://host:model")
            if "://" in model:
                provider, rest = model.split("://", 1)
                if ":" in rest:
                    host, model_name = rest.rsplit(":", 1)
                else:
                    host = rest
                    model_name = "default"
            elif ":" in model:
                provider, model_name = model.split(":", 1)
                host = None
            else:
                provider = "ollama"
                model_name = model
                host = None
            
            # Validate provider
            if not validate_provider(provider):
                raise ValueError(f"Invalid provider: {provider}")
            
            # Validate model name
            if not validate_model_name(model_name):
                raise ValueError(f"Invalid model name: {model_name}")
            
            logger.info(f"Loading model {model_name} from {provider}")
            
            # Load based on provider
            if provider == "ollama":
                self._load_ollama_model(model_name, host)
            else:
                logger.warning(f"Provider {provider} not yet implemented")
        except Exception as e:
            logger.error(f"Error loading model {model}: {e}")
            raise
    
    def _load_ollama_model(self, model_name: str, host: Optional[str] = None) -> None:
        """Load an Ollama model safely.
        
        Args:
            model_name: Name of the model to load
            host: Optional Ollama host address
            
        Raises:
            ImportError: If ollama package not available
            Exception: If model cannot be loaded
        """
        try:
            ollama = safe_import_package("ollama")
            if not ollama:
                raise ImportError("Could not import ollama package")
            
            # Create client
            client_kwargs = {}
            if host:
                client_kwargs["host"] = host
            
            try:
                client = ollama.Client(**client_kwargs)
                # Verify model exists
                client.show(model_name)
                self.clients[model_name] = client
                logger.info(f"Successfully loaded Ollama model: {model_name}")
            except Exception:
                logger.info(f"Model {model_name} not found. Attempting to pull...")
                client = ollama.Client(**client_kwargs)
                # Pull model (this may take time)
                client.pull(model_name)
                self.clients[model_name] = client
                logger.info(f"Successfully pulled and loaded Ollama model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading Ollama model {model_name}: {e}")
            raise
    
    def get_model_client(self, model_name: str) -> Optional[Any]:
        """Get client for a loaded model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model client or None if not loaded
        """
        if not validate_model_name(model_name):
            logger.error(f"Invalid model name: {model_name}")
            return None
        
        return self.clients.get(model_name)
    
    def list_loaded_models(self) -> List[str]:
        """Get list of currently loaded models.
        
        Returns:
            List of loaded model names
        """
        return list(self.clients.keys())
    
    def add_to_history(self, entry: Dict) -> bool:
        """Add entry to history with validation.
        
        Args:
            entry: History entry to add
            
        Returns:
            True if added successfully
        """
        try:
            if not isinstance(entry, dict):
                logger.error("History entry must be a dictionary")
                return False
            
            # Validate entry has required fields
            required_fields = {'timestamp', 'action', 'status'}
            if not required_fields.issubset(entry.keys()):
                logger.error(f"History entry missing required fields: {required_fields}")
                return False
            
            self.history.append(entry)
            return True
        except Exception as e:
            logger.error(f"Error adding to history: {e}")
            return False
