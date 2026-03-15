# Plan: Thêm API Key Authentication Layer

## Context

Cần thêm 1 lớp bảo mật API key vào toàn bộ API endpoints để:

- Xác thực giữa các service nội bộ
- Chặn truy cập từ bên ngoài không được authorize

## Requirements

1. **Static API Key trong header**: `X-API-Key: CnzZNw4NXknHObpFuLXqoDqAEjNXwWpI`
2. **Cờ bật/tắt trong .env**:
    - `API_KEY_ENABLED=false`: Cho phép request đi qua nhưng **alert lên Google Chat**
    - `API_KEY_ENABLED=true`: **Bắt buộc** phải có API key hợp lệ, không có thì reject (401)
3. **Apply cho tất cả API endpoints**

## Implementation Approach

### 1. Thêm config vào `app/common/config.py`

Thêm 2 biến mới:

```python
API_KEY_ENABLED: bool = False  # Mặc định tắt (dev)
API_KEY: str = "CnzZNw4NXknHObpFuLXqoDqAEjNXwWpI"
```

### 2. Tạo middleware mới `app/middleware.py`

Thêm `APIKeyMiddleware`:

- Đọc header `X-API-Key`
- Nếu `API_KEY_ENABLED=true`:
    - Không có key → reject 401 Unauthorized
    - Key sai → reject 401 Unauthorized
- Nếu `API_KEY_ENABLED=false`:
    - Không có key → alert lên Google Chat (AlertType: AUTH_FAILURE)
    - Key sai → alert lên Google Chat (AlertType: AUTH_FAILURE)
    - Request vẫn cho đi qua (warn level)

### 3. Đăng ký middleware trong `app/server.py`

Thêm vào `make_middleware()`:

```python
Middleware(APIKeyMiddleware)
```

### 4. Update `.env`

Thêm:

```
API_KEY_ENABLED=false
```

## Files to Modify

|File|Changes|
|---|---|
|`app/common/config.py`|Thêm `API_KEY_ENABLED`, `API_KEY`|
|`app/middleware.py`|Thêm `APIKeyMiddleware` class|
|`app/server.py`|Đăng ký middleware mới|
|`.env`|Thêm `API_KEY_ENABLED=false`|

## Verification

1. Test với `API_KEY_ENABLED=false`:
    
    - Gọi API không có header → 200 OK + alert lên Google Chat
    - Gọi API với sai key → 200 OK + alert lên Google Chat
    - Gọi API với đúng key → 200 OK + không alert
2. Test với `API_KEY_ENABLED=true`:
    
    - Gọi API không có header → 401 Unauthorized
    - Gọi API với sai key → 401 Unauthorized
    - Gọi API với đúng key → 200 OK