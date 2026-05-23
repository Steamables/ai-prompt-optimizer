# Prompt Optimizer CLI

A beginner-friendly Python command-line tool that reads a prompt from `stdin`,
sends it to the Gemini API, and prints a clearer optimized version.

## Project Structure

```text
main.py              # CLI entry point: reads stdin, loads .env, prints output
llm_client.py        # Gemini API client and API-related error handling
prompt_templates.py  # Prompt template sent to Gemini
requirements.txt     # Python package dependencies
.env.example         # Example environment file
```

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and add your real Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit `.env`. It should contain your private API key.

## Usage

Send a prompt into the tool through `stdin`:

```powershell
"Write me a LinkedIn post about my new app" | python main.py
```

You can also read a prompt from a text file:

```powershell
Get-Content prompt.txt | python main.py
```

The tool prints only the optimized prompt, so you can copy it directly into an
LLM chat or another tool.

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

## Error Handling

The CLI includes basic error messages for common problems:

- Missing `GEMINI_API_KEY`
- Empty user input
- Gemini API request failure
- Gemini returning no text

