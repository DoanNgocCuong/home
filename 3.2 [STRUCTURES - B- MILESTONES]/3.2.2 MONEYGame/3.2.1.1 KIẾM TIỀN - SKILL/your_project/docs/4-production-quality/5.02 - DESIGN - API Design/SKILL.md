# API Design Best Practices — Production Systems

> **Domain:** 5.02 | **Group:** DESIGN | **Lifecycle:** Design Time
> **Last Updated:** 2026-03-13
>
> *API là hợp đồng giữa client và server; phải rõ ràng, ổn định, và có thể thay đổi an toàn*

---

## 1. Overview

APIs are contracts. Once released, they're used by third-party developers, mobile apps, and internal services. Breaking changes cause outages and support tickets. API design is about clarity, consistency, and forward compatibility.

This domain covers modern API design across REST, GraphQL, and gRPC. Most production systems use REST or GraphQL; gRPC is for internal service-to-service communication. The principles—clear contracts, versioning, error handling, security—apply to all three.

Good API design makes services effortless to use. Bad API design causes integration headaches, security bugs, and developer frustration.

---

## 2. Core Principles

1. **Clarity Over Cleverness** — API should be obvious. Resources are nouns, actions are verbs. Patterns should be predictable.

2. **Backward Compatibility** — New versions should not break old clients. Plan for versioning from day one.

3. **Fail Predictably** — Errors should have consistent format. Clients can parse and handle them reliably.

4. **Assume the Network Fails** — Implement timeouts, retries, idempotency. Clients will make concurrent requests.

5. **Security by Default** — Require authentication, enforce rate limiting, validate input. Don't assume "it's internal."

---

## 3. Best Practices

### 3.1 RESTful API Design

**Practice:** Use REST for resource-oriented APIs; HTTP methods map to operations

- **What:** REST uses HTTP methods (GET, POST, PUT, DELETE) on resources (identified by URLs). Stateless communication.

- **Resources and Naming:**
  - Use plural nouns: `/users`, not `/user`
  - Resource hierarchy: `/users/123/orders/456` (user 123's order 456)
  - No verbs in URLs: Use HTTP method instead
  - Good: `POST /orders` (create order)
  - Bad: `GET /createOrder?id=123` (verb in URL, should be POST)

- **HTTP Methods:**
  - **GET**: Retrieve resource. Safe and idempotent. No request body.
  - **POST**: Create resource or trigger action. Not idempotent (multiple POSTs create multiple resources). Use request body.
  - **PUT**: Replace entire resource. Idempotent (PUT same data multiple times = same result).
  - **PATCH**: Partial update. Less common; can be non-idempotent.
  - **DELETE**: Remove resource. Idempotent.

- **Status Codes:**
  - **2xx Success**: 200 OK (resource returned), 201 Created (new resource), 204 No Content (success, no body)
  - **3xx Redirect**: 301 Moved Permanently, 302 Found
  - **4xx Client Error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity (validation failed)
  - **5xx Server Error**: 500 Internal Error, 503 Service Unavailable
  - **Rate Limit**: 429 Too Many Requests

- **Example:**
  ```
  GET /api/v1/users/123 → 200 OK with user object
  POST /api/v1/users → 201 Created, Location header points to /api/v1/users/456
  PATCH /api/v1/users/123 → 200 OK with updated user
  DELETE /api/v1/users/123 → 204 No Content
  GET /api/v1/users?limit=10&offset=20 → 200 OK with paginated list
  ```

- **Anti-pattern:** Using GET for actions (GET /deleteUser). Inconsistent status codes (sometimes 200, sometimes 201 for creation). No versioning in URL. Verbs in URLs.

### 3.2 Pagination Design

**Practice:** Provide cursor-based or offset-based pagination; always specify total count and has_more

- **Offset-Based Pagination:**
  - Simple: `?offset=20&limit=10` (skip 20, return 10)
  - Problem: If data changes between requests (items inserted), client might see duplicates
  - Use when: Data is stable, dataset small (< 100k records)
  - Implementation: `SELECT * FROM users OFFSET 20 LIMIT 10`

- **Cursor-Based Pagination:**
  - Efficient: `?cursor=eyJpZCI6IDEyM30=&limit=10`
  - Cursor is encoded position (e.g., base64 of `{"id": 123}`)
  - Resilient to insertions (cursor points to exact position)
  - Use when: Large dataset, or data changes frequently
  - Implementation: Encode last ID as cursor, query `WHERE id > cursor_id LIMIT 10`

- **Response Format:**
  ```json
  {
    "data": [...],
    "pagination": {
      "limit": 10,
      "offset": 20,
      "total": 5000,
      "has_more": true,
      "next_cursor": "eyJpZCI6IDEzM30="
    }
  }
  ```

- **Best Practice:** Use cursor-based for large datasets; offset-based for small or internal APIs.

### 3.3 GraphQL vs REST vs gRPC Decision Matrix

**Practice:** Choose based on use case

| Aspect | REST | GraphQL | gRPC |
|--------|------|---------|------|
| **Use Case** | CRUD, resource-oriented | Multiple clients with varying data needs | Internal service-to-service, high throughput |
| **Learning Curve** | Low (standard HTTP) | Medium (new query language) | Medium (protocol buffers) |
| **Caching** | Easy (HTTP caching) | Hard (POST requests, custom logic) | No HTTP caching; application caching |
| **Over-fetching** | Common (fixed schema) | No (request exact fields) | No (defined messages) |
| **Network Overhead** | JSON (text) | JSON (text) | Binary (smaller) |
| **Real-time** | Polling or WebSocket | Subscriptions | Streaming |
| **Browser Support** | Native | Via fetch/Apollo | Via gRPC-web or proxies |
| **Debugging** | Easy (curl, Postman) | Medium (GraphQL playground) | Hard (binary protocol) |

- **When to use REST:**
  - Simple CRUD operations
  - Public APIs (developers expect REST)
  - Mobile clients with good caching (reduce bandwidth)
  - Legacy systems (standardization)

- **When to use GraphQL:**
  - Multiple clients with different data needs (web, mobile, TV apps)
  - Want to reduce over-fetching
  - Need complex queries with nested relations
  - Building API aggregation layer

- **When to use gRPC:**
  - Internal service-to-service communication
  - Need high throughput, low latency
  - Services in same organization/network
  - Bidirectional streaming needed

- **Hybrid Approach:** REST for public API, gRPC for internal services. GraphQL gateway on top of REST APIs.

### 3.4 API Versioning Strategies

**Practice:** Plan versioning from day one; version in URL or header

- **URL Versioning (Recommended):**
  - `/api/v1/users`, `/api/v2/users`
  - Pros: Explicit, easy to route, easier to deprecate
  - Cons: URL duplication, must maintain multiple versions
  - Use this for public APIs

- **Header Versioning:**
  - `Accept: application/vnd.myapi.v2+json`
  - Pros: URL stays clean, can route internally
  - Cons: Less obvious, harder for browser access
  - Use this for internal APIs

- **No Versioning (Not Recommended):**
  - Rely on backward compatibility forever
  - Only works if you're very disciplined about breaking changes
  - Almost always fails at scale

- **Versioning Guidelines:**
  - Add fields freely (backward compatible)
  - Deprecate fields before removal (keep for at least 2 versions / 6 months)
  - Breaking changes require major version bump (v1 → v2)
  - Communicate deprecations clearly in docs and headers
  - Example: `Deprecation: true`, `Sunset: Wed, 21 Dec 2026 11:59:59 GMT` headers

- **Migration Path:**
  ```
  v1: Active (current)
  v2: Active (stable)
  v3: Beta (upcoming)
  v4: Deprecated (6 month notice before removal)
  ```

### 3.5 Rate Limiting Design

**Practice:** Implement rate limiting; communicate limits to clients via headers

- **Rate Limiting Strategies:**
  - **Per IP**: `/users/register` limit to 10 per hour per IP (prevent spam)
  - **Per User**: `/api/search` limit to 100 per hour per authenticated user (fair usage)
  - **Per API Key**: Third-party APIs limit by API key
  - **Global**: `/upload` total server limit (e.g., 1TB/day)

- **Communication to Client:**
  ```
  HTTP/1.1 200 OK
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 987
  X-RateLimit-Reset: 1372700873
  ```

- **When Rate Limited:**
  ```
  HTTP/1.1 429 Too Many Requests
  Retry-After: 60
  {
    "error": "rate_limit_exceeded",
    "limit": 1000,
    "window": "1 hour",
    "retry_after": 60
  }
  ```

- **Implementation:**
  - Simple: In-memory counter (single server only)
  - Distributed: Redis (key: user_id, increment, set TTL)
  - Example Redis: `INCR rate:user:123; EXPIRE rate:user:123 3600; GET rate:user:123`
  - Use sliding window or token bucket algorithm for accuracy

- **Anti-pattern:** No rate limiting (denial of service). Rate limiting without communicating to client. IP-based rate limiting (breaks behind proxies).

### 3.6 API Authentication

**Practice:** Use OAuth2 for third-party, API keys for internal, JWT for stateless

- **API Keys:**
  - Simple secret shared with client
  - Use for: Internal integrations, public APIs with low security requirements
  - Pass in header: `Authorization: Bearer <api_key>`
  - Or query param: `?api_key=...` (not recommended, logged in URLs)
  - Example: GitHub Personal Access Token, Stripe API key

- **OAuth2:**
  - Delegated authorization; user approves without sharing password
  - Use for: Third-party integrations accessing user data
  - Flows:
    - **Authorization Code**: User redirected to auth provider, receives code, exchanges for token. For web/mobile.
    - **Client Credentials**: Service-to-service. Client ID and secret exchanged for token.
    - **PKCE**: Authorization Code + proof key. For mobile apps (prevents code interception).
  - Example: "Sign in with Google", "Sign in with GitHub"

- **JWT (JSON Web Token):**
  - Self-contained token. Client includes in every request.
  - Format: `header.payload.signature`
  - Stateless (server doesn't store session; verifies signature)
  - Use for: Internal APIs, microservices, when you need stateless auth
  - Payload contains claims: `{"user_id": 123, "exp": 1234567890, "scope": "read"}`
  - Cons: Can't revoke immediately (until expiration); if key leaked, all tokens are valid until expiration

- **Implementation Best Practice:**
  ```
  GET /api/v1/me
  Authorization: Bearer <token>

  Server verifies:
  1. Token format (JWT) or lookup in database (API key)
  2. Token signature/validity
  3. Token not expired
  4. User has required permissions
  5. Request is for their own data (or user has admin scope)
  ```

- **Security Requirements:**
  - Always use HTTPS (never HTTP)
  - Never log tokens
  - Store tokens securely (client-side: secure, httpOnly, sameSite cookies)
  - Rotate keys regularly
  - Support token revocation (logout)

### 3.7 Error Response Format (RFC 7807)

**Practice:** Use consistent, machine-readable error format

- **Standard Format (RFC 7807):**
  ```json
  {
    "type": "https://api.example.com/errors/validation-failed",
    "title": "Validation Failed",
    "status": 422,
    "detail": "Email must be valid",
    "instance": "/users",
    "errors": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "Must be >= 18",
        "code": "out_of_range"
      }
    ]
  }
  ```

- **Fields:**
  - `type`: URI identifying error class (reusable, so clients can link to docs)
  - `title`: Human-readable error name
  - `status`: HTTP status code
  - `detail`: Specific error message
  - `instance`: URL where error occurred (helps debugging)
  - `errors`: Array of field-level errors (for validation)

- **Example Errors:**
  - 400 Bad Request: Malformed JSON, missing required field
  - 401 Unauthorized: Missing or invalid authentication
  - 403 Forbidden: Authenticated but no permission (you can read /orders, not /admin)
  - 404 Not Found: Resource doesn't exist
  - 409 Conflict: State conflict (e.g., trying to create duplicate email)
  - 422 Unprocessable Entity: Validation failed
  - 429 Too Many Requests: Rate limited

- **Anti-pattern:** HTML error pages in API. No `type` field (hard to categorize errors). Error detail in status code only (unclear what happened).

### 3.8 OpenAPI / Swagger Specification

**Practice:** Document API with OpenAPI 3.0; generate client libraries and server stubs

- **What:** OpenAPI (formerly Swagger) is a machine-readable spec for REST APIs. Describes endpoints, parameters, responses, schemas.

- **Benefits:**
  - Single source of truth for API documentation
  - Automatic API documentation generation (Swagger UI)
  - Client library generation (OpenAPI Generator)
  - Server stub generation (start coding against spec)
  - Contract testing (validate requests/responses)

- **Basic Structure:**
  ```yaml
  openapi: 3.0.0
  info:
    title: Orders API
    version: 1.0.0
  servers:
    - url: https://api.example.com/v1

  paths:
    /orders:
      get:
        summary: List orders
        parameters:
          - name: limit
            in: query
            schema:
              type: integer
              default: 10
        responses:
          '200':
            description: Success
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/OrderList'
      post:
        summary: Create order
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateOrderRequest'
        responses:
          '201':
            description: Created
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Order'

  components:
    schemas:
      Order:
        type: object
        properties:
          id:
            type: string
          total:
            type: number
          status:
            type: string
            enum: [pending, confirmed, shipped]
        required: [id, total, status]
  ```

- **Tools:**
  - **Swagger UI**: Web UI for exploring API
  - **Redoc**: Beautiful API documentation
  - **OpenAPI Generator**: Generate client libraries in 50+ languages
  - **Postman**: API testing, sync with OpenAPI

### 3.9 HATEOAS (Hypermedia As The Engine Of Application State)

**Practice:** Include links in responses so clients can discover actions

- **What:** Response includes links to related resources and actions

- **Example:**
  ```json
  {
    "id": 123,
    "name": "John",
    "email": "john@example.com",
    "_links": {
      "self": { "href": "/users/123" },
      "orders": { "href": "/users/123/orders" },
      "update": { "href": "/users/123", "method": "PATCH" },
      "delete": { "href": "/users/123", "method": "DELETE" }
    }
  }
  ```

- **Benefits:**
  - Client can discover available actions
  - Server can change URLs without breaking clients (follow links, don't hardcode URLs)
  - Natural pagination (response includes `next` and `previous` links)

- **Drawbacks:**
  - Adds verbosity to responses
  - Extra work to implement
  - Not all REST purists agree it's necessary

- **Recommendation:** Use for public APIs serving browser/UI clients. Skip for internal APIs or mobile clients (they don't need discovery).

### 3.10 WebSocket vs SSE vs HTTP Streaming

**Practice:** Choose based on requirements

- **Server-Sent Events (SSE):**
  - One-way: Server pushes to client
  - HTTP based (simpler than WebSocket)
  - Automatic reconnection
  - Use for: Real-time notifications, live updates (stock prices, sports scores)
  - Example: `GET /events; Accept: text/event-stream`
  ```
  data: {"price": 100}

  data: {"price": 102}
  ```

- **WebSocket:**
  - Bidirectional: Server and client both push
  - Persistent connection, low latency
  - Use for: Chat, collaborative editing, multiplayer games, live dashboards
  - Example: `ws://example.com/chat`

- **HTTP Streaming / Long Polling:**
  - HTTP Streaming: Keep connection open, send data as it arrives
  - Long Polling: Client polls repeatedly, server holds request until data available
  - Less efficient than WebSocket/SSE but works in restricted networks
  - Use when: WebSocket not available, firewall blocks WebSocket

- **Recommendation:**
  - Real-time notifications: SSE
  - Bidirectional communication: WebSocket
  - Restricted network: HTTP Streaming or Long Polling

### 3.11 Backend-for-Frontend (BFF) Pattern

**Practice:** Create API tailored to client needs; separate from backend service API

- **What:** Different API layer for each client (web, mobile, TV, partners)

- **Why:**
  - Mobile clients need compact responses (bandwidth)
  - Web clients need rich data (reduce requests)
  - Different authentication (OAuth for web, token for mobile)
  - Different pagination (mobile: 20 items; web: 50 items)
  - Server-side session for web, stateless for mobile

- **Architecture:**
  ```
  Mobile → Mobile BFF → Services → DB
  Web → Web BFF → Services → DB
  ```

- **Example:**
  - Mobile API: `/orders?limit=5` returns compact order list
  - Web API: `/orders?include=user,items,shipping` returns everything
  - Both backends call same service, but tailor responses

- **Tools:** API Gateway, Kong, Traefik can implement BFF pattern

### 3.12 API Deprecation Strategy

**Practice:** Plan deprecation timeline; communicate clearly; provide migration path

- **Deprecation Timeline:**
  - Month 0: Announce deprecation (docs, email, headers)
  - Month 0-3: Old version still works, new version available
  - Month 3-6: Old version works, nudge clients to migrate
  - Month 6: Remove old version
  - Longer timeline for major changes (12 months common)

- **Communication:**
  - Email to API key owners
  - Blog post with migration guide
  - Deprecation header: `Deprecation: true`, `Sunset: date`
  - Return 400 status with deprecation message to unmigrated clients

- **Example Timeline:**
  ```
  Jan 2026: Announce v1 deprecated, v2 available
  April 2026: v1 still works, nudge messages
  July 2026: v1 removed
  ```

### 3.13 Contract Testing

**Practice:** Use contract tests to verify API consumer and provider agree on contract

- **What:** Tests verify that:
  - Provider returns what consumer expects (schema, status code)
  - Consumer makes request provider understands

- **Tools:** Pact, Spring Cloud Contract

- **Example Test:**
  ```
  Consumer test:
  - Request: GET /users/123
  - Expect: 200, { id: 123, name: string }

  Provider test:
  - Given: User 123 exists
  - Request: GET /users/123
  - Returns: 200, { id: 123, name: "John", email: "john@example.com" }
  - Pact verifies: Response has id and name fields with correct types
  ```

### 3.14 Idempotency Keys

**Practice:** Support idempotent requests via unique keys; retry-safe

- **What:** Client provides unique ID; server deduplicates requests

- **Implementation:**
  ```
  POST /orders
  Idempotency-Key: abc-123-def
  {
    "items": [...],
    "total": 100
  }

  Server:
  1. Check if Idempotency-Key exists in cache/DB
  2. If yes, return previous response
  3. If no, process, store response with key
  4. Return 201 Created
  ```

- **Best Practice:** Idempotency keys required for all POST/PATCH that modify state

- **Example (Stripe):**
  ```
  curl https://api.stripe.com/v1/charges \
    -H "Idempotency-Key: abc123" \
    -d amount=2000 \
    -d currency=usd

  If you retry with same key, get same response (not charged twice)
  ```

### 3.15 Request Validation

**Practice:** Validate early; return clear errors

- **Validation Layers:**
  - **Schema**: Type checking (string, number, object)
  - **Business Logic**: Email domain allowed, age >= 18, inventory >= quantity
  - **Security**: No SQL injection, no XXE, input length limits

- **Response:**
  ```
  POST /users
  { "email": "invalid-email" }

  422 Unprocessable Entity
  {
    "errors": [
      { "field": "email", "message": "Invalid email", "code": "format" }
    ]
  }
  ```

- **Implementation:**
  - Use schema validation library (jsonschema, joi, etc.)
  - Validate at API boundary, not deep in business logic
  - Return all validation errors at once (batch feedback)

### 3.16 Response Caching Headers

**Practice:** Use HTTP caching to reduce server load and client latency

- **Cache Control Headers:**
  ```
  GET /users/123

  HTTP/1.1 200 OK
  Cache-Control: public, max-age=300
  ETag: "abc123"
  Last-Modified: Wed, 21 Dec 2022 11:59:59 GMT
  ```

- **Directives:**
  - `public`: Cache can store (user, proxy)
  - `private`: Only user's browser, not proxy
  - `max-age=300`: Cache for 300 seconds
  - `no-cache`: Can cache, but must revalidate with server
  - `no-store`: Don't cache (sensitive data)
  - `must-revalidate`: After expiry, must check with server

- **Revalidation:**
  - Client sends: `If-None-Match: "abc123"`
  - Server responds: 304 Not Modified (use cached copy)
  - Saves bandwidth

- **When to Cache:**
  - GET requests only
  - User data (private, short expiry)
  - Public data like posts (public, longer expiry)
  - Not authentication endpoints

---

## 4. Decision Frameworks

### REST Endpoint Design Decision Tree

```
Is it resource-oriented?
├─ Yes → Use REST
│  ├─ Retrieve? → GET
│  ├─ Create? → POST
│  ├─ Update? → PUT/PATCH
│  └─ Delete? → DELETE
└─ No (complex operations)
   └─ Consider using POST with action in body or switch to GraphQL
```

### Versioning Decision

```
Public API?
├─ Yes → URL versioning (/v1, /v2)
│  └─ Keep 2 versions, 6-month deprecation window
└─ No (Internal API)
   └─ Header versioning or no versioning
```

### API Selection for New Projects

```
Need to support multiple clients with different data needs?
├─ Yes → GraphQL
└─ No → REST

Then decide on auth: Internal? → API Key. Public? → OAuth2. Microservices? → JWT.

Real-time bidirectional communication?
├─ Yes → WebSocket
└─ No → SSE or polling
```

---

## 5. Checklist

- [ ] API documented in OpenAPI/Swagger
- [ ] Resource naming consistent (plural nouns, no verbs)
- [ ] HTTP method usage correct (GET safe, POST idempotent, etc.)
- [ ] Status codes follow conventions (201 for create, 204 for delete, etc.)
- [ ] Error responses use RFC 7807 format
- [ ] Pagination implemented (offset or cursor)
- [ ] Rate limiting implemented and communicated via headers
- [ ] Authentication implemented (API keys, OAuth2, or JWT)
- [ ] Idempotency keys for POST/PATCH
- [ ] Request validation with clear error messages
- [ ] Versioning strategy defined and documented
- [ ] Deprecation path planned
- [ ] Contract tests written (API matches OpenAPI spec)
- [ ] Response caching headers set appropriately
- [ ] HTTPS enforced (no HTTP)
- [ ] CORS policy defined if serving web clients
- [ ] API Gateway in front (routing, rate limiting, auth)
- [ ] Monitoring/alerting on API errors and latency

---

## 6. Common Mistakes & Anti-Patterns

### RPC-Style API (Not RESTful)
```
Bad: GET /getUser?id=123, GET /getUserOrders?id=123, GET /deleteUser?id=123
Good: GET /users/123, GET /users/123/orders, DELETE /users/123
```
**Fix:** Use resource-based URLs and HTTP methods.

### Inconsistent Status Codes
Using 200 for everything, or 500 for validation errors. Clients can't handle errors properly.

**Fix:** Standardize on HTTP status codes. 4xx for client error, 5xx for server error.

### No Versioning, Breaking Changes
Releasing v2 that removes fields, breaks existing clients. Causes outages.

**Fix:** Plan versioning from day one. Keep old version for 6 months. Communicate deprecations.

### Unbounded Pagination
No limit on results. Client requests all 1 million records. Server crashes.

**Fix:** Enforce limit (e.g., max 100 items per page). Default to 20 items.

### No Rate Limiting
Malicious actor hammers API with requests. Legitimate users suffer.

**Fix:** Implement rate limiting. Return 429. Communicate limits via headers.

### Sensitive Data in URLs
`?api_key=abc123` logged in proxy/browser history. Credentials exposed.

**Fix:** Always use Authorization header. Never pass secrets in URL.

### No Idempotency
Client retries due to network glitch. Charge duplicated, order duplicated.

**Fix:** Support idempotency keys for POST/PATCH. Deduplicate on retry.

### Over-Fetching Data (REST)
Client requests user object; gets 50 unnecessary fields. Wasted bandwidth.

**Fix:** GraphQL if multiple clients. REST: Use field projection (`?fields=id,name,email`) or create BFF.

### GraphQL Without Complexity Limits
Client sends complex query. Joins 10 tables, returns 1 million records. Server crashes.

**Fix:** Limit query depth, query complexity, results per page. Timeout queries.

### No Error Details
Response: `500 Internal Server Error`. No idea what happened.

**Fix:** Include `type`, `title`, `detail`, `instance` in error response. Use RFC 7807.

---

## 7. Tools & References

### API Documentation & Design
- **OpenAPI/Swagger**: Industry standard for REST API specs
- **Postman**: API design, testing, documentation
- **Insomnia**: API client and design tool
- **Redoc**: Beautiful API documentation from OpenAPI
- **Swagger UI**: Interactive API documentation

### Testing
- **Pact**: Contract testing (verify consumer-provider agreement)
- **Dredd**: API testing against OpenAPI spec
- **SoapUI**: API testing tool
- **REST Assured**: Java API testing library
- **Supertest**: Node.js HTTP testing

### Rate Limiting & Caching
- **Redis**: Implement rate limiting and caching
- **Nginx**: Web server with rate limiting, caching
- **HAProxy**: Load balancer with rate limiting
- **Varnish**: HTTP caching proxy

### API Gateways
- **Kong**: Open-source API gateway
- **Traefik**: Cloud-native API gateway
- **AWS API Gateway**: AWS managed service
- **Azure API Management**: Azure managed service
- **Tyk**: Open-source API gateway

### Authoritative References
- **Google API Design Guide**: Industry best practices
- **Microsoft REST API Guidelines**: Comprehensive REST guide
- **Stripe API Design**: Gold standard public API (study their design choices)
- **AWS API Gateway Developer Guide**: Real-world AWS patterns
- **RFC 7231 HTTP Semantics**: Official HTTP spec
- **RFC 7807 Problem Details**: Standard error format
- **OAuth 2.0 Authorization Framework**: Official OAuth spec

### Real-World Examples to Study
- Stripe API (payment processing)
- GitHub API (platform API)
- Twitter API (real-time, massive scale)
- Slack API (WebSocket + REST)
- Twilio API (telecommunications)

---

**Last Updated:** 2026-03-13 | **Version:** 1.0
