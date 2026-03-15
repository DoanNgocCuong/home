"""
Alert Level Mapping - Default level mapping for each AlertType

Mục đích:
    Cung cấp default alert level cho mỗi AlertType để đảm bảo consistency
"""

from .alert_types import AlertType, AlertLevel

# Default level mapping for each AlertType
DEFAULT_ALERT_LEVELS = {
    # CRITICAL (10 types) - System down, data loss
    AlertType.POSTGRES_CONNECTION_FAILURE: AlertLevel.CRITICAL,
    AlertType.POSTGRES_POOL_EXHAUSTED: AlertLevel.CRITICAL,
    AlertType.REDIS_CONNECTION_FAILURE: AlertLevel.CRITICAL,
    AlertType.LLM_BOTH_FAILED: AlertLevel.CRITICAL,
    AlertType.LLM_INVALID_API_KEY: AlertLevel.CRITICAL,
    AlertType.LLM_PROVIDER_DOWN: AlertLevel.CRITICAL,
    AlertType.AUTH_BRUTE_FORCE: AlertLevel.CRITICAL,
    AlertType.DATA_LEAKAGE_DETECTED: AlertLevel.CRITICAL,
    AlertType.UNHANDLED_EXCEPTION: AlertLevel.CRITICAL,
    AlertType.APP_STARTUP_FAILURE: AlertLevel.CRITICAL,
    
    # HIGH (16 types) - Service degradation
    AlertType.LLM_TIMEOUT: AlertLevel.HIGH,
    AlertType.LLM_RATE_LIMIT: AlertLevel.HIGH,
    AlertType.WORKFLOW_EXECUTION_FAILURE: AlertLevel.HIGH,
    AlertType.WORKFLOW_TIMEOUT: AlertLevel.HIGH,
    AlertType.AGENT_EXECUTION_FAILURE: AlertLevel.HIGH,
    AlertType.AGENT_TIMEOUT: AlertLevel.HIGH,
    AlertType.REDIS_OPERATION_TIMEOUT: AlertLevel.HIGH,
    AlertType.REDIS_WRITE_FAILURE: AlertLevel.HIGH,
    AlertType.REDIS_POOL_EXHAUSTED: AlertLevel.HIGH,
    AlertType.POSTGRES_WRITE_FAILURE: AlertLevel.HIGH,
    AlertType.KAFKA_PRODUCER_FAILURE: AlertLevel.HIGH,
    AlertType.KAFKA_SEND_TIMEOUT: AlertLevel.HIGH,
    AlertType.WEBHOOK_PROCESSING_FAILURE: AlertLevel.HIGH,
    AlertType.API_REQUEST_TIMEOUT: AlertLevel.HIGH,
    AlertType.SUSPICIOUS_ACTIVITY: AlertLevel.HIGH,
    AlertType.CONTAINER_UNHEALTHY: AlertLevel.HIGH,
    
    # MEDIUM (14 types) - Feature degradation
    AlertType.LLM_TOKEN_LIMIT_EXCEEDED: AlertLevel.MEDIUM,
    AlertType.LLM_MALFORMED_RESPONSE: AlertLevel.MEDIUM,
    AlertType.LLM_CONTEXT_OVERFLOW: AlertLevel.MEDIUM,
    AlertType.LLM_STREAMING_ERROR: AlertLevel.MEDIUM,
    AlertType.WORKFLOW_STATE_ERROR: AlertLevel.MEDIUM,
    AlertType.AGENT_NOT_FOUND: AlertLevel.MEDIUM,
    AlertType.AGENT_INVALID_OUTPUT: AlertLevel.MEDIUM,
    AlertType.EXTERNAL_API_TIMEOUT: AlertLevel.MEDIUM,
    AlertType.EXTERNAL_API_ERROR: AlertLevel.MEDIUM,
    AlertType.POSTGRES_QUERY_TIMEOUT: AlertLevel.MEDIUM,
    AlertType.AUTH_FAILURE: AlertLevel.MEDIUM,
    AlertType.RATE_LIMIT_EXCEEDED: AlertLevel.MEDIUM,
    AlertType.HIGH_MEMORY_USAGE: AlertLevel.MEDIUM,
    AlertType.HIGH_CPU_USAGE: AlertLevel.MEDIUM,
    AlertType.DISK_SPACE_LOW: AlertLevel.MEDIUM,
    AlertType.HIGH_NETWORK_LATENCY: AlertLevel.MEDIUM,
    AlertType.RESPONSE_SERIALIZATION_ERROR: AlertLevel.MEDIUM,
    AlertType.RESPONSE_SIZE_EXCEEDED: AlertLevel.MEDIUM,
    
    # LOW (7 types) - Minor issues
    AlertType.INVALID_REQUEST_PAYLOAD: AlertLevel.LOW,
    AlertType.PAYLOAD_SIZE_EXCEEDED: AlertLevel.LOW,
    AlertType.INVALID_JSON_FORMAT: AlertLevel.LOW,
    AlertType.MISSING_REQUIRED_FIELDS: AlertLevel.LOW,
    AlertType.HIGH_API_RESPONSE_TIME: AlertLevel.LOW,
    AlertType.SLOW_DATABASE_QUERY: AlertLevel.LOW,
    AlertType.RABBITMQ_CONSUMER_ERROR: AlertLevel.LOW,
}


def get_default_level(alert_type: AlertType) -> AlertLevel:
    """
    Get default alert level for type
    
    Args:
        alert_type: AlertType enum
        
    Returns:
        AlertLevel: Default level for the alert type, MEDIUM if not found
    """
    return DEFAULT_ALERT_LEVELS.get(alert_type, AlertLevel.MEDIUM)

