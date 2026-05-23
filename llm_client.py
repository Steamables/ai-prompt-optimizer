"""
Small Gemini API wrapper.

This file contains only the code that talks to the LLM provider.
Keeping this separate makes the CLI code in main.py easier to read.
"""

from __future__ import annotations

from prompt_templates import build_optimizer_instruction


MODEL_NAME = "gemini-3.5-flash"


def optimize_prompt(original_prompt: str, api_key: str) -> str:
    """Send the user's prompt to Gemini and return the optimized version."""
    try:
        from google import genai
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency: install it with `pip install -r requirements.txt`."
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
