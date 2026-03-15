# 01 - KIẾN TRÚC THIẾT KẾ (ARCHITECTURE DESIGN)

## 1. Architecture Design là gì?

Architecture Design (Thiết kế Kiến trúc) là quá trình lập kế hoạch, quyết định cấu trúc tổng thể của hệ thống phần mềm. Nó xác định cách các thành phần lớn của ứng dụng tương tác với nhau, cách dữ liệu chảy qua hệ thống, và cách các yêu cầu không chức năng (non-functional requirements) được đáp ứng.

**Nói đơn giản:** Architecture Design trả lời những câu hỏi như:
- Ứng dụng có bao nhiêu tầng (layers)?
- Các service sẽ được chia như thế nào?
- Dữ liệu được lưu trữ ở đâu?
- Các phần của hệ thống giao tiếp như thế nào?
- Làm sao để hệ thống có thể mở rộng (scale)?

## 2. Tại sao Architecture Design quan trọng?

### Ảnh hưởng đến Dài hạn
- **Dễ duy trì:** Kiến trúc tốt giúp code dễ hiểu và sửa đổi
- **Dễ mở rộng:** Thêm tính năng mới không phá hủy hệ thống hiện tại
- **Dễ kiểm tra:** Các component độc lập dễ viết unit test
- **Giảm chi phí:** Tránh viết lại code từ đầu

### Ảnh hưởng đến Hiệu suất
- **Hiệu năng cao:** Thiết kế đúng cách giúp hệ thống chạy nhanh
- **Khả năng chịu tải:** Hệ thống có thể xử lý nhiều users cùng lúc
- **Độ tin cậy:** Giảm bugs, downtime
- **Bảo mật:** Dựa trên các pattern bảo mật tốt

## 3. Phân biệt: Architecture vs System Design vs HLD/LLD

### Architecture (Kiến trúc)
- **Mức độ cao nhất:** Toàn bộ hệ thống
- **Phạm vi lớn:** Các thành phần chính, connections chính
- **Ví dụ:** "Chúng ta sẽ dùng microservices, React frontend, PostgreSQL"

### System Design (Thiết kế Hệ thống)
- **Mức độ chi tiết:** Chi tiết từng service, database schema
- **Phạm vi trung bình:** Cách xây dựng từng thành phần to
- **Ví dụ:** "Service này cần cache Redis, message queue Kafka"

### HLD - High Level Design (Thiết kế Cấp Cao)
- **Mức độ khá cao:** Tổng quan các modules chính
- **Chi tiết vừa phải:** Không chi tiết đến từng hàm
- **Ví dụ:** "Module auth sẽ xử lý login, 2FA, token management"

### LLD - Low Level Design (Thiết kế Cấp Thấp)
- **Mức độ chi tiết nhất:** Thiết kế từng function, class, algorithm
- **Chi tiết rất cao:** Cách implement từng tính năng
- **Ví dụ:** "Hàm `hashPassword` sẽ dùng bcrypt với 10 rounds"

```
┌─────────────────────────────────────────────┐
│         ARCHITECTURE (Toàn bộ)              │
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │    SYSTEM DESIGN (Từng service)      │   │
│ │                                      │   │
│ │ ┌────────────────────────────────┐  │   │
│ │ │  HLD (Các modules chính)      │  │   │
│ │ │                                │  │   │
│ │ │ ┌──────────────────────────┐  │  │   │
│ │ │ │  LLD (Chi tiết từng code)│  │  │   │
│ │ │ └──────────────────────────┘  │  │   │
│ │ └────────────────────────────────┘  │   │
│ └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 4. Các loại Architecture chính

### 4.1 Monolithic Architecture (Kiến trúc Đơn khối)
- **Khái niệm:** Toàn bộ ứng dụng là một khối duy nhất
- **Đặc điểm:**
  - Một codebase, một database
  - Deploy toàn bộ hoặc không gì cả
  - Tất cả code chạy trên một process
- **Khi nào dùng:** Dự án nhỏ, startup mới

### 4.2 Microservices Architecture
- **Khái niệm:** Chia ứng dụng thành nhiều service nhỏ, độc lập
- **Đặc điểm:**
  - Mỗi service: một codebase, một database riêng
  - Mỗi service có thể deploy độc lập
  - Services giao tiếp qua API (HTTP/REST, gRPC)
- **Khi nào dùng:** Dự án lớn, cần scale riêng từng phần

### 4.3 Serverless Architecture
- **Khái niệm:** Không cần quản lý server, chỉ tập trung vào code
- **Đặc điểm:**
  - Code chạy bằng functions (AWS Lambda, Google Cloud Functions)
  - Pay-as-you-go (trả tiền theo lượng code chạy)
  - Auto-scaling tự động
- **Khi nào dùng:** Các tác vụ không thường xuyên, event-driven

### 4.4 Event-Driven Architecture
- **Khái niệm:** Các thành phần giao tiếp qua events (sự kiện)
- **Đặc điểm:**
  - Có producer (tạo event) và consumer (xử lý event)
  - Thường dùng message broker (Kafka, RabbitMQ)
  - Loose coupling (các thành phần độc lập)
- **Khi nào dùng:** Hệ thống cần real-time, async processing

### 4.5 Layered/N-Tier Architecture
- **Khái niệm:** Chia ứng dụng thành các tầng (layers)
- **Đặc điểm:**
  - Presentation Layer (UI)
  - Business Logic Layer
  - Data Access Layer
  - Database Layer
  - Mỗi tầng có trách nhiệm riêng
- **Khi nào dùng:** Dự án truyền thống, cần tách biệt rõ ràng

### 4.6 Hexagonal Architecture (Ports & Adapters)
- **Khái niệm:** Business logic ở giữa, giao tiếp với bên ngoài qua ports & adapters
- **Đặc điểm:**
  - Core logic độc lập với framework
  - Dễ kiểm tra (testable)
  - Flexible thay đổi dependencies
- **Khi nào dùng:** Dự án cần flexibility cao, architecture-centric

## 5. Quality Attributes (Các đặc tính chất lượng)

Quality Attributes là những yêu cầu không chức năng (-ilities) ảnh hưởng đến thiết kế:

### Scalability (Khả năng mở rộng)
- **Khái niệm:** Hệ thống có thể xử lý nhiều data/users hơn
- **Ví dụ:** App của bạn hôm nay 100 users, ngày mai 100,000 users
- **Cách đo:** Response time, throughput giữ nguyên khi tăng load

### Reliability (Độ tin cậy)
- **Khái niệm:** Hệ thống hoạt động đúng, không bị lỗi
- **Ví dụ:** API response đúng, không trả về data sai
- **Cách đo:** % thời gian hoạt động đúng (MTBF - Mean Time Between Failures)

### Availability (Tính khả dụng)
- **Khái niệm:** Hệ thống luôn sẵn sàng để sử dụng
- **Ví dụ:** 99.9% uptime (chỉ downtime 43 phút/tháng)
- **Cách đo:** % thời gian hệ thống online (MTTF, MTTR)

### Maintainability (Khả năng bảo trì)
- **Khái niệm:** Code dễ sửa, dễ thêm tính năng mới
- **Ví dụ:** Developer mới hiểu code sau 1 ngày
- **Cách đo:** Thời gian để fix bug, thêm feature

### Security (Bảo mật)
- **Khái niệm:** Bảo vệ dữ liệu, ngăn chặn truy cập trái phép
- **Ví dụ:** Mật khẩu mã hóa, SQL injection protection
- **Cách đo:** Số lỗi bảo mật tìm được, security audit score

### Performance (Hiệu suất)
- **Khái niệm:** Hệ thống chạy nhanh
- **Ví dụ:** API response trong 200ms
- **Cách đo:** Response time, latency, throughput

### Usability (Khả năng sử dụng)
- **Khái niệm:** Giao diện dễ sử dụng
- **Ví dụ:** Người dùng tìm được tính năng dễ dàng
- **Cách đo:** User testing, NPS score

## 6. CAP Theorem

CAP Theorem nói rằng hệ thống phân tán chỉ có thể đạt được 2 trong 3 điều sau:

```
        ┌─ Consistency (Nhất quán)
        │  Tất cả nodes luôn có dữ liệu giống nhau
        │
    ┌───┴────┐
    │   CAP   │
    └────┬────┘
    ┌────┘
    │
    ├─ Availability (Khả dụng)
    │  Hệ thống luôn response
    │
    └─ Partition Tolerance (Chịu phân vùng)
       Hệ thống hoạt động khi network bị chia cắt
```

### CP (Consistency + Partition Tolerance)
- Sacrifice Availability
- Database chọn nhất quán hơn khả dụng
- Ví dụ: PostgreSQL, MongoDB (strongly consistent)

### AP (Availability + Partition Tolerance)
- Sacrifice Consistency
- Luôn response nhưng dữ liệu có thể không nhất quán
- Ví dụ: DynamoDB, Cassandra (eventually consistent)

### CA (Consistency + Availability)
- Sacrifice Partition Tolerance
- Chỉ có thể dùng khi network không có vấn đề
- Hiếm gặp trong thực tế

## 7. Khi nào cần suy nghĩ về Architecture

**Nên bắt đầu suy nghĩ về architecture từ sớm nếu:**

✓ Dự án sẽ lớn (>50,000 lines of code)
✓ Có nhiều developers làm việc cùng lúc
✓ Cần scale theo thời gian
✓ Dữ liệu nhạy cảm (cần bảo mật cao)
✓ High availability requirement (99.9%+ uptime)
✓ Dự kiến nhiều external integrations

**Có thể không cần ngay nếu:**
- MVP nhỏ, muốn ra nhanh
- Dự án prototype
- Không chắc requirements

**Nhưng sau vài tháng, khi dự án phát triển, bắt buộc phải có architecture tốt!**

## 8. Tóm tắt

| Khía cạnh | Nội dung |
|-----------|---------|
| **Định nghĩa** | Lập kế hoạch cấu trúc tổng thể hệ thống |
| **Mục đích** | Đảm bảo hệ thống scalable, reliable, maintainable |
| **Loại chính** | Monolith, Microservices, Serverless, Event-Driven, Layered, Hexagonal |
| **Quality Attributes** | Scalability, Reliability, Availability, Maintainability, Security, Performance |
| **CAP Theorem** | Chọn 2 trong 3: Consistency, Availability, Partition Tolerance |
| **Bắt đầu khi nào** | Từ sớm cho dự án lớn, hoặc khi dự án phát triển |

---

**Tiếp theo:** Tìm hiểu chi tiết từng Architecture Pattern trong tài liệu `01-Architecture-Patterns`
