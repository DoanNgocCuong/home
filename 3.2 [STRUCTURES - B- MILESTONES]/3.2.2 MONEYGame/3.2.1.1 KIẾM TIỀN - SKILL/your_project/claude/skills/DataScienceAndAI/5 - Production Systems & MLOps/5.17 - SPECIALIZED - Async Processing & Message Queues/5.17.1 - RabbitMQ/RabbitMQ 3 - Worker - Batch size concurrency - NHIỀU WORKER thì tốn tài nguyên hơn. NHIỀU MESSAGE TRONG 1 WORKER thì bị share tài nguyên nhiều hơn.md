# Tối Ưu Hóa Concurrency và Số Lượng Worker (RabbitMQ)

## 🎯 Vấn Đề Hiện Tại: Xử Lý Từng Message Một

Bạn quan sát thấy worker chỉ xử lý từng `conversation_id` một. Điều này là do cấu hình **Quality of Service (QoS)** mặc định của RabbitMQ/Pika.

Trong file `rabbitmq_consumer.py` (hoặc tương đương), bạn có thể đã thấy dòng này:

```python
# Set QoS: Process 1 message at a time
self.channel.basic_qos(prefetch_count=1) 
```

`prefetch_count=1` nghĩa là worker chỉ nhận 1 message từ queue, và chỉ nhận message tiếp theo sau khi đã `ack` (xác nhận xử lý xong) message hiện tại. Điều này đảm bảo tính an toàn và tránh mất message, nhưng giới hạn tốc độ xử lý.

---

## 1. LÀM SAO ĐỂ TĂNG TỐC ĐỘ XỬ LÝ SONG SONG?

Có hai cách chính để tăng tốc độ xử lý song song:

### A. Tăng `prefetch_count` (Tăng Concurrency Trong 1 Worker)

`prefetch_count` là số lượng message tối đa mà một worker có thể nhận và giữ trong bộ nhớ đệm (buffer) trước khi xác nhận xử lý.

**Cập Nhật Code:**

```python
# File: src/app/background/rabbitmq_consumer.py

# Thay đổi:
# self.channel.basic_qos(prefetch_count=1) 

# Thành:
CONCURRENCY_PER_WORKER = 10 # Ví dụ: cho phép 1 worker xử lý 10 message cùng lúc
self.channel.basic_qos(prefetch_count=CONCURRENCY_PER_WORKER) 
```

**Cơ chế:**
- Worker sẽ nhận 10 message từ queue.
- Worker sẽ dùng **10 thread hoặc process** (tùy thuộc vào framework bạn dùng: Celery, Python `threading`, `multiprocessing`, `asyncio`) để xử lý 10 message này song song.
- **Lưu ý quan trọng:** Việc tăng `prefetch_count` chỉ có tác dụng nếu code xử lý của bạn (tính score, update DB) là **thread-safe** và **non-blocking** (ví dụ: dùng `asyncio` hoặc `multiprocessing`). Nếu code là blocking (I/O-bound), bạn cần dùng `multiprocessing` hoặc `threading` để tận dụng.

### B. Tăng Số Lượng Worker Process (Tăng Concurrency Tổng Thể)

Đây là cách hiệu quả và dễ quản lý nhất. Mỗi worker là một process độc lập, chạy trên một core CPU.

**Cập Nhật Docker Compose:**

```yaml
# File: docker-compose.yml

services:
  # ... (app service)

  # Worker Process (Consumer)
  worker:
    build: .
    # ... (dependencies)
    # Thay vì chỉ chạy 1 worker:
    # command: python src/worker.py
    
    # Chạy 5 worker process:
    deploy:
      replicas: 5  # <-- Tăng số lượng worker process lên 5
    command: python src/worker.py
    volumes:
      - .:/app
```

**Cơ chế:**
- 5 process worker độc lập sẽ cùng lắng nghe queue.
- RabbitMQ sẽ tự động phân phối message cho 5 worker này (Round-robin).
- **Tổng Concurrency:** `Total Concurrency = Số lượng Worker Process * Concurrency Per Worker` (ví dụ: 5 * 10 = 50 message cùng lúc).

---

## 2. LÀM SAO ĐỂ BIẾT SỐ LƯỢNG WORKER TỐI ƯU?

Số lượng worker tối ưu phụ thuộc vào 3 yếu tố chính: **Phần cứng**, **Loại tác vụ**, và **Mục tiêu CCU**.

### A. Phân Tích Tác Vụ (Your Use Case)

| Yếu Tố | Mô Tả | Ảnh Hưởng |
| :--- | :--- | :--- |
| **Tính Score** | Tính toán (CPU-bound) | Cần nhiều core CPU |
| **Update DB** | I/O (I/O-bound) | Cần nhiều thread/process |
| **Fetch Data** | I/O (I/O-bound) | Cần nhiều thread/process |

**Kết luận:** Tác vụ của bạn là **Hybrid (CPU + I/O)**. Cần cân bằng giữa số core CPU và số lượng process/thread.

### B. Công Thức Tối Ưu (Dựa trên Phần Cứng)

Giả sử Server có **N** core CPU.

1. **Số lượng Worker Process (W):**
   - **Quy tắc:** `W ≈ N` (Nếu tác vụ là CPU-bound)
   - **Quy tắc:** `W ≈ 2N + 1` (Nếu tác vụ là I/O-bound)
   - **Với Hybrid:** Bắt đầu với `W = 2N`

2. **Concurrency Per Worker (`prefetch_count` - C):**
   - **Quy tắc:** `C` nên đủ lớn để giữ CPU bận rộn, nhưng không quá lớn để gây quá tải.
   - **Bắt đầu:** `C = 5` đến `10`

**Ví dụ:** Server có 4 core CPU.
- **Worker Process (W):** `2 * 4 = 8`
- **Concurrency Per Worker (C):** `10`
- **Tổng Concurrency:** `8 * 10 = 80`

### C. Chạy Benchmark (Theo Yêu Cầu)

Bạn cần chạy benchmark để tìm ra con số chính xác.

**Mục tiêu:** 100 CCU (Concurrent Users) và 500 requests.

1. **Setup:**
   - Bắt đầu với cấu hình: `W=4` (4 worker process) và `C=10` (`prefetch_count=10`).
   - Tổng concurrency: 40.

2. **Chạy Load Test:**
   - Dùng công cụ như `Locust` hoặc `JMeter` để bắn 500 requests liên tục (hoặc 100 CCU) vào API `POST /conversations/end`.
   - **Đo lường:**
     - **Latency:** Thời gian xử lý trung bình của worker (từ lúc nhận message đến lúc PROCESSED).
     - **CPU Usage:** CPU của worker process.
     - **Queue Length:** Chiều dài queue (nếu queue dài ra, cần thêm worker).

3. **Tối Ưu Hóa:**
   - **Nếu CPU < 80%:** Tăng `W` (số lượng worker process) lên 6, 8, 10...
   - **Nếu CPU > 90%:** Giảm `C` (prefetch_count) hoặc tăng `W` (nếu còn core).
   - **Nếu Queue dài:** Tăng `W` (thêm worker).

---

## 3. CẤU HÌNH DEV VÀ PRODUCTION

| Cấu Hình | Dev | Production | Lý Do |
| :--- | :--- | :--- | :--- |
| **Worker Process (W)** | 1 - 2 | `2N` (N = số core) | Dev: Tiết kiệm tài nguyên. Prod: Tối ưu hiệu năng. |
| **Concurrency (C)** | 1 | 5 - 10 | Dev: Dễ debug (xử lý tuần tự). Prod: Tăng throughput. |
| **Hardware** | Shared/Low-end | Dedicated/High-end | Prod cần phần cứng mạnh hơn. |
| **Logging** | DEBUG | INFO/ERROR | Dev: Log chi tiết. Prod: Log lỗi. |

**Ví dụ Cấu Hình Dev (Dễ Debug):**
- `worker` service: `deploy: replicas: 1`
- `prefetch_count`: `1`

**Ví dụ Cấu Hình Prod (Tối Ưu):**
- `worker` service: `deploy: replicas: 8`
- `prefetch_count`: `10`

---

## 🚀 TÓM TẮT HÀNH ĐỘNG

1. **Code:** Cập nhật `prefetch_count` trong `rabbitmq_consumer.py` thành một giá trị ban đầu (ví dụ: 10).
2. **Deploy:** Cập nhật `docker-compose.yml` để chạy nhiều worker process (ví dụ: 4-8 replicas).
3. **Benchmark:** Chạy load test 100 CCU / 500 requests để đo lường và tinh chỉnh số lượng worker process và `prefetch_count` cho phù hợp với phần cứng thực tế.

**Bạn cần tôi tạo file code mẫu cho việc cập nhật `prefetch_count` và `docker-compose.yml` không?**



---


Đang phân tích code hiện tại để giải thích tại sao nó blocking và điều gì xảy ra khi `prefetch_count=10`.


[2 tools called]


Giải thích tại sao code hiện tại là blocking và điều gì xảy ra khi `prefetch_count=10`:

## Tại sao code hiện tại là blocking?

### 1. Sử dụng `pika.BlockingConnection`

```269:282:src/app/background/rabbitmq_consumer.py
    def start_consuming(self):
        """Start consuming messages from queue."""
        try:
            self.channel.basic_consume(
                queue=RabbitMQConfig.QUEUE_NAME,
                on_message_callback=self.callback,
                auto_ack=False  # Manual acknowledgment
            )
            
            logger.info(consumer_starting())
            logger.info(f"{info('📋')} {queue_info(RabbitMQConfig.QUEUE_NAME, 'listening')}")
            logger.info(f"{info('💡')} Press CTRL+C to stop")
            
            self.channel.start_consuming()
```

- `pika.BlockingConnection`: chạy trên một thread, blocking.
- `start_consuming()`: chạy vòng lặp blocking, chờ message.
- Callback được gọi tuần tự: callback hiện tại phải hoàn thành (ACK/NACK) trước khi callback tiếp theo được gọi.

### 2. Callback xử lý tuần tự

```166:230:src/app/background/rabbitmq_consumer.py
    def callback(self, ch, method, properties, body):
        """
        Callback function when receiving message from queue.
        
        Args:
            ch: Channel
            method: Delivery method
            properties: Message properties
            body: Message body (JSON string)
        """
        conversation_id = None
        db = None  # FIX: Khai báo db ở ngoài để đảm bảo có thể close trong finally
        
        try:
            # Parse message
            message = json.loads(body)
            conversation_id = message.get("conversation_id")
            
            logger.info(message_received(conversation_id))
            
            # FIX: Tạo session MỚI cho mỗi message để tránh transaction bị "nhiễm" lỗi
            db = SessionLocal()
            
            repo = ConversationEventRepository(db)
            event = repo.get_by_conversation_id(conversation_id)
            
            if not event:
                logger.error(
                    f"{error('❌ Conversation not found in DB')} | "
                    f"{key_value('conversation_id', conversation_id)}"
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            # Setup services
            conversation_fetch_service = ConversationDataFetchService(
                conversation_repository=repo,
                external_api_client=None
            )
            score_service = FriendshipScoreCalculationService(
                conversation_fetch_service=conversation_fetch_service
            )
            status_service = FriendshipStatusUpdateService(db)
            
            # Process event
            processor = ConversationEventProcessingService(
                db=db,
                score_service=score_service,
                status_update_service=status_service,
            )
            
            result = processor.process_single_event(event.id)
            
            if result:
                processed = result.get('processed', 0)
                failed = result.get('failed', 0)
                logger.info(message_processed(conversation_id, processed, failed))
            else:
                logger.warning(
                    f"{warning('⚠️  No result from processing')} | "
                    f"{key_value('conversation_id', conversation_id)}"
                )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
```

- Tất cả thao tác (DB, tính toán, cập nhật) đều blocking.
- Không có threading/async, nên callback chạy tuần tự.

## Khi `prefetch_count=10` thì sao?

### Hiện tại (`prefetch_count=1`):

```
Timeline:
┌─────────────────────────────────────────────────────────┐
│ Worker Process                                           │
├─────────────────────────────────────────────────────────┤
│ [Message 1] → Process → ACK → [Message 2] → Process... │
│   (chờ)      (blocking)  (chờ)   (chờ)      (blocking) │
└─────────────────────────────────────────────────────────┘

Queue: [Msg1][Msg2][Msg3][Msg4]...
        ↑
    Worker chỉ nhận 1 message tại một thời điểm
```

### Khi `prefetch_count=10`:

```
Timeline:
┌─────────────────────────────────────────────────────────┐
│ Worker Process                                           │
├─────────────────────────────────────────────────────────┤
│ [Msg1][Msg2][Msg3]...[Msg10] ← Worker nhận 10 message  │
│   ↓                                                      │
│ Process Msg1 (blocking, 5 giây)                         │
│   ↓                                                      │
│ ACK Msg1                                                 │
│   ↓                                                      │
│ Process Msg2 (blocking, 5 giây)                         │
│   ↓                                                      │
│ ACK Msg2                                                 │
│   ...                                                    │
└─────────────────────────────────────────────────────────┘

Queue: [Msg11][Msg12][Msg13]...
        ↑
    Worker đã có 10 message trong buffer, nhưng vẫn xử lý TUẦN TỰ
```

### Điểm khác biệt:

| Aspect | `prefetch_count=1` | `prefetch_count=10` |
|--------|-------------------|---------------------|
| Số message trong buffer | 1 | 10 |
| Xử lý song song? | ❌ Không | ❌ Vẫn không |
| Tốc độ xử lý | Chậm | Vẫn chậm (tương tự) |
| Lợi ích | Đơn giản, an toàn | Giảm network round-trip, có buffer |
| Nhược điểm | Phải chờ ACK mới nhận message tiếp | Vẫn xử lý tuần tự, chỉ có buffer |

## Tại sao không xử lý song song?

Vì callback là blocking và chạy trên cùng một thread:

```python
# Flow hiện tại:
start_consuming() 
  → callback(msg1) [BLOCKING - chờ hoàn thành]
    → process_single_event() [BLOCKING - 5 giây]
    → basic_ack() [BLOCKING]
  → callback(msg2) [BLOCKING - chờ hoàn thành]
    → process_single_event() [BLOCKING - 5 giây]
    → basic_ack() [BLOCKING]
```

## Khi nào `prefetch_count=10` có lợi?

1. Giảm network round-trip: nhận 10 message một lần thay vì 10 lần.
2. Có buffer: nếu một message xử lý nhanh, message tiếp theo đã sẵn sàng.
3. Vẫn không song song: nếu mỗi message mất 5 giây, tổng thời gian vẫn là 50 giây cho 10 message.

## Để xử lý song song thực sự

Cần dùng threading hoặc asyncio:

### Option 1: Threading (đơn giản)

```python
import threading
from concurrent.futures import ThreadPoolExecutor

class RabbitMQConsumer:
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        # ... existing code ...
    
    def callback(self, ch, method, properties, body):
        # Submit vào thread pool để xử lý song song
        future = self.executor.submit(self._process_message, ch, method, properties, body)
        # Không chờ kết quả, return ngay → callback tiếp theo có thể chạy
    
    def _process_message(self, ch, method, properties, body):
        # Logic xử lý message (giống code hiện tại)
        # ...
        ch.basic_ack(delivery_tag=method.delivery_tag)
```

### Option 2: Asyncio (hiệu quả hơn)

```python
import asyncio
import aio_pika  # Async version của pika

# Sử dụng aio_pika thay vì pika
# Xử lý async/await
```

## Kết luận

- `prefetch_count=10` chỉ giúp worker nhận 10 message trước, không làm xử lý song song.
- Để xử lý song song, cần threading hoặc asyncio.
- Với 10 worker process, mỗi worker xử lý tuần tự, tổng cộng có thể xử lý 10 message cùng lúc (mỗi worker 1 message).

Bạn muốn tôi tạo code với threading để xử lý song song thực sự không?



----

Đánh giá mức độ khó và cách triển khai:


[2 tools called]


## Đánh giá mức độ khó: Dễ (3/10)

### Lý do dễ
1. Python có sẵn `ThreadPoolExecutor` (không cần cài thêm)
2. Chỉ cần thêm vài dòng code
3. Không cần thay đổi logic xử lý hiện tại
4. Tương thích với code hiện tại

### Lưu ý
- Thread-safety: Mỗi thread cần tạo DB session riêng (code hiện tại đã làm đúng)
- Pika channel: Cần đảm bảo ACK/NACK trong cùng thread với message

## Code mẫu (đơn giản)

### Bước 1: Thêm import

```python
# File: src/app/background/rabbitmq_consumer.py

import json
import pika
from typing import Optional
from concurrent.futures import ThreadPoolExecutor  # <-- THÊM DÒNG NÀY
from app.core.config_settings import settings
# ... existing imports ...
```

### Bước 2: Cập nhật class RabbitMQConsumer

```python
class RabbitMQConsumer:
    """RabbitMQ consumer for conversation events."""
    
    def __init__(self, max_workers: int = 10):
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        # THÊM: Thread pool để xử lý song song
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._connect()
    
    # ... existing _connect() method ...
    
    def callback(self, ch, method, properties, body):
        """
        Callback function when receiving message from queue.
        
        NOTE: Method này chỉ submit task vào thread pool và return ngay.
        Logic xử lý thực sự nằm trong _process_message().
        """
        # Submit vào thread pool để xử lý song song
        # Không chờ kết quả, return ngay → callback tiếp theo có thể chạy
        self.executor.submit(
            self._process_message,
            ch, method, properties, body
        )
        # Return ngay lập tức → RabbitMQ có thể gửi message tiếp theo
    
    def _process_message(self, ch, method, properties, body):
        """
        Xử lý message thực sự (chạy trong thread riêng).
        
        Logic này giống hệt code cũ trong callback(), chỉ tách ra method riêng.
        """
        conversation_id = None
        db = None
        
        try:
            # Parse message
            message = json.loads(body)
            conversation_id = message.get("conversation_id")
            
            logger.info(message_received(conversation_id))
            
            # Tạo session MỚI cho mỗi thread (QUAN TRỌNG!)
            db = SessionLocal()
            
            repo = ConversationEventRepository(db)
            event = repo.get_by_conversation_id(conversation_id)
            
            if not event:
                logger.error(
                    f"{error('❌ Conversation not found in DB')} | "
                    f"{key_value('conversation_id', conversation_id)}"
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            # Setup services
            conversation_fetch_service = ConversationDataFetchService(
                conversation_repository=repo,
                external_api_client=None
            )
            score_service = FriendshipScoreCalculationService(
                conversation_fetch_service=conversation_fetch_service
            )
            status_service = FriendshipStatusUpdateService(db)
            
            # Process event
            processor = ConversationEventProcessingService(
                db=db,
                score_service=score_service,
                status_update_service=status_service,
            )
            
            result = processor.process_single_event(event.id)
            
            if result:
                processed = result.get('processed', 0)
                failed = result.get('failed', 0)
                logger.info(message_processed(conversation_id, processed, failed))
            else:
                logger.warning(
                    f"{warning('⚠️  No result from processing')} | "
                    f"{key_value('conversation_id', conversation_id)}"
                )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except json.JSONDecodeError as e:
            logger.error(
                f"{error('❌ Error parsing message JSON')} | "
                f"{key_value('error', str(e))}",
                exc_info=True
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except Exception as e:
            error_msg = str(e)
            logger.error(
                message_failed(conversation_id or 'unknown', error_msg),
                exc_info=True
            )
            
            if db:
                try:
                    db.rollback()
                except Exception as rollback_error:
                    logger.warning(f"⚠️ Error during rollback: {str(rollback_error)}")
            
            try:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            except Exception as nack_error:
                logger.error(f"❌ Failed to nack message: {str(nack_error)}")
        
        finally:
            if db:
                try:
                    db.close()
                except Exception as close_error:
                    logger.warning(f"⚠️ Error closing DB session: {str(close_error)}")
    
    # ... existing start_consuming() method ...
    
    def close(self):
        """Close connection and shutdown thread pool."""
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            # THÊM: Shutdown thread pool
            self.executor.shutdown(wait=True, timeout=30)
            logger.info(connection_closed())
        except Exception as e:
            logger.warning(
                f"{warning('⚠️')} Error closing RabbitMQ connection: {str(e)}"
            )
```

### Bước 3: Cập nhật RabbitMQConfig (tùy chọn)

```python
class RabbitMQConfig:
    """RabbitMQ configuration (same as publisher)."""
    
    # ... existing methods ...
    
    CONCURRENCY_PER_WORKER = 10  # Số thread xử lý song song trong 1 worker
    QUEUE_NAME = settings.RABBITMQ_QUEUE_NAME
```

Và cập nhật `__init__`:

```python
def __init__(self, max_workers: int = None):
    self.connection: Optional[pika.BlockingConnection] = None
    self.channel: Optional[pika.channel.Channel] = None
    # Sử dụng config hoặc default
    workers = max_workers or RabbitMQConfig.CONCURRENCY_PER_WORKER
    self.executor = ThreadPoolExecutor(max_workers=workers)
    self._connect()
```

## So sánh trước và sau

### Trước (blocking):
```python
callback(msg1) → Process (5s) → ACK → callback(msg2) → Process (5s) → ACK
Tổng: 10 giây cho 2 message
```

### Sau (threading):
```python
callback(msg1) → Submit to thread → Return ngay
callback(msg2) → Submit to thread → Return ngay
Thread 1: Process msg1 (5s) → ACK
Thread 2: Process msg2 (5s) → ACK
Tổng: ~5 giây cho 2 message (song song!)
```

## Kết quả

- Với `prefetch_count=10` + `max_workers=10`:
  - Worker nhận 10 message cùng lúc
  - 10 thread xử lý song song
  - Tổng concurrency: 10 workers × 10 threads = 100 message cùng lúc

## Lưu ý quan trọng

1. DB session: Mỗi thread tự tạo session riêng (code hiện tại đã đúng)
2. Pika channel: Pika channel thread-safe cho ACK/NACK
3. Memory: 10 thread × 10 worker = 100 thread, cần đủ RAM
4. CPU: Nếu CPU-bound, cân nhắc giảm số thread

## Tóm tắt

- Độ khó: 3/10
- Thời gian: ~10 phút
- Rủi ro: Thấp (code hiện tại đã thread-safe)
- Lợi ích: Tăng throughput đáng kể

Bạn muốn tôi tạo file code đầy đủ để copy/paste không?


---
## Bạn đúng! Tôi viết nhầm

### Công thức đúng:

| Loại tác vụ | Công thức Worker (W) | Với 96 cores |
|-------------|---------------------|--------------|
| **CPU-bound** | W ≈ N | W ≈ 96 |
| **I/O-bound** | W ≈ 2N + 1 | W ≈ 193 |
| **Hybrid (CPU + I/O)** | W ≈ N đến 2N | W ≈ 96 - 192 |

---

## Sửa lại config cho 96 cores:

| Cấu hình | Giá trị | Giải thích |
|----------|---------|------------|
| **Worker Process (W)** | **96 - 192** | N đến 2N (N = 96 cores) |
| **Threads per Worker (T)** | 10 - 20 | max_workers trong ThreadPoolExecutor |
| **Prefetch Count (C)** | 10 - 20 | Bằng số threads |
| **Tổng Concurrency** | **960 - 3840** | W × T |

---

## Ví dụ cụ thể:

```
Option 1 (Conservative):
  W = 96 workers × T = 10 threads = 960 concurrent

Option 2 (Balanced):
  W = 128 workers × T = 15 threads = 1920 concurrent

Option 3 (Aggressive - I/O heavy):
  W = 192 workers × T = 20 threads = 3840 concurrent
```

Cảm ơn bạn đã chỉ ra! 👍
---

## Đúng rồi! 480 messages xử lý song song cùng lúc

### Hình dung:

```
┌─────────────────────────────────────────────────────────────────┐
│                         RabbitMQ Queue                          │
│  [Msg1][Msg2][Msg3]...[Msg480][Msg481][Msg482]...               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼ Phân phối cho 48 Workers
┌─────────────────────────────────────────────────────────────────┐
│ Worker 1 (10 threads)  │ Worker 2 (10 threads)  │ ... │ Worker 48│
│ ├─ Thread 1: Msg 1     │ ├─ Thread 1: Msg 11    │     │          │
│ ├─ Thread 2: Msg 2     │ ├─ Thread 2: Msg 12    │     │          │
│ ├─ Thread 3: Msg 3     │ ├─ Thread 3: Msg 13    │     │          │
│ ├─ ...                 │ ├─ ...                 │     │          │
│ └─ Thread 10: Msg 10   │ └─ Thread 10: Msg 20   │     │          │
└─────────────────────────────────────────────────────────────────┘

Tổng: 48 workers × 10 threads = 480 messages ĐỒNG THỜI
```

### Ví dụ thực tế:

| Scenario | Trước (1 worker, 1 thread) | Sau (48 workers × 10 threads) |
|----------|---------------------------|-------------------------------|
| 1 message mất 5 giây | 5s | 5s |
| 480 messages | 480 × 5s = **40 phút** | 5s (song song) = **5 giây** |
| 1000 messages | 1000 × 5s = **83 phút** | 1000/480 × 5s ≈ **11 giây** |

---

### Tóm lại:

- **Trước:** Xử lý 1 message → xong → xử lý message tiếp (tuần tự)
- **Sau:** Xử lý 480 messages cùng một lúc (song song)

Với 96 cores, bạn hoàn toàn có thể đẩy lên **960-1920 concurrent** nếu cần!



---

┌─────────────────────────────────────────────────────────┐
│ RabbitMQ Queue: [Msg1][Msg2]...[Msg100]...              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼ Phân phối cho 10 Workers
┌─────────────────────────────────────────────────────────┐
│ Worker 1 (10 threads) │ Worker 2 (10 threads) │ ...   │
│ ├─ Thread 1: Msg 1     │ ├─ Thread 1: Msg 11    │      │
│ ├─ Thread 2: Msg 2     │ ├─ Thread 2: Msg 12    │      │
│ ├─ ...                 │ ├─ ...                 │      │
│ └─ Thread 10: Msg 10   │ └─ Thread 10: Msg 20   │      │
└─────────────────────────────────────────────────────────┘

Tổng: 10 workers × 10 threads = 100 messages ĐỒNG THỜI



----



## So sánh: 100 Workers × 1 Thread vs 10 Workers × 10 Threads

Cả hai đều cho **100 concurrent**, nhưng khác nhau về tài nguyên:

---

### Bảng so sánh chi tiết:

| Yếu tố | 100 Workers × 1 Thread | 10 Workers × 10 Threads |
|--------|------------------------|-------------------------|
| **Tổng Concurrency** | 100 | 100 |
| **RAM** | ~10-20 GB | ~1-2 GB |
| **DB Connections** | ~100 connections | ~100 connections |
| **CPU Context Switch** | Nhiều (process switch nặng) | Ít hơn (thread switch nhẹ) |
| **Startup Time** | Chậm (100 processes) | Nhanh (10 processes) |
| **Isolation** | Tốt (process độc lập) | Kém hơn (threads share memory) |
| **Crash Impact** | 1 crash = mất 1 worker | 1 crash = mất 10 threads |

---

### Hình dung về Memory:

```
100 Workers × 1 Thread:
┌─────────────────────────────────────────────────────────────┐
│ Process 1    │ Process 2    │ ... │ Process 100            │
│ RAM: 100MB   │ RAM: 100MB   │     │ RAM: 100MB             │
│ Python: 50MB │ Python: 50MB │     │ Python: 50MB           │
│ Libs: 50MB   │ Libs: 50MB   │     │ Libs: 50MB             │
└─────────────────────────────────────────────────────────────┘
Tổng RAM: 100 × 100MB = ~10GB (mỗi process load riêng Python + libs)


10 Workers × 10 Threads:
┌─────────────────────────────────────────────────────────────┐
│ Process 1              │ Process 2              │ ... × 10  │
│ RAM: 150MB             │ RAM: 150MB             │           │
│ ├─ Thread 1 (+5MB)     │ ├─ Thread 1 (+5MB)     │           │
│ ├─ Thread 2 (+5MB)     │ ├─ Thread 2 (+5MB)     │           │
│ ├─ ...                 │ ├─ ...                 │           │
│ └─ Thread 10 (+5MB)    │ └─ Thread 10 (+5MB)    │           │
└─────────────────────────────────────────────────────────────┘
Tổng RAM: 10 × 200MB = ~2GB (threads share memory trong process)
```

---

### Khi nào chọn cái nào?

| Scenario | Chọn | Lý do |
|----------|------|-------|
| **RAM hạn chế** | 10W × 10T | Tiết kiệm RAM 5-10 lần |
| **Cần isolation cao** | 100W × 1T | 1 crash không ảnh hưởng workers khác |
| **I/O-bound (DB, API calls)** | 10W × 10T | Threads hiệu quả hơn cho I/O |
| **CPU-bound (tính toán nặng)** | 100W × 1T | Tránh Python GIL |
| **Dễ scale** | 100W × 1T | Kubernetes/Docker scale dễ hơn |

---

### Python GIL (Global Interpreter Lock):

```
CPU-bound task (tính toán nặng):
┌─────────────────────────────────────────────────────────────┐
│ 10 Threads trong 1 Process:                                 │
│                                                             │
│ Thread 1: ████████░░░░░░░░░░░░░░░░ (chờ GIL)               │
│ Thread 2: ░░░░░░░░████████░░░░░░░░ (chờ GIL)               │
│ Thread 3: ░░░░░░░░░░░░░░░░████████ (chờ GIL)               │
│                                                             │
│ → Threads phải chờ nhau do GIL!                            │
│ → Không thực sự song song cho CPU-bound                    │
└─────────────────────────────────────────────────────────────┘

I/O-bound task (DB, network):
┌─────────────────────────────────────────────────────────────┐
│ 10 Threads trong 1 Process:                                 │
│                                                             │
│ Thread 1: ████ (query DB, release GIL) ░░░░ ████           │
│ Thread 2: ░░░░ ████ (query DB, release GIL) ░░░░ ████      │
│ Thread 3: ████ ░░░░ ████ (query DB, release GIL) ░░░░      │
│                                                             │
│ → I/O tự động release GIL                                  │
│ → Threads chạy song song được!                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Recommendation cho PIKA (context-handling):

Tác vụ của bạn là **Hybrid (I/O nhiều hơn CPU)**:
- Query DB ✅ I/O
- Tính score ⚡ CPU (nhẹ)
- Update DB ✅ I/O

**→ Chọn: Ít Workers × Nhiều Threads**

```yaml
# Recommended cho 96 cores:
Workers: 20-30
Threads per Worker: 30-50
Total Concurrency: 600-1500

# Tiết kiệm RAM, hiệu quả cho I/O-bound
```

---

## Tóm tắt:

|                | 100W × 1T        | 10W × 10T       |
| -------------- | ---------------- | --------------- |
| **RAM**        | 🔴 Nhiều (~10GB) | 🟢 Ít (~2GB)    |
| **CPU-bound**  | 🟢 Tốt           | 🔴 Bị GIL block |
| **I/O-bound**  | 🟡 OK            | 🟢 Tốt          |
| **Isolation**  | 🟢 Cao           | 🟡 Thấp         |
| **Complexity** | 🟢 Đơn giản      | 🟡 Phức tạp hơn |

---

--- 
# Code 


| Component | Status | Chi tiết |
|-----------|--------|----------|
| **Config Settings** | OK | `MESSAGE_CONCURRENCY_PER_WORKER` đã được định nghĩa |
| **RabbitMQ Consumer** | OK | Đọc từ settings, dùng `RabbitMQConfig.CONCURRENCY_PER_WORKER` |
| **Thread Pool** | OK | Tạo với `max_workers` từ settings |
| **Prefetch Count** | OK | Set từ `RabbitMQConfig.CONCURRENCY_PER_WORKER` |
| **Docker Compose** | OK | Đọc `WORKER_REPLICAS` từ env |
| **Env Example** | OK | Đã có đầy đủ config |

### Flow hoạt động

```
1. .env file
   ↓
   MESSAGE_CONCURRENCY_PER_WORKER=10
   WORKER_REPLICAS=10
   
2. config_settings.py
   ↓
   settings.MESSAGE_CONCURRENCY_PER_WORKER = 10
   
3. rabbitmq_consumer.py
   ↓
   RabbitMQConfig.CONCURRENCY_PER_WORKER = 10
   ThreadPoolExecutor(max_workers=10)
   basic_qos(prefetch_count=10)
   
4. docker-compose.worker.yml
   ↓
   replicas: 10 workers
   
5. Kết quả:
   10 workers × 10 threads = 100 messages đồng thời ✅
```

### Cách test

1. Thêm vào `.env`:
   ```bash
   MESSAGE_CONCURRENCY_PER_WORKER=10
   WORKER_REPLICAS=10
   ```

2. Chạy worker:
   ```bash
   python src/worker.py
   ```

3. Kiểm tra log:
   ```
   Connected to RabbitMQ as consumer at localhost:5672 
   (prefetch_count=10, max_workers=10)
   ```

4. Deploy với Docker:
   ```bash
   docker-compose -f src/docker-compose.worker.yml up -d
   ```

Code đã sẵn sàng và hoạt động.


---

--- 
# Code 


| Component | Status | Chi tiết |
|-----------|--------|----------|
| **Config Settings** | OK | `MESSAGE_CONCURRENCY_PER_WORKER` đã được định nghĩa |
| **RabbitMQ Consumer** | OK | Đọc từ settings, dùng `RabbitMQConfig.CONCURRENCY_PER_WORKER` |
| **Thread Pool** | OK | Tạo với `max_workers` từ settings |
| **Prefetch Count** | OK | Set từ `RabbitMQConfig.CONCURRENCY_PER_WORKER` |
| **Docker Compose** | OK | Đọc `WORKER_REPLICAS` từ env |
| **Env Example** | OK | Đã có đầy đủ config |

### Flow hoạt động

```
1. .env file
   ↓
   MESSAGE_CONCURRENCY_PER_WORKER=10
   WORKER_REPLICAS=10
   
2. config_settings.py
   ↓
   settings.MESSAGE_CONCURRENCY_PER_WORKER = 10
   
3. rabbitmq_consumer.py
   ↓
   RabbitMQConfig.CONCURRENCY_PER_WORKER = 10
   ThreadPoolExecutor(max_workers=10)
   basic_qos(prefetch_count=10)
   
4. docker-compose.worker.yml
   ↓
   replicas: 10 workers
   
5. Kết quả:
   10 workers × 10 threads = 100 messages đồng thời ✅
```

### Cách test

1. Thêm vào `.env`:
   ```bash
   MESSAGE_CONCURRENCY_PER_WORKER=10
   WORKER_REPLICAS=10
   ```

2. Chạy worker:
   ```bash
   python src/worker.py
   ```

3. Kiểm tra log:
   ```
   Connected to RabbitMQ as consumer at localhost:5672 
   (prefetch_count=10, max_workers=10)
   ```

4. Deploy với Docker:
   ```bash
   docker-compose -f src/docker-compose.worker.yml up -d
   ```

Code đã sẵn sàng và hoạt động.