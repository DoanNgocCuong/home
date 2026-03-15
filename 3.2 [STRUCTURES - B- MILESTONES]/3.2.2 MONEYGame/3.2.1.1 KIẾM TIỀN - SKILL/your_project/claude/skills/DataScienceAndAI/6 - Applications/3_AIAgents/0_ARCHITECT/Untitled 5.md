# SOFTWARE DESIGN DOCUMENT (SDD) - ULTIMATE TEMPLATE

**Production Quality Standard | Version 5.0 ULTIMATE**

> 🎯 **Template này kết hợp 100% best practices từ:**
> - IEEE 1016-2009 Standard
> - Google Design Docs & SRE Book  
> - AWS Well-Architected Framework
> - Netflix/Stripe/Meta Production Standards
> - 40-Chapter Production Quality Guide
> - MLOps Best Practices

---

## 📋 DOCUMENT METADATA

```yaml
# ============================================
# DOCUMENT INFORMATION
# ============================================
Title: "[Tên Project/Module]"
Document_ID: "SDD-[PROJECT]-[MODULE]-[VERSION]"

# Ownership
Author: "[Primary Engineer/Architect]"
Co_Authors: 
  - "[Name 1]"
  - "[Name 2]"

# Review & Approval
Reviewers:
  Technical_Lead: "[Name]"
  Product_Manager: "[Name]"
  Security_Engineer: "[Name]"
  QA_Lead: "[Name]"
  ML_Engineer: "[Name]"  # If MLOps applicable
Approved_By: "[Name, Role]"

# Status Tracking
Status: "[Draft | In Review | Approved | Implemented | Deprecated]"
Priority: "[P0-Critical | P1-High | P2-Medium | P3-Low]"

# Timeline
Created_Date: "YYYY-MM-DD"
Last_Updated: "YYYY-MM-DD"
Target_Release: "YYYY-MM-DD (Sprint/Quarter)"
Review_Deadline: "YYYY-MM-DD"

# Versioning (Semantic: X.Y.Z)
Version: "X.Y.Z"

# Related Documents
Related_Docs:
  PRD: "[Link]"
  API_Spec: "[Link]"
  UI_Design: "[Link]"
  Test_Plan: "[Link]"
  Runbook: "[Link]"
  Postmortem_Template: "[Link]"
```

---

## 📖 TABLE OF CONTENTS

### Part I: Foundation & Architecture
1. [Executive Summary (TL;DR)](#1-executive-summary-tldr)
2. [Introduction](#2-introduction)
3. [Goals, Scope & Constraints](#3-goals-scope--constraints)
4. [System Overview](#4-system-overview)
5. [High-Level Design (HLD)](#5-high-level-design-hld)
6. [Low-Level Design (LLD)](#6-low-level-design-lld)

### Part II: Implementation Details
7. [API Design & Contracts](#7-api-design--contracts)
8. [Data Design](#8-data-design)
9. [Security Design](#9-security-design)

### Part III: Production Readiness
10. [Resilience & Reliability](#10-resilience--reliability)
11. [Observability & Monitoring](#11-observability--monitoring)
12. [Deployment & Operations](#12-deployment--operations)
13. [Testing Strategy](#13-testing-strategy)

### Part IV: Quality & Governance
14. [Non-Functional Requirements (NFR)](#14-non-functional-requirements-nfr)
15. [Performance & Capacity Planning](#15-performance--capacity-planning)
16. [Cost Optimization](#16-cost-optimization)
17. [Trade-offs & Architecture Decisions](#17-trade-offs--architecture-decisions)

### Part V: Operations & MLOps
18. [Incident Response & Runbooks](#18-incident-response--runbooks)
19. [MLOps (Machine Learning Operations)](#19-mlops-machine-learning-operations)

### Part VI: Launch & Beyond
20. [Implementation Roadmap](#20-implementation-roadmap)
21. [Production Readiness Checklist](#21-production-readiness-checklist)
22. [Common Mistakes & Anti-Patterns](#22-common-mistakes--anti-patterns)
23. [Tool Recommendations](#23-tool-recommendations)
24. [Appendices](#24-appendices)

---

# PART I: FOUNDATION & ARCHITECTURE

---

# 1. EXECUTIVE SUMMARY (TL;DR)

> 💡 **Mục đích**: Tóm tắt toàn bộ document trong 1 trang

## 1.1 Summary Table

| Aspect | Details |
|--------|---------|
| **Problem Statement** | [1-2 câu mô tả vấn đề] |
| **Proposed Solution** | [1-2 câu mô tả giải pháp] |
| **Business Impact** | [Quantifiable: Tăng revenue X%, giảm cost Y%] |
| **Technical Impact** | [Reduce latency 50%, improve reliability 99.9%] |
| **Key Technology** | [Golang/Python, PostgreSQL, Kafka, K8s] |
| **Estimated Effort** | [X người × Y sprint = Z man-days] |
| **Risk Level** | [Low/Medium/High] với justification |
| **Timeline** | [MVP: X tháng, Production: Y tháng] |
| **Key Stakeholders** | [Team/Department names] |
| **Total Cost (Year 1)** | [$X infrastructure + $Y development] |

## 1.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       [SYSTEM NAME]                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐    ┌───────────┐    ┌─────────────┐              │
│   │ Clients │───▶│API Gateway│───▶│  Services   │              │
│   └─────────┘    └───────────┘    └──────┬──────┘              │
│                                          │                       │
│                  ┌───────────────────────┼───────────────────┐  │
│                  │                       ▼                   │  │
│                  │  ┌────────┐   ┌───────────┐   ┌────────┐ │  │
│                  │  │  DB    │   │   Cache   │   │ Queue  │ │  │
│                  │  └────────┘   └───────────┘   └────────┘ │  │
│                  └───────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 1.3 Key Metrics & Success Criteria

| KPI | Current | Target | Measurement Method |
|-----|---------|--------|-------------------|
| Response Time (p95) | [X]ms | [Y]ms | Datadog APM |
| Error Rate | [X]% | <0.1% | Prometheus |
| Throughput | [X] rps | [Y] rps | Load Test |
| Uptime SLA | [X]% | 99.9% | StatusPage |
| Cost per Request | $[X] | $[Y] | Cloud billing |

## 1.4 Risk Summary

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High | High | [Mitigation strategy] |
| [Risk 2] | Medium | Medium | [Mitigation strategy] |

---

# 2. INTRODUCTION

## 2.1 Document Purpose

Tài liệu này cung cấp **bản thiết kế production-ready** cho **[PROJECT_NAME]**:
- **HLD**: Kiến trúc tổng thể
- **LLD**: Chi tiết implementation
- **Production Standards**: Security, Observability, Reliability
- **MLOps**: ML pipeline và model serving (nếu applicable)
- **Operations**: Runbooks, Incident Response

## 2.2 Target Audience

| Audience | Primary Use | Key Sections |
|----------|-------------|--------------|
| **Engineers** | Implementation | 5-8, 10-13 |
| **Architects** | Review | 5, 17 |
| **DevOps/SRE** | Operations | 10-12, 18 |
| **QA** | Test Design | 13 |
| **Product** | Scope/Timeline | 1, 3, 20 |
| **Security** | Security Review | 9 |
| **ML Engineers** | MLOps | 19 |

## 2.3 Definitions & Acronyms

| Term | Definition |
|------|------------|
| **SDD** | Software Design Document |
| **HLD/LLD** | High/Low-Level Design |
| **NFR** | Non-Functional Requirement |
| **SLA/SLO/SLI** | Service Level Agreement/Objective/Indicator |
| **ADR** | Architecture Decision Record |
| **RPO/RTO** | Recovery Point/Time Objective |
| **MTBF/MTTR** | Mean Time Between Failures / To Repair |
| **MLOps** | Machine Learning Operations |
| **CI/CD** | Continuous Integration/Deployment |
| **IaC** | Infrastructure as Code |

## 2.4 Document Standards

This document follows:
- **IEEE 1016-2009**: Software Design Descriptions
- **C4 Model**: Architecture visualization
- **OpenAPI 3.0**: API specifications
- **ADR Format**: Architecture decisions

---

# 3. GOALS, SCOPE & CONSTRAINTS

## 3.1 Goals

### Business Goals

| Goal | Metric | Target | Timeline |
|------|--------|--------|----------|
| Increase Revenue | Conversion Rate | +20% | Q2 |
| Reduce Cost | Infrastructure | -30% | Q3 |
| Improve UX | NPS Score | >50 | Q4 |

### Technical Goals

| Goal | Metric | Target | Timeline |
|------|--------|--------|----------|
| Performance | P95 Latency | <200ms | Sprint 5 |
| Reliability | Uptime | 99.9% | Sprint 6 |
| Scalability | Concurrent Users | 100K | Q2 |
| Security | Vulnerability | Zero Critical | Ongoing |

## 3.2 In-Scope ✅

**MVP (Must Have)**:
- ✅ [Feature 1]: [Description]
- ✅ [Feature 2]: [Description]

**Phase 2 (Should Have)**:
- 📋 [Feature 3]: [Description]

**Phase 3 (Nice to Have)**:
- 💡 [Feature 4]: [Description]

## 3.3 Out-of-Scope / Non-Goals ❌

> ⚠️ **Critical**: Prevent scope creep

| Non-Goal | Reason | Future? |
|----------|--------|---------|
| Multi-language | Budget | Phase 3 |
| Mobile app | Different team | Parallel |

## 3.4 Assumptions

| ID | Assumption | Impact if Wrong | Validation |
|----|------------|-----------------|------------|
| A1 | DB available | High - delay | Confirm DevOps |
| A2 | User <100K/6mo | Medium - rescale | Monitor |

## 3.5 Constraints

### Technical Constraints

| Constraint | Reason | Workaround |
|------------|--------|------------|
| Python 3.11+ | Standard | N/A |
| PostgreSQL | Compliance | N/A |
| AWS only | Vendor | N/A |

### Business Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Budget <$50K/yr | Limited infra | Reserved instances |
| Launch Q2 | Tight timeline | Reduce MVP |

### Compliance

| Regulation | Requirement | Implementation |
|------------|-------------|----------------|
| GDPR | EU residency | eu-west-1 |
| SOC2 | Audit trail | Logging |

## 3.6 Dependencies

```mermaid
graph LR
    A[This Project] --> B[User Service v2]
    A --> C[Payment API]
    A --> D[OpenAI API]
    B --> E[Auth DB]
```

| Dependency | Owner | Risk | Fallback |
|------------|-------|------|----------|
| OpenAI API | External | High | Local LLM |
| Stripe | External | Medium | PayPal |

---

# 4. SYSTEM OVERVIEW

## 4.1 Business Context

**Problem**: [Detailed problem statement]

**Solution**: [How system solves it]

**Value**: [Quantified business value]

## 4.2 Stakeholders

| Stakeholder | Interest | Communication |
|-------------|----------|---------------|
| Executive | ROI, Timeline | Monthly report |
| Product | Features | Weekly sync |
| Engineering | Tech debt | Sprint review |
| Operations | Stability | Daily standup |

## 4.3 Functional Requirements

| ID | Module | Description | Priority | Acceptance Criteria |
|----|--------|-------------|----------|---------------------|
| FR-001 | Auth | User login | P0 | Login <2s, MFA support |
| FR-002 | Catalog | Search products | P0 | <500ms, 99% relevance |
| FR-003 | Order | Process orders | P0 | <5s, idempotent |

## 4.4 User Stories (Gherkin)

```gherkin
Feature: User Authentication
  As a registered user
  I want to login securely
  So that I can access my account

  Scenario: Successful login
    Given I am on login page
    When I enter valid credentials
    Then I am redirected to dashboard
    And session is created with 24h expiry
    
  Scenario: Failed login - wrong password
    Given I am on login page
    When I enter wrong password
    Then I see "Invalid credentials" error
    And login attempt is logged
    And after 5 failures, account is locked 15 minutes
```

---

# 5. HIGH-LEVEL DESIGN (HLD)

## 5.1 Architecture Pattern

**Selected**: Microservices with Event-Driven Architecture

**Rationale**:
- ✅ Independent scalability
- ✅ Fault isolation
- ✅ Technology flexibility
- ✅ Team autonomy

**Key Principles**:
- **SOLID**: Class/module design
- **DDD**: Bounded contexts
- **12-Factor App**: Cloud-native
- **Zero Trust**: Security model

## 5.2 System Context (C4 Level 1)

```
┌────────────────────────────────────────────────────────────────────┐
│                      SYSTEM CONTEXT                                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────┐     ┌──────────┐     ┌──────────────────┐         │
│    │   Web    │     │  Mobile  │     │  Third-Party     │         │
│    │  Users   │     │   Users  │     │  Partners (API)  │         │
│    └────┬─────┘     └────┬─────┘     └────────┬─────────┘         │
│         │                │                     │                    │
│         └────────────────┼─────────────────────┘                   │
│                          │ HTTPS/WSS                               │
│                          ▼                                          │
│    ┌─────────────────────────────────────────────────────────┐    │
│    │                                                         │    │
│    │               [SYSTEM NAME]                             │    │
│    │                                                         │    │
│    │  • User authentication & authorization                  │    │
│    │  • Business logic processing                            │    │
│    │  • Data management & analytics                          │    │
│    │  • ML inference (if applicable)                         │    │
│    │                                                         │    │
│    └─────────────────────────────────────────────────────────┘    │
│         │              │              │              │              │
│         ▼              ▼              ▼              ▼              │
│    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────────┐     │
│    │Database │   │  Cache  │   │  Email  │   │  Payment    │     │
│    │(Postgres)│  │ (Redis) │   │(SendGrid)│  │  (Stripe)   │     │
│    └─────────┘   └─────────┘   └─────────┘   └─────────────┘     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## 5.3 Container Diagram (C4 Level 2)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CONTAINER DIAGRAM                                │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    PRESENTATION LAYER                            │  │
│  │  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐   │  │
│  │  │   Web App     │    │  Mobile App   │    │   Admin UI    │   │  │
│  │  │  (React/TS)   │    │(React Native) │    │   (React)     │   │  │
│  │  └───────────────┘    └───────────────┘    └───────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    GATEWAY LAYER                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │           API Gateway (Kong / AWS API Gateway)           │  │  │
│  │  │  • Rate Limiting  • Auth  • Routing  • Load Balancing   │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    SERVICE LAYER                                 │  │
│  │                                                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │  │
│  │  │   Auth     │ │   User     │ │  Product   │ │   Order    │   │  │
│  │  │  Service   │ │  Service   │ │  Service   │ │  Service   │   │  │
│  │  │ (Python)   │ │ (Python)   │ │ (Python)   │ │ (Python)   │   │  │
│  │  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘   │  │
│  │         │              │              │              │           │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │  │
│  │  │   ML       │ │ Notification│ │  Payment   │ │ Analytics  │   │  │
│  │  │ Service    │ │  Service   │ │  Service   │ │  Service   │   │  │
│  │  │ (Python)   │ │  (Python)  │ │ (Python)   │ │ (Python)   │   │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    DATA LAYER                                    │  │
│  │                                                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │  │
│  │  │ PostgreSQL │ │   Redis    │ │   Kafka    │ │    S3      │   │  │
│  │  │ (Primary)  │ │  (Cache)   │ │  (Events)  │ │ (Storage)  │   │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │  │
│  │                                                                   │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐                   │  │
│  │  │Elasticsearch│ │  ClickHouse│ │   MLflow   │                   │  │
│  │  │  (Search)  │ │ (Analytics)│ │ (ML Models)│                   │  │
│  │  └────────────┘ └────────────┘ └────────────┘                   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## 5.4 Layered Architecture Design - một **production-grade microservice architecture** theo **Clean Architecture + Hexagonal Pattern**

```bash
┌─────────────────────────────────────────────────┐
│           API Layer (HTTP Interface)            │
├─────────────────────────────────────────────────┤
│         Core Layer (Security, Middleware)       │
├─────────────────────────────────────────────────┤
│      Service Layer (Business Logic)             │
├─────────────────────────────────────────────────┤
│    Repository Layer (Data Access)               │
├─────────────────────────────────────────────────┤
│   Infrastructure (Milvus, Neo4j, Postgres)      │
└─────────────────────────────────────────────────┘

```

## 5.5 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python 3.11/FastAPI | Async, high performance |
| **Frontend** | React 18 + TypeScript | Type safety, ecosystem |
| **Database** | PostgreSQL 15 | ACID, JSONB, extensions |
| **Cache** | Redis 7 | Sub-ms latency |
| **Queue** | Apache Kafka | High throughput, durability |
| **Search** | Elasticsearch 8 | Full-text, analytics |
| **ML** | MLflow + PyTorch | Experiment tracking |
| **Container** | Docker | Consistency |
| **Orchestration** | Kubernetes (EKS) | Auto-scaling |
| **CI/CD** | GitHub Actions | Native integration |
| **IaC** | Terraform + Helm | Declarative infra |
| **Monitoring** | Datadog / Prometheus+Grafana | Full observability |

## 5.6 Communication Patterns

| Pattern | Use Case | Protocol | Implementation |
|---------|----------|----------|----------------|
| Sync Request/Response | API calls | REST/gRPC | Circuit Breaker |
| Async Events | Order created | Kafka | Event Sourcing |
| Streaming | Real-time updates | WebSocket | Redis Pub/Sub |
| Batch | Data processing | Airflow | Schedule jobs |

---

# 6. LOW-LEVEL DESIGN (LLD)

## 6.1 Component Template

> 📝 **Repeat for each service/module**

### 6.1.1 [Service Name] Service

#### Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | [Brief description] |
| **Owner** | [Team/Person] |
| **Language** | Python 3.11 |
| **Framework** | FastAPI |
| **Database** | PostgreSQL |

#### Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    [SERVICE NAME] SERVICE                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐                                          │
│  │    Controller    │  ← HTTP/gRPC handlers                    │
│  │   (API Layer)    │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│  ┌────────▼─────────┐                                          │
│  │     Service      │  ← Business logic                        │
│  │ (Business Layer) │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│  ┌────────▼─────────┐                                          │
│  │   Repository     │  ← Data access                           │
│  │  (Data Layer)    │                                          │
│  └────────┬─────────┘                                          │
│           │                                                     │
│  ┌────────▼─────────┐                                          │
│  │    Database      │                                          │
│  │   (PostgreSQL)   │                                          │
│  └──────────────────┘                                          │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

#### Sequence Diagram

```
┌──────┐     ┌──────────┐     ┌─────────┐     ┌────────────┐     ┌────┐
│Client│     │Controller│     │ Service │     │ Repository │     │ DB │
└──┬───┘     └────┬─────┘     └────┬────┘     └─────┬──────┘     └──┬─┘
   │              │                │                │               │
   │  Request     │                │                │               │
   │─────────────▶│                │                │               │
   │              │  Validate      │                │               │
   │              │───────────────▶│                │               │
   │              │                │  Query         │               │
   │              │                │───────────────▶│               │
   │              │                │                │  SQL          │
   │              │                │                │──────────────▶│
   │              │                │                │               │
   │              │                │                │  Result       │
   │              │                │                │◀──────────────│
   │              │                │  Entity        │               │
   │              │                │◀───────────────│               │
   │              │  DTO           │                │               │
   │              │◀───────────────│                │               │
   │  Response    │                │                │               │
   │◀─────────────│                │                │               │
   │              │                │                │               │
```

#### Pseudo Code (Business Logic)

```python
# user_service.py
class UserService:
    """
    Business logic for user management
    """
    
    def __init__(self, user_repo: UserRepository, cache: RedisCache):
        self.user_repo = user_repo
        self.cache = cache
        
    async def create_user(self, request: CreateUserRequest) -> User:
        """
        Create new user with validation
        
        Steps:
        1. Validate email uniqueness
        2. Hash password
        3. Create user in DB
        4. Send verification email
        5. Return user
        
        Raises:
            EmailExistsError: If email already registered
            ValidationError: If input invalid
        """
        # Step 1: Check email exists
        existing = await self.user_repo.find_by_email(request.email)
        if existing:
            raise EmailExistsError(f"Email {request.email} already exists")
            
        # Step 2: Hash password
        hashed_password = bcrypt.hash(request.password, rounds=12)
        
        # Step 3: Create user
        user = User(
            id=uuid.uuid4(),
            email=request.email,
            password_hash=hashed_password,
            status=UserStatus.PENDING_VERIFICATION,
            created_at=datetime.utcnow()
        )
        
        await self.user_repo.save(user)
        
        # Step 4: Send verification (async)
        await self.event_bus.publish(UserCreatedEvent(user.id))
        
        return user
        
    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user with caching
        """
        # Try cache first
        cache_key = f"user:{user_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return User.from_dict(cached)
            
        # Fallback to DB
        user = await self.user_repo.find_by_id(user_id)
        if user:
            await self.cache.set(cache_key, user.to_dict(), ttl=3600)
            
        return user
```

#### Class Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLASS DIAGRAM                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐       ┌─────────────────────────┐     │
│  │   <<interface>> │       │     UserService         │     │
│  │  UserRepository │◀──────│                         │     │
│  ├─────────────────┤       ├─────────────────────────┤     │
│  │ +find_by_id()   │       │ -user_repo: UserRepo    │     │
│  │ +find_by_email()│       │ -cache: RedisCache      │     │
│  │ +save()         │       │ -event_bus: EventBus    │     │
│  │ +delete()       │       ├─────────────────────────┤     │
│  └─────────────────┘       │ +create_user()          │     │
│          ▲                 │ +get_user()             │     │
│          │                 │ +update_user()          │     │
│  ┌───────┴────────┐        │ +delete_user()          │     │
│  │PostgresUserRepo │        └─────────────────────────┘     │
│  ├────────────────┤                                         │
│  │ -db: Database  │        ┌─────────────────────────┐     │
│  ├────────────────┤        │       User              │     │
│  │ +find_by_id()  │        ├─────────────────────────┤     │
│  │ +find_by_email()│       │ +id: UUID               │     │
│  │ +save()        │        │ +email: str             │     │
│  │ +delete()      │        │ +password_hash: str     │     │
│  └────────────────┘        │ +status: UserStatus     │     │
│                            │ +created_at: datetime   │     │
│                            ├─────────────────────────┤     │
│                            │ +to_dict()              │     │
│                            │ +from_dict()            │     │
│                            └─────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```




---
## 6.1.5 Project Structure





# PART II: IMPLEMENTATION DETAILS

---

# 7. API DESIGN & CONTRACTS

## 7.1 API Design Principles

- **RESTful**: Resource-oriented URLs
- **Versioning**: URL path (`/api/v1/`)
- **Pagination**: Cursor-based for large datasets
- **Rate Limiting**: Per-user/per-IP limits
- **Idempotency**: Via `Idempotency-Key` header

## 7.2 OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: "[PROJECT] API"
  version: 1.0.0
  description: Production API for [PROJECT]
  
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api-staging.example.com/v1
    description: Staging

security:
  - BearerAuth: []

paths:
  /users:
    post:
      summary: Create new user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '429':
          $ref: '#/components/responses/RateLimited'
          
  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUserById
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      
  schemas:
    CreateUserRequest:
      type: object
      required: [email, password, name]
      properties:
        email:
          type: string
          format: email
          maxLength: 255
        password:
          type: string
          minLength: 8
          maxLength: 128
        name:
          type: string
          minLength: 1
          maxLength: 100
          
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        status:
          type: string
          enum: [PENDING, ACTIVE, SUSPENDED]
        created_at:
          type: string
          format: date-time
          
    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
        trace_id:
          type: string
          
  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "VALIDATION_ERROR"
            message: "Invalid input"
            
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
            
    RateLimited:
      description: Too many requests
      headers:
        Retry-After:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

## 7.3 Error Response Standards

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "email": "Invalid email format",
      "password": "Must be at least 8 characters"
    },
    "trace_id": "abc-123-xyz",
    "timestamp": "2024-01-15T10:30:00Z",
    "documentation_url": "https://docs.example.com/errors/VALIDATION_ERROR"
  }
}
```

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 400 | VALIDATION_ERROR | Invalid input |
| 401 | UNAUTHORIZED | Missing/invalid auth |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource conflict |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |
| 503 | SERVICE_UNAVAILABLE | Temporary unavailable |

## 7.4 Rate Limiting

| Tier | Requests/min | Burst | Scope |
|------|-------------|-------|-------|
| Free | 60 | 10 | Per user |
| Pro | 600 | 100 | Per user |
| Enterprise | 6000 | 1000 | Per org |
| Internal | Unlimited | - | Service-to-service |

---

# 8. DATA DESIGN

## 8.1 Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ENTITY RELATIONSHIP DIAGRAM                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌────────────────┐         ┌────────────────┐                        │
│   │     USERS      │         │     ORDERS     │                        │
│   ├────────────────┤         ├────────────────┤                        │
│   │ id (PK)        │─┐       │ id (PK)        │                        │
│   │ email (UK)     │ │       │ user_id (FK)   │◀─┐                     │
│   │ password_hash  │ │       │ status         │  │                     │
│   │ name           │ │       │ total_amount   │  │                     │
│   │ status         │ │       │ created_at     │  │                     │
│   │ created_at     │ │       │ updated_at     │  │                     │
│   │ updated_at     │ │       └────────────────┘  │                     │
│   └────────────────┘ │              │            │                     │
│          │           │              │ 1:N        │                     │
│          │           └──────────────┼────────────┘                     │
│          │ 1:N                      │                                   │
│          │                          ▼                                   │
│          │               ┌────────────────┐      ┌────────────────┐   │
│          │               │  ORDER_ITEMS   │      │    PRODUCTS    │   │
│          │               ├────────────────┤      ├────────────────┤   │
│          │               │ id (PK)        │      │ id (PK)        │   │
│          │               │ order_id (FK)  │◀──┐  │ sku (UK)       │   │
│          │               │ product_id (FK)│───┼─▶│ name           │   │
│          │               │ quantity       │   │  │ price          │   │
│          │               │ unit_price     │   │  │ stock          │   │
│          ▼               └────────────────┘   │  │ category_id(FK)│   │
│   ┌────────────────┐                          │  └────────────────┘   │
│   │   ADDRESSES    │                          │          │            │
│   ├────────────────┤                          │          │            │
│   │ id (PK)        │                          │          ▼            │
│   │ user_id (FK)   │                          │  ┌────────────────┐   │
│   │ type           │                          │  │   CATEGORIES   │   │
│   │ street         │                          │  ├────────────────┤   │
│   │ city           │                          │  │ id (PK)        │   │
│   │ country        │                          │  │ name           │   │
│   │ postal_code    │                          │  │ parent_id (FK) │──┘│
│   └────────────────┘                          │  └────────────────┘   │
│                                               │                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## 8.2 Database Schema (PostgreSQL)

```sql
-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy search

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT users_email_uk UNIQUE (email),
    CONSTRAINT users_status_check CHECK (status IN ('PENDING', 'ACTIVE', 'SUSPENDED'))
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- Products table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(12,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id UUID REFERENCES categories(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT products_sku_uk UNIQUE (sku),
    CONSTRAINT products_price_positive CHECK (price >= 0),
    CONSTRAINT products_stock_positive CHECK (stock >= 0)
);

-- Indexes
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_name_search ON products USING GIN(name gin_trgm_ops);

-- Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total_amount DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    shipping_address_id UUID REFERENCES addresses(id),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT orders_status_check CHECK (
        status IN ('PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
    )
);

-- Indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    
CREATE TRIGGER products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    
CREATE TRIGGER orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

## 8.3 Caching Strategy

| Data | Cache Type | TTL | Invalidation |
|------|------------|-----|--------------|
| User profile | Read-through | 1 hour | On update |
| Product catalog | Aside | 15 min | CDC events |
| Session | Write-through | 24 hours | On logout |
| API responses | CDN | 5 min | Purge API |

```python
# Cache implementation
class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def get_or_set(
        self, 
        key: str, 
        fetcher: Callable, 
        ttl: int = 3600
    ):
        """Cache-aside pattern"""
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
            
        value = await fetcher()
        await self.redis.setex(key, ttl, json.dumps(value))
        return value
        
    async def invalidate(self, pattern: str):
        """Invalidate by pattern"""
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)
```

## 8.4 Event Streaming (Kafka)

```yaml
# Topic Configuration
topics:
  user-events:
    partitions: 12
    replication_factor: 3
    retention_ms: 604800000  # 7 days
    cleanup_policy: delete
    
  order-events:
    partitions: 24
    replication_factor: 3
    retention_ms: 2592000000  # 30 days
    cleanup_policy: compact
```

```python
# Event Schema (Avro)
{
    "type": "record",
    "name": "UserCreatedEvent",
    "namespace": "com.example.events",
    "fields": [
        {"name": "event_id", "type": "string"},
        {"name": "event_type", "type": "string"},
        {"name": "timestamp", "type": "long"},
        {"name": "user_id", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "metadata", "type": {"type": "map", "values": "string"}}
    ]
}
```

## 8.5 Data Retention Policy

| Data Type | Retention | Archive | Deletion |
|-----------|-----------|---------|----------|
| User data | Active + 2 years | S3 Glacier | Hard delete |
| Orders | 7 years | S3 Glacier | Soft delete |
| Logs | 90 days | S3 Standard | Auto-delete |
| Metrics | 15 months | N/A | Auto-delete |
| Audit logs | 7 years | S3 Glacier | Never |

---

# 9. SECURITY DESIGN

## 9.1 STRIDE Threat Model

| Threat | Description | Mitigation |
|--------|-------------|------------|
| **S**poofing | Fake identity | MFA, OAuth 2.0 |
| **T**ampering | Data modification | HMAC, checksums |
| **R**epudiation | Deny actions | Audit logs |
| **I**nformation Disclosure | Data leak | Encryption, RBAC |
| **D**enial of Service | System unavailable | Rate limiting, WAF |
| **E**levation of Privilege | Unauthorized access | RBAC, least privilege |

## 9.2 Authentication (OAuth 2.0 + JWT)

```python
# JWT Token Structure
{
    "header": {
        "alg": "RS256",
        "typ": "JWT",
        "kid": "key-id-123"
    },
    "payload": {
        "sub": "user-uuid",
        "iss": "https://auth.example.com",
        "aud": "https://api.example.com",
        "exp": 1705401600,
        "iat": 1705315200,
        "scope": "read:users write:orders",
        "roles": ["user", "admin"]
    }
}
```

```python
# Token validation
from jose import jwt, JWTError

async def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="https://api.example.com",
            issuer="https://auth.example.com"
        )
        
        # Check expiration
        if payload["exp"] < time.time():
            raise TokenExpiredError()
            
        # Check revocation
        if await is_token_revoked(payload["jti"]):
            raise TokenRevokedError()
            
        return payload
        
    except JWTError as e:
        raise InvalidTokenError(str(e))
```

## 9.3 Authorization (RBAC)

```python
# Role definitions
ROLES = {
    "admin": ["*"],  # All permissions
    "manager": [
        "users:read", "users:write",
        "orders:read", "orders:write",
        "products:read", "products:write"
    ],
    "user": [
        "users:read:self",
        "orders:read:self", "orders:write:self",
        "products:read"
    ],
    "guest": ["products:read"]
}

# Permission decorator
def require_permission(*permissions):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            user_permissions = ROLES.get(user.role, [])
            
            for perm in permissions:
                if perm not in user_permissions and "*" not in user_permissions:
                    raise ForbiddenError(f"Missing permission: {perm}")
                    
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.delete("/users/{user_id}")
@require_permission("users:delete")
async def delete_user(user_id: str):
    pass
```

## 9.4 Data Encryption

| Type | Algorithm | Key Management |
|------|-----------|----------------|
| At Rest | AES-256-GCM | AWS KMS |
| In Transit | TLS 1.3 | ACM |
| Passwords | Argon2id | N/A |
| Secrets | AES-256 | Vault |
| PII | AES-256-GCM | Envelope encryption |

```python
# Field-level encryption
from cryptography.fernet import Fernet

class EncryptedField:
    def __init__(self, key_id: str):
        self.kms = KMSClient()
        self.key_id = key_id
        
    async def encrypt(self, plaintext: str) -> str:
        # Get data key from KMS
        data_key = await self.kms.generate_data_key(self.key_id)
        
        # Encrypt with data key
        fernet = Fernet(data_key.plaintext)
        ciphertext = fernet.encrypt(plaintext.encode())
        
        # Return encrypted data key + ciphertext
        return base64.b64encode(
            data_key.encrypted + b":" + ciphertext
        ).decode()
        
    async def decrypt(self, encrypted: str) -> str:
        data = base64.b64decode(encrypted)
        encrypted_key, ciphertext = data.split(b":", 1)
        
        # Decrypt data key
        data_key = await self.kms.decrypt(encrypted_key)
        
        # Decrypt data
        fernet = Fernet(data_key)
        return fernet.decrypt(ciphertext).decode()
```

## 9.5 Input Validation

```python
from pydantic import BaseModel, validator, EmailStr
import re
import html

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError('Minimum 12 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Needs uppercase')
        if not re.search(r'[a-z]', v):
            raise ValueError('Needs lowercase')
        if not re.search(r'[0-9]', v):
            raise ValueError('Needs digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Needs special character')
        return v
        
    @validator('name')
    def sanitize_name(cls, v):
        # Remove HTML tags and escape
        clean = re.sub(r'<[^>]+>', '', v)
        return html.escape(clean.strip())[:100]
```

## 9.6 Security Scanning Pipeline

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      # SAST - Static Analysis
      - name: Bandit (Python)
        run: bandit -r src/ -f json -o bandit-report.json
        
      - name: SonarQube
        uses: sonarsource/sonarqube-scan-action@master
        
      # Dependency Scanning
      - name: Snyk
        uses: snyk/actions/python@master
        with:
          args: --severity-threshold=high
          
      # Secrets Detection
      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          
      # Container Scanning
      - name: Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          severity: 'CRITICAL,HIGH'
          
      # DAST - Dynamic Analysis (staging only)
      - name: OWASP ZAP
        if: github.ref == 'refs/heads/staging'
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'https://staging.example.com'
```

## 9.7 Security Checklist

- [ ] OWASP Top 10 addressed
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection (tokens)
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Authentication required for sensitive endpoints
- [ ] Authorization checks at service layer
- [ ] Secrets in Vault/Secrets Manager
- [ ] TLS 1.3 for all communications
- [ ] Security headers configured (HSTS, CSP, etc.)
- [ ] Audit logging for sensitive operations
- [ ] Penetration testing completed

---

# PART III: PRODUCTION READINESS

---

# 10. RESILIENCE & RELIABILITY

## 10.1 Resilience Patterns

### Retry with Exponential Backoff + Jitter

```python
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential_jitter,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=30, jitter=5),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry attempt {retry_state.attempt_number}"
    )
)
async def call_external_service(request):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=request)
        response.raise_for_status()
        return response.json()
```

### Circuit Breaker

```python
from pybreaker import CircuitBreaker, CircuitBreakerError

# Configuration
payment_breaker = CircuitBreaker(
    fail_max=5,              # Open after 5 failures
    reset_timeout=60,        # Try again after 60s
    exclude=[ValidationError],  # Don't count these
    listeners=[CircuitBreakerMetrics()]  # Prometheus metrics
)

@payment_breaker
async def process_payment(order):
    return await payment_client.charge(order)

# Usage with fallback
async def handle_order(order):
    try:
        result = await process_payment(order)
    except CircuitBreakerError:
        # Circuit is open - use fallback
        result = await queue_for_later(order)
        await notify_ops("Payment circuit open")
    return result
```

### Bulkhead Pattern

```python
from asyncio import Semaphore

class BulkheadService:
    def __init__(self):
        # Separate limits for different services
        self.payment_semaphore = Semaphore(10)
        self.user_semaphore = Semaphore(20)
        self.notification_semaphore = Semaphore(50)
        
    async def call_payment(self, request):
        async with self.payment_semaphore:
            return await payment_client.call(request)
            
    async def call_user_service(self, user_id):
        async with self.user_semaphore:
            return await user_client.get(user_id)
```

### Timeout Configuration

```python
# Service-specific timeouts
TIMEOUTS = {
    "database": httpx.Timeout(connect=2, read=5, write=5, pool=10),
    "external_api": httpx.Timeout(connect=5, read=30, write=10, pool=30),
    "cache": httpx.Timeout(connect=0.5, read=1, write=1, pool=2),
    "internal_service": httpx.Timeout(connect=1, read=5, write=5, pool=5),
}

async def call_with_timeout(service_type: str, func, *args):
    timeout = TIMEOUTS[service_type]
    try:
        return await asyncio.wait_for(func(*args), timeout=timeout.read)
    except asyncio.TimeoutError:
        logger.error(f"Timeout calling {service_type}")
        raise ServiceTimeoutError(service_type)
```

## 10.2 Error Handling Strategy

```python
class ErrorHandler:
    # Retryable errors
    TRANSIENT_ERRORS = [
        TimeoutError,
        ConnectionError,
        HTTPStatusError(503),
        HTTPStatusError(429),
        HTTPStatusError(502),
        HTTPStatusError(504),
    ]
    
    # Non-retryable errors
    PERMANENT_ERRORS = [
        ValidationError,
        AuthenticationError,
        NotFoundError,
        HTTPStatusError(400),
        HTTPStatusError(401),
        HTTPStatusError(403),
        HTTPStatusError(404),
    ]
    
    @staticmethod
    def is_retryable(error: Exception) -> bool:
        if isinstance(error, tuple(ErrorHandler.TRANSIENT_ERRORS)):
            return True
        if hasattr(error, 'status_code'):
            return error.status_code in [429, 502, 503, 504]
        return False
        
    @staticmethod
    def handle(error: Exception, context: dict) -> Response:
        trace_id = context.get('trace_id')
        
        if isinstance(error, ValidationError):
            return ErrorResponse(
                code="VALIDATION_ERROR",
                message=str(error),
                status=400,
                trace_id=trace_id
            )
        elif isinstance(error, NotFoundError):
            return ErrorResponse(
                code="NOT_FOUND",
                message=f"Resource not found: {error.resource}",
                status=404,
                trace_id=trace_id
            )
        else:
            # Log unexpected errors
            logger.exception(f"Unexpected error: {error}", extra=context)
            return ErrorResponse(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                status=500,
                trace_id=trace_id
            )
```

## 10.3 Health Checks

```python
from enum import Enum
from dataclasses import dataclass

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    latency_ms: float
    message: str = ""

class HealthService:
    async def check_all(self) -> dict:
        checks = await asyncio.gather(
            self.check_database(),
            self.check_cache(),
            self.check_kafka(),
            return_exceptions=True
        )
        
        overall = HealthStatus.HEALTHY
        for check in checks:
            if isinstance(check, Exception):
                overall = HealthStatus.UNHEALTHY
                break
            if check.status == HealthStatus.UNHEALTHY:
                overall = HealthStatus.UNHEALTHY
                break
            if check.status == HealthStatus.DEGRADED:
                overall = HealthStatus.DEGRADED
                
        return {
            "status": overall.value,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": [c.__dict__ for c in checks if not isinstance(c, Exception)]
        }
        
    async def check_database(self) -> HealthCheck:
        start = time.time()
        try:
            await db.execute("SELECT 1")
            return HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                latency_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                latency_ms=(time.time() - start) * 1000,
                message=str(e)
            )
```

## 10.4 Disaster Recovery

| Metric | Target | Strategy |
|--------|--------|----------|
| **RPO** | 15 minutes | Continuous replication |
| **RTO** | 1 hour | Multi-AZ failover |

### Backup Strategy (3-2-1 Rule)

```yaml
# Backup configuration
backup:
  database:
    type: continuous
    provider: AWS RDS
    retention: 35 days
    point_in_time_recovery: true
    
  files:
    type: incremental
    provider: S3 + S3 Glacier
    schedule:
      hourly: "0 * * * *"
      daily: "0 2 * * *"
      weekly: "0 3 * * 0"
    retention:
      hourly: 24
      daily: 30
      weekly: 52
      
  disaster_recovery:
    primary_region: us-east-1
    dr_region: us-west-2
    replication_lag_threshold: 30s
    failover_mode: automatic
```

### Failover Procedure

```python
# Automated failover
class FailoverManager:
    async def execute_failover(self, reason: str):
        logger.critical(f"Initiating failover: {reason}")
        
        # 1. Notify on-call
        await self.alert_oncall(f"FAILOVER INITIATED: {reason}")
        
        # 2. Stop writes to primary
        await self.primary.stop_writes()
        
        # 3. Ensure replication caught up
        lag = await self.check_replication_lag()
        if lag > timedelta(seconds=30):
            raise FailoverError("Replication lag too high")
            
        # 4. Promote secondary
        await self.secondary.promote()
        
        # 5. Update DNS
        await self.dns.update_record(
            name="db.example.com",
            target=self.secondary.endpoint
        )
        
        # 6. Verify
        await self.verify_connectivity()
        
        logger.info("Failover complete")
```

---

# 11. OBSERVABILITY & MONITORING

## 11.1 Three Pillars Implementation

### Metrics (Prometheus)

```python
from prometheus_client import Counter, Histogram, Gauge, Info

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status', 'service']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

# Business metrics
ORDERS_TOTAL = Counter(
    'orders_total',
    'Total orders',
    ['status', 'payment_method']
)

REVENUE_TOTAL = Counter(
    'revenue_total_cents',
    'Total revenue in cents',
    ['currency', 'product_category']
)

# System metrics
ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Current active connections',
    ['pool']
)

DB_POOL_SIZE = Gauge(
    'db_pool_size',
    'Database connection pool size',
    ['status']  # available, in_use
)

# Middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
        service="api"
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

### Structured Logging

```python
import structlog
from pythonjsonlogger import jsonlogger

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Usage
logger.info(
    "order_created",
    order_id=order.id,
    user_id=user.id,
    total_amount=order.total,
    currency=order.currency,
    items_count=len(order.items),
    trace_id=request.state.trace_id,
    span_id=request.state.span_id
)

# Output
{
    "event": "order_created",
    "order_id": "ord_123",
    "user_id": "usr_456",
    "total_amount": 99.99,
    "currency": "USD",
    "items_count": 3,
    "trace_id": "abc123",
    "span_id": "def456",
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "info",
    "logger": "order_service"
}
```

### Distributed Tracing (OpenTelemetry)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to Jaeger/Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Auto-instrument
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument(engine=engine)

# Manual spans
async def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Child span for validation
        with tracer.start_as_current_span("validate_order"):
            order = await validate_order(order_id)
            span.set_attribute("order.valid", True)
            
        # Child span for payment
        with tracer.start_as_current_span("process_payment") as payment_span:
            payment_span.set_attribute("payment.method", order.payment_method)
            result = await payment_service.charge(order)
            payment_span.set_attribute("payment.status", result.status)
            
        return order
```

## 11.2 Golden Signals (SRE)

| Signal | Metric | SLO | Alert Threshold |
|--------|--------|-----|-----------------|
| **Latency** | P50, P95, P99 | P95 < 200ms | P95 > 500ms for 5min |
| **Traffic** | Requests/sec | N/A | >50% drop in 5min |
| **Errors** | Error rate % | < 0.1% | > 1% for 2min |
| **Saturation** | CPU, Memory, Disk | < 80% | > 90% for 10min |

## 11.3 Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: slo-alerts
    rules:
      # Error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) 
          / sum(rate(http_requests_total[5m])) > 0.01
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook_url: "https://runbooks.example.com/high-error-rate"
          
      # Latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s"
          
      # Saturation
      - alert: HighCPU
        expr: |
          avg(rate(container_cpu_usage_seconds_total[5m])) by (pod) > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          
      # Circuit breaker
      - alert: CircuitBreakerOpen
        expr: circuit_breaker_state{state="open"} == 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Circuit breaker open for {{ $labels.service }}"
```

## 11.4 Dashboard Template (Grafana)

```json
{
  "dashboard": {
    "title": "[Service Name] Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (status)"
          }
        ]
      },
      {
        "title": "Latency (P50, P95, P99)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "P99"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m])) * 100"
          }
        ],
        "thresholds": "0.1,1",
        "colors": ["green", "orange", "red"]
      }
    ]
  }
}
```

---

# 12. DEPLOYMENT & OPERATIONS

## 12.1 CI/CD Pipeline

```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Build & Test
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
        
      - name: Lint (Ruff)
        run: ruff check .
        
      - name: Type check (MyPy)
        run: mypy src/
        
      - name: Unit tests
        run: pytest tests/unit --cov=src --cov-report=xml
        
      - name: Integration tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          pytest tests/integration --timeout=300
          
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        
  # Stage 2: Security
  security:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: SAST (Bandit)
        run: bandit -r src/ -f json -o bandit.json
        
      - name: Dependency scan (Snyk)
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
          
      - name: Secret scan (TruffleHog)
        uses: trufflesecurity/trufflehog@main
        
  # Stage 3: Build Docker
  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}
            
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          
      - name: Scan image (Trivy)
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          severity: 'CRITICAL,HIGH'
          
  # Stage 4: Deploy Staging
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        uses: azure/k8s-deploy@v4
        with:
          namespace: staging
          manifests: k8s/staging/
          images: ${{ needs.build.outputs.image_tag }}
          
      - name: Smoke tests
        run: |
          kubectl rollout status deployment/app -n staging
          ./scripts/smoke-test.sh https://staging.example.com
          
  # Stage 5: Deploy Production
  deploy-production:
    needs: [build, deploy-staging]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy canary (10%)
        uses: azure/k8s-deploy@v4
        with:
          strategy: canary
          percentage: 10
          namespace: production
          manifests: k8s/production/
          images: ${{ needs.build.outputs.image_tag }}
          
      - name: Monitor canary (10min)
        run: ./scripts/monitor-canary.sh 600
        
      - name: Promote to 100%
        uses: azure/k8s-deploy@v4
        with:
          strategy: canary
          action: promote
          namespace: production
          manifests: k8s/production/
```

## 12.2 Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue-Green with Kubernetes
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: myapp
    version: green  # Switch between blue/green
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: app
          image: myapp:v1.0.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
        - name: app
          image: myapp:v1.1.0
```

### Canary Deployment (Argo Rollouts)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: {duration: 5m}
        - setWeight: 20
        - pause: {duration: 10m}
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 80
        - pause: {duration: 5m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
        args:
          - name: service-name
            value: app
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:v1.1.0
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

## 12.3 Infrastructure as Code

### Terraform (AWS)

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "app/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "app-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = false
  
  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"
  
  cluster_name    = "app-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10
      
      instance_types = ["m6i.large"]
      capacity_type  = "ON_DEMAND"
    }
    
    spot = {
      desired_size = 2
      min_size     = 0
      max_size     = 20
      
      instance_types = ["m6i.large", "m5.large"]
      capacity_type  = "SPOT"
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.0.0"
  
  identifier = "app-db"
  
  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  major_engine_version = "15"
  instance_class       = "db.r6g.large"
  
  allocated_storage     = 100
  max_allocated_storage = 500
  
  db_name  = "app"
  username = "admin"
  port     = 5432
  
  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.security_group_rds.security_group_id]
  
  backup_retention_period = 35
  skip_final_snapshot     = false
  deletion_protection     = true
  
  performance_insights_enabled = true
  
  parameters = [
    {
      name  = "max_connections"
      value = "500"
    }
  ]
}

# ElastiCache Redis
module "redis" {
  source  = "terraform-aws-modules/elasticache/aws"
  version = "1.0.0"
  
  cluster_id           = "app-cache"
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.r6g.large"
  num_cache_nodes      = 2
  parameter_group_name = "default.redis7"
  
  subnet_group_name    = module.vpc.elasticache_subnet_group_name
  security_group_ids   = [module.security_group_redis.security_group_id]
  
  automatic_failover_enabled = true
  multi_az_enabled           = true
}
```

### Helm Chart

```yaml
# helm/app/values.yaml
replicaCount: 3

image:
  repository: ghcr.io/myorg/myapp
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 50
  targetCPUUtilizationPercentage: 70

env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
  - name: REDIS_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: redis-url

livenessProbe:
  httpGet:
    path: /health/live
    port: http
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5

podDisruptionBudget:
  enabled: true
  minAvailable: 2
```

---

# 13. TESTING STRATEGY

## 13.1 Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  5%  - Slow, expensive
                   ─┴─────────┴─
                  ┌─────────────┐
                  │ Integration │  15% - Medium speed
                 ─┴─────────────┴─
                ┌─────────────────┐
                │      Unit       │  80% - Fast, cheap
               ─┴─────────────────┴─
```

| Level | Coverage | Tools | Speed |
|-------|----------|-------|-------|
| Unit | 80% | pytest, unittest | <1s each |
| Integration | 60% | pytest, testcontainers | <30s each |
| E2E | Critical paths | Playwright, Cypress | <5min each |
| Load | N/A | k6, Locust | As needed |

## 13.2 Unit Testing

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.user_service import UserService
from src.models import User, CreateUserRequest

class TestUserService:
    @pytest.fixture
    def user_repo(self):
        return AsyncMock()
        
    @pytest.fixture
    def cache(self):
        return AsyncMock()
        
    @pytest.fixture
    def service(self, user_repo, cache):
        return UserService(user_repo, cache)
        
    @pytest.mark.asyncio
    async def test_create_user_success(self, service, user_repo):
        # Arrange
        user_repo.find_by_email.return_value = None
        request = CreateUserRequest(
            email="test@example.com",
            password="SecureP@ss123",
            name="Test User"
        )
        
        # Act
        result = await service.create_user(request)
        
        # Assert
        assert result.email == "test@example.com"
        assert result.status == "PENDING"
        user_repo.save.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, service, user_repo):
        # Arrange
        user_repo.find_by_email.return_value = User(id="123", email="test@example.com")
        request = CreateUserRequest(
            email="test@example.com",
            password="SecureP@ss123",
            name="Test"
        )
        
        # Act & Assert
        with pytest.raises(EmailExistsError):
            await service.create_user(request)
            
    @pytest.mark.asyncio
    async def test_get_user_from_cache(self, service, user_repo, cache):
        # Arrange
        cached_user = {"id": "123", "email": "test@example.com"}
        cache.get.return_value = cached_user
        
        # Act
        result = await service.get_user("123")
        
        # Assert
        assert result.id == "123"
        user_repo.find_by_id.assert_not_called()  # DB not hit
```

## 13.3 Integration Testing

```python
# tests/integration/test_user_api.py
import pytest
from httpx import AsyncClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres
        
@pytest.fixture(scope="session")
def redis():
    with RedisContainer("redis:7") as redis:
        yield redis

@pytest.fixture
async def client(postgres, redis):
    app.config["DATABASE_URL"] = postgres.get_connection_url()
    app.config["REDIS_URL"] = redis.get_connection_url()
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

class TestUserAPI:
    @pytest.mark.asyncio
    async def test_create_user_e2e(self, client):
        # Create user
        response = await client.post("/api/v1/users", json={
            "email": "integration@test.com",
            "password": "SecureP@ss123!",
            "name": "Integration Test"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "integration@test.com"
        user_id = data["id"]
        
        # Get user
        response = await client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "integration@test.com"
        
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, client):
        # Create first user
        await client.post("/api/v1/users", json={
            "email": "duplicate@test.com",
            "password": "SecureP@ss123!",
            "name": "First"
        })
        
        # Try duplicate
        response = await client.post("/api/v1/users", json={
            "email": "duplicate@test.com",
            "password": "SecureP@ss123!",
            "name": "Second"
        })
        
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "EMAIL_EXISTS"
```

## 13.4 Load Testing

```python
# load_tests/locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login and get token
        response = self.client.post("/auth/login", json={
            "email": "loadtest@example.com",
            "password": "TestP@ss123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
    @task(10)
    def get_products(self):
        self.client.get("/api/v1/products", headers=self.headers)
        
    @task(3)
    def search_products(self):
        self.client.get("/api/v1/products/search?q=test", headers=self.headers)
        
    @task(1)
    def create_order(self):
        self.client.post("/api/v1/orders", 
            json={
                "items": [{"product_id": "prod_123", "quantity": 1}]
            },
            headers=self.headers
        )
```

```bash
# Run load test
locust -f load_tests/locustfile.py \
  --host=https://staging.example.com \
  --users=1000 \
  --spawn-rate=50 \
  --run-time=10m \
  --html=report.html
```

## 13.5 Contract Testing (Pact)

```python
# tests/contract/test_user_service_provider.py
from pact import Verifier

def test_user_service_provider():
    verifier = Verifier(
        provider="UserService",
        provider_base_url="http://localhost:8000"
    )
    
    output = verifier.verify_pacts(
        "./pacts",
        enable_pending=True,
        provider_states_setup_url="http://localhost:8000/_pact/provider-states",
        publish_verification_results=True,
        provider_app_version=os.getenv("GIT_COMMIT")
    )
    
    assert output == 0
```

---

# PART IV: QUALITY & GOVERNANCE

---

# 14. NON-FUNCTIONAL REQUIREMENTS (NFR)

## 14.1 Performance Requirements

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| P50 Latency | 100ms | 50ms | Datadog APM |
| P95 Latency | 500ms | 200ms | Datadog APM |
| P99 Latency | 2s | 500ms | Datadog APM |
| Throughput | 500 rps | 2000 rps | Load test |
| Error Rate | 1% | 0.1% | Prometheus |

### Endpoint Performance Baselines

| Endpoint | P50 | P95 | P99 | Max RPS |
|----------|-----|-----|-----|---------|
| GET /users/{id} | 20ms | 50ms | 100ms | 5000 |
| POST /users | 50ms | 150ms | 300ms | 1000 |
| GET /products | 30ms | 100ms | 200ms | 3000 |
| POST /orders | 100ms | 300ms | 500ms | 500 |

## 14.2 Scalability Requirements

| Dimension | Current | Target | Strategy |
|-----------|---------|--------|----------|
| Users | 10K DAU | 100K DAU | Horizontal scaling |
| Data | 100GB | 1TB | Partitioning |
| Requests | 500 rps | 5000 rps | Auto-scaling |

### Auto-scaling Configuration

```yaml
# HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 100
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

## 14.3 Reliability Requirements

| Metric | Target | Calculation |
|--------|--------|-------------|
| **Availability (SLA)** | 99.9% | 8.76h downtime/year |
| **MTBF** | >720 hours | Historical data |
| **MTTR** | <30 minutes | Incident tracking |
| **RPO** | <15 minutes | Backup frequency |
| **RTO** | <1 hour | DR testing |

## 14.4 Security Requirements

- [ ] All data encrypted at rest (AES-256)
- [ ] All communications over TLS 1.3
- [ ] No hardcoded secrets
- [ ] Rate limiting on all public endpoints
- [ ] Input validation on all inputs
- [ ] OWASP Top 10 compliance
- [ ] SOC2 Type II compliance
- [ ] Annual penetration testing

## 14.5 Maintainability Requirements

| Metric | Target | Tool |
|--------|--------|------|
| Code Coverage | >80% | pytest-cov |
| Cyclomatic Complexity | <10/function | Radon |
| Documentation | 100% public APIs | OpenAPI |
| Tech Debt Ratio | <5% | SonarQube |

---

# 15. PERFORMANCE & CAPACITY PLANNING

## 15.1 Capacity Planning Formulas

### Traffic Estimation

```
Daily Active Users (DAU) = Monthly Active Users × 0.3
Peak Concurrent Users = DAU × 0.1
Requests per Second (RPS) = Peak Users × Actions per Minute / 60

Example:
- MAU: 1,000,000
- DAU: 300,000 (30% of MAU)
- Peak concurrent: 30,000 (10% of DAU)
- Actions/minute: 5
- Peak RPS: 30,000 × 5 / 60 = 2,500 RPS
```

### Database Sizing

```
Storage = Records × Avg Record Size × Replication Factor × Growth Factor

Example:
- Records: 10,000,000
- Avg size: 2KB
- Replication: 3
- Growth (2 years): 2x
- Storage: 10M × 2KB × 3 × 2 = 120GB

IOPS = (Read RPS × Read Ratio) + (Write RPS × Write Ratio × Write Amplification)

Example:
- Read RPS: 5,000
- Write RPS: 500
- Write amplification: 2 (indexes)
- IOPS: 5,000 + (500 × 2) = 6,000 IOPS
```

### Memory Sizing

```
Cache Memory = Working Set × Hit Ratio Target / Hit Ratio Actual

Example:
- Working set: 10GB
- Target hit ratio: 95%
- Current hit ratio: 80%
- Cache needed: 10GB × 0.95 / 0.80 = 11.9GB
```

## 15.2 Benchmarking Methodology

### Benchmark Types

| Type | Purpose | Duration | Tools |
|------|---------|----------|-------|
| Baseline | Current performance | 30 min | k6 |
| Load | Normal traffic | 1 hour | Locust |
| Stress | Find limits | Until failure | k6 |
| Soak | Memory leaks | 24 hours | Locust |
| Spike | Sudden traffic | 15 min | k6 |

### Benchmark Script Template

```javascript
// k6 load test script
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latency = new Trend('latency');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Stay
    { duration: '2m', target: 200 },   // Ramp up more
    { duration: '5m', target: 200 },   // Stay
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],  // P95 < 200ms
    errors: ['rate<0.01'],              // Error rate < 1%
  },
};

export default function () {
  const start = Date.now();
  
  const res = http.get('https://api.example.com/users/123', {
    headers: { 'Authorization': `Bearer ${__ENV.TOKEN}` },
  });
  
  latency.add(Date.now() - start);
  
  const success = check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  
  errorRate.add(!success);
  
  sleep(1);
}
```

## 15.3 Capacity Planning Table

| Component | Current | +6 Months | +1 Year | +2 Years |
|-----------|---------|-----------|---------|----------|
| **Users (DAU)** | 10K | 50K | 150K | 500K |
| **API RPS** | 100 | 500 | 1500 | 5000 |
| **DB Storage** | 50GB | 150GB | 400GB | 1TB |
| **DB IOPS** | 1000 | 3000 | 8000 | 20000 |
| **Cache Memory** | 2GB | 8GB | 20GB | 50GB |
| **App Pods** | 3 | 10 | 25 | 60 |
| **Est. Monthly Cost** | $2K | $8K | $20K | $50K |

---

# 16. COST OPTIMIZATION

## 16.1 Cloud Cost Breakdown

| Service | Monthly Cost | % of Total | Optimization |
|---------|-------------|------------|--------------|
| EKS | $500 | 25% | Spot instances |
| RDS | $400 | 20% | Reserved instances |
| ElastiCache | $200 | 10% | Right-size |
| S3 | $100 | 5% | Lifecycle policies |
| Data Transfer | $300 | 15% | CDN, compression |
| Others | $500 | 25% | Review unused |
| **Total** | **$2,000** | 100% | |

## 16.2 Cost Optimization Strategies

### 1. Compute Optimization

```yaml
# Use spot instances for non-critical workloads
eks_managed_node_groups:
  spot-workers:
    instance_types: ["m6i.large", "m5.large", "m5a.large"]
    capacity_type: SPOT
    desired_size: 5
    
  on-demand-workers:
    instance_types: ["m6i.large"]
    capacity_type: ON_DEMAND
    desired_size: 2  # Minimum for critical workloads
```

### 2. Storage Optimization

```python
# S3 Lifecycle policy
lifecycle_rules = [
    {
        "id": "archive-old-logs",
        "filter": {"prefix": "logs/"},
        "transitions": [
            {"days": 30, "storage_class": "STANDARD_IA"},
            {"days": 90, "storage_class": "GLACIER"},
        ],
        "expiration": {"days": 365}
    }
]
```

### 3. Database Optimization

```sql
-- Identify unused indexes
SELECT 
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan AS index_scans
FROM pg_stat_user_indexes ui
JOIN pg_index i ON ui.indexrelid = i.indexrelid
WHERE idx_scan < 50
ORDER BY pg_relation_size(i.indexrelid) DESC;

-- Identify large tables for partitioning
SELECT 
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    n_live_tup AS row_count
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
```

### 4. Cost Monitoring Dashboard

```yaml
# CloudWatch cost anomaly detection
resource "aws_ce_anomaly_monitor" "cost" {
  name              = "ServiceCostMonitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "alert" {
  name      = "CostAnomalyAlert"
  frequency = "IMMEDIATE"
  
  monitor_arn_list = [aws_ce_anomaly_monitor.cost.arn]
  
  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_PERCENTAGE"
      values        = ["10"]
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
  
  subscriber {
    type    = "EMAIL"
    address = "platform-team@example.com"
  }
}
```

## 16.3 Cost per Request Analysis

```python
# Calculate cost per request
def calculate_cost_per_request(monthly_cost: float, monthly_requests: int) -> dict:
    cost_per_request = monthly_cost / monthly_requests
    
    return {
        "monthly_cost": monthly_cost,
        "monthly_requests": monthly_requests,
        "cost_per_request": cost_per_request,
        "cost_per_1000_requests": cost_per_request * 1000,
        "cost_per_million_requests": cost_per_request * 1_000_000
    }

# Example
result = calculate_cost_per_request(
    monthly_cost=2000,
    monthly_requests=50_000_000
)
# cost_per_request: $0.00004
# cost_per_million: $40
```

---

# 17. TRADE-OFFS & ARCHITECTURE DECISIONS

## 17.1 Architecture Decision Records (ADR)

### ADR-001: Database Selection

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2024-01-15 |
| **Deciders** | Tech Lead, Architect, DBA |
| **Context** | Need primary database for transactional data with complex queries |
| **Decision** | PostgreSQL 15 over MongoDB |
| **Rationale** | ACID compliance required for financial transactions, complex JOINs needed, team expertise, mature ecosystem |
| **Consequences** | ✅ Strong consistency, ✅ Rich SQL features, ✅ Extensions (pg_trgm, PostGIS); ⚠️ Requires schema migrations, ⚠️ Horizontal scaling more complex |
| **Alternatives Rejected** | MongoDB (eventual consistency), CockroachDB (operational complexity), Aurora (cost) |

### ADR-002: Message Queue Selection

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2024-01-15 |
| **Context** | Need async communication for event-driven architecture |
| **Decision** | Apache Kafka over RabbitMQ |
| **Rationale** | Higher throughput (100K+ msg/s), event replay capability, event sourcing support, better durability |
| **Consequences** | ✅ High throughput, ✅ Replay capability; ⚠️ More operational complexity, ⚠️ Higher resource usage |

### ADR-003: API Style

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2024-01-20 |
| **Context** | Need API style for client-service communication |
| **Decision** | REST + OpenAPI for external APIs, gRPC for internal services |
| **Rationale** | REST is universally supported, better tooling; gRPC for internal high-performance needs |
| **Consequences** | ✅ Wide client support, ✅ Good documentation; ⚠️ Two protocols to maintain |

## 17.2 Trade-off Analysis Matrix

| Decision | Option A | Option B | Chosen | Reason |
|----------|----------|----------|--------|--------|
| Consistency vs Availability | CP | AP | CP | Financial data requires consistency |
| Latency vs Throughput | Low latency | High throughput | Low latency | User experience priority |
| Cost vs Performance | Save cost | Max performance | Balanced | 99.9% SLA at reasonable cost |
| Build vs Buy | Custom | SaaS | SaaS (Auth0) | Faster time-to-market |
| Monolith vs Microservices | Monolith | Microservices | Microservices | Team autonomy, scale independently |

## 17.3 CAP Theorem Position

```
                 Consistency
                     ▲
                    /|\
                   / | \
                  /  |  \
                 /   |   \
                /    |    \
               /     |     \
              /      |      \
             /   CP  |  CA   \
            /        |        \
           /    [WE ARE       \
          /      HERE]         \
         /           |          \
        /___________ | ___________\
       Partition    AP    Availability
       Tolerance

Our choice: CP (Consistency + Partition Tolerance)
- Strong consistency for transactions
- Accept temporary unavailability during network partitions
- Use async replication for read replicas
```

---

# PART V: OPERATIONS & MLOps

---

# 18. INCIDENT RESPONSE & RUNBOOKS

## 18.1 Incident Severity Levels

| Severity | Definition | Response Time | Resolution Time | Escalation |
|----------|------------|---------------|-----------------|------------|
| **SEV1** | Complete outage, data loss | 5 min | 1 hour | VP Eng |
| **SEV2** | Major feature down | 15 min | 4 hours | Eng Manager |
| **SEV3** | Minor feature degraded | 1 hour | 24 hours | Tech Lead |
| **SEV4** | Cosmetic/minor issue | 4 hours | 1 week | Team |

## 18.2 On-Call Procedures

### On-Call Rotation

```yaml
# PagerDuty schedule
rotation:
  name: "Platform Team Primary"
  type: weekly
  handoff_time: "09:00 Monday"
  
  members:
    - name: "Engineer A"
      start: "2024-01-01"
    - name: "Engineer B"
      start: "2024-01-08"
    - name: "Engineer C"
      start: "2024-01-15"
      
escalation:
  - level: 1
    timeout: 5m
    target: on-call-primary
  - level: 2
    timeout: 15m
    target: on-call-secondary
  - level: 3
    timeout: 30m
    target: engineering-manager
```

### On-Call Handoff Checklist

- [ ] Review open incidents from last week
- [ ] Check monitoring dashboards
- [ ] Verify access to all systems
- [ ] Review recent deployments
- [ ] Update personal contact info

## 18.3 Runbook Templates

### Runbook: High Error Rate

```markdown
# Runbook: High Error Rate Alert

## Overview
- **Alert**: HighErrorRate (>1% for 2 minutes)
- **Severity**: SEV2
- **Owner**: Platform Team

## Symptoms
- Error rate exceeds 1%
- Users reporting 5xx errors
- Spike in error logs

## Diagnosis Steps

### Step 1: Check Service Health
```bash
kubectl get pods -n production
kubectl logs -f deployment/api -n production --tail=100
```

### Step 2: Check Dependencies
```bash
# Database
kubectl exec -it postgres-0 -- pg_isready

# Redis
kubectl exec -it redis-0 -- redis-cli ping

# External APIs
curl -s https://api.stripe.com/healthcheck
```

### Step 3: Check Recent Changes
```bash
# Recent deployments
kubectl rollout history deployment/api -n production

# Recent config changes
git log --oneline -10 -- k8s/
```

## Resolution Steps

### If: Database connection issues
```bash
# Restart DB connections
kubectl rollout restart deployment/api -n production
```

### If: Memory/CPU exhaustion
```bash
# Scale up
kubectl scale deployment/api --replicas=10 -n production
```

### If: Bad deployment
```bash
# Rollback
kubectl rollout undo deployment/api -n production
```

## Escalation
- If not resolved in 30 minutes: Page Engineering Manager
- If data loss suspected: Page VP Engineering

## Post-Incident
- [ ] Create incident report
- [ ] Schedule post-mortem
- [ ] Create follow-up tickets
```

### Runbook: Database Connection Pool Exhausted

```markdown
# Runbook: Database Connection Pool Exhausted

## Alert
- Connection pool usage > 90%
- "too many connections" errors

## Immediate Actions

### Step 1: Identify Connection Leaks
```sql
SELECT 
    pid, 
    usename, 
    application_name,
    client_addr,
    state,
    query_start,
    NOW() - query_start AS duration,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC
LIMIT 20;
```

### Step 2: Kill Long-Running Queries
```sql
-- Kill queries running > 5 minutes
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE duration > interval '5 minutes'
  AND state != 'idle';
```

### Step 3: Scale Connection Pool
```bash
# Increase max connections temporarily
kubectl set env deployment/api DATABASE_POOL_SIZE=50 -n production
```

## Root Cause Investigation
- Check for connection leaks in code
- Verify connection pool settings
- Review slow query log
```

## 18.4 Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

## Summary
| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Duration | X hours Y minutes |
| Severity | SEV2 |
| Impact | Z% of users affected |
| Root Cause | [Brief description] |

## Timeline (all times in UTC)
| Time | Event |
|------|-------|
| 14:00 | Deployment started |
| 14:15 | Alert fired: HighErrorRate |
| 14:17 | On-call engineer acknowledged |
| 14:25 | Root cause identified |
| 14:30 | Rollback initiated |
| 14:35 | Service restored |

## Root Cause Analysis
[Detailed explanation of what went wrong]

## Impact
- X% of API requests failed
- Y users affected
- Z orders delayed

## What Went Well
- Alert fired quickly
- Rollback was smooth
- Communication was clear

## What Went Poorly
- Took 10 minutes to identify root cause
- Missing runbook for this scenario

## Action Items
| Action | Owner | Due Date | Ticket |
|--------|-------|----------|--------|
| Add integration test | @engineer | 2024-01-20 | JIRA-123 |
| Update runbook | @sre | 2024-01-22 | JIRA-124 |
| Add circuit breaker | @engineer | 2024-01-25 | JIRA-125 |

## Lessons Learned
[Key takeaways for the team]
```

---

# 19. MLOps (MACHINE LEARNING OPERATIONS)

> 🤖 **Note**: Section này chỉ applicable nếu system có ML components

## 19.1 ML System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ML SYSTEM ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      DATA PIPELINE                                  │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐   │ │
│  │  │   Raw    │──▶│  Clean   │──▶│ Feature  │──▶│   Feature    │   │ │
│  │  │  Data    │   │  Data    │   │ Engineer │   │    Store     │   │ │
│  │  │  (S3)    │   │ (Spark)  │   │          │   │  (Feast)     │   │ │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                      │                                   │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      TRAINING PIPELINE                              │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐   │ │
│  │  │ Feature  │──▶│  Model   │──▶│  Model   │──▶│   Model      │   │ │
│  │  │  Store   │   │ Training │   │  Eval    │   │  Registry    │   │ │
│  │  │          │   │(PyTorch) │   │          │   │  (MLflow)    │   │ │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                      │                                   │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                      SERVING PIPELINE                               │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐   │ │
│  │  │  Model   │──▶│  Model   │──▶│  A/B     │──▶│  Monitoring  │   │ │
│  │  │ Registry │   │ Serving  │   │  Test    │   │  & Logging   │   │ │
│  │  │          │   │(TorchSrv)│   │          │   │              │   │ │
│  │  └──────────┘   └──────────┘   └──────────┘   └──────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 19.2 Model Training Pipeline

```python
# training/pipeline.py
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import torch

class TrainingPipeline:
    def __init__(self, config: dict):
        self.config = config
        mlflow.set_tracking_uri(config["mlflow_uri"])
        mlflow.set_experiment(config["experiment_name"])
        
    def run(self, data_path: str):
        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(self.config["hyperparameters"])
            
            # Load and prepare data
            X_train, X_test, y_train, y_test = self.prepare_data(data_path)
            
            # Train model
            model = self.train_model(X_train, y_train)
            
            # Evaluate
            metrics = self.evaluate(model, X_test, y_test)
            mlflow.log_metrics(metrics)
            
            # Save model
            mlflow.pytorch.log_model(
                model, 
                "model",
                registered_model_name=self.config["model_name"]
            )
            
            # Log artifacts
            mlflow.log_artifact("feature_importance.png")
            
            return metrics
            
    def train_model(self, X_train, y_train):
        model = MyModel(self.config["hyperparameters"])
        
        for epoch in range(self.config["epochs"]):
            loss = model.train_epoch(X_train, y_train)
            mlflow.log_metric("train_loss", loss, step=epoch)
            
        return model
        
    def evaluate(self, model, X_test, y_test) -> dict:
        predictions = model.predict(X_test)
        return {
            "accuracy": accuracy_score(y_test, predictions),
            "f1_score": f1_score(y_test, predictions),
        }
```

## 19.3 Model Serving

```python
# serving/model_server.py
from fastapi import FastAPI
import mlflow
from prometheus_client import Counter, Histogram

# Metrics
PREDICTION_COUNT = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_name', 'model_version']
)

PREDICTION_LATENCY = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency',
    ['model_name']
)

app = FastAPI()

class ModelServer:
    def __init__(self):
        self.model = None
        self.model_version = None
        
    def load_model(self, model_name: str, version: str = "latest"):
        model_uri = f"models:/{model_name}/{version}"
        self.model = mlflow.pytorch.load_model(model_uri)
        self.model_version = version
        
    @app.post("/predict")
    async def predict(self, request: PredictRequest):
        start_time = time.time()
        
        try:
            # Feature extraction
            features = self.extract_features(request)
            
            # Inference
            prediction = self.model.predict(features)
            
            # Log metrics
            PREDICTION_COUNT.labels(
                model_name=request.model_name,
                model_version=self.model_version
            ).inc()
            
            PREDICTION_LATENCY.labels(
                model_name=request.model_name
            ).observe(time.time() - start_time)
            
            return PredictResponse(
                prediction=prediction,
                model_version=self.model_version,
                latency_ms=(time.time() - start_time) * 1000
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
```

## 19.4 Model Monitoring

```python
# monitoring/model_monitor.py
from evidently import ColumnMapping
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, ModelPerformanceTab

class ModelMonitor:
    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.column_mapping = ColumnMapping(
            target="label",
            prediction="prediction",
            numerical_features=["feature1", "feature2"],
            categorical_features=["feature3"]
        )
        
    def check_data_drift(self, current_data: pd.DataFrame) -> dict:
        """Detect data drift between reference and current data"""
        dashboard = Dashboard(tabs=[DataDriftTab()])
        dashboard.calculate(
            self.reference_data,
            current_data,
            column_mapping=self.column_mapping
        )
        
        # Get drift score
        drift_score = dashboard.get_drift_score()
        
        if drift_score > 0.1:
            logger.warning(f"Data drift detected: {drift_score}")
            self.alert_team("Data drift detected", drift_score)
            
        return {"drift_score": drift_score}
        
    def check_model_performance(self, predictions_df: pd.DataFrame) -> dict:
        """Monitor model performance over time"""
        metrics = {
            "accuracy": accuracy_score(predictions_df["actual"], predictions_df["predicted"]),
            "f1": f1_score(predictions_df["actual"], predictions_df["predicted"]),
        }
        
        # Check against baseline
        if metrics["accuracy"] < 0.9 * self.baseline_accuracy:
            logger.error("Model performance degradation detected")
            self.trigger_retraining()
            
        return metrics
```

## 19.5 A/B Testing for ML Models

```python
# ab_testing/experiment.py
import hashlib

class ABExperiment:
    def __init__(self, experiment_id: str, variants: dict):
        """
        variants = {
            "control": {"model_version": "v1", "weight": 0.5},
            "treatment": {"model_version": "v2", "weight": 0.5}
        }
        """
        self.experiment_id = experiment_id
        self.variants = variants
        
    def get_variant(self, user_id: str) -> str:
        """Deterministic variant assignment based on user ID"""
        hash_value = hashlib.md5(
            f"{self.experiment_id}:{user_id}".encode()
        ).hexdigest()
        
        hash_int = int(hash_value, 16) % 100
        
        cumulative = 0
        for variant_name, config in self.variants.items():
            cumulative += config["weight"] * 100
            if hash_int < cumulative:
                return variant_name
                
        return list(self.variants.keys())[0]
        
    async def log_outcome(self, user_id: str, variant: str, outcome: dict):
        """Log experiment outcome for analysis"""
        await experiment_store.save({
            "experiment_id": self.experiment_id,
            "user_id": user_id,
            "variant": variant,
            "outcome": outcome,
            "timestamp": datetime.utcnow()
        })
```

## 19.6 ML Checklist

- [ ] Data pipeline automated and version-controlled
- [ ] Feature store implemented
- [ ] Model training reproducible
- [ ] Model versioned in registry
- [ ] Model serving scalable
- [ ] A/B testing framework ready
- [ ] Data drift monitoring active
- [ ] Model performance monitoring active
- [ ] Retraining pipeline automated
- [ ] Model explainability implemented

---

# PART VI: LAUNCH & BEYOND

---

# 20. IMPLEMENTATION ROADMAP

## 20.1 Phase Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     IMPLEMENTATION ROADMAP                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 1          Phase 2          Phase 3          Phase 4             │
│  Foundation       Core Features    Scale & Polish   Production          │
│  (4 weeks)        (6 weeks)        (4 weeks)        (2 weeks)           │
│                                                                          │
│  ┌────────┐       ┌────────┐       ┌────────┐       ┌────────┐         │
│  │ Infra  │──────▶│  MVP   │──────▶│  Scale │──────▶│ Launch │         │
│  │ Setup  │       │ Build  │       │  Test  │       │ Ready  │         │
│  └────────┘       └────────┘       └────────┘       └────────┘         │
│                                                                          │
│  Deliverables:    Deliverables:    Deliverables:    Deliverables:       │
│  - CI/CD          - User Service   - Load testing   - Runbooks          │
│  - IaC            - Product Svc    - Perf tuning    - Training          │
│  - Monitoring     - Order Service  - Security audit - DR test           │
│  - Security       - Payment        - Documentation  - Launch!           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 20.2 Detailed Phase Breakdown

### Phase 1: Foundation (Weeks 1-4)

| Week | Tasks | Owner | Deliverable |
|------|-------|-------|-------------|
| 1 | Setup IaC (Terraform) | DevOps | VPC, EKS cluster |
| 1 | Setup CI/CD pipeline | DevOps | GitHub Actions |
| 2 | Setup monitoring | SRE | Prometheus, Grafana |
| 2 | Setup logging | SRE | ELK stack |
| 3 | Database setup | DBA | PostgreSQL, Redis |
| 3 | Security baseline | Security | IAM, secrets |
| 4 | Development environment | DevOps | Local + staging |
| 4 | Documentation | All | Architecture docs |

**Exit Criteria:**
- [ ] All infrastructure provisioned
- [ ] CI/CD deploying to staging
- [ ] Monitoring dashboards live
- [ ] Security scan passing

### Phase 2: Core Features (Weeks 5-10)

| Week | Tasks | Owner | Deliverable |
|------|-------|-------|-------------|
| 5-6 | User Service | Backend | Auth, profile |
| 6-7 | Product Service | Backend | CRUD, search |
| 7-8 | Order Service | Backend | Ordering flow |
| 8-9 | Payment Integration | Backend | Stripe |
| 9-10 | Frontend integration | Frontend | React app |
| 10 | Integration testing | QA | Test coverage |

**Exit Criteria:**
- [ ] All MVP features working
- [ ] Integration tests passing
- [ ] Code coverage > 80%
- [ ] API documentation complete

### Phase 3: Scale & Polish (Weeks 11-14)

| Week | Tasks | Owner | Deliverable |
|------|-------|-------|-------------|
| 11 | Load testing | QA | Performance report |
| 11-12 | Performance tuning | Backend | Optimized queries |
| 12 | Security audit | Security | Pen test report |
| 13 | Bug fixes | All | Bug-free system |
| 13-14 | Documentation | All | User guides |
| 14 | UAT | Product | Sign-off |

**Exit Criteria:**
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] UAT approved
- [ ] All critical bugs fixed

### Phase 4: Production (Weeks 15-16)

| Week | Tasks | Owner | Deliverable |
|------|-------|-------|-------------|
| 15 | Runbooks | SRE | Operations docs |
| 15 | DR testing | SRE | DR verified |
| 15 | Team training | All | Trained team |
| 16 | Soft launch (10%) | All | Canary release |
| 16 | Full launch | All | Production! |

**Exit Criteria:**
- [ ] Production readiness checklist complete
- [ ] Runbooks verified
- [ ] Team trained
- [ ] Launched successfully

## 20.3 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Schedule slip | Medium | High | Buffer time, scope reduction |
| Tech debt | High | Medium | Regular refactoring |
| Key person leave | Low | High | Knowledge sharing |
| Dependency delay | Medium | Medium | Early coordination |

---

# 21. PRODUCTION READINESS CHECKLIST

## 21.1 Pre-Launch Checklist

### Architecture & Design ✅
- [ ] Architecture documented and reviewed
- [ ] Scalability plan defined (horizontal + vertical)
- [ ] Capacity planning completed
- [ ] Load balancing configured
- [ ] Disaster recovery plan tested
- [ ] Trade-offs documented (ADRs)

### Reliability ✅
- [ ] Retry logic implemented with exponential backoff
- [ ] Circuit breakers configured for all external calls
- [ ] Timeouts set appropriately (connect, read, write)
- [ ] Fallback strategies defined
- [ ] Health checks implemented (liveness + readiness)
- [ ] Graceful shutdown implemented
- [ ] Idempotency for critical operations

### Observability ✅
- [ ] Metrics collection (Prometheus)
- [ ] Structured logging (JSON format)
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Alerting rules configured
- [ ] Dashboards created (Golden Signals)
- [ ] On-call schedule established
- [ ] Log retention policy defined

### Security ✅
- [ ] Authentication implemented (OAuth 2.0/JWT)
- [ ] Authorization (RBAC) implemented
- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.3)
- [ ] Security scanning passed (SAST, DAST)
- [ ] Penetration testing completed
- [ ] Secrets management setup (Vault)
- [ ] OWASP Top 10 addressed
- [ ] Input validation on all endpoints
- [ ] Rate limiting configured

### Testing ✅
- [ ] Unit tests > 80% coverage
- [ ] Integration tests > 60% coverage
- [ ] E2E tests for critical paths
- [ ] Load testing completed (target RPS achieved)
- [ ] Security testing completed
- [ ] Chaos engineering performed
- [ ] Contract tests passing

### Deployment ✅
- [ ] CI/CD pipeline setup
- [ ] Automated testing in pipeline
- [ ] Deployment strategy chosen (Blue-Green/Canary)
- [ ] Rollback strategy tested
- [ ] Infrastructure as Code (Terraform)
- [ ] Environment parity (staging ≈ production)
- [ ] Feature flags implemented

### Documentation ✅
- [ ] API documentation (OpenAPI)
- [ ] Architecture documentation
- [ ] Runbooks written
- [ ] Incident response plan
- [ ] Post-mortem template ready
- [ ] Team training completed

### Operations ✅
- [ ] SLO/SLI/SLA defined
- [ ] Error budget established
- [ ] Capacity planning done
- [ ] Cost monitoring setup
- [ ] Compliance requirements met

## 21.2 Launch Day Checklist

### T-24 Hours
- [ ] Final deployment to production
- [ ] Smoke tests passed
- [ ] Monitoring verified
- [ ] On-call team confirmed
- [ ] Communication plan ready

### T-1 Hour
- [ ] All systems green
- [ ] War room setup
- [ ] Stakeholders notified
- [ ] Rollback plan reviewed

### Launch
- [ ] Feature flag enabled
- [ ] Monitor error rates
- [ ] Monitor latency
- [ ] Monitor resource usage
- [ ] Ready to rollback if needed

### T+1 Hour
- [ ] Metrics within SLO
- [ ] No critical bugs
- [ ] User feedback positive
- [ ] Celebrate! 🎉

---

# 22. COMMON MISTAKES & ANTI-PATTERNS

## 22.1 Architecture Anti-Patterns

### ❌ Distributed Monolith

**Problem:** Microservices that are tightly coupled, requiring synchronized deployments.

```
# Bad: Services depend on each other's internal state
OrderService → directly calls → UserService.get_user_internal()
```

**Solution:**
```
# Good: Services communicate via APIs/events
OrderService → calls → UserService API /users/{id}
OrderService → publishes → UserCreated event
```

### ❌ Chatty Services

**Problem:** Too many network calls between services.

```python
# Bad: Multiple calls
user = await user_service.get_user(user_id)
address = await user_service.get_address(user_id)
preferences = await user_service.get_preferences(user_id)
```

**Solution:**
```python
# Good: Aggregate endpoint or GraphQL
user_data = await user_service.get_user_complete(user_id)
# Returns: {user, address, preferences}
```

### ❌ Missing Idempotency

**Problem:** Duplicate requests cause duplicate operations.

```python
# Bad: Non-idempotent order creation
@app.post("/orders")
async def create_order(request):
    order = Order(**request.dict())
    await db.save(order)  # Creates duplicate on retry!
    return order
```

**Solution:**
```python
# Good: Idempotent with idempotency key
@app.post("/orders")
async def create_order(request, idempotency_key: str = Header()):
    existing = await cache.get(f"idempotency:{idempotency_key}")
    if existing:
        return existing  # Return cached response
        
    order = Order(**request.dict())
    await db.save(order)
    await cache.setex(f"idempotency:{idempotency_key}", 86400, order)
    return order
```

## 22.2 Database Anti-Patterns

### ❌ N+1 Query Problem

```python
# Bad: N+1 queries
orders = await Order.query.all()
for order in orders:
    user = await User.query.get(order.user_id)  # N queries!
```

```python
# Good: Eager loading
orders = await Order.query.options(
    joinedload(Order.user)
).all()
```

### ❌ Missing Indexes

```sql
-- Bad: Full table scan
SELECT * FROM orders WHERE user_id = 'xyz' AND status = 'pending';
-- Execution time: 2.5s (seq scan)

-- Good: Add composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Execution time: 5ms (index scan)
```

### ❌ Unbounded Queries

```python
# Bad: No limit
users = await User.query.all()  # Returns ALL users!

# Good: Always paginate
users = await User.query.limit(100).offset(page * 100).all()
```

## 22.3 Security Anti-Patterns

### ❌ Hardcoded Secrets

```python
# Bad
DATABASE_URL = "postgresql://admin:supersecret123@db.example.com/mydb"

# Good
DATABASE_URL = os.environ.get("DATABASE_URL")
# Or use secrets manager
DATABASE_URL = await secrets_manager.get_secret("database-url")
```

### ❌ Missing Rate Limiting

```python
# Bad: No rate limiting
@app.post("/login")
async def login(request):
    return await authenticate(request.email, request.password)

# Good: Rate limited
@app.post("/login")
@rate_limit(requests=5, window=60)  # 5 per minute
async def login(request):
    return await authenticate(request.email, request.password)
```

### ❌ SQL Injection

```python
# Bad: String concatenation
query = f"SELECT * FROM users WHERE email = '{email}'"

# Good: Parameterized query
query = "SELECT * FROM users WHERE email = $1"
result = await db.execute(query, [email])
```

## 22.4 Observability Anti-Patterns

### ❌ Log Spam

```python
# Bad: Logging inside tight loops
for item in items:
    logger.info(f"Processing item {item.id}")  # Millions of logs!
    process(item)

# Good: Aggregate logging
logger.info(f"Processing {len(items)} items")
for item in items:
    process(item)
logger.info(f"Processed {len(items)} items successfully")
```

### ❌ Missing Trace Context

```python
# Bad: No correlation
logger.info("Order created")
# In another service
logger.info("Payment processed")  # Can't correlate!

# Good: With trace ID
logger.info("Order created", extra={"trace_id": request.trace_id})
# In another service
logger.info("Payment processed", extra={"trace_id": trace_id})
```

## 22.5 Deployment Anti-Patterns

### ❌ Big Bang Releases

```bash
# Bad: Deploy everything at once to 100% users
kubectl set image deployment/app app=myapp:v2

# Good: Gradual rollout
# Step 1: 5% traffic
kubectl set image deployment/app-canary app=myapp:v2
# Step 2: Monitor for 30 minutes
# Step 3: Gradually increase to 100%
```

### ❌ No Rollback Plan

```yaml
# Bad: No rollback strategy documented

# Good: Always have rollback ready
rollback:
  automatic: true
  condition: "error_rate > 1% for 5m"
  command: "kubectl rollout undo deployment/app"
```

---

# 23. TOOL RECOMMENDATIONS

## 23.1 Technology Comparison Matrix

### Backend Frameworks

| Framework | Language | Performance | Learning Curve | Ecosystem | Best For |
|-----------|----------|-------------|----------------|-----------|----------|
| **FastAPI** | Python | High | Low | Good | APIs, ML |
| Spring Boot | Java | High | Medium | Excellent | Enterprise |
| Express | Node.js | Medium | Low | Excellent | Startups |
| Gin | Go | Very High | Medium | Good | High perf |
| Rails | Ruby | Medium | Low | Excellent | Rapid dev |

**Recommendation:** FastAPI for Python teams, Spring Boot for enterprise Java teams.

### Databases

| Database | Type | Scalability | Consistency | Best For |
|----------|------|-------------|-------------|----------|
| **PostgreSQL** | SQL | Vertical + Read replicas | Strong | General OLTP |
| MySQL | SQL | Vertical + Sharding | Strong | Web apps |
| MongoDB | Document | Horizontal | Eventual | Flexible schema |
| Cassandra | Wide column | Horizontal | Eventual | Time series |
| Redis | Key-value | Cluster | Strong | Caching |

**Recommendation:** PostgreSQL as primary, Redis for caching.

### Message Queues

| System | Throughput | Latency | Durability | Best For |
|--------|------------|---------|------------|----------|
| **Kafka** | Very High | Medium | Excellent | Event streaming |
| RabbitMQ | High | Low | Good | Task queues |
| SQS | High | Medium | Excellent | AWS native |
| Redis Streams | Very High | Very Low | Good | Real-time |

**Recommendation:** Kafka for event-driven architecture.

### Container Orchestration

| Platform | Complexity | Features | Cost | Best For |
|----------|------------|----------|------|----------|
| **Kubernetes** | High | Full | Medium | Large scale |
| ECS | Medium | Good | Low | AWS native |
| Docker Swarm | Low | Basic | Low | Simple needs |
| Nomad | Medium | Good | Low | Multi-cloud |

**Recommendation:** Kubernetes (EKS/GKE) for production.

### Observability Stack

| Tool | Metrics | Logs | Traces | Cost |
|------|---------|------|--------|------|
| **Datadog** | ✅ | ✅ | ✅ | $$$ |
| New Relic | ✅ | ✅ | ✅ | $$$ |
| Prometheus+Grafana | ✅ | ❌ | ❌ | $ |
| ELK Stack | ❌ | ✅ | ❌ | $$ |
| Jaeger | ❌ | ❌ | ✅ | $ |

**Recommendation:** Datadog (all-in-one) or Prometheus+Loki+Jaeger (self-hosted).

### CI/CD

| Tool | Complexity | Integration | Cost | Best For |
|------|------------|-------------|------|----------|
| **GitHub Actions** | Low | GitHub | $ | GitHub users |
| GitLab CI | Medium | GitLab | $$ | GitLab users |
| Jenkins | High | Any | $ | Customization |
| CircleCI | Low | Any | $$ | Simplicity |
| ArgoCD | Medium | K8s | $ | GitOps |

**Recommendation:** GitHub Actions + ArgoCD for GitOps.

## 23.2 Recommended Stack

### Startup Stack (< $5K/month)

```yaml
backend: FastAPI (Python)
database: PostgreSQL (Supabase)
cache: Redis (Upstash)
queue: Redis Streams
hosting: Fly.io / Railway
monitoring: Grafana Cloud (free tier)
ci_cd: GitHub Actions
```

### Scale-up Stack ($5K - $50K/month)

```yaml
backend: FastAPI / Spring Boot
database: PostgreSQL (RDS)
cache: Redis (ElastiCache)
queue: Kafka (MSK)
hosting: EKS / GKE
monitoring: Datadog
ci_cd: GitHub Actions + ArgoCD
```

### Enterprise Stack (> $50K/month)

```yaml
backend: Spring Boot / Go
database: PostgreSQL (Aurora) + Read replicas
cache: Redis Cluster (ElastiCache)
queue: Kafka (Confluent)
hosting: Multi-region EKS
monitoring: Datadog Enterprise
ci_cd: GitLab CI + ArgoCD + Spinnaker
security: HashiCorp Vault, Snyk
```

---

# 24. APPENDICES

## 24.1 Glossary

| Term   | Definition                                                               |
| ------ | ------------------------------------------------------------------------ |
| ADR    | Architecture Decision Record - Document capturing architecture decisions |
| CAP    | Consistency, Availability, Partition Tolerance theorem                   |
| CDC    | Change Data Capture - Tracking database changes                          |
| CI/CD  | Continuous Integration / Continuous Deployment                           |
| DDD    | Domain-Driven Design                                                     |
| ERD    | Entity-Relationship Diagram                                              |
| gRPC   | Google Remote Procedure Call                                             |
| HLD    | High-Level Design                                                        |
| HPA    | Horizontal Pod Autoscaler                                                |
| IaC    | Infrastructure as Code                                                   |
| JWT    | JSON Web Token                                                           |
| LLD    | Low-Level Design                                                         |
| MLOps  | Machine Learning Operations                                              |
| MTBF   | Mean Time Between Failures                                               |
| MTTR   | Mean Time To Repair                                                      |
| NFR    | Non-Functional Requirement                                               |
| OIDC   | OpenID Connect                                                           |
| RBAC   | Role-Based Access Control                                                |
| RPO    | Recovery Point Objective                                                 |
| RTO    | Recovery Time Objective                                                  |
| SLA    | Service Level Agreement                                                  |
| SLI    | Service Level Indicator                                                  |
| SLO    | Service Level Objective                                                  |
| SRE    | Site Reliability Engineering                                             |
| STRIDE | Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation        |
|        |                                                                          |

## 24.2 References

| Document | Description | Link |
|----------|-------------|------|
| IEEE 1016-2009 | Software Design Descriptions Standard | [IEEE](https://standards.ieee.org) |
| C4 Model | Software Architecture Visualization | [c4model.com](https://c4model.com) |
| AWS Well-Architected | Cloud Architecture Best Practices | [AWS](https://aws.amazon.com/architecture/well-architected) |
| Google SRE Book | Site Reliability Engineering | [sre.google](https://sre.google/books/) |
| OWASP Top 10 | Web Application Security Risks | [OWASP](https://owasp.org/Top10/) |
| 12 Factor App | Cloud-Native Application Principles | [12factor.net](https://12factor.net) |
| Martin Fowler | Microservices Patterns | [martinfowler.com](https://martinfowler.com) |

## 24.3 Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial draft |
| 2.0 | YYYY-MM-DD | [Name] | Added MLOps section |
| 3.0 | YYYY-MM-DD | [Name] | Added Cost Optimization |
| 4.0 | YYYY-MM-DD | [Name] | Production Quality integration |
| 5.0 | YYYY-MM-DD | [Name] | ULTIMATE version - full integration |

## 24.4 Template Changelog

```
Version 5.0 ULTIMATE (Current)
- Integrated 100% of Production Quality Guide (40 chapters)
- Added MLOps section (Model Training, Serving, Monitoring, A/B Testing)
- Added Cost Optimization strategies
- Added Capacity Planning formulas
- Added Incident Response & Runbooks
- Added Implementation Roadmap (4 phases)
- Added Common Mistakes & Anti-Patterns (25+ patterns)
- Added Tool Recommendations & Comparisons
- Enhanced all code examples (Python, SQL, YAML, Terraform)
- Added comprehensive checklists for each phase
```

---

# 🎯 HOW TO USE THIS TEMPLATE

## Quick Start Guide

### Step 1: Copy Template
```bash
cp SOFTWARE_DESIGN_ULTIMATE_TEMPLATE.md PROJECT_NAME_SDD.md
```

### Step 2: Fill Metadata
Complete the YAML metadata section with project info.

### Step 3: Follow Phase Priority

| Phase | Sections to Complete |
|-------|---------------------|
| **Planning** | 1-4 (Summary, Intro, Goals, Overview) |
| **Design** | 5-9 (HLD, LLD, API, Data, Security) |
| **Implementation** | 10-13 (Resilience, Observability, Deploy, Test) |
| **Quality** | 14-17 (NFR, Capacity, Cost, Trade-offs) |
| **Operations** | 18-19 (Runbooks, MLOps) |
| **Pre-Launch** | 20-22 (Roadmap, Checklist, Anti-patterns) |

### Step 4: Review & Iterate
- Get peer review for each section
- Update as design evolves
- Keep document living

## Section Completion Tips

| Section | Time Estimate | Key Focus |
|---------|---------------|-----------|
| Executive Summary | 2 hours | 1-page overview |
| HLD | 1 day | Architecture diagrams |
| LLD | 2-3 days | Detailed design |
| Security | 1 day | STRIDE analysis |
| Testing | 1 day | Strategy & coverage |
| Runbooks | 1 day | Operational procedures |

## ⚠️ Common Mistakes to Avoid

1. ❌ Skipping Non-Goals section → Scope creep
2. ❌ No diagrams → Hard to understand
3. ❌ Missing NFRs → Performance issues
4. ❌ No runbooks → Incident chaos
5. ❌ Outdated document → Wrong decisions

## ✅ Success Criteria

Your SDD is complete when:
- [ ] All stakeholders can understand the system
- [ ] New team members can onboard quickly
- [ ] Operations team can handle incidents
- [ ] Security team approved the design
- [ ] Production readiness checklist passed

---

<div align="center">

**⁂**

_This template combines best practices from:_

**IEEE 1016-2009 | Google SRE | AWS Well-Architected | Netflix | Stripe | Meta**

_Plus 40-Chapter Production Quality Guide integration_

**Version 5.0 ULTIMATE - The Most Comprehensive SDD Template**

_For world-class production systems_

</div>
