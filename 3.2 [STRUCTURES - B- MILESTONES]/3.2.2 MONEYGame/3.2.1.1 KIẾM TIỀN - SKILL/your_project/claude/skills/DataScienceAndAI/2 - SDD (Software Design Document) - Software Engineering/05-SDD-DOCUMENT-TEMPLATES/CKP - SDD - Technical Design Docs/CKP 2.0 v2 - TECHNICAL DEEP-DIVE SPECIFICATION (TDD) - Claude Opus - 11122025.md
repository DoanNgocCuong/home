# TECHNICAL DEEP-DIVE SPECIFICATION (TDD)

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