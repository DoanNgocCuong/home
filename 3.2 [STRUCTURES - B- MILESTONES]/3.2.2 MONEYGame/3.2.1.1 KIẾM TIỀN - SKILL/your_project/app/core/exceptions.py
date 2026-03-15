"""
Custom exceptions (domain-agnostic).

Best Practices:
- Create base exception class for app-wide handling
- Use semantic exception names (self-documenting)
- Include context (user_id, request_id) for debugging
- Use HTTP status codes as exception codes
"""

from typing import Any


class AppException(Exception):
    """
    Base exception for all application errors.

    Attributes:
        message: Human-readable error message
        code: Error code for programmatic handling
        status_code: HTTP status code
        details: Additional context for debugging
    """

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details,
        }


# ============== Validation Errors ==============

class ValidationError(AppException):
    """Invalid input data."""
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400, details=details)


class UnauthorizedError(AppException):
    """Authentication failed or missing."""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, code="UNAUTHORIZED", status_code=401)


class ForbiddenError(AppException):
    """Authenticated but not authorized."""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, code="FORBIDDEN", status_code=403)


# ============== Not Found Errors ==============

class NotFoundError(AppException):
    """Resource not found."""
    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": str(identifier)},
        )


# ============== Business Logic Errors ==============

class ConflictError(AppException):
    """Resource conflict (e.g., duplicate email)."""
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, code="CONFLICT", status_code=409, details=details)


class RateLimitError(AppException):
    """Too many requests."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT_EXCEEDED", status_code=429)


# ============== External Service Errors ==============

class ExternalServiceError(AppException):
    """Third-party service unavailable."""
    def __init__(self, service: str, message: str = "Service unavailable"):
        super().__init__(
            message=f"{service}: {message}",
            code="EXTERNAL_SERVICE_ERROR",
            status_code=503,
            details={"service": service},
        )
