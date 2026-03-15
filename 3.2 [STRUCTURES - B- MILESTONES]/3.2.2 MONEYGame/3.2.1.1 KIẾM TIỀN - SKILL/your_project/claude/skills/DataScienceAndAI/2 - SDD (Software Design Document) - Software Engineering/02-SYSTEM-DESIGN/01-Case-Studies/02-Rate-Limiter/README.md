# Rate Limiter - Hệ thống giới hạn tốc độ yêu cầu

## Mức độ khó: ⭐⭐⭐ (Trung bình)

## Giới thiệu
Hệ thống Rate Limiter được thiết kế để kiểm soát tốc độ truy cập vào API hoặc dịch vụ web. Mục đích là ngăn chặn spam, bảo vệ khỏi DDoS attack, và đảm bảo công bằng trong việc sử dụng tài nguyên.

## Yêu cầu Chức năng (Functional Requirements)
- Giới hạn số lượng yêu cầu từ một user/IP trong khoảng thời gian nhất định
- Hỗ trợ nhiều loại rate limit policy (sliding window, token bucket, fixed window)
- Trả về HTTP 429 khi vượt giới hạn
- Cung cấp thông tin về giới hạn còn lại (headers: X-RateLimit-Remaining)

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Độ trễ thấp (milliseconds) cho mỗi request
- Khả năng mở rộng: hỗ trợ hàng triệu users đồng thời
- High availability: yêu cầu bị drop tốt hơn bị trì hoãn
- Consistency: tất cả servers phải áp dụng giới hạn giống nhau

## Các khái niệm chính
- **Token Bucket**: Mô hình phổ biến, tokens được thêm vào bucket định kỳ
- **Sliding Window**: Theo dõi chính xác trong time window
- **Fixed Window**: Đơn giản nhất, rate reset tại boundary
- **Distributed Rate Limiting**: Sử dụng Redis/Memcached để sync state
- **Leaky Bucket**: Queue requests, xử lý với tốc độ cố định

## Ước lượng
- Lưu trữ: ~1KB per active user/key
- Throughput: ~100,000 requests/second trên single instance
- Latency: < 10ms per request

## Kiến trúc cấp cao
```
Client Request
    ↓
Rate Limit Check (Redis/Memory)
    ├─ Within Limit → Allow Request
    └─ Exceeded → Return 429
    ↓
Upstream Service
```

## Các trade-off chính
- **Accuracy vs Performance**: Sliding window chính xác nhưng chậm hơn fixed window
- **Distributed Consistency**: Yêu cầu Redis/cache tập trung, nhưng cải thiện accuracy
- **Memory vs Network**: Cache local nhanh nhưng không consistent, centralized store chậm hơn
- **Hard limit vs Soft limit**: Hard limit chính xác nhưng có thể reject valid requests

## Các bài toán phân nhánh
- Multi-tier rate limiting (per user, per endpoint, per region)
- Async requests và rate limiting queue
- Rate limiting cho microservices
- Dynamic rate limits dựa trên user tier/subscription
