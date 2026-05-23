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
from pathlib import Path

from llm_client import optimize_prompt


ENV_FILE_NAME = ".env"
API_KEY_NAME = "GEMINI_API_KEY"


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


def main() -> int:
    """Run the CLI program."""
    project_folder = Path(__file__).resolve().parent
    load_env_file(project_folder / ENV_FILE_NAME)

    api_key = os.getenv(API_KEY_NAME)
    if not api_key:
        print(
            f"Error: {API_KEY_NAME} was not found.\n"
            f"Copy {project_folder / '.env.example'} to {project_folder / ENV_FILE_NAME} "
            "and add your real API key.",
            file=sys.stderr,
        )
        return 1

    original_prompt = read_prompt_from_stdin()
    if not original_prompt:
        print("Error: no prompt was provided through stdin.", file=sys.stderr)
        return 1

    try:
        optimized_prompt = optimize_prompt(original_prompt, api_key)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(optimized_prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
