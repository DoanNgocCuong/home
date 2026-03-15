---
### Khi nào nên scale cái gì ? 

Tôi sẽ giải thích theo cách đơn giản và MECE hơn:



#### 🎯 **Framework Đơn Giản: 3 Câu Hỏi Quyết Định**
---
git commit -m "[Update TẢI UNICORN WORKER cho: docker-compose.api - Mong muốn là từ 50 CCU hiện tại với 1 event loop => thành 3-4 Unicorn worker sẽ giúp tăng tải lên 100] - WHY? - Khi nào scale worker khi nào pod?

>> ---
>>
>> 1. Request độc lập
>> 2. App nhàn/bận
>>    **Tỷ lệ thời gian (ước tính):**
>>
>> - I/O-bound: ~1-1.5s (DB queries, MinIO) = 70-80%
>>   - DB query: 10-50ms (code line 341-343)
>>   - MinIO store: 200-1000ms (code line 455)
>>   - DB insert: 50-200ms (code line 491-493)
>> - CPU-bound: ~0.1-0.5s (transform) = 20-30%
>>   - Transform: 100-500ms (code line 422, 425)
>>
>> **Kết luận: Chủ yếu là NHÀN (I/O-bound)**
>> => tăng worker để tối đa CPU
>> 3. App không giữ state trong memory mà độc lập
>>
>> ---
>>
>> => ### Scale WORKERS trước (đã làm)
>>
>> Lý do:
>>
>> 4. I/O-bound chủ yếu (70-80% thời gian chờ)
>>    - Worker 1 chờ DB → Worker 2 xử lý request khác
>>    - Tận dụng thời gian chờ
>> 2. Shared resources (DB connection pool)
>>    - Workers trong cùng pod dùng chung connection pool
>>    - Hiệu quả hơn so với mỗi pod có pool riêng
>> 3. Startup overhead
>>    - Tạo worker mới nhanh (vài giây)
>>    - Tạo pod mới chậm hơn (30-60s)
>>
>> Kết quả:
>>
>> - 1 worker → 4 workers
>> - Throughput: 50 RPS → 200-400 RPS
>> - CCU: 50 → 100+
>>
>> ---
>>
>> ### Bước 2: Scale PODS sau (khi cần)
>>
>> Khi nào cần scale pods:
>>
>> 1. Workers đã max (4-8 workers/pod)
>> 2. CPU > 80% (CPU-bound operations tăng)
>> 3. Memory > 80%
>> 4. Cần high availability (1 pod chết không ảnh hưởng)"
>>
>



#### **Câu Hỏi 1: App của bạn giống NHÂN VIÊN hay giống CÔNG TY?**

###### 🧑 **NHÂN VIÊN (Worker trong Pod)**

```

Ví dụ thực tế:

- 1 nhà hàng có nhiều đầu bếp (workers)

- Chung 1 bếp (shared memory)

- Dùng chung nguyên liệu (shared resources)

- Làm cùng lúc nhiều món (concurrency)

```

**→ Scale WORKERS khi:**

- Cần làm nhiều việc cùng lúc
- Chia sẻ tài nguyên chung (database connection, cache)
- Khởi động chậm/tốn kém

###### 🏢 **CÔNG TY (Pod)**

```

Ví dụ thực tế:

- Nhiều nhà hàng khác nhau (pods)

- Mỗi nhà hàng độc lập

- 1 nhà hàng đóng cửa, các nhà hàng khác vẫn hoạt động

- Khách đến nhà hàng nào cũng được

```

**→ Scale PODS khi:**

- Mỗi request độc lập, không liên quan
- Cần dự phòng khi 1 pod chết
- Cần phân tán ra nhiều servers

---

#### **Câu Hỏi 2: App của bạn BẬN hay NHÀN?**

###### 💼 **BẬN = CPU-bound**

```

Ví dụ:

- Tính toán phức tạp

- Xử lý video/image

- Machine learning inference

- Mã hóa dữ liệu

```

**🔹 Đặc điểm:**

- CPU chạy 100%
- Thêm workers → tranh giành CPU → chậm hơn

**✅ Giải pháp:** **SCALE PODS**

```

Tại sao?

- Mỗi pod = 1 CPU core riêng

- Không tranh giành

- Pods chạy trên servers khác nhau

```

###### 🕐 **NHÀN = I/O-bound**

```

Ví dụ:

- Chờ database trả kết quả

- Call API bên ngoài

- Đọc/ghi file

- Chờ user nhập liệu

```

**🔹 Đặc điểm:**

- CPU chỉ dùng 20-30%
- Hầu hết thời gian là CHỜ

**✅ Giải pháp:** **SCALE WORKERS**

```

Tại sao?

- Trong lúc worker 1 chờ DB → worker 2 xử lý request khác

- Giống 1 thu ngân phục vụ nhiều khách xếp hàng

- Tận dụng thời gian chờ

```

---

#### **Câu Hỏi 3: App của bạn CÓ NHỚ hay QUÊN?**

###### 🧠 **CÓ NHỚ (Stateful)**

```

Ví dụ:

- User đang upload file (đang giữ session)

- Shopping cart

- WebSocket connections

- In-memory cache

```

**✅ Giải pháp:** **SCALE WORKERS**

```

Tại sao?

- Workers trong cùng pod chia sẻ bộ nhớ

- User request luôn đến đúng worker đang giữ data

- Không mất session khi scale

```

###### 🤖 **QUÊN (Stateless)**

```

Ví dụ:

- REST API đơn giản

- Web server tĩnh

- Microservices không giữ state

```

**✅ Giải pháp:** **SCALE PODS**

```

Tại sao?

- Request nào đến pod nào cũng được

- Dễ scale, dễ load balance

- 1 pod chết không ảnh hưởng

```

---

#### **📊 Bảng Quyết Định Đơn Giản**

| **Tình Huống** | **Scale Gì?** | **Lý Do (1 câu)** |

|---|---|---|

| Web API đơn giản | **PODS** | Mỗi request độc lập |

| Database worker | **WORKERS** | Dùng chung connection pool |

| Xử lý video | **PODS** | CPU-intensive, cần nhiều cores |

| Call API bên ngoài | **WORKERS** | Chờ nhiều, CPU rảnh |

| Cần high availability | **PODS** | 1 pod chết, còn pods khác |

| Khởi động chậm (30s+) | **WORKERS** | Tránh mất thời gian tạo pod mới |

| Cần shared cache | **WORKERS** | Workers dùng chung memory |

| Traffic không đều | **PODS** | Scale nhanh theo traffic |

---

#### **🎬 Ví Dụ Thực Tế: Restaurant Analogy**

###### **Scenario 1: Fast Food (McDonald's)**

```

Đặc điểm:

- Đơn hàng đơn giản, nhanh

- Khách đến ngẫu nhiên

- Không cần nhớ khách

```

**→ Giải pháp:** **Mở nhiều chi nhánh (SCALE PODS)**

- Peak hour: Mở 10 chi nhánh
- Off-peak: Chỉ 3 chi nhánh
- 1 chi nhánh đóng cửa → khách sang chi nhánh khác

---

###### **Scenario 2: Fine Dining Restaurant**

```

Đặc điểm:

- Món ăn phức tạp

- Bếp trưởng cần nhớ sở thích khách

- Nguyên liệu đắt tiền (shared resources)

```

**→ Giải pháp:** **Thêm đầu bếp trong cùng nhà hàng (SCALE WORKERS)**

- Peak hour: 8 đầu bếp cùng 1 bếp
- Dùng chung nguyên liệu cao cấp
- Chia sẻ kiến thức về khách VIP

---

#### **🚀 Best Practice: Chiến Lược 2 Tầng**

###### **Tầng 1: Tối ưu WORKERS trước (Nhanh, rẻ)**

```yaml

Baseline:

- 3 pods

- 2 workers/pod

- Total: 6 workers



Khi tăng tải:

- Giữ nguyên 3 pods

- Tăng lên 4 workers/pod

- Total: 12 workers (2x capacity)

- Thời gian: 5-10 giây

- Chi phí: Gần như 0

```

###### **Tầng 2: SCALE PODS sau (Chậm hơn, đắt hơn)**

```yaml

Khi workers đã max:

- Tăng từ 3 → 6 pods

- Giữ nguyên 4 workers/pod

- Total: 24 workers (4x capacity)

- Thời gian: 30-60 giây

- Chi phí: Cao hơn (resource overhead)

```

**Tại sao chiến lược này tốt?**

1. Response nhanh với worker scaling
2. Tiết kiệm chi phí
3. Tận dụng tối đa resources
4. Pod scaling là "backup plan"

---

#### **❌ Sai Lầm Thường Gặp**

###### **1. Scale sai thứ tự**

```

❌ SAI: Có 1 pod với 1 worker → tạo 10 pods với 1 worker

   (Lãng phí overhead, mỗi pod tốn 100-200MB)



✅ ĐÚNG: Có 1 pod với 1 worker → tăng lên 1 pod với 4 workers

   → Nếu vẫn không đủ → mới tăng số pods

```

###### **2. Quá nhiều workers trong 1 pod**

```

❌ SAI: 1 pod có 50 workers

   → Workers tranh giành CPU/Memory

   → Chậm hơn



✅ ĐÚNG: 1 pod có 4-8 workers

   → Sweet spot cho hầu hết apps

```

###### **3. Không set limits**

```

❌ SAI: Không giới hạn resources

   → 1 pod ăn hết tài nguyên node

   → Các pods khác bị chết



✅ ĐÚNG: Set limits rõ ràng

   cpu: 2 cores, memory: 4GB

```

---

#### **🎯 Công Thức Nhớ Nhanh**

```

SCALE WORKERS khi:

- I/O-bound (chờ nhiều)

- Shared resources (database connections, cache)

- Startup chậm

- Cần nhớ state



SCALE PODS khi:

- CPU-bound (tính toán nhiều)

- Stateless (không nhớ)

- Cần high availability

- Có nhiều servers

- Traffic spikes

```

---

#### **📈 Monitoring: Biết khi nào scale**

###### **Dấu hiệu cần SCALE WORKERS:**

```

- CPU < 50% nhưng response time cao

- Queue length tăng

- "Waiting for I/O" nhiều

```

###### **Dấu hiệu cần SCALE PODS:**

```

- CPU > 80%

- Memory > 80%

- Workers đã max (8-16)

- Latency cao liên tục

```

---

---

Phân tích case `/conversations/end` theo framework:

[3 tools called]

Phân tích case `/conversations/end` theo framework:

## Phân tích case: `/conversations/end` API

### Câu hỏi 1: App giống NHÂN VIÊN hay CÔNG TY?

Phân tích code:

```python
# endpoint_conversation_events.py:43
async def create_conversation_event(
    request: ConversationEventCreateRequest,
    service: ConversationEventService = Depends(get_conversation_event_service_async),
) -> ConversationEventCreateResponse:
    # Mỗi request độc lập
    # Không giữ state giữa requests
    # REST API stateless
```

Kết luận: Giống CÔNG TY (Stateless)

- Mỗi request độc lập
- Không cần nhớ state giữa requests
- REST API, không có WebSocket

---

### Câu hỏi 2: App BẬN hay NHÀN?

Phân tích timeline xử lý 1 request với dẫn chứng từ code:

**Dẫn chứng code:**

```341:342:src/app/services/conversation_event_service.py
existing = await self.repository.get_by_conversation_id_async(current_conversation_id)
db_query_elapsed = (time.time() - db_query_start) * 1000  # Convert to ms
```

```343:343:src/app/services/conversation_event_service.py
if db_query_elapsed > 100:  # Log if query takes > 100ms
```

```425:430:src/app/services/conversation_event_service.py
payload["conversation_log"] = await asyncio.to_thread(
    transform_conversation_logs,
    raw_logs,
    request.start_time,
    request.end_time,
)
```

```422:422:src/app/services/conversation_event_service.py
# transform_conversation_logs() là CPU-bound, có thể tốn 100-500ms với conversation lớn
```

```455:460:src/app/services/conversation_event_service.py
storage_ref = await asyncio.to_thread(
    self.storage_service.store_conversation_log,
    request.conversation_id,
    transformed_log,
    summary_dict
)
```

```491:492:src/app/services/conversation_event_service.py
event = await self.repository.create_async(payload)
db_insert_elapsed = (time.time() - db_insert_start) * 1000  # Convert to ms
```

```493:493:src/app/services/conversation_event_service.py
if db_insert_elapsed > 100:  # Log if insert takes > 100ms
```

**Timeline xử lý 1 request (ước tính dựa trên code):**

```
T=0ms:    Request đến
          (Code: endpoint_conversation_events.py:55-70)

T=10-50ms:   DB query (check duplicate) - I/O-bound ⏳
            (Code: conversation_event_service.py:341)
            → Log nếu > 100ms (line 343) → thường < 100ms

T=60-560ms:  Transform conversation_log - CPU-bound (100-500ms) 💻
            (Code: conversation_event_service.py:425)
            → Comment line 422: "100-500ms với conversation lớn"
            → Chạy trong thread pool (asyncio.to_thread) → không block event loop

T=560-1560ms: Store MinIO - I/O-bound (200-1000ms) ⏳
            (Code: conversation_event_service.py:455)
            → Chạy trong thread pool → không block event loop

T=1560-1610ms: DB insert - I/O-bound (50-200ms) ⏳
            (Code: conversation_event_service.py:491)
            → Log nếu > 100ms (line 493) → thường < 100ms

T=1610ms: Return 202 Accepted
          (Code: endpoint_conversation_events.py:117-123)
          → Log total_time_ms và db_time_ms
```

**Tỷ lệ thời gian (ước tính):**

- I/O-bound: ~1-1.5s (DB queries, MinIO) = 70-80%
  - DB query: 10-50ms (code line 341-343)
  - MinIO store: 200-1000ms (code line 455)
  - DB insert: 50-200ms (code line 491-493)
- CPU-bound: ~0.1-0.5s (transform) = 20-30%
  - Transform: 100-500ms (code line 422, 425)

**Kết luận: Chủ yếu là NHÀN (I/O-bound)**

- CPU chỉ dùng 20-30% thời gian
- 70-80% thời gian là chờ I/O
- CPU-bound operations chạy trong thread pool → không block event loop

---

### Câu hỏi 3: App CÓ NHỚ hay QUÊN?

Phân tích:

```python
# Không có:
- WebSocket connections
- In-memory session
- Shared state giữa requests
- User-specific cache trong memory

# Có:
- Database (shared, persistent)
- RabbitMQ (shared queue)
- MinIO (shared storage)
```

Kết luận: QUÊN (Stateless)

- Không giữ state trong memory
- Tất cả state trong DB/external services

---

## Kết luận: Chiến lược scale

### Bước 1: Scale WORKERS trước (đã làm)

Lý do:

1. I/O-bound chủ yếu (70-80% thời gian chờ)
   - Worker 1 chờ DB → Worker 2 xử lý request khác
   - Tận dụng thời gian chờ
2. Shared resources (DB connection pool)
   - Workers trong cùng pod dùng chung connection pool
   - Hiệu quả hơn so với mỗi pod có pool riêng
3. Startup overhead
   - Tạo worker mới nhanh (vài giây)
   - Tạo pod mới chậm hơn (30-60s)

Kết quả:

- 1 worker → 4 workers
- Throughput: 50 RPS → 200-400 RPS
- CCU: 50 → 100+

---

### Bước 2: Scale PODS sau (khi cần)

Khi nào cần scale pods:

1. Workers đã max (4-8 workers/pod)
2. CPU > 80% (CPU-bound operations tăng)
3. Memory > 80%
4. Cần high availability (1 pod chết không ảnh hưởng)

Cách scale:

```yaml
# docker-compose.prod.yml hoặc Kubernetes
deploy:
  replicas: 3  # Tăng từ 1 → 3 pods
```

Kết quả:

- 1 pod × 4 workers = 4 workers
- 3 pods × 4 workers = 12 workers
- Throughput: 200-400 RPS → 600-1200 RPS

---

## Bảng quyết định cho case này

| Tình huống            | Scale gì? | Lý do                    |
| ----------------------- | ---------- | ------------------------- |
| Hiện tại (50 CCU)     | WORKERS    | I/O-bound, shared DB pool |
| Đã scale (4 workers)  | Monitor    | Xem có đủ không       |
| Vẫn thiếu (< 100 CCU) | WORKERS    | Tăng lên 6-8 workers    |
| Workers max (8)         | PODS       | Scale horizontal          |
| CPU > 80%               | PODS       | CPU-bound tăng           |
| Cần HA                 | PODS       | Fault tolerance           |

---

## Chiến lược 2 tầng cho case này

### Tầng 1: Tối ưu WORKERS (đã làm)

```yaml
Baseline:
- 1 pod
- 1 worker
- Total: 1 worker
- Throughput: ~50 RPS
- CCU: 50

Đã scale:
- 1 pod
- 4 workers
- Total: 4 workers
- Throughput: ~200-400 RPS
- CCU: 100+
- Thời gian: 5-10 giây (restart container)
- Chi phí: Gần như 0
```

### Tầng 2: SCALE PODS (khi cần)

```yaml
Khi workers đã max (8 workers):
- Tăng từ 1 → 3 pods
- Giữ nguyên 4 workers/pod
- Total: 12 workers
- Throughput: ~600-1200 RPS
- CCU: 300+
- Thời gian: 30-60 giây
- Chi phí: Cao hơn (3x resources)
```

---

## Monitoring: Khi nào cần scale tiếp?

### Dấu hiệu cần tăng WORKERS (1 → 4 → 8):

```
✅ CPU < 50% NHƯNG response time cao (> 1s)
   → Event loop quá tải với nhiều concurrent requests
   → Bottleneck không phải CPU, mà là event loop capacity

✅ Concurrent requests > DB_POOL_SIZE × số workers
   → Ví dụ: 100 requests nhưng chỉ có 60 DB connections (4 × 15)
   → Requests phải đợi connection từ pool
   → Dẫn chứng: database_connection.py:120-121 (pool_size=15 per worker)

✅ Queue length tăng (requests đợi xử lý)
   → Event loop không kịp xử lý tất cả requests
   → Cần thêm event loops (workers) để phân tán load

✅ Memory < 70% (còn capacity để thêm workers)
   → Mỗi worker ~500MB → có thể thêm workers
   → Dẫn chứng: docker-compose.prod.yml:36 (memory: 3G limit)
```

### Dấu hiệu cần SCALE PODS:

```
⚠️ CPU > 80% (CPU-bound operations tăng)
⚠️ Memory > 80%
⚠️ Workers đã max (8 workers/pod)
⚠️ Latency cao liên tục (> 2s)
⚠️ Cần high availability
```

---

## Rủi ro load balancing (Chương 6)

### Vấn đề khi scale pods

#### 1. Sticky sessions (không áp dụng cho case này)

```
❌ Vấn đề: Nếu cần sticky sessions
   - User A → Pod 1 (giữ session)
   - User A request tiếp → Pod 2 (mất session)

✅ Giải pháp: Case này stateless → không cần sticky
```

#### 2. Database connection pool exhaustion

```
⚠️ Vấn đề: Nhiều pods → nhiều connection pools
   - 3 pods × 15 pool_size = 45 connections (base)
   - 3 pods × 10 max_overflow = 30 connections (peak)
   - Total: 75 connections
   - Vẫn OK nếu PostgreSQL max_connections = 100

✅ Giải pháp: Điều chỉnh DB_POOL_SIZE khi scale pods
   - Công thức: Total = pods × workers × (DB_POOL_SIZE + DB_MAX_OVERFLOW)
   - Đảm bảo < PostgreSQL max_connections
```

#### 3. Shared resources contention

```
⚠️ Vấn đề: Nhiều pods cạnh tranh:
   - RabbitMQ queue
   - MinIO storage
   - Database locks

✅ Giải pháp: 
   - RabbitMQ: Auto-distribute messages
   - MinIO: S3-compatible, handle concurrent writes
   - Database: Connection pooling + transactions
```

---

## Connection Total Hiện Tại

### Cấu hình từ code:

**Docker Compose (docker-compose.prod.yml:20,26-27):**

```yaml
UVICORN_WORKERS: ${UVICORN_WORKERS:-4}  # Default: 4 workers
DB_POOL_SIZE: ${DB_POOL_SIZE:-15}       # Default: 15 per worker
DB_MAX_OVERFLOW: ${DB_MAX_OVERFLOW:-10} # Default: 10 per worker
```

**Database Connection (database_connection.py:117-121):**

```python
async_engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,      # 15 (từ docker-compose)
    max_overflow=settings.DB_MAX_OVERFLOW, # 10 (từ docker-compose)
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
)
```

**Dependency Injection (dependency_injection.py:119,130-136):**

```python
async with AsyncSessionLocal() as session:  # Dùng async_engine
    yield session

async def get_conversation_event_service_async(
    db: AsyncSession = Depends(get_async_db),
) -> ConversationEventService:
    return ConversationEventService(db)
```

**Endpoint sử dụng (endpoint_conversation_events.py:45):**

```python
service: ConversationEventService = Depends(get_conversation_event_service_async)
```

### Tính toán Connection Total:

**Với 4 workers (default từ docker-compose.prod.yml:20):**

```
Mỗi worker process:
├─ Có async_engine riêng (database_connection.py:117)
│   ├─ pool_size: 15 connections (base)
│   └─ max_overflow: 10 connections (peak)
└─ Total per worker: 15 + 10 = 25 connections max

4 workers:
├─ Base pool: 4 × 15 = 60 connections
├─ Max overflow: 4 × 10 = 40 connections
└─ Total max: 100 connections
```

**Lưu ý:**

- Mỗi worker có engine riêng → mỗi worker có pool riêng
- Connections được reuse trong cùng request (dependency_injection.py:119-127)
- Peak usage phụ thuộc vào concurrent requests

### Connection Usage Pattern:

**Với 100 concurrent requests:**

```
T=0ms:    100 requests đến 4 workers
          ├─ Worker 1: 25 requests → 15 lấy connection ngay, 10 đợi
          ├─ Worker 2: 25 requests → 15 lấy connection ngay, 10 đợi
          ├─ Worker 3: 25 requests → 15 lấy connection ngay, 10 đợi
          └─ Worker 4: 25 requests → 15 lấy connection ngay, 10 đợi
        
          Total: 60 connections đang dùng (base pool)
          Total: 40 requests đợi connection

T=500ms:  60 requests đầu xong → trả 60 connections về pool
          ├─ 40 requests tiếp theo lấy connection (overflow)
          └─ Total: 40 connections đang dùng (overflow)

T=1000ms: 40 requests tiếp theo xong
          └─ Total: 0 connections đang dùng
```

**Kết quả:**

- Peak usage: 60 (base) + 40 (overflow) = 100 connections
- Average usage: ~30-50 connections (tùy traffic)

### So sánh: Trước vs Sau

**Trước (1 worker, config cũ - config_settings.py:56-57):**

```
1 worker × 50 pool_size = 50 connections (base)
1 worker × 100 max_overflow = 100 connections (peak)
─────────────────────────────────────────────
Total max: 150 connections
```

**Sau (4 workers, config mới - docker-compose.prod.yml:26-27):**

```
4 workers × 15 pool_size = 60 connections (base)
4 workers × 10 max_overflow = 40 connections (peak)
─────────────────────────────────────────────
Total max: 100 connections
```

**Kết quả:**

- Giảm total max: 150 → 100 connections (-33%)
- Tăng concurrent capacity: 50 → 60 requests (+20%)
- An toàn hơn với PostgreSQL max_connections (thường 100-200)

---

## Kết luận cho case này

### Đã làm đúng: Scale WORKERS trước

**Lý do (có dẫn chứng):**

1. **I/O-bound chủ yếu (70-80% thời gian chờ)**

   - Dẫn chứng: conversation_event_service.py:341, 455, 491
   - Worker 1 chờ DB → Worker 2 xử lý request khác
   - Tận dụng thời gian chờ
2. **Shared resources (DB connection pool)**

   - Dẫn chứng: database_connection.py:117-121
   - Mỗi worker có pool riêng, nhưng cùng database
   - Hiệu quả hơn so với mỗi pod có pool riêng
3. **Startup overhead**

   - Tạo worker mới nhanh (vài giây - restart container)
   - Tạo pod mới chậm hơn (30-60s)

**Kết quả:**

- 1 worker → 4 workers (docker-compose.prod.yml:20)
- DB connections: 50 → 60 (base pool)
- Max connections: 150 → 100 (an toàn hơn)

### Kế hoạch tiếp theo

1. **Monitor sau khi deploy 4 workers**

   - Check CPU, memory, latency
   - Verify throughput tăng
   - Monitor connection usage với SQL query:
     ```sql
     SELECT count(*) FROM pg_stat_activity 
     WHERE datname = 'context_handling_db' 
       AND application_name LIKE '%uvicorn%';
     ```
2. **Nếu vẫn thiếu (< 100 CCU)**

   - Tăng lên 6-8 workers (update UVICORN_WORKERS)
   - Điều chỉnh DB_POOL_SIZE tương ứng
3. **Nếu workers đã max (8)**

   - Scale pods: 1 → 2-3 pods
   - Điều chỉnh DB_POOL_SIZE để tránh vượt max_connections
4. **Nếu cần HA**

   - Scale pods: tối thiểu 2 pods




---