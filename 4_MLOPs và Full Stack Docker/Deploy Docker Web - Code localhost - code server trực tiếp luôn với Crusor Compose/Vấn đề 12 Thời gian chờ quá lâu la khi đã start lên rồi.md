
# Báo cáo: Phân tích lỗi Docker container bị treo

# Vấn đề: 
- Sau khi container compose build xong được Image, nhưng không up và không run được container (cụ thể là mất quá nhiều thời gian). 1 số cách đã thử fix  [Mặc dù run riêng backend, frontend ở localhost thì được, docker compose lại không được]
1. Giảm thời gian chờ và thậm chí bỏ bước check health? 
2. Cho Cursor Composer để sửa cách viết của Dockerfile và cách viết của docker compose 
3. Bị treo hoài mỗi lần muốn run lại phải xoá terminal hiện tại đi 
4. Thêm file ngix, .. vẫn không được 

## Nguyên nhân
Container Docker bị treo trong quá trình khởi động do xung đột cổng (port conflict). Port 25050 đã bị chiếm bởi các tiến trình đang chạy trên máy host:

1. Một server uvicorn (PID: 54474)
2. Một tiến trình Python (PID: 54506) 
3. Các kết nối Node.js (PID: 15297)

## Cách khắc phục
Để giải quyết vấn đề, chúng ta đã dừng các tiến trình đang chiếm port bằng một trong hai cách:

```bash
# Cách 1: Kill trực tiếp theo PID
sudo kill -9 54474 54506 15297

# Cách 2: Kill theo tên tiến trình
sudo pkill -f uvicorn
sudo pkill -f python
sudo pkill -f node
```

Sau khi giải phóng port 25050, container đã có thể khởi động thành công.

## Biện pháp phòng tránh
Để tránh tình trạng tương tự trong tương lai, cần:

1. Kiểm tra các port đang được sử dụng trước khi chạy container:
```bash
sudo lsof -i :25050
```

2. Đảm bảo tắt các service local đang chạy trên các port mà container cần sử dụng

3. Hoặc có thể điều chỉnh port mapping trong file docker-compose.yml để tránh xung đột với các service local

## Kết luận
Đây là một vấn đề phổ biến khi làm việc với Docker. Việc quản lý port và kiểm tra xung đột là rất quan trọng để đảm bảo container có thể khởi động thành công.


---


# Phân tích cấu trúc server và vấn đề xung đột

## Cấu trúc hiện tại
Dựa vào file `docker-compose.yml`, hệ thống gồm 2 service chính:

1. **Backend Service**
```yaml
backend:
    ports:
      - "25050:25050"    # Map port 25050 của host vào container
    environment:
      - CORS_ORIGINS=http://localhost:25051,http://frontend:80,...
    command: uvicorn main:app --host 0.0.0.0 --port 25050
```

2. **Frontend Service**
```yaml
frontend:
    ports:
      - "25051:80"       # Map port 25051 của host vào port 80 của container
    environment:
      - VITE_BACKEND_URL=http://103.253.20.13:25050
```

## Nguyên nhân xung đột
Vấn đề xảy ra do có nhiều instance của service đang chạy cùng lúc:

1. **Local Development Environment:**
   - Có uvicorn server đang chạy trực tiếp trên máy host (port 25050)
   - Có Node.js development server cho frontend (có thể đang kết nối đến port 25050)

2. **Docker Environment:**
   - Container backend cũng cần sử dụng port 25050
   - Không thể bind port vì đã bị chiếm bởi local services

## Quy trình dẫn đến xung đột

1. Developer chạy services locally để development
```bash
# Terminal 1
cd backend
uvicorn main:app --reload    # Chiếm port 25050

# Terminal 2
cd frontend
npm run dev                  # Tạo các kết nối đến backend
```

2. Sau đó cố gắng deploy bằng Docker
```bash
docker compose up --build -d  # Không thể bind port 25050
```

## Giải pháp tổng thể

1. **Quản lý môi trường rõ ràng:**
   - Tạo script để dừng tất cả local services trước khi chạy Docker
   - Sử dụng các port khác nhau cho development và Docker

2. **Cải thiện Docker Compose:**
```yaml
services:
  backend:
    ports:
      - "${BACKEND_PORT:-25050}:25050"    # Có thể config port qua env
    environment:
      - PORT=25050
```

3. **Tạo startup script:**
```bash
#!/bin/bash
# stop-local-services.sh

# Kiểm tra và dừng các service đang chạy
echo "Stopping local services..."
pkill -f uvicorn
pkill -f node

# Kiểm tra port
if lsof -i :25050; then
    echo "Port 25050 is still in use"
    exit 1
fi

# Start Docker services
docker compose up -d
```

Việc hiểu rõ cấu trúc này giúp tránh được các xung đột tương tự trong tương lai và quản lý deployment hiệu quả hơn.
