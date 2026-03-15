# High-Level Design (HLD) Template

**Project Name:** [Tên dự án]
**Version:** 1.0
**Date:** [Ngày viết]
**Author(s):** [Tên tác giả]

---

## 1. System Overview

### 1.1 Purpose & Scope

Giải thích tại sao hệ thống này được xây dựng và phạm vi của nó.

**Ví dụ:**
> Hệ thống quản lý người dùng được xây dựng để replace legacy monolithic system. Nó cung cấp scalable, microservices-based solution cho authentication, user management, và RBAC.
>
> **In Scope:**
> - User CRUD operations
> - Authentication (login, logout, OAuth2)
> - Role-Based Access Control
> - Audit logging
>
> **Out of Scope:**
> - Frontend UI (separate design document)
> - Email service configuration
> - Billing/payment processing

### 1.2 Key Features

Liệt kê tính năng chính ở high level.

- User authentication (email/password, Google OAuth)
- User profile management
- Role & permission management
- Real-time notifications
- Audit logging & compliance
- Multi-tenancy support

### 1.3 Success Criteria

Tiêu chí đo lường thành công.

- System handles 100K concurrent users
- Response time < 200ms for 95% requests
- 99.99% uptime SLA
- Support 50+ languages

---

## 2. Architecture Overview

### 2.1 Architecture Diagram

Vẽ toàn bộ architecture.

```
                    ┌──────────────────────┐
                    │   Client Apps        │
                    │ (Web, Mobile, etc)   │
                    └──────────┬───────────┘
                               │ HTTPS
                    ┌──────────▼───────────┐
                    │   API Gateway        │
                    │  (Auth, Rate limit)  │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
    ┌───▼────┐         ┌───────▼──────┐      ┌───────▼──────┐
    │ User   │         │ Auth Service │      │ Role Service │
    │Service │         │              │      │              │
    │ CRUD   │         │ JWT, OAuth2  │      │ RBAC, Perms  │
    └───┬────┘         └───────┬──────┘      └───────┬──────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                 ┌─────────────▼────────────┐
                 │   PostgreSQL Database    │
                 │  (Multi-AZ replicas)     │
                 └──────────────────────────┘
                               │
                 ┌─────────────▼────────────┐
                 │   Redis Cache Layer      │
                 │   (Session, Users)       │
                 └──────────────────────────┘

External Systems:
    ├─ Google OAuth API
    ├─ SendGrid (Email)
    ├─ Twilio (SMS)
    └─ AWS S3 (Avatar storage)
```

### 2.2 Architecture Pattern

Loại architecture yang digunakan.

**Pattern: Microservices Architecture**

Characteristics:
- Services dipisah berdasarkan business capability
- Each service punya database/datastore sendiri (optional)
- Services communicate via HTTP REST atau message queues
- API Gateway sebagai single entry point
- Independent deployment, scaling, dan technology stack

Benefits:
- Scalability: masing-masing service scale independently
- Fault isolation: service down tidak affect lainnya
- Technology flexibility: masing-masing service pakai tech stack berbeda
- Team autonomy: teams develop/deploy independent

Trade-offs:
- Operational complexity: monitoring, logging, tracing lebih complicated
- Network latency: inter-service communication lebih slow
- Data consistency: distributed transactions lebih challenging

---

## 3. Core Components

### 3.1 Component Breakdown

List semua main components dan responsibilities.

```
┌────────────────────────────────────────────┐
│ API Gateway                                │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • Route requests ke services               │
│ • Authentication check (JWT validation)    │
│ • Rate limiting (10K req/sec/user)         │
│ • CORS handling                            │
│ • Request/response transformation          │
│ Technology: Kong / Nginx                   │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ User Service                               │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • User CRUD operations                     │
│ • User data validation                     │
│ • User search & filtering                  │
│ • Avatar upload handling                   │
│ • Publish user-related events              │
│ Technology: Node.js + Express + PostgreSQL│
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Auth Service                               │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • User login (email/password)              │
│ • User logout                              │
│ • JWT token generation & refresh           │
│ • OAuth2 integration (Google, Facebook)    │
│ • Password reset handling                  │
│ • Session management                       │
│ Technology: Node.js + Express + JWT        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Role Service                               │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • Role CRUD operations                     │
│ • Permission management                    │
│ • Assign roles to users                    │
│ • Check user permissions                   │
│ • Cache roles & permissions                │
│ Technology: Node.js + Express + Redis      │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Database Layer (PostgreSQL)                │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • Persistent data storage                  │
│ • Data consistency & integrity             │
│ • Query optimization                       │
│ • Backup & recovery                        │
│ Configuration:                             │
│ • Multi-AZ for high availability            │
│ • Read replicas for read-heavy workloads    │
│ • Daily automated backups                  │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Cache Layer (Redis)                        │
├────────────────────────────────────────────┤
│ Responsibilities:                          │
│ • Session caching (user tokens)            │
│ • User data caching (reduce DB queries)    │
│ • Role & permission caching                │
│ • Rate limiting counters                   │
│ Configuration:                             │
│ • Multi-AZ cluster                         │
│ • TTL: 1 hour for user data                │
│ • TTL: 7 days for refresh tokens           │
└────────────────────────────────────────────┘
```

### 3.2 Component Interactions

Bagaimana components berinteraksi dengan satu sama lain?

```
Sequence: User Login Flow

Client                 API Gateway           Auth Service          User Service         Database
│                      │                     │                      │                    │
│─POST /auth/login────▶│                     │                      │                    │
│                      │─validate JWT────────│ (untuk rate limit)    │                    │
│                      │◀─OK────────────────│                      │                    │
│                      │                     │                      │                    │
│                      │─POST /login────────▶│                      │                    │
│                      │  {email, password}  │                      │                    │
│                      │                     │                      │                    │
│                      │                     │─GET /users/byEmail──▶│                    │
│                      │                     │  {email}             │                    │
│                      │                     │                      │──query users───────▶│
│                      │                     │                      │  WHERE email = ...  │
│                      │                     │                      │◀─user record───────│
│                      │                     │◀─user object────────│                    │
│                      │                     │                      │                    │
│                      │                     │ (bcrypt verify pass) │                    │
│                      │                     │ ✓ Password OK        │                    │
│                      │                     │                      │                    │
│                      │                     │─Generate JWT────────▶│                    │
│                      │                     │  (sign token)        │                    │
│                      │                     │◀─JWT token─────────│                    │
│                      │                     │                      │                    │
│                      │◀─200 OK JWT────────│                      │                    │
│◀─200 OK JWT────────│                     │                      │                    │
│  {token}            │                     │                      │                    │
```

### 3.3 Data Flow

Bagaimana data mengalir melalui sistem?

```
1. Request Entry Point
   └─ User sends request to API Gateway (http://api.example.com/v1/users)

2. API Gateway Processing
   ├─ Extract JWT from Authorization header
   ├─ Validate JWT signature in Redis cache
   ├─ Check rate limits
   ├─ Route request to appropriate service
   └─ Add context (user ID, IP, trace ID)

3. Service Processing
   ├─ User Service:
   │  ├─ Deserialize request payload
   │  ├─ Validate input (email format, required fields)
   │  ├─ Check user permissions via Role Service
   │  ├─ Query database or cache
   │  └─ Serialize response
   │
   ├─ Auth Service:
   │  ├─ Verify credentials (hash password, compare)
   │  ├─ Generate JWT (sign with secret)
   │  ├─ Cache token in Redis
   │  └─ Return JWT to client
   │
   └─ Role Service:
      ├─ Check role & permission in cache
      ├─ Query database if not in cache
      ├─ Update cache (TTL: 1 hour)
      └─ Return permission result

4. Response
   ├─ Service returns JSON response
   ├─ API Gateway adds security headers
   ├─ Log request/response
   └─ Send to client

5. Client Side
   └─ Store JWT in localStorage for next requests
```

---

## 4. Data Storage Design

### 4.1 Data Models

Entities utama dalam sistem.

```
User
├─ id (UUID)
├─ email (string, unique)
├─ password_hash (string)
├─ first_name (string)
├─ last_name (string)
├─ is_active (boolean)
├─ created_at (timestamp)
└─ updated_at (timestamp)

Role
├─ id (UUID)
├─ name (string, unique)
├─ description (text)
└─ created_at (timestamp)

Permission
├─ id (UUID)
├─ name (string, unique)
├─ resource (string)
├─ action (string)
└─ description (text)

UserRole (junction table)
├─ id (UUID)
├─ user_id (FK)
└─ role_id (FK)

RolePermission (junction table)
├─ id (UUID)
├─ role_id (FK)
└─ permission_id (FK)
```

### 4.2 Database Design

```
┌──────────────────┐          ┌──────────────────┐
│     users        │          │     roles        │
├──────────────────┤          ├──────────────────┤
│ id (PK)          │◄─────┐   │ id (PK)          │
│ email (UNIQUE)   │      │   │ name (UNIQUE)    │
│ password_hash    │      │   │ description      │
│ first_name       │      │   │ created_at       │
│ last_name        │      │   └──────────────────┘
│ is_active        │      │
│ created_at       │      │   ┌──────────────────┐
│ updated_at       │      └───┤ user_roles       │
└──────────────────┘          ├──────────────────┤
                               │ id (PK)          │
                               │ user_id (FK)     │
                               │ role_id (FK)     │
                               └──────────────────┘
                                      │
                               ┌──────▼──────────┐
                               │   permissions   │
                               ├─────────────────┤
                               │ id (PK)         │
                               │ name (UNIQUE)   │
                               │ resource        │
                               │ action          │
                               ├─────────────────┤
                               │ role_perm (FK)  │
                               └─────────────────┘
```

### 4.3 Storage Strategy

Bagaimana data disimpan & diakses?

- **Hot Data** (frequently accessed): Redis cache → PostgreSQL
- **Warm Data** (occasionally accessed): PostgreSQL only
- **Cold Data** (rarely accessed): PostgreSQL with archival → S3
- **Real-time Data** (session, tokens): Redis only

---

## 5. Integration Points

### 5.1 External System Integration

System yang terintegrasi dengan aplikasi.

```
┌─────────────────────────────────────────────┐
│ Our System (User Management)                │
└────────────┬────────────────────────────────┘
             │
   ┌─────────┼─────────┬──────────┬───────────┐
   │         │         │          │           │
   ▼         ▼         ▼          ▼           ▼
Google     SendGrid   Twilio    AWS S3   Slack
OAuth2     (Email)    (SMS)     (Avatar) (Notify)

Integration Details:
└─ Google OAuth2: OAuth2 flow for social login
└─ SendGrid: Send welcome email, password reset email
└─ Twilio: Send SMS notifications
└─ AWS S3: Store user avatars
└─ Slack: Notify on security events
```

### 5.2 API Contracts

Contracts dengan external systems.

```
Google OAuth2:
  POST https://oauth2.googleapis.com/token
  {
    "client_id": "...",
    "client_secret": "...",
    "code": "...",
    "redirect_uri": "https://api.example.com/auth/callback"
  }
  Response:
  {
    "access_token": "...",
    "id_token": "...",
    "expires_in": 3600
  }

SendGrid:
  POST https://api.sendgrid.com/v3/mail/send
  {
    "personalizations": [...],
    "from": {"email": "noreply@example.com"},
    "subject": "Welcome to our platform",
    "content": [{"type": "text/html", "value": "..."}]
  }
  Response: 202 Accepted

AWS S3:
  PUT https://bucket.s3.amazonaws.com/avatars/user-123.jpg
  Content: image binary
  Response: 200 OK
```

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

Target performance metrics.

| Metric | Target | Rationale |
|--------|--------|-----------|
| Login response time | < 200ms (p95) | User experience |
| User CRUD response time | < 100ms (p95) | User experience |
| Search users response time | < 500ms (p95) | Acceptable for search |
| Cache hit rate | > 80% | Reduce DB load |
| API throughput | 10,000 req/sec | Peak load |

### 6.2 Scalability Requirements

Bagaimana system scale?

- **Horizontal Scaling**: Add more service instances
- **Auto-scaling**: Scale up when CPU > 70%, down when CPU < 30%
- **Database Scaling**: Read replicas untuk read-heavy queries
- **Caching**: Multi-level caching strategy
- **Load Balancing**: Distribute traffic evenly

### 6.3 Availability & Reliability

SLA dan reliability targets.

- **Availability**: 99.99% uptime (4.38 minutes downtime per month)
- **RTO** (Recovery Time Objective): < 30 minutes
- **RPO** (Recovery Point Objective): < 1 minute
- **Backup**: Daily automated backups, tested quarterly
- **Failover**: Automatic failover untuk database & cache

### 6.4 Security Requirements

Security considerations.

- **Authentication**: JWT tokens + OAuth2
- **Authorization**: RBAC dengan permission checking
- **Encryption**: HTTPS for data in transit, AES-256 for data at rest
- **Password**: bcrypt hashing + salt
- **Token**: JWT expires in 1 hour, refresh token expires in 7 days
- **Rate Limiting**: 10K requests per user per hour
- **Audit Logging**: All sensitive operations logged

---

## 7. Deployment Architecture

### 7.1 Deployment Model

Dimana dan bagaimana system di-deploy?

**Infrastructure: AWS**

```
┌────────────────────────────────────────────┐
│ AWS Region (us-east-1)                     │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ EKS Cluster (Kubernetes)             │ │
│  │ ├─ 3 Availability Zones              │ │
│  │ ├─ Auto-scaling groups               │ │
│  │ ├─ Services in pods                  │ │
│  │ └─ ConfigMaps + Secrets              │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ RDS PostgreSQL                       │ │
│  │ ├─ Multi-AZ deployment               │ │
│  │ ├─ Automated backups                 │ │
│  │ └─ Read replicas                     │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ ElastiCache Redis                    │ │
│  │ ├─ Multi-AZ cluster                  │ │
│  │ ├─ Automatic failover                │ │
│  │ └─ Cluster mode enabled              │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ S3 Bucket                            │ │
│  │ ├─ For avatar storage                │ │
│  │ ├─ Versioning enabled                │ │
│  │ └─ Server-side encryption            │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ CloudFront CDN                       │ │
│  │ ├─ Cache static assets               │ │
│  │ └─ Serve from edge locations         │ │
│  └──────────────────────────────────────┘ │
│                                            │
└────────────────────────────────────────────┘
         │
         │ via Route 53 (DNS)
         │
    ┌────▼────────────┐
    │ api.example.com │
    └─────────────────┘
```

### 7.2 Environment Separation

Dev, staging, production.

```
Development Environment:
├─ Laptop / local VM
├─ Single node Kubernetes
├─ SQLite database
└─ No backups required

Staging Environment:
├─ AWS (small instance)
├─ Similar to production (but smaller)
├─ RDS PostgreSQL (backup daily)
├─ ElastiCache Redis
└─ Used for final testing before production

Production Environment:
├─ AWS (large instances, multi-AZ)
├─ EKS Kubernetes cluster
├─ RDS PostgreSQL (multi-AZ, backup hourly)
├─ ElastiCache Redis (cluster mode)
├─ CloudFront CDN
└─ All monitoring & alerting enabled
```

---

## 8. Sequence Diagrams

### 8.1 Main Use Cases

Sequence diagram untuk main flows.

**Use Case 1: User Registration**

```
User           Browser        API Gateway      User Service      Database
│              │              │                │                 │
│─submit form─▶│              │                │                 │
│              │─POST /users─▶│                │                 │
│              │ {email,pwd}  │                │                 │
│              │              │─validate JWT──▶│                 │
│              │              │ (optional)     │                 │
│              │              │                │                 │
│              │              │─POST /users──▶│                 │
│              │              │                │─validate input──│
│              │              │                │─check uniqueness│
│              │              │                │──query users───▶│
│              │              │                │◀─no duplicates──│
│              │              │                │                 │
│              │              │                │─hash password───│
│              │              │                │                 │
│              │              │                │─INSERT user────▶│
│              │              │                │◀─user created──│
│              │              │                │                 │
│              │              │◀─201 Created──│                 │
│              │◀─201 Created│                │                 │
│◀─show msg───│              │                │                 │
│ (success)   │              │                │                 │
```

**Use Case 2: User Login**

```
User           Browser        API Gateway      Auth Service      Database
│              │              │                │                 │
│─submit login▶│              │                │                 │
│              │─POST /login─▶│                │                 │
│              │ {email,pwd}  │                │                 │
│              │              │─rate limit────│ (check counter)  │
│              │              │                │                 │
│              │              │─POST /login──▶│                 │
│              │              │                │                 │
│              │              │                │─query users────▶│
│              │              │                │◀─user data──────│
│              │              │                │                 │
│              │              │                │-bcrypt compare──│
│              │              │                │ ✓ password OK   │
│              │              │                │                 │
│              │              │                │-generate JWT───│
│              │              │                │ (sign token)    │
│              │              │                │                 │
│              │              │◀─200 OK JWT──│                 │
│◀─200 OK JWT─│◀─200 OK JWT─│                │                 │
│              │              │                │                 │
│              │ store JWT in localStorage     │                 │
```

---

## 9. Risk Assessment

### 9.1 Identified Risks

Risks dan mitigation strategies.

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Database failure | High | Medium | Multi-AZ, automated backups, failover |
| Service outage | High | Low | Health checks, auto-restart, load balancer |
| Security breach | Critical | Low | Encryption, RBAC, audit logs, penetration testing |
| Performance degradation | Medium | Medium | Caching, monitoring, load testing |
| Data loss | Critical | Very Low | Daily backups, backup testing, recovery drills |

### 9.2 Mitigation Strategies

Rencana untuk mengurangi risks.

- **Database Failure**: Multi-AZ setup, automated backups, regular restore testing
- **Service Outage**: Health checks, circuit breakers, auto-restart, load balancer redundancy
- **Security**: Regular security audits, penetration testing, secret rotation, access control
- **Performance**: Load testing, cache optimization, database query optimization, monitoring
- **Data Loss**: Backup strategy with multiple copies, tested recovery procedures

---

## 10. Technology Stack

### 10.1 Technology Choices

Teknologi yang digunakan.

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **API Gateway** | Kong / Nginx | Mature, scalable, feature-rich |
| **Services** | Node.js + Express | Fast, good for I/O, JavaScript ecosystem |
| **Authentication** | JWT + OAuth2 | Stateless, scalable, industry standard |
| **Database** | PostgreSQL 13 | ACID compliant, mature, excellent performance |
| **Cache** | Redis | Fast, in-memory, great for sessions |
| **Queue** | RabbitMQ | Reliable message processing, AMQP standard |
| **Container** | Docker | Standard container format |
| **Orchestration** | Kubernetes | Production-grade orchestration, auto-scaling |
| **Logging** | ELK Stack | Centralized logging, searchable |
| **Monitoring** | Prometheus + Grafana | Metrics collection, dashboards, alerting |

---

## 11. Implementation Timeline

### 11.1 Phasing Plan

Breakdown menjadi phases implementasi.

```
Phase 1 (Month 1-2): MVP
├─ User CRUD operations
├─ Basic authentication (email/password login)
├─ Role & permission models (no UI yet)
├─ Deploy to staging on AWS
└─ Basic monitoring setup

Phase 2 (Month 3-4): Enhancement
├─ OAuth2 integration (Google, Facebook)
├─ User profile management
├─ Password reset functionality
├─ Audit logging
└─ Performance optimization

Phase 3 (Month 5-6): Production Ready
├─ Multi-tenancy support
├─ Advanced monitoring & alerting
├─ Security audit + penetration testing
├─ Disaster recovery testing
└─ Production deployment

Phase 4 (Month 7+): Maintenance & Scaling
├─ Performance tuning based on real usage
├─ Feature requests implementation
├─ Continuous monitoring & optimization
└─ Infrastructure scaling as needed
```

---

## 12. Appendix

### 12.1 Glossary

| Term | Definition |
|------|-----------|
| **JWT** | JSON Web Token untuk authentication |
| **OAuth2** | Open authentication protocol |
| **RBAC** | Role-Based Access Control |
| **API Gateway** | Single entry point untuk semua API requests |
| **Microservices** | Small independent services vs monolith |
| **Multi-AZ** | Multiple Availability Zones (high availability) |
| **Redis** | In-memory data store untuk caching |
| **PostgreSQL** | Relational database |
| **Kubernetes** | Container orchestration platform |
| **RTO** | Recovery Time Objective |
| **RPO** | Recovery Point Objective |

### 12.2 References

- [Microservices Patterns](https://microservices.io/)
- [JWT.io Documentation](https://jwt.io/)
- [PostgreSQL Best Practices](https://www.postgresql.org/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### 12.3 Related Documents

- SDD-Full-Template.md - Complete SDD with all details
- LLD-Template.md - Low-level design with code details
- ADR-Template.md - Architecture Decision Records
- Deployment Guide - Step-by-step deployment instructions

---

**Document Prepared By:** [Name]
**Last Updated:** [Date]
**Status:** [Draft / In Review / Approved]

---
