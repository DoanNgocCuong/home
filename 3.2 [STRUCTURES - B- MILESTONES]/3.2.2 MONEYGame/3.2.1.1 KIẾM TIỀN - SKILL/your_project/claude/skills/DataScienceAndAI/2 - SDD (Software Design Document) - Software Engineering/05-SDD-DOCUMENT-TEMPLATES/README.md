# Software Design Document (SDD) - Hướng Dẫn & Template

## SDD là gì?

**Software Design Document (SDD)** là tài liệu chi tiết mô tả cách thiết kế và xây dựng một hệ thống phần mềm. Nó là bản thiết kế kỹ thuật chi tiết, chuyên dùng cho **developers** để hiểu rõ cách code sẽ được viết.

### Khác biệt quan trọng:
- **SDD** = Tài liệu kỹ thuật CHI TIẾT cho developers (code-level design)
- **PRD** = Tài liệu yêu cầu cho product managers (tính năng, use cases)
- **BRD** = Tài liệu yêu cầu kinh doanh cho stakeholders (lợi ích, mục tiêu)
- **TDD** = Tài liệu kiểm thử kỹ thuật chi tiết (test cases)

## Ai viết SDD?

- **Chủ yếu**: Architects, Senior Developers, Tech Leads
- **Có thể**: Team leads, Principal engineers
- **Không phải**: Junior developers, business analysts (họ viết PRD/BRD)

## Khi nào viết SDD?

```
Timeline: BRD → PRD → SDD → Code → Testing
           ↓      ↓      ↓     ↓
         Lợi ích Tính   Thiết Code
         kinh doanh  năng  kế  kỹ thuật
```

**SDD viết TRƯỚC khi code**, thường sau khi PRD đã được approve.

---

## 13 Sections của SDD

SDD hoàn chỉnh bao gồm 13 phần chính:

### 1. **Introduction & Purpose** (Giới thiệu & Mục đích)
   - Mục tiêu tài liệu
   - Scope (phạm vi)
   - Audience (đối tượng đọc)
   - Document history

### 2. **System Overview** (Tổng quan hệ thống)
   - High-level description
   - Business context
   - Key features summary

### 3. **Design Considerations** (Các xem xét thiết kế)
   - Constraints (ràng buộc kỹ thuật, tiền, thời gian)
   - Assumptions (giả định)
   - Limitations (hạn chế)

### 4. **Architecture Design** (Thiết kế kiến trúc)
   - Overall architecture pattern (monolithic, microservices, serverless, etc.)
   - Architecture diagram
   - Component overview

### 5. **High-Level Design (HLD)** (Thiết kế cấp cao)
   - Main modules/components
   - Data flow between components
   - External system integrations
   - System interactions diagram

### 6. **Low-Level Design (LLD)** (Thiết kế cấp thấp)
   - Class diagrams (OOP)
   - Function/method specifications
   - Algorithm descriptions
   - Code structure

### 7. **Data Design** (Thiết kế dữ liệu)
   - Database schema (Entity-Relationship Diagram)
   - Data models
   - Data validation rules
   - Data flow

### 8. **Interface Design** (Thiết kế giao diện)
   - API specifications (REST, GraphQL, gRPC)
   - API endpoints
   - Request/Response formats
   - Error codes
   - UI/UX design (nếu có frontend)

### 9. **Security Design** (Thiết kế bảo mật)
   - Authentication & Authorization (who & what)
   - Encryption (data in transit, at rest)
   - Vulnerability assessment
   - Security protocols

### 10. **Performance & Scalability** (Hiệu suất & Khả năng mở rộng)
   - Performance targets (response time, throughput)
   - Scalability strategy (horizontal/vertical)
   - Caching strategy
   - Load balancing

### 11. **Error Handling & Logging** (Xử lý lỗi & Ghi log)
   - Exception handling strategy
   - Logging levels & formats
   - Monitoring & alerting
   - Debugging approach

### 12. **Deployment & DevOps** (Triển khai & DevOps)
   - Deployment architecture (AWS, GCP, Kubernetes, etc.)
   - CI/CD pipeline
   - Environment setup (dev, staging, production)
   - Rollback strategy

### 13. **Appendix** (Phụ lục)
   - Glossary (thuật ngữ)
   - References (tài liệu tham khảo)
   - FAQ
   - Related documents links

---

## Phân biệt: SDD vs PRD vs BRD vs TDD

| Tiêu chí | BRD | PRD | SDD | TDD |
|----------|-----|-----|-----|-----|
| **Mục đích** | Lợi ích kinh doanh | Tính năng chi tiết | Thiết kế kỹ thuật | Kiểm thử |
| **Viết bởi** | Business Analyst | Product Manager | Architect/Tech Lead | QA/Test Engineer |
| **Đọc bởi** | Stakeholders, PMs | PMs, Designers, Devs | Developers, Devs | QA, Developers |
| **Độ sâu** | Tổng quan | Trung bình | Sâu (code-level) | Chi tiết test cases |
| **Nội dung** | Tại sao, lợi ích, khoản đầu tư | Cái gì, khi nào, ai dùng | Làm sao, architecture, design | Làm cách nào để kiểm chứng |
| **Ví dụ** | "Tăng doanh thu 30%" | "User có thể login bằng Google" | "OAuth2 flow, JWT tokens, PostgreSQL" | "Test case: Login with Google should return JWT" |

---

## Workflow: BRD → PRD → SDD → Code

```
1. BRD (Business Requirements Document)
   ├─ Tại sao? Lợi ích kinh doanh
   ├─ Ai? Stakeholders, C-level
   └─ Câu hỏi: Chúng ta nên làm gì? Tại sao?

2. PRD (Product Requirements Document)
   ├─ Cái gì? Các tính năng chi tiết
   ├─ Ai dùng? User personas, use cases
   ├─ Khi nào? Timeline, milestones
   └─ Câu hỏi: Chúng ta sẽ xây dựng những gì?

3. SDD (Software Design Document)
   ├─ Làm sao? Thiết kế kỹ thuật chi tiết
   ├─ Ai viết? Architects, Developers
   └─ Câu hỏi: Chúng ta sẽ code nó như thế nào?

4. CODE (Implementation)
   ├─ Developers viết code
   ├─ Follow SDD guidelines
   └─ Result: Working software

5. TESTING (Quality Assurance)
   ├─ QA kiểm thử theo TDD
   ├─ Verify requirements từ PRD
   └─ Result: Bug-free product
```

---

## Tips viết SDD tốt

### 1. **Clarity (Rõ ràng)**
   - Dùng ngôn ngữ đơn giản, tránh jargon phức tạp
   - Một ý trong một câu
   - Ví dụ cụ thể thay vì mô tả trừu tượng

### 2. **Completeness (Đầy đủ)**
   - Đừng bỏ sót chi tiết quan trọng
   - Include error cases, edge cases
   - Specify constraints & assumptions rõ ràng

### 3. **Consistency (Nhất quán)**
   - Dùng cùng terminology trong toàn tài liệu
   - Format giống nhau cho tất cả diagrams
   - Naming conventions nhất quán

### 4. **Visual Communication (Giao tiếp hình ảnh)**
   - Dùng diagrams (architecture, sequence, ER, flow)
   - Diagrams giải thích 1000 words
   - Tools: Draw.io, Miro, Lucidchart

### 5. **Keep it Code-Ready (Sẵn sàng code)**
   - Chi tiết đủ để developers code ngay
   - API specs cần complete (endpoints, methods, payloads)
   - Database schema cần exact (table names, columns, types)

### 6. **Version Control**
   - Track changes (v1.0, v1.1, etc.)
   - Maintain document history
   - Comment on major changes

### 7. **Review & Approval**
   - SDD cần được review bởi:
     - Tech lead/Architect
     - Senior developers
     - DevOps (nếu có deployment specs)
   - Sign-off trước khi code

### 8. **Living Document**
   - Update khi thiết kế thay đổi
   - Không được out-of-sync với code
   - Regular review (mỗi sprint hoặc mỗi milestone)

---

## Cách sử dụng Templates

### Với dự án nhỏ (< 10 developers):
→ Dùng **SDD-Full-Template.md**, bỏ các sections không cần

### Với dự án lớn (> 10 developers):
→ Dùng **SDD-Full-Template.md** FULL 13 sections

### Nếu chỉ cần HLD:
→ Dùng **HLD-Template.md** (standalone)

### Nếu chỉ cần LLD:
→ Dùng **LLD-Template.md** (standalone)

### Cho Architecture Decisions:
→ Dùng **ADR-Template.md** (thường 3-5 ADRs per SDD)

---

## Lưu ý quan trọng

⚠️ **SDD không phải là:**
- Mã code (đó là code!)
- User manual (đó là documentation)
- Marketing material (đó là PRD)

✅ **SDD là:**
- Bản thiết kế kỹ thuật CHI TIẾT
- Hướng dẫn cho developers code
- Tài liệu reference cho maintenance

---

## Tài liệu liên quan

- SDD-Full-Template.md - Template đầy đủ
- HLD-Template.md - Thiết kế cấp cao
- LLD-Template.md - Thiết kế cấp thấp
- ADR-Template.md - Architecture Decision Records

---

## Tổng kết

| Giai đoạn | Tài liệu | Ai | Mục đích |
|-----------|----------|----|---------|
| Planning | BRD | Business Analyst | Tại sao? Lợi ích? |
| Design | PRD | Product Manager | Cái gì? Ai dùng? |
| Architecture | SDD | Tech Lead/Architect | Làm sao? Chi tiết kỹ thuật |
| Development | Code | Developers | Implement theo SDD |
| Verification | TDD | QA Engineer | Kiểm chứng đúng không? |

Hãy viết SDD chi tiết, rõ ràng, và đầy đủ. Nó là khoảng cách cầu nối giữa thiết kế và code!
