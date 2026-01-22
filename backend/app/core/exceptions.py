"""Custom exceptions for the application."""


class HelperlyException(Exception):
    """Base exception for all Helperly exceptions."""
    
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(HelperlyException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class NotFoundError(HelperlyException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str):
        super().__init__(message, code="NOT_FOUND")


class UnauthorizedError(HelperlyException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, code="UNAUTHORIZED")


class ForbiddenError(HelperlyException):
    """Raised when user doesn't have permission for an action."""
    
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, code="FORBIDDEN")


class RateLimitError(HelperlyException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT_EXCEEDED")


class ExternalServiceError(HelperlyException):
    """Raised when an external service (OpenAI, etc.) fails."""
    
    def __init__(self, message: str, service: str = "external"):
        super().__init__(message, code="EXTERNAL_SERVICE_ERROR")
        self.service = service


class OriginNotAllowedError(ForbiddenError):
    """Raised when request origin is not in chatbox's allowed domains."""
    
    def __init__(self, origin: str):
        super().__init__(f"Origin '{origin}' is not allowed for this chatbox")
        self.origin = origin
