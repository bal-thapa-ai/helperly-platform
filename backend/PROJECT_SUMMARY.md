# Helperly Backend - Project Summary

## Overview

A production-ready FastAPI backend for Helperly, a SaaS platform that enables organizations to create AI-powered chatboxes with RAG (Retrieval-Augmented Generation) capabilities.

## Key Features Implemented

### ✅ Core Infrastructure
- **FastAPI Application** with proper lifecycle management
- **Structured Logging** with request ID correlation
- **Global Exception Handling** with consistent error responses
- **Request Tracking Middleware** for observability
- **CORS Configuration** for cross-origin requests
- **Pydantic Settings** for environment-based configuration

### ✅ Database Layer
- **SQLAlchemy 2.0** with async support (asyncpg)
- **PostgreSQL + pgvector** for vector similarity search
- **Models**: Organization, Chatbox, Document, Chunk
- **Repository Pattern** for clean data access
- **Automatic Schema Creation** on startup

### ✅ SaaS Multi-tenancy
- **Organization-based** tenant isolation
- **Chatbox Management** (CRUD operations)
- **Plan-based Features**:
  - Free/Starter: Optional domain validation
  - Pro/Enterprise: Required domain validation
- **Origin Validation** for embedded widget security

### ✅ RAG Pipeline
- **Document Ingestion**:
  - Raw text ingestion
  - URL crawling (basic, TODO: robust crawler)
  - File upload (TXT, PDF placeholder)
- **Text Chunking**: Character-based with overlap
- **Embeddings**: OpenAI integration with stub fallback
- **Vector Search**: pgvector cosine similarity
- **LLM Generation**: OpenAI chat completions with stub fallback

### ✅ API Endpoints

#### Health
- `GET /health` - Application and database health check

#### Chatboxes
- `POST /v1/chatboxes` - Create chatbox
- `GET /v1/chatboxes` - List chatboxes
- `GET /v1/chatboxes/{id}` - Get chatbox
- `PATCH /v1/chatboxes/{id}` - Update chatbox

#### Ingestion
- `POST /v1/ingest/text` - Ingest raw text
- `POST /v1/ingest/url` - Ingest from URL
- `POST /v1/ingest/upload` - Upload file

#### Query
- `POST /v1/query` - Query chatbox with RAG

### ✅ Authentication
- **MVP**: Simple API key authentication
- **Structure**: Ready for JWT migration
- **Dev Mode**: Optional auth (disable with empty API_KEY)

### ✅ Development Experience
- **Stub Implementations**: Run without database or OpenAI
- **Auto-generated Docs**: Swagger UI at `/docs`
- **Type Safety**: Full Pydantic validation
- **Clear Error Messages**: Helpful validation errors

### ✅ Production Ready
- **Exception Handling**: Custom exceptions with proper HTTP codes
- **Request Logging**: Structured JSON logs with metadata
- **Configuration Management**: Environment-based settings
- **Database Pooling**: Connection pool with health checks
- **CORS Security**: Configurable allowed origins

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py          # Dependency injection
│   │   └── routes/                  # API endpoints
│   │       ├── health.py
│   │       ├── chatboxes.py
│   │       ├── ingest.py
│   │       └── query.py
│   ├── core/
│   │   ├── config.py                # Settings & configuration
│   │   ├── database.py              # DB connection & session
│   │   ├── exceptions.py            # Custom exceptions
│   │   ├── exception_handlers.py    # Global error handlers
│   │   ├── logging_config.py        # Structured logging
│   │   └── middleware.py            # Request tracking
│   ├── models/                      # SQLAlchemy ORM models
│   │   ├── organization.py
│   │   ├── chatbox.py
│   │   ├── document.py
│   │   └── chunk.py
│   ├── repositories/                # Data access layer
│   │   ├── chatbox_repository.py
│   │   ├── document_repository.py
│   │   └── chunk_repository.py
│   ├── schemas/                     # Pydantic request/response schemas
│   │   ├── chatbox.py
│   │   ├── ingest.py
│   │   ├── query.py
│   │   └── health.py
│   ├── services/                    # Business logic
│   │   ├── embedding_service.py     # OpenAI embeddings + stub
│   │   ├── llm_service.py           # OpenAI chat + stub
│   │   ├── chunking_service.py      # Text chunking
│   │   ├── ingestion_service.py     # Document processing
│   │   └── query_service.py         # RAG query pipeline
│   └── main.py                      # FastAPI application
├── scripts/
│   ├── init_db.py                   # Database initialization
│   └── test_api.py                  # API testing script
├── .env.example                     # Environment template
├── .gitignore
├── requirements.txt
├── README.md                        # Full documentation
├── QUICKSTART.md                    # Quick start guide
└── PROJECT_SUMMARY.md               # This file
```

## Technology Stack

### Core
- **Python 3.11+**
- **FastAPI 0.109.0** - Modern async web framework
- **Uvicorn 0.27.0** - ASGI server
- **Pydantic 2.5.3** - Data validation

### Database
- **SQLAlchemy 2.0.25** - ORM with async support
- **asyncpg 0.29.0** - PostgreSQL async driver
- **pgvector 0.2.4** - Vector similarity extension

### AI/ML
- **OpenAI 1.10.0** - Embeddings and LLM (optional)
- **NumPy 1.26.3** - Numerical operations

### Utilities
- **Requests 2.31.0** - HTTP client
- **BeautifulSoup4 4.12.3** - HTML parsing

## Configuration

### Environment Variables

All configuration via `.env` file:

```env
# Application
APP_NAME=Helperly API
ENV=local
LOG_LEVEL=INFO

# Auth
API_KEY=your-secret-key

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# OpenAI (optional)
OPENAI_API_KEY=sk-...

# Vector Search
VECTOR_MIN_SCORE_DEFAULT=0.7
VECTOR_TOP_K_DEFAULT=5

# Uploads
UPLOAD_MAX_MB=7
```

## Running the Application

### Development Mode (No Dependencies)

```bash
# Install packages
pip install -r requirements.txt

# Create minimal .env
echo "API_KEY=" > .env

# Start server
uvicorn app.main:app --reload
```

### Full Setup (With Database)

```bash
# Install packages
pip install -r requirements.txt

# Configure .env with DATABASE_URL

# Initialize database
python scripts/init_db.py

# Start server
uvicorn app.main:app --reload
```

### Testing

```bash
# Run test suite
python scripts/test_api.py
```

## API Usage Examples

### Create Chatbox
```bash
curl -X POST http://localhost:8000/v1/chatboxes \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Chatbox", "enforce_allowed_domains": false}'
```

### Ingest Text
```bash
curl -X POST http://localhost:8000/v1/ingest/text \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"chatbox_id": 1, "text": "Your content here"}'
```

### Query
```bash
curl -X POST http://localhost:8000/v1/query \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"chatbox_id": 1, "question": "What is...?"}'
```

## Design Decisions

### 1. Repository Pattern
- Separates data access from business logic
- Makes testing easier (can mock repositories)
- Provides clean abstraction over SQLAlchemy

### 2. Service Layer
- Encapsulates business logic
- Reusable across different endpoints
- Singleton services for stateless operations

### 3. Dependency Injection
- FastAPI's native DI system
- Per-request database sessions
- Singleton services for efficiency

### 4. Stub Implementations
- Allows development without external APIs
- Deterministic embeddings for testing
- Clear dev/prod separation

### 5. Structured Logging
- JSON logs in production
- Human-readable in development
- Request ID correlation for tracing

### 6. Exception Handling
- Custom exception hierarchy
- Consistent error responses
- Proper HTTP status codes

## TODO / Future Enhancements

### High Priority
- [ ] **JWT Authentication** - Replace API key with JWT tokens
- [ ] **Alembic Migrations** - Database schema versioning
- [ ] **PDF Extraction** - Implement PyPDF2/pdfplumber
- [ ] **Rate Limiting** - Per-organization limits
- [ ] **Caching** - Redis for embeddings/queries

### Medium Priority
- [ ] **Advanced Chunking** - Sentence-aware, semantic chunking
- [ ] **Robust Crawler** - Multi-page, respect robots.txt
- [ ] **Background Jobs** - Celery for async ingestion
- [ ] **Monitoring** - Prometheus metrics, Sentry
- [ ] **Testing** - Unit and integration tests

### Low Priority
- [ ] **DOCX/XLSX Support** - Additional file formats
- [ ] **Webhook Notifications** - Event callbacks
- [ ] **Admin Dashboard** - Management UI
- [ ] **Usage Analytics** - Query tracking, insights

## Security Considerations

### Implemented
✅ API key authentication
✅ Origin validation per chatbox
✅ Input validation with Pydantic
✅ SQL injection protection (SQLAlchemy)
✅ File size limits
✅ CORS configuration

### TODO
- [ ] Rate limiting per organization
- [ ] JWT with refresh tokens
- [ ] Request signing for webhooks
- [ ] Audit logging
- [ ] Data encryption at rest

## Performance Considerations

### Current
- Async I/O throughout
- Database connection pooling
- Vector similarity with pgvector
- Efficient chunking algorithm

### Future Optimizations
- [ ] HNSW index for vector search
- [ ] Embedding caching
- [ ] Query result caching
- [ ] Background processing for ingestion
- [ ] CDN for static assets

## Deployment Recommendations

### Infrastructure
- **Compute**: Cloud VM, Kubernetes, or serverless (AWS Lambda, Google Cloud Run)
- **Database**: Supabase (managed Postgres + pgvector)
- **Secrets**: AWS Secrets Manager, Azure Key Vault, or similar
- **Monitoring**: Datadog, New Relic, or CloudWatch

### Environment Setup
1. Set `ENV=production`
2. Use strong `API_KEY` (or migrate to JWT)
3. Configure `DATABASE_URL` with production database
4. Add `OPENAI_API_KEY` for real embeddings/LLM
5. Set appropriate `CORS_ORIGINS`
6. Enable pgvector and create HNSW index
7. Set up logging aggregation (ELK, CloudWatch Logs)

### Scaling
- Horizontal: Multiple Uvicorn workers
- Vertical: Increase worker count per instance
- Database: Read replicas for queries
- Caching: Redis for frequently accessed data

## Support & Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Full Docs**: See `README.md`
- **API Docs**: http://localhost:8000/docs (when running)
- **Code Comments**: Extensive inline documentation

## License

Proprietary - All rights reserved

---

**Built with ❤️ for production use**
