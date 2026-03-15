# 02-ADR - Architecture Decision Records

## 1. ADR là gì?

**ADR (Architecture Decision Record)** là tài liệu ghi lại một quyết định kiến trúc quan trọng, lý do tại sao ta chọn nó, và hậu quả của nó.

### Tại sao cần ADR?

Hãy tưởng tượng bạn:
- Vào một team mới, nhìn code, thắc mắc "Tại sao chúng ta dùng Kafka thay vì RabbitMQ?"
- Sáu tháng sau, developer mới hỏi cùng câu hỏi
- Hai năm sau, cả team quên lý do tại sao lựa chọn này được đưa ra

**ADR giải quyết vấn đề này bằng cách:**
- Ghi lại WHAT (cái gì)
- Ghi lại WHY (tại sao)
- Ghi lại WHEN (khi nào quyết định này được đưa ra)
- Ghi lại CONSEQUENCES (hậu quả)

### Lợi ích của ADR

✓ **Tài liệu lịch sử** - Biết được lý do quyết định trong quá khứ
✓ **Onboarding** - Developer mới hiểu tại sao architecture như vậy
✓ **Tránh vòng tròn** - Không bàn lại quyết định đã xong
✓ **Traceability** - Có thể track thay đổi architecture theo thời gian
✓ **Học hỏi** - Nếu quyết định không tốt, biết để tránh lần sau

---

## 2. ADR Template (Mẫu tiêu chuẩn)

Dưới đây là template phổ biến nhất cho ADR:

```markdown
# ADR [number]: [Title]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded]

## Context

Mô tả bối cảnh, vấn đề cần giải quyết, ràng buộc.
- Vấn đề là gì?
- Tại sao vấn đề này quan trọng?
- Đâu là constraints (thời gian, budget, team)?

## Decision

Quyết định chúng ta đưa ra.
- Cái gì ta chọn?
- Cách implement?

## Rationale

Tại sao ta chọn quyết định này?
- Pro/cons so với lựa chọn khác
- Tại sao pro vượt trội hơn cons
- Assumptions

## Consequences

Hậu quả (cả tích cực và tiêu cực) của quyết định này:
- Tích cực: X, Y, Z
- Tiêu cực: A, B, C
- Trade-offs

## Alternatives Considered

Những lựa chọn khác ta xem xét nhưng không chọn:
- Alternative 1: pros/cons
- Alternative 2: pros/cons
- Tại sao không chọn nó?

## References

Tài liệu tham khảo:
- Link 1
- Link 2
```

---

## 3. Example ADR #1: Chọn Database cho User Service

```markdown
# ADR 001: Use PostgreSQL as Primary Database for User Service

**Date:** 2024-01-15
**Status:** Accepted
**Author:** Backend Team Lead

## Context

User Service cần một database để lưu user information, credentials, profiles.

**Requirements:**
- ACID transactions (tính integrity là critical cho user data)
- Complex queries (user search, filtering, aggregation)
- Phải handle ~1000 concurrent connections
- Future: có thể scale tới 100K users

**Constraints:**
- Budget: moderate infrastructure cost
- Timeline: 2 weeks to setup
- Team expertise: Node.js team, familiar với SQL databases

## Decision

**Chúng ta sẽ sử dụng PostgreSQL (version 13+) cho User Service.**

- Primary datastore cho user profiles, authentication data, audit logs
- Running on managed service (AWS RDS hoặc GCP Cloud SQL)
- Automatic backups, failover, patching được provider quản lý

## Rationale

### Lợi ích của PostgreSQL

✓ **ACID Compliance**
- User data phải chính xác 100%
- ACID transactions đảm bảo consistency
- Transactions quan trọng: password updates, 2FA setup

✓ **Complex Queries**
- User search: filter by email, name, location
- Aggregations: count active users by region
- Joins: user with profile, preferences
- SQL ưu việt cho các queries phức tạp này

✓ **Scalability**
- PostgreSQL handle 1000s concurrent connections dễ dàng
- Read replicas để scale reads
- Connection pooling (pgBouncer) support

✓ **Ecosystem**
- Mature, stable, widely-used
- Great libraries trong Node.js (pg, Sequelize, TypeORM)
- Excellent documentation
- Large community

✓ **Cost**
- Open source (free)
- Managed service giá hợp lý
- Không cần expensive licenses

### So sánh với alternatives

| Criteria | PostgreSQL | MongoDB | Firebase |
|----------|-----------|---------|----------|
| ACID | ✓ Excellent | ✗ Limited | ✗ No |
| Complex queries | ✓ Excellent | ⚠ Medium | ✗ Limited |
| Scalability | ✓ Good | ✓ Excellent | ✓ Excellent |
| Cost | ✓ Low | ✓ Low | ✗ High at scale |
| Team expertise | ✓ Familiar | ✗ Learning curve | ✓ Simple |
| Flexibility | ✓ High | ✓ High | ✗ Limited |

**Tại sao không MongoDB?**
- MongoDB không ACID transactions (before v4.0)
- Complex aggregation queries khó hơn SQL
- Vì team familiar với SQL, setup dễ hơn

**Tại sao không Firebase?**
- Cost tăng exponentially khi scale
- Limited query flexibility
- Vendor lock-in cao

## Consequences

### Tích cực

✓ ACID transactions đảm bảo data integrity
✓ Team can leverage SQL expertise
✓ Read replicas cho scaling reads
✓ Can backup/restore easily
✓ Standard relational model easy to understand

### Tiêu cực

✗ Need to manage schema migrations
✗ Vertical scaling limits (single server bottleneck)
✗ Must implement connection pooling
✗ Cold start latency for serverless apps

### Trade-offs

- **Consistency vs Scalability:** PostgreSQL prioritizes consistency, MongoDB prioritizes availability/scalability
- **Flexibility vs Structure:** Schema required (good for validation, bad for rapid iteration)
- **Cost at Scale:** As scale increases, might need to shard (complexity increases)

## Alternatives Considered

### 1. MongoDB (Document Database)
**Pros:**
- Flexible schema, easy iterations
- Horizontal scaling simple
- Good for semi-structured data

**Cons:**
- No ACID transactions (critical for user service)
- Complex aggregations harder
- Higher cost at our scale

**Decision:** Rejected because ACID is critical for user data

### 2. Firebase (BaaS)
**Pros:**
- Zero infrastructure management
- Built-in authentication
- Real-time capabilities

**Cons:**
- Very expensive at scale
- Limited query capabilities
- High vendor lock-in
- Limited customization

**Decision:** Rejected because cost concerns and lack of flexibility

### 3. DynamoDB (NoSQL)
**Pros:**
- Serverless, auto-scaling
- Very fast for simple lookups

**Cons:**
- No complex queries
- Expensive for large scans
- Limited transaction support
- Requires denormalization

**Decision:** Rejected because we need complex queries

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [AWS RDS PostgreSQL Pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- [PostgreSQL vs MongoDB comparison](https://www.mongodb.com/compare/postgresql-vs-mongodb)
- [ACID Properties - Wikipedia](https://en.wikipedia.org/wiki/ACID)

## Follow-up ADRs

- ADR 002: Database replication strategy
- ADR 003: Backup and disaster recovery plan
```

---

## 4. Example ADR #2: Chọn Message Queue

```markdown
# ADR 002: Use Apache Kafka for Inter-Service Communication

**Date:** 2024-02-01
**Status:** Accepted
**Author:** Platform Team

## Context

Hệ thống đang có 3 services: User, Order, Payment.
Hiện tại dùng HTTP REST calls:
```
User Service → Order Service: "Create order for user ID 123"
Order Service → Payment Service: "Process payment"
```

Nhưng có vấn đề:
- **Timing issues:** Nếu Payment Service offline, Order không thành công
- **High coupling:** Order Service phải biết Payment Service URL
- **No audit trail:** Không có record của transactions
- **No retry logic:** Nếu call fail, data lost

## Decision

**Chúng ta sẽ chuyển sang Apache Kafka cho inter-service communication.**

- Order Service publish `OrderCreated` event lên Kafka topic
- Payment Service subscribe, consume event, process payment
- Mỗi event được lưu lại trong Kafka (audit trail)
- Natural retry mechanism

## Rationale

### Event-Driven Benefits

✓ **Decoupling**
- Order Service không biết Payment Service tồn tại
- Có thể add Notification Service sau mà không thay đổi Order Service

✓ **Reliability**
- Payment Service down? Event vẫn queue trong Kafka
- Khi Payment Service online, process events lại

✓ **Audit Trail**
- Tất cả events lưu trong Kafka
- Có thể replay events để debug issues
- Compliance friendly

✓ **Scalability**
- Order Service produce nhanh
- Payment Service consume at own pace
- Không cần synchronous waiting

✓ **Ordering Guarantee**
- Kafka guarantee message order per partition
- Events xảy ra theo đúng order

### Kafka vs Alternatives

| Aspect | Kafka | RabbitMQ | AWS SQS |
|--------|-------|----------|---------|
| Throughput | ✓ Very High | ⚠ Medium | ✓ High |
| Persistence | ✓ Long-term | ⚠ Short | ⚠ Very short |
| Message Ordering | ✓ Per Partition | ✗ Limited | ✗ No |
| Replay | ✓ Yes | ✗ No | ✗ No |
| Scaling | ✓ Excellent | ⚠ Decent | ✓ Excellent |
| Operational Cost | ⚠ High | ✓ Low | ⚠ Medium |
| Learning Curve | ✗ Steep | ✓ Easy | ✓ Easy |

**Tại sao không RabbitMQ?**
- RabbitMQ không lưu messages lâu dài (default delete sau consume)
- Không thể replay history
- Messages không persist để long-term audit

**Tại sao không AWS SQS?**
- SQS không lưu messages sau consume
- Không thể replay
- Vendor lock-in với AWS

## Consequences

### Tích cực

✓ Loosely coupled services
✓ Complete audit trail of all events
✓ Can replay events for debugging/recovery
✓ Services can fail independently
✓ Easy to add new consumers
✓ High throughput (millions of events/day)

### Tiêu cực

✗ Operational complexity increases
✗ Need to manage Kafka cluster
✗ Learning curve steep for team
✗ Eventual consistency (dữ liệu không nhất quán ngay)
✗ Higher infrastructure cost
✗ Need to implement idempotency (in case of duplicate events)

### Trade-offs

- **Complexity vs Decoupling:** Kafka adds complexity but huge decoupling benefits
- **Eventual Consistency vs Strong Consistency:** Payments eventually consistent, not immediately
- **Cost vs Reliability:** Higher cost but much better reliability

## Alternatives Considered

### 1. Continue with HTTP REST Calls
**Pros:**
- Simple, understood by all developers
- No additional infrastructure
- Synchronous (know result immediately)

**Cons:**
- Services tightly coupled
- No audit trail
- Cascading failures
- No retry mechanism

**Decision:** Rejected because brittleness and lack of audit trail

### 2. RabbitMQ (Message Queue)
**Pros:**
- Lighter weight than Kafka
- Easier to setup
- Good for simple use cases

**Cons:**
- No message persistence (deleted after consume)
- Cannot replay messages
- Limited for future needs

**Decision:** Rejected because audit trail is regulatory requirement

### 3. AWS EventBridge
**Pros:**
- Fully managed (no ops overhead)
- Integrates well with AWS services
- Serverless

**Cons:**
- Vendor lock-in
- Limited replay capabilities
- Expensive for high volume
- Limited ordering guarantees

**Decision:** Rejected because multi-cloud strategy and cost concerns

## Implementation Plan

1. **Week 1:** Setup Kafka cluster (3 brokers, 3 ZK nodes)
2. **Week 2:** Migrate Order Service to publish OrderCreated events
3. **Week 3:** Migrate Payment Service to consume events
4. **Week 4:** Testing, monitoring setup
5. **Week 5:** Gradual rollout, dual-write period

## References

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Kafka vs RabbitMQ comparison](https://aws.amazon.com/kinesis/firehose/faqs/)
- [Idempotency Pattern](https://en.wikipedia.org/wiki/Idempotence)

## Follow-up ADRs

- ADR 003: Event schema versioning strategy
- ADR 004: Dead letter queue handling
- ADR 005: Kafka cluster operations and monitoring
```

---

## 5. Example ADR #3: Monolith vs Microservices

```markdown
# ADR 003: Transition from Monolith to Microservices Architecture

**Date:** 2024-03-01
**Status:** Proposed
**Author:** Architecture Committee

## Context

Current System (Monolith):
- Single codebase (Python Django)
- Single database (PostgreSQL)
- ~50,000 lines of code
- 15 developers working on same codebase

**Problems we're experiencing:**

1. **Deployment Risk**
   - Any change = deploy entire app
   - Risk of breaking unrelated features
   - Last month: 2 production incidents from bad deploys

2. **Scaling Issues**
   - User Service (auth) is CPU-heavy
   - Payment Service needs separate DB (compliance)
   - Can't scale individual components
   - Having to buy bigger servers every quarter

3. **Developer Productivity**
   - 15 devs on same codebase = many merge conflicts
   - Can't work in parallel effectively
   - Code reviews take long (many changing files)
   - Feature takes 3 weeks when should be 1 week

4. **Technology Constraints**
   - Stuck with Django ecosystem
   - Can't use better tools for specific jobs
   - Want to use Go for high-performance services
   - Want to use Node.js for APIs

## Decision

**We will transition from Monolith to Microservices architecture.**

Target state:
```
User Service (Node.js)     → PostgreSQL
Order Service (Python)     → MongoDB
Payment Service (Go)       → PostgreSQL
Notification Service (Go)  → Redis
Inventory Service (Node)   → PostgreSQL
```

## Rationale

### Benefits of Microservices

✓ **Independent Scaling**
- Payment service handle higher load independently
- User service scale based on auth requests
- No need to over-provision entire system

✓ **Independent Deployment**
- Notification service deploy ≠ affect Order service
- Faster deployment cycle
- Reduced risk per deploy

✓ **Team Velocity**
- Each team own 1-2 services
- Fewer merge conflicts
- Parallel development
- 3 services x 5 devs each > 1 app x 15 devs

✓ **Technology Flexibility**
- Use best tool for each job
- Go for performance-critical services
- Python for ML/analytics tasks
- Node.js for REST APIs

✓ **Scaling Development**
- As team grows, can add more teams/services
- Clear ownership
- Service contract-based integration

### Current Monolith Issues Solved

✗ Deployment Risk → ✓ Deploy single service
✗ Scaling Issues → ✓ Scale individual services
✗ Developer Productivity → ✓ Fewer conflicts, parallel work
✗ Technology Constraints → ✓ Pick best tool per service

### Microservices Challenges We Accept

⚠ Operational complexity → Invest in DevOps/infra team
⚠ Network latency → Optimize with caching, batching
⚠ Data consistency → Implement Saga pattern for distributed transactions
⚠ Testing complexity → Invest in comprehensive integration tests
⚠ Monitoring overhead → Setup central logging (ELK), tracing (Jaeger)

## Consequences

### Positive Consequences

✓ Can scale User Service 10x without scaling everything
✓ Payment Service deploys don't affect Order Service
✓ Payment team use Go (better for their domain)
✓ Each team own their service → clear accountability
✓ Feature delivery faster (1 week instead of 3)
✓ New team members onboard faster (smaller codebase)

### Negative Consequences

✗ Infrastructure complexity increases significantly
✗ Need DevOps/SRE team (5-10 people)
✗ Network latency increases (each call now network call)
✗ Distributed debugging harder
✗ Cost increases (more infrastructure, more ops)
✗ Testing more complex (mock 10 services)

### Trade-offs

- **Simplicity vs Flexibility:** Lose monolithic simplicity, gain flexibility to scale/evolve
- **Cost vs Capability:** Higher cost but can scale to millions of users
- **Development Speed vs Operational Complexity:** Slower deploy/monitoring, but faster feature development

## Implementation Strategy

**Phase 1 (Months 1-2): Foundation**
- Setup container orchestration (Kubernetes)
- Setup service mesh (Istio)
- Setup central logging (ELK)
- Setup distributed tracing (Jaeger)

**Phase 2 (Months 3-4): Extract Services**
- Extract User Service → Node.js, PostgreSQL
- Extract Payment Service → Go, PostgreSQL
- Implement inter-service communication (gRPC)

**Phase 3 (Months 5-6): Complete Migration**
- Extract remaining services
- Decommission monolith
- Training + documentation

**Phase 4 (Months 7+): Optimization**
- Fine-tune service boundaries
- Performance optimization
- Cost optimization

## Alternatives Considered

### 1. Keep Monolith, but Split Teams
**Pros:**
- No infrastructure complexity
- No operational overhead
- Same codebase, same language

**Cons:**
- Still have merge conflicts
- Still can't scale individually
- Still have deployment risk
- Team productivity same as now

**Decision:** Rejected because doesn't solve core problems

### 2. Strangler Fig Pattern (Slow Migration)
**Pros:**
- Lower risk
- Can learn along the way
- Less infrastructure investment upfront

**Cons:**
- Takes 2-3 years
- Have to maintain both monolith and services
- Benefits delayed
- Lose focus/momentum

**Decision:** Not rejected but slower than full migration

### 3. Modular Monolith (Internal separation)
**Pros:**
- Still single deployment
- Better code organization
- Can eventually extract services

**Cons:**
- Doesn't solve scaling issues
- Doesn't solve deployment risk
- Doesn't solve team scaling
- Still single language

**Decision:** Rejected because doesn't address our core problems

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Operational complexity | Hire DevOps engineers, invest in automation |
| Data consistency issues | Use Saga pattern, implement compensating transactions |
| Network latency | Implement caching, service mesh optimization |
| Team not ready | Training program, hire experienced architects |
| Cost overrun | Start with 2-3 critical services, expand gradually |

## Success Criteria

- [ ] Feature delivery time: 3 weeks → 1 week
- [ ] Deployment frequency: 1x/week → daily
- [ ] Deployment failure rate: 5% → <1%
- [ ] System availability: 99.5% → 99.9%
- [ ] Horizontal scaling: Manual → Automatic

## References

- [Microservices Architecture](https://microservices.io/)
- [Building Microservices - Sam Newman](https://samnewman.ie/building_microservices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)

## Follow-up ADRs

- ADR 004: Service boundary definition
- ADR 005: Inter-service communication protocol (gRPC vs REST)
- ADR 006: Data consistency strategy
- ADR 007: Service discovery and load balancing
- ADR 008: Monitoring and observability architecture
```

---

## 6. ADR Best Practices

### Do's ✓

✓ **Be concise but complete**
- 1-2 pages ideal
- Enough detail to understand decision
- Not a 50-page thesis

✓ **Document early**
- ADR right after decision made
- While reasoning still fresh
- Don't wait months

✓ **Use clear language**
- Avoid jargon if possible
- Explain acronyms
- Make it understandable to junior devs

✓ **Include alternatives**
- Show you considered options
- Why other options rejected
- Shows decision was thoughtful

✓ **Document consequences**
- Be honest about trade-offs
- Acknowledge negative consequences
- Don't hide problems

✓ **Version control ADRs**
- Keep in git repository
- Part of codebase
- Searchable, versionable

✓ **Update status over time**
- Accepted → Deprecated (if no longer valid)
- Accepted → Superseded (if replaced by newer ADR)
- This shows evolution of thinking

### Don'ts ✗

✗ **Don't bury ADR**
- Make sure team knows ADRs exist
- Reference in onboarding docs
- Link from architecture docs

✗ **Don't write ADR for every decision**
- Minor config changes: no ADR needed
- Major architectural: definitely ADR
- Use judgment: if affects multiple services → ADR

✗ **Don't treat ADR as final**
- If decision is wrong, update it
- Document why decision changed
- Learn from mistakes

✗ **Don't skip alternatives section**
- Shows you did research
- Helps future people understand trade-offs
- Prevents repeating same debates

✗ **Don't use ADR as blame**
- "These idiots chose technology X"
- Focus on reasoning at the time
- Decisions made with info available then

---

## 7. Tóm tắt

| Aspect | Details |
|--------|---------|
| **ADR là gì** | Document recording architecture decisions |
| **Tại sao cần** | Preserve why decisions made, onboard developers |
| **Sections** | Context, Decision, Rationale, Consequences, Alternatives |
| **Best cho** | Major technical decisions affecting multiple teams |
| **Tần suất** | 1-2 new ADRs per quarter (varies) |
| **Maintenance** | Update status as architecture evolves |
| **Storage** | Version control (git), part of codebase |

---

## 8. Tạo ADR cho dự án của bạn

**Bước 1:** Nhận diện decision cần ghi
**Bước 2:** Viết ADR sử dụng template ở trên
**Bước 3:** Gửi cho review, discuss với team
**Bước 4:** Approve, update status thành "Accepted"
**Bước 5:** Commit vào git

Ví dụ command:
```bash
# Tạo folder
mkdir -p docs/adr

# Tạo file
touch docs/adr/0001-choose-database.md

# Commit
git add docs/adr/0001-choose-database.md
git commit -m "ADR 0001: Choose PostgreSQL as primary database"
```

**Start documenting your architectural decisions today!**
