"""Interface Wrapper Module - Safe model loading and management. 
This module provides secure loading and interaction with models, preventing command and path injections. 
Key Features: 
- Strict filename/path and input validation (CWE-22) 
- Safe subprocess execution (CWE-77/78) 
- Comprehensive error handling 
- Parameterized command calls only 
- Whitelisted filenames and extensions 
- Model/provider validation."""
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
# Logging config
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# SECURITY CONSTANTS
ALLOWED_MODEL_PATTERN = re.compile(r'^[a-zA-Z0-9:._-]+$')
ALLOWED_PACKAGE_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
ALLOWED_PROVIDERS = {'ollama', 'gemini', 'openai', 'local'}
MAX_MODEL_NAME_LENGTH = 200
MAX_PACKAGE_NAME_LENGTH = 100
ALLOWED_EXTENSIONS = {'.bin', '.json', '.txt', '.yaml'}
ALLOWED_FILENAMES = {'config.json', 'model.bin', 'history.json', 'state.yaml'}
def validate_filename(filename: str) -> bool:
    """Only allow whitelisted filenames/extensions, deny all others."""
    try:
        if not isinstance(filename, str):
            return False
        if len(filename) > 128:
            return False
        ext = Path(filename).suffix
        if filename in ALLOWED_FILENAMES or (ext in ALLOWED_EXTENSIONS):
            # Disallow any form of path traversal
            if (os.path.basename(filename) == filename) and ('..' not in filename and filename[0] != '/'): 
                return True
        return False
    except Exception:
        return False
def validate_model_name(model: str) -> bool:
    if not isinstance(model, str) or len(model) > MAX_MODEL_NAME_LENGTH:
        return False
    return bool(ALLOWED_MODEL_PATTERN.match(model))
def validate_package_name(pkg: str) -> bool:
    if not isinstance(pkg, str) or len(pkg) > MAX_PACKAGE_NAME_LENGTH:
        return False
    return bool(ALLOWED_PACKAGE_PATTERN.match(pkg))
def validate_provider(provider: str) -> bool:
    return provider in ALLOWED_PROVIDERS
# Example safe file open
def safe_open_json(filename) -> dict:
    if not validate_filename(filename):
        logger.error(f"Invalid file access attempt: {filename}")
        raise ValueError("Invalid filename")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"File read failed: {filename}: {e}")
        raise
# Example safe subprocess call
def safe_subprocess_run(args: List[str], timeout_sec=10) -> subprocess.CompletedProcess:
    if not (isinstance(args, list) and len(args) >= 1 and all(isinstance(a, str) for a in args)):
        raise ValueError("Invalid args for subprocess")
    # NEVER invoke with shell=True and NEVER concatenate user input into commands
    try:
        result = subprocess.run(args, timeout=timeout_sec, check=True, text=True, capture_output=True, shell=False)
        return result
    except subprocess.CalledProcessError as cpe:
        logger.error(f"Subprocess error: {cpe}")
        raise
    except Exception as e:
        logger.error(f"Subprocess failure: {e}")
        raise
# Model/client wrapper
class ModelManager:
    def __init__(self):
        self.clients = {}
        self.history = []
    def load_model(self, model_name: str, provider: str, config_file: str = None):
        if not validate_model_name(model_name):
            raise ValueError("Invalid model name")
        if not validate_provider(provider):
            raise ValueError("Invalid provider")
        if config_file and not validate_filename(config_file):
            logger.warning(f"Unsafe config filename: {config_file}")
            raise ValueError("Invalid config file")
        try:
            # Example: Load or startup model safely
            if provider == 'local':
                # Import dynamically, only allowed packages
                if not validate_package_name(model_name):
                    raise ValueError('Unsafe package name')
                client = importlib.import_module(model_name)
            elif provider == 'ollama':
                import ollama
                client_kwargs = {}
                if config_file:
                    client_kwargs['config'] = safe_open_json(config_file)
                # Additional validation if needed
                client = ollama.Client(**client_kwargs)
                client.show(model_name)  # Validate exists
            else:
                raise NotImplementedError('Provider not supported')
            self.clients[model_name] = client
            logger.info(f"Loaded model {model_name} using {provider}")
        except Exception as e:
            logger.error(f"Model load failure: {model_name}: {e}")
            raise
    def run_model_command(self, model_name: str, args: List[str]):
        if not validate_model_name(model_name):
            raise ValueError("Invalid model name")
        if not isinstance(args, list) or not all(isinstance(x,str) for x in args):
            raise ValueError("Invalid command arguments")
        try:
            result = safe_subprocess_run(args)
            return result.stdout
        except Exception as e:
            logger.error(f"Run command failed: {e}")
            raise
    def get_model_client(self, model_name: str):
        if not validate_model_name(model_name):
            logger.error(f"Invalid model name: {model_name}")
            return None
        return self.clients.get(model_name)
    def add_to_history(self, entry: dict):
        if not isinstance(entry, dict):
            logger.error("History entry must be a dictionary")
            return False
        required = {'timestamp', 'action', 'status'}
        if not required.issubset(entry.keys()):
            logger.error(f"Missing required history fields: {required}")
            return False
        self.history.append(entry)
        return True
    def list_loaded_models(self) -> List[str]:
        return list(self.clients.keys())
