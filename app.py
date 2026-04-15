import json
import os
from typing import List

import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

# Load API keys from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Fallback models are used when a configured model is decommissioned.
GROQ_FALLBACK_MODELS = [
    GROQ_MODEL,
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


class StudyResponse(BaseModel):
    explanation: str
    key_points: List[str]
    quiz_questions: List[str]


def get_search_data(topic: str) -> str:
    """Fetch top snippets from Serper for additional model context."""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    data = {"q": topic}

    response = requests.post(url, headers=headers, json=data, timeout=20)
    response.raise_for_status()
    results = response.json()

    snippets = []
    if "organic" in results:
        for item in results["organic"][:2]:
            snippets.append(item.get("snippet", ""))

    return " ".join(snippets)


def get_ai_response(topic: str, context: str) -> str:
    prompt = f"""Explain this topic in simple words: {topic}

Use this context:
{context}

Return ONLY JSON:
{{
  "explanation": "...",
  "key_points": ["...", "..."],
  "quiz_questions": ["...", "..."]
}}"""

    last_error: Exception | None = None
    tried_models = []

    for model_name in GROQ_FALLBACK_MODELS:
        if model_name in tried_models:
            continue
        tried_models.append(model_name)

        try:
            chat = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return chat.choices[0].message.content or ""
        except Exception as exc:
            last_error = exc
            error_text = str(exc).lower()
            if "decommissioned" in error_text or "model_decommissioned" in error_text:
                continue
            raise

    raise RuntimeError(
        f"No available Groq model succeeded. Tried: {', '.join(tried_models)}. Last error: {last_error}"
    )


def parse_json_response(raw_output: str) -> dict:
    """Handle plain JSON and fenced JSON outputs from the model."""
    cleaned = raw_output.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    return json.loads(cleaned)


st.title("Simple AI Study Helper")

topic = st.text_input("Enter a topic:")

if st.button("Generate"):
    if topic.strip() == "":
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating..."):
            try:
                context = get_search_data(topic)
                raw_output = get_ai_response(topic, context)
                data = parse_json_response(raw_output)
                result = StudyResponse(**data)

                st.subheader("Explanation")
                st.write(result.explanation)

                st.subheader("Key Points")
                for point in result.key_points:
                    st.write(f"- {point}")

                st.subheader("Quiz Questions")
                for question in result.quiz_questions:
                    st.write(f"- {question}")
            except Exception as exc:
                st.error("Something went wrong while generating results. Check your API keys and try again.")
                st.caption(str(exc))
