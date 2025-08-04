Đây là các lệnh khác để kiểm tra port 3099 đã được sử dụng bằng grep:

**1. Sử dụng netstat với grep:**
```bash
netstat -tulpn | grep :3099
```

**2. Sử dụng ss với grep:**
```bash
ss -tulpn | grep :3099
```

**3. Kiểm tra tất cả kết nối và lọc bằng grep:**
```bash
netstat -an | grep 3099
```

**4. Sử dụng ss để kiểm tra listening ports:**
```bash
ss -ln | grep :3099
```

**5. Kiểm tra process đang sử dụng port:**
```bash
netstat -tlnp | grep :3099
```

**Giải thích các tham số:**
- `t`: TCP connections
- `u`: UDP connections  
- `l`: listening ports
- `n`: hiển thị số port thay vì tên service
- `p`: hiển thị process ID và tên
- `a`: tất cả connections

Lệnh phổ biến nhất là `netstat -tulpn | grep :3099` để xem process nào đang sử dụng port 3099.