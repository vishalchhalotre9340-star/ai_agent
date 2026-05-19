# Agentic Chatbot

This repository contains a FastAPI backend (`main.py`) and a Streamlit frontend (`frontend.py`) for an AI agent powered by `ai_agent.py`.

## Deploy-Ready Files

- `requirements.txt` — Python dependencies for deployment
- `Dockerfile` — Container image for backend and frontend
- `docker-compose.yml` — Local development and deployment setup
- `.env.example` — Environment variable template
- `.dockerignore` — Docker ignore rules

## Setup

1. Copy `.env.example` to `.env`
2. Add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Local Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Run the frontend:

```bash
streamlit run frontend.py
```

Then visit:

- Backend: `http://127.0.0.1:8000/chat`
- Frontend: `http://127.0.0.1:8501`

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

The frontend will be available at `http://127.0.0.1:8501` and the backend at `http://127.0.0.1:8000`.

## Notes

- Use `BACKEND_URL` environment variable to configure the frontend backend endpoint.
- `ALLOWED_ORIGINS` is configurable for CORS in the backend.
"# ai-agent-for-guidance" 
