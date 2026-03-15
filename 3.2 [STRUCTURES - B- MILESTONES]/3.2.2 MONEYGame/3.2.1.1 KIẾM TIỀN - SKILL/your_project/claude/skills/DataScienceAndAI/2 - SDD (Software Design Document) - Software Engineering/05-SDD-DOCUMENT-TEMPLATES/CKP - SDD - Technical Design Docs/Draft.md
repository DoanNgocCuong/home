Trong Software Engineering, có nhiều loại tài liệu khác nhau phục vụ cho các giai đoạn và mục đích khác nhau của dự án. Tôi sẽ phân loại chúng thành các nhóm chính:

  

1. *Tài liệu Yêu cầu (Requirements Documentation)*

- Business Requirements Document (BRD)

- Software Requirements Specification (SRS)

- User Requirements Document (URD)

- Use Case Document

- User Stories

- Product Backlog

  

2. *Tài liệu Thiết kế (Design Documentation)*

- System Design Document (SDD)

- High-Level Design (HLD)

- Low-Level Design (LLD)

- Database Design Document

- API Design Document

- UI/UX Design Specification

- Architecture Design Document

  

3. *Tài liệu Kỹ thuật (Technical Documentation)*

- Technical Specification

- Code Documentation

- API Documentation

- Database Documentation

- Configuration Guide

- Deployment Guide

- Integration Guide

  

4. *Tài liệu Kiểm thử (Testing Documentation)*

- Test Plan

- Test Cases

- Test Scripts

- Test Reports

- Bug Reports

- Test Strategy Document

- Quality Assurance Plan

  

5. *Tài liệu Người dùng (User Documentation)*

- User Manual

- User Guide

- Installation Guide

- Quick Start Guide

- FAQ Document

- Help Documentation

- Release Notes

  

6. *Tài liệu Quản lý Dự án (Project Management Documentation)*

- Project Plan

- Project Charter

- Risk Management Plan

- Change Management Plan

- Status Reports

- Meeting Minutes

- Project Timeline

  

7. *Tài liệu Vận hành (Operations Documentation)*

- Operations Manual

- Maintenance Guide

- Disaster Recovery Plan

- Security Documentation

- Backup and Recovery Procedures

- Standard Operating Procedures (SOPs)

  

8. *Tài liệu Quy trình (Process Documentation)*

- Development Process Guide

- Coding Standards

- Version Control Guidelines

- Review Guidelines

- Release Process Document

- CI/CD Pipeline Documentation

  

9. *Tài liệu Pháp lý (Legal Documentation)*

- License Agreements

- Terms of Service

- Privacy Policy

- Service Level Agreements (SLAs)

- Compliance Documents

- Security Policies

  

10. *Tài liệu Bảo trì (Maintenance Documentation)*

- Change Log

- Version History

- Maintenance Records

- Update Procedures

- Troubleshooting Guide

- System Recovery Guide

  

11. *Tài liệu Đánh giá (Review Documentation)*

- Code Review Reports

- Performance Review Documents

- Security Audit Reports

- Quality Assessment Reports

- Post-mortem Reports

  

12. *Tài liệu Kiến trúc (Architecture Documentation)*

- System Architecture Document

- Infrastructure Design

- Network Architecture

- Security Architecture

- Integration Architecture

- Data Flow Diagrams

  

Mỗi loại tài liệu này phục vụ một mục đích cụ thể và có thể được điều chỉnh theo:

- Quy mô dự án

- Phương pháp phát triển (Agile, Waterfall, etc.)

- Yêu cầu của khách hàng

- Tiêu chuẩn ngành

- Quy định của tổ chức

  

Việc lựa chọn và sử dụng các loại tài liệu phù hợp sẽ giúp:

- Quản lý dự án hiệu quả

- Đảm bảo chất lượng sản phẩm

- Dễ dàng bảo trì và nâng cấp

- Thuận lợi trong việc chuyển giao và đào tạo

- Tuân thủ các tiêu chuẩn và quy định

  

  

  

  

---


Để trả lời câu hỏi của bạn theo nguyên tắc **MECE** (Không trùng lặp - Không bỏ sót) và xếp theo **thứ tự thời gian/độ chi tiết** (từ bao quát đến cụ thể), đây là bản đồ toàn diện các loại tài liệu thiết kế trong quy trình phát triển phần mềm chuẩn Big Tech:

Thứ tự được sắp xếp theo dòng chảy: **Business $\to$ Architecture $\to$ Detail Code**.

---

## 1. Giai đoạn Concept & Yêu cầu (The "WHY" & "WHAT")

_Trước khi vẽ bất kỳ thiết kế kỹ thuật nào, cần xác định hệ thống làm gì._

- **PRD (Product Requirement Document)**: Tài liệu yêu cầu sản phẩm.
    
    - _Nội dung:_ User stories, tính năng, logic nghiệp vụ, giao diện (Wireframe).
        
    - _Đối tượng:_ PM, PO, Stakeholder.
        
- **SRS (Software Requirements Specification)**: Đặc tả yêu cầu phần mềm.
    
    - _Nội dung:_ Yêu cầu phi chức năng (Performance, Security), yêu cầu chức năng chi tiết hơn PRD.
        
    - _Đối tượng:_ BA, SA (System Architect).
        

---

## 2. Giai đoạn Kiến trúc Tổng thể (The "WHERE")

_Nhìn hệ thống từ độ cao 10.000 mét. Định hình khung xương._

- **HLD (High-Level Design) / System Architecture Document (SAD)**:
    
    - _Nội dung:_ Sơ đồ khối (Block Diagram), Kiến trúc hệ thống (Microservices vs Monolith), Công nghệ sử dụng (Tech Stack), Luồng dữ liệu chính (Data Flow).
        
    - _Mục tiêu:_ Các thành phần nói chuyện với nhau thế nào? (Frontend $\leftrightarrow$ API Gateway $\leftrightarrow$ Service A $\leftrightarrow$ DB).
        
    - _Đối tượng:_ Architect, Tech Lead.
        

---

## 3. Giai đoạn Thiết kế Kỹ thuật Chi tiết (The "HOW")

_Đây là phần bạn đang quan tâm nhất (TDD, LLD)._

- **TDD (Technical Design Document)**:
    
    - _Vị trí:_ Nằm giữa HLD và LLD. Đôi khi bao trùm cả hai.
        
    - _Nội dung:_ Chiến lược thực thi, Database Schema sơ bộ, API Contract, Class Diagram chính, các thuật toán lõi.
        
    - _Mục tiêu:_ Làm sao để hiện thực hóa HLD?
        
- **LLD (Low-Level Design) / DSD (Detailed System Design)**:
    
    - _Nội dung:_ Chi tiết đến mức Class/Object, Pseudocode (mã giả), Luồng xử lý chi tiết (Sequence Diagram), Error Handling cụ thể từng hàm.
        
    - _Mục tiêu:_ Dev nhìn vào là code được ngay (Ready to code).
        

---

## 4. Giai đoạn Dữ liệu & Giao diện (The "DATA" & "UI")

_Các tài liệu bổ trợ chuyên sâu._

- **DBDD (Database Design Document)**:
    
    - _Nội dung:_ ERD (Entity Relationship Diagram), Indexing strategy, Partitioning, Caching strategy.
        
- **API Spec (API Specification)**:
    
    - _Nội dung:_ Swagger/OpenAPI file, định nghĩa Request/Response, Error codes.
        
- **IDD (Interface Design Document)**:
    
    - _Nội dung:_ Giao thức giao tiếp giữa các module (Internal) hoặc với bên thứ 3 (External).
        

---

## 5. TỔNG HỢP & XẾP HẠNG (MECE VIEW)

Nếu chia theo **mức độ chi tiết (Granularity)**, ta có 3 tầng chính không trùng lặp:

|Tầng (Level)|Tên tài liệu đại diện|Nội dung cốt lõi|Câu hỏi trả lời|
|---|---|---|---|
|**Level 1: Concept**|**PRD / SRS**|Business Logic, Features|**Làm cái gì?** (What)|
|**Level 2: Architecture**|**HLD / SAD**|System Components, Tech Stack|**Hệ thống trông thế nào?** (Where)|
|**Level 3: Implementation**|**LLD / TDD**|Classes, Functions, Algorithms|**Code như thế nào?** (How)|

## ⚠️ Lưu ý về thuật ngữ "TDD"

Trong thực tế, **TDD** là từ dễ gây nhầm lẫn nhất:

1. **Test-Driven Development:** Phương pháp code (Viết test trước khi code).
    
2. **Technical Design Document:** Tài liệu thiết kế kỹ thuật (như ngữ cảnh bạn đang dùng).
    

Ở các công ty lớn (Google/Facebook), họ thường gộp HLD và LLD vào một file duy nhất gọi là **Design Doc** (chính là template TDD bạn đang làm), có phần _Overview_ (HLD) và phần _Detailed Design_ (LLD).

**Kết luận:**  
Tài liệu chi tiết hơn cái TDD (nếu TDD của bạn đang ở mức HLD) chính xác là **LLD (Low-Level Design)**.

---

Các bản “design doc” trong Software Engineering thường được chia thành vài tầng rõ ràng, đi từ business → kiến trúc → chi tiết triển khai.altexsoft+1​

## Ba level chính (MECE, từ trên xuống)

|Level|Tài liệu đại diện|Câu hỏi chính|Độ chi tiết|
|---|---|---|---|
|Level 1|PRD, SRS, BRD/FRD|Hệ thống cần làm gì?|Mô tả yêu cầu, hành vi mong đợi, constraint nghiệp vụ. altexsoft+1​|
|Level 2|HLD / System Architecture / SDD|Hệ thống trông như thế nào? Các khối nói chuyện với nhau ra sao?|Kiến trúc, module, data flow, interface ở mức macro. geeksforgeeks+1​|
|Level 3|LLD / Detailed Design / Module Design Spec / Technical Design Doc|Code như thế nào? Logic cụ thể ra sao?|Class, hàm, thuật toán, schema chi tiết, pseudo-code. geeksforgeeks+1​|

## Tên gọi phổ biến theo thứ tự

1. Tầng yêu cầu (trước khi design kỹ thuật):
    
    - BRD / MRD / PRD (Business/Product Requirement Document).modernanalyst+1​
        
    - SRS (Software Requirement Specification).testfort+1​
        
2. Tầng kiến trúc (High-Level Design):
    
    - HLD (High-Level Design) hoặc High-Level Solution Design.geeksforgeeks+1​
        
    - System Architecture Document / System Design Document (SDD).scribd+1​
        
3. Tầng thiết kế chi tiết (Low-Level/Technical Design):
    
    - LLD (Low-Level Design) hoặc Detailed System Design (DLD).huspi+1​
        
    - Technical Design Document / Module Design Specification cho từng module.geeksforgeeks+1​
        

## Gợi ý mapping với case của bạn

- Tài liệu TDD hiện tại của bạn đang nằm giữa HLD và LLD: có cả overview kiến trúc lẫn chi tiết module.geeksforgeeks+1​
    
- Nếu muốn làm bản “chi tiết hơn TDD cho từng module”, tên hợp lý là:
    
    - “Module X – Low-Level Design (LLD)” hoặc
        
    - “Module X – Technical Design & Deep-Dive Spec” để rõ đây là source of truth chi tiết cho implementation.santhalakshminarayana.github+1​
        

1. [https://www.altexsoft.com/blog/technical-documentation-in-software-development-types-best-practices-and-tools/](https://www.altexsoft.com/blog/technical-documentation-in-software-development-types-best-practices-and-tools/)
2. [https://en.wikipedia.org/wiki/Software_documentation](https://en.wikipedia.org/wiki/Software_documentation)
3. [https://www.modernanalyst.com/Resources/Articles/tabid/115/ID/5464/9-Types-Of-Requirements-Documents-What-They-Mean-And-Who-Writes-Them.aspx](https://www.modernanalyst.com/Resources/Articles/tabid/115/ID/5464/9-Types-Of-Requirements-Documents-What-They-Mean-And-Who-Writes-Them.aspx)
4. [https://www.geeksforgeeks.org/system-design/difference-between-high-level-design-and-low-level-design/](https://www.geeksforgeeks.org/system-design/difference-between-high-level-design-and-low-level-design/)
5. [https://www.geeksforgeeks.org/software-engineering/design-documentation-in-software-engineering/](https://www.geeksforgeeks.org/software-engineering/design-documentation-in-software-engineering/)
6. [https://www.kutztown.edu/Departments-Offices/A-F/ComputerScienceInformationTechnology/Documents/Student%20Resources/DocumentationLevels.pdf](https://www.kutztown.edu/Departments-Offices/A-F/ComputerScienceInformationTechnology/Documents/Student%20Resources/DocumentationLevels.pdf)
7. [https://testfort.com/blog/important-software-testing-documentation-srs-frs-and-brs](https://testfort.com/blog/important-software-testing-documentation-srs-frs-and-brs)
8. [https://softwaredominos.com/home/software-design-development-articles/high-level-solution-design-documents-what-is-it-and-when-do-you-need-one/](https://softwaredominos.com/home/software-design-development-articles/high-level-solution-design-documents-what-is-it-and-when-do-you-need-one/)
9. [https://www.scribd.com/document/833415214/1-SDLC](https://www.scribd.com/document/833415214/1-SDLC)
10. [https://huspi.com/blog-open/what-the-differences-lld-hld-dld/](https://huspi.com/blog-open/what-the-differences-lld-hld-dld/)
11. [https://www.docuwriter.ai/posts/example-of-software-design-document](https://www.docuwriter.ai/posts/example-of-software-design-document)
12. [https://www.geeksforgeeks.org/system-design/getting-started-with-system-design/](https://www.geeksforgeeks.org/system-design/getting-started-with-system-design/)
13. [https://santhalakshminarayana.github.io/blog/software-development-comprehensive-guide](https://santhalakshminarayana.github.io/blog/software-development-comprehensive-guide)
14. [https://www.perplexity.ai/search/hoan-thien-chi-tiet-giup-to-ta-Rtx6iAThQKiWlytVv.skVg](https://www.perplexity.ai/search/hoan-thien-chi-tiet-giup-to-ta-Rtx6iAThQKiWlytVv.skVg)
15. [https://testrigor.com/blog/high-level-design-hld-vs-low-level-design-lld/](https://testrigor.com/blog/high-level-design-hld-vs-low-level-design-lld/)
16. [https://www.coudo.ai/blog/hld-vs-lld-best-practices-for-successful-technical-design](https://www.coudo.ai/blog/hld-vs-lld-best-practices-for-successful-technical-design)
17. [https://odysseyinc.com/low-level-design-vs-high-level-design-key-differences-and-why-they-matter-in-custom-software/](https://odysseyinc.com/low-level-design-vs-high-level-design-key-differences-and-why-they-matter-in-custom-software/)
18. [https://orhanergun.net/high-level-design-vs-low-level-design-understanding-the-key-differences](https://orhanergun.net/high-level-design-vs-low-level-design-understanding-the-key-differences)
19. [https://www.systemdesignhandbook.com/answers/what-is-low-level-system-design/](https://www.systemdesignhandbook.com/answers/what-is-low-level-system-design/)
20. [https://www.sdlcforms.com/UnderstandingSDLC.html](https://www.sdlcforms.com/UnderstandingSDLC.html)
21. [https://www.linkedin.com/posts/ashsau_high-level-design-hld-vs-low-level-design-activity-7325101947005345794-pss7](https://www.linkedin.com/posts/ashsau_high-level-design-hld-vs-low-level-design-activity-7325101947005345794-pss7)