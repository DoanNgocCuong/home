
D:\GIT\context-handling-bigmodule_PikaRobot_25112025\docs\4_TimeOut_Fallback_Alert


> Đây **không phải “một lỗi” duy nhất**, mà là một _nhóm lỗi/pattern_ thuộc lớp **Transport/Session** và **Resource exhaustion**: “half‑open (zombie) TCP connection / client abort / connection leak dẫn đến cạn worker & pool”

---

Đây **không phải “một lỗi” duy nhất**, mà là một _nhóm lỗi/pattern_ thuộc lớp **Transport/Session** và **Resource exhaustion**: “half‑open (zombie) TCP connection / client abort / connection leak dẫn đến cạn worker & pool”.[uvicorn+1](https://www.uvicorn.org/server-behavior/)​

## “Client không đóng connection đúng cách” là gì

Trong TCP/HTTP keep-alive, “đóng đúng” nghĩa là client kết thúc phiên bằng cơ chế đóng kết nối (FIN/ACK) hoặc ít nhất server phát hiện được peer đã chết và giải phóng tài nguyên.[wikipedia](https://en.wikipedia.org/wiki/TCP_half-open)​  
“Không đóng đúng cách” thường rơi vào các tình huống: client crash/mất mạng, timeout ở client rồi bỏ request, hoặc client không đọc hết response nên connection không được “drain/release” đúng quy trình.[wikipedia](https://en.wikipedia.org/wiki/TCP_half-open)​

## Tại sao nó làm server bị treo/504

Khi client biến mất hoặc bỏ request, server vẫn có thể giữ socket/connection ở trạng thái “còn sống” cho đến khi có tín hiệu rõ ràng (FIN/RST/timeout/keepalive detect), khiến tài nguyên (connection slot, file descriptor, worker) bị giữ lâu hơn dự kiến.[wikipedia](https://en.wikipedia.org/wiki/TCP_half-open)​  
Nếu tích tụ đủ nhiều connection kiểu này, server sẽ gặp **resource exhaustion** (cạn worker/connection) và bắt đầu timeout/504 hàng loạt (đây là failure biểu hiện ra ngoài).[uvicorn](https://www.uvicorn.org/server-behavior/)​

## `--timeout-keep-alive` và `--timeout-graceful-shutdown` thực sự là gì (Uvicorn)

- `--timeout-keep-alive <seconds>`: đóng các **Keep‑Alive connections** nếu _giữa các request_ không có dữ liệu mới trong khoảng thời gian đó; mặc định là 5 giây.[uvicorn](https://www.uvicorn.org/settings/)​
    
- `--timeout-graceful-shutdown <seconds>`: thời gian tối đa Uvicorn chờ để “shutdown êm” (đợi request đang xử lý hoàn tất); quá thời gian thì server bắt đầu terminate request.[uvicorn+1](https://www.uvicorn.org/settings/)​
    

## Chốt lại: “Đây là lỗi gì?”

Tên gọi thực chiến (DevOps/SRE hay dùng) cho case bạn mô tả thường là:

- **Half-open / zombie TCP connections** (một bên tưởng còn sống, bên kia đã chết/mất sync).[wikipedia](https://en.wikipedia.org/wiki/TCP_half-open)​
    
- **Connection leak / resource exhaustion** (hậu quả hệ thống: cạn worker/pool → timeout/504).[uvicorn](https://www.uvicorn.org/server-behavior/)​
    

Muốn “đặt tên” đúng theo log/triệu chứng của bạn thì cần 2 thứ: log error cụ thể (ECONNRESET/EPIPE/timeout?) và số liệu `ss -s`/`netstat` (ESTABLISHED/CLOSE_WAIT) tại thời điểm treo.

1. [https://www.uvicorn.org/server-behavior/](https://www.uvicorn.org/server-behavior/)
2. [https://en.wikipedia.org/wiki/TCP_half-open](https://en.wikipedia.org/wiki/TCP_half-open)
3. [https://www.uvicorn.org/settings/](https://www.uvicorn.org/settings/)
4. [https://stackoverflow.com/questions/70265343/python-fastapi-server-how-to-extend-connection-timeout](https://stackoverflow.com/questions/70265343/python-fastapi-server-how-to-extend-connection-timeout)
5. [https://github.com/encode/uvicorn/issues/716](https://github.com/encode/uvicorn/issues/716)
6. [https://github.com/encode/uvicorn/issues/669](https://github.com/encode/uvicorn/issues/669)
7. [https://github.com/benoitc/gunicorn/issues/1493](https://github.com/benoitc/gunicorn/issues/1493)
8. [https://www.linkedin.com/pulse/tcp-3-way-handshake-vs-half-open-lyacine-khima](https://www.linkedin.com/pulse/tcp-3-way-handshake-vs-half-open-lyacine-khima)
9. [https://github.com/Kludex/uvicorn/discussions/2578](https://github.com/Kludex/uvicorn/discussions/2578)
10. [https://bleepingcoder.com/gunicorn/218871310/clarify-what-how-timeout-and-graceful-timeout-work](https://bleepingcoder.com/gunicorn/218871310/clarify-what-how-timeout-and-graceful-timeout-work)
11. [https://sanchitgurukul.com/understanding-tcp-half-open-connections/](https://sanchitgurukul.com/understanding-tcp-half-open-connections/)
12. [https://stackoverflow.com/questions/77479479/uvicorn-no-response-after-275-seconds](https://stackoverflow.com/questions/77479479/uvicorn-no-response-after-275-seconds)
13. [https://github.com/encode/uvicorn/discussions/2098](https://github.com/encode/uvicorn/discussions/2098)
14. [https://community.f5.com/discussions/technicalforum/tcp-3-way-handshake-vs-tcp-half-open/263887](https://community.f5.com/discussions/technicalforum/tcp-3-way-handshake-vs-tcp-half-open/263887)
15. [https://www.reddit.com/r/webdev/comments/1e4xfn3/how_to_set_timeout_for_uvicorn_in_python_file/](https://www.reddit.com/r/webdev/comments/1e4xfn3/how_to_set_timeout_for_uvicorn_in_python_file/)
16. [https://github.com/Kludex/uvicorn/discussions/2257](https://github.com/Kludex/uvicorn/discussions/2257)
17. [https://github.com/encode/uvicorn/discussions/1660](https://github.com/encode/uvicorn/discussions/1660)
18. [https://github.com/encode/uvicorn/discussions/2281](https://github.com/encode/uvicorn/discussions/2281)
19. [https://en.wikipedia.org/wiki/Embryonic_connection](https://en.wikipedia.org/wiki/Embryonic_connection)
20. [https://manpages.ubuntu.com/manpages/focal/man1/uvicorn.1.html](https://manpages.ubuntu.com/manpages/focal/man1/uvicorn.1.html)


---



# Câu hỏi 1: trong phần code của mình có nginx đâu nhỉ

Đang kiểm tra cấu hình infrastructure (Docker Compose, K8s, reverse proxy) để xác định nơi cấu hình timeout:


[5 tools called]


Đang kiểm tra docker-compose để xem có reverse proxy/nginx:


[3 tools called]


Xác nhận: không có Nginx trong codebase. Docker compose chỉ expose Uvicorn trực tiếp qua port 30020.

## Phân tích setup hiện tại

Từ `docker-compose.prod.yml` và `Dockerfile`:
- Uvicorn chạy trực tiếp, không có reverse proxy
- Port 30020 được expose trực tiếp
- CMD: `uvicorn app.main_app:app --host 0.0.0.0 --port 30020 --reload`

## Nơi cấu hình timeout

### 1. Application level (Uvicorn) — trong codebase
File: `src/Dockerfile` (line 39)

```dockerfile
# ❌ CURRENT:
CMD ["uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "30020", "--reload"]

# ✅ SHOULD BE:
CMD ["uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "30020", "--timeout-keep-alive", "55", "--timeout-graceful-shutdown", "10"]
```

### 2. Cloud Load Balancer (nếu có) — ngoài codebase
- AWS ALB/NLB, GCP Load Balancer, Azure LB
- Config ở infrastructure/cloud console, không trong codebase

### 3. Client timeout (BE gọi đến) — ngoài codebase
- Timeout từ client (BE) khi gọi API của bạn

## ACTION 1.6 cập nhật (phù hợp với setup thực tế)

### ACTION 1.6: Configure Uvicorn timeout (REVISED)

Mức độ: P0 (Critical)  
File: `src/Dockerfile`  
Impact: Tránh 504 khi client timeout < app timeout

Implementation:

```dockerfile
# File: src/Dockerfile
# Line ~39

# ✅ CHANGE: Add timeout flags to Uvicorn
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \
     "--timeout-graceful-shutdown", "10", \
     "--no-reload"]  # ✅ Remove --reload in production
```

Lưu ý:
- `--timeout-keep-alive 55`: timeout cho keep-alive connections (55s)
- `--timeout-graceful-shutdown 10`: thời gian graceful shutdown (10s)
- `--no-reload`: bỏ `--reload` trong production (chỉ dùng cho dev)

Nếu dùng Gunicorn + Uvicorn workers (production):

```dockerfile
# Alternative: Use Gunicorn with Uvicorn workers (better for production)
CMD ["gunicorn", "app.main_app:app", \
     "--bind", "0.0.0.0:30020", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--timeout", "55", \
     "--graceful-timeout", "10", \
     "--keep-alive", "5"]
```

---

## Nếu có Load Balancer (Cloud/Infrastructure)

Nếu deploy lên Cloud (AWS/GCP/Azure) hoặc có Load Balancer riêng, cần config timeout ở đó:

### AWS ALB:
```yaml
# Infrastructure config (Terraform/CloudFormation)
resource "aws_lb_target_group" "api" {
  health_check_timeout = 10
  deregistration_delay = 10
}

resource "aws_lb_listener_rule" "api" {
  # Timeout: 60s (default, có thể tăng lên 60s)
}
```

### GCP Load Balancer:
```yaml
# Infrastructure config
backend:
  timeout_sec: 60
```

### Nginx (nếu tự setup):
```nginx
# File: nginx.conf (nếu bạn tự setup Nginx)
upstream api_backend {
    server api:30020;
}

server {
    location / {
        proxy_pass http://api_backend;
        proxy_read_timeout 60s;      # ✅ LB timeout: 60s
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
    }
}
```

---

## Tóm tắt: ACTION 1.6 (REVISED)

### Option A: Chỉ có Uvicorn (setup hiện tại)
- File: `src/Dockerfile`
- Thêm `--timeout-keep-alive 55` vào Uvicorn CMD
- Không cần Nginx config

### Option B: Có Cloud Load Balancer
- Config timeout ở Cloud Console (60s)
- Vẫn cần config Uvicorn timeout (55s) để có buffer

### Option C: Tự setup Nginx (tùy chọn)
- Tạo `nginx.conf` trong infrastructure repo
- Không cần trong app codebase

---

## Khuyến nghị

Với setup hiện tại (Uvicorn trực tiếp):
1. Ưu tiên: fix ACTION 1.6 trong `Dockerfile` (Uvicorn timeout)
2. Nếu có Load Balancer: hỏi DevOps/Infrastructure team về timeout config
3. Nếu không có LB: đảm bảo client (BE) có timeout >= 60s

Bạn có đang dùng Cloud Load Balancer (AWS/GCP/Azure) không, hay chỉ expose Uvicorn trực tiếp?

# Câu hỏi 2: "--timeout-keep-alive", "55", "--timeout-graceful-shutdown", "10"] LÀ GÌ


Giải thích 2 tham số timeout của Uvicorn:

## `--timeout-keep-alive` và `--timeout-graceful-shutdown`

### 1. `--timeout-keep-alive 55` (giây)

Là gì:
- Thời gian Uvicorn giữ kết nối HTTP mở sau khi request hoàn thành (keep-alive).
- Giúp tái sử dụng kết nối, tránh tạo kết nối mới cho mỗi request.

Ví dụ:
```
Client → Uvicorn: Request 1 (mất 2s)
         ↓
Client ← Uvicorn: Response 1 (2s)
         ↓
[Connection vẫn mở, chờ request tiếp theo]
         ↓
Client → Uvicorn: Request 2 (trong vòng 55s) ← Dùng lại connection cũ
         ↓
Client ← Uvicorn: Response 2
```

Tại sao 55 giây:
- Nếu client (BE) có timeout 60s, Uvicorn timeout 55s → có buffer 5s.
- Nếu Uvicorn timeout > client timeout → client sẽ 504 trước khi Uvicorn timeout.

Mặc định:
- Uvicorn không có timeout mặc định cho keep-alive (có thể giữ vô hạn).
- Nếu không set → connection có thể bị treo nếu client không đóng đúng cách.

---

### 2. `--timeout-graceful-shutdown 10` (giây)

Là gì:
- Thời gian Uvicorn chờ các request đang xử lý hoàn thành khi nhận tín hiệu shutdown (SIGTERM/SIGINT).
- Giúp tránh cắt đột ngột request đang chạy.

Ví dụ:
```
1. Uvicorn đang xử lý 5 requests:
   - Request A: đang chạy (2s)
   - Request B: đang chạy (3s)
   - Request C: đang chạy (1s)
   - Request D: đang chạy (8s) ← Chậm nhất
   - Request E: đang chạy (1s)

2. DevOps gửi: docker stop container (SIGTERM)

3. Uvicorn nhận SIGTERM:
   - ✅ Không nhận request mới
   - ✅ Chờ các request đang chạy hoàn thành
   - ⏱️ Timeout: 10 giây

4. Sau 10 giây:
   - Request A, B, C, E: ✅ Hoàn thành (trong 10s)
   - Request D: ❌ Bị kill (vượt 10s) → Client nhận 502/504
```

Tại sao 10 giây:
- Đủ để các request bình thường hoàn thành.
- Không quá dài để trì hoãn shutdown.

Mặc định:
- Uvicorn mặc định là 30 giây (có thể quá dài).

---

## So sánh: có vs không có timeout

### Scenario: Client timeout = 60s, Uvicorn không set timeout

```
Timeline:
0s:  Client gửi request → Uvicorn
5s:  Uvicorn đang xử lý (DB query chậm)
30s: DB query vẫn chạy (chưa xong)
60s: Client timeout → 504 Gateway Timeout
     ↓
     Nhưng Uvicorn vẫn đang chạy request đó!
     Connection vẫn mở, worker thread vẫn bị block
     ↓
65s: DB query xong, Uvicorn trả response
     ↓
     Nhưng client đã timeout rồi → Response bị bỏ qua
     Worker thread bị lãng phí
```

Vấn đề:
- Client đã timeout nhưng Uvicorn vẫn giữ connection/worker.
- Worker bị block → không xử lý request mới → dễ 504 hàng loạt.

---

### Scenario: Client timeout = 60s, Uvicorn `--timeout-keep-alive 55`

```
Timeline:
0s:  Client gửi request → Uvicorn
5s:  Uvicorn đang xử lý (DB query chậm)
30s: DB query vẫn chạy
55s: Uvicorn timeout → Đóng connection, kill request
     ↓
     Worker thread được giải phóng ngay
     Client nhận 504 (nhưng đúng lúc, không lãng phí worker)
```

Lợi ích:
- Worker được giải phóng sớm.
- Tránh giữ connection/thread không cần thiết.

---

## Liên quan đến vấn đề 504 của bạn

Vấn đề hiện tại:
- Service treo từ 23h đến 9h sáng → tất cả worker threads bị block.
- Không có timeout → worker chờ vô hạn → không xử lý request mới → 504.

Sau khi thêm timeout:
```python
# Dockerfile
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \      # ✅ Kill request sau 55s
     "--timeout-graceful-shutdown", "10"] # ✅ Shutdown nhanh hơn
```

Kết quả:
- Request chậm bị kill sau 55s → worker được giải phóng.
- Service không bị treo lâu → có thể xử lý request mới.

---

## Tóm tắt

| Tham số | Mục đích | Giá trị đề xuất | Ảnh hưởng đến 504 |
|---------|----------|-----------------|-------------------|
| `--timeout-keep-alive` | Giới hạn thời gian giữ connection mở | 55s | Quan trọng: giải phóng worker sớm |
| `--timeout-graceful-shutdown` | Thời gian chờ request hoàn thành khi shutdown | 10s | Ít ảnh hưởng: chỉ khi restart |

---

## Code thay đổi cụ thể

```dockerfile
# File: src/Dockerfile
# Line 39

# ❌ BEFORE (không có timeout):
CMD ["uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "30020", "--reload"]

# ✅ AFTER (có timeout):
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \
     "--timeout-graceful-shutdown", "10", \
     "--no-reload"]  # Bỏ --reload trong production
```

Lưu ý:
- `--timeout-keep-alive 55` là quan trọng nhất để tránh 504.
- `--timeout-graceful-shutdown 10` giúp shutdown nhanh hơn.
- Bỏ `--reload` trong production (chỉ dùng cho dev).

Bạn muốn tôi tạo PR/commit với thay đổi này không?


---
# Câu hỏi 3: client ko đóng đúng cách là sao nhỉ ?


```
# File: src/Dockerfile
# Line 39

# ❌ BEFORE (không có timeout):
CMD ["uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "30020", "--reload"]

# ✅ AFTER (có timeout):
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \
     "--timeout-graceful-shutdown", "10", \
     "--no-reload"]  # Bỏ --reload trong production
```


Giải thích "client không đóng connection đúng cách" và tại sao nó gây vấn đề:

## Client đóng connection đúng cách vs không đúng cách

### 1. Client đóng đúng cách (normal flow)

```
Timeline:
0s:  Client → Server: HTTP Request (POST /conversations/end)
     Connection: ESTABLISHED
     
2s:  Server → Client: HTTP Response (202 Accepted)
     Connection: KEEP-ALIVE (vẫn mở để tái sử dụng)
     
2.1s: Client đọc xong response
      Client → Server: TCP FIN (đóng connection)
      Server → Client: TCP ACK
      Connection: CLOSED ✅
```

Đặc điểm:
- Client gửi TCP FIN sau khi nhận response
- Server giải phóng connection ngay
- Worker thread được giải phóng

---

### 2. Client không đóng đúng cách (các trường hợp)

#### Case 1: Client crash/disconnect đột ngột (network issue)

```
Timeline:
0s:  Client → Server: HTTP Request (POST /conversations/end)
     Connection: ESTABLISHED
     
1s:  Server đang xử lý (DB query chậm...)
     
2s:  Client bị crash / mất mạng đột ngột
     ❌ Client KHÔNG gửi TCP FIN
     ❌ Server KHÔNG biết client đã mất
     
5s:  Server query xong, chuẩn bị gửi response
     Server → Client: HTTP Response (202 Accepted)
     ↓
     ❌ Không có client để nhận → Response bị drop
     ❌ Connection vẫn ở trạng thái "ESTABLISHED" (zombie connection)
     ❌ Worker thread vẫn bị block, chờ client đọc response
```

Vấn đề:
- Server không biết client đã mất
- Connection trở thành "zombie" (half-open)
- Worker thread bị block vô hạn

---

#### Case 2: Client timeout nhưng không đóng connection

```
Timeline:
0s:  Client → Server: HTTP Request
     Client timeout: 60s
     
30s: Server vẫn đang xử lý (DB query chậm)
     
60s: Client timeout → Client bỏ request
     ❌ Client KHÔNG gửi TCP FIN (vì đã timeout)
     ❌ Client chỉ bỏ request, không đóng connection
     
65s: Server query xong, gửi response
     Server → Client: HTTP Response
     ↓
     ❌ Client không đọc (đã timeout rồi)
     ❌ Connection vẫn mở, worker thread vẫn block
```

Vấn đề:
- Client timeout nhưng connection vẫn mở
- Server vẫn giữ connection và worker thread

---

#### Case 3: Client không đọc response body (lazy client)

```python
# ❌ BAD: Client code không đọc response
import requests

response = requests.post("http://api/v1/conversations/end", json=data, timeout=60)
# ❌ Không gọi response.close() hoặc response.raise_for_status()
# ❌ Connection vẫn mở, chờ client đọc response body
```

Vấn đề:
- Client nhận response nhưng không đọc hết body
- Server chờ client đọc → connection bị giữ

---

#### Case 4: Client dùng connection pool nhưng không release

```python
# ❌ BAD: Client code
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post("http://api/v1/conversations/end", json=data)
    # ❌ Không await response.aread() hoặc response.aclose()
    # ❌ Connection trong pool không được release
```

Vấn đề:
- Connection trong pool không được release
- Pool cạn → không thể tạo connection mới

---

## Tại sao gây vấn đề cho server

### Vấn đề 1: Worker thread bị block

```
Server có 4 worker threads:

Thread 1: ✅ Xử lý request A (2s) → Done → Free
Thread 2: ❌ Xử lý request B (client crash) → Blocked forever
Thread 3: ❌ Xử lý request C (client timeout) → Blocked forever  
Thread 4: ❌ Xử lý request D (client lazy) → Blocked forever

Request E mới đến: ❌ Không có worker available → 504 Timeout
Request F mới đến: ❌ Không có worker available → 504 Timeout
...
```

Kết quả:
- Tất cả worker bị block → service không thể xử lý request mới → 504 hàng loạt

---

### Vấn đề 2: Connection pool cạn kiệt

```
Server có connection pool: 50 connections

Connection 1-10: ✅ Normal requests → Released
Connection 11-20: ❌ Zombie connections (client crash)
Connection 21-30: ❌ Zombie connections (client timeout)
Connection 31-40: ❌ Zombie connections (client lazy)
Connection 41-50: ✅ Normal requests → Released

Request mới: ❌ Không có connection available → Chờ timeout → 504
```

Kết quả:
- Pool cạn → request mới không lấy được connection → 504

---

## Cách phòng tránh (server-side)

### 1. Thêm `--timeout-keep-alive` (quan trọng nhất)

```dockerfile
CMD ["uvicorn", "app.main_app:app", \
     "--timeout-keep-alive", "55"]  # ✅ Force đóng connection sau 55s
```

Cách hoạt động:
```
Timeline:
0s:  Client → Server: Request
30s: Server đang xử lý
55s: Uvicorn timeout → Server tự động đóng connection
     ✅ Worker thread được giải phóng
     ✅ Connection được release
```

---

### 2. Thêm timeout cho DB query

```python
# File: src/app/db/database_connection.py
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "options": "-c statement_timeout=10000"  # ✅ 10s query timeout
    }
)
```

Cách hoạt động:
```
Timeline:
0s:  Client → Server: Request
5s:  DB query bắt đầu
15s: DB query timeout → Exception → Response 500
     ✅ Worker thread được giải phóng ngay
     ✅ Connection được đóng
```

---

### 3. Thêm timeout cho HTTP client (nếu gọi external API)

```python
# File: src/app/services/utils/llm_analysis_utils.py
async with httpx.AsyncClient(timeout=15.0) as client:
    response = await client.post(...)
    # ✅ Timeout sau 15s → Exception → Worker được giải phóng
```

---

## Ví dụ cụ thể: vấn đề của bạn

### Scenario: Service treo từ 23h đến 9h sáng

Có thể xảy ra:

```
23:00: Nightly Job bắt đầu → Gửi 10,000 requests
23:01: 100 requests đang xử lý
       - 50 requests: DB query chậm (30s mỗi request)
       - 30 requests: Client timeout (60s) nhưng connection vẫn mở
       - 20 requests: Client crash/disconnect đột ngột
       
23:02: Tất cả 100 worker threads bị block:
       - 50 threads: Chờ DB query (không có timeout)
       - 30 threads: Chờ client đọc response (client đã timeout)
       - 20 threads: Chờ client đóng connection (client đã crash)
       
23:03: Request mới đến → ❌ Không có worker available → 504
23:04: Request mới đến → ❌ Không có worker available → 504
...
09:00: Admin restart service → ✅ Worker threads được giải phóng
```

---

## Giải pháp tổng hợp

### 1. Server-side (bạn có thể fix)

```dockerfile
# ✅ Fix 1: Uvicorn timeout
CMD ["uvicorn", "app.main_app:app", \
     "--timeout-keep-alive", "55"]
```

```python
# ✅ Fix 2: DB query timeout
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"options": "-c statement_timeout=10000"}
)
```

```python
# ✅ Fix 3: RabbitMQ timeout
self.connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        socket_timeout=5,  # ✅ 5s timeout
        blocked_connection_timeout=5
    )
)
```

### 2. Client-side (bạn không thể fix, nhưng có thể document)

```python
# ✅ GOOD: Client code nên làm
import httpx

async with httpx.AsyncClient(timeout=60.0) as client:
    response = await client.post("http://api/v1/conversations/end", json=data)
    await response.aread()  # ✅ Đọc hết response body
    response.raise_for_status()  # ✅ Check status
    # ✅ Connection tự động đóng khi ra khỏi context
```

---

## Tóm tắt

"Client không đóng connection đúng cách" có thể là:
1. Client crash/disconnect đột ngột → không gửi TCP FIN
2. Client timeout nhưng không đóng connection
3. Client không đọc response body → connection bị giữ
4. Client dùng connection pool nhưng không release

Hậu quả:
- Worker threads bị block vô hạn
- Connection pool cạn kiệt
- Service không thể xử lý request mới → 504

Giải pháp:
- Thêm timeout ở mọi layer (Uvicorn, DB, RabbitMQ, External API)
- Timeout sẽ force đóng connection → giải phóng worker → tránh 504

Bạn muốn tôi tạo checklist các timeout cần thêm không?