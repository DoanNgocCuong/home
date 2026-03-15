# Langfuse + Redis Worker Integration Template

## Overview

Template for implementing Langfuse tracing with Redis queue + independent worker pattern. Designed for **zero-overhead** in API request path.

## 1. Common Mistakes

### 1.1 Race Condition

| # | Mistake | Symptom | Root Cause | Fix |
|---|---------|---------|------------|-----|
| 1 | Worker consumes before all events published | Hierarchy broken: child events at same level as parent | Worker BRPOP before all LPUSH complete | **Bundle all events** into 1 message, publish at end of request |
| 2 | Event ordering wrong | Generation has no parent span | Worker processes generations before spans | **Process spans FIRST, then generations SECOND** |

### 1.2 Hierarchy Issues

| # | Mistake | Symptom | Root Cause | Fix |
|---|---------|---------|------------|-----|
| 3 | Duplicate root nodes | 2 identical nodes in Langfuse UI | Both `trace()` and `span()` create root | **Don't create separate root span** - use trace as direct parent |
| 4 | Wrong trace name | UI shows wrong name | Hardcoded incorrect name | Use standard naming: `API_REQUEST_COMPLETE` |

### 1.3 Format Handling

| # | Mistake | Symptom | Root Cause | Fix |
|---|---------|---------|------------|-----|
| 5 | Worker doesn't handle bundle | Traces not appearing | Worker only handles 1 format | Add `bundle_type` detection - support both formats |

---

## 2. Best Practices Checklist

### 2.1 Architecture **

- [ ]Independent worker process** - separate from API service
- [ ] **Redis queue** as message buffer between API and worker
- [ ] **Async Redis operations** in API (non-blocking ~1ms)
- [ ] **Graceful degradation** - log warning when Redis/Langfuse down, don't crash request

### 2.2 Event Collection

- [ ] **Bundle events** at end of request (not publish individually)
- [ ] Collect all events before publishing:
  - Root span (from middleware)
  - Child spans (from endpoints)
  - LLM generations (from LLM client)
- [ ] Single Redis LPUSH for entire bundle (3 → 1)

### 2.3 Worker Processing

- [ ] **Detect format**: Check `bundle_type` field
- [ ] **Process spans FIRST** → add to span_map
- [ ] **Process generations SECOND** → use span_map for parent lookup
- [ ] Handle both bundle and legacy formats

### 2.4 Langfuse Hierarchy

```
TRACE_NAME (from trace())
  └── span_1 (from endpoint)
      └── generation_1 (from LLM client)
```

- [ ] Use `trace()` as root (not `span()`)
- [ ] Standard trace name: `API_REQUEST_COMPLETE`
- [ ] Proper parent-child relationships

### 2.5 Error Handling

- [ ] Try-catch all tracing calls
- [ ] Never let tracing errors affect API response
- [ ] Log errors with appropriate levels

---

## 3. Low Level Design

### 3.1 System Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   API      │     │   Redis     │     │   Worker    │
│  Service   │     │   Queue     │     │  Process    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                    │
       │ LPUSH (bundle)   │                    │
       │────────────────>│                    │
       │                  │                    │
       │                  │ BRPOP             │
       │                  │<─────────────────│
       │                  │                    │
       │                  │ Parse & Send      │
       │                  │                   │
       │                  │                   │──────> Langfuse
       │                  │                   │       Cloud
       │                  │                   │
       │ 200 OK           │                   │
       │<────────────────│                    │
```

### 3.2 Data Models

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

### 3.3 Worker Processing Logic

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

### 3.4 Redis Keys

| Key | Type | Purpose |
|-----|------|---------|
| `langfuse:traces` | List (LPUSH/BRPOP) | Main trace queue |

### 3.5 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TRACE_ENABLED` | No | Enable/disable tracing (default: true) |
| `REDIS_URL` | Yes | Redis connection URL |
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_BASE_URL` | Yes | Langfuse host URL |

---

## 4. Debugging Guide

### 4.1 Check Queue

```bash
# Queue length
redis-cli LLEN langfuse:traces

# View messages
redis-cli LRANGE langfuse:traces 0 5

# Pretty print
redis-cli LRANGE langfuse:traces 0 0 | jq .
```

### 4.2 Worker Logs

```bash
# All logs
docker compose logs langfuse-worker

# Bundle processing
docker compose logs langfuse-worker | grep bundle

# Errors only
docker compose logs langfuse-worker | grep -i error
```

### 4.3 Test End-to-End

```bash
# Make API call
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "test", "messages": [{"role": "user", "content": "test"}]}'

# Check worker received bundle
docker compose logs langfuse-worker | grep "Sent trace bundle"
```

---

## 5. Performance Considerations

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

## 6. Related Documents

- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [LLD_Langfuse_Zero_Overhead_Tracing.md](../5-CKP_research_plan_implement_docs/batch1/L/LD_Langfuse_Zero_Overhead_Tracing.md) - Full LLD

---

*Template version: 1.0*
*Last updated: 2026-03-10*
