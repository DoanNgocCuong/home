# Networking Basics cho System Design

---

## 1. HTTP/HTTPS

Giao thức nền tảng của web. Client gửi request, server trả response.

### HTTP Methods
- **GET**: lấy data (đọc)
- **POST**: tạo mới
- **PUT**: cập nhật toàn bộ
- **PATCH**: cập nhật 1 phần
- **DELETE**: xóa

### Status Codes cần nhớ
- **2xx**: thành công (200 OK, 201 Created)
- **3xx**: redirect (301 Moved, 304 Not Modified)
- **4xx**: lỗi client (400 Bad Request, 401 Unauthorized, 404 Not Found, 429 Too Many Requests)
- **5xx**: lỗi server (500 Internal Error, 502 Bad Gateway, 503 Service Unavailable)

---

## 2. TCP vs UDP

| | TCP | UDP |
|---|-----|-----|
| Kết nối | Connection-oriented (3-way handshake) | Connectionless |
| Tin cậy | Guaranteed delivery, ordering | Best-effort, có thể mất gói |
| Tốc độ | Chậm hơn (overhead) | Nhanh hơn |
| Use case | Web, email, file transfer | Video streaming, gaming, DNS |

---

## 3. DNS (Domain Name System)

Chuyển đổi domain name → IP address. Như "danh bạ điện thoại" của internet.

```
Browser → Local DNS Cache → ISP DNS → Root DNS → TLD DNS → Authoritative DNS → IP
```

**Tại sao quan trọng cho System Design?**
- DNS-based load balancing
- GeoDNS: route user đến server gần nhất
- DNS caching: giảm latency

---

## 4. WebSocket

HTTP là request-response (1 chiều tại 1 thời điểm). WebSocket là full-duplex (2 chiều đồng thời).

```
HTTP:      Client ──request──> Server
           Client <──response── Server

WebSocket: Client <────────────> Server (luôn mở)
```

**Khi nào dùng WebSocket?**
- Chat real-time
- Live notifications
- Collaborative editing (Google Docs)
- Live sports scores

---

## 5. API Design Patterns

### REST
- Resource-based URLs: `/users/123/orders`
- Stateless: mỗi request chứa đủ info
- Dùng HTTP methods chuẩn
- Phổ biến nhất, dễ hiểu

### GraphQL
- 1 endpoint duy nhất
- Client chọn chính xác fields cần lấy
- Giảm over-fetching / under-fetching
- Phức tạp hơn REST

### gRPC
- Dùng Protocol Buffers (binary, không JSON)
- Cực nhanh, low latency
- Phù hợp microservices giao tiếp nội bộ
- Hỗ trợ streaming

### Khi nào dùng gì?
- **REST**: public API, CRUD đơn giản, mobile/web clients
- **GraphQL**: frontend cần flexibility, nhiều data sources
- **gRPC**: service-to-service, cần performance cao

---

## 6. Long Polling vs Server-Sent Events vs WebSocket

| | Long Polling | SSE | WebSocket |
|---|------------|-----|-----------|
| Direction | Client → Server | Server → Client | Bi-directional |
| Connection | Repeated HTTP | Single HTTP | Persistent TCP |
| Complexity | Thấp | Thấp | Trung bình |
| Use case | Simple updates | Live feed, notifications | Chat, gaming |

---

## Checklist Tự Kiểm Tra

- [ ] Phân biệt GET vs POST khi nào dùng
- [ ] Giải thích 3-way handshake của TCP
- [ ] Vẽ được flow DNS resolution
- [ ] Biết khi nào dùng WebSocket vs Long Polling
- [ ] So sánh REST vs GraphQL vs gRPC với use case cụ thể
