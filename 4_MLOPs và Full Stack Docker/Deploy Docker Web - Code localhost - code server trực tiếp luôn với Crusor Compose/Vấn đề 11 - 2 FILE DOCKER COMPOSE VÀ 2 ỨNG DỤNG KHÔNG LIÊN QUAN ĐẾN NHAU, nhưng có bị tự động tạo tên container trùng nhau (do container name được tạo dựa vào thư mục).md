# Vấn đề: 

Tại sao 1 ứng dụng khác cũng khởi tạo cả 4 cái này ???

RÕ RÀNG 2 FILE DOCKER COMPOSE VÀ 2 ỨNG DỤNG KHÔNG LIÊN QUAN ĐẾN NHAU MẸ GÌ CẢ 

[+] Running 4/4
 ✔ Container src-backend-1         Recreated                                               10.7s 
 ✔ Container src-frontend-1        Recreated                                                0.7s 
 ✔ Container chatbot-rag-backend   Started                                                  1.0s 
 ✔ Container chatbot-rag-frontend  Started                                                  1.1s 
1d [ubuntu@mgc-dev-3090-01:~/cuong_dn/MiniProj_RAG3_RAG6_LegalChatbot_/src]└4 [base] main ± 

Điều này dẫn đến là: chạy docker compose của port 30001 thì bị mất 25007 và ngược lại. 

version: '3.8'

## Mô tả chi tiết và giải thích vấn đề: 

Tôi sẽ giải thích tại sao Docker hiển thị 4 container trong thông báo của bạn:

1. Có 2 cặp container được hiển thị vì cách Docker Compose đặt tên:

- Cặp 1:
  - `src-backend-1`
  - `chatbot-rag-backend`

- Cặp 2:  
  - `src-frontend-1`
  - `chatbot-rag-frontend`

Thực tế đây chỉ là 2 container, nhưng mỗi container có 2 cách đặt tên:

1. Tên tự động từ Docker Compose: `src-backend-1` và `src-frontend-1`
   - Được tạo từ tên thư mục (`src`) + tên service + số thứ tự

2. Tên được chỉ định trong file docker-compose.yml: `chatbot-rag-backend` và `chatbot-rag-frontend`
   - Được định nghĩa bởi thuộc tính `container_name` trong file của bạn

Vì vậy, khi Docker khởi động lại các container, nó hiển thị cả hai cách đặt tên cho mỗi container, tạo ra thông báo có 4 dòng dù thực tế chỉ có 2 container đang chạy.

Bạn có thể kiểm tra số container thực tế đang chạy bằng lệnh:
```bash
docker ps
```

  
# Nguyên nhân? 





Tôi thấy vấn đề rồi. Hệ thống của bạn có rất nhiều mạng Docker đã được tạo trước đó, bao gồm cả `src_app-network` và `src_RAG-network`. Đây chính là nguyên nhân gây ra xung đột.

Hãy thử một cách tiếp cận khác:

1. Đầu tiên, hãy xóa các mạng không sử dụng:

```bash
docker network prune -f
```

2. Sau đó, hãy sửa đổi cả hai file docker-compose.yml để sử dụng mạng bên ngoài (external network) thay vì tạo mạng mới:

```yaml:MiniProj_RAG3_RAG6_LegalChatbot_/src/docker-compose.yml
version: '3.8'

name: legal-chatbot

services:
  backend:
    build:
      context: ./back-end
      dockerfile: Dockerfile
    image: chatbot-rag-backend:latest
    container_name: chatbot-rag-backend
    ports:
      - "30000:30000"
    environment:
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - COLLECTION_NAME=${COLLECTION_NAME:-legal_rag}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - EMBEDDINGS_MODEL_NAME=${EMBEDDINGS_MODEL_NAME:-sentence-transformers/paraphrase-multilingual-mpnet-base-v2}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./back-end/.env:/app/.env
    restart: unless-stopped
    networks:
      - legal-chatbot-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:30000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    build:
      context: ./front-end
      dockerfile: Dockerfile
    image: chatbot-rag-frontend:latest
    container_name: chatbot-rag-frontend
    ports:
      - "30001:30001"
    volumes:
      - ./front-end/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    restart: unless-stopped
    networks:
      - legal-chatbot-network
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:30001"]
      interval: 20s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  legal-chatbot-network:
    name: legal-chatbot-network
```


```yaml:MiniProd_Web4_ContentEngFlow_StepUpE_T102024/1_srcContentGeneration/src/docker-compose.yml
version: '3.8'

name: content-generation

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    ports:
      - "3000:3000"
    volumes:
      - ./backend:/app:delegated
      - node_modules_backend:/app/node_modules
    environment:
      - NODE_ENV=production
      - CORS_ORIGIN=http://103.253.20.13:25007
    restart: unless-stopped
    networks:
      - content-gen-network
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/api/health', (r) => process.exit(r.statusCode > 299))"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    ports:
      - "25007:25007"
    volumes:
      - ./frontend:/app:delegated
      - node_modules_frontend:/app/node_modules
    environment:
      - NODE_ENV=production
      - BACKEND_URL=http://backend:3000
      - API_URL=http://backend:3000
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - content-gen-network
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:25007', (r) => process.exit(r.statusCode > 299))"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 40s

volumes:
  node_modules_backend:
  node_modules_frontend:

networks:
  content-gen-network:
    name: content-gen-network
```


3. Trước khi chạy docker-compose, hãy tạo trước các mạng này:

```bash
docker network create legal-chatbot-network
docker network create content-gen-network
```

4. Sau đó chạy lại docker-compose cho mỗi dự án:

```bash
# Trong thư mục MiniProj_RAG3_RAG6_LegalChatbot_/src
docker compose down -v
docker compose up -d

# Trong thư mục MiniProd_Web4_ContentEngFlow_StepUpE_T102024/1_srcContentGeneration/src
docker compose down -v
docker compose up -d
```

Cách tiếp cận này sẽ:
1. Sử dụng tên mạng cố định thay vì để Docker tự tạo tên
2. Tránh xung đột với các mạng hiện có
3. Đảm bảo mỗi dự án có mạng riêng biệt


# 3. Cách giải quyết? 


---


# Báo cáo chi tiết: Vấn đề xung đột Docker Compose và cách giải quyết

## 1. Mô tả vấn đề

Khi chạy hai ứng dụng Docker Compose khác nhau trong cùng một máy chủ, chúng ta gặp phải hiện tượng kỳ lạ: Docker hiển thị 4 container đang chạy, mặc dù mỗi ứng dụng chỉ nên có 2 container (backend và frontend). Cụ thể, Docker hiển thị:

```
[+] Running 4/4
 ✔ Container src-backend-1         Recreated                                               10.7s 
 ✔ Container src-frontend-1        Recreated                                                0.7s 
 ✔ Container chatbot-rag-backend   Started                                                  1.0s 
 ✔ Container chatbot-rag-frontend  Started                                                  1.1s 
```

## 2. Phân tích nguyên nhân

### 2.1. Vấn đề về tên container

Thực tế, chỉ có 2 container đang chạy, nhưng mỗi container có 2 cách đặt tên:

1. **Tên tự động từ Docker Compose**:
   - `src-backend-1` và `src-frontend-1`
   - Được tạo theo công thức: `<tên_thư_mục>_<tên_service>_<số_thứ_tự>`
   - Trong trường hợp này, thư mục là "src", dẫn đến tên container bắt đầu bằng "src-"

2. **Tên được chỉ định trong file docker-compose.yml**:
   - `chatbot-rag-backend` và `chatbot-rag-frontend`
   - Được định nghĩa bởi thuộc tính `container_name` trong file docker-compose.yml

Docker hiển thị cả hai cách đặt tên này trong thông báo, tạo ra ảo giác rằng có 4 container đang chạy.

### 2.2. Vấn đề về tên dự án

Cả hai ứng dụng đều nằm trong thư mục có tên là "src". Khi không có thuộc tính `name` trong file docker-compose.yml, Docker Compose sẽ sử dụng tên thư mục làm tên dự án. Điều này dẫn đến:

- Cả hai dự án đều có tên là "src"
- Docker Compose tạo ra các tên container tự động bắt đầu bằng "src-"
- Xung đột xảy ra khi cả hai dự án cố gắng tạo container với tên tương tự

### 2.3. Vấn đề về mạng Docker

Hệ thống đã có nhiều mạng Docker được tạo trước đó (33 mạng như đã liệt kê). Khi Docker Compose tạo mạng mới, nó sẽ:

1. Tạo tên mạng dựa trên tên dự án (ví dụ: `src_RAG-network`, `src_app-network`)
2. Cố gắng tìm dải địa chỉ IP không chồng chéo với các mạng hiện có
3. Gặp lỗi khi không thể tìm thấy dải địa chỉ IP phù hợp

## 3. Giải pháp chi tiết

### 3.1. Đặt tên rõ ràng cho mỗi dự án

Thêm thuộc tính `name` vào file docker-compose.yml:

```yaml
version: '3.8'
name: legal-chatbot  # hoặc content-generation
```

Lợi ích:
- Đặt tên cố định cho dự án, không phụ thuộc vào tên thư mục
- Tránh xung đột tên dự án giữa các ứng dụng
- Giúp Docker Compose tạo ra các tên container và mạng rõ ràng hơn

### 3.2. Sử dụng mạng có tên cố định

Thay đổi cấu hình mạng trong file docker-compose.yml:

```yaml
networks:
  legal-chatbot-network:  # hoặc content-gen-network
    name: legal-chatbot-network  # hoặc content-gen-network
```

Lợi ích:
- Đặt tên cố định cho mạng Docker, không phụ thuộc vào tên dự án
- Tránh xung đột tên mạng giữa các ứng dụng
- Dễ dàng quản lý và theo dõi các mạng Docker

### 3.3. Tạo mạng trước khi chạy Docker Compose

Trước khi chạy docker-compose, tạo trước các mạng:

```bash
docker network create legal-chatbot-network
docker network create content-gen-network
```

Lợi ích:
- Đảm bảo mạng đã tồn tại trước khi Docker Compose cố gắng sử dụng
- Tránh lỗi khi Docker Compose không thể tự động tạo mạng
- Cho phép kiểm soát cấu hình mạng (nếu cần)

### 3.4. Dọn dẹp tài nguyên không sử dụng

Thường xuyên dọn dẹp các mạng Docker không sử dụng:

```bash
docker network prune -f
```

Lợi ích:
- Giải phóng tài nguyên hệ thống
- Giảm khả năng xung đột giữa các mạng
- Làm sạch môi trường Docker

## 4. Quy trình triển khai đầy đủ

1. **Dừng tất cả các container hiện có**:
   ```bash
   docker compose down -v
   ```

2. **Dọn dẹp các mạng không sử dụng**:
   ```bash
   docker network prune -f
   ```

3. **Tạo mạng mới với tên cố định**:
   ```bash
   docker network create legal-chatbot-network
   docker network create content-gen-network
   ```

4. **Cập nhật file docker-compose.yml** cho cả hai dự án:
   - Thêm thuộc tính `name` cho dự án
   - Thay đổi tên mạng và cấu hình mạng
   - Đảm bảo các service sử dụng mạng mới

5. **Khởi động lại các dự án**:
   ```bash
   # Trong thư mục MiniProj_RAG3_RAG6_LegalChatbot_/src
   docker compose up -d
   
   # Trong thư mục MiniProd_Web4_ContentEngFlow_StepUpE_T102024/1_srcContentGeneration/src
   docker compose up -d
   ```

6. **Kiểm tra container đang chạy**:
   ```bash
   docker ps
   ```

7. **Kiểm tra mạng Docker**:
   ```bash
   docker network ls
   ```

## 5. Kết luận

Vấn đề xung đột trong Docker Compose thường xảy ra khi nhiều dự án được triển khai trên cùng một máy chủ mà không có sự phân biệt rõ ràng về tên dự án và tài nguyên. Bằng cách đặt tên rõ ràng cho dự án và mạng, chúng ta có thể tránh được các xung đột này và đảm bảo mỗi ứng dụng hoạt động độc lập.

Các thay đổi đã thực hiện không chỉ giải quyết vấn đề hiện tại mà còn cải thiện khả năng quản lý và bảo trì hệ thống trong tương lai. Đây là một bài học quan trọng về cách tổ chức và quản lý các dự án Docker Compose trong môi trường phức tạp.
