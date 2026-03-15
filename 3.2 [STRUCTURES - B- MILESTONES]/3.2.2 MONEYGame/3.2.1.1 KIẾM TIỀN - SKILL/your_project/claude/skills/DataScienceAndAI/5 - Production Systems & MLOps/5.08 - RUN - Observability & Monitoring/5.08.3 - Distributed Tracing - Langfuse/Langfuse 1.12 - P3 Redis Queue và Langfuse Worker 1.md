

> Deep research về nó

# PHẦN A - LLD - Langfuse Zero-Overhead Tracing - Low Level Design (LLD)

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

## 11. Revision History

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



---
# A

- [ ] **Async Redis operations** in API (non-blocking ~1ms)

- [ ] **Graceful degradation** - log warning when Redis/Langfuse down, don't crash request

  

### Event Collection - Bundle events, single LPUSH

  

- [ ] **Bundle events** at end of request (not publish individually)

- [ ] Collect all events before publishing:

  - Root span (from middleware)

  - Child spans (from endpoints)

  - LLM generations (from LLM client)

- [ ] Single Redis LPUSH for entire bundle (3 → 1)

  

### Worker Processing - Detect format, spans FIRST, generations SECOND

  

- [ ] **Detect format**: Check `bundle_type` field

- [ ] **Process spans FIRST** → add to span_map

- [ ] **Process generations SECOND** → use span_map for parent lookup

- [ ] Handle both bundle and legacy formats

  

### Langfuse Hierarchy - trace() as root, đúng parent-child

  

```

TRACE_NAME (from trace())

  └── span_1 (from endpoint)

      └── generation_1 (from LLM client)

```

  

- [ ] Use `trace()` as root (not `span()`)

- [ ] Standard trace name: `API_REQUEST_COMPLETE`

- [ ] Proper parent-child relationships

  

### Error Handling - Graceful degradation

  

- [ ] Try-catch all tracing calls

- [ ] Never let tracing errors affect API response

- [ ] Log errors with appropriate levels

  

### Performance - ~1ms overhead target

  

- [ ] **Async Redis operations** - không block event loop

- [ ] **Non-blocking LPUSH** - ~1ms overhead

- [ ] Worker chạy **independent process** - không ảnh hưởng API latency

  

---

  

# ═══════════════════════════════════════════════

# PHASE 4: THỬ NGHIỆM — Validate trước khi ship

# ═══════════════════════════════════════════════

  

> _Mỗi thử nghiệm = 1 giả thuyết + 1 test + 1 kết luận._

> _Fail nhanh, fail nhỏ, fail nhiều → tìm ra đáp án đúng._

  

## Experiment 1: Test TraceBundle với hierarchy đúng

  

| Item | Detail |

|------|--------|

| **Giả thuyết** | Nếu publish TraceBundle (3 events cùng lúc) thì hierarchy sẽ đúng |

| **Setup** | Call API endpoint, check worker logs |

| **Expected** | Worker nhận đủ 3 events, Langfuse UI hiển thị 3 levels nested |

| **Actual** | ✅ Confirmed - Worker logs: "Sent trace bundle xxx with 1 generations" |

| **Kết luận** | ✅ Confirm - TraceBundle hoạt động đúng |

  

---

  

# ═══════════════════════════════════════════════

# PHASE 5: TRIỂN KHAI — Implementation

# ═══════════════════════════════════════════════

  

## 5.1 System Diagram

  

```

┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐

│   Client    │     │     API     │     │   Redis     │     │   Worker    │     │  Langfuse   │

└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬─────┘

       │                    │                   │                    │                  │

       │ POST /v1/chat      │                   │                    │                  │

       │───────────────────>│                   │                    │                  │

       │                    │                   │                    │                  │

       │                    │ Call vLLM         │                    │                  │

       │                    │────────────────────────────────────────────────────────────>│

       │                    │<────────────────────────────────────────────────────────────│

       │                    │                   │                    │                  │

       │                    │ Build TraceBundle │                    │                  │

       │                    │ (root + span +    │                    │                  │

       │                    │  generation)      │                    │                  │

       │                    │                   │                    │                  │

       │                    │ Publish Bundle    │                    │                  │

       │                    │ (1 LPUSH)         │                    │                  │

       │                    │─────────────────>│                    │                  │

       │                    │                   │                    │                  │

       │                    │                   │ LPUSH + OK        │                  │

       │                    │<──────────────────│                    │                  │

       │                    │                   │                    │                  │

       │                    │                   │ BRPOP + bundle    │                  │

       │                    │                   │<───────────────────│                  │

       │                    │                   │                    │                  │

       │                    │                   │ Parse bundle       │                  │

       │                    │                   │ (bundle_type=     │                  │

       │                    │                   │  trace_bundle)    │                  │

       │                    │                   │                    │                  │

       │                    │                   │                    │ Send trace     │

       │                    │                   │                    │───────────────>│

       │                    │                   │                    │                  │

       │                    │                   │                    │<───────────────│

       │                    │                   │                    │                  │

       │ 200 OK            │                   │                    │                  │

       │<──────────────────│                   │                    │                  │

```

  

## 5.2 Data Models

  

### Event Types

  

| Event | Source | Parent | Fields |

|-------|--------|--------|--------|

| `APIRequestEvent` | Middleware | None (root) | trace_id, span_id, request_id, start_time, end_time, http_method, endpoint, status_code |

| `APISpanEvent` | Endpoint | root_span_id | trace_id, span_id, parent_span_id, request_id, name, endpoint |

| `LLMGenerationEvent` | LLM client | api_span_id | trace_id, span_id, parent_span_id, model, input_messages, output_content, usage |

  

### TraceBundle Format

  

```python

@dataclass

class TraceBundle:

    bundle_type: str = "trace_bundle"  # For detection

    trace_id: str

    request_id: str

    root_span: Optional[APIRequestEvent]

    child_spans: List[APISpanEvent]

    generations: List[LLMGenerationEvent]

    service_name: str

    created_at: float

```

  

### Legacy Format (for backward compatibility)

  

```python

{

    "event_type": "api_request" | "api_span" | "llm_generation",

    "trace_id": "...",

    "span_id": "...",

    ...

}

```

  

## 5.3 Worker Processing Logic

  

```python

def process_events(events: List[str]):

    bundles = []

    legacy_events = []

  

    # Step 1: Detect format

    for json_str in events:

        data = json.loads(json_str)

        if data.get("bundle_type") == "trace_bundle":

            bundles.append(TraceBundle.from_json(json_str))

        else:

            legacy_events.append(json_str)

  

    # Step 2: Process bundles

    for bundle in bundles:

        _send_bundle_to_langfuse(bundle)

  

    # Step 3: Process legacy events (group by trace_id first)

    if legacy_events:

        groups = group_by_trace_id(legacy_events)

        for group in groups:

            _send_legacy_to_langfuse(group)

  

def _send_bundle_to_langfuse(bundle: TraceBundle):

    # Create trace

    trace = langfuse.trace(name="API_REQUEST_COMPLETE")

  

    # Step 1: Create ALL spans first, store in map

    span_map = {}

    for span in bundle.child_spans:

        parent = span_map.get(span.parent_span_id, trace)

        span_obj = parent.span(name=span.name, ...)

        span_map[span.span_id] = span_obj

  

    # Step 2: Create generations (span_map now has all spans)

    for gen in bundle.generations:

        parent = span_map.get(gen.parent_span_id, trace)

        gen_obj = parent.generation(name="vllm_chat_completion", ...)

```

  

## 5.4 Redis Keys & Environment Variables

  

### Redis Keys

  

| Key | Type | Purpose |

|-----|------|---------|

| `langfuse:traces` | List (LPUSH/BRPOP) | Main trace queue |

  

### Environment Variables

  

| Variable | Required | Description |

|----------|----------|-------------|

| `TRACE_ENABLED` | No | Enable/disable tracing (default: true) |

| `REDIS_URL` | Yes | Redis connection URL |

| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |

| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |

| `LANGFUSE_BASE_URL` | Yes | Langfuse host URL |

  

---

  

# ═══════════════════════════════════════════════

# PHASE 6: KIỂM TRA — Verify fix đã work

# ═══════════════════════════════════════════════

  

> ⚠️ Chạy TOÀN BỘ checklist **trước khi** đóng ticket.

  

## 6.1 Verification Commands

  

```bash

# Check Redis Queue

redis-cli LLEN langfuse:traces

redis-cli LRANGE langfuse:traces 0 5

  

# Check Worker Logs

docker compose logs langfuse-worker

docker compose logs langfuse-worker | grep bundle

docker compose logs langfuse-worker | grep -i error

  

# Test End-to-End

curl -X POST http://localhost:8080/v1/chat/completions \

  -H "Content-Type: application/json" \

  -d '{"model": "test", "messages": [{"role": "user", "content": "test"}]}'

docker compose logs langfuse-worker | grep "Sent trace bundle"

```

  

## 6.2 Verification Checklist

  

- [ ] ✅ Symptom ban đầu đã hết (test lại reproduce steps)

- [ ] ✅ Error rate < 0.1% trong 10 phút liên tục

- [ ] ✅ Latency P99 trong ngưỡng bình thường

- [ ] ✅ Không có side effect mới

- [ ] ✅ Langfuse dashboard hierarchy đúng (3 levels)

  

## 6.3 Metrics Before vs After

  

| Metric | Before | After | Target |

|--------|--------|-------|--------|

| Redis LPUSH overhead | N/A | ~1ms | ~1ms |

| Worker latency | N/A | ~10-50ms | <100ms |

| Trace hierarchy | ❌ Sai | ✅ Đúng | 100% correct |

| Queue backlog | N/A | <100 | <1000 |

  

---

  

# ═══════════════════════════════════════════════

# PHASE 7: ĐÚC KẾT — Kaizen & Knowledge Capture

# ═══════════════════════════════════════════════

  

> _"Không đo lường — Không cải tiến."_

> _Viết phần này SAU KHI resolve. Đúc kết từ Phase 1-6 thành knowledge tái sử dụng._

  

---

  

## 7.1 Common Mistakes — Các lỗi đã mắc

  

### M-01: Race Condition — Worker consume trước khi đủ events

  

**Severity:** 🔴

  

❌ **Sai:**

```python

# Publish từng event riêng lẻ

await trace_publisher.publish(root_event)   # LPUSH 1

await trace_publisher.publish(span_event)   # LPUSH 2

await trace_publisher.publish(gen_event)    # LPUSH 3

# Worker BRPOP có thể nhận trước khi tất cả được push!

```

  

> **Tại sao sai:** Worker BRPOP trước khi tất cả events được LPUSH → thiếu event → hierarchy sai

  

✅ **Đúng:**

```python

# Gom tất cả vào TraceBundle, publish 1 lần

bundle = TraceBundle(

    root_span=root_event,

    child_spans=[span_event],

    generations=[gen_event]

)

await trace_publisher.publish_trace_bundle(bundle)  # 1 LPUSH duy nhất

```

  

> **Tại sao đúng:** Worker nhận 1 message = đầy đủ 3 events → không có race condition

  

🔍 **Detect trong codebase:**

```bash

grep -rn "publish.*event" src/infrastructure/observability/

```

  

---

  

### M-02: Event Ordering — Process generations trước spans

  

**Severity:** 🟠

  

❌ **Sai:**

```python

# Process generations TRƯỚC

for gen in bundle.generations:

    parent = span_map.get(gen.parent_span_id, root_span)  # span_map chưa có!

    gen_span = parent.generation(...)

```

  

✅ **Đúng:**

```python

# Process spans FIRST

for span in bundle.child_spans:

    parent = span_map.get(span.parent_span_id, trace)

    span_obj = parent.span(...)

    span_map[span.span_id] = span_obj

  

# Process generations SECOND

for gen in bundle.generations:

    parent = span_map.get(gen.parent_span_id, trace)  # span_map đã có!

    gen_span = parent.generation(...)

```

  

---

  

### M-03: Duplicate Root Span

  

**Severity:** 🟠

  

❌ **Sai:**

```python

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

root_span = langfuse_trace.span(name="API_REQUEST_COMPLETE")  # DUPLICATE!

```

  

✅ **Đúng:**

```python

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

span_map[root.span_id] = langfuse_trace  # Dùng trace làm parent

```

  

---

  

## 7.2 Best Practices Checklist — Rút ra từ vấn đề này

  

### Architecture

  

- [ ] ✅ Independent worker process cho Langfuse publishing

- [ ] ✅ Redis queue as message buffer

- [ ] ✅ Async I/O cho non-blocking operations

  

### Event Collection

  

- [ ] ✅ Bundle all events vào 1 message trước khi publish

- [ ] ✅ Single LPUSH thay vì nhiều LPUSH

  

### Worker Processing

  

- [ ] ✅ Detect bundle_type field

- [ ] ✅ Process spans FIRST, generations SECOND

- [ ] ✅ Handle both bundle và legacy formats

  

### Performance

  

- [ ] ✅ Target ~1ms overhead cho tracing

- [ ] ✅ Worker separate process - không ảnh hưởng API latency

  

## 7.3 Action Items — Ngăn tái phát

  

| # | Action | Priority | Owner | Due | Status | Ticket |

|---|--------|----------|-------|-----|--------|--------|

| 1 | Thêm alert cho queue length > 1000 | P1 | @cuongdn | 2026-03-15 | ⏳ | - |

| 2 | Viết integration test cho TraceBundle | P2 | @cuongdn | 2026-03-20 | ⏳ | - |

  

## 7.4 Lessons Learned

  

**Làm tốt ✅:**

- TraceBundle approach giải quyết triệt để race condition

- Async LPUSH đạt target ~1ms overhead

- Worker process tách biệt hoàn toàn không ảnh hưởng API

  

**Cần cải thiện ⚠️:**

- Cần thêm monitoring/alerting cho queue health

- Test coverage cho tracing path còn thiếu

  

**Câu hỏi mở ❓:**

- Có nên batch nhiều bundles lại không?

  

---

  

## 7.5 Quick Reference Card

  

```

╔══════════════════════════════════════════════════════════╗

║  LANGFUSE WORKER — Quick Ref from PROB-2026-03-10   ║

╠══════════════════════════════════════════════════════════╣

║  🔴 M-01: Race Condition → Bundle all events in 1 msg  ║

║  🟠 M-02: Event Ordering → Spans FIRST, Generations 2nd║

║  🟠 M-03: Duplicate Root → Use trace() as root         ║

╠══════════════════════════════════════════════════════════╣

║  ✅ BP-01: Async LPUSH → ~1ms overhead                 ║

║  ✅ BP-02: Worker process → Zero API impact            ║

║  ✅ BP-03: Bundle format → No race condition            ║

╠══════════════════════════════════════════════════════════╣

║  Debug: redis-cli LLEN langfuse:traces                  ║

║  Worker: docker compose logs langfuse-worker           ║

╚══════════════════════════════════════════════════════════╝

```

  

---

  

# APPENDIX

  

## A. @observe vs Manual SDK - Why not use @observe

  

**Q: Tại sao không dùng Langfuse `@observe` decorator thay vì tự build Redis queue + worker?**

  

**A:** `@observe` decorator không phù hợp với mục tiêu **zero-overhead** của architecture này.

  

| Aspect | @observe Decorator | Current Architecture (Redis + Worker) |

|--------|-------------------|--------------------------------------|

| **Latency impact** | ~5-50ms per call (sync) | ~1ms (async LPUSH, non-blocking) |

| **Execution** | Synchronous SDK call trong request path | Async push to Redis, worker xử lý riêng |

| **GIL contention** | Block event loop, contention với request | Worker có GIL riêng, không ảnh hưởng API |

| **Implementation** | Dễ (~1 dòng code) | Cần Redis + Worker + queue logic |

| **Flexibility** | Bị coupling với Langfuse SDK | Full control over data flow |

  

---

  

## B. Performance Considerations

  

| Metric | Target | Notes |

|--------|--------|-------|

| Redis LPUSH overhead | ~1ms | Async, non-blocking |

| Worker latency | ~10-50ms | Per trace to Langfuse |

| Queue backlog | <1000 | Monitor with LLEN |

| Memory per event | ~1KB | JSON serialized |

  

### Optimization Tips

  

1. **Batch processing**: Worker processes up to 50 events per batch

2. **Async I/O**: Use `asyncio` for Redis operations in API

3. **Connection pooling**: Reuse Redis connections

4. **No GIL contention**: Worker runs in separate process

  

---

  

## C. References

  

- [LLD_Langfuse_Zero_Overhead_Tracing.md](../2-explanation_ADR_HighLevelDesign/batch1/LLD_Langfuse_Zero_Overhead_Tracing.md)

- [Langfuse_Worker_Guide.md](../Langfuse_Worker_Guide.md)

- [CHANGELOG.md](../CHANGELOG.md)

  

---

  

# REPORT FORMAT

  

```

1. VẤN ĐỀ:    Zero-overhead Langfuse tracing với Redis Worker

   IMPACT:     Latency tăng ~5-50ms/call khi tích hợp trực tiếp

   METRICS:    Redis LPUSH ~1ms, Worker latency ~10-50ms

  

2. NGUYÊN NHÂN: Race condition khi worker consume trước khi đủ events

   DẪN CHỨNG:   Hierarchy sai - generation cùng cấp với span

  

3. GIẢI PHÁP:  TraceBundle - gom 3 events thành 1 message

   DẪN CHỨNG:   Worker logs: "Sent trace bundle with 1 generations"

  

4. PREVENT:    Thêm alert queue length, viết integration test

```

  

---

  

*Created by `@cuongdn` on `2026-03-10` · Last updated: `2026-03-10`*

*Naming: `PROB-2026-03-10-langfuse-worker.md`*


---

# PHẦN C - CHỈ RA MECE CÁC NHƯỢC ĐIỂM CỦA CÁCH TRIỂN KHAI NÀY VÀ ĐỀ XUẤT MECE CÁC GIẢI PHÁP => sAU ĐÓ ĐỀ XUẤT BEST PRACTICES cho việc triển khai langfuse overhead 0 ms

## MECE Analysis: Nhược điểm & Giải pháp

---

### Chiều 1: Data Durability (Mất data khi nào?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|1.1|**BRPOP = fire-and-forget** — Worker pop event ra, crash trước khi gửi Langfuse → mất event vĩnh viễn|🔴|Worker OOM, segfault, kill -9|
|1.2|**Redis restart không persistence** — Nếu Redis chưa config RDB/AOF, restart = mất toàn bộ queue|🔴|Redis container restart|
|1.3|**No Dead Letter Queue** — Event parse lỗi hoặc Langfuse reject → event bị drop, không retry|🟠|Malformed JSON, Langfuse schema change|
|1.4|**No retry mechanism** — Langfuse trả 5xx → event mất, không có cơ chế retry|🟠|Langfuse downtime|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|Recommendation|
|---|---|---|---|
|**S1.1: Redis STREAM (XADD/XREADGROUP/XACK)**|1.1 hoàn toàn — message chỉ bị xóa sau XACK, crash → auto re-deliver|Trung bình|⭐ Best practice|
|S1.2: Redis persistence (RDB + AOF)|1.2|Thấp (config only)|Phải làm ngay|
|S1.3: DLQ key `langfuse:traces:dlq`|1.3, 1.4|Thấp|Nên làm|
|S1.4: Retry với exponential backoff|1.4|Trung bình|Nên làm nếu giữ LIST|

---

### Chiều 2: Trace Completeness (Hierarchy có đúng không?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|2.1|**Legacy mode vẫn bị race condition** — Publish 3 events riêng lẻ, worker có thể nhận không đủ trong 1 batch|🔴|Khi KHÔNG dùng TraceBundle (backward compat path)|
|2.2|**Bundle chưa được dùng ở tất cả paths** — Error path, timeout path có thể vẫn publish từng event|🟠|Request timeout, exception trước khi gom bundle|
|2.3|**Không có validation** — Worker không check xem bundle có đủ root + span + generation không|🟡|Partial bundle do bug ở API side|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|**S2.1: Loại bỏ legacy path** hoàn toàn, chỉ chấp nhận bundle|2.1|Thấp — nhưng cần đảm bảo tất cả publishers đã migrate|
|**S2.2: Middleware gom bundle ở finally block** — dù success hay error đều publish|2.2|Thấp|
|S2.3: Worker validate bundle schema trước khi send|2.3|Thấp|

---

### Chiều 3: Observability of the Observability (Ai monitor worker?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|3.1|**Không có alert khi queue backlog tăng** — Queue có thể phình 100k events mà không ai biết|🔴|Worker chậm/crash, traffic spike|
|3.2|**Không có metrics export** — Không biết worker throughput, error rate, latency|🟠|Production monitoring|
|3.3|**Không có health check** cho worker — K8s không biết worker dead|🟠|Worker hang (không crash nhưng không process)|
|3.4|**Worker log chỉ có INFO** — Không log chi tiết trace_id nào thành công/thất bại|🟡|Debug production issues|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S3.1: Cron job `redis-cli LLEN` + alert khi > threshold|3.1|Thấp|
|S3.2: Worker expose `/metrics` (Prometheus format)|3.2|Trung bình|
|S3.3: Worker expose `/health` + K8s liveness probe|3.3|Thấp|
|S3.4: Structured logging với trace_id, event_count, duration|3.4|Thấp|

---

### Chiều 4: Scalability (Scale thế nào?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|4.1|**Single worker** — 1 worker bottleneck khi traffic cao|🟠|>500 req/s sustained|
|4.2|**Redis LIST không hỗ trợ multi-consumer** — BRPOP chỉ 1 consumer nhận 1 message|🟠|Muốn scale workers|
|4.3|**Không có backpressure** — API cứ LPUSH, không biết queue đầy → Redis OOM|🟡|Sustained high traffic + worker down|
|4.4|**Sync worker loop** — Blocking BRPOP + sync Langfuse SDK = throughput thấp|🟡|High volume tracing|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|**S4.1: Redis STREAM + Consumer Group**|4.1 + 4.2 cùng lúc — N workers chia tải tự động|Trung bình|
|S4.2: MAXLEN trên Redis LIST/STREAM|4.3 — drop oldest khi quá capacity|Thấp|
|S4.3: Async worker (asyncio + httpx)|4.4 — concurrent Langfuse calls|Trung bình|
|S4.4: Publisher check LLEN trước LPUSH, skip nếu > threshold|4.3|Thấp|

---

### Chiều 5: Operational Complexity (Vận hành khó ở đâu?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|5.1|**Thêm 2 components** (Redis + Worker) — tăng operational surface|🟠|Mọi lúc|
|5.2|**Worker và API dùng chung Dockerfile** nhưng khác entrypoint — confusion khi debug|🟡|New team member onboard|
|5.3|**Không có drain mode** — Deploy worker mới = có thể mất events đang process|🟡|Rolling deployment|
|5.4|**Config scattered** — Redis URL ở cả API và Worker, dễ mismatch|🟡|Config change|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S5.1: Acceptance — đây là trade-off cần thiết cho zero-overhead|5.1|—|
|S5.2: Tách Dockerfile riêng cho worker, hoặc document rõ|5.2|Thấp|
|S5.3: SIGTERM handler → stop consuming, flush buffer, exit|5.3|Thấp|
|S5.4: Shared `.env` file, validate on startup|5.4|Thấp|

---

### Chiều 6: Data Accuracy (Data có đúng không?)

|#|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|6.1|**Timestamp drift** — API tạo timestamp, worker gửi muộn → Langfuse duration có thể sai|🟡|Clock skew giữa containers|
|6.2|**Duplicate traces** — Worker crash sau khi gửi Langfuse nhưng trước khi XACK (nếu dùng STREAM)|🟡|Worker crash|
|6.3|**No sampling** — 100% traces → Langfuse cost cao khi traffic lớn|🟡|High traffic production|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S6.1: Dùng `time.time()` ở API, worker chỉ forward — OK vì cùng host|6.1|Không cần fix|
|S6.2: Langfuse dedupe by trace_id — đã xử lý server-side|6.2|Không cần fix|
|S6.3: Thêm `sample_rate` ở publisher — chỉ publish N% traces|6.3|Thấp|

---

## Best Practices: Langfuse Zero-Overhead Implementation

Dựa trên toàn bộ phân tích 6 chiều, đây là **tiered recommendation**:

### Tier 1 — Phải làm (High impact, Low effort)

|#|Practice|Giải quyết chiều nào|Implementation|
|---|---|---|---|
|**BP-1**|**Loại bỏ legacy path, chỉ dùng TraceBundle**|Chiều 2 (completeness)|Xóa code path publish từng event. Middleware gom bundle ở `finally` block — dù success hay error|
|**BP-2**|**Redis persistence (appendonly yes)**|Chiều 1 (durability)|1 dòng config: `redis-server --appendonly yes`|
|**BP-3**|**SIGTERM graceful shutdown**|Chiều 5 (ops)|`signal.signal(SIGTERM, handler)` → stop consume → flush → exit|
|**BP-4**|**Queue length alert**|Chiều 3 (monitoring)|Cron `redis-cli LLEN langfuse:traces`, alert nếu > 1000|
|**BP-5**|**MAXLEN cap trên queue**|Chiều 4 (backpressure)|`LPUSH` + `LTRIM 0 99999` hoặc STREAM `MAXLEN ~ 100000`|

### Tier 2 — Nên làm (Medium impact)

|#|Practice|Giải quyết chiều nào|Implementation|
|---|---|---|---|
|**BP-6**|**Dead Letter Queue**|Chiều 1 (durability)|Parse fail / Langfuse fail N lần → `LPUSH langfuse:traces:dlq`|
|**BP-7**|**Retry với backoff**|Chiều 1 (durability)|Langfuse 5xx → retry 3 lần (1s, 2s, 4s) → DLQ|
|**BP-8**|**Circuit breaker**|Chiều 1 + 4|Langfuse 5xx liên tục 10 lần → pause 30s → retry|
|**BP-9**|**Worker structured logging**|Chiều 3 (monitoring)|Log JSON: `{"trace_id": "...", "events": 3, "duration_ms": 45, "status": "sent"}`|
|**BP-10**|**Sample rate**|Chiều 6 (accuracy/cost)|`TRACE_SAMPLE_RATE=0.5` → chỉ trace 50% requests|

### Tier 3 — Tốt nhưng chưa cần ngay (Scale future)

|#|Practice|Khi nào cần|Implementation|
|---|---|---|---|
|**BP-11**|**Redis STREAM thay LIST**|Khi cần multi-worker hoặc at-least-once|Migrate LPUSH/BRPOP → XADD/XREADGROUP/XACK|
|**BP-12**|**Multi-worker consumer group**|>500 req/s sustained|STREAM consumer group, N worker containers|
|**BP-13**|**Async worker (asyncio)**|Worker throughput bottleneck|Async Langfuse HTTP calls, concurrent processing|
|**BP-14**|**Worker health check endpoint**|K8s deployment|Expose `/health`, liveness/readiness probes|

---

## Tóm lại: Current State vs Target State

```
CURRENT STATE (Image 1 - đang bị sai):

emotion-api-request          ← Sai tên
  └── API_REQUEST_COMPLETE   ← Duplicate root
      └── api_chat_completions
  └── vllm_chat_completion   ← Lọt ra ngoài!

TARGET STATE (Image 2 - muốn đạt):

API_REQUEST_COMPLETE
  └── API_REQUEST_COMPLETE
      └── api_chat_completions
          └── vllm_chat_completion

IDEAL STATE (sau khi apply best practices):

API_REQUEST_COMPLETE              ← trace() tạo, KHÔNG duplicate
  └── api_chat_completions        ← span, parent = trace
      └── vllm_chat_completion    ← generation, parent = span
```

**3 fixes cần làm ngay** để đạt target state:

1. Trace name: `"emotion-api-request"` → `"API_REQUEST_COMPLETE"`
2. Không tạo thêm `span("API_REQUEST_COMPLETE")` — dùng `trace()` làm parent trực tiếp
3. Spans FIRST, generations SECOND — đảm bảo span_map đầy đủ

**5 best practices nên làm tiếp** (Tier 1): Bỏ legacy path, Redis persistence, graceful shutdown, queue alert, MAXLEN cap.



---

# PHẦN D - ê, có cách nào khác ko, ví dụ như @observe nhưng được langfuse hỗ trợ trực tiếp cho việc triển riêng 1 luồng như này ý bro ????




---

Câu hỏi cực hay — để mình research xem Langfuse có hỗ trợ native cho pattern này không.Okay, research xong rồi. Có **3 cách native/semi-native** mà Langfuse hỗ trợ, không cần tự build Redis + Worker từ đầu. Mình so sánh thẳng:

---

## MECE: Tất cả các cách đạt zero-overhead với Langfuse

### Option A: Tự build Redis + Worker (cách của bạn hiện tại)

```
App → LPUSH Redis → Worker process → Langfuse API
```

Ưu: Full control. Nhược: Tự build + maintain tất cả.

---

### Option B: `@observe` + OTel Collector sidecar (container riêng)

**Đây là cách Langfuse THỰC SỰ hỗ trợ native.** Và đây chính là thứ bạn đang hỏi.

```
App (@observe / Langfuse SDK)
  → BatchSpanProcessor → OTLP HTTP export → localhost:4318
                                                    ↓
                                            ┌──────────────┐
                                            │  OTel        │
                                            │  Collector   │  ← Container riêng
                                            │  (sidecar)   │
                                            └──────┬───────┘
                                                   ↓
                                            Langfuse OTLP endpoint
                                            /api/public/otel/v1/traces
```

Langfuse có **OTLP endpoint chính thức**: Langfuse có thể nhận traces trên endpoint `/api/public/otel`, hỗ trợ OTLP over HTTP với cả HTTP/JSON và HTTP/protobuf.

Code app side cực đơn giản:

```python
from langfuse import observe, get_client

@observe()
def my_endpoint(query: str):
    result = call_llm(query)
    return result
```

docker-compose thêm 1 container OTel Collector:

```yaml
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel-config.yaml:/etc/otelcol-contrib/config.yaml
    ports:
      - "4318:4318"

  your-api:
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
      - LANGFUSE_PUBLIC_KEY=pk-lf-xxx
      - LANGFUSE_SECRET_KEY=sk-lf-xxx
```

OTel Collector config (`otel-config.yaml`):

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 512

exporters:
  otlphttp/langfuse:
    endpoint: "https://cloud.langfuse.com/api/public/otel"
    headers:
      Authorization: "Basic <base64(pk:sk)>"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/langfuse]
```

**NHƯNG — vẫn KHÔNG giải quyết GIL contention:**

Vấn đề: Langfuse SDK v3 là "a thin layer on top of the official OpenTelemetry client" — nó đăng ký `LangfuseSpanProcessor` lên global TracerProvider. Nghĩa là `BatchSpanProcessor` vẫn chạy **trong app process**, serialize vẫn giữ GIL, chỉ là HTTP POST đi sang collector thay vì đi thẳng Langfuse. Bước serialize (CPU-bound, giữ GIL) vẫn xảy ra trong app.

---

### Option C: Langfuse Async API trực tiếp (không dùng SDK trong app)

```
App → json.dumps() → HTTP POST async → Langfuse /api/public/ingestion
```

Langfuse v3 dùng kiến trúc event-driven: nhận HTTP requests từ SDK, queue HTTP bodies trong backend, và xử lý bất đồng bộ. Endpoint `/api/public/ingestion` giờ là async — nó accept events và trả 207 ngay lập tức.

Nghĩa là bạn có thể **bỏ Langfuse SDK khỏi app**, tự build HTTP POST async (dùng `httpx` hoặc `aiohttp`) gửi thẳng lên Langfuse API. Langfuse server tự queue + process.

Nhưng bạn phải tự format đúng Langfuse ingestion API schema — mất hết tiện ích của SDK (`@observe`, auto context propagation, v.v.).

---

### Option D: `@observe` + `SimpleSpanProcessor` thay `BatchSpanProcessor`

Thay vì batch (gom rồi flush — gây GIL spike), dùng `SimpleSpanProcessor` gửi **từng span ngay lập tức**. Overhead đều hơn (không có spike) nhưng tổng overhead cao hơn.

Langfuse SDK không trực tiếp hỗ trợ swap processor, nhưng vì nó dựa trên OTel, bạn có thể override:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from langfuse.opentelemetry import LangfuseExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(LangfuseExporter()))
```

**Vấn đề:** Mỗi span = 1 HTTP call đồng bộ → latency tăng 5-20ms mỗi span. Tệ hơn batch cho hầu hết use cases.

---

## So sánh thẳng 4 options

||**A: Redis + Worker** (của bạn)|**B: @observe + OTel Collector**|**C: Async HTTP API**|**D: SimpleSpanProcessor**|
|---|---|---|---|---|
|**GIL contention**|✅ Zero — SDK không ở app|❌ **Vẫn có** — serialize trong app|✅ Zero — không import SDK|❌ Vẫn có|
|**Overhead per request**|~1ms (LPUSH)|~5-15ms (serialize + network to collector)|~2-5ms (json + async HTTP)|~5-20ms per span × N spans|
|**DX cho coder**|❌ Phải tự quản lý parent_span_id|✅ `@observe` tự propagate|❌ Tự build mọi thứ|✅ `@observe` hoạt động|
|**Nested spans**|❌ Phải dùng TraceContext helper|✅ OTel context propagation tự động|❌ Tự build|✅ Tự động|
|**Infrastructure**|Redis + Worker container|OTel Collector container|Không thêm gì|Không thêm gì|
|**Khi Langfuse down**|Events nằm trong Redis|Events trong collector buffer (limited)|Mất nếu không buffer|Mất|
|**Complexity**|Cao|Trung bình|Cao|Thấp|

---

## Phát hiện quan trọng: Option B KHÔNG giải quyết được GIL

Nhiều người nghĩ OTel Collector sidecar giải quyết GIL — **SAI**. Tài liệu nghiên cứu ban đầu của bạn đã chỉ đúng:

```
App process:
  span.end() → BatchSpanProcessor.on_end()
    → acquire lock → queue.put(span)        ← GIL contention ở đây
    → background thread: serialize → export  ← GIL contention ở đây

OTel Collector chỉ thay đổi:
  export destination: Langfuse → localhost collector
  
KHÔNG thay đổi:
  serialize vẫn trong app process
  lock contention vẫn trong app process
  GIL vẫn bị giữ khi serialize
```

---

## Vậy best practice thực sự là gì?

Tuỳ vào **mức độ nhạy cảm với latency**:

### Nếu P99 latency < 100ms là bắt buộc (production AI, real-time):

→ **Option A (Redis + Worker)** là cách duy nhất triệt để.

Nhưng nên kết hợp **TraceContext helper** (như mình đã đề xuất ở message trước) để coder dùng dễ như `@observe`:

```python
# Gần như dễ dùng như @observe, nhưng zero GIL:
ctx = TraceContext(request)
with ctx.span("orchestrator"):
    with ctx.span("tool_search"):
        ctx.generation("embedding", model="text-embedding-3", ...)
```

### Nếu chấp nhận ~5-15ms overhead (đa số web app, không real-time):

→ **Option B (@observe + OTel Collector)** — đơn giản nhất, Langfuse hỗ trợ native, DX tốt nhất.

GIL spike ~1s sẽ **giảm đáng kể** (vì HTTP export đi localhost thay vì Langfuse cloud), nhưng không triệt để zero.

### Nếu prototype / dev environment:

→ **Dùng @observe thẳng**, không cần collector, không cần Redis. Chấp nhận overhead.

---

## Tóm lại 1 câu

**Langfuse KHÔNG có cơ chế native nào để tách GIL ra khỏi app process.** SDK v3 dựa trên OTel, và OTel Python SDK luôn serialize trong app process. OTel Collector sidecar chỉ offload phần HTTP, không offload phần serialize.

Nếu cần **thật sự zero-overhead**, cách của bạn (Redis + Worker, không import Langfuse SDK trong app) là **đúng và là cách duy nhất**. Cái cần cải thiện không phải kiến trúc mà là **DX** — thêm TraceContext helper để coder không phải quản lý parent_span_id thủ công.


---

# PHẦN E: Để overhead ~0, đâu là best practices.  Với mục tiêu là trace được toàn bộ request chứ ko phải ramdom chỉ 0.3 mới được trace



# PHẦN B -🔧 PROB-2026-03-10-langfuse-worker-integration

  

> Zero-overhead Langfuse tracing với Redis Worker — từ race condition → stable implementation

  

| Field | Value |

|-------|-------|

| **ID** | PROB-2026-03-10-langfuse-worker |

| **Type** | 🐛 Bug / ⚡ Perf |

| **Severity** | 🟠 SEV-2 |

| **Status** | ✅ Resolved |

| **Owner** | @cuongdn |

| **Started** | 2026-03-08 |

| **Resolved** | 2026-03-10 |

| **Duration** | 3 days |

| **Related** | [LLD_Langfuse_Zero_Overhead_Tracing.md](../2-explanation_ADR_HighLevelDesign/batch1/LLD_Langfuse_Zero_Overhead_Tracing.md) |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 1: VẤN ĐỀ — Chuyện gì đang xảy ra?

## ═══════════════════════════════════════════════

  

> _"Định nghĩa đúng vấn đề = giải quyết 50% vấn đề."_

> _Giải quyết triệu chứng ≠ Giải quyết nguyên nhân._

  

### 1.1 Background - Tại sao cần Langfuse + Redis Worker

  

Langfuse SDK v3 khi tích hợp trực tiếp vào FastAPI service gây ra **overhead ~1s** do GIL (Global Interpreter Lock) contention khi background flush thread chạy trùng với request đang xử lý.

  

**Mục tiêu:** Zero-overhead tracing cho production AI service với high-throughput requirements.

  

### 1.2 Root Cause - Vấn đề khi tích hợp trực tiếp

  

| Issue | Impact |

|-------|--------|

| Langfuse SDK dùng OpenTelemetry `BatchSpanProcessor` | Background thread serialize + HTTP POST giữ GIL |

| Flush trùng với request | Event loop bị block |

| Latency tăng | ~5-50ms per call |

  

### 1.3 Solution - Architecture overview

  

Tách biệt Langfuse publishing thành **independent worker process**, giao tiếp qua Redis queue.

  

**Best Practices Implemented:**

  

| Practice | Description | Status |

|----------|-------------|--------|

| **Trace Bundle** | Gom tất cả events vào 1 bundle, publish 1 lần thay vì 3 LPUSH | ✅ Implemented |

| **Langfuse SDK Native** | Worker gửi từng observation riêng lẻ, Langfuse tự reconstruct hierarchy | ✅ Implemented |

| **Backward Compatibility** | Worker hỗ trợ cả bundle format (mới) và legacy events | ✅ Implemented |

| **Graceful Degradation** | Redis/Langfuse down → log warning, không crash request | ✅ Implemented |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 2: NGUYÊN NHÂN — Tại sao xảy ra?

## ═══════════════════════════════════════════════

  

> _"Nghi ngờ suy nghĩ của chính mình. Trong mọi cuộc tìm giải pháp,_

> _đầu tiên hãy luôn nghĩ giải pháp của mình SAI."_

> _— First Principles: Bóc tách từng lớp, không chấp nhận bề mặt._

  

### 2.1 Race Condition - Worker consume trước khi đủ events

  

| ## | Issue | Symptom | Root Cause | Fix |

|---|-------|---------|------------|-----|

| 1 | **Worker nhận không đủ events** | Hierarchy sai: `vllm_chat_completion` cùng cấp với `api_chat_completions` | Worker BRPOP trước khi tất cả events được LPUSH | Gom tất cả events vào **TraceBundle**, publish 1 lần cuối request |

  

### 2.2 Event Ordering - Process generations trước spans

  

| ## | Issue | Symptom | Root Cause | Fix |

|---|-------|---------|------------|-----|

| 2 | **Event ordering** | Generation không có parent span | Worker process generations TRƯỚC khi process spans | **Process spans FIRST, then generations SECOND** |

  

```python

## SAI (trước fix):

for gen in group.llm_generation_events:

    parent = span_map.get(gen.parent_span_id, root_span)  ## span_map chưa có!

    gen_span = parent.generation(...)

  

## ĐÚNG (sau fix):

## FIRST: Create ALL API spans and add to span_map

for api_span in group.api_span_events:

    parent = span_map.get(api_span.parent_span_id, root_span)

    span = parent.span(...)

    span_map[api_span.span_id] = span

  

## SECOND: Create LLM generations (sau khi span_map đã có đầy đủ spans)

for gen in group.llm_generation_events:

    parent = span_map.get(gen.parent_span_id, root_span)

    gen_span = parent.generation(...)

```

  

### 2.3 Duplicate Root Span - Tạo 2 root nodes

  

| ## | Issue | Symptom | Root Cause | Fix |

|---|-------|---------|------------|-----|

| 3 | **Duplicate nodes trong Langfuse UI** | 2 nodes cùng tên "API_REQUEST_COMPLETE" | Cả `trace()` và `span()` đều tạo root span | Không tạo root span riêng, dùng trace làm parent trực tiếp |

  

```python

## SAI (trước fix):

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

root_span = langfuse_trace.span(name="API_REQUEST_COMPLETE")  ## DUPLICATE!

## → Tạo 2 nodes trong UI

  

## ĐÚNG (sau fix):

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

span_map[root.span_id] = langfuse_trace  ## Dùng trace làm parent

## → api_chat_completions sẽ nested dưới trace's root span

```

  

### 2.4 Trace Name - Sai tên hiển thị

  

| ## | Issue | Symptom | Root Cause | Fix |

|---|-------|---------|------------|-----|

| 4 | **Trace name sai trong UI** | Hiển thị "emotion-api-request" thay vì "API_REQUEST_COMPLETE" | Hardcoded wrong name | Đổi trace name thành "API_REQUEST_COMPLETE" |

  

### 2.5 Legacy vs Bundle Format - Worker không handle cả 2

  

| ## | Issue | Symptom | Root Cause | Fix |

|---|-------|---------|------------|-----|

| 5 | **Worker không xử lý bundle** | Traces không hiển thị trong Langfuse | Worker chỉ xử lý 1 format | Thêm logic detect `bundle_type` - hỗ trợ cả 2 formats |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 3: GIẢI PHÁP — Các hướng xử lý

## ═══════════════════════════════════════════════

  

> _"Không chỉ fix — mà phải tạo đòn bẩy mới từ chính vấn đề."_

> _Liệt kê TẤT CẢ options → Đánh giá → Chọn → Giải thích tại sao loại các cái khác._

  

### 3.1 Solution Options

  

| ## | Option | Mô tả | Effort | Risk | Trade-off |

|---|--------|-------|--------|------|-----------|

| A | Direct Langfuse SDK | Gọi Langfuse SDK trực tiếp trong request | 🟢 | 🔴 | Overhead ~1s, GIL contention |

| B | **Redis + Worker** | Tách worker process, giao tiếp qua Redis queue | 🟡 | 🟢 | Zero-overhead, phải deploy thêm worker |

  

> **Chọn: Option B** - Zero-overhead target

  

### 3.2 Best Practices Checklist

  

#### Architecture - Worker process, Redis queue, async I/O

  

- [ ] **Independent worker process** - separate from API service

- [ ] **Redis queue** as message buffer between API and worker

- [ ] **Async Redis operations** in API (non-blocking ~1ms)

- [ ] **Graceful degradation** - log warning when Redis/Langfuse down, don't crash request

  

#### Event Collection - Bundle events, single LPUSH

  

- [ ] **Bundle events** at end of request (not publish individually)

- [ ] Collect all events before publishing:

  - Root span (from middleware)

  - Child spans (from endpoints)

  - LLM generations (from LLM client)

- [ ] Single Redis LPUSH for entire bundle (3 → 1)

  

#### Worker Processing - Detect format, spans FIRST, generations SECOND

  

- [ ] **Detect format**: Check `bundle_type` field

- [ ] **Process spans FIRST** → add to span_map

- [ ] **Process generations SECOND** → use span_map for parent lookup

- [ ] Handle both bundle and legacy formats

  

#### Langfuse Hierarchy - trace() as root, đúng parent-child

  

```

TRACE_NAME (from trace())

  └── span_1 (from endpoint)

      └── generation_1 (from LLM client)

```

  

- [ ] Use `trace()` as root (not `span()`)

- [ ] Standard trace name: `API_REQUEST_COMPLETE`

- [ ] Proper parent-child relationships

  

#### Error Handling - Graceful degradation

  

- [ ] Try-catch all tracing calls

- [ ] Never let tracing errors affect API response

- [ ] Log errors with appropriate levels

  

#### Performance - ~1ms overhead target

  

- [ ] **Async Redis operations** - không block event loop

- [ ] **Non-blocking LPUSH** - ~1ms overhead

- [ ] Worker chạy **independent process** - không ảnh hưởng API latency

  

---

  

## ═══════════════════════════════════════════════

## PHASE 4: THỬ NGHIỆM — Validate trước khi ship

## ═══════════════════════════════════════════════

  

> _Mỗi thử nghiệm = 1 giả thuyết + 1 test + 1 kết luận._

> _Fail nhanh, fail nhỏ, fail nhiều → tìm ra đáp án đúng._

  

### Experiment 1: Test TraceBundle với hierarchy đúng

  

| Item | Detail |

|------|--------|

| **Giả thuyết** | Nếu publish TraceBundle (3 events cùng lúc) thì hierarchy sẽ đúng |

| **Setup** | Call API endpoint, check worker logs |

| **Expected** | Worker nhận đủ 3 events, Langfuse UI hiển thị 3 levels nested |

| **Actual** | ✅ Confirmed - Worker logs: "Sent trace bundle xxx with 1 generations" |

| **Kết luận** | ✅ Confirm - TraceBundle hoạt động đúng |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 5: TRIỂN KHAI — Implementation

## ═══════════════════════════════════════════════

  

### 5.1 System Diagram

  

```

┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐

│   Client    │     │     API     │     │   Redis     │     │   Worker    │     │  Langfuse   │

└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬─────┘

       │                    │                   │                    │                  │

       │ POST /v1/chat      │                   │                    │                  │

       │───────────────────>│                   │                    │                  │

       │                    │                   │                    │                  │

       │                    │ Call vLLM         │                    │                  │

       │                    │────────────────────────────────────────────────────────────>│

       │                    │<────────────────────────────────────────────────────────────│

       │                    │                   │                    │                  │

       │                    │ Build TraceBundle │                    │                  │

       │                    │ (root + span +    │                    │                  │

       │                    │  generation)      │                    │                  │

       │                    │                   │                    │                  │

       │                    │ Publish Bundle    │                    │                  │

       │                    │ (1 LPUSH)         │                    │                  │

       │                    │─────────────────>│                    │                  │

       │                    │                   │                    │                  │

       │                    │                   │ LPUSH + OK        │                  │

       │                    │<──────────────────│                    │                  │

       │                    │                   │                    │                  │

       │                    │                   │ BRPOP + bundle    │                  │

       │                    │                   │<───────────────────│                  │

       │                    │                   │                    │                  │

       │                    │                   │ Parse bundle       │                  │

       │                    │                   │ (bundle_type=     │                  │

       │                    │                   │  trace_bundle)    │                  │

       │                    │                   │                    │                  │

       │                    │                   │                    │ Send trace     │

       │                    │                   │                    │───────────────>│

       │                    │                   │                    │                  │

       │                    │                   │                    │<───────────────│

       │                    │                   │                    │                  │

       │ 200 OK            │                   │                    │                  │

       │<──────────────────│                   │                    │                  │

```

  

### 5.2 Data Models

  

#### Event Types

  

| Event | Source | Parent | Fields |

|-------|--------|--------|--------|

| `APIRequestEvent` | Middleware | None (root) | trace_id, span_id, request_id, start_time, end_time, http_method, endpoint, status_code |

| `APISpanEvent` | Endpoint | root_span_id | trace_id, span_id, parent_span_id, request_id, name, endpoint |

| `LLMGenerationEvent` | LLM client | api_span_id | trace_id, span_id, parent_span_id, model, input_messages, output_content, usage |

  

#### TraceBundle Format

  

```python

@dataclass

class TraceBundle:

    bundle_type: str = "trace_bundle"  ## For detection

    trace_id: str

    request_id: str

    root_span: Optional[APIRequestEvent]

    child_spans: List[APISpanEvent]

    generations: List[LLMGenerationEvent]

    service_name: str

    created_at: float

```

  

#### Legacy Format (for backward compatibility)

  

```python

{

    "event_type": "api_request" | "api_span" | "llm_generation",

    "trace_id": "...",

    "span_id": "...",

    ...

}

```

  

### 5.3 Worker Processing Logic

  

```python

def process_events(events: List[str]):

    bundles = []

    legacy_events = []

  

    ## Step 1: Detect format

    for json_str in events:

        data = json.loads(json_str)

        if data.get("bundle_type") == "trace_bundle":

            bundles.append(TraceBundle.from_json(json_str))

        else:

            legacy_events.append(json_str)

  

    ## Step 2: Process bundles

    for bundle in bundles:

        _send_bundle_to_langfuse(bundle)

  

    ## Step 3: Process legacy events (group by trace_id first)

    if legacy_events:

        groups = group_by_trace_id(legacy_events)

        for group in groups:

            _send_legacy_to_langfuse(group)

  

def _send_bundle_to_langfuse(bundle: TraceBundle):

    ## Create trace

    trace = langfuse.trace(name="API_REQUEST_COMPLETE")

  

    ## Step 1: Create ALL spans first, store in map

    span_map = {}

    for span in bundle.child_spans:

        parent = span_map.get(span.parent_span_id, trace)

        span_obj = parent.span(name=span.name, ...)

        span_map[span.span_id] = span_obj

  

    ## Step 2: Create generations (span_map now has all spans)

    for gen in bundle.generations:

        parent = span_map.get(gen.parent_span_id, trace)

        gen_obj = parent.generation(name="vllm_chat_completion", ...)

```

  

### 5.4 Redis Keys & Environment Variables

  

#### Redis Keys

  

| Key | Type | Purpose |

|-----|------|---------|

| `langfuse:traces` | List (LPUSH/BRPOP) | Main trace queue |

  

#### Environment Variables

  

| Variable | Required | Description |

|----------|----------|-------------|

| `TRACE_ENABLED` | No | Enable/disable tracing (default: true) |

| `REDIS_URL` | Yes | Redis connection URL |

| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |

| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |

| `LANGFUSE_BASE_URL` | Yes | Langfuse host URL |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 6: KIỂM TRA — Verify fix đã work

## ═══════════════════════════════════════════════

  

> ⚠️ Chạy TOÀN BỘ checklist **trước khi** đóng ticket.

  

### 6.1 Verification Commands

  

```bash

## Check Redis Queue

redis-cli LLEN langfuse:traces

redis-cli LRANGE langfuse:traces 0 5

  

## Check Worker Logs

docker compose logs langfuse-worker

docker compose logs langfuse-worker | grep bundle

docker compose logs langfuse-worker | grep -i error

  

## Test End-to-End

curl -X POST http://localhost:8080/v1/chat/completions \

  -H "Content-Type: application/json" \

  -d '{"model": "test", "messages": [{"role": "user", "content": "test"}]}'

docker compose logs langfuse-worker | grep "Sent trace bundle"

```

  

### 6.2 Verification Checklist

  

- [ ] ✅ Symptom ban đầu đã hết (test lại reproduce steps)

- [ ] ✅ Error rate < 0.1% trong 10 phút liên tục

- [ ] ✅ Latency P99 trong ngưỡng bình thường

- [ ] ✅ Không có side effect mới

- [ ] ✅ Langfuse dashboard hierarchy đúng (3 levels)

  

### 6.3 Metrics Before vs After

  

| Metric | Before | After | Target |

|--------|--------|-------|--------|

| Redis LPUSH overhead | N/A | ~1ms | ~1ms |

| Worker latency | N/A | ~10-50ms | <100ms |

| Trace hierarchy | ❌ Sai | ✅ Đúng | 100% correct |

| Queue backlog | N/A | <100 | <1000 |

  

---

  

## ═══════════════════════════════════════════════

## PHASE 7: ĐÚC KẾT — Kaizen & Knowledge Capture

## ═══════════════════════════════════════════════

  

> _"Không đo lường — Không cải tiến."_

> _Viết phần này SAU KHI resolve. Đúc kết từ Phase 1-6 thành knowledge tái sử dụng._

  

---

  

### 7.1 Common Mistakes — Các lỗi đã mắc

  

#### M-01: Race Condition — Worker consume trước khi đủ events

  

**Severity:** 🔴

  

❌ **Sai:**

```python

## Publish từng event riêng lẻ

await trace_publisher.publish(root_event)   ## LPUSH 1

await trace_publisher.publish(span_event)   ## LPUSH 2

await trace_publisher.publish(gen_event)    ## LPUSH 3

## Worker BRPOP có thể nhận trước khi tất cả được push!

```

  

> **Tại sao sai:** Worker BRPOP trước khi tất cả events được LPUSH → thiếu event → hierarchy sai

  

✅ **Đúng:**

```python

## Gom tất cả vào TraceBundle, publish 1 lần

bundle = TraceBundle(

    root_span=root_event,

    child_spans=[span_event],

    generations=[gen_event]

)

await trace_publisher.publish_trace_bundle(bundle)  ## 1 LPUSH duy nhất

```

  

> **Tại sao đúng:** Worker nhận 1 message = đầy đủ 3 events → không có race condition

  

🔍 **Detect trong codebase:**

```bash

grep -rn "publish.*event" src/infrastructure/observability/

```

  

---

  

#### M-02: Event Ordering — Process generations trước spans

  

**Severity:** 🟠

  

❌ **Sai:**

```python

## Process generations TRƯỚC

for gen in bundle.generations:

    parent = span_map.get(gen.parent_span_id, root_span)  ## span_map chưa có!

    gen_span = parent.generation(...)

```

  

✅ **Đúng:**

```python

## Process spans FIRST

for span in bundle.child_spans:

    parent = span_map.get(span.parent_span_id, trace)

    span_obj = parent.span(...)

    span_map[span.span_id] = span_obj

  

## Process generations SECOND

for gen in bundle.generations:

    parent = span_map.get(gen.parent_span_id, trace)  ## span_map đã có!

    gen_span = parent.generation(...)

```

  

---

  

#### M-03: Duplicate Root Span

  

**Severity:** 🟠

  

❌ **Sai:**

```python

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

root_span = langfuse_trace.span(name="API_REQUEST_COMPLETE")  ## DUPLICATE!

```

  

✅ **Đúng:**

```python

langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")

span_map[root.span_id] = langfuse_trace  ## Dùng trace làm parent

```

  

---

  

### 7.2 Best Practices Checklist — Rút ra từ vấn đề này

  

#### Architecture

  

- [ ] ✅ Independent worker process cho Langfuse publishing

- [ ] ✅ Redis queue as message buffer

- [ ] ✅ Async I/O cho non-blocking operations

  

#### Event Collection

  

- [ ] ✅ Bundle all events vào 1 message trước khi publish

- [ ] ✅ Single LPUSH thay vì nhiều LPUSH

  

#### Worker Processing

  

- [ ] ✅ Detect bundle_type field

- [ ] ✅ Process spans FIRST, generations SECOND

- [ ] ✅ Handle both bundle và legacy formats

  

#### Performance

  

- [ ] ✅ Target ~1ms overhead cho tracing

- [ ] ✅ Worker separate process - không ảnh hưởng API latency

  

### 7.3 Action Items — Ngăn tái phát

  

| ## | Action | Priority | Owner | Due | Status | Ticket |

|---|--------|----------|-------|-----|--------|--------|

| 1 | Thêm alert cho queue length > 1000 | P1 | @cuongdn | 2026-03-15 | ⏳ | - |

| 2 | Viết integration test cho TraceBundle | P2 | @cuongdn | 2026-03-20 | ⏳ | - |

  

### 7.4 Lessons Learned

  

**Làm tốt ✅:**

- TraceBundle approach giải quyết triệt để race condition

- Async LPUSH đạt target ~1ms overhead

- Worker process tách biệt hoàn toàn không ảnh hưởng API

  

**Cần cải thiện ⚠️:**

- Cần thêm monitoring/alerting cho queue health

- Test coverage cho tracing path còn thiếu

  

**Câu hỏi mở ❓:**

- Có nên batch nhiều bundles lại không?

  

---

  

### 7.5 Quick Reference Card

  

```

╔══════════════════════════════════════════════════════════╗

║  LANGFUSE WORKER — Quick Ref from PROB-2026-03-10   ║

╠══════════════════════════════════════════════════════════╣

║  🔴 M-01: Race Condition → Bundle all events in 1 msg  ║

║  🟠 M-02: Event Ordering → Spans FIRST, Generations 2nd║

║  🟠 M-03: Duplicate Root → Use trace() as root         ║

╠══════════════════════════════════════════════════════════╣

║  ✅ BP-01: Async LPUSH → ~1ms overhead                 ║

║  ✅ BP-02: Worker process → Zero API impact            ║

║  ✅ BP-03: Bundle format → No race condition            ║

╠══════════════════════════════════════════════════════════╣

║  Debug: redis-cli LLEN langfuse:traces                  ║

║  Worker: docker compose logs langfuse-worker           ║

╚══════════════════════════════════════════════════════════╝

```

  

---

  

## APPENDIX

  

### A. @observe vs Manual SDK - Why not use @observe

  

**Q: Tại sao không dùng Langfuse `@observe` decorator thay vì tự build Redis queue + worker?**

  

**A:** `@observe` decorator không phù hợp với mục tiêu **zero-overhead** của architecture này.

  

| Aspect | @observe Decorator | Current Architecture (Redis + Worker) |

|--------|-------------------|--------------------------------------|

| **Latency impact** | ~5-50ms per call (sync) | ~1ms (async LPUSH, non-blocking) |

| **Execution** | Synchronous SDK call trong request path | Async push to Redis, worker xử lý riêng |

| **GIL contention** | Block event loop, contention với request | Worker có GIL riêng, không ảnh hưởng API |

| **Implementation** | Dễ (~1 dòng code) | Cần Redis + Worker + queue logic |

| **Flexibility** | Bị coupling với Langfuse SDK | Full control over data flow |

  

---

  

### B. Performance Considerations

  

| Metric | Target | Notes |

|--------|--------|-------|

| Redis LPUSH overhead | ~1ms | Async, non-blocking |

| Worker latency | ~10-50ms | Per trace to Langfuse |

| Queue backlog | <1000 | Monitor with LLEN |

| Memory per event | ~1KB | JSON serialized |

  

#### Optimization Tips

  

1. **Batch processing**: Worker processes up to 50 events per batch

2. **Async I/O**: Use `asyncio` for Redis operations in API

3. **Connection pooling**: Reuse Redis connections

4. **No GIL contention**: Worker runs in separate process

  

---

  

### C. References

  

- [LLD_Langfuse_Zero_Overhead_Tracing.md](../2-explanation_ADR_HighLevelDesign/batch1/LLD_Langfuse_Zero_Overhead_Tracing.md)

- [Langfuse_Worker_Guide.md](../Langfuse_Worker_Guide.md)

- [CHANGELOG.md](../CHANGELOG.md)

  

---

  

## REPORT FORMAT

  

```

1. VẤN ĐỀ:    Zero-overhead Langfuse tracing với Redis Worker

   IMPACT:     Latency tăng ~5-50ms/call khi tích hợp trực tiếp

   METRICS:    Redis LPUSH ~1ms, Worker latency ~10-50ms

  

2. NGUYÊN NHÂN: Race condition khi worker consume trước khi đủ events

   DẪN CHỨNG:   Hierarchy sai - generation cùng cấp với span

  

3. GIẢI PHÁP:  TraceBundle - gom 3 events thành 1 message

   DẪN CHỨNG:   Worker logs: "Sent trace bundle with 1 generations"

  

4. PREVENT:    Thêm alert queue length, viết integration test

```

  

---

  

*Created by `@cuongdn` on `2026-03-10` · Last updated: `2026-03-10`*

*Naming: `PROB-2026-03-10-langfuse-worker.md`*


---

# PHẦN C - CHỈ RA MECE CÁC NHƯỢC ĐIỂM CỦA CÁCH TRIỂN KHAI NÀY VÀ ĐỀ XUẤT MECE CÁC GIẢI PHÁP => sAU ĐÓ ĐỀ XUẤT BEST PRACTICES cho việc triển khai langfuse overhead 0 ms

### MECE Analysis: Nhược điểm & Giải pháp

---

#### Chiều 1: Data Durability (Mất data khi nào?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|1.1|**BRPOP = fire-and-forget** — Worker pop event ra, crash trước khi gửi Langfuse → mất event vĩnh viễn|🔴|Worker OOM, segfault, kill -9|
|1.2|**Redis restart không persistence** — Nếu Redis chưa config RDB/AOF, restart = mất toàn bộ queue|🔴|Redis container restart|
|1.3|**No Dead Letter Queue** — Event parse lỗi hoặc Langfuse reject → event bị drop, không retry|🟠|Malformed JSON, Langfuse schema change|
|1.4|**No retry mechanism** — Langfuse trả 5xx → event mất, không có cơ chế retry|🟠|Langfuse downtime|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|Recommendation|
|---|---|---|---|
|**S1.1: Redis STREAM (XADD/XREADGROUP/XACK)**|1.1 hoàn toàn — message chỉ bị xóa sau XACK, crash → auto re-deliver|Trung bình|⭐ Best practice|
|S1.2: Redis persistence (RDB + AOF)|1.2|Thấp (config only)|Phải làm ngay|
|S1.3: DLQ key `langfuse:traces:dlq`|1.3, 1.4|Thấp|Nên làm|
|S1.4: Retry với exponential backoff|1.4|Trung bình|Nên làm nếu giữ LIST|

---

#### Chiều 2: Trace Completeness (Hierarchy có đúng không?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|2.1|**Legacy mode vẫn bị race condition** — Publish 3 events riêng lẻ, worker có thể nhận không đủ trong 1 batch|🔴|Khi KHÔNG dùng TraceBundle (backward compat path)|
|2.2|**Bundle chưa được dùng ở tất cả paths** — Error path, timeout path có thể vẫn publish từng event|🟠|Request timeout, exception trước khi gom bundle|
|2.3|**Không có validation** — Worker không check xem bundle có đủ root + span + generation không|🟡|Partial bundle do bug ở API side|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|**S2.1: Loại bỏ legacy path** hoàn toàn, chỉ chấp nhận bundle|2.1|Thấp — nhưng cần đảm bảo tất cả publishers đã migrate|
|**S2.2: Middleware gom bundle ở finally block** — dù success hay error đều publish|2.2|Thấp|
|S2.3: Worker validate bundle schema trước khi send|2.3|Thấp|

---

#### Chiều 3: Observability of the Observability (Ai monitor worker?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|3.1|**Không có alert khi queue backlog tăng** — Queue có thể phình 100k events mà không ai biết|🔴|Worker chậm/crash, traffic spike|
|3.2|**Không có metrics export** — Không biết worker throughput, error rate, latency|🟠|Production monitoring|
|3.3|**Không có health check** cho worker — K8s không biết worker dead|🟠|Worker hang (không crash nhưng không process)|
|3.4|**Worker log chỉ có INFO** — Không log chi tiết trace_id nào thành công/thất bại|🟡|Debug production issues|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S3.1: Cron job `redis-cli LLEN` + alert khi > threshold|3.1|Thấp|
|S3.2: Worker expose `/metrics` (Prometheus format)|3.2|Trung bình|
|S3.3: Worker expose `/health` + K8s liveness probe|3.3|Thấp|
|S3.4: Structured logging với trace_id, event_count, duration|3.4|Thấp|

---

#### Chiều 4: Scalability (Scale thế nào?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|4.1|**Single worker** — 1 worker bottleneck khi traffic cao|🟠|>500 req/s sustained|
|4.2|**Redis LIST không hỗ trợ multi-consumer** — BRPOP chỉ 1 consumer nhận 1 message|🟠|Muốn scale workers|
|4.3|**Không có backpressure** — API cứ LPUSH, không biết queue đầy → Redis OOM|🟡|Sustained high traffic + worker down|
|4.4|**Sync worker loop** — Blocking BRPOP + sync Langfuse SDK = throughput thấp|🟡|High volume tracing|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|**S4.1: Redis STREAM + Consumer Group**|4.1 + 4.2 cùng lúc — N workers chia tải tự động|Trung bình|
|S4.2: MAXLEN trên Redis LIST/STREAM|4.3 — drop oldest khi quá capacity|Thấp|
|S4.3: Async worker (asyncio + httpx)|4.4 — concurrent Langfuse calls|Trung bình|
|S4.4: Publisher check LLEN trước LPUSH, skip nếu > threshold|4.3|Thấp|

---

#### Chiều 5: Operational Complexity (Vận hành khó ở đâu?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|5.1|**Thêm 2 components** (Redis + Worker) — tăng operational surface|🟠|Mọi lúc|
|5.2|**Worker và API dùng chung Dockerfile** nhưng khác entrypoint — confusion khi debug|🟡|New team member onboard|
|5.3|**Không có drain mode** — Deploy worker mới = có thể mất events đang process|🟡|Rolling deployment|
|5.4|**Config scattered** — Redis URL ở cả API và Worker, dễ mismatch|🟡|Config change|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S5.1: Acceptance — đây là trade-off cần thiết cho zero-overhead|5.1|—|
|S5.2: Tách Dockerfile riêng cho worker, hoặc document rõ|5.2|Thấp|
|S5.3: SIGTERM handler → stop consuming, flush buffer, exit|5.3|Thấp|
|S5.4: Shared `.env` file, validate on startup|5.4|Thấp|

---

#### Chiều 6: Data Accuracy (Data có đúng không?)

|##|Nhược điểm|Severity|Khi nào xảy ra|
|---|---|---|---|
|6.1|**Timestamp drift** — API tạo timestamp, worker gửi muộn → Langfuse duration có thể sai|🟡|Clock skew giữa containers|
|6.2|**Duplicate traces** — Worker crash sau khi gửi Langfuse nhưng trước khi XACK (nếu dùng STREAM)|🟡|Worker crash|
|6.3|**No sampling** — 100% traces → Langfuse cost cao khi traffic lớn|🟡|High traffic production|

**Giải pháp MECE:**

|Option|Giải quyết|Effort|
|---|---|---|
|S6.1: Dùng `time.time()` ở API, worker chỉ forward — OK vì cùng host|6.1|Không cần fix|
|S6.2: Langfuse dedupe by trace_id — đã xử lý server-side|6.2|Không cần fix|
|S6.3: Thêm `sample_rate` ở publisher — chỉ publish N% traces|6.3|Thấp|

---

### Best Practices: Langfuse Zero-Overhead Implementation

Dựa trên toàn bộ phân tích 6 chiều, đây là **tiered recommendation**:

#### Tier 1 — Phải làm (High impact, Low effort)

|##|Practice|Giải quyết chiều nào|Implementation|
|---|---|---|---|
|**BP-1**|**Loại bỏ legacy path, chỉ dùng TraceBundle**|Chiều 2 (completeness)|Xóa code path publish từng event. Middleware gom bundle ở `finally` block — dù success hay error|
|**BP-2**|**Redis persistence (appendonly yes)**|Chiều 1 (durability)|1 dòng config: `redis-server --appendonly yes`|
|**BP-3**|**SIGTERM graceful shutdown**|Chiều 5 (ops)|`signal.signal(SIGTERM, handler)` → stop consume → flush → exit|
|**BP-4**|**Queue length alert**|Chiều 3 (monitoring)|Cron `redis-cli LLEN langfuse:traces`, alert nếu > 1000|
|**BP-5**|**MAXLEN cap trên queue**|Chiều 4 (backpressure)|`LPUSH` + `LTRIM 0 99999` hoặc STREAM `MAXLEN ~ 100000`|

#### Tier 2 — Nên làm (Medium impact)

|##|Practice|Giải quyết chiều nào|Implementation|
|---|---|---|---|
|**BP-6**|**Dead Letter Queue**|Chiều 1 (durability)|Parse fail / Langfuse fail N lần → `LPUSH langfuse:traces:dlq`|
|**BP-7**|**Retry với backoff**|Chiều 1 (durability)|Langfuse 5xx → retry 3 lần (1s, 2s, 4s) → DLQ|
|**BP-8**|**Circuit breaker**|Chiều 1 + 4|Langfuse 5xx liên tục 10 lần → pause 30s → retry|
|**BP-9**|**Worker structured logging**|Chiều 3 (monitoring)|Log JSON: `{"trace_id": "...", "events": 3, "duration_ms": 45, "status": "sent"}`|
|**BP-10**|**Sample rate**|Chiều 6 (accuracy/cost)|`TRACE_SAMPLE_RATE=0.5` → chỉ trace 50% requests|

#### Tier 3 — Tốt nhưng chưa cần ngay (Scale future)

|##|Practice|Khi nào cần|Implementation|
|---|---|---|---|
|**BP-11**|**Redis STREAM thay LIST**|Khi cần multi-worker hoặc at-least-once|Migrate LPUSH/BRPOP → XADD/XREADGROUP/XACK|
|**BP-12**|**Multi-worker consumer group**|>500 req/s sustained|STREAM consumer group, N worker containers|
|**BP-13**|**Async worker (asyncio)**|Worker throughput bottleneck|Async Langfuse HTTP calls, concurrent processing|
|**BP-14**|**Worker health check endpoint**|K8s deployment|Expose `/health`, liveness/readiness probes|

---

### Tóm lại: Current State vs Target State

```
CURRENT STATE (Image 1 - đang bị sai):

emotion-api-request          ← Sai tên
  └── API_REQUEST_COMPLETE   ← Duplicate root
      └── api_chat_completions
  └── vllm_chat_completion   ← Lọt ra ngoài!

TARGET STATE (Image 2 - muốn đạt):

API_REQUEST_COMPLETE
  └── API_REQUEST_COMPLETE
      └── api_chat_completions
          └── vllm_chat_completion

IDEAL STATE (sau khi apply best practices):

API_REQUEST_COMPLETE              ← trace() tạo, KHÔNG duplicate
  └── api_chat_completions        ← span, parent = trace
      └── vllm_chat_completion    ← generation, parent = span
```

**3 fixes cần làm ngay** để đạt target state:

1. Trace name: `"emotion-api-request"` → `"API_REQUEST_COMPLETE"`
2. Không tạo thêm `span("API_REQUEST_COMPLETE")` — dùng `trace()` làm parent trực tiếp
3. Spans FIRST, generations SECOND — đảm bảo span_map đầy đủ

**5 best practices nên làm tiếp** (Tier 1): Bỏ legacy path, Redis persistence, graceful shutdown, queue alert, MAXLEN cap.



---

# PHẦN D - ê, có cách nào khác ko, ví dụ như @observe nhưng được langfuse hỗ trợ trực tiếp cho việc triển riêng 1 luồng như này ý bro ????




---

Câu hỏi cực hay — để mình research xem Langfuse có hỗ trợ native cho pattern này không.Okay, research xong rồi. Có **3 cách native/semi-native** mà Langfuse hỗ trợ, không cần tự build Redis + Worker từ đầu. Mình so sánh thẳng:

---

### MECE: Tất cả các cách đạt zero-overhead với Langfuse

#### Option A: Tự build Redis + Worker (cách của bạn hiện tại)

```
App → LPUSH Redis → Worker process → Langfuse API
```

Ưu: Full control. Nhược: Tự build + maintain tất cả.

---

#### Option B: `@observe` + OTel Collector sidecar (container riêng)

**Đây là cách Langfuse THỰC SỰ hỗ trợ native.** Và đây chính là thứ bạn đang hỏi.

```
App (@observe / Langfuse SDK)
  → BatchSpanProcessor → OTLP HTTP export → localhost:4318
                                                    ↓
                                            ┌──────────────┐
                                            │  OTel        │
                                            │  Collector   │  ← Container riêng
                                            │  (sidecar)   │
                                            └──────┬───────┘
                                                   ↓
                                            Langfuse OTLP endpoint
                                            /api/public/otel/v1/traces
```

Langfuse có **OTLP endpoint chính thức**: Langfuse có thể nhận traces trên endpoint `/api/public/otel`, hỗ trợ OTLP over HTTP với cả HTTP/JSON và HTTP/protobuf.

Code app side cực đơn giản:

```python
from langfuse import observe, get_client

@observe()
def my_endpoint(query: str):
    result = call_llm(query)
    return result
```

docker-compose thêm 1 container OTel Collector:

```yaml
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel-config.yaml:/etc/otelcol-contrib/config.yaml
    ports:
      - "4318:4318"

  your-api:
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
      - LANGFUSE_PUBLIC_KEY=pk-lf-xxx
      - LANGFUSE_SECRET_KEY=sk-lf-xxx
```

OTel Collector config (`otel-config.yaml`):

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 512

exporters:
  otlphttp/langfuse:
    endpoint: "https://cloud.langfuse.com/api/public/otel"
    headers:
      Authorization: "Basic <base64(pk:sk)>"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/langfuse]
```

**NHƯNG — vẫn KHÔNG giải quyết GIL contention:**

Vấn đề: Langfuse SDK v3 là "a thin layer on top of the official OpenTelemetry client" — nó đăng ký `LangfuseSpanProcessor` lên global TracerProvider. Nghĩa là `BatchSpanProcessor` vẫn chạy **trong app process**, serialize vẫn giữ GIL, chỉ là HTTP POST đi sang collector thay vì đi thẳng Langfuse. Bước serialize (CPU-bound, giữ GIL) vẫn xảy ra trong app.

---

#### Option C: Langfuse Async API trực tiếp (không dùng SDK trong app)

```
App → json.dumps() → HTTP POST async → Langfuse /api/public/ingestion
```

Langfuse v3 dùng kiến trúc event-driven: nhận HTTP requests từ SDK, queue HTTP bodies trong backend, và xử lý bất đồng bộ. Endpoint `/api/public/ingestion` giờ là async — nó accept events và trả 207 ngay lập tức.

Nghĩa là bạn có thể **bỏ Langfuse SDK khỏi app**, tự build HTTP POST async (dùng `httpx` hoặc `aiohttp`) gửi thẳng lên Langfuse API. Langfuse server tự queue + process.

Nhưng bạn phải tự format đúng Langfuse ingestion API schema — mất hết tiện ích của SDK (`@observe`, auto context propagation, v.v.).

---

#### Option D: `@observe` + `SimpleSpanProcessor` thay `BatchSpanProcessor`

Thay vì batch (gom rồi flush — gây GIL spike), dùng `SimpleSpanProcessor` gửi **từng span ngay lập tức**. Overhead đều hơn (không có spike) nhưng tổng overhead cao hơn.

Langfuse SDK không trực tiếp hỗ trợ swap processor, nhưng vì nó dựa trên OTel, bạn có thể override:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from langfuse.opentelemetry import LangfuseExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(LangfuseExporter()))
```

**Vấn đề:** Mỗi span = 1 HTTP call đồng bộ → latency tăng 5-20ms mỗi span. Tệ hơn batch cho hầu hết use cases.

---

### So sánh thẳng 4 options

||**A: Redis + Worker** (của bạn)|**B: @observe + OTel Collector**|**C: Async HTTP API**|**D: SimpleSpanProcessor**|
|---|---|---|---|---|
|**GIL contention**|✅ Zero — SDK không ở app|❌ **Vẫn có** — serialize trong app|✅ Zero — không import SDK|❌ Vẫn có|
|**Overhead per request**|~1ms (LPUSH)|~5-15ms (serialize + network to collector)|~2-5ms (json + async HTTP)|~5-20ms per span × N spans|
|**DX cho coder**|❌ Phải tự quản lý parent_span_id|✅ `@observe` tự propagate|❌ Tự build mọi thứ|✅ `@observe` hoạt động|
|**Nested spans**|❌ Phải dùng TraceContext helper|✅ OTel context propagation tự động|❌ Tự build|✅ Tự động|
|**Infrastructure**|Redis + Worker container|OTel Collector container|Không thêm gì|Không thêm gì|
|**Khi Langfuse down**|Events nằm trong Redis|Events trong collector buffer (limited)|Mất nếu không buffer|Mất|
|**Complexity**|Cao|Trung bình|Cao|Thấp|

---

### Phát hiện quan trọng: Option B KHÔNG giải quyết được GIL

Nhiều người nghĩ OTel Collector sidecar giải quyết GIL — **SAI**. Tài liệu nghiên cứu ban đầu của bạn đã chỉ đúng:

```
App process:
  span.end() → BatchSpanProcessor.on_end()
    → acquire lock → queue.put(span)        ← GIL contention ở đây
    → background thread: serialize → export  ← GIL contention ở đây

OTel Collector chỉ thay đổi:
  export destination: Langfuse → localhost collector
  
KHÔNG thay đổi:
  serialize vẫn trong app process
  lock contention vẫn trong app process
  GIL vẫn bị giữ khi serialize
```

---

### Vậy best practice thực sự là gì?

Tuỳ vào **mức độ nhạy cảm với latency**:

#### Nếu P99 latency < 100ms là bắt buộc (production AI, real-time):

→ **Option A (Redis + Worker)** là cách duy nhất triệt để.

Nhưng nên kết hợp **TraceContext helper** (như mình đã đề xuất ở message trước) để coder dùng dễ như `@observe`:

```python
## Gần như dễ dùng như @observe, nhưng zero GIL:
ctx = TraceContext(request)
with ctx.span("orchestrator"):
    with ctx.span("tool_search"):
        ctx.generation("embedding", model="text-embedding-3", ...)
```

#### Nếu chấp nhận ~5-15ms overhead (đa số web app, không real-time):

→ **Option B (@observe + OTel Collector)** — đơn giản nhất, Langfuse hỗ trợ native, DX tốt nhất.

GIL spike ~1s sẽ **giảm đáng kể** (vì HTTP export đi localhost thay vì Langfuse cloud), nhưng không triệt để zero.

#### Nếu prototype / dev environment:

→ **Dùng @observe thẳng**, không cần collector, không cần Redis. Chấp nhận overhead.

---

### Tóm lại 1 câu

**Langfuse KHÔNG có cơ chế native nào để tách GIL ra khỏi app process.** SDK v3 dựa trên OTel, và OTel Python SDK luôn serialize trong app process. OTel Collector sidecar chỉ offload phần HTTP, không offload phần serialize.

Nếu cần **thật sự zero-overhead**, cách của bạn (Redis + Worker, không import Langfuse SDK trong app) là **đúng và là cách duy nhất**. Cái cần cải thiện không phải kiến trúc mà là **DX** — thêm TraceContext helper để coder không phải quản lý parent_span_id thủ công.


---

# PHẦN E: Để overhead ~0, đâu là best practices.  Với mục tiêu là trace được toàn bộ request chứ ko phải ramdom chỉ 0.3 mới được trace

