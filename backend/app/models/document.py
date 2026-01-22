"""Document model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum
import enum

from app.core.database import Base
from sqlalchemy.orm import relationship


class DocumentType(str, enum.Enum):
    """Document source type."""
    TEXT = "text"
    URL = "url"
    FILE = "file"


class Document(Base):
    """
    Document represents an ingested piece of content.
    It can be raw text, a URL crawl result, or an uploaded file.
    """
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    chatbox_id = Column(Integer, ForeignKey("chatboxes.id"), nullable=False, index=True)
    
    # Document metadata
    source_type = Column(SQLEnum(DocumentType), nullable=False)
    source_name = Column(String(500), nullable=True)  # URL, filename, or custom name
    source_url = Column(Text, nullable=True)
    
    # Content (store original for re-processing if needed)
    raw_content = Column(Text, nullable=False)
    
    # Metadata
    file_size_bytes = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    chatbox = relationship("Chatbox", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
