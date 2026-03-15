

Giải thích cách FastAPI hoạt động với async/await:


[3 tools called]



Giải thích cách FastAPI hoạt động với async/await:

## FastAPI + Async/Await: Cách hoạt động

### 1. Event loop (single-threaded)

FastAPI/Uvicorn dùng 1 event loop (1 thread) để xử lý nhiều requests:

```
┌─────────────────────────────────────┐
│  Event Loop (1 thread duy nhất)    │
│                                     │
│  Chạy liên tục:                    │
│  1. Nhận request                    │
│  2. Tạo coroutine (async function) │
│  3. Schedule coroutine vào loop    │
│  4. Xử lý các coroutines đang chờ  │
│  5. Đợi I/O (DB/API) → chuyển sang│
│     coroutine khác                  │
│  6. Khi I/O xong → resume coroutine│
│  7. Trả response                    │
└─────────────────────────────────────┘
```

---

### 2. Cơ chế async/await

Khi gặp `await`, event loop tạm dừng coroutine đó và chuyển sang coroutine khác:

```python
# Request 1
async def endpoint():
    data = await service.create_event_async(request)  # ← TẠM DỪNG tại đây
    return data  # ← Chờ I/O xong mới chạy dòng này
```

Timeline:

```
T=0ms:   Request 1 đến → Tạo coroutine 1
T=1ms:   Coroutine 1 chạy → gặp await DB query
         ↓
         Event loop TẠM DỪNG coroutine 1
         ↓
         Chuyển sang xử lý Request 2 (nếu có)
         
T=50ms:  DB query xong → Event loop RESUME coroutine 1
T=51ms:  Coroutine 1 tiếp tục → return response
```

---

### 3. Ví dụ với code thực tế

#### Endpoint của bạn:

```python
@router.post("/conversations/end")
async def create_conversation_event(
    request: ConversationEventCreateRequest,
    service: ConversationEventService = Depends(get_conversation_event_service_async),
):
    # STEP 1: Async DB operation
    data = await service.create_event_async(request)  # ← NON-BLOCKING!
    
    # STEP 2: Fire-and-forget RabbitMQ
    asyncio.create_task(publish_conversation_event(...))  # ← NON-BLOCKING!
    
    # STEP 3: Return ngay
    return ConversationEventCreateResponse(...)  # ← < 50ms total
```

Timeline chi tiết:

```
T=0ms:    Request đến → FastAPI tạo coroutine
T=1ms:    Coroutine bắt đầu chạy
T=2ms:    Gặp: await service.create_event_async(request)
          ↓
          Event loop:
          1. Gửi DB query (async SQLAlchemy)
          2. TẠM DỪNG coroutine này
          3. Chuyển sang xử lý request khác (nếu có)
          
T=30ms:   DB query xong → Event loop RESUME coroutine
T=31ms:   Chạy: asyncio.create_task(...) (fire-and-forget, không await)
T=32ms:   Return response → 202 Accepted
          
Total: ~32ms (thay vì 2000ms+ với sync)
```

---

### 4. So sánh: Blocking vs Non-blocking

#### ❌ Blocking (Cách cũ):

```python
async def endpoint():
    data = service.create_event(request)  # SYNC call → BLOCK!
    return data
```

Timeline với 3 requests:

```
T=0ms:    Request 1 đến → Block event loop 2000ms
T=1ms:    Request 2 đến → PHẢI ĐỢI (event loop bị block)
T=2ms:    Request 3 đến → PHẢI ĐỢI (event loop bị block)

T=2000ms: Request 1 xong
T=2001ms: Request 2 mới bắt đầu → Block event loop 2000ms
T=2002ms: Request 3 vẫn đợi

T=4000ms: Request 2 xong
T=4001ms: Request 3 mới bắt đầu → Block event loop 2000ms

T=6000ms: Request 3 xong

Total: 6000ms (sequential)
→ Requests 2, 3 bị timeout (30s gateway timeout) ❌
```

---

#### ✅ Non-blocking (Cách mới):

```python
async def endpoint():
    data = await service.create_event_async(request)  # ASYNC call → NON-BLOCK!
    return data
```

Timeline với 3 requests:

```
T=0ms:    Request 1 đến → Tạo coroutine 1
T=1ms:    Request 2 đến → Tạo coroutine 2
T=2ms:    Request 3 đến → Tạo coroutine 3

T=3ms:    Coroutine 1: await DB query → TẠM DỪNG
T=4ms:    Coroutine 2: await DB query → TẠM DỪNG
T=5ms:    Coroutine 3: await DB query → TẠM DỪNG

          Event loop: Tất cả 3 DB queries chạy SONG SONG!

T=50ms:   Coroutine 1: DB xong → RESUME → Return response (52ms)
T=51ms:   Coroutine 2: DB xong → RESUME → Return response (53ms)
T=52ms:   Coroutine 3: DB xong → RESUME → Return response (54ms)

Total: ~54ms (parallel) ✅
→ Tất cả requests thành công!
```

---

### 5. Parallel execution với `asyncio.gather()`

Ví dụ với LLM analysis:

```python
async def analyze_conversation_with_llm_async(...):
    # Format conversation (CPU-bound → thread pool)
    formatted = await asyncio.to_thread(format_conversation_for_llm, ...)
    
    # Parallel execution: 3 tasks chạy SONG SONG
    results = await asyncio.gather(
        get_questions(),   # LLM call 1
        get_emotion(),     # LLM call 2  
        get_memories(),    # Memory API call
        return_exceptions=True
    )
    return results
```

Timeline:

```
T=0ms:    Bắt đầu analysis
T=10ms:   Format conversation xong (thread pool)
T=11ms:   Gọi asyncio.gather() → 3 tasks SONG SONG:

          Task 1 (LLM questions):   await → TẠM DỪNG (đợi LLM API)
          Task 2 (LLM emotion):     await → TẠM DỪNG (đợi LLM API)
          Task 3 (Memory API):      await → TẠM DỪNG (đợi Memory API)

T=12ms:   Event loop: Cả 3 HTTP requests chạy SONG SONG!

T=15000ms: Task 1 xong (LLM questions response)
T=15001ms: Task 2 xong (LLM emotion response)  
T=15002ms: Task 3 xong (Memory API response)

T=15003ms: asyncio.gather() xong → Return results

Total: ~15s (parallel)
→ Thay vì 45s nếu chạy tuần tự (15s + 15s + 15s) ✅
```

---

### 6. Fire-and-forget với `asyncio.create_task()`

```python
# STEP 2: Fire-and-forget RabbitMQ
asyncio.create_task(
    publish_conversation_event(...)  # Chạy background, không đợi
)
# ← KHÔNG có await → API return ngay!
```

Timeline:

```
T=0ms:    await service.create_event_async(request) → DB save xong
T=50ms:   asyncio.create_task(publish_conversation_event(...))
          ↓
          Tạo background task → KHÔNG đợi
          ↓
          Return response ngay (202 Accepted)
          
T=51ms:   Response đã gửi về client ✅

          (Background task vẫn chạy):
T=100ms:  RabbitMQ publish xong (background)
```

Lợi ích:
- API response nhanh (< 50ms)
- RabbitMQ publish chạy background
- Không block event loop

---

## Tóm tắt

### Khi chuyển sang async:

1. Event loop quản lý tất cả coroutines
2. `await` = tạm dừng coroutine, chuyển sang coroutine khác
3. I/O operations chạy song song (không chờ tuần tự)
4. Event loop không bị block → xử lý nhiều requests cùng lúc
5. `asyncio.gather()` = chạy nhiều tasks song song
6. `asyncio.create_task()` = fire-and-forget (background)

### Kết quả:

| Metric | Blocking (Sync) | Non-blocking (Async) | Improvement |
|--------|------------------|----------------------|-------------|
| **Response Time** | 2000ms | 50ms | **40x faster** |
| **Concurrent Requests** | 1 tại một thời điểm | 100+ cùng lúc | **100x better** |
| **Throughput** | 0.5 req/s | 2000+ req/s | **4000x better** |
| **Timeout Rate** | 70% | <1% | **99% better** |

FastAPI với async/await giúp xử lý nhiều requests đồng thời, không bị block, và tăng đáng kể throughput.



---

# Phân biệt thread - worker - pod

Trong hệ Uvicorn/Gunicorn chạy trên Kubernetes, có thể xếp các “tầng” như sau: **pod → container/app → worker → thread**; ngoài ra còn có worker class, concurrency, replicas, autoscaling.gunicorn+3​

## Thread

- **Thread**: luồng thực thi bên trong **một process**, các thread cùng process share chung memory.github+1​
    
- Gunicorn: `--threads` = số thread **trong mỗi worker process** (chỉ dùng với worker class kiểu `gthread`).guidebook.devops.uis.cam+2​
    

## Worker

- **Worker**: thường là **process** do server tạo ra để xử lý request (Gunicorn worker, Uvicorn worker).guide.biznetgio+2​
    
- Ví dụ: `gunicorn app:app --workers 4 --threads 2` ⇒ 1 process master + 4 worker processes, mỗi worker có 2 threads xử lý request.stackoverflow+2​
    

## Pod

- **Pod** (Kubernetes): đơn vị deploy nhỏ nhất, bọc 1 hoặc vài container cùng network/storage.kubernetes+2​
    
- Thường 1 pod = 1 container chạy Gunicorn/Uvicorn, bên trong container có nhiều worker, mỗi worker có thể có nhiều thread.uvicorn+2​
    

## Các khái niệm nữa nên biết

- **Worker class / worker type** (Gunicorn): `sync`, `gthread`, `gevent`, `uvicorn.workers.UvicornWorker`… quyết định model concurrency (blocking vs async).gunicorn+2​
    
- **Concurrency**: mức song song thực tế = `pods × containers/pod × workers/container × threads/worker × (yếu tố async)`.dev+2​
    
- **Replicas** (K8s): số **pod replicas** của một Deployment (`spec.replicas`), dùng để scale ngang.kubernetes+2​
    
- **Autoscaling**:
    
    - HPA: tự tăng/giảm **số pod** dựa trên metrics.spectrocloud+2​
        
    - VPA: tự chỉnh **CPU/RAM request/limit** cho pod.codefresh+1​
        

Nếu bạn gửi cụ thể: `replicas`, `workers`, `threads`, resource (CPU/RAM) hiện đang dùng, có thể gợi ý luôn cấu hình tối ưu để test với Locust theo từng mục tiêu (throughput, latency, cost).

1. [https://docs.gunicorn.org/en/latest/design.html](https://docs.gunicorn.org/en/latest/design.html)
2. [https://www.uvicorn.org/deployment/](https://www.uvicorn.org/deployment/)
3. [https://kubernetes.io/docs/concepts/workloads/pods/](https://kubernetes.io/docs/concepts/workloads/pods/)
4. [https://guidebook.devops.uis.cam.ac.uk/reference/notes/gunicorn-tuning/](https://guidebook.devops.uis.cam.ac.uk/reference/notes/gunicorn-tuning/)
5. [https://github.com/benoitc/gunicorn/issues/1045](https://github.com/benoitc/gunicorn/issues/1045)
6. [https://stackoverflow.com/questions/77333340/gunicorn-behavior-with-worker-and-thread-configuration](https://stackoverflow.com/questions/77333340/gunicorn-behavior-with-worker-and-thread-configuration)
7. [https://docs.gunicorn.org/en/stable/settings.html](https://docs.gunicorn.org/en/stable/settings.html)
8. [https://guide.biznetgio.dev/guide/gunicorn/](https://guide.biznetgio.dev/guide/gunicorn/)
9. [https://fastapi.tiangolo.com/deployment/server-workers/](https://fastapi.tiangolo.com/deployment/server-workers/)
10. [https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads](https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads)
11. [https://www.sysdig.com/learn-cloud-native/what-is-a-kubernetes-pod](https://www.sysdig.com/learn-cloud-native/what-is-a-kubernetes-pod)
12. [https://www.mirantis.com/cloud-native-concepts/getting-started-with-kubernetes/what-are-kubernetes-pods/](https://www.mirantis.com/cloud-native-concepts/getting-started-with-kubernetes/what-are-kubernetes-pods/)
13. [https://www.plural.sh/blog/kubernetes-pod/](https://www.plural.sh/blog/kubernetes-pod/)
14. [https://www.redhat.com/en/topics/containers/what-is-kubernetes-pod](https://www.redhat.com/en/topics/containers/what-is-kubernetes-pod)
15. [https://dev.to/lsena/gunicorn-worker-types-how-to-choose-the-right-one-4n2c](https://dev.to/lsena/gunicorn-worker-types-how-to-choose-the-right-one-4n2c)
16. [https://devcenter.heroku.com/articles/python-concurrency](https://devcenter.heroku.com/articles/python-concurrency)
17. [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
18. [https://last9.io/blog/how-replicas-work-in-kubernetes/](https://last9.io/blog/how-replicas-work-in-kubernetes/)
19. [https://www.apptio.com/topics/kubernetes/autoscaling/horizontal/](https://www.apptio.com/topics/kubernetes/autoscaling/horizontal/)
20. [https://www.spectrocloud.com/blog/kubernetes-autoscaling-patterns-hpa-vpa-and-keda](https://www.spectrocloud.com/blog/kubernetes-autoscaling-patterns-hpa-vpa-and-keda)
21. [https://spacelift.io/blog/kubernetes-hpa-horizontal-pod-autoscaler](https://spacelift.io/blog/kubernetes-hpa-horizontal-pod-autoscaler)
22. [https://www.devzero.io/blog/kubernetes-hpa](https://www.devzero.io/blog/kubernetes-hpa)
23. [https://codefresh.io/learn/kubernetes-management/5-types-of-kubernetes-autoscaling-pros-cons-advanced-methods/](https://codefresh.io/learn/kubernetes-management/5-types-of-kubernetes-autoscaling-pros-cons-advanced-methods/)
24. [http://localhost:8089/](http://localhost:8089/)

1. [https://github.com/benoitc/gunicorn/issues/1045](https://github.com/benoitc/gunicorn/issues/1045)
2. [https://docs.gunicorn.org/en/stable/settings.html](https://docs.gunicorn.org/en/stable/settings.html)
3. [https://kubernetes.io/docs/concepts/workloads/pods/](https://kubernetes.io/docs/concepts/workloads/pods/)
4. [https://stackoverflow.com/questions/77333340/gunicorn-behavior-with-worker-and-thread-configuration](https://stackoverflow.com/questions/77333340/gunicorn-behavior-with-worker-and-thread-configuration)
5. [https://guidebook.devops.uis.cam.ac.uk/reference/notes/gunicorn-tuning/](https://guidebook.devops.uis.cam.ac.uk/reference/notes/gunicorn-tuning/)
6. [https://docs.gunicorn.org/en/latest/design.html](https://docs.gunicorn.org/en/latest/design.html)
7. [https://guide.biznetgio.dev/guide/gunicorn/](https://guide.biznetgio.dev/guide/gunicorn/)
8. [https://www.plural.sh/blog/kubernetes-pod/](https://www.plural.sh/blog/kubernetes-pod/)
9. [https://www.mirantis.com/cloud-native-concepts/getting-started-with-kubernetes/what-are-kubernetes-pods/](https://www.mirantis.com/cloud-native-concepts/getting-started-with-kubernetes/what-are-kubernetes-pods/)
10. [https://www.sysdig.com/learn-cloud-native/what-is-a-kubernetes-pod](https://www.sysdig.com/learn-cloud-native/what-is-a-kubernetes-pod)
11. [https://www.redhat.com/en/topics/containers/what-is-kubernetes-pod](https://www.redhat.com/en/topics/containers/what-is-kubernetes-pod)
12. [https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/](https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/)
13. [https://fastapi.tiangolo.com/deployment/server-workers/](https://fastapi.tiangolo.com/deployment/server-workers/)
14. [http://localhost:8089/](http://localhost:8089/)
15. [https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads](https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads)
16. [https://stackoverflow.com/questions/72374634/how-many-uvicorn-workers-do-i-have-to-have-in-production](https://stackoverflow.com/questions/72374634/how-many-uvicorn-workers-do-i-have-to-have-in-production)
17. [https://dev.to/lsena/gunicorn-worker-types-how-to-choose-the-right-one-4n2c](https://dev.to/lsena/gunicorn-worker-types-how-to-choose-the-right-one-4n2c)
18. [https://stackoverflow.com/questions/72374634/how-many-uvicorn-workers-do-i-have-to-have-in-production/72605405](https://stackoverflow.com/questions/72374634/how-many-uvicorn-workers-do-i-have-to-have-in-production/72605405)
19. [https://azureossd.github.io/2023/01/27/Configuring-Gunicorn-worker-classes-and-other-general-settings/](https://azureossd.github.io/2023/01/27/Configuring-Gunicorn-worker-classes-and-other-general-settings/)
20. [https://github.com/encode/uvicorn/issues/1232](https://github.com/encode/uvicorn/issues/1232)
21. [https://www.reddit.com/r/django/comments/11ddkag/gunicorn_only_1_simultaneous_connection_per_worker/](https://www.reddit.com/r/django/comments/11ddkag/gunicorn_only_1_simultaneous_connection_per_worker/)


----


```
tức là CPU bound thì dùng thread pool

tức là I/O bound thì dùng async
```

- CPU-bound → Thread Pool (asyncio.to_thread())

- I/O-bound → Async (await với async library)

---
Đúng. Đây là quy tắc cơ bản:

## Quy tắc: CPU-bound vs I/O-bound

### CPU-bound → Thread Pool
```python
# ❌ SAI: Block event loop
async def process_data():
    result = heavy_calculation()  # Block 500ms!
    return result

# ✅ ĐÚNG: Thread pool
async def process_data():
    result = await asyncio.to_thread(heavy_calculation)
    return result
```

Lý do:
- Python async không tăng tốc CPU-bound
- Event loop bị block nếu chạy trực tiếp
- Thread pool chạy trong thread riêng, event loop tiếp tục

### I/O-bound → Async
```python
# ❌ SAI: Block event loop
async def fetch_data():
    response = httpx.get("http://api.com")  # Block 1s!
    return response

# ✅ ĐÚNG: Async
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://api.com")
    return response
```

Lý do:
- I/O-bound chờ network/disk
- Async cho phép chờ mà không block event loop
- Nhiều I/O operations có thể chạy đồng thời

