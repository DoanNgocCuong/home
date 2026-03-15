"""
Test script cho TẤT CẢ Alerts đã implement

Mục đích:
    Test đầy đủ tất cả alerts đã implement:
    - Phase 1: CRITICAL alerts (4 alerts)
    - Phase 2: HIGH priority alerts (4 alerts)
    - Phase 3: MEDIUM priority alerts (4 alerts)
    
    Tổng cộng: 12 alerts

Usage:
    python -m tests.alert_test.test_all_alerts
    # hoặc
    python tests/alert_test/test_all_alerts.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()  # Load .env file từ project root

from app.common.alerts import get_alert_manager, AlertType, AlertLevel


async def test_postgres_connection_alert():
    """Test PostgreSQL connection failure alert (CRITICAL)"""
    print("\n" + "="*60)
    print("TEST 1: PostgreSQL Connection Failure Alert (CRITICAL)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.POSTGRES_CONNECTION_FAILURE,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Failed to connect to PostgreSQL. Service may be degraded.",
        context={
            "host": "103.253.20.30",
            "port": "5441",
            "database": "postgres",
            "error": "Connection timeout after 5s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_redis_connection_alert():
    """Test Redis connection failure alert (CRITICAL)"""
    print("\n" + "="*60)
    print("TEST 2: Redis Connection Failure Alert (CRITICAL)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.REDIS_CONNECTION_FAILURE,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Failed to connect to Redis. Service may be degraded.",
        context={
            "host": "callbot-llm-redis",
            "port": "6379",
            "error": "Connection refused"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_redis_operation_timeout_alert():
    """Test Redis operation timeout alert (HIGH)"""
    print("\n" + "="*60)
    print("TEST 3: Redis Operation Timeout Alert (HIGH)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.REDIS_OPERATION_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Redis GET operation timeout (>2s).",
        context={
            "conversation_id": "test_conv_123",
            "operation": "GET",
            "duration": "2.5s",
            "threshold": "2s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_llm_timeout_alert():
    """Test LLM timeout alert (HIGH)"""
    print("\n" + "="*60)
    print("TEST 4: LLM Timeout Alert (HIGH)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] LLM main model timeout after 1.5s. Switching to fallback.",
        context={
            "conversation_id": "test_conv_456",
            "provider": "openai",
            "model": "gpt-4",
            "timeout": "1.5s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_llm_rate_limit_alert():
    """Test LLM rate limit alert (HIGH) - Phase 2"""
    print("\n" + "="*60)
    print("TEST 5: LLM Rate Limit Alert (HIGH) - Phase 2")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.LLM_RATE_LIMIT,
        level=AlertLevel.HIGH,
        message="[doancuong] LLM rate limit detected. Switching to fallback.",
        context={
            "conversation_id": "test_conv_789",
            "provider": "openai",
            "model": "gpt-4",
            "attempt": 1,
            "max_retries": 3,
            "error": "HTTP 429: Rate limit exceeded"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_llm_both_failed_alert():
    """Test LLM both failed alert (CRITICAL)"""
    print("\n" + "="*60)
    print("TEST 6: LLM Both Failed Alert (CRITICAL)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.LLM_BOTH_FAILED,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Both main and fallback LLM failed. Using INTENT_FALLBACK.",
        context={
            "conversation_id": "test_conv_101",
            "provider": "openai",
            "model": "gpt-4",
            "fallback_model": "gpt-4o-mini",
            "error": "Timeout after 5s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_kafka_producer_failure_alert():
    """Test Kafka producer failure alert (HIGH) - Phase 2"""
    print("\n" + "="*60)
    print("TEST 7: Kafka Producer Failure Alert (HIGH) - Phase 2")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.KAFKA_PRODUCER_FAILURE,
        level=AlertLevel.HIGH,
        message="[doancuong] Kafka send operation timeout (>3s).",
        context={
            "topic": "robot-events",
            "timeout": "3s",
            "operation": "send_kafka_one"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_workflow_execution_failure_alert():
    """Test Workflow execution failure alert (HIGH) - Phase 2"""
    print("\n" + "="*60)
    print("TEST 8: Workflow Execution Failure Alert (HIGH) - Phase 2")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.WORKFLOW_EXECUTION_FAILURE,
        level=AlertLevel.HIGH,
        message="[doancuong] Workflow execution timeout (>60s).",
        context={
            "conversation_id": "test_conv_202",
            "timeout": "60s",
            "duration": "65.2s",
            "workflow": "PoliciesWorkflow.process"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_agent_execution_failure_alert():
    """Test Agent execution failure alert (HIGH) - Phase 2"""
    print("\n" + "="*60)
    print("TEST 9: Agent Execution Failure Alert (HIGH) - Phase 2")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.AGENT_EXECUTION_FAILURE,
        level=AlertLevel.HIGH,
        message="[doancuong] Agent execution timeout (>30s).",
        context={
            "agent_id": "qc_workflow",
            "timeout": "30s",
            "duration": "32.5s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_external_api_timeout_alert():
    """Test External API timeout alert (MEDIUM) - Phase 3"""
    print("\n" + "="*60)
    print("TEST 10: External API Timeout Alert (MEDIUM) - Phase 3")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.EXTERNAL_API_TIMEOUT,
        level=AlertLevel.MEDIUM,
        message="[doancuong] External API timeout: Get User Profile.",
        context={
            "api": "get_user_profile",
            "url": "https://api.example.com/user_profile",
            "conversation_id": "test_conv_303",
            "timeout": "5s",
            "duration": "5.8s"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_database_query_timeout_alert():
    """Test Database query timeout alert (MEDIUM) - Phase 3"""
    print("\n" + "="*60)
    print("TEST 11: Database Query Timeout Alert (MEDIUM) - Phase 3")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.POSTGRES_QUERY_TIMEOUT,
        level=AlertLevel.MEDIUM,
        message="[doancuong] Database query timeout (>5s).",
        context={
            "operation": "query_execution",
            "duration": "6.2s",
            "threshold": "5s",
            "query": "SELECT * FROM bots WHERE..."
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_high_api_response_time_alert():
    """Test High API response time alert (MEDIUM) - Phase 3"""
    print("\n" + "="*60)
    print("TEST 12: High API Response Time Alert (MEDIUM) - Phase 3")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.HIGH_API_RESPONSE_TIME,
        level=AlertLevel.MEDIUM,
        message="[doancuong] High API response time detected (>5s for 3 consecutive requests).",
        context={
            "path": "/api/v1/bot/webhook",
            "method": "POST",
            "response_times": ["5.2s", "5.8s", "6.1s"],
            "threshold": "5s",
            "status_code": 200
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_rate_limit_exceeded_alert():
    """Test Rate limit exceeded alert (MEDIUM) - Phase 3"""
    print("\n" + "="*60)
    print("TEST 13: Rate Limit Exceeded Alert (MEDIUM) - Phase 3")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.RATE_LIMIT_EXCEEDED,
        level=AlertLevel.MEDIUM,
        message="[doancuong] Rate limit exceeded: Too many requests from IP.",
        context={
            "client_ip": "192.168.1.100",
            "request_count": 105,
            "threshold": 100,
            "window": "60s",
            "path": "/api/v1/bot/webhook",
            "method": "POST"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_unhandled_exception_alert():
    """Test Unhandled exception alert (CRITICAL)"""
    print("\n" + "="*60)
    print("TEST 14: Unhandled Exception Alert (CRITICAL)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.UNHANDLED_EXCEPTION,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Unhandled exception occurred in application.",
        context={
            "path": "/api/v1/bot/webhook",
            "method": "POST",
            "client_ip": "192.168.1.100",
            "error_type": "ValueError",
            "error_message": "Invalid input format",
            "traceback": "Traceback (most recent call last):\n  File ..."
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_app_startup_failure_alert():
    """Test Application startup failure alert (CRITICAL)"""
    print("\n" + "="*60)
    print("TEST 15: Application Startup Failure Alert (CRITICAL)")
    print("="*60)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        return False
    
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    success = await alert_manager.send_alert(
        alert_type=AlertType.APP_STARTUP_FAILURE,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Application startup failure: Kafka producer initialization failed.",
        context={
            "component": "kafka",
            "environment": "production",
            "error": "Connection timeout to Kafka broker"
        }
    )
    
    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def run_all_tests():
    """Run all alert tests"""
    print("\n" + "🚨"*30)
    print("COMPREHENSIVE ALERTS TEST SUITE")
    print("Testing ALL 12+ Alerts (Phase 1 + Phase 2 + Phase 3)")
    print("🚨"*30)
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("\n❌ Error: GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        print("   Please add it to .env file:")
        print("   GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/...")
        return
    
    print(f"\n🔗 Webhook URL: {webhook_url[:50]}...\n")
    
    results = []
    
    # Phase 1: CRITICAL Alerts
    print("\n" + "="*60)
    print("PHASE 1: CRITICAL ALERTS")
    print("="*60)
    results.append(("PostgreSQL Connection", await test_postgres_connection_alert()))
    await asyncio.sleep(2)
    
    results.append(("Redis Connection", await test_redis_connection_alert()))
    await asyncio.sleep(2)
    
    results.append(("LLM Both Failed", await test_llm_both_failed_alert()))
    await asyncio.sleep(2)
    
    results.append(("Unhandled Exception", await test_unhandled_exception_alert()))
    await asyncio.sleep(2)
    
    results.append(("App Startup Failure", await test_app_startup_failure_alert()))
    await asyncio.sleep(2)
    
    # Phase 2: HIGH Priority Alerts
    print("\n" + "="*60)
    print("PHASE 2: HIGH PRIORITY ALERTS")
    print("="*60)
    results.append(("Redis Operation Timeout", await test_redis_operation_timeout_alert()))
    await asyncio.sleep(2)
    
    results.append(("LLM Timeout", await test_llm_timeout_alert()))
    await asyncio.sleep(2)
    
    results.append(("LLM Rate Limit", await test_llm_rate_limit_alert()))
    await asyncio.sleep(2)
    
    results.append(("Kafka Producer Failure", await test_kafka_producer_failure_alert()))
    await asyncio.sleep(2)
    
    results.append(("Workflow Execution Failure", await test_workflow_execution_failure_alert()))
    await asyncio.sleep(2)
    
    results.append(("Agent Execution Failure", await test_agent_execution_failure_alert()))
    await asyncio.sleep(2)
    
    # Phase 3: MEDIUM Priority Alerts
    print("\n" + "="*60)
    print("PHASE 3: MEDIUM PRIORITY ALERTS")
    print("="*60)
    results.append(("External API Timeout", await test_external_api_timeout_alert()))
    await asyncio.sleep(2)
    
    results.append(("Database Query Timeout", await test_database_query_timeout_alert()))
    await asyncio.sleep(2)
    
    results.append(("High API Response Time", await test_high_api_response_time_alert()))
    await asyncio.sleep(2)
    
    results.append(("Rate Limit Exceeded", await test_rate_limit_exceeded_alert()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 Results by Phase:")
    print(f"   Phase 1 (CRITICAL): {sum(1 for name, r in results[:5] if r)}/5")
    print(f"   Phase 2 (HIGH): {sum(1 for name, r in results[5:11] if r)}/6")
    print(f"   Phase 3 (MEDIUM): {sum(1 for name, r in results[11:] if r)}/4")
    
    print(f"\n📋 Detailed Results:")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    print(f"\n📈 Total: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Check Google Chat room to verify all alerts.")
        print("📱 All alerts should have '[doancuong]' prefix in Google Chat!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check logs.")
    
    print("\n" + "="*60)
    print("✅ Test suite completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())

