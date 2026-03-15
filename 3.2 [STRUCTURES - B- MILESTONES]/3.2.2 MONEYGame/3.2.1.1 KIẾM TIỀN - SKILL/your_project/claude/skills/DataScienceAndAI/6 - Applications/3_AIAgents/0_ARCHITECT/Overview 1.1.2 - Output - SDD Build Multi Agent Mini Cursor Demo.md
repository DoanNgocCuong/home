## SOFTWARE DESIGN DOCUMENT (SDD)

### Multi-Agent Coding System - Cursor Demo

**Version 1.0 | Production Quality Standard**

---

### DOCUMENT METADATA

```yaml
Title: "Multi-Agent Coding System - Cursor Demo"
Document_ID: "SDD-FINAI-CURSOR-DEMO-v1.0"

## Ownership
Author: "AI Architecture Team"
Co_Authors:
  - "Backend Development Team"
  - "DevOps Team"

## Review & Approval
Reviewers:
  Technical_Lead: "To Be Assigned"
  Product_Manager: "To Be Assigned"
  QA_Lead: "To Be Assigned"

## Status Tracking
Status: "Draft"
Priority: "P1-High"

## Timeline
Created_Date: "2025-12-17"
Last_Updated: "2025-12-17"
Target_Release: "Q1 2025"

## Versioning
Version: "1.0.0"

## Related Documents
Related_Docs:
  HLD: "utils/docs/HLD_.md"
  Architecture_Guide: "docs/HUONG_DAN_KHOI_TAO_AGENT.md"
```

---

### MỤC LỤC

**Phần I: Nền Tảng & Kiến Trúc**
1. [Tóm Tắt Điều Hành (TL;DR)](##1-tóm-tắt-điều-hành-tldr)
2. [Giới Thiệu](##2-giới-thiệu)
3. [Mục Tiêu, Phạm Vi & Ràng Buộc](##3-mục-tiêu-phạm-vi--ràng-buộc)
4. [Tổng Quan Hệ Thống](##4-tổng-quan-hệ-thống)
5. [Thiết Kế Cấp Cao (HLD)](##5-thiết-kế-cấp-cao-hld)
6. [Thiết Kế Cấp Thấp (LLD)](##6-thiết-kế-cấp-thấp-lld)

**Phần II: Chi Tiết Triển Khai**
7. [Thiết Kế API & Contracts](##7-thiết-kế-api--contracts)
8. [Thiết Kế Dữ Liệu](##8-thiết-kế-dữ-liệu)
9. [Thiết Kế Bảo Mật](##9-thiết-kế-bảo-mật)

**Phần III: Production Readiness**
10. [Resilience & Reliability](##10-resilience--reliability)
11. [Observability & Monitoring](##11-observability--monitoring)
12. [Deployment & Operations](##12-deployment--operations)
13. [Testing Strategy](##13-testing-strategy)

**Phần IV: Phân Tích Kiến Trúc**
14. [Brainstorm Kiến Trúc MECE](##14-brainstorm-kiến-trúc-mece)
15. [Trade-offs & Architecture Decisions](##15-trade-offs--architecture-decisions)

**Phần V: Roadmap & Checklist**
16. [Implementation Roadmap](##16-implementation-roadmap)
17. [Production Readiness Checklist](##17-production-readiness-checklist)

---

## PHẦN I: NỀN TẢNG & KIẾN TRÚC

---

### 1. TÓM TẮT ĐIỀU HÀNH (TL;DR)

#### 1.1 Summary Table

| Khía Cạnh | Chi Tiết |
|-----------|----------|
| **Problem Statement** | Cần hệ thống tự động sửa bug với nhiều agents chuyên biệt phối hợp, thay vì một agent đơn lẻ |
| **Proposed Solution** | Multi-Agent System với Hierarchical Choreography: 4 agents (Coder, Tester, Reviewer) + Chief Agent |
| **Business Impact** | Giảm 70% thời gian review code thủ công, tăng chất lượng code |
| **Technical Impact** | Parallel execution, fault isolation, scalable agent architecture |
| **Key Technology** | Python 3.11, LangGraph, FastAPI, Redis PubSub, Kafka |
| **Estimated Effort** | 2 người × 3 sprint = 30 man-days |
| **Risk Level** | Medium - Async coordination phức tạp |
| **Timeline** | MVP: 2 tuần, Production: 4 tuần |
| **Key Stakeholders** | AI Team, Backend Team, DevOps |

#### 1.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT CODING SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User: "Fix all failing tests in repo"                                  │
│                          ↓                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               LAYER 0: GOVERNANCE                               │    │
│  │   Input Gate → Whitelist agents, budget check, validation      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                          ↓                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               LAYER 1: PERCEPTION                               │    │
│  │   Parse input → Extract intent → Build context                 │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                          ↓                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               LAYER 2: COGNITION                                │    │
│  │  ┌────────────────────────────────────────────────────────┐   │    │
│  │  │            🧑‍💼 CHIEF AGENT                              │   │    │
│  │  │      (Facilitator - LangGraph Orchestrator)            │   │    │
│  │  └───────────────────────┬────────────────────────────────┘   │    │
│  │                          ↓                                     │    │
│  │  ┌────────────────────────────────────────────────────────┐   │    │
│  │  │           📬 MESSAGE BUS (Redis PubSub)                │   │    │
│  │  │  Topics: task_available, code_ready, test_result,      │   │    │
│  │  │          review_done, fix_request                      │   │    │
│  │  └────────────────────────────────────────────────────────┘   │    │
│  │           ↓              ↓              ↓                      │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │    │
│  │  │ CoderAgent   │ │ TesterAgent  │ │ReviewerAgent │          │    │
│  │  │  (P2P)       │←→│  (P2P)       │←→│  (P2P)      │          │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘          │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                          ↓                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               LAYER 3: ACTION                                   │    │
│  │   Tools: read_file, write_file, run_tests, git_diff           │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                          ↓                                              │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │               LAYER 0: OUTPUT GATE                              │    │
│  │   Validate results → Audit log → Return to user               │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 1.3 Key Metrics & Success Criteria

| KPI | Hiện Tại | Mục Tiêu | Phương Pháp Đo |
|-----|----------|----------|----------------|
| Task Completion Time | N/A | <5 phút/task | LangFuse tracing |
| Agent Collaboration Success | N/A | >95% | Message bus logs |
| Test Pass Rate sau fix | N/A | >90% | CI/CD metrics |
| Error Rate | N/A | <2% | Prometheus |
| P95 Latency | N/A | <30s | Datadog APM |

#### 1.4 Risk Summary

| Risk | Xác Suất | Impact | Mitigation |
|------|----------|--------|------------|
| Deadlock giữa agents | Medium | High | Timeout + circuit breaker |
| Message loss | Low | High | Redis persistence + retry |
| LLM rate limiting | Medium | Medium | Multi-provider fallback |
| Memory leak trong long sessions | Low | Medium | Session timeout + cleanup |

---

### 2. GIỚI THIỆU

#### 2.1 Mục Đích Tài Liệu

Tài liệu này cung cấp **bản thiết kế chi tiết production-ready** cho **Multi-Agent Coding System** (Cursor Demo):

- **HLD (High-Level Design)**: Kiến trúc tổng thể 4-layer với Q4 Hierarchical Choreography
- **LLD (Low-Level Design)**: Chi tiết implementation cho từng agent và message bus
- **Integration**: Cách tích hợp với hệ thống FinAI Agent hiện có
- **Production Standards**: Security, Observability, Reliability
- **Operations**: Runbooks, Testing Strategy, Deployment

#### 2.2 Đối Tượng Đọc

| Đối Tượng | Mục Đích Sử Dụng | Sections Chính |
|-----------|------------------|----------------|
| **Engineers** | Implementation | 5-8, 10-13 |
| **Architects** | Review kiến trúc | 5, 14-15 |
| **DevOps/SRE** | Operations | 10-12 |
| **QA** | Test Design | 13 |
| **Product** | Scope/Timeline | 1, 3, 16 |

#### 2.3 Định Nghĩa & Từ Viết Tắt

| Thuật Ngữ | Định Nghĩa |
|-----------|------------|
| **Q4** | Quadrant 4 - Multi-agents với high autonomy + dynamic coordination |
| **P2P** | Peer-to-Peer - Communication trực tiếp giữa agents |
| **Chief Agent** | Agent điều phối chính, không micromanage |
| **Message Bus** | Hệ thống PubSub cho inter-agent communication |
| **LangGraph** | Framework để xây dựng stateful, multi-actor applications với LLMs |
| **Choreography** | Pattern coordination nơi agents tự quyết định hành động |

#### 2.4 Tham Chiếu Code Base Hiện Tại

Dự án được xây dựng trên nền tảng **SpecialProd Agent FinAI WebBrowser** với các components chính:

```
app/
├── common/agent/           ## Base agent framework (BaseAgent, Registry, Factory)
├── module/agent/           ## Specific agents (talk_agent, demo_agent, etc.)
├── api/services/           ## Application services
└── common/                 ## Infrastructure (Redis, Kafka, MySQL, etc.)
```

---

### 3. MỤC TIÊU, PHẠM VI & RÀNG BUỘC

#### 3.1 Mục Tiêu

###### Business Goals

| Mục Tiêu | Metric | Target | Timeline |
|----------|--------|--------|----------|
| Tự động hóa bug fixing | Tasks completed/day | +500% | Sprint 3 |
| Giảm manual review | Review time | -70% | Sprint 4 |
| Demo Cursor-style | Working demo | 100% | Sprint 2 |

###### Technical Goals

| Mục Tiêu | Metric | Target | Timeline |
|----------|--------|--------|----------|
| Multi-agent coordination | Message delivery | 99.9% | Sprint 2 |
| Parallel execution | Throughput | 4x baseline | Sprint 3 |
| Fault isolation | Recovery time | <10s | Sprint 3 |
| Scalability | Agents | 10+ concurrent | Sprint 4 |

#### 3.2 Trong Phạm Vi ✅

**MVP (Must Have)**:
- ✅ 4 Agents: Chief, Coder, Tester, Reviewer
- ✅ Message Bus với Redis PubSub
- ✅ P2P communication giữa agents
- ✅ Basic tools: read_file, write_file, run_tests
- ✅ LangGraph integration cho Chief Agent

**Phase 2 (Should Have)**:
- 📋 Git integration (git_diff, git_commit)
- 📋 Security Agent
- 📋 Documentation Agent

**Phase 3 (Nice to Have)**:
- 💡 Web UI for monitoring
- 💡 A/B testing framework
- 💡 Custom agent builder

#### 3.3 Ngoài Phạm Vi ❌

| Non-Goal | Lý Do | Tương Lai? |
|----------|-------|-----------|
| IDE integration | Scope khác | Phase 4 |
| Multi-language support | Focus Python first | Phase 3 |
| Real-time collaboration | Complexity | Phase 4 |

#### 3.4 Assumptions

| ID | Assumption | Impact nếu Sai | Validation |
|----|------------|-----------------|------------|
| A1 | Redis cluster available | High - delay | DevOps confirm |
| A2 | LLM API stable | Medium - fallback needed | Monitor API |
| A3 | Team familiar với LangGraph | Low - training | Training plan |

#### 3.5 Constraints

###### Technical Constraints

| Constraint | Lý Do | Workaround |
|------------|-------|------------|
| Python 3.11+ | Company standard | N/A |
| Redis 7+ | PubSub features | N/A |
| LangGraph 0.2+ | State management | N/A |

###### Business Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| 2 week MVP timeline | Limited features | Reduce MVP scope |
| Budget for LLM calls | Rate limiting | Caching + batching |

#### 3.6 Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPENDENCY GRAPH                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Multi-Agent System                                         │
│        │                                                     │
│        ├──→ Base Agent Framework (app/common/agent/)        │
│        │         │                                          │
│        │         ├──→ LangGraph                             │
│        │         ├──→ LangChain                             │
│        │         └──→ LangFuse (tracing)                    │
│        │                                                     │
│        ├──→ Message Bus                                     │
│        │         │                                          │
│        │         └──→ Redis PubSub                          │
│        │                                                     │
│        ├──→ LLM Providers                                   │
│        │         │                                          │
│        │         ├──→ OpenAI API                            │
│        │         ├──→ Groq API                              │
│        │         └──→ Gemini API                            │
│        │                                                     │
│        └──→ Infrastructure                                  │
│                  │                                          │
│                  ├──→ MySQL (state persistence)             │
│                  ├──→ Kafka (event sourcing)               │
│                  └──→ S3 (file storage)                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. TỔNG QUAN HỆ THỐNG

#### 4.1 Business Context

**Vấn Đề**: 
Các coding assistant hiện tại (như Cursor) thường sử dụng single agent approach, dẫn đến:
- Bottleneck khi xử lý tasks phức tạp
- Không có separation of concerns
- Khó scale và maintain

**Giải Pháp**: 
Multi-Agent System với Hierarchical Choreography (Q4):
- 4+ agents chuyên biệt phối hợp
- Chief Agent điều phối nhưng không micromanage
- P2P communication cho hiệu quả cao

**Giá Trị**:
- Parallel execution: 4x throughput
- Fault isolation: Agent failure không ảnh hưởng toàn hệ thống
- Scalability: Dễ dàng thêm agents mới

#### 4.2 Stakeholders

| Stakeholder | Interest | Communication |
|-------------|----------|---------------|
| AI Team | Agent architecture | Daily standup |
| Backend Team | Integration | Sprint review |
| DevOps | Deployment | Weekly sync |
| Product | Demo quality | Bi-weekly demo |

#### 4.3 Functional Requirements

| ID | Module | Mô Tả | Priority | Acceptance Criteria |
|----|--------|-------|----------|---------------------|
| FR-001 | Chief Agent | Phân tích task và broadcast | P0 | Phân tích chính xác >90% |
| FR-002 | Coder Agent | Đọc và sửa code | P0 | Fix success rate >80% |
| FR-003 | Tester Agent | Chạy tests | P0 | Test coverage report accurate |
| FR-004 | Reviewer Agent | Review code quality | P0 | Detect issues >85% |
| FR-005 | Message Bus | P2P communication | P0 | Message delivery 99.9% |
| FR-006 | Tools | File operations | P0 | CRUD operations work |

#### 4.4 User Stories (Gherkin)

```gherkin
Feature: Multi-Agent Bug Fixing
  As a developer
  I want the system to automatically fix failing tests
  So that I can focus on feature development

  Scenario: Successful bug fix flow
    Given I have a repository with failing tests
    When I send command "Fix all failing tests in repo_demo"
    Then Chief Agent broadcasts task to all agents
    And Coder Agent reads the code
    And Coder Agent identifies the bug
    And Coder Agent fixes the code
    And Tester Agent runs tests
    And tests pass
    And Reviewer Agent approves the fix
    And I receive success confirmation

  Scenario: Bug fix requires multiple iterations
    Given Coder Agent has fixed the code
    When Tester Agent runs tests and they fail
    Then Reviewer Agent sends fix_request to Coder Agent
    And Coder Agent fixes the code again
    And process repeats until tests pass

  Scenario: Agent communication failure
    Given Message Bus is temporarily unavailable
    When an agent tries to send a message
    Then message is retried with exponential backoff
    And after 3 retries, error is logged
    And Chief Agent is notified of failure
```

---

### 5. THIẾT KẾ CẤP CAO (HLD)

#### 5.1 Architecture Pattern

**Selected**: Q4 - Hierarchical Choreography (Multi-Agent với High Autonomy)

**Rationale**:
- ✅ Agents tự quyết định actions dựa trên messages nhận được
- ✅ Chief Agent chỉ facilitate, không micromanage
- ✅ P2P communication cho low latency
- ✅ Parallel execution cho high throughput
- ✅ Fault isolation - agent failure không crash toàn hệ thống

**Key Principles**:
- **Autonomy**: Mỗi agent tự quyết định hành động
- **Choreography**: Không có central orchestrator cứng
- **Message-Driven**: Communication qua Message Bus
- **Stateless Agents**: State lưu trong shared store

#### 5.2 System Context (C4 Level 1)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM CONTEXT                                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    ┌──────────────┐           ┌──────────────────────────────────┐    │
│    │  Developer   │           │  External LLM APIs                │    │
│    │   (User)     │           │  • OpenAI                         │    │
│    └──────┬───────┘           │  • Groq                           │    │
│           │                   │  • Gemini                         │    │
│           │ HTTP/WebSocket    └──────────────┬───────────────────┘    │
│           │                                  │                         │
│           ▼                                  │                         │
│    ┌──────────────────────────────────────────────────────────────┐   │
│    │                                                              │   │
│    │              MULTI-AGENT CODING SYSTEM                       │   │
│    │                                                              │   │
│    │  • Nhận task từ user                                         │   │
│    │  • Phân tích và phân phối cho agents                        │   │
│    │  • Agents tự phối hợp qua Message Bus                       │   │
│    │  • Tổng hợp kết quả và trả về user                          │   │
│    │                                                              │   │
│    └──────────────────────────────────────────────────────────────┘   │
│           │                                  │                         │
│           │                                  │                         │
│           ▼                                  ▼                         │
│    ┌──────────────┐                  ┌──────────────┐                 │
│    │  Repository  │                  │   Storage    │                 │
│    │   (Files)    │                  │   (Redis)    │                 │
│    └──────────────┘                  └──────────────┘                 │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

#### 5.3 Container Diagram (C4 Level 2)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         CONTAINER DIAGRAM                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                        API LAYER                                       ││
│  │  ┌─────────────────┐       ┌─────────────────┐                        ││
│  │  │   FastAPI       │       │   WebSocket     │                        ││
│  │  │   REST API      │       │   Handler       │                        ││
│  │  │  /api/v1/agent  │       │   /ws/agent     │                        ││
│  │  └─────────────────┘       └─────────────────┘                        ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                     GOVERNANCE LAYER (Layer 0)                         ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       ││
│  │  │   Input Gate    │  │  In-Flight      │  │  Output Gate    │       ││
│  │  │  • Validation   │  │  Guards         │  │  • Validation   │       ││
│  │  │  • Rate limit   │  │  • Budget check │  │  • Audit log    │       ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                     PERCEPTION LAYER (Layer 1)                         ││
│  │  ┌─────────────────┐  ┌─────────────────┐                             ││
│  │  │  Input          │  │  Context        │                             ││
│  │  │  Processor      │  │  Builder        │                             ││
│  │  │  • Parse text   │  │  • Build prompt │                             ││
│  │  │  • Extract intent│  │  • Add context  │                             ││
│  │  └─────────────────┘  └─────────────────┘                             ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                      COGNITION LAYER (Layer 2)                         ││
│  │                                                                        ││
│  │  ┌──────────────────────────────────────────────────────────────────┐││
│  │  │                    CHIEF AGENT                                    │││
│  │  │  • Analyze task                                                   │││
│  │  │  • Broadcast to Message Bus                                       │││
│  │  │  • Synthesize results                                             │││
│  │  └──────────────────────────────────────────────────────────────────┘││
│  │                            ↓                                          ││
│  │  ┌──────────────────────────────────────────────────────────────────┐││
│  │  │                    MESSAGE BUS (Redis PubSub)                     │││
│  │  │  Topics: task_available | code_ready | test_result | review_done │││
│  │  └──────────────────────────────────────────────────────────────────┘││
│  │            ↓                    ↓                    ↓               ││
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         ││
│  │  │  CODER AGENT   │  │  TESTER AGENT  │  │ REVIEWER AGENT │         ││
│  │  │                │←→│                │←→│                │         ││
│  │  │  • Read code   │  │  • Run tests   │  │  • Review code │         ││
│  │  │  • Fix bugs    │  │  • Report      │  │  • Approve/    │         ││
│  │  │  • Write code  │  │    results     │  │    Request fix │         ││
│  │  └────────────────┘  └────────────────┘  └────────────────┘         ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                       ACTION LAYER (Layer 3)                           ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ ││
│  │  │  read_file  │  │ write_file  │  │  run_tests  │  │  git_diff   │ ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐│
│  │                       DATA LAYER                                       ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                   ││
│  │  │   Redis     │  │    MySQL    │  │   Kafka     │                   ││
│  │  │  (State)    │  │ (Persist)   │  │  (Events)   │                   ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘                   ││
│  └───────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

#### 5.4 Technology Stack

| Layer | Technology | Lý Do Chọn |
|-------|------------|------------|
| **Framework** | Python 3.11 + FastAPI | Async support, ecosystem |
| **Agent Framework** | LangGraph | Native multi-agent, state management |
| **LLM** | OpenAI GPT-4 / Groq | Quality + Speed fallback |
| **Message Bus** | Redis PubSub | Low latency, simple |
| **State Store** | Redis | In-memory, fast |
| **Database** | MySQL | Persistence, existing infra |
| **Event Stream** | Kafka | Event sourcing, audit |
| **Tracing** | LangFuse | LLM-native tracing |
| **Container** | Docker | Consistency |
| **Orchestration** | Kubernetes | Production scaling |

#### 5.5 Communication Patterns

| Pattern | Use Case | Protocol | Implementation |
|---------|----------|----------|----------------|
| **Broadcast** | Chief → All agents | PubSub | task_available topic |
| **P2P** | Agent ↔ Agent | Direct message | Specific agent topic |
| **Request/Response** | API calls | REST | FastAPI |
| **Streaming** | Real-time updates | WebSocket | Agent events |

#### 5.6 Agent Roles Summary

| Agent | Role | Subscribe Topics | Publish Topics | Tools |
|-------|------|------------------|----------------|-------|
| **Chief** | Facilitator | all | task_available, final_report | LLM planning |
| **Coder** | Code writer | task_available, fix_request | code_ready | read_file, write_file |
| **Tester** | Test runner | code_ready | test_result | run_tests |
| **Reviewer** | Quality gate | test_result | review_done, fix_request | search_in_files |

---

### 6. THIẾT KẾ CẤP THẤP (LLD)

#### 6.1 File Structure

```bash
app/module/finai_agent/
├── __init__.py
├── agent_entrypoint.py              ## Entry point - spawn all agents
│
├── layer_0_governance/
│   ├── __init__.py
│   ├── phase_1_input_gate/
│   │   ├── __init__.py
│   │   ├── input_gate.py           ## Input validation
│   │   ├── pii_detector.py         ## PII detection
│   │   ├── injection_detector.py   ## Injection detection
│   │   ├── models.py
│   │   └── exceptions.py
│   │
│   ├── phase_2_in_flight_guards/
│   │   ├── __init__.py
│   │   ├── base_guard.py
│   │   └── models.py
│   │
│   ├── phase_3_output_gate/
│   │   ├── __init__.py
│   │   ├── result_validator.py
│   │   ├── audit_logger.py
│   │   ├── models.py
│   │   └── exceptions.py
│   │
│   └── exceptions.py
│
├── layer_1_perception/
│   ├── __init__.py
│   ├── input_processor.py          ## Parse user input
│   ├── context_builder.py          ## Build context for agents
│   ├── state.py
│   ├── models.py
│   └── exceptions.py
│
├── layer_2_cognition/
│   ├── __init__.py
│   ├── message_bus.py              ## 🆕 Redis PubSub wrapper
│   ├── base_agent.py               ## 🆕 Base P2P agent class
│   ├── state.py                    ## Shared state schema
│   │
│   ├── chief_agent/                ## Chief Agent
│   │   ├── __init__.py
│   │   ├── chief.py               ## Main chief logic
│   │   ├── graph.py               ## LangGraph definition
│   │   └── prompts.py
│   │
│   ├── coder_agent/                ## Coder Agent
│   │   ├── __init__.py
│   │   ├── coder.py
│   │   └── prompts.py
│   │
│   ├── tester_agent/               ## Tester Agent
│   │   ├── __init__.py
│   │   ├── tester.py
│   │   └── prompts.py
│   │
│   ├── reviewer_agent/             ## Reviewer Agent
│   │   ├── __init__.py
│   │   ├── reviewer.py
│   │   └── prompts.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_manager.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── router.py              ## LLM provider router
│   │   └── prompts.py
│   │
│   └── exceptions.py
│
├── layer_3_action/
│   ├── __init__.py
│   ├── tool_registry.py
│   ├── executor.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base_tool.py
│   │   ├── file_tools.py          ## read_file, write_file, list_files
│   │   ├── execution_tools.py     ## run_tests
│   │   └── models.py
│   └── exceptions.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_message_bus.py
│   │   ├── test_chief_agent.py
│   │   ├── test_coder_agent.py
│   │   ├── test_tester_agent.py
│   │   └── test_reviewer_agent.py
│   ├── integration/
│   │   └── test_multi_agent_flow.py
│   └── fixtures/
│       ├── repo_demo/
│       │   ├── math_utils.py
│       │   └── tests.py
│       └── mock_data.py
│
├── README.md
└── ARCHITECTURE.md
```

#### 6.2 Core Components Detail

###### 6.2.1 Message Bus (message_bus.py)

```python
"""
Message Bus Module - Central PubSub cho P2P communication.

Module này cung cấp:
- In-memory PubSub cho demo
- Redis PubSub cho production
- Message history cho debugging
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from enum import Enum

from app.common.log import setup_logger

logger = setup_logger(__name__)


class MessageTopic(Enum):
    """Defined topics cho type safety."""
    TASK_AVAILABLE = "task_available"
    CODE_READY = "code_ready"
    TEST_RESULT = "test_result"
    REVIEW_DONE = "review_done"
    FIX_REQUEST = "fix_request"
    FINAL_REPORT = "final_report"


@dataclass
class Message:
    """
    Message schema cho inter-agent communication.
    
    Attributes:
        from_agent: Agent gửi message
        to_agent: "broadcast" hoặc specific agent name
        topic: MessageTopic enum
        payload: Message data
        timestamp: Auto-generated
        message_id: Unique ID cho tracing
    """
    from_agent: str
    to_agent: str  ## "broadcast" hoặc agent name
    topic: str
    payload: Dict[str, Any]
    timestamp: float = None
    message_id: str = None
    
    def __post_init__(self):
        import uuid
        if not self.timestamp:
            self.timestamp = datetime.now().timestamp()
        if not self.message_id:
            self.message_id = str(uuid.uuid4())[:8]


class MessageBus:
    """
    Central PubSub cho P2P communication.
    
    In-memory implementation cho demo.
    Production: nên thay bằng Redis PubSub.
    
    Features:
    - Subscribe/Publish pattern
    - Message history cho debugging
    - Async handlers
    """
    
    def __init__(self, redis_client=None):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
        self.redis = redis_client
        self._lock = asyncio.Lock()
        
    def subscribe(self, topic: str, callback: Callable):
        """
        Subscribe một callback vào topic.
        
        Args:
            topic: Topic name (từ MessageTopic enum)
            callback: Async function để handle message
        """
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.info(f"[MessageBus] ✓ Subscribed to '{topic}'")
        
    async def publish(self, msg: Message):
        """
        Publish message đến tất cả subscribers của topic.
        
        Args:
            msg: Message object
        """
        async with self._lock:
            self.message_history.append(msg)
            
        logger.info(
            f"[MessageBus] 📨 {msg.from_agent} → {msg.to_agent} | "
            f"{msg.topic} | ID: {msg.message_id}"
        )
        
        ## Notify all subscribers
        tasks = []
        for callback in self.subscribers.get(msg.topic, []):
            tasks.append(asyncio.create_task(callback(msg)))
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
    def get_history(self, topic: str = None, limit: int = 100) -> List[Message]:
        """Get message history cho debugging."""
        if topic:
            return [m for m in self.message_history if m.topic == topic][-limit:]
        return self.message_history[-limit:]
        
    def clear_history(self):
        """Clear message history."""
        self.message_history.clear()


## Global bus instance - singleton pattern
_bus_instance: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """Get or create MessageBus singleton."""
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = MessageBus()
    return _bus_instance
```

###### 6.2.2 Base P2P Agent (base_agent.py)

```python
"""
Base P2P Agent Module - Abstract base class cho tất cả P2P agents.

Module này cung cấp:
- Base class với subscribe/publish methods
- Autonomous run loop
- State management
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import asyncio

from app.module.finai_agent.layer_2_cognition.message_bus import (
    Message, MessageBus, get_message_bus
)
from app.common.log import setup_logger

logger = setup_logger(__name__)


class P2PAgent(ABC):
    """
    Abstract base class cho autonomous P2P agents.
    
    Mỗi agent:
    - Subscribe vào các topics quan tâm
    - Tự xử lý messages trong inbox
    - Tự quyết định hành động tiếp theo
    - Có thể gửi P2P messages
    """
    
    def __init__(
        self, 
        name: str, 
        subscribed_topics: List[str],
        bus: MessageBus = None
    ):
        """
        Initialize P2P Agent.
        
        Args:
            name: Agent name (unique identifier)
            subscribed_topics: List of topics to subscribe
            bus: MessageBus instance (optional, uses global if not provided)
        """
        self.name = name
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.state = "idle"
        self.bus = bus or get_message_bus()
        self._running = False
        
        ## Subscribe to topics
        for topic in subscribed_topics:
            self.bus.subscribe(topic, self._on_message)
            
        logger.info(f"[{self.name}] Initialized with topics: {subscribed_topics}")
            
    async def _on_message(self, msg: Message):
        """
        Callback khi nhận message từ bus.
        Chỉ nhận nếu message gửi cho mình hoặc broadcast.
        """
        if msg.to_agent in ["broadcast", self.name]:
            await self.inbox.put(msg)
            logger.debug(
                f"[{self.name}] 📬 Received: {msg.topic} from {msg.from_agent}"
            )
            
    async def send(
        self, 
        to_agent: str, 
        topic: str, 
        payload: Dict[str, Any]
    ):
        """
        Send message qua Message Bus.
        
        Args:
            to_agent: "broadcast" hoặc specific agent name
            topic: Message topic
            payload: Message data
        """
        msg = Message(
            from_agent=self.name,
            to_agent=to_agent,
            topic=topic,
            payload=payload,
        )
        await self.bus.publish(msg)
        
    @abstractmethod
    async def decide_next_action(self, msg: Message) -> str:
        """
        Agent TỰ quyết định hành động tiếp theo.
        
        Args:
            msg: Message vừa nhận
            
        Returns:
            str: Action name hoặc "STOP" để dừng
        """
        pass
        
    @abstractmethod
    async def execute_action(self, action: str, msg: Message):
        """
        Execute action đã quyết định.
        
        Args:
            action: Action name
            msg: Message context
        """
        pass
        
    async def run_loop(self, timeout: float = 300):
        """
        Main autonomous loop.
        
        Agent sẽ:
        1. Chờ message trong inbox
        2. Quyết định action
        3. Execute action
        4. Repeat
        
        Args:
            timeout: Max time to run (seconds)
        """
        self._running = True
        logger.info(f"[{self.name}] 🚀 Started")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            while self._running:
                ## Check timeout
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.warning(f"[{self.name}] ⏰ Timeout reached")
                    break
                    
                try:
                    ## Wait for message with timeout
                    msg = await asyncio.wait_for(
                        self.inbox.get(), 
                        timeout=5.0
                    )
                    
                    ## Decide action
                    action = await self.decide_next_action(msg)
                    
                    if action == "STOP":
                        logger.info(f"[{self.name}] 🛑 Stopping")
                        break
                        
                    ## Execute action
                    await self.execute_action(action, msg)
                    
                except asyncio.TimeoutError:
                    ## No message, continue waiting
                    continue
                    
        except Exception as e:
            logger.error(f"[{self.name}] Error in run loop: {e}")
            raise
        finally:
            self._running = False
            logger.info(f"[{self.name}] Stopped")
            
    def stop(self):
        """Signal agent to stop."""
        self._running = False
```

###### 6.2.3 Chief Agent (chief.py)

```python
"""
Chief Agent - Facilitator cho Multi-Agent System.

Chief Agent responsibilities:
1. Nhận task từ user
2. Phân tích và break down thành sub-tasks
3. Broadcast sub-tasks lên Message Bus
4. Collect results từ các agents
5. Synthesize final report
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage

from app.module.finai_agent.layer_2_cognition.base_agent import P2PAgent
from app.module.finai_agent.layer_2_cognition.message_bus import Message
from app.common.log import setup_logger

logger = setup_logger(__name__)


CHIEF_SYSTEM_PROMPT = """
Bạn là Chief Agent - người điều phối trong Multi-Agent Coding System.

Nhiệm vụ của bạn:
1. Phân tích task từ user
2. Xác định sub-tasks cần thiết
3. Broadcast task cho các agents phù hợp
4. Tổng hợp kết quả

Available agents:
- CoderAgent: Viết và sửa code
- TesterAgent: Chạy tests
- ReviewerAgent: Review code quality

Hãy trả lời ngắn gọn và rõ ràng.
"""


class ChiefAgent(P2PAgent):
    """
    Chief Agent: Facilitator, không micromanage.
    
    Workflow:
    1. Nhận task → Phân tích
    2. Broadcast → Chờ results
    3. Synthesize → Return to user
    """
    
    def __init__(self, llm=None, **kwargs):
        super().__init__(
            name="Chief",
            subscribed_topics=[
                "code_ready", 
                "test_result", 
                "review_done"
            ],
            **kwargs
        )
        self.llm = llm
        self.results_collected: List[Message] = []
        self.current_task: str = None
        self.waiting_for_results = False
        
    async def decide_next_action(self, msg: Message) -> str:
        """Chief quyết định action dựa trên message nhận được."""
        
        ## Nếu nhận được review_done → có thể synthesize
        if msg.topic == "review_done":
            self.results_collected.append(msg)
            if msg.payload.get("status") == "approved":
                return "synthesize"
            ## Nếu chưa approved, chờ thêm
            return "wait"
            
        ## Nếu nhận được test_result hoặc code_ready → log và chờ
        if msg.topic in ["test_result", "code_ready"]:
            self.results_collected.append(msg)
            return "wait"
            
        return "wait"
        
    async def execute_action(self, action: str, msg: Message):
        """Execute Chief's actions."""
        
        if action == "synthesize":
            await self._synthesize_results()
            
        elif action == "wait":
            logger.debug(f"[{self.name}] Waiting for more results...")
            
    async def _synthesize_results(self):
        """Tổng hợp results từ tất cả agents."""
        logger.info(f"[{self.name}] 📊 Synthesizing results...")
        
        report_lines = [
            "✓ Multi-agent collaboration completed:",
            f"  - Task: {self.current_task}",
            f"  - Results collected: {len(self.results_collected)}",
            ""
        ]
        
        for msg in self.results_collected:
            status = msg.payload.get("status", "unknown")
            report_lines.append(f"  - {msg.from_agent}: {status}")
            
        final_report = "\n".join(report_lines)
        logger.info(f"[{self.name}] Final Report:\n{final_report}")
        
        ## Publish final report
        await self.send(
            to_agent="broadcast",
            topic="final_report",
            payload={
                "status": "completed",
                "report": final_report,
                "task": self.current_task,
            }
        )
        
        ## Clear state
        self.results_collected.clear()
        self.current_task = None
        
    async def broadcast_task(self, goal: str, repo_path: str = "."):
        """
        Entry point: Broadcast task lên bus cho các agents.
        
        Args:
            goal: User's goal (e.g., "Fix all failing tests")
            repo_path: Path to repository
        """
        self.current_task = goal
        self.waiting_for_results = True
        
        logger.info(f"[{self.name}] 📣 Broadcasting task: {goal}")
        
        await self.send(
            to_agent="broadcast",
            topic="task_available",
            payload={
                "goal": goal,
                "repo_path": repo_path,
            },
        )
```

###### 6.2.4 Coder Agent (coder.py)

```python
"""
Coder Agent - Chuyên viết và sửa code.

Responsibilities:
1. Nhận task từ Chief
2. Đọc code hiện tại
3. Phân tích và fix bugs
4. Gửi code đã fix cho Tester
"""

from typing import Dict, Any

from app.module.finai_agent.layer_2_cognition.base_agent import P2PAgent
from app.module.finai_agent.layer_2_cognition.message_bus import Message
from app.module.finai_agent.layer_3_action.tools.file_tools import (
    read_file, write_file, list_files
)
from app.common.log import setup_logger

logger = setup_logger(__name__)


CODER_SYSTEM_PROMPT = """
Bạn là Coder Agent - chuyên viết và sửa code.

Nhiệm vụ:
1. Đọc code hiện tại
2. Phân tích lỗi (nếu có)
3. Fix bug hoặc viết code mới
4. Đảm bảo code chạy được

Hãy viết code clean, có comments, và follow best practices.
"""


class CoderAgent(P2PAgent):
    """
    Coder Agent: Chuyên viết & sửa code.
    
    Subscribe: task_available, fix_request
    Publish: code_ready
    Tools: read_file, write_file, list_files
    """
    
    def __init__(self, llm=None, **kwargs):
        super().__init__(
            name="Coder",
            subscribed_topics=["task_available", "fix_request"],
            **kwargs
        )
        self.llm = llm
        self.current_file: str = None
        
    async def decide_next_action(self, msg: Message) -> str:
        """Coder quyết định action."""
        
        if msg.topic == "task_available":
            return "analyze_and_code"
            
        elif msg.topic == "fix_request":
            return "fix_bug"
            
        return "idle"
        
    async def execute_action(self, action: str, msg: Message):
        """Execute coder actions."""
        
        if action == "analyze_and_code":
            await self._analyze_and_code(msg)
            
        elif action == "fix_bug":
            await self._fix_bug(msg)
            
    async def _analyze_and_code(self, msg: Message):
        """Phân tích task và viết/sửa code."""
        repo_path = msg.payload.get("repo_path", ".")
        goal = msg.payload.get("goal", "")
        
        logger.info(f"[{self.name}] 🔍 Analyzing task: {goal}")
        
        ## List files trong repo
        files = list_files(repo_path)
        logger.info(f"[{self.name}] Files found: {files}")
        
        ## Đọc file chính (demo: math_utils.py)
        target_file = f"{repo_path}/math_utils.py"
        try:
            code = read_file(target_file)
            self.current_file = target_file
            logger.info(f"[{self.name}] ✍️ Current code:\n{code}")
            
            ## Gửi code cho Tester
            await self.send(
                to_agent="Tester",
                topic="code_ready",
                payload={
                    "file": target_file,
                    "code": code,
                    "action": "initial_read"
                }
            )
            
        except FileNotFoundError:
            logger.error(f"[{self.name}] File not found: {target_file}")
            
    async def _fix_bug(self, msg: Message):
        """Fix bug dựa trên error report."""
        error = msg.payload.get("error", "")
        
        logger.info(f"[{self.name}] 🔧 Fixing bug: {error}")
        
        ## Demo fix: thay a - b thành a + b
        fixed_code = '''def add(a, b):
    """Add two numbers and return result."""
    return a + b  ## Fixed by CoderAgent
'''
        
        ## Write fixed code
        if self.current_file:
            write_file(self.current_file, fixed_code)
            logger.info(f"[{self.name}] ✅ Code fixed and saved")
            
            ## Gửi lại cho Tester verify
            await self.send(
                to_agent="Tester",
                topic="code_ready",
                payload={
                    "file": self.current_file,
                    "code": fixed_code,
                    "action": "fix_applied"
                }
            )
```

###### 6.2.5 Tester Agent (tester.py)

```python
"""
Tester Agent - Chạy tests và report results.

Responsibilities:
1. Nhận code từ Coder
2. Chạy tests
3. Report kết quả cho Reviewer
"""

from typing import Dict, Any

from app.module.finai_agent.layer_2_cognition.base_agent import P2PAgent
from app.module.finai_agent.layer_2_cognition.message_bus import Message
from app.module.finai_agent.layer_3_action.tools.execution_tools import run_tests
from app.common.log import setup_logger

logger = setup_logger(__name__)


class TesterAgent(P2PAgent):
    """
    Tester Agent: Chạy tests.
    
    Subscribe: code_ready
    Publish: test_result
    Tools: run_tests
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Tester",
            subscribed_topics=["code_ready"],
            **kwargs
        )
        
    async def decide_next_action(self, msg: Message) -> str:
        """Tester quyết định action."""
        if msg.topic == "code_ready":
            return "run_tests"
        return "idle"
        
    async def execute_action(self, action: str, msg: Message):
        """Execute tester actions."""
        
        if action == "run_tests":
            await self._run_tests(msg)
            
    async def _run_tests(self, msg: Message):
        """Chạy tests và report kết quả."""
        file_path = msg.payload.get("file", "")
        
        logger.info(f"[{self.name}] 🧪 Running tests for: {file_path}")
        
        ## Run tests
        output = run_tests()
        passed = "passed" in output.lower() or "ok" in output.lower()
        
        if passed:
            logger.info(f"[{self.name}] ✅ Tests PASSED")
            status = "passed"
        else:
            logger.info(f"[{self.name}] ❌ Tests FAILED")
            status = "failed"
            
        ## Send result to Reviewer
        await self.send(
            to_agent="Reviewer",
            topic="test_result",
            payload={
                "status": status,
                "output": output,
                "file": file_path,
            }
        )
```

###### 6.2.6 Reviewer Agent (reviewer.py)

```python
"""
Reviewer Agent - Review code quality và approve/request fixes.

Responsibilities:
1. Nhận test results từ Tester
2. Review code quality
3. Approve hoặc request fix
"""

from typing import Dict, Any

from app.module.finai_agent.layer_2_cognition.base_agent import P2PAgent
from app.module.finai_agent.layer_2_cognition.message_bus import Message
from app.common.log import setup_logger

logger = setup_logger(__name__)


class ReviewerAgent(P2PAgent):
    """
    Reviewer Agent: Review code quality.
    
    Subscribe: test_result
    Publish: review_done, fix_request
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="Reviewer",
            subscribed_topics=["test_result"],
            **kwargs
        )
        self._fix_attempts = 0
        self._max_fix_attempts = 3
        
    async def decide_next_action(self, msg: Message) -> str:
        """Reviewer quyết định action."""
        
        if msg.topic == "test_result":
            status = msg.payload.get("status", "")
            
            if status == "passed":
                return "approve"
            else:
                return "request_fix"
                
        return "idle"
        
    async def execute_action(self, action: str, msg: Message):
        """Execute reviewer actions."""
        
        if action == "approve":
            await self._approve(msg)
            
        elif action == "request_fix":
            await self._request_fix(msg)
            
    async def _approve(self, msg: Message):
        """Approve code sau khi tests pass."""
        logger.info(f"[{self.name}] ✅ Code APPROVED")
        
        ## Reset fix attempts
        self._fix_attempts = 0
        
        ## Report to Chief
        await self.send(
            to_agent="Chief",
            topic="review_done",
            payload={
                "status": "approved",
                "message": "Code quality OK, tests passed",
                "file": msg.payload.get("file", ""),
            }
        )
        
    async def _request_fix(self, msg: Message):
        """Request Coder để fix bug."""
        self._fix_attempts += 1
        
        if self._fix_attempts > self._max_fix_attempts:
            logger.error(
                f"[{self.name}] ❌ Max fix attempts ({self._max_fix_attempts}) reached"
            )
            await self.send(
                to_agent="Chief",
                topic="review_done",
                payload={
                    "status": "failed",
                    "message": "Max fix attempts reached",
                    "error": msg.payload.get("output", ""),
                }
            )
            return
            
        logger.info(
            f"[{self.name}] 🔍 Bug detected, requesting fix "
            f"(attempt {self._fix_attempts}/{self._max_fix_attempts})"
        )
        
        ## Send fix request to Coder
        await self.send(
            to_agent="Coder",
            topic="fix_request",
            payload={
                "error": msg.payload.get("output", ""),
                "file": msg.payload.get("file", ""),
                "attempt": self._fix_attempts,
            }
        )
```

###### 6.2.7 Entry Point (agent_entrypoint.py)

```python
"""
Agent Entrypoint - Spawn và run all agents.

Đây là entry point cho Multi-Agent System.
"""

import asyncio
from typing import List

from app.module.finai_agent.layer_2_cognition.message_bus import (
    get_message_bus, MessageBus
)
from app.module.finai_agent.layer_2_cognition.chief_agent.chief import ChiefAgent
from app.module.finai_agent.layer_2_cognition.coder_agent.coder import CoderAgent
from app.module.finai_agent.layer_2_cognition.tester_agent.tester import TesterAgent
from app.module.finai_agent.layer_2_cognition.reviewer_agent.reviewer import ReviewerAgent
from app.common.log import setup_logger

logger = setup_logger(__name__)


async def run_multi_agent_system(goal: str, repo_path: str = "."):
    """
    Q4: Spawn 4 agents + run Multi-Agent System.
    
    Args:
        goal: User's goal (e.g., "Fix all failing tests")
        repo_path: Path to target repository
        
    Returns:
        dict: Final result with status and report
    """
    logger.info("=" * 60)
    logger.info("Q4 Hierarchical Choreography: Multi-Agent System")
    logger.info("=" * 60)
    
    ## Get message bus
    bus = get_message_bus()
    bus.clear_history()  ## Clear previous history
    
    ## Spawn agents
    chief = ChiefAgent(bus=bus)
    coder = CoderAgent(bus=bus)
    tester = TesterAgent(bus=bus)
    reviewer = ReviewerAgent(bus=bus)
    
    agents = [chief, coder, tester, reviewer]
    logger.info(f"Spawned {len(agents)} agents: {[a.name for a in agents]}")
    
    ## Run agents in parallel
    agent_tasks = [
        asyncio.create_task(chief.run_loop(timeout=120)),
        asyncio.create_task(coder.run_loop(timeout=120)),
        asyncio.create_task(tester.run_loop(timeout=120)),
        asyncio.create_task(reviewer.run_loop(timeout=120)),
    ]
    
    ## Wait for agents to initialize
    await asyncio.sleep(1)
    
    ## Chief kicks off task
    await chief.broadcast_task(goal, repo_path)
    
    ## Wait for completion or timeout
    try:
        done, pending = await asyncio.wait(
            agent_tasks,
            timeout=120,
            return_when=asyncio.FIRST_COMPLETED
        )
        
        ## Stop all agents
        for agent in agents:
            agent.stop()
            
        ## Cancel pending tasks
        for task in pending:
            task.cancel()
            
    except asyncio.TimeoutError:
        logger.warning("Multi-agent system timeout")
        for agent in agents:
            agent.stop()
            
    ## Get final result from message history
    history = bus.get_history(topic="final_report")
    if history:
        final_msg = history[-1]
        result = {
            "status": "success",
            "report": final_msg.payload.get("report", ""),
        }
    else:
        result = {
            "status": "incomplete",
            "report": "No final report generated",
        }
        
    logger.info("=" * 60)
    logger.info("Multi-Agent Demo Complete")
    logger.info("=" * 60)
    
    return result


## CLI entry point
if __name__ == "__main__":
    result = asyncio.run(
        run_multi_agent_system(
            goal="Fix all failing tests in repo_demo",
            repo_path="tests/fixtures/repo_demo"
        )
    )
    print(f"\nFinal Result: {result}")
```

#### 6.3 Layer 3: Action Tools

###### 6.3.1 File Tools (file_tools.py)

```python
"""
File Tools - Tools để đọc/ghi files trong repository.
"""

import os
from typing import List
from pathlib import Path

from app.common.log import setup_logger

logger = setup_logger(__name__)


def read_file(path: str) -> str:
    """
    Đọc nội dung file.
    
    Args:
        path: Path tới file
        
    Returns:
        str: Nội dung file
        
    Raises:
        FileNotFoundError: Nếu file không tồn tại
    """
    logger.debug(f"Reading file: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    logger.debug(f"Read {len(content)} characters from {path}")
    return content


def write_file(path: str, content: str) -> None:
    """
    Ghi nội dung vào file.
    
    Args:
        path: Path tới file
        content: Nội dung cần ghi
    """
    logger.debug(f"Writing to file: {path}")
    
    ## Ensure directory exists
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    logger.debug(f"Wrote {len(content)} characters to {path}")


def list_files(directory: str = ".") -> List[str]:
    """
    List files trong directory.
    
    Args:
        directory: Path tới directory
        
    Returns:
        List[str]: Danh sách file paths
    """
    logger.debug(f"Listing files in: {directory}")
    
    files = []
    path = Path(directory)
    
    if not path.exists():
        return files
        
    for item in path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            files.append(str(item))
            
    logger.debug(f"Found {len(files)} files")
    return files
```

###### 6.3.2 Execution Tools (execution_tools.py)

```python
"""
Execution Tools - Tools để chạy tests và commands.
"""

import subprocess
from typing import Optional

from app.common.log import setup_logger

logger = setup_logger(__name__)


def run_tests(
    pattern: str = "*",
    directory: str = ".",
    timeout: int = 60
) -> str:
    """
    Chạy tests trong directory.
    
    Args:
        pattern: Test file pattern
        directory: Directory chứa tests
        timeout: Timeout in seconds
        
    Returns:
        str: Test output
    """
    logger.info(f"Running tests in {directory} with pattern {pattern}")
    
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "-v", directory],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=directory if directory != "." else None
        )
        
        output = result.stdout + result.stderr
        
        if result.returncode == 0:
            logger.info("Tests PASSED")
        else:
            logger.warning(f"Tests FAILED (return code: {result.returncode})")
            
        return output
        
    except subprocess.TimeoutExpired:
        logger.error(f"Tests timed out after {timeout}s")
        return f"TIMEOUT: Tests did not complete within {timeout} seconds"
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        return f"ERROR: {str(e)}"


def run_command(
    command: str,
    cwd: Optional[str] = None,
    timeout: int = 30
) -> str:
    """
    Chạy shell command.
    
    Args:
        command: Shell command to run
        cwd: Working directory
        timeout: Timeout in seconds
        
    Returns:
        str: Command output
    """
    logger.debug(f"Running command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        
        return result.stdout + result.stderr
        
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: Command did not complete within {timeout} seconds"
        
    except Exception as e:
        return f"ERROR: {str(e)}"
```

---

### 7. THIẾT KẾ API & CONTRACTS

#### 7.1 API Endpoints

```yaml
openapi: 3.0.3
info:
  title: Multi-Agent Coding System API
  version: 1.0.0
  description: API cho Multi-Agent Coding System (Cursor Demo)

servers:
  - url: http://localhost:8000/api/v1
    description: Development
  - url: https://api.example.com/v1
    description: Production

paths:
  /agent/run:
    post:
      summary: Chạy Multi-Agent System
      operationId: runMultiAgentSystem
      tags: [Agent]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '##/components/schemas/RunAgentRequest'
      responses:
        '200':
          description: Task completed
          content:
            application/json:
              schema:
                $ref: '##/components/schemas/RunAgentResponse'
        '400':
          $ref: '##/components/responses/BadRequest'
        '500':
          $ref: '##/components/responses/InternalError'

  /agent/status/{task_id}:
    get:
      summary: Lấy status của task
      operationId: getTaskStatus
      tags: [Agent]
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task status
          content:
            application/json:
              schema:
                $ref: '##/components/schemas/TaskStatus'

  /agent/history:
    get:
      summary: Lấy message history
      operationId: getMessageHistory
      tags: [Agent]
      parameters:
        - name: topic
          in: query
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: Message history
          content:
            application/json:
              schema:
                $ref: '##/components/schemas/MessageHistory'

components:
  schemas:
    RunAgentRequest:
      type: object
      required: [goal]
      properties:
        goal:
          type: string
          description: Task goal for the multi-agent system
          example: "Fix all failing tests in repo_demo"
        repo_path:
          type: string
          description: Path to repository
          default: "."
        timeout:
          type: integer
          description: Timeout in seconds
          default: 120

    RunAgentResponse:
      type: object
      properties:
        task_id:
          type: string
        status:
          type: string
          enum: [success, failed, timeout]
        report:
          type: string
        duration_ms:
          type: integer

    TaskStatus:
      type: object
      properties:
        task_id:
          type: string
        status:
          type: string
          enum: [pending, running, completed, failed]
        agents_status:
          type: object
          additionalProperties:
            type: string

    MessageHistory:
      type: object
      properties:
        messages:
          type: array
          items:
            $ref: '##/components/schemas/Message'
        total:
          type: integer

    Message:
      type: object
      properties:
        message_id:
          type: string
        from_agent:
          type: string
        to_agent:
          type: string
        topic:
          type: string
        payload:
          type: object
        timestamp:
          type: number

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              details:
                type: object

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              trace_id:
                type: string
```

#### 7.2 WebSocket Protocol

```python
"""
WebSocket Protocol cho real-time agent updates.
"""

## Connection
ws://localhost:8000/ws/agent/{task_id}

## Client -> Server Messages
{
    "type": "subscribe",
    "topics": ["agent_status", "message_bus"]
}

## Server -> Client Messages

## Agent Status Update
{
    "type": "agent_status",
    "data": {
        "agent": "Coder",
        "status": "running",
        "action": "analyze_and_code"
    }
}

## Message Bus Event
{
    "type": "message_bus",
    "data": {
        "from_agent": "Coder",
        "to_agent": "Tester",
        "topic": "code_ready",
        "timestamp": 1702800000
    }
}

## Task Complete
{
    "type": "task_complete",
    "data": {
        "status": "success",
        "report": "..."
    }
}
```

---

### 8. THIẾT KẾ DỮ LIỆU

#### 8.1 State Schema

```python
"""
State Schema cho Multi-Agent System.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class AgentState:
    """State cho một agent."""
    name: str
    status: AgentStatus = AgentStatus.IDLE
    current_action: Optional[str] = None
    last_message_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TaskState:
    """State cho một task."""
    task_id: str
    goal: str
    repo_path: str
    status: TaskStatus = TaskStatus.PENDING
    agents: Dict[str, AgentState] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)  ## Message IDs
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


@dataclass  
class SystemState:
    """Global system state."""
    tasks: Dict[str, TaskState] = field(default_factory=dict)
    active_agents: List[str] = field(default_factory=list)
    message_count: int = 0
```

#### 8.2 Redis Data Structure

```
## Task State
task:{task_id} -> Hash
  - goal: string
  - repo_path: string
  - status: string (pending|running|completed|failed)
  - created_at: timestamp
  - updated_at: timestamp

## Agent State  
task:{task_id}:agent:{agent_name} -> Hash
  - status: string (idle|running|completed|failed)
  - current_action: string
  - last_message_id: string

## Message History
task:{task_id}:messages -> List
  - [message_id_1, message_id_2, ...]

## Message Detail
message:{message_id} -> Hash
  - from_agent: string
  - to_agent: string
  - topic: string
  - payload: json string
  - timestamp: float

## PubSub Channels
channel:task_available
channel:code_ready
channel:test_result
channel:review_done
channel:fix_request
channel:final_report
```

#### 8.3 Data Retention Policy

| Data Type | Retention | Strategy |
|-----------|-----------|----------|
| Task State | 7 ngày | Auto-expire |
| Message History | 24 giờ | Auto-expire |
| Audit Logs | 90 ngày | Archive to S3 |
| Metrics | 30 ngày | Prometheus |

---

### 9. THIẾT KẾ BẢO MẬT

#### 9.1 Threat Model (STRIDE)

| Threat | Mô Tả | Mitigation |
|--------|-------|------------|
| **Spoofing** | Fake agent messages | Agent authentication |
| **Tampering** | Modify code maliciously | Checksum validation |
| **Repudiation** | Deny actions | Audit logging |
| **Information Disclosure** | Leak source code | Access control |
| **Denial of Service** | Flood message bus | Rate limiting |
| **Elevation of Privilege** | Agent escalation | Role-based permissions |

#### 9.2 Input Validation

```python
"""
Input validation cho API và Messages.
"""

from pydantic import BaseModel, validator
import re


class RunAgentRequest(BaseModel):
    goal: str
    repo_path: str = "."
    timeout: int = 120
    
    @validator('goal')
    def validate_goal(cls, v):
        if len(v) < 5:
            raise ValueError('Goal too short')
        if len(v) > 1000:
            raise ValueError('Goal too long')
        ## Check for injection patterns
        if re.search(r'[<>{};\|&]', v):
            raise ValueError('Invalid characters in goal')
        return v
        
    @validator('repo_path')
    def validate_repo_path(cls, v):
        ## Prevent path traversal
        if '..' in v or v.startswith('/'):
            raise ValueError('Invalid repo path')
        return v
        
    @validator('timeout')
    def validate_timeout(cls, v):
        if v < 10 or v > 600:
            raise ValueError('Timeout must be between 10-600 seconds')
        return v
```

#### 9.3 Rate Limiting

```python
"""
Rate limiting configuration.
"""

RATE_LIMITS = {
    "api_requests": {
        "requests": 60,
        "window": 60,  ## 60 requests per minute
    },
    "agent_tasks": {
        "requests": 10,
        "window": 60,  ## 10 tasks per minute
    },
    "message_bus": {
        "requests": 1000,
        "window": 60,  ## 1000 messages per minute
    }
}
```

---

### 10. RESILIENCE & RELIABILITY

#### 10.1 Retry Strategy

```python
"""
Retry configuration cho Message Bus và external calls.
"""

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10, jitter=2),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
async def publish_with_retry(bus, msg):
    await bus.publish(msg)
```

#### 10.2 Circuit Breaker

```python
"""
Circuit breaker cho external services (LLM API).
"""

from pybreaker import CircuitBreaker

llm_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
)

@llm_breaker
async def call_llm(prompt: str):
    return await llm_client.generate(prompt)
```

#### 10.3 Health Checks

```python
"""
Health check endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness():
    """Kubernetes readiness probe."""
    checks = {
        "redis": await check_redis(),
        "message_bus": check_message_bus(),
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    return {"status": "not_ready", "checks": checks}, 503
```

#### 10.4 Graceful Shutdown

```python
"""
Graceful shutdown handling.
"""

import signal
import asyncio


class GracefulShutdown:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        
    def setup(self):
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                sig, self.handle_shutdown
            )
            
    def handle_shutdown(self):
        logger.info("Shutdown signal received")
        self.shutdown_event.set()
        
    async def wait(self):
        await self.shutdown_event.wait()
```

---

### 11. OBSERVABILITY & MONITORING

#### 11.1 Metrics (Prometheus)

```python
"""
Prometheus metrics cho Multi-Agent System.
"""

from prometheus_client import Counter, Histogram, Gauge

## Agent metrics
AGENT_MESSAGES_TOTAL = Counter(
    'agent_messages_total',
    'Total messages sent by agents',
    ['from_agent', 'to_agent', 'topic']
)

AGENT_ACTION_DURATION = Histogram(
    'agent_action_duration_seconds',
    'Duration of agent actions',
    ['agent', 'action'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

ACTIVE_AGENTS = Gauge(
    'active_agents',
    'Number of currently active agents'
)

## Task metrics
TASK_TOTAL = Counter(
    'task_total',
    'Total tasks processed',
    ['status']
)

TASK_DURATION = Histogram(
    'task_duration_seconds',
    'Duration of tasks',
    ['status'],
    buckets=[1, 5, 10, 30, 60, 120, 300]
)
```

#### 11.2 Structured Logging

```python
"""
Structured logging configuration.
"""

import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

## Usage
logger = structlog.get_logger()

logger.info(
    "message_published",
    from_agent="Coder",
    to_agent="Tester",
    topic="code_ready",
    message_id="abc123"
)
```

#### 11.3 Distributed Tracing (LangFuse)

```python
"""
LangFuse tracing cho LLM calls.
"""

from langfuse import observe

@observe(name="chief_analyze_task")
async def analyze_task(goal: str):
    """Analyze task with LangFuse tracing."""
    response = await llm.generate(
        system=CHIEF_SYSTEM_PROMPT,
        user=goal
    )
    return response
```

#### 11.4 Alerting Rules

```yaml
## Prometheus alerting rules
groups:
  - name: multi-agent-alerts
    rules:
      - alert: HighMessageBusLatency
        expr: histogram_quantile(0.95, agent_action_duration_seconds) > 5
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High message bus latency"
          
      - alert: AgentFailureRate
        expr: rate(task_total{status="failed"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High agent failure rate"
          
      - alert: DeadlockDetected
        expr: active_agents > 0 and rate(agent_messages_total[5m]) == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Possible deadlock - agents active but no messages"
```

---

### 12. DEPLOYMENT & OPERATIONS

#### 12.1 Docker Configuration

```dockerfile
## Dockerfile
FROM python:3.11-slim

WORKDIR /app

## Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## Copy application
COPY app/ ./app/

## Environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

## Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

## Run
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 12.2 Docker Compose (Development)

```yaml
## docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - MYSQL_URL=mysql://user:pass@mysql:3306/db
    depends_on:
      - redis
      - mysql
    volumes:
      - ./app:/app/app

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: finai_agent
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  redis_data:
  mysql_data:
```

#### 12.3 Kubernetes Deployment

```yaml
## k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-agent-system
  labels:
    app: multi-agent-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: multi-agent-system
  template:
    metadata:
      labels:
        app: multi-agent-system
    spec:
      containers:
        - name: app
          image: multi-agent-system:latest
          ports:
            - containerPort: 8000
          env:
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: redis-url
          resources:
            requests:
              cpu: 250m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

---

### 13. TESTING STRATEGY

#### 13.1 Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  5%  - Full system tests
                   ─┴─────────┴─
                  ┌─────────────┐
                  │ Integration │  20% - Agent interaction tests
                 ─┴─────────────┴─
                ┌─────────────────┐
                │      Unit       │  75% - Individual agent tests
               ─┴─────────────────┴─
```

#### 13.2 Unit Tests

```python
"""
Unit tests cho individual agents.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.module.finai_agent.layer_2_cognition.message_bus import (
    Message, MessageBus
)
from app.module.finai_agent.layer_2_cognition.coder_agent.coder import CoderAgent


class TestCoderAgent:
    @pytest.fixture
    def mock_bus(self):
        bus = MagicMock(spec=MessageBus)
        bus.publish = AsyncMock()
        return bus
        
    @pytest.fixture
    def coder(self, mock_bus):
        return CoderAgent(bus=mock_bus)
        
    @pytest.mark.asyncio
    async def test_decide_action_task_available(self, coder):
        msg = Message(
            from_agent="Chief",
            to_agent="broadcast",
            topic="task_available",
            payload={"goal": "Fix tests"}
        )
        
        action = await coder.decide_next_action(msg)
        assert action == "analyze_and_code"
        
    @pytest.mark.asyncio
    async def test_decide_action_fix_request(self, coder):
        msg = Message(
            from_agent="Reviewer",
            to_agent="Coder",
            topic="fix_request",
            payload={"error": "Test failed"}
        )
        
        action = await coder.decide_next_action(msg)
        assert action == "fix_bug"
```

#### 13.3 Integration Tests

```python
"""
Integration tests cho multi-agent flow.
"""

import pytest
import asyncio

from app.module.finai_agent.agent_entrypoint import run_multi_agent_system
from app.module.finai_agent.layer_2_cognition.message_bus import get_message_bus


class TestMultiAgentFlow:
    @pytest.fixture
    def setup_test_repo(self, tmp_path):
        """Create test repository with failing tests."""
        ## Create math_utils.py with bug
        math_file = tmp_path / "math_utils.py"
        math_file.write_text('''
def add(a, b):
    return a - b  ## Bug: should be a + b
''')
        
        ## Create test file
        test_file = tmp_path / "test_math.py"
        test_file.write_text('''
from math_utils import add

def test_add():
    assert add(1, 2) == 3
''')
        
        return tmp_path
        
    @pytest.mark.asyncio
    async def test_full_flow_success(self, setup_test_repo):
        """Test complete flow: Chief -> Coder -> Tester -> Reviewer -> Chief"""
        result = await run_multi_agent_system(
            goal="Fix all failing tests",
            repo_path=str(setup_test_repo)
        )
        
        assert result["status"] == "success"
        assert "approved" in result["report"].lower()
        
    @pytest.mark.asyncio
    async def test_message_flow(self, setup_test_repo):
        """Test message flow between agents."""
        bus = get_message_bus()
        bus.clear_history()
        
        await run_multi_agent_system(
            goal="Fix tests",
            repo_path=str(setup_test_repo)
        )
        
        history = bus.get_history()
        
        ## Verify message sequence
        topics = [m.topic for m in history]
        assert "task_available" in topics
        assert "code_ready" in topics
        assert "test_result" in topics
        assert "review_done" in topics
```

#### 13.4 Test Fixtures

```python
"""
Test fixtures for demo repository.
"""

## tests/fixtures/repo_demo/math_utils.py
def add(a, b):
    """Add two numbers - Bug: returns subtraction instead."""
    return a - b  ## Intentional bug for demo

## tests/fixtures/repo_demo/test_math.py
import pytest
from math_utils import add

def test_add_positive():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0
```

---

### 14. BRAINSTORM KIẾN TRÚC MECE

#### 14.1 Các Kiến Trúc Được Phân Tích

Sử dụng framework MECE (Mutually Exclusive, Collectively Exhaustive), chúng tôi phân tích 4 quadrants của Multi-Agent Architecture:

```
                    High Autonomy
                         │
              Q3         │         Q4
         Single Agent    │    Multi-Agent
         Orchestration   │    Choreography
                         │
   ─────────────────────┼─────────────────────
                         │
              Q1         │         Q2
         Single Agent    │    Multi-Agent
         Simple Flow     │    Orchestration
                         │
                    Low Autonomy
```

#### 14.2 Comparison Matrix

| Aspect | Q1: Simple | Q2: Multi-Orch | Q3: Single-Auto | Q4: Multi-Choreo |
|--------|------------|----------------|-----------------|------------------|
| **Agents** | 1 | 4+ | 1 | 4+ |
| **Autonomy** | Low | Low | High | High |
| **Coordination** | Sequential | Centralized | Self-managed | P2P |
| **Complexity** | Low | Medium | Medium | High |
| **Scalability** | Low | Medium | Low | High |
| **Fault Tolerance** | Low | Medium | Medium | High |
| **Use Case** | Simple tasks | Workflow | Smart assistant | Complex collab |

#### 14.3 ADR: Chọn Q4 - Hierarchical Choreography

**Decision**: Chọn Q4 - Multi-Agent với Hierarchical Choreography

**Context**: 
- Cần demo Cursor-style coding với nhiều chuyên gia phối hợp
- Cần parallel execution cho throughput cao
- Cần fault isolation để agent failure không crash hệ thống

**Alternatives Considered**:

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Q1: Simple | Easy to implement | Not scalable | ❌ Rejected |
| Q2: Multi-Orch | Clear flow | Central bottleneck | ❌ Rejected |
| Q3: Single-Auto | Intelligent | Single point of failure | ❌ Rejected |
| **Q4: Multi-Choreo** | Scalable, fault tolerant | Complex | ✅ Selected |

**Consequences**:
- ✅ Parallel execution
- ✅ Fault isolation
- ✅ Scalable architecture
- ⚠️ More complex debugging
- ⚠️ Potential for deadlocks

---

### 15. TRADE-OFFS & ARCHITECTURE DECISIONS

#### 15.1 ADR-001: Message Bus Selection

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Decision** | Redis PubSub over RabbitMQ |
| **Rationale** | Simpler setup, lower latency, sufficient for demo scale |
| **Consequences** | ✅ Fast, ✅ Simple; ⚠️ Less durable than RabbitMQ |

#### 15.2 ADR-002: Agent State Management

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Decision** | Stateless agents + Redis state store |
| **Rationale** | Easier to scale, recover from failures |
| **Consequences** | ✅ Scalable, ✅ Recoverable; ⚠️ Redis dependency |

#### 15.3 ADR-003: P2P vs Centralized Communication

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Decision** | P2P with Chief as facilitator (not orchestrator) |
| **Rationale** | Lower latency, agents can communicate directly |
| **Consequences** | ✅ Faster, ✅ Flexible; ⚠️ Harder to trace |

#### 15.4 Trade-off Analysis

| Trade-off | Option A | Option B | Decision | Reason |
|-----------|----------|----------|----------|--------|
| Latency vs Durability | Low latency (Redis) | High durability (Kafka) | Redis | Demo priority |
| Simplicity vs Flexibility | Fixed workflow | Dynamic choreography | Dynamic | Scalability |
| Single LLM vs Multi | GPT-4 only | Multi-provider | Multi | Fallback needed |

---

### 16. IMPLEMENTATION ROADMAP

#### 16.1 Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      IMPLEMENTATION ROADMAP                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Sprint 1          Sprint 2          Sprint 3          Sprint 4         │
│  Foundation        Core Agents       Integration       Production       │
│  (1 week)          (1 week)          (1 week)          (1 week)         │
│                                                                          │
│  ┌────────┐        ┌────────┐        ┌────────┐        ┌────────┐      │
│  │ Setup  │───────▶│ Agents │───────▶│ Test   │───────▶│ Deploy │      │
│  │ Infra  │        │ Build  │        │ & Fix  │        │ & Demo │      │
│  └────────┘        └────────┘        └────────┘        └────────┘      │
│                                                                          │
│  Deliverables:     Deliverables:     Deliverables:     Deliverables:    │
│  - Message Bus     - Chief Agent     - Integration     - Docker         │
│  - Base Agent      - Coder Agent     - Unit tests      - K8s configs    │
│  - File Tools      - Tester Agent    - Performance     - Documentation  │
│  - Project setup   - Reviewer Agent  - Bug fixes       - Demo ready     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 16.2 Sprint Details

###### Sprint 1: Foundation (Week 1)

| Task | Owner | Effort | Priority |
|------|-------|--------|----------|
| Setup project structure | Backend | 2h | P0 |
| Implement Message Bus | Backend | 4h | P0 |
| Implement Base P2P Agent | Backend | 4h | P0 |
| Implement File Tools | Backend | 2h | P0 |
| Implement Execution Tools | Backend | 2h | P0 |
| Setup tests framework | QA | 2h | P0 |

**Exit Criteria**:
- [ ] Message Bus working với PubSub
- [ ] Base Agent class with subscribe/publish
- [ ] File tools tested
- [ ] Unit tests setup

###### Sprint 2: Core Agents (Week 2)

| Task | Owner | Effort | Priority |
|------|-------|--------|----------|
| Implement Chief Agent | Backend | 8h | P0 |
| Implement Coder Agent | Backend | 6h | P0 |
| Implement Tester Agent | Backend | 4h | P0 |
| Implement Reviewer Agent | Backend | 4h | P0 |
| Unit tests for agents | QA | 4h | P0 |

**Exit Criteria**:
- [ ] All 4 agents implemented
- [ ] Agents can communicate via Message Bus
- [ ] Unit tests passing

###### Sprint 3: Integration (Week 3)

| Task | Owner | Effort | Priority |
|------|-------|--------|----------|
| Integration tests | QA | 8h | P0 |
| API endpoints | Backend | 4h | P0 |
| WebSocket support | Backend | 4h | P1 |
| Bug fixes | Backend | 4h | P0 |
| Performance testing | QA | 4h | P1 |

**Exit Criteria**:
- [ ] Full flow working end-to-end
- [ ] API documentation complete
- [ ] Performance baseline established

###### Sprint 4: Production (Week 4)

| Task | Owner | Effort | Priority |
|------|-------|--------|----------|
| Docker setup | DevOps | 4h | P0 |
| Kubernetes configs | DevOps | 4h | P1 |
| Monitoring setup | DevOps | 4h | P1 |
| Documentation | All | 4h | P0 |
| Demo preparation | All | 4h | P0 |

**Exit Criteria**:
- [ ] Deployable to K8s
- [ ] Monitoring working
- [ ] Demo ready

---

### 17. PRODUCTION READINESS CHECKLIST

#### 17.1 Pre-Launch Checklist

###### Architecture ✅
- [ ] 4-layer architecture implemented
- [ ] Message Bus working
- [ ] All 4 agents functional
- [ ] P2P communication verified

###### Reliability ✅
- [ ] Retry logic implemented
- [ ] Circuit breaker for LLM calls
- [ ] Timeout handling
- [ ] Graceful shutdown

###### Observability ✅
- [ ] Prometheus metrics
- [ ] Structured logging
- [ ] LangFuse tracing
- [ ] Alerting rules

###### Security ✅
- [ ] Input validation
- [ ] Rate limiting
- [ ] Audit logging

###### Testing ✅
- [ ] Unit tests >75% coverage
- [ ] Integration tests passing
- [ ] Load testing completed

###### Deployment ✅
- [ ] Docker image built
- [ ] K8s manifests ready
- [ ] Health checks working

#### 17.2 Launch Day Checklist

###### T-24 Hours
- [ ] Final deployment to staging
- [ ] Smoke tests passed
- [ ] Monitoring verified
- [ ] On-call team confirmed

###### T-1 Hour
- [ ] All systems green
- [ ] Rollback plan reviewed
- [ ] Stakeholders notified

###### Launch
- [ ] Deploy to production
- [ ] Monitor error rates
- [ ] Monitor latency
- [ ] Ready to rollback

###### T+1 Hour
- [ ] Metrics within SLO
- [ ] No critical bugs
- [ ] Demo successful 🎉

---

### APPENDIX

#### A. Glossary

| Term | Definition |
|------|------------|
| P2P | Peer-to-Peer communication |
| Choreography | Decentralized coordination pattern |
| Message Bus | Central message routing system |
| LangGraph | Framework for multi-agent applications |

#### B. References

- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- Redis PubSub: https://redis.io/docs/manual/pubsub/
- FastAPI: https://fastapi.tiangolo.com/
- LangFuse: https://langfuse.com/docs

#### C. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-17 | AI Team | Initial draft |

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-17  
**Status**: Draft

---

*Tài liệu này được tạo theo Software Design Document Ultimate Template v5.0*



---
Đã hoàn thành **Software Design Document (SDD)** chi tiết cho dự án **Multi-Agent Coding System - Cursor Demo**. Tài liệu bao gồm khoảng **30+ trang** với các nội dung chính:

### 📋 Tóm Tắt Nội Dung SDD

#### Phần I: Nền Tảng & Kiến Trúc

- **Executive Summary**: Tổng quan hệ thống Multi-Agent với Q4 Hierarchical Choreography
- **Architecture**: 4-Layer Architecture (Governance → Perception → Cognition → Action)
- **Agent Design**: 4 agents chuyên biệt (Chief, Coder, Tester, Reviewer) + Message Bus

#### Phần II: Chi Tiết Triển Khai

- **LLD chi tiết**: Code mẫu cho từng component
    - `message_bus.py` - Redis PubSub wrapper
    - `base_agent.py` - Base class cho P2P agents
    - `chief.py`, `coder.py`, `tester.py`, `reviewer.py` - Implementation agents
    - `file_tools.py`, `execution_tools.py` - Action layer tools
- **API Design**: OpenAPI spec cho REST endpoints
- **Data Design**: Redis data structures cho state management

#### Phần III: Production Readiness

- **Resilience**: Retry strategy, Circuit breaker, Health checks
- **Observability**: Prometheus metrics, Structured logging, LangFuse tracing
- **Deployment**: Docker, Kubernetes configs

#### Phần IV: Phân Tích Kiến Trúc

- **MECE Brainstorm**: So sánh 4 quadrants (Q1-Q4)
- **ADRs**: Architecture Decision Records cho các lựa chọn quan trọng
- **Trade-offs**: Phân tích đánh đổi giữa các options

#### Phần V: Roadmap

- **4 Sprints** trong 4 tuần
- **Production Checklist** đầy đủ

### 🔑 Highlights

- **Kiến trúc Q4** được chọn vì: Parallel execution, Fault isolation, Scalability
- **P2P Communication** qua Redis PubSub cho low latency
- **4 Agents** với roles rõ ràng và topics subscribe/publish được định nghĩa
- **Code mẫu** chi tiết có thể implement ngay

---
# BẢN CẬP NHẬT: SDD Multi-Agent Coding System - UPDATE NOTES

## Tài Liệu Cập Nhật Để Mapping Với Source Code FinAI

**Version**: 1.0  
**Date**: 2025-12-17  
**Status**: Required Updates Identified

---

## 📋 TÓM TẮT THAY ĐỔI

| # | Hạng Mục | SDD Hiện Tại | Cần Update Thành | Priority |
|---|----------|--------------|------------------|----------|
| 1 | File Structure | `app/module/finai_agent/` | `app/module/agent/multi_agent_coding/` | P0 |
| 2 | Base Class | Custom `P2PAgent` | Extend `BaseAgent` + Mixin | P0 |
| 3 | Agent Registration | Không có | Dùng `@agent` decorator | P0 |
| 4 | Dependency Injection | Không có | Dùng `DependencyResolver` | P0 |
| 5 | State Model | Custom state | Extend `BaseState` | P0 |
| 6 | Kafka Integration | Manual | Tự động từ `BaseAgent` | P1 |
| 7 | LangFuse Tracing | Custom setup | Đã có sẵn trong `BaseAgent` | P1 |
| 8 | Auto-discovery | Không đề cập | Factory auto-discover | P1 |
| 9 | Message Bus | In-memory only | Tích hợp `graph_pub_sub.py` | P1 |
| 10 | Input Validation | Custom | Dùng Pydantic + `input_model` | P2 |

---

## 1. CẬP NHẬT FILE STRUCTURE

### ❌ SDD Hiện Tại

```
app/module/finai_agent/
├── layer_0_governance/
├── layer_1_perception/
├── layer_2_cognition/
│   ├── message_bus.py
│   ├── base_agent.py          # Custom P2PAgent
│   ├── chief_agent/
│   ├── coder_agent/
│   └── ...
└── layer_3_action/
```

### ✅ Nên Update Thành

```
app/module/agent/multi_agent_coding/
├── __init__.py
├── agent.py                    # Main entry + @agent decorator (REQUIRED for auto-discovery)
├── models.py                   # Input models + State models
├── config.py                   # Configuration
│
├── message_bus/
│   ├── __init__.py
│   ├── bus.py                  # MessageBus class (extend from graph_pub_sub pattern)
│   ├── topics.py               # MessageTopic enum
│   └── models.py               # Message dataclass
│
├── agents/                     # Individual agents (NOT separate folders)
│   ├── __init__.py
│   ├── base_p2p_agent.py       # P2PMixin class
│   ├── chief.py
│   ├── coder.py
│   ├── tester.py
│   └── reviewer.py
│
├── tools/
│   ├── __init__.py
│   ├── file_tools.py
│   └── execution_tools.py
│
├── governance/                 # Optional: Keep governance layer
│   ├── input_gate.py
│   └── output_gate.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_multi_agent.py
```

### 📝 Lý Do

- `AgentFactory` auto-discover từ `app.module.agent` package
- Cần có file `agent.py` để trigger registration
- Flatten structure để dễ maintain

---

## 2. CẬP NHẬT BASE AGENT PATTERN

### ❌ SDD Hiện Tại - Custom P2PAgent

```python
# SDD định nghĩa class mới hoàn toàn
class P2PAgent(ABC):
    def __init__(self, name: str, subscribed_topics: List[str], bus: MessageBus = None):
        self.name = name
        self.inbox = asyncio.Queue()
        self.bus = bus or get_message_bus()
        # ...
```

### ✅ Nên Update - Extend BaseAgent + Mixin

```python
# app/module/agent/multi_agent_coding/agents/base_p2p_agent.py

from typing import List, Dict, Any
from abc import abstractmethod
import asyncio

from app.common.agent.base import BaseAgent
from app.common.agent.models import BaseState
from app.common.log import setup_logger

from ..message_bus.bus import MessageBus, get_message_bus
from ..message_bus.models import Message

logger = setup_logger(__name__)


class P2PMixin:
    """
    Mixin để thêm P2P communication capabilities vào BaseAgent.
    
    Mixin này KHÔNG replace BaseAgent mà BỔ SUNG thêm:
    - Subscribe/Publish qua Message Bus
    - Autonomous run loop
    - P2P messaging
    
    Usage:
        class MyAgent(P2PMixin, BaseAgent):
            subscribed_topics = ["task_available", "fix_request"]
            # ...
    """
    
    # Class attributes - override trong subclass
    subscribed_topics: List[str] = []
    agent_name: str = "unnamed"
    
    def __init__(self, **kwargs):
        # Call BaseAgent.__init__ first
        super().__init__(**kwargs)
        
        # P2P specific initialization
        self.inbox: asyncio.Queue = asyncio.Queue()
        self._bus: MessageBus = None
        self._running = False
        
    @property
    def bus(self) -> MessageBus:
        """Lazy load message bus."""
        if self._bus is None:
            self._bus = get_message_bus()
            # Subscribe to topics
            for topic in self.subscribed_topics:
                self._bus.subscribe(topic, self._on_message)
        return self._bus
        
    async def _on_message(self, msg: Message):
        """Callback khi nhận message từ bus."""
        if msg.to_agent in ["broadcast", self.agent_name]:
            await self.inbox.put(msg)
            logger.debug(f"[{self.agent_name}] 📬 Received: {msg.topic}")
            
    async def send_p2p(self, to_agent: str, topic: str, payload: Dict[str, Any]):
        """Send P2P message qua Message Bus."""
        msg = Message(
            from_agent=self.agent_name,
            to_agent=to_agent,
            topic=topic,
            payload=payload,
        )
        await self.bus.publish(msg)
        
    @abstractmethod
    async def decide_next_action(self, msg: Message) -> str:
        """Agent tự quyết định action tiếp theo."""
        pass
        
    @abstractmethod
    async def execute_action(self, action: str, msg: Message):
        """Execute action đã quyết định."""
        pass
        
    async def p2p_run_loop(self, timeout: float = 300):
        """
        Autonomous P2P run loop.
        
        Note: Đây là THÊM vào, không thay thế BaseAgent.run_async()
        """
        self._running = True
        logger.info(f"[{self.agent_name}] 🚀 P2P loop started")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            while self._running:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.warning(f"[{self.agent_name}] ⏰ Timeout")
                    break
                    
                try:
                    msg = await asyncio.wait_for(self.inbox.get(), timeout=5.0)
                    action = await self.decide_next_action(msg)
                    
                    if action == "STOP":
                        break
                        
                    await self.execute_action(action, msg)
                    
                except asyncio.TimeoutError:
                    continue
                    
        finally:
            self._running = False
            logger.info(f"[{self.agent_name}] Stopped")
            
    def stop_p2p(self):
        """Signal agent to stop P2P loop."""
        self._running = False
```

### 📝 Key Changes

| Aspect | SDD Hiện Tại | Sau Update |
|--------|--------------|------------|
| Inheritance | `P2PAgent(ABC)` | `P2PMixin + BaseAgent` |
| LangGraph | Không có | Kế thừa từ `BaseAgent.graph` |
| Kafka | Không có | Kế thừa từ `BaseAgent.send_kafka_one()` |
| Tracing | Không có | Kế thừa `@observe` decorator |

---

## 3. CẬP NHẬT AGENT REGISTRATION

### ❌ SDD Hiện Tại - Không Có Registration

```python
# SDD không sử dụng registry
class ChiefAgent(P2PAgent):
    def __init__(self, llm=None, **kwargs):
        super().__init__(
            name="Chief",
            subscribed_topics=["code_ready", "test_result", "review_done"],
            **kwargs
        )
```

### ✅ Nên Update - Dùng @agent Decorator

```python
# app/module/agent/multi_agent_coding/agent.py
"""
Multi-Agent Coding System - Main Entry Point.

File này PHẢI có để AgentFactory auto-discover.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal

from app.common.agent.base import BaseAgent
from app.common.agent.decorators import agent
from app.common.agent.models import BaseState
from app.common.log import setup_logger

from .agents.chief import ChiefAgentLogic
from .agents.base_p2p_agent import P2PMixin
from .message_bus.bus import get_message_bus

logger = setup_logger(__name__)


# ══════════════════════════════════════════════════════════════
# INPUT MODELS (API Input)
# ══════════════════════════════════════════════════════════════

class MultiAgentInput(BaseModel):
    """Input model cho API endpoint."""
    goal: str = Field(..., min_length=5, max_length=1000, description="Task goal")
    repo_path: str = Field(default=".", description="Repository path")
    timeout: int = Field(default=120, ge=10, le=600, description="Timeout in seconds")
    

# ══════════════════════════════════════════════════════════════
# STATE MODEL (Internal State)
# ══════════════════════════════════════════════════════════════

class MultiAgentState(BaseState):
    """State model cho LangGraph."""
    # Input
    goal: str = ""
    repo_path: str = "."
    timeout: int = 120
    
    # Progress
    current_phase: str = "init"
    agents_status: dict = {}
    messages_processed: int = 0
    
    # Results
    final_report: Optional[str] = None
    error: Optional[str] = None


def convert_input_to_state(input_model: MultiAgentInput) -> MultiAgentState:
    """Convert API input to internal state."""
    return MultiAgentState(
        goal=input_model.goal,
        repo_path=input_model.repo_path,
        timeout=input_model.timeout,
    )


# ══════════════════════════════════════════════════════════════
# MAIN AGENT (Registered with @agent decorator)
# ══════════════════════════════════════════════════════════════

@agent(
    agent_id="multi_agent_coding",
    name="Multi-Agent Coding System",
    description="Q4 Hierarchical Choreography system with Chief, Coder, Tester, Reviewer agents",
    input_model=MultiAgentInput,
    state_model=MultiAgentState,
    input_to_state=convert_input_to_state,
    kafka_topic="multi_agent_coding_events",
    dependency_specs={
        "kafka": "kafka_producer",      # Inject Kafka producer
        "redis": "redis_client",        # Inject Redis client
        # Thêm dependencies khác nếu cần
    }
)
class MultiAgentCodingSystem(P2PMixin, BaseAgent[MultiAgentState]):
    """
    Multi-Agent Coding System - Cursor Demo.
    
    Đây là ORCHESTRATOR agent, quản lý các sub-agents:
    - ChiefAgent
    - CoderAgent
    - TesterAgent
    - ReviewerAgent
    
    Flow:
    1. API call → MultiAgentCodingSystem.run_async()
    2. Spawn sub-agents
    3. Chief broadcasts task
    4. Sub-agents communicate via Message Bus
    5. Collect results → Return
    """
    
    agent_name = "Orchestrator"
    subscribed_topics = ["final_report"]  # Only listen for final results
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Build LangGraph for orchestration
        from langgraph.graph import StateGraph, START, END
        
        builder = StateGraph(MultiAgentState)
        
        # Nodes
        builder.add_node("spawn_agents", self._spawn_agents)
        builder.add_node("wait_for_completion", self._wait_for_completion)
        builder.add_node("collect_results", self._collect_results)
        
        # Edges
        builder.add_edge(START, "spawn_agents")
        builder.add_edge("spawn_agents", "wait_for_completion")
        builder.add_edge("wait_for_completion", "collect_results")
        builder.add_edge("collect_results", END)
        
        self.graph = builder.compile()
        
    async def _spawn_agents(self, state: MultiAgentState) -> dict:
        """Spawn all sub-agents."""
        logger.info("[Orchestrator] Spawning sub-agents...")
        
        # Import and create sub-agents
        from .agents.chief import ChiefAgent
        from .agents.coder import CoderAgent
        from .agents.tester import TesterAgent
        from .agents.reviewer import ReviewerAgent
        
        bus = get_message_bus()
        
        self.chief = ChiefAgent(bus=bus)
        self.coder = CoderAgent(bus=bus)
        self.tester = TesterAgent(bus=bus)
        self.reviewer = ReviewerAgent(bus=bus)
        
        return {"current_phase": "agents_spawned"}
        
    async def _wait_for_completion(self, state: MultiAgentState) -> dict:
        """Run agents and wait for completion."""
        import asyncio
        
        # Start all agent loops
        tasks = [
            asyncio.create_task(self.chief.p2p_run_loop(state.timeout)),
            asyncio.create_task(self.coder.p2p_run_loop(state.timeout)),
            asyncio.create_task(self.tester.p2p_run_loop(state.timeout)),
            asyncio.create_task(self.reviewer.p2p_run_loop(state.timeout)),
        ]
        
        # Wait a bit for agents to initialize
        await asyncio.sleep(1)
        
        # Chief kicks off task
        await self.chief.broadcast_task(state.goal, state.repo_path)
        
        # Wait for completion
        try:
            await asyncio.wait(tasks, timeout=state.timeout)
        except asyncio.TimeoutError:
            logger.warning("[Orchestrator] Timeout reached")
            
        # Stop all agents
        self.chief.stop_p2p()
        self.coder.stop_p2p()
        self.tester.stop_p2p()
        self.reviewer.stop_p2p()
        
        return {"current_phase": "completed"}
        
    async def _collect_results(self, state: MultiAgentState) -> dict:
        """Collect final results from message bus."""
        history = self.bus.get_history(topic="final_report")
        
        if history:
            final_msg = history[-1]
            return {
                "final_report": final_msg.payload.get("report", ""),
                "status": "success",
            }
        else:
            return {
                "final_report": "No report generated",
                "status": "error",
                "error": "Agents did not produce final report",
            }
```

### 📝 Key Points

1. **File `agent.py` là BẮT BUỘC** - Factory auto-discover từ đây
2. **Dùng `@agent` decorator** thay vì manual registration
3. **`input_model`** cho API validation
4. **`state_model`** extend từ `BaseState`
5. **`dependency_specs`** để inject dependencies

---

## 4. CẬP NHẬT SUB-AGENTS

### ❌ SDD Hiện Tại

```python
class CoderAgent(P2PAgent):
    def __init__(self, llm=None, **kwargs):
        super().__init__(
            name="Coder",
            subscribed_topics=["task_available", "fix_request"],
            **kwargs
        )
        self.llm = llm
```

### ✅ Nên Update

```python
# app/module/agent/multi_agent_coding/agents/coder.py

from typing import Dict, Any

from app.common.log import setup_logger
from .base_p2p_agent import P2PMixin
from ..message_bus.models import Message
from ..tools.file_tools import read_file, write_file, list_files

logger = setup_logger(__name__)


class CoderAgent(P2PMixin):
    """
    Coder Agent - Chuyên viết và sửa code.
    
    Note: KHÔNG cần @agent decorator vì đây là sub-agent,
    được quản lý bởi MultiAgentCodingSystem.
    """
    
    agent_name = "Coder"
    subscribed_topics = ["task_available", "fix_request"]
    
    def __init__(self, bus=None, llm=None, **kwargs):
        self._bus = bus
        self.llm = llm
        self.inbox = __import__('asyncio').Queue()
        self._running = False
        self.current_file = None
        
    async def decide_next_action(self, msg: Message) -> str:
        if msg.topic == "task_available":
            return "analyze_and_code"
        elif msg.topic == "fix_request":
            return "fix_bug"
        return "idle"
        
    async def execute_action(self, action: str, msg: Message):
        if action == "analyze_and_code":
            await self._analyze_and_code(msg)
        elif action == "fix_bug":
            await self._fix_bug(msg)
            
    async def _analyze_and_code(self, msg: Message):
        """Phân tích và sửa code."""
        repo_path = msg.payload.get("repo_path", ".")
        goal = msg.payload.get("goal", "")
        
        logger.info(f"[{self.agent_name}] 🔍 Analyzing: {goal}")
        
        files = list_files(repo_path)
        logger.info(f"[{self.agent_name}] Files: {files}")
        
        # Find and read main file
        target_file = f"{repo_path}/math_utils.py"
        try:
            code = read_file(target_file)
            self.current_file = target_file
            
            await self.send_p2p(
                to_agent="Tester",
                topic="code_ready",
                payload={"file": target_file, "code": code, "action": "initial_read"}
            )
        except FileNotFoundError:
            logger.error(f"[{self.agent_name}] File not found: {target_file}")
            
    async def _fix_bug(self, msg: Message):
        """Fix bug dựa trên error report."""
        error = msg.payload.get("error", "")
        logger.info(f"[{self.agent_name}] 🔧 Fixing: {error}")
        
        fixed_code = '''def add(a, b):
    """Add two numbers."""
    return a + b  # Fixed by CoderAgent
'''
        
        if self.current_file:
            write_file(self.current_file, fixed_code)
            logger.info(f"[{self.agent_name}] ✅ Fixed")
            
            await self.send_p2p(
                to_agent="Tester",
                topic="code_ready",
                payload={"file": self.current_file, "code": fixed_code, "action": "fix_applied"}
            )
```

---

## 5. CẬP NHẬT MESSAGE BUS

### ❌ SDD Hiện Tại

```python
# In-memory only
class MessageBus:
    def __init__(self):
        self.subscribers = {}
        self.message_history = []
```

### ✅ Nên Update - Tích Hợp Redis PubSub

```python
# app/module/agent/multi_agent_coding/message_bus/bus.py

"""
Message Bus với Redis PubSub support.

Tham khảo: app/common/redis/graph_pub_sub.py
"""

import asyncio
import json
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime

import redis.asyncio as redis

from app.common.log import setup_logger
from app.common.config import settings

logger = setup_logger(__name__)


@dataclass
class Message:
    """Message schema cho inter-agent communication."""
    from_agent: str
    to_agent: str
    topic: str
    payload: Dict
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    message_id: str = field(default_factory=lambda: __import__('uuid').uuid4().hex[:8])


class MessageBus:
    """
    Message Bus với dual-mode:
    - In-memory: Cho development/testing
    - Redis PubSub: Cho production (multi-worker support)
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
        self._lock = asyncio.Lock()
        
        # Redis support
        self.redis_url = redis_url or getattr(settings, 'REDIS_URL', None)
        self.redis_client: Optional[redis.Redis] = None
        self._pubsub = None
        self._listener_task = None
        
    async def connect_redis(self):
        """Connect to Redis for production mode."""
        if self.redis_url:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            self._pubsub = self.redis_client.pubsub()
            logger.info("[MessageBus] Connected to Redis")
            
    async def disconnect_redis(self):
        """Disconnect from Redis."""
        if self._listener_task:
            self._listener_task.cancel()
        if self._pubsub:
            await self._pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
            
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.debug(f"[MessageBus] Subscribed to '{topic}'")
        
    async def publish(self, msg: Message):
        """Publish message to all subscribers."""
        async with self._lock:
            self.message_history.append(msg)
            
        logger.info(f"[MessageBus] 📨 {msg.from_agent} → {msg.to_agent} | {msg.topic}")
        
        # Local subscribers
        tasks = []
        for callback in self.subscribers.get(msg.topic, []):
            tasks.append(asyncio.create_task(callback(msg)))
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        # Redis publish (for multi-worker)
        if self.redis_client:
            await self.redis_client.publish(
                f"multi_agent:{msg.topic}",
                json.dumps({
                    "from_agent": msg.from_agent,
                    "to_agent": msg.to_agent,
                    "topic": msg.topic,
                    "payload": msg.payload,
                    "timestamp": msg.timestamp,
                    "message_id": msg.message_id,
                })
            )
            
    def get_history(self, topic: str = None, limit: int = 100) -> List[Message]:
        """Get message history."""
        if topic:
            return [m for m in self.message_history if m.topic == topic][-limit:]
        return self.message_history[-limit:]
        
    def clear_history(self):
        """Clear message history."""
        self.message_history.clear()


# Singleton instance
_bus_instance: Optional[MessageBus] = None


def get_message_bus() -> MessageBus:
    """Get or create MessageBus singleton."""
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = MessageBus()
    return _bus_instance


def reset_message_bus():
    """Reset message bus (for testing)."""
    global _bus_instance
    if _bus_instance:
        _bus_instance.clear_history()
    _bus_instance = None
```

---

## 6. CẬP NHẬT API ENDPOINT

### ❌ SDD Hiện Tại

```python
@router.post("/agent/run")
async def run_agent(request: RunAgentRequest):
    result = await run_multi_agent_system(request.goal, request.repo_path)
    return result
```

### ✅ Nên Update - Dùng Factory Pattern

```python
# app/api/routes/multi_agent.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.common.agent.factory import AgentFactory
from app.common.dependency_resolver import DependencyResolver
from app.common.log import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/multi-agent", tags=["Multi-Agent Coding"])


def get_agent_factory() -> AgentFactory:
    """Dependency injection for AgentFactory."""
    resolver = DependencyResolver()
    # Register dependencies
    # resolver.register("kafka_producer", singleton=kafka_producer)
    # resolver.register("redis_client", singleton=redis_client)
    return AgentFactory(resolver)


@router.post("/run")
async def run_multi_agent_system(
    goal: str,
    repo_path: str = ".",
    timeout: int = 120,
    factory: AgentFactory = Depends(get_agent_factory)
) -> Dict[str, Any]:
    """
    Chạy Multi-Agent Coding System.
    
    Flow:
    1. Factory.get_agent() → Get registered agent
    2. agent.run_async() → Execute LangGraph
    3. Return results
    """
    try:
        # Get agent from factory (auto-discovered and cached)
        agent = factory.get_agent("multi_agent_coding")
        
        # Get config for input conversion
        config = factory.get_agent_config("multi_agent_coding")
        
        # Create input model
        input_data = config.input_model(
            goal=goal,
            repo_path=repo_path,
            timeout=timeout
        )
        
        # Convert to state
        state = config.input_to_state(input_data)
        
        # Run agent
        result = await agent.run_async(state)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Multi-agent system error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 7. CẬP NHẬT DEPENDENCIES

### ❌ SDD Hiện Tại

```python
# Không đề cập dependency injection
class ChiefAgent:
    def __init__(self, llm=None):
        self.llm = llm
```

### ✅ Nên Update

```python
# Trong @agent decorator
@agent(
    agent_id="multi_agent_coding",
    # ...
    dependency_specs={
        "kafka": "kafka_producer",
        "redis": "redis_client",
        "llm": "openai_client",
        "db": "database_manager",
    }
)

# Dependencies được inject tự động qua **kwargs
class MultiAgentCodingSystem(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.kafka, self.redis, self.llm, self.db đã được set
```

### 📝 Cách Register Dependencies

```python
# app/common/lifespans.py hoặc app/container.py

from app.common.dependency_resolver import DependencyResolver

resolver = DependencyResolver()

# Register singletons
resolver.register("kafka_producer", singleton=kafka_producer_instance)
resolver.register("redis_client", singleton=redis_client_instance)

# Register factories (lazy creation)
resolver.register("database_manager", factory=lambda: DatabaseManager())
resolver.register("openai_client", factory=lambda: OpenAIClient(api_key=settings.OPENAI_API_KEY))
```

---

## 8. CẬP NHẬT TESTING

### ❌ SDD Hiện Tại

```python
# Test không sử dụng fixtures của project
def test_coder_agent():
    coder = CoderAgent()
    # ...
```

### ✅ Nên Update

```python
# app/module/agent/multi_agent_coding/tests/conftest.py

import pytest
from unittest.mock import MagicMock, AsyncMock

from app.common.agent.registry import AgentRegistry


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before each test."""
    AgentRegistry.clear_registry()
    yield
    AgentRegistry.clear_registry()


@pytest.fixture
def mock_bus():
    """Mock MessageBus."""
    bus = MagicMock()
    bus.publish = AsyncMock()
    bus.subscribe = MagicMock()
    bus.get_history = MagicMock(return_value=[])
    return bus


@pytest.fixture
def mock_dependencies():
    """Mock dependencies for agents."""
    return {
        "kafka": MagicMock(),
        "redis": MagicMock(),
        "llm": MagicMock(),
    }


# app/module/agent/multi_agent_coding/tests/test_coder.py

import pytest
from ..agents.coder import CoderAgent
from ..message_bus.models import Message


class TestCoderAgent:
    @pytest.fixture
    def coder(self, mock_bus):
        return CoderAgent(bus=mock_bus)
        
    @pytest.mark.asyncio
    async def test_decide_action_task_available(self, coder):
        msg = Message(
            from_agent="Chief",
            to_agent="broadcast",
            topic="task_available",
            payload={"goal": "Fix tests"}
        )
        
        action = await coder.decide_next_action(msg)
        assert action == "analyze_and_code"
        
    @pytest.mark.asyncio
    async def test_decide_action_fix_request(self, coder):
        msg = Message(
            from_agent="Reviewer",
            to_agent="Coder",
            topic="fix_request",
            payload={"error": "Test failed"}
        )
        
        action = await coder.decide_next_action(msg)
        assert action == "fix_bug"
```

---

## 9. CHECKLIST IMPLEMENTATION

### Phase 1: Setup (Day 1-2)

- [ ] Tạo folder structure mới: `app/module/agent/multi_agent_coding/`
- [ ] Tạo `agent.py` với `@agent` decorator
- [ ] Tạo `models.py` với Input/State models
- [ ] Tạo `message_bus/` package

### Phase 2: Agents (Day 3-4)

- [ ] Implement `P2PMixin` trong `base_p2p_agent.py`
- [ ] Migrate `ChiefAgent` sang pattern mới
- [ ] Migrate `CoderAgent`
- [ ] Migrate `TesterAgent`
- [ ] Migrate `ReviewerAgent`

### Phase 3: Integration (Day 5)

- [ ] Implement `MultiAgentCodingSystem` orchestrator
- [ ] Setup API route với Factory pattern
- [ ] Test auto-discovery
- [ ] Integration tests

### Phase 4: Polish (Day 6-7)

- [ ] Add Redis PubSub support
- [ ] Add Kafka event logging
- [ ] Documentation
- [ ] Demo preparation

---

## 10. TÓM TẮT THAY ĐỔI QUAN TRỌNG

| Component | Thay Đổi | Lý Do |
|-----------|----------|-------|
| **File Structure** | Đặt trong `app/module/agent/` | Auto-discovery |
| **Base Class** | Dùng `P2PMixin + BaseAgent` | Tái sử dụng framework |
| **Registration** | Dùng `@agent` decorator | Consistency |
| **Dependencies** | Dùng `dependency_specs` | DI pattern |
| **State** | Extend `BaseState` | Compatibility |
| **Message Bus** | Thêm Redis support | Multi-worker |
| **API** | Dùng `AgentFactory` | Factory pattern |

---

## 📎 REFERENCES

- `app/common/agent/base.py` - BaseAgent class
- `app/common/agent/registry.py` - AgentRegistry
- `app/common/agent/factory.py` - AgentFactory
- `app/common/agent/decorators.py` - @agent decorator
- `app/common/dependency_resolver.py` - DependencyResolver
- `app/common/redis/graph_pub_sub.py` - Redis PubSub pattern
- `app/module/agent/talk_agent/agent.py` - Reference implementation

---

*Document Version: 1.0*  
*Last Updated: 2025-12-17*
