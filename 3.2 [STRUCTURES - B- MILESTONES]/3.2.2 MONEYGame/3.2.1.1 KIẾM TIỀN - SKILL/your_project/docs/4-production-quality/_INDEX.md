# 5 - Production Systems & MLOps

> **Best Practices · Production Quality · Production Engineering**
> 20 Domains MECE | Grouped by Lifecycle | Owner: Cường Learning | Updated: 2026-03-13

---

## Cấu trúc: 20 Domains (flat, grouped by Lifecycle)

```
5 - Production Systems & MLOps/
│
├── _INDEX.md                                              ← BẠN ĐANG Ở ĐÂY
├── _CKP_OLD/                                              ← ~301 files cũ (PHAN_I → PHAN_XV)
│
│   ── DESIGN TIME ──────────────────────────────────────
├── 5.01 - DESIGN - Architecture & Design/
├── 5.02 - DESIGN - API Design/
├── 5.03 - DESIGN - Database & Data Management/
│
│   ── BUILD TIME ───────────────────────────────────────
├── 5.04 - BUILD - Deployment & CI-CD/
├── 5.05 - BUILD - Testing/
├── 5.06 - BUILD - Code Quality & Maintainability/
│
│   ── RUN TIME ─────────────────────────────────────────
├── 5.07 - RUN - Reliability & Resilience/
├── 5.08 - RUN - Observability & Monitoring/
├── 5.09 - RUN - Error Handling/
├── 5.10 - RUN - Production Readiness/
│
│   ── CROSS-CUTTING ────────────────────────────────────
├── 5.11 - CROSS - Security/
├── 5.12 - CROSS - Configuration & Secrets/
├── 5.13 - CROSS - Infrastructure & Containerization/
├── 5.14 - CROSS - Documentation & Runbooks/
│
│   ── SPECIALIZED ──────────────────────────────────────
├── 5.15 - SPECIALIZED - MLOps & AI Systems/
├── 5.16 - SPECIALIZED - Caching & Performance Optimization/
├── 5.17 - SPECIALIZED - Async Processing & Message Queues/
├── 5.18 - SPECIALIZED - Compliance & Data Protection/
├── 5.19 - SPECIALIZED - Chaos Engineering & Resilience Testing/
└── 5.20 - SPECIALIZED - Cost Optimization/
```

---

## View 1: Master Table

| #              | Group                 | Domain                                 | Ghi chú                           |
| -------------- | --------------------- | -------------------------------------- | ---------------------------------- |
| 5.01           | DESIGN                | Architecture & Design                  | Core                               |
| 5.02           | DESIGN                | API Design                             | Core                               |
| 5.03           | DESIGN                | Database & Data Management             | Core                               |
| 5.04           | BUILD                 | Deployment & CI-CD                     | Core                               |
| 5.05           | BUILD                 | Testing                                | Core                               |
| 5.06           | BUILD                 | Code Quality & Maintainability         | Core                               |
| 5.07           | RUN                   | Reliability & Resilience               | Core                               |
| 5.08           | RUN                   | Observability & Monitoring             | Core                               |
| 5.09           | RUN                   | Error Handling                         | Core                               |
| 5.10           | RUN                   | Production Readiness                   | Core                               |
| 5.11           | CROSS                 | Security                               | Core                               |
| 5.12           | CROSS                 | Configuration & Secrets                | Core                               |
| 5.13           | CROSS                 | Infrastructure & Containerization      | Core                               |
| 5.14           | CROSS                 | Documentation & Runbooks               | Core                               |
| 5.15           | SPECIALIZED           | MLOps & AI Systems                     | Core                               |
| 5.16           | SPECIALIZED           | Caching & Performance Optimization     | Từ 3.4 v3.0                       |
| 5.17           | SPECIALIZED           | Async Processing & Message Queues      | Từ 3.4 v3.0                       |
| 5.18           | SPECIALIZED           | Compliance & Data Protection           | Từ 3.4 v3.0                       |
| 5.19           | SPECIALIZED           | Chaos Engineering & Resilience Testing | Từ 3.4 v3.0                       |
| **5.20** | **SPECIALIZED** | **Cost Optimization**            | **Từ file 3.2 — bổ sung** |

---

## View 2: Mapping với file 3.4 (La Mã → Arabic mới)

| File 3.4 | Folder mới | Group       | Domain                                 |
| -------- | ----------- | ----------- | -------------------------------------- |
| I        | 5.01        | DESIGN      | Architecture & Design                  |
| IX       | 5.02        | DESIGN      | API Design                             |
| VIII     | 5.03        | DESIGN      | Database & Data Management             |
| IV       | 5.04        | BUILD       | Deployment & CI-CD                     |
| VI       | 5.05        | BUILD       | Testing                                |
| XI       | 5.06        | BUILD       | Code Quality & Maintainability         |
| II       | 5.07        | RUN         | Reliability & Resilience               |
| III      | 5.08        | RUN         | Observability & Monitoring             |
| VII      | 5.09        | RUN         | Error Handling                         |
| XIV      | 5.10        | RUN         | Production Readiness                   |
| V        | 5.11        | CROSS       | Security                               |
| X        | 5.12        | CROSS       | Configuration & Secrets                |
| XII      | 5.13        | CROSS       | Infrastructure & Containerization      |
| XIII     | 5.14        | CROSS       | Documentation & Runbooks               |
| XV       | 5.15        | SPECIALIZED | MLOps & AI Systems                     |
| XVI      | 5.16        | SPECIALIZED | Caching & Performance Optimization     |
| XVII     | 5.17        | SPECIALIZED | Async Processing & Message Queues      |
| XVIII    | 5.18        | SPECIALIZED | Compliance & Data Protection           |
| XIX      | 5.19        | SPECIALIZED | Chaos Engineering & Resilience Testing |
| ★ NEW   | 5.20        | SPECIALIZED | Cost Optimization                      |

**Tổng: 72 best practices across 19 domains gốc + 1 domain mở rộng (5.20)**

---

## View 3: Mapping _CKP_OLD → Folders mới

| Folder cũ (PHAN_*)               | Content chính                         | → Folder mới |
| --------------------------------- | -------------------------------------- | -------------- |
| PHAN_I_Foundation_Risks           | FastAPI, Docker basics                 | 5.01, 5.13     |
| PHAN_II_Architecture_Design_Risks | Docker deep dive (40 files)            | 5.13           |
| PHAN_III_Reliability_Resilience   | Timeout, Fallback, OOM                 | 5.07           |
| PHAN_IV_Observability_Monitoring  | Langfuse, Locust, Logging (49 files)   | 5.08           |
| PHAN_V_Deployment_CI_CD           | Deploy, SSH, Git                       | 5.04           |
| PHAN_VI_Security                  | API Keys, JWT, Bitcoin hack            | 5.11           |
| PHAN_VIII_Code_Quality            | Code standards                         | 5.06           |
| PHAN_IX_Infrastructure            | Server, Azure                          | 5.13           |
| PHAN_X_Database                   | PostgreSQL, Redis, RabbitMQ (76 files) | 5.03, 5.17     |
| PHAN_XI_API_Design                | WebSocket, HTTP Streaming              | 5.02           |
| PHAN_XII_Configuration            | Docker tools, commands                 | 5.12           |
| PHAN_XIII_Documentation           | System Design prompts                  | 5.14           |
| PHAN_XV_MLOps                     | MLOps, Serving, Pipeline (92 files)    | 5.15           |

---

## View 4: 5.20 Cost Optimization — Chi tiết

> Source: File 3.2 Deep Research + AWS Well-Architected Cost Optimization Pillar

| # | Best Practice                    | Mô tả                                                                               |
| - | -------------------------------- | ------------------------------------------------------------------------------------- |
| 1 | Right-sizing & Resource Planning | Chọn đúng instance type, auto-scaling thresholds, không over-provision            |
| 2 | Spot/Reserved/Savings Plans      | Tối ưu pricing model cho workload (on-demand vs reserved vs spot)                   |
| 3 | Cost Observability & Tagging     | Tag resources theo team/project/env, cost dashboards, anomaly alerts                  |
| 4 | Idle Resource Cleanup            | Tự động detect & terminate unused resources (zombie instances, unattached volumes) |
| 5 | FinOps Culture & Accountability  | Mỗi team own cost metrics, budget alerts, cost review trong sprint                   |

---

## Quy tắc đặt tên file

```
[Ngày] - [Loại] - [Tên ngắn gọn].md

Ví dụ:
20260313 - Note - Circuit Breaker Config Production.md
20260313 - UseCase - Langfuse RAM Overflow 50GB Fix.md
20260313 - Bug - RabbitMQ Infinite Loop Worker.md
20260313 - Checklist - Pre-Deploy Verification.md
20260313 - Template - Incident Report.md
```

Loại: `Note` · `Summary` · `UseCase` · `Bug` · `Template` · `Checklist` · `DeepResearch`

---

## Quy tắc mở rộng

- **Folder trống = gap cần fill.** Không xoá folder trống.
- **Khi 1 domain > 50 files** → tạo sub-folder lúc đó (flat until painful).
- **Domain mới** → thêm 5.21, 5.22... không phá cấu trúc cũ.
- **Mỗi folder có _CKP/** cho bản nháp/checkpoint.
- **Format tên folder:** `5.XX - GROUP - Domain Name`


---

![1773346051083](image/_INDEX/1773346051083.png)


---

```
Ở mỗi folder trong 20 folders 
1. Cậu deep research về domain đó, SKILL domain đó, dùng những cái đã được đóng gói và dùng cho các agents từ các repo lớn mọi người chia sẻ về SKILL agent
2. mỗi folder tạo 1 file SKILL.md nhé 
3. DEEP RESEARCH ĐỂ TẠO RA   MỖI FILE SKILL.md đều là BEST PRACTICES
```


---



Đây là task lớn — 20 file SKILL.md, mỗi file cần deep research. Tớ triển song song cho nhanh:Done bro. **20/20 SKILL.md** đã tạo xong, tổng cộng **~11,000 dòng, ~380KB** knowledge base:

| Group                 | Domain                 | Lines | Nội dung chính                                        |
| --------------------- | ---------------------- | ----- | ------------------------------------------------------- |
| **DESIGN**      | 5.01 Architecture      | 448   | Clean Architecture, DDD, 12-Factor, Scalability         |
|                       | 5.02 API Design        | 788   | REST/GraphQL/gRPC, Pagination, Versioning, Stripe-style |
|                       | 5.03 Database          | 780   | PostgreSQL, Indexing, Connection Pooling, Sharding      |
| **BUILD**       | 5.04 Deployment        | 848   | Blue-green, Canary, Feature Flags, GitHub Actions       |
|                       | 5.05 Testing           | 979   | Test Pyramid, Contract Testing, Locust, Chaos           |
|                       | 5.06 Code Quality      | 1,221 | Clean Code, SonarQube, Refactoring, CODEOWNERS          |
| **RUN**         | 5.07 Reliability       | 341   | Circuit Breaker, Retry, Timeout, Error Budgets          |
|                       | 5.08 Observability     | 404   | Logs/Metrics/Traces, Langfuse, OpenTelemetry            |
|                       | 5.09 Error Handling    | 476   | RFC 7807, Dead Letter Queue, Saga Pattern               |
|                       | 5.10 Prod Readiness    | 589   | PRR Checklist, On-call, Google SRE Book                 |
| **CROSS**       | 5.11 Security          | 275   | OWASP, OAuth2, Secret Management, mTLS                  |
|                       | 5.12 Config & Secrets  | 383   | Vault, 12-Factor, Secret Rotation, Feature Flags        |
|                       | 5.13 Infrastructure    | 536   | Docker Best Practices, Terraform, K8s, Nginx            |
|                       | 5.14 Documentation     | 627   | ADR, Runbooks, Mermaid, Postmortem Templates            |
| **SPECIALIZED** | 5.15 MLOps             | 437   | vLLM, MLflow, Langfuse, RAG, Guardrails                 |
|                       | 5.16 Caching           | 508   | Redis, CDN, Cache Stampede, N+1 Query                   |
|                       | 5.17 Async/MQ          | 622   | RabbitMQ vs Kafka, DLQ, Saga, Stream Processing         |
|                       | 5.18 Compliance        | 793   | GDPR, PII, SOC 2, Data Breach Response                  |
|                       | 5.19 Chaos Engineering | 758   | Chaos Monkey, Game Days, Failure Injection              |
|                       | 5.20 Cost Optimization | 1,179 | FinOps, Right-sizing, Spot Instances, Tagging           |

Mỗi file đều có: Overview → Core Principles → Best Practices (What/Why/How/Anti-pattern) → Decision Frameworks → Checklist → Common Mistakes → Tools & References. Code examples thực tế (Python, Docker, Terraform, K8s).
