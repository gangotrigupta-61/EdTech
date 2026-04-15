# 📘 Simple AI Study Helper

A beginner-friendly EDTech mini project that uses AI to explain topics, generate key points, and create quiz questions.

---

## 🚀 Features

* 🔍 Fetches real-time data using Serper API
* 🤖 Generates explanations using Groq AI
* ✅ Validates output using Pydantic
* 🎯 Simple and clean Streamlit UI

---

## 🧠 How It Works

1. User enters a topic
2. App fetches short search data (Serper)
3. Sends data to AI (Groq)
4. AI returns structured response
5. Pydantic validates the response
6. Results are displayed on screen

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pydantic
* Groq API
* Serper API

---

## 📁 Project Structure

```
project/
│── app.py
│── .env
│── requirements.txt
```

---

## 🔐 Setup Instructions

### 1. Clone / Download Project

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

---

## ▶️ Run the App

```
streamlit run app.py
```

---

## 💡 Usage

* Enter any topic (e.g., "Photosynthesis")
* Click **Generate**
* Get:

  * Explanation
  * Key Points
  * Quiz Questions

---

## 🎓 Learning Outcome

This project demonstrates:

* AI integration in education
* Real-time search usage
* Data validation using Pydantic
* Basic web app development

---

## 📌 Note

* Keep API keys private
* If error occurs, try again (AI response may vary)

---


