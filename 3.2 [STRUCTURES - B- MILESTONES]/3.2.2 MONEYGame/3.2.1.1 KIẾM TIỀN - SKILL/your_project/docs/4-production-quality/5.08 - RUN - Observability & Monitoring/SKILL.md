# Observability & Monitoring — Production Best Practices

> **Domain:** 5.08 | **Group:** RUN | **Lifecycle:** Run Time
> **Last Updated:** 2026-03-13

---

## 1. Overview

Observability is the ability to understand system behavior from external outputs without knowing internal state. It differs from monitoring (checking against thresholds). **Three pillars** — Logs, Metrics, Traces — give comprehensive visibility into production systems.

**Tiếng Việt:** Khả năng quan sát (observability) cho phép hiểu hành vi hệ thống từ các đầu ra bên ngoài. Ba trụ cột: Logs (nhật ký), Metrics (chỉ số), Traces (dấu vết).

---

## 2. Core Principles

1. **Observability > Monitoring** — Understand *why* not just *if* something failed
2. **Structured Data** — Machine-readable logs enable querying and alerting
3. **Context Propagation** — Trace requests across services via correlation IDs
4. **Cost-Aware** — Observability is expensive; sample strategically
5. **Actionable Alerts** — Alert on symptoms, not raw metrics
6. **Observability-Driven Development** — Instrument as you build

---

## 3. Best Practices

### 3.1 The Three Pillars

**LOGS (Logs):**
- Human-readable record of events
- **Volume:** Highest, most storage
- **Latency:** Can be delayed (batch processing)
- **Use:** Debugging, compliance, audit trail

**METRICS (Chỉ số):**
- Time-series numerical data (counters, gauges, histograms)
- **Volume:** Lowest, compressible
- **Latency:** Real-time, sub-second
- **Use:** Alerting, trending, capacity planning

**TRACES (Dấu vết):**
- Request journey through services
- **Volume:** Medium
- **Latency:** Real-time for high-volume services
- **Use:** Performance debugging, latency analysis, microservice debugging

**Example (User purchases item):**
```
TRACE: request_id=xyz789
├─ Log: "Purchase initiated, user_id=42"
├─ METRIC: order_creation_latency=45ms
├─ SPAN: payment_service (latency=120ms)
│  └─ Log: "Payment authorized"
├─ SPAN: inventory_service (latency=80ms)
│  └─ Log: "Stock decremented"
└─ SPAN: email_service (latency=200ms)
   └─ Log: "Confirmation sent"
```

---

### 3.2 Structured Logging

**Practice:** Make logs queryable and parseable by machines

- **JSON Format:** Every log entry is valid JSON
- **Correlation ID:** Unique ID tracking request across services
- **Severity Level:** ERROR, WARN, INFO, DEBUG
- **Context:** Include user_id, request_id, service_name, version

**Anti-pattern:** Text logs like `"Error at line 42"`; no context; mixing multiple concerns

**Example (Python JSON logging):**
```python
import json
import logging
import uuid

logger = logging.getLogger(__name__)

def process_order(order_id):
    correlation_id = uuid.uuid4()
    logger.info(json.dumps({
        "event": "order_received",
        "order_id": order_id,
        "correlation_id": str(correlation_id),
        "user_id": 42,
        "service": "order-service",
        "version": "1.2.0",
        "timestamp": datetime.utcnow().isoformat()
    }))
```

---

### 3.3 Log Aggregation

**Practice:** Collect logs from all services into central system for querying

**ELK Stack (Elasticsearch, Logstash, Kibana):**
- Industry standard, open-source
- Logstash parses/transforms logs
- Elasticsearch indexes for fast search
- Kibana visualizes, creates dashboards

**Loki (Grafana):**
- Lightweight alternative, lower cost
- Index labels instead of full text
- Integrates with Grafana
- Better for high-volume environments

**Fluentd / Fluent Bit:**
- Agents that forward logs from services
- Fluentd: heavier, more plugins
- Fluent Bit: lightweight edge agent

**Anti-pattern:** Local logs only; trying to SSH into servers to debug

---

### 3.4 Distributed Tracing

**Practice:** Track request across microservices to identify bottlenecks

**OpenTelemetry (OTEL):**
- Vendor-neutral standard for instrumentation
- Supports traces, metrics, logs
- Exporters: Jaeger, Datadog, AWS X-Ray, etc.

**Jaeger:**
- Open-source trace backend
- Visualizes trace waterfall (which service is slow)
- **Example:** Payment service takes 120ms, why?

**Langfuse (for LLM applications):**
- Tracks LLM calls, token counts, latency
- Debugging for chains and agents
- Cost tracking per request

**Trace Context Propagation:**
- HTTP Header: `traceparent: 00-trace_id-span_id-sampled`
- Every service includes header in outbound requests
- Enables correlation across services

**Anti-pattern:** Each service uses different trace ID; losing context between services

**Example (Python with OpenTelemetry):**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

jaeger_exporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("payment_processing"):
    # Call downstream services; spans auto-linked
    payment_result = call_payment_service()
```

---

### 3.5 Metrics Collection

**Practice:** Track system behavior quantitatively in time-series database

**Prometheus:**
- Pull-based (scrapes metrics from `/metrics` endpoint)
- Time-series database optimized for high cardinality
- PromQL query language
- Local storage, good for < 1M metrics/sec

**Grafana:**
- Visualization layer for Prometheus, Elasticsearch, etc.
- Create dashboards, heatmaps, alerts
- Popular with all observability stacks

**Datadog:**
- SaaS alternative, integrated (logs + metrics + traces)
- Higher cost but no ops burden
- Better for enterprises

**Metric Types:**
- **Counter:** Only increases (requests, errors)
- **Gauge:** Can go up/down (CPU, memory)
- **Histogram:** Distribution of values (latency in buckets)
- **Summary:** Like histogram but computed on client

**Anti-pattern:** Too many high-cardinality metrics (user_id in metric name → explosion); metrics without labels

---

### 3.6 Alerting Best Practices

**Practice:** Alert on actionable symptoms, not raw thresholds

**Alert Fatigue:**
- Too many alerts → team ignores all
- Alert only on user-impacting issues
- Use burn rate for error budgets (not raw error count)

**Runbook Links:**
- Every alert includes link to troubleshooting procedure
- Runbook: what does this mean? how to fix?
- Reduces MTTR significantly

**Severity Levels:**
- **Critical:** Page on-call immediately (user impact now)
- **High:** Create ticket, notify on-call next business day
- **Medium:** Create ticket for backlog
- **Low:** Informational only

**Error Budget Alerting:**
- If error rate > SLO * 10%, alert immediately (burn fast)
- Prevents exhausting budget before month end

**Anti-pattern:** Alert on "CPU > 70%" (too common); alert on "disk full" (too late)

**Example (Prometheus alert):**
```yaml
alert: HighErrorRate
expr: rate(requests_failed[5m]) / rate(requests_total[5m]) > 0.01
for: 5m
annotations:
  summary: "High error rate detected"
  runbook_url: "https://wiki/runbooks/high-error-rate"
  severity: "critical"
```

---

### 3.7 SLI/SLO Dashboards

**Practice:** Visualize progress toward SLOs

**Dashboard Should Show:**
- Current SLI (% of requests meeting SLO)
- Error budget remaining (in time, not percentage)
- Burn rate (how fast we're burning budget)
- Trends (are we improving?)

**Example SLO:** 99.5% of requests complete in < 200ms
- **SLI:** Actual % of requests meeting this
- **Error Budget:** 0.5% * 43200 seconds/day = 216 seconds/day ≈ 3.6 minutes/day
- **Current Burn:** If 2% failed today, we've burned 4 days of budget in 1 day

---

### 3.8 Application Performance Monitoring (APM)

**Practice:** Instrument code to measure performance end-to-end

**What to Instrument:**
- Request entry/exit (latency, status)
- Database queries (slow queries detected)
- External API calls (timeout, retry, fallback)
- Cache hits/misses
- Background jobs (duration, failures)

**Tools:** New Relic, DataDog, Elastic APM, Dynatrace

---

### 3.9 Real User Monitoring (RUM)

**Practice:** Measure what actual users experience

**Metrics:**
- **FCP (First Contentful Paint):** First content visible
- **LCP (Largest Contentful Paint):** Main content loaded
- **CLS (Cumulative Layout Shift):** Unexpected layout changes
- **TTFB (Time to First Byte):** Server response time

**Use:** Detect frontend performance regressions, user-impacting issues

---

### 3.10 Synthetic Monitoring

**Practice:** Simulate user interactions to detect issues before customers

- **Uptime Checks:** Ping endpoints from multiple regions
- **Transaction Checks:** Full user flow (login → purchase → logout)
- **Frequency:** Every 1-5 minutes
- **Alerting:** Page if endpoint down

**Tools:** DataDog, UptimeRobot, Checkly, New Relic Synthetics

---

### 3.11 Log Levels (When to Use Each)

- **ERROR:** User-impacting failures (payment failed, data corrupted)
- **WARN:** Unusual but handled (retry after failure, fallback used)
- **INFO:** Normal operations (request received, job completed) - be selective
- **DEBUG:** Development only (variable values, function entry/exit)

**Anti-pattern:** Logging everything at INFO level (noise); logging at DEBUG in production

---

### 3.12 Performance Profiling (p50/p95/p99)

**Practice:** Understand latency distribution, not just average

- **p50 (Median):** 50% of requests faster
- **p95:** 95% faster; common SLO target
- **p99:** 99% faster; tail latency, catches outliers
- **Average:** Misleading (1 sec + 0 sec = 500ms avg, but users see 1s)

**Example:**
```
Response times: [10ms, 15ms, 20ms, 25ms, 1000ms]
Average: 214ms (misleading!)
p50: 15ms
p95: 1000ms (worst 5% of users)
```

---

### 3.13 Anomaly Detection

**Practice:** Alert on unusual patterns, not just thresholds

- **Baseline:** Learn normal behavior (ML models)
- **Deviation:** Alert if metrics deviate > 2 standard deviations
- **Seasonal:** Account for expected patterns (traffic dips at night)
- **Tools:** Datadog, Grafana, Moogsoft

---

### 3.14 Cost of Observability

- **Logs:** 1-5 GB/day per service (expensive storage)
- **Metrics:** ~1 KB per metric per day
- **Traces:** Sample 1-10% (full tracing is expensive)
- **Strategies to reduce cost:**
  - Drop DEBUG logs in production
  - Sample traces (1% for high-volume, 100% for low-volume)
  - Aggregate logs (1-day rollup for old data)
  - Use metric cardinality controls

---

## 4. Decision Frameworks

**When to use each pillar?**

| Scenario | Logs | Metrics | Traces |
|----------|------|---------|--------|
| "Is service up?" | No | Yes (health gauge) | No |
| "Why did payment fail?" | Yes | No | Yes |
| "What's our p99 latency?" | No | Yes | Yes |
| "Which service is slow?" | No | No | Yes |
| "Audit trail for compliance?" | Yes | No | No |

---

## 5. Checklist

- [ ] All logs in structured JSON format
- [ ] Correlation IDs propagated across services
- [ ] Log aggregation (ELK/Loki) deployed and queryable
- [ ] OpenTelemetry instrumented for traces
- [ ] Jaeger or equivalent trace backend operational
- [ ] Prometheus scraping metrics from all services
- [ ] Grafana dashboards created for key metrics
- [ ] SLI/SLO dashboard visible to team
- [ ] Alerting rules defined with runbook links
- [ ] APM tool capturing performance data
- [ ] Synthetic monitoring checks running
- [ ] RUM metrics collected and analyzed
- [ ] Log levels used consistently (ERROR/WARN/INFO/DEBUG)
- [ ] Cost of observability tracked and optimized

---

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Text logs without structure | Unsearchable, can't alert | Use JSON, add context |
| Missing correlation IDs | Can't track request across services | Add/propagate trace ID everywhere |
| No trace sampling | Tracing is 10x more expensive | Sample 1-5% for high-volume |
| Alert on raw CPU% | Constantly alerting on normal spikes | Alert on burn rate or 99th percentile |
| No SLO dashboard | Team doesn't know if within budget | Create and update daily |
| Metrics with user_id labels | Cardinality explosion, Prometheus crashes | Use static labels only (service, version) |
| 1-minute alert evaluation | Flaky alerts, false positives | Use 5-minute window minimum |

---

## 7. Tools & References

**Logs:** ELK, Loki, Splunk, Datadog
**Metrics:** Prometheus, Graphite, InfluxDB, Datadog
**Traces:** Jaeger, Zipkin, DataDog APM, New Relic, Langfuse (LLM)
**APM:** New Relic, Datadog, Elastic APM, Dynatrace
**Synthetic:** Checkly, UptimeRobot, Datadog Synthetics
**Documentation:** Google SRE Book (Ch. 6: Monitoring, Ch. 7: Automation), OTEL Docs

---

**Next:** → 5.09 Error Handling
