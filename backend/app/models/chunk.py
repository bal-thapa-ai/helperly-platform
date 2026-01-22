"""Chunk model with pgvector support."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Fallback if pgvector not installed (dev mode)
    Vector = None

from app.core.database import Base


class Chunk(Base):
    """
    Chunk represents a piece of a document with its embedding.
    Used for vector similarity search in RAG.
    """
    
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    chatbox_id = Column(Integer, ForeignKey("chatboxes.id"), nullable=False, index=True)
    
    # Chunk content
    content = Column(Text, nullable=False)
    
    # Position in document
    chunk_index = Column(Integer, nullable=False)
    
    # Vector embedding (1536 dimensions for text-embedding-3-small)
    # TODO: Ensure pgvector extension is enabled in Supabase:
    # CREATE EXTENSION IF NOT EXISTS vector;
    if Vector is not None:
        embedding = Column(Vector(1536), nullable=True)
    else:
        # Fallback for development without pgvector
        embedding = Column(Text, nullable=True)  # Store as JSON string
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    # Index for efficient vector similarity search
    # TODO: Create HNSW index for better performance:
    # CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
    __table_args__ = (
        Index("idx_chunks_chatbox_id", "chatbox_id"),
    )
