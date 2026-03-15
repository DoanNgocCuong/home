"""
Convenience Functions - Helper functions for common alert patterns

Mục đích:
    Cung cấp convenience functions cho các alert patterns phổ biến:
    - Connection failures
    - Timeouts
    - Rate limits
"""

from typing import Dict, Any, Optional
from ..alert_types import AlertType, AlertLevel
from .send_alert_safe import send_alert_safe


def alert_connection_failure(
    service: str,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    component: str = "unknown"
) -> None:
    """
    Alert for connection failures
    
    Args:
        service: Service name (postgres, redis, kafka, etc.)
        error: Exception that occurred
        context: Additional context
        component: Component name
    """
    alert_type_map = {
        "postgres": AlertType.POSTGRES_CONNECTION_FAILURE,
        "redis": AlertType.REDIS_CONNECTION_FAILURE,
        "kafka": AlertType.KAFKA_PRODUCER_FAILURE,
    }
    
    alert_type = alert_type_map.get(service.lower(), AlertType.UNHANDLED_EXCEPTION)
    
    send_alert_safe(
        alert_type=alert_type,
        level=AlertLevel.CRITICAL,
        message=f"{service} connection failed.",
        context={
            **(context or {}),
            "error": str(error)[:500],
            "service": service
        },
        component=component
    )


def alert_timeout(
    operation: str,
    duration: float,
    threshold: float,
    context: Optional[Dict[str, Any]] = None,
    component: str = "unknown"
) -> None:
    """
    Alert for timeout operations
    
    Args:
        operation: Operation name (query, redis, llm, api, etc.)
        duration: Actual duration in seconds
        threshold: Timeout threshold in seconds
        context: Additional context
        component: Component name
    """
    alert_type_map = {
        "query": AlertType.POSTGRES_QUERY_TIMEOUT,
        "redis": AlertType.REDIS_OPERATION_TIMEOUT,
        "llm": AlertType.LLM_TIMEOUT,
        "api": AlertType.EXTERNAL_API_TIMEOUT,
        "workflow": AlertType.WORKFLOW_TIMEOUT,
        "agent": AlertType.AGENT_TIMEOUT,
    }
    
    alert_type = alert_type_map.get(operation.lower(), AlertType.UNHANDLED_EXCEPTION)
    level = AlertLevel.CRITICAL if duration > threshold * 2 else AlertLevel.MEDIUM
    
    send_alert_safe(
        alert_type=alert_type,
        level=level,
        message=f"{operation} timeout ({duration:.2f}s > {threshold}s).",
        context={
            **(context or {}),
            "operation": operation,
            "duration": f"{duration:.2f}s",
            "threshold": f"{threshold}s"
        },
        component=component
    )


def alert_rate_limit(
    service: str,
    context: Optional[Dict[str, Any]] = None,
    component: str = "unknown"
) -> None:
    """
    Alert for rate limit exceeded
    
    Args:
        service: Service name (api, llm, etc.)
        context: Additional context
        component: Component name
    """
    alert_type_map = {
        "api": AlertType.RATE_LIMIT_EXCEEDED,
        "llm": AlertType.LLM_RATE_LIMIT,
    }
    
    alert_type = alert_type_map.get(service.lower(), AlertType.RATE_LIMIT_EXCEEDED)
    
    send_alert_safe(
        alert_type=alert_type,
        level=AlertLevel.MEDIUM if service.lower() == "api" else AlertLevel.HIGH,
        message=f"{service} rate limit exceeded.",
        context={
            **(context or {}),
            "service": service
        },
        component=component
    )

