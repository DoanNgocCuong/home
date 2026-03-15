# Message Queues & Event-Driven Architecture

---

## 1. Message Queue là gì?

Hệ thống trung gian giữa producer và consumer, giúp decouple các services.

```
Producer → [Message Queue] → Consumer
              ↑
         Messages chờ ở đây
         cho đến khi consumer sẵn sàng
```

**Tại sao cần?**
- **Decoupling**: services không cần biết nhau trực tiếp
- **Async processing**: không cần xử lý ngay, xử lý khi rảnh
- **Load leveling**: absorb traffic spikes
- **Reliability**: message không mất nếu consumer chết tạm

---

## 2. Patterns

### Point-to-Point (Queue)
1 message → 1 consumer. Như hàng đợi: ai lấy trước thì xong.

### Publish/Subscribe (Pub/Sub)
1 message → nhiều consumers. Như broadcast: tất cả subscribers đều nhận.

```
Point-to-Point:         Pub/Sub:
Producer → Queue → C1   Publisher → Topic → C1
                                         → C2
                                         → C3
```

---

## 3. Kafka vs RabbitMQ

| | Kafka | RabbitMQ |
|---|-------|---------|
| Model | Distributed log | Message broker |
| Ordering | Guaranteed per partition | Per queue |
| Throughput | Cực cao (millions/sec) | Cao (10K-100K/sec) |
| Persistence | Lưu trên disk lâu dài | Xóa sau khi consumed |
| Use case | Event streaming, data pipeline | Task queue, RPC |
| Replay | Có thể đọc lại messages | Không (đã consumed thì mất) |

### Khi nào dùng gì?
- **Kafka**: event sourcing, log aggregation, real-time analytics, data pipeline
- **RabbitMQ**: background jobs, email sending, order processing

---

## 4. Event-Driven Architecture

Thay vì services gọi nhau trực tiếp (synchronous), services publish events và listen events (asynchronous).

```
Truyền thống:         Event-Driven:
Order → Payment       Order → publishes "OrderCreated"
Order → Inventory          ↓
Order → Notification  Payment listens → xử lý
                      Inventory listens → xử lý
                      Notification listens → xử lý
```

**Ưu điểm**: loose coupling, dễ thêm service mới, resilient. **Nhược điểm**: debug khó hơn, eventual consistency, message ordering.

---

## 5. Delivery Guarantees

| Guarantee | Nghĩa | Trade-off |
|-----------|-------|-----------|
| At-most-once | Gửi 1 lần, có thể mất | Nhanh nhất, có thể mất data |
| At-least-once | Đảm bảo nhận, có thể duplicate | Consumer phải idempotent |
| Exactly-once | Mỗi message xử lý đúng 1 lần | Khó nhất, chậm nhất |

**Thực tế**: hầu hết dùng **at-least-once** + idempotent consumer.

---

## 6. Dead Letter Queue (DLQ)

Messages xử lý thất bại sau N lần retry → chuyển vào DLQ để debug/xử lý manual. Tránh block queue chính.

---

## Checklist Tự Kiểm Tra

- [ ] Giải thích được tại sao cần message queue
- [ ] Phân biệt point-to-point vs pub/sub
- [ ] Chọn đúng Kafka hay RabbitMQ cho scenario cụ thể
- [ ] Hiểu event-driven architecture ưu nhược
- [ ] Biết 3 loại delivery guarantee và trade-offs
- [ ] Giải thích Dead Letter Queue
