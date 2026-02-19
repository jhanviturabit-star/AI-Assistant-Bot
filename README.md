# 🤖 CRM AI Assistant

An AI-powered CRM backend built using FastAPI and LangChain (Groq LLM) that helps manage customers and support tickets through natural language commands.

---

## 🚀 Features

- 🔐 JWT Authentication
- 👤 Customer Management
- 🎫 Ticket Management
- 📊 Ticket Filtering & Summary
- 🤖 AI Agent powered by Groq (LLaMA 3.3 70B)
- 🛠 Tool-based Function Calling Architecture
- 🔒 Strict CRM-only assistant behavior

---

## 🏗 Project Structure

backend/
│
├── auth/              # Authentication logic
├── routes/            # Customers & Tickets routes
├── custom_tools.py    # AI tools
├── main.py            # FastAPI app + AI agent setup
├── config.py          # Environment variables
└── context.py         # Token handling


frontend/
│
├── app.py             # Streamlit UI
├── customers.py
├── tickets.py
└── stats.py

---

## 🧠 AI Agent Design

The assistant uses:

- `langchain_groq`
- Tool-based architecture
- Strict system prompt (CRM-only restrictions)

The AI:
- Calls one tool per request
- Summarizes tool output
- Refuses non-CRM questions

---

## 🔑 Tech Stack

- FastAPI
- LangChain
- Groq API (LLaMA 3.3 70B)
- Streamlit
- JWT Authentication
- Python

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd ai-assistant-bot
