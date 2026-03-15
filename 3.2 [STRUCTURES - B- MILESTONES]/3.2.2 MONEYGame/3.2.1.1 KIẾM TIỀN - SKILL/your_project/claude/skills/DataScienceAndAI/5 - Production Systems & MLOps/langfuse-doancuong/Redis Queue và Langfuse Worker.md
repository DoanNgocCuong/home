## Tại sao Redis LIST thay vì RabbitMQ/Celery?

### Vấn đề GIL

```
FastAPI (event loop - single thread)
│
├── Request xử lý ~40ms
│
└── Langfuse SDK dùng background thread để flush
    │
    ├── Thread giữ GIL để serialize + send data
    ├── Event loop bị BLOCK vì GIL
    └── ❌ Request phải đợi thêm ~1s
```

**GIL (Global Interpreter Lock)** chỉ cho phép **1 thread chạy Python bytecode** tại một thời điểm. Khi Langfuse SDK (chạy trong background thread) giữ GIL để send data → event loop của FastAPI bị block hoàn toàn.

### Tại sao Redis LIST là đủ?

|Yêu cầu|Redis LIST|RabbitMQ/Celery|
|---|---|---|
|Pub/Sub đơn giản|✅ LPUSH/BRPOP|✅|
|Blocking read|✅ BRPOP|✅|
|Persistence|✅ AOF/RDB|✅|
|Đã có trong infra|✅ (đã dùng)|❌ Thêm|
|Scale với N instances|✅ (shared Redis)|✅|
|Complexity|Thấp|Cao|

**Không cần message queue phức tạp** vì:

1. **1 producer** (FastAPI) → **1 consumer** (Worker) - pattern đơn giản
2. **Không cần routing, exchanges, ack** phức tạp
3. **Redis đã có sẵn** - không thêm infra mới

### Flow

```
FastAPI (GIL #1)              Redis LIST              Langfuse Worker (GIL #2)
     │                                                    │
     │ LPUSH "langfuse:traces"                           │
     ├───────────────────► [event1, event2, ...]         │
     │ (1ms - non-blocking)                              │
     │                                                    │ BRPOP
     │                                                    ├──────────────►
     │                                                    │ (blocking)
     │                                                    │
     ▼                                                    │ Call Langfuse SDK
Response ngay lập tức                                    │ (GIL block OK!)
                                                        ├──────────────────► Langfuse Cloud
```

**Tóm lại:** Redis LIST đủ để giải quyết vấn đề GIL mà không cần thêm queue phức tạp như RabbitMQ. GIL là lý do cần tách process, còn Redis chỉ là transport đơn giản để nối 2 process.


---

# RỦI RO PRODUCTION
## 1. **Worker Failure - Traces bị tắc**

```
Redis: [event1, event2, event3, ..., event10000...]  ← Queue grow unbounded
Worker: ❌ Crashed
```

|Risk|Impact|Mitigation|
|---|---|---|
|Worker crash|Traces pile up in Redis|Monitor queue length + alert|
|Worker chậm|Queue grow → OOM|Worker scale horizontally|

## 2. **Redis Down - Lose Traces**

```
FastAPI → LPUSH → Redis ❌ (connection error)
           │
           └── Trace bị mất hoàn toàn
```

**Nhưng:** FastAPI vẫn hoạt động bình thường (traces là optional). Chỉ mất observability, không ảnh hưởng business logic.

## 3. **No Retry - Langfuse API Fail = Data Loss**

```python
# Trong worker
try:
    langfuse.trace(...)
except Exception:
    # ❌ Event bị drop - không retry
    pass
```

|Scenario|Result|
|---|---|
|Langfuse API timeout|Event lost|
|Langfuse rate limit|Event lost|
|Network blip|Event lost|

## 4. **At-Least-Once (Potential Duplicates)**

```
Worker: BRPOP → process → Langfuse OK
Redis: [event1, event2, ...]
       ^ Chưa xóa!
       
# Nếu worker crash SAU khi call Langfuse NHƯNG TRƯỚC khi xóa:
# → Event được gửi 2 lần (duplicate)
```

## 5. **Single Point of Failure**

```
          ┌─────────────────┐
          │  Langfuse       │
          │  Worker #1      │  ← Chỉ có 1 worker
          └────────┬────────┘
                   │
                   ▼
            Nếu worker down → Không trace gì được gửi
```

## 6. **Trace Delay - Không Real-time**

```
Request → Redis (1ms) → Worker (process) → Langfuse (2-5s delay)
                                    ↑
                              Batch accumulate
```

## Risk Matrix

|Risk|Probability|Impact|Mitigation|
|---|---|---|---|
|Worker crash|Medium|High|Auto-restart, monitoring|
|Redis down|Low|Low|FastAPI vẫn chạy|
|Langfuse API fail|Medium|Low|Retry logic|
|Duplicates|Low|Low|Idempotent (Langfuse handles)|
|Queue full|Low|High|Alert when >N items|

## Recommendations

1. **Thêm health check** cho worker
2. **Monitor queue length** - alert khi >1000 items
3. **Thêm retry** với exponential backoff
4. **Consider dead letter queue** cho failed events
5. **2 workers** để redundancy

