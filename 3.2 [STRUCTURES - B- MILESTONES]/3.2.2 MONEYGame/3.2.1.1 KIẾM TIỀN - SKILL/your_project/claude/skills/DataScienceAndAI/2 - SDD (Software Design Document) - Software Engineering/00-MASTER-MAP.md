# SDD (Software Design Document) - Master Map

## Tổng Quan Toàn Bộ Tài Liệu

Đây là tài liệu toàn diện về Software Design Document - một quy trình thiết kế hệ thống phần mềm từ cấp độ cao nhất (Architecture) xuống cấp độ chi tiết nhất (Low-Level Design).

---

## Sơ Đồ Mối Quan Hệ Các Thành Phần

```
┌─────────────────────────────────────────────────────────┐
│                  BUSINESS REQUIREMENTS                  │
│         (Yêu cầu kinh doanh từ người dùng)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         ARCHITECTURE DESIGN (Kiến Trúc Hệ Thống)       │
│  - Lựa chọn mô hình: Monolith, Microservices, v.v.    │
│  - Định nghĩa Quality Attributes (Scalability, etc)   │
│  - CAP Theorem, Trade-offs                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         SYSTEM DESIGN (Thiết Kế Hệ Thống)              │
│  - Database Schema, Caching Strategy                   │
│  - Load Balancing, Message Queues                      │
│  - Back-of-envelope Estimation, Capacity Planning      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│    HLD - High-Level Design (Thiết Kế Mức Cao)         │
│  - Biểu đồ các Module chính                            │
│  - Tương tác giữa các thành phần                       │
│  - API contracts giữa các service                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│    LLD - Low-Level Design (Thiết Kế Chi Tiết)         │
│  - Mã giả (Pseudocode)                                │
│  - Data structures cụ thể                              │
│  - Algorithms, Class diagrams                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Bảng Tổng Hợp 8 Phần Chính

| Phần | Tên | Mục Đích | Cấp Độ |
|------|-----|---------|--------|
| **01** | Architecture Design | Lựa chọn mô hình kiến trúc, định nghĩa Quality Attributes | Cao |
| **02** | System Design | Thiết kế các thành phần của hệ thống (Database, Cache, Load Balancer) | Cao |
| **03** | High-Level Design (HLD) | Biểu đồ tổng thể, API contracts, Module relationships | Trung bình |
| **04** | Low-Level Design (LLD) | Mã giả, thuật toán, class diagrams, chi tiết triển khai | Thấp |
| **05** | Database Design | Schema design, indexing, sharding, replication | Hỗ trợ |
| **06** | API Design | RESTful endpoints, request/response schemas, error handling | Hỗ trợ |
| **07** | Security Design | Authentication, Authorization, Encryption, OWASP Top 10 | Hỗ trợ |
| **08** | Deployment & DevOps | CI/CD, containerization, monitoring, logging | Hỗ trợ |

**Ghi chú:** Phần 05, 06, 07 là các lĩnh vực **hỗ trợ Software Engineering**, không phải là phần chính của quy trình SDD.

---

## 🗺️ Lộ Trình Học Tập 9 Tuần cho 2 Người

### Cấu Trúc Chung
- **Mỗi tuần:** 1 chủ đề chính + bài tập thực hành
- **Hình thức học:** Đọc lý thuyết, thảo luận nhóm, vẽ diagram, giải case study
- **Thời gian mỗi buổi:** 2-3 giờ

---

### Tuần 1: Nền Tảng Architecture Design
**Mục tiêu:** Hiểu các mô hình kiến trúc khác nhau

- Đọc: `01-ARCHITECTURE-DESIGN/README.md`
- Đọc: `01-ARCHITECTURE-DESIGN/01-Architecture-Patterns/README.md`
- **Bài tập:** Vẽ diagram so sánh Monolith vs Microservices cho một ứng dụng giả định
- **Thảo luận:** Khi nào nên dùng từng mô hình?

---

### Tuần 2: Quality Attributes & Giải Quyết Tranh Chấp
**Mục tiêu:** Hiểu các thuộc tính chất lượng và trade-offs

- Đọc: `01-ARCHITECTURE-DESIGN/05-Quality-Attributes/README.md`
- Đọc: `01-ARCHITECTURE-DESIGN/02-ADR-Architecture-Decision-Records/README.md`
- **Bài tập:** Viết 2-3 ADR cho một project giả định
- **Thảo luận:** Scalability vs Maintainability: cái nào quan trọng hơn?

---

### Tuần 3: Nền Tảng System Design
**Mục tiêu:** Hiểu các khái niệm cơ bản về System Design

- Đọc: `02-SYSTEM-DESIGN/00-ROADMAP.md`
- Đọc: `02-SYSTEM-DESIGN/00-Foundations/01-Core-Concepts/README.md`
- **Bài tập:** Tính toán capacity planning cho một hệ thống giả định (back-of-envelope estimation)
- **Thảo luận:** CAP Theorem - bạn sẽ lựa chọn gì?

---

### Tuần 4: Networking & API Design
**Mục tiêu:** Hiểu giao thức mạng và thiết kế API

- Đọc: `02-SYSTEM-DESIGN/00-Foundations/02-Networking-Basics/README.md`
- **Bài tập:** Thiết kế REST API cho một resource đơn giản
- **Thảo luận:** REST vs GraphQL - trade-offs?

---

### Tuần 5: Database Fundamentals
**Mục tiêu:** Hiểu các loại database và khi nào sử dụng

- Đọc: `02-SYSTEM-DESIGN/00-Foundations/03-Database-Fundamentals/README.md`
- **Bài tập:** Thiết kế schema cho một ứng dụng e-commerce đơn giản
- **Thảo luận:** SQL vs NoSQL - trade-offs?

---

### Tuần 6: Caching & CDN
**Mục tiêu:** Hiểu các chiến lược cache và tối ưu hóa hiệu suất

- Đọc: `02-SYSTEM-DESIGN/00-Foundations/04-Caching-CDN/README.md`
- **Bài tập:** Thiết kế caching strategy cho News Feed
- **Thảo luận:** Cache invalidation - bài toán khó nhất trong khoa học máy tính?

---

### Tuần 7: Load Balancing & Message Queues
**Mục tiêu:** Hiểu cách phân tán tải và xử lý bất đồng bộ

- Đọc: `02-SYSTEM-DESIGN/00-Foundations/05-Load-Balancing/README.md`
- Đọc: `02-SYSTEM-DESIGN/00-Foundations/06-Message-Queues/README.md`
- **Bài tập:** Thiết kế Load Balancing architecture cho hệ thống có lưu lượng cao
- **Thảo luận:** Kafka vs RabbitMQ - bạn sẽ chọn cái nào?

---

### Tuần 8: Case Study Dễ & Trung Bình
**Mục tiêu:** Áp dụng kiến thức vào các bài toán thực tế

- Đọc:
  - `02-SYSTEM-DESIGN/01-Case-Studies/01-URL-Shortener/README.md`
  - `02-SYSTEM-DESIGN/01-Case-Studies/02-Rate-Limiter/README.md`
  - `02-SYSTEM-DESIGN/01-Case-Studies/08-Notification-System/README.md`
- **Bài tập:** Tự thiết kế 1 system từ danh sách
- **Thảo luận:** So sánh thiết kế của bạn với nhau

---

### Tuần 9: Case Study Khó & Rất Khó
**Mục tiêu:** Hiểu các hệ thống phức tạp, thách thức

- Đọc:
  - `02-SYSTEM-DESIGN/01-Case-Studies/03-Chat-System-WhatsApp/README.md`
  - `02-SYSTEM-DESIGN/01-Case-Studies/04-News-Feed-Facebook/README.md`
  - `02-SYSTEM-DESIGN/01-Case-Studies/05-Video-Platform-YouTube/README.md`
  - `02-SYSTEM-DESIGN/01-Case-Studies/06-Ride-Sharing-Uber/README.md`
- **Bài tập:** Chọn 1 system khó, thiết kế toàn bộ (Architecture → LLD)
- **Thảo luận:** Những thách thức lớn nhất khi thiết kế hệ thống này?

---

## 🎯 Cách Sử Dụng Tài Liệu Này

### Học Lý Thuyết
1. Bắt đầu với **Architecture Design** (phần 01)
2. Tiến tới **System Design Foundations** (phần 02, subsection 00)
3. Áp dụng vào **Case Studies** (phần 02, subsection 01)

### Thực Hành
- **Vẽ diagrams** bằng Excalidraw hoặc Mermaid
- **Viết pseudocode** cho các thuật toán
- **Thảo luận** về trade-offs và lựa chọn thiết kế

### Các Tài Nguyên Bổ Sung
- Xem: `02-SYSTEM-DESIGN/_Resources/RECOMMENDED.md` để danh sách sách, YouTube channels, websites

---

## 📌 Ghi Chú Quan Trọng

1. **Phần 05, 06, 07** (Database Design, API Design, Security Design) là những lĩnh vực **hỗ trợ**, không phải core SDD. Chúng cần được học song song hoặc sau cùng.

2. **System Design khó hơn Architecture Design** vì nó yêu cầu kiến thức sâu hơn về các công nghệ cụ thể.

3. **Case Studies** rất quan trọng - đó là nơi bạn áp dụng toàn bộ kiến thức.

4. **Thảo luận nhóm** giúp bạn hiểu sâu hơn và khám phá các góc nhìn khác nhau.

---

## 📖 Tổng Hợp Nhanh Các Folder

```
01-ARCHITECTURE-DESIGN/
├── README.md (Giới thiệu chung)
├── 01-Architecture-Patterns/ (Chi tiết các mô hình)
├── 02-ADR-Architecture-Decision-Records/ (Cách viết quyết định kiến trúc)
└── 05-Quality-Attributes/ (Scalability, Reliability, v.v.)

02-SYSTEM-DESIGN/
├── 00-ROADMAP.md (Lộ trình học)
├── 00-Foundations/
│   ├── 01-Core-Concepts/ (CAP, Scalability, etc)
│   ├── 02-Networking-Basics/ (HTTP, DNS, TCP/UDP)
│   ├── 03-Database-Fundamentals/ (SQL vs NoSQL)
│   ├── 04-Caching-CDN/ (Cache strategies)
│   ├── 05-Load-Balancing/ (Phân tán tải)
│   └── 06-Message-Queues/ (Kafka, RabbitMQ)
├── 01-Case-Studies/ (10 bài toán thực tế)
├── _Resources/ (Sách, YouTube, website)
└── _Templates/ (Template ghi chú học tập)
```

---

**Hãy bắt đầu với Architecture Design, sau đó tiến tới System Design Foundations, và cuối cùng là Case Studies!**
