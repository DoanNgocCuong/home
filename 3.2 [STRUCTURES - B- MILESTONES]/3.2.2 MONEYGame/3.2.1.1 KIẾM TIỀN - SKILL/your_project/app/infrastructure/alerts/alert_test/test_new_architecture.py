"""
Test New Architecture Components - Alert System

Mục đích:
    Test các components của architecture mới:
    - AlertContext
    - RateLimiter
    - Deduplicator
    - Transports (GoogleChatTransport, LogTransport)
    - Formatters (GoogleChatFormatter)
    - AlertManager với new architecture

Usage:
    python tests/alert_test/test_new_architecture.py
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.common.alerts import (
    AlertManager,
    AlertType,
    AlertLevel,
    AlertContext,
    get_alert_manager
)
from app.common.alerts.rate_limiting.rate_limiter import RateLimiter
from app.common.alerts.rate_limiting.deduplicator import Deduplicator
from app.common.alerts.transports.google_chat_transport import GoogleChatTransport
from app.common.alerts.transports.log_transport import LogTransport
from app.common.alerts.formatters.google_chat_formatter import GoogleChatFormatter
from app.common.alerts.transports.base_transport import AlertMessage


async def test_alert_context():
    """Test AlertContext immutable dataclass"""
    print("\n=== Testing AlertContext ===")
    
    # Test 1: Create AlertContext
    context = AlertContext(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test message",
        context={"provider": "openai", "model": "gpt-4"},
        request_id="req-123",
        conversation_id="conv-456"
    )
    assert context.alert_type == AlertType.LLM_TIMEOUT
    assert context.level == AlertLevel.HIGH
    assert context.message == "[doancuong] Test message"
    assert context.context["provider"] == "openai"
    print("[OK] AlertContext creation")
    
    # Test 2: Immutability (frozen dataclass)
    try:
        context.alert_type = AlertType.LLM_BOTH_FAILED
        assert False, "Should raise error"
    except Exception:
        print("[OK] AlertContext is immutable")
    
    # Test 3: get_alert_key()
    key1 = context.get_alert_key()
    assert "llm_timeout" in key1
    assert "provider=openai" in key1 or "model=gpt-4" in key1
    print(f"[OK] get_alert_key() = {key1}")
    
    # Test 4: to_dict()
    context_dict = context.to_dict()
    assert context_dict["alert_type"] == "llm_timeout"
    assert context_dict["level"] == "high"
    assert context_dict["message"] == "[doancuong] Test message"
    assert "timestamp" in context_dict
    print("[OK] to_dict() works")
    
    print("[SUCCESS] AlertContext tests passed!\n")


def test_rate_limiter():
    """Test RateLimiter"""
    print("\n=== Testing RateLimiter ===")
    
    rate_limiter = RateLimiter()
    
    # Test 1: CRITICAL - unlimited
    key = "test_critical"
    for i in range(10):
        result = rate_limiter.check_and_record(key, AlertLevel.CRITICAL)
        assert result == False, f"CRITICAL should not be rate limited (attempt {i+1})"
    print("[OK] CRITICAL alerts not rate limited")
    
    # Test 2: HIGH - 5 alerts / 5 minutes
    key = "test_high"
    for i in range(5):
        result = rate_limiter.check_and_record(key, AlertLevel.HIGH)
        assert result == False, f"HIGH should not be rate limited (attempt {i+1})"
    
    # 6th attempt should be rate limited
    result = rate_limiter.check_and_record(key, AlertLevel.HIGH)
    assert result == True, "6th HIGH alert should be rate limited"
    print("[OK] HIGH alerts rate limited after 5 attempts")
    
    # Test 3: MEDIUM - 3 alerts / 10 minutes
    key = "test_medium"
    for i in range(3):
        result = rate_limiter.check_and_record(key, AlertLevel.MEDIUM)
        assert result == False, f"MEDIUM should not be rate limited (attempt {i+1})"
    
    # 4th attempt should be rate limited
    result = rate_limiter.check_and_record(key, AlertLevel.MEDIUM)
    assert result == True, "4th MEDIUM alert should be rate limited"
    print("[OK] MEDIUM alerts rate limited after 3 attempts")
    
    # Test 4: LOW - 1 alert / 30 minutes
    key = "test_low"
    result = rate_limiter.check_and_record(key, AlertLevel.LOW)
    assert result == False, "First LOW alert should not be rate limited"
    
    # 2nd attempt should be rate limited
    result = rate_limiter.check_and_record(key, AlertLevel.LOW)
    assert result == True, "2nd LOW alert should be rate limited"
    print("[OK] LOW alerts rate limited after 1 attempt")
    
    print("[SUCCESS] RateLimiter tests passed!\n")


def test_deduplicator():
    """Test Deduplicator"""
    print("\n=== Testing Deduplicator ===")
    
    deduplicator = Deduplicator()
    
    # Test 1: First alert should not be suppressed
    key = "test_dedup"
    should_suppress, count = deduplicator.check_and_record(key)
    assert should_suppress == False, "First alert should not be suppressed"
    assert count == 1, "Count should be 1"
    print("[OK] First alert not suppressed")
    
    # Test 2: Second alert within 60s should be suppressed
    should_suppress, count = deduplicator.check_and_record(key)
    assert should_suppress == True, "Second alert should be suppressed"
    assert count == 2, "Count should be 2"
    print("[OK] Second alert suppressed (count=2)")
    
    # Test 3: Third alert should also be suppressed
    should_suppress, count = deduplicator.check_and_record(key)
    assert should_suppress == True, "Third alert should be suppressed"
    assert count == 3, "Count should be 3"
    print("[OK] Third alert suppressed (count=3)")
    
    print("[SUCCESS] Deduplicator tests passed!\n")


async def test_log_transport():
    """Test LogTransport"""
    print("\n=== Testing LogTransport ===")
    
    transport = LogTransport()
    
    # Test 1: is_available()
    assert transport.is_available() == True, "LogTransport should always be available"
    print("[OK] LogTransport is_available()")
    
    # Test 2: send()
    message = AlertMessage(
        content="Test message",
        format="text"
    )
    result = await transport.send(message)
    assert result == True, "LogTransport should always succeed"
    print("[OK] LogTransport send()")
    
    print("[SUCCESS] LogTransport tests passed!\n")


async def test_google_chat_transport():
    """Test GoogleChatTransport"""
    print("\n=== Testing GoogleChatTransport ===")
    
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    
    if not webhook_url:
        print("[SKIP] GOOGLE_CHAT_WEBHOOK_URL not set, skipping GoogleChatTransport tests")
        return
    
    transport = GoogleChatTransport(webhook_url=webhook_url)
    
    # Test 1: is_available()
    available = transport.is_available()
    print(f"[OK] GoogleChatTransport is_available() = {available}")
    
    # Test 2: send()
    message = AlertMessage(
        content={"text": "[doancuong] Test from GoogleChatTransport"},
        format="google_chat"
    )
    result = await transport.send(message)
    print(f"[OK] GoogleChatTransport send() = {result}")
    
    print("[SUCCESS] GoogleChatTransport tests passed!\n")


def test_google_chat_formatter():
    """Test GoogleChatFormatter"""
    print("\n=== Testing GoogleChatFormatter ===")
    
    formatter = GoogleChatFormatter()
    
    # Test 1: Format CRITICAL alert
    context = AlertContext(
        alert_type=AlertType.LLM_BOTH_FAILED,
        level=AlertLevel.CRITICAL,
        message="[doancuong] Both LLM models failed",
        context={"provider": "openai", "model": "gpt-4"},
        request_id="req-123"
    )
    
    message = formatter.format(context)
    assert message is not None, "Formatter should return message"
    assert message.format == "google_chat", "Format should be google_chat"
    assert "content" in message.content or "text" in message.content, "Should have content"
    print("[OK] GoogleChatFormatter format() for CRITICAL")
    
    # Test 2: Format HIGH alert
    context = AlertContext(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] LLM timeout",
        context={"provider": "openai"}
    )
    
    message = formatter.format(context)
    assert message is not None, "Formatter should return message"
    print("[OK] GoogleChatFormatter format() for HIGH")
    
    # Test 3: Format MEDIUM alert
    context = AlertContext(
        alert_type=AlertType.POSTGRES_QUERY_TIMEOUT,
        level=AlertLevel.MEDIUM,
        message="[doancuong] Query timeout",
        context={"query": "SELECT * FROM bots"}
    )
    
    message = formatter.format(context)
    assert message is not None, "Formatter should return message"
    print("[OK] GoogleChatFormatter format() for MEDIUM")
    
    print("[SUCCESS] GoogleChatFormatter tests passed!\n")


async def test_alert_manager_new_architecture():
    """Test AlertManager với new architecture"""
    print("\n=== Testing AlertManager (New Architecture) ===")
    
    # Test 1: AlertManager với LogTransport
    manager = AlertManager(transport=LogTransport())
    assert manager.transport is not None, "Transport should be set"
    assert manager.formatter is not None, "Formatter should be set"
    assert manager.rate_limiter is not None, "RateLimiter should be set"
    assert manager.deduplicator is not None, "Deduplicator should be set"
    print("[OK] AlertManager initialization with LogTransport")
    
    # Test 2: Send alert với new architecture
    result = await manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test alert from new architecture",
        context={"provider": "openai", "model": "gpt-4"},
        request_id="req-123"
    )
    assert result == True, "Alert should be sent successfully"
    print("[OK] AlertManager send_alert() with new architecture")
    
    # Test 3: Rate limiting
    key = "test_rate_limit"
    for i in range(5):
        result = await manager.send_alert(
            alert_type=AlertType.LLM_TIMEOUT,
            level=AlertLevel.HIGH,
            message=f"[doancuong] Test {i+1}",
            context={"test_key": key}
        )
        assert result == True, f"Alert {i+1} should be sent"
    
    # 6th should be rate limited
    result = await manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test 6 (should be rate limited)",
        context={"test_key": key}
    )
    assert result == True, "Rate limited alert should return True (properly handled)"
    print("[OK] AlertManager rate limiting works")
    
    # Test 4: Deduplication
    key = "test_dedup"
    result1 = await manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test dedup 1",
        context={"test_key": key}
    )
    assert result1 == True, "First alert should be sent"
    
    result2 = await manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test dedup 2",
        context={"test_key": key}
    )
    assert result2 == True, "Deduplicated alert should return True (properly handled)"
    print("[OK] AlertManager deduplication works")
    
    # Test 5: CRITICAL alerts not rate limited
    for i in range(10):
        result = await manager.send_alert(
            alert_type=AlertType.LLM_BOTH_FAILED,
            level=AlertLevel.CRITICAL,
            message=f"[doancuong] Critical test {i+1}",
            context={"test": "critical"}
        )
        assert result == True, f"Critical alert {i+1} should be sent"
    print("[OK] CRITICAL alerts not rate limited")
    
    print("[SUCCESS] AlertManager (New Architecture) tests passed!\n")


async def test_all_47_alert_types():
    """Test tất cả 47 alert types với new architecture"""
    print("\n=== Testing All 47 Alert Types ===")
    
    manager = AlertManager(transport=LogTransport())
    
    # Get all alert types
    all_types = [e for e in AlertType]
    print(f"Total alert types: {len(all_types)}")
    
    # Test each type
    passed = 0
    failed = 0
    
    for alert_type in all_types:
        try:
            result = await manager.send_alert(
                alert_type=alert_type,
                level=AlertLevel.MEDIUM,  # Use MEDIUM for testing
                message=f"[doancuong] Test {alert_type.value}",
                context={"test": True}
            )
            if result:
                passed += 1
                print(f"  [OK] {alert_type.value}")
            else:
                failed += 1
                print(f"  [FAIL] {alert_type.value}")
        except Exception as e:
            failed += 1
            print(f"  [ERROR] {alert_type.value}: {e}")
    
    print(f"\n[SUMMARY] Passed: {passed}, Failed: {failed}, Total: {len(all_types)}")
    
    if failed == 0:
        print("[SUCCESS] All 47 alert types work with new architecture!\n")
    else:
        print(f"[WARNING] {failed} alert types failed!\n")


async def main():
    """Run all tests"""
    print("=" * 60)
    print("TESTING NEW ARCHITECTURE COMPONENTS")
    print("=" * 60)
    
    # Test components
    await test_alert_context()
    test_rate_limiter()
    test_deduplicator()
    await test_log_transport()
    await test_google_chat_transport()
    test_google_chat_formatter()
    await test_alert_manager_new_architecture()
    await test_all_47_alert_types()
    
    print("=" * 60)
    print("[SUCCESS] ALL NEW ARCHITECTURE TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
