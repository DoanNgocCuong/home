# Langfuse + Redis Worker Integration Guide

## Table of Contents

1. [Problem Statement](#1-problem-statement)
   - 1.1 [Background - Tại sao cần Langfuse + Redis Worker](#11-background---tại-sao-cần-langfuse--redis-worker)
   - 1.2 [Root Cause - Vấn đề khi tích hợp trực tiếp](#12-root-cause---vấn-đề-khi-tích-hợp-trực-tiếp)
   - 1.3 [Solution - Architecture overview](#13-solution---architecture-overview)

2. [Các Sai Lầm Đã Gặp (Common Mistakes)](#2-các-sai-lầm-đã-gặp-common-mistakes)
   - 2.1 [Race Condition - Worker consume trước khi đủ events](#21-race-condition---worker-consume-trước-khi-đủ-events)
   - 2.2 [Event Ordering - Process generations trước spans](#22-event-ordering---process-generations-trước-spans)
   - 2.3 [Duplicate Root Span - Tạo 2 root nodes](#23-duplicate-root-span---tạo-2-root-nodes)
   - 2.4 [Trace Name - Sai tên hiển thị](#24-trace-name---sai-tên-hiển-thị)
   - 2.5 [Legacy vs Bundle Format - Worker không handle cả 2](#25-legacy-vs-bundle-format---worker-không-handle-cả-2)

3. [Best Practices Checklist](#3-best-practices-checklist)
   - 3.1 [Architecture - Worker process, Redis queue, async I/O](#31-architecture---worker-process-redis-queue-async-io)
   - 3.2 [Event Collection - Bundle events, single LPUSH](#32-event-collection---bundle-events-single-lpush)
   - 3.3 [Worker Processing - Detect format, spans FIRST, generations SECOND](#33-worker-processing---detect-format-spans-first-generations-second)
   - 3.4 [Langfuse Hierarchy - trace() as root, đúng parent-child](#34-langfuse-hierarchy---trace-as-root-đúng-parent-child)
   - 3.5 [Error Handling - Graceful degradation](#35-error-handling---graceful-degradation)
   - 3.6 [Performance - ~1ms overhead target](#36-performance---1ms-overhead-target)

4. [Low Level Design](#4-low-level-design)
   - 4.1 [System Diagram - Flow từ API → Redis → Worker → Langfuse](#41-system-diagram---flow-từ-api--redis--worker--langfuse)
   - 4.2 [Data Models - Event types, TraceBundle format, Legacy format](#42-data-models---event-types-tracebundle-format-legacy-format)
   - 4.3 [Worker Processing Logic - Code examples](#43-worker-processing-logic---code-examples)
   - 4.4 [Redis Keys & Environment Variables](#44-redis-keys--environment-variables)
   - 4.5 [Langfuse @observe vs Manual SDK - Why not use @observe](#45-langfuse-observe-vs-manual-sdk---why-not-use-observe)

5. [Debugging Guide](#5-debugging-guide)
   - 5.1 [Check Redis Queue](#51-check-redis-queue)
   - 5.2 [Check Worker Logs](#52-check-worker-logs)
   - 5.3 [Test End-to-End](#53-test-end-to-end)

6. [Performance Considerations](#6-performance-considerations)

7. [Related Documents](#7-related-documents)

---

## 1. Problem Statement

### 1.1 Background - Tại sao cần Langfuse + Redis Worker

Langfuse SDK v3 khi tích hợp trực tiếp vào FastAPI service gây ra **overhead ~1s** do GIL (Global Interpreter Lock) contention khi background flush thread chạy trùng với request đang xử lý.

**Mục tiêu:** Zero-overhead tracing cho production AI service với high-throughput requirements.

### 1.2 Root Cause - Vấn đề khi tích hợp trực tiếp

- Langfuse SDK dùng OpenTelemetry `BatchSpanProcessor`
- Background thread serialize + HTTP POST giữ GIL
- Khi flush trùng với request → event loop bị block
- Latency tăng ~5-50ms per call

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

## 2. Các Sai Lầm Đã Gặp (Common Mistakes)

### 2.1 Race Condition - Worker consume trước khi đủ events

| # | Issue | Symptom | Root Cause | Fix |
|---|-------|---------|------------|-----|
| 1 | **Worker nhận không đủ events** | Hierarchy sai: `vllm_chat_completion` cùng cấp với `api_chat_completions` | Worker BRPOP trước khi tất cả events được LPUSH | Gom tất cả events vào **TraceBundle**, publish 1 lần cuối request |

### 2.2 Event Ordering - Process generations trước spans

| # | Issue | Symptom | Root Cause | Fix |
|---|-------|---------|------------|-----|
| 2 | **Event ordering** | Generation không có parent span | Worker process generations TRƯỚC khi process spans | **Process spans FIRST, then generations SECOND** |

#### Chi tiết Fix: Event Ordering

```python
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

### 2.3 Duplicate Root Span - Tạo 2 root nodes

| # | Issue | Symptom | Root Cause | Fix |
|---|-------|---------|------------|-----|
| 3 | **Duplicate nodes trong Langfuse UI** | 2 nodes cùng tên "API_REQUEST_COMPLETE" | Cả `trace()` và `span()` đều tạo root span | Không tạo root span riêng, dùng trace làm parent trực tiếp |

#### Chi tiết Fix: Duplicate Root Span

```python
# SAI (trước fix):
langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")
root_span = langfuse_trace.span(name="API_REQUEST_COMPLETE")  # DUPLICATE!
# → Tạo 2 nodes trong UI

# ĐÚNG (sau fix):
langfuse_trace = self.langfuse.trace(name="API_REQUEST_COMPLETE")
span_map[root.span_id] = langfuse_trace  # Dùng trace làm parent
# → api_chat_completions sẽ nested dưới trace's root span
```

### 2.4 Trace Name - Sai tên hiển thị

| # | Issue | Symptom | Root Cause | Fix |
|---|-------|---------|------------|-----|
| 4 | **Trace name sai trong UI** | Hiển thị "emotion-api-request" thay vì "API_REQUEST_COMPLETE" | Hardcoded wrong name | Đổi trace name thành "API_REQUEST_COMPLETE" |

### 2.5 Legacy vs Bundle Format - Worker không handle cả 2

| # | Issue | Symptom | Root Cause | Fix |
|---|-------|---------|------------|-----|
| 5 | **Worker không xử lý bundle** | Traces không hiển thị trong Langfuse | Worker chỉ xử lý 1 format | Thêm logic detect `bundle_type` - hỗ trợ cả 2 formats |

---

## 3. Best Practices Checklist

### 3.1 Architecture - Worker process, Redis queue, async I/O

- [ ] **Independent worker process** - separate from API service
- [ ] **Redis queue** as message buffer between API and worker
- [ ] **Async Redis operations** in API (non-blocking ~1ms)
- [ ] **Graceful degradation** - log warning when Redis/Langfuse down, don't crash request

### 3.2 Event Collection - Bundle events, single LPUSH

- [ ] **Bundle events** at end of request (not publish individually)
- [ ] Collect all events before publishing:
  - Root span (from middleware)
  - Child spans (from endpoints)
  - LLM generations (from LLM client)
- [ ] Single Redis LPUSH for entire bundle (3 → 1)

### 3.3 Worker Processing - Detect format, spans FIRST, generations SECOND

- [ ] **Detect format**: Check `bundle_type` field
- [ ] **Process spans FIRST** → add to span_map
- [ ] **Process generations SECOND** → use span_map for parent lookup
- [ ] Handle both bundle and legacy formats

### 3.4 Langfuse Hierarchy - trace() as root, đúng parent-child

```
TRACE_NAME (from trace())
  └── span_1 (from endpoint)
      └── generation_1 (from LLM client)
```

- [ ] Use `trace()` as root (not `span()`)
- [ ] Standard trace name: `API_REQUEST_COMPLETE`
- [ ] Proper parent-child relationships

### 3.5 Error Handling - Graceful degradation

- [ ] Try-catch all tracing calls
- [ ] Never let tracing errors affect API response
- [ ] Log errors with appropriate levels

### 3.6 Performance - ~1ms overhead target

- [ ] **Async Redis operations** - không block event loop
- [ ] **Non-blocking LPUSH** - ~1ms overhead
- [ ] Worker chạy **independent process** - không ảnh hưởng API latency

---

## 4. Low Level Design

### 4.1 System Diagram - Flow từ API → Redis → Worker → Langfuse

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │     │     API     │     │   Redis     │     │   Worker    │     │Langfuse  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬─────┘
       │                    │                   │                    │                  │
       │ POST /v1/chat      │                   │                    │                  │
       │───────────────────>│                   │                    │                  │
       │                    │                   │                    │                  │
       │                    │ Call vLLM         │                    │                  │
       │                    │────────────────────────────────────────────────────────────>│
       │                    │<────────────────────────────────────────────────────────────│
       │                    │                   │                    │                  │
       │                    │ Build TraceBundle │                    │                  │
       │                    │ (root + span +    │                    │                  │
       │                    │  generation)      │                    │                  │
       │                    │                   │                    │                  │
       │                    │ Publish Bundle    │                    │                  │
       │                    │ (1 LPUSH)        │                    │                  │
       │                    │─────────────────>│                    │                  │
       │                    │                   │                    │                  │
       │                    │                   │ LPUSH + OK        │                  │
       │                    │<──────────────────│                    │                  │
       │                    │                   │                    │                  │
       │                    │                   │ BRPOP + bundle    │                  │
       │                    │                   │<───────────────────│                  │
       │                    │                   │                    │                  │
       │                    │                   │ Parse bundle       │                  │
       │                    │                   │ (bundle_type=     │                  │
       │                    │                   │  trace_bundle)    │                  │
       │                    │                   │                    │                  │
       │                    │                   │                    │ Send trace     │
       │                    │                   │                    │───────────────>│
       │                    │                   │                    │                  │
       │                    │                   │                    │<───────────────│
       │                    │                   │                    │                  │
       │ 200 OK            │                   │                    │                  │
       │<──────────────────│                   │                    │                  │
```

### 4.2 Data Models - Event types, TraceBundle format, Legacy format

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
    bundle_type: str = "trace_bundle"  # For detection
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

### 4.3 Worker Processing Logic - Code examples

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

### 4.4 Redis Keys & Environment Variables

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

### 4.5 Langfuse @observe vs Manual SDK - Why not use @observe

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

---

## 5. Debugging Guide

### 5.1 Check Redis Queue

```bash
# Queue length
redis-cli LLEN langfuse:traces

# View messages
redis-cli LRANGE langfuse:traces 0 5

# Pretty print
redis-cli LRANGE langfuse:traces 0 0 | jq .
```

### 5.2 Check Worker Logs

```bash
# All logs
docker compose logs langfuse-worker

# Bundle processing
docker compose logs langfuse-worker | grep bundle

# Errors only
docker compose logs langfuse-worker | grep -i error
```

### 5.3 Test End-to-End

```bash
# Make API call
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "test", "messages": [{"role": "user", "content": "test"}]}'

# Check worker received bundle
docker compose logs langfuse-worker | grep "Sent trace bundle"
```

---

## 6. Performance Considerations

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

## 7. Related Documents

- [CHANGELOG.md](./CHANGELOG.md) - Version history
- [LANGFUSE_OBSERVE_VS_MANUAL.md](./LANGFUSE_OBSERVE_VS_MANUAL.md) - @observe vs Manual SDK

---

*Generated: 2026-03-10*
*Last updated: 2026-03-10*
