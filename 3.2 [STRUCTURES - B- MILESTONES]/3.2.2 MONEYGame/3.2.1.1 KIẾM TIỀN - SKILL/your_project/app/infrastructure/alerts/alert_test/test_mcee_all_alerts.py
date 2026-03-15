"""
Test MECE All Alerts - Test tất cả 47 alert types theo MECE framework

Mục đích:
    Test giả lập toàn bộ 47 alert types theo 7 layers của MECE framework:
    - Layer 1: Input Layer (7 types)
    - Layer 2: Processing Layer (17 types)
    - Layer 3: Output Layer (7 types)
    - Layer 4: Dependency Layer (7 types)
    - Layer 5: Infrastructure Layer (5 types)
    - Layer 6: Security Layer (3 types)
    - Layer 7: Operational Layer (2 types)

Cách chạy:
    python tests/alert_test/test_mcee_all_alerts.py
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.common.alerts import get_alert_manager, AlertType, AlertLevel
from app.common.alerts.alert_level_mapping import get_default_level


# Test cases cho từng alert type
TEST_CASES: Dict[AlertType, Dict] = {
    # ============================================
    # LAYER 1: INPUT LAYER (7 types)
    # ============================================
    AlertType.API_REQUEST_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] API request timeout (>10s).",
        "context": {
            "path": "/api/v1/bot/webhook",
            "method": "POST",
            "duration": "12.5s",
            "threshold": "10s",
            "client_ip": "192.168.1.100"
        }
    },
    AlertType.INVALID_REQUEST_PAYLOAD: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Invalid request payload.",
        "context": {
            "path": "/api/v1/bot/webhook",
            "method": "POST",
            "error": "ValidationError: conversation_id is required",
            "client_ip": "192.168.1.100"
        }
    },
    AlertType.AUTH_FAILURE: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Authentication failure: Invalid API key.",
        "context": {
            "client_ip": "192.168.1.100",
            "auth_method": "api_key",
            "endpoint": "/api/v1/bot/webhook"
        }
    },
    AlertType.RATE_LIMIT_EXCEEDED: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Rate limit exceeded.",
        "context": {
            "client_ip": "192.168.1.100",
            "endpoint": "/api/v1/bot/webhook",
            "limit": "100 requests/minute",
            "current": "105 requests/minute"
        }
    },
    AlertType.PAYLOAD_SIZE_EXCEEDED: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Payload size exceeded (>10MB).",
        "context": {
            "path": "/api/v1/bot/webhook",
            "size_mb": 12.5,
            "threshold_mb": 10,
            "client_ip": "192.168.1.100"
        }
    },
    AlertType.INVALID_JSON_FORMAT: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Invalid JSON format.",
        "context": {
            "path": "/api/v1/bot/webhook",
            "error": "JSONDecodeError: Expecting value: line 1 column 1",
            "client_ip": "192.168.1.100"
        }
    },
    AlertType.MISSING_REQUIRED_FIELDS: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Missing required fields.",
        "context": {
            "path": "/api/v1/bot/webhook",
            "missing_fields": ["conversation_id", "user_id"],
            "client_ip": "192.168.1.100"
        }
    },
    
    # ============================================
    # LAYER 2: PROCESSING LAYER (17 types)
    # ============================================
    
    # 2A. LLM Processing (9 types)
    AlertType.LLM_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] LLM request timeout (>5s).",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "timeout": "5s",
            "duration": "5.8s",
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_BOTH_FAILED: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Both LLM providers failed.",
        "context": {
            "primary_provider": "groq",
            "fallback_provider": "openai",
            "conversation_id": "test-123",
            "error": "All providers unavailable"
        }
    },
    AlertType.LLM_RATE_LIMIT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] LLM rate limit exceeded (429).",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "status_code": 429,
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_TOKEN_LIMIT_EXCEEDED: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] LLM token limit exceeded.",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "token_count": 85000,
            "max_tokens": 8192,
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_INVALID_API_KEY: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] LLM invalid API key.",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "status_code": 401,
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_MALFORMED_RESPONSE: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] LLM malformed response.",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "error": "JSONDecodeError: Invalid JSON",
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_PROVIDER_DOWN: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] LLM provider down (5xx).",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "status_code": 503,
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_CONTEXT_OVERFLOW: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] LLM context overflow.",
        "context": {
            "provider": "openai",
            "model": "gpt-4",
            "context_length": 150000,
            "max_context": 128000,
            "conversation_id": "test-123"
        }
    },
    AlertType.LLM_STREAMING_ERROR: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] LLM streaming error.",
        "context": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "error": "Stream connection lost",
            "conversation_id": "test-123"
        }
    },
    
    # 2B. Workflow Processing (4 types)
    AlertType.WORKFLOW_EXECUTION_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Workflow execution failed.",
        "context": {
            "conversation_id": "test-123",
            "duration": "8.5s",
            "workflow": "PoliciesWorkflow.process",
            "error_type": "TimeoutError",
            "error": "Workflow execution timeout"
        }
    },
    AlertType.WORKFLOW_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Workflow execution timeout (>6s in webhook).",
        "context": {
            "conversation_id": "test-123",
            "timeout": "6s",
            "duration": "8.2s",
            "workflow": "PoliciesWorkflow.process"
        }
    },
    AlertType.WORKFLOW_STATE_ERROR: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Workflow state validation failed.",
        "context": {
            "workflow_name": "PoliciesWorkflow",
            "state_type": "None",
            "has_status": False,
            "conversation_id": "test-123"
        }
    },
    AlertType.WEBHOOK_PROCESSING_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Webhook processing failure.",
        "context": {
            "conversation_id": "test-123",
            "duration": "15.2s",
            "error_type": "ValueError",
            "error": "Webhook processing error"
        }
    },
    
    # 2C. Agent Processing (4 types)
    AlertType.AGENT_EXECUTION_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Agent execution failed.",
        "context": {
            "agent_id": "test_agent",
            "error_type": "ValueError",
            "error": "Agent execution error",
            "duration": "5.2s"
        }
    },
    AlertType.AGENT_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Agent execution timeout (>30s).",
        "context": {
            "agent_id": "test_agent",
            "timeout": "30s",
            "duration": "32.5s"
        }
    },
    AlertType.AGENT_NOT_FOUND: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Agent not found.",
        "context": {
            "agent_id": "non_existent_agent"
        }
    },
    AlertType.AGENT_INVALID_OUTPUT: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Agent output validation failed.",
        "context": {
            "agent_id": "test_agent",
            "result_type": "None",
            "result_status": "error"
        }
    },
    
    # ============================================
    # LAYER 3: OUTPUT LAYER (7 types)
    # ============================================
    AlertType.REDIS_OPERATION_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Redis GET operation timeout (>2s).",
        "context": {
            "conversation_id": "test-123",
            "operation": "GET",
            "duration": "2.5s",
            "threshold": "2s"
        }
    },
    AlertType.REDIS_WRITE_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Redis write operation failed.",
        "context": {
            "conversation_id": "test-123",
            "operation": "SET",
            "duration": "1.2s",
            "error": "Connection lost"
        }
    },
    AlertType.POSTGRES_WRITE_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] PostgreSQL write operation failed.",
        "context": {
            "error": "Write timeout",
            "operation": "write",
            "duration": "6.2s"
        }
    },
    AlertType.KAFKA_PRODUCER_FAILURE: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Kafka send operation failed.",
        "context": {
            "topic": "test-topic",
            "operation": "send_kafka_one",
            "error": "Broker not available"
        }
    },
    AlertType.KAFKA_SEND_TIMEOUT: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Kafka send timeout (>5s).",
        "context": {
            "topic": "test-topic",
            "duration": "6.5s",
            "threshold": "5s"
        }
    },
    AlertType.RESPONSE_SERIALIZATION_ERROR: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Response serialization error.",
        "context": {
            "path": "/api/v1/bot/webhook",
            "error": "TypeError: Object of type datetime is not JSON serializable",
            "conversation_id": "test-123"
        }
    },
    AlertType.RESPONSE_SIZE_EXCEEDED: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Response size exceeded (>10MB).",
        "context": {
            "path": "/api/v1/bot/webhook",
            "size_mb": 12.8,
            "threshold_mb": 10,
            "conversation_id": "test-123"
        }
    },
    
    # ============================================
    # LAYER 4: DEPENDENCY LAYER (7 types)
    # ============================================
    AlertType.POSTGRES_CONNECTION_FAILURE: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] PostgreSQL connection error during session operation.",
        "context": {
            "error": "Connection refused",
            "operation": "get_db_session",
            "host": "localhost",
            "port": 5432
        }
    },
    AlertType.POSTGRES_POOL_EXHAUSTED: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] PostgreSQL connection pool exhausted.",
        "context": {
            "error": "Pool exhausted",
            "operation": "get_db_session",
            "max_connections": 20
        }
    },
    AlertType.POSTGRES_QUERY_TIMEOUT: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Database query timeout (>5s).",
        "context": {
            "operation": "query",
            "duration": "6.2s",
            "threshold": "5s"
        }
    },
    AlertType.REDIS_CONNECTION_FAILURE: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Redis connection failed.",
        "context": {
            "error": "Connection timeout",
            "host": "localhost",
            "port": 6379,
            "conversation_id": "test-123"
        }
    },
    AlertType.REDIS_POOL_EXHAUSTED: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Redis connection pool exhausted.",
        "context": {
            "conversation_id": "test-123",
            "operation": "GET",
            "error": "Pool exhausted"
        }
    },
    AlertType.EXTERNAL_API_TIMEOUT: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] External API timeout (>5s).",
        "context": {
            "service": "user_profile_api",
            "url": "https://api.example.com/profile",
            "duration": "6.5s",
            "threshold": "5s",
            "conversation_id": "test-123"
        }
    },
    AlertType.EXTERNAL_API_ERROR: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] External API error.",
        "context": {
            "service": "user_profile_api",
            "url": "https://api.example.com/profile",
            "status_code": 500,
            "error": "Internal Server Error",
            "conversation_id": "test-123"
        }
    },
    
    # ============================================
    # LAYER 5: INFRASTRUCTURE LAYER (5 types)
    # ============================================
    AlertType.HIGH_MEMORY_USAGE: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] High memory usage detected (92.5%).",
        "context": {
            "memory_percent": 92.5,
            "threshold": 90,
            "available_mb": 512
        }
    },
    AlertType.HIGH_CPU_USAGE: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] High CPU usage detected (95.2%).",
        "context": {
            "cpu_percent": 95.2,
            "threshold": 90,
            "cpu_count": 8
        }
    },
    AlertType.DISK_SPACE_LOW: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] Low disk space detected (92.8% used).",
        "context": {
            "disk_percent": 92.8,
            "threshold": 90,
            "free_gb": 5.2
        }
    },
    AlertType.HIGH_NETWORK_LATENCY: {
        "level": AlertLevel.MEDIUM,
        "message": "[doancuong] High network latency detected (1200ms).",
        "context": {
            "latency_ms": 1200,
            "threshold_ms": 1000
        }
    },
    AlertType.CONTAINER_UNHEALTHY: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Container unhealthy: main process not running.",
        "context": {
            "pid": 12345,
            "status": "zombie"
        }
    },
    
    # ============================================
    # LAYER 6: SECURITY LAYER (3 types)
    # ============================================
    AlertType.AUTH_BRUTE_FORCE: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Brute force attack detected.",
        "context": {
            "client_ip": "192.168.1.100",
            "endpoint": "api_key_auth",
            "failure_count": 5,
            "threshold": 5,
            "window": "300s"
        }
    },
    AlertType.SUSPICIOUS_ACTIVITY: {
        "level": AlertLevel.HIGH,
        "message": "[doancuong] Suspicious activity detected.",
        "context": {
            "activity_type": "unusual_request_pattern",
            "client_ip": "192.168.1.100",
            "details": "100 requests in 1 minute"
        }
    },
    AlertType.DATA_LEAKAGE_DETECTED: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Data leakage patterns detected.",
        "context": {
            "pattern": "api_key",
            "location": "response_body",
            "severity": "high"
        }
    },
    
    # ============================================
    # LAYER 7: OPERATIONAL LAYER (2 types)
    # ============================================
    AlertType.UNHANDLED_EXCEPTION: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Unhandled exception occurred in application.",
        "context": {
            "path": "/api/v1/bot/webhook",
            "method": "POST",
            "client_ip": "192.168.1.100",
            "error_type": "ValueError",
            "error_message": "Unexpected error"
        }
    },
    AlertType.APP_STARTUP_FAILURE: {
        "level": AlertLevel.CRITICAL,
        "message": "[doancuong] Application startup failure.",
        "context": {
            "error": "Database connection failed",
            "component": "database_init"
        }
    },
}


async def test_alert_type(alert_type: AlertType, test_case: Dict) -> Tuple[bool, str]:
    """
    Test một alert type
    
    Returns:
        (success: bool, message: str)
    """
    try:
        manager = get_alert_manager()
        
        result = await manager.send_alert(
            alert_type=alert_type,
            level=test_case["level"],
            message=test_case["message"],
            context=test_case["context"]
        )
        
        if result:
            return True, f"[OK] {alert_type.value}"
        else:
            return False, f"[FAIL] {alert_type.value} - send_alert returned False"
            
    except Exception as e:
        return False, f"[ERROR] {alert_type.value} - {str(e)}"


async def test_layer(layer_name: str, alert_types: List[AlertType]) -> Dict:
    """
    Test một layer
    
    Returns:
        Dict với stats: {"total": int, "passed": int, "failed": int, "results": List}
    """
    print(f"\n{'='*60}")
    print(f"Testing {layer_name}")
    print(f"{'='*60}")
    
    results = []
    passed = 0
    failed = 0
    
    for alert_type in alert_types:
        if alert_type not in TEST_CASES:
            print(f"[SKIP] {alert_type.value} - No test case defined")
            continue
            
        test_case = TEST_CASES[alert_type]
        success, message = await test_alert_type(alert_type, test_case)
        
        results.append({
            "alert_type": alert_type.value,
            "success": success,
            "message": message
        })
        
        if success:
            passed += 1
            print(f"  {message}")
        else:
            failed += 1
            print(f"  {message}")
    
    return {
        "total": len(alert_types),
        "passed": passed,
        "failed": failed,
        "results": results
    }


async def main():
    """Run all MECE alert tests"""
    print("="*60)
    print("TESTING MECE ALL ALERTS (47 types)")
    print("="*60)
    
    # Define layers
    layers = {
        "Layer 1: INPUT LAYER": [
            AlertType.API_REQUEST_TIMEOUT,
            AlertType.INVALID_REQUEST_PAYLOAD,
            AlertType.AUTH_FAILURE,
            AlertType.RATE_LIMIT_EXCEEDED,
            AlertType.PAYLOAD_SIZE_EXCEEDED,
            AlertType.INVALID_JSON_FORMAT,
            AlertType.MISSING_REQUIRED_FIELDS,
        ],
        "Layer 2: PROCESSING LAYER": [
            # LLM
            AlertType.LLM_TIMEOUT,
            AlertType.LLM_BOTH_FAILED,
            AlertType.LLM_RATE_LIMIT,
            AlertType.LLM_TOKEN_LIMIT_EXCEEDED,
            AlertType.LLM_INVALID_API_KEY,
            AlertType.LLM_MALFORMED_RESPONSE,
            AlertType.LLM_PROVIDER_DOWN,
            AlertType.LLM_CONTEXT_OVERFLOW,
            AlertType.LLM_STREAMING_ERROR,
            # Workflow
            AlertType.WORKFLOW_EXECUTION_FAILURE,
            AlertType.WORKFLOW_TIMEOUT,
            AlertType.WORKFLOW_STATE_ERROR,
            AlertType.WEBHOOK_PROCESSING_FAILURE,
            # Agent
            AlertType.AGENT_EXECUTION_FAILURE,
            AlertType.AGENT_TIMEOUT,
            AlertType.AGENT_NOT_FOUND,
            AlertType.AGENT_INVALID_OUTPUT,
        ],
        "Layer 3: OUTPUT LAYER": [
            AlertType.REDIS_OPERATION_TIMEOUT,
            AlertType.REDIS_WRITE_FAILURE,
            AlertType.POSTGRES_WRITE_FAILURE,
            AlertType.KAFKA_PRODUCER_FAILURE,
            AlertType.KAFKA_SEND_TIMEOUT,
            AlertType.RESPONSE_SERIALIZATION_ERROR,
            AlertType.RESPONSE_SIZE_EXCEEDED,
        ],
        "Layer 4: DEPENDENCY LAYER": [
            AlertType.POSTGRES_CONNECTION_FAILURE,
            AlertType.POSTGRES_POOL_EXHAUSTED,
            AlertType.POSTGRES_QUERY_TIMEOUT,
            AlertType.REDIS_CONNECTION_FAILURE,
            AlertType.REDIS_POOL_EXHAUSTED,
            AlertType.EXTERNAL_API_TIMEOUT,
            AlertType.EXTERNAL_API_ERROR,
        ],
        "Layer 5: INFRASTRUCTURE LAYER": [
            AlertType.HIGH_MEMORY_USAGE,
            AlertType.HIGH_CPU_USAGE,
            AlertType.DISK_SPACE_LOW,
            AlertType.HIGH_NETWORK_LATENCY,
            AlertType.CONTAINER_UNHEALTHY,
        ],
        "Layer 6: SECURITY LAYER": [
            AlertType.AUTH_BRUTE_FORCE,
            AlertType.SUSPICIOUS_ACTIVITY,
            AlertType.DATA_LEAKAGE_DETECTED,
        ],
        "Layer 7: OPERATIONAL LAYER": [
            AlertType.UNHANDLED_EXCEPTION,
            AlertType.APP_STARTUP_FAILURE,
        ],
    }
    
    # Run tests for each layer
    all_results = {}
    total_passed = 0
    total_failed = 0
    total_tested = 0
    
    for layer_name, alert_types in layers.items():
        layer_results = await test_layer(layer_name, alert_types)
        all_results[layer_name] = layer_results
        
        total_passed += layer_results["passed"]
        total_failed += layer_results["failed"]
        total_tested += layer_results["total"]
    
    # Print summary
    print("\n" + "="*60)
    print("MECE TEST SUMMARY")
    print("="*60)
    
    for layer_name, results in all_results.items():
        print(f"\n{layer_name}:")
        print(f"  Total: {results['total']}")
        print(f"  Passed: {results['passed']}")
        print(f"  Failed: {results['failed']}")
    
    print("\n" + "="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    print(f"Total Alert Types: {total_tested}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {(total_passed/total_tested*100):.1f}%" if total_tested > 0 else "N/A")
    
    if total_failed == 0:
        print("\n[SUCCESS] ALL MECE ALERT TESTS PASSED!")
        print("[INFO] Check Google Chat to verify alerts were received")
    else:
        print(f"\n[WARNING] {total_failed} alert type(s) failed")
        print("[INFO] Check logs above for details")
    
    print("="*60)
    
    return total_failed == 0


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

