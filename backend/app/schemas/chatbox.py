"""Chatbox schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatboxCreate(BaseModel):
    """Request schema for creating a chatbox."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Chatbox name")
    description: Optional[str] = Field(None, description="Optional description")
    allowed_domains: Optional[list[str]] = Field(
        None,
        description="List of allowed origins/domains (e.g., https://example.com)"
    )
    enforce_allowed_domains: bool = Field(
        False,
        description="Whether to enforce domain validation (required for Pro+ plans)"
    )


class ChatboxUpdate(BaseModel):
    """Request schema for updating a chatbox."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    allowed_domains: Optional[list[str]] = None
    enforce_allowed_domains: Optional[bool] = None


class ChatboxResponse(BaseModel):
    """Response schema for a single chatbox."""
    
    id: int
    organization_id: int
    name: str
    description: Optional[str]
    allowed_domains: Optional[list[str]]
    enforce_allowed_domains: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatboxListResponse(BaseModel):
    """Response schema for listing chatboxes."""
    
    chatboxes: list[ChatboxResponse]
    total: int
