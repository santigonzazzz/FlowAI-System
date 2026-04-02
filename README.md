# FlowAI — Intelligent Message Automation Engine

> A full-stack system that classifies customer messages using AI and rule-based automation, then generates context-aware responses in real time.

---

## 🚀 Overview

FlowAI simulates a real-world customer automation pipeline. When a message comes in, the system first checks a configurable rule engine for known patterns — if a match is found, a predefined response fires instantly. If no rule matches, the message is passed to **Groq's LLaMA 3.3-70B model**, which classifies the intent and generates a natural language response.

The result is a hybrid automation system that combines the **speed of deterministic rules** with the **flexibility of large language models** — without relying entirely on either.

This type of architecture is used in production customer support, sales automation, and CRM enrichment pipelines.

---

## 🧠 Features

- **AI-powered classification** — Categorizes messages as `hot`, `warm`, or `cold` based on purchase intent
- **Rule engine** — Keyword-triggered overrides that run before the AI, enabling instant deterministic responses
- **Graceful fallback** — If the Groq API is unavailable, the system falls back to keyword-based classification automatically
- **Structured outputs** — Responses from the AI are validated with Pydantic before being returned, ensuring consistent data shapes
- **In-memory store** — Messages are persisted in memory with full metadata (classification, response, rule match flag)
- **Interactive dashboard** — React frontend to send messages, visualize classification results, and browse history
- **CORS-enabled API** — Fully decoupled frontend and backend with proper CORS configuration
- **Modular architecture** — Services, routes, schemas, and models are completely separated for easy scaling

---

## 🛠 Tech Stack

### Backend
- **FastAPI** — High-performance async web framework
- **Pydantic v2** — Runtime data validation and settings management
- **Pydantic Settings** — Environment variable management via `.env`
- **Uvicorn** — ASGI server with hot reload

### AI Layer
- **Groq API** — Inference endpoint for LLaMA 3.3-70B (via OpenAI-compatible SDK)
- **OpenAI Python SDK** — Used as the HTTP client with `base_url` pointing to Groq

### Frontend
- **React 18** — Component-based UI
- **Vite** — Fast development server and bundler
- **Vanilla CSS** — Custom dark-mode design system with glassmorphism

---

## 📁 Project Structure

```
FlowAI/
├── backend/
│   ├── app/
│   │   ├── config/           # Pydantic Settings (env vars, GROQ config)
│   │   ├── models/           # Domain models (Message dataclass)
│   │   ├── routes/           # HTTP route handlers (health, messages)
│   │   ├── schemas/          # Request & response schemas
│   │   └── services/
│   │       ├── ai_service.py       # Groq integration + fallback logic
│   │       ├── rule_engine.py      # Keyword-based rule matching
│   │       └── message_service.py  # Orchestration layer
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── components/       # MessageForm, ResultCard, HistoryPanel
│       ├── services/         # api.js (fetch wrapper)
│       └── App.jsx
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- A [Groq API key](https://console.groq.com/keys)

---

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start the API server
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Dashboard available at: `http://localhost:5173`

---

## 📡 API Reference

| Method | Endpoint    | Description                          |
|--------|-------------|--------------------------------------|
| `GET`  | `/health`   | Returns `{ "status": "ok" }`         |
| `POST` | `/messages` | Process and classify a message       |
| `GET`  | `/messages` | Return all processed messages        |

### POST /messages

**Request**
```json
{
  "content": "I'd like to know your pricing plans"
}
```

**Response**
```json
{
  "id": "3f1a8c12-...",
  "content": "I'd like to know your pricing plans",
  "created_at": "2026-04-01T21:00:00Z",
  "classification": "hot",
  "response": "Great timing! Let me share our pricing right away...",
  "rule_matched": true
}
```

---

## 🔄 System Flow

```
Incoming message
       │
       ▼
 Rule Engine ──── keyword match? ────► Yes ──► Use rule (classification + response)
       │                                              │
       ▼ No                                           │
  Groq LLM ─────────────────────────────────────────►│
  (llama-3.3-70b-versatile)                          │
       │                                             │
       ▼                                             │
  Pydantic validation                                │
       │                                             │
       └──────────────────────────────────────────── ▼
                                            Merge results
                                                  │
                                                  ▼
                                         Save to store + return

  * If Groq API fails at any point → fallback to keyword classification
```

### Classification Logic

| Label  | Intent       | Example trigger                        |
|--------|--------------|----------------------------------------|
| `hot`  | Ready to buy | "price", "quote", "buy", "contract"    |
| `warm` | Interested   | "how does it work", "tell me more"     |
| `cold` | Neutral      | general greetings, off-topic messages  |

---

## 📸 Screenshots

> Dashboard — initial state

![Dashboard](docs/screenshots/dashboard.png)

> Message classified as `hot` via rule engine

![Hot classification](docs/screenshots/result_hot.png)

---

## 📌 Future Improvements

- [ ] **Database integration** — Replace in-memory store with PostgreSQL via SQLAlchemy (models and services are already structured for this)
- [ ] **Authentication** — JWT-based auth to secure the API and support multi-tenant setups
- [ ] **Rule management UI** — CRUD interface to create, edit, and prioritize rules without touching code
- [ ] **Streaming responses** — Use Groq's streaming API for faster perceived response times
- [ ] **Analytics dashboard** — Charts for classification distribution, rule match rate, and response quality over time
- [ ] **Webhook support** — Trigger external actions (CRM updates, notifications) based on classification outcome
- [ ] **Docker + CI/CD** — Containerize both services and automate deployments

---

## 👨‍💻 Author

Built as a portfolio project demonstrating real-world patterns in AI-integrated backend systems.

If you have questions or want to discuss the architecture, feel free to reach out.

---

> **Note:** The `.env` file is gitignored. Copy `.env.example` and add your own `GROQ_API_KEY` to run the AI layer. The system works without it using the keyword-based fallback.