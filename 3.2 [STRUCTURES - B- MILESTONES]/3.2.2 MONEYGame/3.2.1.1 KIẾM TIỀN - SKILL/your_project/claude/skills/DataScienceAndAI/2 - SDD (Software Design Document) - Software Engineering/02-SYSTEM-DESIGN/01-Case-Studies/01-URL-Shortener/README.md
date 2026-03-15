# Case Study #1: URL Shortener (TinyURL)

> Độ khó: ⭐ | Concepts: Hashing, Database Design, Caching, Read-heavy system
> Đây là bài kinh điển nhất để bắt đầu System Design!

---

## Bài Toán

Thiết kế hệ thống rút gọn URL: nhập URL dài → nhận URL ngắn. Click URL ngắn → redirect đến URL gốc.

**Ví dụ**: `https://example.com/very/long/path?param=value` → `https://tiny.url/abc123`

---

## Step 1: Requirements

### Functional
- Cho URL dài → tạo URL ngắn duy nhất
- Click URL ngắn → redirect đến URL gốc
- URL ngắn có thể custom (optional)
- URL có thể set thời gian hết hạn (optional)

### Non-Functional
- Hệ thống read-heavy (nhiều người click hơn tạo): tỉ lệ 100:1
- URL ngắn phải ngắn nhất có thể
- Redirect phải nhanh (< 200ms)
- High availability (không chấp nhận downtime)

---

## Step 2: Estimation

| Metric | Con số |
|--------|--------|
| New URLs/day | 100M |
| Reads/day | 10B (100:1 ratio) |
| Write QPS | ~1,160 |
| Read QPS | ~116,000 |
| Storage/URL | ~500 bytes |
| Storage/5 năm | ~100M × 365 × 5 × 500B ≈ 91 TB |

---

## Step 3: API Design

```
POST /api/v1/shorten
  Body: { "long_url": "https://...", "custom_alias": "abc", "expiry": "2025-12-31" }
  Response: { "short_url": "https://tiny.url/abc123" }

GET /{short_url_key}
  Response: 301 Redirect to long_url
```

**301 vs 302 Redirect?**
- 301 (Permanent): browser cache → giảm load server nhưng mất analytics
- 302 (Temporary): browser không cache → nhiều request hơn nhưng track được clicks

---

## Step 4: Data Model

```sql
Table: urls
├── id (PK, BIGINT)
├── short_key (VARCHAR(7), UNIQUE, INDEX)
├── long_url (VARCHAR(2048))
├── created_at (TIMESTAMP)
├── expires_at (TIMESTAMP, nullable)
└── user_id (BIGINT, nullable, FK)
```

---

## Step 5: URL Shortening Strategies

### Option A: Hash Function
1. Hash long URL: MD5/SHA256 → lấy 7 ký tự đầu
2. Collision? → thêm salt rồi hash lại

**Ưu**: deterministic, cùng URL → cùng short key
**Nhược**: collision handling phức tạp

### Option B: Counter-based (Base62)
1. Auto-increment ID: 1, 2, 3, ...
2. Convert sang Base62: `1 → 1`, `62 → 10`, `3521614606208 → zzzzzz`
3. 7 ký tự Base62 = 62^7 = ~3.5 trillion URLs

**Ưu**: không collision, đơn giản
**Nhược**: cần distributed ID generator, URL có thể đoán được

### Option C: Pre-generated Keys
1. Tạo sẵn pool random keys
2. Mỗi request → lấy 1 key từ pool
3. Dùng KGS (Key Generation Service) riêng

**Ưu**: nhanh, không collision tại runtime
**Nhược**: cần maintain key pool, sync giữa servers

---

## Step 6: High-Level Architecture

```
Client → Load Balancer → Web Servers → Cache (Redis) → Database
                              ↑
                    Key Generation Service
```

### Flow - Tạo URL ngắn:
1. Client POST long URL
2. Web server request key từ KGS (hoặc hash)
3. Lưu mapping vào DB
4. Cache mapping vào Redis
5. Return short URL

### Flow - Redirect:
1. Client GET short URL
2. Check Redis cache → hit? → redirect
3. Cache miss → query DB → cache result → redirect
4. Not found → 404

---

## Step 7: Deep Dive

### Caching
- Cache top 20% URLs (theo Pareto principle, 20% URLs chiếm 80% traffic)
- LRU eviction
- Redis cluster cho HA

### Database
- Read-heavy → dùng read replicas
- Sharding by hash(short_key) cho scale
- NoSQL (DynamoDB) cũng phù hợp vì chỉ key-value lookup

### Rate Limiting
- Giới hạn URL creation per user/IP
- Tránh abuse (spam, phishing)

### Analytics (bonus)
- Track clicks, referrer, geo, device
- Stream click events vào Kafka → analytics pipeline

---

## Tổng Kết Trade-offs

| Decision | Chọn | Lý do |
|----------|------|-------|
| Hash vs Counter vs KGS | KGS | Không collision, predictable performance |
| SQL vs NoSQL | NoSQL (DynamoDB) | Simple key-value, high scale |
| 301 vs 302 | 302 | Cần analytics tracking |
| Cache strategy | Cache-aside + LRU | Read-heavy, hot URLs |
