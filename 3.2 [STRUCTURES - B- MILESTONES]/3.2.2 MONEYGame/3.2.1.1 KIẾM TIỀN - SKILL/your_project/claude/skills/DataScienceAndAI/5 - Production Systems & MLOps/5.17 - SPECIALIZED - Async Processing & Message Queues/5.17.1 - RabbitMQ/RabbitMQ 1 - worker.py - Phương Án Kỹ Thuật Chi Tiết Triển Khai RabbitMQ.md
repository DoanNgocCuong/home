# Phương Án Kỹ Thuật Chi Tiết: Triển Khai RabbitMQ

## Dựa Trên Kiến Trúc Code Hiện Tại

**Phiên bản:** 3.1 (Realistic)
**Ngày:** 27/11/2025
**Dựa trên:** Kiến trúc code hiện tại + RabbitMQ integration
**Trạng thái:** Sẵn sàng triển khai

---

## 📋 TÓNG QUAN

### Tình Trạng Hiện Tại

```
✅ API Layer: FastAPI endpoints sẵn sàng
✅ Service Layer: Tất cả business logic đã implement
✅ Repository Layer: CRUD operations đã có
✅ Database: PostgreSQL schema đã setup
⚠️  Background Processing: Hiện tại synchronous
❌ RabbitMQ: Chưa có
```

### Mục Tiêu

```
Chuyển từ:
  API nhận request → Xử lý ngay (synchronous) → Return response

Sang:
  API nhận request → Lưu DB → Publish to queue → Return 202 ngay
  Queue → Worker consume → Xử lý ở background
```

---

## 🔄 LUỒNG MỚI (Chi Tiết)

### STEP 1: API Endpoint (Không Thay Đổi Nhiều)

**File:** `src/app/api/v1/endpoints/endpoint_conversation_events.py`

**Hiện Tại:**

```python
@router.post("/conversations/end", status_code=202)
async def conversation_end(
    request: ConversationEndRequest,
    service: ConversationEventService = Depends(get_conversation_event_service)
):
    # 1. Validate
    # 2. Create event
    # 3. Process immediately (SYNCHRONOUS) ← PROBLEM
    # 4. Return response
    result = service.create_event(request)
    return result
```

**Cập Nhật:**

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
        # STEP 1: Validate request
        # (existing code)
      
        # STEP 2: Create event (lưu vào DB, status=PENDING)
        event = service.create_event_without_processing(request)
      
        # STEP 3: Publish to RabbitMQ queue
        await publish_conversation_event(
            conversation_id=event.conversation_id,
            user_id=event.user_id,
            bot_id=event.bot_id,
            conversation_log=event.conversation_log
        )
      
        # STEP 4: Return 202 Accepted (ngay, không đợi)
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

---

### STEP 2: Tách Immediate Processing

**File:** `src/app/services/conversation_event_service.py`

**Hiện Tại:**

```python
class ConversationEventService:
    def create_event(self, request):
        # 1. Validate
        # 2. Transform logs
        # 3. Save to DB
        event = self.repository.create(...)
      
        # 4. Process immediately ← REMOVE THIS
        processor.process_single_event(event.id)
      
        return event
```

**Cập Nhật:**

```python
class ConversationEventService:
    def create_event_without_processing(self, request):
        """
        Chỉ lưu event vào DB, không xử lý ngay.
        Xử lý sẽ được làm bởi background worker từ queue.
        """
        # 1. Validate request
        self._validate_request(request)
      
        # 2. Transform conversation_logs
        transformed_logs = self._transform_conversation_logs(request.conversation_logs)
      
        # 3. Save to DB (status=PENDING)
        event = self.repository.create(
            conversation_id=request.conversation_id,
            user_id=request.user_id,
            bot_id=request.bot_id,
            bot_name=request.bot_name,
            bot_type=request.bot_type,
            conversation_log=transformed_logs,
            raw_conversation_log=request.conversation_logs,
            status="PENDING",
            next_attempt_at=datetime.utcnow() + timedelta(hours=6)
        )
      
        logger.info(f"Created conversation event: {event.conversation_id}")
      
        return event
```

---

### STEP 3: RabbitMQ Publisher

**File:** `src/app/background/rabbitmq_publisher.py` (NEW)

```python
import pika
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RabbitMQConfig:
    HOST = "rabbitmq"  # Docker service name
    PORT = 5672
    USERNAME = "guest"
    PASSWORD = "guest"
    QUEUE_NAME = "conversation_events_processing"
    EXCHANGE_NAME = "conversation_exchange"
    ROUTING_KEY = "conversation.end"

class RabbitMQPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._connect()
  
    def _connect(self):
        """Kết nối đến RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                RabbitMQConfig.USERNAME,
                RabbitMQConfig.PASSWORD
            )
          
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RabbitMQConfig.HOST,
                    port=RabbitMQConfig.PORT,
                    credentials=credentials,
                    connection_attempts=3,
                    retry_delay=2
                )
            )
          
            self.channel = self.connection.channel()
          
            # Declare queue (durable)
            self.channel.queue_declare(
                queue=RabbitMQConfig.QUEUE_NAME,
                durable=True,
                arguments={
                    'x-message-ttl': 86400000,  # 24 hours
                    'x-max-length': 100000  # Max 100k messages
                }
            )
          
            logger.info("Connected to RabbitMQ")
      
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise
  
    def publish(self, message: dict):
        """Publish message to queue"""
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=RabbitMQConfig.QUEUE_NAME,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent
                    content_type='application/json',
                    timestamp=int(datetime.utcnow().timestamp())
                )
            )
          
            logger.info(f"Published message: {message.get('conversation_id')}")
      
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise
  
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Singleton instance
_publisher = None

def get_publisher():
    global _publisher
    if _publisher is None:
        _publisher = RabbitMQPublisher()
    return _publisher

async def publish_conversation_event(
    conversation_id: str,
    user_id: str,
    bot_id: str,
    conversation_log: list
):
    """Publish conversation event to queue"""
    publisher = get_publisher()
  
    message = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "bot_id": bot_id,
        "conversation_log": conversation_log,
        "enqueued_at": datetime.utcnow().isoformat()
    }
  
    publisher.publish(message)
```

---

### STEP 4: Background Worker (Consumer)

**File:** `src/app/background/rabbitmq_consumer.py` (NEW)

```python
import pika
import json
import logging
from datetime import datetime
from app.services.conversation_event_processing_service import ConversationEventProcessingService
from app.repositories.conversation_event_repository import ConversationEventRepository
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.processing_service = None
        self._connect()
  
    def _connect(self):
        """Kết nối đến RabbitMQ"""
        try:
            credentials = pika.PlainCredentials("guest", "guest")
          
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    port=5672,
                    credentials=credentials,
                    connection_attempts=3,
                    retry_delay=2
                )
            )
          
            self.channel = self.connection.channel()
            self.channel.queue_declare(
                queue="conversation_events_processing",
                durable=True
            )
          
            # Set QoS: Process 1 message at a time
            self.channel.basic_qos(prefetch_count=1)
          
            logger.info("Connected to RabbitMQ as consumer")
      
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise
  
    def callback(self, ch, method, properties, body):
        """
        Callback function khi nhận message từ queue.
        """
        try:
            # Parse message
            message = json.loads(body)
            conversation_id = message.get("conversation_id")
          
            logger.info(f"Processing conversation: {conversation_id}")
          
            # STEP 4.1: Lấy conversation event từ DB
            db = SessionLocal()
            repo = ConversationEventRepository(db)
            event = repo.get_by_conversation_id(conversation_id)
          
            if not event:
                logger.error(f"Conversation not found: {conversation_id}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
          
            # STEP 4.2: Xử lý event
            processor = ConversationEventProcessingService(
                conversation_repo=repo,
                friendship_repo=...,  # Inject dependencies
                ...
            )
          
            result = processor.process_single_event(event.id)
          
            logger.info(f"Successfully processed: {conversation_id}")
          
            # STEP 4.3: Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
      
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
          
            # Nack message (requeue for retry)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
  
    def start_consuming(self):
        """Bắt đầu consume messages"""
        try:
            self.channel.basic_consume(
                queue="conversation_events_processing",
                on_message_callback=self.callback
            )
          
            logger.info("Starting to consume messages...")
            self.channel.start_consuming()
      
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()
            logger.info("Consumer stopped")
      
        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")
            raise

# Entry point
def start_consumer():
    consumer = RabbitMQConsumer()
    consumer.start_consuming()

if __name__ == "__main__":
    start_consumer()
```

---

### STEP 5: Worker Process (Standalone Script)

**File:** `src/worker.py` (NEW)

```python
"""
Worker process để consume messages từ RabbitMQ queue.
Chạy: python src/worker.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.background.rabbitmq_consumer import start_consumer

if __name__ == "__main__":
    start_consumer()
```

---

## 🐳 DOCKER SETUP

### Docker Compose (Cập Nhật)

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: context_handling
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    ports:
      - "5672:5672"      # AMQP port
      - "15672:15672"    # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache (Optional)
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Application
  app:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/context_handling
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: guest
      RABBITMQ_PASSWORD: guest
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    command: uvicorn app.main_app:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app

  # Worker Process (Consumer)
  worker:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/context_handling
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: guest
      RABBITMQ_PASSWORD: guest
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    command: python src/worker.py
    volumes:
      - .:/app

volumes:
  postgres_data:
  rabbitmq_data:
  redis_data:
```

---

## 📊 TIMELINE & PERFORMANCE

### Timeline (Real Case)

```
18:30:00 - User kết thúc hội thoại
18:30:01 - BE gửi POST /conversations/end
          ├─ API validate request
          ├─ Save to DB (status=PENDING)
          ├─ Publish to RabbitMQ
          └─ Return 202 Accepted (< 100ms)
18:30:01 - BE nhận 202 (không đợi)
18:30:02 - Worker consume từ queue
18:30:07 - Worker xử lý xong (5s)
          ├─ Tính score
          ├─ Update DB
          └─ Mark as PROCESSED
```

**Latency:** < 100ms (BE không đợi)
**Processing:** 5-7 giây (ở background)

---

## 🔧 IMPLEMENTATION STEPS

### Phase 1: Setup RabbitMQ (Day 1)

- [ ] Add `pika` to `requirements.txt`
- [ ] Create `rabbitmq_publisher.py`
- [ ] Create `rabbitmq_consumer.py`
- [ ] Update `docker-compose.yml`
- [ ] Test RabbitMQ connection

### Phase 2: Update API Endpoint (Day 1-2)

- [ ] Modify `endpoint_conversation_events.py`
- [ ] Add `create_event_without_processing()` method
- [ ] Add `publish_conversation_event()` call
- [ ] Test API returns 202 immediately

### Phase 3: Create Worker Process (Day 2)

- [ ] Create `worker.py`
- [ ] Implement message callback
- [ ] Test worker consumes messages
- [ ] Test event processing

### Phase 4: Testing & Deployment (Day 3)

- [ ] Unit tests
- [ ] Integration tests
- [ ] Load testing (100+ messages/min)
- [ ] Deploy to staging
- [ ] Deploy to production

---

## ✅ TESTING

### Test 1: API Returns 202 Immediately

```bash
time curl -X POST http://localhost:8000/v1/conversations/end \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_test_001",
    "user_id": "user_test",
    "bot_id": "talk_movie",
    "bot_name": "Movie Talk",
    "bot_type": "TALK",
    "conversation_log": [...],
    "start_time": "2025-11-26T10:00:00Z",
    "end_time": "2025-11-26T10:20:00Z"
  }'

# Expected: Response in < 100ms
```

### Test 2: Message in Queue

```bash
# Check RabbitMQ Management UI
# http://localhost:15672 (guest/guest)
# Queue: conversation_events_processing
# Expected: 1 message in queue
```

### Test 3: Worker Processes Message

```bash
# Check logs
docker-compose logs -f worker

# Expected: "Processing conversation: conv_test_001"
# Expected: "Successfully processed: conv_test_001"
```

### Test 4: Database Updated

```bash
# Query DB
SELECT * FROM conversation_events WHERE conversation_id = 'conv_test_001';

# Expected: status = 'PROCESSED'
# Expected: friendship_score_change populated
```

---

## 📈 MONITORING

### Logs

```python
# Check logs
docker-compose logs -f app
docker-compose logs -f worker

# Expected patterns:
# - "Conversation event accepted for processing"
# - "Published message: conv_xxx"
# - "Processing conversation: conv_xxx"
# - "Successfully processed: conv_xxx"
```

### RabbitMQ Management UI

```
URL: http://localhost:15672
Username: guest
Password: guest

Check:
- Queue: conversation_events_processing
- Messages: Should decrease as worker processes
- Consumers: Should show 1 active consumer
```

### Database

```sql
-- Check conversation_events
SELECT id, conversation_id, status, created_at, updated_at
FROM conversation_events
ORDER BY created_at DESC
LIMIT 10;

-- Expected: status transitions from PENDING → PROCESSING → PROCESSED
```

---

## 🚀 QUICK START

### 1. Update Code

```bash
# Copy files
cp rabbitmq_publisher.py src/app/background/
cp rabbitmq_consumer.py src/app/background/
cp worker.py src/

# Update endpoint
# Edit src/app/api/v1/endpoints/endpoint_conversation_events.py

# Update service
# Edit src/app/services/conversation_event_service.py
```

### 2. Update Dependencies

```bash
# Add to requirements.txt
pika==1.3.1

# Install
pip install -r requirements.txt
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Verify
docker-compose ps
docker-compose logs -f
```

### 4. Test

```bash
# Test API
curl -X POST http://localhost:8000/v1/conversations/end ...

# Check RabbitMQ
# http://localhost:15672

# Check logs
docker-compose logs -f worker
```

---

## ⚠️ POTENTIAL ISSUES & SOLUTIONS

### Issue 1: Worker không consume messages

**Symptoms:**

- Messages stay in queue
- Worker logs show no activity

**Solutions:**

- Check RabbitMQ connection: `docker-compose logs rabbitmq`
- Check worker logs: `docker-compose logs worker`
- Verify queue name matches
- Restart worker: `docker-compose restart worker`

### Issue 2: Message processing fails

**Symptoms:**

- Worker logs show errors
- Event status stays PROCESSING

**Solutions:**

- Check database connection
- Check service dependencies injection
- Check conversation_log format
- Add more detailed logging

### Issue 3: RabbitMQ connection refused

**Symptoms:**

- "Connection refused" error
- Worker can't connect

**Solutions:**

- Check RabbitMQ is running: `docker-compose ps`
- Check health: `docker-compose logs rabbitmq`
- Wait for RabbitMQ to be ready (healthcheck)
- Restart RabbitMQ: `docker-compose restart rabbitmq`

---

## 📝 SUMMARY

### Thay Đổi Chính

| Thành Phần       | Trước            | Sau                  |
| :--------------- | :--------------- | :------------------- |
| **API Response** | Xử lý ngay, chậm | 202 Accepted, nhanh  |
| **Processing**   | Synchronous      | Asynchronous (queue) |
| **Scalability**  | Limited          | High                 |
| **Latency**      | 5-10s            | < 100ms (API)        |
| **Reliability**  | Không có retry   | Có retry + DLQ       |

### Files Cần Thêm/Sửa

**Thêm:**

- `src/app/background/rabbitmq_publisher.py`
- `src/app/background/rabbitmq_consumer.py`
- `src/worker.py`

**Sửa:**

- `src/app/api/v1/endpoints/endpoint_conversation_events.py`
- `src/app/services/conversation_event_service.py`
- `docker-compose.yml`
- `requirements.txt`

---

**Phương án kỹ thuật chi tiết sẵn sàng triển khai!** 🚀



---



Tôi sẽ đọc tài liệu triển khai RabbitMQ để trả lời câu hỏi của bạn.## Trả lời câu hỏi của bạn

**Có, khi chạy localhost bạn CẦN chạy riêng worker!**

Theo kiến trúc RabbitMQ trong tài liệu, có  **2 process riêng biệt** :

| Process                 | Lệnh chạy                                                       | Vai trò                                                   |
| ----------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| **API (FastAPI)** | `uvicorn app.main_app:app --reload --host 0.0.0.0 --port 30020` | Nhận request → Lưu DB → Publish to queue → Return 202 |
| **Worker**        | `python src/worker.py`                                          | Consume từ queue → Xử lý background → Update DB       |

### Cách chạy localhost:

**Terminal 1 - API:**

```bash
uvicorn app.main_app:app --reload --host 0.0.0.0 --port 30020
```

**Terminal 2 - Worker:**

```bash
python src/worker.py
```

**Terminal 3 - RabbitMQ (nếu chưa có):**

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Nếu dùng Docker Compose thì đơn giản hơn:

```bash
docker-compose up -d
```

Docker Compose sẽ tự động chạy cả 2 services (`app` + `worker`) như định nghĩa trong file `docker-compose.yml`.

### Lưu ý khi chạy localhost:

1. **RabbitMQ host** cần đổi từ `"rabbitmq"` (Docker service name) thành `"localhost"` trong config
2. **Database connection** cũng cần đổi tương tự
3. Worker cần chạy độc lập vì nó là **blocking consumer** - nó chờ message từ queue liên tục

Nếu không chạy worker, messages sẽ đọng trong queue và không được xử lý!self**.**db**.**query**(**ConversationEvent**)**.get**(**conversation_id**)**

```
┌─────────────────────────────────────────────────────────────────┐
│                        RabbitMQ Queue                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │Msg 1   │ │ Msg 2   │ │ Msg 3   │ │ Msg 4   │  ...          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ Khi có message mới
                          ▼
              ┌───────────────────────┐
              │   Consumer (Worker)   │
              │                       │
              │  callback(message) ◄──┼── RabbitMQ tự động gọi
              │       │               │
              │       ▼               │
              │  Xử lý message        │
              │  - Parse JSON         │
              │  - Query DB           │
              │  - Tính score         │
              │  - Update DB          │
              └───────────────────────┘
```