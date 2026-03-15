# Load Balancing

---

## 1. Load Balancer là gì?

Phân phối traffic đến nhiều servers để không server nào bị quá tải.

```
                    ┌─── Server 1
Client → LB ───────┼─── Server 2
                    └─── Server 3
```

---

## 2. Load Balancing Algorithms

### Round Robin
Lần lượt từng server. Đơn giản, fair khi servers giống nhau.

### Weighted Round Robin
Server mạnh hơn nhận nhiều requests hơn. VD: Server A (weight 3), Server B (weight 1) → A nhận 75%.

### Least Connections
Gửi đến server đang có ít connections nhất. Tốt khi requests có thời gian xử lý khác nhau.

### IP Hash
Hash IP của client → luôn route đến cùng 1 server. Tốt cho session affinity.

### Random
Chọn ngẫu nhiên. Đơn giản, hoạt động tốt khi server đồng đều.

---

## 3. Layer 4 vs Layer 7

### L4 (Transport Layer)
- Route dựa trên IP + port
- Nhanh hơn (không cần đọc content)
- Không biết HTTP headers, URL, cookies

### L7 (Application Layer)
- Route dựa trên content: URL path, headers, cookies
- Có thể route `/api/*` đến API servers, `/static/*` đến CDN
- Chậm hơn nhưng thông minh hơn

---

## 4. Health Checks

LB phải biết server nào còn sống:

- **Active**: LB gửi ping/HTTP request định kỳ đến mỗi server
- **Passive**: LB theo dõi responses, nếu server trả lỗi nhiều → đánh dấu unhealthy

Server unhealthy → LB ngừng gửi traffic → server recover → LB thêm lại.

---

## 5. Reverse Proxy vs Load Balancer

| | Reverse Proxy | Load Balancer |
|---|--------------|---------------|
| Mục đích chính | Bảo vệ & optimize | Phân phối traffic |
| SSL termination | Có | Có thể |
| Caching | Có | Thường không |
| Compression | Có | Thường không |
| Cần nhiều servers? | Không (1 server cũng dùng) | Có (>= 2 servers) |

**Thực tế**: Nginx, HAProxy, AWS ALB làm cả 2 vai trò.

---

## 6. Global Server Load Balancing (GSLB)

Load balancing across datacenters/regions:
- GeoDNS: route user đến datacenter gần nhất
- Anycast: cùng 1 IP nhưng nhiều locations
- Failover: nếu DC1 chết → route sang DC2

---

## Checklist Tự Kiểm Tra

- [ ] Chọn đúng LB algorithm cho từng scenario
- [ ] Phân biệt L4 vs L7 load balancing
- [ ] Giải thích health check hoạt động thế nào
- [ ] Biết khi nào cần reverse proxy vs load balancer
- [ ] Hiểu GSLB cho multi-region deployment
