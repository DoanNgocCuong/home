Đây là roadmap thực tế, sắp theo thứ tự ưu tiên — mỗi tầng build trên tầng trước:

---

## 📁 Navigation

| Folder | Tầng | Mô tả |
|--------|------|-------|
| [1_Structured_Logging](./1_Structured_Logging) | Tầng 1 | Structured JSON Logging (đã có ✅) |
| [2_Log_Aggregation](./2_Log_Aggregation) | Tầng 2 | Log Aggregation (Datadog/ELK) |
| [3_Distributed_Tracing](./3_Distributed_Tracing) | Tầng 3 | Distributed Tracing (request_id propagation) |
| [4_Metrics_Dashboards](./4_Metrics_Dashboards) | Tầng 4 | Metrics & Dashboards |
| [5_Alerting](./5_Alerting) | Tầng 5 | Alerting |
| [6_Health_Checks_Runbooks](./6_Health_Checks_Runbooks) | Tầng 6 | Health Checks & Runbooks |

---

**Tầng 1: Structured Logging (đã có ✅)**

Đang có JSON logs với structlog, event naming convention, middleware logging. Đây là foundation.

---

**Tầng 2: Log Aggregation — thu thập logs về một nơi**

Hiện tại đang `docker logs` để đọc — không scale được. Cần đẩy logs về centralized platform để search, filter, alert.

Với stack hiện tại (Kubernetes + Datadog đã có trên Pika), bước tiếp là đảm bảo mọi service đều có Datadog agent thu logs. JSON logs sẵn rồi nên Datadog auto-parse được, filter theo `event`, `request_id`, `duration_ms` trực tiếp. Nếu chưa có Datadog thì ELK hoặc Grafana Loki là alternative self-hosted.

Kết quả: query `event:api.request.server_error` trên Datadog ra tất cả 5xx trong 24h qua, không cần SSH vào server.

---

**Tầng 3: Distributed Tracing — theo dõi request xuyên services**

Logging cho biết *chuyện gì xảy ra* trong từng service. Tracing cho biết *request đi qua những service nào, mỗi chỗ mất bao lâu*.

Với Pika stack (API → Orchestration → Emotion Service → LLM → TTS), một request từ robot đi qua 4-5 services. Không có tracing thì khi latency cao, không biết bottleneck ở đâu.

Cách làm: propagate `request_id` / `trace_id` qua tất cả service calls (HTTP header, message queue metadata). Mỗi service log cùng `request_id`. Sau đó trên Datadog APM hoặc Langfuse, filter theo `request_id` sẽ thấy toàn bộ journey.

Langfuse là layer tracing chuyên cho LLM calls (input/output/tokens/cost). Datadog APM là layer tracing cho infrastructure (latency, error rate, throughput). Cả hai bổ sung cho nhau.

---

**Tầng 4: Metrics & Dashboards — đo lường liên tục**

Từ logs và traces, extract metrics:

- **RED metrics** cho mỗi service: Rate (requests/sec), Errors (error rate %), Duration (p50, p95, p99)
- **LLM-specific**: tokens/request, cost/request, model latency
- **Business**: lessons generated/day, success rate, average generation time

Dashboard trên Datadog hoặc Grafana hiển thị realtime. Team mở lên là biết hệ thống đang healthy hay không, không cần ai hỏi.

---

**Tầng 5: Alerting — phát hiện sớm, không đợi user báo**

Dựa trên metrics ở tầng 4, set alert:

- Error rate > 5% trong 5 phút → Slack notification
- P95 latency > 10s → Slack notification
- LLM cost spike > 2x trung bình → Slack notification
- Service restart loop (như worker lúc trước) → Slack notification

Alert phải actionable — nhận alert là biết cần làm gì, không phải chỉ "có lỗi".

---

**Tầng 6: Health Checks & Runbooks — chuẩn bị cho incidents**

Mỗi service có `/health` endpoint check dependencies (Redis, DB, LLM API). Docker/K8s dùng health check để auto-restart.

Mỗi loại incident có runbook (như RUNBOOK-002 vừa viết cho Langfuse). Khi alert fire, runbook nói rõ: detect → diagnose → fix → verify.

---

**Tóm lại thứ tự triển khai cho Pika:**

| Thứ tự | Tầng | Effort | Impact |
|---|---|---|---|
| ✅ | Structured JSON Logging | Done | Foundation |
| → Tiếp | Log Aggregation (Datadog/ELK) | 1-2 ngày | Search logs không cần SSH |
| → Sau | Distributed Tracing (request_id propagation) | 2-3 ngày | Debug cross-service issues |
| → Sau | Langfuse integration (LLM tracing) | 2-3 ngày | Track LLM cost/quality |
| → Sau | Metrics Dashboard | 1-2 ngày | Real-time health visibility |
| → Sau | Alerting | 1 ngày | Phát hiện sớm, không đợi user |
| → Sau | Runbooks | Ongoing | Giảm MTTR khi incident |

Bước tiếp theo cụ thể nhất bây giờ là gì — log aggregation lên Datadog, hay finish Langfuse integration trước?