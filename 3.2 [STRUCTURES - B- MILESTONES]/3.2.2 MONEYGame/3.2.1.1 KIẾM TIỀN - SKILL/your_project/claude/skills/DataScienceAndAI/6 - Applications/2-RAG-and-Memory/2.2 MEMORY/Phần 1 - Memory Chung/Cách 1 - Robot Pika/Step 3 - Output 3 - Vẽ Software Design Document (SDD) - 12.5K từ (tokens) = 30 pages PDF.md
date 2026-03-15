```
Đây là tài liệu SDD về dự án : 1.1 file SDD v1 + docs 1.2 là file SDD khi optimize + docs 1.3 là folder structure ---- Hoàn thành checklist sau: 1. GIÚP TỚ LÊN 1 BẢN HLD (high level design) chi tiết khoảng 10K tokens - 40K characters đầy đủ các phần 2. MUST base on template HIGH LEVEL DESIGN ĐÍNH KÈM (file: pasted_content.txt)
```

# HIGH-LEVEL DESIGN (HLD)

# HIGH-LEVEL DESIGN (HLD)

# PIKA Mem0 Long-Term Memory System - Self-Hosted Solution

**Phiên bản: 2.0 | Ngày: 2025-12-20**

---

## 📖 MỤC LỤC

1.  [**Tổng quan (Executive Summary)**](#1-tổng-quan-executive-summary)
2.  [**System Architecture Overview (Kiến trúc tổng quan)**](#2-system-architecture-overview-kiến-trúc-tổng-quan)
3.  [**Modules / Components & Data Flow (Các khối chính & Luồng dữ liệu)**](#3-modules--components--data-flow-các-khối-chính--luồng-dữ-liệu)
4.  [**Data & Database Design (Thiết kế dữ liệu & Database)**](#4-data--database-design-thiết-kế-dữ-liệu--database)
5.  [**Interfaces & Integrations (Giao diện & Tích hợp)**](#5-interfaces--integrations-giao-diện--tích-hợp)
6.  [**Technology & Deployment Architecture (Công nghệ & Kiến trúc triển khai)**](#6-technology--deployment-architecture-công-nghệ--kiến-trúc-triển-khai)
7.  [**Cross-cutting Concerns (Các vấn đề xuyên suốt)**](#7-cross-cutting-concerns-các-vấn-đề-xuyên-suốt)

---

## 1. TỔNG QUAN (EXECUTIVE SUMMARY)

Tài liệu này trình bày thiết kế kiến trúc cấp cao (High-Level Design) cho hệ thống **PIKA Long-Term Memory**, một giải pháp self-hosted được xây dựng để thay thế dịch vụ Mem0 Enterprise. Mục tiêu chính là giảm chi phí vận hành, tăng cường bảo mật dữ liệu, và cung cấp khả năng tùy chỉnh logic cho phù hợp với nhu vực của PIKA robot.

Thiết kế này tập trung vào việc xây dựng một hệ thống có khả năng mở rộng, hiệu năng cao và đáng tin cậy, dựa trên hạ tầng có sẵn (Milvus, Neo4j) và áp dụng các phương pháp tối ưu hóa hiện đại như caching đa tầng, xử lý bất đồng bộ và tăng tốc phần cứng.

| Khía cạnh | Chi tiết |
| :--- | :--- |
| **Vấn đề** | Phụ thuộc vào dịch vụ Mem0 Enterprise tốn kém ($500-1000/tháng), thiếu kiểm soát dữ liệu và logic. |
| **Giải pháp** | Xây dựng hệ thống self-hosted với 2 API lõi (`extract_facts`, `search_facts`), tối ưu hóa cho độ trễ thấp và khả năng mở rộng. |
| **Tác động Business** | Tiết kiệm >60% chi phí, đảm bảo 100% chủ quyền dữ liệu, cho phép tùy chỉnh logic (vd: theo dõi tiến độ học tập). |
| **Tác động Technical** | **P95 Latency < 200ms** cho API tìm kiếm, **P99 < 1s** cho API trích xuất (bất đồng bộ), hỗ trợ >100K người dùng đồng thời. |
| **Kiến trúc lõi** | Microservices, Event-Driven, Multi-Layer Caching, CQRS (ở mức độ nhẹ). |
| **Rủi ro chính** | Sự ổn định của hạ tầng Milvus/Neo4j và độ trễ của OpenAI API. |

---

## 2. SYSTEM ARCHITECTURE OVERVIEW (KIẾN TRÚC TỔNG QUAN)

Kiến trúc tổng thể của hệ thống được thiết kế theo mô hình **Microservices** và **Event-Driven**, tách biệt các mối quan tâm và cho phép mở rộng từng thành phần độc lập.

### 2.1. System Context Diagram (C4 Level 1)

Sơ đồ này mô tả hệ thống trong bối cảnh rộng hơn, bao gồm các người dùng và các hệ thống bên ngoài mà nó tương tác.

```mermaid
graph TD
    subgraph External Systems
        OpenAI[OpenAI API<br/>(Embeddings, LLM)]
        Datadog[Datadog<br/>(Monitoring)]
    end

    subgraph Users
        PikaRobot[PIKA Robot<br/>(AI Workflow)]
        Admin[Admin Panel<br/>(Future)]
    end

    subgraph System Boundary [PIKA Memory System]
        MemoryAPI[
            <b>Memory API Service</b><br/>
            <i>FastAPI, Python 3.11</i><br/>
            Hệ thống lõi cung cấp các API<br/>để lưu trữ và truy xuất trí nhớ.
        ]
    end

    PikaRobot -- "HTTPS/JSON" --> MemoryAPI
    Admin -- "HTTPS/JSON" --> MemoryAPI
    MemoryAPI -- "API Calls" --> OpenAI
    MemoryAPI -- "Logs, Metrics, Traces" --> Datadog
```

### 2.2. Architecture Pattern

Hệ thống áp dụng các mẫu kiến trúc chính sau:

*   **Microservices**: `Memory API Service` là một microservice độc lập, dễ dàng triển khai, nâng cấp và mở rộng.
*   **Event-Driven Architecture (cho `extract_facts`)**: Để giải quyết vấn đề độ trễ cao của LLM, API `extract_facts` sẽ hoạt động bất đồng bộ. Nó nhận yêu cầu, đẩy vào một hàng đợi (Message Queue) và trả về `202 Accepted` ngay lập tức. Một worker riêng sẽ xử lý tác vụ này.
*   **CQRS (Command Query Responsibility Segregation) - Mức độ nhẹ**: Tách biệt rõ ràng giữa luồng ghi (Command - `extract_facts`) và luồng đọc (Query - `search_facts`). Điều này cho phép tối ưu hóa riêng biệt cho từng luồng.
*   **Multi-Layer Caching**: Áp dụng chiến lược caching 3 lớp (L1 In-memory, L2 Distributed, L3 Persistent) để giảm thiểu độ trễ và tải cho các hệ thống backend.

---

## 3. MODULES / COMPONENTS & DATA FLOW (CÁC KHỐI CHÍNH & LUỒNG DỮ LIỆU)

### 3.1. Container Diagram (C4 Level 2)

Sơ đồ này chi tiết hóa các thành phần bên trong `Memory API Service` và cách chúng tương tác với các data store.

```mermaid
graph TD
    subgraph PIKA Memory API Service
        direction LR
        APILayer[API Layer<br/>(FastAPI)]
        ServiceLayer[Service Layer<br/>(Business Logic)]
        DataAccessLayer[Data Access Layer<br/>(Repositories)]

        APILayer --> ServiceLayer
        ServiceLayer --> DataAccessLayer
    end

    subgraph Infrastructure
        direction TB
        Milvus[Milvus<br/>(Vector Store)]
        Neo4j[Neo4j<br/>(Graph Store)]
        PostgreSQL[PostgreSQL<br/>(Metadata)]
        Redis[Redis<br/>(Cache & Message Queue)]
    end

    DataAccessLayer -- "gRPC" --> Milvus
    DataAccessLayer -- "Bolt" --> Neo4j
    DataAccessLayer -- "TCP" --> PostgreSQL
    DataAccessLayer -- "TCP" --> Redis

    APILayer -- "Async Task" --> Redis
```

### 3.2. Luồng dữ liệu (Data Flow)

#### 3.2.1. Luồng 1: Trích xuất Facts (Asynchronous)

Luồng này được tối ưu hóa để xử lý các tác vụ tốn thời gian (gọi LLM) mà không block client.

1.  **Client (PIKA Robot)** gửi `POST /v1/extract_facts` với nội dung cuộc hội thoại.
2.  **API Layer** xác thực request, tạo một `task_id` duy nhất và đẩy một job vào **RabbitMQ** (hoặc Redis Queue) với toàn bộ thông tin cần thiết.
3.  **API Layer** ngay lập tức trả về `HTTP 202 Accepted` cho client cùng với `task_id`.
4.  Một **Fact Extractor Worker** (một process riêng) lắng nghe và nhận job từ queue.
5.  **Worker** gọi **OpenAI LLM** để trích xuất các facts dưới dạng JSON có cấu trúc.
6.  **Worker** gọi **OpenAI Embedding API** để chuyển đổi các facts thành vector.
7.  **Worker** lưu đồng thời:
    *   Vectors vào **Milvus**.
    *   Các mối quan hệ (relationships) vào **Neo4j**.
    *   Metadata (conversation, fact IDs) vào **PostgreSQL**.
8.  (Tùy chọn) Worker cập nhật trạng thái của task (dựa trên `task_id`) vào Redis hoặc PostgreSQL.

#### 3.2.2. Luồng 2: Tìm kiếm Facts (Synchronous & Optimized)

Luồng này được tối ưu hóa cho tốc độ, mục tiêu P95 latency < 200ms.

1.  **Client** gửi `POST /v1/search_facts` với `query` và `user_id`.
2.  **API Layer** tạo một hash từ query và các tham số.
3.  **Service Layer** thực hiện kiểm tra cache đa tầng:
    *   **L1 Cache (In-memory)**: Kiểm tra cache cục bộ của process (ví dụ: `lru_cache`). Nếu có, trả về ngay lập tức (<1ms).
    *   **L2 Cache (Redis)**: Nếu L1 miss, kiểm tra Redis Semantic Cache. Một cache riêng sẽ lưu các vector của query, tìm các query tương tự đã được cache. Nếu cache hit (độ tương đồng > ngưỡng), lấy kết quả đã lưu và trả về (5-20ms).
4.  Nếu cache miss hoàn toàn:
    *   Gọi **OpenAI Embedding API** để vector hóa `query`.
    *   Thực hiện tìm kiếm tương đồng (similarity search) trên **Milvus** để lấy top-K fact IDs. (Tận dụng GPU acceleration và index HNSW được tối ưu).
    *   (Tùy chọn) Lấy thêm thông tin ngữ cảnh từ **Neo4j** dựa trên các fact IDs.
    *   (Tùy chọn) Sử dụng một LLM nhỏ để re-rank kết quả.
5.  **Service Layer** lưu kết quả vào **L2 Redis Cache** với một TTL (Time-to-Live) hợp lý.
6.  **API Layer** trả về danh sách các facts cho client.

---

## 4. DATA & DATABASE DESIGN (THIẾT KẾ DỮ LIỆU & DATABASE)

Thiết kế dữ liệu ở mức high-level tập trung vào việc lựa chọn đúng công cụ cho từng loại dữ liệu.

| Data Store | Công nghệ | Mô hình dữ liệu & Vai trò | Lý do lựa chọn |
| :--- | :--- | :--- | :--- |
| **Vector Store** | **Milvus** | **Collections & Partitions**: Lưu trữ các vector embeddings của facts. Mỗi user có thể có một partition riêng để tăng tốc độ tìm kiếm và cô lập dữ liệu. | Hiệu năng cao cho similarity search, hỗ trợ các index mạnh (HNSW, IVF-PQ), có khả năng scale và GPU acceleration. |
| **Graph Store** | **Neo4j** | **Nodes & Relationships**: Lưu các thực thể (User, Fact, Entity) và mối quan hệ giữa chúng (e.g., `(User)-[:HAS_FACT]->(Fact)`, `(Fact)-[:MENTIONS]->(Entity)`). | Mạnh mẽ trong việc truy vấn các mối quan hệ phức tạp, làm giàu ngữ cảnh cho kết quả tìm kiếm. |
| **Metadata Store** | **PostgreSQL** | **Relational Tables**: Lưu dữ liệu có cấu trúc như thông tin user, lịch sử conversation, metadata của facts (ID, source, timestamp). | ACID, ổn định, quen thuộc. Phù hợp cho các dữ liệu cần tính toàn vẹn cao. |
| **Cache & Queue** | **Redis** | **Key-Value & Pub/Sub**: Lớp L2 caching cho kết quả search. Dùng làm message broker đơn giản cho tác vụ `extract_facts` bất đồng bộ. | Tốc độ cực nhanh, đa dụng (caching, queueing, pub/sub), hệ sinh thái mạnh. |

### 4.2. Database Trade-offs & Scalability Limits

| Database | Ưu điểm | Nhược điểm | Giới hạn Scalability & Giải pháp |
| :--- | :--- | :--- | :--- |
| **Milvus** | - Hiệu năng cực cao cho vector search.<br>- Hỗ trợ nhiều loại index (HNSW, CAGRA).<br>- Khả năng scale ngang tốt. | - Phức tạp trong vận hành.<br>- Không hỗ trợ transaction ACID.<br>- Query language hạn chế. | - **Giới hạn**: Số lượng vector trong một collection. Hiệu năng giảm khi dữ liệu quá lớn.<br>- **Giải pháp**: Partition collection theo `user_id`. Sử dụng các node truy vấn (query nodes) và node dữ liệu (data nodes) mạnh mẽ hơn. Áp dụng L3 caching để giảm tải. |
| **Neo4j** | - Tối ưu cho việc truy vấn mối quan hệ phức tạp.<br>- Ngôn ngữ truy vấn Cypher mạnh mẽ, dễ hiểu.<br>- Hỗ trợ transaction ACID. | - Khó scale ghi (write).<br>- Hiệu năng kém với các truy vấn full-scan.<br>- Yêu cầu nhiều bộ nhớ. | - **Giới hạn**: Hiệu năng ghi bị giới hạn bởi một node leader trong Causal Cluster.<br>- **Giải pháp**: Sử dụng Causal Cluster với nhiều read replica để scale đọc. Tối ưu hóa các truy vấn Cypher. Tránh các "supernodes" (node có quá nhiều mối quan hệ). |
| **PostgreSQL** | - Ổn định, tin cậy, hỗ trợ ACID.<br>- Hệ sinh thái mạnh, nhiều extension (vd: pgvector).<br>- Linh hoạt, có thể lưu metadata, cache, và cả vector. | - Hiệu năng vector search không bằng Milvus.<br>- Scale ghi phức tạp hơn (yêu cầu sharding thủ công). | - **Giới hạn**: Hiệu năng giảm khi bảng quá lớn (hàng tỷ dòng).<br>- **Giải pháp**: Partition bảng `facts` theo `user_id` hoặc `created_at`. Sử dụng read replicas để scale đọc. Áp dụng connection pooling (PgBouncer). |
| **Redis** | - Độ trễ cực thấp (<1ms).<br>- Cấu trúc dữ liệu đa dạng.<br>- Dễ sử dụng. | - Dữ liệu lưu trong RAM, chi phí cao.<br>- Không đảm bảo bền vững (persistence) nếu không cấu hình đúng. | - **Giới hạn**: Dung lượng bị giới hạn bởi RAM.<br>- **Giải pháp**: Sử dụng Redis Cluster để scale ngang. Áp dụng các chính sách eviction (vd: allkeys-lru) để quản lý bộ nhớ. Chỉ cache các dữ liệu "nóng". |

### 4.1. Conceptual Data Model

*   **Fact**: Đơn vị thông tin cơ bản (e.g., "Sở thích của user là bơi lội"). Mỗi fact có một vector embedding, ID, nội dung text, và các metadata khác.
*   **Entity**: Các thực thể được nhắc đến trong fact (e.g., "bơi lội").
*   **Conversation**: Một chuỗi các trao đổi giữa user và robot, là nguồn để trích xuất facts.
*   **User**: Người dùng của PIKA.

Mối quan hệ chính: `User` có nhiều `Conversation`, mỗi `Conversation` tạo ra nhiều `Fact`, mỗi `Fact` có thể đề cập đến nhiều `Entity`.

---

## 5. INTERFACES & INTEGRATIONS (GIAO DIỆN & TÍCH HỢP)

### 5.1. Public APIs

Hệ thống sẽ cung cấp các RESTful API qua giao thức HTTPS.

| Endpoint | Method | Mô tả | Request Body | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `/v1/extract_facts` | `POST` | **(Asynchronous)** Nhận một cuộc hội thoại và đưa vào hàng đợi để trích xuất. | `{ "user_id": "...", "conversation": [...] }` | `202 Accepted` `{ "task_id": "..." }` |
| `/v1/search_facts` | `POST` | **(Synchronous)** Tìm kiếm các facts liên quan đến một query. | `{ "user_id": "...", "query": "...", "top_k": 5 }` | `200 OK` `{ "facts": [...] }` |
| `/v1/tasks/{task_id}` | `GET` | (Tùy chọn) Kiểm tra trạng thái của một tác vụ trích xuất. | N/A | `200 OK` `{ "status": "completed/pending/failed" }` |
| `/health` | `GET` | Endpoint kiểm tra sức khỏe cho Kubernetes liveness/readiness probes. | N/A | `200 OK` `{ "status": "healthy" }` |

### 5.2. External Integrations

*   **OpenAI API**: Tích hợp để lấy embeddings (`text-embedding-3-small`) và trích xuất facts có cấu trúc (`gpt-4o-mini`). Cần có cơ chế retry và fallback.
*   **Datadog/Prometheus**: Tích hợp để gửi metrics, logs, và traces, đảm bảo khả năng quan sát (observability) toàn diện.

---

## 6. TECHNOLOGY & DEPLOYMENT ARCHITECTURE (CÔNG NGHỆ & KIẾN TRÚC TRIỂN KHAI)

### 6.1. Tech Stack

| Layer | Technology | Version | Lý do |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.11+ | Hệ sinh thái AI/ML mạnh, hiệu năng tốt với async. |
| **API Framework** | FastAPI | 0.109+ | Hiệu năng cao, hỗ trợ async, tự động sinh docs. |
| **Vector Store** | Milvus | 2.3+ | Chuyên dụng cho vector search, có thể scale. |
| **Graph Store** | Neo4j | 5.x | Dẫn đầu thị trường graph database. |
| **Metadata DB** | PostgreSQL | 15+ | Ổn định, tin cậy. |
| **Cache & Queue** | Redis | 7.x | Nhanh và đa năng. |
| **Embeddings** | OpenAI API | `text-embedding-3-small` | Chất lượng tốt, chi phí hợp lý. |
| **LLM** | OpenAI API | `gpt-4o-mini` | Tốc độ nhanh, thông minh, hỗ trợ structured output. |
| **Deployment** | Docker, Kubernetes | latest | Tiêu chuẩn ngành cho containerization và orchestration. |

### 6.2. Deployment Architecture

Hệ thống sẽ được triển khai trên **Kubernetes (K8s)** để đảm bảo khả năng tự phục hồi, mở rộng và quản lý dễ dàng.

*   **Memory API Service** sẽ được đóng gói thành một Docker image và triển khai dưới dạng một K8s Deployment.
*   **Fact Extractor Worker** cũng là một K8s Deployment riêng, có thể scale số lượng replicas độc lập với API service dựa trên độ dài của message queue.
*   Sử dụng **Horizontal Pod Autoscaler (HPA)** cho cả API và Worker để tự động scale dựa trên CPU/memory hoặc số lượng message trong queue.
*   Một **K8s Service** và **Ingress** sẽ expose API service ra bên ngoài.
*   Các database (Milvus, Neo4j, PostgreSQL, Redis) được giả định là đã có sẵn và được quản lý bên ngoài K8s cluster hoặc sử dụng các managed service.

---

## 7. CROSS-CUTTING CONCERNS (CÁC VẤN ĐỀ XUYÊN SUỐT)

### 7.5. Rate Limiting & Backpressure

*   **Rate Limiting**: Để bảo vệ hệ thống khỏi bị quá tải và lạm dụng, một cơ chế rate limiting sẽ được áp dụng tại API Gateway (hoặc middleware trong FastAPI). Sử dụng thuật toán **Token Bucket** hoặc **Fixed Window Counter** lưu trên Redis để giới hạn số lượng request mỗi user có thể thực hiện trong một khoảng thời gian (vd: 100 requests/phút).
*   **Backpressure**: Khi hệ thống bị quá tải (vd: message queue đầy, worker xử lý không kịp), nó cần có khả năng "đẩy ngược" áp lực lại cho client. API `extract_facts` sẽ trả về lỗi `HTTP 429 Too Many Requests` hoặc `HTTP 503 Service Unavailable` nếu message queue đã đầy, yêu cầu client thử lại sau.

### 7.1. Performance & Scalability

*   **Latency**: Mục tiêu P95 < 200ms cho `search_facts` và P99 < 1s cho `extract_facts` (nhờ async). Điều này đạt được qua:
    *   **Async I/O**: Tận dụng FastAPI và aiohttp/httpx cho các cuộc gọi non-blocking.
    *   **Multi-Layer Caching**: Giảm thiểu các cuộc gọi đến database và OpenAI.
    *   **GPU Acceleration**: Cấu hình Milvus sử dụng GPU (với index CAGRA) để tăng tốc độ search lên 10-50 lần.
    *   **Optimized Indexing**: Sử dụng index HNSW cho Milvus với các tham số `efConstruction` và `efSearch` được tinh chỉnh.
*   **Scalability**: Hệ thống được thiết kế để scale theo chiều ngang. Có thể tăng số lượng pod cho API service và worker service một cách độc lập.

### 7.2. Security

*   **Authentication & Authorization**: Sử dụng JWT (JSON Web Tokens) để xác thực các request từ PIKA robot. API Gateway hoặc một middleware sẽ chịu trách nhiệm validate token.
*   **Data Encryption**: Toàn bộ dữ liệu nhạy cảm của người dùng (conversations) phải được mã hóa cả khi lưu trữ (at-rest) và khi truyền đi (in-transit - TLS).
*   **Network Security**: Sử dụng K8s Network Policies để giới hạn traffic giữa các pod, chỉ cho phép các kết nối cần thiết.
*   **Input Validation**: Sử dụng Pydantic để validate tất cả dữ liệu đầu vào, chống lại các tấn công injection.

### 7.3. Availability & Resiliency

*   **High Availability**: Triển khai nhiều replica cho mỗi service trên K8s để tránh SPOF (Single Point of Failure).
*   **Health Checks**: Cung cấp endpoint `/health` để K8s có thể tự động phát hiện và khởi động lại các pod bị lỗi.
*   **Resiliency Patterns**:
    *   **Retry & Timeouts**: Implement cơ chế retry với exponential backoff và jitter cho các cuộc gọi đến external services (OpenAI, Milvus). Mỗi request phải có một timeout chặt chẽ để tránh bị treo.
    *   **Circuit Breaker**: Sử dụng thư viện như `resilience4py` để implement mẫu Circuit Breaker. Nếu một service phụ thuộc (vd: Neo4j) có tỷ lệ lỗi cao, circuit sẽ "mở", và các request sẽ thất bại ngay lập tức (fail-fast) hoặc được chuyển hướng đến fallback, tránh làm quá tải service đang gặp sự cố.
    *   **Bulkhead**: Phân bổ tài nguyên (connection pools, thread pools) riêng cho các cuộc gọi đến từng service phụ thuộc. Điều này ngăn chặn việc một service chậm làm ảnh hưởng đến toàn bộ hệ thống (vd: connection pool riêng cho Milvus và Neo4j).
    *   **Fallback**: Nếu một service phụ thuộc bị lỗi, hệ thống có thể hoạt động ở chế độ "degraded". Ví dụ, nếu Neo4j lỗi, API search vẫn trả về kết quả từ Milvus và PostgreSQL mà không có dữ liệu ngữ cảnh từ graph.

### 7.4. Observability

*   **Logging**: Sử dụng structured logging (JSON format) để dễ dàng tìm kiếm và phân tích trên các hệ thống như Datadog hoặc ELK stack. Mỗi request sẽ có một `correlation_id` để trace.
*   **Metrics**: Expose các metrics theo chuẩn Prometheus (e.g., request latency, error rate, cache hit rate, queue length) để theo dõi sức khỏe hệ thống theo thời gian thực.
*   **Tracing**: Tích hợp OpenTelemetry để thực hiện distributed tracing, cho phép theo dõi một request qua nhiều services và xác định các điểm nghẽn cổ chai.


---

## 8. DETAILED COMPONENT INTERACTIONS (TƯƠNG TÁC CHI TIẾT GIỮA CÁC THÀNH PHẦN)

### 8.1. Extract Facts API - Detailed Flow

Luồng này được thiết kế để xử lý các tác vụ tốn thời gian mà không làm block client. Dưới đây là chi tiết từng bước:

**Bước 1: Request Validation & Queueing (API Layer)**

Khi client gửi `POST /v1/extract_facts`, API layer sẽ:

1.  Xác thực JWT token từ header `Authorization`.
2.  Validate request body (kiểm tra `user_id`, `conversation` format).
3.  Tạo một UUID duy nhất làm `task_id`.
4.  Tạo một job object chứa toàn bộ thông tin: `{ task_id, user_id, conversation, timestamp }`.
5.  Đẩy job vào **Redis Queue** (hoặc RabbitMQ) với một TTL (ví dụ: 24 giờ).
6.  Lưu trạng thái của task vào Redis: `task:{task_id} -> { status: "pending", created_at: ... }`.
7.  Trả về `HTTP 202 Accepted` với payload `{ "task_id": "...", "status_url": "/v1/tasks/{task_id}" }`.

**Bước 2: Asynchronous Processing (Fact Extractor Worker)**

Một hoặc nhiều worker process (có thể là một K8s Deployment riêng) sẽ:

1.  Lắng nghe message từ queue.
2.  Khi nhận được job, cập nhật trạng thái: `status: "processing"`.
3.  Gửi **OpenAI LLM API** (model: `gpt-4o-mini`) với một prompt được thiết kế để trích xuất facts dưới dạng JSON có cấu trúc. Prompt sẽ yêu cầu LLM trả về một danh sách các facts với các trường: `{ id, content, entities, confidence_score }`.
4.  Xử lý response từ LLM, validate JSON, và xử lý các lỗi (ví dụ: JSON không hợp lệ).
5.  Gửi **OpenAI Embedding API** (`text-embedding-3-small`) để vector hóa nội dung của mỗi fact. Mỗi fact sẽ nhận được một vector 1536-dimensional.
6.  Lưu các vectors vào **Milvus**:
    *   Tạo một collection cho user này nếu chưa tồn tại.
    *   Insert các vectors với metadata (fact ID, user_id, conversation_id, timestamp).
7.  Lưu các mối quan hệ vào **Neo4j**:
    *   Tạo các node cho Fact và Entity.
    *   Tạo các relationship: `(User)-[:HAS_FACT]->(Fact)`, `(Fact)-[:MENTIONS]->(Entity)`, `(Fact)-[:FROM_CONVERSATION]->(Conversation)`.
8.  Lưu metadata vào **PostgreSQL**:
    *   Insert vào bảng `facts` với các cột: `id, user_id, conversation_id, content, created_at, updated_at`.
    *   Insert vào bảng `conversations` nếu chưa tồn tại.
9.  Cập nhật trạng thái task: `status: "completed", completed_at: ..., result: { fact_count: N }`.
10. Nếu có lỗi ở bất kỳ bước nào, cập nhật `status: "failed", error_message: ...` và log chi tiết lỗi.

**Bước 3: Status Polling (Optional)**

Client có thể poll endpoint `/v1/tasks/{task_id}` để kiểm tra trạng thái của task. Response sẽ chứa `status` (pending/processing/completed/failed) và các thông tin liên quan.

### 8.2. Search Facts API - Detailed Flow

Luồng này được tối ưu hóa để đạt P95 latency < 200ms thông qua caching đa tầng.

**Bước 1: Request Validation (API Layer)**

1.  Xác thực JWT token.
2.  Validate request body: `user_id`, `query`, `top_k` (default: 5).
3.  Tạo một `cache_key` từ `user_id`, `query`, và `top_k`: `search:{user_id}:{hash(query)}:{top_k}`.

**Bước 2: Multi-Layer Cache Lookup (Service Layer)**

**L1 Cache (In-Memory)**

*   Kiểm tra `@lru_cache` trên hàm search. Nếu cache hit, trả về ngay lập tức (<1ms).

**L2 Cache (Redis Semantic Cache)**

*   Nếu L1 miss, kiểm tra Redis với `cache_key`. Nếu cache hit, deserialize và trả về (5-20ms).

**L3 Cache (PostgreSQL Persistent Cache)**

*   Nếu L2 miss, kiểm tra bảng `search_result_cache` trong PostgreSQL với `query_hash`. Nếu cache hit, trả về kết quả (50-100ms) và "làm ấm" L2 cache bằng cách ghi lại kết quả vào Redis.
*   Nếu L3 miss, tiếp tục.

**Bước 3: Query Embedding (nếu cache miss)**

1.  Gửi **OpenAI Embedding API** để vector hóa `query` thành một vector 1536-dimensional (~100-200ms).
2.  Cache vector này trong Redis với TTL ngắn (ví dụ: 1 giờ) để tái sử dụng nếu có query tương tự.

**Bước 4: Vector Similarity Search (Milvus)**

1.  Gửi Milvus với vector query và `top_k=10` (lấy nhiều hơn để có lựa chọn cho re-ranking).
2.  Milvus sẽ sử dụng index HNSW (hoặc CAGRA nếu có GPU) để tìm các vector tương tự nhất (~50-100ms với optimization).
3.  Nhận lại danh sách fact IDs với similarity scores.

**Bước 5: Enrichment & Re-ranking (Optional)**

1.  Lấy thêm metadata từ **PostgreSQL** (fact content, timestamps).
2.  (Tùy chọn) Lấy thêm ngữ cảnh từ **Neo4j** (entities liên quan, facts liên quan).
3.  (Tùy chọn) Sử dụng một LLM nhỏ hoặc một model re-ranking để sắp xếp lại kết quả dựa trên độ liên quan cao hơn (~50-100ms nếu thực hiện).

**Bước 6: Response & Caching**

1.  Chuẩn bị response JSON chứa top-K facts (sau khi filter lại nếu cần).
2.  Lưu kết quả vào **L2 Redis Cache** với TTL hợp lý (ví dụ: 1 giờ cho các query hot, 30 phút cho các query lạnh).
3.  Trả về `HTTP 200 OK` với payload `{ "facts": [...], "total_count": N }`.

### 8.3. Cache Invalidation Strategy

Khi một fact mới được thêm vào (qua `extract_facts`), các cache liên quan cần được invalidate:

1.  **Invalidate L1 Cache**: Xóa toàn bộ `@lru_cache` hoặc sử dụng một cache key versioning.
2.  **Invalidate L2 Cache (Redis)**: Xóa tất cả các key Redis có pattern `search:{user_id}:*` để buộc refresh.
3.  **Invalidate L3 Cache (PostgreSQL)**: Nếu sử dụng materialized views, refresh chúng.

Cách tốt nhất là sử dụng **event-driven invalidation**: Khi worker hoàn thành `extract_facts`, nó sẽ publish một event (ví dụ: `FactsExtracted`) vào một message broker. Một service khác sẽ subscribe và thực hiện cache invalidation.

---

## 9. OPTIMIZATION STRATEGIES (CÁC CHIẾN LƯỢC TỐI ƯU HÓA)

### 9.1. Latency Optimization

Để đạt được mục tiêu P95 < 200ms cho `search_facts`, các chiến lược sau được áp dụng:

1.  **Async I/O**: Sử dụng `asyncio` và `aiohttp`/`httpx` để thực hiện các cuộc gọi non-blocking.
2.  **Connection Pooling**: Duy trì các pool kết nối đến Milvus, Neo4j, PostgreSQL, Redis để tái sử dụng và giảm overhead.
3.  **Batch Processing**: Nếu có nhiều search requests cùng một lúc, có thể batch chúng lại và gửi một batch query duy nhất đến Milvus.
4.  **GPU Acceleration**: Cấu hình Milvus sử dụng GPU (CAGRA index) để tăng tốc độ search lên 10-50 lần.
5.  **Index Optimization**: Tuning các tham số của index HNSW (M, efConstruction, efSearch) để cân bằng giữa tốc độ và độ chính xác.
6.  **Semantic Caching**: Sử dụng Redis semantic cache để lưu các query đã được xử lý và tái sử dụng kết quả cho các query tương tự.

### 9.2. Throughput Optimization

Để hỗ trợ >100K người dùng đồng thời:

1.  **Horizontal Scaling**: Triển khai nhiều pod cho API service và worker service trên K8s.
2.  **Load Balancing**: Sử dụng K8s Service hoặc Ingress controller để phân phối traffic đều.
3.  **Queue Management**: Sử dụng một message queue mạnh mẽ (Redis Queue hoặc RabbitMQ) để xử lý các tác vụ bất đồng bộ.
4.  **Database Optimization**: Tối ưu hóa các query PostgreSQL, sử dụng indexing, partitioning nếu cần.
5.  **Milvus Partitioning**: Chia các collection thành các partition theo `user_id` để tăng tốc độ search.

### 9.3. Cost Optimization

1.  **OpenAI API Cost**: Sử dụng embedding model nhỏ hơn (`text-embedding-3-small` thay vì `text-embedding-3-large`) để giảm chi phí. Cache embeddings để tái sử dụng.
2.  **Infrastructure Cost**: Sử dụng các hạ tầng có sẵn (Milvus, Neo4j đã deployed). Tối ưu hóa việc sử dụng CPU/memory để giảm chi phí cloud.
3.  **Data Storage**: Implement một chính sách retention (ví dụ: xóa các facts cũ hơn 2 năm) để giảm dung lượng lưu trữ.

---

## 10. DEPLOYMENT & ROLLOUT STRATEGY (CHIẾN LƯỢC TRIỂN KHAI)

### 10.1. Phased Rollout

**Phase 1 (MVP - Tuần 1-3)**

*   Triển khai các API cơ bản (`extract_facts`, `search_facts`) với caching đơn giản (L2 Redis).
*   Không có worker bất đồng bộ; `extract_facts` sẽ là synchronous (tạm thời).
*   Testing cơ bản: unit tests, integration tests.
*   Monitoring cơ bản: logs, basic metrics.

**Phase 2 (Production Ready - Tuần 4-6)**

*   Implement worker bất đồng bộ cho `extract_facts`.
*   Thêm multi-layer caching (L1, L2, L3).
*   Implement cache invalidation strategy.
*   Load testing để xác minh P95 latency < 200ms.
*   Monitoring nâng cao: distributed tracing, detailed metrics.
*   Security hardening: encryption, network policies.

**Phase 3 (Optimization - Tuần 7-8)**

*   GPU acceleration cho Milvus (nếu có GPU available).
*   Query optimization, index tuning.
*   Cost optimization.
*   Performance tuning dựa trên production metrics.

### 10.2. Blue-Green Deployment

Để tránh downtime khi cập nhật, sử dụng blue-green deployment:

1.  Duy trì hai bản sao của hệ thống: "Blue" (hiện tại) và "Green" (mới).
2.  Deploy phiên bản mới vào "Green".
3.  Chạy smoke tests trên "Green".
4.  Chuyển traffic từ "Blue" sang "Green" (thông qua load balancer).
5.  Nếu có vấn đề, quay lại "Blue" ngay lập tức.

---

## 11. RISK ANALYSIS & MITIGATION (PHÂN TÍCH RỦI RO & GIẢM THIỂU)

| Rủi ro | Mức độ | Tác động | Giải pháp giảm thiểu |
| :--- | :--- | :--- | :--- |
| **Milvus/Neo4j downtime** | High | Hệ thống không thể search hoặc store facts | Implement health checks, fallback modes, backup/restore strategy |
| **OpenAI API latency/outage** | Medium | Extract facts bị chậm hoặc thất bại | Implement retry logic, fallback embedding model (local), queue management |
| **High volume of extract requests** | Medium | Queue bị tắc, worker không kịp xử lý | Auto-scale worker pods, optimize LLM calls, batch processing |
| **Cache inconsistency** | Low | Kết quả search không chính xác | Implement cache versioning, TTL management, invalidation strategy |
| **Data privacy breach** | High | Dữ liệu người dùng bị lộ | Encryption at rest/in-transit, access controls, audit logging |

---

## 12. SUCCESS METRICS & KPIs (CHỈ SỐ THÀNH CÔNG)

| KPI | Baseline (Mem0) | Target (Self-hosted) | Cách đo |
| :--- | :--- | :--- | :--- |
| **P95 Latency (Search)** | ~150ms | <200ms | Datadog APM, Prometheus |
| **P99 Latency (Extract)** | N/A | <1s | Worker processing time |
| **Error Rate** | <0.5% | <0.1% | Prometheus, logs |
| **Cache Hit Rate** | N/A | >60% (L2), >30% (L3) | Redis stats, custom metrics |
| **Monthly Cost** | $500-1000 | <$250 (infra) | Cloud billing, OpenAI usage |
| **Memory Accuracy** | ~85% | >90% | Manual testing, user feedback |
| **Uptime** | 99.9% | 99.9%+ | K8s health checks, monitoring |

---

## 13. FUTURE ENHANCEMENTS (CÁC CẢI TIẾN TRONG TƯƠNG LAI)

1.  **Memory Consolidation**: Tự động merge các facts tương tự để giảm dung lượng lưu trữ.
2.  **Time-Decay Scoring**: Các facts cũ sẽ có độ quan trọng thấp hơn trong kết quả search.
3.  **Multi-Language Support**: Mở rộng hỗ trợ cho các ngôn ngữ khác ngoài Vietnamese/English.
4.  **Memory Analytics Dashboard**: Giao diện web để xem thống kê, trends về memory của user.
5.  **Bulk Import/Export**: API để import/export facts từ các hệ thống khác.
6.  **Hybrid Search**: Kết hợp vector search với keyword search (BM25) để cải thiện độ chính xác.
7.  **Custom Embedding Models**: Hỗ trợ các embedding model tùy chỉnh được fine-tune cho domain PIKA.

---

## 14. CONCLUSION (KẾT LUẬN)

Bản HLD này cung cấp một kiến trúc toàn diện, có khả năng mở rộng và tối ưu hóa cho hệ thống PIKA Long-Term Memory. Bằng cách áp dụng các mẫu kiến trúc hiện đại (microservices, event-driven, CQRS), tối ưu hóa hiệu năng (multi-layer caching, GPU acceleration), và đảm bảo độ tin cậy cao (health checks, fallback strategies), hệ thống này sẽ đáp ứng các yêu cầu về hiệu năng, bảo mật, và khả năng mở rộng.

Tiếp theo, các kỹ sư phát triển sẽ sử dụng HLD này để tạo ra Low-Level Design (LLD) chi tiết hơn, sau đó là implementation. Quá trình này sẽ được hỗ trợ bởi các test kỹ lưỡng, monitoring toàn diện, và một quy trình triển khai cẩn thận để đảm bảo chất lượng production.


---

## APPENDIX A: DETAILED ARCHITECTURE DIAGRAMS

### A.1. Request Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SEARCH FACTS REQUEST PROCESSING                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Client Request                                                              │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ API Layer: JWT Validation, Input Validation                    │       │
│  │ Create cache_key = hash(user_id, query, top_k)                 │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ L1 Cache Check (In-Memory @lru_cache)                          │       │
│  │ Hit? → Return immediately (<1ms)                               │       │
│  │ Miss? → Continue                                               │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ L2 Cache Check (Redis Semantic Cache)                          │       │
│  │ Hit? → Deserialize and return (5-20ms)                         │       │
│  │ Miss? → Continue                                               │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Query Embedding (OpenAI API)                                   │       │
│  │ Convert query text → 1536-dim vector (~100-200ms)              │       │
│  │ Cache vector in Redis for reuse                                │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Milvus Vector Similarity Search                                │       │
│  │ Search with HNSW/CAGRA index                                   │       │
│  │ Return top-10 fact IDs with scores (~50-100ms)                 │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Optional: Enrichment & Re-ranking                              │       │
│  │ Fetch metadata from PostgreSQL                                 │       │
│  │ Fetch context from Neo4j                                       │       │
│  │ Re-rank with LLM if needed                                     │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Cache Result in L2 (Redis)                                     │       │
│  │ Set TTL based on query patterns                                │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  Response to Client (HTTP 200 OK)                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### A.2. Extract Facts Asynchronous Processing

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTRACT FACTS ASYNCHRONOUS FLOW                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Client Request                                                              │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ API Layer: Validation, Create task_id, Push to Queue           │       │
│  │ Return HTTP 202 Accepted with task_id                          │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                    (Immediate response to client)                           │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Message Queue (Redis/RabbitMQ)                                 │       │
│  │ Job stored with TTL (24 hours)                                 │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Fact Extractor Worker (Separate Process/Pod)                   │       │
│  │ Poll queue, pick up job                                        │       │
│  │ Update status: "processing"                                    │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Call OpenAI LLM (gpt-4o-mini)                                  │       │
│  │ Extract facts with structured output (~500-1000ms)             │       │
│  │ Validate JSON response                                         │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Generate Embeddings (OpenAI API)                               │       │
│  │ Convert each fact text → 1536-dim vector (~100-200ms)          │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│         ┌───────────────────┼───────────────────┐                          │
│         │                   │                   │                          │
│         ▼                   ▼                   ▼                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐              │
│  │ Milvus         │  │ Neo4j          │  │ PostgreSQL     │              │
│  │ Insert vectors │  │ Create nodes & │  │ Save metadata  │              │
│  │ with metadata  │  │ relationships  │  │ & conversation │              │
│  │ (~50-100ms)    │  │ (~50-100ms)    │  │ (~50-100ms)    │              │
│  └────────────────┘  └────────────────┘  └────────────────┘              │
│         │                   │                   │                          │
│         └───────────────────┼───────────────────┘                          │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Update Task Status in Redis                                    │       │
│  │ status: "completed", completed_at, result: { fact_count: N }   │       │
│  └──────────────────────────┬──────────────────────────────────────┘       │
│                             │                                               │
│                             ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ Publish Event: FactsExtracted                                  │       │
│  │ Trigger cache invalidation for this user                       │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  Client can poll /v1/tasks/{task_id} to check status                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## APPENDIX B: DATABASE SCHEMA OVERVIEW

### B.1. PostgreSQL Tables (Metadata)

**Table: users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Table: conversations**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(500),
    message_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Table: facts**
```sql
CREATE TABLE facts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    content TEXT NOT NULL,
    confidence_score FLOAT DEFAULT 0.0,
    milvus_vector_id BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

**Table: entities**
```sql
CREATE TABLE entities (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### B.2. Milvus Collection Schema

**Collection: facts_vectors**
```python
{
    "name": "facts_vectors",
    "fields": [
        {"name": "id", "datatype": "Int64", "is_primary": True},
        {"name": "user_id", "datatype": "VarChar", "max_length": 36},
        {"name": "fact_id", "datatype": "VarChar", "max_length": 36},
        {"name": "conversation_id", "datatype": "VarChar", "max_length": 36},
        {"name": "embedding", "datatype": "FloatVector", "dim": 1536},
        {"name": "timestamp", "datatype": "Int64"},
    ],
    "index": {
        "metric_type": "L2",  # or "COSINE"
        "index_type": "HNSW",  # or "CAGRA" for GPU
        "params": {
            "M": 32,
            "efConstruction": 200,
        }
    }
}
```

### B.3. Neo4j Graph Schema

**Nodes:**
- `User { id, email, name }`
- `Fact { id, content, confidence_score, created_at }`
- `Entity { id, name, type }`
- `Conversation { id, title, created_at }`

**Relationships:**
- `(User)-[:HAS_FACT]->(Fact)` - User owns a fact
- `(Fact)-[:MENTIONS]->(Entity)` - Fact mentions an entity
- `(Fact)-[:FROM_CONVERSATION]->(Conversation)` - Fact comes from a conversation
- `(User)-[:HAS_CONVERSATION]->(Conversation)` - User has a conversation
- `(Entity)-[:RELATED_TO]->(Entity)` - Entities are related

---

## APPENDIX C: API SPECIFICATION EXAMPLES

### C.1. Extract Facts API Request/Response

**Request:**
```json
POST /v1/extract_facts
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "conversation": [
    {
      "role": "user",
      "content": "Tôi rất thích chơi bóng đá và bơi lội vào cuối tuần."
    },
    {
      "role": "assistant",
      "content": "Thế là bạn có hai sở thích thể thao yêu thích! Bóng đá và bơi lội đều là những hoạt động tuyệt vời."
    }
  ]
}
```

**Response (202 Accepted):**
```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "pending",
  "status_url": "/v1/tasks/660e8400-e29b-41d4-a716-446655440001",
  "created_at": "2025-12-20T10:30:00Z"
}
```

### C.2. Search Facts API Request/Response

**Request:**
```json
POST /v1/search_facts
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "Những sở thích thể thao của tôi là gì?",
  "top_k": 5
}
```

**Response (200 OK):**
```json
{
  "facts": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "content": "Tôi rất thích chơi bóng đá và bơi lội vào cuối tuần.",
      "similarity_score": 0.92,
      "conversation_id": "660e8400-e29b-41d4-a716-446655440001",
      "created_at": "2025-12-20T10:30:00Z",
      "entities": ["bóng đá", "bơi lội"]
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "content": "Tôi cũng yêu thích chạy bộ vào sáng sớm.",
      "similarity_score": 0.78,
      "conversation_id": "660e8400-e29b-41d4-a716-446655440004",
      "created_at": "2025-12-20T11:15:00Z",
      "entities": ["chạy bộ"]
    }
  ],
  "total_count": 2,
  "cached": false,
  "latency_ms": 145
}
```

### C.3. Task Status API Request/Response

**Request:**
```json
GET /v1/tasks/660e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <JWT_TOKEN>
```

**Response (200 OK - Completed):**
```json
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "completed",
  "created_at": "2025-12-20T10:30:00Z",
  "completed_at": "2025-12-20T10:32:15Z",
  "result": {
    "fact_count": 2,
    "facts": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "content": "Tôi rất thích chơi bóng đá và bơi lội vào cuối tuần."
      },
      {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "content": "Tôi cũng yêu thích chạy bộ vào sáng sớm."
      }
    ]
  }
}
```

---

## APPENDIX D: MONITORING & OBSERVABILITY METRICS

### D.1. Key Metrics to Track

**Latency Metrics:**
- `search_facts_latency_p50`, `p95`, `p99` (milliseconds)
- `extract_facts_processing_time_p50`, `p95`, `p99` (seconds)
- `cache_lookup_latency` (milliseconds)
- `milvus_search_latency` (milliseconds)
- `openai_api_latency` (milliseconds)

**Throughput Metrics:**
- `search_facts_requests_per_second`
- `extract_facts_jobs_per_second`
- `milvus_queries_per_second`
- `redis_operations_per_second`

**Cache Metrics:**
- `l1_cache_hit_rate` (percentage)
- `l2_cache_hit_rate` (percentage)
- `l3_cache_hit_rate` (percentage)
- `cache_eviction_rate`

**Error Metrics:**
- `search_facts_error_rate` (percentage)
- `extract_facts_error_rate` (percentage)
- `openai_api_error_rate` (percentage)
- `database_error_rate` (percentage)

**Resource Metrics:**
- `cpu_usage` (percentage)
- `memory_usage` (percentage)
- `redis_memory_usage` (bytes)
- `milvus_memory_usage` (bytes)
- `postgres_connection_pool_usage` (percentage)

**Queue Metrics:**
- `message_queue_length`
- `message_queue_processing_time`
- `worker_pod_count`
- `worker_utilization` (percentage)

### D.2. Alert Rules (Example)

```yaml
alerts:
  - name: SearchLatencyHigh
    condition: search_facts_latency_p95 > 200ms
    severity: warning
    
  - name: ExtractLatencyHigh
    condition: extract_facts_processing_time_p99 > 1s
    severity: warning
    
  - name: CacheHitRateLow
    condition: l2_cache_hit_rate < 30%
    severity: info
    
  - name: MilvusDowntime
    condition: milvus_health_check == down
    severity: critical
    
  - name: OpenAIAPIErrors
    condition: openai_api_error_rate > 5%
    severity: critical
    
  - name: QueueBacklog
    condition: message_queue_length > 10000
    severity: warning
```

---

## APPENDIX E: SECURITY CONSIDERATIONS

### E.1. Authentication & Authorization

*   **JWT Tokens**: Each request must include a valid JWT token in the `Authorization: Bearer <token>` header.
*   **Token Validation**: Tokens are validated on every request by the API middleware.
*   **Token Expiration**: Tokens expire after 1 hour; clients must refresh using a refresh token.
*   **Role-Based Access Control (RBAC)**: Different users can only access their own facts and conversations.

### E.2. Data Protection

*   **Encryption at Rest**: All sensitive data (conversations, facts) stored in PostgreSQL, Milvus, and Neo4j must be encrypted using AES-256.
*   **Encryption in Transit**: All API communication must use TLS 1.3 (HTTPS).
*   **Key Management**: Encryption keys must be stored in a secure key management service (e.g., AWS KMS, HashiCorp Vault).

### E.3. Network Security

*   **Network Policies**: Kubernetes Network Policies restrict traffic between pods. Only necessary connections are allowed.
*   **API Gateway**: An API Gateway (e.g., Kong, Nginx) sits in front of the service to handle rate limiting and request filtering.
*   **VPC Isolation**: The service runs in a private VPC with restricted ingress/egress rules.

### E.4. Compliance

*   **GDPR Compliance**: Support for data deletion requests. Users can request their data to be deleted, which triggers a cascade delete across all databases.
*   **Data Retention**: Implement automatic deletion of facts older than 2 years.
*   **Audit Logging**: All API calls and data modifications are logged with user ID, timestamp, and action for audit purposes.

---

## APPENDIX F: GLOSSARY & TERMINOLOGY

| Term | Definition |
| :--- | :--- |
| **Fact** | A unit of information extracted from a conversation (e.g., "User likes swimming"). |
| **Entity** | A named item mentioned in a fact (e.g., "swimming", "Monday"). |
| **Embedding** | A numerical vector representation of text, generated by an embedding model. |
| **Vector Store** | A database optimized for storing and searching high-dimensional vectors (Milvus). |
| **Graph Store** | A database optimized for storing and querying relationships between entities (Neo4j). |
| **Cache Hit** | When a requested item is found in the cache, avoiding a backend query. |
| **Cache Miss** | When a requested item is not found in the cache, requiring a backend query. |
| **Latency** | The time taken to process a request and return a response. |
| **Throughput** | The number of requests processed per unit time (e.g., requests per second). |
| **Async** | Asynchronous processing; the API returns immediately while the actual work happens in the background. |
| **Sync** | Synchronous processing; the API waits for the work to complete before returning. |
| **TTL** | Time-To-Live; the duration for which a cached item remains valid before expiration. |
| **SLA** | Service Level Agreement; a commitment to uptime and performance metrics. |

---

**Document Version**: 2.0  
**Last Updated**: 2025-12-20  
**Author**: Manus AI  
**Status**: Final - Ready for Implementation
