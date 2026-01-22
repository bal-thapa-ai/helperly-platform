"""Middleware for request tracking and logging."""

import uuid
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import request_id_ctx, get_logger


logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    - Generates a unique request_id for each request
    - Stores it in context for structured logging
    - Includes it in response headers
    - Logs request/response metadata
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Store in context for logging
        request_id_ctx.set(request_id)
        
        # Start timer
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as exc:
            logger.exception(
                f"Unhandled exception during request",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                }
            )
            raise
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
        )
        
        # Add request_id to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
