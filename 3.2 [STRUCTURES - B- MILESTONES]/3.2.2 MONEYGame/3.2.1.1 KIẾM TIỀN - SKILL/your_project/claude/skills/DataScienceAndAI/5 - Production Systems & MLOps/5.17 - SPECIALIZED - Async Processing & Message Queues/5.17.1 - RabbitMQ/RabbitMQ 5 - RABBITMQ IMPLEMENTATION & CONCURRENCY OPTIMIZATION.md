## 8. RABBITMQ IMPLEMENTATION & CONCURRENCY OPTIMIZATION

### 8.1 Event-Driven Flow (202 Accepted Pattern)

Để đảm bảo API trả về phản hồi nhanh chóng (< 100ms), chúng ta áp dụng mô hình **202 Accepted** với RabbitMQ.

**Luồng Xử Lý Mới:**

```
API nhận request → Lưu DB (status=PENDING) → Publish to queue → Return 202 ngay
Queue → Worker consume → Xử lý ở background
```

#### 8.1.1 Cập Nhật API Endpoint (`POST /v1/conversations/end`)

Endpoint sẽ chỉ thực hiện 3 bước: Lưu DB, Publish message, và Trả về 202.

```python
from app.background.rabbitmq_publisher import publish_conversation_event

@router.post("/conversations/end", status_code=202)
async def conversation_end(
    request: ConversationEndRequest,
    service: ConversationEventService = Depends(get_conversation_event_service)
):
    """
    Endpoint để nhận conversation end event.
    - Lưu vào DB (status=PENDING)
    - Publish to RabbitMQ queue
    - Return 202 Accepted ngay (không đợi xử lý)
    """
    try:
        # STEP 1: Create event (lưu vào DB, status=PENDING)
        event = service.create_event_without_processing(request)
      
        # STEP 2: Publish to RabbitMQ queue
        await publish_conversation_event(
            conversation_id=event.conversation_id,
            user_id=event.user_id,
            bot_id=event.bot_id,
            conversation_log=event.conversation_log
        )
      
        # STEP 3: Return 202 Accepted (ngay, không đợi)
        return {
            "status": "accepted",
            "message": "Conversation event accepted for processing",
            "conversation_id": event.conversation_id,
            "event_id": event.id
        }
  
    except Exception as e:
        logger.error(f"Error in conversation_end: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 8.2 RabbitMQ Publisher & Consumer Implementation

#### 8.2.1 Publisher (`rabbitmq_publisher.py`)

Sử dụng `pika.BlockingConnection` để đảm bảo tính đồng bộ và đơn giản trong việc publish từ API.

**Cấu hình Queue:**
- `QUEUE_NAME`: `conversation_events_processing`
- `durable=True`: Đảm bảo queue không bị mất khi RabbitMQ restart.
- `delivery_mode=2`: Message được lưu trữ trên đĩa (persistent) để không bị mất.

#### 8.2.2 Consumer (Worker) (`rabbitmq_consumer.py`)

Worker sẽ consume message, lấy event từ DB, xử lý logic (tính score, update DB), và ACK/NACK message.

**QoS (Quality of Service):**
- Mặc định: `self.channel.basic_qos(prefetch_count=1)` (xử lý tuần tự).
- **Cập nhật cho Production:** Sẽ được tối ưu hóa ở mục 8.3.

**Xử lý Lỗi và Retry:**
- **Thành công:** `ch.basic_ack(delivery_tag=method.delivery_tag)`
- **Thất bại:** `ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)` (đưa message vào lại queue để retry).

### 8.3 Concurrency Optimization & Worker Sizing

Tác vụ xử lý event là **Hybrid (CPU-bound: tính score + I/O-bound: DB update)**. Để tối ưu hóa throughput, chúng ta cần tăng concurrency.

#### 8.3.1 Vấn Đề Blocking của Pika

Worker hiện tại sử dụng `pika.BlockingConnection` và xử lý logic tuần tự trong `callback`. Khi `prefetch_count` > 1, worker sẽ nhận nhiều message nhưng vẫn xử lý chúng **tuần tự** trên một thread duy nhất, dẫn đến message bị backlog trong bộ nhớ đệm của worker.

#### 8.3.2 Giải Pháp Tăng Concurrency

**A. Tăng Số Lượng Worker Process (W)**
Đây là phương pháp hiệu quả nhất, mỗi worker là một process độc lập, chạy trên một core CPU.

**Cập Nhật Docker Compose:**
Sử dụng `deploy: replicas` để chạy nhiều worker process.

```yaml
# File: docker-compose.yml
services:
  worker:
    # ...
    deploy:
      replicas: 8  # Ví dụ: Chạy 8 worker process
    command: python src/worker.py
    # ...
```

**B. Tăng `prefetch_count` (C)**
Chỉ tăng `prefetch_count` khi worker được cấu hình để xử lý song song (ví dụ: dùng `multiprocessing` hoặc `asyncio` với `pika.AsyncioConnection`).
Với cấu hình `pika.BlockingConnection` hiện tại, **nên giữ `prefetch_count` thấp (ví dụ: 1-5)** để tránh quá tải bộ nhớ đệm.

```python
# File: src/app/background/rabbitmq_consumer.py
# Cấu hình cho Production (nếu worker được tối ưu hóa)
CONCURRENCY_PER_WORKER = 10 
self.channel.basic_qos(prefetch_count=CONCURRENCY_PER_WORKER) 
```

#### 8.3.3 Công Thức Tối Ưu Worker Sizing

Số lượng worker tối ưu phụ thuộc vào phần cứng (N core CPU) và loại tác vụ (Hybrid).

| Yếu Tố | Mô Tả | Công Thức Bắt Đầu |
| :--- | :--- | :--- |
| **Worker Process (W)** | Số lượng process độc lập | $W \approx 2N$ (Với tác vụ Hybrid) |
| **Concurrency (C)** | `prefetch_count` | $C = 5 \text{ đến } 10$ |
| **Tổng Concurrency** | $W \times C$ | $2N \times 10$ |

**Ví dụ:** Server 4 core CPU ($N=4$).
- **Worker Process (W):** $2 \times 4 = 8$
- **Concurrency (C):** $10$
- **Tổng Concurrency:** $8 \times 10 = 80$ message cùng lúc.
