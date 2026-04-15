import streamlit as st
import requests
import os
import json
from pydantic import BaseModel
from typing import List
from groq import Groq
from dotenv import load_dotenv

# Load API keys from .env file

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Initialize Groq client

client = Groq(api_key=GROQ_API_KEY)

# -------------------------------

# Step 1: Pydantic Model

# -------------------------------

class StudyResponse(BaseModel):
explanation: str
key_points: List[str]
quiz_questions: List[str]

# -------------------------------

# Step 2: Get search data (Serper)

# -------------------------------

def get_search_data(topic):
url = "https://google.serper.dev/search"
headers = {
"X-API-KEY": SERPER_API_KEY,
"Content-Type": "application/json"
}
data = {
"q": topic
}

```
response = requests.post(url, headers=headers, json=data)
results = response.json()

snippets = []
if "organic" in results:
    for item in results["organic"][:2]:  # top 2 results
        snippets.append(item.get("snippet", ""))

return " ".join(snippets)
```

# -------------------------------

# Step 3: Call Groq AI

# -------------------------------

def get_ai_response(topic, context):
prompt = f"""
Explain this topic in simple words: {topic}

```
Use this context:
{context}

Return ONLY JSON:
{{
  "explanation": "...",
  "key_points": ["...", "..."],
  "quiz_questions": ["...", "..."]
}}
"""

chat = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[{"role": "user", "content": prompt}]
)

return chat.choices[0].message.content
```

# -------------------------------

# Step 4: Streamlit UI

# -------------------------------

st.title("📘 Simple AI Study Helper")

topic = st.text_input("Enter a topic:")

if st.button("Generate"):
if topic.strip() == "":
st.warning("Please enter a topic")
else:
with st.spinner("Generating..."):

```
        # Step 1: Get search data
        context = get_search_data(topic)

        # Step 2: Get AI response
        raw_output = get_ai_response(topic, context)

        try:
            # Step 3: Convert to JSON
            data = json.loads(raw_output)

            # Step 4: Validate with Pydantic
            result = StudyResponse(**data)

            # Step 5: Display output
            st.subheader("🧠 Explanation")
            st.write(result.explanation)

            st.subheader("🔑 Key Points")
            for point in result.key_points:
                st.write("- ", point)

            st.subheader("❓ Quiz Questions")
            for q in result.quiz_questions:
                st.write("- ", q)

        except Exception as e:
            st.error("Error parsing AI response. Try again.")
```
