# Chat System (WhatsApp) - Hệ thống nhắn tin real-time

## Mức độ khó: ⭐⭐⭐⭐ (Khó)

## Giới thiệu
Một hệ thống chat real-time giống WhatsApp cần hỗ trợ millions của users đang active cùng lúc. Hệ thống phải đảm bảo messages được deliver nhanh chóng, reliably, và maintain conversation history.

## Yêu cầu Chức năng (Functional Requirements)
- Users có thể gửi và nhận messages 1-to-1 hoặc group
- Real-time message delivery (notification lập tức)
- Offline message handling: lưu messages cho users offline, deliver khi online
- Message history: retrieve past conversations
- Typing indicators: show khi user đang gõ
- Delivery status: sent, delivered, read
- Media sharing: images, videos, files
- Group management: create, add/remove members

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Low latency: < 100ms cho message delivery
- Availability: 99.9% uptime
- Reliability: no message loss
- Scalability: support billions của messages/day
- Data consistency: messages không được duplicate hay lost
- Mobile-friendly: efficient bandwidth và battery usage

## Các khái niệm chính
- **WebSocket/Long-Polling**: Real-time communication protocols
- **Message Queue**: Store messages chờ delivery (Kafka, RabbitMQ)
- **Presence System**: Track who's online/offline
- **Pub/Sub Model**: Efficient message broadcasting
- **Message Deduplication**: Ensure no duplicate messages
- **End-to-End Encryption**: Security consideration
- **Sharding**: Partition data cho scalability

## Ước lượng
- Daily Active Users: 100 million
- Messages per second: 1 million
- Message size: ~1KB average
- Storage per user: ~500MB/year
- Concurrent connections: 10-20 million

## Kiến trúc cấp cao
```
Client A (WebSocket)
    ↓
API Gateway → Chat Servers (stateful)
    ↓
Message Queue (Kafka)
    ↓
Message Storage (database)
    ↓
Presence Service (Redis)
    ↓
Notification Service
    ↓
Client B (WebSocket)
```

## Các trade-off chính
- **Push vs Pull**: Push faster nhưng yêu cầu persistent connection, pull simple nhưng more latency
- **Strong vs Eventual Consistency**: Strong consistency chậm hơn, eventual consistency faster
- **Memory vs Disk**: Cache frequently accessed messages in memory nhưng limited space
- **Single region vs Multi-region**: Single region simpler, multi-region better availability
- **Encryption overhead**: E2E encryption adds latency but better security

## Các bài toán phân nhánh
- Group chat optimization (1000+ members)
- Search history efficiently
- Message reactions/threads
- Voice/video call integration
- Read receipts at scale
