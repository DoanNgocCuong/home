### Câu trả lời ngắn gọn

**Hiện tại không thấy bug “rò rỉ bộ nhớ” (memory leak) kiểu kinh điển** trong code (như giữ reference vô hạn trong global list), nhưng có **một số trường hợp “memory bloat / memory growth dài hạn” rất dễ xảy ra**, nhìn từ thiết kế hiện tại.

Dưới đây là các case cụ thể (liên quan trực tiếp worker + load conversation nặng):

---

### 1. Worker giữ DB connection / session quá lâu (leak theo pool)

- **Code**: `RabbitMQConsumer._process_message()`
- **Điểm rủi ro**:
  - Mỗi message: `db = SessionLocal()`
  - Nếu trong `process_single_event()` có bug khiến:
    - Không throw exception (nên không vào rollback)
    - Nhưng cũng không kết thúc task đúng cách (ví dụ: loop vô hạn, block I/O,…)
  - Khi đó:
    - Thread giữ `db` + connection **rất lâu**
    - Dù có `finally: db.close()` nhưng nếu task không bao giờ tới `finally` → connection “bị giữ” gần như vĩnh viễn.
- **Kết quả**:
  - Connection pool bị “ngốn dần” (tưởng là leak, thật ra là long-lived connection).
  - Dưới load cao có thể giống memory leak: RAM tăng dần, pool full, app nghẹt.

---

### 2. Large `conversation_log` / `raw_conversation_log` sống lâu trong memory

- **Ở API**:
  - `request.model_dump(mode="json")` → tạo một bản copy full payload
  - `transform_conversation_logs()` → tạo thêm cấu trúc mới
  - Nếu conversation lớn (hàng nghìn message, text dài) → mỗi request nhân 2–3 lần memory.
- **Ở Worker**:
  - Message body RabbitMQ chứa `conversation_log` → `json.loads(body)` tạo object lớn trong RAM
  - `ConversationEvent` model (SQLAlchemy) giữ `conversation_log` / `raw_conversation_log` trong instance cho đến khi:
    - Session commit/close
    - Object được GC
- **Khi nào giống leak**:
  - Nếu worker giữ nhiều event trong một session lâu (VD: future thêm batch process, hoặc code lỡ giữ list các event trong biến toàn cục) → RAM tăng dần và không giảm nhanh.
  - Python GC không giải phóng tức thì → dưới monitoring sẽ thấy RAM chỉ tăng, ít giảm → cảm giác như leak.

---

### 3. Poison message + infinite retry → memory + queue “phình dài hạn”

- **Code**: `basic_nack(requeue=True)`
- **Rủi ro**:
  - Một message “bị lỗi logic” (poison) luôn ném exception.
  - Worker:
    - Load body lớn vào RAM
    - Parse JSON
    - Tạo DB session
    - Load event từ DB (có `conversation_log` lớn)
    - Gọi `process_single_event()` → crash → rollback → close
    - NACK requeue → lặp lại vô hạn.
- **Kết quả**:
  - **Không đúng nghĩa leak về mặt kỹ thuật**, nhưng:
    - RAM và CPU của worker luôn bị ăn bởi cùng một message
    - Số lượng object tạo ra và GC liên tục → memory fragmentation, RSS process tăng dần.
  - Nhìn từ monitoring → rất “giống” memory leak P0.

---

### 4. Memory growth do LLM / Memory API formatters (indirect)

- **Code**: `format_conversation_for_llm()`, `format_conversation_for_memory_api()`
- **Rủi ro**:
  - Nếu có chỗ nào gọi các hàm này trên full `conversation_log` **mà không truncate** (LLM đang off nhưng future có thể on lại):
    - Tạo string rất dài (hàng chục nghìn ký tự) trong RAM.
  - Nếu log level `INFO`/`DEBUG` in full text → log file/phần memory cho logging cũng phình.
- **Hiện tại**: Đã có truncate cho LLM, nên **rủi ro vừa phải**, nhưng pattern này dễ bị tái phạm nếu ai đó patch thêm chỗ dùng mới.

---

### 5. Memory bloat từ worker process sống rất lâu

- **Đặc thù worker**:
  - Là process long-running (chạy nhiều ngày / tuần).
  - Dù không có leak rõ rệt, **fragmentation + object churn** (tạo/xóa object lớn liên tục) vẫn làm **RSS của process chỉ tăng, không giảm**.
- **Kết hợp với:**
  - Large JSONB
  - Nhiều thread cùng xử lý
  - Không có cơ chế restart định kỳ / autoscaling / HPA
- ⇒ Rất dễ bị “leak theo thời gian” ở mức OS quan sát.

---

### 6. Config sai khiến memory trông như leak

- **Ví dụ**:
  - `WORKER_CONCURRENCY_PER_WORKER` quá cao so với RAM/node.
  - `DB_POOL_SIZE` / `DB_MAX_OVERFLOW` quá lớn → nhiều connection, mỗi connection có buffer, cache riêng.
- Không phải bug trong code, nhưng **tạo hiệu ứng giống leak** khi tăng load: RAM tăng gần tuyến tính với concurrency.

---

### Tóm lại

- **Không thấy một dòng code nào giữ reference vô hạn kiểu: list global append mãi không xóa.**
- Nhưng có **nhiều pattern dễ gây “memory growth dài hạn / dễ bị hiểu là leak”**:
  - Long-lived DB sessions nếu task không kết thúc
  - Large `conversation_log` / JSONB lặp lại quá nhiều lần (API + worker)
  - Poison messages retry vô hạn
  - Worker sống lâu, không restart định kỳ

Nếu bạn muốn, tớ có thể liệt kê **checklist cụ thể để debug memory** (trên Pod / container):

- metric nào cần bật (RSS, heap, pool usage),
- log gì cần thêm,
- và cách chứng minh là leak thật hay chỉ là bloat / fragmentation.


---



Đang phân tích luồng dữ liệu hiện tại:

[4 tools called]

Đang đọc thêm các file để hiểu rõ luồng xử lý:

[3 tools called]

## Luồng đi của data hiện tại

### Tổng quan

```
Client (spring-robot)
  ↓ HTTP POST
API Endpoint (/v1/conversations/end)
  ↓ Save to DB (status=PENDING)
  ↓ Fire-and-forget publish
RabbitMQ Queue
  ↓ Consume message
Worker (RabbitMQ Consumer)
  ↓ Process event
  ↓ Calculate score (LLM + Memory API)
  ↓ Update friendship_status & topic_metrics
Database (status=PROCESSED)
```

---

### Chi tiết từng bước

#### Bước 1: API nhận request

File: `src/app/api/v1/endpoints/endpoint_conversation_events.py`

```python
POST /v1/conversations/end
  ↓
1. Validate request (conversation_id, user_id, bot_id, conversation_log)
2. Transform conversation_log (nếu cần) → Thread pool (asyncio.to_thread)
3. Save to DB (status=PENDING) → Async DB operation
4. Publish to RabbitMQ → Fire-and-forget (asyncio.create_task)
5. Return 202 Accepted (< 100ms)
```

Data flow:

- Input: `ConversationEventCreateRequest` (JSON)
- Transform: `transform_conversation_logs()` (CPU-bound → thread pool)
- Save: `ConversationEvent` model → PostgreSQL
- Publish: Message → RabbitMQ queue

---

#### Bước 2: RabbitMQ Consumer nhận message

File: `src/app/background/rabbitmq_consumer.py`

```python
RabbitMQ Queue
  ↓
callback() → Submit vào ThreadPoolExecutor
  ↓
_process_message() (chạy trong thread riêng)
  ↓
1. Parse JSON message → conversation_id
2. Tạo DB session mới (SessionLocal)
3. Lấy event từ DB (status=PENDING)
4. Setup services
5. Process event
6. ACK/NACK message
```

Data flow:

- Message body: `{"conversation_id": "...", "user_id": "...", "bot_id": "...", "conversation_log": [...]}`
- Parse: `json.loads(body)` → Thread pool (không block event loop)
- DB query: `SELECT * FROM conversation_events WHERE conversation_id = ?`

---

#### Bước 3: Process event

File: `src/app/services/conversation_event_processing_service.py`

```python
process_single_event(event_id)
  ↓
1. Mark status=PROCESSING
2. Check bot_type (skip nếu NEXT_LESSON)
3. Calculate friendship score
   ├─ Fetch conversation_log từ DB
   ├─ Analyze với LLM (2 calls song song)
   │  ├─ analyze_user_questions_async()
   │  └─ analyze_session_emotion_async()
   └─ Extract memories (Memory API)
4. Update friendship_status
5. Update topic_metrics (nếu có agent_tag)
6. Mark status=PROCESSED
```

Data flow:

- Input: `event_id` (integer)
- Fetch: `conversation_log` từ DB (JSONB)
- LLM analysis: `analyze_conversation_with_llm_async()` → Parallel execution
- Memory extraction: `extract_memories_from_api()` → Async HTTP call
- Output: `friendship_score_change`, `session_emotion`, `user_initiated_questions`, `new_memories_count`

---

#### Bước 4: Calculate friendship score

File: `src/app/services/friendship_score_calculation_service.py`

```python
calculate_score_from_conversation_id(conversation_id)
  ↓
1. Fetch conversation_log từ DB
2. Check metadata completeness
3. Nếu incomplete → analyze_conversation_with_llm_async()
   ├─ Format conversation → Thread pool (asyncio.to_thread)
   ├─ Parallel execution (asyncio.gather):
   │  ├─ get_questions() → LLM API (15s timeout)
   │  ├─ get_emotion() → LLM API (15s timeout)
   │  └─ get_memories() → Memory API (240s timeout)
   └─ Merge results vào metadata
4. Calculate score:
   ├─ base_score = total_turns * 0.5
   ├─ engagement_bonus = user_initiated_questions * 3
   ├─ emotion_bonus = mapping (interesting: +15, boring: -15, ...)
   └─ memory_bonus = new_memories_count * 5
5. Return score_change + calculation_details
```

Data flow:

- Input: `conversation_log` (List[Dict])
- Format: `format_conversation_for_llm()` → Thread pool
- LLM calls: Groq API → JSON response → Parse
- Memory API: Mem0 API → Extract facts → Count
- Output: `friendship_score_change` (float), `calculation_details` (Dict)

---

#### Bước 5: Update friendship status & topic metrics

File: `src/app/services/friendship_status_update_service.py`

```python
apply_score_change(user_id, score_change)
  ↓
1. Get current friendship_status
2. Calculate new score = current_score + score_change
3. Determine new friendship_level (PHASE1_STRANGER, PHASE2_ACQUAINTANCE, PHASE3_FRIEND)
4. Update DB (friendship_score, friendship_level)

update_topic_metrics(user_id, topic_id, score_change, bot_id, turns_change)
  ↓
1. Get current topic_metrics
2. Update topic score = current_score + score_change
3. Update topic turns = current_turns + turns_change
4. Update agents_used (add bot_id)
5. Update friendship_score (cascade)
```

Data flow:

- Input: `user_id`, `score_change`, `topic_id`, `bot_id`
- DB queries: `SELECT/UPDATE` trên `friendship_status` và `topic_metrics`
- Output: Updated `friendship_level`, `friendship_score`, `topic_metrics`

---

### Sơ đồ luồng dữ liệu chi tiết

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. API ENDPOINT (FastAPI)                                      │
│    POST /v1/conversations/end                                  │
│    └─→ ConversationEventCreateRequest                         │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. CONVERSATION EVENT SERVICE                                   │
│    create_event_async()                                         │
│    ├─→ Transform conversation_log (thread pool)               │
│    ├─→ Save to DB (status=PENDING)                            │
│    └─→ Return data                                             │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. RABBITMQ PUBLISHER (Fire-and-forget)                        │
│    asyncio.create_task(publish_conversation_event())          │
│    └─→ Message → RabbitMQ Queue                                │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. RABBITMQ CONSUMER (Worker)                                   │
│    callback() → ThreadPoolExecutor                             │
│    └─→ _process_message() (thread riêng)                      │
│        ├─→ Parse JSON                                         │
│        ├─→ Tạo DB session                                      │
│        ├─→ Lấy event từ DB                                     │
│        └─→ Process event                                       │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. CONVERSATION EVENT PROCESSING SERVICE                         │
│    process_single_event(event_id)                              │
│    ├─→ Mark status=PROCESSING                                 │
│    ├─→ Calculate score                                         │
│    ├─→ Update friendship_status                                │
│    ├─→ Update topic_metrics                                    │
│    └─→ Mark status=PROCESSED                                  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. FRIENDSHIP SCORE CALCULATION SERVICE                         │
│    calculate_score_from_conversation_id()                      │
│    ├─→ Fetch conversation_log                                 │
│    ├─→ Analyze với LLM (parallel)                             │
│    │   ├─→ analyze_user_questions_async()                     │
│    │   └─→ analyze_session_emotion_async()                    │
│    ├─→ Extract memories (Memory API)                           │
│    └─→ Calculate score_change                                  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. FRIENDSHIP STATUS UPDATE SERVICE                             │
│    apply_score_change() + update_topic_metrics()               │
│    ├─→ Update friendship_score                                 │
│    ├─→ Update friendship_level                                 │
│    └─→ Update topic_metrics                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### Các điểm quan trọng

1. Non-blocking I/O:

   - API trả về 202 ngay (< 100ms)
   - RabbitMQ publish: fire-and-forget
   - LLM calls: async với timeout
   - Memory API: async với timeout
2. Thread pool cho CPU-bound:

   - JSON parsing: ThreadPoolExecutor
   - Conversation formatting: `asyncio.to_thread()`
   - Conversation log transformation: `asyncio.to_thread()`
3. Parallel execution:

   - LLM analysis: `asyncio.gather()` (2 LLM calls + 1 Memory API)
   - Giảm total time từ 45s → 15-20s
4. Error handling:

   - DB pool timeout: 10s (fail fast)
   - LLM timeout: 15s
   - Memory API timeout: 240s
   - RabbitMQ timeout: 5s
5. Data persistence:

   - Raw data: `raw_conversation_log` (JSONB)
   - Transformed data: `conversation_log` (JSONB)
   - Status tracking: `status` (PENDING → PROCESSING → PROCESSED)

---

### Tóm tắt

Luồng dữ liệu: API → DB → RabbitMQ → Worker → Processing → Score Calculation → Status Update → DB

Đặc điểm:

- Async/Non-blocking
- Thread pool cho CPU-bound operations
- Parallel execution cho LLM calls
- Timeout configurations cho tất cả external calls
- Fire-and-forget cho RabbitMQ publish

Kết quả:

- API response time: < 100ms
- Processing time: 15-20s (parallel LLM analysis)
- Zero blocking operations trong async context


---



### Ngắn gọn: Trạng thái hiện tại

**1. 504 / Timeout / Blocking I/O**

- **Đã xử lý ổn**:
  - Timeout full chain (Uvicorn, DB pool, statement_timeout, LLM, RabbitMQ, Memory API, HTTP slow request).
  - LLM + Memory API đã async, dùng thread pool đúng chỗ (JSON parsing, transform, format conversation).
  - RabbitMQ publish đã fire‑and‑forget, worker dùng thread pool, DB session luôn `close()` trong `finally`.
  - Bộ test `test_p0_timeout_resilience.py --test New_Alerts` pass → alert + timeout logic hoạt động.

**2. Các risk còn lại (theo docs `5_Opt_DataFlow_30122025`) – không phải bug, mà là “chỗ cần canh”:**

- **Poison message + retry vô hạn**

  - Nếu 1 message lỗi logic vĩnh viễn → bị `basic_nack(requeue=True)` mãi → tốn CPU/RAM dài hạn, queue không bao giờ sạch.
  - Hiện chưa có dead-letter queue / max retry count → đây là **risk cần design thêm**, không phải bug runtime.
- **Memory bloat dài hạn ở worker**

  - Worker là long‑running process, xử lý JSON/`conversation_log` lớn liên tục → dễ bị “memory growth theo thời gian” (fragmentation, bloat), dù không phải memory leak thực sự.
  - Tài liệu `docs5_Opt_DataFlow` đã note rõ: cần kết hợp **restart định kỳ / HPA / autoscaling** để an toàn về lâu dài.
- **Config tuning phụ thuộc load thật**

  - Các config như `DB_POOL_SIZE`, `DB_MAX_OVERFLOW`, `WORKER_CONCURRENCY_PER_WORKER`, timeout của Memory API (240s) hiện đang ở mức **an toàn theo lý thuyết**, nhưng:
  - Cần chạy **stress test trên môi trường gần Production** để chốt: pool có đủ không, có bị chờ connection nhiều không, Memory API có thường xuyên chạm 240s không.
- **Monitoring & Alert vẫn cần “nuôi dưỡng”**

  - Metrics Prometheus + alert Google Chat đã có, nhưng dashboard / threshold tối ưu (P95, P99, queue backlog, worker RSS memory) cần **theo dõi vài ngày** rồi chỉnh.

---

### Tóm lại

- **Hiện tại không thấy bug P0/P1 rõ ràng trong flow mới** (504 root cause đã fix, dataflow async + thread pool OK, tests xanh).
- **Còn lại chủ yếu là risk mang tính vận hành dài hạn**: poison message không giới hạn retry, memory bloat worker, và cần tuning thêm dựa trên số liệu thực tế (APM + Prometheus).
  Nếu bạn muốn, bước tiếp theo có thể là: mình giúp bạn viết **checklist “things to watch in production 1 tuần đầu”** cho module này.