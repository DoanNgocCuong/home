
# Câu hỏi 1: 
  

```
│
├── 📚 docs/                                  ## DOCUMENTATION
│   ├── __init__.py
│   ├── README.md                             ## Project overview, quick start
│   │
│   ├── ARCHITECTURE/
.md                       ## HLD (High-Level Design)
│   │                                         ## Chapter 5 from your SDD template
│   │                                         ## System overview, C4 diagrams, tech stack
│   │
│   ├── DEVELOPMENT.md                        ## Local development setup
│   │                                         ## Prerequisites, env setup, running locally
│   │
│   ├── API.md                                ## API documentation
│   │                                         ## Link to Swagger UI, authentication
│   │
│   ├── DEPLOYMENT.md                         ## Production deployment guide
│   │                                         ## K8s setup, monitoring, scaling
│   │
│   ├── RUNBOOK/                             ## Operational runbook           
│   │                                        ## Incident response, common issues, 
│   │                                        ## Avoidance note
│   │   ├── RUNBOOK-001-....md              
│   │   ├── RUNBOOK-002-....md           
│   │   ├── RUNBOOK-003-....md          
│   │   └── RUNBOOK-004-....md         
│   │
│   ├── ADR/                                  ## Architecture Decision Records
│   │   ├── ADR-001-db-choice.md              ## Why PostgreSQL vs MongoDB
│   │   ├── ADR-002-event-driven.md           ## Why Kafka/RabbitMQ for async
│   │   ├── ADR-003-ddd-structure.md          ## Why DDD bounded contexts
│   │   └── ADR-004-api-versioning.md         ## API versioning strategy
│   │
│   ├── CONTRIBUTING.md                       ## How to contribute
│   │                                         ## Code style, PR process, testing requirements
│   │
│   ├── CHANGELOG.md                          ## Version history
│   │                                         ## v1.0.0 released, breaking changes, new features
│   │
│   ├── SECURITY.md                           ## Security guidelines
│   │                                         ## Vulnerability disclosure, best practices
│   │
│   └── GLOSSARY.md                           ## Domain terminology
│                                             ## User, Order, Payment, Product definitions
```

--- Hỏi xíu, deep research để tìm best practices của cách ghi chú tài liệu trong repo Product Source code.

```
À hiểu rồi! Để tôi quy hoạch theo MECE framework + thứ tự best practices như đã brainstorm:

📁 Recommended Folder Structure (Theo Best Practices)

docs/
│
├── 0-road/                                # THE ROAD - Hướng đi, tầm nhìn
│   ├── VISION.md                          # Tầm nhìn dự án
│   └── ROADMAP.md                        # Lộ trình phát triển
│
├── 1-why/                                 # WHY - Tại sao quyết định như vậy
│   ├── ADR/                              # Architecture Decision Records
│   │   ├── ADR-001-db-choice.md          # Why PostgreSQL vs MongoDB
│   │   ├── ADR-002-event-driven.md       # Why Kafka/RabbitMQ
│   │   ├── ADR-003-ddd-structure.md      # Why DDD bounded contexts
│   │   └── ADR-004-api-versioning.md     # API versioning strategy
│   │
│   └── POST_MORTEM/                      # Sai lầm + Root cause
│       └── PM-001-*.md                   # What → Why → Impact → Prevention
│
├── 2-how/                                 # HOW - Hướng dẫn vận hành
│   ├── DEVELOPMENT.md                    # Local dev setup
│   │                                      # Prerequisites, env vars, run locally
│   │
│   ├── DEPLOYMENT.md                     # Production deployment
│   │                                      # K8s, CI/CD, monitoring
│   │
│   ├── RUNBOOK/                         # Operational runbook
│   │   ├── RUNBOOK-001-*.md             # Incident: DB down
│   │   ├── RUNBOOK-002-*.md             # Incident: High latency
│   │   └── RUNBOOK-003-*.md             # Incident: Payment failure
│   │
│   └── CONTRIBUTING.md                   # How to contribute
│                                          # Code style, PR process, testing
│
├── 3-what/                                # WHAT - Specifications
│   ├── PRD.md                            # Product Requirements Document
│   │                                      # Feature list, user stories
│   │
│   ├── ARCHITECTURE.md                   # High-Level Design (HLD/SDD)
│   │                                      # System overview, C4 diagrams, tech stack
│   │
│   ├── API.md                           # API documentation
│   │                                      # Endpoints, authentication, Swagger
│   │
│   └── GLOSSARY.md                       # Domain terminology
│                                          # Game-specific terms, entities
│
├── 4-when/                                # WHEN - Lịch sử thay đổi
│   ├── CHANGELOG.md                      # Version history
│   │                                      # v1.0.0, breaking changes
│   │
│   └── migrations/                       # Database migrations
│       └── versions/
│
└── 5-team/                                # TEAM - Operations
    └── SECURITY.md                        # Security guidelines
│                                          # Vulnerability disclosure
📊 Mapping MECE
Folder    MECE Group    Nội dung
0-road/    ROAD    Vision, Roadmap, Strategy
1-why/    WHY    ADR, Post-mortem (tại sao quyết định)
2-how/    HOW    Development, Deployment, Runbook, Contributing
3-what/    WHAT    PRD, Architecture, API, Glossary
4-when/    WHEN    Changelog, migrations
5-team/    TEAM    Security guidelines
🔑 Key Changes so với flat structure
Trước    Sau
ADR/ (flat)    1-why/ADR/
RUNBOOK/ (flat)    2-how/RUNBOOK/
ARCHITECTURE.md (flat)    3-what/ARCHITECTURE.md
Không có    0-road/ - thêm mục roadmap
Không có    4-when/migrations/
Không có    5-team/SECURITY.md (tách riêng)
Cấu trúc này đã theo đúng best practices - đọc theo thứ tự tự nhiên: Road → Why → How → What → When → Team.

Bạn thấy sao?
```

???

Recommend cho mình 1. Mục đích của phần docs trong 1 repo để làm gì 2. Folder structure best practices của phần này :?

Show more

4:21 PM

Researched documentation best practices and structured recommendations comprehensively

Researched documentation best practices and structured recommendations comprehensively

Để mình research trước khi đưa ra recommendation.

Synthesized research để đề xuất cấu trúc tài liệu tối ưu

Synthesized research để đề xuất cấu trúc tài liệu tối ưu

Okay, đã research xong. Để mình đưa ra recommendation dựa trên best practices thực tế.

---
## Trả lời 1: 
### 1. Mục đích của `docs/` trong repo

Câu trả lời ngắn gọn: **`docs/` tồn tại để giải quyết vấn đề "knowledge loss" — khi người viết code rời đi, context và lý do đằng sau code không nên rời đi cùng.**

Cụ thể hơn, `docs/` trong repo phục vụ 3 nhóm người đọc chính theo thứ tự ưu tiên:

**Developer mới join team** — cần hiểu: repo này làm gì, chạy local thế nào, tại sao kiến trúc được thiết kế như vậy. Khi một member mới join team, họ sẽ đối mặt với câu hỏi "tại sao hệ thống được thiết kế kiểu này?" [Claudio Taverna](https://ctaverna.github.io/adr/) và ADR log chính là thứ giúp tiết kiệm nhiều ngày onboarding.

**Developer hiện tại** — cần tra cứu nhanh: API spec, runbook xử lý incident, quy trình deploy. Đây là tài liệu tham khảo hàng ngày.

**Ops/SRE** — cần biết cách vận hành: deployment, monitoring, incident response.

Một nguyên tắc quan trọng từ phong trào **docs-as-code**: docs nằm cùng repo với code để đảm bảo documentation luôn được version cùng code, đồng bộ khi code thay đổi [Blog](https://technology.blog.gov.uk/2017/08/25/why-we-use-a-docs-as-code-approach-for-technical-documentation/). Một số team yêu cầu developer phải thay đổi code và docs trong cùng một pull request [Mintlify](https://www.mintlify.com/blog/adopt-docs-as-code), biến documentation thành phần tự nhiên của quá trình phát triển thay vì một bước phụ.

**Quan trọng: `docs/` KHÔNG phải là nơi chứa user-facing documentation** (như help center, public API docs cho external developers). Nó là **internal engineering documentation** — viết cho team, phục vụ team.

---

### 2. Folder structure — Recommendation

#### Về cấu trúc MECE (0-road/1-why/2-how/...) bạn đề xuất

Mình thấy ý tưởng phân loại theo MECE rất tốt ở mức tư duy, nhưng **không nên dùng làm folder structure thực tế** vì vài lý do:

**Thứ nhất**, prefix số (0-, 1-, 2-...) tạo ra cognitive overhead. Developer mở repo không nghĩ "tôi cần tìm WHY" — họ nghĩ "tôi cần tìm ADR" hoặc "tôi cần runbook". Mục tiêu là có cấu trúc phân cấp rõ ràng với URL có ý nghĩa, để người đọc ngay lập tức biết mình đang xem gì [GitLab](https://docs.gitlab.com/development/documentation/site_architecture/folder_structure/).

**Thứ hai**, framework phổ biến nhất hiện nay cho technical docs là **Diátaxis** (được GitHub, Canonical/Ubuntu, Cloudflare, Gatsby áp dụng). Diátaxis xác định 4 nhu cầu riêng biệt và 4 dạng documentation tương ứng: tutorials, how-to guides, technical reference và explanation [Diataxis](https://diataxis.fr/). Nó phân loại theo **nhu cầu của người đọc**, không phải theo câu hỏi triết học (why/how/what).

**Thứ ba**, mỗi document trong repo nên thuộc một trong bốn loại này, giúp người đọc nhanh chóng tìm đúng tài liệu phù hợp với tình huống hiện tại [GitHub](https://github.blog/developer-skills/documentation-done-right-a-developers-guide/).

#### Cấu trúc mình recommend

Kết hợp Diátaxis + thực tế industry (GitLab, GitHub, AWS, Google), đây là structure phù hợp cho một **product source code repo** như Pika:

```
docs/
├── README.md                    # Mục lục + hướng dẫn đọc docs
│
├── getting-started/             # TUTORIALS (learning-oriented)
│   ├── local-development.md     # Setup môi trường dev từ đầu
│   └── first-contribution.md    # Guide cho contributor mới
│
├── guides/                      # HOW-TO GUIDES (task-oriented)  
│   ├── deployment.md            # Cách deploy lên production
│   ├── contributing.md          # PR process, code style, testing
│   └── runbooks/                # Operational procedures
│       ├── RUNBOOK-001-db-down.md
│       ├── RUNBOOK-002-high-latency.md
│       └── RUNBOOK-003-payment-failure.md
│
├── reference/                   # REFERENCE (information-oriented)
│   ├── architecture.md          # HLD, C4 diagrams, tech stack
│   ├── api.md                   # API endpoints, auth, Swagger link
│   ├── glossary.md              # Domain terminology
│   └── changelog.md             # Version history
│
├── decisions/                   # EXPLANATION (understanding-oriented)
│   ├── ADR-001-db-choice.md
│   ├── ADR-002-event-driven.md
│   ├── ADR-003-ddd-structure.md
│   └── ADR-004-api-versioning.md
│
└── security.md                  # Security policies & disclosure
```

#### Tại sao structure này?

**`getting-started/`** — Diátaxis gọi đây là Tutorials. Người mới join team cần đúng 1 nơi để bắt đầu, không phải tìm trong 6 folder.

**`guides/`** — How-to guides giải quyết vấn đề cụ thể. Runbooks nằm ở đây vì bản chất chúng là step-by-step instructions cho một tình huống cụ thể.

**`reference/`** — Tra cứu nhanh, không cần đọc từ đầu đến cuối. Architecture, API spec, glossary đều là dạng này.

**`decisions/`** — Thực tế phổ biến là lưu ADR trong một thư mục chuyên biệt như `docs/adr/` hoặc `architecture/decisions/` trong repo [TechTarget](https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records). Một số team thích dùng tên "decisions" hơn viết tắt "ADR" vì nó trực quan hơn, và team bắt đầu bỏ thêm nhiều loại quyết định khác vào đó [GitHub](https://github.com/joelparkerhenderson/architecture-decision-record) — vendor decisions, planning decisions, v.v. Đây chính là nơi chứa "WHY" trong framework MECE của bạn.

**Những thứ mình bỏ đi so với đề xuất ban đầu:**

- `0-road/` (VISION, ROADMAP) → Không thuộc repo. Đây là **product management artifacts**, nên sống trong Notion/Confluence/wiki riêng. Repo docs chỉ chứa thứ liên quan trực tiếp đến codebase.
- `4-when/migrations/` → Migrations là code, nằm trong `src/` hoặc root-level `migrations/`, không phải docs.
- `5-team/` → Quá mỏng để thành folder riêng. `security.md` đặt ở root của docs là đủ, vì GitHub cũng recognize `SECURITY.md` ở root.
- `PRD.md` → Product requirements không thuộc source code repo. Nó thuộc về product management tooling.
- `POST_MORTEM/` → Tốt hơn nên sống trong wiki/Notion nơi cả team non-technical cũng truy cập được, không chỉ developer.

#### Nguyên tắc chung

Từ research, mấy nguyên tắc quan trọng nhất:

1. **Phân loại theo nhu cầu người đọc** (Diátaxis), không phải theo taxonomy trừu tượng. Developer đến docs với câu hỏi cụ thể, không phải để khám phá một hệ thống phân cấp.
2. **Docs sống cùng code** — đặt ADR cạnh source code trong một folder chuyên biệt trong docs là cách tốt nhất [Red Hat](https://www.redhat.com/en/blog/architecture-decision-records), vì nó được version control cùng code.
3. **Flat hơn là deep** — 2 level là tối đa. Nếu cần click 3+ lần để tìm được file, structure quá sâu.
4. **README.md ở root docs/** — đóng vai trò mục lục, giúp người mới biết đọc gì trước.
5. **Mỗi doc có 1 mục đích rõ ràng** — reference là thông tin kỹ thuật thuần túy để tra cứu, explanation giải thích "tại sao", tutorial hướng dẫn học, how-to hướng dẫn làm [Sequin blog](https://blog.sequinstream.com/we-fixed-our-documentation-with-the-diataxis-framework/). Không trộn lẫn.

  

[Claude is AI and can make mistakes. Please double-check cited sources.](https://support.anthropic.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on)




---


## Trả lời 2:📚 `docs/` Folder Structure — Best Practices

> Dựa trên **Diátaxis framework** + industry practices (GitHub, GitLab, AWS, Google, Canonical)

---

### Nguyên tắc thiết kế

| ## | Nguyên tắc | Giải thích |
|---|-----------|------------|
| 1 | **Phân loại theo nhu cầu người đọc** | Developer đến docs với câu hỏi cụ thể, không phải để khám phá taxonomy |
| 2 | **Flat > Deep** | Tối đa 2 levels. Click 3+ lần = quá sâu |
| 3 | **Docs sống cùng code** | Version control cùng codebase, thay đổi code + docs trong cùng PR |
| 4 | **Mỗi doc có 1 mục đích** | Không trộn tutorial với reference, không trộn how-to với explanation |
| 5 | **README.md = Mục lục** | Điểm vào duy nhất, giúp người mới biết đọc gì trước |

---

### Cấu trúc đề xuất

```
docs/
│
├── README.md                          ## Mục lục + reading guide
│                                      ## "Bạn là ai? → Đọc cái này"
│
│   ┌─────────────────────────────────────────────────────────┐
│   │  TUTORIALS — "Giúp tôi BẮT ĐẦU"                       │
│   │  Audience: New team member, Day 1-3                     │
│   └─────────────────────────────────────────────────────────┘
├── getting-started/
│   ├── local-development.md           ## Setup môi trường dev từ đầu
│   │                                  ## Prerequisites → Clone → Env vars → Run → Verify
│   │
│   └── first-contribution.md          ## Từ zero đến first PR merged
│                                      ## Branch → Code → Test → PR → Review → Merge
│
│   ┌─────────────────────────────────────────────────────────┐
│   │  HOW-TO GUIDES — "Giúp tôi LÀM việc cụ thể"           │
│   │  Audience: Active developer/ops, task-focused           │
│   └─────────────────────────────────────────────────────────┘
├── guides/
│   ├── deployment.md                  ## Cách deploy lên production
│   │                                  ## K8s setup, CI/CD pipeline, rollback
│   │
│   ├── contributing.md                ## Code style, PR process, testing requirements
│   │                                  ## Linting rules, commit conventions
│   │
│   └── runbooks/                      ## Operational incident procedures
│       ├── RUNBOOK-001-db-down.md             ## Detect → Diagnose → Fix → Verify → Prevent
│       ├── RUNBOOK-002-high-latency.md
│       ├── RUNBOOK-003-payment-failure.md
│       └── RUNBOOK-004-cert-expired.md
│
│   ┌─────────────────────────────────────────────────────────┐
│   │  REFERENCE — "Giúp tôi TRA CỨU thông tin"              │
│   │  Audience: Any developer, lookup-oriented               │
│   └─────────────────────────────────────────────────────────┘
├── reference/
│   ├── architecture.md                ## HLD, C4 diagrams, tech stack
│   │                                  ## System overview, bounded contexts
│   │
│   ├── api.md                         ## API endpoints, authentication
│   │                                  ## Link to Swagger UI, request/response examples
│   │
│   ├── glossary.md                    ## Domain terminology
│   │                                  ## User, Order, Payment, Product definitions
│   │
│   └── changelog.md                   ## Version history
│                                      ## v1.0.0 released, breaking changes
│
│   ┌─────────────────────────────────────────────────────────┐
│   │  DECISIONS — "Giúp tôi HIỂU TẠI SAO"                   │
│   │  Audience: Any developer, understanding-oriented        │
│   └─────────────────────────────────────────────────────────┘
├── decisions/
│   ├── ADR-001-db-choice.md           ## Why PostgreSQL vs MongoDB
│   ├── ADR-002-event-driven.md        ## Why Kafka/RabbitMQ for async
│   ├── ADR-003-ddd-structure.md       ## Why DDD bounded contexts
│   └── ADR-004-api-versioning.md      ## API versioning strategy
│
│   ┌─────────────────────────────────────────────────────────┐
│   │  ROOT-LEVEL — GitHub-recognized files                   │
│   └─────────────────────────────────────────────────────────┘
└── security.md                        ## Security policies & vulnerability disclosure
```

---

### So sánh: Trước → Sau

| Trước (flat) | Sau (Diátaxis) | Lý do |
|---|---|---|
| `DEVELOPMENT.md` (root) | `getting-started/local-development.md` | Tutorial, không phải reference. Người mới cần guided path |
| `CONTRIBUTING.md` (root) | `guides/contributing.md` | How-to guide — task-oriented |
| `DEPLOYMENT.md` (root) | `guides/deployment.md` | How-to guide — task-oriented |
| `RUNBOOK/` (root) | `guides/runbooks/` | Runbooks là dạng how-to cho ops |
| `ARCHITECTURE.md` (root) | `reference/architecture.md` | Reference — tra cứu, không đọc từ đầu đến cuối |
| `API.md` (root) | `reference/api.md` | Reference — lookup-oriented |
| `GLOSSARY.md` (root) | `reference/glossary.md` | Reference — lookup-oriented |
| `CHANGELOG.md` (root) | `reference/changelog.md` | Reference — version lookup |
| `ADR/` (root) | `decisions/` | Explanation — "decisions" trực quan hơn "ADR" |
| `SECURITY.md` (root) | `security.md` (root of docs) | Giữ nguyên vị trí, GitHub auto-recognize |
| `__init__.py` | ❌ Xóa | docs/ không phải Python package |

---

### Những thứ NÊN BỎ khỏi repo docs

| Item | Nên sống ở đâu | Lý do |
|---|---|---|
| `VISION.md`, `ROADMAP.md` | Notion / Confluence / Wiki | Product management artifact, không phải engineering doc |
| `PRD.md` | Notion / Confluence / Wiki | Product requirements thay đổi thường xuyên, cần collaboration từ non-dev |
| `POST_MORTEM/` | Notion / Confluence / Wiki | Cần accessible cho cả non-technical stakeholders |
| `migrations/` | `src/` hoặc root `db/migrations/` | Migrations là code, không phải documentation |

---

### Template cho `docs/README.md`

```markdown
## 📚 Documentation

### Bạn đang tìm gì?

#### 🚀 Mới join team?
→ Bắt đầu từ [Local Development Setup](getting-started/local-development.md)
→ Sau đó đọc [First Contribution Guide](getting-started/first-contribution.md)

#### 🔧 Cần làm gì đó cụ thể?
→ [Deployment Guide](guides/deployment.md) — Deploy lên production
→ [Contributing Guide](guides/contributing.md) — Tạo PR đúng chuẩn
→ [Runbooks](guides/runbooks/) — Xử lý incident

#### 📖 Cần tra cứu?
→ [Architecture Overview](reference/architecture.md) — System design & tech stack
→ [API Reference](reference/api.md) — Endpoints & authentication
→ [Glossary](reference/glossary.md) — Domain terminology
→ [Changelog](reference/changelog.md) — Version history

#### 💡 Muốn hiểu tại sao?
→ [Architecture Decisions](decisions/) — Lý do đằng sau mỗi quyết định thiết kế

#### 🔒 Security
→ [Security Policy](security.md) — Vulnerability disclosure & guidelines
```

---

### ADR Template (cho `decisions/ADR-NNN-*.md`)

```markdown
## ADR-NNN: [Tiêu đề quyết định]

### Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

### Date
YYYY-MM-DD

### Context
Vấn đề gì đang xảy ra? Tại sao cần quyết định?

### Options Considered
1. **Option A** — Mô tả ngắn
   - ✅ Pros: ...
   - ❌ Cons: ...

2. **Option B** — Mô tả ngắn
   - ✅ Pros: ...
   - ❌ Cons: ...

### Decision
Chọn Option X vì [lý do chính].

### Consequences
- **Positive**: ...
- **Negative**: ...
- **Risks**: ...
```

---

### Runbook Template (cho `guides/runbooks/RUNBOOK-NNN-*.md`)

```markdown
## RUNBOOK-NNN: [Tên incident]

### Severity
P1 (Critical) | P2 (High) | P3 (Medium)

### Symptoms
- Dấu hiệu 1
- Dấu hiệu 2
- Alert/Dashboard link: [...]

### Diagnosis
1. Bước kiểm tra 1
2. Bước kiểm tra 2

### Resolution
1. Bước fix 1
2. Bước fix 2

### Verification
Cách xác nhận đã fix xong.

### Prevention
Làm gì để tránh tái diễn?

### History
| Date | Incident | Root Cause | Resolution Time |
|------|----------|-----------|----------------|
| YYYY-MM-DD | Mô tả | ... | Xh Xm |
```
