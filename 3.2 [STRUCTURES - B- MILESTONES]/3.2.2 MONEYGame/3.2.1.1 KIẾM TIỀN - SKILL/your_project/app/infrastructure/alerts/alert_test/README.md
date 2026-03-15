# Alert Test Module

## 📋 Mục Đích

Folder này chứa các test scripts cho Alert System - hệ thống bắn alerts đến Google Chat.

## 📁 Files

1. **`test_alert_system.py`** - Test cơ bản cho alert system
   - Simple text message
   - CRITICAL alert (LLM both failed)
   - HIGH alert (LLM timeout)
   - MEDIUM alert (example)

2. **`test_critical_alerts.py`** - Test đầy đủ cho các critical alerts (Phase 1)
   - PostgreSQL connection failure
   - Redis connection failure
   - Redis operation timeout
   - LLM timeout & both failed
   - Unhandled exception
   - Application startup failure

3. **`test_all_alerts.py`** - ⭐ Test COMPREHENSIVE cho TẤT CẢ alerts (Phase 1 + 2 + 3)
   - **Phase 1**: 5 CRITICAL alerts
   - **Phase 2**: 6 HIGH priority alerts
   - **Phase 3**: 4 MEDIUM priority alerts
   - **Tổng cộng**: 15 test cases cho 12+ alert types

## 🚀 Cách Chạy

### Prerequisites

Đảm bảo đã có `GOOGLE_CHAT_WEBHOOK_URL` trong file `.env`:

```env
GOOGLE_CHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/...
```

### Run Tests

```bash
# Test cơ bản
python tests/alert_test/test_alert_system.py

# Test đầy đủ critical alerts (Phase 1)
python tests/alert_test/test_critical_alerts.py

# ⭐ Test COMPREHENSIVE - TẤT CẢ alerts (Phase 1 + 2 + 3) - RECOMMENDED
python tests/alert_test/test_all_alerts.py

# Hoặc dùng module syntax
python -m tests.alert_test.test_alert_system
python -m tests.alert_test.test_critical_alerts
python -m tests.alert_test.test_all_alerts
```

## ✅ Expected Output

Sau khi chạy test, bạn sẽ thấy trong **Google Chat room**:

- Tất cả alerts có prefix `[doancuong]`
- Card format với color coding theo level
- Context information đầy đủ

### Test `test_all_alerts.py` sẽ test:

**Phase 1 (CRITICAL):**
- PostgreSQL Connection Failure
- Redis Connection Failure
- LLM Both Failed
- Unhandled Exception
- App Startup Failure

**Phase 2 (HIGH):**
- Redis Operation Timeout
- LLM Timeout
- LLM Rate Limit
- Kafka Producer Failure
- Workflow Execution Failure
- Agent Execution Failure

**Phase 3 (MEDIUM):**
- External API Timeout
- Database Query Timeout
- High API Response Time
- Rate Limit Exceeded

## 📊 Alert Levels

- **CRITICAL** (🚨): PostgreSQL/Redis connection fail, LLM both failed, Unhandled exception
- **HIGH** (⚠️): LLM timeout, Redis operation timeout
- **MEDIUM** (⚡): Database query timeout, External API timeout

## 🔍 Notes

- Tất cả alerts có prefix `[doancuong]` để dễ nhận biết
- Rate limiting được áp dụng để tránh spam
- Deduplication để group similar alerts trong 1 phút

