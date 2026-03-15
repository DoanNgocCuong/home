# Caching & CDN

---

## 1. Caching là gì?

Lưu trữ tạm kết quả để lần sau truy cập nhanh hơn. Giảm load cho database và giảm latency.

### Caching ở đâu?

```
Client → CDN → Load Balancer → App Server Cache → Database Cache → Database
         ↑           ↑              ↑                  ↑
    Browser cache  Reverse proxy  Redis/Memcached   Query cache
```

---

## 2. Caching Strategies

### Cache-Aside (Lazy Loading)
1. App kiểm tra cache
2. Cache miss → đọc DB → ghi vào cache → return
3. Cache hit → return từ cache

**Ưu**: chỉ cache data thực sự được đọc. **Nhược**: cold start chậm, data có thể stale.

### Write-Through
1. App ghi vào cache VÀ DB đồng thời
2. Read luôn từ cache

**Ưu**: cache luôn fresh. **Nhược**: write chậm hơn (ghi 2 nơi), cache data có thể không bao giờ được đọc.

### Write-Behind (Write-Back)
1. App ghi vào cache
2. Cache async ghi vào DB sau

**Ưu**: write cực nhanh. **Nhược**: risk mất data nếu cache chết trước khi flush.

---

## 3. Cache Eviction Policies

Khi cache đầy, bỏ cái nào?

- **LRU** (Least Recently Used): bỏ item lâu nhất chưa dùng — phổ biến nhất
- **LFU** (Least Frequently Used): bỏ item ít dùng nhất
- **FIFO**: bỏ item cũ nhất
- **TTL** (Time To Live): tự hết hạn sau N giây

---

## 4. Redis

In-memory data store phổ biến nhất cho caching.

**Tại sao Redis?**
- Cực nhanh (in-memory, ~100μs latency)
- Hỗ trợ nhiều data structures: strings, lists, sets, sorted sets, hashes
- Persistence options: RDB snapshots, AOF logs
- Pub/Sub, Lua scripting
- Clustering & replication built-in

**Use cases**: session store, rate limiting, leaderboards, real-time analytics

---

## 5. CDN (Content Delivery Network)

Mạng lưới servers phân tán toàn cầu, phục vụ static content gần user nhất.

### CDN hoạt động thế nào?
1. User request `image.jpg`
2. DNS route đến CDN edge server gần nhất
3. Edge có cache → return ngay (cache hit)
4. Edge không có → lấy từ origin server → cache lại → return

### Push CDN vs Pull CDN
- **Push**: bạn upload content lên CDN chủ động. Tốt cho content ít thay đổi.
- **Pull**: CDN tự lấy từ origin khi có request đầu tiên. Dễ setup hơn, phổ biến hơn.

---

## 6. Cache Problems

### Cache Stampede
Nhiều requests đồng thời cho cùng 1 key bị miss → tất cả đều query DB. **Giải pháp**: lock, stale-while-revalidate.

### Cache Penetration
Request cho data không tồn tại → luôn miss cache, luôn query DB. **Giải pháp**: cache null values, Bloom filter.

### Cache Avalanche
Nhiều cache keys expire cùng lúc → DB bị overwhelm. **Giải pháp**: random TTL, circuit breaker.

---

## Checklist Tự Kiểm Tra

- [ ] Phân biệt Cache-Aside vs Write-Through vs Write-Behind
- [ ] Biết khi nào dùng LRU vs TTL
- [ ] Giải thích Redis dùng để làm gì trong System Design
- [ ] Hiểu CDN flow và Push vs Pull
- [ ] Biết 3 cache problems và cách giải quyết
