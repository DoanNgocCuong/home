# SYSTEM DESIGN ARCHITECT - LỘ TRÌNH HỌC

> 2 anh em cùng chinh phục System Design từ zero to hero
> Approach: **Case Study Driven** - Học qua phân tích hệ thống thực tế

---

## TỔNG QUAN LỘ TRÌNH

### Phase 1: Nền Tảng (Tuần 1-3)
Trước khi nhảy vào case study, cần nắm vững 6 khái niệm nền tảng. Không có foundations này thì đọc case study sẽ như đọc tiếng ngoài hành tinh.

| # | Topic | Thời gian | Mục tiêu |
|---|-------|-----------|----------|
| 1 | Core Concepts | 3-4 ngày | Hiểu scalability, availability, consistency, CAP theorem |
| 2 | Networking Basics | 2-3 ngày | HTTP, TCP/UDP, DNS, WebSocket, API design |
| 3 | Database Fundamentals | 3-4 ngày | SQL vs NoSQL, sharding, replication, indexing |
| 4 | Caching & CDN | 2 ngày | Cache strategies, Redis, CDN hoạt động thế nào |
| 5 | Load Balancing | 1-2 ngày | Algorithms, L4 vs L7, health checks |
| 6 | Message Queues | 2 ngày | Kafka, RabbitMQ, pub/sub, event-driven |

### Phase 2: Case Studies Dễ → Khó (Tuần 4-12)
Mỗi case study sẽ áp dụng kiến thức nền tảng vào hệ thống thực. Sắp xếp từ đơn giản đến phức tạp.

| # | Case Study | Độ khó | Concepts chính |
|---|-----------|--------|----------------|
| 1 | URL Shortener (TinyURL) | ⭐ | Hashing, DB design, caching |
| 2 | Rate Limiter | ⭐ | Algorithms, distributed counting |
| 3 | Chat System (WhatsApp) | ⭐⭐ | WebSocket, message queue, presence |
| 4 | News Feed (Facebook) | ⭐⭐ | Fan-out, ranking, caching |
| 5 | Video Platform (YouTube) | ⭐⭐⭐ | Streaming, encoding, CDN, storage |
| 6 | Ride Sharing (Uber) | ⭐⭐⭐ | Geospatial, matching, real-time |
| 7 | Search Engine (Google) | ⭐⭐⭐ | Indexing, crawling, ranking |
| 8 | Notification System | ⭐⭐ | Push, multi-channel, prioritization |
| 9 | E-Commerce (Amazon) | ⭐⭐⭐ | Inventory, payment, order flow |
| 10 | Cloud Storage (Dropbox) | ⭐⭐⭐ | File sync, chunking, dedup |

### Phase 3: Tổng Hợp & Interview Prep (Tuần 13+)
Sau khi xong các case studies, luyện cách trình bày design trong 45 phút.

---

## CÁCH HỌC HIỆU QUẢ

### Quy trình cho mỗi Case Study:
1. **Đọc README** - Hiểu bài toán và requirements
2. **Tự vẽ diagram** trước khi xem solution
3. **Xem diagram mẫu** trong file mermaid
4. **Thảo luận 2 người** - Trade-offs, tại sao chọn A mà không chọn B?
5. **Ghi chú** vào file notes theo template
6. **Ôn tập** bằng checklist câu hỏi

### Mỗi folder Case Study chứa:
- `README.md` - Lý thuyết + phân tích chi tiết
- `diagram.mermaid` - Kiến trúc hệ thống dạng diagram
- `checklist.md` - Câu hỏi ôn tập + self-check
- `notes.md` - Template ghi chú khi học (2 ae cùng fill)

---

## TÀI NGUYÊN THAM KHẢO

- **Sách**: "System Design Interview" - Alex Xu (Vol 1 & 2)
- **YouTube**: ByteByteGo, Hussein Nasser, Gaurav Sen
- **Web**: systemdesign.one, donnemartin/system-design-primer (GitHub)
- **Practice**: Excalidraw (vẽ diagram), Mermaid Live Editor

---

> **Ghi nhớ**: System Design không có đáp án đúng duy nhất. Quan trọng là hiểu **trade-offs** và biết **giải thích tại sao** mình chọn giải pháp đó.
