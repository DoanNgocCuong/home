# Software Design Document (SDD)

**Project Name:** [Tên dự án]
**Version:** 1.0
**Date:** [Ngày viết]
**Author(s):** [Tên tác giả]
**Reviewed by:** [Tên reviewer]
**Status:** [Draft / In Review / Approved / Archived]

---

## 1. Introduction & Purpose

### 1.1 Mục đích Tài liệu (Document Purpose)

Giải thích lý do tài liệu này tồn tại.

**Ví dụ:**
> Tài liệu này định nghĩa thiết kế kỹ thuật chi tiết cho hệ thống quản lý người dùng (User Management System). Nó được tạo để hướng dẫn developers trong quá trình implementation, đảm bảo consistency về architecture, design patterns, và code quality.

### 1.2 Scope (Phạm vi)

Những gì tài liệu này cover và những gì nó không cover.

**Ví dụ:**
> **Trong scope:**
> - Authentication (login, logout, password reset)
> - User profile management
> - Role-based access control (RBAC)
> - API design cho user services
>
> **Ngoài scope:**
> - Frontend UI/UX (sẽ được cover trong Design Document riêng)
> - Email system configuration (DevOps)
> - Security audit penetration testing

### 1.3 Audience (Đối tượng Đọc)

Ai sẽ đọc tài liệu này?

**Ví dụ:**
- Backend developers
- Full-stack developers
- DevOps engineers
- QA engineers
- Technical leads

### 1.4 Document History (Lịch sử Tài liệu)

Theo dõi các version của tài liệu.

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-15 | [Tên] | Initial draft |
| 1.1 | TBD | | Updated after review |

---

## 2. System Overview

### 2.1 Mô tả Tổng quan (High-Level Description)

Giới thiệu hệ thống từ góc độ cao nhất.

**Ví dụ:**
> [Project Name] là một hệ thống quản lý người dùng cloud-native được xây dựng trên microservices architecture. Hệ thống cung cấp các dịch vụ authentication, user profile management, role management, và audit logging. Tất cả services được deploy trên Kubernetes và scale horizontally dựa trên demand.

### 2.2 Business Context (Bối cảnh Kinh doanh)

Tại sao hệ thống này được xây dựng? Nó giải quyết vấn đề gì?

**Ví dụ:**
> Hệ thống hiện tại (legacy monolith) không scale được với 10 triệu users. Nó gây bottleneck trong việc add tính năng mới. Business yêu cầu một giải pháp có thể scale đến 100 triệu users trong 2 năm tới.

### 2.3 Key Features Summary (Tóm tắt Tính năng Chính)

Liệt kê những tính năng chính (ở high level).

**Ví dụ:**
- User authentication (username/password, OAuth2, SAML)
- User profile management (CRUD operations)
- Role-based access control (RBAC)
- Audit logging & compliance
- Real-time notifications
- User search & filtering

### 2.4 Success Criteria (Tiêu chí Thành công)

Làm sao để biết project này thành công?

**Ví dụ:**
- System có thể handle 100,000 concurrent users
- Response time < 200ms cho 95% requests
- 99.99% uptime (SLA)
- Support cho 50 languages
- Support multi-tenancy

---

## 3. Design Considerations

### 3.1 Constraints (Ràng buộc)

Những ràng buộc kỹ thuật, tiền, hoặc thời gian.

**Ví dụ:**

| Loại | Constraint | Giải thích |
|------|-----------|-----------|
| **Technical** | Must use PostgreSQL | Company standard, cost-effective, mature |
| **Technical** | Kubernetes for orchestration | Flexibility, auto-scaling, standard practice |
| **Timeline** | MVP release trong 6 tháng | Business deadline |
| **Budget** | Max $500K cho infrastructure/năm | CFO approval limit |
| **Team** | Max 8 engineers | Resource available |
| **Compliance** | GDPR compliant | EU users requirement |

### 3.2 Assumptions (Giả định)

Những giả định mà thiết kế này dựa vào.

**Ví dụ:**
- Giả định network latency < 100ms giữa services
- Giả định database failover < 30 seconds
- Giả định 80% reads, 20% writes workload
- Giả định average user session = 30 minutes
- Giả định external APIs (OAuth) have 99.5% uptime

### 3.3 Limitations (Hạn chế)

Những hạn chế của thiết kế này.

**Ví dụ:**
- System không support realtime collaboration (> 1000 concurrent editors)
- Maximum file size upload = 1GB (AWS S3 limitation)
- Batch operations limited to 10,000 items per request
- Historical data retention = 7 years (compliance requirement)

---

## 4. Architecture Design

### 4.1 Architecture Pattern (Kiến trúc Tổng thể)

Loại architecture được sử dụng.

**Ví dụ:**
> **Microservices Architecture**
> - Mỗi business capability là một service riêng (user-service, auth-service, role-service)
> - Services communicate qua HTTP/REST hoặc message queues (RabbitMQ)
> - Shared database (PostgreSQL) hoặc database per service (tùy use case)
> - API Gateway (Kong/Nginx) làm entry point

### 4.2 Architecture Diagram

Vẽ diagram toàn bộ architecture.

```
┌─────────────────────────────────────────────────┐
│         API Gateway (Kong)                      │
│         - Rate limiting                         │
│         - Authentication check                  │
│         - Request routing                       │
└──┬──────────────┬──────────────┬────────────────┘
   │              │              │
┌──▼────┐  ┌──────▼───┐  ┌──────▼────┐
│User   │  │Auth      │  │Role       │
│Service│  │Service   │  │Service    │
│       │  │          │  │           │
│ - GET │  │ - POST   │  │ - GET     │
│ - POST│  │ - PUT    │  │ - POST    │
│ - PUT │  │ - DELETE │  │ - DELETE  │
└──┬────┘  └──┬───────┘  └──┬────────┘
   │          │             │
   └──────────┴─────────────┘
         │
    ┌────▼────────────────┐
    │   PostgreSQL 13     │
    │   (Main database)   │
    └─────────────────────┘
         │
    ┌────▼──────────┐
    │ Redis Cache   │
    │ (Session store)
    └───────────────┘
```

### 4.3 Component Overview (Tóm tắt Các Component)

Giới thiệu từng component chính.

| Component | Responsibility | Technology |
|-----------|---|---|
| API Gateway | Route requests, rate limiting, auth check | Kong |
| User Service | CRUD user data, validation | Node.js + Express |
| Auth Service | Login, logout, token generation | Node.js + JWT |
| Role Service | RBAC, permission checking | Node.js + Express |
| Database | Persist data | PostgreSQL 13 |
| Cache | Session, user data caching | Redis 6.0 |
| Message Queue | Async events, notifications | RabbitMQ |
| Logger | Centralized logging | ELK Stack |
| Monitor | Metrics, alerts | Prometheus + Grafana |

### 4.4 Design Rationale (Lý do Chọn Architecture này)

Tại sao lại chọn architecture này thay vì alternatives?

**Ví dụ:**
> **Tại sao Microservices thay vì Monolith?**
> 1. **Scalability**: Có thể scale từng service độc lập dựa trên demand
> 2. **Autonomy**: Teams có thể develop, deploy riêng biệt (fast time-to-market)
> 3. **Fault Isolation**: Nếu Auth Service down, User Service vẫn hoạt động
> 4. **Technology Flexibility**: Mỗi team có thể dùng khác nhau tech stack nếu cần
>
> **Trade-offs:**
> - Complexity tăng lên (distributed system debugging khó hơn)
> - Network latency (inter-service communication)
> - Data consistency challenges (distributed transactions)
> - Operations overhead (monitoring, deployment, etc.)

---

## 5. High-Level Design (HLD)

### 5.1 Main Modules/Components

Liệt kê các modules chính và responsibilities.

**Ví dụ:**

```
┌─────────────────────────────────────────┐
│ User Management Module                  │
├─────────────────────────────────────────┤
│ • User CRUD (Create, Read, Update, Delete)
│ • Profile Management
│ • Search & Filtering
│ • Bulk import/export
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Authentication Module                   │
├─────────────────────────────────────────┤
│ • Login/Logout
│ • Token generation (JWT)
│ • Password reset
│ • OAuth2 integration
│ • Session management
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Authorization Module                    │
├─────────────────────────────────────────┤
│ • RBAC (Role-Based Access Control)
│ • Permission checking
│ • Access policy evaluation
│ • Audit logging
└─────────────────────────────────────────┘
```

### 5.2 Data Flow Between Components

Luồng dữ liệu giữa các components.

**Ví dụ: Login Flow**

```
1. User submits credentials (email, password) → API Gateway
2. API Gateway → Auth Service (HTTP POST /auth/login)
3. Auth Service:
   - Validate credentials vs User Service
   - Generate JWT token
   - Cache token in Redis
   - Return JWT to client
4. Client stores JWT in localStorage
5. For subsequent requests:
   - Client sends JWT in Authorization header
   - API Gateway validates JWT từ Redis cache
   - If valid → route to service
   - If invalid → return 401 Unauthorized
```

### 5.3 External System Integrations

Integrate với external systems?

**Ví dụ:**
- Google OAuth2 (third-party authentication)
- Sendgrid (email notifications)
- Twilio (SMS notifications)
- AWS S3 (user avatar storage)
- Stripe (payment verification)

### 5.4 System Interactions Diagram

Vẽ sequence diagram cho main flows.

**Ví dụ: User Login Sequence**

```
Client          API Gateway      Auth Service      User Service      Redis
  │                │                 │                  │              │
  │──POST /login───│                 │                  │              │
  │                │──validate creds─│                  │              │
  │                │                 │──GET user────────│              │
  │                │                 │                  │              │
  │                │                 │<──user data──────│              │
  │                │                 │                  │              │
  │                │                 │──check password──│              │
  │                │                 │  (bcrypt)        │              │
  │                │                 │  OK              │              │
  │                │<──JWT token─────│                  │              │
  │                │                 │──CACHE token────────────────────│
  │<──200 OK───────│                 │                  │              │
  │   {JWT}        │                 │                  │              │
```

---

## 6. Low-Level Design (LLD)

### 6.1 Class Diagrams (Nếu OOP)

Chi tiết về classes, relationships.

**Ví dụ:**

```
┌─────────────────────┐
│      User           │
├─────────────────────┤
│ - id: UUID          │
│ - email: String     │
│ - password: String  │
│ - firstName: String │
│ - lastName: String  │
│ - isActive: Boolean │
│ - createdAt: Date   │
│ - updatedAt: Date   │
├─────────────────────┤
│ + create()          │
│ + read()            │
│ + update()          │
│ + delete()          │
│ + validateEmail()   │
│ + hashPassword()    │
└─────────────────────┘
        │
        │ has_many
        │
┌──────▼──────────────┐
│      Role           │
├─────────────────────┤
│ - id: UUID          │
│ - name: String      │
│ - description: Text │
│ - createdAt: Date   │
├─────────────────────┤
│ + create()          │
│ + read()            │
│ + update()          │
│ + delete()          │
└─────────────────────┘
        │
        │ has_many
        │
┌──────▼──────────────┐
│   Permission        │
├─────────────────────┤
│ - id: UUID          │
│ - name: String      │
│ - resource: String  │
│ - action: String    │
├─────────────────────┤
│ + check()           │
└─────────────────────┘
```

### 6.2 Function/Method Specifications

Chi tiết về functions/methods.

**Ví dụ:**

```
Function: createUser()
────────────────────────────────────────────
Input:
  - email: string (required, valid email format)
  - firstName: string (required, 1-50 chars)
  - lastName: string (required, 1-50 chars)
  - password: string (required, min 8 chars, contains uppercase, number, special char)
  - roles: UUID[] (optional, default=['user'])

Output:
  - userId: UUID
  - email: string
  - firstName: string
  - lastName: string
  - roles: Role[]
  - createdAt: ISO8601 timestamp

Validation:
  - Email must be unique (check database)
  - Password must meet complexity requirements
  - Roles must exist in Role table

Error Cases:
  - 409 Conflict: Email already exists
  - 400 Bad Request: Invalid email format
  - 400 Bad Request: Password does not meet requirements
  - 422 Unprocessable Entity: Role not found

Side Effects:
  - Hash password using bcrypt (salt rounds: 10)
  - Create audit log entry
  - Send welcome email via Sendgrid
  - Cache user in Redis (TTL: 1 hour)
────────────────────────────────────────────
```

### 6.3 Algorithm Descriptions

Chi tiết về algorithms quan trọng.

**Ví dụ: Password Hashing Algorithm**

```
Algorithm: hashPassword(plainPassword)
──────────────────────────────────
1. Generate random salt (bcrypt default: rounds=10)
2. Apply bcrypt hash function: hashedPassword = bcrypt(plainPassword, salt)
3. Store hashedPassword in database
4. Never store plainPassword

Verification: verifyPassword(plainPassword, hashedPassword)
1. Apply bcrypt with same hashedPassword: result = bcrypt.compare(plainPassword, hashedPassword)
2. Return true/false

Why bcrypt:
- Slow intentionally (protects against brute force)
- Adaptive (salt rounds can increase over time)
- Industry standard for password hashing
```

### 6.4 Code Structure

Project structure và organization.

**Ví dụ:**

```
user-service/
├── src/
│   ├── controllers/
│   │   ├── userController.js
│   │   └── authController.js
│   ├── services/
│   │   ├── userService.js
│   │   ├── authService.js
│   │   └── validationService.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Role.js
│   │   └── Permission.js
│   ├── routes/
│   │   ├── users.js
│   │   └── auth.js
│   ├── middleware/
│   │   ├── authMiddleware.js
│   │   ├── errorHandler.js
│   │   └── logger.js
│   ├── utils/
│   │   ├── passwordUtils.js
│   │   ├── tokenUtils.js
│   │   └── validators.js
│   ├── config/
│   │   ├── database.js
│   │   ├── redis.js
│   │   └── env.js
│   └── app.js
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/
│   └── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── package.json
```

---

## 7. Data Design

### 7.1 Database Schema (Entity-Relationship Diagram)

Thiết kế database.

**Ví dụ:**

```
┌──────────────────┐
│      users       │
├──────────────────┤
│ id (PK)          │◄────┐
│ email (UNIQUE)   │     │
│ first_name       │     │
│ last_name        │     │
│ password_hash    │     │
│ is_active        │     │
│ created_at       │     │
│ updated_at       │     │
└──────────────────┘     │
         │               │
         │ 1:M           │
         │               │
┌────────▼──────────┐    │
│  user_roles       │    │
├───────────────────┤    │
│ id (PK)           │    │
│ user_id (FK)──────┘    │
│ role_id (FK)──┐        │
└───────────────┼────────┘
                │
         1:M    │
┌───────────────▼──────┐
│     roles            │
├──────────────────────┤
│ id (PK)              │
│ name (UNIQUE)        │
│ description          │
│ created_at           │
└──────────────────────┘
         │
         │ 1:M
         │
┌────────▼──────────────┐
│ role_permissions     │
├──────────────────────┤
│ id (PK)              │
│ role_id (FK)         │
│ permission_id (FK)───┐
└──────────────────────┘
                │
         1:M    │
┌───────────────▼──────┐
│    permissions       │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ resource             │
│ action               │
│ description          │
└──────────────────────┘
```

### 7.2 Data Models (DDL Scripts)

SQL để create tables.

**Ví dụ:**

```sql
-- Create users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

-- Create roles table
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create permissions table
CREATE TABLE permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  resource VARCHAR(100) NOT NULL,
  action VARCHAR(50) NOT NULL,
  description TEXT,
  UNIQUE(resource, action)
);

-- Create junction tables
CREATE TABLE user_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  UNIQUE(user_id, role_id)
);

CREATE TABLE role_permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
  UNIQUE(role_id, permission_id)
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
```

### 7.3 Data Validation Rules

Rules cho data validation.

**Ví dụ:**

| Field | Validation Rules | Error Message |
|-------|---|---|
| email | Must match email regex; must be unique; max 255 chars | Invalid email format |
| first_name | Required; 1-100 chars; no special chars | Invalid first name |
| last_name | Required; 1-100 chars; no special chars | Invalid last name |
| password | Min 8 chars; must contain uppercase, lowercase, number, special char | Password does not meet requirements |
| is_active | Boolean only | Invalid value for is_active |

### 7.4 Data Flow

Bagaimana data mengalir dalam system?

**Ví dụ: User Registration Flow**

```
1. User submits form (email, password, firstName, lastName)
   ↓
2. Client-side validation (format check)
   ↓
3. API receives POST /users request
   ↓
4. Server-side validation
   ├─ Email format validation
   ├─ Email uniqueness check (query database)
   ├─ Password strength check
   └─ Name format check
   ↓
5. Hash password (bcrypt)
   ↓
6. Insert user record to PostgreSQL
   ↓
7. Assign default 'user' role via user_roles table
   ↓
8. Cache user data in Redis (TTL: 1 hour)
   ↓
9. Generate JWT token
   ↓
10. Send welcome email via Sendgrid (async queue)
   ↓
11. Return user data + JWT to client
```

---

## 8. Interface Design

### 8.1 API Specifications

Rest API, GraphQL, gRPC?

**Ví dụ: RESTful API**

```
BASE_URL: https://api.example.com/v1
Authentication: Bearer {JWT_TOKEN} in Authorization header
```

### 8.2 API Endpoints

List tất cả endpoints.

**Ví dụ:**

```
┌─────────────────────────────────────────────────────┐
│ USER MANAGEMENT                                     │
├─────────────────────────────────────────────────────┤
│ POST   /users              → Create user            │
│ GET    /users              → List all users         │
│ GET    /users/{id}         → Get user by ID         │
│ PUT    /users/{id}         → Update user            │
│ DELETE /users/{id}         → Delete user            │
│ GET    /users/search?q=... → Search users           │
│ PATCH  /users/{id}/avatar  → Upload avatar         │
│ POST   /users/bulk-import  → Bulk import from CSV  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ AUTHENTICATION                                      │
├─────────────────────────────────────────────────────┤
│ POST   /auth/login         → Login (username/pwd)   │
│ POST   /auth/logout        → Logout                 │
│ POST   /auth/refresh       → Refresh JWT token      │
│ POST   /auth/oauth/google  → OAuth2 Google login    │
│ POST   /auth/password-reset → Request password reset│
│ POST   /auth/password-reset/verify → Verify reset  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ AUTHORIZATION                                       │
├─────────────────────────────────────────────────────┤
│ GET    /roles              → List all roles         │
│ POST   /roles              → Create role            │
│ PUT    /roles/{id}         → Update role            │
│ DELETE /roles/{id}         → Delete role            │
│ GET    /permissions        → List permissions       │
│ POST   /roles/{id}/permissions → Assign permission  │
│ DELETE /roles/{id}/permissions/{pid} → Revoke perm │
└─────────────────────────────────────────────────────┘
```

### 8.3 Request/Response Formats

Schema untuk request dan response.

**Ví dụ: POST /users (Create User)**

```json
REQUEST:
────────
POST /v1/users
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "password": "SecurePass123!",
  "roles": ["uuid-user-role"]
}

RESPONSE (201 Created):
──────────────────────
{
  "id": "uuid-1234-5678",
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isActive": true,
  "roles": [
    {
      "id": "uuid-user-role",
      "name": "user",
      "description": "Regular user role"
    }
  ],
  "createdAt": "2026-03-15T10:30:00Z",
  "updatedAt": "2026-03-15T10:30:00Z"
}

ERROR RESPONSE (409 Conflict):
──────────────────────────────
{
  "error": {
    "code": "DUPLICATE_EMAIL",
    "message": "Email john.doe@example.com already exists",
    "timestamp": "2026-03-15T10:30:00Z"
  }
}
```

### 8.4 Error Codes

Tất cả error codes dan meanings.

| Status | Code | Message | Cause |
|--------|------|---------|-------|
| 400 | BAD_REQUEST | Invalid request parameters | Wrong format, missing required fields |
| 401 | UNAUTHORIZED | Authentication required | Missing or invalid JWT token |
| 403 | FORBIDDEN | Access denied | User doesn't have permission |
| 404 | NOT_FOUND | Resource not found | User ID doesn't exist |
| 409 | DUPLICATE_EMAIL | Email already exists | Trying to create user with duplicate email |
| 422 | VALIDATION_ERROR | Validation failed | Data validation error |
| 429 | RATE_LIMIT | Too many requests | Rate limit exceeded |
| 500 | INTERNAL_ERROR | Internal server error | Unexpected error |

### 8.5 UI/UX Design (Jika có Frontend)

(Thường được cover dalam Design Document riêng, bukan SDD)

Link ke Figma, design files, wireframes.

**Ví dụ:**
- Login page: https://figma.com/...
- User profile page: https://figma.com/...
- User management dashboard: https://figma.com/...

---

## 9. Security Design

### 9.1 Authentication & Authorization

Xác thực và phân quyền.

**Authentication:**
- Method: JWT (JSON Web Token) + OAuth2
- Flow:
  1. User login with email + password
  2. Server validate credentials
  3. If valid, generate JWT (HS256 algorithm)
  4. Client store JWT in localStorage (NOT cookies, for CSRF protection)
  5. Each request include JWT in Authorization header
  6. Server validate JWT signature

**Authorization (RBAC):**
- Each user has roles (admin, moderator, user, etc.)
- Each role has permissions (user:read, user:write, user:delete)
- API checks user permissions before executing action
- Policy: If user lacks permission → return 403 Forbidden

### 9.2 Encryption (Data in Transit & at Rest)

**Data in Transit:**
- All API requests use HTTPS (TLS 1.3)
- Certificate: Let's Encrypt (auto-renewed)
- Force redirect from HTTP to HTTPS
- HSTS header: Strict-Transport-Security: max-age=31536000

**Data at Rest:**
- Passwords: bcrypt hash (salt rounds: 10)
- Sensitive data (SSN, payment info): AES-256 encryption in database
- Database: Encrypted volume (AWS EBS encryption enabled)
- Secrets: Stored in HashiCorp Vault, not in code/config files

### 9.3 Vulnerability Assessment

Potential vulnerabilities and mitigation.

| Vulnerability | Risk | Mitigation |
|---|---|---|
| SQL Injection | High | Use parameterized queries, ORM, input validation |
| XSS | High | HTML encode output, CSP headers, DOMPurify library |
| CSRF | Medium | CSRF tokens, SameSite cookies, check Referer header |
| Brute Force | Medium | Rate limiting (10 attempts/minute), account lockout (5 mins) |
| DDoS | Medium | WAF (Web Application Firewall), rate limiting, CDN |
| Privilege Escalation | High | Strict RBAC, audit logging, regular access review |
| Data Leakage | High | Encryption, secrets management, access control, audit logs |

### 9.4 Security Protocols

Standards dan best practices.

- **OWASP Top 10**: Follow OWASP security guidelines
- **PCI DSS**: Compliance jika handle payment data
- **GDPR**: Data protection, privacy, consent management
- **Password Policy**: Min 8 chars, uppercase, lowercase, number, special char
- **Token Expiration**: JWT expires in 1 hour; refresh token = 7 days
- **API Key Rotation**: Monthly rotation untuk external API keys
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, CSP

---

## 10. Performance & Scalability

### 10.1 Performance Targets

Target metrics dan SLA.

| Metric | Target | Rationale |
|--------|--------|-----------|
| Response Time (p50) | < 100ms | Good user experience |
| Response Time (p95) | < 200ms | Acceptable for most users |
| Response Time (p99) | < 500ms | Outliers acceptable |
| Throughput | 10,000 req/sec | Expected peak load |
| Error Rate | < 0.1% | 99.9% success rate |
| Availability | 99.99% (4 hours downtime/year) | Enterprise SLA |

### 10.2 Scalability Strategy

Horizontal vs Vertical scaling.

**Horizontal Scaling (Preferred):**
- Run multiple instances of each service (User Service, Auth Service, etc.)
- Load balancer distributes requests (round-robin)
- Auto-scaling: Scale up when CPU > 70%, scale down when CPU < 30%
- Kubernetes HPA (Horizontal Pod Autoscaler) untuk orchestration

**Vertical Scaling (Fallback):**
- Increase server resources (CPU, RAM)
- Limited by single machine hardware limits
- Usually not recommended untuk cloud-native apps

### 10.3 Caching Strategy

Multi-level caching.

| Layer | Technology | TTL | Use Case |
|-------|---|---|---|
| Client | Browser cache | 1 hour | Static assets, user data |
| CDN | CloudFlare | 1 day | Static files, CSS, JS |
| Application | Redis | 1 hour | User sessions, role/permission data |
| Database | PostgreSQL query cache | N/A | Frequent queries |

**Cache Invalidation:**
- TTL-based: Automatic expiry
- Event-based: Clear cache when data changes (user update → clear user cache)
- Conditional GET: Use ETags to reduce data transfer

### 10.4 Load Balancing & Database Optimization

**Load Balancing:**
- API Gateway (Kong) load balance across service instances
- Database read replicas untuk read-heavy queries
- Connection pooling (PgBouncer) untuk reuse DB connections

**Database Optimization:**
- Indexes on frequently queried columns (email, user_id)
- Query optimization (use EXPLAIN ANALYZE)
- Partition large tables (time-based partitioning untuk audit logs)
- Denormalization where needed (cache calculated fields)

---

## 11. Error Handling & Logging

### 11.1 Exception Handling Strategy

Bagaimana handle errors?

**Approach:**
1. **Try-Catch Blocks**: Wrap risky operations
2. **Custom Exceptions**: Define application-specific exceptions
3. **Error Responses**: Return meaningful error messages to clients
4. **Graceful Degradation**: Fallback behavior jika possible
5. **Error Propagation**: Log errors yang tidak bisa handle

**Ví dụ:**

```javascript
try {
  // 1. Validate input
  validateUserInput(email, password);

  // 2. Query database
  const user = await User.findByEmail(email);

  // 3. Check result
  if (!user) {
    throw new UserNotFoundError(`User with email ${email} not found`);
  }

  // 4. Verify password
  const passwordValid = await bcrypt.compare(password, user.passwordHash);
  if (!passwordValid) {
    throw new InvalidPasswordError('Password incorrect');
  }

  // 5. Success
  return generateJWT(user);

} catch (error) {
  // 6. Error handling
  if (error instanceof ValidationError) {
    logger.warn('Validation failed', { error });
    return { status: 400, message: error.message };
  } else if (error instanceof UserNotFoundError) {
    logger.info('User not found', { email });
    return { status: 404, message: error.message };
  } else if (error instanceof InvalidPasswordError) {
    logger.warn('Invalid password attempt', { email, ip: req.ip });
    return { status: 401, message: 'Invalid credentials' };
  } else {
    // Unexpected error
    logger.error('Unexpected error in login', { error: error.stack });
    return { status: 500, message: 'Internal server error' };
  }
}
```

### 11.2 Logging Levels & Formats

Structured logging.

**Log Levels:**
- **ERROR**: System errors, exceptions, failed operations
- **WARN**: Suspicious activities, degraded performance, auth failures
- **INFO**: Important events, user actions, deployments
- **DEBUG**: Detailed info for debugging (disabled in production)
- **TRACE**: Very detailed info (rarely used)

**Log Format (JSON structured logs):**

```json
{
  "timestamp": "2026-03-15T10:30:45.123Z",
  "level": "ERROR",
  "logger": "auth-service",
  "message": "Database connection failed",
  "error": {
    "type": "ConnectionError",
    "message": "Cannot connect to PostgreSQL",
    "stack": "..."
  },
  "context": {
    "userId": "user-123",
    "requestId": "req-456",
    "ip": "192.168.1.1"
  }
}
```

### 11.3 Monitoring & Alerting

Paano mo i-monitor ang system health?

**Metrics to Monitor:**
- Request latency (p50, p95, p99)
- Error rate (5xx, 4xx)
- CPU, memory usage
- Database connection pool
- Cache hit rate
- Queue depth (message queue)

**Alerting Rules:**
- Error rate > 1% → Alert immediately
- p95 latency > 500ms → Alert
- CPU > 85% → Alert
- Memory > 90% → Alert
- Database disk usage > 80% → Alert

**Tools:**
- Prometheus: Metrics collection
- Grafana: Dashboards
- AlertManager: Alert routing
- DataDog: Distributed tracing (optional)

### 11.4 Debugging Approach

Cách debug issues?

1. **Check Logs**: Look for error messages, stack traces
2. **Check Metrics**: CPU, memory, latency spikes
3. **Reproduce Issue**: Try to replicate locally or in staging
4. **Use Distributed Tracing**: Follow request across services
5. **Check Dependencies**: External APIs, database, cache
6. **Review Recent Changes**: Code changes, deployments, infrastructure changes
7. **Check Network**: Latency, packet loss, DNS resolution
8. **Load Test**: Reproduce under load conditions nếu needed

---

## 12. Deployment & DevOps

### 12.1 Deployment Architecture

Infrastructure setup.

**Ví dụ: Kubernetes on AWS**

```
┌────────────────────────────────────────────────┐
│         AWS Account (Prod)                     │
├────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐  │
│  │ EKS Cluster (Kubernetes)                │  │
│  │ ├─ 3 Worker Nodes (t3.large, AZ spread)│  │
│  │ ├─ User Service Pod (3 replicas)       │  │
│  │ ├─ Auth Service Pod (3 replicas)       │  │
│  │ ├─ Role Service Pod (2 replicas)       │  │
│  │ └─ API Gateway Pod (3 replicas, Nginx) │  │
│  └─────────────────────────────────────────┘  │
│           ↓                                    │
│  ┌─────────────────────────────────────────┐  │
│  │ RDS PostgreSQL (Multi-AZ)               │  │
│  │ ├─ Primary (writer)                     │  │
│  │ └─ Standby replica (read-only)          │  │
│  └─────────────────────────────────────────┘  │
│           ↓                                    │
│  ┌─────────────────────────────────────────┐  │
│  │ ElastiCache Redis (Multi-AZ)            │  │
│  │ ├─ Primary (writer)                     │  │
│  │ └─ Replica (read-only)                  │  │
│  └─────────────────────────────────────────┘  │
│           ↓                                    │
│  ┌─────────────────────────────────────────┐  │
│  │ Application Load Balancer (ALB)         │  │
│  │ └─ Routes traffic to API Gateway        │  │
│  └─────────────────────────────────────────┘  │
│           ↓                                    │
│  ┌─────────────────────────────────────────┐  │
│  │ Route 53 (DNS)                          │  │
│  │ └─ api.example.com → ALB                │  │
│  └─────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
```

### 12.2 CI/CD Pipeline

Automation dari code to production.

```
Developer pushes code to GitHub
        ↓
GitHub Actions triggers CI job
        ├─ Run tests (unit + integration)
        ├─ Run linter (ESLint)
        ├─ Run security scan (Snyk)
        ├─ Build Docker image
        └─ Push to Docker registry
        ↓
If tests pass:
        ├─ Deploy to dev environment
        ├─ Deploy to staging environment
        └─ Create release in GitHub
        ↓
Manual approval → Deploy to production
        ├─ Update Kubernetes deployment
        ├─ Rolling update (no downtime)
        └─ Run smoke tests
        ↓
Monitor metrics & logs
        ├─ If error rate > 1%: Auto-rollback
        └─ If OK: Keep new version
```

### 12.3 Environment Setup

Development, staging, production.

| Aspect | Dev | Staging | Production |
|--------|-----|---------|-----------|
| **Infra** | Laptop/VM | AWS (small) | AWS (large, multi-AZ) |
| **Database** | SQLite/local | RDS PostgreSQL | RDS PostgreSQL (backup, replicas) |
| **Data** | Test data | Copy of prod | Real customer data |
| **Monitoring** | None | CloudWatch | CloudWatch + DataDog |
| **Backup** | None | Daily | Hourly |
| **SSL/TLS** | HTTP OK | HTTPS required | HTTPS required |
| **Secrets** | Hardcoded OK | Environment vars | AWS Secrets Manager |

### 12.4 Rollback Strategy

Bagaimana revert bad deployment?

**Strategy: Blue-Green Deployment**

```
Before:
  Blue deployment (current) = v1.5 running
  Green deployment (new) = v1.6 not running

After deploy v1.6:
  Green deployment (new) = v1.6 running
  Load balancer still routes to Blue

If v1.6 is OK:
  Wait 24 hours for stability
  Then switch load balancer to Green
  Keep Blue as fallback

If v1.6 has bugs:
  Switch load balancer back to Blue immediately
  Kill Green deployment
  No downtime!
```

---

## 13. Appendix

### 13.1 Glossary (Thuật ngữ)

| Term | Definition |
|------|-----------|
| **JWT** | JSON Web Token - token-based authentication |
| **RBAC** | Role-Based Access Control - permission system |
| **HLD** | High-Level Design - big picture architecture |
| **LLD** | Low-Level Design - detailed code structure |
| **API Gateway** | Entry point for all API requests |
| **Microservices** | Small independent services vs monolithic |
| **Kubernetes** | Container orchestration platform |
| **Redis** | In-memory data store for caching |
| **PostgreSQL** | Relational database |
| **OAuth2** | Open authentication standard |
| **BCrypt** | Password hashing algorithm |
| **HTTPS/TLS** | Encrypted communication protocol |
| **CI/CD** | Continuous Integration/Deployment automation |

### 13.2 References (Tài liệu Tham khảo)

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT.io](https://jwt.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Spring Boot Best Practices](https://spring.io/guides)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)

### 13.3 FAQ

**Q: Khi nào update SDD?**
A: Update khi:
- Major design changes
- New requirements come in
- Found design issues during implementation
- End of each sprint (review & update)

**Q: SDD có cần đầy đủ tất cả 13 sections?**
A: Không phải. Tùy vào project size:
- Small projects: sections 1-8 enough
- Large projects: tất cả 13 sections
- Startup/MVP: core sections (1-6, 9)

**Q: SDD nên bao chi tiết?**
A: Chi tiết đủ để developer code mà không cần hỏi. Nếu trong 1 sprint 1 dev bỏ 10 giờ hỏi "cái này làm sao?", SDD chưa đủ chi tiết.

**Q: SDD nên dùng tool gì?**
A: Tùy preference:
- Google Docs (colaboration, easy sharing)
- Markdown + Git (version control, automation)
- Confluence (enterprise, search capability)
- Notion (flexible, multimedia)

### 13.4 Related Documents Links

- [Product Requirements Document (PRD)](./PRD-Template.md)
- [Business Requirements Document (BRD)](./BRD-Template.md)
- [High-Level Design (HLD)](./HLD-Template.md)
- [Low-Level Design (LLD)](./LLD-Template.md)
- [Architecture Decision Record (ADR)](./ADR-Template.md)
- [Test Design Document (TDD)](./TDD-Template.md)

---

## Document Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| **Tech Lead** | [Name] | [Date] | [Signature] |
| **Architect** | [Name] | [Date] | [Signature] |
| **Dev Lead** | [Name] | [Date] | [Signature] |
| **QA Lead** | [Name] | [Date] | [Signature] |

---

**Document Prepared By:** [Name]
**Document Approved By:** [Name]
**Last Updated:** [Date]
**Next Review Date:** [Date]

---

*This document is confidential and intended for authorized personnel only. Unauthorized access is prohibited.*
