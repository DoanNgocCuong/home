"""
Test script cho Alert System

Mục đích:
    Test Google Chat alert system với LLM timeout scenario

Usage:
    # Run test (webhook URL sẽ được đọc từ .env)
    python -m tests.alert_test.test_alert_system
    # hoặc
    python tests/alert_test/test_alert_system.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path để import app modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()  # Load .env file từ project root

from app.common.alerts import get_alert_manager, AlertType, AlertLevel


async def test_google_chat_alert():
    """Test gửi alert đến Google Chat"""
    
    # Get webhook URL từ .env (đã được load bởi dotenv)
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ Error: GOOGLE_CHAT_WEBHOOK_URL not found!")
        print("   Please add it to .env file:")
        print("   GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/...")
        return
    
    print(f"🔗 Webhook URL: {webhook_url[:50]}...")
    print("\n🧪 Testing Google Chat Alert System...\n")
    
    # Get alert manager với webhook URL từ .env
    alert_manager = get_alert_manager(webhook_url=webhook_url)
    
    # Test 1: Simple text message
    print("Test 1: Sending simple text message...")
    success = await alert_manager.chat_client.send_text("🧪 Test alert từ Alert System - Simple text message")
    print(f"✅ Result: {'Success' if success else 'Failed'}\n")
    await asyncio.sleep(2)
    
    # Test 2: CRITICAL alert (LLM both failed)
    print("Test 2: Sending CRITICAL alert (LLM both failed)...")
    success = await alert_manager.send_alert(
        alert_type=AlertType.LLM_BOTH_FAILED,
        level=AlertLevel.CRITICAL,
        message="Both main and fallback LLM failed. Using INTENT_FALLBACK.",
        context={
            "conversation_id": "test_conv_123",
            "provider": "openai",
            "model": "gpt-4",
            "fallback_model": "gpt-4o-mini",
            "error": "Timeout after 5s"
        }
    )
    print(f"✅ Result: {'Success' if success else 'Failed'}\n")
    await asyncio.sleep(2)
    
    # Test 3: HIGH alert (LLM timeout)
    print("Test 3: Sending HIGH alert (LLM timeout)...")
    success = await alert_manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="LLM main model timeout after 1.5s. Switching to fallback.",
        context={
            "conversation_id": "test_conv_456",
            "provider": "openai",
            "model": "gpt-4",
            "timeout": "1.5s"
        }
    )
    print(f"✅ Result: {'Success' if success else 'Failed'}\n")
    await asyncio.sleep(2)
    
    # Test 4: MEDIUM alert
    print("Test 4: Sending MEDIUM alert...")
    success = await alert_manager.send_alert(
        alert_type=AlertType.POSTGRES_QUERY_TIMEOUT,
        level=AlertLevel.MEDIUM,
        message="Database query timeout after 5s",
        context={
            "query": "SELECT * FROM bots",
            "duration": "5.2s",
            "threshold": "5s"
        }
    )
    print(f"✅ Result: {'Success' if success else 'Failed'}\n")
    
    print("✅ All tests completed!")
    print("\n📱 Check Google Chat room để xem alerts!")


if __name__ == "__main__":
    # Webhook URL sẽ được đọc từ .env file
    # dotenv đã được load ở đầu file
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️  Warning: GOOGLE_CHAT_WEBHOOK_URL not found in .env or environment")
        print("   Please add it to .env file:")
        print("   GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/...")
    
    asyncio.run(test_google_chat_alert())

