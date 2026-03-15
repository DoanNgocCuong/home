```bash
docs/
├── product/
│   ├── product-vision.md                          # Tầm nhìn dài hạn của sản phẩm, why tồn tại, mục tiêu lớn
│   ├── product-brief.md                           # Tóm tắt nhanh: vấn đề, giải pháp, đối tượng, value prop
│   ├── brd-business-requirements.md               # Business Requirements Document: yêu cầu từ góc business
│   ├── prd-product-requirements.md                # Product Requirements Document: mô tả tính năng ở level product
│   └── roadmap/
│       └── product-roadmap-qx-2025.md             # Lộ trình feature theo quý/năm, ưu tiên & mốc phát hành
│
├── requirements/
│   ├── srs-software-requirements-spec.md          # SRS: đặc tả đầy đủ yêu cầu hệ thống ở mức software
│   ├── use-cases/
│   │   ├── use-case-login.md                      # Use case chi tiết cho luồng đăng nhập
│   │   └── use-case-friendship-leveling.md        # Use case mô tả hành vi level up/down tình bạn
│   └── user-stories/
│       ├── us-001-as-user-i-want-xxx.md           # User story cụ thể #001 (mô tả nhu cầu người dùng)
│       └── us-002-as-user-i-want-yyy.md           # User story cụ thể #002
│
├── design/
│   ├── architecture/
│   │   ├── system-architecture-overview.md        # Tổng quan kiến trúc hệ thống (các service, boundary)
│   │   ├── context-handling-architecture.md       # Kiến trúc riêng cho Context Handling (containers, flow)
│   │   └── diagrams/
│   │       ├── sequence-diagrams.md               # Bộ sequence diagram chi tiết (BE ↔ AI ↔ DB, etc.)
│   │       ├── flowcharts.md                      # Flowchart cho logic xử lý (scoring, selection, phase…)
│   │       └── state-class-diagrams.md            # State diagram & class diagram cho các entity/phase
│   ├── technical-design/
│   │   ├── tdd-context-handling-friendship.md     # Tài liệu triển khai kỹ thuật module Context/Friendship (CHÍNH LÀ FILE BẠN GỬI)
│   │   ├── tdd-auth-service.md                    # Thiết kế kỹ thuật cho Auth Service
│   │   └── tdd-orchestration-service.md           # Thiết kế kỹ thuật cho Orchestration/Selection Service
│   ├── data-model/
│   │   ├── erd-overview.md                        # ERD tổng thể của hệ thống (các bảng & quan hệ)
│   │   ├── friendship-db-schema.md                # Chi tiết schema DB cho friendship, agent mapping, candidates
│   │   └── migration-notes.md                     # Ghi chú migration: thay đổi schema theo thời gian
│   └── api-specs/
│       ├── rest-api-spec.md                       # Spec tổng thể các REST API chính (format, auth, versioning)
│       ├── friendship-api-spec.md                 # API spec riêng cho tuyến /friendship, /activities, scoring
│       └── activities-suggestion-api-spec.md      # API spec cho việc đề xuất activities/agents đầu phiên
│
├── dev/
│   ├── README.md                                  # Hướng dẫn dev: cách chạy project, cấu trúc, entrypoint
│   ├── CONTRIBUTING.md                            # Quy tắc đóng góp code: PR rules, review, branch naming
│   ├── coding-guidelines.md                       # Quy ước code: pattern, kiến trúc, anti-pattern cần tránh
│   ├── git-workflow.md                            # Quy trình git: Git Flow / Trunk-based, cách dùng branch
│   └── code-style-guide.md                        # Style guide: PEP8 / ESLint rules, naming, format
│
├── testing/
│   ├── test-plan.md                               # Test Plan tổng: scope, mục tiêu, loại test, timeline
│   ├── test-strategy.md                           # Chiến lược test: phân tầng unit/integration/E2E, công cụ
│   ├── test-cases/
│   │   ├── tc-friendship-scoring.md               # Test case chi tiết cho logic friendship scoring
│   │   └── tc-activities-selection.md             # Test case chi tiết cho logic chọn Talk/Game agents
│   ├── test-report/
│   │   └── regression-report-2025-11-25.md        # Báo cáo regression test cho build ngày 25/11/2025
│   └── qa-checklists.md                           # Checklist QA trước release (sanity, smoke, UX…)
│
├── ops/
│   ├── deployment-guide.md                        # Hướng dẫn deploy: steps, script, rollback plan
│   ├── environments.md                            # Mô tả các môi trường: dev/staging/prod, URL, config
│   ├── infra/
│   │   ├── infra-overview.md                      # Tổng quan hạ tầng: k8s, cloud provider, network
│   │   └── k8s-terraform-notes.md                 # Ghi chú về manifest K8s, Terraform modules
│   ├── monitoring-alerting.md                     # Thiết kế monitoring, metric & alert (delay score, error rate)
│   └── runbooks/
│       ├── incident-friendship-score-delay.md     # Runbook xử lý incident khi việc update score bị trễ
│       └── service-down-runbook.md                # Runbook khi service down: bước check & khôi phục
│
├── user/
│   ├── user-manual.md                             # Hướng dẫn sử dụng chi tiết cho end-user
│   ├── quick-start-guide.md                       # Quick start: vài bước nhanh để bắt đầu dùng Pika
│   ├── faq.md                                     # Câu hỏi thường gặp (FAQ) cho user & support
│   └── release-notes/
│       ├── release-0.1.0.md                       # Ghi chú phát hành version 0.1.0 (alpha/beta)
│       └── release-1.0.0.md                       # Ghi chú phát hành chính thức 1.0.0
│
└── process/
    ├── adr-architecture-decisions.md              # Architecture Decision Records: log các quyết định kiến trúc
    ├── meeting-notes/
    │   ├── 2025-11-20-kickoff.md                  # Biên bản họp kickoff (phạm vi, mục tiêu, team)
    │   └── 2025-11-25-architecture-review.md      # Biên bản review kiến trúc context/friendship
    ├── security-policy.md                         # Chính sách bảo mật: data, access control, PII
    └── engineering-practices.md                   # Chuẩn & văn hoá kỹ thuật: code review, incident, retro


```