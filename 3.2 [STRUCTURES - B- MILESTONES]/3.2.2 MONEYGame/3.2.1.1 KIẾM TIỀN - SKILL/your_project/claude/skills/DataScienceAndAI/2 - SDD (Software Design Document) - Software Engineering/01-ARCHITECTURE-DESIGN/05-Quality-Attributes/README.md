# 05-Quality-Attributes - Các Đặc tính Chất lượng Hệ thống

## Giới thiệu

Quality Attributes (hay còn gọi "Non-Functional Requirements" hoặc "-ilities") là những yêu cầu về cách hệ thống hoạt động, không phải cái nó làm.

**Ví dụ:**
- Functional requirement: "Hệ thống phải cho phép users tạo account"
- Quality attribute: "User registration phải xong trong <2 giây"

Bài này chi tiết 6 quality attributes chính:
1. Scalability (Khả năng mở rộng)
2. Reliability (Độ tin cậy)
3. Availability (Tính khả dụng)
4. Maintainability (Khả năng bảo trì)
5. Performance (Hiệu suất)
6. Security (Bảo mật)

---

## 1. Scalability (Khả năng mở rộng)

### Định nghĩa

Scalability là khả năng hệ thống xử lý tăng trưởng trong:
- Số lượng users
- Lượng data
- Số requests
- Complexity

mà **không bị hạ chất lượng dịch vụ**.

### Ví dụ Scalability

```
Today:        1,000 users, response time: 200ms
Tomorrow:    10,000 users, response time: 200ms (Scalable!)
Next week:  100,000 users, response time: 200ms (Still scalable!)
```

vs

```
Today:       1,000 users, response time: 200ms
Tomorrow:   10,000 users, response time: 2,000ms (Not scalable!)
Next week: 100,000 users, system crashes (Not scalable!)
```

### Loại Scalability

#### 1.1 Horizontal Scaling (Scale Out)
**Thêm nhiều máy chủ**

```
┌─────────────┐      ┌─────────────┐    ┌─────────────┐
│   Server 1  │      │   Server 1  │    │   Server 1  │
│ 1000 users  │ ---> │   500 users │--->│   250 users │
└─────────────┘      │   Server 2  │    │   Server 2  │
                     │   500 users │    │   250 users │
                     └─────────────┘    │   Server 3  │
                                        │   250 users │
                                        │   Server 4  │
                                        │   250 users │
                                        └─────────────┘
```

**Ưu điểm:**
- Có thể scale đến vô hạn (lý thuyết)
- Tính chịu lỗi cao (một server down, others still running)
- Có thể xoay vòng servers (rolling updates)

**Nhược điểm:**
- Phức tạp (load balancing, session management)
- Network overhead (servers giao tiếp)
- Data consistency khó (data ở nhiều nơi)

**Khi nào dùng:**
- Web applications
- Microservices
- Stateless services

#### 1.2 Vertical Scaling (Scale Up)
**Nâng cấp máy chủ (more CPU, RAM, disk)**

```
┌──────────────────┐      ┌────────────────────────┐
│  Server 1        │      │  Server 1 (Upgraded)   │
│  1 Core, 4GB RAM │ ---> │  8 Cores, 64GB RAM     │
│  1000 users      │      │  8000 users            │
└──────────────────┘      └────────────────────────┘
```

**Ưu điểm:**
- Đơn giản (không cần load balancer)
- Dữ liệu tập trung (consistency dễ)
- Ít network overhead

**Nhược điểm:**
- Có giới hạn (máy chủ lớn nhất bao nhiêu?)
- Single point of failure (server down = all down)
- Downtime khi upgrade

**Khi nào dùng:**
- Databases
- Caches
- Ban đầu (khi scale không quá lớn)

### Cách đo Scalability

```
Scalability Metric = (Response Time at Peak Load) / (Response Time at Normal Load)
```

**Ví dụ:**
- Normal load: 1000 users, response time 200ms
- Peak load: 10,000 users, response time 500ms
- Scalability = 500/200 = 2.5x (không lý tưởng, nên <1.2x)

### Factors ảnh hưởng đến Scalability

| Factor | Impact | Solution |
|--------|--------|----------|
| **Database** | Single DB bottleneck | Caching, sharding, read replicas |
| **Session state** | Can't distribute | Use external store (Redis) |
| **File I/O** | Slow disk | Use CDN, object storage |
| **CPU-bound** | Can't parallelize | Optimize algorithm, horizontal scale |
| **Memory** | Limited per server | Compress data, pagination |

### Real-world Example: YouTube Scalability

```
2005: 1 server, thousands of users per day
      ↓
2006: Multiple servers, millions of views per day
      ↓
2012: Thousands of servers, billions of views per day
      ↓
2024: Global distribution, trillions of views per year
```

Architecture evolution:
- Monolith → Microservices
- Single datacenter → Global distributed
- MySQL → Bigtable, Spanner
- Simple caching → Multi-layer caching

---

## 2. Reliability (Độ tin cậy)

### Định nghĩa

Reliability là khả năng hệ thống hoạt động đúng, không gặp lỗi.

**Nói đơn giản:** System làm đúng việc nó được thiết kế làm.

### Ví dụ Reliability

```
Banking Transfer:
- Input: Transfer 1000 USD from A → B
- Expected: A loses 1000, B gains 1000
- Unreliable: A loses 1000, B gains 900 (lỗi!)
- Reliable: A loses 1000, B gains 1000 (đúng!)
```

### Cách đo Reliability

**MTBF (Mean Time Between Failures)**
- Thời gian trung bình giữa 2 lần fail
- Ví dụ: MTBF = 30 days (hệ thống fail trung bình 30 ngày 1 lần)

**MTTR (Mean Time To Repair)**
- Thời gian trung bình để fix khi bị lỗi
- Ví dụ: MTTR = 1 hour (mất 1 giờ để fix)

**Reliability = MTBF / (MTBF + MTTR)**
```
Example:
MTBF = 30 days
MTTR = 1 hour
Reliability = 30 days / (30 days + 1 hour)
           = 720 hours / 721 hours
           = 99.86%
```

### Cách improve Reliability

#### 1. Input Validation
```javascript
// Unreliable
function transfer(from, to, amount) {
  from.balance -= amount;
  to.balance += amount;
}

// Reliable
function transfer(from, to, amount) {
  if (!from || !to) throw new Error("Invalid accounts");
  if (amount <= 0) throw new Error("Amount must be positive");
  if (from.balance < amount) throw new Error("Insufficient funds");

  from.balance -= amount;
  to.balance += amount;
}
```

#### 2. Error Handling
```javascript
// Unreliable - silently fails
async function saveUserData(user) {
  const result = await db.save(user);
  console.log(result); // What if save fails?
}

// Reliable - handles errors
async function saveUserData(user) {
  try {
    const result = await db.save(user);
    if (!result) throw new Error("Save failed");
    return result;
  } catch (error) {
    logger.error('Failed to save user:', error);
    throw error; // Or handle gracefully
  }
}
```

#### 3. Defensive Programming
```javascript
// Unreliable - assumes data is correct
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Reliable - validates data
function calculateTotal(items) {
  if (!Array.isArray(items)) {
    throw new Error("Items must be an array");
  }

  return items.reduce((sum, item) => {
    if (typeof item.price !== 'number' || item.price < 0) {
      throw new Error("Invalid price");
    }
    return sum + item.price;
  }, 0);
}
```

#### 4. Testing
- Unit tests: Test individual functions
- Integration tests: Test components together
- E2E tests: Test full workflows

#### 5. Logging & Monitoring
- Log all important operations
- Monitor for anomalies
- Alert when things go wrong

### Real-world Example: Google Cloud Reliability

Google publishes monthly uptime:
- Typical: 99.95%+ uptime
- Failures tracked and analyzed
- Post-mortems published
- Continuous improvements made

---

## 3. Availability (Tính khả dụng)

### Định nghĩa

Availability là % thời gian hệ thống sẵn sàng phục vụ requests.

**Khác với Reliability:**
- **Reliability:** Làm đúng khi hoạt động
- **Availability:** Hoạt động (có thể không đúng!)

**Ví dụ:**
- Reliable but unavailable: System crashed (can't use, but if it worked, it would be right)
- Available but unreliable: System respond nhưng sai dữ liệu

### Cách đo Availability

**SLA (Service Level Agreement)**
```
Availability = (Total Time - Downtime) / Total Time × 100%
```

**Các tiers:**

| Nines | % Uptime | Downtime/month | Downtime/year | Tier |
|-------|----------|----------------|---------------|------|
| 1 nine | 90% | 72 hours | 36.5 days | Unacceptable |
| 2 nines | 99% | 7.2 hours | 3.65 days | Bad |
| 3 nines | 99.9% | 43 minutes | 8.76 hours | OK |
| 4 nines | 99.99% | 4.3 minutes | 52 minutes | Good |
| 5 nines | 99.999% | 26 seconds | 5 minutes | Excellent |
| 6 nines | 99.9999% | 2.6 seconds | 31 seconds | Extreme |

**Ví dụ:**
- Netflix: Target 99.99% uptime (4 nines)
- Gmail: Target 99.99% uptime
- Bank system: Target 99.999%+ uptime

### Cách improve Availability

#### 1. Redundancy (Dự phòng)
```
┌─────────────────────────────────────┐
│        Load Balancer                │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
    Server 1    Server 2
   (Active)     (Standby)

If Server 1 down → Switch to Server 2
```

#### 2. Failover
```
Current: Server 1 (Active)
         Server 2 (Standby)

Server 1 crashes → Automatic failover to Server 2
Users don't notice outage!
```

#### 3. Replication
```
┌─────────────────────┐
│  Primary Database   │
│  (Read + Write)     │
└──────────┬──────────┘
           │ Replicate
    ┌──────┴──────┐
    │             │
Replica 1    Replica 2
(Read only)  (Read only)

If Primary down → Promote Replica 1 as Primary
```

#### 4. Circuit Breaker Pattern
```javascript
// Without circuit breaker (cascading failures)
try {
  const result = await externalService.call();
} catch (e) {
  // Retry immediately, might overload external service
}

// With circuit breaker
const breaker = new CircuitBreaker(externalService.call, {
  failureThreshold: 5,
  resetTimeout: 60000 // Reset after 1 minute
});

try {
  const result = await breaker.execute();
} catch (e) {
  // If service down, fail fast instead of retrying
  // Give service time to recover
}
```

### Real-world Example: Amazon/AWS Availability

```
2021: AWS DynamoDB outage (affected Netflix, Airbnb)
      - Some regions unavailable for 4+ hours
      - Caused by cascading failures in one data center
      - AWS improved after-incident

2022: AWS US-East outage
      - 6-hour outage
      - Widespread impact across internet
      - Emphasized need for multi-region strategy
```

**Lesson:** Even world-class systems have availability issues
→ Need redundancy, failover, multi-region architecture

---

## 4. Maintainability (Khả năng bảo trì)

### Định nghĩa

Maintainability là dễ bao nhiêu để:
- Fix bugs
- Thêm tính năng mới
- Refactor code
- Hiểu cách hệ thống hoạt động

### Cách đo Maintainability

**Cyclomatic Complexity (CC)**
```javascript
// CC = 1 (Simple, maintainable)
function add(a, b) {
  return a + b;
}

// CC = 2 (Still simple)
function max(a, b) {
  if (a > b) return a;
  return b;
}

// CC = 5+ (Getting complex, harder to maintain)
function validate(user) {
  if (!user) return false;
  if (!user.email) return false;
  if (!user.name) return false;
  if (user.age < 18) return false;
  if (!user.phone) return false;
  return true;
}
```

**Goal:** Keep CC < 10 per function

**Code Coverage**
- Unit test coverage goal: 70-80%
- Critical path: 90%+

**Technical Debt**
- Amount of "quick hacks" that need refactoring later
- Should track and pay down regularly

### Cách improve Maintainability

#### 1. Clear Code
```javascript
// Bad - unclear what this does
function x(a) {
  return a.filter(b => b.a > 100).map(b => b.b);
}

// Good - clear what it does
function getExpensiveProductNames(products) {
  return products
    .filter(product => product.price > 100)
    .map(product => product.name);
}
```

#### 2. SOLID Principles

**S - Single Responsibility**
```javascript
// Bad - UserService does too much
class UserService {
  createUser() { }
  sendEmail() { }
  logAnalytics() { }
  updateDatabase() { }
}

// Good - Each class has one reason to change
class UserService {
  createUser() { }
}
class EmailService {
  sendEmail() { }
}
class AnalyticsService {
  logAnalytics() { }
}
```

**O - Open/Closed Principle**
```javascript
// Bad - Need to modify when adding new types
function calculateDiscount(user) {
  if (user.type === 'gold') return 0.2;
  if (user.type === 'silver') return 0.1;
  // Need to modify this every time we add new type
}

// Good - Extensible without modifying
class DiscountStrategy {
  getDiscount() { }
}
class GoldUserDiscount extends DiscountStrategy {
  getDiscount() { return 0.2; }
}
class SilverUserDiscount extends DiscountStrategy {
  getDiscount() { return 0.1; }
}
```

#### 3. Documentation
- Code comments (WHY not WHAT)
- Architecture Decision Records (ADR)
- README files
- API documentation

#### 4. Testing
- Unit tests = documentation + safety net
- Integration tests = verify contracts
- E2E tests = verify user flows

#### 5. Automation
- Linting (catch style issues)
- Type checking (catch bugs early)
- CI/CD (automated testing, deployment)

### Real-world Example: Legacy Code Maintenance

**Before:**
```
Monolithic codebase: 500,000 lines
Single file: 50,000 lines
No tests: 0% coverage
No documentation
One person understands entire system

→ Adding feature takes months
→ Bugs take weeks to fix
```

**After (Refactored):**
```
Microservices: 20,000 lines per service
Each file: 200-500 lines
Tests: 80% coverage
ADR documentation
Multiple people know each service

→ Adding feature takes days
→ Bugs fixed quickly
```

---

## 5. Performance (Hiệu suất)

### Định nghĩa

Performance là tốc độ hệ thống xử lý requests.

**Metrics:**
- **Latency:** Time từ request gửi đi đến response nhận về
- **Throughput:** Số requests xử lý per unit time
- **Response time:** Thời gian xử lý một request

### Cách đo Performance

#### 1. Latency (Độ trễ)
```
Request → Server → Response
  │                   │
  └───────────────────┘
       Latency
```

**Ví dụ:**
- API response: 200ms latency
- Database query: 50ms latency
- Network call: 100ms latency

**Các thresholds:**
- < 100ms: Excellent
- 100-200ms: Good
- 200-500ms: Acceptable
- 500ms-1s: Poor
- > 1s: Unacceptable

#### 2. Throughput (Thông lượng)
```
Throughput = Requests per second (RPS)

Example:
- Server can handle 1000 requests/second
- Each request takes 10ms
- Throughput = 1000 RPS
```

#### 3. Response Time (Thời phản hồi)
```
Response Time = Processing Time + Network Latency + Waiting in Queue

Example:
API response time = 300ms
  - Processing: 100ms
  - Network: 100ms
  - Queue wait: 100ms
```

### Cách improve Performance

#### 1. Caching
```
Request → Check Cache (hit!)
          Return cached response (fast!)

vs

Request → Process (slow)
        → Database query (slow)
        → Build response (slow)
```

**Types:**
- Browser cache (localStorage)
- Server cache (Redis)
- Database query cache
- HTTP cache headers

#### 2. Database Optimization
```javascript
// Bad - N+1 problem
const users = await db.getUsers();
for (let user of users) {
  user.posts = await db.getPosts(user.id); // N queries!
}
// Queries: 1 (getUsers) + N (getPosts for each user)

// Good - Batch fetch
const users = await db.getUsers();
const allPosts = await db.getPosts(users.map(u => u.id));
// Queries: 2 (much better!)
```

#### 3. Async/Non-blocking
```javascript
// Bad - Blocking (waits for each operation)
const user = await db.getUser(1);
const posts = await db.getPosts(user.id);
const comments = await db.getComments(posts[0].id);
// Time: 100ms + 100ms + 100ms = 300ms

// Good - Parallel (does operations concurrently)
const user = await db.getUser(1);
const [posts, friends] = await Promise.all([
  db.getPosts(user.id),
  db.getFriends(user.id)
]);
// Time: max(100ms, 100ms) = ~100ms (much faster!)
```

#### 4. Indexing
```sql
-- Bad - Full table scan (slow for large tables)
SELECT * FROM users WHERE email = 'john@example.com';

-- Good - Index on email (fast!)
CREATE INDEX idx_email ON users(email);
SELECT * FROM users WHERE email = 'john@example.com';
```

#### 5. Code Optimization
```javascript
// Bad - Inefficient algorithm (O(n²))
function findDuplicate(arr) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return arr[i];
    }
  }
}

// Good - Efficient algorithm (O(n))
function findDuplicate(arr) {
  const seen = new Set();
  for (let num of arr) {
    if (seen.has(num)) return num;
    seen.add(num);
  }
}
```

### Real-world Example: Google Search Performance

```
Google optimized search response time:
- 2000: ~1 second average response
- 2005: ~0.5 second
- 2010: ~0.25 second
- 2020: ~0.1 second (100ms)

Techniques used:
1. Multi-layer caching
2. Distributed search across data centers
3. Database sharding
4. Efficient algorithms
5. Hardware optimization
```

---

## 6. Security (Bảo mật)

### Định nghĩa

Security là bảo vệ hệ thống khỏi:
- Unauthorized access
- Data theft
- Data modification
- Denial of service

### OWASP Top 10 Vulnerabilities

#### 1. Injection
```javascript
// Bad - SQL Injection vulnerable
const email = request.body.email;
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.execute(query);

// If user enters: admin' --
// Query becomes: SELECT * FROM users WHERE email = 'admin' --'
// Returns ALL users!

// Good - Parameterized queries
const query = 'SELECT * FROM users WHERE email = ?';
db.execute(query, [email]);
```

#### 2. Broken Authentication
```javascript
// Bad - Weak password hashing
const hash = md5(password); // MD5 is broken!

// Good - Strong password hashing
const hash = bcrypt.hash(password, 10);
```

#### 3. Sensitive Data Exposure
```javascript
// Bad - Storing passwords in plain text
const user = {
  email: 'john@example.com',
  password: 'john123' // NEVER!
};

// Bad - Logging sensitive data
logger.info('User logged in:', user); // password exposed in logs!

// Good - Hash passwords, never log sensitive data
const user = {
  email: 'john@example.com',
  passwordHash: '$2b$10$...' // Hashed
};
```

#### 4. XML External Entity (XXE)
```xml
<!-- Bad - Vulnerable to XXE -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>

<!-- Good - Disable external entities -->
<!-- Use a security-focused XML parser -->
```

#### 5. Broken Access Control
```javascript
// Bad - No authorization check
app.get('/users/:id', (req, res) => {
  const user = db.getUser(req.params.id);
  res.json(user); // Anyone can access any user!
});

// Good - Check authorization
app.get('/users/:id', (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = db.getUser(req.params.id);
  res.json(user);
});
```

#### 6. Security Misconfiguration
```javascript
// Bad - Debug mode on production
app.set('debug', true); // Stack traces exposed!

// Bad - Default credentials
db.connect('localhost', 'admin', 'password');

// Good - Use environment variables
db.connect(process.env.DB_HOST, process.env.DB_USER, process.env.DB_PASS);
```

#### 7. Cross-Site Scripting (XSS)
```javascript
// Bad - Reflected XSS
const name = request.query.name;
res.send(`<h1>Hello ${name}</h1>`);

// If user visits: ?name=<script>alert('hacked')</script>
// Script executes in browser!

// Good - Escape HTML
const name = request.query.name;
const escaped = htmlEscape(name);
res.send(`<h1>Hello ${escaped}</h1>`);
```

#### 8. Insecure Deserialization
```javascript
// Bad - Deserializing untrusted data
const user = JSON.parse(request.body);
// Attacker could inject code

// Good - Validate before deserializing
const schema = Joi.object({
  email: Joi.string().email(),
  name: Joi.string()
});
const { error, value } = schema.validate(request.body);
if (error) throw error;
const user = value;
```

#### 9. Using Components with Known Vulnerabilities
```bash
# Bad - Using old dependencies
npm ls
# See vulnerable packages

# Good - Keep dependencies updated
npm audit
npm audit fix
npm update
```

#### 10. Insufficient Logging & Monitoring
```javascript
// Bad - No logging of suspicious activities
app.post('/login', (req, res) => {
  const user = db.getUser(req.body.email);
  if (!user || user.password !== req.body.password) {
    res.status(401).json({ error: 'Invalid credentials' });
  }
  // No log of failed attempt!
});

// Good - Log security events
app.post('/login', (req, res) => {
  const user = db.getUser(req.body.email);
  if (!user || user.password !== req.body.password) {
    logger.warn('Failed login attempt', {
      email: req.body.email,
      ip: req.ip,
      timestamp: new Date()
    });
    res.status(401).json({ error: 'Invalid credentials' });
  }
});
```

### Cách improve Security

#### 1. Use HTTPS
```javascript
// Bad - HTTP (data in plain text)
app.listen(3000); // HTTP

// Good - HTTPS (encrypted)
const https = require('https');
const fs = require('fs');
const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};
https.createServer(options, app).listen(443);
```

#### 2. Authentication & Authorization
```javascript
// Good - JWT tokens
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// Good - Role-based access control
if (!request.user.roles.includes('admin')) {
  return res.status(403).json({ error: 'Forbidden' });
}
```

#### 3. Input Validation
```javascript
// Good - Validate and sanitize input
const email = validator.isEmail(request.body.email);
const name = request.body.name.trim();
if (name.length < 1 || name.length > 100) {
  throw new Error('Invalid name length');
}
```

#### 4. Secrets Management
```javascript
// Bad - Hardcoded secrets
const apiKey = 'sk-1234567890';

// Good - Environment variables
const apiKey = process.env.API_KEY;

// Better - Secrets manager (AWS Secrets Manager, HashiCorp Vault)
const secret = await secretsManager.getSecret('api-key');
```

#### 5. Security Headers
```javascript
// Good - Add security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## 7. Trade-offs entre Quality Attributes

Không thể optimize tất cả cùng lúc. Phải chọn:

```
┌──────────────────────────────────────────┐
│   Quality Attributes Trade-offs          │
├──────────────────────────────────────────┤
│ Scalability ↔ Complexity                 │
│ Performance ↔ Maintainability            │
│ Availability ↔ Cost                      │
│ Security ↔ Usability                     │
│ Flexibility ↔ Performance                │
└──────────────────────────────────────────┘
```

### Ví dụ Trade-offs

#### Scalability ↔ Complexity
```
Monolith (Simple, Hard to scale)
↓
Microservices (Complex, Easy to scale)

Choose based on current needs!
```

#### Performance ↔ Maintainability
```
Optimized code (Fast, Hard to understand)
↓
Clean code (Slower, Easy to understand)

Find balance!
```

#### Availability ↔ Cost
```
Single server (Cheap, Low availability)
↓
Multi-region, redundant (Expensive, High availability)

Choose based on business criticality!
```

---

## 8. Đo lường Quality Attributes

### Metrics và SLAs

| Attribute | Metric | Example SLA |
|-----------|--------|-------------|
| **Scalability** | Response time increase | <20% when load 10x |
| **Reliability** | MTBF, MTTR | MTBF > 30 days |
| **Availability** | Uptime % | 99.9% uptime |
| **Maintainability** | Code coverage, CC | >80% coverage |
| **Performance** | Latency, Throughput | <200ms latency |
| **Security** | Vulnerabilities found | Zero critical bugs |

### Monitoring & Observability

```
┌─────────────────────────────────────────┐
│  Monitoring Stack                       │
├─────────────────────────────────────────┤
│  Metrics (Prometheus)                   │
│  Logs (ELK Stack)                       │
│  Traces (Jaeger)                        │
│  Alerts (PagerDuty)                     │
│  Dashboards (Grafana)                   │
└─────────────────────────────────────────┘
```

---

## 9. Tóm tắt Quality Attributes

| Attribute | Focus | Metric | Goal |
|-----------|-------|--------|------|
| **Scalability** | Handle growth | Response time | Consistent under load |
| **Reliability** | Correct behavior | MTBF | No wrong results |
| **Availability** | Uptime | % Available | 99.9%+ uptime |
| **Maintainability** | Code quality | Code coverage | Easy to change |
| **Performance** | Speed | Latency/RPS | <200ms response |
| **Security** | Protection | Vuln count | Zero critical bugs |

---

## 10. Bước tiếp theo

1. **Identify your priorities:** Cái gì quan trọng nhất cho dự án?
2. **Set targets:** SLO (Service Level Objectives)
3. **Measure current state:** Baseline metrics
4. **Implement improvements:** Focus on bottlenecks
5. **Monitor continuously:** Track over time
6. **Adjust based on feedback:** Iterate

Không thể perfect tất cả, nhưng có thể balanced và good!
