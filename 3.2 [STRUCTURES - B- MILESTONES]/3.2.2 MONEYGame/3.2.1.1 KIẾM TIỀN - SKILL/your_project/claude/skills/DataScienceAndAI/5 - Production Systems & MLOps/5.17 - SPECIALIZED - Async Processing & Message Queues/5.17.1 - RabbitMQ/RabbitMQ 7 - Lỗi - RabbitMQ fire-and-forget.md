> 25.12.2025

Đang xem code hiện tại để giải thích "RabbitMQ fire-and-forget" trong ngữ cảnh của bạn.

[3 tools called]

## 🔥 "Fire-and-Forget" là gì?

Fire-and-forget = gửi đi và không chờ kết quả. API trả response ngay, còn việc publish vào RabbitMQ chạy nền.

---

## 📊 So sánh: Hiện tại vs Fire-and-Forget

### ❌ Cách hiện tại (blocking - đang gây timeout):

```81:86:src/app/api/v1/endpoints/endpoint_conversation_events.py
        publish_success = await publish_conversation_event(
            conversation_id=data["conversation_id"],
            user_id=data["user_id"],
            bot_id=data["bot_id"],
            conversation_log=data.get("conversation_log", [])
        )
```

Luồng hiện tại:

1. Client gọi `/conversations/end`
2. API lưu vào DB (OK)
3. API gọi `await publish_conversation_event()` → chờ RabbitMQ publish xong
4. Nếu RabbitMQ chậm/down → API bị block → timeout → 504
5. Client nhận 504

Vấn đề: API phụ thuộc vào RabbitMQ, nếu RabbitMQ chậm/down thì API bị block.

---

### ✅ Fire-and-Forget (non-blocking - đề xuất):

```python
# STEP 2: Publish to RabbitMQ queue (FIRE-AND-FORGET)
logger.debug(f"📤 Publishing to RabbitMQ queue: {final_conversation_id}")

# ✅ KHÔNG await - schedule task trong background
try:
    asyncio.create_task(
        publish_conversation_event(
            conversation_id=data["conversation_id"],
            user_id=data["user_id"],
            bot_id=data["bot_id"],
            conversation_log=data.get("conversation_log", [])
        )
    )
    logger.info(f"✅ Scheduled publish (async)")
except Exception as e:
    logger.warning(f"⚠️  Queue publish failed (async): {str(e)}")
    # KHÔNG fail API - background scheduler sẽ retry

# STEP 3: Return 202 ngay lập tức (< 100ms)
return ConversationEventCreateResponse(...)
```

Luồng mới:

1. Client gọi `/conversations/end`
2. API lưu vào DB (OK)
3. API schedule task publish vào RabbitMQ (không chờ)
4. API trả 202 ngay (< 100ms)
5. Client nhận 202
6. RabbitMQ publish chạy nền (thành công hay lỗi không ảnh hưởng response)

Lợi ích: API không bị block bởi RabbitMQ, response nhanh, RabbitMQ lỗi không làm API fail.

---

## 🎯 Tại sao quan trọng trong trường hợp 3h sáng bị spam?

Khi có service khác spam call:

### ❌ Với blocking (hiện tại):

```
Request 1 → DB OK → RabbitMQ đang chậm (5s) → chờ...
Request 2 → DB OK → RabbitMQ đang chậm (5s) → chờ...
Request 3 → DB OK → RabbitMQ đang chậm (5s) → chờ...
...
Request 100 → DB OK → RabbitMQ timeout → 504
→ Tất cả requests bị block → Service sập
```

### ✅ Với fire-and-forget:

```
Request 1 → DB OK → Schedule RabbitMQ → Trả 202 (< 100ms) ✅
Request 2 → DB OK → Schedule RabbitMQ → Trả 202 (< 100ms) ✅
Request 3 → DB OK → Schedule RabbitMQ → Trả 202 (< 100ms) ✅
...
Request 100 → DB OK → Schedule RabbitMQ → Trả 202 (< 100ms) ✅

→ RabbitMQ publish chạy nền, không block API
→ Service vẫn hoạt động bình thường
```

---

## 🔍 Chi tiết implementation

Trong file `P0_ContextHandling_Risk.md`, action 1.4 đề xuất:

```129:161:docs/4_TimeOut_Fallback_Alert/P0_ContextHandling_Risk.md
import asyncio
from app.background.rabbitmq_publisher import publish_conversation_event

# STEP 2: Publish to RabbitMQ queue for async processing (FIRE-AND-FORGET)
logger.debug(f"📤 Publishing to RabbitMQ queue: {final_conversation_id}")

# ✅ CHANGE: Fire-and-forget instead of await
try:
    # Schedule publish in background, don't wait
    asyncio.create_task(
        publish_conversation_event(
            conversation_id=data["conversation_id"],
            user_id=data["user_id"],
            bot_id=data["bot_id"],
            conversation_log=data.get("conversation_log", [])
        )
    )
    logger.info(
        f"{success('✅ Published to queue (async)')} | "
        f"{key_value('conversation_id', final_conversation_id)}"
    )
except Exception as e:
    # Don't fail API if publish fails - background scheduler will retry
    logger.warning(
        f"{warning('⚠️  Queue publish failed (async)')} | "
        f"{key_value('conversation_id', final_conversation_id)} | "
        f"error={str(e)} | Event saved to DB (PENDING), scheduler will retry"
    )
```

Điểm chính:

- `asyncio.create_task()`: tạo task chạy nền, không chờ
- Không `await`: không block API
- Try/except: nếu lỗi chỉ log warning, không fail API
- Background scheduler: sẽ retry các event PENDING trong DB sau

---

## 📝 Tóm tắt

| Khía cạnh         | Blocking (hiện tại)                 | Fire-and-Forget (đề xuất) |
| ------------------- | ------------------------------------- | ---------------------------- |
| Response time       | Phụ thuộc RabbitMQ (có thể 5-30s) | < 100ms                      |
| Khi RabbitMQ chậm  | API bị block → timeout              | API vẫn OK                  |
| Khi RabbitMQ down   | API trả 504                          | API vẫn OK, log warning     |
| Resilience          | Thấp                                 | Cao                          |
| Phù hợp spam call | Không                                | Có                          |

Bạn muốn mình implement thay đổi này không?