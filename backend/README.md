# Helperly Backend

Production-ready FastAPI backend for Helperly - an AI-powered chatbox SaaS platform with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🚀 **FastAPI** - Modern, fast web framework with automatic API docs
- 🗄️ **PostgreSQL + pgvector** - Vector database for semantic search
- 🤖 **RAG Pipeline** - Document ingestion, chunking, embedding, and retrieval
- 🔐 **API Key Auth** - Simple authentication (JWT ready for future)
- 🏢 **Multi-tenant** - Organization-based isolation
- 📦 **Chatboxes** - Create multiple AI chatboxes per organization
- 🌐 **Origin Validation** - Domain-based access control per plan
- 📝 **Structured Logging** - Request tracking with correlation IDs
- 🛡️ **Error Handling** - Consistent error responses with custom exceptions
- 🔌 **Pluggable Services** - Stub mode for dev without external APIs

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL with pgvector extension (or Supabase)
- (Optional) OpenAI API key

### Installation

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` with your settings (see Configuration section below)

6. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

#### Required for Production:
- `DATABASE_URL` - PostgreSQL connection string with asyncpg driver
- `API_KEY` - Secret key for API authentication

#### Optional (Dev Mode Works Without):
- `OPENAI_API_KEY` - For production embeddings and LLM
  - Without this, the system uses stub implementations
  - Get key from: https://platform.openai.com/api-keys

#### Other Settings:
- `ENV` - Environment: local, staging, production
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)
- `UPLOAD_MAX_MB` - Max file upload size (default: 7MB)
- `VECTOR_TOP_K_DEFAULT` - Number of chunks to retrieve (default: 5)
- `VECTOR_MIN_SCORE_DEFAULT` - Minimum similarity score (default: 0.7)

### Database Setup

#### Using Supabase (Recommended):

1. Create a Supabase project at https://supabase.com
2. Enable pgvector extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Copy connection string from Supabase dashboard
4. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres
   ```

#### Using Local PostgreSQL:

1. Install PostgreSQL and pgvector
2. Create database:
   ```sql
   CREATE DATABASE helperly;
   CREATE EXTENSION vector;
   ```
3. Set `DATABASE_URL` in `.env`

## API Endpoints

### Health
- `GET /health` - Health check with database status

### Chatboxes
- `POST /v1/chatboxes` - Create a chatbox
- `GET /v1/chatboxes` - List chatboxes
- `GET /v1/chatboxes/{id}` - Get chatbox details
- `PATCH /v1/chatboxes/{id}` - Update chatbox

### Ingestion
- `POST /v1/ingest/text` - Ingest raw text
- `POST /v1/ingest/url` - Ingest from URL
- `POST /v1/ingest/upload` - Upload file (txt, pdf)

### Query
- `POST /v1/query` - Query chatbox with RAG

## Architecture

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py      # Shared dependencies & DI
│   │   └── routes/              # API endpoints
│   │       ├── health.py
│   │       ├── chatboxes.py
│   │       ├── ingest.py
│   │       └── query.py
│   ├── core/
│   │   ├── config.py            # Settings management
│   │   ├── database.py          # DB connection & session
│   │   ├── exceptions.py        # Custom exceptions
│   │   ├── exception_handlers.py # Global error handlers
│   │   ├── logging_config.py    # Structured logging
│   │   └── middleware.py        # Request tracking
│   ├── models/                  # SQLAlchemy models
│   │   ├── organization.py
│   │   ├── chatbox.py
│   │   ├── document.py
│   │   └── chunk.py
│   ├── repositories/            # Data access layer
│   │   ├── chatbox_repository.py
│   │   ├── document_repository.py
│   │   └── chunk_repository.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── chatbox.py
│   │   ├── ingest.py
│   │   ├── query.py
│   │   └── health.py
│   ├── services/                # Business logic
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── chunking_service.py
│   │   ├── ingestion_service.py
│   │   └── query_service.py
│   └── main.py                  # FastAPI app
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Development Mode

The backend can run without external dependencies:

- **No Database**: Health check returns "not_configured" status
- **No OpenAI Key**: Uses stub embeddings and LLM responses
- **No Auth**: Set `API_KEY=` (empty) to disable authentication

This allows rapid development and testing without setup overhead.

## Production Deployment

### Pre-deployment Checklist:

1. ✅ Set `ENV=production` in `.env`
2. ✅ Configure `DATABASE_URL` with production database
3. ✅ Set strong `API_KEY`
4. ✅ Add `OPENAI_API_KEY` for real embeddings/LLM
5. ✅ Configure `CORS_ORIGINS` with your frontend domains
6. ✅ Set `LOG_LEVEL=INFO` or `WARNING`
7. ✅ Enable pgvector extension in database
8. ✅ Create HNSW index for vector search performance:
   ```sql
   CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
   ```

### Run with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## TODO / Future Enhancements

- [ ] **JWT Authentication** - Replace API key with JWT tokens
- [ ] **Alembic Migrations** - Database schema versioning
- [ ] **PDF Extraction** - Implement PyPDF2/pdfplumber for PDF support
- [ ] **Advanced Chunking** - Sentence-aware and semantic chunking
- [ ] **Robust Web Crawler** - Multi-page crawling with depth support
- [ ] **Rate Limiting** - Per-user/organization rate limits
- [ ] **Caching** - Redis for embeddings and query results
- [ ] **Background Jobs** - Celery for async ingestion
- [ ] **Monitoring** - Prometheus metrics and Sentry error tracking
- [ ] **Testing** - Comprehensive unit and integration tests

## Support

For issues or questions, please open an issue on the repository.

## License

Proprietary - All rights reserved
