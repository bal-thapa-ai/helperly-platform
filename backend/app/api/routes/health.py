"""Health check endpoint."""

from fastapi import APIRouter

from app.core.database import check_db_health
from app.schemas.health import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Checks:
    - Application status
    - Database connectivity (if configured)
    """
    db_status = "not_configured"
    
    try:
        db_healthy = await check_db_health()
        db_status = "healthy" if db_healthy else "unhealthy"
    except Exception:
        db_status = "not_configured"
    
    overall_status = "healthy" if db_status in ["healthy", "not_configured"] else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        message="Helperly API is running",
    )

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}
