# Unified Inbox Agent with Persistent Memory

A runnable portfolio implementation of a unified inbox assistant. It includes a FastAPI backend, PostgreSQL-ready persistence (SQLite works out of the box), contact memory, mock Gmail/Calendar/LinkedIn adapters, reply drafting, and a Telegram webhook endpoint.

> This is a demo scaffold. External services are represented by safe mock adapters until real API credentials and OAuth setup are configured. Do not claim benchmark figures in the README as measured results; the figures in the original resume description should be independently validated.

## Requirements
- Python 3.10+
- Optional: Docker + Docker Compose for PostgreSQL
- Optional: Telegram bot token to connect a real bot

## Quick start (Windows)
```powershell
cd unified-inbox-agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/.

## Quick start (macOS/Linux)
```bash
cd unified-inbox-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## PostgreSQL (optional)
```bash
docker compose up -d db
# set DATABASE_URL in .env to postgresql+psycopg://inbox:inboxpass@localhost:5432/inboxdb
```
The app defaults to SQLite so it runs without Docker.

## Main API
- `GET /api/health`
- `GET /api/inbox` — normalized messages from mock providers
- `POST /api/draft` — draft a reply using contact memory and tone
- `GET /api/memory/{contact_key}` — retrieve persisted contact context
- `POST /api/memory` — add a memory entry
- `POST /api/telegram/webhook` — Telegram update handler (safe demo mode)
- `GET /docs` — interactive OpenAPI docs

## Integrations
`app/integrations.py` isolates provider adapters. Replace mock implementations with authorized Composio actions/MCP tool calls and official provider APIs. Keep OAuth tokens in a secret manager, never in source control. LinkedIn API access is restricted and must follow its current developer terms.
