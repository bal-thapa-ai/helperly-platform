"""Chatbox (Brain) model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base


class Chatbox(Base):
    """
    Chatbox (aka Brain) belongs to an organization.
    It contains documents and has allowed domains for origin validation.
    """
    
    __tablename__ = "chatboxes"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Allowed domains/origins for embedding (e.g., ["https://example.com", "https://app.example.com"])
    # ARRAY type works with PostgreSQL; for other DBs, use JSON
    allowed_domains = Column(ARRAY(String), nullable=True)
    
    # Plan-level settings
    # Free/Starter: allowed_domains is optional
    # Pro/Enterprise: allowed_domains is required (enforced by validation)
    enforce_allowed_domains = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="chatboxes")
    documents = relationship("Document", back_populates="chatbox", cascade="all, delete-orphan")
