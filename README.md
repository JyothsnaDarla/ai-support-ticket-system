# 🤖 AI-Powered Support Ticket Analytics System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini_3.6_Flash-8E7CC3.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, end-to-end AI analytics platform that converts natural language queries into executable, optimized SQLite commands and automatically identifies operational anomalies in support workflows.

---

## 🎯 Purpose of the Project

In modern customer support operations, non-technical support managers often struggle to extract actionable insights from raw database logs due to SQL barriers. This system bridges that gap by providing:

1. **Natural Language Data Access:** Allows support leads, ops managers, and non-technical stakeholders to ask plain English questions (e.g., *"Which agent has the lowest average customer rating?"*) and receive real-time tabular data.
2. **Automated Anomaly Detection:** Proactively flags unresolved critical tickets, response time SLA breaches, and outlier performance metrics without manual querying.
3. **Enterprise Data Safety:** Prevents direct raw SQL injection risks by utilizing structured system prompting and deterministic parsing layers.

---

## 🏗️ System Architecture & Data Flow


```

+------------------+         HTTP POST         +------------------+
|                  | ------------------------> |                  |
| Streamlit UI     |   /query & /anomalies     | FastAPI Backend  |
| (Interactive)    | <------------------------ | (REST Endpoint)  |
+------------------+        JSON Payload       +------------------+
|
| Prompt + Context
v
+------------------+
| Google Gemini    |
| 3.6 Flash Engine |
+------------------+
|
| Generated SQL
v
+------------------+
| SQLite Database  |
| (tickets.db)     |
+------------------+

```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend Dashboard** | Streamlit | Lightweight, interactive data visualizer and query portal |
| **Backend Framework** | FastAPI | High-concurrency RESTful API engine with Pydantic validation |
| **Database Engine** | SQLite3 | Local high-speed relational storage for ticket telemetry |
| **LLM Provider** | Google Gemini 3.6 Flash | State-of-the-art Text-to-SQL logic generation engine |
| **API Client SDK** | `google-genai` | Official Google GenAI SDK integration |
| **Environment Control** | `python-dotenv` | Secure API credential and secret management |

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+** installed on your system.
* A free **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

---

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/JyothsnaDarla/ai-support-ticket-system.git](https://github.com/JyothsnaDarla/ai-support-ticket-system.git)
   cd ai-support-ticket-system

```

2. **Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure environment credentials:**
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here

```



---

## 💻 Running the Application

This system operates as a decoupled architecture. You will run the backend server and frontend interface in separate terminals.

### Terminal 1: Launch FastAPI Backend

```bash
uvicorn main:app --reload --port 8000

```

* **API Server:** `http://127.0.0.1:8000`
* **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

### Terminal 2: Launch Streamlit Frontend

```bash
streamlit run app.py

```

* **Dashboard App:** `http://localhost:8501`

---

## 📊 Database Schema Context

The LLM logic converts natural language into queries based on the following schema for the `tickets` table:

```sql
CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    created_at DATETIME,
    category TEXT,
    priority TEXT,             -- 'Low', 'Medium', 'High', 'Critical'
    status TEXT,               -- 'Open', 'In Progress', 'Resolved', 'Closed'
    response_time_hrs REAL,
    resolution_time_hrs REAL,
    agent_id TEXT,             -- Unique Support Agent ID
    customer_rating REAL,      -- Rating scale 1.0 - 5.0
    issue_summary TEXT
);

```

---

## 🔍 Sample Analytical Queries

Try testing these questions inside the Streamlit interface:

* *"Which agent has the lowest average customer rating?"*
* *"Show all unresolved tickets with Critical priority."*
* *"List the top 5 agents with the fastest average resolution time."*
* *"Count how many tickets are currently open per category."*

---
## 🛡️License
Distributed under the MIT License. See LICENSE for more information.


<ElicitationsGroup message="Would you like assistance with any of these next steps?">
  <Elicitation label="Create a LICENSE file for GitHub" query="Generate a standard MIT License file that I can add to my GitHub repository."/>
  <Elicitation label="Deploy FastAPI to Render" query="Give me step-by-step instructions to deploy my FastAPI backend live on Render."/>
  <Elicitation label="Deploy Streamlit UI to Streamlit Cloud" query="Give me step-by-step instructions to deploy my Streamlit app live on Streamlit Cloud."/>
</ElicitationsGroup>
