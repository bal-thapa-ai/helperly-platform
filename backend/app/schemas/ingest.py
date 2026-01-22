"""Ingestion schemas."""

from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class IngestTextRequest(BaseModel):
    """Request schema for ingesting raw text."""
    
    chatbox_id: int = Field(..., description="Chatbox ID to ingest into")
    text: str = Field(..., min_length=1, description="Text content to ingest")
    source_name: Optional[str] = Field(None, description="Optional name/label for this content")


class IngestTextResponse(BaseModel):
    """Response schema for text ingestion."""
    
    document_id: int
    chunks_created: int
    message: str


class IngestURLRequest(BaseModel):
    """Request schema for ingesting from URL."""
    
    chatbox_id: int = Field(..., description="Chatbox ID to ingest into")
    url: HttpUrl = Field(..., description="URL to crawl and ingest")
    depth: int = Field(1, ge=1, le=3, description="Crawl depth (1-3)")


class IngestURLResponse(BaseModel):
    """Response schema for URL ingestion."""
    
    document_id: int
    chunks_created: int
    url: str
    message: str


class UploadResponse(BaseModel):
    """Response schema for file upload."""
    
    document_id: int
    chunks_created: int
    filename: str
    file_size_bytes: int
    message: str
