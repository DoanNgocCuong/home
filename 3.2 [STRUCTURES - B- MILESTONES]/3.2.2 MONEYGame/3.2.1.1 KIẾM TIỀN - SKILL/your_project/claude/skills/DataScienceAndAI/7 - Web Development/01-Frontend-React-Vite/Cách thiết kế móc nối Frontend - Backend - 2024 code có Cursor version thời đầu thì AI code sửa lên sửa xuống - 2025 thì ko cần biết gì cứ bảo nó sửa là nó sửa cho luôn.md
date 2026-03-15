# Logic Host và Port - 0.0.0.0 vs localhost

## Tổng quan

Giải thích logic khi chạy với `0.0.0.0` ở local và trên server.

## `0.0.0.0` là gì?

`0.0.0.0` = **Bind vào tất cả network interfaces**

### Ở Local (Development)

- ✅ Có thể truy cập từ:
  - `http://localhost:8000`
  - `http://127.0.0.1:8000`
  - `http://192.168.x.x:8000` (IP local của máy)
- ✅ Cho phép các thiết bị khác trong cùng mạng truy cập
- ⚠️ Frontend **KHÔNG thể** dùng `http://0.0.0.0:8000` (browser không hiểu)

### Ở Server (Production)

- ✅ **BẮT BUỘC** dùng `0.0.0.0` để expose ra ngoài
- ✅ Cho phép truy cập từ IP public: `http://103.253.20.30:30015`
- ⚠️ Frontend phải dùng IP public, không dùng `0.0.0.0`

## Logic hiện tại

### Backend (Python/FastAPI)

```python
# app.py
uvicorn.run(app, host='0.0.0.0', port=8000)
```

**Kết quả:**

- Backend bind vào `0.0.0.0:8000`
- Có thể truy cập từ nhiều địa chỉ khác nhau

### Frontend (JavaScript)

```javascript
// js/data.js
// Detect environment và chọn URL phù hợp
if (hostname === 'localhost') {
    // Local: dùng localhost (KHÔNG dùng 0.0.0.0)
    API_BASE = 'http://localhost:8000/api';
} else {
    // Server: dùng production URL
    API_BASE = 'http://103.253.20.30:30015/api';
}
```

## Scenarios

### Scenario 1: Chạy Local (Development)

**Backend:**

```bash
python app.py --host 0.0.0.0 --port 8000
# Hoặc từ .env: API_HOST=0.0.0.0 API_PORT=8000
```

**Frontend:**

- Mở `index.html` từ `file://` hoặc web server
- Frontend detect `localhost` → dùng `http://localhost:8000/api`
- ✅ Hoạt động tốt

**Có thể truy cập:**

- `http://localhost:8000` (từ chính máy)
- `http://192.168.1.100:8000` (từ máy khác trong mạng)

### Scenario 2: Chạy trên Server (Production)

**Backend:**

```bash
python app.py --host 0.0.0.0 --port 30015
# Hoặc từ .env: API_HOST=0.0.0.0 API_PORT=30015
```

**Frontend:**

- Deploy lên server hoặc serve từ server
- Frontend detect không phải `localhost` → dùng production URL
- ✅ Hoạt động tốt

**Có thể truy cập:**

- `http://103.253.20.30:30015` (từ bất kỳ đâu)

### Scenario 3: Frontend và Backend cùng server

**Backend:**

```bash
python app.py --host 0.0.0.0 --port 8000
```

**Frontend:**

- Serve từ cùng server (ví dụ: nginx serve static files)
- Frontend detect hostname → dùng relative path hoặc same origin
- ✅ Hoạt động tốt

## Cấu hình .env

### Local Development

```env
API_HOST=0.0.0.0          # Cho phép access từ network
API_PORT=8000
API_PRODUCTION_URL=http://103.253.20.30:30015
```

### Production Server

```env
API_HOST=0.0.0.0          # BẮT BUỘC để expose ra ngoài
API_PORT=30015
API_PRODUCTION_URL=http://103.253.20.30:30015
```

## Lưu ý quan trọng

1. **Backend luôn dùng `0.0.0.0`** (cả local và server)

   - Local: vẫn OK, cho phép access từ network
   - Server: bắt buộc để expose ra ngoài
2. **Frontend KHÔNG BAO GIỜ dùng `0.0.0.0`**

   - Browser không hiểu `0.0.0.0`
   - Local: dùng `localhost` hoặc `127.0.0.1`
   - Server: dùng IP public hoặc domain
3. **Auto-detection**

   - Frontend tự động detect environment
   - Local → `localhost:port`
   - Server → production URL từ config

## Troubleshooting

### Lỗi: "Failed to fetch" khi frontend gọi API

**Nguyên nhân:**

- Frontend đang dùng `0.0.0.0` (sai)
- Hoặc CORS chưa được enable

**Giải pháp:**

- Kiểm tra `API_BASE` trong console
- Đảm bảo dùng `localhost` ở local, IP public ở server
- Kiểm tra CORS trong `app.py`

### Backend không accessible từ máy khác

**Nguyên nhân:**

- Đang dùng `localhost` thay vì `0.0.0.0`

**Giải pháp:**

- Đổi sang `0.0.0.0` trong `.env` hoặc command line
- Kiểm tra firewall


---



# Cấu hình từ .env File

## Tổng quan

Hệ thống đọc cấu hình từ file `.env` ở root project (`D:\GIT\Fintech\fintech\.env`).

## Cách hoạt động

1. **Backend (Python)** đọc `.env` file và expose config qua API endpoint `/api/config`
2. **Frontend (JavaScript)** gọi API để lấy config thay vì hard code

## File .env

Tạo file `.env` ở `D:\GIT\Fintech\fintech\.env` với nội dung:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_PRODUCTION_URL=http://YOUR_SERVER_IP:30015

# Database Configuration (REQUIRED)
DB_HOST=YOUR_DB_HOST
DB_PORT=29990
DB_NAME=financial-reporting-database
DB_USER=postgres
DB_PASSWORD=postgres
```

## Các biến môi trường

### API Configuration

- `API_HOST`: Host để bind API server (default: `0.0.0.0`)
- `API_PORT`: Port để bind API server (default: `8000`)
- `API_PRODUCTION_URL`: Production API URL cho frontend (**REQUIRED** - không có default)

### Database Configuration (**REQUIRED**)

**BẮT BUỘC** phải có trong .env:

- `DB_HOST`: Database host (**REQUIRED**)
- `DB_PORT`: Database port (default: `29990`)
- `DB_NAME`: Database name (default: `financial-reporting-database`)
- `DB_USER`: Database user (default: `postgres`)
- `DB_PASSWORD`: Database password (default: `postgres`)

## API Endpoint

### GET /api/config

Trả về config cho frontend:

```json
{
  "success": true,
  "config": {
    "api_base_url": "http://YOUR_SERVER_IP:30015",
    "api_local_url": "http://localhost:8000"
  }
}
```

## Frontend

Frontend tự động gọi `/api/config` khi load để lấy API base URL. Nếu không thể kết nối, sẽ fallback về default detection.

## Priority

1. `.env` file (nếu có)
2. Environment variables (nếu có)
3. **Không có defaults** - Bắt buộc phải config trong .env

## ⚠️ QUAN TRỌNG

- **DB_HOST**: BẮT BUỘC phải có trong .env, không có default
- **API_PRODUCTION_URL**: Nên có trong .env, nếu không sẽ dùng localhost (development mode)
- Tất cả config đều đọc từ .env, **KHÔNG có hard code IP/URL trong code**

## Lưu ý

- File `.env` nên được thêm vào `.gitignore` để không commit sensitive data
- Production URL được expose cho frontend, không expose database credentials