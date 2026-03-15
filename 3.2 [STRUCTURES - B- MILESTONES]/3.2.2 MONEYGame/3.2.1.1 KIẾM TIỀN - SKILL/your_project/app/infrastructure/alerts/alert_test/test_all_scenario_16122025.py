"""
Test script cho TOÀN BỘ các alert liên quan đến SCENARIO

Mục đích:
    - Verify các alert MECE cho scenario đã implement:
        + SCENARIO_VALIDATION_ERROR (nhiều subtype)
        + WORKFLOW_STATE_ERROR (scenario_state_invalid)
        + WORKFLOW_EXECUTION_FAILURE (scenario_* trong format/profile)

Usage:
    python -m tests.alert_test.test_all_scenario_16122025
    # hoặc
    python tests/alert_test/test_all_scenario_16122025.py
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()  # Load .env file từ project root

from app.common.alerts import get_alert_manager, AlertType, AlertLevel  # noqa: E402


async def _get_alert_manager():
    """Helper: khởi tạo AlertManager từ GOOGLE_CHAT_WEBHOOK_URL."""
    webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
    if not webhook_url:
        print("❌ GOOGLE_CHAT_WEBHOOK_URL not found in .env")
        print("   Vui lòng cấu hình GOOGLE_CHAT_WEBHOOK_URL trước khi chạy test.")
        return None
    print(f"\n🔗 Webhook URL: {webhook_url[:60]}...")
    return get_alert_manager(webhook_url=webhook_url)


async def test_scenario_not_found():
    """SCENARIO_VALIDATION_ERROR - scenario_not_found (CRITICAL)"""
    print("\n" + "=" * 60)
    print("TEST 1: SCENARIO_NOT_FOUND (SCENARIO_VALIDATION_ERROR - CRITICAL)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    success = await alert_manager.send_alert(
        alert_type=AlertType.SCENARIO_VALIDATION_ERROR,
        level=AlertLevel.CRITICAL,
        message="[doancuong][scenario] Scenario is missing in bot configuration.",
        context={
            "bot_id": 999999,
            "conversation_id": "test_scn_not_found",
            "error_type": "scenario_not_found",
        },
    )

    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_scenario_parsing_error():
    """SCENARIO_VALIDATION_ERROR - scenario_parsing_error (CRITICAL)"""
    print("\n" + "=" * 60)
    print("TEST 2: SCENARIO_PARSING_ERROR (SCENARIO_VALIDATION_ERROR - CRITICAL)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    success = await alert_manager.send_alert(
        alert_type=AlertType.SCENARIO_VALIDATION_ERROR,
        level=AlertLevel.CRITICAL,
        message="[doancuong][scenario] Scenario JSON parsing error from bot configuration.",
        context={
            "bot_id": 12345,
            "conversation_id": "test_scn_parsing_error",
            "error_type": "scenario_parsing_error",
            "error": "Expecting ',' delimiter: line 1 column 42 (char 41)",
        },
    )

    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_scenario_invalid_type_and_empty():
    """SCENARIO_VALIDATION_ERROR - scenario_invalid_type + scenario_empty (HIGH)"""
    print("\n" + "=" * 60)
    print("TEST 3: SCENARIO_INVALID_TYPE / SCENARIO_EMPTY (SCENARIO_VALIDATION_ERROR - HIGH)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    results = []

    # 3A. Invalid type
    success_invalid_type = await alert_manager.send_alert(
        alert_type=AlertType.SCENARIO_VALIDATION_ERROR,
        level=AlertLevel.HIGH,
        message="[doancuong][scenario] Scenario type is invalid (must be list).",
        context={
            "bot_id": 12346,
            "conversation_id": "test_scn_invalid_type",
            "error_type": "scenario_invalid_type",
            "parsed_type": "<class 'dict'>",
        },
    )
    results.append(success_invalid_type)

    # 3B. Empty scenario
    success_empty = await alert_manager.send_alert(
        alert_type=AlertType.SCENARIO_VALIDATION_ERROR,
        level=AlertLevel.HIGH,
        message="[doancuong][scenario] Scenario is empty.",
        context={
            "bot_id": 12347,
            "conversation_id": "test_scn_empty",
            "error_type": "scenario_empty",
        },
    )
    results.append(success_empty)

    all_ok = all(results)
    print(f"✅ Result: {'Success' if all_ok else 'Failed'}")
    return all_ok


async def test_scenario_link_sanitization():
    """SCENARIO_VALIDATION_ERROR - invalid special chars in link (MEDIUM)"""
    print("\n" + "=" * 60)
    print("TEST 4: SCENARIO_INVALID_SPECIAL_CHARS_IN_LINK (SCENARIO_VALIDATION_ERROR - MEDIUM)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    success = await alert_manager.send_alert(
        alert_type=AlertType.SCENARIO_VALIDATION_ERROR,
        level=AlertLevel.MEDIUM,
        message="[doancuong][scenario] Scenario link contained invalid characters and was sanitized.",
        context={
            "field": "IMAGE",
            "original_preview": "https://example.com/image\u200b!.png",
            "cleaned_preview": "https://example.com/image.png",
            "error_type": "scenario_invalid_special_chars_in_link",
        },
    )

    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_scenario_state_invalid():
    """WORKFLOW_STATE_ERROR - scenario_state_invalid (MEDIUM)"""
    print("\n" + "=" * 60)
    print("TEST 5: SCENARIO_STATE_INVALID (WORKFLOW_STATE_ERROR - MEDIUM)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    success = await alert_manager.send_alert(
        alert_type=AlertType.WORKFLOW_STATE_ERROR,
        level=AlertLevel.MEDIUM,
        message="[doancuong][scenario] Workflow state is invalid for given scenario.",
        context={
            "error_type": "scenario_state_invalid",
            "cur_state": 10,
            "scenario_length": 5,
            "conversation_id": "test_scn_state_invalid",
        },
    )

    print(f"✅ Result: {'Success' if success else 'Failed'}")
    return success


async def test_scenario_format_and_preprocess_errors():
    """WORKFLOW_EXECUTION_FAILURE - scenario_preprocessing_error + scenario_format_error (MEDIUM)"""
    print("\n" + "=" * 60)
    print("TEST 6: SCENARIO_PREPROCESSING_ERROR / SCENARIO_FORMAT_ERROR (WORKFLOW_EXECUTION_FAILURE - MEDIUM)")
    print("=" * 60)

    alert_manager = await _get_alert_manager()
    if not alert_manager:
        return False

    results = []

    # 6A. preprocess_scenario error
    success_preprocess = await alert_manager.send_alert(
        alert_type=AlertType.WORKFLOW_EXECUTION_FAILURE,
        level=AlertLevel.MEDIUM,
        message="[doancuong][scenario] Scenario preprocessing failed, falling back to original scenario.",
        context={
            "error_type": "scenario_preprocessing_error",
            "conversation_id": "test_scn_preprocess",
        },
    )
    results.append(success_preprocess)

    # 6B. update_data_from_profile error
    success_format = await alert_manager.send_alert(
        alert_type=AlertType.WORKFLOW_EXECUTION_FAILURE,
        level=AlertLevel.MEDIUM,
        message="[doancuong][scenario] Scenario update_data_from_profile failed, falling back to original data.",
        context={
            "error_type": "scenario_format_error",
            "conversation_id": "test_scn_format",
        },
    )
    results.append(success_format)

    all_ok = all(results)
    print(f"✅ Result: {'Success' if all_ok else 'Failed'}")
    return all_ok


async def run_all_scenario_tests():
    """Run all scenario-related alert tests."""
    print("\n" + "🎭" * 30)
    print("SCENARIO ALERTS TEST SUITE - 16/12/2025")
    print("Testing ALL scenario-related alerts (validation + workflow)")
    print("🎭" * 30)

    results = []

    results.append(("SCENARIO_NOT_FOUND", await test_scenario_not_found()))
    await asyncio.sleep(1)

    results.append(("SCENARIO_PARSING_ERROR", await test_scenario_parsing_error()))
    await asyncio.sleep(1)

    results.append(("SCENARIO_INVALID_TYPE/EMPTY", await test_scenario_invalid_type_and_empty()))
    await asyncio.sleep(1)

    results.append(("SCENARIO_INVALID_SPECIAL_CHARS_IN_LINK", await test_scenario_link_sanitization()))
    await asyncio.sleep(1)

    results.append(("SCENARIO_STATE_INVALID", await test_scenario_state_invalid()))
    await asyncio.sleep(1)

    results.append(("SCENARIO_PREPROCESSING/FORMAT_ERROR", await test_scenario_format_and_preprocess_errors()))

    # Summary
    print("\n" + "=" * 60)
    print("SCENARIO ALERTS TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, r in results:
        status = "✅ PASSED" if r else "❌ FAILED"
        print(f"   {status}: {name}")

    print(f"\n📈 Total: {passed}/{total} tests passed ({passed * 100 // total}%)")
    if passed == total:
        print("\n🎉 All scenario alert tests passed! Check Google Chat room để verify thông điệp.")
    else:
        print("\n⚠️ Một số scenario tests FAILED. Vui lòng kiểm tra lại cấu hình webhook / alert.")

    print("\n" + "=" * 60)
    print("✅ Scenario alert test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_scenario_tests())


