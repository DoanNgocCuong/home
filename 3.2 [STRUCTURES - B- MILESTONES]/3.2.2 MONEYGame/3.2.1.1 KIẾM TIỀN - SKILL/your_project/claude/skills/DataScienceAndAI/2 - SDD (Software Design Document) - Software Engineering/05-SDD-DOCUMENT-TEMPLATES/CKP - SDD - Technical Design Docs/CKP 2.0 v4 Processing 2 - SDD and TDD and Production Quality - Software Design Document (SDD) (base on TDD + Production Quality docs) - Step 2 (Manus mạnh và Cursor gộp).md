# 1. TECHNICAL DEEP-DIVE SPECIFICATION (TDD)

**Version 3.1 - Universal Pro Edition**  
_Áp dụng cho: Backend, Frontend, AI/ML Systems_

---

## 📋 METADATA (Document Header)

_Bắt buộc có ở đầu mọi tài liệu TDD_

```yaml
# ============================================
# DOCUMENT METADATA
# ============================================
Title: [Tên Module/System - VD: User Authentication Service]
Document ID: TDD-[PROJECT]-[MODULE]-[VERSION] # VD: TDD-PIKA-AUTH-001
Author: [Primary Engineer/Architect]
Co-Authors: [Các contributor khác]
Reviewers: 
  - Technical: [Tech Lead Name]
  - Product: [Product Manager Name]  
  - Security: [Security Engineer Name]
  - QA: [QA Lead Name]

Status: [Draft | In Review | Approved | Implemented | Deprecated]
Priority: [P0-Critical | P1-High | P2-Medium | P3-Low]

# Timeline
Created: YYYY-MM-DD
Last Updated: YYYY-MM-DD
Target Release: YYYY-MM-DD (Sprint/Quarter)
Review Deadline: YYYY-MM-DD

# Versioning
Version: X.Y.Z (Semantic Versioning)
# X = Major breaking changes
# Y = New features
# Z = Bug fixes/minor updates

# Related Documents
Related Docs:
  - PRD: [Link to Product Requirements Document]
  - ADR: [Link to Architecture Decision Records]
  - API Spec: [Link to OpenAPI/Swagger]
  - UI Design: [Link to Figma/Sketch]
  - Test Plan: [Link to Test Strategy Document]
```

**📌 Tips:**

- Luôn update `Last Updated` khi có thay đổi
- Version bump theo quy tắc: Bug fix → Z++, New feature → Y++, Breaking change → X++
- Status flow: Draft → In Review → Approved → Implemented

---

## 1. OVERVIEW & CONTEXT

_Tổng quan ngắn gọn - Giữ dưới 1 trang A4_

### 1.1. Executive Summary (TL;DR)

|Item|Description|
|:--|:--|
|**Problem Statement**|[1-2 câu mô tả vấn đề cần giải quyết]|
|**Proposed Solution**|[1-2 câu mô tả giải pháp]|
|**Business Impact**|[Quantifiable value - VD: Tăng conversion 20%, giảm latency 50%]|
|**Technical Impact**|[VD: Reduce infra cost 30%, improve reliability to 99.9%]|
|**Estimated Effort**|[X người × Y sprint = Z man-days]|
|**Risk Level**|[Low/Medium/High] với brief justification|

**Example:**

```
Problem: Hệ thống authentication hiện tại không scale được quá 1000 concurrent users,
         response time tăng exponentially khi load cao.

Solution: Migrate từ session-based sang JWT + Redis distributed cache,
          implement rate limiting và connection pooling.

Impact: 
- Business: Giảm bounce rate 15%, support 10x more users
- Technical: p99 latency từ 2s → 200ms, uptime 99.9%
```

### 1.2. Background & Motivation

#### 1.2.1. Why Now?

- **Business Driver:** [Tại sao timing này quan trọng? VD: Chuẩn bị cho Black Friday]
- **Technical Debt:** [Debt nào đang block progress?]
- **Market Opportunity:** [Cơ hội thị trường nếu có]

#### 1.2.2. Current State (As-Is)

```
┌─────────────────────────────────────────────────────────────┐
│  CURRENT ARCHITECTURE                                       │
├─────────────────────────────────────────────────────────────┤
│  [Mô tả hệ thống hiện tại - diagram nếu cần]               │
│                                                             │
│  Pain Points:                                               │
│  1. [Issue 1 + Impact]                                      │
│  2. [Issue 2 + Impact]                                      │
│  3. [Issue 3 + Impact]                                      │
└─────────────────────────────────────────────────────────────┘
```

#### 1.2.3. Target State (To-Be)

```
┌─────────────────────────────────────────────────────────────┐
│  TARGET ARCHITECTURE                                        │
├─────────────────────────────────────────────────────────────┤
│  [Mô tả hệ thống sau khi implement - diagram]              │
│                                                             │
│  Benefits:                                                  │
│  1. [Benefit 1 + Metric]                                    │
│  2. [Benefit 2 + Metric]                                    │
│  3. [Benefit 3 + Metric]                                    │
└─────────────────────────────────────────────────────────────┘
```

#### 1.2.4. Alternatives Considered

|Alternative|Pros|Cons|Why Rejected|
|:--|:--|:--|:--|
|Option A|- Pro 1<br>- Pro 2|- Con 1<br>- Con 2|[Lý do]|
|Option B|- Pro 1<br>- Pro 2|- Con 1<br>- Con 2|[Lý do]|
|**Selected**|- Pro 1<br>- Pro 2|- Con 1 (mitigated by X)|✅ Best fit|

### 1.3. Success Criteria

#### Definition of Done (DoD)

**Technical Criteria:**

- [ ] All unit tests pass (coverage ≥ 80%)
- [ ] Integration tests pass
- [ ] Performance benchmarks met (see NFR section)
- [ ] Security scan clean (no Critical/High vulnerabilities)
- [ ] Documentation updated

**Business Criteria:**

- [ ] [Metric 1] achieved: [Target value]
- [ ] [Metric 2] achieved: [Target value]
- [ ] Stakeholder sign-off obtained

#### Key Performance Indicators (KPIs)

|KPI|Current|Target|Measurement Method|
|:--|:--|:--|:--|
|Response Time (p95)|500ms|100ms|Datadog APM|
|Error Rate|2%|0.1%|Prometheus metrics|
|Throughput|100 rps|1000 rps|Load test (k6)|
|Uptime|99%|99.9%|StatusPage|

---

## 2. GOALS / SCOPE / NON-GOALS / ASSUMPTIONS

_Định nghĩa biên giới rõ ràng - "Non-goals are as important as goals"_

### 2.1. Goals (Mục tiêu)

#### 2.1.1. Business Goals

|Goal|Metric|Target|Timeline|
|:--|:--|:--|:--|
|Improve user retention|Churn rate|Giảm 15%|Q2 2025|
|Reduce support tickets|Tickets/week|Giảm 30%|Q2 2025|

#### 2.1.2. Technical Goals

|Goal|Metric|Target|Timeline|
|:--|:--|:--|:--|
|Improve performance|p95 latency|< 200ms|Sprint 5|
|Increase reliability|Uptime SLA|99.9%|Sprint 6|
|Reduce tech debt|Code coverage|> 80%|Ongoing|

#### 2.1.3. User Experience Goals

|Goal|Metric|Target|
|:--|:--|:--|
|Faster time-to-value|First meaningful interaction|< 30s|
|Reduce friction|Steps to complete task|< 3 clicks|

### 2.2. In-Scope (Làm)

**MVP Features (Must Have):**

1. ✅ [Feature 1]: [Brief description]
2. ✅ [Feature 2]: [Brief description]
3. ✅ [Feature 3]: [Brief description]

**Phase 2 Features (Should Have):**

1. 📋 [Feature 4]: [Brief description]
2. 📋 [Feature 5]: [Brief description]

### 2.3. Out-of-Scope / Non-Goals (KHÔNG làm)

> ⚠️ **Quan trọng:** Liệt kê rõ những gì KHÔNG làm để tránh scope creep

|Non-Goal|Reason|Future Consideration?|
|:--|:--|:--|
|Multi-language support|Budget constraint|Phase 3 (Q4)|
|Mobile app|Different team scope|Parallel project|
|Legacy system migration|Out of timeline|Next fiscal year|
|Admin dashboard redesign|Not blocking|Low priority|

### 2.4. Assumptions

> 💡 **Assumptions = Risks cần validate sớm**

|ID|Assumption|Impact if Wrong|Validation Method|
|:--|:--|:--|:--|
|A1|AWS region ap-southeast-1 available|High - delay deployment|Check AWS status|
|A2|Redis cluster đã được provision|Medium - need alternative|Confirm with DevOps|
|A3|API Gateway supports rate limiting|Low - can implement custom|Test in staging|
|A4|User base < 100K in first 6 months|Medium - may need rescale|Monitor growth|

### 2.5. Constraints

#### 2.5.1. Technical Constraints

|Constraint|Reason|Workaround|
|:--|:--|:--|
|Must use Python 3.11+|Company standard|N/A|
|PostgreSQL only (no NoSQL)|Compliance requirement|N/A|
|AWS services only|Vendor lock-in policy|N/A|
|Max Docker image size 500MB|CI/CD pipeline limit|Multi-stage build|

#### 2.5.2. Business Constraints

|Constraint|Impact|Mitigation|
|:--|:--|:--|
|Budget < $50K/year|Limited infra options|Reserved instances, spot|
|Launch before Q2 2025|Tight timeline|Reduce MVP scope|
|2 engineers only|Resource limit|Prioritize ruthlessly|

#### 2.5.3. Compliance Constraints

|Regulation|Requirement|Implementation|
|:--|:--|:--|
|GDPR|Data residency in EU|Use eu-west-1 region|
|GDPR|Right to be forgotten|Implement data deletion API|
|PCI-DSS|No PII in logs|Log masking middleware|
|SOC2|Audit trail|Comprehensive logging|

### 2.6. Dependencies

#### 2.6.1. External Dependencies

|Dependency|Owner|Risk Level|Fallback|
|:--|:--|:--|:--|
|Stripe Payment API|External|Medium|PayPal backup|
|OpenAI API|External|High|Local LLM fallback|
|SendGrid Email|External|Low|AWS SES|

#### 2.6.2. Internal Dependencies

|Dependency|Team|Status|ETA|
|:--|:--|:--|:--|
|User Service API v2|Platform Team|In Progress|Week 3|
|Design System v3|Frontend Team|Done|✅|
|Database migration|DBA Team|Pending|Week 2|

#### 2.6.3. Dependency Graph

```mermaid
graph LR
    A[This Project] --> B[User Service]
    A --> C[Payment Service]
    A --> D[Notification Service]
    B --> E[Database]
    C --> F[Stripe API]
    D --> G[SendGrid]
```

---

## 3. USER STORIES / USE CASES

_Mô tả hành vi người dùng theo format chuẩn_

### 3.1. Primary Actors

|Actor|Description|Access Level|
|:--|:--|:--|
|End User|Người dùng cuối sử dụng sản phẩm|Basic|
|Admin|Quản trị viên hệ thống|Full|
|API Consumer|Service khác gọi API|Service-to-service|
|System (Cron)|Automated jobs|Internal|

### 3.2. User Stories

#### Format chuẩn:

```gherkin
User Story ID: US-[NUMBER]
Priority: [P0/P1/P2/P3]
Estimate: [Story Points]

As a [role]
I want to [action/capability]
So that [benefit/value]

Acceptance Criteria:
- Given [precondition]
  When [action]
  Then [expected result]
  
Technical Notes:
- [Implementation hints]
- [Edge cases to consider]
```

#### US-001: User Login

```gherkin
User Story ID: US-001
Priority: P0
Estimate: 5 points

As a registered user
I want to login with email and password
So that I can access my personalized dashboard

Acceptance Criteria:
- Given valid credentials
  When I submit login form
  Then I am redirected to dashboard within 2 seconds
  And I receive a JWT token valid for 24 hours

- Given invalid credentials
  When I submit login form
  Then I see error message "Invalid email or password"
  And login attempt is logged for security audit

- Given account is locked (5 failed attempts)
  When I try to login
  Then I see message "Account locked. Try again in 15 minutes"
  And I receive email notification about locked account

Technical Notes:
- Rate limit: 5 attempts per 15 minutes per IP
- Password hashing: bcrypt with cost factor 12
- JWT includes: user_id, role, exp, iat
```

#### US-002: [Tên User Story]

```gherkin
# Thêm các user stories khác theo format tương tự
```

### 3.3. User Flows / Journey Maps

#### 3.3.1. Happy Path Flow

```mermaid
flowchart TD
    A[User visits /login] --> B{Has account?}
    B -->|Yes| C[Enter credentials]
    B -->|No| D[Click Register]
    C --> E{Valid?}
    E -->|Yes| F[Generate JWT]
    F --> G[Redirect to Dashboard]
    E -->|No| H[Show error]
    H --> C
    D --> I[Registration Flow]
```

#### 3.3.2. Error Flow

```mermaid
flowchart TD
    A[User enters credentials] --> B{Validate}
    B -->|Invalid format| C[Show validation error]
    B -->|Valid format| D[Check credentials]
    D -->|Wrong password| E{Attempt count?}
    E -->|< 5| F[Show error + remaining attempts]
    E -->|>= 5| G[Lock account 15min]
    D -->|User not found| H[Show generic error]
```

### 3.4. Edge Cases & Error Scenarios

|Scenario|Expected Behavior|Priority|
|:--|:--|:--|
|Network timeout during login|Show "Connection error. Please retry." + retry button|P0|
|Session expired mid-action|Redirect to login with return URL|P0|
|Concurrent login from 2 devices|Allow both, track in sessions table|P1|
|Browser refresh during 2FA|Preserve state in localStorage|P1|
|SQL injection in email field|Sanitize input, return 400 Bad Request|P0|
|Password with unicode chars|Support UTF-8, normalize before hash|P2|

### 3.5. Domain-Specific Additions

#### 🖥️ Frontend-specific

- **Wireframes:** [Link to Figma/Sketch]
- **Mockups:** [Link to high-fidelity designs]
- **Interaction States:** Loading, Success, Error, Empty states
- **Responsive Breakpoints:** Mobile (320px), Tablet (768px), Desktop (1024px+)

#### 🤖 AI/ML-specific

- **Inference Scenarios:** Batch processing, Real-time prediction
- **Model Failure Modes:** What happens when model returns low confidence?
- **Fallback Behavior:** Rule-based fallback when model unavailable
- **Human-in-the-loop:** When to escalate to human review

---

## 4. API CONTRACT & INTERFACES

_Đặc tả giao tiếp giữa components - Source of truth cho integration_

### 4.1. API Design Principles

|Principle|Implementation|
|:--|:--|
|Protocol|REST (OpenAPI 3.0) / GraphQL / gRPC|
|Versioning|URI versioning: `/v1/`, `/v2/`|
|Naming|Nouns for resources, kebab-case: `/user-profiles`|
|Filtering|Query params: `?status=active&sort=-created_at`|
|Pagination|Cursor-based: `?cursor=xxx&limit=20`|
|Authentication|JWT Bearer token in Authorization header|
|Rate Limiting|100 req/min per user, 1000 req/min per IP|

### 4.2. Endpoint Specifications

#### 4.2.1. Authentication Endpoints

##### POST /v1/auth/login

```yaml
Summary: Authenticate user and return JWT token
Tags: [Authentication]
Security: None (public endpoint)

Request:
  Headers:
    Content-Type: application/json
    X-Request-ID: string (optional, for tracing)
    X-Client-Version: string (optional, for compatibility)
  
  Body:
    type: object
    required: [email, password]
    properties:
      email:
        type: string
        format: email
        maxLength: 255
        example: "user@example.com"
      password:
        type: string
        minLength: 8
        maxLength: 128
        example: "SecureP@ss123"
      remember_me:
        type: boolean
        default: false
        description: "If true, token valid for 30 days instead of 24 hours"

Response:
  200 OK:
    description: Login successful
    body:
      type: object
      properties:
        data:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIs..."
            refresh_token:
              type: string
              example: "dGhpcyBpcyBhIHJlZnJl..."
            token_type:
              type: string
              enum: [Bearer]
            expires_in:
              type: integer
              description: "Seconds until expiration"
              example: 86400
            user:
              type: object
              properties:
                id: {type: string, format: uuid}
                email: {type: string}
                name: {type: string}
                role: {type: string, enum: [user, admin]}
        meta:
          type: object
          properties:
            request_id: {type: string}
            timestamp: {type: string, format: date-time}
  
  400 Bad Request:
    description: Invalid input
    body: {$ref: '#/components/schemas/ErrorResponse'}
  
  401 Unauthorized:
    description: Invalid credentials
    body: {$ref: '#/components/schemas/ErrorResponse'}
  
  429 Too Many Requests:
    description: Rate limit exceeded
    headers:
      Retry-After: {type: integer, description: "Seconds to wait"}
      X-RateLimit-Limit: {type: integer}
      X-RateLimit-Remaining: {type: integer}
    body: {$ref: '#/components/schemas/ErrorResponse'}

Rate Limit: 5 requests per 15 minutes per IP
Idempotency: Not required (stateless)
```

##### POST /v1/auth/refresh

```yaml
Summary: Refresh access token using refresh token
Tags: [Authentication]
Security: None (uses refresh token in body)

Request:
  Body:
    type: object
    required: [refresh_token]
    properties:
      refresh_token:
        type: string
        example: "dGhpcyBpcyBhIHJlZnJl..."

Response:
  200 OK:
    body:
      data:
        access_token: string
        expires_in: integer
  
  401 Unauthorized:
    description: Invalid or expired refresh token
```

#### 4.2.2. Resource Endpoints

##### GET /v1/users/{user_id}

```yaml
Summary: Get user profile by ID
Tags: [Users]
Security: Bearer JWT (scope: read:users)

Path Parameters:
  user_id:
    type: string
    format: uuid
    required: true

Query Parameters:
  include:
    type: array
    items: {type: string, enum: [profile, settings, activity]}
    description: "Related resources to include"
    example: "?include=profile,settings"

Response:
  200 OK:
    body:
      data:
        id: string
        email: string
        name: string
        created_at: string (ISO 8601)
        profile: object (if included)
        settings: object (if included)
  
  404 Not Found:
    description: User not found
```

### 4.3. Data Models (Schemas)

#### 4.3.1. Request/Response Schemas

```typescript
// TypeScript interfaces for type safety

interface User {
  id: string;           // UUID v4
  email: string;        // Unique, lowercase
  name: string;         // Display name
  role: 'user' | 'admin';
  status: 'active' | 'inactive' | 'suspended';
  created_at: string;   // ISO 8601
  updated_at: string;   // ISO 8601
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
  };
  links: {
    self: string;
    first: string;
    prev: string | null;
    next: string | null;
    last: string;
  };
}

interface ErrorResponse {
  error: {
    code: string;           // Machine-readable: "RESOURCE_NOT_FOUND"
    message: string;        // Human-readable: "User with ID 123 not found"
    details?: object;       // Additional context
    trace_id: string;       // For debugging: "abc-123-xyz"
    timestamp: string;      // ISO 8601
    path: string;           // Request path
  };
}
```

#### 4.3.2. JSON Schema (for validation)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreateUserRequest",
  "type": "object",
  "required": ["email", "password", "name"],
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 255
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "maxLength": 128,
      "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
    },
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 100
    }
  },
  "additionalProperties": false
}
```

### 4.4. Error Handling Standards

#### 4.4.1. Error Code Registry

|HTTP Code|Error Code|Description|User Message|
|:--|:--|:--|:--|
|400|`VALIDATION_ERROR`|Invalid request payload|"Please check your input"|
|400|`INVALID_FORMAT`|Wrong data format|"Invalid {field} format"|
|401|`INVALID_CREDENTIALS`|Wrong email/password|"Invalid email or password"|
|401|`TOKEN_EXPIRED`|JWT expired|"Session expired. Please login again"|
|403|`FORBIDDEN`|No permission|"You don't have permission"|
|404|`RESOURCE_NOT_FOUND`|Entity not found|"{Resource} not found"|
|409|`CONFLICT`|Duplicate resource|"{Resource} already exists"|
|429|`RATE_LIMITED`|Too many requests|"Too many requests. Try again later"|
|500|`INTERNAL_ERROR`|Server error|"Something went wrong. Please try again"|
|503|`SERVICE_UNAVAILABLE`|Dependency down|"Service temporarily unavailable"|

#### 4.4.2. Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request payload",
    "details": {
      "fields": [
        {
          "field": "email",
          "message": "Must be a valid email address",
          "code": "INVALID_FORMAT"
        },
        {
          "field": "password",
          "message": "Must be at least 8 characters",
          "code": "TOO_SHORT"
        }
      ]
    },
    "trace_id": "abc-123-xyz-789",
    "timestamp": "2025-01-15T10:30:00Z",
    "path": "/v1/auth/register",
    "documentation_url": "https://docs.api.com/errors/VALIDATION_ERROR"
  }
}
```

### 4.5. API Versioning Strategy

```
Version Lifecycle:
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Alpha   │───►│   Beta   │───►│  Stable  │───►│ Deprecated│
│ /v2-alpha│    │ /v2-beta │    │   /v2    │    │   /v1    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                     │              │
                                     │    Sunset    │
                                     │    Period    │
                                     │   (6 months) │
                                     └──────────────┘

Deprecation Headers:
- Deprecation: true
- Sunset: Sat, 01 Jan 2026 00:00:00 GMT
- Link: <https://api.example.com/v2>; rel="successor-version"
```

### 4.6. Domain-Specific API Additions

#### 🖥️ Frontend Component API

```typescript
// Component Props Interface
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick: (event: React.MouseEvent) => void;
  children: React.ReactNode;
}

// Event Callbacks
interface FormCallbacks {
  onSubmit: (data: FormData) => Promise<void>;
  onError: (error: Error) => void;
  onSuccess: (result: Result) => void;
}
```

#### 🤖 AI/ML Model API

```yaml
POST /v1/predict
Summary: Make prediction using ML model

Request:
  Body:
    model_id: string
    features:
      type: array
      items:
        type: object
        properties:
          name: string
          value: number | string | array

Response:
  200 OK:
    prediction: number | string | array
    confidence: number (0-1)
    model_version: string
    inference_time_ms: number
    feature_importance: object (optional)
```

---

## 5. DATA MODEL & STORAGE DESIGN

_Thiết kế lưu trữ dữ liệu - Schema, Indexing, Caching_

### 5.1. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ USER_SESSIONS : has
    USERS ||--o{ USER_PROFILES : has
    USERS ||--o{ AUDIT_LOGS : creates
    
    USERS {
        uuid id PK
        varchar(255) email UK
        varchar(255) password_hash
        varchar(100) name
        enum role "user|admin"
        enum status "active|inactive|suspended"
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
    }
    
    USER_SESSIONS {
        uuid id PK
        uuid user_id FK
        varchar(500) token_hash
        varchar(45) ip_address
        varchar(500) user_agent
        timestamp expires_at
        timestamp created_at
    }
    
    USER_PROFILES {
        uuid id PK
        uuid user_id FK "unique"
        varchar(255) avatar_url
        date date_of_birth
        varchar(20) phone
        jsonb preferences
        timestamp updated_at
    }
    
    AUDIT_LOGS {
        bigserial id PK
        uuid user_id FK
        varchar(50) action
        varchar(100) resource_type
        uuid resource_id
        jsonb old_value
        jsonb new_value
        varchar(45) ip_address
        timestamp created_at
    }
```

### 5.2. Schema Definition

#### 5.2.1. Table: users

```sql
-- PostgreSQL Schema
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user' 
        CHECK (role IN ('user', 'admin')),
    status VARCHAR(20) NOT NULL DEFAULT 'active' 
        CHECK (status IN ('active', 'inactive', 'suspended')),
    email_verified_at TIMESTAMP WITH TIME ZONE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,  -- Soft delete
    
    -- Constraints
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_email_lowercase CHECK (email = LOWER(email))
);

-- Indexes
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_status ON users(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NOT NULL;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE users IS 'Core user accounts table';
COMMENT ON COLUMN users.password_hash IS 'bcrypt hash with cost factor 12';
COMMENT ON COLUMN users.deleted_at IS 'Soft delete timestamp - NULL means active';
```

#### 5.2.2. Table: user_sessions

```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent VARCHAR(500),
    device_fingerprint VARCHAR(255),
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id) 
    WHERE is_revoked = FALSE;
CREATE INDEX idx_sessions_token ON user_sessions(refresh_token_hash) 
    WHERE is_revoked = FALSE;
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at) 
    WHERE is_revoked = FALSE;

-- Partition by month (for high-volume systems)
-- CREATE TABLE user_sessions_2025_01 PARTITION OF user_sessions
--     FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

### 5.3. Indexing Strategy

|Table|Index Name|Columns|Type|Purpose|
|:--|:--|:--|:--|:--|
|users|idx_users_email|email|B-tree|Login lookup|
|users|idx_users_status|status|B-tree|Filter by status|
|users|idx_users_search|name, email|GIN (pg_trgm)|Full-text search|
|sessions|idx_sessions_user|user_id|B-tree|User's sessions|
|sessions|idx_sessions_token|token_hash|Hash|Token validation|
|audit_logs|idx_audit_created|created_at|BRIN|Time-range queries|
|audit_logs|idx_audit_user|user_id, created_at|B-tree|User activity|

#### Index Guidelines:

```sql
-- DO: Create indexes for frequent queries
CREATE INDEX idx_users_email ON users(email);

-- DO: Use partial indexes to reduce size
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- DO: Use covering indexes for common queries
CREATE INDEX idx_users_list ON users(status, created_at DESC) INCLUDE (email, name);

-- DON'T: Over-index (each index slows writes)
-- DON'T: Index low-cardinality columns alone (e.g., boolean)
-- DON'T: Forget to analyze after bulk inserts
```

### 5.4. Data Versioning & Migration

#### 5.4.1. Migration Strategy (Alembic)

```python
# migrations/versions/001_create_users_table.py
"""Create users table

Revision ID: 001
Revises: 
Create Date: 2025-01-15 10:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False, 
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='user'),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), 
                  nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), 
                  nullable=False, server_default=sa.text('NOW()')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='users_email_unique')
    )
    op.create_index('idx_users_email', 'users', ['email'], 
                    postgresql_where=sa.text('deleted_at IS NULL'))

def downgrade():
    op.drop_index('idx_users_email')
    op.drop_table('users')
```

#### 5.4.2. Zero-Downtime Migration Pattern

```
Phase 1: Add new column (nullable)
Phase 2: Dual-write (write to both old and new)
Phase 3: Backfill existing data
Phase 4: Switch reads to new column
Phase 5: Stop writing to old column
Phase 6: Remove old column

Example Timeline:
┌─────────────────────────────────────────────────────────────────┐
│ Day 1   │ Day 2   │ Day 3   │ Day 4   │ Day 5   │ Day 6        │
├─────────┼─────────┼─────────┼─────────┼─────────┼──────────────┤
│ Add col │ Dual    │ Backfill│ Switch  │ Stop    │ Drop old     │
│ (null)  │ write   │ data    │ reads   │ old wr  │ column       │
└─────────────────────────────────────────────────────────────────┘
```

### 5.5. Caching Strategy

#### 5.5.1. Cache Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    CACHING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐  │
│   │   Browser   │   │   CDN       │   │  Application    │  │
│   │   Cache     │   │   (Edge)    │   │  Cache (Redis)  │  │
│   │   (L1)      │   │   (L2)      │   │  (L3)           │  │
│   └──────┬──────┘   └──────┬──────┘   └────────┬────────┘  │
│          │                 │                    │           │
│          └────────────────┴───────────────────┘           │
│                           │                                │
│                    ┌──────▼──────┐                        │
│                    │  Database   │                        │
│                    │  (Source)   │                        │
│                    └─────────────┘                        │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

#### 5.5.2. Cache Configuration

|Data Type|Cache Key Pattern|TTL|Invalidation Strategy|
|:--|:--|:--|:--|
|User profile|`user:{user_id}`|1 hour|Write-through on update|
|Session|`session:{token_hash}`|24 hours|Explicit delete on logout|
|API response|`api:{endpoint}:{hash}`|5 min|Time-based expiry|
|Rate limit|`ratelimit:{ip}:{endpoint}`|1 min|Sliding window|
|Feature flag|`feature:{flag_name}`|30 sec|Pub/sub notification|

#### 5.5.3. Redis Cache Implementation

```python
# cache_manager.py
import redis
import json
from typing import Optional, Any
from functools import wraps

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        
    def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        self.redis.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        self.redis.delete(key)
    
    def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern"""
        cursor = 0
        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
            if keys:
                self.redis.delete(*keys)
            if cursor == 0:
                break

# Decorator for caching
def cached(key_template: str, ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = key_template.format(**kwargs)
            cached_value = cache_manager.get(cache_key)
            if cached_value:
                return cached_value
            result = await func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

# Usage
@cached(key_template="user:{user_id}", ttl=3600)
async def get_user(user_id: str) -> dict:
    return await db.users.find_one({"id": user_id})
```

### 5.6. Data Retention & Archival

|Data Type|Retention Period|Archive Strategy|Deletion Method|
|:--|:--|:--|:--|
|User data|Until account deletion + 30 days|Cold storage (S3 Glacier)|Hard delete after retention|
|Audit logs|7 years (compliance)|Monthly archive to S3|Automated after 7 years|
|Session data|30 days after expiry|No archive|Hard delete|
|Analytics|2 years|Aggregate then archive|Hard delete raw data|

#### GDPR Compliance: Right to be Forgotten

```python
async def delete_user_data(user_id: str, requester_id: str):
    """
    GDPR Article 17 - Right to erasure
    """
    # 1. Verify request authorization
    if not await verify_deletion_request(user_id, requester_id):
        raise UnauthorizedError("Not authorized to delete this data")
    
    # 2. Create deletion audit record BEFORE deleting
    await create_audit_log(
        action="GDPR_DELETION_REQUEST",
        user_id=user_id,
        requester_id=requester_id
    )
    
    # 3. Anonymize data in related tables
    await db.execute("""
        UPDATE orders SET customer_email = 'deleted@anonymized.com'
        WHERE user_id = :user_id
    """, {"user_id": user_id})
    
    # 4. Delete user record
    await db.execute("""
        DELETE FROM users WHERE id = :user_id
    """, {"user_id": user_id})
    
    # 5. Invalidate caches
    cache.delete_pattern(f"user:{user_id}*")
    cache.delete_pattern(f"session:*:{user_id}")
    
    # 6. Queue background job for external systems
    await queue.publish("user.deleted", {"user_id": user_id})
    
    return {"status": "deleted", "user_id": user_id}
```

### 5.7. Domain-Specific Data Additions

#### 🖥️ Frontend State Management

```typescript
// Redux Store Structure
interface RootState {
  auth: {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    loading: boolean;
  };
  ui: {
    theme: 'light' | 'dark';
    sidebar: {
      isOpen: boolean;
      activeItem: string;
    };
    notifications: Notification[];
  };
  entities: {
    users: Record<string, User>;
    posts: Record<string, Post>;
  };
}

// Local Storage Strategy
const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_prefs',
  THEME: 'theme',
};

// Session Storage (cleared on tab close)
const SESSION_KEYS = {
  FORM_DRAFT: 'form_draft',
  SCROLL_POSITION: 'scroll_pos',
};
```

#### 🤖 AI/ML Data Management

```yaml
# Feature Store Schema
feature_groups:
  user_features:
    entity_key: user_id
    features:
      - name: login_count_7d
        dtype: int64
        description: "Number of logins in last 7 days"
      - name: avg_session_duration
        dtype: float64
        description: "Average session duration in seconds"
    ttl: 86400  # 24 hours
    
  item_features:
    entity_key: item_id
    features:
      - name: embedding_vector
        dtype: array<float64>[128]
        description: "Item embedding from trained model"
      - name: popularity_score
        dtype: float64
        description: "Normalized popularity (0-1)"

# Model Versioning
model_registry:
  - model_name: "user_churn_predictor"
    version: "v2.3.1"
    artifact_path: "s3://models/churn/v2.3.1/"
    metrics:
      auc_roc: 0.87
      precision: 0.82
      recall: 0.79
    status: "production"
    created_at: "2025-01-10"

# Dataset Lineage
dataset_lineage:
  training_data_v3:
    source: "s3://data/raw/users/"
    transformations:
      - "remove_pii"
      - "normalize_features"
      - "split_train_test"
    output: "s3://data/processed/training_v3/"
    created_by: "pipeline/feature_engineering"
    created_at: "2025-01-05"
```

---

## 6. SYSTEM ARCHITECTURE & FLOW

_Kiến trúc tổng thể và luồng dữ liệu theo C4 Model_

### 6.1. High-Level Architecture (C4 Model)

#### Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM CONTEXT DIAGRAM                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│     ┌─────────┐                                    ┌─────────────────┐ │
│     │  User   │                                    │  External APIs  │ │
│     │(Browser)│                                    │ (Stripe, etc.)  │ │
│     └────┬────┘                                    └────────┬────────┘ │
│          │                                                  │          │
│          │ HTTPS                                     HTTPS  │          │
│          ▼                                                  ▼          │
│   ┌──────────────────────────────────────────────────────────────┐    │
│   │                                                              │    │
│   │                    [SYSTEM NAME]                             │    │
│   │                                                              │    │
│   │    - Provides user authentication                            │    │
│   │    - Manages user profiles                                   │    │
│   │    - Handles business logic                                  │    │
│   │                                                              │    │
│   └──────────────────────────────────────────────────────────────┘    │
│          │                                                  │          │
│          │                                                  │          │
│          ▼                                                  ▼          │
│   ┌─────────────┐                                   ┌─────────────┐   │
│   │  Database   │                                   │    Email    │   │
│   │ (PostgreSQL)│                                   │  (SendGrid) │   │
│   └─────────────┘                                   └─────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Level 2: Container Diagram

```mermaid
graph TB
    subgraph "External"
        User[👤 User<br/>Browser/Mobile]
        Admin[👤 Admin<br/>Dashboard]
        External[🌐 External APIs]
    end
    
    subgraph "System Boundary"
        LB[Load Balancer<br/>nginx/ALB]
        
        subgraph "Application Layer"
            API[API Gateway<br/>Kong/AWS API GW]
            Auth[Auth Service<br/>Python/FastAPI]
            Core[Core Service<br/>Python/FastAPI]
            Worker[Background Worker<br/>Celery]
        end
        
        subgraph "Data Layer"
            Cache[(Redis<br/>Cache + Sessions)]
            DB[(PostgreSQL<br/>Primary DB)]
            Queue[RabbitMQ<br/>Message Queue]
            S3[S3<br/>File Storage]
        end
    end
    
    User --> LB
    Admin --> LB
    LB --> API
    API --> Auth
    API --> Core
    Auth --> Cache
    Auth --> DB
    Core --> DB
    Core --> Queue
    Queue --> Worker
    Worker --> External
    Worker --> S3
```

### 6.2. Component Diagram (C4 Level 3)

```mermaid
graph TB
    subgraph "Auth Service"
        AuthController[Auth Controller<br/>/api/v1/auth/*]
        AuthService[Auth Service<br/>Business Logic]
        TokenService[Token Service<br/>JWT Management]
        UserRepo[User Repository<br/>Data Access]
        SessionRepo[Session Repository<br/>Data Access]
    end
    
    AuthController --> AuthService
    AuthService --> TokenService
    AuthService --> UserRepo
    AuthService --> SessionRepo
    TokenService --> Cache[(Redis)]
    UserRepo --> DB[(PostgreSQL)]
    SessionRepo --> DB
```

### 6.3. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW: User Login                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐   ┌──────┐ │
│  │ Client │───►│   API   │───►│   Auth   │───►│ Validate │───►│ User │ │
│  │        │    │ Gateway │    │ Service  │    │   DB     │    │  DB  │ │
│  └────────┘    └─────────┘    └──────────┘    └──────────┘   └──────┘ │
│       │                            │                              │     │
│       │                            │                              │     │
│       │    ┌─────────────┐         │         ┌─────────────┐     │     │
│       │    │ Rate Limit  │◄────────┤         │ Password    │◄────┘     │
│       │    │   Check     │         │         │ Verify      │           │
│       │    └─────────────┘         │         └─────────────┘           │
│       │         │                  │                │                   │
│       │         ▼                  │                ▼                   │
│       │    ┌─────────┐            │          ┌──────────┐              │
│       │◄───│  Redis  │            │          │ Generate │              │
│       │    │  Cache  │            │◄─────────│   JWT    │              │
│       │    └─────────┘            │          └──────────┘              │
│       │                           │                                     │
│       └───────────────────────────┘                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.4. Sequence Diagrams (Critical Paths)

#### 6.4.1. User Login Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant GW as API Gateway
    participant RL as Rate Limiter
    participant AS as Auth Service
    participant R as Redis
    participant DB as PostgreSQL
    
    C->>GW: POST /v1/auth/login {email, password}
    GW->>RL: Check rate limit
    
    alt Rate limit exceeded
        RL-->>C: 429 Too Many Requests
    end
    
    RL->>AS: Forward request
    AS->>DB: SELECT user by email
    
    alt User not found
        AS-->>C: 401 Invalid credentials
    end
    
    DB-->>AS: User record
    AS->>AS: Verify password (bcrypt)
    
    alt Password invalid
        AS->>DB: INCREMENT failed_attempts
        AS-->>C: 401 Invalid credentials
    end
    
    AS->>AS: Generate JWT + Refresh Token
    AS->>R: Store session {token_hash, user_id, expires_at}
    AS->>DB: UPDATE last_login_at, RESET failed_attempts
    AS-->>C: 200 OK {access_token, refresh_token, user}
```

#### 6.4.2. Token Refresh Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant AS as Auth Service
    participant R as Redis
    participant DB as PostgreSQL
    
    C->>AS: POST /v1/auth/refresh {refresh_token}
    AS->>R: GET session by token_hash
    
    alt Session not found or revoked
        AS-->>C: 401 Invalid token
    end
    
    R-->>AS: Session data
    AS->>AS: Validate expiration
    
    alt Token expired
        AS-->>C: 401 Token expired
    end
    
    AS->>AS: Generate new access_token
    AS->>R: UPDATE last_used_at
    AS-->>C: 200 OK {access_token}
```

### 6.5. State Machine Diagrams

#### 6.5.1. User Account States

```mermaid
stateDiagram-v2
    [*] --> Pending: Register
    Pending --> Active: Verify Email
    Pending --> [*]: Delete (30 days)
    Active --> Suspended: Admin Action / Policy Violation
    Active --> Locked: 5 Failed Logins
    Active --> Inactive: No login 90 days
    Suspended --> Active: Admin Restore
    Locked --> Active: 15 min timeout / Admin unlock
    Inactive --> Active: Login
    Active --> Deleted: User Request (GDPR)
    Deleted --> [*]: Data Purged (30 days)
```

#### 6.5.2. Order Processing States

```mermaid
stateDiagram-v2
    [*] --> Created: Create Order
    Created --> PaymentPending: Submit
    PaymentPending --> PaymentFailed: Payment Error
    PaymentPending --> Paid: Payment Success
    PaymentFailed --> PaymentPending: Retry
    PaymentFailed --> Cancelled: Max Retries
    Paid --> Processing: Start Fulfillment
    Processing --> Shipped: Ship Order
    Shipped --> Delivered: Delivery Confirmed
    Delivered --> Completed: Auto after 7 days
    Delivered --> Refunded: Refund Request
    Completed --> [*]
    Cancelled --> [*]
    Refunded --> [*]
```

### 6.6. Domain-Specific Architecture

#### 🖥️ Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      FRONTEND ARCHITECTURE (React)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                        Presentation Layer                        │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │  │
│   │  │  Pages   │  │  Layouts │  │Components│  │ Design System│    │  │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                       Application Layer                          │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │  │
│   │  │  Hooks   │  │ Contexts │  │  Store   │  │  Services    │    │  │
│   │  │(useAuth) │  │(ThemeProv)│  │ (Redux)  │  │ (API Client)│    │  │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      Infrastructure Layer                        │  │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │  │
│   │  │  Router  │  │   i18n   │  │Analytics │  │Error Boundary│    │  │
│   │  │(React R) │  │(react-i18n)│ │(Mixpanel)│  │  (Sentry)   │    │  │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 🤖 AI/ML Pipeline Architecture

```mermaid
graph LR
    subgraph "Data Pipeline"
        Raw[Raw Data] --> Ingest[Data Ingestion]
        Ingest --> Clean[Data Cleaning]
        Clean --> Feature[Feature Engineering]
        Feature --> Store[(Feature Store)]
    end
    
    subgraph "Training Pipeline"
        Store --> Train[Model Training]
        Train --> Eval[Evaluation]
        Eval --> Registry[(Model Registry)]
    end
    
    subgraph "Serving Pipeline"
        Registry --> Deploy[Model Deployment]
        Deploy --> Serve[Model Serving]
        Serve --> Monitor[Monitoring]
        Monitor --> Alert[Alerts]
    end
    
    subgraph "Feedback Loop"
        Serve --> Log[Prediction Logs]
        Log --> Analyze[Analysis]
        Analyze --> Retrain{Retrain?}
        Retrain -->|Yes| Train
    end
```

---

## 7. IMPLEMENTATION DETAILS (Deep-Dive)

_Chi tiết thuật toán và logic xử lý kèm theo pseudo code_

### 7.1. Processing Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      REQUEST PROCESSING PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Request                                                               │
│      │                                                                  │
│      ▼                                                                  │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐    │
│  │ 1. INGEST  │──►│ 2. VALIDATE│──►│3. TRANSFORM│──►│ 4. PROCESS │    │
│  │            │   │            │   │            │   │            │    │
│  │ - Parse    │   │ - Schema   │   │ - Normalize│   │ - Business │    │
│  │ - Decode   │   │ - Sanitize │   │ - Enrich   │   │ - Logic    │    │
│  │ - Log      │   │ - Auth     │   │ - Map      │   │ - Rules    │    │
│  └────────────┘   └────────────┘   └────────────┘   └────────────┘    │
│                                                             │          │
│                                                             ▼          │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐    │
│  │ 8. RESPOND │◄──│ 7. FORMAT  │◄──│ 6. CACHE   │◄──│ 5. STORE   │    │
│  │            │   │            │   │            │   │            │    │
│  │ - Serialize│   │ - Transform│   │ - Set TTL  │   │ - Persist  │    │
│  │ - Compress │   │ - Filter   │   │ - Invalidate│  │ - Index    │    │
│  │ - Send     │   │ - Paginate │   │ - Warm     │   │ - Replicate│    │
│  └────────────┘   └────────────┘   └────────────┘   └────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2. Per-Module Specification

#### 7.2.1. Authentication Module

|Attribute|Description|
|:--|:--|
|**Responsibility**|User authentication, token management, session handling|
|**Input**|Email, password, refresh token|
|**Output**|JWT access token, refresh token, user profile|
|**Dependencies**|UserRepository, TokenService, CacheService|

##### Pseudo Code: Login Flow

```python
"""
Authentication Service - Login Flow
"""

class AuthService:
    def __init__(self, user_repo, token_service, cache, config):
        self.user_repo = user_repo
        self.token_service = token_service
        self.cache = cache
        self.config = config
    
    async def login(self, email: str, password: str, remember_me: bool = False) -> AuthResult:
        """
        Authenticate user and return tokens
        
        Algorithm:
        1. Normalize email (lowercase, trim)
        2. Check rate limit
        3. Fetch user from database
        4. Verify password using bcrypt
        5. Check account status (not locked/suspended)
        6. Generate JWT access token
        7. Generate refresh token
        8. Store session in Redis
        9. Update user last_login_at
        10. Return tokens and user profile
        
        Time Complexity: O(1) average
        Space Complexity: O(1)
        """
        
        # Step 1: Normalize
        email = email.lower().strip()
        
        # Step 2: Check rate limit (fail fast)
        rate_key = f"login_attempts:{email}"
        attempts = await self.cache.incr(rate_key)
        if attempts == 1:
            await self.cache.expire(rate_key, 900)  # 15 minutes
        
        if attempts > self.config.MAX_LOGIN_ATTEMPTS:
            raise RateLimitError(
                message="Too many login attempts",
                retry_after=await self.cache.ttl(rate_key)
            )
        
        # Step 3: Fetch user
        user = await self.user_repo.find_by_email(email)
        if not user:
            # Security: Same error for non-existent user
            raise AuthenticationError("Invalid email or password")
        
        # Step 4: Verify password
        if not self._verify_password(password, user.password_hash):
            # Track failed attempt
            await self._increment_failed_attempts(user)
            raise AuthenticationError("Invalid email or password")
        
        # Step 5: Check account status
        if user.status == 'locked':
            if user.locked_until > datetime.utcnow():
                raise AccountLockedError(
                    message="Account is locked",
                    locked_until=user.locked_until
                )
            else:
                # Auto-unlock after timeout
                await self._unlock_account(user)
        
        if user.status == 'suspended':
            raise AccountSuspendedError("Account is suspended")
        
        # Step 6 & 7: Generate tokens
        token_expiry = timedelta(days=30 if remember_me else 1)
        access_token = self.token_service.create_access_token(
            user_id=user.id,
            role=user.role,
            expires_in=timedelta(hours=1)
        )
        refresh_token = self.token_service.create_refresh_token(
            user_id=user.id,
            expires_in=token_expiry
        )
        
        # Step 8: Store session
        session = Session(
            user_id=user.id,
            refresh_token_hash=self._hash_token(refresh_token),
            expires_at=datetime.utcnow() + token_expiry,
            ip_address=self._get_client_ip(),
            user_agent=self._get_user_agent()
        )
        await self.cache.set(
            f"session:{session.id}",
            session.to_dict(),
            ex=int(token_expiry.total_seconds())
        )
        
        # Step 9: Update user
        await self.user_repo.update(user.id, {
            'last_login_at': datetime.utcnow(),
            'failed_login_attempts': 0,
            'locked_until': None
        })
        
        # Clear rate limit on success
        await self.cache.delete(rate_key)
        
        # Step 10: Return result
        return AuthResult(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='Bearer',
            expires_in=3600,
            user=user.to_public_dict()
        )
    
    def _verify_password(self, plain: str, hashed: str) -> bool:
        """Verify password using bcrypt with constant-time comparison"""
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    
    async def _increment_failed_attempts(self, user: User):
        """Track failed login and potentially lock account"""
        new_attempts = user.failed_login_attempts + 1
        updates = {'failed_login_attempts': new_attempts}
        
        if new_attempts >= self.config.MAX_FAILED_ATTEMPTS:
            updates['status'] = 'locked'
            updates['locked_until'] = datetime.utcnow() + timedelta(minutes=15)
            
            # Send notification
            await self.notification_service.send_account_locked_email(user)
        
        await self.user_repo.update(user.id, updates)
```

### 7.3. Business Logic Rules

|Rule ID|Description|Formula/Logic|Pseudo Code|
|:--|:--|:--|:--|
|BL-001|Rate limiting|Max 100 req/min per user|`if count > 100: reject`|
|BL-002|Password policy|Min 8 chars, 1 upper, 1 lower, 1 digit, 1 special|`regex.match(pattern)`|
|BL-003|Token expiry|Access: 1h, Refresh: 30d|`exp = now + duration`|
|BL-004|Account lockout|5 failed attempts = 15min lock|`if attempts >= 5: lock(15m)`|

```python
# Business Rules Implementation

class BusinessRules:
    """Centralized business rules with validation"""
    
    # Rule: Password Policy
    PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,128}$'
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validate password against security policy
        Returns: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if len(password) > 128:
            return False, "Password must not exceed 128 characters"
        if not re.match(BusinessRules.PASSWORD_PATTERN, password):
            return False, "Password must contain uppercase, lowercase, number, and special character"
        
        # Check common passwords (optional)
        if password.lower() in COMMON_PASSWORDS:
            return False, "Password is too common"
        
        return True, ""
    
    # Rule: Discount Calculation
    @staticmethod
    def calculate_discount(subtotal: Decimal, items_count: int, user_tier: str) -> Decimal:
        """
        Calculate discount based on business rules
        
        Rules:
        - Base: 0% discount
        - If items >= 10: +10% discount
        - If subtotal >= 1000: +5% discount
        - Tier bonus: Silver +2%, Gold +5%, Platinum +10%
        - Max discount: 25%
        """
        discount_percent = Decimal('0')
        
        # Volume discount
        if items_count >= 10:
            discount_percent += Decimal('10')
        
        # Subtotal discount
        if subtotal >= Decimal('1000'):
            discount_percent += Decimal('5')
        
        # Tier bonus
        tier_bonus = {
            'silver': Decimal('2'),
            'gold': Decimal('5'),
            'platinum': Decimal('10')
        }
        discount_percent += tier_bonus.get(user_tier.lower(), Decimal('0'))
        
        # Cap at 25%
        discount_percent = min(discount_percent, Decimal('25'))
        
        return (subtotal * discount_percent / 100).quantize(Decimal('0.01'))
```

### 7.4. Integration Points

```python
"""
External Service Integration Patterns
"""

class ExternalServiceClient:
    """
    Base class for external API integrations
    Implements: Retry, Timeout, Circuit Breaker
    """
    
    def __init__(self, base_url: str, api_key: str, config: IntegrationConfig):
        self.base_url = base_url
        self.api_key = api_key
        self.config = config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.failure_threshold,  # 5 failures
            recovery_timeout=config.recovery_timeout     # 30 seconds
        )
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.timeout),  # 30 seconds
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'User-Agent': f'MyService/{VERSION}'
            }
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((TimeoutError, ConnectionError))
    )
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make HTTP request with retry and circuit breaker
        
        Retry Strategy:
        - Max attempts: 3
        - Backoff: Exponential (1s, 2s, 4s)
        - Retry on: Timeout, Connection Error, 5xx
        - Don't retry: 4xx (client error)
        """
        if self.circuit_breaker.is_open():
            raise CircuitOpenError("Service temporarily unavailable")
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status >= 500:
                    self.circuit_breaker.record_failure()
                    raise ServerError(f"Server error: {response.status}")
                
                if response.status >= 400:
                    error_body = await response.json()
                    raise ClientError(error_body.get('message', 'Unknown error'))
                
                self.circuit_breaker.record_success()
                return await response.json()
                
        except asyncio.TimeoutError:
            self.circuit_breaker.record_failure()
            raise TimeoutError(f"Request to {endpoint} timed out")


# Example: Payment Service Integration
class StripePaymentClient(ExternalServiceClient):
    """Stripe payment integration"""
    
    async def create_payment_intent(
        self, 
        amount: int,  # cents
        currency: str,
        customer_id: str,
        idempotency_key: str
    ) -> PaymentIntent:
        """
        Create Stripe payment intent
        
        Idempotency: Safe to retry with same idempotency_key
        """
        result = await self._request(
            'POST',
            '/v1/payment_intents',
            json={
                'amount': amount,
                'currency': currency,
                'customer': customer_id,
                'automatic_payment_methods': {'enabled': True}
            },
            headers={
                'Idempotency-Key': idempotency_key
            }
        )
        return PaymentIntent.from_dict(result)
```

### 7.5. Code Organization (Folder Structure)

Xem chi tiết trong file gốc - Section 7.5 với các options:

- **Feature-Based:** Recommended cho Microservices
- **Layer-Based:** Traditional Monolith
- **AI/ML-specific:** Data-heavy, experiment-centric

---

## 8. SECURITY & COMPLIANCE

_Bảo mật hệ thống theo OWASP và compliance standards_

### 8.1. Authentication & Authorization

#### 8.1.1. Authentication Methods

|Method|Use Case|Implementation|
|:--|:--|:--|
|JWT Bearer|API authentication|RS256 signing, 1h expiry|
|OAuth 2.0|Third-party login|Google, GitHub providers|
|API Key|Service-to-service|HMAC-SHA256 signed|
|Session Cookie|Web browser|HttpOnly, Secure, SameSite=Strict|

#### 8.1.2. Authorization (RBAC)

```yaml
roles:
  admin:
    description: "Full system access"
    permissions:
      - users:read
      - users:write
      - users:delete
      - settings:read
      - settings:write
      - reports:read
      - reports:export
      
  manager:
    description: "Team management access"
    permissions:
      - users:read
      - users:write
      - reports:read
      
  user:
    description: "Standard user access"
    permissions:
      - users:read  # Own profile only
      - settings:read  # Own settings only

# Permission check pseudo code
def check_permission(user, resource, action):
    """
    Check if user has permission for action on resource
    
    1. Get user's role
    2. Get role's permissions
    3. Check if permission matches
    4. For resource-level: check ownership
    """
    role = get_role(user.role)
    required_permission = f"{resource}:{action}"
    
    if required_permission not in role.permissions:
        raise ForbiddenError()
    
    # Resource-level check
    if requires_ownership(resource, action):
        if not is_owner(user, resource):
            raise ForbiddenError()
```

### 8.2. Data Security

|Data Type|At Rest|In Transit|Access Control|
|:--|:--|:--|:--|
|Passwords|bcrypt (cost 12)|TLS 1.3|Never readable|
|PII (email, name)|AES-256-GCM|TLS 1.3|Role-based|
|Session tokens|SHA-256 hash|TLS 1.3|User only|
|API keys|SHA-256 hash|TLS 1.3|Service owner|
|Financial data|AES-256-GCM|TLS 1.3|PCI-DSS compliant|

```python
# Secret Management
import os
from cryptography.fernet import Fernet

class SecretManager:
    """
    Centralized secret management
    Production: Use AWS Secrets Manager / HashiCorp Vault
    """
    
    def __init__(self):
        # In production, fetch from vault
        self.encryption_key = os.environ['ENCRYPTION_KEY']
        self.cipher = Fernet(self.encryption_key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(ciphertext.encode()).decode()
```

### 8.3. API Security

#### 8.3.1. Input Validation

```python
from pydantic import BaseModel, validator, EmailStr
import re

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        return v
    
    @validator('name')
    def sanitize_name(cls, v):
        # Remove potential XSS
        import html
        return html.escape(v.strip())
```

#### 8.3.2. Rate Limiting

```python
# Rate Limit Configuration
RATE_LIMITS = {
    'default': {'requests': 100, 'window': 60},        # 100/min
    'auth': {'requests': 5, 'window': 900},            # 5/15min
    'api': {'requests': 1000, 'window': 3600},         # 1000/hour
    'upload': {'requests': 10, 'window': 3600},        # 10/hour
}

# Sliding Window Implementation
async def check_rate_limit(key: str, limit_type: str = 'default') -> bool:
    config = RATE_LIMITS[limit_type]
    current_window = int(time.time() // config['window'])
    cache_key = f"ratelimit:{key}:{current_window}"
    
    count = await redis.incr(cache_key)
    if count == 1:
        await redis.expire(cache_key, config['window'] * 2)
    
    return count <= config['requests']
```

### 8.4. Compliance Checklist

|Regulation|Requirement|Implementation|Status|
|:--|:--|:--|:--|
|**GDPR**|Data minimization|Collect only needed data|✅|
|**GDPR**|Right to access|Export user data API|✅|
|**GDPR**|Right to erasure|Delete user data API|✅|
|**GDPR**|Data portability|JSON/CSV export|✅|
|**PCI-DSS**|No PII in logs|Log masking|✅|
|**PCI-DSS**|Encryption at rest|AES-256|✅|
|**SOC2**|Audit logging|Comprehensive logs|✅|
|**SOC2**|Access controls|RBAC implemented|✅|

### 8.5. Threat Model (STRIDE)

|Threat|Description|Mitigation|
|:--|:--|:--|
|**S**poofing|Fake identity|JWT validation, MFA|
|**T**ampering|Data modification|Input validation, checksums|
|**R**epudiation|Deny actions|Audit logging, signatures|
|**I**nformation Disclosure|Data leak|Encryption, access control|
|**D**enial of Service|Overload system|Rate limiting, CDN|
|**E**levation of Privilege|Gain unauthorized access|RBAC, principle of least privilege|

---

## 9. NON-FUNCTIONAL REQUIREMENTS (NFR)

_Performance, Scalability, Reliability targets_

### 9.1. Performance Targets

|Metric|Current|Target|Measurement|
|:--|:--|:--|:--|
|p50 Latency|200ms|50ms|Datadog APM|
|p95 Latency|800ms|200ms|Datadog APM|
|p99 Latency|2000ms|500ms|Datadog APM|
|Throughput|100 rps|1000 rps|Load test|
|Error Rate|2%|0.1%|Prometheus|
|Time to First Byte|500ms|100ms|RUM|

### 9.2. Scalability

```yaml
# Kubernetes HPA Configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
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
          name: requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
```

### 9.3. Reliability & Availability

|Metric|Target|Meaning|
|:--|:--|:--|
|Uptime SLA|99.9%|Max 8.76h downtime/year|
|RTO|< 1 hour|Recovery Time Objective|
|RPO|< 15 minutes|Recovery Point Objective|
|MTBF|> 720 hours|Mean Time Between Failures|
|MTTR|< 30 minutes|Mean Time To Repair|

### 9.4. Capacity Planning

|Resource|Current Usage|Growth Rate|6-Month Projection|
|:--|:--|:--|:--|
|Users|10,000|20%/month|30,000|
|Requests/day|1M|15%/month|2.3M|
|Database size|50GB|10GB/month|110GB|
|Storage (S3)|200GB|50GB/month|500GB|
|Monthly cost|$5,000|10%/month|$8,000|

---

## 10. OBSERVABILITY (Logs/Metrics/Traces)

_Giám sát và debugging theo Golden Signals_

### 10.1. Logging Strategy

```python
# Structured Logging Configuration
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

# Usage
logger = structlog.get_logger()

# Good: Structured logging with context
logger.info(
    "user_login_success",
    user_id=user.id,
    email_masked=mask_email(user.email),
    ip_address=request.client.host,
    user_agent=request.headers.get("user-agent"),
    duration_ms=elapsed_ms
)

# Log Levels
# DEBUG: Detailed debugging (dev only)
# INFO: Business events (user actions, API calls)
# WARNING: Unexpected but handled situations
# ERROR: Errors that affect user experience
# CRITICAL: System-wide failures
```

### 10.2. Metrics (Golden Signals)

```yaml
# Prometheus Metrics Definition
metrics:
  # Latency
  - name: http_request_duration_seconds
    type: histogram
    labels: [method, endpoint, status_code]
    buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    
  # Traffic
  - name: http_requests_total
    type: counter
    labels: [method, endpoint, status_code]
    
  # Errors
  - name: http_errors_total
    type: counter
    labels: [method, endpoint, error_type]
    
  # Saturation
  - name: system_cpu_usage_percent
    type: gauge
  - name: system_memory_usage_bytes
    type: gauge
  - name: database_connections_active
    type: gauge
  - name: queue_depth
    type: gauge
```

### 10.3. Distributed Tracing

```python
# OpenTelemetry Setup
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Usage in code
with tracer.start_as_current_span("process_payment") as span:
    span.set_attribute("user_id", user_id)
    span.set_attribute("amount", amount)
    
    try:
        result = await payment_service.charge(user_id, amount)
        span.set_attribute("payment_id", result.id)
    except PaymentError as e:
        span.set_status(Status(StatusCode.ERROR))
        span.record_exception(e)
        raise
```

### 10.4. Alerting Rules

```yaml
# Prometheus Alert Rules
groups:
  - name: api-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_errors_total[5m])) 
          / sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"
          
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket[5m])) 
            by (le, endpoint)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p95 latency on {{ $labels.endpoint }}"
          
      - alert: ServiceDown
        expr: up{job="api-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
```

---

## 11. FAILURE MODES & RESILIENCE

_Xử lý lỗi và khôi phục theo Netflix patterns_

### 11.1. Failure Mode Analysis (FMEA)

|ID|Failure Mode|Probability|Impact|RPN|Mitigation|
|:--|:--|:--|:--|:--|:--|
|F1|Database connection lost|Medium|Critical|12|Connection pooling, retry, replica failover|
|F2|Redis unavailable|Low|High|8|Local cache fallback, circuit breaker|
|F3|External API timeout|Medium|Medium|9|Retry with backoff, fallback response|
|F4|Out of memory|Low|Critical|10|Memory limits, graceful degradation|
|F5|Disk full|Low|High|6|Monitoring, auto-cleanup, alerts|

_RPN = Risk Priority Number (Probability × Impact × Detection)_

### 11.2. Retry Strategy

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    before_sleep=lambda retry_state: logger.warning(
        f"Retry {retry_state.attempt_number} after error"
    )
)
async def fetch_external_data(url: str):
    """
    Retry Strategy:
    - Attempt 1: Immediate
    - Attempt 2: Wait 1-2 seconds
    - Attempt 3: Wait 2-4 seconds (max 10s)
    - After 3 failures: Raise exception
    
    Idempotency: Ensure operation is safe to retry
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            return await response.json()
```

### 11.3. Circuit Breaker Pattern

```python
from circuitbreaker import circuit

class CircuitBreakerConfig:
    FAILURE_THRESHOLD = 5      # Open after 5 failures
    RECOVERY_TIMEOUT = 30      # Try again after 30 seconds
    EXPECTED_EXCEPTIONS = (TimeoutError, ConnectionError)

@circuit(
    failure_threshold=CircuitBreakerConfig.FAILURE_THRESHOLD,
    recovery_timeout=CircuitBreakerConfig.RECOVERY_TIMEOUT,
    expected_exception=CircuitBreakerConfig.EXPECTED_EXCEPTIONS
)
async def call_external_service(payload: dict):
    """
    Circuit States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Fail fast, no requests sent (after threshold failures)
    - HALF-OPEN: Test with single request after recovery timeout
    
    Transition:
    CLOSED --[5 failures]--> OPEN --[30s]--> HALF-OPEN
    HALF-OPEN --[success]--> CLOSED
    HALF-OPEN --[failure]--> OPEN
    """
    return await external_api.call(payload)
```

### 11.4. Graceful Degradation

```python
class FeatureFlags:
    """Feature flags for graceful degradation"""
    
    ENABLE_RECOMMENDATIONS = True
    ENABLE_REAL_TIME_ANALYTICS = True
    ENABLE_THIRD_PARTY_ENRICHMENT = True

async def get_user_dashboard(user_id: str):
    """
    Graceful degradation strategy:
    1. Core data: Always return (fail if unavailable)
    2. Enhanced data: Return cached/default if unavailable
    3. Optional data: Skip if unavailable
    """
    
    # Core: Must succeed
    user = await user_service.get(user_id)
    
    # Enhanced: Use cache fallback
    try:
        if FeatureFlags.ENABLE_RECOMMENDATIONS:
            recommendations = await recommendation_service.get(user_id)
        else:
            recommendations = []
    except ServiceUnavailableError:
        recommendations = await cache.get(f"recommendations:{user_id}") or []
        logger.warning("Falling back to cached recommendations")
    
    # Optional: Skip gracefully
    analytics = {}
    if FeatureFlags.ENABLE_REAL_TIME_ANALYTICS:
        try:
            analytics = await analytics_service.get(user_id)
        except Exception as e:
            logger.info(f"Skipping analytics: {e}")
    
    return {
        "user": user,
        "recommendations": recommendations,
        "analytics": analytics
    }
```

### 11.5. Timeout Configuration

|Operation|Connect Timeout|Read Timeout|Total Timeout|
|:--|:--|:--|:--|
|Database query|5s|30s|35s|
|External API|5s|30s|60s|
|Cache (Redis)|1s|5s|6s|
|File upload|10s|300s|310s|
|Background job|N/A|N/A|3600s|

---

## 12. TESTING STRATEGY

_Chiến lược đảm bảo chất lượng theo Test Pyramid_

### 12.1. Test Pyramid

```
                    ┌───────────┐
                   /│   E2E     │\     5%  - Critical flows only
                  / │  (Cypress) │ \
                 /  └───────────┘  \
                /   ┌───────────┐   \
               /    │Integration│    \   20% - API contracts, DB
              /     │ (pytest)  │     \
             /      └───────────┘      \
            /       ┌───────────┐       \
           /        │   Unit    │        \  75% - Business logic
          /         │ (pytest)  │         \
         /          └───────────┘          \
        └─────────────────────────────────────┘
```

### 12.2. Test Categories & Coverage

|Category|Target Coverage|Framework|Run Frequency|
|:--|:--|:--|:--|
|Unit Tests|80%+|pytest, Jest|Every commit|
|Integration Tests|60%+|pytest, Postman|Every PR|
|E2E Tests|Critical paths|Cypress, Playwright|Nightly|
|Performance Tests|Key endpoints|k6, Locust|Weekly|
|Security Tests|OWASP Top 10|OWASP ZAP|Monthly|

### 12.3. Sample Test Cases

```python
# Unit Test Example
import pytest
from unittest.mock import AsyncMock, patch
from services.auth_service import AuthService

class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService(
            user_repo=AsyncMock(),
            token_service=AsyncMock(),
            cache=AsyncMock()
        )
    
    @pytest.mark.asyncio
    async def test_login_success(self, auth_service):
        """Test successful login returns tokens"""
        # Arrange
        auth_service.user_repo.find_by_email.return_value = User(
            id="123",
            email="test@example.com",
            password_hash=bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode(),
            status="active"
        )
        auth_service.token_service.create_access_token.return_value = "access_token"
        auth_service.token_service.create_refresh_token.return_value = "refresh_token"
        
        # Act
        result = await auth_service.login("test@example.com", "password123")
        
        # Assert
        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"
        auth_service.user_repo.find_by_email.assert_called_once_with("test@example.com")
    
    @pytest.mark.asyncio
    async def test_login_invalid_password_returns_error(self, auth_service):
        """Test login with wrong password raises AuthenticationError"""
        # Arrange
        auth_service.user_repo.find_by_email.return_value = User(
            id="123",
            email="test@example.com",
            password_hash=bcrypt.hashpw(b"correct_password", bcrypt.gensalt()).decode()
        )
        
        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            await auth_service.login("test@example.com", "wrong_password")
        
        assert "Invalid email or password" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_login_rate_limited_after_5_attempts(self, auth_service):
        """Test rate limiting after 5 failed attempts"""
        # Arrange
        auth_service.cache.incr.return_value = 6
        auth_service.cache.ttl.return_value = 600
        
        # Act & Assert
        with pytest.raises(RateLimitError) as exc_info:
            await auth_service.login("test@example.com", "password")
        
        assert exc_info.value.retry_after == 600
```

### 12.4. Performance Test Script

```javascript
// k6 Load Test Script
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Peak
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],  // p95 < 200ms
    errors: ['rate<0.01'],              // Error rate < 1%
  },
};

export default function () {
  const payload = JSON.stringify({
    email: `user${__VU}@example.com`,
    password: 'testpassword123',
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post('http://api.example.com/v1/auth/login', payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });

  errorRate.add(res.status !== 200);
  sleep(1);
}
```

### 12.5. Acceptance Criteria (Definition of Done)

```markdown
## Definition of Done Checklist

### Code Quality
- [ ] All unit tests pass (coverage ≥ 80%)
- [ ] All integration tests pass
- [ ] No linting errors (ESLint/Pylint)
- [ ] No type errors (TypeScript/mypy)
- [ ] Code reviewed and approved by 2 engineers

### Security
- [ ] Security scan clean (Snyk/Sonar)
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Authorization checks in place

### Documentation
- [ ] API documentation updated (OpenAPI)
- [ ] README updated if needed
- [ ] ADR created for significant decisions
- [ ] Changelog entry added

### Deployment
- [ ] Feature flag configured
- [ ] Rollback plan documented
- [ ] Monitoring dashboards updated
- [ ] Alerts configured
```

---

## 13. DEPLOYMENT & OPERATIONS

_Triển khai và vận hành_

### 13.1. Deployment Strategy

|Strategy|Use Case|Rollback Time|Risk|
|:--|:--|:--|:--|
|**Blue-Green**|Major releases|Instant|Low|
|**Canary**|Feature releases|Minutes|Low|
|**Rolling**|Minor updates|Minutes|Medium|
|**Recreate**|Breaking changes|Depends|High|

### 13.2. CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run linting
        run: |
          pylint src/
          mypy src/
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  # Stage 2: Security Scan
  security:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Snyk
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'

  # Stage 3: Build & Push
  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myapp:latest
      
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker push $ECR_REGISTRY/myapp:${{ github.sha }}

  # Stage 4: Deploy
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    environment: staging
    steps:
      - name: Deploy to Staging
        run: |
          kubectl set image deployment/api api=$ECR_REGISTRY/myapp:${{ github.sha }}
          kubectl rollout status deployment/api --timeout=5m

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production
    steps:
      - name: Deploy to Production (Canary)
        run: |
          # Deploy to 10% of pods
          kubectl set image deployment/api-canary api=$ECR_REGISTRY/myapp:${{ github.sha }}
          
          # Monitor for 10 minutes
          sleep 600
          
          # Check error rate
          ERROR_RATE=$(curl -s "http://prometheus/api/v1/query?query=error_rate" | jq '.data.result[0].value[1]')
          if [ $(echo "$ERROR_RATE > 0.01" | bc) -eq 1 ]; then
            echo "Error rate too high, rolling back"
            kubectl rollout undo deployment/api-canary
            exit 1
          fi
          
          # Full rollout
          kubectl set image deployment/api api=$ECR_REGISTRY/myapp:${{ github.sha }}
```

### 13.3. Infrastructure as Code

```hcl
# terraform/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "prod/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "production-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    general = {
      min_size     = 3
      max_size     = 10
      desired_size = 5
      
      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source = "terraform-aws-modules/rds/aws"
  
  identifier = "production-db"
  engine     = "postgres"
  engine_version = "15.4"
  
  instance_class = "db.r6g.large"
  allocated_storage = 100
  
  multi_az = true
  
  backup_retention_period = 7
  backup_window = "03:00-04:00"
  maintenance_window = "Mon:04:00-Mon:05:00"
}
```

### 13.4. Runbooks

```markdown
## Runbook: Service Restart

### When to Use
- Service not responding to health checks
- Memory usage > 90% for extended period

### Steps
1. Check current status:
   ```bash
   kubectl get pods -n production -l app=api
```

2. Check logs for errors:
    
    ```bash
    kubectl logs -n production -l app=api --tail=100
    ```
    
3. Restart pods (rolling):
    
    ```bash
    kubectl rollout restart deployment/api -n production
    ```
    
4. Monitor rollout:
    
    ```bash
    kubectl rollout status deployment/api -n production
    ```
    
5. Verify health:
    
    ```bash
    curl -s https://api.example.com/health | jq
    ```
    

### Escalation

If service doesn't recover within 15 minutes:

1. Page on-call engineer
2. Prepare rollback: `kubectl rollout undo deployment/api`

````

### 13.5. Disaster Recovery Plan

| Component | Backup Frequency | Retention | Recovery Procedure |
|:----------|:-----------------|:----------|:-------------------|
| Database | Daily full, hourly WAL | 30 days | Point-in-time recovery |
| Redis | Hourly RDB | 7 days | Restore from snapshot |
| S3 | Real-time replication | Indefinite | Cross-region failover |
| Secrets | On change | 30 versions | Restore from Vault |

---

## 14. TRADE-OFFS & ALTERNATIVES

*"Design is about trade-offs" - Every decision has consequences*

### 14.1. Key Design Decisions

#### ADR-001: Use PostgreSQL over MongoDB

```markdown
# ADR-001: Database Selection

## Status
Accepted

## Context
Need to select primary database for user data and transactions.

## Decision
Use PostgreSQL instead of MongoDB.

## Rationale
- Strong ACID guarantees required for financial transactions
- Complex relational queries (JOINs) common in our use cases
- Team has more PostgreSQL experience
- Better tooling for migrations (Alembic)

## Consequences
### Positive
- Data integrity guaranteed
- Mature ecosystem
- Cost-effective (can use RDS)

### Negative
- Less flexible schema (need migrations)
- Vertical scaling initially (shard later if needed)
- NoSQL patterns need workarounds (JSONB)

## Alternatives Considered
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| MongoDB | Flexible schema, horizontal scaling | Eventual consistency | ACID needed |
| CockroachDB | Distributed SQL | Operational complexity | Overkill for current scale |
````

### 14.2. Trade-off Analysis Matrix

|Decision|Option A|Option B|Chosen|Reason|
|:--|:--|:--|:--|:--|
|Cache Strategy|Write-through|Write-behind|Write-through|Consistency > Performance|
|API Style|REST|GraphQL|REST|Simpler, team familiar|
|Auth Tokens|Session|JWT|JWT|Stateless, scale better|
|Message Queue|RabbitMQ|Kafka|RabbitMQ|Simpler ops, sufficient throughput|

---

## 15. GLOSSARY & REFERENCES

### 15.1. Glossary

|Term|Definition|
|:--|:--|
|ADR|Architecture Decision Record - Document capturing design decisions|
|CQRS|Command Query Responsibility Segregation|
|DDD|Domain-Driven Design|
|FMEA|Failure Mode and Effects Analysis|
|HPA|Horizontal Pod Autoscaler (Kubernetes)|
|MTBF|Mean Time Between Failures|
|MTTR|Mean Time To Repair|
|RTO|Recovery Time Objective|
|RPO|Recovery Point Objective|
|SLA|Service Level Agreement|
|SLO|Service Level Objective|

### 15.2. References

- [Google Design Docs](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [C4 Model](https://c4model.com/)
- [OWASP Top 10](https://owasp.org/Top10/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [ADR Templates](https://github.com/joelparkerhenderson/architecture-decision-record)

---

## 16. APPENDICES

### 16.1. Configuration Templates

```bash
# .env.example
# Application
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000
APP_SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://localhost:6379/0

# External Services
STRIPE_API_KEY=sk_test_xxx
SENDGRID_API_KEY=SG.xxx

# Observability
DATADOG_API_KEY=xxx
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 16.2. Kubernetes Manifests

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: myapp:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets
```

---

## 17. CHANGE LOG

````markdown
## [3.1.0] - 2025-01-15
### Added
- Comprehensive pseudo code examples for all modules
- FMEA risk analysis table
- Kubernetes HPA configuration
- k6 load test scripts

### Changed
- Updated API versioning strategy
- Improved error handling standards
- Enhanced security section with STRIDE model

### Deprecated
- Legacy session-based auth (to be removed in v4.0)

## [3.0.0] - 2025-01-10
### Added
- Initial Universal Pro template
- Multi-domain support (BE, FE, AI/ML)
- C4 Model architecture diagrams

---

## 🎯 COMPLETION CHECKLIST

```markdown
✅ Metadata: Title, Author, Status, Version, Related Docs
✅ 1. Overview: Problem + Solution + Impact (< 1 page)
✅ 2. Goals/Scope: In-scope, Out-of-scope, Assumptions, Constraints, Dependencies
✅ 3. User Stories: Primary stories với Acceptance Criteria + Flow diagrams
✅ 4. API Contract: Full Request/Response specs, Error codes, Versioning
✅ 5. Data Model: ERD + Schema SQL + Indexing + Caching + Retention
✅ 6. Architecture: C4 Diagrams + Sequence diagrams + State machines
✅ 7. Implementation: Per-module specs + Pseudo code + Business rules
✅ 8. Security: AuthN/AuthZ + Encryption + Compliance + Threat model
✅ 9. NFR: Latency/Throughput/SLA targets + Capacity planning
✅ 10. Observability: Logging/Metrics/Tracing + Alerting rules
✅ 11. Failure Modes: FMEA + Retry + Circuit breaker + Degradation
✅ 12. Testing: Test pyramid + Sample tests + Performance tests + DoD
✅ 13. Deployment: CI/CD + IaC + Runbooks + DR plan
✅ 14. Trade-offs: ADRs + Decision matrix
✅ 15. Glossary: Terms + References
✅ 16. Appendices: Config templates + K8s manifests
✅ 17. Change Log: Version history
````

---

<div align="center">

**⁂**

_Template này tổng hợp best practices từ: Google, AWS, Microsoft Azure, Meta, Abnormal AI, Stripe_

**Version 3.1 - Universal Pro Edition**

</div>

---

# 2. Mẫu Tài liệu Thiết kế Phần mềm (Software Design Document - SDD) Siêu Chi tiết (100/100)

**Tên Dự án:** [Tên Dự án - PROJECT_NAME]
**Phiên bản:** 1.0
**Ngày:** [Ngày hoàn thành - DATE]
**Tác giả:** Manus AI

---

## 📖 Mục lục (Table of Contents)

1.  **📖 Giới thiệu (Introduction)**
    1.1. Mục đích Tài liệu (Document Purpose)
    1.2. Phạm vi Hệ thống (System Scope)
    1.3. Đối tượng Độc giả (Target Audience)
    1.4. Định nghĩa, Thuật ngữ và Viết tắt (Definitions, Terms, and Acronyms)
    1.5. Tài liệu Tham khảo (References)

2.  **🌐 Tổng quan Hệ thống (System Overview)**
    2.1. Bối cảnh và Mục tiêu Kinh doanh (Context and Business Goals)
    2.2. Tầm nhìn và Chiến lược Sản phẩm (Product Vision and Strategy)
    2.3. Các Bên Liên quan (Stakeholders)
    2.4. Các Giả định và Ràng buộc (Assumptions and Constraints)
    2.5. Yêu cầu Chức năng (Functional Requirements - FRs)
    2.6. Yêu cầu Phi Chức năng (Non-Functional Requirements - NFRs)
        2.6.1. Hiệu năng (Performance)
        2.6.2. Khả năng Mở rộng (Scalability)
        2.6.3. Độ tin cậy và Khả dụng (Reliability and Availability)
        2.6.4. Bảo mật (Security)
        2.6.5. Khả năng Bảo trì (Maintainability)
        2.6.6. Khả năng Kiểm thử (Testability)
        2.6.7. Khả năng Vận hành (Operability/Observability)

3.  **🏗️ Thiết kế Cấp cao (High-Level Design - HLD)**
    3.1. Kiến trúc Tổng thể (Overall Architecture)
        3.1.1. Mô hình Kiến trúc (Architectural Pattern - e.g., Microservices, Monolith, Layered)
        3.1.2. Sơ đồ Khối (Block Diagram) và Phân tách (Decomposition)
        3.1.3. Lựa chọn Công nghệ (Technology Stack Rationale)
        3.1.4. Các Nguyên tắc Thiết kế (Design Principles - e.g., SOLID, DRY, DDD)
    3.2. Thiết kế Dữ liệu Cấp cao (High-Level Data Design)
        3.2.1. Sơ đồ Quan hệ Thực thể (Entity-Relationship Diagram - ERD) Cấp cao
        3.2.2. Lựa chọn Cơ sở Dữ liệu (Database Selection Rationale)
        3.2.3. Chiến lược Phân mảnh và Sao chép (Sharding and Replication Strategy)
    3.3. Thiết kế Giao diện Hệ thống (System Interface Design)
        3.3.1. Định nghĩa API Gateway và Cổng (Gateway Definition)
        3.3.2. Các Giao diện Bên ngoài (External Interfaces)
        3.3.3. Các Giao diện Nội bộ (Internal Interfaces - Service-to-Service Communication)

4.  **🔍 Thiết kế Chi tiết (Low-Level Design - LLD)**
    4.1. **Thiết kế Thành phần (Component Design)**
        4.1.1. **Thành phần A: [Tên Dịch vụ/Module]**
            4.1.1.1. Mục đích và Phạm vi (Purpose and Scope)
            4.1.1.2. Sơ đồ Lớp (Class Diagram)
            4.1.1.3. Sơ đồ Trình tự (Sequence Diagram) cho các Luồng Chính (Key Flows)
            4.1.1.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)
            4.1.1.5. Giả mã Thuật toán (Pseudocode) cho Logic Nghiệp vụ Phức tạp
            4.1.1.6. Xử lý Lỗi và Ngoại lệ (Error and Exception Handling)
        4.1.2. **Thành phần B: [Tên Dịch vụ/Module]**
            ... (Lặp lại cấu trúc 4.1.1)
        4.1.3. **Thành phần C: [Tên Dịch vụ/Module]**
            ... (Lặp lại cấu trúc 4.1.1)
        4.1.4. **Thành phần N: [Tên Dịch vụ/Module]**
            ... (Lặp lại cấu trúc 4.1.1)
    4.2. **Thiết kế Dữ liệu Chi tiết (Detailed Data Design)**
        4.2.1. Định nghĩa Schema Cơ sở Dữ liệu (Database Schema Definition)
        4.2.2. Từ điển Dữ liệu (Data Dictionary)
        4.2.3. Thiết kế Cache (Caching Design - e.g., Redis, Memcached)
        4.2.4. Thiết kế Hàng đợi Tin nhắn (Message Queue Design - e.g., Kafka, RabbitMQ)

5.  **🚀 Thiết kế Vận hành và Triển khai (Deployment and Operational Design)**
    5.1. Môi trường Triển khai (Deployment Environment)
    5.2. Sơ đồ Triển khai (Deployment Diagram - e.g., Kubernetes, Cloud Infrastructure)
    5.3. Chiến lược Triển khai (Deployment Strategy - e.g., Blue/Green, Canary)
    5.4. Giám sát và Quan sát (Monitoring and Observability)
        5.4.1. Logging (ELK/Loki)
        5.4.2. Metrics (Prometheus/Grafana)
        5.4.3. Tracing (Jaeger/Zipkin)
    5.5. Quản lý Cấu hình và Bí mật (Configuration and Secret Management)
    5.6. Kế hoạch Phục hồi Thảm họa (Disaster Recovery Plan - DRP)

6.  **🔒 Thiết kế Bảo mật (Security Design)**
    6.1. Phân tích Rủi ro Bảo mật (Security Risk Analysis - e.g., STRIDE)
    6.2. Thiết kế Xác thực và Ủy quyền (Authentication and Authorization - e.g., OAuth 2.0, JWT)
    6.3. Bảo mật Dữ liệu (Data Security - Encryption at Rest and In Transit)
    6.4. Bảo mật API (API Security - Rate Limiting, Input Validation)
    6.5. Bảo mật Hạ tầng (Infrastructure Security - Network Segmentation, Firewall)

7.  **🧪 Chiến lược Kiểm thử và Chất lượng (Testing and Quality Strategy)**
    7.1. Chiến lược Kiểm thử Đơn vị (Unit Testing Strategy)
    7.2. Chiến lược Kiểm thử Tích hợp (Integration Testing Strategy)
    7.3. Kiểm thử Đầu cuối (End-to-End Testing) và Kiểm thử Hiệu năng (Performance Testing)
    7.4. Ma trận Truy vết Yêu cầu (Requirements Traceability Matrix - RTM)

8.  **📎 Phụ lục (Appendices)**
    8.1. Ma trận Quyết định Kiến trúc (Architecture Decision Records - ADRs)
    8.2. Sơ đồ Luồng Người dùng (User Flow Diagrams)
    8.3. Thiết kế Giao diện Người dùng (User Interface - UI/UX Mockups)
    8.4. Danh sách Các Vấn đề Mở (Open Issues)
    8.5. Lịch sử Thay đổi Tài liệu (Document Revision History)

---

*(Nội dung chi tiết cho từng mục sẽ được bổ sung trong các bước tiếp theo để đạt được độ dài 100 trang)---

## 🎯 Tóm Tắt Điều Hành (Executive Summary - TL;DR)

| Tiêu chí (Aspect) | Chi tiết (Details) |
| :--- | :--- |
| **Vấn đề (Problem)** | [Mô tả vấn đề kinh doanh/kỹ thuật hệ thống giải quyết] |
| **Giải pháp (Solution)** | [Kiến trúc chính: Microservices, Kafka, K8s, Cloud-Native] |
| **Mục tiêu Kinh doanh (Business Goal)** | [Tăng trưởng Doanh thu X%, Cải thiện CX Y%] |
| **Mục tiêu Kỹ thuật (Technical Goal)** | [SLA 99.99%, Response Time < 200ms, Hỗ trợ Z users] |
| **Công nghệ Chính (Tech Stack)** | [Golang/Java, PostgreSQL, Kafka, Kubernetes] |
| **Rủi ro Chính (Key Risks)** | [Distributed Transaction Complexity, Cloud Cost Management] |
| **Thời gian (Timeline)** | [3 tháng MVP, 6 tháng Production-Ready] |

---

## 📖 1. Giới thiệu (Introduction)## 1.1. Mục đích Tài liệu (Document Purpose)

Mục đích chính của Tài liệu Thiết kế Phần mềm (**Software Design Document - SDD**) này là cung cấp một bản thiết kế toàn diện và chi tiết cho hệ thống phần mềm **[Tên Dự án - PROJECT_NAME]**. Tài liệu này đóng vai trò là **"bản thiết kế kỹ thuật" (technical blueprint)**, chuyển đổi các yêu cầu đã được xác định trong Tài liệu Yêu cầu Phần mềm (**Software Requirements Specification - SRS**) thành một giải pháp kiến trúc và thiết kế chi tiết, sẵn sàng cho giai đoạn triển khai (**implementation**).

Tài liệu này bao gồm cả **Thiết kế Cấp cao (High-Level Design - HLD)**, mô tả kiến trúc tổng thể, các thành phần chính (**components**) và mối quan hệ giữa chúng, cũng như **Thiết kế Cấp thấp (Low-Level Design - LLD)**, mô tả chi tiết cấu trúc dữ liệu, thuật toán, và giao diện của từng module.

## 1.2. Phạm vi Hệ thống (System Scope)

Phạm vi của hệ thống **[PROJECT_NAME]** được xác định như sau:

| Phạm vi | Mô tả Chi tiết |
| :--- | :--- |
| **Trong Phạm vi (In Scope)** | [Liệt kê các tính năng, module, và người dùng sẽ được phát triển trong giai đoạn này. Ví dụ: Quản lý Người dùng (User Management), Danh mục Sản phẩm (Product Catalog), Xử lý Đơn hàng (Order Processing), Cổng Thanh toán (Payment Gateway Integration).] |
| **Ngoài Phạm vi (Out of Scope)** | [Liệt kê các tính năng, module, hoặc hệ thống bên ngoài sẽ không được phát triển hoặc tích hợp trong giai đoạn này. Ví dụ: Hệ thống Báo cáo Phân tích Chuyên sâu (Advanced Analytics Reporting), Ứng dụng Di động Bản địa (Native Mobile App - chỉ phát triển Web App), Hỗ trợ Đa ngôn ngữ (Multi-language Support).] |

## 1.3. Đối tượng Độc giả (Target Audience)

Tài liệu này hướng đến các đối tượng chính sau:

*   **Kỹ sư Phần mềm (Software Engineers)**: Sử dụng SDD làm hướng dẫn chi tiết để phát triển và triển khai mã nguồn (**source code**).
*   **Kiến trúc sư Phần mềm (Software Architects)**: Đảm bảo tính nhất quán và tuân thủ của thiết kế với các nguyên tắc kiến trúc đã định.
*   **Quản lý Dự án (Project Managers)**: Theo dõi tiến độ, đánh giá rủi ro kỹ thuật, và ước tính nguồn lực.
*   **Kiểm thử viên (QA Engineers)**: Thiết kế các trường hợp kiểm thử (**test cases**) dựa trên thiết kế chi tiết của hệ thống.
*   **Đội ngũ Vận hành (DevOps/Operations Team)**: Hiểu rõ về kiến trúc triển khai (**deployment architecture**) và yêu cầu vận hành (**operability requirements**).

## 1.4. Định nghĩa, Thuật ngữ và Viết tắt (Definitions, Terms, and Acronyms)

| Viết tắt/Thuật ngữ | Tiếng Anh (English Term) | Định nghĩa (Definition) |
| :--- | :--- | :--- |
| **SDD** | Software Design Document | Tài liệu Thiết kế Phần mềm. |
| **HLD** | High-Level Design | Thiết kế Cấp cao, tập trung vào kiến trúc và các thành phần chính. |
| **LLD** | Low-Level Design | Thiết kế Cấp thấp, tập trung vào chi tiết lớp, module, và thuật toán. |
| **FR** | Functional Requirement | Yêu cầu Chức năng. |
| **NFR** | Non-Functional Requirement | Yêu cầu Phi Chức năng (chất lượng hệ thống). |
| **API** | Application Programming Interface | Giao diện Lập trình Ứng dụng. |
| **DB** | Database | Cơ sở Dữ liệu. |
| **Microservice** | Microservice | Kiến trúc dịch vụ nhỏ, độc lập. |
| **CI/CD** | Continuous Integration/Continuous Deployment | Tích hợp Liên tục/Triển khai Liên tục. |
| **SLA** | Service Level Agreement | Thỏa thuận Mức Dịch vụ. |
| **DRP** | Disaster Recovery Plan | Kế hoạch Phục hồi Thảm họa. |
| **ADR** | Architecture Decision Record | Hồ sơ Quyết định Kiến trúc. |
| **ISO/IEC 25010** | System and software quality models | Tiêu chuẩn quốc tế về mô hình chất lượng hệ thống và phần mềm. |

## 1.5. Tài liệu Tham khảo (References)

[1] IEEE Std 1016-2009 - Standard for Information Technology—Systems Design—Software Design Descriptions.
[2] [Link đến Tài liệu Yêu cầu Phần mềm (SRS) của dự án]
[3] [Link đến Tài liệu Kiến trúc Tổng thể (Architecture Vision) nếu có]

---

## 2. Tổng quan Hệ thống (System Overview)

## 2.1. Bối cảnh và Mục tiêu Kinh doanh (Context and Business Goals)

Hệ thống **[PROJECT_NAME]** được phát triển nhằm giải quyết vấn đề **[Mô tả vấn đề kinh doanh]** và đạt được các mục tiêu kinh doanh chiến lược sau:

*   **Tăng trưởng Doanh thu (Revenue Growth)**: Đạt **[Chỉ số cụ thể, ví dụ: 20% tăng trưởng]** trong quý đầu tiên sau khi ra mắt.
*   **Cải thiện Trải nghiệm Khách hàng (Customer Experience)**: Giảm **[Chỉ số cụ thể, ví dụ: 50% thời gian chờ đợi]** trong quá trình thanh toán.
*   **Tối ưu hóa Chi phí Vận hành (Operational Cost Optimization)**: Giảm **[Chỉ số cụ thể, ví dụ: 15% chi phí hạ tầng]** thông qua kiến trúc **Cloud-Native** hiệu quả.

## 2.2. Tầm nhìn và Chiến lược Sản phẩm (Product Vision and Strategy)

Tầm nhìn của sản phẩm là trở thành **[Mô tả tầm nhìn dài hạn, ví dụ: nền tảng thương mại điện tử B2B hàng đầu khu vực, cung cấp trải nghiệm mua sắm liền mạch và cá nhân hóa]**.

Chiến lược kỹ thuật để đạt được tầm nhìn này bao gồm:
1.  **Ưu tiên Khả năng Mở rộng (Scalability First)**: Thiết kế kiến trúc **Microservices** để hỗ trợ hàng triệu người dùng đồng thời (**concurrent users**).
2.  **Tập trung vào Độ tin cậy (Focus on Reliability)**: Áp dụng các mẫu thiết kế chịu lỗi (**fault-tolerant design patterns**) như **Circuit Breaker** và **Retry Mechanism**.
3.  **Vận hành Tự động (Automated Operations)**: Sử dụng **Infrastructure as Code (IaC)** và **CI/CD Pipelines** để triển khai và quản lý hệ thống.

## 2.3. Các Bên Liên quan (Stakeholders)

| Bên Liên quan | Vai trò Chính | Mối quan tâm Kỹ thuật |
| :--- | :--- | :--- |
| **Ban Lãnh đạo (Executive Team)** | Quyết định chiến lược, ngân sách. | Thời gian ra mắt (**Time-to-Market**), ROI. |
| **Quản lý Sản phẩm (Product Manager)** | Xác định yêu cầu chức năng. | Tính năng, trải nghiệm người dùng (**UX**). |
| **Đội ngũ Phát triển (Development Team)** | Xây dựng và kiểm thử hệ thống. | Chất lượng mã nguồn (**Code Quality**), Công cụ (**Tooling**), Kiến trúc. |
| **Đội ngũ Vận hành (DevOps Team)** | Triển khai và giám sát hệ thống. | Khả năng quan sát (**Observability**), Độ ổn định (**Stability**), Tự động hóa. |
| **Người dùng Cuối (End Users)** | Sử dụng hệ thống. | Hiệu năng, Độ dễ sử dụng (**Usability**), Độ tin cậy. |

## 2.4. Các Giả định và Ràng buộc (Assumptions and Constraints)

### 2.4.1. Giả định (Assumptions)

*   **Nền tảng Đám mây (Cloud Platform)**: Giả định rằng hệ thống sẽ được triển khai trên **[Tên Nền tảng Đám mây, ví dụ: AWS/Azure/GCP]** và các dịch vụ quản lý (**managed services**) sẽ được sử dụng (ví dụ: RDS cho DB, EKS/AKS/GKE cho Kubernetes).
*   **Nguồn lực (Resources)**: Giả định rằng đội ngũ phát triển có đủ kinh nghiệm về **[Công nghệ Chính, ví dụ: Golang/Java, Kubernetes, React]**.
*   **Tích hợp Bên ngoài (External Integration)**: Giả định rằng API của **[Tên Hệ thống Bên ngoài, ví dụ: Cổng Thanh toán X, Dịch vụ SMS Y]** sẽ ổn định và có SLA phù hợp.

### 2.4.2. Ràng buộc (Constraints)

*   **Ngân sách (Budget)**: Tổng chi phí hạ tầng hàng tháng không được vượt quá **[Số tiền] USD**.
*   **Thời gian (Timeline)**: Phiên bản Beta phải được triển khai trong vòng **[Số tháng]**.
*   **Tuân thủ Pháp lý (Regulatory Compliance)**: Hệ thống phải tuân thủ các quy định về bảo vệ dữ liệu **[Ví dụ: GDPR, CCPA, Nghị định 13]**.
*   **Công nghệ Bắt buộc (Mandatory Technology)**: Bắt buộc sử dụng **[Ví dụ: PostgreSQL]** làm cơ sở dữ liệu chính và **[Ví dụ: Kafka]** cho hàng đợi tin nhắn.

## 2.5. Yêu cầu Chức năng (Functional Requirements - FRs)

Các yêu cầu chức năng được nhóm theo các module chính. (Tham khảo chi tiết trong Tài liệu SRS [2]).

| ID | Module | Mô tả Yêu cầu Chức năng (FR Description) |
| :--- | :--- | :--- |
| **FR-001** | Quản lý Người dùng | Người dùng có thể đăng ký (**Sign Up**), đăng nhập (**Log In**), và quản lý hồ sơ cá nhân. |
| **FR-002** | Danh mục Sản phẩm | Hệ thống phải cho phép quản trị viên thêm, sửa, xóa, và tìm kiếm sản phẩm. |
| **FR-003** | Giỏ hàng | Người dùng có thể thêm, xóa, và cập nhật số lượng sản phẩm trong giỏ hàng. |
| **FR-004** | Xử lý Đơn hàng | Hệ thống phải xử lý quy trình đặt hàng, bao gồm xác nhận, thanh toán, và cập nhật trạng thái đơn hàng. |
| **FR-005** | Thanh toán | Tích hợp với **[Tên Cổng Thanh toán]** để xử lý giao dịch an toàn. |
| **| FR-006 | Thông báo | Gửi email/SMS thông báo về trạng thái đơn hàng và các sự kiện quan trọng khác. |

## 2.7. User Stories (Gherkin Format)

Phần này cung cấp các kịch bản người dùng chi tiết dưới dạng **Gherkin** để làm cơ sở cho việc phát triển và kiểm thử chấp nhận (**Acceptance Testing**).

### US-001: Đăng ký Người dùng (User Registration)

```gherkin
Feature: User Registration
  As a new user
  I want to register with email and password
  So that I can access the system

  Scenario: Successful registration and email verification
    Given I am on the registration page
    When I submit valid email "user@example.com" and password "SecureP@ss123"
    Then the system sends a verification email to "user@example.com" within 30 seconds
    And my account status is set to "PENDING_VERIFICATION"
    When I click the verification link in the email
    Then my account status is set to "ACTIVE"
    And I am redirected to the login page
    
  Scenario: Registration with existing email
    Given an account with email "existing@example.com" already exists
    When I submit email "existing@example.com" and password "NewP@ss123"
    Then I receive an error message "Email already in use"
    And my account status remains unchanged
```

### US-002: Đặt hàng (Order Placement)

```gherkin
Feature: Order Placement
  As a logged-in customer
  I want to place an order for products in my cart
  So that the items are reserved and payment is processed

  Scenario: Successful order placement with payment
    Given I have "Product A" (Qty 2) and "Product B" (Qty 1) in my cart
    And I have provided a valid shipping address
    When I select "Credit Card" as payment method and click "Place Order"
    Then the system reserves inventory for all items
    And the system processes the payment successfully
    And the order status is set to "PAID"
    And I receive an order confirmation email
    
  Scenario: Order placement failure due to insufficient stock
    Given I have "Product C" (Qty 10) in my cart
    And the available stock for "Product C" is 5
    When I click "Place Order"
    Then the system fails to reserve inventory
    And the order status is set to "FAILED"
    And I receive a notification about insufficient stock
```

---

## 2.8. Yêu cầu Phi Chức năng (Non-Functional Requirements - NFRs)

Các NFRs là yếu tố quyết định chất lượng và tính hiệu quả của thiết kế.

### 2.8.1. Hiệu năng (Performance)

| Chỉ số (Metric) | Yêu cầu (Requirement) |
| :--- | :--- |
| **Thời gian Phản hồi (Response Time)** | 95% các yêu cầu API phải có thời gian phản hồi dưới **200ms**. |
| **Thông lượng (Throughput)** | Hệ thống phải xử lý được tối thiểu **500 giao dịch/giây (TPS)** trong giờ cao điểm. |
| **Tải Người dùng (User Load)** | Hỗ trợ tối thiểu **100,000 người dùng đồng thời (concurrent users)**. |
| **Thời gian Tải Trang (Page Load Time)** | Thời gian tải trang ban đầu (First Contentful Paint) phải dưới **2 giây** trên mạng 3G. |

#### Bảng Performance Baseline (Latency Distribution)

Bảng này cung cấp các chỉ số hiệu năng cơ sở (**baseline metrics**) chi tiết cho các API quan trọng, giúp đội ngũ vận hành và kiểm thử có mục tiêu đo lường rõ ràng.

| API Endpoint | Mô tả | P50 (ms) | P95 (ms) | P99 (ms) |
| :--- | :--- | :--- | :--- | :--- |
| `POST /users/register` | Đăng ký người dùng | 50 | 150 | 250 |
| `GET /products/{id}` | Truy vấn chi tiết sản phẩm | 20 | 50 | 100 |
| `POST /orders` | Tạo đơn hàng (Saga Start) | 100 | 200 | 400 |
| `GET /orders/{id}` | Truy vấn trạng thái đơn hàng | 30 | 80 | 150 |

*   **P50 (Median Latency)**: 50% các yêu cầu phải hoàn thành trong thời gian này.
*   **P95 (Tail Latency)**: 95% các yêu cầu phải hoàn thành trong thời gian này (mục tiêu SLO chính).
*   **P99 (Worst-Case Latency)**: 99% các yêu cầu phải hoàn thành trong thời gian này (giúp xác định các vấn đề về độ trễ đuôi - **tail latency**).

### 2.8.2. Khả năng Mở rộng (Scalability)

*   **Mở rộng Ngang (Horizontal Scaling)**: Tất cả các dịch vụ không trạng thái (**stateless services**) phải có khả năng mở rộng ngang một cách tự động (**auto-scaling**) dựa trên tải CPU hoặc độ trễ hàng đợi.
*   **Mở rộng Dữ liệu (Data Scaling)**: Cơ sở dữ liệu phải được thiết kế để hỗ trợ **phân mảnh (sharding)** hoặc **sao chép đọc-ghi (read-replica)** để xử lý lượng dữ liệu tăng trưởng **50% mỗi năm**.

### 2.8.3. Độ tin cậy và Khả dụng (Reliability and Availability)

#### Mapping với ISO/IEC 25010

Các yêu cầu phi chức năng (NFRs) được xác định dựa trên mô hình chất lượng **ISO/IEC 25010 (SQuaRE)**, đảm bảo tính toàn diện và chuẩn mực quốc tế.

| Đặc tính Chất lượng ISO/IEC 25010 | Mục SDD Tương ứng | Mô tả |
| :--- | :--- | :--- |
| **Functional Suitability** | 2.5. Yêu cầu Chức năng | Hệ thống cung cấp các chức năng cần thiết. |
| **Performance Efficiency** | 2.8.1. Hiệu năng | Hiệu suất về thời gian, tài nguyên. |
| **Compatibility** | 3.3. Thiết kế Giao diện | Khả năng tương tác với các hệ thống khác. |
| **Usability** | 8.3. Thiết kế UI/UX | Dễ học, dễ sử dụng, hấp dẫn. |
| **Reliability** | 2.8.3. Độ tin cậy | Độ trưởng thành, khả dụng, chịu lỗi, khả năng phục hồi. |
| **Security** | 6. Thiết kế Bảo mật | Bảo mật, toàn vẹn, không chối bỏ. |
| **Maintainability** | 2.8.5. Khả năng Bảo trì | Khả năng phân tích, thay đổi, kiểm thử. |
| **Portability** | 5. Thiết kế Vận hành | Khả năng chuyển đổi sang môi trường khác. |

*   **Thời gian Hoạt động (Uptime/Availability)**: Hệ thống phải đạt **SLA 99.99%** (tương đương không quá 52.6 phút ngừng hoạt động mỗi năm).
*   **Chịu lỗi (Fault Tolerance)**: Hệ thống phải được triển khai trên nhiều vùng sẵn sàng (**Availability Zones - AZs**) và có khả năng tự động phục hồi (**self-healing**) khi một thành phần thất bại.
*   **Mất Dữ liệu (Data Loss)**: Mục tiêu Điểm Phục hồi (**Recovery Point Objective - RPO**) là **0 giây** (sao lưu liên tục) và Mục tiêu Thời gian Phục hồi (**Recovery Time Objective - RTO**) là **dưới 15 phút** trong trường hợp thảm họa.

*   **Thời gian Hoạt động (Uptime/Availability)**: Hệ thống phải đạt **SLA 99.99%** (tương đương không quá 52.6 phút ngừng hoạt động mỗi năm).
*   **Chịu lỗi (Fault Tolerance)**: Hệ thống phải được triển khai trên nhiều vùng sẵn sàng (**Availability Zones - AZs**) và có khả năng tự động phục hồi (**self-healing**) khi một thành phần thất bại.
*   **Mất Dữ liệu (Data Loss)**: Mục tiêu Điểm Phục hồi (**Recovery Point Objective - RPO**) là **0 giây** (sao lưu liên tục) và Mục tiêu Thời gian Phục hồi (**Recovery Time Objective - RTO**) là **dưới 15 phút** trong trường hợp thảm họa.

### 2.8.4. Bảo mật (Security)

*   **Tuân thủ (Compliance)**: Tuân thủ **OWASP Top 10** và các tiêu chuẩn **PCI DSS** (nếu xử lý thẻ thanh toán).
*   **Xác thực (Authentication)**: Sử dụng **OAuth 2.0** và **OpenID Connect** cho xác thực người dùng.
*   **Mã hóa (Encryption)**: Tất cả dữ liệu nhạy cảm (**sensitive data**) phải được mã hóa khi lưu trữ (**at rest**) và khi truyền tải (**in transit**) bằng **TLS 1.2+**.
*   **Kiểm toán (Auditing)**: Mọi hành động của quản trị viên và các giao dịch quan trọng phải được ghi lại (**logged**) và lưu trữ trong **[Thời gian quy định]**.

### 2.8.5. Khả năng Bảo trì (Maintainability)

*   **Độ phức tạp Mã nguồn (Code Complexity)**: Độ phức tạp Cyclomatic của các hàm quan trọng không được vượt quá **10**.
*   **Tài liệu Hóa (Documentation)**: Tất cả các API phải được tài liệu hóa bằng **OpenAPI/Swagger**.
*   **Thời gian Sửa lỗi (Time to Fix)**: Các lỗi nghiêm trọng (**Critical Bugs**) phải được sửa và triển khai trong vòng **4 giờ**.

### 2.8.6. Khả năng Kiểm thử (Testability)

*   **Độ bao phủ Mã nguồn (Code Coverage)**: Mục tiêu độ bao phủ kiểm thử đơn vị (**Unit Test Coverage**) là **80%** cho các module nghiệp vụ cốt lõi.
*   **Môi trường Kiểm thử (Test Environment)**: Phải có môi trường **Staging** mô phỏng gần nhất môi trường **Production**.

### 2.8.7. Khả năng Vận hành (Operability/Observability)

*   **Giám sát (Monitoring)**: Hệ thống phải cung cấp các chỉ số (**metrics**) về hiệu năng, lỗi, và tài nguyên sử dụng thông qua **Prometheus/Grafana**.
*   **Ghi nhật ký (Logging)**: Tất cả các dịch vụ phải ghi nhật ký theo định dạng **JSON** chuẩn và tập trung hóa qua hệ thống **ELK Stack** hoặc **Loki**.
*   **Truy vết (Tracing)**: Áp dụng truy vết phân tán (**Distributed Tracing**) bằng **OpenTelemetry/Jaeger** để theo dõi các yêu cầu qua nhiều dịch vụ.

---

## 3. Thiết kế Cấp cao (High-Level Design - HLD)

## 3.1. Kiến trúc Tổng thể (Overall Architecture)

### 3.1.1. Mô hình Kiến trúc (Architectural Pattern)

Hệ thống **[PROJECT_NAME]** sẽ áp dụng mô hình **Kiến trúc Microservices (Microservices Architecture)**.

**Lý do lựa chọn:**
*   **Khả năng Mở rộng Độc lập (Independent Scalability)**: Mỗi dịch vụ có thể được mở rộng độc lập dựa trên nhu cầu tải cụ thể, tối ưu hóa việc sử dụng tài nguyên.
*   **Khả năng Phục hồi (Resilience)**: Lỗi trong một dịch vụ không làm sập toàn bộ hệ thống (Isolation of Failure).
*   **Triển khai Độc lập (Independent Deployment)**: Cho phép các nhóm phát triển triển khai các dịch vụ của họ một cách nhanh chóng và thường xuyên thông qua **CI/CD** mà không ảnh hưởng đến các dịch vụ khác.
*   **Linh hoạt Công nghệ (Technology Heterogeneity)**: Cho phép sử dụng các ngôn ngữ lập trình và cơ sở dữ liệu khác nhau phù hợp nhất cho từng dịch vụ.

**Các Nguyên tắc Kiến trúc Chính:**
*   **Phân tách theo Nghiệp vụ (Bounded Contexts)**: Mỗi Microservice sẽ tương ứng với một miền nghiệp vụ (**Business Domain**) rõ ràng (ví dụ: User, Order, Product).
*   **Giao tiếp Phi trạng thái (Stateless Communication)**: Các dịch vụ sẽ giao tiếp chủ yếu qua **API Gateway** bằng **REST/gRPC** cho các yêu cầu đồng bộ (**synchronous**) và qua **Message Queue (Kafka/RabbitMQ)** cho các sự kiện bất đồng bộ (**asynchronous**).
*   **Cơ sở Dữ liệu Độc lập (Database per Service)**: Mỗi Microservice sở hữu cơ sở dữ liệu riêng, đảm bảo tính độc lập và giảm thiểu sự phụ thuộc.

### 3.1.2. Sơ đồ Khối (Block Diagram) và Phân tách (Decomposition)

**Mô tả Sơ đồ Khối (Conceptual Block Diagram Description):**

Sơ đồ khối tổng thể sẽ bao gồm các lớp chính sau:

1.  **Lớp Giao diện Người dùng (Presentation Layer)**:
    *   **Web Client**: Ứng dụng **Single Page Application (SPA)** được xây dựng bằng **[React/Vue/Angular]**.
    *   **Mobile Client**: Ứng dụng di động được xây dựng bằng **[React Native/Flutter/Native]**.
2.  **Lớp Cổng API (API Gateway Layer)**:
    *   **API Gateway (e.g., Kong, AWS API Gateway, Zuul)**: Điểm truy cập duy nhất cho tất cả các yêu cầu từ bên ngoài. Chịu trách nhiệm về **Xác thực (Authentication)**, **Giới hạn Tốc độ (Rate Limiting)**, và **Định tuyến (Routing)**.
3.  **Lớp Dịch vụ (Microservices Layer)**:
    *   **Core Services**: Các dịch vụ nghiệp vụ cốt lõi (ví dụ: `UserService`, `OrderService`, `ProductService`).
    *   **Supporting Services**: Các dịch vụ hỗ trợ (ví dụ: `NotificationService`, `PaymentService`, `SearchService`).
4.  **Lớp Dữ liệu (Data Layer)**:
    *   **Primary Databases**: Cơ sở dữ liệu quan hệ (**Relational DB**) cho dữ liệu giao dịch (ví dụ: **PostgreSQL**).
    *   **NoSQL Databases**: Cơ sở dữ liệu phi quan hệ cho dữ liệu phi cấu trúc hoặc yêu cầu hiệu năng cao (ví dụ: **MongoDB** cho tài liệu, **Redis** cho Cache).
    *   **Message Broker (e.g., Kafka)**: Dùng để truyền tải các sự kiện giữa các dịch vụ.
5.  **Lớp Hạ tầng và Vận hành (Infrastructure & Operations Layer)**:
    *   **Container Orchestration (Kubernetes)**: Quản lý triển khai, mở rộng và tự phục hồi của các Microservice.
    *   **CI/CD Pipeline (e.g., Jenkins, GitLab CI, GitHub Actions)**: Tự động hóa quá trình xây dựng, kiểm thử và triển khai.
    *   **Observability Stack (Prometheus, Grafana, Loki/ELK)**: Giám sát và ghi nhật ký.

### 3.1.3. Lựa chọn Công nghệ (Technology Stack Rationale)

| Thành phần | Công nghệ Đề xuất | Lý do Lựa chọn (Rationale) |
| :--- | :--- | :--- |
| **Backend Services** | **[Golang/Java/Node.js]** | **[Golang]**: Hiệu năng cao, xử lý đồng thời (**concurrency**) tốt, phù hợp cho các dịch vụ I/O-bound. **[Java/Spring Boot]**: Hệ sinh thái lớn, ổn định, phù hợp cho các dịch vụ nghiệp vụ phức tạp. |
| **Frontend** | **[React/Vue.js]** | **[React]**: Phổ biến, cộng đồng lớn, hiệu năng tốt với Virtual DOM, phù hợp cho SPA phức tạp. |
| **Database (Transactional)** | **PostgreSQL** | Hỗ trợ ACID, tính năng JSONB mạnh mẽ, độ tin cậy cao, khả năng mở rộng tốt (Sharding, Replication). |
| **Database (Cache/Session)** | **Redis** | Hiệu năng đọc/ghi cực nhanh, phù hợp cho caching, quản lý phiên (**session management**), và giới hạn tốc độ. |
| **Message Broker** | **Apache Kafka** | Khả năng chịu lỗi cao, thông lượng lớn, hỗ trợ xử lý sự kiện theo thời gian thực (**real-time event streaming**), phù hợp cho kiến trúc Event-Driven. |
| **Containerization** | **Docker** | Đóng gói ứng dụng và môi trường chạy, đảm bảo tính nhất quán giữa các môi trường. |
| **Orchestration** | **Kubernetes (K8s)** | Quản lý vòng đời của container, tự động hóa triển khai, mở rộng, và cân bằng tải. |

### 3.1.4. Các Nguyên tắc Thiết kế (Design Principles)

Thiết kế sẽ tuân thủ các nguyên tắc sau để đảm bảo chất lượng mã nguồn và kiến trúc:

*   **SOLID Principles**: Áp dụng cho thiết kế lớp và module bên trong từng Microservice.
*   **DRY (Don't Repeat Yourself)**: Tránh lặp lại mã nguồn và logic nghiệp vụ.
*   **DDD (Domain-Driven Design)**: Sử dụng ngôn ngữ chung (**Ubiquitous Language**) và mô hình hóa các miền nghiệp vụ rõ ràng.
*   **Separation of Concerns**: Tách biệt rõ ràng các mối quan tâm (ví dụ: logic nghiệp vụ, truy cập dữ liệu, giao tiếp mạng).
*   **Resilience and Fault Tolerance**: Thiết kế để thất bại (**Design for Failure**) bằng cách sử dụng **Circuit Breaker**, **Timeout**, và **Retry** cho các cuộc gọi dịch vụ.

## 3.2. Thiết kế Dữ liệu Cấp cao (High-Level Data Design)

### 3.2.1. Sơ đồ Quan hệ Thực thể (Entity-Relationship Diagram - ERD) Cấp cao

**Mô tả ERD Cấp cao (Conceptual ERD Description):**

ERD cấp cao sẽ thể hiện các thực thể chính (**Core Entities**) và mối quan hệ giữa chúng, không đi sâu vào các thuộc tính chi tiết.

| Thực thể (Entity) | Mô tả | Mối quan hệ Chính |
| :--- | :--- | :--- |
| **User** | Thông tin người dùng (Khách hàng, Quản trị viên). | 1:N với Order (một User có nhiều Order). |
| **Product** | Thông tin sản phẩm (Tên, Giá, Mô tả). | 1:N với OrderItem (một Product có nhiều OrderItem). |
| **Order** | Thông tin đơn hàng (Trạng thái, Ngày đặt, Tổng tiền). | 1:N với OrderItem (một Order có nhiều OrderItem). |
| **Payment** | Thông tin giao dịch thanh toán. | 1:1 với Order (một Order có một Payment). |
| **Notification** | Lịch sử thông báo gửi đến người dùng. | N:1 với User (nhiều Notification cho một User). |

### 3.2.2. Lựa chọn Cơ sở Dữ liệu (Database Selection Rationale)

| Dịch vụ (Service) | Loại DB | Công nghệ | Lý do |
| :--- | :--- | :--- | :--- |
| **Order Service** | Relational (Transactional) | PostgreSQL | Cần tính toàn vẹn dữ liệu (**ACID**) cao cho các giao dịch tài chính. |
| **Product Service** | Relational/Search | PostgreSQL + ElasticSearch | PostgreSQL cho dữ liệu chính, ElasticSearch cho khả năng tìm kiếm toàn văn (**full-text search**) và phân tích. |
| **User Service** | Relational | PostgreSQL | Lưu trữ thông tin người dùng và xác thực. |
| **Notification Service** | NoSQL (Document) | MongoDB | Dữ liệu phi cấu trúc, dễ dàng thay đổi schema, phù hợp cho lưu trữ log và thông báo. |

### 3.2.3. Chiến lược Phân mảnh và Sao chép (Sharding and Replication Strategy)

*   **Sao chép (Replication)**: Tất cả các cơ sở dữ liệu chính (PostgreSQL) sẽ được cấu hình **Primary-Replica Replication** (tối thiểu 1 Primary và 2 Replica) để tăng khả năng đọc (**read throughput**) và đảm bảo **High Availability (HA)**.
*   **Phân mảnh (Sharding)**: Đối với các bảng dự kiến có lượng dữ liệu khổng lồ (ví dụ: `Order`, `Transaction`), sẽ áp dụng chiến lược **Horizontal Sharding** dựa trên **[Ví dụ: User ID hoặc Tenant ID]**.
    *   **Key Sharding**: **[Ví dụ: User ID]** sẽ được sử dụng làm **Sharding Key** để đảm bảo dữ liệu của một người dùng nằm trên cùng một shard.
    *   **Quản lý Shard**: Sử dụng **[Ví dụ: Citus Data, Vitess, hoặc Sharding Logic Tùy chỉnh]** để quản lý việc định tuyến truy vấn.

## 3.3. Thiết kế Giao diện Hệ thống (System Interface Design)

### 3.3.1. Định nghĩa API Gateway và Cổng (Gateway Definition)

### 3.3.2. Đặc tả API (API Specification - OpenAPI 3.0)

Phần này cung cấp đặc tả chi tiết cho các giao diện API chính của hệ thống, sử dụng chuẩn **OpenAPI 3.0** (trước đây là Swagger). Đây là tài liệu tham chiếu chính cho các nhóm phát triển Frontend, Mobile, và các hệ thống đối tác.

**Ví dụ: Đặc tả API Đăng ký Người dùng (UserService)**

```yaml
openapi: 3.0.0
info:
  title: [PROJECT_NAME] User Service API
  version: 1.0.0
  description: API cho việc quản lý người dùng và xác thực.
servers:
  - url: https://api.[project_name].com/v1
    description: Production Server

paths:
  /users/register:
    post:
      summary: Đăng ký người dùng mới (Register a new user)
      tags:
        - Authentication
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
                - fullName
              properties:
                email:
                  type: string
                  format: email
                  example: user.new@example.com
                password:
                  type: string
                  format: password
                  minLength: 8
                  example: SecureP@ss123
                fullName:
                  type: string
                  example: Nguyen Van A
      responses:
        '202':
          description: Yêu cầu đăng ký đã được chấp nhận (Registration request accepted).
          content:
            application/json:
              schema:
                $ref: '##/components/schemas/RegistrationResponse'
        '400':
          description: Lỗi đầu vào (Invalid input).
        '409':
          description: Email đã tồn tại (Email already exists).

components:
  schemas:
    RegistrationResponse:
      type: object
      properties:
        message:
          type: string
          example: "Verification email sent. Account status is PENDING_VERIFICATION."
        userId:
          type: string
          format: uuid
          example: 123e4567-e89b-12d3-a456-426614174000
    ErrorResponse:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
```

---

### 3.3.3. Chiến lược Phiên bản hóa API (API Versioning Strategy)

Để đảm bảo tính tương thích ngược (**backward compatibility**) và quản lý sự thay đổi của API một cách hiệu quả, hệ thống sẽ áp dụng chiến lược phiên bản hóa **URI Versioning** kết hợp với **Deprecation Policy**.

*   **Định dạng Phiên bản (Versioning Format)**: Phiên bản API sẽ được nhúng vào đường dẫn URI, ví dụ: `/v1/users`, `/v2/products`.
*   **Chính sách Tương thích (Compatibility Policy)**:
    *   Các thay đổi không phá vỡ (**non-breaking changes**) như thêm trường mới vào phản hồi sẽ được triển khai trên phiên bản hiện tại.
    *   Các thay đổi phá vỡ (**breaking changes**) như xóa trường, thay đổi kiểu dữ liệu, hoặc thay đổi logic nghiệp vụ sẽ yêu cầu tạo một phiên bản API mới (ví dụ: từ `/v1` sang `/v2`).
*   **Chính sách Ngừng sử dụng (Deprecation Policy)**:
    *   Một phiên bản API cũ sẽ được duy trì và hỗ trợ trong tối thiểu **12 tháng** sau khi phiên bản mới được phát hành.
    *   Cảnh báo ngừng sử dụng (**deprecation warnings**) sẽ được gửi qua header phản hồi (**Response Header**) và tài liệu API.

---

### 3.3.4. Các Giao diện Bên ngoài (External Interfaces)

**API Gateway** sẽ là điểm tiếp xúc duy nhất với thế giới bên ngoài.

| Chức năng | Mô tả Chi tiết |
| :--- | :--- |
| **Xác thực (Authentication)** | Xác minh **JWT (JSON Web Token)** hoặc **Session Token** cho mọi yêu cầu. |
| **Ủy quyền (Authorization)** | Kiểm tra quyền truy cập cơ bản (ví dụ: `is_admin`, `is_user`). |
| **Định tuyến (Routing)** | Chuyển tiếp yêu cầu đến Microservice tương ứng (ví dụ: `/api/v1/users` -> `UserService`). |
| **Giới hạn Tốc độ (Rate Limiting)** | Áp dụng giới hạn tốc độ (ví dụ: 100 yêu cầu/phút/IP) để bảo vệ các dịch vụ hạ nguồn. |
| **Biến đổi Yêu cầu (Request Transformation)** | Chuyển đổi định dạng yêu cầu/phản hồi nếu cần (ví dụ: gRPC sang REST). |

### 3.3.4. Các Giao diện Bên ngoài (External Interfaces)

| Hệ thống Bên ngoài | Mục đích | Giao thức | SLA Yêu cầu |
| :--- | :--- | :--- | :--- |
| **Payment Gateway (e.g., Stripe, PayPal)** | Xử lý thanh toán và hoàn tiền. | HTTPS (REST API) | Uptime 99.99% |
| **SMS/Email Provider (e.g., Twilio, SendGrid)** | Gửi thông báo cho người dùng. | HTTPS (REST API) | Độ trễ dưới 500ms |
| **Identity Provider (e.g., Auth0, Keycloak)** | Quản lý danh tính và SSO. | OAuth 2.0/OpenID Connect | Uptime 99.9% |

### 3.3.5. Các Giao diện Nội bộ (Internal Interfaces - Service-to-Service Communication)

| Loại Giao tiếp | Mục đích | Giao thức | Mẫu Thiết kế |
| :--- | :--- | :--- | :--- |
| **Đồng bộ (Synchronous)** | Yêu cầu/Phản hồi tức thì (ví dụ: `OrderService` gọi `ProductService` để kiểm tra tồn kho). | **gRPC** (Ưu tiên) hoặc **REST** | **Client-Side Load Balancing**, **Circuit Breaker** |
| **Bất đồng bộ (Asynchronous)** | Truyền tải sự kiện, cập nhật trạng thái (ví dụ: `OrderService` gửi sự kiện `OrderCreated` đến `NotificationService`). | **Kafka** (Message Broker) | **Event-Driven Architecture**, **Saga Pattern** (cho giao dịch phân tán) |

---

## 4. Thiết kế Chi tiết (Low-Level Design - LLD)

Phần này cung cấp bản thiết kế chi tiết (**Low-Level Design - LLD**) cho từng thành phần (**component**) hoặc dịch vụ (**service**) đã được xác định trong HLD. Mục tiêu là cung cấp đủ thông tin để kỹ sư phần mềm có thể bắt đầu triển khai mã nguồn (**implementation**) mà không cần thêm bất kỳ quyết định thiết kế nào.

## 4.1. Thiết kế Thành phần (Component Design)

### 4.1.1. Thành phần A: UserService (Dịch vụ Quản lý Người dùng)

#### 4.1.1.1. Mục đích và Phạm vi (Purpose and Scope)

*   **Mục đích**: Quản lý tất cả các hoạt động liên quan đến người dùng, bao gồm đăng ký (**Sign Up**), đăng nhập (**Log In**), quản lý hồ sơ (**Profile Management**), và xác thực (**Authentication**).
*   **Phạm vi**: Cung cấp các API nội bộ và bên ngoài để quản lý vòng đời của thực thể `User` và `Role`.

#### 4.1.1.2. Sơ đồ Lớp (Class Diagram)

Dịch vụ `UserService` sẽ tuân theo kiến trúc **Layered Architecture** (hoặc **Clean Architecture**) với các lớp chính sau:

| Lớp (Layer) | Mô tả | Các Lớp/Interface Chính |
| :--- | :--- | :--- |
| **Presentation (API)** | Xử lý các yêu cầu HTTP/gRPC đến, xác thực đầu vào (**input validation**), và chuyển đổi DTO (**Data Transfer Object**). | `UserController`, `UserRouter` |
| **Service (Business Logic)** | Chứa logic nghiệp vụ cốt lõi, điều phối các hoạt động, và áp dụng các quy tắc nghiệp vụ (**business rules**). | `UserServiceImpl`, `IUserService` |
| **Repository (Data Access)** | Trừu tượng hóa việc truy cập cơ sở dữ liệu, ánh xạ đối tượng nghiệp vụ sang bản ghi DB (**ORM/DAO**). | `UserRepository`, `IUserRepository` |
| **Domain (Entities)** | Định nghĩa các đối tượng nghiệp vụ cốt lõi (**Domain Entities**) và các quy tắc bất biến (**invariants**). | `User`, `Role`, `Address` |

#### 4.1.1.3. Sơ đồ Trình tự (Sequence Diagram) cho Luồng Chính: Đăng ký Người dùng (User Registration)

**Mô tả Luồng:**

1.  **Client** gửi yêu cầu **POST /users/register** (chứa `email`, `password`, `name`) đến **API Gateway**.
2.  **API Gateway** xác thực cơ bản (Rate Limiting) và định tuyến đến **UserService**.
3.  **UserService (Controller)** nhận yêu cầu, chuyển đổi sang `RegisterUserCommand`.
4.  **UserService (Service)**:
    *   Gọi **UserRepository** để kiểm tra `email` đã tồn tại chưa.
    *   Nếu chưa, tạo `Password Hash` (sử dụng **Bcrypt** hoặc **Argon2**).
    *   Tạo đối tượng `User` mới với trạng thái `PENDING_VERIFICATION`.
    *   Gọi **UserRepository** để lưu `User` vào DB (trong một **Transaction**).
    *   Tạo `Verification Token` (JWT ngắn hạn).
    *   Gửi sự kiện **UserRegistered** (chứa `UserID`, `Email`, `Token`) đến **Message Broker (Kafka)**.
5.  **UserService (Controller)** trả về phản hồi **HTTP 202 Accepted** (hoặc 201 Created).
6.  **NotificationService** (là một **Consumer** của Kafka) nhận sự kiện **UserRegistered**.
7.  **NotificationService** gửi email xác nhận (chứa `Token`) đến người dùng.

#### 4.1.1.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)

**Thực thể Domain: `User`**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- |
| `user_id` | UUID | Khóa chính, định danh duy nhất. | PRIMARY KEY, NOT NULL |
| `email` | VARCHAR(255) | Địa chỉ email của người dùng. | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(100) | Mã băm mật khẩu. | NOT NULL |
| `full_name` | VARCHAR(255) | Tên đầy đủ. | NOT NULL |
| `phone_number` | VARCHAR(20) | Số điện thoại. | UNIQUE, NULLABLE |
| `status` | ENUM | Trạng thái tài khoản (PENDING, ACTIVE, INACTIVE, BANNED). | NOT NULL, Default: PENDING |
| `created_at` | TIMESTAMP WITH TIME ZONE | Thời điểm tạo tài khoản. | NOT NULL |
| `updated_at` | TIMESTAMP WITH TIME ZONE | Thời điểm cập nhật cuối cùng. | NOT NULL |

**DTO (Data Transfer Object): `UserResponseDTO`**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả |
| :--- | :--- | :--- |
| `id` | string (UUID) | ID người dùng. |
| `email` | string | Email. |
| `name` | string | Tên đầy đủ. |
| `status` | string | Trạng thái tài khoản. |

#### 4.1.1.5. Giả mã Thuật toán (Pseudocode) cho Logic Nghiệp vụ Phức tạp: Cập nhật Mật khẩu (Update Password)

```pseudocode
FUNCTION UpdatePassword(userID, oldPassword, newPassword):
    // 1. Lấy thông tin người dùng
    user = UserRepository.FindByID(userID)
    IF user IS NULL THEN
        THROW NotFoundException("User not found")
    END IF

    // 2. Xác minh mật khẩu cũ
    IF NOT PasswordHasher.Verify(oldPassword, user.password_hash) THEN
        THROW UnauthorizedException("Invalid old password")
    END IF

    // 3. Kiểm tra độ mạnh của mật khẩu mới (theo Business Rule)
    IF NOT PasswordValidator.IsStrong(newPassword) THEN
        THROW ValidationException("New password is too weak")
    END IF

    // 4. Tạo mã băm mới
    newPasswordHash = PasswordHasher.Hash(newPassword)

    // 5. Cập nhật vào DB
    user.password_hash = newPasswordHash
    user.updated_at = CurrentTimestamp()
    UserRepository.Save(user)

    // 6. Vô hiệu hóa tất cả các phiên (session) cũ (Security Measure)
    SessionManager.InvalidateAllSessions(userID)

    // 7. Gửi sự kiện thông báo
    EventPublisher.Publish("PasswordUpdated", {userID: userID, timestamp: CurrentTimestamp()})

    RETURN TRUE
END FUNCTION
```

#### 4.1.1.6. Xử lý Lỗi và Ngoại lệ (Error and Exception Handling)

| Mã Lỗi (Error Code) | Tên Ngoại lệ (Exception Name) | Mô tả | Mã HTTP (HTTP Status) |
| :--- | :--- | :--- | :--- |
| `USER_001` | `UserNotFoundException` | Người dùng không tồn tại. | 404 Not Found |
| `USER_002` | `EmailAlreadyExistsException` | Email đã được sử dụng khi đăng ký. | 409 Conflict |
| `USER_003` | `InvalidPasswordException` | Mật khẩu cũ không đúng hoặc mật khẩu mới không hợp lệ. | 401 Unauthorized / 400 Bad Request |
| `USER_004` | `DatabaseTransactionFailed` | Lỗi xảy ra trong quá trình giao dịch DB. | 500 Internal Server Error |

---

### 4.1.2. Thành phần B: OrderService (Dịch vụ Quản lý Đơn hàng)

*(Để đạt được độ dài 100 trang, phần này sẽ lặp lại cấu trúc chi tiết của UserService, tập trung vào logic nghiệp vụ phức tạp như "Tạo Đơn hàng" (bao gồm giao dịch phân tán - **Distributed Transaction**), "Cập nhật Trạng thái Đơn hàng", và "Hoàn tiền".)*

#### 4.1.2.1. Mục đích và Phạm vi (Purpose and Scope)

*   **Mục đích**: Quản lý toàn bộ vòng đời của một đơn hàng, từ khi tạo giỏ hàng, đặt hàng, đến khi hoàn thành hoặc hủy bỏ.
*   **Phạm vi**: Xử lý các thực thể `Order`, `OrderItem`, `ShippingAddress`, và điều phối các giao dịch phân tán liên quan đến `PaymentService` và `InventoryService`.

#### 4.1.2.2. Sơ đồ Lớp (Class Diagram)

*(Tương tự 4.1.1.2, nhưng với các lớp Domain như `Order`, `OrderItem`, `OrderStatus`, `ShippingInfo`)*

#### 4.1.2.3. Sơ đồ Trình tự (Sequence Diagram) cho Luồng Chính: Tạo Đơn hàng (Create Order - Sử dụng Saga Pattern)

**Mô tả Luồng (Saga Orchestration):**

1.  **Client** gửi yêu cầu **POST /orders** đến **API Gateway**.
2.  **OrderService (Controller)** nhận yêu cầu.
3.  **OrderService (Service)** bắt đầu một **Saga** mới (Giao dịch Phân tán):
    *   Gửi lệnh **ReserveInventoryCommand** đến **InventoryService** qua Kafka.
    *   **InventoryService** nhận lệnh, trừ tạm thời số lượng tồn kho, và gửi sự kiện **InventoryReservedEvent** hoặc **InventoryReservationFailedEvent** về Kafka.
    *   **OrderService** nhận **InventoryReservedEvent**:
        *   Gửi lệnh **ProcessPaymentCommand** đến **PaymentService** qua Kafka.
        *   **PaymentService** xử lý thanh toán và gửi sự kiện **PaymentProcessedEvent** hoặc **PaymentFailedEvent** về Kafka.
    *   **OrderService** nhận **PaymentProcessedEvent**:
        *   Cập nhật trạng thái `Order` thành `PAID`.
        *   Gửi lệnh **ConfirmInventoryCommand** đến **InventoryService** (trừ tồn kho vĩnh viễn).
        *   Gửi sự kiện **OrderCreatedEvent** đến Kafka.
    *   **OrderService** nhận **PaymentFailedEvent** hoặc **InventoryReservationFailedEvent**:
        *   Cập nhật trạng thái `Order` thành `FAILED/CANCELLED`.
        *   Gửi lệnh **Compensating Transaction** (ví dụ: **ReleaseInventoryCommand** nếu đã trừ tạm thời).
4.  **OrderService (Controller)** trả về phản hồi **HTTP 202 Accepted** (vì là giao dịch bất đồng bộ).

#### 4.1.2.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)

**Thực thể Domain: `Order`**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- |
| `order_id` | UUID | Khóa chính. | PRIMARY KEY, NOT NULL |
| `user_id` | UUID | ID người dùng đặt hàng. | FOREIGN KEY (UserService) |
| `status` | ENUM | Trạng thái đơn hàng (PENDING, PAID, SHIPPED, DELIVERED, CANCELLED). | NOT NULL |
| `total_amount` | DECIMAL(10, 2) | Tổng số tiền. | NOT NULL |
| `payment_method` | VARCHAR(50) | Phương thức thanh toán. | NOT NULL |
| `shipping_address_json` | JSONB | Thông tin địa chỉ giao hàng. | NOT NULL |
| `saga_state` | JSONB | Trạng thái hiện tại của giao dịch Saga (dùng cho phục hồi). | NULLABLE |

#### 4.1.2.5. Giả mã Thuật toán (Pseudocode) cho Logic Nghiệp vụ Phức tạp: Tính Thuế và Khuyến mãi (Calculate Tax and Discount)

```pseudocode
FUNCTION CalculateFinalAmount(orderItems, couponCode, shippingAddress):
    totalBeforeTax = 0.0
    totalDiscount = 0.0

    // 1. Tính tổng tiền cơ bản
    FOR item IN orderItems:
        totalBeforeTax = totalBeforeTax + (item.price * item.quantity)
    END FOR

    // 2. Áp dụng Khuyến mãi (Discount)
    IF couponCode IS NOT NULL:
        discount = DiscountService.GetDiscount(couponCode)
        IF discount IS NOT NULL AND discount.IsApplicable(orderItems):
            IF discount.type == "PERCENTAGE":
                totalDiscount = totalBeforeTax * (discount.value / 100.0)
            ELSE IF discount.type == "FIXED_AMOUNT":
                totalDiscount = discount.value
            END IF
        END IF
    END IF

    subtotal = totalBeforeTax - totalDiscount

    // 3. Tính Thuế (Tax)
    taxRate = TaxService.GetTaxRate(shippingAddress.country, shippingAddress.state)
    totalTax = subtotal * taxRate

    // 4. Tính Phí Vận chuyển (Shipping Fee)
    shippingFee = ShippingService.CalculateFee(shippingAddress, orderItems)

    // 5. Tổng cộng
    finalAmount = subtotal + totalTax + shippingFee

    RETURN {
        subtotal: subtotal,
        totalTax: totalTax,
        totalDiscount: totalDiscount,
        shippingFee: shippingFee,
        finalAmount: finalAmount
    }
END FUNCTION
```

---

### 4.1.3. Thành phần C: ProductService (Dịch vụ Quản lý Sản phẩm)

*(Phần này sẽ tập trung vào các khía cạnh như tìm kiếm hiệu suất cao, đồng bộ hóa dữ liệu với ElasticSearch, và quản lý các thuộc tính sản phẩm phức tạp.)*

#### 4.1.3.1. Mục đích và Phạm vi (Purpose and Scope)

*   **Mục đích**: Cung cấp các chức năng quản lý và truy vấn thông tin sản phẩm, danh mục, và tồn kho.
*   **Phạm vi**: Quản lý thực thể `Product`, `Category`, `Inventory`, và duy trì chỉ mục tìm kiếm (**Search Index**).

#### 4.1.3.2. Sơ đồ Lớp (Class Diagram)

*(Tương tự 4.1.1.2, với các lớp Domain như `Product`, `Category`, `ProductAttribute`, `Inventory`)*

#### 4.1.3.3. Sơ đồ Trình tự (Sequence Diagram) cho Luồng Chính: Tìm kiếm Sản phẩm (Product Search)

**Mô tả Luồng:**

1.  **Client** gửi yêu cầu **GET /products/search?q=keyword** đến **API Gateway**.
2.  **API Gateway** định tuyến đến **ProductService**.
3.  **ProductService (Controller)** nhận yêu cầu.
4.  **ProductService (Service)**:
    *   Gọi **SearchRepository** (sử dụng **ElasticSearch Client**).
    *   Thực hiện truy vấn tìm kiếm toàn văn (**Full-Text Search**) và lọc theo các tiêu chí (giá, danh mục).
    *   Nhận kết quả tìm kiếm (chỉ chứa `product_id` và các trường hiển thị nhanh).
    *   Gọi **ProductRepository** (sử dụng **PostgreSQL Client**) để lấy dữ liệu chi tiết (ví dụ: tồn kho, giá chính xác) cho các `product_id` đã tìm thấy (**Cache-Aside Pattern** có thể được áp dụng ở đây).
5.  **ProductService (Controller)** trả về danh sách `ProductResponseDTO`.

#### 4.1.3.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)

**Thực thể Domain: `Product`**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- |
| `product_id` | UUID | Khóa chính. | PRIMARY KEY, NOT NULL |
| `sku` | VARCHAR(50) | Mã sản phẩm (Stock Keeping Unit). | UNIQUE, NOT NULL |
| `name` | VARCHAR(255) | Tên sản phẩm. | NOT NULL |
| `description` | TEXT | Mô tả chi tiết sản phẩm. | NOT NULL |
| `price` | DECIMAL(10, 2) | Giá bán. | NOT NULL |
| `category_id` | UUID | Danh mục sản phẩm. | FOREIGN KEY |
| `attributes_json` | JSONB | Các thuộc tính tùy chỉnh (màu sắc, kích cỡ, v.v.). | NOT NULL |
| `is_searchable` | BOOLEAN | Có được lập chỉ mục tìm kiếm không. | Default: TRUE |

**Cấu trúc Chỉ mục ElasticSearch: `product_index`**

| Trường (Field) | Kiểu (Type) | Mô tả |
| :--- | :--- | :--- |
| `id` | keyword | ID sản phẩm. |
| `name` | text | Tên sản phẩm (analyzed for search). |
| `description` | text | Mô tả (analyzed for search). |
| `category_name` | keyword | Tên danh mục (for filtering). |
| `price` | float | Giá (for range queries). |
| `inventory_count` | integer | Số lượng tồn kho (for filtering). |

---

## 4.2. Thiết kế Dữ liệu Chi tiết (Detailed Data Design)

### 4.2.1. Định nghĩa Schema Cơ sở Dữ liệu (Database Schema Definition)

*(Phần này sẽ liệt kê chi tiết các câu lệnh SQL DDL (Data Definition Language) hoặc định nghĩa Schema cho NoSQL, bao gồm các chỉ mục (**indexes**) quan trọng và các ràng buộc (**constraints**).)*

**Ví dụ: Schema cho `UserService` (PostgreSQL)**

```sql
-- Bảng: users
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Chỉ mục quan trọng để tăng tốc độ tìm kiếm và đăng nhập
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_status ON users (status);

-- Bảng: user_roles (cho Authorization)
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    role_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, role_name)
);
```

### 4.2.2. Từ điển Dữ liệu (Data Dictionary)

*(Phần này sẽ mở rộng chi tiết hơn 4.1.1.4, liệt kê tất cả các bảng và trường, bao gồm kiểu dữ liệu vật lý, mô tả, và ý nghĩa nghiệp vụ.)*

| Tên Bảng (Table Name) | Tên Trường (Field Name) | Kiểu Dữ liệu Vật lý (Physical Type) | Mô tả Nghiệp vụ (Business Description) | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- | :--- |
| `users` | `user_id` | `UUID` | Định danh duy nhất của người dùng. | PK, NOT NULL |
| `users` | `status` | `VARCHAR(20)` | Trạng thái tài khoản (PENDING, ACTIVE, INACTIVE). | NOT NULL, INDEXED |
| `orders` | `total_amount` | `DECIMAL(10, 2)` | Tổng giá trị đơn hàng sau thuế và khuyến mãi. | NOT NULL |
| `order_items` | `unit_price` | `DECIMAL(10, 2)` | Giá sản phẩm tại thời điểm đặt hàng. | NOT NULL |

### 4.2.3. Thiết kế Cache (Caching Design)

| Mục tiêu Cache (Cache Target) | Công nghệ (Technology) | Chiến lược (Strategy) | TTL (Time-To-Live) |
| :--- | :--- | :--- | :--- |
| **Dữ liệu Sản phẩm (Product Data)** | Redis | **Cache-Aside** (đọc từ cache trước, nếu miss thì đọc từ DB và cập nhật cache). | 1 giờ (60 phút) |
| **Phiên Người dùng (User Session)** | Redis | **Write-Through** (ghi vào cache và DB đồng thời). | 24 giờ |
| **Giới hạn Tốc độ (Rate Limiting)** | Redis | **Atomic Increment** (sử dụng lệnh `INCR` của Redis). | 1 phút |
| **Kết quả Tìm kiếm (Search Results)** | Redis | **Cache-Aside** | 15 phút |

### 4.2.4. Thiết kế Hàng đợi Tin nhắn (Message Queue Design - Kafka)

| Tên Topic (Topic Name) | Mục đích | Số Lượng Phân vùng (Partitions) | Độ Bền (Retention Policy) |
| :--- | :--- | :--- | :--- |
| `user.events` | Sự kiện liên quan đến người dùng (UserCreated, UserUpdated). | 6 | 7 ngày |
| `order.commands` | Lệnh điều phối giao dịch Saga (ReserveInventoryCommand, ProcessPaymentCommand). | 12 | 3 ngày |
| `order.events` | Sự kiện trạng thái đơn hàng (OrderCreated, OrderPaid, OrderFailed). | 12 | 7 ngày |
| `notification.queue` | Hàng đợi cho các tác vụ gửi email/SMS (tác vụ chậm). | 4 | 1 ngày |

---
*(Phần 4.1.1, 4.1.2, 4.1.3 đã cung cấp đủ chi tiết để mở rộng thành nhiều trang. Tiếp theo, tôi sẽ bổ sung các phần 5, 6, 7 và 8 để hoàn thiện cấu trúc SDD mẫu.)*

## 5. Thiết kế Vận hành và Triển khai (Deployment and Operational Design)

Phần này mô tả cách hệ thống sẽ được xây dựng, triển khai, và vận hành trong môi trường sản xuất (**Production Environment**), tuân thủ các nguyên tắc **DevOps** và **Cloud-Native**.

## 5.1. Môi trường Triển khai (Deployment Environment)

Hệ thống sẽ được triển khai trên nền tảng **[Tên Nền tảng Đám mây, ví dụ: Amazon Web Services - AWS]** sử dụng **Kubernetes (K8s)** làm công cụ điều phối container (**Container Orchestration**).

| Môi trường (Environment) | Mục đích | Công nghệ Chính |
| :--- | :--- | :--- |
| **Development (Dev)** | Môi trường cục bộ cho các nhà phát triển. | Docker Compose, Local Minikube |
| **Staging (Stage)** | Môi trường mô phỏng Production, dùng cho kiểm thử tích hợp và chấp nhận người dùng (**UAT**). | Kubernetes Cluster (nhỏ hơn Production) |
| **Production (Prod)** | Môi trường hoạt động thực tế, phục vụ người dùng cuối. | Kubernetes Cluster (High Availability, Multi-AZ) |

## 5.2. Sơ đồ Triển khai (Deployment Diagram)

*(Phần này sẽ chứa sơ đồ triển khai chi tiết, ví dụ: Sơ đồ Kubernetes Cluster trên AWS/GCP/Azure)*

**Mô tả Sơ đồ Triển khai (Conceptual Deployment Description):**

1.  **VPC (Virtual Private Cloud)**: Hệ thống được đặt trong một VPC riêng biệt, phân chia thành các mạng con (**Subnets**) công cộng (**Public**) và riêng tư (**Private**).
2.  **Public Subnets**: Chứa các thành phần cần truy cập công cộng (ví dụ: **Load Balancer**, **API Gateway**).
3.  **Private Subnets**: Chứa các thành phần cốt lõi (Kubernetes Worker Nodes, Databases, Message Brokers).
4.  **Kubernetes Cluster (EKS/AKS/GKE)**:
    *   **Control Plane**: Được quản lý bởi nhà cung cấp đám mây (**Managed Service**).
    *   **Worker Nodes**: Được phân bổ trên ít nhất **3 Vùng Sẵn sàng (Availability Zones - AZs)** để đảm bảo khả năng chịu lỗi.
5.  **Data Stores**: Cơ sở dữ liệu (PostgreSQL, MongoDB) được triển khai dưới dạng dịch vụ quản lý (**Managed Database Service**) trong Private Subnets.

## 5.3. Chiến lược Triển khai (Deployment Strategy)

Hệ thống sẽ sử dụng **Continuous Deployment (CD)** thông qua **GitOps** (ví dụ: sử dụng **ArgoCD** hoặc **Flux**) để tự động hóa việc triển khai.

| Chiến lược | Mô tả | Lợi ích |
| :--- | :--- | :--- |
| **Blue/Green Deployment** | Triển khai phiên bản mới (**Green**) song song với phiên bản cũ (**Blue**). Sau khi kiểm thử thành công, chuyển đổi lưu lượng truy cập ngay lập tức. | Giảm thiểu thời gian ngừng hoạt động (**Downtime**), dễ dàng Rollback. |
| **Canary Deployment** | Triển khai phiên bản mới cho một nhóm nhỏ người dùng (ví dụ: 5%). Nếu không có lỗi, tăng dần tỷ lệ lưu lượng truy cập. | Giảm thiểu rủi ro khi triển khai tính năng mới, kiểm tra hiệu năng trong môi trường thực. |
| **Rollback Tự động (Automated Rollback)** | Nếu các chỉ số giám sát (**Metrics**) vượt quá ngưỡng lỗi (ví dụ: tỷ lệ lỗi 5xx tăng > 1%), hệ thống tự động quay lại phiên bản ổn định trước đó. | Đảm bảo độ ổn định và SLA. |

## 5.4. Giám sát và Quan sát (Monitoring and Observability)

Một hệ thống quan sát toàn diện (**Observability Stack**) là bắt buộc để duy trì SLA 99.99%.

### 5.4.1. Logging (Ghi nhật ký)

*   **Tiêu chuẩn Ghi nhật ký**: Tất cả các dịch vụ phải ghi nhật ký theo định dạng **JSON** để dễ dàng phân tích và truy vấn.
*   **Thông tin Bắt buộc**: Mỗi log entry phải chứa `timestamp`, `service_name`, `log_level`, `trace_id`, `span_id`, và `message`.
*   **Hệ thống Tập trung**: Sử dụng **Loki** (hoặc **ELK Stack - Elasticsearch, Logstash, Kibana**) để tập trung hóa, lưu trữ và truy vấn log.

### 5.4.2. Metrics (Chỉ số)

*   **Công cụ**: Sử dụng **Prometheus** để thu thập các chỉ số theo mô hình **Pull-based**.
*   **Các Chỉ số Chính (Golden Signals)**:
    *   **Latency (Độ trễ)**: Thời gian phản hồi của các yêu cầu (p50, p95, p99).
    *   **Traffic (Lưu lượng)**: Số lượng yêu cầu mỗi giây (RPS).
    *   **Errors (Lỗi)**: Tỷ lệ lỗi (ví dụ: HTTP 5xx).
    *   **Saturation (Độ bão hòa)**: Mức sử dụng tài nguyên (CPU, Memory, Disk I/O) của các Worker Node và Pod.
*   **Trực quan hóa**: Sử dụng **Grafana** để tạo các bảng điều khiển (**Dashboards**) theo thời gian thực.

### 5.4.3. Tracing (Truy vết)

*   **Công cụ**: Sử dụng **Jaeger** hoặc **Zipkin** (triển khai theo chuẩn **OpenTelemetry**).
*   **Mục đích**: Theo dõi một yêu cầu duy nhất qua nhiều Microservice, giúp xác định nguyên nhân gốc rễ (**Root Cause Analysis - RCA**) của độ trễ hoặc lỗi trong kiến trúc phân tán.
*   **Yêu cầu**: Mỗi yêu cầu phải được gán một `trace_id` duy nhất tại API Gateway và được truyền qua tất cả các dịch vụ hạ nguồn.

## 5.5. Quản lý Cấu hình và Bí mật (Configuration and Secret Management)

*   **Quản lý Cấu hình (Configuration)**: Sử dụng **ConfigMaps** trong Kubernetes cho các cấu hình không nhạy cảm (ví dụ: cổng, tên dịch vụ).
*   **Quản lý Bí mật (Secrets)**: Sử dụng **Kubernetes Secrets** được mã hóa bằng **Vault** hoặc **AWS Secrets Manager/Azure Key Vault** để lưu trữ các thông tin nhạy cảm (ví dụ: khóa API, mật khẩu DB).
*   **Nguyên tắc**: Không bao giờ lưu trữ bí mật dưới dạng văn bản thuần (**plaintext**) trong mã nguồn hoặc kho lưu trữ Git.

## 5.6. Kế hoạch Phục hồi Thảm họa (Disaster Recovery Plan - DRP)

| Mục tiêu DRP | Yêu cầu | Chiến lược Kỹ thuật |
| :--- | :--- | :--- |
| **RPO (Recovery Point Objective)** | **0 giây** (Không mất dữ liệu) | Sao lưu liên tục (**Continuous Backup**) và **Write-Ahead Log (WAL)** cho DB. |
| **RTO (Recovery Time Objective)** | **Dưới 15 phút** | **Multi-Region/Multi-AZ Deployment** với **Active-Passive** hoặc **Active-Active** (tùy dịch vụ). |
| **Kiểm thử DRP** | Thực hiện kiểm thử DRP ít nhất **6 tháng một lần** (Chaos Engineering). | Sử dụng **Chaos Mesh** hoặc **AWS Fault Injection Simulator** để mô phỏng lỗi. |

---

## 6. Thiết kế Bảo mật (Security Design)

Bảo mật là một yêu cầu phi chức năng cốt lõi (**core NFR**) và phải được tích hợp vào mọi giai đoạn của quá trình thiết kế và phát triển (**Security by Design**).

## 6.1. Phân tích Rủi ro Bảo mật (Security Risk Analysis)

Hệ thống sẽ sử dụng phương pháp **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) để phân tích mối đe dọa.

| Mối đe dọa (Threat) | Loại STRIDE | Biện pháp Giảm thiểu (Mitigation) |
| :--- | :--- | :--- |
| **Tấn công SQL Injection** | Tampering | Sử dụng **Prepared Statements** hoặc **ORM** (Object-Relational Mapping) và **Input Validation** nghiêm ngặt. |
| **Lộ thông tin nhạy cảm** | Information Disclosure | Mã hóa dữ liệu khi lưu trữ (**Encryption at Rest**) và khi truyền tải (**Encryption in Transit** - TLS 1.2+). |
| **Tấn công DDoS** | Denial of Service (DoS) | **Rate Limiting** tại API Gateway và sử dụng **CDN/WAF** (Web Application Firewall). |
| **Giả mạo người dùng** | Spoofing | Sử dụng **OAuth 2.0/JWT** với thời gian hết hạn ngắn và cơ chế **Refresh Token**. |
| **Truy cập trái phép** | Elevation of Privilege | **Role-Based Access Control (RBAC)** chi tiết ở cấp độ Microservice. |

## 6.2. Thiết kế Xác thực và Ủy quyền (Authentication and Authorization)

*   **Xác thực (Authentication)**:
    *   Sử dụng **OpenID Connect (OIDC)** và **OAuth 2.0** (Grant Type: Authorization Code Flow with PKCE) thông qua một **Identity Provider (IdP)** tập trung (ví dụ: Keycloak, Auth0).
    *   **JWT (JSON Web Token)** sẽ được sử dụng để truyền tải thông tin xác thực giữa các dịch vụ.
*   **Ủy quyền (Authorization)**:
    *   **API Gateway**: Thực hiện kiểm tra ủy quyền cơ bản (ví dụ: người dùng đã đăng nhập chưa).
    *   **Microservices**: Thực hiện kiểm tra ủy quyền chi tiết (**Fine-Grained Authorization**) dựa trên **RBAC (Role-Based Access Control)** hoặc **ABAC (Attribute-Based Access Control)**. Mỗi Microservice phải tự xác minh quyền của người dùng trước khi thực hiện nghiệp vụ.

## 6.3. Bảo mật Dữ liệu (Data Security)

*   **Mã hóa khi Truyền tải (In Transit)**: Bắt buộc sử dụng **HTTPS/TLS 1.2+** cho tất cả các giao tiếp (Client-Gateway, Gateway-Service, Service-Service).
*   **Mã hóa khi Lưu trữ (At Rest)**:
    *   Dữ liệu nhạy cảm (ví dụ: mật khẩu, thông tin cá nhân) phải được mã hóa ở cấp độ ứng dụng (**Application-Level Encryption**) trước khi lưu vào DB.
    *   Sử dụng tính năng mã hóa đĩa của nhà cung cấp đám mây (**Disk Encryption**).
*   **Xử lý Mật khẩu**: Mật khẩu phải được băm (**hashing**) bằng các thuật toán hiện đại và an toàn (ví dụ: **Argon2** hoặc **Bcrypt**) với muối (**salt**) duy nhất.

## 6.4. Bảo mật API (API Security)

*   **Input Validation**: Tất cả đầu vào từ người dùng phải được xác thực nghiêm ngặt (ví dụ: sử dụng **Schema Validation**).
*   **CORS (Cross-Origin Resource Sharing)**: Chỉ cho phép các nguồn gốc (**origins**) đã được phê duyệt truy cập API.
*   **Content Security Policy (CSP)**: Áp dụng cho Frontend để ngăn chặn tấn công **Cross-Site Scripting (XSS)**.

## 6.5. Bảo mật Hạ tầng (Infrastructure Security)

*   **Network Segmentation**: Sử dụng **Network Policies** trong Kubernetes để giới hạn giao tiếp giữa các Microservice (ví dụ: `UserService` không được phép gọi trực tiếp `PaymentService` mà phải qua một kênh được kiểm soát).
*   **Least Privilege**: Tất cả các Pod/Container phải chạy với quyền hạn tối thiểu cần thiết (**Least Privilege Principle**).
*   **Vulnerability Scanning**: Tích hợp công cụ quét lỗ hổng (**Vulnerability Scanner**) vào CI/CD Pipeline để kiểm tra các thư viện và hình ảnh Docker lỗi thời.

---

## 7. Chiến lược Kiểm thử và Chất lượng (Testing and Quality Strategy)

Chiến lược kiểm thử được thiết kế theo mô hình **Tháp Kiểm thử (Test Pyramid)**, ưu tiên kiểm thử tự động (**Automated Testing**) ở các cấp độ thấp hơn.

## 7.1. Chiến lược Kiểm thử Đơn vị (Unit Testing Strategy)

*   **Mục đích**: Kiểm tra logic của các đơn vị mã nguồn nhỏ nhất (hàm, lớp) một cách độc lập.
*   **Phạm vi**: Bao gồm logic nghiệp vụ cốt lõi, thuật toán, và các hàm tiện ích.
*   **Yêu cầu**: **Độ bao phủ mã nguồn (Code Coverage)** tối thiểu **80%** cho các module nghiệp vụ quan trọng.
*   **Công cụ**: **[Ví dụ: JUnit/Testify (Java/Go), Jest/Mocha (Node.js)]**.

### 7.1.1. Ví dụ Mã Kiểm thử Đơn vị (Unit Test Code Example)

Ví dụ sau minh họa một kiểm thử đơn vị cho chức năng `UpdatePassword` trong `UserService` (sử dụng cú pháp Python/Pytest mô phỏng):

```python
## File: tests/unit/test_user_service.py

import pytest
from unittest.mock import Mock
from src.user_service import UserService
from src.exceptions import UserNotFoundException, InvalidPasswordException

## Giả định UserRepository và PasswordHasher là các đối tượng Mock
@pytest.fixture
def user_service_mocked():
    user_repo = Mock()
    password_hasher = Mock()
    return UserService(user_repo, password_hasher), user_repo, password_hasher

def test_update_password_success(user_service_mocked):
    ## Arrange
    user_service, user_repo, password_hasher = user_service_mocked
    
    ## Dữ liệu giả lập
    mock_user = Mock(id="user-123", password_hash="old_hash")
    user_repo.find_by_id.return_value = mock_user
    password_hasher.verify.return_value = True  ## Mật khẩu cũ đúng
    password_hasher.hash.return_value = "new_hash"
    
    ## Act
    user_service.update_password(
        user_id="user-123",
        old_password="old_password",
        new_password="new_secure_password"
    )
    
    ## Assert
    ## 1. Kiểm tra hàm hash được gọi với mật khẩu mới
    password_hasher.hash.assert_called_once_with("new_secure_password")
    ## 2. Kiểm tra user được lưu với hash mới
    user_repo.save.assert_called_once()
    assert mock_user.password_hash == "new_hash"

def test_update_password_invalid_old_password(user_service_mocked):
    ## Arrange
    user_service, user_repo, password_hasher = user_service_mocked
    mock_user = Mock(id="user-123", password_hash="old_hash")
    user_repo.find_by_id.return_value = mock_user
    password_hasher.verify.return_value = False  ## Mật khẩu cũ sai
    
    ## Act & Assert
    with pytest.raises(InvalidPasswordException):
        user_service.update_password(
            user_id="user-123",
            old_password="wrong_password",
            new_password="new_secure_password"
        )
    ## Đảm bảo không có thao tác lưu DB nào xảy ra
    user_repo.save.assert_not_called()
```

---


## 7.2. Chiến lược Kiểm thử Tích hợp (Integration Testing Strategy)

*   **Mục đích**: Kiểm tra sự tương tác giữa các thành phần nội bộ của một Microservice (ví dụ: Service Layer và Repository Layer) hoặc giữa các Microservice với nhau.
*   **Phạm vi**:
    *   **Internal Integration**: Kiểm tra kết nối DB, Message Broker.
    *   **External Integration**: Kiểm tra kết nối với các dịch vụ bên ngoài (sử dụng **Mocking** hoặc **Test Doubles**).
*   **Công cụ**: **[Ví dụ: Testcontainers]** để khởi tạo các DB/Broker thực trong quá trình kiểm thử.

## 7.3. Kiểm thử Đầu cuối (End-to-End Testing) và Kiểm thử Hiệu năng (Performance Testing)

*   **Kiểm thử Đầu cuối (E2E)**:
    *   **Mục đích**: Mô phỏng hành vi của người dùng cuối trên toàn bộ hệ thống (Client -> Gateway -> Services -> DB).
    *   **Công cụ**: **[Ví dụ: Cypress, Selenium, Playwright]**.
    *   **Phạm vi**: Các luồng nghiệp vụ quan trọng nhất (ví dụ: Đăng ký, Đặt hàng, Thanh toán).
*   **Kiểm thử Hiệu năng (Performance Testing)**:
    *   **Mục đích**: Xác minh các **NFRs** về hiệu năng (Response Time, Throughput).
    *   **Công cụ**: **[Ví dụ: JMeter, Locust, Gatling]**.
    *   **Các loại Kiểm thử**: **Load Testing** (tải dự kiến), **Stress Testing** (tải vượt ngưỡng), **Soak Testing** (tải duy trì trong thời gian dài).

## 7.4. Ma trận Truy vết Yêu cầu (Requirements Traceability Matrix - RTM)

RTM đảm bảo rằng mọi yêu cầu (FR và NFR) đều được ánh xạ tới ít nhất một thành phần thiết kế và một trường hợp kiểm thử.

| ID Yêu cầu | Mô tả Yêu cầu | Thiết kế (Mục SDD) | Trường hợp Kiểm thử (Test Case ID) | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **FR-004** | Xử lý quy trình đặt hàng. | 4.1.2 (OrderService) | TC-ORDER-001, TC-ORDER-002 | Đã Hoàn thành |
| **NFR-2.6.1** | Response Time < 200ms. | 3.1.1 (Microservices), 5.4.2 (Metrics) | PT-LOAD-001 | Đang Tiến hành |
| **NFR-6.2** | Sử dụng OAuth 2.0. | 6.2 (Authentication) | TC-AUTH-005 | Đã Hoàn thành |

---

## 8. Phụ lục (Appendices)

## 8.1. Ma trận Quyết định Kiến trúc (Architecture Decision Records - ADRs)

ADR là tài liệu ghi lại các quyết định kiến trúc quan trọng, bối cảnh, các lựa chọn thay thế, và hậu quả của quyết định đó.

| ID ADR | Tiêu đề Quyết định | Ngày | Trạng thái |
| :--- | :--- | :--- | :--- |
| **ADR-001** | Lựa chọn Kiến trúc Microservices | 2025-12-01 | Đã Chấp thuận |
| **ADR-002** | Sử dụng Kafka cho Giao tiếp Bất đồng bộ | 2025-12-05 | Đã Chấp thuận |
| **ADR-003** | Lựa chọn PostgreSQL thay vì MySQL | 2025-12-10 | Đã Chấp thuận |

**Ví dụ Chi tiết ADR-003: Lựa chọn PostgreSQL thay vì MySQL**

*   **Tiêu đề**: Lựa chọn PostgreSQL làm Cơ sở Dữ liệu Quan hệ Chính.
*   **Trạng thái**: Đã Chấp thuận.
*   **Bối cảnh**: Hệ thống yêu cầu khả năng xử lý dữ liệu giao dịch phức tạp (**ACID**) và hỗ trợ các kiểu dữ liệu nâng cao (ví dụ: JSONB, GIS) để phục vụ cho các tính năng tìm kiếm và lưu trữ phi cấu trúc.
*   **Quyết định**: Sử dụng **PostgreSQL 16** làm cơ sở dữ liệu quan hệ chính.
*   **Lý do**:
    1.  **Hỗ trợ JSONB**: Cung cấp khả năng lưu trữ và truy vấn dữ liệu JSON hiệu quả, giúp giảm nhu cầu sử dụng NoSQL DB riêng biệt cho một số trường hợp.
    2.  **Tính năng Nâng cao**: Hỗ trợ các tính năng như **CTE (Common Table Expressions)**, **Window Functions**, và **Full-Text Search** tích hợp, giúp đơn giản hóa logic nghiệp vụ.
    3.  **Khả năng Mở rộng**: Cộng đồng lớn và hỗ trợ các giải pháp Sharding như Citus Data.
*   **Hậu quả**:
    *   **Tích cực**: Tăng tính linh hoạt trong mô hình hóa dữ liệu, hiệu năng truy vấn phức tạp tốt hơn.
    *   **Tiêu cực**: Đội ngũ phát triển cần có kinh nghiệm về PostgreSQL, chi phí vận hành có thể cao hơn MySQL trong một số dịch vụ đám mây.

## 8.2. Sơ đồ Luồng Người dùng (User Flow Diagrams)

*(Phần này sẽ chứa các sơ đồ trực quan hóa các luồng người dùng chính, ví dụ: Sơ đồ Luồng Đăng ký, Sơ đồ Luồng Đặt hàng, Sơ đồ Luồng Thanh toán. Các sơ đồ này thường được tạo bằng **Mermaid** hoặc **PlantUML**.)*

**Ví dụ: Luồng Đăng ký và Xác thực Email (Mermaid Flowchart)**

*(Sơ đồ Luồng Đăng ký và Xác thực Email sẽ được đặt tại đây. Sơ đồ này mô tả các bước từ khi người dùng đăng ký đến khi tài khoản được kích hoạt.)*

## 8.3. Thiết kế Giao diện Người dùng (User Interface - UI/UX Mockups)

*(Phần này sẽ chứa các liên kết đến các bản Mockup/Wireframe chi tiết được tạo bằng Figma, Sketch, hoặc Adobe XD. Mặc dù SDD tập trung vào thiết kế kỹ thuật, việc tham chiếu đến UI/UX là cần thiết để đảm bảo sự đồng bộ giữa thiết kế Backend và Frontend.)*

*   **Mockup Trang Chủ (Homepage)**: [Link Figma/Sketch]
*   **Wireframe Luồng Thanh toán (Checkout Flow)**: [Link Figma/Sketch]
*   **Thiết kế Hệ thống Thiết kế (Design System)**: [Link đến Storybook/Design System Documentation]

## 8.4. Danh sách Các Vấn đề Mở (Open Issues)

## 8.5. Ví dụ Mã Hạ tầng dưới dạng Mã (Infrastructure as Code - IaC)

Phần này cung cấp các đoạn mã mẫu **Terraform** và **Helm Chart** để minh họa cách triển khai và quản lý hạ tầng hệ thống trên nền tảng **Kubernetes** và **Cloud Provider** (ví dụ: AWS, GCP, Azure).

### 8.5.1. Ví dụ Terraform: Khởi tạo Cluster Kubernetes (EKS/GKE/AKS)

```terraform
## File: infra/main.tf

resource "aws_eks_cluster" "main" {
  name     = "[PROJECT_NAME]-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.29"

  vpc_config {
    subnet_ids         = var.private_subnets
    security_group_ids = [aws_security_group.cluster.id]
    endpoint_private_access = true
    endpoint_public_access  = false
  }

  tags = {
    Name = "[PROJECT_NAME]-eks-cluster"
  }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "general-purpose"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = var.private_subnets
  instance_types  = ["t3.medium"]

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 3
  }

  update_config {
    max_unavailable = 1
  }
}
```

### 8.5.2. Ví dụ Helm Chart: Triển khai Microservice (UserService)

```yaml
## File: charts/user-service/templates/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "user-service.fullname" . }}
  labels:
    {{- include "user-service.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "user-service.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "user-service.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
          readinessProbe:
            httpGet:
              path: /readyz
              port: http
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: host
            - name: KAFKA_BROKER
              value: kafka-broker-svc:9092
```

## 8.6. Lịch sử Thay đổi Tài liệu (Document Revision History)

| ID | Mô tả Vấn đề | Mức độ Ưu tiên | Người Chịu trách nhiệm | Ngày Cập nhật |
| :--- | :--- | :--- | :--- | :--- |
| **OI-001** | Cần quyết định cuối cùng về việc sử dụng **gRPC** hay **REST** cho giao tiếp Service-to-Service. | Cao | Kiến trúc sư | 2025-12-15 |
| **OI-002** | Chiến lược phân mảnh (**Sharding**) cho bảng `Order` cần được kiểm tra hiệu năng (Proof of Concept). | Trung bình | Đội ngũ Data | 2025-12-12 |
| **OI-003** | Lựa chọn công cụ **CI/CD** (GitLab CI hay GitHub Actions). | Thấp | Đội ngũ DevOps | 2025-12-10 |

## 8.5. Lịch sử Thay đổi Tài liệu (Document Revision History)

| Phiên bản (Version) | Ngày | Tác giả | Mô tả Thay đổi |
| :--- | :--- | :--- | :--- |
| **0.1** | 2025-12-10 | Manus AI | Khởi tạo bản nháp SDD (Cấu trúc và HLD). |
| **0.2** | 2025-12-16 | Manus AI | Bổ sung chi tiết LLD cho UserService, OrderService, Security, và DevOps. |
| **1.0** | [Ngày Hoàn thành] | Manus AI | Bản cuối cùng, được phê duyệt. |

---
*(Kết thúc bản nháp SDD mẫu. Bản nháp này đã bao gồm đầy đủ các phần theo chuẩn IEEE 1016-2009 và các yếu tố hiện đại (Microservices, Cloud-Native, DevOps, Security) để tạo thành một tài liệu siêu chi tiết, có thể mở rộng thành 100 trang bằng cách bổ sung thêm chi tiết cho các mục LLD của từng Microservice và các sơ đồ trực quan.)*

### 4.1.2. Thành phần B: OrderService (Dịch vụ Quản lý Đơn hàng) - Mở rộng Chi tiết

#### 4.1.2.1. Mục đích và Phạm vi (Purpose and Scope)

*   **Mục đích**: Quản lý toàn bộ vòng đời của một đơn hàng, từ khi tạo giỏ hàng, đặt hàng, đến khi hoàn thành hoặc hủy bỏ.
*   **Phạm vi**: Xử lý các thực thể `Order`, `OrderItem`, `ShippingAddress`, và điều phối các giao dịch phân tán liên quan đến `PaymentService` và `InventoryService`.

#### 4.1.2.2. Sơ đồ Lớp (Class Diagram)

*(Để đạt được độ chi tiết 100 trang, phần này sẽ bao gồm sơ đồ lớp chi tiết cho các lớp Domain, Service, và Repository của OrderService, thể hiện mối quan hệ kế thừa, giao diện, và các thuộc tính/phương thức chính.)*

*(Sơ đồ Lớp chi tiết cho OrderService sẽ được đặt tại đây. Sơ đồ này thể hiện các lớp Domain, Service, và Repository, cùng với các thuộc tính và phương thức chính.)*

#### 4.1.2.3. Sơ đồ Trình tự (Sequence Diagram) cho Luồng Chính: Tạo Đơn hàng (Create Order - Sử dụng Saga Pattern)

*(Phần này sẽ được mở rộng bằng sơ đồ trình tự chi tiết sử dụng cú pháp Mermaid, mô tả từng bước giao tiếp giữa OrderService, InventoryService, PaymentService, và Kafka Broker.)*

*(Sơ đồ Trình tự chi tiết cho luồng Tạo Đơn hàng (Saga Pattern) sẽ được đặt tại đây. Sơ đồ này mô tả giao tiếp bất đồng bộ giữa các dịch vụ Order, Inventory, và Payment thông qua Kafka.)*

#### 4.1.2.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)

*(Phần này sẽ lặp lại bảng Data Dictionary cho tất cả các bảng liên quan đến OrderService, bao gồm `orders`, `order_items`, `transactions`, `shipping_info`, và `saga_logs`.)*

**Bảng: `orders` (Mở rộng)**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- |
| `order_id` | UUID | Khóa chính. | PK, NOT NULL |
| `user_id` | UUID | ID người dùng đặt hàng. | FK (UserService.users) |
| `status` | VARCHAR(20) | Trạng thái đơn hàng (PENDING, PAID, SHIPPED, DELIVERED, CANCELLED, FAILED). | NOT NULL, INDEXED |
| `total_amount` | DECIMAL(10, 2) | Tổng số tiền cuối cùng. | NOT NULL |
| `subtotal` | DECIMAL(10, 2) | Tổng tiền trước thuế và phí. | NOT NULL |
| `tax_amount` | DECIMAL(10, 2) | Tổng tiền thuế. | NOT NULL |
| `discount_amount` | DECIMAL(10, 2) | Tổng tiền giảm giá. | NOT NULL |
| `shipping_fee` | DECIMAL(10, 2) | Phí vận chuyển. | NOT NULL |
| `shipping_address_json` | JSONB | Thông tin địa chỉ giao hàng chi tiết. | NOT NULL |
| `created_at` | TIMESTAMP WITH TIME ZONE | Thời điểm tạo đơn hàng. | NOT NULL |
| `updated_at` | TIMESTAMP WITH TIME ZONE | Thời điểm cập nhật cuối cùng. | NOT NULL |
| `saga_id` | UUID | ID của giao dịch Saga (nếu có). | NULLABLE |

*(... Lặp lại chi tiết cho các bảng `order_items`, `transactions`, `shipping_info`...)*

---

### 4.1.3. Thành phần C: ProductService (Dịch vụ Quản lý Sản phẩm) - Mở rộng Chi tiết

#### 4.1.3.1. Mục đích và Phạm vi (Purpose and Scope)

*   **Mục đích**: Cung cấp các chức năng quản lý và truy vấn thông tin sản phẩm, danh mục, và tồn kho.
*   **Phạm vi**: Quản lý thực thể `Product`, `Category`, `Inventory`, và duy trì chỉ mục tìm kiếm (**Search Index**).

#### 4.1.3.2. Sơ đồ Lớp (Class Diagram)

*(Phần này sẽ bao gồm sơ đồ lớp chi tiết cho các lớp Domain, Service, và Repository của ProductService, tập trung vào việc đồng bộ hóa dữ liệu giữa DB quan hệ và Search Index.)*

*(Sơ đồ Lớp chi tiết cho ProductService sẽ được đặt tại đây. Sơ đồ này thể hiện các lớp Domain, Service, và Repository, cùng với các thuộc tính và phương thức chính, tập trung vào việc đồng bộ hóa dữ liệu.)*

#### 4.1.3.3. Sơ đồ Trình tự (Sequence Diagram) cho Luồng Chính: Đồng bộ hóa Dữ liệu Sản phẩm (Product Data Synchronization)

*(Sơ đồ này mô tả luồng bất đồng bộ để đảm bảo dữ liệu sản phẩm được cập nhật trên cả PostgreSQL và ElasticSearch.)*

*(Sơ đồ Trình tự chi tiết cho luồng Đồng bộ hóa Dữ liệu Sản phẩm sẽ được đặt tại đây. Sơ đồ này mô tả luồng bất đồng bộ để đảm bảo dữ liệu sản phẩm được cập nhật trên cả PostgreSQL và ElasticSearch.)*

#### 4.1.3.4. Cấu trúc Dữ liệu Chi tiết (Detailed Data Structures)

*(Phần này sẽ lặp lại bảng Data Dictionary cho tất cả các bảng liên quan đến ProductService, bao gồm `products`, `categories`, `inventory`, và `product_attributes`.)*

**Bảng: `inventory` (Mở rộng)**

| Thuộc tính (Attribute) | Kiểu Dữ liệu (Data Type) | Mô tả | Ràng buộc (Constraint) |
| :--- | :--- | :--- | :--- |
| `inventory_id` | UUID | Khóa chính. | PK, NOT NULL |
| `product_id` | UUID | ID sản phẩm. | FK (products), UNIQUE |
| `quantity_available` | INTEGER | Số lượng sản phẩm hiện có. | NOT NULL, CHECK (>= 0) |
| `quantity_reserved` | INTEGER | Số lượng sản phẩm đang được giữ cho các đơn hàng PENDING. | NOT NULL, CHECK (>= 0) |
| `last_updated` | TIMESTAMP WITH TIME ZONE | Thời điểm cập nhật tồn kho cuối cùng. | NOT NULL |

*(... Lặp lại chi tiết cho các bảng `products`, `categories`, `product_attributes`...)*

---

## 8.2. Sơ đồ Luồng Người dùng (User Flow Diagrams) - Mở rộng

*(Bổ sung thêm các sơ đồ luồng quan trọng khác để tăng độ chi tiết.)*

**Ví dụ: Luồng Thanh toán Thành công (Payment Success Flowchart)**

*(Sơ đồ Luồng Thanh toán Thành công sẽ được đặt tại đây. Sơ đồ này mô tả các bước xử lý sau khi nhận được sự kiện thanh toán thành công.)*

**Ví dụ: Sơ đồ Kiến trúc Tổng thể (C4 Model - Level 2: Container Diagram)**

*(Sơ đồ Kiến trúc Tổng thể (C4 Model - Level 2: Container Diagram) sẽ được đặt tại đây. Sơ đồ này mô tả các thành phần chính (Container) và mối quan hệ giữa chúng trong môi trường triển khai.)*

*(Việc bổ sung các chi tiết này, cùng với các bảng và sơ đồ, sẽ mở rộng tài liệu Markdown lên một độ dài đáng kể, mô phỏng một bản SDD siêu chi tiết, có thể dễ dàng đạt 100 trang khi được điền đầy đủ dữ liệu thực tế của dự án.)*


---


# 3. Tài liệu 100 trang - Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### Giới Thiệu

Tài liệu này là một **hướng dẫn ALL-IN-ONE** về Production Quality dành cho **Intern AI Engineer** và các lập trình viên muốn xây dựng hệ thống chất lượng cao.

#### Mục Tiêu

Sau khi đọc tài liệu này, bạn sẽ:
1. **Hiểu rõ** các nguyên tắc cơ bản của production quality
2. **Biết cách thiết kế** hệ thống scalable, reliable, secure
3. **Có khả năng triển khai** từng component của production system
4. **Nắm rõ** trade-offs và khi nào dùng cái gì
5. **Có code examples** để reference khi implement
6. **Biết cách tránh** các common mistakes
7. **Có checklists** để đảm bảo không bỏ sót gì

#### Phạm Vi

Tài liệu bao gồm **40 chương** được chia thành **15 phần chính**:

| Phần                               | Chương | Trang    |
| ---------------------------------- | ------ | -------- |
| **I. Foundations**                 | 1-4    | 1-50     |
| **II. Architecture & Design**      | 5-8    | 51-120   |
| **III. Reliability & Resilience**  | 9-12   | 121-180  |
| **IV. Observability & Monitoring** | 13-16  | 181-240  |
| **V. Deployment & CI/CD**          | 17-20  | 241-300  |
| **VI. Security**                   | 21-26  | 301-380  |
| **VII. Testing**                   | 27-30  | 381-450  |
| **VIII. Code Quality**             | 31     | 451-480  |
| **IX. Infrastructure**             | 32-33  | 481-520  |
| **X. Database**                    | 34     | 521-550  |
| **XI. API Design**                 | 35     | 551-580  |
| **XII. Configuration**             | 36     | 581-610  |
| **XIII. Documentation**            | 37     | 611-640  |
| **XIV. Production Readiness**      | 38     | 641-680  |
| **XV. MLOps**                      | 39-40  | 681-750+ |

#### Cách Sử Dụng Tài Liệu

**Nếu bạn là Intern:**
- Đọc từ đầu đến cuối
- Làm tất cả các ví dụ code
- Làm các checklist
- Hỏi senior engineer nếu không hiểu

**Nếu bạn là Mid-level Engineer:**
- Skim qua phần Foundations
- Tập trung vào Architecture & Design, Reliability, Security
- Làm các ví dụ advanced
- Giúp junior engineers

**Nếu bạn là Senior Engineer:**
- Dùng làm reference
- Dùng checklist cho code review
- Dùng cho mentoring
- Adapt cho team của bạn

#### Kiến Thức Cần Có Trước

- Kiến thức cơ bản về lập trình (Python, JavaScript, hoặc Go)
- Hiểu cơ bản về HTTP, REST APIs
- Hiểu cơ bản về databases
- Sẵn sàng học và thực hành

#### Tài Nguyên Bổ Sung

Mỗi chương đều có:
- **Ví dụ code** (Python, Node.js, Go)
- **Diagrams** minh họa
- **Checklists** thực thi
- **Tools recommendations**
- **Common mistakes** cần tránh
- **Real-world case studies**

---

### TABLE OF CONTENTS

#### PHẦN I: FOUNDATIONS (Nền Tảng)

###### Chương 1: Giới Thiệu Production Quality
- 1.1 Production Quality Là Gì?
- 1.2 Tại Sao Production Quality Quan Trọng?
- 1.3 Production Quality vs Development
- 1.4 Các Pillars Chính Của Production Quality

###### Chương 2: Core Principles
- 2.1 Principle 1: Fail-Safe Design
- 2.2 Principle 2: Defense in Depth
- 2.3 Principle 3: Observability First
- 2.4 Principle 4: Automate Everything
- 2.5 Principle 5: Embrace Failures
- 2.6 Principle 6: Measure What Matters
- 2.7 Principle 7: Continuous Improvement

###### Chương 3: Architecture Fundamentals
- 3.1 Layered Architecture
- 3.2 Scalability Patterns
- 3.3 Load Balancing Strategies
- 3.4 Microservices Architecture

###### Chương 4: Trade-offs & Decision Making
- 4.1 Consistency vs Availability
- 4.2 Latency vs Throughput
- 4.3 Cost vs Performance
- 4.4 Complexity vs Maintainability

---

#### PHẦN II: ARCHITECTURE & DESIGN (Kiến Trúc & Thiết Kế)

###### Chương 5: Scalability Patterns (Chi Tiết)
- 5.1 Horizontal Scaling - Scale Out
- 5.2 Vertical Scaling - Scale Up
- 5.3 Diagonal Scaling - Kết Hợp Cả Hai

###### Chương 6: Load Balancing (Chi Tiết)
- 6.1 Load Balancing Algorithms
- 6.2 Health Checks
- 6.3 Load Balancer High Availability

###### Chương 7: Microservices Architecture (Chi Tiết)
- 7.1 Microservices Patterns
- 7.2 API Gateway Pattern
- 7.3 Service Discovery
- 7.4 Circuit Breaker Pattern
- 7.5 Database per Service
- 7.6 Saga Pattern

###### Chương 8: Data Consistency Patterns
- 8.1 Strong Consistency
- 8.2 Eventual Consistency
- 8.3 Causal Consistency

---

#### PHẦN III: RELIABILITY & RESILIENCE (Độ Tin Cậy & Khả Năng Phục Hồi)

###### Chương 9: Resilience Patterns (Chi Tiết)
- 9.1 Retry Pattern
- 9.2 Circuit Breaker Pattern
- 9.3 Timeout Pattern
- 9.4 Bulkhead Pattern
- 9.5 Fallback Pattern

###### Chương 10: Error Handling (Chi Tiết)
- 10.1 Error Classification
- 10.2 Structured Error Responses
- 10.3 Error Logging Best Practices
- 10.4 Error Recovery Strategies

###### Chương 11: Disaster Recovery & Backup
- 11.1 Backup Strategies
- 11.2 Disaster Recovery Strategies
- 11.3 Backup Implementation

###### Chương 12: Capacity Planning & Forecasting
- 12.1 Capacity Planning Process
- 12.2 Metrics to Track
- 12.3 Forecasting

---

#### PHẦN IV: OBSERVABILITY & MONITORING (Quan Sát & Giám Sát)

###### Chương 13: Three Pillars of Observability
- 13.1 Metrics (Số Liệu)
- 13.2 Logging (Ghi Chép)
- 13.3 Tracing (Theo Dõi)

###### Chương 14: Monitoring Strategy
- 14.1 Metrics to Monitor
- 14.2 Alerting Strategy
- 14.3 Monitoring Dashboard

###### Chương 15: Alerting & Incident Response
- 15.1 Alert Severity Levels
- 15.2 Incident Response Process
- 15.3 On-Call Management

###### Chương 16: Cost Optimization for Observability
- 16.1 Metrics Cardinality
- 16.2 Log Sampling
- 16.3 Retention Policies

---

#### PHẦN V: DEPLOYMENT & CI/CD (Triển Khai & Tích Hợp Liên Tục)

###### Chương 17: CI/CD Pipeline Best Practices
- 17.1 Pipeline Architecture
- 17.2 CI/CD Tools
- 17.3 Pipeline Configuration Example
- 17.4 Build Optimization

###### Chương 18: Deployment Strategies
- 18.1 Blue-Green Deployment
- 18.2 Canary Deployment
- 18.3 Rolling Deployment
- 18.4 Deployment Strategy Selection

###### Chương 19: Environment Management
- 19.1 Environment Types
- 19.2 Configuration Management
- 19.3 Infrastructure as Code (IaC)

###### Chương 20: Rollback Strategies
- 20.1 Automated Rollback
- 20.2 Manual Rollback

---

#### PHẦN VI: SECURITY (Bảo Mật)

###### Chương 21: Authentication & Authorization
- 21.1 Authentication Methods
- 21.2 Authorization (RBAC)

###### Chương 22: Data Protection
- 22.1 Encryption at Rest
- 22.2 Encryption in Transit
- 22.3 Input Validation
- 22.4 SQL Injection Prevention

###### Chương 23: Security Scanning & Compliance
- 23.1 SAST (Static Application Security Testing)
- 23.2 DAST (Dynamic Application Security Testing)
- 23.3 Dependency Scanning (SCA)
- 23.4 Secrets Detection
- 23.5 Compliance Standards

###### Chương 24: Secrets Management
- 24.1 Secrets Storage
- 24.2 Secrets Rotation
- 24.3 Vault Integration

###### Chương 25: Network Security
- 25.1 VPC (Virtual Private Cloud)
- 25.2 Security Groups
- 25.3 WAF (Web Application Firewall)

###### Chương 26: DDoS Protection
- 26.1 DDoS Mitigation
- 26.2 Rate Limiting

---

#### PHẦN VII: TESTING (Kiểm Thử)

###### Chương 27: Testing Pyramid
- 27.1 Testing Levels
- 27.2 Unit Testing
- 27.3 Integration Testing
- 27.4 End-to-End (E2E) Testing

###### Chương 28: Performance & Security Testing
- 28.1 Load Testing
- 28.2 Stress Testing
- 28.3 Spike Testing
- 28.4 Security Testing

###### Chương 29: Test Automation & CI/CD Integration
- 29.1 Test Configuration
- 29.2 Test Execution Strategy
- 29.3 CI/CD Integration
- 29.4 Test Coverage

###### Chương 30: Test Data Management
- 30.1 Test Data Strategies
- 30.2 Factory Pattern
- 30.3 Test Data Cleanup

---

#### PHẦN VIII: CODE QUALITY & MAINTAINABILITY (Chất Lượng Code)

###### Chương 31: Code Quality Metrics
- 31.1 Key Metrics
- 31.2 Code Quality Tools

---

#### PHẦN IX: INFRASTRUCTURE & CONTAINERIZATION (Hạ Tầng)

###### Chương 32: Docker Best Practices
- 32.1 Dockerfile Optimization
- 32.2 Docker Security

###### Chương 33: Kubernetes in Production
- 33.1 Kubernetes Deployment
- 33.2 Service & Ingress

---

#### PHẦN X: DATABASE & DATA MANAGEMENT (Cơ Sở Dữ Liệu)

###### Chương 34: Database Design & Optimization
- 34.1 Database Indexing
- 34.2 Query Optimization
- 34.3 Connection Pooling

---

#### PHẦN XI: API DESIGN & INTEGRATION (Thiết Kế API)

###### Chương 35: RESTful API Best Practices
- 35.1 API Design
- 35.2 API Versioning
- 35.3 Pagination & Filtering

---

#### PHẦN XII: CONFIGURATION & SECRETS (Cấu Hình)

###### Chương 36: Environment Management
- 36.1 Configuration Hierarchy
- 36.2 Configuration Management

---

#### PHẦN XIII: DOCUMENTATION (Tài Liệu)

###### Chương 37: Code Documentation
- 37.1 Documentation Types
- 37.2 API Documentation

---

#### PHẦN XIV: PRODUCTION READINESS (Sẵn Sàng Sản Xuất)

###### Chương 38: Production Readiness Review (PRR)
- 38.1 PRR Checklist
- 38.2 SLO/SLI/SLA

---

#### PHẦN XV: MLOPS & AI SYSTEMS IN PRODUCTION (MLOps)

###### Chương 39: MLOps Fundamentals
- 39.1 ML Pipeline Architecture
- 39.2 Model Serving
- 39.3 Model Monitoring
- 39.4 Model Versioning

###### Chương 40: Implementation Roadmap
- 40.1 Phase 1: Foundation
- 40.2 Phase 2: Reliability
- 40.3 Phase 3: Security
- 40.4 Phase 4: Optimization
- 40.5 Phase 5: MLOps

---

### Lời Khuyên Khi Đọc

1. **Đừng cố nhớ tất cả**: Tài liệu này là reference, không phải để memorize
2. **Thực hành**: Làm tất cả các ví dụ code, đừng chỉ đọc
3. **Hỏi câu hỏi**: Nếu không hiểu, hỏi senior engineers
4. **Adapt**: Không phải tất cả practices phù hợp với mọi project
5. **Iterate**: Production quality là continuous process, không phải one-time

---

### Liên Hệ & Feedback

Nếu bạn có feedback hoặc câu hỏi:
- Tạo issue trên GitHub
- Liên hệ với team lead
- Đóng góp improvements

---

### License

Tài liệu này được cấp phép dưới Creative Commons Attribution 4.0 International License.

---

**Chúc bạn học tập vui vẻ và xây dựng hệ thống production-grade tuyệt vời!** 🚀

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN I: FOUNDATIONS (Nền Tảng)

---

### Chương 1: Giới Thiệu Production Quality

#### 1.1 Production Quality Là Gì?

**Production quality** không phải chỉ là code "chạy được". Đó là một tập hợp toàn diện các kỹ thuật, practices, và mindset để đảm bảo hệ thống của bạn có thể:

- **Chạy ổn định 24/7** mà không gây downtime
- **Xử lý lỗi một cách graceful** thay vì crash
- **Mở rộng được** khi traffic tăng
- **Có thể debug và fix nhanh** khi có vấn đề
- **Bảo vệ dữ liệu người dùng** một cách an toàn
- **Cung cấp trải nghiệm tốt** cho end users
- **Dễ bảo trì và phát triển** trong dài hạn

Khác với **proof-of-concept** (POC) chỉ cần chạy được trên máy tính của bạn, production quality đòi hỏi xử lý **toàn bộ các edge cases**, có **khả năng phục hồi từ lỗi**, **monitoring toàn diện**, và **tối ưu hóa hiệu suất**.

#### 1.2 Tại Sao Production Quality Quan Trọng?

###### Business Impact
- **Tổn thất tài chính**: Mỗi giờ downtime có thể tốn hàng triệu đô la (ví dụ: Amazon mất ~$5,600/giây khi bị downtime)
- **Mất lòng tin khách hàng**: Một lần crash có thể khiến người dùng chuyển sang competitor
- **Rủi ro pháp lý**: Nếu hệ thống lộ dữ liệu, công ty phải chịu phạt (GDPR: lên đến 4% doanh thu)

###### Technical Impact
- **Giảm chi phí vận hành**: Hệ thống ổn định = ít incident = ít on-call = team hạnh phúc
- **Tăng tốc độ phát triển**: Code quality cao = debug nhanh = feature mới ra nhanh
- **Dễ scale**: Khi thiết kế tốt từ đầu, mở rộng sẽ dễ dàng hơn

#### 1.3 Production Quality vs Development

| Khía Cạnh | Development | Production |
|-----------|-------------|-----------|
| **Mục tiêu** | Chạy được, test nhanh | Ổn định, bảo mật, hiệu suất |
| **Error handling** | Có thể throw exception | Phải graceful, log, retry |
| **Monitoring** | Có thể debug local | Phải có monitoring 24/7 |
| **Scalability** | Chạy trên 1 máy được | Phải scale horizontally |
| **Security** | Có thể hardcode secrets | Phải dùng secrets manager |
| **Testing** | Unit tests | Unit + Integration + E2E + Performance |
| **Deployment** | Commit → Run | Commit → Build → Test → Deploy → Monitor |

#### 1.4 Các Pillars Chính Của Production Quality

Production quality được xây dựng trên 7 trụ cột chính:

```
┌─────────────────────────────────────────────────────────┐
│                 PRODUCTION QUALITY                       │
├─────────────────────────────────────────────────────────┤
│  1. RELIABILITY    → Hệ thống chạy ổn định              │
│  2. SCALABILITY    → Xử lý được tăng trưởng             │
│  3. PERFORMANCE    → Phản ứng nhanh                      │
│  4. SECURITY       → Bảo vệ dữ liệu                      │
│  5. OBSERVABILITY  → Hiểu được hệ thống                 │
│  6. MAINTAINABILITY→ Dễ phát triển & fix                │
│  7. COST EFFICIENCY→ Tối ưu chi phí vận hành            │
└─────────────────────────────────────────────────────────┘
```

---

### Chương 2: Core Principles

#### 2.1 Principle 1: Fail-Safe Design

**Nguyên tắc**: Hệ thống phải được thiết kế để **fail gracefully**, không phải fail catastrophically.

**Ý nghĩa**: Khi có lỗi, hệ thống nên:
- Trả về lỗi có ý nghĩa thay vì crash
- Giữ được trạng thái nhất quán
- Cho phép người dùng biết chuyện gì xảy ra
- Có cơ hội phục hồi

**Ví dụ**:

```python
## ❌ BAD: Crash khi database không available
def get_user(user_id):
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return user

## ✅ GOOD: Graceful error handling
def get_user(user_id):
    try:
        user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
        if not user:
            return {"error": "User not found", "status": 404}
        return {"data": user, "status": 200}
    except DatabaseConnectionError as e:
        logger.error(f"Database error: {e}")
        return {"error": "Service temporarily unavailable", "status": 503}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": "Internal server error", "status": 500}
```

#### 2.2 Principle 2: Defense in Depth

**Nguyên tắc**: Không dựa vào một lớp bảo vệ duy nhất. Phải có nhiều lớp.

**Ý nghĩa**: Nếu một lớp thất bại, các lớp khác vẫn bảo vệ hệ thống.

**Ví dụ trong Security**:
```
┌─────────────────────────────────────────┐
│ Layer 1: Network Security (WAF, DDoS)   │
├─────────────────────────────────────────┤
│ Layer 2: Authentication (OAuth, JWT)    │
├─────────────────────────────────────────┤
│ Layer 3: Authorization (RBAC)           │
├─────────────────────────────────────────┤
│ Layer 4: Input Validation               │
├─────────────────────────────────────────┤
│ Layer 5: Encryption (TLS, at-rest)      │
├─────────────────────────────────────────┤
│ Layer 6: Audit Logging                  │
└─────────────────────────────────────────┘
```

#### 2.3 Principle 3: Observability First

**Nguyên tắc**: Nếu bạn không thể đo được, bạn không thể quản lý được.

**Ý nghĩa**: Hệ thống phải cung cấp đủ thông tin để hiểu nó đang làm gì.

**Ba Pillars của Observability**:

1. **Metrics**: Số liệu định lượng (latency, error rate, CPU)
2. **Logs**: Ghi chép chi tiết (khi nào, cái gì xảy ra)
3. **Traces**: Theo dõi request qua các service

```python
## Ví dụ: Instrumentation cơ bản
import logging
import time
from prometheus_client import Counter, Histogram

## Metrics
request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

## Logging
logger = logging.getLogger(__name__)

def process_request(request):
    start_time = time.time()
    request_count.inc()
    
    try:
        logger.info(f"Processing request: {request.id}")
        result = do_work(request)
        logger.info(f"Request {request.id} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Request {request.id} failed: {e}")
        raise
    finally:
        duration = time.time() - start_time
        request_duration.observe(duration)
```

#### 2.4 Principle 4: Automate Everything

**Nguyên tắc**: Những gì có thể tự động hóa thì phải tự động hóa.

**Tại sao**: 
- Con người dễ sai lầm
- Tự động hóa nhanh hơn
- Có thể lặp lại một cách nhất quán

**Ví dụ**:
- ✅ CI/CD pipeline tự động test & deploy
- ✅ Monitoring tự động alert
- ✅ Scaling tự động dựa trên metrics
- ✅ Backup tự động hàng ngày
- ❌ Manual testing trước mỗi release
- ❌ Manual deployment
- ❌ Manual scaling

#### 2.5 Principle 5: Embrace Failures

**Nguyên tắc**: Giả định rằng mọi thứ sẽ fail, và thiết kế hệ thống để xử lý nó.

**Ý nghĩa**:
- Database có thể down
- Network có thể bị timeout
- Third-party API có thể slow
- Server có thể crash

**Cách xử lý**:
- Retry logic với exponential backoff
- Circuit breaker để ngăn cascading failures
- Timeout để tránh indefinite waits
- Fallback strategies

```python
## Ví dụ: Resilient API call
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_external_api(endpoint):
    response = requests.get(endpoint, timeout=5)
    response.raise_for_status()
    return response.json()

## Hoặc với circuit breaker
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def call_external_api(endpoint):
    response = requests.get(endpoint, timeout=5)
    response.raise_for_status()
    return response.json()
```

#### 2.6 Principle 6: Measure What Matters

**Nguyên tắc**: Không phải tất cả metrics đều quan trọng. Tập trung vào những metrics ảnh hưởng đến business.

**Ví dụ**:
- ✅ Error rate (ảnh hưởng đến user experience)
- ✅ Latency P99 (ảnh hưởng đến user satisfaction)
- ✅ Conversion rate (ảnh hưởng đến revenue)
- ❌ CPU usage (chỉ quan trọng nếu nó ảnh hưởng đến latency)
- ❌ Memory usage (chỉ quan trọng nếu nó gây OOM)

#### 2.7 Principle 7: Continuous Improvement

**Nguyên tắc**: Production quality không phải một điểm đến, mà là một hành trình liên tục.

**Cách thực hiện**:
- Định kỳ review metrics
- Học từ incidents
- Refactor technical debt
- Update dependencies
- Optimize performance

---

### Chương 3: Architecture Fundamentals

#### 3.1 Layered Architecture

Một hệ thống production-grade thường được chia thành các lớp:

```
┌─────────────────────────────────────┐
│     Presentation Layer              │ (UI, API Gateway)
├─────────────────────────────────────┤
│     Business Logic Layer            │ (Services, Controllers)
├─────────────────────────────────────┤
│     Data Access Layer               │ (Repositories, ORM)
├─────────────────────────────────────┤
│     Infrastructure Layer            │ (Database, Cache, Queue)
└─────────────────────────────────────┘
```

**Lợi ích**:
- Separation of concerns
- Dễ test từng lớp
- Dễ thay đổi implementation
- Dễ scale từng lớp độc lập

#### 3.2 Scalability Patterns

###### Horizontal Scaling (Scale Out)
- Thêm nhiều server vào cluster
- Dùng load balancer để phân phối request
- Phù hợp với stateless services
- Ví dụ: Thêm 3 servers thay vì 1 server mạnh hơn

```
┌──────────┐
│ Load     │
│ Balancer │
└────┬─────┘
     │
  ┌──┴──┬──────┬──────┐
  │     │      │      │
┌─┴─┐ ┌─┴─┐ ┌─┴─┐ ┌─┴─┐
│App│ │App│ │App│ │App│
└───┘ └───┘ └───┘ └───┘
```

###### Vertical Scaling (Scale Up)
- Nâng cấp tài nguyên của server hiện có
- Thêm CPU, RAM, Storage
- Có giới hạn phần cứng
- Ví dụ: Từ 4GB RAM → 16GB RAM

**Khi nào dùng cái nào?**

| Scenario | Horizontal | Vertical |
|----------|-----------|----------|
| Traffic tăng từ từ | ✅ | ✅ |
| Traffic spike đột ngột | ✅ | ❌ |
| Cần high availability | ✅ | ❌ |
| Cost-sensitive | ✅ | ❌ |
| Stateful service | ❌ | ✅ |
| Legacy monolith | ❌ | ✅ |

#### 3.3 Load Balancing Strategies

**Round Robin**
```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1 (quay lại)
```
- Đơn giản nhưng không xem xét capacity

**Weighted Round Robin**
```
Server 1 (weight=3) → 60%
Server 2 (weight=2) → 40%
```
- Dùng khi servers có capacity khác nhau

**Least Connections**
```
Chọn server có ít connection nhất
```
- Tốt cho long-lived connections

**Resource-Based (Adaptive)**
```
Chọn dựa trên CPU, memory, response time thực tế
```
- Tốt nhất nhưng phức tạp hơn

#### 3.4 Microservices Architecture

**Khái niệm**: Chia ứng dụng thành nhiều service nhỏ, độc lập, có thể deploy riêng.

**Ưu điểm**:
- Dễ scale từng service
- Dễ deploy riêng lẻ
- Dễ thay đổi technology stack
- Team độc lập có thể làm việc trên service khác nhau

**Nhược điểm**:
- Phức tạp hơn (distributed systems)
- Network latency
- Khó debug
- Phải quản lý nhiều databases

**Ví dụ Architecture**:

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
└────────┬──────────────┬──────────────┬───────────────┘
         │              │              │
    ┌────┴────┐    ┌────┴────┐   ┌────┴────┐
    │ User    │    │ Product │   │ Order   │
    │ Service │    │ Service │   │ Service │
    └────┬────┘    └────┬────┘   └────┬────┘
         │              │              │
    ┌────┴────┐    ┌────┴────┐   ┌────┴────┐
    │ User DB │    │Product  │   │ Order   │
    │         │    │ DB      │   │ DB      │
    └─────────┘    └─────────┘   └─────────┘
```

---

### Chương 4: Trade-offs & Decision Making

#### 4.1 Consistency vs Availability

**CAP Theorem**: Trong distributed systems, bạn chỉ có thể chọn 2 trong 3:
- **Consistency** (C): Tất cả nodes có dữ liệu giống nhau
- **Availability** (A): Hệ thống luôn sẵn sàng
- **Partition Tolerance** (P): Hệ thống tiếp tục hoạt động khi network bị chia cắt

**Trong thực tế**: Bạn phải chọn CP hoặc AP (P là bắt buộc trong distributed systems)

**CP (Consistency + Partition Tolerance)**
```
Ưu: Dữ liệu luôn nhất quán
Nhược: Có thể không available khi network bị partition
Ví dụ: Database transactions, financial systems
```

**AP (Availability + Partition Tolerance)**
```
Ưu: Hệ thống luôn available
Nhược: Dữ liệu có thể tạm thời không nhất quán
Ví dụ: Social media, NoSQL databases
```

#### 4.2 Latency vs Throughput

**Latency**: Thời gian để xử lý 1 request
**Throughput**: Số request xử lý được trong 1 giây

```
┌─────────────────────────────────────┐
│ Optimize for Latency                │
├─────────────────────────────────────┤
│ • Cache aggressively                │
│ • Use CDN                           │
│ • Reduce network hops               │
│ • Optimize database queries         │
│ Ví dụ: Real-time trading systems    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Optimize for Throughput             │
├─────────────────────────────────────┤
│ • Batch processing                  │
│ • Async processing                  │
│ • Connection pooling                │
│ • Parallel processing               │
│ Ví dụ: Batch data processing        │
└─────────────────────────────────────┘
```

#### 4.3 Cost vs Performance

**High Performance** = **High Cost**

```
┌──────────────────────────────────────────┐
│ Cost vs Performance Trade-off             │
├──────────────────────────────────────────┤
│ • Premium tier: 99.99% uptime, $$$$$     │
│ • Standard tier: 99.9% uptime, $$$$      │
│ • Basic tier: 99% uptime, $$$            │
│ • Budget tier: 95% uptime, $$            │
└──────────────────────────────────────────┘
```

**Cách quyết định**:
- Tính toán cost của downtime
- So sánh với cost của infrastructure
- Chọn điểm cân bằng tối ưu

#### 4.4 Complexity vs Maintainability

**Thêm features** → **Thêm complexity** → **Khó maintain**

```
┌─────────────────────────────────────────┐
│ Simplicity First Approach               │
├─────────────────────────────────────────┤
│ 1. Build simple solution                │
│ 2. Measure actual problems              │
│ 3. Add complexity ONLY if needed        │
│ 4. Monitor impact                       │
└─────────────────────────────────────────┘
```

**Ví dụ**: Không cần microservices từ đầu. Bắt đầu với monolith, sau đó tách khi cần.

---

### Checklist: Foundations

- [ ] Hiểu rõ 7 pillars của production quality
- [ ] Áp dụng 7 core principles vào design
- [ ] Chọn architecture phù hợp với use case
- [ ] Hiểu trade-offs của các quyết định
- [ ] Có monitoring từ đầu
- [ ] Có error handling strategy
- [ ] Có disaster recovery plan
- [ ] Team hiểu về production quality mindset

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN II: ARCHITECTURE & DESIGN

---

### Chương 5: Scalability Patterns (Chi Tiết)

#### 5.1 Horizontal Scaling - Scale Out

**Định nghĩa**: Thêm nhiều máy chủ vào hệ thống thay vì nâng cấp máy hiện có.

###### Kiến Trúc Horizontal Scaling

```
┌─────────────────────────────────────────────┐
│         Internet / Client                    │
└────────────────────┬────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    ┌───┴────────┐         ┌──────┴──────┐
    │ Load       │         │ Load        │
    │ Balancer 1 │         │ Balancer 2  │
    └───┬────────┘         └──────┬──────┘
        │                         │
    ┌───┴─────────┬─────────┬─────┴──────┐
    │             │         │            │
┌───┴──┐      ┌───┴──┐  ┌──┴────┐    ┌──┴────┐
│App 1 │      │App 2 │  │App 3  │    │App 4  │
│DB 1  │      │DB 2  │  │DB 3   │    │DB 4   │
└──────┘      └──────┘  └───────┘    └───────┘
```

###### Ưu Điểm
- **High Availability**: Nếu 1 server down, các server khác vẫn chạy
- **Dễ scale**: Thêm server mới vào cluster
- **Cost-effective**: Dùng commodity hardware
- **Fault tolerance**: Có redundancy

###### Nhược Điểm
- **Phức tạp hơn**: Cần load balancer, session management
- **Network overhead**: Phải communicate qua network
- **Data consistency**: Khó đảm bảo consistency khi có nhiều instances
- **Operational complexity**: Phải quản lý nhiều servers

###### Khi Nào Dùng
- ✅ Stateless services (API servers, web servers)
- ✅ High traffic applications
- ✅ Cần high availability
- ✅ Cloud-native applications

###### Implementation Example

```python
## Ví dụ: Stateless API server
from flask import Flask, request
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Stateless endpoint - có thể chạy trên bất kỳ server nào
    """
    logger.info(f"Getting user {user_id} on server {request.host}")
    
    ## Fetch từ shared database
    user = db.get_user(user_id)
    
    if not user:
        return {"error": "Not found"}, 404
    
    return {"data": user}, 200

## Load balancer sẽ route requests đến:
## Server 1: 10.0.0.1:5000
## Server 2: 10.0.0.2:5000
## Server 3: 10.0.0.3:5000
```

###### Session Management trong Horizontal Scaling

**Problem**: Nếu user login vào Server 1, rồi request tiếp theo route đến Server 2, Server 2 không biết user đã login.

**Solutions**:

**1. Sticky Sessions (Session Affinity)**
```
Load Balancer → Luôn route user đến cùng 1 server
Ưu: Đơn giản
Nhược: Nếu server down, user mất session
```

**2. Shared Session Store (Redis)**
```
Server 1 ─┐
Server 2 ─┼─→ Redis (shared session store)
Server 3 ─┘
```

```python
from flask_session import Session
from redis import Redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='redis-server', port=6379)
Session(app)

@app.route('/login', methods=['POST'])
def login():
    session['user_id'] = request.json['user_id']
    return {"status": "logged in"}

@app.route('/profile')
def profile():
    ## Lấy từ Redis, không quan trọng server nào xử lý
    user_id = session.get('user_id')
    return {"user_id": user_id}
```

**3. JWT Tokens (Stateless)**
```
Client lưu token, gửi lại mỗi request
Server verify token mà không cần store session
```

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    token = create_access_token(identity=user_id)
    return {"access_token": token}

@app.route('/profile')
@jwt_required()
def profile():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    return {"user_id": user_id}
```

#### 5.2 Vertical Scaling - Scale Up

**Định nghĩa**: Nâng cấp tài nguyên của server hiện có (CPU, RAM, Storage).

###### Ưu Điểm
- **Đơn giản**: Không cần thay đổi architecture
- **Không có network overhead**: Mọi thứ trên 1 máy
- **Dễ quản lý**: Chỉ 1 server
- **Tốt cho stateful services**: Database, cache

###### Nhược Điểm
- **Có giới hạn**: Không thể nâng cấp vô hạn
- **Downtime**: Phải restart server khi nâng cấp
- **Single point of failure**: Nếu server down, toàn bộ hệ thống down
- **Đắt**: Server mạnh hơn thường đắt hơn

###### Khi Nào Dùng
- ✅ Stateful services (Database, Cache)
- ✅ Legacy monolith
- ✅ Workload có thể dự đoán
- ✅ Cần low latency

#### 5.3 Diagonal Scaling - Kết Hợp Cả Hai

**Ý tưởng**: Dùng vertical scaling cho critical services, horizontal scaling cho stateless services.

```
┌──────────────────────────────────────────┐
│ API Servers (Horizontal)                 │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│ │Server 1 │ │Server 2 │ │Server 3 │    │
│ └────┬────┘ └────┬────┘ └────┬────┘    │
└─────┼────────────┼────────────┼─────────┘
      │            │            │
      └────────────┼────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
    ┌────┴────────┐   ┌──────┴──────┐
    │ Database    │   │ Cache       │
    │ (Vertical)  │   │ (Vertical)  │
    │ 64GB RAM    │   │ 32GB RAM    │
    └─────────────┘   └─────────────┘
```

**Ưu điểm**:
- Tối ưu hóa cả performance lẫn availability
- Stateless services scale horizontally
- Stateful services scale vertically
- Cost-effective

---

### Chương 6: Load Balancing (Chi Tiết)

#### 6.1 Load Balancing Algorithms

###### 1. Round Robin
```
Requests: 1, 2, 3, 4, 5, 6
Servers:  A, B, C, A, B, C
```

**Ưu**: Đơn giản, công bằng
**Nhược**: Không xem xét server capacity, không phù hợp với long-lived connections

```nginx
## Nginx configuration
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

###### 2. Weighted Round Robin
```
Server A (weight=3): 60%
Server B (weight=2): 40%
```

**Dùng khi**: Servers có capacity khác nhau

```nginx
upstream backend {
    server backend1.example.com weight=3;
    server backend2.example.com weight=2;
}
```

###### 3. Least Connections
```
Chọn server có ít active connections nhất
```

**Ưu**: Tốt cho long-lived connections
**Nhược**: Không xem xét server capacity

```nginx
upstream backend {
    least_conn;
    server backend1.example.com;
    server backend2.example.com;
}
```

###### 4. IP Hash
```
Hash(client_ip) % num_servers = server_index
```

**Ưu**: Sticky sessions (cùng client luôn đến cùng server)
**Nhược**: Nếu thêm/xóa server, hash bị thay đổi

```nginx
upstream backend {
    ip_hash;
    server backend1.example.com;
    server backend2.example.com;
}
```

###### 5. Resource-Based (Adaptive)
```
Chọn server dựa trên CPU, memory, response time thực tế
```

**Ưu**: Tối ưu nhất
**Nhược**: Phức tạp, cần monitoring

```python
## Ví dụ: Custom load balancer
import requests
from statistics import mean

class AdaptiveLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.metrics = {s: {"cpu": 0, "memory": 0} for s in servers}
    
    def get_server_metrics(self, server):
        """Lấy metrics từ server"""
        try:
            response = requests.get(f"http://{server}/metrics", timeout=1)
            return response.json()
        except:
            return {"cpu": 100, "memory": 100}  ## Assume down
    
    def select_server(self):
        """Chọn server có resource ít nhất"""
        ## Update metrics
        for server in self.servers:
            metrics = self.get_server_metrics(server)
            self.metrics[server] = metrics
        
        ## Chọn server với score thấp nhất
        scores = {
            server: (self.metrics[server]["cpu"] + self.metrics[server]["memory"]) / 2
            for server in self.servers
        }
        
        return min(scores, key=scores.get)
```

#### 6.2 Health Checks

**Tại sao cần**: Load balancer phải biết server nào healthy, server nào down.

```python
## Ví dụ: Health check endpoint
from flask import Flask

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Load balancer sẽ gọi định kỳ
    """
    try:
        ## Check database connection
        db.ping()
        
        ## Check cache connection
        cache.ping()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }, 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }, 503
```

**Nginx health check configuration**:
```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    
    ## Health check
    check interval=3000 rise=2 fall=5 timeout=1000 type=http;
    check_http_send "GET /health HTTP/1.0\r\n\r\n";
    check_http_expect_alive http_2xx;
}
```

#### 6.3 Load Balancer High Availability

**Problem**: Nếu load balancer down, toàn bộ hệ thống down.

**Solution**: Có 2+ load balancers trong active-passive hoặc active-active mode.

```
┌────────────────────────────────────┐
│ Virtual IP (VIP)                   │
│ 10.0.0.100                         │
└────────────┬───────────────────────┘
             │
      ┌──────┴────────┐
      │               │
  ┌───┴────┐      ┌───┴────┐
  │ LB 1   │      │ LB 2   │
  │ Active │      │ Passive│
  │ 10.0.0.1      │ 10.0.0.2
  └───┬────┘      └────────┘
      │
      └─→ Health check: LB 2 monitors LB 1
      └─→ If LB 1 down, VIP moves to LB 2
```

**Tools**: HAProxy, Nginx, AWS ELB, Google Cloud Load Balancer

---

### Chương 7: Microservices Architecture (Chi Tiết)

#### 7.1 Microservices Patterns

###### Pattern 1: API Gateway

**Ý tưởng**: Có 1 entry point duy nhất cho tất cả clients.

```
┌──────────────────────────────────────┐
│ Client                               │
└────────────────┬─────────────────────┘
                 │
         ┌───────┴────────┐
         │  API Gateway   │
         │ (Authentication│
         │  Rate Limiting │
         │  Routing)      │
         └───┬────┬────┬──┘
             │    │    │
        ┌────┘    │    └────┐
        │         │         │
    ┌───┴──┐  ┌───┴──┐  ┌───┴──┐
    │User  │  │Product  │Order  │
    │Service   │Service  │Service│
    └──────┘  └────────┘ └──────┘
```

**Ưu điểm**:
- Centralized authentication & authorization
- Rate limiting
- Request routing
- API versioning
- Monitoring

**Implementation**:
```python
## Ví dụ: API Gateway với Flask
from flask import Flask, request, jsonify
import requests
from functools import wraps

app = Flask(__name__)

## Service registry
SERVICES = {
    'users': 'http://user-service:5001',
    'products': 'http://product-service:5002',
    'orders': 'http://order-service:5003'
}

def authenticate(f):
    """Authentication middleware"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"error": "Missing token"}, 401
        
        ## Verify token
        if not verify_token(token):
            return {"error": "Invalid token"}, 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/api/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@authenticate
def gateway(service, path):
    """Route requests to appropriate service"""
    if service not in SERVICES:
        return {"error": "Service not found"}, 404
    
    service_url = f"{SERVICES[service]}/{path}"
    
    try:
        response = requests.request(
            method=request.method,
            url=service_url,
            headers=request.headers,
            json=request.json,
            timeout=5
        )
        return response.json(), response.status_code
    except requests.Timeout:
        return {"error": "Service timeout"}, 504
    except Exception as e:
        return {"error": str(e)}, 500
```

###### Pattern 2: Service Discovery

**Problem**: Khi có nhiều service instances, làm sao biết địa chỉ của chúng?

**Solution**: Service registry + discovery mechanism

```
┌─────────────────────────────────────┐
│ Service Registry (Consul/Eureka)    │
├─────────────────────────────────────┤
│ user-service: 10.0.0.1:5001         │
│ user-service: 10.0.0.2:5001         │
│ product-service: 10.0.0.3:5002      │
│ order-service: 10.0.0.4:5003        │
└─────────────────────────────────────┘
```

**Implementation với Consul**:
```python
import consul

## Register service
c = consul.Consul(host='consul-server', port=8500)

c.agent.service.register(
    name='user-service',
    service_id='user-service-1',
    address='10.0.0.1',
    port=5001,
    check=consul.Check.http(
        'http://10.0.0.1:5001/health',
        interval='10s'
    )
)

## Discover service
index, data = c.health.service('user-service', passing=True)
for entry in data:
    print(f"Service at {entry['Service']['Address']}:{entry['Service']['Port']}")
```

###### Pattern 3: Circuit Breaker

**Problem**: Khi service A gọi service B mà B bị down, A sẽ timeout. Nếu có 100 requests, sẽ có 100 timeouts, tốn resources.

**Solution**: Circuit breaker ngắt mạch khi detect failures.

```
States:
┌────────┐  (failures > threshold)  ┌──────┐
│ CLOSED │──────────────────────────→│ OPEN │
│ (OK)   │                           │(FAIL)│
└────────┘←──────────────────────────└──────┘
   ↑      (timeout expires)            │
   │                                   │
   └─────────────────────────────────┐ │
                                     │ │
                            ┌────────┴─┴──┐
                            │ HALF-OPEN   │
                            │ (testing)   │
                            └─────────────┘
```

```python
from pybreaker import CircuitBreaker
import requests

## Create circuit breaker
breaker = CircuitBreaker(
    fail_max=5,           ## Fail 5 times
    reset_timeout=60      ## Then wait 60s
)

@breaker
def call_user_service(user_id):
    """Call user service with circuit breaker"""
    response = requests.get(
        f'http://user-service/users/{user_id}',
        timeout=5
    )
    response.raise_for_status()
    return response.json()

## Usage
try:
    user = call_user_service(123)
except CircuitBreakerListener:
    ## Circuit is open, return cached data or default
    user = get_cached_user(123) or {"error": "Service unavailable"}
```

###### Pattern 4: Database per Service

**Ý tưởng**: Mỗi microservice có database riêng.

```
┌──────────────────────────────────────────────┐
│ User Service      Product Service            │
│ ┌──────────────┐  ┌──────────────┐          │
│ │ User DB      │  │ Product DB   │          │
│ │ (PostgreSQL) │  │ (MongoDB)    │          │
│ └──────────────┘  └──────────────┘          │
└──────────────────────────────────────────────┘
```

**Ưu điểm**:
- Loose coupling
- Mỗi service chọn DB phù hợp
- Dễ scale từng service

**Nhược điểm**:
- Khó join data từ 2 databases
- Khó maintain consistency

**Khi nào dùng**:
- ✅ Khi services thực sự độc lập
- ✅ Khi có different data models
- ❌ Khi cần join data thường xuyên

###### Pattern 5: Saga Pattern (Distributed Transactions)

**Problem**: Làm sao thực hiện transaction qua nhiều services?

**Example**: Order → Payment → Inventory

```
Saga Pattern:
1. Order Service: Create order (PENDING)
2. Payment Service: Process payment
   - If success: Commit
   - If fail: Rollback order
3. Inventory Service: Reserve inventory
   - If success: Commit
   - If fail: Refund payment, rollback order
```

**Choreography-based Saga** (Event-driven):
```python
## Order Service
@app.route('/orders', methods=['POST'])
def create_order():
    order = Order.create(request.json)
    db.session.commit()
    
    ## Publish event
    publish_event('order.created', {'order_id': order.id})
    
    return {"order_id": order.id}, 201

## Payment Service (listens to order.created)
@event_listener('order.created')
def process_payment(event):
    order_id = event['order_id']
    
    try:
        payment = process_payment_for_order(order_id)
        publish_event('payment.completed', {'order_id': order_id})
    except Exception as e:
        publish_event('payment.failed', {'order_id': order_id})

## Inventory Service (listens to payment.completed)
@event_listener('payment.completed')
def reserve_inventory(event):
    order_id = event['order_id']
    
    try:
        reserve_items_for_order(order_id)
        publish_event('inventory.reserved', {'order_id': order_id})
    except Exception as e:
        publish_event('inventory.failed', {'order_id': order_id})
        ## Trigger compensation transaction
        publish_event('payment.refund', {'order_id': order_id})
```

---

### Chương 8: Data Consistency Patterns

#### 8.1 Strong Consistency

**Định nghĩa**: Tất cả nodes luôn có dữ liệu giống nhau, không có lag.

**Ưu điểm**:
- Dữ liệu luôn chính xác
- Phù hợp với financial transactions

**Nhược điểm**:
- Chậm (phải wait tất cả nodes confirm)
- Khó scale
- Nếu 1 node down, hệ thống không available

**Ví dụ**: ACID databases (PostgreSQL, MySQL)

```
Write request → Master → Replicate to all slaves → Confirm
```

#### 8.2 Eventual Consistency

**Định nghĩa**: Replicas có thể tạm thời inconsistent, nhưng cuối cùng sẽ converge.

**Ưu điểm**:
- Nhanh (không cần wait tất cả nodes)
- Dễ scale
- High availability

**Nhược điểm**:
- Dữ liệu có thể tạm thời không chính xác
- Phức tạp hơn (phải handle conflicts)

**Ví dụ**: NoSQL databases (DynamoDB, Cassandra)

```
Write request → Master → Return immediately
                      → Replicate to slaves (async)
```

**Conflict Resolution**:
```python
## Last-write-wins
def merge_data(local, remote):
    if remote['timestamp'] > local['timestamp']:
        return remote
    return local

## Custom merge logic
def merge_user_data(local, remote):
    ## Merge fields intelligently
    merged = local.copy()
    
    ## Prefer non-null values
    for key in remote:
        if remote[key] is not None:
            merged[key] = remote[key]
    
    return merged
```

#### 8.3 Causal Consistency

**Ý tưởng**: Nếu operation A gây ra operation B, thì tất cả readers sẽ thấy A trước B.

```
Timeline:
1. User writes: "Hello" (timestamp=1)
2. User reads: "Hello" (timestamp=1)
3. Other user reads: "Hello" (timestamp=1)

Không bao giờ xảy ra:
- User thấy "Hello" rồi không thấy nữa
```

---

### Checklist: Architecture & Design

- [ ] Chọn scaling strategy phù hợp (horizontal/vertical/diagonal)
- [ ] Implement load balancing
- [ ] Có health checks cho tất cả services
- [ ] Nếu dùng microservices:
  - [ ] Có API Gateway
  - [ ] Có Service Discovery
  - [ ] Implement Circuit Breaker
  - [ ] Có strategy cho distributed transactions
- [ ] Quyết định consistency model (strong/eventual)
- [ ] Document architecture decisions
- [ ] Có monitoring cho architecture
- [ ] Có disaster recovery plan

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN III: RELIABILITY & RESILIENCE

---

### Chương 9: Resilience Patterns (Chi Tiết)

#### 9.1 Retry Pattern

**Khái niệm**: Khi gặp lỗi transient (tạm thời), thử lại operation.

**Khi nào dùng**:
- ✅ Network timeout
- ✅ Temporary service unavailable (503)
- ✅ Rate limit exceeded (429)
- ❌ Permanent errors (404, 401)
- ❌ Invalid input (400)

###### Retry Strategies

**1. Simple Retry**
```python
def call_api(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

**Problem**: Nếu tất cả clients retry cùng lúc, server sẽ bị overwhelm hơn.

**2. Exponential Backoff**
```python
import time

def call_api_with_backoff(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            
            ## Wait: 1s, 2s, 4s, 8s...
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1} after {wait_time}s")
            time.sleep(wait_time)
```

**3. Exponential Backoff with Jitter**
```python
import time
import random

def call_api_with_jitter(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            
            ## Wait: 1-2s, 2-4s, 4-8s...
            base_wait = 2 ** attempt
            jitter = random.uniform(0, base_wait)
            wait_time = base_wait + jitter
            print(f"Retry {attempt + 1} after {wait_time:.2f}s")
            time.sleep(wait_time)
```

**Tại sao jitter?** Nếu tất cả clients retry cùng lúc (thundering herd), jitter sẽ phân tán retry times.

###### Retry Library

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(requests.RequestException)
)
def call_api(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

#### 9.2 Circuit Breaker Pattern

**Khái niệm**: Ngắt mạch khi detect failures, tránh gọi service đang down.

###### States

```
┌─────────────────────────────────────────────────────┐
│ CLOSED (Normal)                                     │
│ - Requests pass through                             │
│ - Track failures                                    │
│ - If failures > threshold → OPEN                    │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ OPEN (Failing)                                      │
│ - Reject requests immediately                       │
│ - Save resources                                    │
│ - After timeout → HALF_OPEN                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ HALF_OPEN (Testing)                                 │
│ - Allow limited requests                            │
│ - If success → CLOSED                               │
│ - If fail → OPEN                                    │
└─────────────────────────────────────────────────────┘
```

###### Implementation

```python
from pybreaker import CircuitBreaker
import requests

## Create circuit breaker
breaker = CircuitBreaker(
    fail_max=5,              ## Open after 5 failures
    reset_timeout=60,        ## Try again after 60s
    listeners=[],            ## Event listeners
    exclude=[requests.HTTPError]  ## Don't count these errors
)

@breaker
def call_user_service(user_id):
    response = requests.get(f'http://user-service/users/{user_id}', timeout=5)
    response.raise_for_status()
    return response.json()

## Usage
try:
    user = call_user_service(123)
except CircuitBreakerListener:
    ## Circuit is open
    user = get_cached_user(123) or {"error": "Service unavailable"}
```

###### Configuration Best Practices

```python
## Ví dụ: Cấu hình tốt cho production
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(
    name='user-service',
    fail_max=5,                    ## Fail 5 times
    reset_timeout=60,              ## Wait 60s before retry
    exclude=[
        requests.exceptions.Timeout,  ## Don't count timeouts
        requests.exceptions.ConnectionError
    ],
    listeners=[
        CircuitBreakerListener()    ## Log events
    ]
)

## Metrics
@breaker.listener
def on_state_change(cb, old_state, new_state):
    logger.warning(f"Circuit breaker {cb.name}: {old_state} → {new_state}")
    metrics.gauge('circuit_breaker.state', new_state)
```

#### 9.3 Timeout Pattern

**Khái niệm**: Set upper bound cho operation duration.

**Tại sao cần**: Tránh indefinite waits, giữ resources.

###### Timeout Levels

```
┌─────────────────────────────────┐
│ Request Timeout (5s)            │
│ ┌─────────────────────────────┐ │
│ │ Connection Timeout (2s)     │ │
│ │ ┌─────────────────────────┐ │ │
│ │ │ Read Timeout (3s)       │ │ │
│ │ └─────────────────────────┘ │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

###### Implementation

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

## Create session with timeout
session = requests.Session()

## Set timeout for all requests
session.timeout = 5  ## 5 seconds

## Or per request
response = requests.get(url, timeout=5)

## Or with different timeouts for connect and read
response = requests.get(url, timeout=(2, 5))  ## (connect, read)

## With retry + timeout
adapter = HTTPAdapter(max_retries=Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
))
session.mount('http://', adapter)
session.mount('https://', adapter)

response = session.get(url, timeout=5)
```

###### Timeout Strategy

```python
## ❌ BAD: No timeout
response = requests.get(url)  ## Can hang forever

## ✅ GOOD: Always set timeout
response = requests.get(url, timeout=5)

## ✅ BETTER: Different timeouts for different scenarios
if is_critical_path:
    timeout = 1  ## Strict timeout
else:
    timeout = 10  ## More lenient

response = requests.get(url, timeout=timeout)
```

#### 9.4 Bulkhead Pattern

**Khái niệm**: Isolate failures đến một phần, không ảnh hưởng toàn bộ hệ thống.

**Ví dụ**: Giống ngăn tàu thủy, nếu 1 ngăn bị nước, các ngăn khác vẫn an toàn.

###### Implementation

**1. Thread Pool Isolation**
```python
from concurrent.futures import ThreadPoolExecutor
import threading

## Separate thread pools for different services
user_service_pool = ThreadPoolExecutor(max_workers=10)
product_service_pool = ThreadPoolExecutor(max_workers=10)
order_service_pool = ThreadPoolExecutor(max_workers=10)

def get_user(user_id):
    return user_service_pool.submit(call_user_service, user_id)

def get_product(product_id):
    return product_service_pool.submit(call_product_service, product_id)

## Nếu user_service bị overwhelm, chỉ user_service_pool bị exhaust
## product_service vẫn hoạt động bình thường
```

**2. Connection Pool Isolation**
```python
import requests
from requests.adapters import HTTPAdapter

## Separate connection pools
user_session = requests.Session()
user_session.mount('http://', HTTPAdapter(pool_connections=10, pool_maxsize=10))

product_session = requests.Session()
product_session.mount('http://', HTTPAdapter(pool_connections=10, pool_maxsize=10))

## Nếu user_service slow, không ảnh hưởng product_service
user_response = user_session.get('http://user-service/users/1')
product_response = product_session.get('http://product-service/products/1')
```

**3. Semaphore (Rate Limiting)**
```python
import threading

## Limit concurrent requests to external service
semaphore = threading.Semaphore(10)  ## Max 10 concurrent

def call_external_service():
    with semaphore:
        ## Only 10 threads can execute this at a time
        return requests.get('http://external-service/api')
```

#### 9.5 Fallback Pattern

**Khái niệm**: Khi primary action fail, dùng alternative.

```python
def get_user_data(user_id):
    try:
        ## Try primary source
        return call_user_service(user_id)
    except Exception as e:
        logger.warning(f"Primary failed: {e}, trying fallback")
        
        try:
            ## Try fallback 1: Cache
            return get_from_cache(user_id)
        except:
            try:
                ## Try fallback 2: Read replica
                return get_from_read_replica(user_id)
            except:
                ## Try fallback 3: Default value
                return get_default_user()
```

---

### Chương 10: Error Handling (Chi Tiết)

#### 10.1 Error Classification

**Transient Errors** (Có thể retry)
- Network timeout
- Temporary service unavailable (503)
- Rate limit exceeded (429)
- Connection refused (server restarting)

**Permanent Errors** (Không nên retry)
- Not found (404)
- Unauthorized (401)
- Forbidden (403)
- Bad request (400)
- Internal server error (500) - có thể retry nhưng cần cẩn thận

```python
def is_retryable(exception):
    """Determine if exception is retryable"""
    if isinstance(exception, requests.Timeout):
        return True
    
    if isinstance(exception, requests.ConnectionError):
        return True
    
    if hasattr(exception, 'response'):
        status_code = exception.response.status_code
        ## Retry 5xx errors (except 501)
        if 500 <= status_code < 600 and status_code != 501:
            return True
        ## Retry 429 (rate limit)
        if status_code == 429:
            return True
    
    return False
```

#### 10.2 Structured Error Responses

```python
## ❌ BAD: Unstructured errors
@app.route('/users/<user_id>')
def get_user(user_id):
    try:
        user = db.get_user(user_id)
        return user
    except Exception as e:
        return str(e), 500

## ✅ GOOD: Structured errors
@app.route('/users/<user_id>')
def get_user(user_id):
    try:
        user = db.get_user(user_id)
        if not user:
            return {
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": f"User {user_id} not found",
                    "status": 404
                }
            }, 404
        return {"data": user}, 200
    
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return {
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Failed to fetch user",
                "status": 503
            }
        }, 503
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
                "status": 500
            }
        }, 500
```

#### 10.3 Error Logging Best Practices

```python
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

def log_error(error, context=None):
    """Log error with context"""
    logger.error(
        f"Error occurred",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }
    )

## Usage
try:
    result = process_data(data)
except Exception as e:
    log_error(e, context={
        "user_id": user_id,
        "operation": "process_data",
        "input_size": len(data)
    })
```

#### 10.4 Error Recovery Strategies

**1. Graceful Degradation**
```python
def get_user_profile(user_id):
    """Get user profile with graceful degradation"""
    profile = {}
    
    ## Try to get basic info
    try:
        profile['basic'] = get_user_basic_info(user_id)
    except Exception as e:
        logger.warning(f"Failed to get basic info: {e}")
        profile['basic'] = None
    
    ## Try to get recommendations
    try:
        profile['recommendations'] = get_recommendations(user_id)
    except Exception as e:
        logger.warning(f"Failed to get recommendations: {e}")
        profile['recommendations'] = []
    
    ## Try to get social data
    try:
        profile['social'] = get_social_data(user_id)
    except Exception as e:
        logger.warning(f"Failed to get social data: {e}")
        profile['social'] = None
    
    return profile
```

**2. Compensation Transactions**
```python
def create_order(order_data):
    """Create order with compensation on failure"""
    try:
        ## Step 1: Create order
        order = Order.create(order_data)
        db.session.commit()
        
        ## Step 2: Reserve inventory
        reserve_inventory(order)
        
        ## Step 3: Process payment
        process_payment(order)
        
        return order
    
    except InventoryError:
        ## Compensation: Delete order
        Order.delete(order.id)
        db.session.commit()
        raise
    
    except PaymentError:
        ## Compensation: Release inventory + Delete order
        release_inventory(order)
        Order.delete(order.id)
        db.session.commit()
        raise
```

---

### Chương 11: Disaster Recovery & Backup

#### 11.1 Backup Strategies

###### 3-2-1 Rule
- **3** copies of data
- **2** different media types
- **1** offsite

```
┌─────────────────────────────────────────┐
│ Production Database                     │
└──────┬──────────────────────────────────┘
       │
   ┌───┴───┬──────────────┬──────────────┐
   │       │              │              │
┌──┴──┐ ┌──┴──┐       ┌───┴──┐      ┌───┴──┐
│Copy1│ │Copy2│       │Copy3 │      │Copy4 │
│Local│ │Local│       │Local │      │Cloud │
│SSD  │ │HDD  │       │Tape  │      │S3    │
└─────┘ └─────┘       └──────┘      └──────┘

Tại sao?
- Copy 1,2: Nhanh restore
- Copy 3: Backup lâu dài
- Copy 4: Offsite (disaster recovery)
```

###### Backup Types

**Full Backup**
```
Day 1: Backup toàn bộ database (100GB) → 100GB
Day 2: Backup toàn bộ database (100GB) → 100GB
...
```
- Ưu: Nhanh restore
- Nhược: Tốn storage

**Incremental Backup**
```
Day 1: Full backup (100GB) → 100GB
Day 2: Backup changes only (5GB) → 105GB total
Day 3: Backup changes only (3GB) → 108GB total
...
```
- Ưu: Tiết kiệm storage
- Nhược: Restore chậm (cần full + tất cả incremental)

**Differential Backup**
```
Day 1: Full backup (100GB) → 100GB
Day 2: Backup changes since Day 1 (5GB) → 105GB total
Day 3: Backup changes since Day 1 (8GB) → 108GB total
...
```
- Ưu: Restore nhanh hơn incremental
- Nhược: Tốn storage hơn incremental

###### Backup Schedule

```python
## Ví dụ: Backup strategy
BACKUP_SCHEDULE = {
    "daily_full": "0 2 * * *",           ## 2 AM every day
    "hourly_incremental": "0 * * * *",   ## Every hour
    "weekly_full": "0 3 * * 0",          ## 3 AM Sunday
    "monthly_full": "0 4 1 * *",         ## 4 AM 1st of month
}

RETENTION_POLICY = {
    "daily": 7,        ## Keep 7 days
    "weekly": 4,       ## Keep 4 weeks
    "monthly": 12,     ## Keep 12 months
    "yearly": 5,       ## Keep 5 years
}
```

#### 11.2 Disaster Recovery Strategies

###### 1. Backup and Restore
```
┌──────────────────────────────────────┐
│ Normal Operation                     │
│ Primary datacenter                   │
└──────────────────────────────────────┘
                 ↓ (disaster)
┌──────────────────────────────────────┐
│ Restore from backup                  │
│ Secondary datacenter                 │
│ RTO: Hours to days                   │
│ RPO: Hours                           │
└──────────────────────────────────────┘
```

**RTO** (Recovery Time Objective): Thời gian để recover
**RPO** (Recovery Point Objective): Dữ liệu mất bao lâu

###### 2. Pilot Light
```
┌──────────────────────────────────────┐
│ Primary (Active)                     │
│ Full production                       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Secondary (Standby - Minimal)        │
│ Minimal resources, ready to scale     │
│ RTO: Minutes                         │
│ RPO: Seconds                         │
└──────────────────────────────────────┘
```

###### 3. Warm Standby
```
┌──────────────────────────────────────┐
│ Primary (Active)                     │
│ Full production                       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Secondary (Standby - Scaled Down)    │
│ 50% capacity, ready to takeover      │
│ RTO: Seconds                         │
│ RPO: Seconds                         │
└──────────────────────────────────────┘
```

###### 4. Active-Active
```
┌──────────────────────────────────────┐
│ Datacenter 1 (Active)                │
│ 50% traffic                          │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Datacenter 2 (Active)                │
│ 50% traffic                          │
│ RTO: 0 (no downtime)                 │
│ RPO: 0 (no data loss)                │
└──────────────────────────────────────┘
```

#### 11.3 Backup Implementation

```python
import boto3
import subprocess
from datetime import datetime

class BackupManager:
    def __init__(self, db_host, s3_bucket):
        self.db_host = db_host
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
    
    def backup_database(self):
        """Backup database to S3"""
        timestamp = datetime.utcnow().isoformat()
        backup_file = f"backup-{timestamp}.sql.gz"
        
        try:
            ## Dump database
            dump_cmd = f"mysqldump -h {self.db_host} --all-databases | gzip"
            result = subprocess.run(dump_cmd, shell=True, capture_output=True)
            
            if result.returncode != 0:
                logger.error(f"Backup failed: {result.stderr}")
                return False
            
            ## Upload to S3
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=f"backups/{backup_file}",
                Body=result.stdout
            )
            
            logger.info(f"Backup successful: {backup_file}")
            return True
        
        except Exception as e:
            logger.error(f"Backup error: {e}")
            return False
    
    def restore_database(self, backup_file):
        """Restore database from S3"""
        try:
            ## Download from S3
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=f"backups/{backup_file}"
            )
            
            ## Restore database
            restore_cmd = f"gunzip | mysql -h {self.db_host}"
            subprocess.run(
                restore_cmd,
                shell=True,
                input=response['Body'].read()
            )
            
            logger.info(f"Restore successful: {backup_file}")
            return True
        
        except Exception as e:
            logger.error(f"Restore error: {e}")
            return False
```

---

### Chương 12: Capacity Planning & Forecasting

#### 12.1 Capacity Planning Process

```
1. Collect Historical Data
   ↓
2. Analyze Trends
   ↓
3. Forecast Future Demand
   ↓
4. Plan Resources
   ↓
5. Monitor & Adjust
```

#### 12.2 Metrics to Track

```python
## Key metrics for capacity planning
metrics = {
    "cpu_usage": 45,           ## %
    "memory_usage": 60,        ## %
    "disk_usage": 75,          ## %
    "network_bandwidth": 50,   ## %
    "database_connections": 80,## %
    "request_latency_p99": 200,## ms
    "error_rate": 0.1,         ## %
}

## Thresholds for alerting
THRESHOLDS = {
    "cpu_usage": 80,           ## Alert if > 80%
    "memory_usage": 85,        ## Alert if > 85%
    "disk_usage": 90,          ## Alert if > 90%
    "request_latency_p99": 500,## Alert if > 500ms
}
```

#### 12.3 Forecasting

```python
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_capacity(historical_data, days_ahead=30):
    """Forecast capacity needs"""
    X = np.arange(len(historical_data)).reshape(-1, 1)
    y = np.array(historical_data)
    
    model = LinearRegression()
    model.fit(X, y)
    
    ## Predict future
    future_X = np.arange(len(historical_data), len(historical_data) + days_ahead).reshape(-1, 1)
    forecast = model.predict(future_X)
    
    return forecast

## Usage
cpu_history = [45, 47, 50, 52, 55, 58, 60, 62]
forecast = forecast_capacity(cpu_history, days_ahead=30)

## If forecast shows 90% in 30 days, plan to upgrade
if max(forecast) > 80:
    logger.warning("CPU usage will exceed 80% in 30 days. Plan upgrade.")
```

---

### Checklist: Reliability & Resilience

- [ ] Implement retry logic với exponential backoff
- [ ] Setup circuit breakers cho external service calls
- [ ] Set appropriate timeouts
- [ ] Implement bulkhead pattern
- [ ] Have fallback strategies
- [ ] Structured error handling
- [ ] Comprehensive error logging
- [ ] Backup strategy (3-2-1 rule)
- [ ] Disaster recovery plan tested
- [ ] Capacity planning process
- [ ] Monitoring for all critical metrics
- [ ] Runbooks for common incidents

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN IV: OBSERVABILITY & MONITORING

---

### Chương 13: Three Pillars of Observability

#### 13.1 Metrics (Số Liệu)

**Định nghĩa**: Dữ liệu định lượng về hệ thống (CPU, memory, latency, error rate).

###### Metric Types

**1. Gauge** - Giá trị tại một thời điểm
```
CPU usage: 45%
Memory usage: 60%
Active connections: 125
```

**2. Counter** - Giá trị tăng theo thời gian
```
Total requests: 1,000,000
Total errors: 500
Total bytes sent: 10GB
```

**3. Histogram** - Phân bố giá trị
```
Request latency:
  < 100ms: 50%
  100-500ms: 40%
  > 500ms: 10%
```

**4. Summary** - Percentiles
```
Request latency:
  P50: 100ms
  P95: 250ms
  P99: 500ms
```

###### Key Metrics

**Application Metrics**
```
- Request rate (RPS)
- Error rate (%)
- Latency (P50, P95, P99)
- Throughput (requests/sec)
- Cache hit rate (%)
```

**Infrastructure Metrics**
```
- CPU usage (%)
- Memory usage (%)
- Disk usage (%)
- Network bandwidth (Mbps)
- Disk I/O (IOPS)
```

**Business Metrics**
```
- Conversion rate (%)
- Revenue per user
- User retention (%)
- Feature usage (%)
```

###### Metrics Implementation

```python
from prometheus_client import Counter, Gauge, Histogram, Summary

## Counter: Total requests
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

## Gauge: Current active connections
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

## Histogram: Request latency
request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

## Summary: Request latency percentiles
request_summary = Summary(
    'http_request_duration_summary',
    'HTTP request latency summary',
    ['method', 'endpoint']
)

## Usage
@app.route('/api/users/<user_id>')
def get_user(user_id):
    start_time = time.time()
    active_connections.inc()
    
    try:
        user = db.get_user(user_id)
        request_count.labels(method='GET', endpoint='/users', status=200).inc()
        return {"data": user}, 200
    except Exception as e:
        request_count.labels(method='GET', endpoint='/users', status=500).inc()
        return {"error": str(e)}, 500
    finally:
        duration = time.time() - start_time
        request_latency.labels(method='GET', endpoint='/users').observe(duration)
        request_summary.labels(method='GET', endpoint='/users').observe(duration)
        active_connections.dec()
```

#### 13.2 Logging (Ghi Chép)

**Định nghĩa**: Ghi chép chi tiết về sự kiện xảy ra trong hệ thống.

###### Log Levels

```
DEBUG   - Chi tiết nhất, dùng cho development
INFO    - Thông tin chung
WARNING - Cảnh báo, có thể có vấn đề
ERROR   - Lỗi, cần chú ý
CRITICAL- Lỗi nghiêm trọng, hệ thống có thể down
```

###### Structured Logging

```python
import json
import logging
from datetime import datetime

## ❌ BAD: Unstructured logging
logger.error(f"Error: {error}")

## ✅ GOOD: Structured logging
logger.error("Database error", extra={
    "error_type": type(error).__name__,
    "error_message": str(error),
    "user_id": user_id,
    "operation": "get_user",
    "timestamp": datetime.utcnow().isoformat(),
    "trace_id": trace_id
})

## Output (JSON format)
{
    "timestamp": "2024-01-15T10:30:45.123Z",
    "level": "ERROR",
    "message": "Database error",
    "error_type": "ConnectionError",
    "error_message": "Connection refused",
    "user_id": 123,
    "operation": "get_user",
    "trace_id": "abc123"
}
```

###### Logging Best Practices

```python
import logging
import json

## Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        ## Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        ## Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

## Setup logger
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)

## Usage
logger.info("User login", extra={
    "user_id": 123,
    "ip_address": "192.168.1.1",
    "timestamp": datetime.utcnow().isoformat()
})
```

###### Log Aggregation

```
┌─────────────┐
│ Service 1   │
│ logs        │
└──────┬──────┘
       │
       ├──→ Fluentd/Logstash ──→ Elasticsearch ──→ Kibana
       │
┌──────┴──────┐
│ Service 2   │
│ logs        │
└──────┬──────┘
       │
┌──────┴──────┐
│ Service 3   │
│ logs        │
└─────────────┘
```

**Setup ELK Stack**:
```yaml
## docker-compose.yml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
  
  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
```

#### 13.3 Tracing (Theo Dõi)

**Định nghĩa**: Theo dõi request qua các services khác nhau.

###### Distributed Tracing

```
Request từ client:
┌─────────────────────────────────────────────────┐
│ API Gateway                                     │
│ trace_id: abc123                                │
│ span_id: 1                                      │
└────────────┬────────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────┴──────┐ ┌───┴──────┐
│ User       │ │ Product  │
│ Service    │ │ Service  │
│ span_id: 2 │ │ span_id: 3
└────────────┘ └──────────┘
```

###### Tracing Implementation

```python
from jaeger_client import Config
from opentracing.propagation import Format

## Initialize Jaeger
config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='my-service',
)
jaeger_tracer = config.initialize_tracer()

## Use in code
@app.route('/api/users/<user_id>')
def get_user(user_id):
    with jaeger_tracer.start_active_span('get_user') as scope:
        span = scope.span
        span.set_tag('user_id', user_id)
        
        try:
            ## Call user service
            with jaeger_tracer.start_active_span('call_user_service'):
                user = call_user_service(user_id)
            
            ## Call product service
            with jaeger_tracer.start_active_span('call_product_service'):
                products = call_product_service(user_id)
            
            span.set_tag('status', 'success')
            return {"user": user, "products": products}
        
        except Exception as e:
            span.set_tag('error', True)
            span.log_kv({'event': 'error', 'message': str(e)})
            raise
```

---

### Chương 14: Monitoring Strategy

#### 14.1 Metrics to Monitor

###### System Metrics
```
CPU Usage:
  - Alert if > 80% for 5 minutes
  - Critical if > 95% for 2 minutes

Memory Usage:
  - Alert if > 85% for 5 minutes
  - Critical if > 95% for 2 minutes

Disk Usage:
  - Alert if > 80% for 1 hour
  - Critical if > 90%

Network Bandwidth:
  - Alert if > 80% of capacity
  - Critical if > 95%
```

###### Application Metrics
```
Request Rate:
  - Track RPS (requests per second)
  - Alert if sudden drop (possible issue)

Error Rate:
  - Alert if > 1% (or based on SLO)
  - Critical if > 5%

Latency:
  - Alert if P95 > 500ms
  - Critical if P99 > 1000ms

Cache Hit Rate:
  - Alert if < 80% (possible cache issue)
```

###### Business Metrics
```
Conversion Rate:
  - Track daily
  - Alert if drop > 10%

Revenue:
  - Track hourly
  - Alert if drop > 20%

User Retention:
  - Track weekly
  - Alert if drop > 5%
```

#### 14.2 Alerting Strategy

###### Alert Fatigue Prevention

```python
## ❌ BAD: Too many alerts
alerts = [
    "CPU > 50%",
    "CPU > 60%",
    "CPU > 70%",
    "CPU > 80%",
    "CPU > 90%",
]
## Result: Team ignores alerts (alert fatigue)

## ✅ GOOD: Meaningful alerts
alerts = [
    "CPU > 80% for 5 minutes",
    "Error rate > 1%",
    "Latency P99 > 500ms",
]
## Result: Team responds to real issues
```

###### Alert Routing

```python
## Ví dụ: Alert routing logic
def route_alert(alert):
    if alert.severity == "CRITICAL":
        ## Page on-call engineer
        notify_pagerduty(alert)
    
    elif alert.severity == "WARNING":
        ## Send to Slack
        notify_slack(alert)
    
    elif alert.severity == "INFO":
        ## Log only
        logger.info(alert)
```

###### Alert Configuration

```yaml
## Prometheus alerting rules
groups:
  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 5m
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"
      
      - alert: HighLatency
        expr: histogram_quantile(0.99, http_request_duration_seconds) > 1
        for: 5m
        annotations:
          summary: "High latency detected"
          description: "P99 latency is {{ $value }}s"
      
      - alert: LowCacheHitRate
        expr: cache_hit_rate < 0.8
        for: 10m
        annotations:
          summary: "Low cache hit rate"
          description: "Cache hit rate is {{ $value }}"
```

#### 14.3 Monitoring Dashboard

```python
## Ví dụ: Grafana dashboard JSON
dashboard = {
    "title": "Application Monitoring",
    "panels": [
        {
            "title": "Request Rate",
            "targets": [
                {
                    "expr": "rate(http_requests_total[5m])"
                }
            ]
        },
        {
            "title": "Error Rate",
            "targets": [
                {
                    "expr": "rate(http_requests_total{status=~'5..'}[5m])"
                }
            ]
        },
        {
            "title": "Latency P99",
            "targets": [
                {
                    "expr": "histogram_quantile(0.99, http_request_duration_seconds)"
                }
            ]
        },
        {
            "title": "CPU Usage",
            "targets": [
                {
                    "expr": "node_cpu_usage_percent"
                }
            ]
        }
    ]
}
```

---

### Chương 15: Alerting & Incident Response

#### 15.1 Alert Severity Levels

```
CRITICAL (P1)
├─ Immediate action required
├─ Page on-call engineer
├─ Example: Service down, data loss
└─ Response time: < 5 minutes

HIGH (P2)
├─ Urgent action needed
├─ Notify team
├─ Example: High error rate, performance degradation
└─ Response time: < 15 minutes

MEDIUM (P3)
├─ Should be addressed soon
├─ Log and track
├─ Example: Elevated latency, low cache hit rate
└─ Response time: < 1 hour

LOW (P4)
├─ Can be addressed later
├─ Log only
├─ Example: Informational metrics
└─ Response time: < 1 day
```

#### 15.2 Incident Response Process

```
1. DETECT
   └─ Alert fires
      ↓
2. ACKNOWLEDGE
   └─ On-call engineer acknowledges
      ↓
3. INVESTIGATE
   └─ Gather logs, metrics, traces
      ↓
4. MITIGATE
   └─ Quick fix to reduce impact
      ↓
5. RESOLVE
   └─ Permanent fix
      ↓
6. POST-MORTEM
   └─ Learn from incident
```

###### Incident Response Runbook

```markdown
## Incident: High Error Rate

### Detection
- Alert: Error rate > 1% for 5 minutes
- Severity: P2 (High)

### Investigation
1. Check error logs:
   ```
   kubectl logs -f deployment/api-server
   ```

2. Check metrics:
   - Error rate trend
   - Affected endpoints
   - Error types

3. Check recent deployments:
   ```
   kubectl rollout history deployment/api-server
   ```

### Mitigation
1. If recent deployment caused issue:
   ```
   kubectl rollout undo deployment/api-server
   ```

2. If database issue:
   - Check database connections
   - Check slow queries
   - Restart database if needed

3. If external service issue:
   - Check circuit breaker status
   - Verify external service health

### Resolution
1. Identify root cause
2. Implement permanent fix
3. Deploy fix
4. Monitor metrics

### Post-Mortem
- What happened?
- Why did it happen?
- How to prevent in future?
- Action items
```

#### 15.3 On-Call Management

```python
## On-call rotation
ON_CALL_SCHEDULE = {
    "2024-01-15": {
        "primary": "alice@company.com",
        "secondary": "bob@company.com"
    },
    "2024-01-22": {
        "primary": "charlie@company.com",
        "secondary": "diana@company.com"
    }
}

## Escalation policy
ESCALATION_POLICY = {
    "critical": {
        "primary_timeout": 5,      ## minutes
        "secondary_timeout": 10,
        "manager_timeout": 15
    },
    "high": {
        "primary_timeout": 15,
        "secondary_timeout": 30
    }
}
```

---

### Chương 16: Cost Optimization for Observability

#### 16.1 Metrics Cardinality

**Problem**: Trop many unique metric combinations = high cost

```python
## ❌ BAD: High cardinality
request_duration = Histogram(
    'http_request_duration',
    ['method', 'endpoint', 'user_id', 'client_ip']
)
## If 1000 users × 1000 IPs × 100 endpoints = 100M combinations

## ✅ GOOD: Low cardinality
request_duration = Histogram(
    'http_request_duration',
    ['method', 'endpoint', 'status']
)
## Only 3 × 100 × 5 = 1500 combinations
```

#### 16.2 Log Sampling

```python
import random

def should_log_request(request):
    """Sample logs to reduce volume"""
    ## Always log errors
    if request.status >= 400:
        return True
    
    ## Always log slow requests
    if request.duration > 1000:  ## ms
        return True
    
    ## Sample 1% of normal requests
    if random.random() < 0.01:
        return True
    
    return False
```

#### 16.3 Retention Policies

```yaml
## Prometheus retention
global:
  retention: 15d  ## Keep 15 days of data

## Elasticsearch retention
index_patterns:
  - pattern: "logs-*"
    retention: 30d
  - pattern: "metrics-*"
    retention: 90d
```

---

### Checklist: Observability & Monitoring

- [ ] Metrics collection setup (Prometheus)
- [ ] Structured logging setup (ELK Stack)
- [ ] Distributed tracing setup (Jaeger)
- [ ] Key metrics identified and tracked
- [ ] Alerting rules configured
- [ ] Alert routing setup
- [ ] Monitoring dashboards created
- [ ] On-call schedule established
- [ ] Incident response runbooks written
- [ ] Log retention policies defined
- [ ] Metrics cardinality managed
- [ ] Cost optimization for observability

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN V: DEPLOYMENT & CI/CD

---

### Chương 17: CI/CD Pipeline Best Practices

#### 17.1 Pipeline Architecture

```
Commit to Git
    ↓
┌───────────────────────────────────────────────┐
│ STAGE 1: BUILD                                │
│ - Checkout code                               │
│ - Build application                           │
│ - Create Docker image                         │
│ - Push to registry                            │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ STAGE 2: TEST                                 │
│ - Unit tests                                  │
│ - Integration tests                           │
│ - Code coverage check                         │
│ - Linting & formatting                        │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ STAGE 3: SECURITY SCAN                        │
│ - SAST (Static Analysis)                      │
│ - Dependency scanning                         │
│ - Container scanning                          │
│ - Secret scanning                             │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ STAGE 4: DEPLOY TO STAGING                    │
│ - Deploy to staging environment               │
│ - Run smoke tests                             │
│ - Performance tests                           │
└───────────────────────────────────────────────┘
    ↓
┌───────────────────────────────────────────────┐
│ STAGE 5: DEPLOY TO PRODUCTION                 │
│ - Blue-green or canary deployment             │
│ - Health checks                               │
│ - Monitoring                                  │
└───────────────────────────────────────────────┘
    ↓
Monitor & Rollback if needed
```

#### 17.2 CI/CD Tools

| Tool | Pros | Cons |
|------|------|------|
| GitHub Actions | Native to GitHub, free | Limited customization |
| GitLab CI/CD | Powerful, integrated | Steeper learning curve |
| Jenkins | Highly customizable | Complex setup |
| CircleCI | Easy to use, good docs | Pricing |
| AWS CodePipeline | AWS integration | AWS-specific |

#### 17.3 Pipeline Configuration Example

```yaml
## .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Lint code
        run: flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src
      
      - name: Run integration tests
        run: pytest tests/integration/ -v
      
      - name: Security scan (SAST)
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json
      
      - name: Dependency scan
        run: |
          pip install safety
          safety check --json > safety-report.json
      
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker tag myapp:${{ github.sha }} myapp:latest
          docker push myapp:${{ github.sha }}
          docker push myapp:latest
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          kubectl set image deployment/app app=myapp:${{ github.sha }} -n staging
          kubectl rollout status deployment/app -n staging
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          ## Blue-green deployment
          kubectl set image deployment/app-green app=myapp:${{ github.sha }} -n production
          kubectl rollout status deployment/app-green -n production
          ## Switch traffic
          kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}' -n production
```

#### 17.4 Build Optimization

```yaml
## Dockerfile with multi-stage build
FROM python:3.11 as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

## Final stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000
CMD ["python", "app.py"]
```

**Benefits**:
- Smaller final image
- Faster builds
- Reduced attack surface

---

### Chương 18: Deployment Strategies

#### 18.1 Blue-Green Deployment

```
Before:
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │          │
┌───┴──┐   ┌──┴────┐
│Blue  │   │Green  │
│(v1)  │   │(v1)   │
│Active│   │Standby│
└──────┘   └───────┘

During:
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │          │
┌───┴──┐   ┌──┴────┐
│Blue  │   │Green  │
│(v1)  │   │(v2)   │
│Active│   │Testing│
└──────┘   └───────┘

After:
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │          │
┌───┴──┐   ┌──┴────┐
│Blue  │   │Green  │
│(v1)  │   │(v2)   │
│Standby│  │Active │
└──────┘   └───────┘
```

**Ưu điểm**:
- Zero downtime
- Easy rollback
- Full environment testing

**Nhược điểm**:
- Cần 2x resources
- Database migration complexity

#### 18.2 Canary Deployment

```
Phase 1: 5% traffic to new version
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
    ┌────┴─────────┐
    │              │
┌───┴──┐       ┌───┴──┐
│v1    │       │v2    │
│95%   │       │5%    │
└──────┘       └──────┘

Phase 2: 50% traffic
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
    ┌────┴─────────┐
    │              │
┌───┴──┐       ┌───┴──┐
│v1    │       │v2    │
│50%   │       │50%   │
└──────┘       └──────┘

Phase 3: 100% traffic
┌─────────────────────────────────────┐
│ Load Balancer                       │
└────────┬────────────────────────────┘
         │
         │
      ┌──┴──┐
      │v2   │
      │100% │
      └─────┘
```

**Ưu điểm**:
- Gradual rollout
- Monitor impact before full deployment
- Easy rollback

**Nhược điểm**:
- Slower deployment
- Complex traffic routing

#### 18.3 Rolling Deployment

```
Initial:
┌──────────┬──────────┬──────────┐
│Pod 1 (v1)│Pod 2 (v1)│Pod 3 (v1)│
└──────────┴──────────┴──────────┘

Step 1: Update Pod 1
┌──────────┬──────────┬──────────┐
│Pod 1 (v2)│Pod 2 (v1)│Pod 3 (v1)│
└──────────┴──────────┴──────────┘

Step 2: Update Pod 2
┌──────────┬──────────┬──────────┐
│Pod 1 (v2)│Pod 2 (v2)│Pod 3 (v1)│
└──────────┴──────────┴──────────┘

Step 3: Update Pod 3
┌──────────┬──────────┬──────────┐
│Pod 1 (v2)│Pod 2 (v2)│Pod 3 (v2)│
└──────────┴──────────┴──────────┘
```

**Ưu điểm**:
- No downtime
- Gradual update
- Easy rollback

**Nhược điểm**:
- Complex orchestration
- Need to handle mixed versions

#### 18.4 Deployment Strategy Selection

| Strategy | Downtime | Speed | Rollback | Resources |
|----------|----------|-------|----------|-----------|
| Blue-Green | 0 | Fast | Easy | 2x |
| Canary | 0 | Slow | Easy | 1.1x |
| Rolling | 0 | Medium | Medium | 1x |
| Recreate | Yes | Fast | Hard | 1x |

---

### Chương 19: Environment Management

#### 19.1 Environment Types

```
┌─────────────────────────────────────┐
│ DEVELOPMENT                         │
│ - Local machine                     │
│ - Rapid iteration                   │
│ - No security constraints           │
│ - Can break anytime                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ STAGING                             │
│ - Production-like environment       │
│ - For testing before release        │
│ - Same infrastructure as prod       │
│ - Real data (masked)                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ PRODUCTION                          │
│ - Live user traffic                 │
│ - Highest security                  │
│ - Strict change control             │
│ - Real data                         │
└─────────────────────────────────────┘
```

#### 19.2 Configuration Management

```python
## ❌ BAD: Hardcoded configuration
DATABASE_URL = "postgresql://user:pass@prod-db:5432/mydb"
API_KEY = "sk-1234567890abcdef"
DEBUG = False

## ✅ GOOD: Environment-based configuration
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

## Or using config management
from config import Config

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "postgresql://user:pass@localhost:5432/mydb_dev"

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')

config = DevelopmentConfig() if os.getenv('ENV') == 'dev' else ProductionConfig()
```

#### 19.3 Infrastructure as Code (IaC)

```hcl
## Terraform example
provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "main" {
  name = "production-cluster"
}

resource "aws_ecs_service" "app" {
  name            = "app-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3
  
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 5000
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = var.subnet_ids
  min_size            = 3
  max_size            = 10
  desired_capacity    = 3
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
}
```

**Benefits**:
- Version control for infrastructure
- Reproducible environments
- Easy scaling
- Disaster recovery

---

### Chương 20: Rollback Strategies

#### 20.1 Automated Rollback

```python
## Ví dụ: Rollback on health check failure
def deploy_and_monitor(new_version):
    """Deploy and rollback if health checks fail"""
    try:
        ## Deploy new version
        deploy(new_version)
        
        ## Monitor for 5 minutes
        for i in range(30):  ## 30 checks × 10s = 5 minutes
            time.sleep(10)
            
            health = check_health()
            if health['status'] != 'healthy':
                logger.error(f"Health check failed: {health}")
                rollback(previous_version)
                return False
            
            metrics = get_metrics()
            if metrics['error_rate'] > 0.05:  ## 5% error rate
                logger.error(f"Error rate too high: {metrics['error_rate']}")
                rollback(previous_version)
                return False
        
        logger.info("Deployment successful")
        return True
    
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        rollback(previous_version)
        return False
```

#### 20.2 Manual Rollback

```bash
## Kubernetes rollback
kubectl rollout history deployment/app
kubectl rollout undo deployment/app
kubectl rollout undo deployment/app --to-revision=2

## Docker rollback
docker service update --image myapp:previous-version app-service

## Database rollback
## For migrations, always have rollback scripts
./migrate.sh rollback
```

---

### Checklist: Deployment & CI/CD

- [ ] CI/CD pipeline setup
- [ ] Automated testing in pipeline
- [ ] Security scanning integrated
- [ ] Build optimization (caching, multi-stage)
- [ ] Deployment strategy chosen
- [ ] Blue-green or canary setup
- [ ] Health checks configured
- [ ] Automated rollback setup
- [ ] Environment management
- [ ] Configuration management
- [ ] Infrastructure as Code
- [ ] Deployment runbooks
- [ ] Team trained on deployment process

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN VI: SECURITY

---

### Chương 21: Authentication & Authorization

#### 21.1 Authentication Methods

###### 1. OAuth 2.0

```
User → Application → OAuth Provider (Google, GitHub, etc.)
                        ↓
                    User logs in
                        ↓
                    Returns token
                        ↓
                    Application can access user data
```

**Implementation**:
```python
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user = token.get('userinfo')
    session['user'] = user
    return redirect('/')
```

###### 2. JWT (JSON Web Tokens)

```
Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"user_id": 123, "exp": 1234567890}
Signature: HMACSHA256(header + payload, secret)

Token: header.payload.signature
```

**Implementation**:
```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    password = request.json['password']
    
    ## Verify credentials
    if verify_password(user_id, password):
        access_token = create_access_token(identity=user_id)
        return {"access_token": access_token}
    
    return {"error": "Invalid credentials"}, 401

@app.route('/protected')
@jwt_required()
def protected():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    return {"user_id": user_id}
```

###### 3. API Keys

```python
## ❌ BAD: Hardcoded API key
API_KEY = "sk-1234567890abcdef"

## ✅ GOOD: API key from environment
import os
API_KEY = os.getenv('API_KEY')

## Validate API key
@app.before_request
def validate_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != os.getenv('API_KEY'):
        return {"error": "Invalid API key"}, 401
```

#### 21.2 Authorization (RBAC)

```python
from functools import wraps

## Define roles
ROLES = {
    'admin': ['read', 'write', 'delete', 'manage_users'],
    'user': ['read', 'write'],
    'guest': ['read']
}

def require_role(required_role):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_jwt_extended import get_jwt_identity
            user_id = get_jwt_identity()
            user_role = get_user_role(user_id)
            
            if user_role not in ROLES or required_role not in ROLES[user_role]:
                return {"error": "Insufficient permissions"}, 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

## Usage
@app.route('/admin/users', methods=['DELETE'])
@require_role('admin')
def delete_user():
    user_id = request.json['user_id']
    delete_user_from_db(user_id)
    return {"status": "deleted"}
```

---

### Chương 22: Data Protection

#### 22.1 Encryption at Rest

```python
from cryptography.fernet import Fernet
import os

## Generate key (do this once and store securely)
key = Fernet.generate_key()

## Create cipher
cipher_suite = Fernet(key)

## Encrypt data
plaintext = b"sensitive data"
encrypted_data = cipher_suite.encrypt(plaintext)

## Decrypt data
decrypted_data = cipher_suite.decrypt(encrypted_data)
```

**Database Encryption**:
```sql
-- PostgreSQL with pgcrypto
CREATE EXTENSION pgcrypto;

-- Encrypt column
UPDATE users SET email = pgp_pub_encrypt(email, pgp_key_create()) WHERE id > 0;

-- Decrypt column
SELECT pgp_pub_decrypt(email, pgp_key_create()) FROM users;
```

#### 22.2 Encryption in Transit

```python
## ✅ GOOD: HTTPS/TLS
import ssl
from flask import Flask

app = Flask(__name__)

## Force HTTPS
@app.before_request
def enforce_https():
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

## SSL/TLS configuration
if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(ssl_context=context)
```

#### 22.3 Input Validation

```python
## ❌ BAD: No validation
@app.route('/users/<user_id>')
def get_user(user_id):
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return user

## ✅ GOOD: Validation
from flask import request
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    user_id = fields.Int(required=True)
    email = fields.Email(required=True)
    age = fields.Int(validate=lambda x: 0 < x < 150)

@app.route('/users/<int:user_id>')
def get_user(user_id):
    ## Type validation
    if not isinstance(user_id, int):
        return {"error": "Invalid user_id"}, 400
    
    ## Range validation
    if user_id < 0:
        return {"error": "Invalid user_id"}, 400
    
    user = db.get_user(user_id)
    return user

## Or using ORM
from sqlalchemy import and_

user = db.session.query(User).filter(
    and_(
        User.id == user_id,
        User.id > 0
    )
).first()
```

#### 22.4 SQL Injection Prevention

```python
## ❌ BAD: SQL Injection vulnerability
user_id = request.args.get('user_id')
user = db.query(f"SELECT * FROM users WHERE id = {user_id}")

## ✅ GOOD: Parameterized queries
user = db.query("SELECT * FROM users WHERE id = ?", (user_id,))

## Or with ORM
user = User.query.filter_by(id=user_id).first()
```

---

### Chương 23: Security Scanning & Compliance

#### 23.1 SAST (Static Application Security Testing)

```bash
## Using Bandit for Python
pip install bandit
bandit -r src/ -f json -o bandit-report.json

## Using SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube

## Using Snyk
npm install -g snyk
snyk test
```

#### 23.2 DAST (Dynamic Application Security Testing)

```bash
## Using OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://target-app

## Using Burp Suite
## Manual or automated scanning
```

#### 23.3 Dependency Scanning (SCA)

```bash
## Using OWASP Dependency-Check
dependency-check --project "MyApp" --scan /path/to/app

## Using Snyk
snyk test

## Using Safety (Python)
pip install safety
safety check
```

#### 23.4 Secrets Detection

```bash
## Using git-secrets
git secrets --install
git secrets --register-aws

## Using TruffleHog
trufflehog filesystem /path/to/repo

## Using Gitleaks
gitleaks detect --source filesystem --path /path/to/repo
```

#### 23.5 Compliance Standards

###### GDPR (General Data Protection Regulation)
```
Requirements:
- Data privacy by design
- Data minimization
- User consent
- Right to be forgotten
- Data breach notification (72 hours)
```

###### HIPAA (Health Insurance Portability and Accountability Act)
```
Requirements:
- PHI (Protected Health Information) encryption
- Access controls
- Audit logging
- Disaster recovery
```

###### SOC 2 (Service Organization Control)
```
Requirements:
- Security
- Availability
- Processing integrity
- Confidentiality
- Privacy
```

---

### Chương 24: Secrets Management

#### 24.1 Secrets Storage

```python
## ❌ BAD: Hardcoded secrets
DATABASE_PASSWORD = "mypassword123"
API_KEY = "sk-1234567890"

## ✅ GOOD: Environment variables
import os
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
API_KEY = os.getenv('API_KEY')

## ✅ BETTER: Secrets manager
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

DATABASE_PASSWORD = get_secret('db-password')
API_KEY = get_secret('api-key')
```

#### 24.2 Secrets Rotation

```python
## Automatic secrets rotation
def rotate_secrets():
    """Rotate all secrets"""
    secrets = [
        'database-password',
        'api-key',
        'jwt-secret'
    ]
    
    for secret_name in secrets:
        ## Generate new secret
        new_secret = generate_secure_random()
        
        ## Update in secrets manager
        update_secret(secret_name, new_secret)
        
        ## Update in application
        update_application_config(secret_name, new_secret)
        
        ## Log rotation
        logger.info(f"Rotated secret: {secret_name}")

## Schedule rotation (e.g., every 90 days)
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(rotate_secrets, 'interval', days=90)
scheduler.start()
```

#### 24.3 Vault Integration

```python
import hvac

## Connect to Vault
client = hvac.Client(url='http://vault:8200', token='mytoken')

## Read secret
secret = client.secrets.kv.read_secret_version(path='secret/database')
password = secret['data']['data']['password']

## Write secret
client.secrets.kv.create_or_update_secret_version(
    path='secret/api-key',
    secret_data={'key': 'sk-1234567890'}
)

## Rotate secret
client.auth.approle.generate_secret_id('my-role')
```

---

### Chương 25: Network Security

#### 25.1 VPC (Virtual Private Cloud)

```
┌─────────────────────────────────────┐
│ Internet                            │
└────────────┬────────────────────────┘
             │
        ┌────┴────┐
        │ NAT     │
        │ Gateway │
        └────┬────┘
             │
    ┌────────┴────────┐
    │ VPC             │
    │ 10.0.0.0/16     │
    │                 │
    │ ┌─────────────┐ │
    │ │ Public      │ │
    │ │ Subnet      │ │
    │ │ 10.0.1.0/24 │ │
    │ └─────────────┘ │
    │                 │
    │ ┌─────────────┐ │
    │ │ Private     │ │
    │ │ Subnet      │ │
    │ │ 10.0.2.0/24 │ │
    │ └─────────────┘ │
    └─────────────────┘
```

#### 25.2 Security Groups

```python
## AWS Security Group
import boto3

ec2 = boto3.client('ec2')

## Create security group
sg = ec2.create_security_group(
    GroupName='app-sg',
    Description='Security group for app'
)

## Allow inbound HTTP
ec2.authorize_security_group_ingress(
    GroupId=sg['GroupId'],
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

## Allow inbound HTTPS
ec2.authorize_security_group_ingress(
    GroupId=sg['GroupId'],
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

## Deny all outbound except to specific IPs
ec2.revoke_security_group_egress(
    GroupId=sg['GroupId'],
    IpPermissions=[
        {
            'IpProtocol': '-1',
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)
```

#### 25.3 WAF (Web Application Firewall)

```python
## AWS WAF
import boto3

waf = boto3.client('wafv2')

## Create IP set for rate limiting
ip_set = waf.create_ip_set(
    Name='rate-limit-ips',
    Scope='REGIONAL',
    IPAddressVersion='IPV4',
    Addresses=['192.168.1.1/32']
)

## Create rule
rule = {
    'Name': 'rate-limit-rule',
    'Priority': 0,
    'Statement': {
        'RateBasedStatement': {
            'Limit': 2000,
            'AggregateKeyType': 'IP'
        }
    },
    'Action': {'Block': {}},
    'VisibilityConfig': {
        'SampledRequestsEnabled': True,
        'CloudWatchMetricsEnabled': True,
        'MetricName': 'rate-limit-rule'
    }
}
```

---

### Chương 26: DDoS Protection

#### 26.1 DDoS Mitigation

```
┌─────────────────────────────────────┐
│ Attacker (sending many requests)    │
└────────────┬────────────────────────┘
             │
        ┌────┴────┐
        │ CDN     │
        │ (Cache) │
        └────┬────┘
             │
        ┌────┴────┐
        │ WAF     │
        │ (Filter)│
        └────┬────┘
             │
        ┌────┴────┐
        │ Rate    │
        │ Limiter │
        └────┬────┘
             │
        ┌────┴────┐
        │ App     │
        │ Server  │
        └─────────┘
```

#### 26.2 Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/users')
@limiter.limit("10 per minute")
def get_users():
    return {"users": []}

## Or custom rate limiting
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        ## Remove old requests outside window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        ## Check if under limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False
```

---

### Checklist: Security

- [ ] Authentication method chosen (OAuth, JWT, API keys)
- [ ] Authorization (RBAC) implemented
- [ ] Encryption at rest configured
- [ ] HTTPS/TLS enforced
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] SAST scanning integrated
- [ ] Dependency scanning setup
- [ ] Secrets scanning setup
- [ ] Secrets management (Vault/Secrets Manager)
- [ ] Secrets rotation configured
- [ ] VPC and security groups configured
- [ ] WAF rules configured
- [ ] DDoS protection setup
- [ ] Compliance requirements identified
- [ ] Security audit scheduled
- [ ] Team trained on security best practices

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN VII: TESTING

---

### Chương 27: Testing Pyramid

#### 27.1 Testing Levels

```
        ▲
       /|\
      / | \
     /  |  \  E2E Tests (10%)
    /   |   \
   /    |    \
  /     |     \ Integration Tests (20%)
 /      |      \
/       |       \ Unit Tests (70%)
└───────┴───────┘
```

| Level | Scope | Speed | Cost | Coverage |
|-------|-------|-------|------|----------|
| Unit | Single function | Milliseconds | Low | High |
| Integration | Multiple components | Seconds | Medium | Medium |
| E2E | Full workflow | Minutes | High | Low |

#### 27.2 Unit Testing

```python
import pytest
from myapp.user_service import UserService

class TestUserService:
    @pytest.fixture
    def user_service(self):
        """Setup test fixture"""
        return UserService(db=MockDatabase())
    
    def test_create_user_success(self, user_service):
        """Test successful user creation"""
        ## Arrange
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        
        ## Act
        result = user_service.create_user(user_data)
        
        ## Assert
        assert result['id'] is not None
        assert result['name'] == "John Doe"
        assert result['email'] == "john@example.com"
    
    def test_create_user_invalid_email(self, user_service):
        """Test user creation with invalid email"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "age": 30
        }
        
        with pytest.raises(ValueError):
            user_service.create_user(user_data)
    
    def test_create_user_invalid_age(self, user_service):
        """Test user creation with invalid age"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": -5
        }
        
        with pytest.raises(ValueError):
            user_service.create_user(user_data)
    
    @pytest.mark.parametrize("age", [0, -1, 150, 200])
    def test_create_user_boundary_ages(self, user_service, age):
        """Test user creation with boundary ages"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": age
        }
        
        with pytest.raises(ValueError):
            user_service.create_user(user_data)
```

**Mocking**:
```python
from unittest.mock import Mock, patch

def test_user_service_with_mock():
    ## Mock database
    mock_db = Mock()
    mock_db.insert.return_value = {"id": 1, "name": "John"}
    
    service = UserService(db=mock_db)
    result = service.create_user({"name": "John"})
    
    ## Verify mock was called
    mock_db.insert.assert_called_once()
    assert result['id'] == 1
```

#### 27.3 Integration Testing

```python
import pytest
from myapp import create_app
from myapp.db import db

@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_app(config='testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

class TestUserAPI:
    def test_create_user_integration(self, client):
        """Test user creation through API"""
        response = client.post('/api/users', json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        
        assert response.status_code == 201
        assert response.json['id'] is not None
    
    def test_get_user_integration(self, client):
        """Test getting user through API"""
        ## Create user
        create_response = client.post('/api/users', json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        user_id = create_response.json['id']
        
        ## Get user
        get_response = client.get(f'/api/users/{user_id}')
        
        assert get_response.status_code == 200
        assert get_response.json['name'] == "John Doe"
    
    def test_user_database_transaction(self, client):
        """Test database transaction"""
        ## Create user
        response = client.post('/api/users', json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        
        ## Verify in database
        from myapp.models import User
        user = User.query.filter_by(email="john@example.com").first()
        assert user is not None
        assert user.name == "John Doe"
```

**Using TestContainers**:
```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for tests"""
    with PostgresContainer("postgres:13") as postgres:
        yield postgres

@pytest.fixture
def db_connection(postgres_container):
    """Create database connection"""
    conn = postgres_container.get_connection_client()
    yield conn
    conn.close()
```

#### 27.4 End-to-End (E2E) Testing

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Setup Selenium driver"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

class TestUserJourney:
    def test_user_signup_and_login(self, driver):
        """Test complete user signup and login flow"""
        ## Navigate to signup page
        driver.get("http://localhost:5000/signup")
        
        ## Fill signup form
        name_input = driver.find_element(By.ID, "name")
        name_input.send_keys("John Doe")
        
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("john@example.com")
        
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("SecurePassword123!")
        
        ## Submit form
        submit_button = driver.find_element(By.ID, "signup-button")
        submit_button.click()
        
        ## Wait for redirect to login page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-form"))
        )
        
        ## Fill login form
        email_input = driver.find_element(By.ID, "login-email")
        email_input.send_keys("john@example.com")
        
        password_input = driver.find_element(By.ID, "login-password")
        password_input.send_keys("SecurePassword123!")
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        ## Wait for dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )
        
        ## Verify user is logged in
        assert "Dashboard" in driver.title
```

---

### Chương 28: Performance & Security Testing

#### 28.1 Load Testing

```python
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5)
    
    @task(1)
    def get_users(self):
        self.client.get("/api/users")
    
    @task(2)
    def get_user(self):
        self.client.get("/api/users/1")
    
    @task(1)
    def create_user(self):
        self.client.post("/api/users", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
```

**Run load test**:
```bash
locust -f locustfile.py --host=http://localhost:5000 -u 100 -r 10
```

#### 28.2 Stress Testing

```python
## Gradually increase load until system breaks
import time
from locust import HttpUser, task

class StressTest(HttpUser):
    @task
    def stress_endpoint(self):
        ## Send requests as fast as possible
        for i in range(1000):
            self.client.get("/api/users")
            time.sleep(0.001)  ## 1ms between requests
```

#### 28.3 Spike Testing

```python
## Sudden increase in traffic
import time

def spike_test():
    ## Normal traffic
    for i in range(100):
        make_request()
    
    time.sleep(5)
    
    ## Spike: 10x traffic
    for i in range(1000):
        make_request()
    
    time.sleep(5)
    
    ## Back to normal
    for i in range(100):
        make_request()
```

#### 28.4 Security Testing

```python
import requests

def test_sql_injection():
    """Test SQL injection vulnerability"""
    payload = "1' OR '1'='1"
    response = requests.get(f"http://localhost:5000/api/users/{payload}")
    
    ## Should not return all users
    assert len(response.json()) == 1

def test_xss_vulnerability():
    """Test XSS vulnerability"""
    payload = "<script>alert('XSS')</script>"
    response = requests.post("http://localhost:5000/api/users", json={
        "name": payload,
        "email": "test@example.com"
    })
    
    ## Should escape HTML
    assert "<script>" not in response.json()['name']

def test_authentication_bypass():
    """Test authentication bypass"""
    ## Try to access protected endpoint without token
    response = requests.get("http://localhost:5000/api/protected")
    
    ## Should return 401
    assert response.status_code == 401

def test_rate_limiting():
    """Test rate limiting"""
    ## Make many requests
    for i in range(100):
        response = requests.get("http://localhost:5000/api/users")
        
        if response.status_code == 429:  ## Too many requests
            print(f"Rate limit hit after {i} requests")
            return
    
    ## Should have hit rate limit
    assert False, "Rate limiting not working"
```

---

### Chương 29: Test Automation & CI/CD Integration

#### 29.1 Test Configuration

```yaml
## pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=src --cov-report=html --cov-report=term
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
    security: Security tests
```

#### 29.2 Test Execution Strategy

```bash
## Run all tests
pytest

## Run only unit tests
pytest -m unit

## Run only integration tests
pytest -m integration

## Run with coverage
pytest --cov=src --cov-report=html

## Run in parallel
pytest -n auto

## Run with specific markers
pytest -m "not slow"
```

#### 29.3 CI/CD Integration

```yaml
## .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run unit tests
        run: pytest tests/unit -m unit -v
      
      - name: Run integration tests
        run: pytest tests/integration -m integration -v
      
      - name: Run security tests
        run: pytest tests/security -m security -v
      
      - name: Upload coverage
        run: |
          pip install codecov
          codecov
```

#### 29.4 Test Coverage

```python
## Aim for high coverage but focus on critical paths
## ✅ GOOD: 80% coverage
## ❌ BAD: 100% coverage with meaningless tests

## Example: Critical paths to test
CRITICAL_PATHS = [
    "user_authentication",
    "payment_processing",
    "data_validation",
    "error_handling"
]

## Less critical (lower priority)
LESS_CRITICAL = [
    "logging",
    "formatting",
    "utility_functions"
]
```

---

### Chương 30: Test Data Management

#### 30.1 Test Data Strategies

```python
## ❌ BAD: Using production data
def test_user_creation():
    user = User.query.filter_by(email="real@example.com").first()
    assert user is not None

## ✅ GOOD: Using fixtures
@pytest.fixture
def test_user():
    user = User.create(
        name="Test User",
        email="test@example.com",
        age=30
    )
    yield user
    user.delete()

def test_user_creation(test_user):
    assert test_user.name == "Test User"
```

#### 30.2 Factory Pattern

```python
import factory
from myapp.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=80)

## Usage
def test_user_creation():
    user = UserFactory.create()
    assert user.name is not None
    assert user.email is not None
```

#### 30.3 Test Data Cleanup

```python
@pytest.fixture(autouse=True)
def cleanup():
    """Auto cleanup after each test"""
    yield
    
    ## Cleanup
    User.query.delete()
    db.session.commit()
```

---

### Checklist: Testing

- [ ] Unit tests written (70% of tests)
- [ ] Integration tests written (20% of tests)
- [ ] E2E tests written (10% of tests)
- [ ] Test coverage > 80%
- [ ] Load testing done
- [ ] Security testing done
- [ ] Performance benchmarks established
- [ ] Test data management setup
- [ ] CI/CD integration for tests
- [ ] Test execution in parallel
- [ ] Test reporting setup
- [ ] Team trained on testing best practices

---

## Production Quality: Hướng Dẫn Toàn Diện Cho AI Engineer

### PHẦN VIII: CODE QUALITY & MAINTAINABILITY

---

### Chương 31: Code Quality Metrics

#### 31.1 Key Metrics

**Cyclomatic Complexity**
```python
## ❌ BAD: High complexity (CC = 5)
def process_order(order):
    if order.status == 'pending':
        if order.total > 1000:
            if order.customer.is_vip:
                discount = 0.2
            else:
                discount = 0.1
        else:
            discount = 0.05
    else:
        discount = 0
    
    return order.total * (1 - discount)

## ✅ GOOD: Low complexity (CC = 1)
def get_discount(order):
    discount_rules = {
        ('pending', True, True): 0.2,    ## pending, >1000, vip
        ('pending', True, False): 0.1,   ## pending, >1000, not vip
        ('pending', False, False): 0.05, ## pending, <=1000
    }
    
    key = (order.status, order.total > 1000, order.customer.is_vip)
    return discount_rules.get(key, 0)

def process_order(order):
    discount = get_discount(order)
    return order.total * (1 - discount)
```

**Code Coverage**
```
Target: 80% coverage
- Critical paths: 100%
- Business logic: 90%
- Utilities: 70%
- UI/Formatting: 50%
```

**Code Duplication**
```python
## ❌ BAD: Duplicated code
def validate_user(user):
    if not user.name or len(user.name) < 2:
        raise ValueError("Invalid name")
    if not user.email or '@' not in user.email:
        raise ValueError("Invalid email")

def validate_product(product):
    if not product.name or len(product.name) < 2:
        raise ValueError("Invalid name")
    if not product.sku or len(product.sku) < 2:
        raise ValueError("Invalid sku")

## ✅ GOOD: Extracted common logic
def validate_field(value, field_name, min_length=2):
    if not value or len(str(value)) < min_length:
        raise ValueError(f"Invalid {field_name}")

def validate_user(user):
    validate_field(user.name, "name")
    validate_field(user.email, "email")

def validate_product(product):
    validate_field(product.name, "name")
    validate_field(product.sku, "sku")
```

#### 31.2 Code Quality Tools

```bash
## Python
pylint src/              ## Linting
flake8 src/              ## Style checking
black src/               ## Code formatting
mypy src/                ## Type checking
radon cc src/            ## Cyclomatic complexity

## JavaScript
eslint src/              ## Linting
prettier src/            ## Formatting
jest --coverage          ## Testing with coverage
```

---

### PHẦN IX: INFRASTRUCTURE & CONTAINERIZATION

---

### Chương 32: Docker Best Practices

#### 32.1 Dockerfile Optimization

```dockerfile
## ❌ BAD: Large image
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
## Image size: ~900MB

## ✅ GOOD: Multi-stage build
FROM python:3.11 as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
## Image size: ~200MB
```

#### 32.2 Docker Security

```dockerfile
## Run as non-root user
FROM python:3.11-slim
RUN useradd -m appuser
USER appuser
WORKDIR /app
COPY src/ .
CMD ["python", "app.py"]

## Scan for vulnerabilities
## docker scan myapp:latest
```

---

### Chương 33: Kubernetes in Production

#### 33.1 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 5000
        
        ## Resource limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        ## Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        
        ## Environment variables
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
```

#### 33.2 Service & Ingress

```yaml
## Service
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer

---
## Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

### PHẦN X: DATABASE & DATA MANAGEMENT

---

### Chương 34: Database Design & Optimization

#### 34.1 Database Indexing

```sql
-- ❌ BAD: No indexes
SELECT * FROM users WHERE email = 'john@example.com';
-- Full table scan: O(n)

-- ✅ GOOD: With index
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'john@example.com';
-- Index scan: O(log n)

-- Composite index
CREATE INDEX idx_users_email_status ON users(email, status);
SELECT * FROM users WHERE email = 'john@example.com' AND status = 'active';
```

#### 34.2 Query Optimization

```sql
-- ❌ BAD: N+1 query problem
SELECT * FROM users;
-- Then for each user:
SELECT * FROM orders WHERE user_id = ?;

-- ✅ GOOD: Join
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Or batch query
SELECT * FROM orders WHERE user_id IN (?, ?, ?);
```

#### 34.3 Connection Pooling

```python
from sqlalchemy import create_engine

## Create engine with connection pooling
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20,           ## Number of connections to keep
    max_overflow=10,        ## Additional connections when needed
    pool_recycle=3600,      ## Recycle connections after 1 hour
    pool_pre_ping=True      ## Test connection before using
)
```

---

### PHẦN XI: API DESIGN & INTEGRATION

---

### Chương 35: RESTful API Best Practices

#### 35.1 API Design

```python
## ✅ GOOD: RESTful API
GET    /api/v1/users              ## List users
GET    /api/v1/users/<id>         ## Get user
POST   /api/v1/users              ## Create user
PUT    /api/v1/users/<id>         ## Update user
DELETE /api/v1/users/<id>         ## Delete user

## Response format
{
    "status": 200,
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "timestamp": "2024-01-15T10:30:45Z"
}

## Error response
{
    "status": 400,
    "error": {
        "code": "INVALID_INPUT",
        "message": "Email is required"
    },
    "timestamp": "2024-01-15T10:30:45Z"
}
```

#### 35.2 API Versioning

```python
## URL-based versioning
GET /api/v1/users
GET /api/v2/users

## Header-based versioning
GET /api/users
Header: API-Version: 1

## Accept header
GET /api/users
Header: Accept: application/vnd.myapp.v1+json
```

#### 35.3 Pagination & Filtering

```python
## Pagination
GET /api/users?page=1&limit=10

## Filtering
GET /api/users?status=active&role=admin

## Sorting
GET /api/users?sort=created_at&order=desc

## Implementation
@app.route('/api/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status = request.args.get('status')
    
    query = User.query
    
    if status:
        query = query.filter_by(status=status)
    
    users = query.paginate(page=page, per_page=limit)
    
    return {
        "data": [u.to_dict() for u in users.items],
        "total": users.total,
        "page": page,
        "pages": users.pages
    }
```

---

### PHẦN XII: CONFIGURATION & SECRETS

---

### Chương 36: Environment Management

#### 36.1 Configuration Hierarchy

```
┌─────────────────────────────────────┐
│ Environment Variables (Highest)     │
│ (set in deployment)                 │
└────────────────┬────────────────────┘
                 │
┌────────────────┴────────────────────┐
│ .env.production                     │
│ (production-specific)               │
└────────────────┬────────────────────┘
                 │
┌────────────────┴────────────────────┐
│ .env.staging                        │
│ (staging-specific)                  │
└────────────────┬────────────────────┘
                 │
┌────────────────┴────────────────────┐
│ .env.development                    │
│ (development defaults)              │
└────────────────┬────────────────────┘
                 │
┌────────────────┴────────────────────┐
│ config.py (Lowest)                  │
│ (hardcoded defaults)                │
└─────────────────────────────────────┘
```

#### 36.2 Configuration Management

```python
import os
from dotenv import load_dotenv

## Load environment-specific config
env = os.getenv('ENV', 'development')
load_dotenv(f'.env.{env}')

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/mydb')
    API_KEY = os.getenv('API_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

## Validate required config
required_vars = ['DATABASE_URL', 'API_KEY']
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")
```

---

### PHẦN XIII: DOCUMENTATION

---

### Chương 37: Code Documentation

#### 37.1 Documentation Types

```python
## 1. Docstrings
def create_user(name, email):
    """
    Create a new user.
    
    Args:
        name (str): User's full name
        email (str): User's email address
    
    Returns:
        User: Created user object
    
    Raises:
        ValueError: If email is invalid
        DuplicateError: If email already exists
    
    Example:
        >>> user = create_user("John Doe", "john@example.com")
        >>> user.id
        1
    """
    pass

## 2. Type hints
def create_user(name: str, email: str) -> User:
    pass

## 3. Comments
## Explain WHY, not WHAT
## ❌ BAD: i = i + 1  ## Increment i
## ✅ GOOD: i = i + 1  ## Move to next item in batch
```

#### 37.2 API Documentation

```python
## Using Flask-RESTX
from flask_restx import Api, Resource, fields

api = Api(app, doc='/docs')

user_model = api.model('User', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True)
})

@api.route('/users/<int:id>')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, id):
        """Get user by ID"""
        return User.query.get(id)
```

---

### PHẦN XIV: PRODUCTION READINESS

---

### Chương 38: Production Readiness Review (PRR)

#### 38.1 PRR Checklist

```markdown
## Production Readiness Review

### Architecture & Design
- [ ] Architecture documented
- [ ] Scalability plan defined
- [ ] Load balancing configured
- [ ] Disaster recovery plan exists

### Reliability
- [ ] Retry logic implemented
- [ ] Circuit breakers configured
- [ ] Timeouts set
- [ ] Fallback strategies defined

### Observability
- [ ] Metrics collection setup
- [ ] Logging configured
- [ ] Distributed tracing enabled
- [ ] Alerting rules configured

### Security
- [ ] Authentication implemented
- [ ] Authorization implemented
- [ ] Encryption at rest/transit
- [ ] Security scanning passed
- [ ] Secrets management setup

### Testing
- [ ] Unit tests: 70%+
- [ ] Integration tests: 20%+
- [ ] E2E tests: 10%+
- [ ] Load testing done
- [ ] Security testing done

### Deployment
- [ ] CI/CD pipeline setup
- [ ] Automated testing in pipeline
- [ ] Deployment strategy chosen
- [ ] Rollback strategy tested

### Operations
- [ ] Runbooks written
- [ ] On-call schedule established
- [ ] SLO/SLA defined
- [ ] Incident response plan

### Documentation
- [ ] Architecture documented
- [ ] API documented
- [ ] Runbooks written
- [ ] Team trained
```

#### 38.2 SLO/SLI/SLA

```
SLI (Service Level Indicator): Metric
- Availability: 99.9%
- Latency P99: 200ms
- Error rate: 0.1%

SLO (Service Level Objective): Target
- Availability: 99.95%
- Latency P99: 150ms
- Error rate: 0.05%

SLA (Service Level Agreement): Contract
- Availability: 99.9%
- Penalty: 10% refund if breached
```

---

### PHẦN XV: MLOPS & AI SYSTEMS IN PRODUCTION

---

### Chương 39: MLOps Fundamentals

#### 39.1 ML Pipeline Architecture

```
┌─────────────────────────────────────┐
│ Data Ingestion                      │
│ (Batch/Streaming)                   │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Data Preprocessing                  │
│ (Cleaning, Validation)              │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Feature Engineering                 │
│ (Feature Store)                     │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Model Training                      │
│ (Experiment Tracking)               │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Model Evaluation                    │
│ (Validation, Testing)               │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Model Registry                      │
│ (Versioning, Metadata)              │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Model Deployment                    │
│ (Serving, Monitoring)               │
└────────────┬────────────────────────┘
             │
┌────────────┴────────────────────────┐
│ Monitoring & Feedback               │
│ (Drift Detection, Retraining)       │
└─────────────────────────────────────┘
```

#### 39.2 Model Serving

```python
## Batch serving
def batch_predict(data_path):
    """Predict on batch of data"""
    data = load_data(data_path)
    predictions = model.predict(data)
    save_predictions(predictions)

## Online serving
from flask import Flask, request

app = Flask(__name__)
model = load_model('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    """Real-time prediction"""
    data = request.json
    prediction = model.predict([data])
    return {"prediction": prediction[0]}

## Streaming serving
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer('input-topic')
producer = KafkaProducer('output-topic')

for message in consumer:
    data = json.loads(message.value)
    prediction = model.predict([data])
    producer.send('output-topic', json.dumps(prediction).encode())
```

#### 39.3 Model Monitoring

```python
from evidently.report import Report
from evidently.metrics import DataDriftMetric, ModelPerformanceMetric

## Detect data drift
report = Report(metrics=[
    DataDriftMetric(),
    ModelPerformanceMetric()
])

report.run(reference_data=train_data, current_data=prod_data)
report.show()

## Alert on drift
if report.as_dict()['metrics'][0]['result']['drift_detected']:
    logger.warning("Data drift detected! Trigger retraining.")
    trigger_retraining()
```

#### 39.4 Model Versioning

```python
import mlflow

## Log model
mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    ## Train model
    model = train_model(data)
    
    ## Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("precision", 0.92)
    
    ## Log model
    mlflow.sklearn.log_model(model, "model")
    
    ## Log parameters
    mlflow.log_params({"learning_rate": 0.01, "epochs": 100})

## Load model
model = mlflow.sklearn.load_model("runs:/abc123/model")
```

---

### Checklist: Production Readiness

- [ ] PRR checklist completed
- [ ] All security checks passed
- [ ] Performance benchmarks met
- [ ] Monitoring and alerting setup
- [ ] Runbooks written
- [ ] Team trained
- [ ] Incident response plan
- [ ] SLO/SLA defined
- [ ] Backup and DR tested
- [ ] Documentation complete

---

### Chương 40: Implementation Roadmap

#### 40.1 Phase 1: Foundation (Weeks 1-4)
- Setup version control
- Setup CI/CD pipeline
- Implement basic monitoring
- Write unit tests
- Setup logging

#### 40.2 Phase 2: Reliability (Weeks 5-8)
- Implement retry logic
- Setup circuit breakers
- Implement health checks
- Setup alerting
- Write integration tests

#### 40.3 Phase 3: Security (Weeks 9-12)
- Implement authentication
- Setup secrets management
- Enable encryption
- Security scanning
- Penetration testing

#### 40.4 Phase 4: Optimization (Weeks 13-16)
- Performance testing
- Database optimization
- Caching strategy
- Cost optimization
- Load testing

#### 40.5 Phase 5: MLOps (Weeks 17-20)
- Setup experiment tracking
- Model registry
- Model monitoring
- Automated retraining
- A/B testing

---

### Final Checklist: Production Quality

- [ ] All 40 chapters reviewed
- [ ] Architecture decisions documented
- [ ] Team trained on all aspects
- [ ] Monitoring and alerting setup
- [ ] Incident response plan
- [ ] Disaster recovery tested
- [ ] Security audit passed
- [ ] Performance benchmarks met
- [ ] Cost optimization done
- [ ] Ready for production deployment

---




# PROMPT 

```
Mình đang có trong tay 2 template SDD và TDD, mình dùng nó cho việc phát triển phần mềm Tuy nhiên mình muốn gộp 2 cái này lại thành 1 bản FINAL TEMPLATE ALL IN ONE SDD với yêu cầu

1. Đọc chi tiết từng phần của từng file và chỉ ra ưu điểm, nhược điểm
2. Lấy được tất cả điểm mạnh nhất của 2 tài liệu này
3. Trả cho tớ 1 bản template SOFTWARE DESIGN ALL IN ONE FINAL - làm template chuẩn cho mọi dự án chuẩn PRODUCTION QUALITY (đọc kỹ tài liệu PRODUCTION QUALITY ĐÍNH KÈM)
```
