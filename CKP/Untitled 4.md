# Langfuse Zero-Overhead Tracing - Low Level Design (LLD)

## 1. Problem Statement

### 1.1 Background
Langfuse SDK v3 khi tích hợp trực tiếp vào FastAPI service gây ra **overhead ~1s** do GIL (Global Interpreter Lock) contention khi background flush thread chạy trùng với request đang xử lý.

### 1.2 Root Cause
- Langfuse SDK dùng OpenTelemetry `BatchSpanProcessor`
- Background thread serialize + HTTP POST giữ GIL
- Khi flush trùng với request → event loop bị block

### 1.3 Solution
Tách biệt Langfuse publishing thành **independent worker process**, giao tiếp qua Redis queue.

### 1.4 Best Practices Implemented

Dựa trên MECE analysis, implementation áp dụng các best practices sau:

| Practice | Description | Status |
|----------|-------------|--------|
| **Trace Bundle** | Gom tất cả events vào 1 bundle, publish 1 lần thay vì 3 LPUSH | ✅ Implemented |
| **Langfuse SDK Native** | Worker gửi từng observation riêng lẻ, Langfuse tự reconstruct hierarchy | ✅ Implemented |
| **Backward Compatibility** | Worker hỗ trợ cả bundle format (mới) và legacy events | ✅ Implemented |
| **Graceful Degradation** | Redis/Langfuse down → log warning, không crash request | ✅ Implemented |

### 1.5 Known Issues & Fixes

Trong quá trình triển khai và test, đã phát hiện và fix các lỗi sau:

| # | Issue | Root Cause | Fix |
|---|-------|------------|-----|
| 1 | **Worker không gửi traces lên Langfuse** | Worker chỉ xử lý bundle format, không xử lý legacy events (từng event riêng lẻ) | Thêm logic phân biệt bundle vs legacy events trong `_process_batch()` |
| 2 | **Duplicate API_REQUEST_COMPLETE trong hierarchy** | Cả `trace()` và `span()` đều tạo root span với tên "API_REQUEST_COMPLETE" | Không tạo root span riêng, dùng trace trực tiếp làm parent |
| 3 | **vllm_chat_completion không nằm trong api_chat_completions** | Khi worker process LLM generation, parent span chưa tồn tại trong span_map, fallback về root_span | **Process spans TRƯỚC, rồi mới process generations SAU** |
| 4 | **Trace name sai trong UI** | Dùng "emotion-api-request" thay vì "API_REQUEST_COMPLETE" | Đổi trace name thành "API_REQUEST_COMPLETE" |

#### Chi tiết Fix: Event Ordering

```
# SAI (trước fix):
for gen in group.llm_generation_events:
    parent = span_map.get(gen.parent_span_id, root_span)  # span_map chưa có!
    gen_span = parent.generation(...)

# ĐÚNG (sau fix):
# FIRST: Create ALL API spans and add to span_map
for api_span in group.api_span_events:
    parent = span_map.get(api_span.parent_span_id, root_span)
    span = parent.span(...)
    span_map[api_span.span_id] = span

# SECOND: Create LLM generations (sau khi span_map đã có đầy đủ spans)
for gen in group.llm_generation_events:
    parent = span_map.get(gen.parent_span_id, root_span)
    gen_span = parent.generation(...)
```

#### Chi tiết Fix: Duplicate Root Span

```
# SAI (trước fix):
langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")
root_span = langfuse_trace.span(name="API_REQUEST_COMPLETE")  # DUPLICATE!
# → Tạo 2 nodes trong UI

# ĐÚNG (sau fix):
langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")
span_map[root.span_id] = langfuse_trace  # Dùng trace làm parent
# → api_chat_completions sẽ nested dưới trace's root span
```

#### Hierarchy đúng sau khi fix

```
API_REQUEST_COMPLETE (root từ trace())
  └── api_chat_completions
      └── vllm_chat_completion
```

### 1.6 Langfuse @observe Decorator - Why Not Used

**Q: Tại sao không dùng Langfuse `@observe` decorator thay vì tự build Redis queue + worker?**

**A:** `@observe` decorator không phù hợp với mục tiêu **zero-overhead** của architecture này.

#### So sánh hai approaches

| Aspect | @observe Decorator | Current Architecture (Redis + Worker) |
|--------|-------------------|--------------------------------------|
| **Latency impact** | ~5-50ms per call (sync) | ~1ms (async LPUSH, non-blocking) |
| **Execution** | Synchronous SDK call trong request path | Async push to Redis, worker xử lý riêng |
| **GIL contention** | Block event loop, contention với request | Worker có GIL riêng, không ảnh hưởng API |
| **Implementation** | Dễ (~1 dòng code) | Cần Redis + Worker + queue logic |
| **Flexibility** | Bị coupling với Langfuse SDK | Full control over data flow |

#### Tại sao @observe không zero-overhead

```python
# @observe decorator hoạt động như thế này:
@observe()
def my_function():
    # Langfuse SDK được gọi ĐỒNG BỘ tại đây
    # → Thêm latency vào request path
    return do_work()
```

- `@observe` gọi Langfuse SDK **ngay trong request path**
- SDK calls là **synchronous**, không async → block event loop
- Background flush thread của Langfuse gây GIL contention
- Đi ngược với mục tiêu: **tách Langfuse ra khỏi request path**

#### Các options nếu vẫn muốn dùng @observe

| Option | Description | Trade-off |
|--------|-------------|-----------|
| **Hybrid Mode** | Dev/QA: enable @observe, Production: dùng Redis queue | Worth effort? |
| **Custom Handler** | Override @observe handler để ghi vào Redis | Hacky, có thể break khi Langfuse update |
| **Background Thread** | Dùng @observe với threading để không block | Complex, potential race conditions |

#### Kết luận

Nếu **zero-overhead là requirement** (low latency AI service), tiếp tục với architecture hiện tại. `@observe` chỉ phù hợp khi:
- Chấp nhận thêm latency
- Không cần real-time performance
- Dùng cho debugging/monitoring đơn thuần

Architecture hiện tại đã tối ưu cho **production với high-throughput low-latency requirements**.

---

## 2. Architecture Overview

### 2.1 System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRODUCTION DEPLOYMENT                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │  emotion-api │     │     redis     │     │langfuse-     │               │
│  │   (FastAPI)  │     │  (queue)     │     │  worker      │               │
│  │              │     │              │     │              │               │
│  │  LPUSH       │ ──▶ │ langfuse:    │ ◀── │ BRPOP        │               │
│  │  (~1ms)      │     │ traces       │     │ (batch)      │               │
│  └──────────────┘     └──────────────┘     └──────┬───────┘               │
│                                                    │                        │
│                                                    ▼                        │
│                                          ┌──────────────────┐              │
│                                          │   Langfuse      │              │
│                                          │   Cloud         │              │
│                                          │   (Observability)│             │
│                                          └──────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRACE HIERARCHY                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  trace(id=trace_id)                                                         │
│  ├── span(API_REQUEST_COMPLETE)  [root - from middleware]                  │
│  │   └── span(api_chat_completions)  [child - from endpoint]              │
│  │       └── generation(vllm_chat_completion)  [leaf - from vllm_client]  │
│  │           ├── input: [messages]                                         │
│  │           ├── output: "excited"                                         │
│  │           └── usage: {input: 245, output: 2, total: 247}               │
│  │                                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Components

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| `emotion-api` | FastAPI | Nhận request, gọi vLLM, publish trace events |
| `TracePublisher` | asyncio + redis | LPUSH events vào Redis (~1ms overhead) |
| `Redis` | redis:7-alpine | Message queue `langfuse:traces` |
| `langfuse-worker` | Python process | BRPOP, batch process, gửi lên Langfuse |
| `Langfuse Cloud` | SaaS | UI hiển thị traces |

> **Note:** Trace name = "API_REQUEST_COMPLETE", root span cũng từ trace này nên không tạo duplicate.

---

## 3. Data Flow

### 3.1 Sequence Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │     │   API    │     │  Redis   │     │ Worker   │     │Langfuse  │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │                 │                 │                 │
     │ POST /v1/chat   │                 │                 │                 │
     │────────────────>│                 │                 │                 │
     │                 │                 │                 │                 │
     │                 │ Publish API     │                 │                 │
     │                 │ Request Event   │                 │                 │
     │                 │────────────────>│                 │                 │
     │                 │                 │                 │                 │
     │                 │                 │ LPUSH + OK      │                 │
     │                 │<────────────────│                 │                 │
     │                 │                 │                 │                 │
     │                 │ Call vLLM       │                 │                 │
     │                 │────────────────────────────────────────────────────>│
     │                 │<────────────────────────────────────────────────────│
     │                 │                 │                 │                 │
     │                 │ Publish LLM     │                 │                 │
     │                 │ Generation      │                 │                 │
     │                 │────────────────>│                 │                 │
     │                 │                 │                 │                 │
     │                 │                 │ BRPOP + event   │                 │
     │                 │                 │<────────────────│                 │
     │                 │                 │                 │                 │
     │                 │                 │ Group by        │                 │
     │                 │                 │ trace_id        │                 │
     │                 │                 │                 │                 │
     │                 │                 │                 │ Send trace     │
     │                 │                 │                 │────────────────>│
     │                 │                 │                 │                 │
     │                 │                 │                 │<────────────────│
     │                 │                 │                 │                 │
     │ 200 OK         │                 │                 │                 │
     │<────────────────│                 │                 │                 │
     │                 │                 │                 │                 │
```

> **Note:** Với **TraceBundle** (2026-03-10+), endpoint gom tất cả 3 events vào 1 bundle và publish 1 lần duy nhất:
>
> ```
> ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
> │  Client  │     │   API    │     │  Redis   │     │ Worker   │     │Langfuse  │
> └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
>      │                 │                 │                 │                 │
>      │ POST /v1/chat  │                 │                 │                 │
>      │────────────────>│                 │                 │                 │
>      │                 │                 │                 │                 │
>      │                 │ Call vLLM       │                 │                 │
>      │                 │────────────────────────────────────────────────────>│
>      │                 │<────────────────────────────────────────────────────│
>      │                 │                 │                 │                 │
>      │                 │ Build TraceBundle│                 │                 │
>      │                 │ (root + span +  │                 │                 │
>      │                 │  generation)    │                 │                 │
>      │                 │                 │                 │                 │
>      │                 │ Publish Bundle  │                 │                 │
>      │                 │ (1 LPUSH)       │                 │                 │
>      │                 │────────────────>│                 │                 │
>      │                 │                 │                 │                 │
>      │                 │                 │ LPUSH + OK      │                 │
>      │                 │<────────────────│                 │                 │
>      │                 │                 │                 │                 │
>      │                 │                 │ BRPOP + bundle  │                 │
>      │                 │                 │<────────────────│                 │
>      │                 │                 │                 │                 │
>      │                 │                 │ Parse bundle    │                 │
>      │                 │                 │ (bundle_type=  │                 │
>      │                 │                 │  trace_bundle)  │                 │
>      │                 │                 │                 │                 │
>      │                 │                 │                 │ Send trace     │
>      │                 │                 │                 │────────────────>│
>      │                 │                 │                 │                 │
>      │                 │                 │                 │<────────────────│
>      │                 │                 │                 │                 │
>      │ 200 OK         │                 │                 │                 │
>      │<────────────────│                 │                 │                 │
> ```
>
> **Benefits:**
> - Giảm Redis calls: 3 LPUSH → 1 LPUSH (66% reduction)
> - Worker nhận đầy đủ 3 events trong 1 message → **Không có race condition**
> - Hierarchy đúng: `trace > span > generation`

### 3.2 Event Types

| Event Type | Source | Description |
|------------|--------|-------------|
| `APIRequestEvent` | Middleware | Root span - toàn bộ request |
| `APISpanEvent` | Endpoint | Child span - xử lý API |
| `LLMGenerationEvent` | vllm_client | Leaf - LLM call details |

---

## 4. Component Specifications

### 4.1 TracePublisher (`trace_publisher.py`)

```python
class TracePublisher:
    """Publishes trace events to Redis queue."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        queue_name: str = "langfuse:traces",
        enabled: bool = True,
    ):
        ...

    async def connect() -> bool: ...
    async def publish(event: TraceEvent) -> bool: ...
    async def publish_batch(events: List[TraceEvent]) -> int: ...
    async def publish_api_request(...) -> bool: ...
    async def publish_api_span(...) -> bool: ...
    async def publish_llm_generation(...) -> bool: ...
    async def publish_trace_bundle(bundle: TraceBundle) -> bool: ...
```

**Key Features:**
- Async Redis operations (~1ms overhead)
- Graceful degradation: Redis down → log warning, không crash
- Batch publish support với pipeline
- **TraceBundle support**: Gom tất cả events vào 1 message → giảm 66% Redis calls (3 → 1 LPUSH)

### 4.2 TraceEvent Models (`trace_models.py`)

```python
@dataclass
class APIRequestEvent:
    """Root span: API_REQUEST_COMPLETE"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None  # Always None for root
    request_id: str
    start_time: float
    end_time: float
    http_method: str
    endpoint: str
    status_code: int
    client_ip: str
    user_agent: str
    status: str  # success, error
    error_message: Optional[str]

@dataclass
class APISpanEvent:
    """Intermediate span: api_chat_completions"""
    trace_id: str
    span_id: str
    parent_span_id: str  # Points to root
    request_id: str
    start_time: float
    end_time: float
    name: str = "api_chat_completions"
    input_summary: Optional[str]
    output_summary: Optional[str]
    status: str

@dataclass
class LLMGenerationEvent:
    """Leaf generation: vllm_chat_completion"""
    trace_id: str
    span_id: str
    parent_span_id: str  # Points to api_span
    request_id: str
    start_time: float
    end_time: float
    model: str
    input_messages: List[Dict]
    output_content: Optional[str]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    temperature: float
    max_tokens: Optional[int]
    original_emotion: Optional[str]
    randomized_emotion: Optional[str]
    emotion_changed: bool
    status: str

@dataclass
class TraceBundle:
    """
    Bundle chứa toàn bộ trace events cho một request.

    Thay vì publish từng event riêng lẻ (3 LPUSH),
    gom tất cả vào 1 bundle và publish 1 lần (1 LPUSH).
    Worker nhận 1 message = 1 trace hoàn chỉnh.

    Best Practice: Gom trace 1 lần cuối request thay vì publish từng event.
    """
    bundle_type: str = "trace_bundle"
    trace_id: str = ""
    request_id: str = ""
    root_span: Optional[APIRequestEvent] = None
    child_spans: List[APISpanEvent] = field(default_factory=list)
    generations: List[LLMGenerationEvent] = field(default_factory=list)
    service_name: str = "emotion-service"
    created_at: float = 0.0
```

### 4.3 LangfuseWorker (`langfuse_worker.py`)

```python
class LangfuseWorker:
    """Worker consumes trace events from Redis and sends to Langfuse."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        queue_name: str = "langfuse:traces",
        batch_size: int = 50,
        poll_timeout: int = 5,
    ):
        ...

    def run(self):
        """Main worker loop."""
        while not self._shutdown:
            self._process_batch()

    def _consume_batch(self) -> List[str]:
        """BRPOP + rpop up to batch_size."""

    def _group_by_trace(self, json_events) -> Dict[str, TraceGroup]:
        """Parse JSON, group by trace_id."""

    def _send_to_langfuse(self, group: TraceGroup):
        """
        Reconstruct hierarchy: trace > span > generation.

        Important: Process spans FIRST, then generations SECOND.
        This ensures span_map is populated before creating generations.
        """
```

---

## 5. Configuration

### 5.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection |
| `TRACE_QUEUE_NAME` | `langfuse:traces` | Queue key |
| `TRACE_PUBLISHING_ENABLED` | `true` | Enable/disable tracing |
| `LANGFUSE_SECRET_KEY` | - | Langfuse secret key |
| `LANGFUSE_PUBLIC_KEY` | - | Langfuse public key |
| `LANGFUSE_HOST` | `https://cloud.langfuse.com` | Langfuse host |
| `WORKER_BATCH_SIZE` | `50` | Max events per batch |
| `WORKER_POLL_TIMEOUT` | `5` | BRPOP timeout (seconds) |

### 5.2 Docker Compose Services

```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "16379:6379"
    profiles: [infra, full]

  emotion-api:
    environment:
      - REDIS_URL=redis://redis:6379/0
      - TRACE_QUEUE_NAME=langfuse:traces
      - TRACE_PUBLISHING_ENABLED=true
    profiles: [app, full]

  langfuse-worker:
    command: python -m infrastructure.observability.langfuse_worker
    environment:
      - REDIS_URL=redis://redis:6379/0
      - TRACE_QUEUE_NAME=langfuse:traces
      - WORKER_BATCH_SIZE=50
      - WORKER_POLL_TIMEOUT=5
    profiles: [worker, full]
```

### 5.3 Usage

```bash
# Chạy tất cả (infra + app + worker)
docker compose --profile full up -d

# Chỉ chạy API (không worker)
docker compose --profile app up -d

# Worker chạy riêng
docker compose --profile worker up -d
```

---

## 6. Error Handling

### 6.1 Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| Redis unavailable | Log warning, continue request, skip tracing |
| Langfuse unavailable | Log warning, events stay in queue |
| Worker crash | Events remain in Redis, retry on restart |
| JSON parse error | Log warning, skip event, continue batch |

### 6.2 Worker Recovery

```
Worker starts
    │
    ▼
Connect to Redis ──── FAIL ───▶ Exit with error
    │
    ▼
Connect to Langfuse ── FAIL ──▶ Continue (log only)
    │
    ▼
Main loop:
    │
    ├─ BRPOP timeout ──▶ Continue polling
    │
    ├─ Parse error ────▶ Log warning, skip
    │
    ├─ Send error ────▶ Log error, continue
    │
    └─ SIGTERM ──────▶ Cleanup + flush + exit
```

---

## 7. Performance Characteristics

### 7.1 Latency Impact

| Operation | Overhead |
|-----------|----------|
| `TracePublisher.publish()` | ~1ms |
| Redis LPUSH | ~0.1ms |
| Worker BRPOP | 5s (blocking) |
| Parse + send to Langfuse | ~10-50ms |

**Total end-to-end:** ~1ms added to API request (non-blocking)

### 7.2 Throughput

- **API:** ~1000 req/s (với 1 worker)
- **Worker:** Xử lý batch 50 events → ~20 batches/s
- **Redis:** Hỗ trợ ~100k ops/s

---

## 8. Monitoring

### 8.1 Health Checks

```bash
# Kiểm tra Redis queue
redis-cli LLEN langfuse:traces

# Kiểm tra worker logs
docker logs langfuse-worker

# Kiểm tra Langfuse dashboard
# Truy cập https://cloud.langfuse.com
```

### 8.2 Key Metrics

| Metric | Source | Description |
|--------|--------|-------------|
| `trace_publisher.publish.latency_ms` | API logs | Thời gian publish |
| `worker.events_processed` | Worker stats | Tổng events đã xử lý |
| `worker.traces_sent` | Worker stats | Tổng traces đã gửi |
| `worker.errors` | Worker stats | Số lỗi |
| `redis.llen.langfuse:traces` | Redis | Số events pending |

---

## 9. Trade-offs

### 9.1 Pros

| Benefit | Description |
|---------|-------------|
| Zero overhead | API latency không bị ảnh hưởng |
| Decoupled | Worker có GIL riêng, không block API |
| Scalable | Worker có thể scale horizontally |
| Resilient | Redis queue lưu events khi Langfuse down |
| Async | Non-blocking publishing từ API |

### 9.2 Cons

| Trade-off | Impact |
|-----------|--------|
| Eventual consistency | Traces hiển thị chậm ~1-5s |
| Additional infrastructure | Cần Redis + Worker container |
| Complexity | Thêm 2 components để maintain |

---

## 10. Appendix

### 10.1 Project Folder Structure

```
VeryFastMoodEmotionClassification_T12_2025/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI entrypoint
│   │   ├── config.py                    # Configuration
│   │   └── logging/
│   │       ├── __init__.py
│   │       ├── config.py                # Logging setup
│   │       ├── formatters.py            # JSON formatter
│   │       └── body_utils.py            # Body logging utilities
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── external/
│   │   │   ├── __init__.py
│   │   │   └── vllm_client.py          # vLLM client
│   │   │
│   │   └── observability/
│   │       ├── __init__.py
│   │       ├── trace_publisher.py      # Async Redis publisher
│   │       ├── langfuse_worker.py      # Worker process
│   │       └── trace_models.py         # Event data models
│   │
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   └── chat.py             # Chat completions endpoint
│   │   │   └── middleware/
│   │   │       ├── __init__.py
│   │   │       ├── correlation_id.py   # Correlation ID middleware
│   │   │       └── request_logger.py  # Request logging middleware
│   │   │
│   │   └── dto/
│   │       ├── __init__.py
│   │       └── emotion_dto.py          # Data transfer objects
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── emotion_randomizer.py      # Emotion randomization logic
│   │   └── prompt_manager.py          # Prompt templates
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml                  # All-in-one (profiles: infra, model, app, worker, full)
├── docker-compose.infra.yml            # Redis only
├── docker-compose.models.yml           # vLLM only
├── docker-compose.app.yml              # emotion-api only
├── docker-compose.worker.yml           # langfuse-worker only
│
├── .env                               # Environment variables (production)
├── .env.example                       # Environment variables template
│
└── docs/
    ├── CHANGELOG.md
    └── 5-CKP_research_plan_implement_docs/
        └── batch1/
            ├── research_docs.md
            ├── implement_docs_005.md
            └── LLD_Langfuse_Zero_Overhead_Tracing.md
```

### 10.2 Redis Queue Structure

```
Key: langfuse:traces (LIST)
┌─────────────────────────────────────────┐
│  [event_1, event_2, event_3, ...]      │
│  ↓                                     │
│  LPUSH ← new events                    │
│  BRPOP → worker consumes               │
└─────────────────────────────────────────┘

Event JSON structure:
{
  "event_type": "api_request|api_span|llm_generation",
  "trace_id": "uuid-v4",
  "span_id": "16-char-hex",
  "parent_span_id": "16-char-hex",
  "request_id": "uuid-v4",
  "start_time": 1234567890.123,
  "end_time": 1234567890.456,
  ...
}
```

### 10.3 Docker Network

```
Network: emotion-network (bridge)
┌─────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐   │
│  │ emotion-api  │  │ vllm-qwen    │   │
│  │   :8080     │  │   :30029     │   │
│  └──────────────┘  └──────────────┘   │
│  ┌──────────────┐  ┌──────────────┐   │
│  │ redis        │  │langfuse-     │   │
│  │   :6379      │  │  worker      │   │
│  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────┘
```

### 10.4 Environment Variables (.env.example)

```bash
# === Langfuse Configuration ===
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key-here
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# === Redis Configuration (for Langfuse tracing) ===
REDIS_URL=redis://redis:6379/0
TRACE_QUEUE_NAME=langfuse:traces
TRACE_PUBLISHING_ENABLED=true

# === Worker Configuration ===
WORKER_BATCH_SIZE=50
WORKER_POLL_TIMEOUT=5
```

### 10.5 References

- [Langfuse Documentation](https://langfuse.com/docs)
- [Redis Python Client](https://redis-py.readthedocs.io)
- [vLLM Documentation](https://docs.vllm.ai)

---

## 11. CHANGELOG - Revision History

| Version | Date | Description |
|---------|------|-------------|
| 1.5 | 2026-03-10 | **Enable TraceBundle in endpoint**: Cập nhật completions.py build và publish TraceBundle, cập nhật vLLM client return_generation_event parameter, thêm sequence diagram cho bundle flow, thêm TraceBundle vào TracePublisher interface |
| 1.4 | 2026-03-10 | Fix: Remove duplicate root span, fix trace name to API_REQUEST_COMPLETE, add hierarchy diagram |
| 1.3 | 2026-03-10 | Add section 1.6: Langfuse @observe Decorator - Why Not Used |
| 1.2 | 2026-03-10 | Add Known Issues & Fixes section: event ordering fix, duplicate trace name fix, backward compatibility |
| 1.1 | 2026-03-09 | Add TraceBundle model, update worker for bundle format, add best practices section |
| 1.0 | 2026-03-07 | Initial LLD |

---

*Generated: 2026-03-10*



Mình thấy 2 vấn đề trong Image 1 so với Image 2:

1. **Trace name sai**: `emotion-api-request` thay vì `API_REQUEST_COMPLETE`
2. **vllm_chat_completion bị lọt ra ngoài** api_chat_completions (parent_span_id mapping sai)

Để mình fix worker code:Mình không truy cập được trực tiếp server, nhưng dựa vào context, đây là **2 fix cần làm** trong `langfuse_worker.py`:

---

## Fix 1: Trace name → `API_REQUEST_COMPLETE`

Trong method `_send_to_langfuse`, tìm dòng tạo trace:

```python
# SỬA TỪ:
langfuse_trace = self.langfuse.trace(
    name="emotion-api-request",
    ...
)

# THÀNH:
langfuse_trace = self.langfuse.trace(
    name="API_REQUEST_COMPLETE",
    ...
)
```

## Fix 2: vllm_chat_completion bị lọt ra ngoài — Root cause

Vấn đề nằm ở **thứ tự events đến Redis**:

```
Thứ tự publish (LPUSH = push đầu list):
1. LLMGenerationEvent    ← publish TRƯỚC (trong vllm_client)
2. APISpanEvent           ← publish SAU  (trong endpoint)  
3. APIRequestEvent        ← publish CUỐI (trong middleware)

Worker BRPOP lấy từ cuối list:
→ Lấy được: [APIRequestEvent] → batch 1
→ Lấy tiếp: [APISpanEvent, LLMGenerationEvent] → batch 2

Batch 1: Chỉ có root span → tạo trace
Batch 2: Có api_span + generation
  → Nhưng trace đã gửi rồi ở batch 1!
  → api_span tạo OK (parent = root)
  → generation tìm parent = api_span.span_id → KHÔNG CÓ trong span_map
  → Fallback về root → vllm_chat_completion lọt ra ngoài
```

**Vấn đề chính**: Events của cùng 1 trace bị chia thành 2 batch khác nhau, nên span_map không đầy đủ khi tạo generation.

## Fix đúng: Gom events cùng trace_id trước khi send

```python
def _process_batch(self):
    """Process a batch - group ALL events by trace_id first."""
    raw_events = self._consume_batch()
    if not raw_events:
        return

    # Parse all events
    parsed_events = []
    for raw in raw_events:
        try:
            event = json.loads(raw)
            parsed_events.append(event)
        except json.JSONDecodeError:
            logger.warning("Failed to parse event JSON")

    # Group by trace_id
    trace_groups = {}
    for event in parsed_events:
        trace_id = event.get("trace_id")
        if trace_id not in trace_groups:
            trace_groups[trace_id] = {
                "api_request": None,
                "api_spans": [],
                "generations": [],
            }
        
        event_type = event.get("event_type")
        if event_type == "api_request":
            trace_groups[trace_id]["api_request"] = event
        elif event_type == "api_span":
            trace_groups[trace_id]["api_spans"].append(event)
        elif event_type == "llm_generation":
            trace_groups[trace_id]["generations"].append(event)

    # Send each complete trace group
    for trace_id, group in trace_groups.items():
        try:
            self._send_trace_group(trace_id, group)
        except Exception as e:
            logger.error(f"Failed to send trace {trace_id}: {e}")


def _send_trace_group(self, trace_id: str, group: dict):
    """Send a complete trace group to Langfuse."""
    root = group["api_request"]
    if not root:
        logger.warning(f"Trace {trace_id} has no root event, skipping")
        return

    # 1. Create trace (name = API_REQUEST_COMPLETE để match UI mong muốn)
    trace = self.langfuse.trace(
        id=trace_id,
        name="API_REQUEST_COMPLETE",
        metadata={
            "request_id": root.get("request_id"),
            "http_method": root.get("http_method"),
            "endpoint": root.get("endpoint"),
            "status_code": root.get("status_code"),
            "service": "emotion-service",
        },
    )

    # 2. Create root span (API_REQUEST_COMPLETE)
    root_span = trace.span(
        name="API_REQUEST_COMPLETE",
        start_time=_to_datetime(root.get("start_time")),
        end_time=_to_datetime(root.get("end_time")),
        metadata={"status": root.get("status")},
    )

    # 3. Create API spans FIRST → populate span_map
    span_map = {}
    span_map[root.get("span_id")] = root_span  # root span vào map

    for api_span in group["api_spans"]:
        parent = span_map.get(api_span.get("parent_span_id"), root_span)
        span = parent.span(
            name=api_span.get("name", "api_chat_completions"),
            start_time=_to_datetime(api_span.get("start_time")),
            end_time=_to_datetime(api_span.get("end_time")),
            input=api_span.get("input_summary"),
            output=api_span.get("output_summary"),
        )
        span_map[api_span.get("span_id")] = span  # ← KEY: add vào map

    # 4. Create generations SECOND → lookup parent từ span_map
    for gen in group["generations"]:
        parent = span_map.get(gen.get("parent_span_id"), root_span)
        parent.generation(
            name=gen.get("name", "vllm_chat_completion"),
            model=gen.get("model"),
            start_time=_to_datetime(gen.get("start_time")),
            end_time=_to_datetime(gen.get("end_time")),
            input=gen.get("input_messages"),
            output=gen.get("output_content"),
            usage={
                "input": gen.get("prompt_tokens", 0),
                "output": gen.get("completion_tokens", 0),
                "total": gen.get("total_tokens", 0),
            },
            metadata={
                "original_emotion": gen.get("original_emotion"),
                "randomized_emotion": gen.get("randomized_emotion"),
                "emotion_changed": gen.get("emotion_changed"),
            },
        )

    self.langfuse.flush()
    logger.info(f"Sent trace {trace_id}: 1 root + {len(group['api_spans'])} spans + {len(group['generations'])} generations")
```

**Nhưng vẫn còn vấn đề**: Nếu events cùng 1 trace đến ở 2 batch khác nhau (batch 1 có root, batch 2 có span + generation), thì batch 2 sẽ không có root → skip.

## Fix triệt để nhất: Chờ gom đủ events trước khi send

Thêm **buffer + timeout**:

```python
def _process_batch(self):
    raw_events = self._consume_batch()
    if not raw_events:
        # Check buffer for incomplete traces that timed out
        self._flush_stale_buffer()
        return
    
    for raw in raw_events:
        event = json.loads(raw)
        trace_id = event.get("trace_id")
        
        if trace_id not in self._buffer:
            self._buffer[trace_id] = {
                "api_request": None,
                "api_spans": [],
                "generations": [],
                "first_seen": time.time(),
            }
        
        # Add to buffer
        event_type = event.get("event_type")
        if event_type == "api_request":
            self._buffer[trace_id]["api_request"] = event
        elif event_type == "api_span":
            self._buffer[trace_id]["api_spans"].append(event)
        elif event_type == "llm_generation":
            self._buffer[trace_id]["generations"].append(event)
    
    # Send complete traces (have root + at least 1 generation)
    complete = []
    for trace_id, group in self._buffer.items():
        if group["api_request"] and group["generations"]:
            complete.append(trace_id)
    
    for trace_id in complete:
        group = self._buffer.pop(trace_id)
        self._send_trace_group(trace_id, group)


def _flush_stale_buffer(self):
    """Send incomplete traces older than 10s."""
    now = time.time()
    stale = [tid for tid, g in self._buffer.items() 
             if now - g["first_seen"] > 10]
    for trace_id in stale:
        group = self._buffer.pop(trace_id)
        if group["api_request"]:
            self._send_trace_group(trace_id, group)
```

---

## Tóm lại 2 thay đổi cần làm trên server:

| # | Fix | Vị trí |
|---|-----|--------|
| 1 | Trace name: `"emotion-api-request"` → `"API_REQUEST_COMPLETE"` | `_send_trace_group` |
| 2 | Buffer events cùng trace_id, chờ đủ root + spans + generations rồi mới send | `_process_batch` + thêm `self._buffer = {}` |

Bạn muốn mình viết file hoàn chỉnh để copy lên server không?


---



## Logic đơn giản của luồng dữ liệu thực tế

```
┌─────────────────────────────────────────────────────────────────┐
│                    1 REQUEST VÀO API                            │
│              POST /v1/chat/completions                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  2 MIDDLEWARE TẠO ROOT SPAN                                    │
│  ┌─────────────────────────────────────────────┐                │
│  │ trace_id = "abc-123"                        │                │
│  │ root_span_id = "xyz-789"                    │                │
│  │ LPUSH → Redis: APIRequestEvent              │                │
│  └─────────────────────────────────────────────┘                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  3 ENDPOINT TẠO API SPAN                                       │
│  ┌─────────────────────────────────────────────┐                │
│  │ api_span_id = "def-456"                     │                │
│  │ parent_span_id = "xyz-789" (root_span_id)  │  ← CON ĐÚNG   │
│  │ LPUSH → Redis: APISpanEvent                  │                │
│  └─────────────────────────────────────────────┘                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  4 VLLM CLIENT TẠO GENERATION SPAN                             │
│  ┌─────────────────────────────────────────────┐                │
│  │ gen_span_id = "ghi-012"                     │                │
│  │ parent_span_id = "def-456" (api_span_id)   │  ← CON ĐÚNG   │
│  │ LPUSH → Redis: LLMGenerationEvent           │                │
│  └─────────────────────────────────────────────┘                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  5 REDIS QUEUE                                                 │
│                                                                 │
│   [APIRequestEvent, APISpanEvent, LLMGenerationEvent]          │
│       │              │                  │                        │
│       │              │                  │                        │
│       ▼              ▼                  ▼                        │
│   trace_id=abc   parent=        parent=                         │
│                  root_span_id   api_span_id                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  6 WORKER XỬ LÝ                                               │
│                                                                 │
│   a) trace() → tạo root "API_REQUEST_COMPLETE"                │
│   b) span(name="api_chat_completions",                         │
│          parent=root_span_id)                                  │
│   c) generation(name="vllm_chat_completion",                   │
│          parent=api_span_id)                                   │
│                                                                 │
│   KẾT QUẢ TRÊN LANGFUSE:                                       │
│                                                                 │
│   ├─ API_REQUEST_COMPLETE (root)                              │
│   │   └─ api_chat_completions                                  │
│   │       └─ vllm_chat_completion                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tóm tắt 1 câu

**Middleware tạo root → Endpoint tạo span con của root → vLLM tạo generation con của span → Worker gửi lên Langfuse theo đúng hierarchy đó.**