#!/bin/python3
"""
StoryForge - Interactive Testing and Model Selection Utility
This is a comprehensive testing utility that provides an interactive command-line interface
for testing different AI models and configurations with the StoryForge system. It serves as
a developer tool and user-friendly way to experiment with various model combinations.

Key Features:
- Interactive model selection from predefined configurations
- Support for local and remote model testing
- Multiple prompt selection options including custom prompts
- Configurable generation parameters and flags
- Developer testing scripts for advanced model combinations
- Quality vs. speed trade-off options
- Integration with various AI providers (Ollama, Google, etc.)

Model Categories:
1. Local Models: Fast, private, offline generation
   - llama3.2:latest (recommended for general use)
   - llama3.1:latest (higher quality, slower)
   - mistral variants (fast debugging, lower quality)
2. Cloud Models: Higher quality, requires internet
   - Gemini 1.5 Pro/Flash (Google's advanced models)
   - Various quality and speed combinations
3. Developer Configurations: Advanced multi-model setups
   - Specialized model combinations for different tasks
   - High-end models for maximum quality
   - Experimental configurations for research

Prompt Options:
- Pre-built example prompts for testing
- Custom prompt file support
- Default examples covering various genres

Configuration Options:
- Outline expansion control
- Chapter revision settings
- Debug mode activation
- Custom generation flags

Usage Workflow:
1. Select desired model configuration from menu
2. Choose prompt source (examples or custom)
3. Configure additional generation flags
4. System automatically executes Write.py with selected parameters

This utility is essential for:
- Testing new model configurations
- Comparing generation quality across models
- Debugging generation issues
- Experimenting with different parameter combinations
- Developer testing and validation

Note: Some configurations require access to remote model servers
and may have different performance characteristics.
"""

import os
import subprocess
import shlex
from pathlib import Path
from typing import Optional, List, Dict
import logging

# Configure logging for better error tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security constants
ALLOWED_MODELS = {
    'llama3.2:latest',
    'llama3.1:latest',
    'mistral:7b',
    'gemini-1.5-pro',
    'gemini-1.5-flash'
}

MAX_PROMPT_LENGTH = 5000
WHITELIST_PROMPT_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:\'"()-')


def sanitize_input(user_input: str, max_length: int = 1000, whitelist: Optional[set] = None) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        user_input: Raw input from user
        max_length: Maximum allowed length
        whitelist: Set of allowed characters (if None, only basic alphanumeric allowed)
    
    Returns:
        Sanitized input string
    
    Raises:
        ValueError: If input exceeds max length or contains invalid characters
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    if len(user_input) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length} characters")
    
    if whitelist is None:
        whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-')
    
    sanitized = ''.join(c for c in user_input if c in whitelist)
    return sanitized


def validate_model_name(model: str) -> bool:
    """
    Validate that the model name is in the allowed list.
    
    Args:
        model: Model name to validate
    
    Returns:
        True if model is allowed, False otherwise
    """
    return model in ALLOWED_MODELS


def validate_file_path(file_path: str, base_dir: str = '.') -> Optional[Path]:
    """
    Validate and resolve file path safely to prevent path traversal attacks (CWE-22).
    
    Args:
        file_path: Path to validate
        base_dir: Base directory for file access
    
    Returns:
        Resolved Path object if valid, None otherwise
    
    Raises:
        ValueError: If path traversal attempt detected
    """
    try:
        base_path = Path(base_dir).resolve()
        target_path = (base_path / file_path).resolve()
        
        # Ensure target is within base directory
        if not str(target_path).startswith(str(base_path)):
            logger.error(f"Path traversal attempt detected: {file_path}")
            raise ValueError(f"Path traversal attempt detected")
        
        if not target_path.exists():
            logger.error(f"File does not exist: {target_path}")
            return None
        
        return target_path
    except Exception as e:
        logger.error(f"Path validation error: {e}")
        return None


def execute_command_safely(command: List[str], timeout: int = 300) -> int:
    """
    Execute a command safely using subprocess without shell injection (CWE-77/78/88).
    
    Args:
        command: List of command arguments (NOT a string)
        timeout: Command timeout in seconds
    
    Returns:
        Return code of the executed command
    
    Raises:
        subprocess.TimeoutExpired: If command exceeds timeout
        subprocess.CalledProcessError: If command fails
    """
    try:
        logger.info(f"Executing command: {' '.join(command)}")
        result = subprocess.run(
            command,
            timeout=timeout,
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.warning(f"Command failed with return code {result.returncode}")
            if result.stderr:
                logger.error(f"Error output: {result.stderr}")
        else:
            logger.info("Command executed successfully")
        
        return result.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout} seconds")
        raise
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        raise


def run_story_generation(
    prompt: str,
    model: str,
    outline_model: Optional[str] = None,
    chapter_model: Optional[str] = None,
    flags: Optional[str] = None
) -> int:
    """
    Safely execute story generation with validated parameters (CWE-94, CWE-77).
    
    Args:
        prompt: Story prompt (will be validated)
        model: AI model to use (must be in ALLOWED_MODELS)
        outline_model: Optional outline generation model
        chapter_model: Optional chapter generation model
        flags: Optional generation flags
    
    Returns:
        Command return code
    
    Raises:
        ValueError: If validation fails
    """
    try:
        # Validate inputs
        if not validate_model_name(model):
            raise ValueError(f"Invalid model: {model}. Allowed models: {ALLOWED_MODELS}")
        
        if len(prompt) > MAX_PROMPT_LENGTH:
            raise ValueError(f"Prompt exceeds maximum length of {MAX_PROMPT_LENGTH} characters")
        
        if len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be empty")
        
        # Build command as list (prevents shell injection)
        command = [
            'python',
            'Write.py',
            '-Prompt',
            prompt
        ]
        
        # Add optional parameters safely
        if outline_model and validate_model_name(outline_model):
            command.extend(['-InitialOutlineModel', outline_model])
        
        if chapter_model and validate_model_name(chapter_model):
            command.extend(['-ChapterModel', chapter_model])
        
        if flags:
            # Sanitize flags - only allow specific safe flags
            safe_flags = ['-debug', '-expand_outline', '-no_revision']
            for flag in flags.split():
                if flag in safe_flags:
                    command.append(flag)
                else:
                    logger.warning(f"Ignoring unsafe flag: {flag}")
        
        # Execute safely
        return execute_command_safely(command)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in story generation: {e}")
        raise


def load_prompt_from_file(file_path: str) -> Optional[str]:
    """
    Safely load a prompt from a file with path traversal protection (CWE-22).
    
    Args:
        file_path: Path to prompt file
    
    Returns:
        Prompt text if successful, None otherwise
    """
    try:
        # Validate file path
        validated_path = validate_file_path(file_path, base_dir='prompts')
        if not validated_path:
            logger.error(f"Invalid prompt file path: {file_path}")
            return None
        
        with open(validated_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_PROMPT_LENGTH + 1)  # Read slightly more to detect overflow
            
            if len(content) > MAX_PROMPT_LENGTH:
                logger.error(f"Prompt file too large: {file_path}")
                return None
            
            return content.strip()
    except Exception as e:
        logger.error(f"Error loading prompt file: {e}")
        return None


def interactive_test_menu() -> None:
    """
    Interactive testing menu with safe input handling (CWE-94, CWE-77/78/88).
    """
    try:
        print("\n" + "="*60)
        print("StoryForge Interactive Testing Utility")
        print("="*60)
        
        # Model selection
        print("\nAvailable Models:")
        for i, model in enumerate(ALLOWED_MODELS, 1):
            print(f"{i}. {model}")
        
        model_choice = input("\nSelect model (1-{}): ".format(len(ALLOWED_MODELS)))
        
        try:
            model_idx = int(model_choice) - 1
            if not 0 <= model_idx < len(ALLOWED_MODELS):
                raise ValueError("Invalid selection")
            selected_model = list(ALLOWED_MODELS)[model_idx]
        except (ValueError, IndexError):
            logger.error("Invalid model selection")
            return
        
        # Prompt selection
        print("\nPrompt Options:")
        print("1. Use example prompt")
        print("2. Load from file")
        print("3. Enter custom prompt")
        
        prompt_choice = input("\nSelect prompt option (1-3): ")
        prompt = None
        
        if prompt_choice == '1':
            prompt = "Write a fantasy story about a young hero discovering hidden powers."
        elif prompt_choice == '2':
            file_path = input("Enter prompt file path: ")
            prompt = load_prompt_from_file(file_path)
            if not prompt:
                logger.error("Failed to load prompt from file")
                return
        elif prompt_choice == '3':
            prompt = input(f"Enter custom prompt (max {MAX_PROMPT_LENGTH} chars): ")
        else:
            logger.error("Invalid prompt option")
            return
        
        if not prompt:
            logger.error("No prompt provided")
            return
        
        # Flags configuration
        print("\nOptional Flags:")
        print("-debug: Enable debug mode")
        print("-expand_outline: Expand story outline")
        print("-no_revision: Skip chapter revisions")
        
        flags = input("\nEnter flags (space-separated, or press Enter for none): ")
        
        # Execute story generation
        logger.info("Starting story generation...")
        try:
            return_code = run_story_generation(
                prompt=prompt,
                model=selected_model,
                flags=flags if flags else None
            )
            
            if return_code == 0:
                print("\n✓ Story generation completed successfully!")
            else:
                print(f"\n✗ Story generation failed with return code {return_code}")
        except Exception as e:
            logger.error(f"Story generation error: {e}")
            print(f"\n✗ Error: {e}")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error in menu: {e}")
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    try:
        interactive_test_menu()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
