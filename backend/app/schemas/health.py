"""Health check schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for health check."""
    
    status: str
    database: str
    message: str
