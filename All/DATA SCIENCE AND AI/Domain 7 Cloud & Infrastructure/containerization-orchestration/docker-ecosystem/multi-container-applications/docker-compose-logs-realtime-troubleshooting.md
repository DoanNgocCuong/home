# Docker Compose Logs Real-time Troubleshooting

## 🚨 Vấn đề
- Chạy `docker compose logs -f` nhưng không xem được log real-time
- Service tự động shutdown sau khi xử lý request
- Log hiển thị: `INFO: Shutting down` → `INFO: Application shutdown complete`

## 🔍 Nguyên nhân
**Service tự động shutdown vì thiếu database connection!**

```yaml
environment:
  PG_DATABASE: ""  # ❌ Rỗng
  PG_HOST: ""      # ❌ Rỗng  
  PG_PASSWORD: ""  # ❌ Rỗng
  PG_PORT: ""      # ❌ Rỗng
  PG_USER: ""      # ❌ Rỗng
```

## ✅ Giải pháp
1. **Cung cấp đầy đủ database credentials** trong environment variables
2. **Restart service** với cấu hình mới
3. **Service giờ chạy liên tục** thay vì tắt sau mỗi request

## 🎯 Kết quả
- `docker compose logs -f` hoạt động bình thường
- Có thể xem log real-time liên tục
- Service không còn tự động shutdown

## 📚 Bài học
- **Docker logs real-time chỉ hoạt động khi service đang chạy liên tục**
- **Environment variables thiếu → service crash → không xem được log real-time**
- **Luôn kiểm tra cấu hình database trước khi debug logs**

## 🔧 Commands hữu ích
```bash
# Xem logs real-time
docker compose logs -f [service_name]

# Kiểm tra status services
docker compose ps

# Restart service
docker compose restart [service_name]

# Xem environment variables
docker compose config
```

