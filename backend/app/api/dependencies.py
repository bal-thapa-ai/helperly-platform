"""Shared dependencies for API routes."""

from typing import Optional
from fastapi import Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.repositories.chatbox_repository import ChatboxRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.chunking_service import ChunkingService
from app.services.ingestion_service import IngestionService
from app.services.query_service import QueryService


# Service singletons (initialized once)
_embedding_service: Optional[EmbeddingService] = None
_llm_service: Optional[LLMService] = None
_chunking_service: Optional[ChunkingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get singleton embedding service."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def get_llm_service() -> LLMService:
    """Get singleton LLM service."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_chunking_service() -> ChunkingService:
    """Get singleton chunking service."""
    global _chunking_service
    if _chunking_service is None:
        _chunking_service = ChunkingService()
    return _chunking_service


# Repository factories (per-request, depend on DB session)
def get_chatbox_repo(db: AsyncSession = Depends(get_db)) -> ChatboxRepository:
    """Get chatbox repository."""
    return ChatboxRepository(db)


def get_document_repo(db: AsyncSession = Depends(get_db)) -> DocumentRepository:
    """Get document repository."""
    return DocumentRepository(db)


def get_chunk_repo(db: AsyncSession = Depends(get_db)) -> ChunkRepository:
    """Get chunk repository."""
    return ChunkRepository(db)


# Service factories (per-request, depend on repos)
def get_ingestion_service(
    document_repo: DocumentRepository = Depends(get_document_repo),
    chunk_repo: ChunkRepository = Depends(get_chunk_repo),
    chunking_service: ChunkingService = Depends(get_chunking_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> IngestionService:
    """Get ingestion service."""
    return IngestionService(
        document_repo=document_repo,
        chunk_repo=chunk_repo,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
    )


def get_query_service(
    chunk_repo: ChunkRepository = Depends(get_chunk_repo),
    document_repo: DocumentRepository = Depends(get_document_repo),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    llm_service: LLMService = Depends(get_llm_service),
) -> QueryService:
    """Get query service."""
    return QueryService(
        chunk_repo=chunk_repo,
        document_repo=document_repo,
        embedding_service=embedding_service,
        llm_service=llm_service,
    )


# Auth dependency (MVP - simple API key)
async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> None:
    """
    Verify API key from header.
    
    TODO: Replace with JWT authentication later.
    For MVP, simple API key check (if configured).
    """
    # If no API key is configured, allow all requests (dev mode)
    if not settings.api_key:
        return
    
    # Verify API key matches
    if x_api_key != settings.api_key:
        raise UnauthorizedError("Invalid or missing API key")


# Mock organization ID for MVP (later: extract from JWT)
def get_current_org_id() -> int:
    """
    Get current organization ID.
    
    TODO: Extract from JWT token later.
    For MVP, return fixed org_id=1.
    """
    return 1
