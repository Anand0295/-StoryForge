#!/bin/python3
"""
StoryForge - Interactive Testing and Model Selection Utility
Fully security-hardened per CWE-94/77/78/22. Hardened input validation, error handling, and documentation.
"""
import subprocess
from pathlib import Path
from typing import Optional, List
import logging

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Security Constants ---
ALLOWED_MODELS = [
    'llama3.2:latest',
    'llama3.1:latest',
    'mistral:7b',
    'gemini-1.5-pro',
    'gemini-1.5-flash',
]
MAX_PROMPT_LENGTH = 5000
WHITELIST_PROMPT_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:\'\"()-')
SAFE_FLAGS = {'-debug', '-expand_outline', '-no_revision'}  # Explicit flag allow-list

# --- Utility Functions ---
def sanitize_input(user_input: str, max_length: int, whitelist: set) -> str:
    """
    Sanitizes input to allow only whitelisted chars and length.
    Raises ValueError if bad.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    if len(user_input) > max_length:
        raise ValueError(f"Input exceeds max length {max_length}")
    if any(c not in whitelist for c in user_input):
        raise ValueError("Input contains invalid character(s)")
    return user_input

def validate_model_name(model: str) -> bool:
    return model in ALLOWED_MODELS

def validate_file_path(file_path: str, base_dir: str = 'prompts') -> Optional[Path]:
    """
    Path traversal protection: Only allows files inside base_dir.
    """
    try:
        base_path = Path(base_dir).resolve()
        target_path = (base_path / file_path).resolve()
        if not str(target_path).startswith(str(base_path)):
            raise ValueError("Path traversal detected")
        if not target_path.is_file():
            logger.error(f"File does not exist: {target_path}")
            return None
        return target_path
    except Exception as e:
        logger.error(f"File path validation failed: {e}")
        return None

def execute_command_safely(command: List[str], timeout: int = 300) -> int:
    """
    Run process using subprocess (no shell). Logs errors/results.
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
            logger.warning(f"Process failed, code {result.returncode}")
            if result.stderr:
                logger.error(f"STDERR: {result.stderr}")
        else:
            logger.info("Process succeeded")
        return result.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s")
        raise
    except Exception as e:
        logger.error(f"Subprocess error: {e}")
        raise

def run_story_generation(prompt: str, model: str, outline_model: Optional[str]=None, chapter_model: Optional[str]=None, flags: Optional[str]=None) -> int:
    """
    Validates all user parameters, builds command safely, and runs Write.py.
    """
    # Validate model(s)
    if not validate_model_name(model):
        raise ValueError(f"Invalid main model: {model}")
    if outline_model and not validate_model_name(outline_model):
        raise ValueError(f"Invalid outline model: {outline_model}")
    if chapter_model and not validate_model_name(chapter_model):
        raise ValueError(f"Invalid chapter model: {chapter_model}")
    # Sanitize prompt (required, strict)
    prompt = sanitize_input(prompt, MAX_PROMPT_LENGTH, WHITELIST_PROMPT_CHARS)
    if not prompt.strip():
        raise ValueError("Prompt must not be empty")
    # Build command
    command = ['python', 'Write.py', '-Prompt', prompt]
    if outline_model:
        command += ['-InitialOutlineModel', outline_model]
    if chapter_model:
        command += ['-ChapterModel', chapter_model]
    # Only permit explicitly whitelisted flags
    if flags:
        for flag in flags.split():
            if flag in SAFE_FLAGS:
                command.append(flag)
            else:
                logger.warning(f"Unsafe flag ignored: {flag}")
    # Run it
    return execute_command_safely(command)

def load_prompt_from_file(file_path: str) -> Optional[str]:
    """
    Loads prompt file after strict path traversal and file length checks.
    """
    validated_path = validate_file_path(file_path, base_dir='prompts')
    if not validated_path:
        logger.error(f"Invalid prompt file path: {file_path}")
        return None
    with open(validated_path, 'r', encoding='utf-8') as f:
        content = f.read(MAX_PROMPT_LENGTH + 1)
        if len(content) > MAX_PROMPT_LENGTH:
            logger.error(f"Prompt file too large: {file_path}")
            return None
        # Re-use sanitization for this content
        try:
            sanitized = sanitize_input(content.strip(), MAX_PROMPT_LENGTH, WHITELIST_PROMPT_CHARS)
            return sanitized
        except ValueError as e:
            logger.error(f"Loaded prompt contains forbidden data: {e}")
            return None

def interactive_test_menu() -> None:
    """
    Fully interactive CLI menu, validates all inputs, safe execution.
    """
    try:
        print("\n" + "="*60)
        print("StoryForge Interactive Testing Utility (Security-Hardened)")
        print("="*60)

        # Model picker
        print("\nAvailable Models:")
        for idx, m in enumerate(ALLOWED_MODELS, 1):
            print(f"{idx}. {m}")
        model_choice = input(f"Select model (1-{len(ALLOWED_MODELS)}): ")
        try:
            model_idx = int(model_choice.strip()) - 1
            if not 0 <= model_idx < len(ALLOWED_MODELS):
                raise ValueError
            selected_model = ALLOWED_MODELS[model_idx]
        except Exception:
            logger.error("Invalid model selection")
            return

        # Prompt source
        print("\nPrompt Options:")
        print("1. Use example prompt")
        print("2. Load from file")
        print("3. Enter custom prompt")
        prompt_choice = input("Select prompt option (1-3): ").strip()
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
            try:
                prompt = sanitize_input(prompt, MAX_PROMPT_LENGTH, WHITELIST_PROMPT_CHARS)
            except ValueError as e:
                logger.error(f"Invalid prompt input: {e}")
                return
        else:
            logger.error("Invalid prompt option")
            return
        if not prompt:
            logger.error("No prompt provided")
            return

        print("\nOptional Flags:")
        print("-debug: Enable debug mode")
        print("-expand_outline: Expand story outline")
        print("-no_revision: Skip chapter revisions")
        flags = input("Enter flags (space-separated, or press Enter for none): ").strip()

        # Run generation
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
