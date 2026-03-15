
>Output quá ngon: 
>1. Giúp mình có cái nhìn tổng quan - High Level Desing - Stack Overview
>2. Từng tầng, từng pha, từng steps đều MECE các giải pháp - chỉ ra ngay ưu nhược của từng cái trên ngay High Level Design/Stack Overview


# Production Observability Stack: Tổng quan 6 tầng

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION OBSERVABILITY STACK                            │
│                                                                             │
│  "Không thể fix thứ không nhìn thấy"                                       │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 6: RUNBOOKS & INCIDENT RESPONSE          ← Con người hành động
═══════════════════════════════════════════════════════════════════════════════

  Detect → Diagnose → Fix → Verify → Prevent

  Tools:   Runbook templates (Markdown/Confluence)
           PagerDuty / Opsgenie (on-call rotation)
           Postmortem templates

  Output:  MTTR giảm, không ai phải nhớ trong đầu cách fix

───────────────────────────────────────────────────────────────────────────────


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 5: ALERTING                               ← Máy phát hiện sớm
═══════════════════════════════════════════════════════════════════════════════

  "Phát hiện trước khi user báo"

  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │  Error rate > 5%  │    │  P95 > 10s       │    │  Cost spike 2x   │
  │  trong 5 phút     │    │  trong 5 phút     │    │  so với avg       │
  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   ▼
                          ┌────────────────┐
                          │  Slack / Email  │
                          │  + Runbook link │
                          └────────────────┘

  Tools:   Alertmanager (Prometheus)    ← Open source, best practice
           Grafana Alerting             ← Tích hợp sẵn trong Grafana
           Datadog Monitors             ← SaaS
           PagerDuty                    ← On-call escalation

───────────────────────────────────────────────────────────────────────────────


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 4: METRICS & DASHBOARDS                   ← Đo lường liên tục
═══════════════════════════════════════════════════════════════════════════════

  "Team mở dashboard lên là biết hệ thống healthy hay không"

  ┌─────────────────────────────────────────────────────────────────────┐
  │                        Dashboard                                    │
  │                                                                     │
  │  RED Metrics (mỗi service):                                        │
  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐              │
  │  │   Rate    │  │  Errors   │  │    Duration        │              │
  │  │  req/sec  │  │  error %  │  │  p50, p95, p99     │              │
  │  └───────────┘  └───────────┘  └───────────────────┘              │
  │                                                                     │
  │  LLM Metrics:           Business Metrics:                          │
  │  - tokens/request       - lessons/day                              │
  │  - cost/request         - success rate                             │
  │  - model latency        - avg generation time                      │
  └─────────────────────────────────────────────────────────────────────┘

  Tools:   Grafana + Prometheus + Mimir  ← Open source, best practice
           Datadog Dashboards            ← SaaS
           Kibana (ELK)                  ← Nếu đã có ELK

───────────────────────────────────────────────────────────────────────────────


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 3: DISTRIBUTED TRACING                    ← Request đi qua đâu?
═══════════════════════════════════════════════════════════════════════════════

  "Request đi qua 5 services, bottleneck ở đâu?"

  User Request
    │
    ▼
  ┌──────┐ 120ms  ┌──────────────┐ 45ms  ┌─────────┐ 2100ms  ┌─────┐
  │ API  │───────▶│ Orchestration │──────▶│ LLM Call │────────▶│ TTS │
  └──────┘        └──────────────┘        └─────────┘         └─────┘
                         │                     ▲
                         │ 30ms                │ ← Bottleneck!
                         ▼                     │
                  ┌──────────────┐             │
                  │   Emotion    │─────────────┘
                  │   Service    │
                  └──────────────┘

  trace_id: abc-123  (propagate qua HTTP header xuyên tất cả services)

  ┌─────────────────────────────────────────────────────────────────────┐
  │  Infrastructure Tracing        │  LLM Tracing                      │
  │  (latency, errors, throughput) │  (input/output, tokens, cost)     │
  │                                │                                    │
  │  Tools:                        │  Tools:                           │
  │  - Jaeger         (OSS)        │  - Langfuse        (OSS)         │
  │  - Grafana Tempo  (OSS)        │  - LangSmith       (SaaS)        │
  │  - Zipkin         (OSS)        │  - Helicone        (SaaS)        │
  │  - Datadog APM    (SaaS)       │                                   │
  └─────────────────────────────────────────────────────────────────────┘

  Standard:  OpenTelemetry (OTEL) ← vendor-neutral, mọi tool đều support

───────────────────────────────────────────────────────────────────────────────


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 2: LOG AGGREGATION                        ← Thu thập về 1 nơi
═══════════════════════════════════════════════════════════════════════════════

  "Search logs không cần SSH vào server"

  Service A ──┐
  Service B ──┼──▶  [Collector]  ──▶  [Storage + Index]  ──▶  [Query UI]
  Service C ──┤
  Service D ──┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  Option 1: Grafana Loki                    ★ RECOMMENDED           │
  │  ┌──────────┐   ┌──────┐   ┌─────────┐                            │
  │  │  Alloy/  │──▶│ Loki │──▶│ Grafana │  Resource: Thấp            │
  │  │ Promtail │   └──────┘   └─────────┘  Search: Labels (LogQL)    │
  │  └──────────┘                            Best for: K8s, startup    │
  │                                                                     │
  │  Option 2: ELK Stack                                               │
  │  ┌──────────┐   ┌───────────────┐   ┌────────┐                    │
  │  │ Filebeat/│──▶│ Elasticsearch │──▶│ Kibana │  Resource: Cao     │
  │  │ Logstash │   └───────────────┘   └────────┘  Search: Full-text │
  │  └──────────┘                                    Best for: Fintech │
  │                                                                     │
  │  Option 3: SigNoz                      (All-in-one)                │
  │  ┌──────────┐   ┌──────────────────────────────┐                   │
  │  │  OTEL   │──▶│ SigNoz (Logs+Traces+Metrics) │  Resource: TB     │
  │  │Collector│   └──────────────────────────────┘  Search: SQL      │
  │  └──────────┘                                    Best for: Thay DD │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘

───────────────────────────────────────────────────────────────────────────────


═══════════════════════════════════════════════════════════════════════════════
 TẦNG 1: STRUCTURED LOGGING                     ← Foundation (bắt buộc)
═══════════════════════════════════════════════════════════════════════════════

  "Log phải machine-readable, không phải chỉ human-readable"

  ❌ print("API call success, model=gpt-4, duration=450ms")
  ❌ logger.info("API call success, model=gpt-4, duration=450ms")
  ✅ logger.info("api.request.success", model="gpt-4", duration_ms=450)

  Output:
  {"event":"api.request.success","model":"gpt-4","duration_ms":450,"level":"info","timestamp":"..."}

  ┌─────────────────────────────────────────────────────────────────────┐
  │  Tool            │ Đặc điểm                  │ Khi nào dùng        │
  │──────────────────┼────────────────────────────┼─────────────────────│
  │  structlog       │ Kwargs trực tiếp, bind()   │ FastAPI, new project│
  │  std logging     │ extra={}, zero dependency  │ Project đang chạy   │
  │  loguru          │ Zero config, pretty output │ Script, CLI, proto  │
  └─────────────────────────────────────────────────────────────────────┘

  Quy tắc:
  - JSON format bắt buộc trong production
  - Event naming: dot.separated (api.request.success)
  - Có request_id xuyên suốt request lifecycle
  - Numeric fields phải là số (duration_ms: 6, không phải "6")


═══════════════════════════════════════════════════════════════════════════════


┌─────────────────────────────────────────────────────────────────────────────┐
│                     BEST PRACTICE STACK COMBINATIONS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ★ Open Source (Self-hosted) — "LGTM Stack"                                │
│  ┌─────────┬──────────────┬──────────────┬───────────────┬──────────────┐  │
│  │ Logging │ Log Aggreg.  │   Tracing    │   Metrics     │  Alerting    │  │
│  │structlog│ Loki+Alloy   │ Tempo+Jaeger │ Prometheus    │ Alertmanager │  │
│  │         │              │ +Langfuse    │ +Mimir        │              │  │
│  └─────────┴──────────────┴──────────────┴───────────────┴──────────────┘  │
│  Visualize: Grafana (tất cả trong 1 UI)                                    │
│  Ưu: Free, full control, K8s native                                        │
│  Nhược: Phải tự maintain                                                   │
│                                                                             │
│  ★ Open Source All-in-One                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  SigNoz (Logs + Traces + Metrics trong 1 platform)                  │  │
│  │  + Langfuse (LLM-specific tracing)                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  Ưu: Ít component, OpenTelemetry native                                    │
│  Nhược: Community nhỏ hơn Grafana ecosystem                                │
│                                                                             │
│  ★ SaaS (Managed)                                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Datadog (Logs + APM + Metrics + Alerting)                          │  │
│  │  + Langfuse (LLM tracing)                                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  Ưu: Zero ops, scale tự động                                               │
│  Nhược: Tốn tiền, vendor lock-in                                           │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TRIỂN KHAI THEO THỨ TỰ (mỗi tầng build trên tầng trước):                 │
│                                                                             │
│  Tầng 1  →  Tầng 2  →  Tầng 3  →  Tầng 4  →  Tầng 5  →  Tầng 6          │
│  Logging    Aggreg.    Tracing    Metrics    Alerting    Runbooks          │
│  (1 ngày)   (1-2 ngày) (2-3 ngày) (1-2 ngày) (1 ngày)   (ongoing)        │
│                                                                             │
│  Tổng: ~2-3 tuần cho full production observability stack                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# Production Observability & Monitoring: Best Practices toàn diện

> **Mục đích:** Tài liệu này trả lời câu hỏi "thực sự cần làm gì" cho từng tầng observability — không chỉ liệt kê tools mà đi vào practices, patterns, và anti-patterns cụ thể.

---

## Bức tranh tổng thể

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Tầng 6: RUNBOOKS & INCIDENT RESPONSE    "Con người biết phải làm gì" │
│   Tầng 5: ALERTING                        "Máy phát hiện sớm"          │
│   Tầng 4: METRICS & DASHBOARDS            "Đo lường liên tục"          │
│   Tầng 3: DISTRIBUTED TRACING             "Request đi qua đâu?"        │
│   Tầng 2: LOG AGGREGATION                 "Thu thập về 1 nơi"          │
│   Tầng 1: STRUCTURED LOGGING              "Foundation — bắt buộc"      │
│                                                                         │
│   Mỗi tầng BUILD trên tầng trước. Không skip.                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tầng 1: Structured Logging

### Mục đích

Log phải machine-readable, không chỉ human-readable. Đây là foundation — nếu log sai, mọi tầng trên đều vô nghĩa.

### Best Practices

**Format:** JSON bắt buộc trong production. Mọi field phải parse được.

```
❌  logger.info("API call success, model=gpt-4, duration=450ms")
✅  logger.info("api.request.success", model="gpt-4", duration_ms=450)
```

**Output:**

```json
{"event": "api.request.success", "model": "gpt-4", "duration_ms": 450, "level": "info", "timestamp": "2026-03-09T10:23:45.123Z"}
```

**Event naming:** Dùng `dot.separated.lowercase` — dễ wildcard query trên observability platform (`api.request.*`, `pipeline.*`).

**Bắt buộc có trong mọi log line:**

- `event` — tên sự kiện (positional string trong structlog)
- `level` — info/warning/error
- `timestamp` — ISO 8601
- `request_id` — xuyên suốt request lifecycle
- Numeric fields phải là số (`duration_ms: 6`, không phải `"6"`)

**Context binding:** Dùng `bind()` (structlog) hoặc `contextvars` để tự động gắn `request_id`, `user_id` vào mọi log trong cùng request — không pass tay.

### Anti-patterns

- `print()` trong production
- Log message chứa mọi context trong string — không filter/parse được
- Dùng `event=` làm keyword arg trong structlog (gây TypeError collision)
- Numeric fields là string (`"200"` thay vì `200`) — Datadog/ELK không aggregate được

### Tool choices

|Tool|Khi nào dùng|
|---|---|
|**structlog**|Dự án mới, FastAPI, microservices — kwargs trực tiếp, `bind()`, JSON mặc định|
|**Standard logging + `extra={}`**|Dự án đang chạy ổn, không muốn thêm dependency|
|**Loguru**|Script nhỏ, CLI tool, prototype nhanh|

---

## Tầng 2: Log Aggregation

### Mục đích

Thu thập logs từ tất cả services về một nơi duy nhất. Không SSH vào server để đọc log.

### Best Practices

**Flow chuẩn:**

```
Service stdout → Collector (gắn labels) → Storage (index + nén) → UI (query + visualize)
```

**Labels quan trọng cần gắn:** `service_name`, `environment` (dev/staging/prod), `pod_name` (K8s), `level`, `event`.

**Retention policy:** Xác định trước — giữ logs bao lâu? 7 ngày cho dev, 30 ngày cho staging, 90 ngày cho production là baseline phổ biến.

**Không log sensitive data:** Passwords, tokens, PII không bao giờ xuất hiện trong log. Mask hoặc redact trước khi log.

### Anti-patterns

- Chỉ dùng `docker logs` / `kubectl logs` — mất log khi container restart
- Không có retention policy — disk full sau vài tuần
- Log PII/secrets — vi phạm compliance

### Tool choices

|Tool|Resource|Search|Best for|
|---|---|---|---|
|**Grafana Loki + Alloy** ★|Thấp|Labels (LogQL)|K8s, startup, budget hạn chế|
|**ELK Stack**|Cao (ES cần 4-8GB RAM)|Full-text (Lucene)|Fintech, audit trail, compliance|
|**SigNoz**|Trung bình|SQL|All-in-one thay Datadog|
|**Graylog**|Trung bình|Full-text|Security/SIEM, regulated industries|

**Collector choices:**

|Collector|Đặc điểm|
|---|---|
|**Grafana Alloy**|Modern, thu logs + metrics + traces trong 1 binary. Thay thế Promtail|
|**Fluent Bit**|Cực nhẹ, K8s DaemonSet, 500+ plugins|
|**Fluentd**|Nặng hơn Fluent Bit, mạnh transform/routing|
|**Filebeat**|Elastic ecosystem, ship logs về Elasticsearch|
|**Logstash**|Nặng nhất, mạnh parse/transform phức tạp|

---

## Tầng 3: Distributed Tracing

### Mục đích

Theo dõi một request đi qua nhiều services — mỗi service mất bao lâu, lỗi ở đâu, bottleneck chỗ nào.

### Best Practices

**Propagate trace context qua mọi service call:**

```
HTTP Header: X-Request-ID: abc-123 / traceparent: 00-abc123-...
Message Queue: metadata.trace_id = "abc-123"
```

Mỗi service log cùng `request_id` / `trace_id` → filter trên UI sẽ thấy toàn bộ journey.

**Hai layer tracing bổ sung nhau:**

```
┌─────────────────────────────────┬─────────────────────────────────┐
│  Infrastructure Tracing          │  LLM Tracing                    │
│  Latency, errors, throughput     │  Input/output, tokens, cost     │
│                                  │                                  │
│  Jaeger, Grafana Tempo, Zipkin   │  Langfuse, LangSmith, Helicone  │
│  Datadog APM                     │                                  │
└─────────────────────────────────┴─────────────────────────────────┘
```

**Standard: OpenTelemetry (OTEL)** — vendor-neutral, mọi tool đều support. Instrument một lần, gửi đến nhiều backend.

**Sampling:** Production volume cao → không trace 100% requests. Dùng head-based sampling (quyết định ở đầu request) hoặc tail-based sampling (giữ lại traces có lỗi/slow).

### Anti-patterns

- Trace 100% requests ở production — tốn storage, chậm hệ thống
- Không propagate trace_id qua message queue — mất context khi debug async flows
- Chỉ trace infrastructure mà không trace LLM calls — không biết LLM cost/quality

### Tool choices

|Tool|Loại|Đặc điểm|
|---|---|---|
|**Grafana Tempo**|OSS|Tích hợp LGTM stack, search by trace ID|
|**Jaeger**|OSS|Mature, CNCF graduated, standalone|
|**Zipkin**|OSS|Đơn giản, lightweight|
|**Langfuse**|OSS|Chuyên LLM: input/output/tokens/cost/prompt management|
|**Datadog APM**|SaaS|All-in-one, auto-instrumentation|

---

## Tầng 4: Metrics & Dashboards

### Mục đích

Đo lường liên tục. Team mở dashboard là biết hệ thống healthy hay không — không cần ai hỏi.

### Best Practices

**RED Metrics cho mỗi service (bắt buộc):**

- **R**ate — requests per second
- **E**rrors — error rate %
- **D**uration — p50, p95, p99 latency

**USE Metrics cho infrastructure:**

- **U**tilization — CPU%, Memory%, Disk%
- **S**aturation — queue depth, thread pool usage
- **E**rrors — hardware/OS errors

**LLM-specific metrics:**

- Tokens per request (prompt + completion)
- Cost per request (USD)
- Model latency (TTFB, total)
- Prompt cache hit rate

**Business metrics:**

- Lessons generated per day
- Success rate (% requests không lỗi)
- Average generation time
- User satisfaction (nếu có feedback)

**Dashboard hierarchy:**

```
Executive dashboard  → 3-5 key numbers (uptime, error rate, cost)
Team dashboard       → RED per service, LLM metrics
Debug dashboard      → Detailed per-endpoint, per-model breakdown
```

### Anti-patterns

- Dashboard quá nhiều panels — không ai đọc hết → chỉ giữ metrics actionable
- Chỉ đo infrastructure mà không đo business metrics
- Không set baseline — "P95 = 2s" có tốt hay không? So với tuần trước thì sao?

### Tool choices

|Tool|Loại|Đặc điểm|
|---|---|---|
|**Prometheus + Grafana** ★|OSS|Standard cho K8s metrics, PromQL|
|**Mimir**|OSS|Long-term Prometheus storage, Grafana ecosystem|
|**Victoria Metrics**|OSS|Alternative Prometheus, hiệu quả hơn ở scale lớn|
|**Datadog**|SaaS|Auto dashboards, AI anomaly detection|

---

## Tầng 5: Alerting

### Mục đích

Phát hiện vấn đề trước khi user báo. Alert phải actionable — nhận alert là biết cần làm gì.

### Best Practices

**Alert phải có 3 yếu tố:**

1. **What** — cái gì đang sai (error rate > 5%)
2. **Impact** — ảnh hưởng gì (users gặp 500 errors)
3. **Action** — link đến runbook hoặc dashboard

**Alert levels:**

|Level|Khi nào|Action|
|---|---|---|
|**P1 Critical**|Service down, data loss|Page on-call ngay, fix trong 15 phút|
|**P2 High**|Degraded performance, error spike|Slack channel, fix trong 1 giờ|
|**P3 Medium**|Anomaly, warning threshold|Slack, review trong ngày|
|**P4 Low**|Informational|Email digest, review weekly|

**Ví dụ alerts cụ thể:**

```
- Error rate > 5% trong 5 phút           → P2, Slack
- P95 latency > 10s trong 5 phút         → P2, Slack
- LLM cost spike > 2x trung bình ngày    → P3, Slack
- Service restart loop (>3 lần/10 phút)  → P1, Page
- Disk usage > 85%                        → P3, Slack
- Certificate expiry < 7 ngày            → P3, Email
```

### Anti-patterns

- **Alert fatigue** — quá nhiều alerts, team bắt đầu ignore → chỉ alert thứ actionable
- **Missing runbook** — alert fire nhưng không ai biết fix → mỗi alert phải có runbook link
- **No escalation** — alert ringing 30 phút không ai response → cần escalation policy
- **Alert on symptoms, not causes** — "CPU high" không actionable bằng "request queue backing up"

### Tool choices

|Tool|Loại|Đặc điểm|
|---|---|---|
|**Alertmanager** ★|OSS|Prometheus ecosystem, dedup + routing + silencing|
|**Grafana Alerting**|OSS|Tích hợp sẵn, multi-datasource|
|**PagerDuty**|SaaS|On-call rotation, escalation, incident management|
|**Opsgenie**|SaaS|Tương tự PagerDuty, Atlassian ecosystem|

---

## Tầng 6: Runbooks & Incident Response

### Mục đích

Khi alert fire, con người biết phải làm gì. Giảm MTTR (Mean Time To Resolution) — không ai phải nhớ trong đầu cách fix.

### Best Practices

**Mỗi runbook theo format:** Detect → Diagnose → Fix → Verify → Prevent

```markdown
# RUNBOOK: [Tên incident]

## Detect
- Alert nào fire?
- Symptom nhìn thấy?

## Diagnose
- Check commands cụ thể (copy-paste được)
- Decision tree: nếu X thì Y, nếu A thì B

## Fix
- Steps cụ thể, có commands
- Ai có quyền làm?
- Cần approval không?

## Verify
- Làm sao biết đã fix xong?
- Check commands sau khi fix

## Prevent
- Root cause?
- Action items để không lặp lại?
```

**Postmortem sau mỗi incident:**

- Timeline: chuyện gì xảy ra, khi nào
- Root cause: tại sao
- Impact: ảnh hưởng bao nhiêu users, bao lâu
- Action items: làm gì để không lặp lại
- Blameless: focus vào hệ thống, không blame cá nhân

### Anti-patterns

- Runbook outdated — viết xong không update → review quarterly
- Chỉ senior biết fix — runbook phải đủ chi tiết để junior cũng follow được
- Không postmortem — lặp lại cùng incident nhiều lần

---

## Best Practice Stack Combinations

### ★ Open Source Self-hosted — "LGTM Stack" (Recommended)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  App (structlog JSON → stdout)                                     │
│         │                                                           │
│         ▼                                                           │
│  Grafana Alloy (collector: logs + metrics + traces)                │
│         │                                                           │
│    ┌────┼────────────┐                                              │
│    ▼    ▼            ▼                                              │
│  Loki  Prometheus  Tempo      ← Storage                            │
│  (logs) (metrics)  (traces)                                        │
│    │    │            │                                              │
│    └────┼────────────┘                                              │
│         ▼                                                           │
│      Grafana                  ← Tất cả trong 1 UI                  │
│         │                                                           │
│         ▼                                                           │
│    Alertmanager               ← Alert routing                      │
│                                                                     │
│  + Langfuse (LLM-specific tracing, prompt management)              │
│                                                                     │
│  Cost: $0 (chỉ tốn server)                                        │
│  Maintain: Team tự quản lý                                         │
│  Best for: K8s, startup, team có DevOps skill                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### ★ Open Source All-in-One

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  App (OpenTelemetry instrumentation)                               │
│         │                                                           │
│         ▼                                                           │
│  OTEL Collector                                                     │
│         │                                                           │
│         ▼                                                           │
│  SigNoz (Logs + Traces + Metrics trong 1 platform)                 │
│                                                                     │
│  + Langfuse (LLM-specific tracing)                                 │
│                                                                     │
│  Cost: $0                                                           │
│  Maintain: Ít component hơn LGTM                                   │
│  Best for: Team nhỏ, muốn đơn giản, đang adopt OTEL               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### ★ SaaS Managed

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  App (Datadog agent / OTEL)                                        │
│         │                                                           │
│         ▼                                                           │
│  Datadog (Logs + APM + Metrics + Alerting + Dashboards)            │
│                                                                     │
│  + Langfuse (LLM tracing — Datadog chưa cover tốt LLM)            │
│                                                                     │
│  Cost: $15-50/host/month                                           │
│  Maintain: Zero ops                                                 │
│  Best for: Team không có DevOps, cần production nhanh              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Chọn stack theo loại dự án

|Loại dự án|Recommend|Lý do|
|---|---|---|
|**Startup / MVP**|LGTM hoặc SigNoz|Free, đủ dùng, scale sau|
|**K8s microservices**|LGTM Stack|Native K8s, Grafana ecosystem lớn nhất|
|**AI/LLM app**|LGTM + Langfuse|Langfuse chuyên LLM cost/quality tracking|
|**Fintech / Compliance**|ELK + Graylog|Full-text audit trail, SIEM capability|
|**Enterprise / Big budget**|Datadog hoặc Splunk|Zero ops, SLA, support|
|**Team < 5 người**|SigNoz + Langfuse|Ít component nhất, all-in-one|

---

## Triển khai theo thứ tự

```
Tầng 1 → Tầng 2 → Tầng 3 → Tầng 4 → Tầng 5 → Tầng 6
 1 ngày   1-2 ngày  2-3 ngày  1-2 ngày  1 ngày   ongoing

 Tổng: ~2-3 tuần cho full production observability stack
```

Không skip tầng. Tầng 1 sai → mọi thứ phía trên đều vô nghĩa.


---

