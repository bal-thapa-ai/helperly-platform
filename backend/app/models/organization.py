"""Organization (Tenant) model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """
    Organization represents a tenant in the SaaS.
    Each organization can have multiple chatboxes.
    """
    
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    
    # API key for simple auth (MVP)
    api_key = Column(String(255), unique=True, nullable=True, index=True)
    
    # SaaS plan: free, starter, pro, enterprise
    plan = Column(String(50), default="free", nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    chatboxes = relationship("Chatbox", back_populates="organization", cascade="all, delete-orphan")
