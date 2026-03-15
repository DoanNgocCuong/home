# Notification System - Hệ thống gửi thông báo

## Mức độ khó: ⭐⭐⭐ (Trung bình)

## Giới thiệu
Notification system cần deliver messages tới users across multiple channels (email, SMS, push, in-app) reliably at scale. Core requirement là ensure delivery without duplicates, handle failures gracefully, support scheduling.

## Yêu cầu Chức năng (Functional Requirements)
- Send notifications via multiple channels (email, SMS, push, in-app)
- Schedule notifications: immediate, scheduled, recurring
- Retry logic: handle failed deliveries
- Deduplication: no duplicate notifications
- Unsubscribe/Preferences: users control what they receive
- Delivery tracking: know delivery status
- Rate limiting: prevent notification spam
- Batch sending: efficient for bulk notifications

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Reliability: 99.9% delivery success rate
- Low latency: deliver within seconds
- Scalability: millions of notifications/day
- Deduplication: ensure no duplicates
- Extensibility: easy to add new channels
- Cost-effective: minimize cost per notification

## Các khái niệm chính
- **Message Queue**: Async notification processing (Kafka, RabbitMQ)
- **Service Layer**: Abstraction untuk different channels
- **Retry Strategy**: Exponential backoff, dead letter queue
- **Idempotency**: Ensure safe retries (idempotent keys)
- **Rate Limiting**: Per user, per channel quotas
- **Template Engine**: Dynamic notification content
- **Analytics**: Track delivery metrics

## Ước lượng
- Notifications per day: 10 billion
- QPS: 100,000+ notifications per second
- Channels: email, SMS, push, in-app
- Retry attempts: 3-5 attempts
- Success rate: 90-95% first attempt
- Latency requirement: < 5 seconds

## Kiến trúc cấp cao
```
Service/Event
    ↓
Notification API
    ↓
Message Queue (Kafka)
    ↓
Notification Service
    ├─ Email Service
    ├─ SMS Service
    ├─ Push Service
    └─ In-app Service
    ↓
User Notification
```

## Các trade-off chính
- **Real-time vs Batching**: Real-time faster but costlier, batching cheaper but delayed
- **At-most-once vs At-least-once**: At-least-once requires deduplication overhead
- **Sync vs Async**: Sync simpler but blocks caller, async more complex but responsive
- **Push vs Pull**: Push proactive but requires connection, pull simpler but less timely
- **Centralized vs Distributed**: Centralized simpler, distributed more scalable

## Các bài toán phân nhánh
- Personalized notifications (user preferences)
- Rich media notifications (images, videos)
- Interactive notifications (action buttons)
- A/B testing notification content
- Delivery optimization (best time to send)
- Multi-language support
- Accessibility (text-to-speech)
