"""Query schemas."""

from typing import Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request schema for querying a chatbox."""
    
    chatbox_id: int = Field(..., description="Chatbox ID to query")
    question: str = Field(..., min_length=1, description="User question")
    document_id: Optional[int] = Field(None, description="Optional: filter to specific document")
    top_k: Optional[int] = Field(None, ge=1, le=20, description="Number of chunks to retrieve")
    origin: Optional[str] = Field(None, description="Request origin for validation")


class SourceChunk(BaseModel):
    """A source chunk returned with the answer."""
    
    document_id: int
    chunk_id: int
    content: str
    score: float
    source_name: Optional[str]


class QueryResponse(BaseModel):
    """Response schema for query."""
    
    answer: str
    sources: list[SourceChunk]
    chatbox_id: int
