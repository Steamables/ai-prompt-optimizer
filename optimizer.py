"""
Beginner-friendly Gemini prompt optimizer CLI.

Setup:
1. Install the Gemini SDK:
   pip install google-genai

2. Create a file named .env in this same folder:
   GEMINI_API_KEY=your_api_key_here

3. Send a prompt through stdin:
   echo "Write me a LinkedIn post about my new app" | python optimizer.py

   Or from a file:
   Get-Content prompt.txt | python optimizer.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


MODEL_NAME = "gemini-3.5-flash"
ENV_FILE_NAME = ".env"


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


def build_optimizer_instruction(original_prompt: str) -> str:
    """Create the instruction we send to Gemini."""
    return f"""
You are an expert prompt engineer.

Rewrite the user's prompt so it is clearer, more specific, and more useful for
an AI assistant. Preserve the user's original intent. Do not answer the prompt.

Improve the prompt by:
- adding clear role/context when useful
- making the task and expected output explicit
- adding constraints or structure where helpful
- keeping it concise and easy to understand

Return only the optimized prompt.

User's original prompt:
{original_prompt}
""".strip()


def optimize_prompt(original_prompt: str, api_key: str) -> str:
    """Send the prompt to Gemini and return the optimized version."""
    try:
        from google import genai
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency: install it with `pip install google-genai`."
        ) from error

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_optimizer_instruction(original_prompt),
    )

    optimized_prompt = (response.text or "").strip()
    if not optimized_prompt:
        raise RuntimeError("Gemini returned an empty response.")

    return optimized_prompt


def main() -> int:
    """Run the CLI program."""
    script_folder = Path(__file__).resolve().parent
    load_env_file(script_folder / ENV_FILE_NAME)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: GEMINI_API_KEY was not found.\n"
            f"Create {script_folder / ENV_FILE_NAME} and add:\n"
            "GEMINI_API_KEY=your_api_key_here",
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
