# 🚀 Get Started with Helperly Backend

Welcome! This guide will get you up and running in **5 minutes**.

## Prerequisites

- Python 3.11+ installed
- That's it! (Database and OpenAI are optional)

## Quick Start (No Database)

Perfect for testing and development:

### 1. Install Dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Create Minimal Config

Create a `.env` file:

```env
API_KEY=
```

That's it! Empty API_KEY means no auth required.

### 3. Start Server

```bash
uvicorn app.main:app --reload
```

### 4. Test It

Open http://localhost:8000/docs in your browser!

Try the health endpoint: http://localhost:8000/health

## Full Setup (With Database)

For production-like setup with real data persistence:

### 1. Setup Database

**Option A: Supabase (Recommended)**
1. Create account at https://supabase.com
2. Create new project
3. Enable pgvector:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. Copy connection string

**Option B: Local PostgreSQL**
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE helperly;
   CREATE EXTENSION vector;
   ```

### 2. Configure

Create `.env` file:

```env
API_KEY=dev-api-key-12345
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
OPENAI_API_KEY=sk-your-key-here  # Optional
```

### 3. Initialize Database

```bash
python scripts/init_db.py
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

### 5. Test

```bash
python scripts/test_api.py
```

## What's Next?

### Explore the API

- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Endpoints**: See README.md

### Try the API

Create a chatbox:
```bash
curl -X POST http://localhost:8000/v1/chatboxes \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Chatbox", "enforce_allowed_domains": false}'
```

Ingest some text:
```bash
curl -X POST http://localhost:8000/v1/ingest/text \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"chatbox_id": 1, "text": "FastAPI is awesome!", "source_name": "Test"}'
```

Query it:
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"chatbox_id": 1, "question": "What is FastAPI?"}'
```

### Read the Docs

- **QUICKSTART.md** - Detailed setup guide
- **README.md** - Full documentation
- **PROJECT_SUMMARY.md** - Architecture overview
- **IMPLEMENTATION_CHECKLIST.md** - What's implemented

## Troubleshooting

### "Module not found"
Make sure virtual environment is activated:
```bash
.venv\Scripts\activate
```

### "Port already in use"
Change the port:
```bash
uvicorn app.main:app --reload --port 8001
```

### "Database connection failed"
- Check DATABASE_URL in .env
- Or leave it empty to run without database

## Need Help?

Check the documentation files or open an issue!

---

**Happy coding! 🎉**
