# Checklist - Rate Limiter

## Mức độ cơ bản (Basic)
- [ ] Hiểu khái niệm rate limiting là gì và tại sao cần nó?
- [ ] Token bucket algorithm hoạt động thế nào?
- [ ] Fixed window counter là gì? Ưu/nhược điểm gì?
- [ ] Sliding window log là gì? Tại sao chính xác hơn fixed window?
- [ ] HTTP 429 status code là gì và khi nào dùng?
- [ ] Cách lưu trữ rate limit state (in-memory vs distributed)?
- [ ] Làm sao để track rate limit per user/IP/key?

## Mức độ trung bình (Intermediate)
- [ ] Sliding window counter vs Sliding window log - cái nào tốt hơn?
- [ ] Leaky bucket algorithm là gì và khác gì token bucket?
- [ ] Làm sao thiết kế rate limiter có thể scale tới millions của concurrent users?
- [ ] Redis được dùng như thế nào trong distributed rate limiting?
- [ ] Race condition nào có thể xảy ra khi implement sliding window?
- [ ] Cách handle clock skew trong distributed system?
- [ ] Rate limiting headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)?
- [ ] Làm sao implement multi-level rate limiting (global + per-user)?
- [ ] Locality vs Consistency trade-off trong rate limiting?

## Mức độ nâng cao (Advanced)
- [ ] Distributed rate limiting challenges: eventually consistent vs strongly consistent?
- [ ] Làm sao handle rate limiting trong microservices architecture?
- [ ] Adaptive rate limiting dựa trên system load?
- [ ] Cách implement hierarchical rate limiting (endpoint-level, user-level, global-level)?
- [ ] Rate limiting strategy cho long-running requests (uploads, batch processing)?
- [ ] Burst traffic handling - làm sao allow short bursts nhưng prevent abuse?
- [ ] Cách test rate limiter hiệu quả?
- [ ] Monitoring và alerting cho rate limiter system?
- [ ] Cost optimization: in-memory vs Redis vs Memcached trong context này?
- [ ] Backwards compatibility khi update rate limit rules?

## Thực hành
- [ ] Implement single-threaded rate limiter với token bucket
- [ ] Implement distributed rate limiter sử dụng Redis
- [ ] Viết test cases để verify rate limiting behavior
- [ ] Benchmark performance của different algorithms
- [ ] Thiết kế rate limiting rules cho real-world service
