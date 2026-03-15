# MECE Alert Tests - Test Coverage Documentation

**Date:** 2025-01-XX
**Status:** ✅ **COMPLETE - 47/47 Alert Types Covered**

---

## 📊 TỔNG QUAN

### Test Scripts:

1. **`test_mcee_all_alerts.py`** - Test tất cả 47 alert types theo MECE framework ✅
2. **`test_error_alerts.py`** - Test một số error alerts cơ bản
3. **`test_new_architecture.py`** - Test architecture components
4. **`test_backward_compatibility.py`** - Test backward compatibility

---

## 🎯 TEST COVERAGE

### `test_mcee_all_alerts.py` - MECE Complete Coverage

**Coverage:** ✅ **47/47 alert types (100%)**

#### Layer 1: INPUT LAYER (7/7) ✅

- ✅ `API_REQUEST_TIMEOUT`
- ✅ `INVALID_REQUEST_PAYLOAD`
- ✅ `AUTH_FAILURE`
- ✅ `RATE_LIMIT_EXCEEDED`
- ✅ `PAYLOAD_SIZE_EXCEEDED`
- ✅ `INVALID_JSON_FORMAT`
- ✅ `MISSING_REQUIRED_FIELDS`

#### Layer 2: PROCESSING LAYER (17/17) ✅

- ✅ `LLM_TIMEOUT`
- ✅ `LLM_BOTH_FAILED`
- ✅ `LLM_RATE_LIMIT`
- ✅ `LLM_TOKEN_LIMIT_EXCEEDED`
- ✅ `LLM_INVALID_API_KEY`
- ✅ `LLM_MALFORMED_RESPONSE`
- ✅ `LLM_PROVIDER_DOWN`
- ✅ `LLM_CONTEXT_OVERFLOW`
- ✅ `LLM_STREAMING_ERROR`
- ✅ `WORKFLOW_EXECUTION_FAILURE`
- ✅ `WORKFLOW_TIMEOUT`
- ✅ `WORKFLOW_STATE_ERROR`
- ✅ `WEBHOOK_PROCESSING_FAILURE`
- ✅ `AGENT_EXECUTION_FAILURE`
- ✅ `AGENT_TIMEOUT`
- ✅ `AGENT_NOT_FOUND`
- ✅ `AGENT_INVALID_OUTPUT`

#### Layer 3: OUTPUT LAYER (7/7) ✅

- ✅ `REDIS_OPERATION_TIMEOUT`
- ✅ `REDIS_WRITE_FAILURE`
- ✅ `POSTGRES_WRITE_FAILURE`
- ✅ `KAFKA_PRODUCER_FAILURE`
- ✅ `KAFKA_SEND_TIMEOUT`
- ✅ `RESPONSE_SERIALIZATION_ERROR`
- ✅ `RESPONSE_SIZE_EXCEEDED`

#### Layer 4: DEPENDENCY LAYER (7/7) ✅

- ✅ `POSTGRES_CONNECTION_FAILURE`
- ✅ `POSTGRES_POOL_EXHAUSTED`
- ✅ `POSTGRES_QUERY_TIMEOUT`
- ✅ `REDIS_CONNECTION_FAILURE`
- ✅ `REDIS_POOL_EXHAUSTED`
- ✅ `EXTERNAL_API_TIMEOUT`
- ✅ `EXTERNAL_API_ERROR`

#### Layer 5: INFRASTRUCTURE LAYER (5/5) ✅

- ✅ `HIGH_MEMORY_USAGE`
- ✅ `HIGH_CPU_USAGE`
- ✅ `DISK_SPACE_LOW`
- ✅ `HIGH_NETWORK_LATENCY`
- ✅ `CONTAINER_UNHEALTHY`

#### Layer 6: SECURITY LAYER (3/3) ✅

- ✅ `AUTH_BRUTE_FORCE`
- ✅ `SUSPICIOUS_ACTIVITY`
- ✅ `DATA_LEAKAGE_DETECTED`

#### Layer 7: OPERATIONAL LAYER (2/2) ✅

- ✅ `UNHANDLED_EXCEPTION`
- ✅ `APP_STARTUP_FAILURE`

---

## 🚀 CÁCH CHẠY TESTS

### 1. Test MECE All Alerts (47 types)

```bash
python tests/alert_test/test_mcee_all_alerts.py
```

**Output:**

- Test từng layer
- Summary cho mỗi layer
- Overall summary với success rate

### 2. Test Error Alerts

```bash
python tests/alert_test/test_error_alerts.py
```

### 3. Test New Architecture

```bash
python tests/alert_test/test_new_architecture.py
```

### 4. Test Backward Compatibility

```bash
python tests/alert_test/test_backward_compatibility.py
```

---

## 📝 TEST CASE STRUCTURE

Mỗi test case trong `test_mcee_all_alerts.py` có structure:

```python
AlertType.ALERT_NAME: {
    "level": AlertLevel.LEVEL,
    "message": "[doancuong] Alert message.",
    "context": {
        "key1": "value1",
        "key2": "value2",
        # ... context data
    }
}
```

**Ví dụ:**

```python
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
}
```

---

## ✅ VERIFICATION

### Sau khi chạy test:

1. **Check console output:**

   - Tất cả alerts phải show `[OK]`
   - Success rate phải = 100%
2. **Check Google Chat:**

   - Tất cả 47 alerts phải được gửi đến Google Chat
   - Mỗi alert có format đúng với context data
3. **Check logs:**

   - Không có errors trong logs
   - Rate limiting và deduplication hoạt động đúng

---

## 📊 EXPECTED RESULTS

### Success Output:

```
============================================================
TESTING MECE ALL ALERTS (47 types)
============================================================

============================================================
Testing Layer 1: INPUT LAYER
============================================================
  [OK] api_request_timeout
  [OK] invalid_request_payload
  [OK] auth_failure
  ...

============================================================
MECE TEST SUMMARY
============================================================

Layer 1: INPUT LAYER:
  Total: 7
  Passed: 7
  Failed: 0

...

============================================================
OVERALL SUMMARY
============================================================
Total Alert Types: 47
Passed: 47
Failed: 0
Success Rate: 100.0%

[SUCCESS] ALL MECE ALERT TESTS PASSED!
[INFO] Check Google Chat to verify alerts were received
============================================================
```

---

## 🔧 TROUBLESHOOTING

### Issue: Test fails với "send_alert returned False"

**Nguyên nhân:** Google Chat webhook không configured hoặc invalid
**Giải pháp:**

- Check `GOOGLE_CHAT_WEBHOOK_URL` trong `.env`
- Verify webhook URL is valid

### Issue: Rate limiting prevents some alerts

**Nguyên nhân:** Rate limiter đang block alerts
**Giải pháp:**

- Đây là expected behavior
- CRITICAL alerts không bị rate limit
- HIGH/MEDIUM alerts có thể bị rate limit sau 5 alerts

### Issue: Some alerts không xuất hiện trong Google Chat

**Nguyên nhân:** Deduplication đang suppress duplicate alerts
**Giải pháp:**

- Đây là expected behavior
- Alerts giống nhau trong 1 phút sẽ bị deduplicate
- Check console logs để verify alerts đã được gửi

---

## 📈 COVERAGE STATISTICS

| Layer                          | Total Types  | Tested       | Coverage          |
| ------------------------------ | ------------ | ------------ | ----------------- |
| **Input Layer**          | 7            | 7            | 100% ✅           |
| **Processing Layer**     | 17           | 17           | 100% ✅           |
| **Output Layer**         | 7            | 7            | 100% ✅           |
| **Dependency Layer**     | 7            | 7            | 100% ✅           |
| **Infrastructure Layer** | 5            | 5            | 100% ✅           |
| **Security Layer**       | 3            | 3            | 100% ✅           |
| **Operational Layer**    | 2            | 2            | 100% ✅           |
| **TOTAL**                | **47** | **47** | **100%** ✅ |

---

## ✅ KẾT LUẬN

- ✅ **100% MECE Coverage** - Tất cả 47 alert types đã được test
- ✅ **Realistic Test Cases** - Mỗi alert có context data phù hợp
- ✅ **Layer Organization** - Tests được organize theo 7 layers
- ✅ **Comprehensive Verification** - Test cả success và failure cases

---

**END OF DOCUMENT**

_Last Updated: 2025-01-XX_
_Status: ✅ COMPLETE - 47/47 Alert Types Covered_



PS D:\GIT\robot-lesson-workflow> python tests/alert_test/test_mcee_all_alerts.py
================================================================================

TESTING MECE ALL ALERTS (47 types)
==================================

============================================================
Testing Layer 1: INPUT LAYER
============================

  [OK] api_request_timeout
  [OK] invalid_request_payload
  [OK] auth_failure
  [OK] rate_limit_exceeded
  [OK] payload_size_exceeded
  [OK] invalid_json_format
  [OK] missing_required_fields

============================================================
Testing Layer 2: PROCESSING LAYER
=================================

Google Chat failed with status 429 (attempt 1/3): {
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}

  [OK] llm_timeout
  [OK] llm_both_failed
  [OK] llm_rate_limit
  [OK] llm_token_limit_exceeded
  [OK] llm_invalid_api_key
  [OK] llm_malformed_response
  [OK] llm_provider_down
Google Chat failed with status 429 (attempt 1/3): {
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}

  [OK] llm_context_overflow
  [OK] llm_streaming_error
  [OK] workflow_execution_failure
  [OK] workflow_timeout
  [OK] workflow_state_error
  [OK] webhook_processing_failure
  [OK] agent_execution_failure
Google Chat failed with status 429 (attempt 1/3): {
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}

  [OK] agent_timeout
  [OK] agent_not_found
  [OK] agent_invalid_output

============================================================
Testing Layer 3: OUTPUT LAYER
=============================

  [OK] redis_operation_timeout
  [OK] redis_write_failure
  [OK] postgres_write_failure
  [OK] kafka_producer_failure
  [OK] kafka_send_timeout
  [OK] response_serialization_error
  [OK] response_size_exceeded

============================================================
Testing Layer 4: DEPENDENCY LAYER
=================================

  [OK] postgres_connection_failure
  [OK] postgres_pool_exhausted
  [OK] postgres_query_timeout
  [OK] redis_connection_failure
Google Chat failed with status 429 (attempt 1/3): {
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}

  [OK] redis_pool_exhausted
  [OK] external_api_timeout
  [OK] external_api_error

============================================================
Testing Layer 5: INFRASTRUCTURE LAYER
=====================================

  [OK] high_memory_usage
  [OK] high_cpu_usage
  [OK] disk_space_low
  [OK] high_network_latency
Google Chat failed with status 429 (attempt 1/3): {
  "error": {
    "code": 429,
    "message": "Resource has been exhausted (e.g. check quota).",
    "status": "RESOURCE_EXHAUSTED"
  }
}

  [OK] container_unhealthy

============================================================
Testing Layer 6: SECURITY LAYER
===============================

  [OK] auth_brute_force
  [OK] suspicious_activity
  [OK] data_leakage_detected

============================================================
Testing Layer 7: OPERATIONAL LAYER
==================================

  [OK] unhandled_exception
  [OK] app_startup_failure

============================================================
MECE TEST SUMMARY
=================

Layer 1: INPUT LAYER:
  Total: 7
  Passed: 7
  Failed: 0

Layer 2: PROCESSING LAYER:
  Total: 17
  Passed: 17
  Failed: 0

Layer 3: OUTPUT LAYER:
  Total: 7
  Passed: 7
  Failed: 0

Layer 4: DEPENDENCY LAYER:
  Total: 7
  Passed: 7
  Failed: 0

Layer 5: INFRASTRUCTURE LAYER:
  Total: 5
  Passed: 5
  Failed: 0

Layer 6: SECURITY LAYER:
  Total: 3
  Passed: 3
  Failed: 0

Layer 7: OPERATIONAL LAYER:
  Total: 2
  Passed: 2
  Failed: 0

============================================================
OVERALL SUMMARY
===============

Total Alert Types: 48
Passed: 48
Failed: 0
Success Rate: 100.0%

[SUCCESS] ALL MECE ALERT TESTS PASSED!
[INFO] Check Google Chat to verify alerts were received
=======================================================

PS D:\GIT\robot-lesson-workflow>

---

Đang phân tích các test hiện tại và tạo test script để cover MECE (47 alert types):

[3 tools called]

Đang tạo test script để cover MECE (47 alert types):

[1 tool called]

Đang kiểm tra lỗi và tạo README cho test:

[2 tools called]

Đã tạo test script để giả lập MECE cho tất cả 47 alert types.

## Đã tạo

### 1. `test_mcee_all_alerts.py` — Test script chính

Coverage: 47/47 alert types (100%)

Tính năng:

- Test tất cả 47 alert types theo 7 layers
- Mỗi alert có test case với context data phù hợp
- Tổ chức theo layers: Input, Processing, Output, Dependency, Infrastructure, Security, Operational
- Summary report cho từng layer và tổng thể

Cấu trúc:

```python
TEST_CASES = {
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
    # ... 46 alert types khác
}
```

---

## Cách chạy

```bash
python tests/alert_test/test_mcee_all_alerts.py
```

Output:

- Test từng layer (7 layers)
- Summary cho mỗi layer
- Overall summary với success rate
- Verification trong Google Chat

---

## Test coverage

| Layer                          | Types           | Status           |
| ------------------------------ | --------------- | ---------------- |
| **Input Layer**          | 7/7             | ✅               |
| **Processing Layer**     | 17/17           | ✅               |
| **Output Layer**         | 7/7             | ✅               |
| **Dependency Layer**     | 7/7             | ✅               |
| **Infrastructure Layer** | 5/5             | ✅               |
| **Security Layer**       | 3/3             | ✅               |
| **Operational Layer**    | 2/2             | ✅               |
| **TOTAL**                | **47/47** | ✅**100%** |

---

## So sánh với test cũ

| Test File                          | Coverage     | Mục đích                 |
| ---------------------------------- | ------------ | --------------------------- |
| `test_mcee_all_alerts.py`        | 47/47 (100%) | Test MECE đầy đủ        |
| `test_error_alerts.py`           | ~8 types     | Test một số error alerts  |
| `test_new_architecture.py`       | Components   | Test architecture           |
| `test_backward_compatibility.py` | API          | Test backward compatibility |

---

## Kết luận

- 100% MECE coverage — tất cả 47 alert types
- Test cases có context data phù hợp
- Tổ chức theo 7 layers
- Summary report chi tiết

Bạn có muốn tôi chạy test để verify không?

---

Đang đọc file test backward compatibility để giải thích:

[3 tools called]

## Test backward compatibility là gì?

Test backward compatibility đảm bảo code cũ vẫn hoạt động sau khi refactor hệ thống alert.

---

## Vấn đề

Khi refactor alert system:

- Cũ: Code đơn giản, gọi trực tiếp `get_alert_manager().send_alert()`
- Mới: Architecture SOLID với `AlertContext`, `Transport`, `Formatter`, `RateLimiter`, `Deduplicator`

Nếu không có backward compatibility:

- Code cũ sẽ bị lỗi
- Phải sửa toàn bộ codebase
- Rủi ro breaking changes

---

## Giải pháp: Backward compatibility

Đảm bảo API cũ vẫn hoạt động:

### 1. `get_alert_manager()` vẫn hoạt động

```python
# Code cũ (vẫn hoạt động)
manager = get_alert_manager()
result = await manager.send_alert(
    alert_type=AlertType.LLM_TIMEOUT,
    level=AlertLevel.HIGH,
    message="[doancuong] Test",
    context={"test": True}
)
```

### 2. `send_alert()` với signature cũ vẫn hoạt động

```python
# Signature cũ (vẫn hoạt động)
await manager.send_alert(
    alert_type=AlertType.LLM_TIMEOUT,
    level=AlertLevel.HIGH,
    message="[doancuong] Test",
    context={"test": True}
    # Không cần request_id, conversation_id (optional)
)
```

### 3. Legacy alert types vẫn tồn tại

```python
# Legacy types (vẫn hoạt động)
AlertType.HIGH_API_RESPONSE_TIME  # → API_REQUEST_TIMEOUT
AlertType.SLOW_DATABASE_QUERY     # → POSTGRES_QUERY_TIMEOUT
```

### 4. `GoogleChatClient` vẫn export

```python
# Code cũ có thể import (vẫn hoạt động)
from app.common.alerts import GoogleChatClient
```

---

## Test này kiểm tra gì?

File `test_backward_compatibility.py` test 4 điều:

### Test 1: `get_alert_manager()` vẫn hoạt động

```python
manager = get_alert_manager()
assert manager is not None
```

### Test 2: `send_alert()` với signature cũ vẫn hoạt động

```python
result = await manager.send_alert(
    alert_type=AlertType.LLM_TIMEOUT,
    level=AlertLevel.HIGH,
    message="[doancuong] Test from existing API",
    context={"test": True}
)
assert result == True
```

### Test 3: `AlertType` và `AlertLevel` enums vẫn hoạt động

```python
assert AlertType.LLM_TIMEOUT in AlertType
assert AlertLevel.HIGH in AlertLevel
```

### Test 4: Tất cả alert types cũ vẫn tồn tại

```python
existing_types = [
    AlertType.UNHANDLED_EXCEPTION,
    AlertType.APP_STARTUP_FAILURE,
    AlertType.POSTGRES_CONNECTION_FAILURE,
    # ... 12 types khác
]
for alert_type in existing_types:
    assert alert_type in AlertType
```

---

## Tại sao quan trọng?

1. Không breaking changes: Code cũ không cần sửa
2. Migration dễ dàng: Có thể migrate từ từ
3. An toàn: Không ảnh hưởng production code
4. Flexibility: Có thể dùng API cũ hoặc mới

---

## So sánh

| Aspect                  | Code cũ                             | Code mới                          |
| ----------------------- | ------------------------------------ | ---------------------------------- |
| **API**           | `get_alert_manager().send_alert()` | `send_alert_safe()` helper       |
| **Architecture**  | Simple                               | SOLID (Transport, Formatter, etc.) |
| **Compatibility** | ✅ Vẫn hoạt động                 | ✅ Có thể dùng                  |

---

## Kết luận

Test backward compatibility đảm bảo:

- Code cũ vẫn chạy sau khi refactor
- Không cần sửa code hiện tại
- Có thể migrate dần sang API mới
- An toàn cho production

Tóm lại: Đảm bảo hệ thống mới không làm hỏng code cũ.
