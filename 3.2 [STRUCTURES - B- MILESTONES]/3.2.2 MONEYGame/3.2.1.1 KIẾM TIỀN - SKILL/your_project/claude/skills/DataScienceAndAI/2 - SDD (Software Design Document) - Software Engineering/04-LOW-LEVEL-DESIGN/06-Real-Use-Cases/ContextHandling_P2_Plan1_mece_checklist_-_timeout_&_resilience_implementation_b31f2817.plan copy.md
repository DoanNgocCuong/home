---
name: MECE Checklist - Timeout & Resilience Implementation
overview: Tổng hợp checklist MECE các action items cần triển khai để fix timeout/504 crash, được phân loại theo 6 categories không trùng lặp và bao quát toàn bộ hệ thống.
todos: []
---

## PHÂN TÍCH HIỆN TRẠNG (CURRENT STATE ANALYSIS)

### 1. TIMEOUT, FALLBACK, ALERT CHO EXTERNAL SERVICES

#### 1.1 Database (PostgreSQL)

**Status:** ⚠️ PARTIALLY IMPLEMENTED

- ✅ **Connection Pool**: Có `pool_pre_ping`, `pool_recycle`, `pool_timeout=30s` (cần giảm xuống 10s)
- ❌ **Query Timeout**: KHÔNG có `statement_timeout` trong connection string
- ❌ **Pool Monitoring**: KHÔNG có monitoring pool usage trong health check
- ❌ **Alerts**: KHÔNG có alert khi pool exhausted hoặc query timeout
- ✅ **Session Management**: Có `db.close()` trong `finally` block

**Gaps:**

- `DB_POOL_TIMEOUT=30s` quá cao (nên là 10s)
- Thiếu `statement_timeout=10000` trong `connect_args`
- Thiếu pool status monitoring trong health check
- Thiếu Google Chat alerts cho pool exhaustion

#### 1.2 RabbitMQ

**Status:** ⚠️ PARTIALLY IMPLEMENTED

- ❌ **Connection Timeout**: KHÔNG có `socket_timeout` và `blocked_connection_timeout` trong publisher
- ✅ **Health Check Timeout**: Có `socket_timeout=2s` trong health check
- ❌ **Publish Timeout**: KHÔNG có timeout cho `basic_publish()`
- ❌ **Alerts**: KHÔNG có alert khi connection failed hoặc publish failed
- ⚠️ **Fire-and-forget**: `publish_conversation_event()` được `await` (blocking), chưa fire-and-forget

**Gaps:**

- Thiếu `socket_timeout=5` và `blocked_connection_timeout=5` trong `RabbitMQPublisher._connect()`
- `publish_conversation_event()` đang blocking API response
- Thiếu alerts cho connection/publish failures

#### 1.3 LLM (Groq API)

**Status:** ⚠️ PARTIALLY IMPLEMENTED

- ❌ **Call Timeout**: KHÔNG có timeout cho `client.chat.completions.create()` (blocking call)
- ✅ **Circuit Breaker**: Có `@circuit` decorator với `failure_threshold=5`, `recovery_timeout=60`
- ✅ **Fallback Values**: Có fallback (`0` cho questions, `"neutral"` cho emotion)
- ❌ **Exponential Backoff**: KHÔNG có exponential backoff cho rate limit (429)
- ⚠️ **Blocking I/O**: LLM call là **synchronous blocking** trong async function

**Gaps:**

- Thiếu timeout wrapper cho blocking LLM call (nên dùng `ThreadPoolExecutor` với `future.result(timeout=15)`)
- Thiếu exponential backoff (cần `tenacity` library)
- LLM call blocking event loop (nên chuyển sang async hoặc thread pool)

#### 1.4 Memory API (Mem0)

**Status:** ✅ WELL IMPLEMENTED

- ✅ **Timeout**: Có `MEMORY_API_TIMEOUT_SECONDS=600s` (quá cao, nên giảm xuống 60s)
- ✅ **Circuit Breaker**: Có `@circuit` decorator
- ✅ **Fallback**: Có fallback `0` khi error
- ✅ **Error Handling**: Có `httpx.TimeoutException` handling

**Gaps:**

- `MEMORY_API_TIMEOUT_SECONDS=600s` quá cao (nên là 60s)

#### 1.5 Redis

**Status:** ✅ WELL IMPLEMENTED

- ✅ **Connection Timeout**: Có `socket_connect_timeout=2`, `socket_timeout=2` trong cache manager
- ✅ **Health Check**: Có timeout trong health check
- ⚠️ **Alerts**: KHÔNG có alerts cho Redis failures (nhưng Redis là optional, không critical)

**Gaps:**

- Có thể thêm alerts cho Redis failures (P2 priority)

---

### 2. CPU-BOUND VÀ I/O-BOUND OPERATIONS MANAGEMENT

#### 2.1 CPU-Bound Operations (Blocking Event Loop)

**Status:** ⚠️ NOT PROPERLY MANAGED**CPU-bound operations chạy trong async functions (blocking event loop):**

1. **JSON Parsing** (`json.loads`, `json.dumps`):

- Location: `endpoint_conversation_events.py`, `rabbitmq_consumer.py`, `llm_analysis_utils.py`
- Impact: Blocking event loop khi parse large JSON
- Solution: Nên dùng `asyncio.to_thread()` hoặc `run_in_executor()` cho large JSON

2. **String Formatting** (`format_conversation_for_llm`):

- Location: `llm_analysis_utils.py:409-513`
- Impact: Blocking event loop khi format large conversation logs
- Solution: Nên chạy trong thread pool hoặc optimize algorithm

3. **Conversation Log Transformation**:

- Location: `conversation_event_service.py` (transform_conversation_logs)
- Impact: Blocking event loop khi transform large logs
- Solution: Nên chạy trong thread pool

**Gaps:**

- CPU-bound operations chạy trực tiếp trong async functions → block event loop
- Cần wrap trong `asyncio.to_thread()` hoặc `ThreadPoolExecutor` cho operations > 10ms

#### 2.2 I/O-Bound Operations (Blocking)

**Status:** ⚠️ PARTIALLY MANAGED**Blocking I/O operations:**

1. **LLM Calls** (Groq):

- Location: `llm_analysis_utils.py:287` - `client.chat.completions.create()` (synchronous)
- Impact: Blocking event loop, không có timeout
- Solution: Wrap trong `ThreadPoolExecutor` với timeout, hoặc chuyển sang async HTTP client

2. **RabbitMQ Publisher**:

- Location: `rabbitmq_publisher.py:100` - `pika.BlockingConnection` (synchronous)
- Impact: Blocking event loop khi publish
- Solution: Fire-and-forget với `asyncio.create_task()`, hoặc dùng async pika client

3. **Database Queries** (SQLAlchemy):

- Location: Tất cả repositories sử dụng synchronous SQLAlchemy ORM
- Impact: Blocking event loop (nhưng SQLAlchemy có connection pool, ít vấn đề hơn)
- Solution: Có thể chuyển sang `asyncpg` + `SQLAlchemy async` nếu cần

4. **Memory API**:

- Location: `llm_analysis_utils.py:701` - `httpx.Client` (blocking)
- Impact: Blocking event loop
- Solution: Chuyển sang `httpx.AsyncClient` với `await`

**Gaps:**

- LLM calls là blocking, không có timeout
- RabbitMQ publisher blocking API response
- Memory API dùng blocking `httpx.Client` thay vì `httpx.AsyncClient`

---

### 3. MECE COVERAGE - TOÀN BỘ DỰ ÁN

**Current Categories:**

- ✅ Category A: Application Server Timeout
- ✅ Category B: Database Resilience
- ✅ Category C: External Services Resilience
- ✅ Category D: Fallback & Recovery
- ✅ Category E: Observability & Alerting
- ✅ Category F: Performance Optimization

**Missing Categories:**

- ❌ **Category G: CPU-Bound Operations Management** - Cần thêm để quản lý CPU-bound tasks

**MECE Verification:**

- ✅ **Mutually Exclusive**: Mỗi category không trùng lặp
- ⚠️ **Collectively Exhaustive**: Thiếu Category G cho CPU-bound operations

---

### 4. FOLLOW PRODUCTION RISK HANDBOOK

#### 4.1 So sánh với P0_ContextHandling_Risk.md:

**Missing P0 Items:**

- ❌ A1: Uvicorn timeout-keep-alive (Dockerfile line 39)
- ❌ B1: DB_POOL_TIMEOUT = 10s (hiện tại 30s)
- ❌ B2: DB query statement_timeout
- ❌ C1: RabbitMQ connection timeout
- ❌ C2: RabbitMQ fire-and-forget

**Missing P1 Items:**

- ❌ C3: LLM call timeout
- ❌ D1: LLM exponential backoff
- ❌ B3: Monitor DB pool usage
- ❌ E1: Google Chat alerts
- ❌ E2: Response time metrics

#### 4.2 So sánh với P1_ContextHandling_ProductionRiskHandbook.md:

**Missing Requirements:**

- ❌ **Timeout Everywhere**: Thiếu timeout ở nhiều layers
- ❌ **Circuit Breaker + Exponential Backoff**: Có circuit breaker nhưng thiếu exponential backoff
- ❌ **Alerting**: Thiếu alerts cho P0 events (DB pool, RabbitMQ failures)
- ❌ **Tracing**: Langfuse có nhưng chưa verify hoạt động
- ❌ **CPU-Bound Management**: Không có strategy cho CPU-bound operations

---

## TỔNG KẾT GAPS

### Critical Gaps (P0):

1. ❌ Uvicorn timeout-keep-alive chưa config
2. ❌ DB_POOL_TIMEOUT=30s (quá cao)
3. ❌ DB statement_timeout chưa có
4. ❌ RabbitMQ connection timeout chưa có
5. ❌ RabbitMQ publish đang blocking (chưa fire-and-forget)
6. ❌ LLM call không có timeout (blocking vô hạn)

### High Priority Gaps (P1):

1. ❌ LLM exponential backoff chưa có
2. ❌ DB pool monitoring chưa có
3. ❌ Google Chat alerts cho P0 events chưa có
4. ❌ Response time metrics chưa có
5. ❌ CPU-bound operations chưa được quản lý (blocking event loop)

### Medium Priority Gaps (P2):

1. ⚠️ Memory API timeout=600s (quá cao, nên giảm xuống 60s)
2. ⚠️ Langfuse chưa disable nếu không dùng
3. ⚠️ DB queries optimization chưa có
4. ⚠️ DB indexes chưa có

---

# ME

CE CHECKLIST: TIMEOUT & RESILIENCE IMPLEMENTATION

## PHÂN LOẠI MECE

Checklist được phân loại theo **5 categories** đảm bảo **Mutually Exclusive** (không trùng lặp) và **Collectively Exhaustive** (bao quát toàn bộ):

- **Category A: Application Server Timeout** - Uvicorn/Docker configuration
- **Category B: Database Resilience** - Connection pool, query timeout, monitoring
- **Category C: External Services Resilience** - RabbitMQ, LLM timeout & retry
- **Category D: Fallback & Recovery** - Circuit breaker, exponential backoff, default values
- **Category E: Observability & Alerting** - Monitoring, tracing, alerts

---

## CATEGORY A: APPLICATION SERVER TIMEOUT (P0)

### A1: Configure Uvicorn timeout-keep-alive

**Priority:** P0 (Critical)**File:** `src/Dockerfile` (line 39)**Status:** Not implemented**Implementation:**

```dockerfile
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \
     "--timeout-graceful-shutdown", "10", \
     "--no-reload"]
```

**Verification:**

- Test: Kill client connection → Server tự đóng connection sau 55s
- Log: `"Connection timeout after 55s"`

**Dependencies:** None---

### A2: Configure Application-level timeout (if using Gunicorn)

**Priority:** P1 (High)**File:** `src/Dockerfile` (alternative)**Status:** Not implemented (optional)**Implementation:**

```dockerfile
CMD ["gunicorn", "app.main_app:app", \
     "--bind", "0.0.0.0:30020", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--timeout", "55", \
     "--graceful-timeout", "10"]
```

**Verification:**

- Test: Worker timeout after 55s
- Monitor: Worker count stable

**Dependencies:** None (alternative to A1)---

## CATEGORY B: DATABASE RESILIENCE (P0)

### B1: Reduce DB_POOL_TIMEOUT from 30s to 10s

**Priority:** P0 (Critical)**File:** `src/app/core/config_settings.py` (line 58) hoặc `src/.env`**Status:** Not implemented**Implementation:**

```python
# config_settings.py
DB_POOL_TIMEOUT: int = 10  # Change from 30 to 10
```

**Verification:**

- Test: Pool exhausted → Request fail after 10s (not 30s)
- Log: `"Connection pool exhausted, timeout after 10s"`

**Dependencies:** None---

### B2: Add DB query statement_timeout

**Priority:** P0 (Critical)**File:** `src/app/db/database_connection.py` (line 19-27)**Status:** Not implemented**Implementation:**

```python
engine = create_engine(
    settings.DATABASE_URL,
    # ... existing config ...
    connect_args={
        "options": "-c statement_timeout=10000"  # 10s query timeout
    }
)
```

**Verification:**

- Test: Query > 10s → Auto cancel
- Log: `"Query timeout after 10s"`

**Dependencies:** None---

### B3: Monitor DB connection pool usage

**Priority:** P1 (High)**File:** `src/app/services/health_check_service.py` (line 26-50)**Status:** Not implemented**Implementation:**

```python
def check_database(self) -> str:
    # ... existing code ...
    pool = db.bind.pool
    pool_size = pool.size()
    checked_out = pool.checkedout()
    overflow = pool.overflow()
    
    if checked_out + overflow > (pool_size * 0.8):
        logger.warning(f"DB pool nearly exhausted: {checked_out + overflow}/{pool_size + pool._max_overflow}")
```

**Verification:**

- Health check logs pool status
- Alert when pool > 80% capacity

**Dependencies:** None---

## CATEGORY C: EXTERNAL SERVICES RESILIENCE (P0)

### C1: Add RabbitMQ connection timeout

**Priority:** P0 (Critical)**File:** `src/app/background/rabbitmq_publisher.py` (line 100-108)**Status:** Not implemented**Implementation:**

```python
self.connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        # ... existing config ...
        socket_timeout=5,  # 5s socket timeout
        blocked_connection_timeout=5,  # 5s blocked timeout
    )
)
```

**Verification:**

- Test: RabbitMQ down → Connection fail after ~5s (not hang)
- Log: `"Failed to connect to RabbitMQ: timeout after 5s"`

**Dependencies:** None---

### C2: Make RabbitMQ publish fire-and-forget

**Priority:** P0 (Critical)**File:** `src/app/api/v1/endpoints/endpoint_conversation_events.py` (line 79-99)**Status:** Not implemented**Implementation:**

```python
# Change from await to fire-and-forget
asyncio.create_task(
    publish_conversation_event(...)
)
```

**Verification:**

- Test: API `/conversations/end` returns 202 immediately (< 100ms) even if RabbitMQ down
- RabbitMQ publish runs in background

**Dependencies:** None---

### C3: Add LLM call timeout

**Priority:** P1 (High)**File:** `src/app/services/utils/llm_analysis_utils.py` (line 287-298)**Status:** Not implemented**Implementation:**

```python
from concurrent.futures import ThreadPoolExecutor

llm_timeout = getattr(settings, 'LLM_API_TIMEOUT_SECONDS', 15)
with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(self.client.chat.completions.create, ...)
    response = future.result(timeout=llm_timeout)
```

**Verification:**

- Test: LLM call > 15s → Timeout exception
- Log: `"LLM call timeout after 15s"`

**Dependencies:** None---

## CATEGORY D: FALLBACK & RECOVERY (P1)

### D1: Add exponential backoff for LLM rate limit

**Priority:** P1 (High)**File:** `src/app/services/utils/llm_analysis_utils.py` (line 206-210)**Status:** Not implemented (tenacity library not installed)**Implementation:**

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s...
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
@circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
def _invoke_llm(self, ...):
    # ... existing code ...
```

**Verification:**

- Test: Rate limit 429 → Retry with backoff 2s, 4s, 8s
- Log: `"Retrying LLM call after 2s (attempt 1/3)"`

**Dependencies:**

- Install `tenacity` package: `pip install tenacity` or add to `pyproject.toml`

---

### D2: Ensure fallback values for LLM calls

**Priority:** P1 (High)**File:** `src/app/services/utils/llm_analysis_utils.py`**Status:** Partially implemented (has fallback, but need to verify)**Implementation:**

- Verify existing fallback logic:
- `analyze_user_questions()` → returns `0` on error
- `analyze_session_emotion()` → returns `"neutral"` on error

**Verification:**

- Test: LLM timeout → Returns default value (0 or "neutral")
- No exception propagated to caller

**Dependencies:** None (verify existing code)---

### D3: Verify Circuit Breaker is working

**Priority:** P1 (High)**File:** `src/app/services/utils/llm_analysis_utils.py` (line 206-210)**Status:** Implemented (need to verify)**Verification:**

- Test: 5 consecutive LLM failures → Circuit opens → Fallback to default
- Log: `"Circuit breaker opened, using fallback value"`

**Dependencies:** None (verify existing code)---

## CATEGORY E: OBSERVABILITY & ALERTING (P1)

### E1: Setup Google Chat alerts for P0 events

**Priority:** P1 (High)**File:** `src/app/utils/alerts/alert_manager.py`, `src/app/db/database_connection.py`, `src/app/background/rabbitmq_publisher.py`**Status:** Partially implemented (alert_manager exists, need to integrate)**Implementation:**

```python
# In database_connection.py or health_check_service.py
from app.utils.alerts.alert_manager import get_alert_manager

if checked_out + overflow > (pool_size * 0.8):
    alert_manager = get_alert_manager()
    alert_manager.send_alert_fire_and_forget(
        alert_type=AlertType.SYSTEM_ERROR,
        level=AlertLevel.CRITICAL,
        message="Database connection pool exhausted",
        context={"pool_size": pool_size, "checked_out": checked_out}
    )
```

**Verification:**

- Test: DB pool exhausted → Google Chat alert sent
- Test: RabbitMQ down → Google Chat alert sent

**Dependencies:**

- Verify `GOOGLE_CHAT_WEBHOOK_URL` is configured in `.env`

---

### E2: Add response time metrics

**Priority:** P1 (High)**File:** `src/app/main_app.py` (line 66-97)**Status:** Not implemented**Implementation:**

```python
from prometheus_client import Histogram, Counter

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'path', 'status']
)

# In RequestLoggingMiddleware.dispatch():
request_duration.labels(method=method, path=path, status=response.status_code).observe(process_time)

if process_time > 5.0:
    logger.warning(f"Slow request: {method} {path} took {process_time:.2f}s")
```

**Verification:**

- Test: Metrics endpoint `/metrics` shows request duration
- Alert when response time > 5s

**Dependencies:**

- Install `prometheus-client`: `pip install prometheus-client` or add to `pyproject.toml`

---

### E3: Setup distributed tracing (Langfuse/OpenTelemetry)

**Priority:** P1 (High)**File:** `src/app/main_app.py`, `src/app/services/utils/llm_analysis_utils.py`**Status:** Partially implemented (Langfuse decorators exist, need to verify)**Verification:**

- Test: Trace shows exact I/O call that caused timeout
- Can see full request lifecycle from API → DB → LLM → Response

**Dependencies:**

- Verify `LANGFUSE_ENABLED`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` are configured

---

### E4: Disable Langfuse if not using

**Priority:** P2 (Medium)**File:** `src/.env`**Status:** Not implemented**Implementation:**

```bash
LANGFUSE_ENABLED=false
```

**Verification:**

- No log: `"Langfuse client initialized without public_key"`
- Reduced log noise

**Dependencies:** None---

## CATEGORY F: PERFORMANCE OPTIMIZATION (P2)

### F1: Optimize DB queries in `/activities/suggest`

**Priority:** P2 (Medium)**File:** `src/app/services/agent_selection/agent_selection_service.py` (line 77-225)**Status:** Not implemented**Implementation:**

- Batch load all prompts in one query instead of multiple queries
- Build lookup dict for O(1) access

**Verification:**

- Reduce DB queries from ~10 to ~2-3
- Response time reduced by 30-50%

**Dependencies:** None---

### F2: Add database indexes for PromptTemplate

**Priority:** P2 (Medium)**File:** Database migration**Status:** Not implemented**Implementation:**

```sql
CREATE INDEX IF NOT EXISTS idx_prompt_template_friendship_level 
ON prompt_template_for_level_friendship(friendship_level);

CREATE INDEX IF NOT EXISTS idx_prompt_template_agent_category 
ON prompt_template_for_level_friendship(agent_category);

CREATE INDEX IF NOT EXISTS idx_prompt_template_topic_id 
ON prompt_template_for_level_friendship(topic_id);

CREATE INDEX IF NOT EXISTS idx_prompt_template_agent_tag 
ON prompt_template_for_level_friendship(agent_tag);
```

**Verification:**

- Query time reduced from ~100ms to ~10ms
- EXPLAIN ANALYZE shows index usage

**Dependencies:** None---

## CATEGORY G: CPU-BOUND OPERATIONS MANAGEMENT (P1)

### G1: Move CPU-bound JSON parsing to thread pool

**Priority:** P1 (High)**File:** `src/app/api/v1/endpoints/endpoint_conversation_events.py`, `src/app/background/rabbitmq_consumer.py`**Status:** Not implemented**Current Issue:**

- `json.loads()` và `json.dumps()` chạy trực tiếp trong async functions
- Blocking event loop khi parse large JSON (> 10KB)

**Implementation:**

```python
import asyncio

# For large JSON parsing
async def parse_large_json(json_str: str) -> dict:
    """Parse large JSON in thread pool to avoid blocking event loop."""
    return await asyncio.to_thread(json.loads, json_str)

# In endpoint_conversation_events.py
conversation_log = await parse_large_json(request.conversation_log) if isinstance(request.conversation_log, str) else request.conversation_log
```

**Verification:**

- Large JSON (> 10KB) parsing không block event loop
- Response time không tăng đáng kể

**Dependencies:** None (asyncio.to_thread available in Python 3.9+)---

### G2: Move conversation formatting to thread pool

**Priority:** P1 (High)**File:** `src/app/services/utils/llm_analysis_utils.py` (line 409-513)**Status:** Not implemented**Current Issue:**

- `format_conversation_for_llm()` chạy trực tiếp trong async context
- Blocking event loop khi format large conversation logs (> 50 messages)

**Implementation:**

```python
import asyncio

async def format_conversation_async(conversation_log: List[Dict[str, Any]]) -> str:
    """Format conversation in thread pool to avoid blocking event loop."""
    return await asyncio.to_thread(format_conversation_for_llm, conversation_log)

# In analyze_conversation_with_llm():
formatted_conversation = await format_conversation_async(conversation_log)
```

**Verification:**

- Large conversation formatting không block event loop
- Response time không tăng đáng kể

**Dependencies:** None---

### G3: Reduce Memory API timeout from 600s to 60s

**Priority:** P2 (Medium)**File:** `src/app/core/config_settings.py` (line 143)**Status:** Not implemented**Current Issue:**

- `MEMORY_API_TIMEOUT_SECONDS=600s` quá cao (10 phút)
- Nên giảm xuống 60s để tránh blocking quá lâu

**Implementation:**

```python
# config_settings.py
MEMORY_API_TIMEOUT_SECONDS: int = 60  # Change from 600 to 60
```

**Verification:**

- Memory API timeout sau 60s (không chờ 10 phút)
- Log: `"Memory API timeout after 60s"`

**Dependencies:** None---

## SUMMARY BY PRIORITY

### P0 (Critical - Fix in 24h):

- [ ] A1: Uvicorn timeout-keep-alive
- [ ] B1: DB_POOL_TIMEOUT = 10s
- [ ] B2: DB query statement_timeout
- [ ] C1: RabbitMQ connection timeout
- [ ] C2: RabbitMQ fire-and-forget

### P1 (High - Fix this week):

- [ ] C3: LLM call timeout
- [ ] D1: LLM exponential backoff
- [ ] D2: Verify LLM fallback values
- [ ] D3: Verify Circuit Breaker
- [ ] B3: Monitor DB pool usage
- [ ] E1: Google Chat alerts
- [ ] E2: Response time metrics
- [ ] E3: Distributed tracing
- [ ] G1: Move CPU-bound JSON parsing to thread pool
- [ ] G2: Move conversation formatting to thread pool

### P2 (Medium - Next sprint):

- [ ] E4: Disable Langfuse
- [ ] F1: Optimize DB queries
- [ ] F2: Add DB indexes
- [ ] G3: Reduce Memory API timeout from 600s to 60s

---

## DEPENDENCIES TO INSTALL

```bash
# Add to pyproject.toml or install directly:
pip install tenacity  # For exponential backoff
pip install prometheus-client  # For metrics
```

---

## VERIFICATION TEST PLAN

1. **RabbitMQ down** → API `/conversations/end` returns 202 immediately (< 100ms)
2. **DB pool exhausted** → Request fails after 10s (not 30s)
3. **LLM timeout** → Request fails after 15s with fallback value
4. **Health check** → Logs pool status and alerts when > 80%
5. **Large JSON parsing** → Does not block event loop (uses thread pool)
6. **Large conversation formatting** → Does not block event loop (uses thread pool)

---

## COMPLIANCE CHECKLIST

### ✅ Đã kiểm tra timeout, fallback, alert cho external services:

- [x] Database (PostgreSQL) - ⚠️ PARTIALLY: Có pool timeout, thiếu statement_timeout, thiếu alerts
- [x] RabbitMQ - ⚠️ PARTIALLY: Có health check timeout, thiếu publisher timeout, thiếu alerts
- [x] LLM (Groq) - ⚠️ PARTIALLY: Có circuit breaker + fallback, thiếu timeout, thiếu exponential backoff
- [x] Memory API (Mem0) - ✅ WELL: Có timeout (quá cao 600s), có circuit breaker + fallback
- [x] Redis - ✅ WELL: Có timeout, optional service

### ✅ Đã kiểm tra CPU-bound và I/O-bound operations:

- [x] CPU-bound: JSON parsing, string formatting - ⚠️ NOT MANAGED (blocking event loop)
- [x] I/O-bound: LLM calls, RabbitMQ publish, Memory API - ⚠️ PARTIALLY MANAGED (blocking, thiếu timeout)

### ✅ Đã MECE toàn bộ dự án:

- [x] Category A: Application Server Timeout
- [x] Category B: Database Resilience
- [x] Category C: External Services Resilience
- [x] Category D: Fallback & Recovery
- [x] Category E: Observability & Alerting