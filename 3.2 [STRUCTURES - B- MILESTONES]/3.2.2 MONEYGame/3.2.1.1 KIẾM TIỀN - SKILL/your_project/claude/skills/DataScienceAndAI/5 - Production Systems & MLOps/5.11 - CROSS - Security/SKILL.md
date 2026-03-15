# Security & Threat Management — Production Best Practices

> **Domain:** 5.11 | **Group:** CROSS | **Lifecycle:** Cross-Cutting
> **Last Updated:** 2026-03-13

## 1. Overview

Security in production systems is non-negotiable. This domain covers defensive strategies across the entire attack surface: authentication, authorization, data protection, infrastructure hardening, and incident response. Security is not a feature—it's a foundational requirement that scales with application complexity.

**Vietnamese:** Bảo mật là nền tảng không thể thỏa hiệp trong hệ thống production. Phải bảo vệ từ lớp authentication cho đến container security.

## 2. Core Principles

- **Defense in Depth:** Multiple layers of security, not single points of failure
- **Principle of Least Privilege:** Grant minimum necessary access/permissions
- **Fail Securely:** Errors must not expose sensitive data or system details
- **Never Trust User Input:** All external data requires validation
- **Encrypt Sensitive Data:** Both at rest and in transit
- **Log Security Events:** Maintain audit trails for forensics and compliance

## 3. Best Practices

### 3.1 Authentication & Authorization

**Practice: OAuth2 & OIDC Implementation**
- **What:** Industry standard authorization flows (OAuth2) and identity protocol (OIDC)
- **Why:** Delegates auth to specialized providers, enables SSO, reduces password exposure
- **How:**
  ```javascript
  // OAuth2 Authorization Code Flow
  GET /oauth/authorize?client_id=xxx&redirect_uri=https://app.com/callback&scope=openid+profile
  // Server responds with authorization code
  // Frontend exchanges code for token via backend (never expose code to frontend directly)
  POST /oauth/token {code, client_id, client_secret}
  // Response: {access_token, id_token, refresh_token}
  ```
- **Anti-pattern:** Storing passwords in application database, implementing custom auth from scratch

**Practice: JWT Best Practices**
- **What:** JSON Web Tokens for stateless authentication
- **Why:** Scalable, can be verified without server roundtrip, works well in microservices
- **How:**
  ```javascript
  // Payload should contain: {sub, iat, exp, scopes}
  const token = jwt.sign({sub: user.id, exp: Math.floor(Date.now()/1000) + 3600}, SECRET, {algorithm: 'HS256'});

  // Always verify signature and expiration
  const decoded = jwt.verify(token, SECRET, {algorithms: ['HS256']});
  ```
- **Anti-pattern:** Storing sensitive data in JWT (passwords, API keys), using HS256 for public APIs (use RS256), not validating expiration

**Practice: RBAC vs ABAC vs PBAC**
- **What:** Role-Based vs Attribute-Based vs Policy-Based Access Control
- **Why:** Different granularity levels for different needs
- **How:**
  ```yaml
  # RBAC: User has role "admin", admin can delete users
  - role: admin
    permissions: [read, write, delete]

  # ABAC: Check multiple attributes
  - user.department == "finance" AND resource.classification == "internal" → read

  # PBAC: Policies define access (AWS IAM style)
  - Effect: Allow
    Action: s3:GetObject
    Resource: arn:aws:s3:::bucket/user/${aws:username}/*
  ```
- **Anti-pattern:** Hardcoding access checks in business logic, mixing auth concerns with application code

### 3.2 API Security

**Practice: Input Validation & Sanitization**
- **What:** Reject or clean malformed/dangerous user input
- **Why:** Prevents SQL injection, XSS, path traversal, buffer overflow attacks
- **How:**
  ```javascript
  // Whitelist approach (preferred)
  const email = validator.isEmail(input) ? input : null;
  const userId = Number.isInteger(parseInt(input)) ? parseInt(input) : null;

  // Parameterized queries prevent SQL injection
  db.query('SELECT * FROM users WHERE id = ?', [userId]); // ✓ Safe
  db.query(`SELECT * FROM users WHERE id = ${userId}`);   // ✗ SQL injection risk
  ```
- **Anti-pattern:** Black-listing bad characters (incomplete), trusting user input without validation, string concatenation in SQL

**Practice: Rate Limiting & DDoS Mitigation**
- **What:** Limit request frequency per user/IP to prevent abuse
- **Why:** Protects against brute force, credential stuffing, DoS attacks
- **How:**
  ```javascript
  // Using express-rate-limit
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,                  // limit each IP to 100 requests per windowMs
    keyGenerator: (req) => req.user.id || req.ip, // limit by user ID if logged in
    skip: (req) => req.user.isAdmin // admins exempt
  });
  app.post('/api/login', limiter, loginHandler);
  ```
  - Progressive delays: exponential backoff after N failed attempts
  - Use Redis for distributed rate limiting across service replicas
- **Anti-pattern:** Trusting client IP (behind proxy), same limit for all endpoints, no backoff strategy

**Practice: CORS & CSRF Protection**
- **What:** Control Cross-Origin requests and prevent cross-site forgery
- **Why:** Prevents unauthorized requests from attacker-controlled domains
- **How:**
  ```javascript
  // CORS: Only allow specific origins
  app.use(cors({
    origin: ['https://trusted-app.com', 'https://app.example.com'],
    credentials: true, // allow cookies
    methods: ['GET', 'POST']
  }));

  // CSRF: Use SameSite cookies + CSRF tokens
  // Cookie: Set-Cookie: sessionid=abc; SameSite=Strict; HttpOnly; Secure
  // Form: <input type="hidden" name="_csrf" value="token">
  ```
- **Anti-pattern:** Using wildcard CORS (`*`), no CSRF tokens on state-changing requests, missing HttpOnly/Secure flags

### 3.3 Secret Management

**Practice: Never Commit Secrets to Git**
- **What:** Keep API keys, passwords, certificates out of version control
- **Why:** Git history is permanent; secrets in repo = permanently compromised (Velociraptor Principle)
- **How:**
  ```bash
  # .gitignore
  .env
  .env.*.local
  secrets/
  *.pem
  *.key

  # Use pre-commit hooks to detect secrets
  pip install detect-secrets
  detect-secrets scan --list-all-plugins
  ```
  - Immediate rotation required if secret ever committed
  - Use `git-secret` or `blackbox` if secrets must be in repo (encrypted)
- **Anti-pattern:** Committing `.env` files, "dummy" credentials in code, thinking private repos are safe

**Practice: HashiCorp Vault & Secret Rotation**
- **What:** Centralized secret storage with automatic rotation
- **Why:** Audit trail, encryption, key rotation without app restart, revocation
- **How:**
  ```bash
  # Store secret
  vault kv put secret/myapp/db password=secretpass

  # Retrieve in app
  CLIENT_TOKEN=$(vault login -method=kubernetes -path=auth/kubernetes).auth.client_token
  DB_PASSWORD=$(vault kv get -field=password secret/myapp/db)

  # Automatic rotation (e.g., database password every 30 days)
  vault write -f database/rotate-root/mydb
  ```
  - AWS Secrets Manager, Azure Key Vault are managed alternatives
  - Principle: Secrets never in application code, retrieved at runtime
- **Anti-pattern:** Hardcoded secrets, passwords with no rotation, storing Vault token in plaintext

### 3.4 Data Protection & PII

**Practice: Encryption at Rest & in Transit**
- **What:** Encrypt data stored on disk and data in flight over network
- **Why:** Protects against data breach, network interception, physical theft
- **How:**
  ```javascript
  // At rest: database encryption
  // AWS: Enable RDS encryption, S3 SSE, EBS encryption by default
  // Kubernetes: encrypt-etcd in kubelet config

  // In transit: TLS 1.2+, mTLS for service-to-service
  // Express with HTTPS
  const https = require('https');
  const fs = require('fs');
  https.createServer({
    key: fs.readFileSync('private-key.pem'),
    cert: fs.readFileSync('certificate.pem')
  }, app).listen(443);
  ```
  - Cipher suites: prefer AEAD (ChaCha20-Poly1305, AES-GCM)
  - TLS versions: enforce 1.2 minimum, prefer 1.3
- **Anti-pattern:** Unencrypted databases, HTTP for sensitive data, weak cipher suites, self-signed certs in production

**Practice: PII Handling & Data Minimization**
- **What:** Collect, store, and transmit only necessary personal information
- **Why:** Reduces breach impact, GDPR/CCPA compliance, reduces liability
- **How:**
  ```javascript
  // Anonymization: remove identifiers
  user.email = null; // after sending confirmation
  user.ssn = null;   // store only last 4 digits if needed

  // Pseudonymization: hash before storing
  const anonymizedId = crypto.createHash('sha256').update(realId + salt).digest('hex');

  // Retention: delete when no longer needed
  const thirtyDaysAgo = new Date(Date.now() - 30*24*60*60*1000);
  db.query('DELETE FROM user_logs WHERE created_at < ?', [thirtyDaysAgo]);
  ```
  - Separate PII from transaction data when possible
  - Regular data audits to identify unnecessary PII
- **Anti-pattern:** Storing SSN in plaintext, keeping data longer than needed, logging PII in application logs

## 4. Decision Frameworks

**When to use OAuth2 vs SAML vs OIDC:**
- OAuth2: API delegation, mobile apps, modern web applications
- SAML: Enterprise SSO, legacy systems, XML-based
- OIDC: OAuth2 + identity layer, preferred for modern applications

**Secret storage: where to store what**
| Secret | Storage | Rotation |
|--------|---------|----------|
| Database password | Vault/AWS Secrets | Every 90 days |
| API keys | Vault + env var | Every 6 months |
| JWT signing key | Vault + rotated | Asymmetric; rotate yearly |
| TLS certificates | Vault + Secret | Auto-renew (Let's Encrypt) |

## 5. Checklist

- [ ] All authentication flows use OAuth2/OIDC or verified custom implementation
- [ ] JWTs use asymmetric algorithms (RS256+) for public APIs
- [ ] All APIs validate input on both client and server side
- [ ] Rate limiting implemented on authentication endpoints (login, password reset)
- [ ] CORS configured with explicit origin whitelist, not wildcard
- [ ] CSRF tokens on all state-changing requests (POST/PUT/DELETE)
- [ ] Passwords never stored in plaintext, use bcrypt/scrypt with salt
- [ ] All secrets stored in Vault/managed service, not in code/env files
- [ ] HTTPS enforced, TLS 1.2+, strong cipher suites
- [ ] Database encryption enabled (at rest)
- [ ] PII fields identified and access restricted
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Dependencies scanned for vulnerabilities (Snyk/Dependabot)
- [ ] Container images scanned before deployment
- [ ] Non-root user in Dockerfile, read-only filesystem where possible
- [ ] Audit logging configured for security events (auth failures, permission denials)
- [ ] Incident response plan documented

## 6. Common Mistakes & Anti-Patterns

1. **JWT in localStorage** (vulnerable to XSS) → use httpOnly cookies instead
2. **Hardcoded credentials in Docker images** → use Vault or build args
3. **Same encryption key for all customers** → use customer-specific keys
4. **Logging sensitive data** → sanitize logs before storage
5. **Outdated dependencies with known CVEs** → automated scanning + regular updates
6. **Overly broad IAM permissions** → audit and apply principle of least privilege
7. **Testing with production secrets** → use separate test credentials always
8. **No rollback plan for secret rotation** → test rotation in staging first

## 7. Tools & References

**Authentication & Auth:**
- Auth0, Okta, Cognito (managed auth)
- Keycloak, FusionAuth (self-hosted)

**Secret Management:**
- HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Sealed Secrets (Kubernetes)

**Vulnerability Scanning:**
- Snyk (dependencies), Dependabot (GitHub), Trivy (containers), SonarQube (SAST)

**Testing:**
- OWASP ZAP (dynamic testing), Burp Suite (pen testing)

**Standards:**
- OWASP Top 10 2024, CWE Top 25, NIST Cybersecurity Framework

---

**Vietnamese Note:** Bảo mật không phải điều you add thêm. Phải là phần của design từ đầu. (Security is not something you add later; it must be part of design from the beginning.)
