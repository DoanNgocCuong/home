# Architecture Decision Records (ADR)

**Project Name:** [Tên dự án]
**Document Version:** 1.0
**Last Updated:** [Ngày]

---

## Giới Thiệu ADR

### ADR là gì?

**Architecture Decision Record (ADR)** là một tài liệu ngắn ghi lại quyết định kiến trúc quan trọng, lý do đằng sau nó, và những trade-offs được xem xét.

### Tại sao dùng ADR?

1. **Documentation**: Ghi lại "tại sao" (not just "what")
2. **Decision Traceability**: Biết ai quyết định cái gì, khi nào
3. **Knowledge Sharing**: Giúp team members mới hiểu context
4. **Prevents Rework**: Tránh re-discussing decisions
5. **Auditing**: Compliance & regulatory requirements

### Cấu trúc ADR

Mỗi ADR bao gồm:
1. **Status**: Proposed, Accepted, Deprecated, Superseded
2. **Context**: Tại sao quyết định này cần thiết?
3. **Decision**: Quyết định gì?
4. **Consequences**: Tác động gì?
5. **Alternatives**: Cái khác ta xem xét?
6. **Rationale**: Tại sao lựa chọn cái này?

---

## ADR-001: Microservices Architecture thay vì Monolith

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]
**Reviewers:** [Names]

### Context

Hệ thống hiện tại (legacy monolith) built bằng Rails single application. Nó:
- Scale đến 5 triệu users nhưng không tới 10 triệu
- Add tính năng mới từ 3 tháng xuống còn 1 tháng (slow)
- Shared database makes scaling difficult
- Team 50 engineers khó coordinate (silos)

Business requirement:
- Cần scale đến 100 triệu users trong 2 năm
- Time-to-market faster (1 tháng per feature)
- Maintain 99.99% uptime

### Decision

Chúng tôi chọn **Microservices Architecture** thay vì monolithic system.

Kiến trúc sẽ bao gồm:
- **Separate services** per business capability:
  - User Service (user management)
  - Auth Service (authentication & authorization)
  - Role Service (RBAC)
  - Notification Service (emails, SMS)
  - Audit Service (compliance logging)
  - etc.

- **Technology Stack**:
  - Service: Node.js + Express
  - Database: PostgreSQL (per service or shared)
  - Cache: Redis
  - Orchestration: Kubernetes
  - API Gateway: Kong or Nginx
  - Message Queue: RabbitMQ (async communication)

- **Deployment Model**: Kubernetes on AWS EKS

### Consequences

**Positive Consequences:**

1. **Scalability** ✓
   - Each service can scale independently
   - If User Service needs 100 instances, Auth Service can have 5
   - Horizontal scaling is straightforward

2. **Autonomy** ✓
   - Teams can develop independently
   - Independent deployment (fast time-to-market)
   - Own database (technology flexibility)
   - Different tech stacks if needed

3. **Fault Isolation** ✓
   - Auth Service down doesn't break User Service
   - Failure contained to specific service
   - Better resilience

4. **Technology Flexibility** ✓
   - Auth Service: Node.js
   - Payment Service: Python + Django (good for financial logic)
   - Search Service: Golang (high performance)
   - Not locked into single tech stack

**Negative Consequences:**

1. **Operational Complexity** ✗
   - Need to monitor 10+ services instead of 1
   - Distributed tracing becomes important
   - Log aggregation complexity
   - Multiple databases to manage

2. **Network Latency** ✗
   - Inter-service communication slower than in-process
   - Example: User Service → Auth Service → Role Service (2 hops)
   - Each hop adds ~10-50ms latency

3. **Data Consistency Challenges** ✗
   - Distributed transactions difficult
   - Need eventual consistency for some operations
   - Saga pattern for multi-step transactions

4. **Debugging Complexity** ✗
   - Debugging single request that spans 5 services is hard
   - Need distributed tracing (e.g., Jaeger)
   - Correlation IDs important

5. **Infrastructure Cost** ✗
   - More services = more infrastructure
   - Kubernetes overhead
   - More monitoring tools needed

6. **Team Overhead** ✗
   - More DevOps burden
   - Teams need to understand deployment, monitoring
   - More ceremony (service contracts, API versioning)

### Alternatives Considered

#### Alternative 1: Monolithic Architecture (Current)
- **Pros**: Simple deployment, easy debugging, consistent data
- **Cons**: Hard to scale independently, slow time-to-market, team silos
- **Why not**: Doesn't meet scalability requirement (100M users)

#### Alternative 2: Modular Monolith
- **Pros**: Scalability benefits of modules, simple deployment
- **Cons**: Still monolithic, doesn't allow independent scaling
- **Why not**: Would still hit scaling limits

#### Alternative 3: Serverless (AWS Lambda)
- **Pros**: Auto-scaling, pay-per-use, no infrastructure management
- **Cons**: Cold starts, latency unpredictable, vendor lock-in
- **Why not**: Cold starts problematic for user-facing APIs (100-500ms)

#### Alternative 4: Event-Driven Architecture
- **Pros**: Decoupled, scalable, eventual consistency
- **Cons**: Complex to understand, debugging harder, consistency issues
- **Why not**: Can combine with microservices (we will use both)

### Rationale

**Tại sao lại chọn Microservices?**

1. **Scalability**: Meet 100M users requirement ✓
2. **Time-to-Market**: Teams develop independently (faster) ✓
3. **Proven Patterns**: Netflix, Amazon, Google đang dùng ✓
4. **Team Autonomy**: 50 engineers need independence ✓
5. **Technology Flexibility**: Can choose best tool per job ✓

**Trade-offs accepted:**

- Accept operational complexity (invest in DevOps, monitoring tools)
- Accept network latency (mitigate with caching, batching)
- Accept consistency challenges (use Saga pattern, event sourcing where needed)
- Accept higher infrastructure cost (justified by business value)

### Related ADRs

- ADR-002: Kubernetes for Orchestration
- ADR-003: PostgreSQL per Service vs Shared Database
- ADR-004: API Gateway for Service Routing

---

## ADR-002: PostgreSQL per Service vs Shared Database

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

In microservices, decision: should each service have own database or share single database?

**Option A: Database per Service**
```
User Service    Auth Service    Role Service
      │               │               │
      ▼               ▼               ▼
   PostgreSQL    PostgreSQL      PostgreSQL
   (users DB)    (auth DB)       (roles DB)
```

**Option B: Shared Database**
```
User Service    Auth Service    Role Service
      │               │               │
      └───────────────┼───────────────┘
                      ▼
                 PostgreSQL
             (single shared DB)
```

### Decision

Chúng tôi chọn **Database per Service** (Option A).

Mỗi service sẽ có PostgreSQL database riêng:
- User Service: users_db
- Auth Service: auth_db
- Role Service: roles_db
- Notification Service: notifications_db

### Consequences

**Positive:**

1. **Service Autonomy** ✓
   - Services can evolve schema independently
   - No coordination needed for DB migrations
   - Freedom to choose schema design

2. **Scalability** ✓
   - Each database can be optimized per workload
   - User Service DB can have 100 read replicas if needed
   - Independent backup/restore per service

3. **Fault Isolation** ✓
   - Auth Service DB down doesn't affect User Service
   - Reduced blast radius

**Negative:**

1. **Data Consistency** ✗
   - Distributed transactions difficult
   - Can't use ACID transactions across services
   - Need eventually consistent operations

2. **Data Retrieval Complexity** ✗
   - Can't do SQL JOIN across services
   - Need to fetch data from multiple services via APIs
   - Slower, more complex queries

3. **Backup/Recovery** ✗
   - Multiple databases to backup & restore
   - Point-in-time recovery complicated
   - More infrastructure

### Alternatives Considered

**Alternative: Shared Database**
- **Pros**: ACID transactions, simple queries, easy joins
- **Cons**: Services tightly coupled, coordination needed, hard to scale
- **Why not**: Violates microservices principle (coupling)

### Rationale

Database-per-service pattern:
- Aligns with microservices goals (autonomy, independent scaling)
- Used by Netflix, Amazon (proven at scale)
- Consistency handled via API transactions, event sourcing

Mitigations for challenges:
- Use Saga pattern untuk distributed transactions
- Accept eventual consistency
- Use event-driven architecture
- Cache shared data in services (reduce cross-service calls)

---

## ADR-003: JWT for Authentication

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

Need to choose stateless authentication mechanism:

**Option A: JWT (JSON Web Token)**
- Tokens are self-contained, server stateless
- Can be verified without database lookup
- Standard, widely adopted

**Option B: Session Cookies**
- Traditional approach
- Session stored server-side (database or in-memory)
- Easier CSRF protection

**Option C: OAuth2/OpenID Connect**
- For delegated authorization
- Suitable for third-party integrations
- More complex

### Decision

Chúng tôi chọn **JWT + OAuth2 combo**:

1. **JWT** cho internal authentication (user logs in → get JWT)
2. **OAuth2** cho social login (Google, Facebook)

```
User Flow:
1. User email/password → Auth Service
2. Auth Service: validate password, generate JWT
3. JWT sent to client, stored in localStorage
4. Client sends JWT in Authorization header on subsequent requests
5. API Gateway validates JWT signature (no DB lookup needed)
```

### Consequences

**Positive:**

1. **Stateless** ✓
   - Server doesn't store session data
   - Scales horizontally (no session affinity needed)
   - Matches microservices philosophy

2. **Performance** ✓
   - No database lookup for every request (just signature validation)
   - Fast token verification

3. **Mobile-Friendly** ✓
   - Works well with mobile apps
   - Supports Authorization header

4. **Standardized** ✓
   - JWT is industry standard
   - Libraries available in all languages

**Negative:**

1. **Token Revocation** ✗
   - Hard to revoke tokens (they're self-contained)
   - Mitigated by short expiration (1 hour) + refresh tokens

2. **Token Size** ✗
   - JWT bigger than session ID
   - Sent with every request (more bandwidth)
   - Mitigated by payload optimization

3. **CSRF Risk** ✗
   - If stored in cookies, vulnerable to CSRF
   - Mitigated by storing in localStorage (not cookies)
   - Trade-off: localStorage vulnerable to XSS

### Rationale

JWT best for microservices because:
- Stateless (scales horizontally)
- No session store needed
- Standard, proven approach
- Works with both web & mobile

Token lifetime strategy:
- Access token: 1 hour (balance security & UX)
- Refresh token: 7 days (stored securely, used to get new access token)
- Logout: invalidate refresh token in database

---

## ADR-004: Kong API Gateway

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

Need API Gateway to:
- Route requests to microservices
- Handle authentication
- Rate limiting
- Request/response transformation
- Logging, monitoring

**Options:**
- A: Kong (dedicated API Gateway)
- B: Nginx (reverse proxy, manual setup)
- C: AWS API Gateway (managed, AWS-only)
- D: No gateway (direct service calls)

### Decision

Chúng tôi chọn **Kong API Gateway**.

```
Internet → Kong → User Service
                → Auth Service
                → Role Service
                → etc.
```

### Consequences

**Positive:**

1. **Feature-Rich** ✓
   - Authentication, rate limiting, logging out-of-box
   - Plugins ecosystem (JWT, OAuth, etc.)
   - Request transformation

2. **Centralized Control** ✓
   - Single entry point
   - Consistent security policies
   - Monitoring from one place

3. **Mature & Proven** ✓
   - Used at scale (Netflix, Uber, etc.)
   - Good documentation
   - Active community

**Negative:**

1. **Additional Infrastructure** ✗
   - Another component to monitor & maintain
   - Need to scale Kong itself (add instances)

2. **Learning Curve** ✗
   - Team needs to learn Kong-specific configuration
   - Plugins have their own documentation

### Alternatives Considered

**Alternative A: Nginx**
- **Pros**: Lightweight, fast, simpler
- **Cons**: Manual setup for auth, rate limiting; less feature-rich
- **Why not**: Requires more custom coding

**Alternative B: AWS API Gateway**
- **Pros**: Managed service, no infrastructure
- **Cons**: Vendor lock-in, costs at scale, limited customization
- **Why not**: Want flexibility, don't want AWS-only

**Alternative D: No gateway**
- **Pros**: Simpler initially
- **Cons**: Duplicate auth logic in every service, harder to enforce policies
- **Why not**: Violates DRY principle

### Rationale

Kong provides:
- Enterprise features (authentication, RBAC, rate limiting)
- Easy to manage (declarative configuration)
- Extensible (plugins)
- Proven at massive scale

---

## ADR-005: Kubernetes for Orchestration

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

With microservices, need container orchestration:
- Deploy, scale, manage containers
- Health checks, auto-restart
- Load balancing, service discovery
- Rolling updates, rollbacks

**Options:**
- A: Kubernetes (K8s)
- B: Docker Swarm
- C: Nomad (HashiCorp)
- D: Managed services (AWS ECS, Fargate)

### Decision

Chúng tôi chọn **Kubernetes (EKS on AWS)**.

### Consequences

**Positive:**

1. **Industry Standard** ✓
   - De facto standard for container orchestration
   - Largest ecosystem, community, job market
   - Future-proof

2. **Powerful** ✓
   - Auto-scaling, self-healing
   - Rolling updates, canary deployments
   - Service discovery, load balancing

3. **Portable** ✓
   - Same K8s config works on AWS, GCP, Azure, on-premises
   - Not vendor-locked

**Negative:**

1. **Steep Learning Curve** ✗
   - Complex, many concepts (Pods, Deployments, Services, etc.)
   - Team needs training

2. **Infrastructure Cost** ✗
   - Need minimum 3 control plane nodes
   - Worker nodes for applications
   - Not cheapest option for small scale

3. **Operational Overhead** ✗
   - Need Kubernetes expertise
   - Debugging distributed system is hard
   - More things to monitor

### Rationale

Kubernetes:
- Standard in industry (Netflix, Google, Amazon use it)
- Required at scale (100M users)
- Active development, future-proof
- Many managed options (EKS, GKE, AKS)

Mitigations:
- Invest in team training
- Use managed K8s (EKS) to reduce ops burden
- Implement observability (logging, monitoring, tracing)

---

## ADR-006: Redis for Caching & Session Store

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

Need fast, in-memory store for:
- Session storage (JWT tokens, user data)
- Caching (reduce database hits)
- Rate limiting counters
- Real-time data (leaderboards, etc.)

**Options:**
- A: Redis
- B: Memcached
- C: Database only (no cache)
- D: In-application cache only

### Decision

Chúng tôi chọn **Redis with cluster mode**.

### Consequences

**Positive:**

1. **Performance** ✓
   - < 1ms latency
   - Handles millions of ops/sec

2. **Rich Data Types** ✓
   - Strings, Hashes, Lists, Sets, Sorted Sets
   - More flexibility than Memcached

3. **Clustering** ✓
   - High availability (replicas)
   - Horizontal scaling (cluster sharding)

**Negative:**

1. **Data Durability** ✗
   - Primarily in-memory (volatile)
   - Mitigated by RDB dumps, AOF (Append-Only File)

2. **Cost** ✗
   - Need separate Redis cluster
   - Additional infrastructure

### Rationale

Redis:
- Industry standard for caching (used by everyone)
- Rich features (not just key-value like Memcached)
- Good for session storage
- Cluster mode enables high availability & scaling

---

## ADR-007: Bcrypt for Password Hashing

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

Need secure password hashing algorithm:

**Options:**
- A: bcrypt
- B: PBKDF2
- C: Argon2
- D: MD5/SHA1 (❌ DON'T use!)

### Decision

Chúng tôi chọn **bcrypt**.

### Consequences

**Positive:**

1. **Secure** ✓
   - Slow intentionally (protects against brute force)
   - Salted (built-in)
   - Adaptive (salt rounds can increase)

2. **Simple** ✓
   - Easy to use
   - Available in all languages
   - No configuration needed

3. **Industry Standard** ✓
   - Used by major companies
   - Proven security

**Rationale:**

Bcrypt:
- One of best options for password hashing
- Intentionally slow (10 salt rounds = ~100ms per hash)
- Makes brute force attacks impractical
- No known vulnerabilities

Alternatives (Argon2 is newer & even better, but bcrypt more widely used).

---

## ADR-008: ELK Stack for Logging

**Status:** Accepted
**Date:** 2026-03-15
**Authors:** [Names]

### Context

With microservices, need centralized logging:
- Services generate logs
- Need to search, analyze, alert on logs

**Options:**
- A: ELK Stack (Elasticsearch + Logstash + Kibana)
- B: Splunk
- C: Datadog
- D: CloudWatch only

### Decision

Chúng तो chọn **ELK Stack** (self-hosted initially).

### Consequences

**Positive:**

1. **Cost-Effective** ✓
   - Open source
   - Less expensive than commercial options

2. **Flexible** ✓
   - Can customize Logstash pipelines
   - Full control over data

**Negative:**

1. **Operational Overhead** ✗
   - Need to manage, scale Elasticsearch
   - Requires DevOps expertise

2. **Complexity** ✗
   - Multiple components (Elasticsearch, Logstash, Kibana, Beats)
   - More things to monitor

### Rationale

ELK Stack:
- De facto standard for logging in microservices
- Powerful search capabilities
- Cost-effective at scale
- Can grow with business

---

## ADR Governance

### Statuses

| Status | Meaning | Example |
|--------|---------|---------|
| **Proposed** | Under discussion, not yet decided | ADR-009 (draft) |
| **Accepted** | Team agreed, implementing | ADR-001 |
| **Deprecated** | Replaced by newer decision | ADR-003 (if we change auth) |
| **Superseded** | Replaced by ADR-XYZ | Reference new ADR |

### Process

1. **Author writes ADR** (using template below)
2. **Team reviews** in architecture review meeting
3. **Decision made** (accepted or rejected)
4. **Update status** to Accepted/Deprecated
5. **Implement** according to decision

### When to Write ADR

Write ADR for:
- Major architecture decisions (impact > 1 service)
- Technology choices (framework, database, etc.)
- Significant pattern changes
- Decisions that constrain future choices

Don't write ADR for:
- Minor implementation details
- Local optimization within one service
- Configuration changes

---

## ADR Template

```markdown
# ADR-NNN: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** YYYY-MM-DD
**Authors:** [Names]
**Reviewers:** [Names]

## Context

[Why is this decision needed?]
[What problem are we solving?]
[What are the constraints?]

## Decision

[What did we decide?]
[Be specific, describe the chosen option clearly]

## Consequences

### Positive
[List benefits, advantages]

### Negative
[List drawbacks, challenges]
[List mitigations for drawbacks]

## Alternatives Considered

[Describe 2-3 alternatives briefly]
[Why we rejected each one]

## Rationale

[Why this decision is best given context]
[What trade-offs are we accepting]
[How this aligns with architecture goals]

## Related ADRs

- ADR-001: [if relevant]
- ADR-002: [if relevant]

## Implementation Notes

[How to implement this decision]
[Any gotchas or important details]

```

---

## Summary: Key Architectural Decisions

| ADR | Decision | Status |
|-----|----------|--------|
| ADR-001 | Microservices Architecture | Accepted |
| ADR-002 | Database per Service | Accepted |
| ADR-003 | JWT + OAuth2 | Accepted |
| ADR-004 | Kong API Gateway | Accepted |
| ADR-005 | Kubernetes (EKS) | Accepted |
| ADR-006 | Redis Caching | Accepted |
| ADR-007 | Bcrypt Password Hashing | Accepted |
| ADR-008 | ELK Stack Logging | Accepted |

---

## ADR Review Schedule

- **Monthly**: Review new ADR proposals
- **Quarterly**: Review active ADRs for relevance
- **As-needed**: Create new ADRs for significant decisions

---

**Last Updated:** 2026-03-15
**Next Review:** 2026-06-15
**Owner:** Architecture Team

---
