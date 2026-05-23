"""
Prompt templates used by the app.

This is where you can change how the optimizer asks Gemini to rewrite prompts.
"""

from __future__ import annotations


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
