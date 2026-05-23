"""
Command-line entry point for the prompt optimizer.

How to run:
1. Install dependencies:
   pip install -r requirements.txt

2. Copy .env.example to .env and add your Gemini API key:
   GEMINI_API_KEY=your_api_key_here

3. Send a prompt through stdin:
   "Write me a LinkedIn post about my new app" | python main.py

   Or from a file:
   Get-Content prompt.txt | python main.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from llm_client import EmptyGeminiResponseError, GeminiAPIError, optimize_prompt


ENV_FILE_NAME = ".env"
API_KEY_NAME = "GEMINI_API_KEY"
LOG_FILE_NAME = "prompt_logs.txt"


def load_env_file(file_path: Path) -> None:
    """Load KEY=VALUE lines from a .env file into environment variables."""
    if not file_path.exists():
        return

    for line in file_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def read_prompt_from_stdin() -> str:
    """Read the user's prompt from stdin."""
    if sys.stdin.isatty():
        print(
            "Paste your prompt, then press Ctrl+Z and Enter on Windows "
            "(or Ctrl+D on macOS/Linux):",
            file=sys.stderr,
        )

    return sys.stdin.read().strip()


def save_prompt_log(log_file_path: Path, original_prompt: str, optimized_prompt: str) -> None:
    """Append the original and optimized prompt to a readable log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"""
============================================================
Date/Time: {timestamp}

Original Prompt:
{original_prompt}

Optimized Prompt:
{optimized_prompt}

"""

    with log_file_path.open("a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


def main() -> int:
    """Run the CLI program."""
    project_folder = Path(__file__).resolve().parent
    load_env_file(project_folder / ENV_FILE_NAME)

    api_key = os.getenv(API_KEY_NAME)
    if not api_key:
        print(
            f"Missing API key: {API_KEY_NAME} was not found.\n"
            f"Copy {project_folder / '.env.example'} to {project_folder / ENV_FILE_NAME} "
            "and add your real API key.",
            file=sys.stderr,
        )
        return 1

    original_prompt = read_prompt_from_stdin()
    if not original_prompt:
        print("Empty input: no prompt was provided through stdin.", file=sys.stderr)
        return 1

    try:
        optimized_prompt = optimize_prompt(original_prompt, api_key)
    except EmptyGeminiResponseError as error:
        print(f"No response returned: {error}", file=sys.stderr)
        return 1
    except GeminiAPIError as error:
        print(f"Gemini API failure: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"Unexpected error: {error}", file=sys.stderr)
        return 1

    print(optimized_prompt)
    save_prompt_log(project_folder / LOG_FILE_NAME, original_prompt, optimized_prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
