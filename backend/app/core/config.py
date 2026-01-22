from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    
    # App Config
    app_name: str = "Helperly API"
    env: str = "local"  # local, staging, production
    log_level: str = "INFO"
    debug: bool = False
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Auth (MVP - API Key based)
    api_key: Optional[str] = None  # Simple API key for MVP; later: JWT
    
    # Database
    database_url: Optional[str] = None  # Supabase Postgres URL with asyncpg driver
    db_echo: bool = False
    
    # Vector Search Defaults
    vector_min_score_default: float = 0.7
    vector_top_k_default: int = 5
    
    # Upload Config
    upload_max_mb: int = 7
    
    # SaaS Plan Enforcement
    require_allowed_domains_pro: bool = True
    
    # OpenAI (optional - will use stubs if not provided)
    openai_api_key: Optional[str] = None
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"
    
    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        extra = "ignore"
        case_sensitive = False


settings = Settings()
