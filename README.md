# AI Prompt Optimizer

A command-line prompt optimization tool powered by Gemini.

It takes a rough prompt from standard input and returns a clearer, more specific
version that is easier to use with AI assistants.

## Features

- Optimize prompts directly from the terminal
- Use Gemini through the `google-genai` SDK
- Configure the API key with a local `.env` file
- Keep prompt templates separate from API and CLI logic
- Store local run history for reference

## Installation

Clone the repository:

```bash
git clone https://github.com/Steamables/ai-prompt-optimizer.git
cd ai-prompt-optimizer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Optimize a prompt:

```bash
echo "Write me a LinkedIn post about my new app" | python main.py
```

Optimize a prompt from a file:

```bash
python main.py < prompt.txt
```

On Windows PowerShell:

```powershell
Get-Content prompt.txt | python main.py
```

## Example

Input:

```text
write email for job
```

Output:

```text
Act as a professional career assistant. Write a clear and polite job application
email for a specific role. Include a short introduction, explain why I am
interested in the position, highlight relevant skills or experience, and end
with a professional closing. Keep the tone confident, concise, and respectful.
```

## Project Structure

```text
.
|-- main.py
|-- llm_client.py
|-- prompt_templates.py
|-- requirements.txt
|-- .env.example
`-- README.md
```
