
# FinAI Agent - High Level Design (HLD) v1.0

**Production Quality Standard | Version 1.0**

**Document Status:** Final - Production Ready  
**Last Updated:** December 2025  
**Target Audience:** Development Team, Architects, Tech Leads, Product Managers, Stakeholders

---

## PHẦN A: HIGH LEVEL DESIGN

### Executive Summary

Tài liệu Thiết kế Cấp cao (HLD) này mô tả kiến trúc toàn diện của hệ thống **finAI Finance Agent Web Browser**, một ứng dụng AI-native được thiết kế để tự động hóa quy trình nghiên cứu tài chính. Hệ thống kết hợp các công nghệ hiện đại như microservices, event-driven architecture, multi-agent systems, và Model Context Protocol (MCP) để tạo ra một nền tảng mạnh mẽ, có khả năng mở rộng cao và sẵn sàng cho doanh nghiệp.

Kiến trúc được xây dựng trên 4 lớp rõ ràng (Governance, Perception, Cognition, Action), mỗi lớp chịu trách nhiệm cho một tập hợp các mối quan tâm cụ thể. Cách tiếp cận này đảm bảo tính module hóa, khả năng kiểm thử, và dễ dàng bảo trì trong suốt vòng đời của sản phẩm.

---

## 1. System Architecture Overview

Hệ thống finAI Finance Agent Web Browser được thiết kế theo kiến trúc microservices, hướng sự kiện (event-driven) và áp dụng các nguyên tắc của Domain-Driven Design (DDD). Kiến trúc này được xây dựng trên một nền tảng 4 lớp (4-Layer MECE Framework) để đảm bảo tính module hóa, khả năng mở rộng và bảo trì. Mô hình này được lấy cảm hứng từ các kiến trúc thành công của các công ty công nghệ lớn và được điều chỉnh để phù hợp với bối cảnh cụ thể của ứng dụng tài chính.

### 1.1. 4-Layer MECE Framework

Kiến trúc 4 lớp được thiết kế để phân tách các mối quan tâm (separation of concerns) một cách rõ ràng. Mỗi lớp có trách nhiệm cụ thể và giao tiếp với các lớp khác thông qua các giao diện được xác định rõ ràng:

**Layer 4: Governance (Safety & Human Control)** là lớp trên cùng, chịu trách nhiệm về an toàn, kiểm soát và tuân thủ. Bao gồm các cơ chế như Guardrails (URL whitelist, PII detection), Human-in-the-Loop (HITL) cho các quyết định quan trọng và ghi log kiểm toán (audit logs). Lớp này hoạt động như một bộ lọc cuối cùng, đảm bảo rằng không có dữ liệu nhạy cảm hoặc hành động không an toàn nào được thực hiện.

**Layer 3: Action (Browser Control & Execution)** là lớp thực thi, chịu trách nhiệm tương tác với môi trường bên ngoài, chủ yếu là trình duyệt web. Lớp này bao gồm Tool Registry, Playwright Controller để điều khiển trình duyệt và các công cụ tài chính chuyên dụng. Nó cung cấp các công cụ cơ bản mà các agent có thể sử dụng để thực hiện các tác vụ.

**Layer 2: Cognition (Agent Brain - LangGraph Core)** là lõi của hệ thống, nơi các agent AI hoạt động. Lớp này sử dụng LangGraph để điều phối một hệ thống đa agent, quản lý bộ nhớ (ngắn hạn và dài hạn) và định tuyến các yêu cầu đến các mô hình ngôn ngữ lớn (LLM) khác nhau. Đây là nơi xảy ra hầu hết logic quyết định và lập kế hoạch.

**Layer 1: Perception (Browser State Awareness)** là lớp nhận thức, chịu trách nhiệm thu thập và hiểu trạng thái của trình duyệt và các nguồn dữ liệu khác. Lớp này xử lý đầu vào ngôn ngữ tự nhiên, phân tích cây trợ năng (Accessibility Tree) và theo dõi các thay đổi trong DOM. Nó biến các đầu vào thô thành các biểu diễn có cấu trúc mà các agent có thể hiểu.

### 1.2. Multi-Agent Pattern

Để tăng tính linh hoạt và khả năng mở rộng, hệ thống áp dụng mô hình đa agent thay vì một luồng ReAct tuần tự. Các agent chuyên biệt giao tiếp với nhau thông qua một MessageBus (Redis Pub/Sub), cho phép xử lý song song và dễ dàng mở rộng. Mô hình này cho phép các agent hoạt động độc lập, mỗi agent chuyên biệt trong một lĩnh vực cụ thể.

Các agent chính bao gồm:

**Chief Agent (Coordinator)** là điều phối viên chính, nhận yêu cầu từ lớp Perception và phân phối nhiệm vụ cho các agent khác. Nó không thực hiện công việc nặng nề mà chỉ điều phối luồng công việc.

**Planner Agent** lập kế hoạch chi tiết cho các nhiệm vụ. Nó phân tích yêu cầu tài chính, xác định các bước cần thiết, các URL cần truy cập, và các dữ liệu cần trích xuất.

**Navigator Agent** điều khiển trình duyệt và thu thập dữ liệu. Nó sử dụng Playwright để điều hướng đến các trang web, tương tác với các phần tử trên trang, và thu thập nội dung.

**Extractor Agent** trích xuất thông tin từ dữ liệu thu thập được. Nó sử dụng LLM hoặc các công cụ trích xuất có cấu trúc để tách ra các chỉ số tài chính, bảng dữ liệu, và các thông tin quan trọng khác.

**Verifier Agent** xác minh tính chính xác và đầy đủ của dữ liệu. Nó kiểm tra xem dữ liệu có đáp ứng các tiêu chí chất lượng hay không, và nếu cần, yêu cầu re-navigation để thu thập thêm dữ liệu.

**Synthesizer Agent** tổng hợp kết quả và tạo báo cáo cuối cùng. Nó kết hợp tất cả dữ liệu đã trích xuất và xác minh thành một báo cáo toàn diện với các nguồn tham chiếu.

---

## 2. Modules / Components & Data Flow

Kiến trúc hệ thống được chia thành các module và component chính, tương ứng với 4 lớp kiến trúc. Luồng dữ liệu (data flow) di chuyển tuần tự qua các lớp này, với các agent trong Lớp 2 giao tiếp bất đồng bộ. Thiết kế này cho phép các phần khác nhau của hệ thống hoạt động độc lập nhưng vẫn được phối hợp chặt chẽ.

### 2.1. Key Components

**Layer 0: Governance** bao gồm ba thành phần chính. **Input Gate** thực hiện rate limiting, kiểm tra an toàn và xác thực đầu vào. Nó đảm bảo rằng chỉ các yêu cầu hợp lệ mới được xử lý. **In-Flight Guards** giám sát các hành vi bất thường trong quá trình thực thi, ví dụ như các vòng lặp điều hướng vô tận. **Output Gate** xác thực và kiểm tra chất lượng kết quả đầu ra trước khi trả về cho người dùng.

**Layer 1: Perception** bao gồm ba thành phần chính. **Input Processor** chuẩn hóa và phân loại truy vấn của người dùng, chuyển đổi chúng thành một định dạng tiêu chuẩn. **Entity Extractor** trích xuất các thực thể tài chính (ví dụ: tên công ty, mã cổ phiếu) từ truy vấn. **Context Builder** xây dựng ngữ cảnh cho truy vấn, bao gồm lịch sử hội thoại và bối cảnh thị trường.

**Layer 2: Cognition** bao gồm ba thành phần chính. **Multi-Agent System** bao gồm các agent chuyên biệt (Chief, Planner, Navigator, Extractor, Verifier, Synthesizer) hoạt động độc lập. **MessageBus (Redis Pub/Sub)** là kênh giao tiếp chính cho các agent, cho phép giao tiếp hướng sự kiện và bất đồng bộ. **MCPToolAdapter** là một adapter để chuẩn hóa việc gọi các công cụ (tools) thông qua Model Context Protocol (MCP), giúp tách biệt agent khỏi việc triển khai công cụ cụ thể.

**Layer 3: Action** bao gồm ba thành phần chính. **PlaywrightController & BrowserPool** quản lý và điều khiển các phiên trình duyệt. **FinancialDataExtractor** là công cụ chuyên dụng để trích xuất các chỉ số tài chính từ các trang web. **MCP Servers** là các server triển khai MCP (ví dụ: `BrowserMCPServer`, `FinancialMCPServer`) để đóng gói các công cụ cơ bản.

### 2.2. Data Flow

Luồng dữ liệu end-to-end được minh họa như sau:

```
[User Request]
    ↓
┌──────────────────────────────┐
│ Layer 0: Governance          │
│ (Input Gate, Guards)         │
└──────────┬───────────────────┘
           ↓
┌──────────────────────────────┐
│ Layer 1: Perception          │
│ (Input Processing, Entity    │
│  Extraction, Context)        │
└──────────┬───────────────────┘
           ↓
┌────────────────────────────────────────────────┐
│ Layer 2: Cognition (Multi-Agent Orchestration) │
│                                                │
│  ChiefAgent ──broadcast(task)─→ MessageBus    │
│      ↑                              │         │
│      └───(final_report)─────────────┼────────┘
│                                     ↓         
│  ┌──────────────┐  ┌──────────────┐          
│  │PlannerAgent  │  │NavigatorAgent│ ...      
│  └──────┬───────┘  └──────┬───────┘          
│         ↓ (plan)          ↓ (page_content)   
│     MessageBus ────→ MCPToolAdapter ──→ L3   
└────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────┐
│ Layer 3: Action              │
│ (Browser Tools, Extractors)  │
└──────────┬───────────────────┘
           ↓
[Final Report]
```

Luồng dữ liệu hoạt động như sau:

**Request Initiation:** Người dùng gửi một yêu cầu bằng ngôn ngữ tự nhiên, ví dụ: "Tìm doanh thu hàng năm của Apple trong 5 năm qua".

**Governance & Perception (Layer 0 & 1):** Yêu cầu đi qua các cổng kiểm soát, được xử lý, phân tích và làm giàu ngữ cảnh để tạo thành một `FinancialQuery` có cấu trúc. Ở giai đoạn này, các thực thể như "Apple" và "doanh thu hàng năm" được xác định.

**Cognition (Layer 2):** `ChiefAgent` nhận `FinancialQuery` và phát một sự kiện `task_available` lên `MessageBus`. Tất cả các agent khác đều lắng nghe sự kiện này.

**Agent Collaboration:** Các agent bắt đầu làm việc theo thứ tự được xác định. `PlannerAgent` nhận nhiệm vụ, tạo kế hoạch chi tiết (ví dụ: truy cập trang web SEC, tìm các báo cáo 10-K, trích xuất doanh thu) và phát sự kiện `plan_ready`. `NavigatorAgent` nhận kế hoạch, sử dụng `MCPToolAdapter` để gọi công cụ trình duyệt trong **Layer 3**, sau đó phát sự kiện `page_ready` chứa nội dung trang web. `ExtractorAgent` nhận nội dung trang, trích xuất dữ liệu và phát `data_extracted`. `VerifierAgent` xác minh dữ liệu và phát `verification_done`. `SynthesizerAgent` nhận dữ liệu đã xác minh, tổng hợp báo cáo và phát `final_report`.

**Result Delivery:** `ChiefAgent` nhận `final_report` và gửi nó qua **Layer 0** để kiểm tra lần cuối trước khi trả về cho người dùng.

---

## 3. Data & Database Design (Conceptual)

Thiết kế dữ liệu ở mức cao tập trung vào việc lựa chọn các kho lưu trữ dữ liệu (data stores) phù hợp và xác định mô hình dữ liệu khái niệm. Hệ thống sử dụng một cách tiếp cận đa kho (polyglot persistence) để tối ưu hóa cho các loại dữ liệu và trường hợp sử dụng khác nhau.

### 3.1. Data Stores

| Data Store      | Type                | Primary Use Case                                                                                                  | Rationale                                                                                             |
|-----------------|---------------------|-------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **PostgreSQL**  | Relational (RDBMS)  | Lưu trữ dữ liệu có cấu trúc cốt lõi: thông tin người dùng, lịch sử tác vụ, kết quả đã xử lý, và audit logs.          | Đảm bảo tính toàn vẹn dữ liệu (ACID), hỗ trợ các truy vấn phức tạp và các mối quan hệ dữ liệu.         |
| **Redis**       | In-Memory Key-Value | **1. Message Bus:** Giao tiếp bất đồng bộ giữa các agent qua cơ chế Pub/Sub.<br>**2. Short-term Memory:** Lưu trữ trạng thái và dữ liệu tạm thời của agent trong một phiên làm việc. | Tốc độ truy cập cực nhanh, độ trễ thấp, lý tưởng cho việc caching và giao tiếp thời gian thực.        |
| **Pinecone**    | Vector Database     | **Long-term Memory (RAG):** Lưu trữ các vector embedding của các tài liệu và kết quả trước đó để thực hiện Retrieval-Augmented Generation. | Tối ưu hóa cho việc tìm kiếm tương đồng (similarity search) ở quy mô lớn, cần thiết cho các tác vụ RAG. |
| **Kafka**       | Event Stream        | Thu thập và xử lý các sự kiện hệ thống, logs, và dữ liệu phân tích (analytics) ở thông lượng cao.                  | Khả năng chịu lỗi cao, xử lý luồng dữ liệu lớn, tách biệt hệ thống agent khỏi các hệ thống phụ trợ (ví dụ: analytics pipeline). |

### 3.2. Conceptual Data Model

Mô hình dữ liệu khái niệm tập trung vào các thực thể chính của hệ thống:

**User** lưu trữ thông tin tài khoản, quyền hạn và các cài đặt của người dùng. Mỗi người dùng có một ID duy nhất, email, và các quyền truy cập cụ thể.

**FinancialQuery** đại diện cho một yêu cầu nghiên cứu của người dùng, bao gồm truy vấn gốc, các thực thể được trích xuất và ngữ cảnh liên quan. Nó là điểm khởi đầu của mỗi quy trình xử lý.

**AgentTask** là một tác vụ cụ thể được tạo ra từ một `FinancialQuery`, theo dõi trạng thái thực thi của hệ thống agent. Nó ghi lại từng bước của quá trình xử lý.

**TaskResult** lưu trữ kết quả cuối cùng của một `AgentTask`, bao gồm báo cáo tổng hợp, dữ liệu đã trích xuất và các nguồn tham chiếu. Nó là kết quả cuối cùng được trả về cho người dùng.

**AuditLog** ghi lại các hành động quan trọng của hệ thống và người dùng để phục vụ cho việc kiểm toán và tuân thủ. Mỗi mục nhập bao gồm dấu thời gian, người dùng, hành động, và kết quả.

### 3.3. Data Consistency

Hệ thống áp dụng một mô hình nhất quán hỗn hợp:

**Strong Consistency (ACID)** được đảm bảo bởi **PostgreSQL** cho các hoạt động quan trọng như tạo tài khoản, ghi nhận kết quả cuối cùng và các giao dịch tài chính (nếu có trong tương lai). Điều này đảm bảo dữ liệu cốt lõi luôn chính xác và toàn vẹn.

**Eventual Consistency** được chấp nhận trong hệ thống agent và các luồng dữ liệu bất đồng bộ qua **Redis** và **Kafka**. Dữ liệu có thể có độ trễ nhỏ để đồng bộ giữa các agent, nhưng điều này cho phép hệ thống đạt được độ trễ thấp và khả năng mở rộng cao.

---

## 4. Interfaces & Integrations (API, External Systems)

Hệ thống finAI tương tác với cả người dùng cuối và các dịch vụ bên ngoài thông qua một tập hợp các giao diện (interfaces) và điểm tích hợp (integrations) được xác định rõ ràng.

### 4.1. Internal Interfaces

**FastAPI REST API** là giao diện chính (public-facing) cho phép client (ví dụ: browser extension) tương tác với backend. API này cung cấp các endpoint để xác thực người dùng, gửi các yêu cầu nghiên cứu tài chính mới, truy xuất lịch sử và kết quả của các yêu cầu trước đó, và quản lý tài khoản và cài đặt người dùng. API được bảo vệ bằng JWT tokens và rate limiting.

**Model Context Protocol (MCP)** là một giao diện nội bộ quan trọng, đóng vai trò là một lớp trừu tượng giữa các agent (Layer 2) và các công cụ (Layer 3). Bằng cách chuẩn hóa giao tiếp công cụ, MCP cho phép tách biệt (Decoupling) giữa các agent và công cụ, khả năng thay thế (Interchangeability) các công cụ mà không cần thay đổi logic của agent, và khả năng kiểm thử (Testability) bằng cách mock các MCP server.

### 4.2. External Integrations

**Large Language Model (LLM) APIs** là các dịch vụ bên ngoài quan trọng. **OpenAI (GPT-4o)** được sử dụng cho các tác vụ đòi hỏi suy luận phức tạp, lập kế hoạch và tổng hợp thông tin. **Google (Gemini Flash)** được sử dụng cho các tác vụ đơn giản hơn, yêu cầu tốc độ nhanh và chi phí thấp, chẳng hạn như phân loại truy vấn hoặc trích xuất thực thể đơn giản. Việc sử dụng một cơ chế định tuyến (routing) giữa các LLM giúp tối ưu hóa giữa hiệu suất, chi phí và khả năng của hệ thống.

**Financial Data APIs (Future Integration)** để đảm bảo tính chính xác và độ tin cậy của dữ liệu, hệ thống được thiết kế để có thể tích hợp với các nhà cung cấp dữ liệu tài chính chuyên nghiệp như **Bloomberg, Refinitiv, hoặc FactSet** trong tương lai. Việc này sẽ giảm sự phụ thuộc vào việc trích xuất dữ liệu từ các trang web công cộng, vốn không ổn định và có thể không chính xác.

**Compliance & Regulatory Systems** hệ thống sẽ cần tích hợp với các hệ thống giám sát tuân thủ nội bộ để đảm bảo mọi hoạt động nghiên cứu đều tuân thủ các quy định của ngành tài chính (ví dụ: SEC, FINRA). Các audit log được tạo ra sẽ được đẩy đến các hệ thống này để lưu trữ và phân tích.

---

## 5. Technology & Deployment Architecture

Kiến trúc công nghệ và triển khai được lựa chọn để đảm bảo hiệu suất, khả năng mở rộng, và tính sẵn sàng cao, phù hợp với một ứng dụng cấp doanh nghiệp.

### 5.1. Technology Stack

| Category                | Technology / Service                                       | Rat               |
|-------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **Backend Framework**   | Python 3.11+, FastAPI                                      | Hiệu suất cao, phát triển nhanh, hệ sinh thái mạnh mẽ cho AI/ML, và hỗ trợ lập trình bất đồng bộ, phù hợp với kiến trúc hướng sự kiện. |
| **Database**            | PostgreSQL, Redis, Pinecone                                | Sử dụng đa kho (polyglot persistence) để tối ưu cho từng loại dữ liệu: quan hệ, cache/thông điệp, và vector.                             |
| **Event Streaming**     | Kafka                                                      | Xử lý các luồng sự kiện lớn, đảm bảo độ bền và khả năng chịu lỗi cho dữ liệu logs và analytics.                                       |
| **AI / Agent Core**     | LangGraph, OpenAI (GPT-4o), Google (Gemini Flash)          | LangGraph cung cấp một framework mạnh mẽ để xây dựng các agent phức tạp. Định tuyến LLM giúp tối ưu hóa chi phí và hiệu suất.             |
| **Browser Automation**  | Playwright                                                 | Cung cấp API mạnh mẽ và ổn định để điều khiển trình duyệt, hỗ trợ nhiều trình duyệt và các kịch bản tương tác phức tạp.                  |
| **Containerization**    | Docker                                                     | Đóng gói các microservice và phụ thuộc của chúng, đảm bảo tính nhất quán giữa các môi trường phát triển, kiểm thử và sản phẩm.         |
| **Orchestration**       | Kubernetes                                                 | Tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container hóa, cung cấp khả năng tự phục hồi và quản lý tài nguyên hiệu quả. |

### 5.2. Deployment Architecture

Kiến trúc triển khai được thiết kế theo mô hình cloud-native, tận dụng các dịch vụ được quản lý để giảm gánh nặng vận hành.

```
+--------------------------------------------------------------------+
|                   End User (Browser Extension)                     |
+--------------------------------------------------------------------+
                   | (HTTPS)
+------------------v-------------------------------------------------+
|              API Gateway (e.g., AWS API Gateway)                    |
|          (Authentication, Rate Limiting, Routing)                  |
+------------------v-------------------------------------------------+
|                      Load Balancer                                 |
+------------------v-------------------------------------------------+
|              Kubernetes Cluster (e.g., EKS, GKE)                    |
|                                                                    |
| +------------------+  +------------------+  +------------------+  |
| | FastAPI Service  |  | FastAPI Service  |  | Agent Workers    |  |
| | (Pod 1)          |  | (Pod 2)          |  | (Pods)           |  |
| +------------------+  +------------------+  +------------------+  |
|         |                   |                   |                   |
|         +---------+---------+---------+---------+                   |
|                   |                   |                             |
| +-----------------v-+ +---------------v---+ +-------------v----+  |
| | PostgreSQL (RDS)  | | Redis (ElastiCache) | | Kafka (MSK)      |  |
| +-------------------+ +-------------------+ +------------------+  |
|                                                                    |
+--------------------------------------------------------------------+
```

**Cloud Provider:** Hệ thống được thiết kế để có thể triển khai trên bất kỳ nhà cung cấp đám mây lớn nào (AWS, GCP, Azure). Điều này đảm bảo tính linh hoạt và giảm rủi ro vendor lock-in.

**API Gateway:** Tất cả các yêu cầu từ client sẽ đi qua một API Gateway. Cổng này chịu trách nhiệm xác thực, giới hạn tốc độ (rate limiting), và định tuyến yêu cầu đến các microservice phù hợp. Nó cũng cung cấp một điểm duy nhất để giám sát và ghi log tất cả các yêu cầu.

**Kubernetes Cluster:** Các microservice (được đóng gói dưới dạng Docker container) sẽ được triển khai và quản lý bởi một Kubernetes cluster. Kubernetes sẽ tự động xử lý việc mở rộng quy mô, cân bằng tải nội bộ và khởi động lại các service bị lỗi. Nó cũng cung cấp các tính năng như rolling updates, canary deployments, và health checks.

**Managed Services:** Để tăng tính ổn định và giảm chi phí vận hành, hệ thống ưu tiên sử dụng các dịch vụ được quản lý cho các thành phần cơ sở dữ liệu và messaging, chẳng hạn như Amazon RDS cho PostgreSQL, Amazon ElastiCache cho Redis, và Amazon MSK cho Kafka. Các dịch vụ này được quản lý bởi nhà cung cấp đám mây, giảm gánh nặng vận hành cho đội ngũ của chúng tôi.

---

## 6. Cross-cutting Concerns: Security & Non-functional Requirements

Các mối quan tâm xuyên suốt (cross-cutting concerns) là những khía cạnh quan trọng ảnh hưởng đến toàn bộ hệ thống. Trong bối cảnh FinAI, bảo mật và các yêu cầu phi chức năng (NFRs) là ưu tiên hàng đầu.

### 6.1. Security Design

Kiến trúc bảo mật được xây dựng theo nguyên tắc "phòng thủ theo chiều sâu" (defense-in-depth) và Zero Trust. Điều này có nghĩa là không có thành phần nào được tin tưởng hoàn toàn; mỗi thành phần phải xác thực và ủy quyền.

**Authentication & Authorization:** Sử dụng tiêu chuẩn **OIDC (OpenID Connect)** để xác thực người dùng, tích hợp với các nhà cung cấp danh tính (Identity Providers) của doanh nghiệp. Sử dụng **JWT (JSON Web Tokens)** để ủy quyền các yêu cầu API sau khi xác thực thành công. Triển khai **RBAC (Role-Based Access Control)** để quản lý quyền truy cập của người dùng vào các tính năng và dữ liệu khác nhau.

**Data Security:** **Encryption in Transit** - Tất cả giao tiếp giữa client, API Gateway, và các microservice nội bộ đều được mã hóa bằng **TLS 1.3**. **Encryption at Rest** - Dữ liệu nhạy cảm trong PostgreSQL và các kho lưu trữ khác được mã hóa ở cấp độ lưu trữ. **PII Detection** - Lớp Governance (Layer 0) bao gồm một cơ chế để phát hiện và che giấu (mask) thông tin nhận dạng cá nhân (PII) trong cả đầu vào và đầu ra, nhằm ngăn chặn rò rỉ dữ liệu nhạy cảm.

**Compliance:** **Audit Logging** - Mọi hành động quan trọng của người dùng và hệ thống đều được ghi lại trong một bảng `AuditLog` bất biến (immutable) trong PostgreSQL. Các logs này rất quan trọng cho việc điều tra sự cố và tuân thủ các quy định của ngành tài chính. **"Research Tool" Positioning** - Sản phẩm được định vị là một công cụ hỗ trợ nghiên cứu, không phải là công cụ tư vấn đầu tư, để giảm thiểu rủi ro pháp lý.

### 6.2. Non-Functional Requirements (NFRs)

Các NFRs xác định các tiêu chuẩn về chất lượng và hiệu suất của hệ thống.

| NFR Category      | Requirement                                     | Metric & Target (Production)                    | Implementation Strategy                                                                                                                            |
|-------------------|-------------------------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Performance**   | **Latency:** Thời gian phản hồi của hệ thống.     | P95 < 3 giây cho mỗi hành động của agent.         | - Sử dụng FastAPI (bất đồng bộ).<br>- Caching với Redis.<br>- Tối ưu hóa các truy vấn cơ sở dữ liệu.<br>- Định tuyến LLM thông minh.                   |
|                   | **Throughput:** Số lượng tác vụ xử lý đồng thời. | Hỗ trợ 50+ tác vụ nghiên cứu/ngày/analyst.       | - Mở rộng quy mô theo chiều ngang (horizontal scaling) của các agent worker trên Kubernetes.<br>- Sử dụng message queue (Kafka) để xử lý tải đột biến. |
| **Availability**  | **Uptime:** Thời gian hệ thống hoạt động.        | SLA 99.9%                                       | - Triển khai trên nhiều Availability Zone (AZ).<br>- Sử dụng Kubernetes để tự động phục hồi.<br>- Sử dụng các dịch vụ được quản lý có SLA cao.      |
| **Scalability**   | **Horizontal Scaling:** Khả năng mở rộng hệ thống. | Có thể tăng gấp 10 lần số lượng người dùng.      | - Kiến trúc Microservices và stateless agent workers.<br>- Sử dụng Kubernetes Horizontal Pod Autoscaler (HPA).<br>- Database có thể được scale (read replicas). |
| **Reliability**   | **Fault Tolerance:** Khả năng chịu lỗi.          | Không mất dữ liệu khi có lỗi thành phần.         | - Sử dụng cơ sở dữ liệu có cơ chế sao lưu (backup) và phục hồi (recovery).<br>- Kafka đảm bảo độ bền của sự kiện.<br>- Các agent có cơ chế thử lại (retry). |
| **Data Accuracy** | **Extraction Accuracy:** Độ chính xác trích xuất. | > 95%                                           | - Sử dụng Verifier Agent để kiểm tra chéo dữ liệu.<br>- Tích hợp với các API dữ liệu tài chính đáng tin cậy (trong tương lai).<br>- Human-in-the-loop. |

---

## 7. Architecture Decision Records (ADRs)

Phần này ghi lại các quyết định kiến trúc quan trọng đã được đưa ra trong quá trình thiết kế hệ thống. Các quyết định này được ghi lại để giúp các nhà phát triển trong tương lai hiểu được lý do đằng sau mỗi lựa chọn.

### ADR-001: Lựa chọn kiến trúc Microservices

**Status:** Accepted

**Context:** Cần lựa chọn một mô hình kiến trúc cho backend có khả năng mở rộng, dễ bảo trì và cho phép các nhóm phát triển độc lập.

**Decision:** Áp dụng kiến trúc Microservices. Mỗi service sẽ chịu trách nhiệm cho một bounded context cụ thể (ví dụ: quản lý người dùng, điều phối agent, xử lý kết quả).

**Consequences:**
- **Pros:** Tăng khả năng mở rộng độc lập của từng thành phần, cho phép các nhóm làm việc song song, dễ dàng áp dụng các công nghệ khác nhau cho từng service.
- **Cons:** Tăng độ phức tạp trong vận hành, đòi hỏi cơ chế service discovery, và tăng chi phí giao tiếp mạng giữa các service.

### ADR-002: Sử dụng Multi-Agent System thay vì ReAct Pattern

**Status:** Accepted

**Context:** Lõi nhận thức (Cognition Layer) cần một mô hình để điều phối các tác vụ AI. ReAct là một lựa chọn đơn giản, nhưng có thể không đủ linh hoạt.

**Decision:** Triển khai một hệ thống đa agent (Multi-Agent System) giao tiếp qua Message Bus (Redis Pub/Sub).

**Consequences:**
- **Pros:** Tăng tính module hóa và chuyên môn hóa của từng agent, cho phép xử lý song song, dễ dàng mở rộng bằng cách thêm các agent mới.
- **Cons:** Phức tạp hơn trong việc điều phối và gỡ lỗi luồng tác vụ so với một chuỗi tuần tự.

### ADR-003: Lựa chọn FastAPI cho Backend Framework

**Status:** Accepted

**Context:** Cần một framework Python cho việc xây dựng các API backend.

**Decision:** Sử dụng FastAPI.

**Consequences:**
- **Pros:** Hiệu suất cao nhờ lập trình bất đồng bộ (asyncio), tự động tạo tài liệu API (OpenAPI), validation dữ liệu mạnh mẽ với Pydantic.
- **Cons:** Hệ sinh thái nhỏ hơn so với Django. Yêu cầu kiến thức về lập trình bất đồng bộ.

### ADR-004: Sử dụng Model Context Protocol (MCP) cho Tool Abstraction

**Status:** Accepted

**Context:** Cần một cách tiêu chuẩn để các agent giao tiếp với các công cụ khác nhau (browser, extractors, v.v.).

**Decision:** Triển khai Model Context Protocol (MCP) như một lớp trừu tượng giữa các agent và công cụ.

**Consequences:**
- **Pros:** Tách biệt agent khỏi chi tiết triển khai công cụ, dễ dàng thay thế hoặc nâng cấp công cụ, dễ dàng kiểm thử bằng cách mock các MCP server.
- **Cons:** Thêm một lớp trừu tượng có thể làm tăng độ trễ nhẹ, cần phải duy trì MCP server cho mỗi loại công cụ.

---

## 8. Kết luận

Tài liệu Thiết kế Cấp cao (HLD) này đã trình bày một kiến trúc toàn diện cho hệ thống **finAI Finance Agent Web Browser**. Kiến trúc được xây dựng dựa trên các nguyên tắc hiện đại như microservices, event-driven, và multi-agent system, nhằm đáp ứng các yêu cầu khắt khe về hiệu suất, khả năng mở rộng, và độ tin cậy của một ứng dụng FinAI cấp doanh nghiệp.

Bằng cách phân tách hệ thống thành 4 lớp rõ ràng và sử dụng các công nghệ đã được kiểm chứng trong ngành, kiến trúc này tạo ra một nền tảng vững chắc cho việc phát triển, triển khai và vận hành sản phẩm. Các quyết định thiết kế quan trọng, từ việc lựa chọn cơ sở dữ liệu đến chiến lược bảo mật, đều được cân nhắc kỹ lưỡng để tối ưu hóa cho bối cảnh cụ thể của dự án.

Tài liệu này sẽ đóng vai trò là kim chỉ nam cho các nhóm phát triển, kiến trúc sư và các bên liên quan trong suốt vòng đời của dự án, đảm bảo rằng tất cả các thành phần được xây dựng một cách nhất quán và hướng tới mục tiêu chung. Kiến trúc này cũng được thiết kế để linh hoạt, cho phép các điều chỉnh và cải tiến khi dự án phát triển và các yêu cầu mới nảy sinh.

---

## 9. References

*   [1] SDD_P1.md - Project Overview and Executive Summary
*   [2] SDD_P2_Update_ArchitectureMulAgents_for_Layer2.md - Multi-Agent Architecture Details
*   [3] SDD_P3_Update_HighArchitecture_FolderStructure_DataFlow_updated_.md - High Architecture and Data Flow
*   [4] 2.0v4Output-HighArchitect-FolderStructure-DataFlows+SourceCodes.md - Template Structure and Best Practices
*   [5] Các tài liệu dự án khác được cung cấp - Supporting Documentation

---

**Document Version:** 1.0  
**Last Updated:** December 20, 2025  
**Author:** Manus AI - Architecture Team  
**Status:** Production Ready
````