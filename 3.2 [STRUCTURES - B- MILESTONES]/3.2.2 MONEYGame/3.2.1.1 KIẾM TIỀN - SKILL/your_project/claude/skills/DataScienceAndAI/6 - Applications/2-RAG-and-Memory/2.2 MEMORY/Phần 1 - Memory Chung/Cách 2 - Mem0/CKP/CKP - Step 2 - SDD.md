> (Claude hết, nên dùng Manus viết chán vãi)
# SOFTWARE DESIGN DOCUMENT (SDD)
## PIKA Memory System - Mem0 Self-Hosted Implementation

**Document_ID:** SDD-PIKA-MEM0-SELFHOST-v1.0  
**Status:** Approved  
**Priority:** P0-Critical  
**Version:** 1.0.0  
**Last Updated:** 2025-12-20  
**Target Release:** Q1 2026

---

## 📋 DOCUMENT METADATA

| Thông Tin | Chi Tiết |
|-----------|---------|
| **Tác Giả** | Manus AI |
| **Reviewer** | Tech Lead, Product Manager |
| **Phê Duyệt** | Engineering Director |
| **Ngày Tạo** | 2025-12-20 |
| **Deadline Review** | 2025-12-27 |
| **Tài Liệu Liên Quan** | PRD, API Spec, Test Plan, Runbook |

---

## 1. EXECUTIVE SUMMARY (TL;DR)

### 1.1 Bảng Tóm Tắt

| Khía Cạnh | Chi Tiết |
|-----------|---------|
| **Vấn Đề** | Mem0 Enterprise ($600/tháng) quá đắt; cần self-hosted solution |
| **Giải Pháp** | Triển khai Mem0 Open Source với 2 APIs: `search_facts` & `extract_facts` |
| **Tác Động Kinh Tế** | Giảm 75% chi phí ($150/tháng vs $600/tháng) |
| **Tác Động Kỹ Thuật** | P95 latency <100ms, uptime 99.9%, hỗ trợ 1M+ users |
| **Công Nghệ Chính** | Python FastAPI, Mem0 SDK, Qdrant, Neo4j, PostgreSQL, Redis |
| **Nỗ Lực Ước Tính** | 3 engineers × 8 weeks = 96 man-days |
| **Mức Độ Rủi Ro** | Medium (dependency trên Mem0 OSS stability) |
| **Timeline** | MVP: 4 tuần, Production: 8 tuần |
| **Chi Phí Năm 1** | $100K infrastructure + $150K development |

### 1.2 Kiến Trúc Tổng Quan

```
┌──────────────────────────────────────────────────────────────┐
│              PIKA Memory System (Mem0 Self-Hosted)            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ FastAPI Wrapper Layer                               │   │
│  │  ├─ POST /search_facts (Sync, <100ms P95)          │   │
│  │  ├─ POST /extract_facts (Async, 202 Accepted)      │   │
│  │  └─ GET /jobs/{job_id}/status (Polling)            │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │ Mem0 Python SDK (AsyncMemory)                       │   │
│  │  ├─ Fact Extraction (gpt-4o-mini)                   │   │
│  │  ├─ Vector Search (Qdrant)                          │   │
│  │  ├─ Graph Memory (Neo4j)                            │   │
│  │  └─ Metadata Filtering                              │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│    ┌────────────┼────────────┬──────────────┐               │
│    │            │            │              │                │
│    ▼            ▼            ▼              ▼                │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Qdrant │ │ Neo4j  │ │PostgreSQL│ │  Redis   │            │
│  │(Vector)│ │(Graph) │ │(History) │ │ (Cache)  │            │
│  └────────┘ └────────┘ └──────────┘ └──────────┘            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. INTRODUCTION

PIKA Robot là một AI companion cho trẻ em, cần hệ thống memory để nhớ thông tin về người dùng qua các cuộc hội thoại. Hiện tại sử dụng Mem0 Enterprise ($600/tháng), nhưng chi phí quá cao khi scale. Tài liệu này mô tả việc triển khai **Mem0 Open Source** self-hosted để giảm chi phí 75% trong khi vẫn đảm bảo chất lượng production.

---

## 3. GOALS, SCOPE & CONSTRAINTS

### 3.1 Mục Tiêu (Goals)

| Mục Tiêu | Chỉ Số Thành Công |
|----------|------------------|
| **Giảm chi phí** | Từ $600 → $150/tháng |
| **Đảm bảo latency** | P95 search <100ms, P99 <200ms |
| **Uptime** | 99.9% availability |
| **Scalability** | Hỗ trợ 1M+ users, 100M+ memories |
| **Data Privacy** | 100% on-premise, GDPR compliant |

### 3.2 Phạm Vi (Scope)

**Bao Gồm:**
- Triển khai 2 APIs: `search_facts` và `extract_facts`
- Setup Mem0 OSS với Qdrant, Neo4j, PostgreSQL, Redis
- Async job processing cho extract_facts
- Monitoring, logging, alerting
- Load testing và performance tuning

**Không Bao Gồm:**
- Migration từ Mem0 Enterprise (separate project)
- Custom LLM fine-tuning
- Advanced graph analytics

### 3.3 Ràng Buộc (Constraints)

| Ràng Buộc | Mô Tả |
|-----------|-------|
| **Timeline** | Phải launch trong Q1 2026 |
| **Budget** | $250K maximum |
| **Team** | 3 engineers (1 backend, 1 devops, 1 qa) |
| **Infra** | AWS/GCP only, no on-prem |
| **Compliance** | GDPR, CCPA, data residency Vietnam |

---

## 4. SYSTEM OVERVIEW

### 4.1 Thành Phần Chính

**API Gateway (FastAPI)**
- Endpoint: `https://pika-mem0.stepup.edu.vn`
- Authentication: API Key + JWT
- Rate Limiting: 1000 req/min per user
- Timeout: 30s for search, 60s for extract

**Mem0 SDK Layer**
- Python AsyncMemory client
- Custom fact extraction prompts
- Graph relationship extraction
- Semantic caching

**Data Layer**
- **Qdrant:** Vector store (1536-dim embeddings)
- **Neo4j:** Graph DB (entities & relationships)
- **PostgreSQL:** Metadata, audit logs, job status
- **Redis:** Caching, session management

**Background Processing**
- RabbitMQ: Async job queue
- Worker processes: Fact extraction, embedding generation
- Job status tracking in PostgreSQL

### 4.2 Data Flow

**Search Facts Flow:**
```
User Query → FastAPI → Mem0 search() → Qdrant (vector search)
→ Neo4j (relationship enrichment) → Redis cache → Response
Latency: 50-150ms
```

**Extract Facts Flow:**
```
Conversation → FastAPI (202 Accepted) → RabbitMQ queue
→ Worker (LLM extraction + embedding) → Qdrant + Neo4j + PostgreSQL
→ Job status = "completed" → User polls for results
Latency: 1-2s async processing
```

---

## 5. HIGH-LEVEL DESIGN (HLD)

### 5.1 Architecture Diagram

```yaml
Clients (Mobile/Web)
    ↓
API Gateway (FastAPI, 3 replicas)
    ├─ /search_facts (POST)
    ├─ /extract_facts (POST)
    └─ /jobs/{job_id}/status (GET)
    ↓
Mem0 Python SDK (AsyncMemory)
    ├─ LLM: OpenAI gpt-4o-mini
    ├─ Embedder: text-embedding-3-small
    ├─ Vector Store: Qdrant
    ├─ Graph Store: Neo4j
    └─ Metadata: PostgreSQL
    ↓
Data Stores
├─ Qdrant (Vector DB): 1.5M vectors, 10GB
├─ Neo4j (Graph DB): 100M nodes, 500M edges
├─ PostgreSQL: 50GB (metadata, audit logs)
└─ Redis: 10GB (cache, sessions)
```

### 5.2 Deployment Architecture

```yaml
Kubernetes Cluster (3 nodes)
├─ API Service (3 replicas, HPA)
├─ Worker Service (2 replicas)
├─ Qdrant StatefulSet (1 replica)
├─ Neo4j StatefulSet (1 replica)
├─ PostgreSQL StatefulSet (1 replica)
├─ Redis StatefulSet (1 replica)
└─ RabbitMQ StatefulSet (1 replica)

Load Balancer: AWS ALB
Monitoring: Datadog + Prometheus
Logging: ELK Stack
```

---

## 6. LOW-LEVEL DESIGN (LLD)

### 6.1 API Endpoints

#### Endpoint 1: Search Facts

```
POST /search_facts
Content-Type: application/json

Request:
{
  "user_id": "019afe35-1317-7b94-a833-ff5e2504a9c3",
  "query": "Thú cưng",
  "limit": 20,
  "score_threshold": 0.4
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "mem_001",
        "memory": "Mình nuôi mèo tên Miu",
        "score": 0.96,
        "created_at": "2025-12-10T10:00:00Z",
        "relations": [
          {"type": "owns", "target": "Miu (cat)"}
        ]
      }
    ],
    "total": 15,
    "latency_ms": 85
  }
}
```

#### Endpoint 2: Extract Facts

```
POST /extract_facts
Content-Type: application/json

Request:
{
  "user_id": "user_test_1",
  "conversation_id": "conv_001",
  "conversation": [
    {
      "role": "assistant",
      "content": "Chào cậu, tớ là Pika đây!"
    },
    {
      "role": "user",
      "content": "Chào Pika, tớ tên Tuấn"
    }
  ]
}

Response (202 Accepted):
{
  "status": "accepted",
  "job_id": "job_550e8400",
  "status_url": "/jobs/job_550e8400/status",
  "estimated_time_seconds": 30
}

GET /jobs/job_550e8400/status
Response (200 OK):
{
  "job_id": "job_550e8400",
  "status": "completed",
  "progress": 100,
  "data": {
    "facts_extracted": 2,
    "results": [
      {
        "id": "mem_001",
        "memory": "Tên là Tuấn",
        "category": "personal_info",
        "confidence": 0.99
      }
    ]
  }
}
```

### 6.2 Database Schema

**PostgreSQL:**
```sql
-- Jobs table (async processing)
CREATE TABLE jobs (
  id VARCHAR(256) PRIMARY KEY,
  user_id VARCHAR(256),
  conversation_id VARCHAR(256),
  status VARCHAR(50), -- pending, processing, completed, failed
  progress INT,
  result JSONB,
  error_message TEXT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_user_id (user_id)
);

-- Audit logs
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id VARCHAR(256),
  action VARCHAR(256),
  resource_type VARCHAR(128),
  details JSONB,
  created_at TIMESTAMP,
  INDEX idx_user_id (user_id)
);
```

**Qdrant Collections:**
```yaml
collection_name: pika_memories
vector_size: 1536
distance: Cosine
indexed_fields:
  - user_id
  - category
  - created_at
```

**Neo4j Nodes & Relationships:**
```cypher
CREATE CONSTRAINT user_id_unique ON (u:User) ASSERT u.id IS UNIQUE;
CREATE CONSTRAINT fact_id_unique ON (f:Fact) ASSERT f.id IS UNIQUE;

MATCH (u:User)-[:HAS_FACT]->(f:Fact)-[:MENTIONS]->(e:Entity)
```

---

## 7. API DESIGN & CONTRACTS

### 7.1 Request/Response Contracts

| API | Method | Auth | Rate Limit | Timeout |
|-----|--------|------|-----------|---------|
| search_facts | POST | API Key | 100/min | 30s |
| extract_facts | POST | API Key | 50/min | 60s |
| job status | GET | API Key | 1000/min | 5s |

### 7.2 Error Handling

```json
{
  "status": "error",
  "error_code": "INVALID_USER_ID",
  "message": "User ID not found",
  "request_id": "req_123456",
  "timestamp": "2025-12-20T10:00:00Z"
}
```

---

## 8. DATA DESIGN

### 8.1 Data Models

**Memory Entity:**
```python
class Memory(BaseModel):
    id: str
    user_id: str
    content: str
    category: str  # personal_info, hobby, family, school, health
    confidence: float  # 0.0-1.0
    embedding: List[float]  # 1536 dimensions
    created_at: datetime
    updated_at: datetime
```

**Job Status:**
```python
class JobStatus(BaseModel):
    job_id: str
    status: str  # pending, processing, completed, failed
    progress: int  # 0-100
    data: Optional[dict]
    error: Optional[str]
```

### 8.2 Data Retention Policy

| Data Type | Retention | Backup |
|-----------|-----------|--------|
| Memories | Indefinite | Daily |
| Audit Logs | 1 year | Weekly |
| Job History | 30 days | On-demand |
| Cache | 24 hours | None |

---

## 9. SECURITY DESIGN

### 9.1 Authentication & Authorization

- **API Key:** 32-char random string per user
- **JWT Tokens:** 1-hour expiry for session management
- **RBAC:** Admin, User, Viewer roles
- **Encryption:** TLS 1.3 for transit, AES-256 for sensitive data at rest

### 9.2 Data Protection

- **PII Handling:** Tokenization for sensitive fields
- **Access Logging:** All data access logged to audit_logs
- **Rate Limiting:** 1000 req/min per user to prevent abuse
- **Input Validation:** All inputs sanitized, max 10KB per request

---

## 10. RESILIENCE & RELIABILITY

### 10.1 High Availability

- **API:** 3 replicas with auto-scaling (HPA)
- **Database:** Master-slave replication for PostgreSQL
- **Cache:** Redis cluster with 3 nodes
- **Failover:** Automatic failover in <30s

### 10.2 Disaster Recovery

| Scenario | RTO | RPO | Strategy |
|----------|-----|-----|----------|
| Single API pod down | <5s | 0s | Auto-restart |
| Database down | <1min | <1min | Failover to replica |
| Region down | <5min | <5min | Cross-region backup |

---

## 11. OBSERVABILITY & MONITORING

### 11.1 Key Metrics

```yaml
Metrics:
  - api_request_latency (p50, p95, p99)
  - api_error_rate
  - search_facts_latency
  - extract_facts_job_duration
  - vector_search_latency
  - neo4j_query_latency
  - cache_hit_rate
  - job_success_rate
```

### 11.2 Alerting Rules

| Alert | Threshold | Severity |
|-------|-----------|----------|
| High Error Rate | >1% for 5min | Critical |
| High Latency | P95 >200ms for 10min | Warning |
| Low Cache Hit | <30% for 30min | Warning |
| Service Down | 0 healthy pods | Critical |

---

## 12. DEPLOYMENT & OPERATIONS

### 12.1 Deployment Strategy

**Phased Rollout:**
1. **Week 1-2:** Development & testing (staging)
2. **Week 3:** Canary deployment (5% traffic)
3. **Week 4:** Gradual rollout (25% → 50% → 100%)
4. **Week 5-6:** Optimization & monitoring

### 12.2 Infrastructure Requirements

| Component | Spec | Cost/Month |
|-----------|------|-----------|
| API Servers (3×) | t3.large (2 CPU, 8GB RAM) | $90 |
| Qdrant (1×) | c5.2xlarge (8 CPU, 16GB RAM) | $150 |
| Neo4j (1×) | c5.2xlarge (8 CPU, 16GB RAM) | $150 |
| PostgreSQL (1×) | db.r5.2xlarge (8 CPU, 64GB RAM) | $400 |
| Redis (1×) | cache.r6g.xlarge (4 CPU, 32GB) | $100 |
| Load Balancer & Networking | - | $50 |
| **Total** | - | **$940/month** |

---

## 13. TESTING STRATEGY

### 13.1 Test Coverage

| Test Type | Coverage | Tools |
|-----------|----------|-------|
| Unit Tests | >80% | pytest |
| Integration Tests | >60% | pytest + testcontainers |
| Load Tests | N/A | Locust (500 concurrent users) |
| Security Tests | OWASP Top 10 | Bandit, Safety |

### 13.2 Performance Targets

| Metric | Target | Acceptance |
|--------|--------|-----------|
| search_facts P95 | <100ms | ✅ |
| search_facts P99 | <200ms | ✅ |
| extract_facts async | <2s processing | ✅ |
| API uptime | 99.9% | ✅ |
| Cache hit rate | >40% | ✅ |

---

## 14. NON-FUNCTIONAL REQUIREMENTS (NFR)

| NFR | Requirement | Verification |
|-----|-------------|--------------|
| **Performance** | P95 latency <100ms | Load testing |
| **Scalability** | 1M+ users | Capacity planning |
| **Availability** | 99.9% uptime | Monitoring |
| **Security** | GDPR/CCPA compliant | Audit |
| **Maintainability** | Code coverage >80% | CI/CD |
| **Usability** | API response time <1s | User testing |

---

## 15. PERFORMANCE & CAPACITY PLANNING

### 15.1 Capacity Model

| Metric | Current | Year 1 | Year 2 |
|--------|---------|--------|--------|
| Users | 100K | 500K | 1M |
| Memories/User | 100 | 500 | 1000 |
| Total Memories | 10M | 250M | 1B |
| Storage (Qdrant) | 15GB | 375GB | 1.5TB |
| Storage (Neo4j) | 5GB | 125GB | 500GB |
| QPS (search) | 100 | 500 | 1000 |
| QPS (extract) | 10 | 50 | 100 |

### 15.2 Scaling Strategy

- **Horizontal:** Add API replicas (HPA: min 3, max 10)
- **Vertical:** Upgrade database instance size
- **Caching:** Increase Redis cache for hot data
- **Sharding:** Partition data by user_id if needed

---

## 16. COST OPTIMIZATION

### 16.1 Cost Breakdown

| Item | Monthly | Annual | Savings vs Enterprise |
|------|---------|--------|----------------------|
| Infrastructure | $940 | $11,280 | 98% |
| Development (amortized) | $50 | $600 | N/A |
| **Total** | **$990** | **$11,880** | **75% vs $600/mo** |

### 16.2 Cost Reduction Strategies

- Use spot instances for non-critical workloads (-30%)
- Reserved instances for 1-year commitment (-25%)
- Data compression & archival (-15%)
- CDN for static assets (-10%)

---

## 17. TRADE-OFFS & ARCHITECTURE DECISIONS

| Decision | Trade-off | Justification |
|----------|-----------|---------------|
| Async extract_facts | Latency vs throughput | Better UX, supports 1000+ concurrent |
| Qdrant over Milvus | Simplicity vs performance | Easier to manage, sufficient for scale |
| PostgreSQL over MongoDB | Consistency vs flexibility | ACID guarantees for audit logs |
| Redis caching | Memory cost vs latency | 40% hit rate saves 60% DB queries |

---

## 18. INCIDENT RESPONSE & RUNBOOKS

### 18.1 Critical Incidents

**Incident: Search API Latency >500ms**
- **Detection:** Datadog alert (P95 latency)
- **Response:** Check Qdrant CPU/memory, scale if needed
- **Escalation:** Page on-call engineer if not resolved in 5min

**Incident: Extract Jobs Stuck**
- **Detection:** Job status = "processing" for >5min
- **Response:** Check RabbitMQ queue, restart worker if needed
- **Escalation:** Check OpenAI API quota/rate limits

---

## 19. IMPLEMENTATION ROADMAP

### Phase 1: MVP (Weeks 1-4)
- [ ] Setup Mem0 OSS locally
- [ ] Implement FastAPI wrapper
- [ ] Deploy to staging
- [ ] Basic testing

### Phase 2: Production Hardening (Weeks 5-6)
- [ ] Add monitoring & alerting
- [ ] Load testing (500 concurrent)
- [ ] Security audit
- [ ] Documentation

### Phase 3: Launch (Weeks 7-8)
- [ ] Canary deployment (5%)
- [ ] Gradual rollout (100%)
- [ ] Monitoring & optimization
- [ ] Handoff to ops team

---

## 20. PRODUCTION READINESS CHECKLIST

- [ ] Code reviewed (2+ reviewers)
- [ ] Unit tests >80% coverage
- [ ] Integration tests passing
- [ ] Load test completed (500 concurrent)
- [ ] Security scan (no critical issues)
- [ ] Datadog dashboards created
- [ ] Alert rules configured
- [ ] Runbooks documented
- [ ] Deployment guide written
- [ ] Rollback plan tested

---

## 21. COMMON MISTAKES & ANTI-PATTERNS

❌ **Mistake 1:** Synchronous extract_facts → High latency  
✅ **Solution:** Use async 202 Accepted pattern

❌ **Mistake 2:** No caching → 10x more database queries  
✅ **Solution:** Multi-layer caching (L1 in-memory, L2 Redis)

❌ **Mistake 3:** Single database replica → Data loss risk  
✅ **Solution:** Master-slave replication + daily backups

---

## 22. TOOL RECOMMENDATIONS

| Tool | Purpose | Cost |
|------|---------|------|
| Datadog | Monitoring | $30/month |
| PagerDuty | Incident management | $20/month |
| GitHub | Version control | Free |
| Docker | Containerization | Free |
| Kubernetes | Orchestration | Free |

---

## 23. APPENDICES

### A. API Examples

**Search Facts:**
```bash
curl -X POST https://pika-mem0.stepup.edu.vn/search_facts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "019afe35-1317-7b94-a833-ff5e2504a9c3",
    "query": "Thú cưng",
    "limit": 20,
    "score_threshold": 0.4
  }'
```

**Extract Facts:**
```bash
curl -X POST https://pika-mem0.stepup.edu.vn/extract_facts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_test_1",
    "conversation_id": "1",
    "conversation": [...]
  }'
```

### B. Glossary

- **Mem0:** AI memory layer for personalized interactions
- **Qdrant:** Vector database for semantic search
- **Neo4j:** Graph database for entity relationships
- **Async:** Non-blocking operation with polling
- **P95/P99:** 95th/99th percentile latency

---

## 24. SIGN-OFF

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Tech Lead | [Name] | ________ | 2025-12-20 |
| Product Manager | [Name] | ________ | 2025-12-20 |
| Security Lead | [Name] | ________ | 2025-12-20 |
| DevOps Lead | [Name] | ________ | 2025-12-20 |

---

**END OF DOCUMENT**

*Tài liệu này được tạo theo IEEE 1016-2009 Standard và Google Design Docs best practices.*
