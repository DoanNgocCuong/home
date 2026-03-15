"""
Test backward compatibility - Existing code should still work
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from dotenv import load_dotenv

load_dotenv()

from app.common.alerts import get_alert_manager, AlertType, AlertLevel


async def test_existing_api():
    """Test that existing API still works"""
    print("\n=== Testing Backward Compatibility ===")
    
    # Test 1: get_alert_manager() still works
    manager = get_alert_manager()
    assert manager is not None
    print("[OK] get_alert_manager() works")
    
    # Test 2: send_alert() with old signature still works
    result = await manager.send_alert(
        alert_type=AlertType.LLM_TIMEOUT,
        level=AlertLevel.HIGH,
        message="[doancuong] Test from existing API",
        context={"test": True}
    )
    assert result == True
    print("[OK] send_alert() with old signature works")
    
    # Test 3: AlertType and AlertLevel still work
    assert AlertType.LLM_TIMEOUT in AlertType
    assert AlertLevel.HIGH in AlertLevel
    print("[OK] AlertType and AlertLevel enums work")
    
    # Test 4: All existing alert types still exist
    existing_types = [
        AlertType.UNHANDLED_EXCEPTION,
        AlertType.APP_STARTUP_FAILURE,
        AlertType.POSTGRES_CONNECTION_FAILURE,
        AlertType.REDIS_CONNECTION_FAILURE,
        AlertType.LLM_TIMEOUT,
        AlertType.LLM_BOTH_FAILED,
        AlertType.WORKFLOW_EXECUTION_FAILURE,
        AlertType.AGENT_EXECUTION_FAILURE,
        AlertType.KAFKA_PRODUCER_FAILURE,
        AlertType.EXTERNAL_API_TIMEOUT,
        AlertType.RATE_LIMIT_EXCEEDED,
        AlertType.HIGH_API_RESPONSE_TIME,  # Legacy
    ]
    
    for alert_type in existing_types:
        assert alert_type in AlertType
    
    print(f"[OK] All {len(existing_types)} existing alert types still exist")
    
    print("\n[SUCCESS] Backward compatibility verified!")


if __name__ == "__main__":
    asyncio.run(test_existing_api())

