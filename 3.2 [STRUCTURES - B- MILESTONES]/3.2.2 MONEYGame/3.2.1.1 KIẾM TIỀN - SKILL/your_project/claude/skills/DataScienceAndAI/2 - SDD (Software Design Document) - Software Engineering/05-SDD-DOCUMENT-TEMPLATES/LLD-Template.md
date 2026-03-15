# Low-Level Design (LLD) Template

**Project Name:** [Tên dự án]
**Service Name:** [Tên service]
**Version:** 1.0
**Date:** [Ngày viết]
**Author(s):** [Tên tác giả]

---

## 1. Overview

### 1.1 Purpose

Mục đích của service ini dalam context HLD.

**Ví dụ:**
> User Service cung cấp semua functionality liên dengan user management. Service ini responsible untuk CRUD operations pada user data, user validation, user search, dan avatar handling. Service beroperasi dalam User Management microservice ecosystem.

### 1.2 Scope

Yang di-include dan exclude dari LLD ini.

**In Scope:**
- User model dan database schema
- All API endpoints untuk user operations
- Internal service architecture (controllers, services, models)
- Database queries dan indexing strategy
- Error handling dan validation
- Security considerations

**Out of Scope:**
- OAuth integration (Auth Service responsibility)
- Payment processing
- Frontend implementation
- DevOps infrastructure details (documented in HLD)

---

## 2. Class/Module Design

### 2.1 Class Diagrams

Detailed class structure dengan semua properties dan methods.

```
┌─────────────────────────────────────┐
│         User                        │
├─────────────────────────────────────┤
│ Properties:                         │
│ - id: UUID                          │
│ - email: String                     │
│ - firstName: String                 │
│ - lastName: String                  │
│ - passwordHash: String              │
│ - isActive: Boolean                 │
│ - createdAt: DateTime               │
│ - updatedAt: DateTime               │
├─────────────────────────────────────┤
│ Methods:                            │
│ + create(data): User                │
│ + read(id): User                    │
│ + update(id, data): User            │
│ + delete(id): Boolean               │
│ + findByEmail(email): User          │
│ + validateEmail(email): Boolean     │
│ + validatePassword(pwd): Boolean    │
│ + hashPassword(pwd): String         │
│ + comparePassword(pwd, hash): Bool  │
│ + search(query): User[]             │
│ + getAllActive(): User[]            │
└─────────────────────────────────────┘
         │
         │ has_many
         │
┌────────▼──────────────────────────┐
│         Role                      │
├───────────────────────────────────┤
│ Properties:                       │
│ - id: UUID                        │
│ - name: String (unique)           │
│ - description: String             │
│ - createdAt: DateTime             │
├───────────────────────────────────┤
│ Methods:                          │
│ + create(name, desc): Role        │
│ + read(id): Role                  │
│ + update(id, data): Role          │
│ + delete(id): Boolean             │
│ + getPermissions(): Permission[]  │
│ + addPermission(permId): Boolean  │
│ + removePermission(permId): Bool  │
│ + getAllRoles(): Role[]           │
└───────────────────────────────────┘
```

### 2.2 Relationships

Relationships antar classes.

```
User (1) ─── (M) Role
  │                │
  ├─ OneToMany     └─ OneToMany
  │
  └─ @OneToMany
     @JoinTable(name = "user_roles")
     roles: Role[]

Role (1) ─── (M) Permission
  │                │
  ├─ OneToMany     └─ OneToMany
  │
  └─ @OneToMany
     @JoinTable(name = "role_permissions")
     permissions: Permission[]

User ──────▶ Permission
   (implicit via roles)
```

---

## 3. Database Design

### 3.1 Table Schemas

DDL untuk semua tables.

```sql
-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
  CONSTRAINT name_not_empty CHECK (length(trim(first_name)) > 0 AND length(trim(last_name)) > 0)
);

-- Add indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Roles Table
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT name_not_empty CHECK (length(trim(name)) > 0)
);

CREATE INDEX idx_roles_name ON roles(name);

-- Permissions Table
CREATE TABLE permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL UNIQUE,
  resource VARCHAR(100) NOT NULL,
  action VARCHAR(50) NOT NULL,
  description TEXT,

  CONSTRAINT permission_unique UNIQUE(resource, action),
  CONSTRAINT name_not_empty CHECK (length(trim(name)) > 0)
);

CREATE INDEX idx_permissions_resource_action ON permissions(resource, action);

-- User-Role Junction Table
CREATE TABLE user_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,

  CONSTRAINT user_role_unique UNIQUE(user_id, role_id)
);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);

-- Role-Permission Junction Table
CREATE TABLE role_permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,

  CONSTRAINT role_permission_unique UNIQUE(role_id, permission_id)
);

CREATE INDEX idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission_id ON role_permissions(permission_id);

-- Audit Log Table
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  action VARCHAR(50) NOT NULL,
  resource VARCHAR(100) NOT NULL,
  resource_id VARCHAR(100),
  old_values JSONB,
  new_values JSONB,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
```

### 3.2 Query Specifications

Key queries dengan execution plans.

**Query 1: Find user by email (most frequent)**

```sql
SELECT id, email, first_name, last_name, is_active, created_at, updated_at
FROM users
WHERE email = $1 AND is_active = true;

Execution Plan:
└─ Bitmap Index Scan on idx_users_email
   └─ Filter: is_active = true
   └─ Estimated rows: 1
   └─ Cost: 0.29
```

**Query 2: Get user with roles and permissions**

```sql
SELECT
  u.id, u.email, u.first_name, u.last_name,
  json_agg(
    json_build_object(
      'role_id', r.id,
      'role_name', r.name,
      'permissions', (
        SELECT json_agg(json_build_object('id', p.id, 'name', p.name))
        FROM permissions p
        JOIN role_permissions rp ON rp.permission_id = p.id
        WHERE rp.role_id = r.id
      )
    )
  ) AS roles
FROM users u
LEFT JOIN user_roles ur ON ur.user_id = u.id
LEFT JOIN roles r ON r.id = ur.role_id
WHERE u.id = $1
GROUP BY u.id;

Execution Plan:
└─ Aggregate
   └─ Hash Join (users - user_roles)
      └─ Hash Join (roles - permissions via subquery)
      └─ Estimated cost: 1.50
```

**Query 3: Search users (with pagination)**

```sql
SELECT id, email, first_name, last_name, is_active
FROM users
WHERE (lower(email) LIKE $1 OR lower(first_name) LIKE $1 OR lower(last_name) LIKE $1)
  AND is_active = true
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;

Execution Plan:
└─ Limit/Offset
   └─ Sort (created_at DESC)
      └─ Seq Scan with WHERE filter
      └─ Estimated rows: 10 (with limit)
```

### 3.3 Data Validation Rules

Validation rules untuk setiap field.

| Field | Type | Constraints | Validation | Error Message |
|-------|------|-----------|-----------|---------------|
| email | STRING | NOT NULL, UNIQUE, MAX 255 | Must match email regex | Invalid email format |
| first_name | STRING | NOT NULL, MIN 1, MAX 100 | No leading/trailing spaces | First name required (1-100 chars) |
| last_name | STRING | NOT NULL, MIN 1, MAX 100 | No leading/trailing spaces | Last name required (1-100 chars) |
| password | STRING | NOT NULL, MIN 8, MAX 255 | Must contain uppercase, lowercase, number, special char | Password too weak |
| is_active | BOOLEAN | DEFAULT true | - | Must be boolean |

---

## 4. API Specifications

### 4.1 Endpoint Details

Semua endpoints dengan request/response specifications.

#### Endpoint 1: Create User

```
POST /v1/users
Content-Type: application/json
Authorization: Bearer {JWT_TOKEN} (optional for public signup)

REQUEST:
────────
{
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "password": "SecurePass123!",
  "roles": ["uuid-user-role"]  // optional, default: ['user']
}

RESPONSE (201 Created):
──────────────────────
{
  "id": "uuid-1234",
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isActive": true,
  "roles": [
    {
      "id": "uuid-user-role",
      "name": "user",
      "description": "Regular user"
    }
  ],
  "createdAt": "2026-03-15T10:30:00Z",
  "updatedAt": "2026-03-15T10:30:00Z"
}

ERROR RESPONSES:
───────────────
400 Bad Request:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "errors": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "password", "message": "Password too weak"}
    ]
  }
}

409 Conflict:
{
  "error": {
    "code": "DUPLICATE_EMAIL",
    "message": "Email john.doe@example.com already exists"
  }
}

Side Effects:
─────────────
- Hash password using bcrypt (rounds: 10)
- Create audit log entry
- Send welcome email (async)
- Cache user in Redis (TTL: 1 hour)
```

#### Endpoint 2: Get User by ID

```
GET /v1/users/{id}
Authorization: Bearer {JWT_TOKEN}

RESPONSE (200 OK):
──────────────────
{
  "id": "uuid-1234",
  "email": "john.doe@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isActive": true,
  "roles": [...],
  "createdAt": "2026-03-15T10:30:00Z",
  "updatedAt": "2026-03-15T10:30:00Z"
}

ERROR RESPONSES:
───────────────
404 Not Found:
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id uuid-1234 not found"
  }
}

Caching:
───────
- Check Redis cache first (key: user:uuid-1234)
- If hit: return cached data
- If miss: query DB, cache result (TTL: 1 hour)
```

#### Endpoint 3: Update User

```
PUT /v1/users/{id}
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

REQUEST:
────────
{
  "firstName": "Jonathan",
  "lastName": "Doe",
  // email & password tidak bisa di-update via endpoint ini
}

RESPONSE (200 OK):
──────────────────
{
  "id": "uuid-1234",
  "email": "john.doe@example.com",
  "firstName": "Jonathan",
  "lastName": "Doe",
  ...
}

Side Effects:
─────────────
- Create audit log entry
- Invalidate user cache
- Publish user.updated event
```

#### Endpoint 4: Delete User

```
DELETE /v1/users/{id}
Authorization: Bearer {JWT_TOKEN}

RESPONSE (204 No Content):
──────────────────────────

Side Effects:
─────────────
- Soft delete: set is_active = false (keep data for audit)
- Create audit log entry
- Invalidate user cache
- Publish user.deleted event
```

#### Endpoint 5: Search Users

```
GET /v1/users/search?q={query}&page={page}&limit={limit}
Authorization: Bearer {JWT_TOKEN}

QUERY PARAMS:
─────────────
- q (required): search query (min 1 char, max 100)
- page (optional, default: 0): page number
- limit (optional, default: 20, max: 100): results per page

RESPONSE (200 OK):
──────────────────
{
  "total": 42,
  "page": 0,
  "limit": 20,
  "totalPages": 3,
  "results": [
    {
      "id": "uuid-1",
      "email": "john.doe@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "isActive": true
    },
    // ... 19 more results
  ]
}

Error Validation:
─────────────────
- q must be 1-100 characters
- page must be >= 0
- limit must be 1-100
```

### 4.2 Error Codes

Comprehensive error code mapping.

```
HTTP 400 Bad Request:
├─ VALIDATION_ERROR: Input validation failed
├─ INVALID_EMAIL_FORMAT: Email format invalid
├─ PASSWORD_TOO_WEAK: Password doesn't meet requirements
└─ INVALID_REQUEST: Generic bad request

HTTP 401 Unauthorized:
├─ MISSING_TOKEN: Authorization header missing
├─ INVALID_TOKEN: JWT token invalid/expired
├─ TOKEN_EXPIRED: JWT token expired
└─ INSUFFICIENT_PERMISSIONS: Token doesn't have required permissions

HTTP 403 Forbidden:
├─ ACCESS_DENIED: User doesn't have permission
└─ RESOURCE_FORBIDDEN: Resource access denied

HTTP 404 Not Found:
├─ USER_NOT_FOUND: User doesn't exist
├─ ROLE_NOT_FOUND: Role doesn't exist
└─ RESOURCE_NOT_FOUND: Resource not found

HTTP 409 Conflict:
├─ DUPLICATE_EMAIL: Email already exists
├─ DUPLICATE_ROLE: Role already exists
└─ DUPLICATE_PERMISSION: Permission already exists

HTTP 422 Unprocessable Entity:
├─ INVALID_ROLE: Referenced role doesn't exist
└─ INVALID_PERMISSION: Referenced permission doesn't exist

HTTP 429 Too Many Requests:
└─ RATE_LIMIT_EXCEEDED: Too many requests

HTTP 500 Internal Server Error:
├─ DATABASE_ERROR: Database operation failed
├─ CACHE_ERROR: Cache operation failed
└─ UNKNOWN_ERROR: Unexpected error
```

---

## 5. Function/Method Specifications

### 5.1 Core Methods

Detailed specifications untuk setiap method penting.

#### Method: User.create()

```
Function: UserService.createUser(userData)
──────────────────────────────────────────

Input Parameters:
  - userData: Object
    ├─ email: String (required)
    ├─ firstName: String (required)
    ├─ lastName: String (required)
    ├─ password: String (required)
    └─ roles: UUID[] (optional, default: ['user-role-id'])

Validation:
  1. Email validation
     ├─ Check format matches regex
     ├─ Check if already exists in DB
     └─ Throw: DUPLICATE_EMAIL if exists

  2. Password validation
     ├─ Check length >= 8
     ├─ Check has uppercase letter
     ├─ Check has lowercase letter
     ├─ Check has number
     ├─ Check has special character
     └─ Throw: PASSWORD_TOO_WEAK if fails

  3. Name validation
     ├─ Check firstName length 1-100
     ├─ Check lastName length 1-100
     ├─ Check no leading/trailing spaces
     └─ Throw: VALIDATION_ERROR if fails

  4. Role validation
     ├─ Check all role IDs exist
     └─ Throw: INVALID_ROLE if not found

Processing:
  1. Hash password using bcrypt
     password_hash = bcrypt.hash(password, saltRounds=10)

  2. Create user in database
     INSERT INTO users (email, first_name, last_name, password_hash, is_active)
     VALUES (email, firstName, lastName, password_hash, true)

  3. Assign roles
     INSERT INTO user_roles (user_id, role_id)
     VALUES (user.id, role_id) for each role

  4. Create audit log
     INSERT INTO audit_logs (user_id, action, resource, new_values)
     VALUES (user.id, 'CREATE', 'user', {user data})

  5. Send email (async)
     queue.enqueue(sendWelcomeEmail, {email, firstName})

  6. Cache user
     redis.set(user:${user.id}, userJSON, EX=3600)

Output:
  - Returns: User object
  {
    id: UUID,
    email: String,
    firstName: String,
    lastName: String,
    isActive: Boolean,
    roles: Role[],
    createdAt: DateTime,
    updatedAt: DateTime
  }

Exceptions:
  - ValidationError: 400 Bad Request
  - DuplicateEmailError: 409 Conflict
  - PasswordTooWeakError: 400 Bad Request
  - RoleNotFoundError: 422 Unprocessable Entity
  - DatabaseError: 500 Internal Server Error

Performance:
  - Expected execution time: < 200ms
  - Database queries: 4 (insert user, insert roles, create audit, send email async)
  - Cache writes: 1
```

#### Method: User.authenticate()

```
Function: UserService.authenticateUser(email, password)
────────────────────────────────────────────────────────

Input:
  - email: String
  - password: String (plaintext)

Validation:
  1. Email format check
  2. Password format check (not empty)

Processing:
  1. Query database for user by email
     SELECT id, password_hash, is_active
     FROM users
     WHERE email = $1

  2. Check if user exists
     IF user == null THEN
       THROW: UserNotFoundError

  3. Check if user is active
     IF user.is_active == false THEN
       THROW: UserInactiveError

  4. Verify password using bcrypt
     isValid = bcrypt.compare(password, user.password_hash)
     IF isValid == false THEN
       THROW: InvalidPasswordError

  5. Return authenticated user
     RETURN user (without password_hash)

Output:
  - Returns: Authenticated User object

Exceptions:
  - UserNotFoundError: 404 Not Found
  - UserInactiveError: 403 Forbidden
  - InvalidPasswordError: 401 Unauthorized

Performance:
  - Expected time: 100-200ms (bcrypt is slow intentionally)
  - Database queries: 1
```

### 5.2 Helper Methods

Utility functions.

```
Function: validateEmail(email)
───────────────────────────────
- Check format: /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/
- Check length: max 255 chars
- Return: true/false

Function: validatePassword(password)
──────────────────────────────────────
- Check length >= 8
- Check has uppercase (/[A-Z]/)
- Check has lowercase (/[a-z]/)
- Check has digit (/\d/)
- Check has special char (/[!@#$%^&*]/)
- Return: true/false with details

Function: hashPassword(plainPassword)
──────────────────────────────────────
- Use bcrypt with 10 salt rounds
- Return: hashed password string

Function: comparePassword(plainPassword, hash)
────────────────────────────────────────────────
- Use bcrypt.compare()
- Return: true/false
```

---

## 6. Error Handling

### 6.1 Exception Hierarchy

Semua custom exceptions.

```
Error (base)
├─ ValidationError
│  ├─ InvalidEmailFormatError
│  ├─ PasswordTooWeakError
│  └─ InvalidInputError
├─ AuthenticationError
│  ├─ UserNotFoundError
│  ├─ InvalidPasswordError
│  ├─ UserInactiveError
│  └─ TokenExpiredError
├─ AuthorizationError
│  └─ InsufficientPermissionsError
├─ ConflictError
│  ├─ DuplicateEmailError
│  └─ DuplicateRoleError
├─ NotFoundError
│  ├─ UserNotFoundError
│  ├─ RoleNotFoundError
│  └─ ResourceNotFoundError
├─ ServerError
│  ├─ DatabaseError
│  ├─ CacheError
│  └─ ExternalServiceError
└─ RateLimitError
```

### 6.2 Error Handling Strategy

Bagaimana handle errors di berbagai layers.

```
Controller Layer:
├─ Try-catch blocks around service calls
├─ Convert exceptions to HTTP responses
├─ Log error dengan context (user, request ID)
└─ Return appropriate HTTP status code

Service Layer:
├─ Validate inputs
├─ Perform business logic
├─ Throw custom exceptions on errors
├─ Log errors
└─ Do NOT catch exceptions (let controller handle)

Data Access Layer:
├─ Execute database queries
├─ Handle database connection errors
├─ Throw DatabaseError for query failures
└─ Log SQL errors (without exposing sensitive data)

Example Flow:
────────────
try {
  const user = await userService.createUser(userData);
  return res.status(201).json(user);
} catch (error) {
  if (error instanceof ValidationError) {
    logger.warn('Validation failed', {error, userId});
    return res.status(400).json({error: error.message});
  } else if (error instanceof DuplicateEmailError) {
    logger.info('Duplicate email attempt', {email});
    return res.status(409).json({error: 'Email already exists'});
  } else {
    logger.error('Unexpected error', {error: error.stack});
    return res.status(500).json({error: 'Internal server error'});
  }
}
```

---

## 7. Security Details

### 7.1 Authentication & Authorization

Security measures di level code.

```
Authentication (User.authenticate):
├─ Use bcrypt untuk password hashing (NOT md5 or sha1)
├─ Salt rounds: 10 (intentionally slow)
├─ Compare using constant-time function (bcrypt.compare)
├─ Never return password hash di API response
└─ Enforce HTTPS for credential transmission

Authorization (Permission checking):
├─ Implement permission middleware
├─ Check role_id di user_roles table
├─ Check permission_id di role_permissions table
├─ Cache permissions in Redis (reduce DB hits)
├─ Implement permission policies per endpoint:
│
│  Example: @RequirePermission('user:read')
│  ├─ Check if user has 'user:read' permission
│  ├─ If not → return 403 Forbidden
│  └─ If yes → proceed
│
└─ Log all authorization failures
```

### 7.2 Input Validation

Defense against injection attacks.

```
SQL Injection Prevention:
├─ Use parameterized queries (ALWAYS!)
├─ Example WRONG: `SELECT * FROM users WHERE email = '${email}'`
├─ Example CORRECT: `SELECT * FROM users WHERE email = $1` with [email]
└─ ORM (like Sequelize) handles escaping

XSS Prevention:
├─ Validate email format (only emails, not HTML)
├─ HTML encode output dalam API responses (though JSON is safer)
├─ Use DOMPurify di frontend (not backend responsibility)
└─ Set CSP headers in API Gateway

CSRF Prevention:
├─ Use stateless JWT (no sessions/cookies)
├─ Validate Content-Type header
├─ Check Origin/Referer header in API Gateway
└─ Use SameSite cookies if needed

NoSQL Injection (if using MongoDB):
├─ Validate input types
├─ Use schema validation
└─ Never concatenate user input dalam queries
```

---

## 8. Performance Considerations

### 8.1 Optimization Strategies

Cara optimize performance.

```
Database Optimization:
├─ Indexes:
│  ├─ idx_users_email (frequently searched)
│  ├─ idx_users_is_active (filter untuk active users)
│  ├─ idx_user_roles_user_id (lookup user's roles)
│  └─ idx_user_roles_role_id (lookup users in role)
│
├─ Query Optimization:
│  ├─ Use EXPLAIN ANALYZE untuk analyze queries
│  ├─ Batch inserts when possible
│  ├─ Use pagination untuk large result sets
│  └─ Denormalize jika perlu (e.g., cache role count)
│
└─ Connection Pooling:
   └─ PgBouncer untuk reuse DB connections

Caching Strategy:
├─ Cache user data setelah lookup (TTL: 1 hour)
├─ Cache role & permission data (TTL: 1 hour)
├─ Invalidate cache pada update:
│  └─ When user updated → delete cache key
│  └─ When role updated → delete role cache keys
└─ Use cache warming untuk frequently accessed data

Algorithm Optimization:
├─ Bcrypt password hashing is SLOW intentionally
│  └─ Protects against brute force attacks
│
├─ For user search:
│  └─ Use full-text search index di PostgreSQL
│  └─ Implement pagination (don't return 1M results)
│
└─ Batch operations:
   └─ Bulk insert users dalam single transaction
```

### 8.2 Load Testing

Capacity planning.

```
Expected Loads:
├─ Peak: 10,000 requests/second
├─ Average: 1,000 requests/second
└─ Response time targets:
   ├─ p50: < 100ms
   ├─ p95: < 200ms
   └─ p99: < 500ms

Load Test Results:
├─ Single instance: 500 req/sec max
├─ Database max: 5,000 req/sec (connection limited)
├─ With caching: 10,000+ req/sec possible
└─ Bottleneck: Database connections (pool size 20)
```

---

## 9. Testing Strategy

### 9.1 Test Cases

Unit test dan integration test examples.

```
Unit Tests (Controller Layer):
├─ test_createUser_validInput_returns201
├─ test_createUser_duplicateEmail_returns409
├─ test_createUser_invalidPassword_returns400
├─ test_getUser_validId_returns200
├─ test_getUser_invalidId_returns404
├─ test_updateUser_validData_returns200
├─ test_deleteUser_validId_returns204
└─ test_searchUsers_validQuery_returns200

Integration Tests (Service Layer):
├─ test_createUser_savesToDatabase
├─ test_createUser_sendsEmail
├─ test_authenticateUser_validCredentials_succeeds
├─ test_authenticateUser_invalidPassword_throws
├─ test_createUser_cachesInRedis
└─ test_deleteUser_invalidatesCache

Database Tests:
├─ test_uniqueEmailConstraint_enforced
├─ test_foreignKeyConstraint_enforced
├─ test_emailIndexPerformance_lessthan10ms
└─ test_userSearchQuery_usesIndex

Security Tests:
├─ test_passwordHashing_usesBcrypt
├─ test_sqlInjection_blocked
├─ test_unauthorized_accessDenied
└─ test_rateLimiting_enforced
```

---

## 10. Code Structure

### 10.1 Directory Layout

Bagaimana code diorganisir.

```
user-service/
├── src/
│   ├── controllers/
│   │   ├── userController.js
│   │   ├── roleController.js
│   │   └── permissionController.js
│   │
│   ├── services/
│   │   ├── userService.js
│   │   ├── roleService.js
│   │   ├── permissionService.js
│   │   └── validationService.js
│   │
│   ├── models/
│   │   ├── User.js
│   │   ├── Role.js
│   │   └── Permission.js
│   │
│   ├── repositories/
│   │   ├── userRepository.js
│   │   ├── roleRepository.js
│   │   └── permissionRepository.js
│   │
│   ├── middleware/
│   │   ├── authMiddleware.js
│   │   ├── errorHandler.js
│   │   ├── requestLogger.js
│   │   └── rateLimiter.js
│   │
│   ├── utils/
│   │   ├── passwordUtils.js
│   │   ├── tokenUtils.js
│   │   ├── validators.js
│   │   └── logger.js
│   │
│   ├── config/
│   │   ├── database.js
│   │   ├── redis.js
│   │   ├── env.js
│   │   └── constants.js
│   │
│   ├── routes/
│   │   ├── userRoutes.js
│   │   ├── roleRoutes.js
│   │   └── permissionRoutes.js
│   │
│   └── app.js (main Express app)
│
├── tests/
│   ├── unit/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── utils/
│   │   └── models/
│   │
│   ├── integration/
│   │   ├── userService.test.js
│   │   ├── roleService.test.js
│   │   └── database.test.js
│   │
│   └── e2e/
│       ├── userAPI.test.js
│       └── roleAPI.test.js
│
├── docker/
│   └── Dockerfile
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── docs/
│   ├── API-Documentation.md
│   └── Setup-Guide.md
│
├── .env.example
├── package.json
├── jest.config.js
└── README.md
```

### 10.2 Key Files Description

Apa yang ada di file-file penting.

| File | Purpose |
|------|---------|
| userController.js | HTTP request handlers, input parsing, response formatting |
| userService.js | Business logic, validation, database operations |
| userRepository.js | Database queries, data access layer |
| User.js | Model definition, data type validation |
| authMiddleware.js | JWT validation, permission checking |
| errorHandler.js | Error handling middleware |
| validators.js | Input validation functions |
| passwordUtils.js | Password hashing, comparison functions |

---

## 11. Appendix

### 11.1 Glossary

| Term | Definition |
|------|-----------|
| **Bcrypt** | Password hashing algorithm, intentionally slow |
| **JWT** | JSON Web Token untuk stateless authentication |
| **ORM** | Object-Relational Mapping library |
| **RBAC** | Role-Based Access Control |
| **SQL Injection** | Attack by inserting malicious SQL |
| **XSS** | Cross-Site Scripting attack |
| **TTL** | Time To Live, cache expiration time |
| **Repository Pattern** | Data access abstraction layer |

### 11.2 Related Documents

- HLD-Template.md - High-level architecture
- SDD-Full-Template.md - Complete SDD
- ADR-Template.md - Architecture Decision Records
- API-Documentation.md - Detailed API reference

### 11.3 Code Examples

Example implementation struktur:

```javascript
// user.service.js
class UserService {
  constructor(userRepository, roleRepository, cache, mailer) {
    this.repo = userRepository;
    this.roleRepo = roleRepository;
    this.cache = cache;
    this.mailer = mailer;
  }

  async createUser(userData) {
    // 1. Validate
    this.validateUserInput(userData);

    // 2. Check duplicate
    const existing = await this.repo.findByEmail(userData.email);
    if (existing) throw new DuplicateEmailError();

    // 3. Hash password
    const hashedPassword = await this.hashPassword(userData.password);

    // 4. Create user
    const user = await this.repo.create({
      ...userData,
      passwordHash: hashedPassword
    });

    // 5. Assign roles
    await this.assignRoles(user.id, userData.roles);

    // 6. Cache
    await this.cache.set(`user:${user.id}`, user, 3600);

    // 7. Send email (async)
    this.mailer.sendWelcomeEmail(user.email, user.firstName);

    return user;
  }
}
```

---

**Document Prepared By:** [Name]
**Last Updated:** [Date]
**Status:** [Draft / In Review / Approved]

---
