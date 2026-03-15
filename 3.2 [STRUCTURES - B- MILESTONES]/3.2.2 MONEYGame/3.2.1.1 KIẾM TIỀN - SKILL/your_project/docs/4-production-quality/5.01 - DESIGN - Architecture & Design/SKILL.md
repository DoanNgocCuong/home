# Software Architecture & Design Best Practices — Production Systems

> **Domain:** 5.01 | **Group:** DESIGN | **Lifecycle:** Design Time
> **Last Updated:** 2026-03-13
>
> *Kiến trúc phần mềm là nền tảng của hệ thống sản xuất bền vững*

---

## 1. Overview

Software architecture determines how systems scale, fail, recover, and evolve. At production scale, architectural decisions made during design time have compounding effects: poor choices multiply complexity, increase operational burden, and create technical debt. This domain covers battle-tested architectural patterns that Netflix, Amazon, Google, and Stripe use to build reliable systems serving millions of users.

Architecture is about managing complexity through clear separation of concerns, defining boundaries, and making intentional trade-offs visible. It's not about perfection—it's about knowing why you made each choice and being able to change it when conditions change.

---

## 2. Core Principles

1. **Separation of Concerns** — Each component should have a single, well-defined responsibility. Changes in one concern should not cascade unexpectedly to others.

2. **Explicitness Over Magic** — Prefer simple, obvious patterns over framework magic. Production systems need to be debuggable at 3 AM.

3. **Fail Gracefully, Not Loudly** — Design for failure modes. Systems will fail; the question is whether they degrade or shatter.

4. **Measure Everything, Assume Nothing** — Architecture decisions should be grounded in monitoring and observability, not hunches about performance.

5. **Optimize for Change** — The only constant is change. Architecture should enable teams to modify systems without massive rewrites.

---

## 3. Best Practices

### 3.1 Clean Architecture (Hexagonal Architecture)

**Practice:** Organize code in concentric circles with domain logic at the center, insulated from external concerns

- **What:** Clean Architecture separates business logic from infrastructure (databases, APIs, frameworks). The domain layer knows nothing about HTTP, SQL, or deployment mechanisms. External adapters implement the interfaces the domain defines.

- **Why:** Teams can test core business logic without standing up databases. Swapping databases (PostgreSQL → DynamoDB) doesn't require rewriting business logic. Different teams can work on domain vs. infrastructure in parallel.

- **How:**
  - Create a `domain/` package for business entities and use cases
  - Create `adapters/` packages for HTTP controllers, database repositories, message queues
  - Define interfaces in the domain layer; implement them in adapters
  - Example: `UserRepository` interface lives in domain; `PostgresUserRepository` implements it in adapters
  - Dependency injection flows inward—adapters inject into domain, never the reverse

- **Anti-pattern:** Letting database schema dictate domain models. Letting HTTP framework logic leak into business logic. Creating a "manager" class that does everything.

### 3.2 Microservices vs. Monolith Decision

**Practice:** Choose based on organizational structure and deployment frequency, not hype

- **What:** Monoliths = single codebase, one deployment unit. Microservices = multiple services, deployed independently.

- **Why:**
  - **Monolith**: Simpler operations, easier debugging, better performance (no network calls), easier transactions. Best for <50 engineers or early-stage startups.
  - **Microservices**: Independent scaling, different tech stacks per service, smaller blast radius for failures. Needed when organizational silos exist or deployment frequency requirements differ.

- **How:** Decide based on:
  - Team structure: Can teams own services end-to-end?
  - Change velocity: Do different services change at different rates?
  - Scaling: Do different parts need independent scaling?
  - Technology: Do different services need different tech stacks?
  - Start with monolith + modular design. Migrate to microservices only when these pressures become real.

- **Anti-pattern:** "Microservices by default." Distributed monolith (chatty services, shared database). Conway's Law ignored (org structure doesn't match service boundaries).

### 3.3 Domain-Driven Design (DDD)

**Practice:** Organize code around business domains with clear linguistic boundaries

- **What:** DDD defines entities, value objects, aggregates, bounded contexts, and ubiquitous language shared between engineers and business stakeholders.

- **Why:** Reduces miscommunication. Code structure reflects business reality. Teams own business capabilities end-to-end, not technical layers.

- **How:**
  - Define bounded contexts (Order, Shipping, Payment are separate contexts)
  - Create ubiquitous language (Order, LineItem, SKU mean specific things)
  - Model aggregates (Order aggregate contains LineItems; Shipping aggregate is separate)
  - Use domain events for communication between contexts
  - Example: Order service publishes `OrderPlaced` event; Shipping service listens and creates shipment

- **Anti-pattern:** Layer-driven architecture (all controllers in one folder, all services in another). Shared domain models between services. Business logic scattered across controllers.

### 3.4 SOLID Principles

**Practice:** Apply SOLID to create maintainable, testable code

- **Single Responsibility** (S): Each class does one thing. `UserService` handles users, not payments.
- **Open/Closed** (O): Open for extension, closed for modification. Use interfaces and inheritance, not if-else sprawl.
- **Liskov Substitution** (L): Subtypes are substitutable. If you have `PaymentProcessor` interface, all implementations should behave the same way.
- **Interface Segregation** (I): Clients shouldn't depend on interfaces they don't use. Don't make `Logger` with 50 methods.
- **Dependency Inversion** (D): Depend on abstractions, not concretions. Inject `UserRepository` interface, not `PostgresUserRepository`.

- **How:** Enforce through code review. Use static analysis tools. Refactor when violations accumulate.

### 3.5 12-Factor App Methodology

**Practice:** Build cloud-native applications with these 12 attributes

1. **Codebase**: One codebase tracked in version control, deployed to multiple environments
2. **Dependencies**: Explicitly declare all dependencies (requirements.txt, package.json, Gemfile)
3. **Config**: Store config in environment variables, not code
4. **Backing Services**: Treat databases/caches as attached resources
5. **Build/Run/Release**: Strict separation between stages
6. **Processes**: Stateless processes; share-nothing architecture
7. **Port Binding**: Export HTTP as a service via port binding
8. **Concurrency**: Explicit process types (web, worker, scheduler)
9. **Disposability**: Fast startup and graceful shutdown
10. **Dev/Prod Parity**: Same backing services in all environments
11. **Logs**: Write logs to stdout; let infrastructure handle aggregation
12. **Admin Tasks**: Run one-off tasks in identical environment as regular processes

- **Why:** Makes applications portable, scalable, and observable. Aligns with containerization (Docker, Kubernetes).

- **Anti-pattern:** Hardcoded config, storing secrets in code, stateful processes, slow startup times, different databases in dev vs. prod.

### 3.6 Event-Driven Architecture

**Practice:** Use events to decouple services and enable eventual consistency

- **What:** Services communicate through events. OrderService publishes `OrderCreated`; InventoryService subscribes and reserves stock.

- **Why:**
  - Loose coupling: Services don't know about each other
  - Scalability: Can process events asynchronously
  - Auditability: Event log is permanent record
  - Supports CQRS and temporal queries

- **How:**
  - Define event schema (use Avro, Protobuf, or JSON Schema)
  - Use message broker (Kafka, RabbitMQ, SNS/SQS)
  - Publish events from domain models
  - Create subscribers for each interested service
  - Handle idempotency (events may be delivered multiple times)
  - Example: `order-service` publishes to `orders` topic; `inventory-service`, `payment-service`, `notification-service` all subscribe

- **Anti-pattern:** Synchronous RPC wrapped as "event-driven." Events with no schema. No dead-letter queue for failed processing.

### 3.7 CQRS (Command Query Responsibility Segregation)

**Practice:** Separate write model (commands) from read model (queries)

- **What:** Commands modify state (CreateOrder, UpdateInventory). Queries read state (GetOrder, ListOrders). Each has its own model and data store.

- **Why:**
  - Read and write loads are usually unequal (10:1 reads to writes)
  - Enables read optimization independently from writes
  - Natural fit for event-sourcing
  - Can use different databases for reads (e.g., denormalized Elasticsearch)

- **How:**
  - Create command handlers that modify the command model
  - Publish events when state changes
  - Update read models (projections) from events
  - Query only reads models
  - Example: Write to PostgreSQL (command model), publish event, update Elasticsearch (read model)

- **Anti-pattern:** CQRS for simple CRUD. Over-engineering consistency.

### 3.8 API Gateway Pattern

**Practice:** Single entry point for external requests; handles routing, auth, rate limiting, protocol translation

- **What:** Clients don't call services directly. They call the gateway, which routes to appropriate services.

- **Why:**
  - Centralized authentication and authorization
  - Consistent rate limiting and request validation
  - Can serve different clients differently (web, mobile, third-party)
  - Can change internal service locations without breaking clients

- **How:**
  - Use Kong, AWS API Gateway, or Envoy
  - Route by path, hostname, or header
  - Apply auth policies
  - Log all requests
  - Example: `GET /api/users/:id` → routes to user-service; `GET /api/orders/:id` → routes to order-service

- **Anti-pattern:** API Gateway doing business logic. Services calling each other directly (bypassing gateway). No rate limiting.

### 3.9 Service Mesh

**Practice:** Use a service mesh (Istio, Linkerd) to manage service-to-service communication transparently

- **What:** Sidecars (Envoy proxies) intercept all traffic between services. Mesh handles routing, retries, circuit breaking, distributed tracing.

- **Why:**
  - Don't embed resilience patterns in every service
  - Consistent logging and observability
  - Can do advanced traffic management (canary deployments, traffic mirroring)
  - Network-level enforcement of security policies

- **How:**
  - Deploy sidecar proxies alongside each service instance
  - Define VirtualServices for routing, DestinationRules for load balancing
  - Example: Istoc can automatically retry failed requests, enforce mTLS between services, trace requests across hops

- **Anti-pattern:** Service mesh without observability tools. Over-complexity for small systems. Service Mesh before microservices are proven necessary.

### 3.10 Design for Failure

**Practice:** Assume every component will fail; design systems to handle it gracefully

- **What:** Implement timeouts, retries, circuit breakers, fallbacks, and bulkheads.

- **Why:** In distributed systems, failure is the normal state. Networks partition. Services crash. Databases become slow. The system must be resilient.

- **How:**
  - **Timeouts**: Never block indefinitely. Set timeouts on all external calls.
  - **Retries**: Automatically retry transient failures (network glitches), but not permanent ones (invalid request).
  - **Circuit Breaker**: Stop calling a failing service; fail fast and let it recover. Pattern: Closed (normal) → Open (failing, reject calls) → Half-Open (test if recovered).
  - **Fallback**: When a service fails, use stale data or default behavior.
  - **Bulkhead**: Isolate failures. If one resource pool is exhausted, others still work.
  - Example: Payment API times out after 5s; retry once; if still fails, use fallback (mark order as pending); don't crash the entire order service.

- **Anti-pattern:** Synchronous calls with no timeout. Unbounded retries. Cascading failures (one service down brings down others). No circuit breaker.

### 3.11 Scalability Patterns

**Practice:** Distinguish between horizontal and vertical scaling; choose based on bottleneck

- **Horizontal Scaling** (scale-out):
  - Add more servers running the same service
  - Services should be stateless
  - Use load balancer to distribute traffic
  - Example: Run 10 instances of order-service behind a load balancer
  - Pros: Can grow infinitely, supports geographic distribution, resilient
  - Cons: More complex operations, network latency, eventual consistency

- **Vertical Scaling** (scale-up):
  - Use larger, more powerful servers
  - Simpler operations, still consistent
  - Cons: Limited by hardware, single point of failure, expensive

- **Database Scaling:**
  - Read replicas for read-heavy workloads
  - Sharding (partitioning by key) for write-heavy workloads
  - Caching layer (Redis) to reduce database load

- **How:** Start vertical. Move to horizontal when cost or availability becomes critical.

- **Anti-pattern:** Stateful services (storing session in memory). Scaling without removing bottlenecks. Over-scaling on the wrong dimension.

### 3.12 Load Balancing Strategies

**Practice:** Distribute traffic intelligently to maximize utilization and minimize latency

- **Round Robin**: Rotate through servers equally. Simple, fair, but ignores server load.
- **Least Connections**: Route to server with fewest active connections. Better for long-lived connections.
- **Weighted Round Robin**: Some servers get more traffic (new servers at lower weight).
- **IP Hash**: Same client always goes to same server. Good for session affinity, but breaks if servers are added/removed.
- **Least Response Time**: Route to server with lowest average response time. Most intelligent but requires active monitoring.

- **How:** Use load balancer (HAProxy, Nginx, ELB). Monitor backend health. Remove failed servers automatically.

### 3.13 Data Consistency Patterns

**Practice:** Choose consistency model based on requirements; most distributed systems use eventual consistency

- **Strong Consistency**: All replicas have the same data. Write to master; read from any replica (after sync). Hard to scale. Used for payment systems.
- **Eventual Consistency**: Replicas converge over time. Write immediately; replicas catch up. Scales well. User might see stale data briefly.
- **Causal Consistency**: Related writes are seen in order by all readers. Middle ground.

- **How:**
  - Payment systems: Strong consistency (use transactions, 2-phase commit)
  - Social media: Eventual consistency (if my like takes a second to propagate, it's fine)
  - Search results: Eventual consistency (index updates are eventual)

- **Trade-off**: Consistency vs. Availability vs. Partition Tolerance (CAP theorem). You can only have 2. Most systems choose Availability + Partition Tolerance, accepting eventual consistency.

### 3.14 Idempotency

**Practice:** Ensure operations can be safely retried without unintended side effects

- **What:** Idempotent operation: f(x) = f(f(x)). Calling it once or multiple times has the same result.

- **Why:** Network failures cause retries. Without idempotency, retries cause duplicate charges, duplicate orders, etc.

- **How:**
  - Generate idempotency keys (client-provided unique ID)
  - Check if operation already processed (via key)
  - Store result of previous operation
  - Return same result on retry
  - Example: Stripe's API requires `Idempotency-Key` header. If you retry with same key, you get the same result.
  - Implement with database unique constraint or cache (Redis)

- **Anti-pattern:** Assuming network never fails. Processing requests without checking for duplicates.

### 3.15 Backpressure

**Practice:** When downstream is slow, signal upstream to slow down

- **What:** If a queue fills up, don't add more items; tell the producer to wait.

- **Why:** Prevents queue overflow, memory exhaustion, and cascading failures. System stays stable under load.

- **How:**
  - Message queues support backpressure (e.g., when Kafka consumer lags, broker can slow producer)
  - HTTP: Return 429 (Too Many Requests) when rate limit exceeded
  - Connection pools: When all connections busy, new requests wait
  - Example: If payment-service is slow, order-service shouldn't queue infinite requests; it should reject new orders or wait.

- **Anti-pattern:** Unbounded queues, ignoring slow consumers, synchronous calls with no timeout.

### 3.16 Bulkhead Pattern

**Practice:** Isolate resources to contain failures and prevent cascading

- **What:** Separate thread pools, connection pools, or processes for different services. If one exhausts its resources, others still work.

- **Why:** Failure isolation. If payment-service overwhelms connection pool, order-service still gets connections.

- **How:**
  - Separate connection pools for each database
  - Separate thread pools for different service calls
  - Use container resource limits (CPU, memory)
  - Example: Order-service has 100 connections to order-db and 50 connections to inventory-db. If inventory-db is slow, order-db still has connections available.

- **Anti-pattern:** Shared connection pool for all services. Unlimited thread creation.

---

## 4. Decision Frameworks

### When to Use Microservices

| Factor | Use Monolith | Use Microservices |
|--------|--------------|-------------------|
| Team Size | < 30 engineers | > 50 engineers |
| Change Velocity | All services change together | Different services change at different rates |
| Scaling | Single bottleneck | Different services need independent scaling |
| Technology | One tech stack works | Different services need different tech stacks |
| Deployment | One deployment per day | Different services deploy independently |
| Org Structure | Functional teams (frontend, backend) | Product/capability teams |

### Architecture Selection Matrix

```
High Consistency, Low Latency → Monolith with read replicas
High Consistency, Distributed → Event Sourcing + CQRS
High Throughput, Distributed → Event-Driven + Eventual Consistency
Complex Domain → DDD + Bounded Contexts
Multiple Clients → API Gateway + BFF
```

### Failure Mode vs. Pattern

| Failure Mode | Pattern |
|--------------|---------|
| Service is slow | Timeout, Circuit Breaker, Bulkhead |
| Service is down | Retry, Fallback, Bulkhead |
| Network partition | Eventual Consistency, Event-Driven |
| Resource exhausted | Backpressure, Rate Limiting |
| Cascading failure | Circuit Breaker, Bulkhead, Service Mesh |

---

## 5. Checklist

- [ ] Architecture diagrams created and shared with team
- [ ] Service/module boundaries clearly defined
- [ ] Interfaces defined; implementations separated
- [ ] Domain models isolated from infrastructure
- [ ] Consistency model decided and documented (strong vs eventual)
- [ ] Failure modes identified and mitigated (timeouts, retries, circuit breakers)
- [ ] Idempotency implemented for critical operations
- [ ] Async operations use events/queues, not polling
- [ ] Rate limiting designed in
- [ ] Monitoring and alerting strategy defined
- [ ] Data migration path planned (zero-downtime if needed)
- [ ] Security boundaries clear (what data is sensitive, who accesses it)
- [ ] API contracts versioning strategy defined
- [ ] Load testing done to identify bottlenecks
- [ ] Disaster recovery plan exists
- [ ] Team can explain architecture to new members

---

## 6. Common Mistakes & Anti-Patterns

### Distributed Monolith
Creating microservices that are tightly coupled (every service calls every other service, shared database). Result: All the operational complexity of distributed systems with none of the benefits.

**Fix:** Enforce service boundaries, use async communication, eliminate shared database.

### God Service / Blob Service
One massive service that does everything (Orders, Payments, Shipping). Hard to change, hard to scale, hard to test.

**Fix:** Use DDD to identify bounded contexts. Split into separate services.

### Shared Database Across Services
Services in same database break independence. Can't change schema without coordination. Scaling one service doesn't scale the database.

**Fix:** Database per service pattern. Use events for cross-service communication.

### Synchronous Everything
Every operation is a synchronous chain of RPC calls. If any service is slow, everything is slow. Cascading failures.

**Fix:** Use async communication (events, queues) for anything that doesn't need synchronous response.

### No Idempotency
Retries cause duplicate charges, duplicate orders. Users get billed twice.

**Fix:** Implement idempotency keys. Check for duplicates before processing.

### Ignoring Failure Modes
Code assumes network is reliable, services never crash, databases never get slow. Inevitable production outages.

**Fix:** Implement timeouts, retries, circuit breakers, fallbacks. Chaos engineering to test failure modes.

### Premature Optimization
Micro-optimizations before profiling. Caching before load testing. Premature sharding.

**Fix:** Measure first. Optimize bottlenecks based on data, not hunches.

---

## 7. Tools & References

### Authoritative Sources
- Martin Fowler: microservices.io, martinfowler.com
- Sam Newman: "Building Microservices" (O'Reilly)
- AWS Well-Architected Framework: Five pillars (operational excellence, security, reliability, performance, cost)
- Google SRE Book: Site Reliability Engineering practices

### Architecture Tools
- **C4 Model**: Context, Container, Component, Code diagrams for architecture
- **ArchiMate**: Standardized language for architecture descriptions
- **TOGAF**: Enterprise architecture framework

### Implementation Libraries
- **Resilience Patterns**: Polly (C#), Hystrix/Resilience4j (Java), Tenacity (Python)
- **Service Mesh**: Istio, Linkerd, Consul
- **Message Brokers**: Kafka (durable, distributed), RabbitMQ (traditional), SNS/SQS (AWS)
- **API Gateways**: Kong, AWS API Gateway, Envoy, Traefik

### Observability (crucial for production architecture)
- Metrics: Prometheus, Grafana
- Logs: ELK Stack, Datadog, Splunk
- Traces: Jaeger, Zipkin, Datadog
- Monitoring: New Relic, Datadog, CloudWatch

---

**Last Updated:** 2026-03-13 | **Version:** 1.0
