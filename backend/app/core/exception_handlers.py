"""Global exception handlers for consistent error responses."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    HelperlyException,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    RateLimitError,
    ExternalServiceError,
)
from app.core.logging_config import request_id_ctx, get_logger


logger = get_logger(__name__)


def create_error_response(
    status_code: int,
    error_code: str,
    message: str,
    request_id: str | None = None,
) -> JSONResponse:
    """Create a standardized error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
                "request_id": request_id or request_id_ctx.get(""),
            }
        },
    )


async def helperly_exception_handler(request: Request, exc: HelperlyException) -> JSONResponse:
    """Handle custom Helperly exceptions."""
    
    status_map = {
        "VALIDATION_ERROR": status.HTTP_400_BAD_REQUEST,
        "NOT_FOUND": status.HTTP_404_NOT_FOUND,
        "UNAUTHORIZED": status.HTTP_401_UNAUTHORIZED,
        "FORBIDDEN": status.HTTP_403_FORBIDDEN,
        "RATE_LIMIT_EXCEEDED": status.HTTP_429_TOO_MANY_REQUESTS,
        "EXTERNAL_SERVICE_ERROR": status.HTTP_502_BAD_GATEWAY,
    }
    
    status_code = status_map.get(exc.code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Log the exception
    if status_code >= 500:
        logger.exception(
            f"Server error: {exc.message}",
            extra={"error_code": exc.code}
        )
    else:
        logger.warning(
            f"Client error: {exc.message}",
            extra={"error_code": exc.code}
        )
    
    return create_error_response(
        status_code=status_code,
        error_code=exc.code,
        message=exc.message,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path}
    )
    
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        message=f"Request validation failed: {exc.errors()}",
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle Starlette HTTP exceptions."""
    
    return create_error_response(
        status_code=exc.status_code,
        error_code="HTTP_ERROR",
        message=exc.detail,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions."""
    
    logger.exception(
        f"Unhandled exception: {str(exc)}",
        extra={"path": request.url.path}
    )
    
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_ERROR",
        message="An internal error occurred. Please try again later.",
    )
