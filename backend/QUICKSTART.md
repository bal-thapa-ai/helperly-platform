# Helperly Backend - Quick Start Guide

Get the Helperly backend running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- (Optional) PostgreSQL with pgvector or Supabase account
- (Optional) OpenAI API key

## Installation Steps

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

Copy the example environment file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**For Quick Testing (No Database):**

Edit `.env` and set:
```env
DATABASE_URL=
API_KEY=
```

This runs in dev mode with stub implementations!

**For Full Setup (With Database):**

Edit `.env` and configure:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
API_KEY=your-secret-key
OPENAI_API_KEY=sk-your-openai-key  # Optional
```

### 6. Initialize Database (If Using Database)

```bash
python scripts/init_db.py
```

This creates the schema and an initial organization.

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

The server will start at http://localhost:8000

## Verify Installation

### Check Health Endpoint

Open http://localhost:8000/health in your browser or:

```bash
curl http://localhost:8000/health
```

### View API Documentation

Open http://localhost:8000/docs for interactive Swagger UI

### Run Test Suite (Optional)

```bash
python scripts/test_api.py
```

## Quick API Examples

### 1. Create a Chatbox

```bash
curl -X POST http://localhost:8000/v1/chatboxes \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Chatbox",
    "description": "A test chatbox",
    "allowed_domains": ["https://example.com"],
    "enforce_allowed_domains": false
  }'
```

### 2. Ingest Text

```bash
curl -X POST http://localhost:8000/v1/ingest/text \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "chatbox_id": 1,
    "text": "FastAPI is a modern Python web framework for building APIs.",
    "source_name": "FastAPI Info"
  }'
```

### 3. Query the Chatbox

```bash
curl -X POST http://localhost:8000/v1/query \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "chatbox_id": 1,
    "question": "What is FastAPI?",
    "origin": "https://example.com"
  }'
```

## Development Mode Features

When running without external dependencies:

✅ **No Database Required** - Health check returns "not_configured"
✅ **No OpenAI Key Required** - Uses stub embeddings and LLM responses
✅ **No Auth Required** - Set `API_KEY=` (empty) to disable

Perfect for rapid development and testing!

## Troubleshooting

### Import Errors

Make sure virtual environment is activated:
```bash
.venv\Scripts\activate  # Windows
```

### Port Already in Use

Change the port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Database Connection Errors

- Verify `DATABASE_URL` in `.env`
- Check database is running
- Ensure pgvector extension is enabled

### OpenAI Errors

- Verify `OPENAI_API_KEY` in `.env`
- Or leave empty to use stub mode

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the API at http://localhost:8000/docs
3. Check out the architecture and code structure
4. Customize for your use case

## Support

For issues or questions, refer to the main README.md or open an issue.

Happy coding! 🚀
