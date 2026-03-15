# App Core - Best Practices Template

## 📁 Folder Structure

```
app/core/
├── __init__.py
├── config.py              # Pydantic BaseSettings + environment vars
├── constants.py           # App-wide constants, enums
├── exceptions.py          # Custom exceptions (domain-agnostic)
├── enums.py              # Reusable enums
├── logging.py            # Structured logging setup (structlog)
├── telemetry.py          # OpenTelemetry setup
└── security/
    ├── __init__.py
    ├── jwt_handler.py    # JWT create/verify
    ├── password.py       # Password hashing (bcrypt)
    └── cors.py          # CORS configuration
```

---

## 1. config.py - Settings Management

```python
"""
Best Practices:
- Use Pydantic BaseSettings for type-safe environment variables
- Never hardcode secrets - load from environment
- Use SecretStr for sensitive data (masks in logs)
- Validate at startup to fail fast
"""

from functools import lru_cache
from typing import Any, Literal

from pydantic import PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings - loaded from environment variables."""

    # App
    APP_NAME: str = "MyApp"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""  # Secret
    POSTGRES_DB: str = "appdb"

    # Computed: PostgreSQL DSN
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""  # Optional

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # JWT
    JWT_SECRET_KEY: str = ""  # REQUIRED - fail if empty in prod
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External Services
    OPENAI_API_KEY: str = ""  # Secret
    STRIPE_API_KEY: str = ""  # Secret

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,  # CRITICAL: must match env vars exactly
        extra="ignore",  # Allow extra fields in .env without breaking
    )

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return bool(v)

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Fail fast if required settings are missing in production."""
        if self.ENVIRONMENT == "production":
            if not self.JWT_SECRET_KEY or len(self.JWT_SECRET_KEY) < 32:
                raise ValueError("JWT_SECRET_KEY must be set and at least 32 chars in production")
        return self


@lru_cache
def get_settings() -> Settings:
    """Cache settings - singleton pattern. Called once at startup."""
    return Settings()
```

---

## 2. constants.py - App-wide Constants

```python
"""
Best Practices:
- Use ALL_CAPS for constants
- Group related constants with comments
- Document why constants exist
"""

# ============== Pagination ==============
MAX_PAGE_SIZE: int = 100
DEFAULT_PAGE_SIZE: int = 20

# ============== Timeouts (seconds) ==============
DEFAULT_REQUEST_TIMEOUT: int = 30
LONG_REQUEST_TIMEOUT: int = 300  # For async operations
EXTERNAL_API_TIMEOUT: int = 10

# ============== Retry ==============
MAX_RETRY_ATTEMPTS: int = 3
RETRY_BACKOFF_FACTOR: float = 2.0  # Exponential backoff

# ============== Cache TTL (seconds) ==============
CACHE_TTL_SHORT: int = 60       # 1 minute
CACHE_TTL_MEDIUM: int = 3600     # 1 hour
CACHE_TTL_LONG: int = 86400     # 24 hours
CACHE_TTL_USER_PROFILE: int = 1800  # 30 minutes

# ============== Business Rules ==============
MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 128
PASSWORD_COMPLEXITY_REGEX: str = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"

MAX_FILE_SIZE_MB: int = 10
ALLOWED_FILE_EXTENSIONS: list[str] = [".jpg", ".jpeg", ".png", ".pdf"]

# ============== API Rate Limits ==============
RATE_LIMIT_AUTH: int = 5         # per minute - login attempts
RATE_LIMIT_API: int = 60        # per minute - general API
RATE_LIMIT_UPLOAD: int = 10     # per minute - file uploads
```

---

## 3. enums.py - Reusable Enums

```python
"""
Best Practices:
- Use StrEnum (Python 3.11+) for database/API compatibility
- Add docstring explaining each enum's purpose
- Use IntEnum when order matters
"""

from enum import StrEnum


class UserRole(StrEnum):
    """User roles for RBAC."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class OrderStatus(StrEnum):
    """Order lifecycle states."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(StrEnum):
    """Payment transaction states."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class LogLevel(StrEnum):
    """Standard log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class HttpMethod(StrEnum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
```

---

## 4. exceptions.py - Custom Exceptions

```python
"""
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
```

---

## 5. logging.py - Structured Logging

```python
"""
Best Practices:
- Use structlog for structured JSON logging
- Always include context (request_id, user_id)
- Use consistent event naming
- Never log sensitive data (passwords, tokens)
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from app.core.config import get_settings
from app.core.enums import LogLevel

settings = get_settings()


def add_log_level(
    logger: structlog.BoundLogger, method_name: int, event_dict: EventDict
) -> EventDict:
    """Add log level to event dict."""
    event_dict["level"] = method_name
    return event_dict


def add_timestamp(
    logger: structlog.BoundLogger, method_name: int, event_dict: EventDict
) -> EventDict:
    """Add ISO timestamp."""
    import time
    event_dict["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return event_dict


def configure_logging() -> None:
    """Initialize structured logging for the application."""

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            add_timestamp,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.ENVIRONMENT != "development"
                else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL),
    )


def get_logger(name: str | None = None, **initial_context: Any) -> structlog.BoundLogger:
    """
    Get a configured logger with optional initial context.

    Usage:
        logger = get_logger("api")
        logger.info("request_received", request_id="123")

        # With context
        logger = get_logger("api", user_id="456")
        logger.info("user_action")  # Automatically includes user_id
    """
    logger = structlog.get_logger(name)
    if initial_context:
        logger = logger.bind(**initial_context)
    return logger


# ============== Event Naming Conventions ==============

# Use these as the "event" field in logs for consistent filtering

class LogEvents:
    """Standardized event names for log aggregation."""

    # HTTP
    REQUEST_RECEIVED = "http.request.received"
    REQUEST_COMPLETED = "http.request.completed"
    REQUEST_FAILED = "http.request.failed"

    # Auth
    LOGIN_SUCCESS = "auth.login.success"
    LOGIN_FAILED = "auth.login.failed"
    LOGOUT = "auth.logout"
    TOKEN_REFRESHED = "auth.token.refreshed"

    # Business
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    ORDER_CREATED = "order.created"
    ORDER_COMPLETED = "order.completed"

    # Errors
    VALIDATION_ERROR = "error.validation"
    NOT_FOUND_ERROR = "error.not_found"
    EXTERNAL_ERROR = "error.external"
```

---

## 6. security/jwt_handler.py

```python
"""
Best Practices:
- Use strong algorithms (HS256 or RS256)
- Include expiration
- Store user context in claims
- Never store sensitive data in token
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security.password import verify_password

settings = get_settings()


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create JWT access token.

    Args:
        subject: User ID or identifier
        expires_delta: Custom expiration (default: from settings)
        additional_claims: Extra claims (e.g., role, permissions)

    Returns:
        Encoded JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta

    claims = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    if additional_claims:
        claims.update(additional_claims)

    return jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(subject: str) -> str:
    """Create JWT refresh token with longer expiration."""
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    return create_access_token(
        subject=subject,
        expires_delta=expires_delta,
        additional_claims={"type": "refresh"},
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate JWT token.

    Raises:
        UnauthorizedError: If token is invalid or expired

    Returns:
        Token payload (claims)
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except InvalidTokenError as e:
        raise UnauthorizedError(f"Invalid token: {str(e)}")


def verify_token(token: str) -> dict[str, Any]:
    """
    Verify token and return payload.

    Shorthand for decode_token with explicit error handling.
    """
    return decode_token(token)
```

---

## 7. security/password.py

```python
"""
Best Practices:
- Use bcrypt (slow hash) - resistant to rainbow tables
- Always use salt (bcrypt does this automatically)
- Never store plain passwords
- Use constant-time comparison for verification
"""

from typing import Tuple

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password (bcrypt format)
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.

    Uses bcrypt's constant-time comparison.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hash from database

    Returns:
        True if password matches
    """
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password meets security requirements.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    import re
    from app.core.constants import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"

    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must not exceed {MAX_PASSWORD_LENGTH} characters"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    return True, ""
```

---

## 8. security/cors.py

```python
"""
Best Practices:
- Restrict origins in production
- Allow credentials only when necessary
- Use specific methods and headers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the application.

    Args:
        app: FastAPI application instance
    """
    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "X-Correlation-ID",
        ],
        expose_headers=["X-Request-ID"],
        max_age=600,  # Cache preflight for 10 minutes
    )
```

---

## Usage Example

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.security.cors import configure_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    configure_logging()
    logger = get_logger("app")
    logger.info("application_starting", version=get_settings().APP_VERSION)
    yield
    # Shutdown
    logger.info("application_shutting_down")


app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    lifespan=lifespan,
)

configure_cors(app)
```
