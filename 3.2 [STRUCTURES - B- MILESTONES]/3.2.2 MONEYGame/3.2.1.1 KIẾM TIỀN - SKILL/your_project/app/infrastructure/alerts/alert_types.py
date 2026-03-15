"""
Alert Types - Enum định nghĩa các loại alert và mức độ

Mục đích:
    Định nghĩa các enum cho alert levels và alert types để đảm bảo type safety
    và consistency trong toàn bộ hệ thống alerting.
"""

from enum import Enum


class AlertLevel(str, Enum):
    """
    Mức độ nghiêm trọng của alert
    
    - CRITICAL: Hệ thống down, data loss - Bắn ngay lập tức
    - HIGH: Service degradation - Bắn trong vòng 1 phút
    - MEDIUM: Feature degradation - Bắn trong vòng 5 phút
    - LOW: Minor issues - Bắn summary (hourly/daily)
    """
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertType(str, Enum):
    """
    Complete MECE alert type registry
    
    47 alert types organized by layer:
    - Input Layer: 7 types
    - Processing Layer: 17 types
    - Output Layer: 7 types
    - Dependency Layer: 7 types
    - Infrastructure Layer: 5 types
    - Security Layer: 3 types
    - Operational Layer: 2 types
    """
    
    # ============================================
    # LAYER 1: INPUT LAYER (7 types)
    # ============================================
    API_REQUEST_TIMEOUT = "api_request_timeout"
    INVALID_REQUEST_PAYLOAD = "invalid_request_payload"
    AUTH_FAILURE = "auth_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    PAYLOAD_SIZE_EXCEEDED = "payload_size_exceeded"
    INVALID_JSON_FORMAT = "invalid_json_format"
    MISSING_REQUIRED_FIELDS = "missing_required_fields"
    
    # ============================================
    # LAYER 2: PROCESSING LAYER (17 types)
    # ============================================
    
    # 2A. LLM Processing (9 types)
    LLM_TIMEOUT = "llm_timeout"
    LLM_BOTH_FAILED = "llm_both_failed"
    LLM_RATE_LIMIT = "llm_rate_limit"
    LLM_TOKEN_LIMIT_EXCEEDED = "llm_token_limit_exceeded"
    LLM_INVALID_API_KEY = "llm_invalid_api_key"
    LLM_MALFORMED_RESPONSE = "llm_malformed_response"
    LLM_PROVIDER_DOWN = "llm_provider_down"
    LLM_CONTEXT_OVERFLOW = "llm_context_overflow"
    LLM_STREAMING_ERROR = "llm_streaming_error"
    
    # 2B. Workflow Processing (4 types + 1 scenario-specific)
    WORKFLOW_EXECUTION_FAILURE = "workflow_execution_failure"
    WORKFLOW_TIMEOUT = "workflow_timeout"
    WORKFLOW_STATE_ERROR = "workflow_state_error"
    WEBHOOK_PROCESSING_FAILURE = "webhook_processing_failure"
    SCENARIO_VALIDATION_ERROR = "scenario_validation_error"
    
    # 2C. Agent Processing (4 types)
    AGENT_EXECUTION_FAILURE = "agent_execution_failure"
    AGENT_TIMEOUT = "agent_timeout"
    AGENT_NOT_FOUND = "agent_not_found"
    AGENT_INVALID_OUTPUT = "agent_invalid_output"
    
    # ============================================
    # LAYER 3: OUTPUT LAYER (7 types)
    # ============================================
    REDIS_OPERATION_TIMEOUT = "redis_operation_timeout"
    REDIS_WRITE_FAILURE = "redis_write_failure"
    POSTGRES_WRITE_FAILURE = "postgres_write_failure"
    KAFKA_PRODUCER_FAILURE = "kafka_producer_failure"
    KAFKA_SEND_TIMEOUT = "kafka_send_timeout"
    RESPONSE_SERIALIZATION_ERROR = "response_serialization_error"
    RESPONSE_SIZE_EXCEEDED = "response_size_exceeded"
    
    # ============================================
    # LAYER 4: DEPENDENCY LAYER (7 types)
    # ============================================
    POSTGRES_CONNECTION_FAILURE = "postgres_connection_failure"
    POSTGRES_POOL_EXHAUSTED = "postgres_pool_exhausted"
    POSTGRES_QUERY_TIMEOUT = "postgres_query_timeout"
    REDIS_CONNECTION_FAILURE = "redis_connection_failure"
    REDIS_POOL_EXHAUSTED = "redis_pool_exhausted"
    EXTERNAL_API_TIMEOUT = "external_api_timeout"
    EXTERNAL_API_ERROR = "external_api_error"
    
    # ============================================
    # LAYER 5: INFRASTRUCTURE LAYER (5 types)
    # ============================================
    HIGH_MEMORY_USAGE = "high_memory_usage"
    HIGH_CPU_USAGE = "high_cpu_usage"
    DISK_SPACE_LOW = "disk_space_low"
    HIGH_NETWORK_LATENCY = "high_network_latency"
    CONTAINER_UNHEALTHY = "container_unhealthy"
    
    # ============================================
    # LAYER 6: SECURITY LAYER (3 types)
    # ============================================
    AUTH_BRUTE_FORCE = "auth_brute_force"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_LEAKAGE_DETECTED = "data_leakage_detected"
    
    # ============================================
    # LAYER 7: OPERATIONAL LAYER (2 types)
    # ============================================
    UNHANDLED_EXCEPTION = "unhandled_exception"
    APP_STARTUP_FAILURE = "app_startup_failure"
    
    # ============================================
    # LEGACY COMPATIBILITY (mapping to new types)
    # ============================================
    # These are kept for backward compatibility
    HIGH_API_RESPONSE_TIME = "high_api_response_time"  # → API_REQUEST_TIMEOUT
    SLOW_DATABASE_QUERY = "slow_database_query"  # → POSTGRES_QUERY_TIMEOUT
    RABBITMQ_CONSUMER_ERROR = "rabbitmq_consumer_error"  # Keep for RabbitMQ

