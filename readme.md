# AI Study Helper

Simple Streamlit app for learning a topic quickly.
It combines web context from Serper + LLM output from Groq, then validates the response with Pydantic.

## Features

- Topic explanation in simple language
- Key points summary
- Quiz question generation
- Serper context enrichment (top 2 search snippets)
- Pydantic schema validation for predictable output
- Groq model fallback if a model is decommissioned

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a .env file in the project root:

```env
GROQ_API_KEY=your_groq_key
SERPER_API_KEY=your_serper_key
# Optional: override default model
GROQ_MODEL=llama-3.3-70b-versatile
```

3. Run the app:

```bash
streamlit run app.py
```

## Configuration

- Required:
  - GROQ_API_KEY
  - SERPER_API_KEY
- Optional:
  - GROQ_MODEL

If GROQ_MODEL is not set, the app uses llama-3.3-70b-versatile.
If the selected model is unavailable/decommissioned, the app automatically tries fallback models.

## How It Works

1. User enters a topic in Streamlit.
2. App fetches related context from Serper.
3. App sends a prompt to Groq requesting JSON output.
4. App parses JSON (including fenced JSON responses).
5. Pydantic validates output format.
6. UI displays explanation, key points, and quiz questions.

## Project Structure

```text
.
|- app.py
|- requirements.txt
|- readme.md
|- .env (create locally)
```

## Troubleshooting

- Error: model_decommissioned
  - Set GROQ_MODEL in .env to a currently supported Groq model.
  - The app already retries with fallback models automatically.

- Error: 401 / invalid API key
  - Recheck GROQ_API_KEY and SERPER_API_KEY values.

- Error parsing AI response
  - Retry once. The app expects strict JSON and validates it.

- Serper request failed
  - Confirm SERPER_API_KEY is valid and has quota.

## Tech Stack

- Python
- Streamlit
- Requests
- Groq SDK
- Pydantic
- python-dotenv


