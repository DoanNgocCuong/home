# Reliability & Resilience — Production Best Practices

> **Domain:** 5.07 | **Group:** RUN | **Lifecycle:** Run Time
> **Last Updated:** 2026-03-13

---

## 1. Overview

Reliability and resilience are the foundation of stable production systems. While **reliability** measures how often a system works correctly (MTBF), **resilience** is the ability to recover from failures gracefully. Modern production systems must handle partial failures, cascading outages, and resource constraints without taking the entire application down.

**Tiếng Việt:** Độ tin cậy (reliability) đo lường tần suất hệ thống hoạt động đúng, trong khi khả năng phục hồi (resilience) là khả năng hệ thống phục hồi từ lỗi một cách dễ dàng.

---

## 2. Core Principles

1. **Fail Fast, Recover Gracefully** — Detect failures immediately, but handle them without cascading
2. **Assume Network Will Fail** — Design for unreliable networks, transient errors, and latency
3. **Degrade Gracefully** — Reduce functionality rather than crash entirely
4. **Budget for Failure** — Error budgets define acceptable failure rates
5. **Automate Recovery** — Manual intervention shouldn't be required for common failures
6. **Plan for the Worst** — Chaos engineering validates resilience assumptions

---

## 3. Best Practices

### 3.1 Circuit Breaker Pattern

**Practice:** Prevent cascading failures by stopping requests to failing services

- **What:** A circuit breaker monitors downstream service health and trips (opens) when failure threshold exceeded
- **Why:** Without it, your service keeps hammering a broken downstream service, wasting resources and timing out
- **How:**
  - **States:** CLOSED (normal) → OPEN (fail fast) → HALF_OPEN (test recovery) → CLOSED
  - **Hystrix** (Java): `@HystrixCommand(fallback = "fallback()")`
  - **Resilience4j** (Java): `@CircuitBreaker(name = "backend")`
  - **Tenacity** (Python): `@circuit.breaker(fail_max=5, reset_timeout=60)`
- **Anti-pattern:** Not having any circuit breaker; letting threads pile up waiting for dead services

**Example (Python with Tenacity):**
```python
from tenacity import circuit_breaker, stop_after_attempt

@circuit_breaker(failure_threshold=5, recovery_timeout=60)
def call_payment_service(order_id):
    return requests.post("https://payment-api/charge", json={"order_id": order_id})
```

---

### 3.2 Retry with Exponential Backoff + Jitter

**Practice:** Recover from transient failures without overwhelming the system

- **What:** Retry failed requests with increasing delays and randomization
- **Why:** Transient failures (network glitches, temp overload) succeed on retry; without jitter, thundering herd occurs
- **How:**
  - **Formula:** `delay = base * (2 ^ attempt) + random(0, jitter)`
  - Start with 100ms base, cap at 30s, add random ±25%
  - Only retry on **idempotent** operations or transient errors
- **Anti-pattern:** Infinite retries; retrying non-idempotent operations (POST without idempotency key)

**Example (Python):**
```python
import random
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=1, min=2, max=30))
def fetch_user(user_id):
    return requests.get(f"https://api/users/{user_id}")
```

---

### 3.3 Timeout Strategies

**Practice:** Prevent requests from hanging indefinitely

- **Connection Timeout:** How long to wait for initial connection (default 5-10s)
- **Read Timeout:** How long to wait for response data (default 30s)
- **Total Timeout:** Cap on entire operation regardless of retries
- **Why:** Hanging requests consume thread pool, causing cascading failures
- **Anti-pattern:** No timeout set; timeout too generous (> 60s on synchronous paths)

**Example:**
```python
# Connection timeout: 5s, Read timeout: 30s
requests.get("https://api/data", timeout=(5, 30))

# Total timeout for entire operation including retries
async with asyncio.timeout(60):  # Python 3.11+
    await fetch_with_retries()
```

---

### 3.4 Fallback Mechanisms

**Practice:** Provide degraded but functional response when primary path fails

- **What:** Return stale data, cached response, or default value instead of error
- **Why:** User experience is better with stale recommendation than "service unavailable"
- **Examples:**
  - Cache recommendations for 24h, serve if service down
  - Return last known user profile from local cache
  - Use ML model fallback instead of real-time service
- **Anti-pattern:** Fallback that returns misleading data; no expiration on fallback

**Example:**
```python
def get_user_recommendations(user_id):
    try:
        return ml_service.predict(user_id)  # Real-time ML service
    except Timeout:
        cached = cache.get(f"recs:{user_id}")
        if cached and cached.age < timedelta(hours=24):
            return cached.value
        return []  # Empty list better than error
```

---

### 3.5 Bulkhead Pattern

**Practice:** Isolate critical resources to prevent total system failure

- **What:** Separate thread pools, connection pools, or services by function
- **Why:** If one feature uses all threads, others can't respond at all
- **How:**
  - Use separate connection pools for payment vs analytics
  - Reserve 30% of API capacity for high-priority endpoints
  - Run batch jobs in separate service/container
- **Anti-pattern:** Single shared resource pool for all operations

**Example (Java with Hystrix):**
```java
@HystrixCommand(threadPoolKey = "payment")
public PaymentResult processPayment(Order order) { ... }

@HystrixCommand(threadPoolKey = "analytics")  // Different pool
public void logAnalytics(Event event) { ... }
```

---

### 3.6 Rate Limiting & Backpressure

**Practice:** Prevent overload by controlling request flow

**Token Bucket Algorithm:**
- Bucket refills at `rate` tokens/second, capacity = `max_burst`
- Each request costs 1 token; wait if empty
- **Use:** API quotas, per-user limits

**Leaky Bucket:**
- Requests queue, processed at constant `rate`
- Queue overflows if capacity exceeded
- **Use:** Smoothing traffic spikes

**Sliding Window:**
- Count requests in last N seconds
- **Use:** Simple, accurate rate limiting

**Anti-pattern:** No rate limiting; allowing single customer to consume all capacity

**Example (Python Token Bucket):**
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def api_call():
    return requests.get("https://api/endpoint")
```

---

### 3.7 Graceful Degradation

**Practice:** Reduce functionality under load instead of failing

- **Strategies:**
  - Disable personalization during high load (serve generic content)
  - Drop non-critical features (recommendations, analytics)
  - Reduce search result count or quality
  - Serve simplified UI
- **Anti-pattern:** Binary behavior (full features or crash)

---

### 3.8 Health Checks

**Practice:** Continuously verify system health

**Liveness Probe:** Is the service running?
- Simple: HTTP `/health` returns 200
- **Kubernetes:** Kills unresponsive pods

**Readiness Probe:** Can the service handle traffic?
- Checks: Database connection, cache connectivity, downstream dependencies
- **Kubernetes:** Removes unhealthy pods from load balancer

**Anti-pattern:** Liveness probe that depends on database (causes restart cascade)

**Example (Python/Flask):**
```python
@app.get("/health/live")
def liveness():
    return {"status": "alive"}, 200

@app.get("/health/ready")
def readiness():
    if not db.is_connected():
        return {"status": "not_ready"}, 503
    return {"status": "ready"}, 200
```

---

### 3.9 SLA/SLO/SLI Definitions

- **SLA (Service Level Agreement):** Business commitment (99.9% uptime)
- **SLO (Service Level Objective):** Internal target (99.5% uptime)
- **SLI (Service Level Indicator):** Actual measured metric (99.4% uptime)
- **Error Budget:** How much you can fail while still meeting SLO (e.g., 0.5% = 22 min/month)

**Tiếng Việt:** SLA là cam kết với khách, SLO là mục tiêu nội bộ, SLI là chỉ số thực tế

---

### 3.10 Disaster Recovery & Failover

**Practice:** Survive zone/region failures

**RTO (Recovery Time Objective):** Max acceptable downtime (e.g., 1 hour)
**RPO (Recovery Point Objective):** Max acceptable data loss (e.g., 5 minutes)

**Strategies:**
- **Active-Active:** Multiple regions serve traffic, fail transparent
- **Active-Passive:** Standby region activated on primary failure
- **Database Replication:** Async to prevent lag; lag = potential data loss
- **Backup Testing:** Restore from backup monthly to verify it works

---

### 3.11 Chaos Engineering

**Practice:** Proactively test failure scenarios

**Experiments:**
- Kill random pods, verify system stays up
- Introduce 500ms latency, measure impact
- Simulate disk full, database unavailable
- Test under sustained high load

**Tools:** Gremlin, Chaos Mesh, Litmus, Pumba

---

### 3.12 Capacity Planning & Auto-scaling

**Practice:** Right-size infrastructure for demand

- **Vertical:** Bigger machines (hit limits)
- **Horizontal:** More instances (preferred for cloud)
- **Predictive:** Scale before demand hits (based on patterns)
- **Reactive:** Scale in response to load (responds too slowly alone)

**Metrics to Scale On:**
- CPU > 70% → add instances
- Memory > 80% → add instances
- Request latency > threshold → scale
- Queue depth > threshold → scale

---

## 4. Decision Frameworks

**When to use circuit breaker?**
- If downstream service is critical but can fail → use
- If you can tolerate default response → use with fallback

**When to retry?**
- Only for idempotent operations (GET, DELETE with idempotency key)
- Only for transient errors (timeout, 503, connection refused)
- Not for 400/401/403 (client errors won't be fixed by retry)

**How long should timeout be?**
- p99 latency + 10-20% buffer
- For production APIs: 5-30 seconds depending on SLA
- For internal services: tighter (2-5s)

---

## 5. Checklist

- [ ] All downstream service calls have circuit breakers
- [ ] Retries are implemented with exponential backoff + jitter
- [ ] Connection and read timeouts are configured (not default)
- [ ] Fallback mechanisms exist for critical paths
- [ ] Bulkhead isolation configured (separate thread/resource pools)
- [ ] Rate limiting enforced on APIs
- [ ] Graceful degradation strategy documented
- [ ] Health checks (liveness + readiness) implemented
- [ ] SLO and error budget calculated
- [ ] Disaster recovery plan written and tested
- [ ] Chaos engineering experiments run monthly
- [ ] Auto-scaling policies configured and tested
- [ ] Queue-based load leveling for async work
- [ ] OOM prevention: memory limits, overflow handling

---

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| No circuit breaker | Cascading failures | Add circuit breaker to all external calls |
| Retrying non-idempotent ops | Duplicate charges, data corruption | Mark operations idempotent or don't retry |
| Thundering herd on retry | Server overwhelmed more | Add jitter to retry delays |
| Liveness probe too complex | Cascading restarts | Only check process alive, not dependencies |
| Manual failover | Long downtime | Implement automated failover |
| No error budget | Unsafe rapid deploys | Track and respect error budget |
| Timeout too generous | Cascading failures spread | Use p99 latency as baseline |

---

## 7. Tools & References

**Circuit Breaker:** Hystrix, Resilience4j, Tenacity, go-resilience
**Monitoring:** Prometheus, Grafana, Datadog
**Chaos Engineering:** Gremlin, Chaos Mesh, Litmus
**Load Testing:** Locust, k6, JMeter
**Documentation:** Google SRE Book Ch. 2 (Monitoring), Ch. 4 (Service Level Objectives)

---

**Next:** → 5.08 Observability & Monitoring
