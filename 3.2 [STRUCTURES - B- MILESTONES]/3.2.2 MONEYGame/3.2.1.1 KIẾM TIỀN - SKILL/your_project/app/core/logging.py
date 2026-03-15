"""
Structured logging setup.

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
