# Prompt Optimizer CLI

A lightweight Python CLI that improves rough prompts using the Gemini API.

The tool reads a prompt from standard input, sends it to Gemini, prints the
optimized prompt, and stores a local prompt history in `prompt_logs.txt`.

## Features

- Optimizes prompts from the command line
- Uses Gemini through the official `google-genai` package
- Loads the API key from a local `.env` file
- Saves prompt history locally without committing it to git
- Keeps the code split into small beginner-friendly modules

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

```powershell
"Write me a LinkedIn post about my new app" | python main.py
```

Or pass a prompt from a file:

```powershell
Get-Content prompt.txt | python main.py
```

## Example

Before:

```text
write email for job
```

After:

```text
Act as a professional career assistant. Write a clear and polite job application
email for a specific role. Include a short introduction, explain why I am
interested in the position, highlight relevant skills or experience, and end
with a professional closing. Keep the tone confident, concise, and respectful.
```

## Prompt Logs

Each successful run is appended to:

```text
prompt_logs.txt
```

This file is ignored by git because it may contain private prompt history.

## Project Structure

```text
main.py              # CLI entry point
llm_client.py        # Gemini API client
prompt_templates.py  # Prompt optimization template
requirements.txt     # Python dependencies
.env.example         # API key placeholder
```
