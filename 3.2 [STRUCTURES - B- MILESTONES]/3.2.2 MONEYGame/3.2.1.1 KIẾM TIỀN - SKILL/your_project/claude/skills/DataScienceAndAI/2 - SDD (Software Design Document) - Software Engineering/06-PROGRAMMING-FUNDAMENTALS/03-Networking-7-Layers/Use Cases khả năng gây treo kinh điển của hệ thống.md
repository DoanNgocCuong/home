

Dưới đây là bảng MECE phân loại **7 Layer OSI** theo tính chất "Phần Cứng" vs "Phần Mềm" dưới góc độ một người làm **Backend/DevOps** thường gặp.

## Bảng Phân Tầng OSI: Phần Cứng vs Phần Mềm (Góc Nhìn Thực Chiến)

|Tầng OSI|Tên (Layer)|Bản chất (Nature)|Đối tượng quản lý chính|Ví dụ lỗi thường gặp|
|---|---|---|---|---|
|**L7**|**Application**|**100% Phần Mềm**|Ứng dụng, Code, Protocol logic|- HTTP 500/502/503/504  <br>- DNS failure  <br>- API Error/Logic Bug|
|**L6**|**Presentation**|**100% Phần Mềm**|Thư viện mã hóa, Encoding|- SSL/TLS Handshake fail  <br>- Cert hết hạn/không tin cậy  <br>- JSON decode error|
|**L5**|**Session**|**100% Phần Mềm**|Quản lý phiên kết nối|- Half-open connection  <br>- Keep-alive timeout  <br>- Auth session expired|
|**L4**|**Transport**|**Chủ yếu Phần Mềm**  <br>_(OS Kernel TCP Stack)_|Hệ điều hành, Socket Config|- Broken Pipe (EPIPE)  <br>- Connection Reset (ECONNRESET)  <br>- Port Exhaustion (hết port)|
|**L3**|**Network**|**Lai (Hybrid)**  <br>_(Router ảo/thật, Firewall)_|Cloud VPC / NetAdmin / OS Routing|- Host Unreachable (EHOSTUNREACH)  <br>- Blocked by Firewall/Security Group  <br>- Sai IP/Routing Table|
|**L2**|**Data Link**|**Chủ yếu Phần Cứng**  <br>_(NIC, Switch, Driver)_|Network Engineer / Datacenter|- Packet Loss do nghẽn switch  <br>- ARP Storm  <br>- MAC Address duplicate|
|**L1**|**Physical**|**100% Phần Cứng**|Technician / Infra Team|- Đứt cáp quang  <br>- Mất điện  <br>- Hỏng cổng mạng vật lý|

## Cách dùng bảng này để khoanh vùng (Troubleshooting Flow)

1. **L7 (App)**: Check log ứng dụng trước ("Tại sao trả về 504? Code có bug không?").
    
2. **L6 (TLS)**: Nếu L7 chưa tới nơi, check HTTPS/Cert ("Cert có lỗi không? Handshake fail không?").
    
3. **L4 (TCP)**: Nếu TLS cũng chưa tới, check socket ("Có bị timeout kết nối không? Bị reset connection không?").
    
4. **L3 (Net)**: Nếu không kết nối được socket, check network ("Ping được IP đó không? Firewall có chặn không?").
    
5. **L1/L2**: Nếu cả network cũng chết hẳn, mới đẩy ticket cho đội hạ tầng (Infra/NetOps) kiểm tra cáp/switch.
    

Bạn có muốn thêm cột "Cách Fix Nhanh" cho từng dòng không?

1. [https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/760047/c34df809-5a99-4afb-bb0a-7fab5465093d/paste.txt](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/760047/c34df809-5a99-4afb-bb0a-7fab5465093d/paste.txt)


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


---

Working…

Tôi sẽ hoàn thiện bảng OSI MECE còn dở bằng kiến thức chuẩn và ví dụ thực chiến Backend/DevOps.

Searching

network error types classification

software error categories troubleshooting

TCP connection errors EPIPE ECONNRESET

Reviewing sources · 20

[

![viblo.asia favicon](https://www.google.com/s2/favicons?sz=128&domain=viblo.asia)

Hiểu về OSI Model - 7 Tầng Mạng - Viblo

viblo



](https://viblo.asia/p/hieu-ve-osi-model-7-tang-mang-018J2qKR4YK)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Types of Errors in Computer Network - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/computer-networks/types-of-errors-in-computer-network/)

[

![obkio.com favicon](https://www.google.com/s2/favicons?sz=128&domain=obkio.com)

What is a Network Error? Resolving 12 Common Network ... - Obkio

obkio



](https://obkio.com/blog/network-errors/)

[

![blog.ploeh.dk favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.ploeh.dk)

Error categories and category errors - ploeh blog

blog.ploeh



](https://blog.ploeh.dk/2024/01/29/error-categories-and-category-errors/)

[

![scribd.com favicon](https://www.google.com/s2/favicons?sz=128&domain=scribd.com)

Types of Errors | PDF | Computer Network - Scribd

scribd



](https://www.scribd.com/document/846024878/types-of-errors)

[

![docs.oracle.com favicon](https://www.google.com/s2/favicons?sz=128&domain=docs.oracle.com)

Chapter 38 Troubleshooting Software Problems (Overview)

docs.oracle



](https://docs.oracle.com/cd/E19455-01/805-7229/6j6q8svhf/index.html)

[

![github.com favicon](https://www.google.com/s2/favicons?sz=128&domain=github.com)

ECONNRESET · Issue #2227 · discordjs/discord.js

github



](https://github.com/discordjs/discord.js/issues/2227)

[

![thinkcomputers.org favicon](https://www.google.com/s2/favicons?sz=128&domain=thinkcomputers.org)

3 types of network errors you may encounter in data communication

thinkcomputers



](https://thinkcomputers.org/3-types-of-network-errors-you-may-encounter-in-data-communication/)

[

![jotform.com favicon](https://www.google.com/s2/favicons?sz=128&domain=jotform.com)

7 types of software bugs and errors | The Jotform Blog

jotform



](https://www.jotform.com/blog/types-of-software-bug/)

[

![groups.google.com favicon](https://www.google.com/s2/favicons?sz=128&domain=groups.google.com)

How do you get ECONNRESET on recv?

groups.google



](https://groups.google.com/g/comp.unix.programmer/c/La0DzXtKzB8)

[

![websitepulse.com favicon](https://www.google.com/s2/favicons?sz=128&domain=websitepulse.com)

Error types - WebSitePulse

websitepulse



](https://www.websitepulse.com/kb/error_types)

[

![alooba.com favicon](https://www.google.com/s2/favicons?sz=128&domain=alooba.com)

Software Troubleshooting: Everything You Need to Know ... - Alooba

alooba



](https://www.alooba.com/skills/cognitive-abilities/technical-troubleshooting-387/software-troubleshooting/)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

ECONNRESET in Send Linux C

stackoverflow



](https://stackoverflow.com/questions/33053507/econnreset-in-send-linux-c)

[

![fiveable.me favicon](https://www.google.com/s2/favicons?sz=128&domain=fiveable.me)

Error Detection and Correction in Networks | Systems Approach to ...

fiveable



](https://fiveable.me/computer-networks-a-systems-approach/unit-13)

[

![codoid.com favicon](https://www.google.com/s2/favicons?sz=128&domain=codoid.com)

Troubleshooting 101: Differentiating Bugs, Errors, and Issues - Codoid

codoid



](https://codoid.com/software-testing/differentiating-bugs-errors-issues/)

[

ECONNRESET not returned when calling send() on a socket

mail-index.netbsd



](http://mail-index.netbsd.org/netbsd-users/2019/09/22/msg023447.html)

[

![dspmuranchi.ac.in favicon](https://www.google.com/s2/favicons?sz=128&domain=dspmuranchi.ac.in)

[PDF] unit 3: error and their types

dspmuranchi.ac



](https://dspmuranchi.ac.in/pdf/Blog/error%20and%20types.pdf)

[

![blog.codacy.com favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.codacy.com)

10 Common Programming Errors and How to Avoid Them

blog.codacy



](https://blog.codacy.com/common-programming-errors)

[

![forums.meteor.com favicon](https://www.google.com/s2/favicons?sz=128&domain=forums.meteor.com)

Error: read ECONNRESET - help

forums.meteor



](https://forums.meteor.com/t/error-read-econnreset/56299)

[

![jetbrains.com favicon](https://www.google.com/s2/favicons?sz=128&domain=jetbrains.com)

Handling Specific Types of Errors - JetBrains Guide

jetbrains



](https://www.jetbrains.com/guide/go/tutorials/handle_errors_in_go/specific_errors/)

Tìm kiếm thêm lỗi kết nối zombie, leak và EHOSTUNREACH để bổ sung bảng OSI thực chiến.

Searching

zombie connection half-open TCP

connection leak software engineering

EHOSTUNREACH network error meaning

Reviewing sources · 19

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

Is there a way to detect that TCP socket has been closed by ...

stackoverflow



](https://stackoverflow.com/questions/17705239/is-there-a-way-to-detect-that-tcp-socket-has-been-closed-by-the-remote-peer-wit)

[

![github.com favicon](https://www.google.com/s2/favicons?sz=128&domain=github.com)

Dealing with half-opened TCP connections · Issue #622

github



](https://github.com/vibe-d/vibe.d/issues/622)

[

![docs.netscaler.com favicon](https://www.google.com/s2/favicons?sz=128&domain=docs.netscaler.com)

Frequently Asked Questions | Solutions for Telecom Service ...

docs.netscaler



](https://docs.netscaler.com/en-us/citrix-adc/current-release/citrix-adc-support-for-telecom-service-providers/NS_TCP_optimization/ns_tcp_opt_faqs.html)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

TCP half-open

en.wikipedia



](https://en.wikipedia.org/wiki/TCP_half-open)

[

![blog.patoliyainfotech.com favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.patoliyainfotech.com)

Optimizing Software: Connection Leak Mastery

blog.patoliyainfotech



](https://blog.patoliyainfotech.com/how-to-deal-with-connection-leak/)

[

![groups.google.com favicon](https://www.google.com/s2/favicons?sz=128&domain=groups.google.com)

what is the difference between EHOSTUNREACH and ...

groups.google



](https://groups.google.com/g/comp.os.vxworks/c/LLs8ngIBZDU)

[

![sunnyjovita.blog.binusian.org favicon](https://www.google.com/s2/favicons?sz=128&domain=sunnyjovita.blog.binusian.org)

TCP Half Open Port Scan or SYN scan - Sunny's Blog

sunnyjovita.blog.binusian



](https://sunnyjovita.blog.binusian.org/2021/05/05/tcp-half-open-port-scan-or-syn-scan/)

[

![blog.ycrash.io favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.ycrash.io)

Chaos Engineering – DB Connection Leak

blog.ycrash



](https://blog.ycrash.io/chaos-engineering-db-connection-leak/)

[

ARC Error: connect EHOSTUNREACH

community.roonlabs



](https://community.roonlabs.com/t/arc-error-connect-ehostunreach/224601)

[

![youtube.com favicon](https://www.google.com/s2/favicons?sz=128&domain=youtube.com)

Connection Termination | TCP/IP Course 2025 - #Video42

youtube



](https://www.youtube.com/watch?v=3mtWe5swDc8)

[

![softwareatscale.dev favicon](https://www.google.com/s2/favicons?sz=128&domain=softwareatscale.dev)

Mitigate Connection Leaks in Production via Proxies

softwareatscale



](https://www.softwareatscale.dev/p/mitigate-connection-leaks-in-production)

[

![reddit.com favicon](https://www.google.com/s2/favicons?sz=128&domain=reddit.com)

Help for "Error: connect EHOSTUNREACH"

reddit



](https://www.reddit.com/r/RASPBERRY_PI_PROJECTS/comments/suoytx/help_for_error_connect_ehostunreach/)

[

Understanding FortiDDoS Prevention Mode

help.fortinet



](https://help.fortinet.com/fddos/4-3-0/FortiDDoS/Understanding_FortiDDoS_Prevention_Mode.htm)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

How to handle connection leaks in JDBC?

geeksforgeeks



](https://www.geeksforgeeks.org/java/how-to-handle-connection-leaks-in-jdbc/)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

node.js - EHOSTUNREACH error with nodemailer

stackoverflow



](https://stackoverflow.com/questions/33904902/ehostunreach-error-with-nodemailer)

[

![savannah.nongnu.org favicon](https://www.google.com/s2/favicons?sz=128&domain=savannah.nongnu.org)

bug #50837: TCP: zero window probe doesn't timeout

savannah.nongnu



](https://savannah.nongnu.org/bugs/?50837)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

Database connection leak - java

stackoverflow



](https://stackoverflow.com/questions/43070991/database-connection-leak)

[

![github.com favicon](https://www.google.com/s2/favicons?sz=128&domain=github.com)

Error: connect EHOSTUNREACH 192.168.21.34:22

github



](https://github.com/mscdex/ssh2/issues/1428)

[

![ibm.com favicon](https://www.google.com/s2/favicons?sz=128&domain=ibm.com)

Connection leak or ConnectionWaitTimeoutException ...

ibm



](https://www.ibm.com/support/pages/connection-leak-or-connectionwaittimeoutexception-when-using-asynchronous-beans-websphere-application-server)

Tìm kiếm phân loại lỗi phần mềm, tầng OSI và loại lỗi tạm thời/bền vững để hoàn thiện bảng.

Searching

software fault error failure taxonomy

network error classification OSI layer

transient intermittent permanent errors

Reviewing sources · 19

[

![buildsoftwaresystems.com favicon](https://www.google.com/s2/favicons?sz=128&domain=buildsoftwaresystems.com)

Illustrative Explanation of Fault, Error, Failure, bug, and Defect in ...

buildsoftwaresystems



](https://buildsoftwaresystems.com/post/fault-error-failure-bug-defect-software-explained/)

[

![scribd.com favicon](https://www.google.com/s2/favicons?sz=128&domain=scribd.com)

Error and Fault Taxonomy | PDF | Software Bug - Scribd

scribd



](https://www.scribd.com/presentation/608290382/Error-and-Fault-Taxonomy)

[

![decodo.com favicon](https://www.google.com/s2/favicons?sz=128&domain=decodo.com)

What is Error Taxonomy? Definition - Decodo

decodo



](https://decodo.com/glossary/error-taxonomy)

[

![emergentmind.com favicon](https://www.google.com/s2/favicons?sz=128&domain=emergentmind.com)

Failure Modes Taxonomy - Emergent Mind

emergentmind



](https://www.emergentmind.com/topics/taxonomy-of-failure-modes)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Network Layer in OSI Model - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/computer-networks/network-layer-in-osi-model/)

[

![hima.com favicon](https://www.google.com/s2/favicons?sz=128&domain=hima.com)

Dependable Systems: Errors, Faults and Failures - HIMA: Smart Safety

hima



](https://www.hima.com/en/shareandexplore/dependable_systems_errors_faults_failures)

[

![sciencedirect.com favicon](https://www.google.com/s2/favicons?sz=128&domain=sciencedirect.com)

Software Fault - an overview | ScienceDirect Topics

sciencedirect



](https://www.sciencedirect.com/topics/computer-science/software-fault)

[

![talent500.com favicon](https://www.google.com/s2/favicons?sz=128&domain=talent500.com)

What is OSI Model - 7 Layers of OSI Model - Talent500

talent500



](https://talent500.com/blog/what-is-osi-model-and-its-layers/)

[

Ubiquity: Software fault tolerance through run-time fault detection

ubiquity.acm



](https://ubiquity.acm.org/article.cfm?id=1115546)

[

![grottke.de favicon](https://www.google.com/s2/favicons?sz=128&domain=grottke.de)

[PDF] A Classification of Software Faults

grottke



](https://www.grottke.de/documents/AClassificationOfSWFaults.pdf)

[

![studocu.vn favicon](https://www.google.com/s2/favicons?sz=128&domain=studocu.vn)

OSI Model: Understanding the 7 Layers of Network Architecture

studocu



](https://www.studocu.vn/vn/document/truong-dai-hoc-bach-khoa-ha-noi/ky-thuat-dien/osi-model-understanding-the-7-layers-of-network-architecture/135398428)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Fault Tolerance in Distributed System - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/computer-networks/fault-tolerance-in-distributed-system/)

[

![blog.tentamen.eu favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.tentamen.eu)

Context For Software Fault, Error And Failure Classification

blog.tentamen



](https://blog.tentamen.eu/context-for-software-fault-error-and-failure-classification/)

[

![reddit.com favicon](https://www.google.com/s2/favicons?sz=128&domain=reddit.com)

OSI Model - Problems by layer? : r/sysadmin - Reddit

reddit



](https://www.reddit.com/r/sysadmin/comments/19brp4r/osi_model_problems_by_layer/)

[

![sciencedirect.com favicon](https://www.google.com/s2/favicons?sz=128&domain=sciencedirect.com)

Transient Fault - an overview | ScienceDirect Topics

sciencedirect



](https://www.sciencedirect.com/topics/computer-science/transient-fault)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

OSI model - Wikipedia

en.wikipedia



](https://en.wikipedia.org/wiki/OSI_model)

[

![baeldung.com favicon](https://www.google.com/s2/favicons?sz=128&domain=baeldung.com)

Fault and Failure in Distributed Systems - Baeldung

baeldung



](https://www.baeldung.com/cs/distributed-systems-fault-failure)

[

What is the OSI Model? Key Facts About the 7 OSI Layers ... - vnetwork

vnetwork



](https://www.vnetwork.vn/en-US/news/mo-hinh-osi-la-gi/)

[

![en.eeworld.com.cn favicon](https://www.google.com/s2/favicons?sz=128&domain=en.eeworld.com.cn)

A brief discussion on functional safety - fault, error, and failure

en.eeworld.com



](https://en.eeworld.com.cn/news/qcdz/eic683954.html)

Tìm kiếm lỗi cạn kiệt tài nguyên, phân loại timeout và lỗi Byzantine để hoàn thiện bảng OSI thực chiến.

Searching

resource exhaustion error software

timeout error types classification

Byzantine fault distributed systems

Reviewing sources · 19

[

![learn.microsoft.com favicon](https://www.google.com/s2/favicons?sz=128&domain=learn.microsoft.com)

Resource Exhaustion Detected Windows 11 - Microsoft Q&A

learn.microsoft



](https://learn.microsoft.com/en-us/answers/questions/4019236/resource-exhaustion-detected-windows-11)

[

![community.spiceworks.com favicon](https://www.google.com/s2/favicons?sz=128&domain=community.spiceworks.com)

Microsoft-Windows-Resource-Exhaustion-Detector ...

community.spiceworks



](https://community.spiceworks.com/t/microsoft-windows-resource-exhaustion-detector-memory-leak/759553)

[

![twingate.com favicon](https://www.google.com/s2/favicons?sz=128&domain=twingate.com)

What is Resource Exhaustion in cybersecurity?

twingate



](https://www.twingate.com/blog/glossary/resource-exhaustion)

[

![cloud.google.com favicon](https://www.google.com/s2/favicons?sz=128&domain=cloud.google.com)

Learn how to handle 429 resource exhaustion errors in ...

cloud.google



](https://cloud.google.com/blog/products/ai-machine-learning/learn-how-to-handle-429-resource-exhaustion-errors-in-your-llms)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

java - What is the best exception type to use for an I/O timeout?

stackoverflow



](https://stackoverflow.com/questions/41069899/what-is-the-best-exception-type-to-use-for-an-i-o-timeout)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Byzantine Fault Tolerance in Distributed System - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/system-design/byzantine-fault-tolerance-in-distributed-system/)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

wordpress - What is the reason for the error ...

stackoverflow



](https://stackoverflow.com/questions/41457363/what-is-the-reason-for-the-error-resource-exhausted)

[

![realpython.com favicon](https://www.google.com/s2/favicons?sz=128&domain=realpython.com)

TimeoutError | Python's Built-in Exceptions

realpython



](https://realpython.com/ref/builtin-exceptions/timeouterror/)

[

![designgurus.io favicon](https://www.google.com/s2/favicons?sz=128&domain=designgurus.io)

What are Byzantine faults and how do they impact distributed system ...

designgurus



](https://www.designgurus.io/answers/detail/what-are-byzantine-faults-and-how-do-they-impact-distributed-system-design)

[

![groups.google.com favicon](https://www.google.com/s2/favicons?sz=128&domain=groups.google.com)

Error StatusCode=ResourceExhausted, Detail="Resource ...

groups.google



](https://groups.google.com/g/adwords-api/c/1jESbqgPSLg)

[

Timeout Errors - TechDocs - Broadcom Inc.

techdocs.broadcom



](https://techdocs.broadcom.com/us/en/ca-enterprise-software/it-operations-management/spectrum/22-2/managing-network/service-performance-manager/troubleshooting-service-performance-manager/timeout-errors.html)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Byzantine Failure in System Design - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/system-design/byzantine-failure-in-system-design/)

[

![reddit.com favicon](https://www.google.com/s2/favicons?sz=128&domain=reddit.com)

Windows 10 - Resource Exhaustion Detector Warning ...

reddit



](https://www.reddit.com/r/techsupport/comments/jli58v/windows_10_resource_exhaustion_detector_warning/)

[

![developer.mozilla.org favicon](https://www.google.com/s2/favicons?sz=128&domain=developer.mozilla.org)

408 Request Timeout - HTTP - MDN Web Docs

developer.mozilla



](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/408)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

Byzantine fault - Wikipedia

en.wikipedia



](https://en.wikipedia.org/wiki/Byzantine_fault)

[

![youtube.com favicon](https://www.google.com/s2/favicons?sz=128&domain=youtube.com)

Why Do Programs Experience Resource Exhaustion Errors?

youtube



](https://www.youtube.com/watch?v=pK_iso3HyJU)

[

![docs.oracle.com favicon](https://www.google.com/s2/favicons?sz=128&domain=docs.oracle.com)

TimeoutException (Java Platform SE 8 ) - Oracle Help Center

docs.oracle



](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeoutException.html)

[

![maddevs.io favicon](https://www.google.com/s2/favicons?sz=128&domain=maddevs.io)

What Is Byzantine fault tolerance system? | System Design Glossary

maddevs



](https://maddevs.io/glossary/byzantine-fault-tolerance-system/)

[

![forums.tomshardware.com favicon](https://www.google.com/s2/favicons?sz=128&domain=forums.tomshardware.com)

Resource-Exhaustion (No Memory)

forums.tomshardware



](https://forums.tomshardware.com/threads/resource-exhaustion-no-memory.3022369/)

Tìm kiếm phân loại race condition, deadlock, memory leak và cascading failure để bổ sung bảng OSI thực chiến.

Searching

race condition deadlock livelock classification

memory leak vs connection leak software

cascading failure distributed systems

Reviewing sources · 19

[

![viblo.asia favicon](https://www.google.com/s2/favicons?sz=128&domain=viblo.asia)

009: Deadlock, Livelock, Abandoned lock và Starvation - Viblo

viblo



](https://viblo.asia/p/009-deadlock-livelock-abandoned-lock-va-starvation-1VgZvVmmZAw)

[

![designgurus.io favicon](https://www.google.com/s2/favicons?sz=128&domain=designgurus.io)

Deadlock vs Livelock: Key Differences and How to Prevent Both

designgurus



](https://www.designgurus.io/blog/deadlock-vs-livelock)

[

Livelock same as race condition? (Threads forum at Coderanch)

coderanch



](https://coderanch.com/t/516325/java/Livelock-race-condition)

[

![dev.to favicon](https://www.google.com/s2/favicons?sz=128&domain=dev.to)

Multithreading | Handling Race Conditions and Deadlocks in C++

dev



](https://dev.to/shreyosghosh/multithreading-handling-race-conditions-and-deadlocks-in-c-4ae4)

[

![middleware.io favicon](https://www.google.com/s2/favicons?sz=128&domain=middleware.io)

Why Developers Fear Memory Leaks? And How You Can Beat.

middleware



](https://middleware.io/blog/memory-leaks/)

[

![linkedin.com favicon](https://www.google.com/s2/favicons?sz=128&domain=linkedin.com)

Cascading Failures in Distributed Systems - LinkedIn

linkedin



](https://www.linkedin.com/pulse/cascading-failures-distributed-systems-yeshwanth-n)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

What's the difference between deadlock and livelock? - Stack Overflow

stackoverflow



](https://stackoverflow.com/questions/6155951/whats-the-difference-between-deadlock-and-livelock)

[

![browserless.io favicon](https://www.google.com/s2/favicons?sz=128&domain=browserless.io)

Memory Leak: How to Find, Fix & Prevent Them

browserless



](https://www.browserless.io/blog/memory-leak-how-to-find-fix-prevent-them)

[

![infoq.com favicon](https://www.google.com/s2/favicons?sz=128&domain=infoq.com)

How to Avoid Cascading Failures in Distributed Systems - InfoQ

infoq



](https://www.infoq.com/articles/anatomy-cascading-failure/)

[

![baeldung.com favicon](https://www.google.com/s2/favicons?sz=128&domain=baeldung.com)

Deadlock, Livelock and Starvation | Baeldung on Computer Science

baeldung



](https://www.baeldung.com/cs/deadlock-livelock-starvation)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

Memory leak

en.wikipedia



](https://en.wikipedia.org/wiki/Memory_leak)

[

![blog.mi.hdm-stuttgart.de favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.mi.hdm-stuttgart.de)

Cascading failures in large-scale distributed systems

blog.mi.hdm-stuttgart



](https://blog.mi.hdm-stuttgart.de/index.php/2022/03/03/cascading-failures-in-large-scale-distributed-systems/)

[

![linkedin.com favicon](https://www.google.com/s2/favicons?sz=128&domain=linkedin.com)

Race conditions, deadlock, and livelock - Java Tutorial - LinkedIn

linkedin



](https://www.linkedin.com/learning/java-se-11-developer-1z0-819-cert-prep/race-conditions-deadlock-and-livelock)

[

![stackoverflow.com favicon](https://www.google.com/s2/favicons?sz=128&domain=stackoverflow.com)

Memory leaks in Java: database connection in multiple ...

stackoverflow



](https://stackoverflow.com/questions/23525209/memory-leaks-in-java-database-connection-in-multiple-methods)

[

![robertovitillo.com favicon](https://www.google.com/s2/favicons?sz=128&domain=robertovitillo.com)

How distributed systems fail | Roberto's blog

robertovitillo



](https://robertovitillo.com/how-distributed-systems-fail/)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

Deadlock (computer science) - Wikipedia

en.wikipedia



](https://en.wikipedia.org/wiki/Deadlock_\(computer_science\))

[

![payara.fish favicon](https://www.google.com/s2/favicons?sz=128&domain=payara.fish)

Preventing Memory Leaks with JDBC Connection Pool ...

payara



](https://payara.fish/blog/preventing-memory-leaks-with-jdbc-connection-pool-management/)

[

![sre.google favicon](https://www.google.com/s2/favicons?sz=128&domain=sre.google)

Cascading Failures: Reducing System Outage - Google SRE

sre



](https://sre.google/sre-book/addressing-cascading-failures/)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Conditions for Deadlock in Operating System - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/operating-systems/conditions-for-deadlock-in-operating-system/)

Tìm kiếm phân loại lỗi lỗi hỏng sự cố theo IEEE, khuyết điểm phần mềm và phân vùng mạng split-brain để hoàn thiện bảng OSI.

Searching

error fault failure taxonomy IEEE

software defect classification

network partition split brain

Reviewing sources · 18

[

A Reliability-oriented Faults Taxonomy and a Recovery ...

ieeexplore.ieee



](https://ieeexplore.ieee.org/document/9842572/)

[

![ieee.org favicon](https://www.google.com/s2/favicons?sz=128&domain=ieee.org)

January 2025 IEEE Taxonomy Version 1.05

ieee



](https://www.ieee.org/content/dam/ieee-org/ieee/web/org/pubs/ieee-taxonomy.pdf)

[

IEEE Standard Classification for Software Anomalies

ctestlabs



](https://www.ctestlabs.org/neoacm/1044_2009.pdf)

[

![scribd.com favicon](https://www.google.com/s2/favicons?sz=128&domain=scribd.com)

Classification of Defects | PDF | Software Bug | Error - Scribd

scribd



](https://www.scribd.com/document/102097768/Classification-of-Defects)

[

![docs.hazelcast.org favicon](https://www.google.com/s2/favicons?sz=128&domain=docs.hazelcast.org)

13.8. Network Partitioning (Split-Brain Syndrome)

docs.hazelcast



](https://docs.hazelcast.org/docs/2.0/manual/html/ch13s08.html)

[

Empirical Validation of a Web Fault Taxonomy and its ...

ieeexplore.ieee



](https://ieeexplore.ieee.org/servlet/Login?logout=%2Fdocument%2F4380241%2F)

[

Software Defect Classification and Analysis Study - IEEE Xplore

ieeexplore.ieee



](https://ieeexplore.ieee.org/iel8/10667475/10667476/10667506.pdf)

[

![youtube.com favicon](https://www.google.com/s2/favicons?sz=128&domain=youtube.com)

Network Partitions & Split-Brain Explained for Beginners - YouTube

youtube



](https://www.youtube.com/watch?v=Z1c1DihLX1k)

[

Dependability Concepts and Taxonomy - IEEE Xplore

ieeexplore.ieee



](https://ieeexplore.ieee.org/document/10529160/)

[

![kualitatem.com favicon](https://www.google.com/s2/favicons?sz=128&domain=kualitatem.com)

A Beginner's Guide to Software Defect Classification - Kualitatem

kualitatem



](https://www.kualitatem.com/blog/software-testing/defects-priority-severity-levels/)

[

Split-Brain Problem: Prevention and Resolution

systemdr.substack



](https://systemdr.substack.com/p/split-brain-problem-prevention-and)

[

IEEE Standard Classification for Software Anomalies.

ieeexplore.ieee



](https://ieeexplore.ieee.org/iel1/3112/8904/00392549.pdf)

[

![testingmind.com favicon](https://www.google.com/s2/favicons?sz=128&domain=testingmind.com)

20 Types of Software Defects Every Tester Should Know - testingmind

testingmind



](https://www.testingmind.com/20-types-of-software-defects-every-tester-should-know/)

[

![docs.redhat.com favicon](https://www.google.com/s2/favicons?sz=128&domain=docs.redhat.com)

Chapter 43. Handling Network Partitions (Split Brain) | 7.1

docs.redhat



](https://docs.redhat.com/en/documentation/red_hat_data_grid/7.1/html/administration_and_configuration_guide/handling_network_partitions_split_brain)

[

![sciencedirect.com favicon](https://www.google.com/s2/favicons?sz=128&domain=sciencedirect.com)

Fault classification and localization of multi-machine-based ...

sciencedirect



](https://www.sciencedirect.com/science/article/pii/S0378779624007430)

[

![tutorialspoint.com favicon](https://www.google.com/s2/favicons?sz=128&domain=tutorialspoint.com)

STLC - Defect Classification - Tutorials Point

tutorialspoint



](https://www.tutorialspoint.com/stlc/stlc_defect_classification.htm)

[

![45drives.com favicon](https://www.google.com/s2/favicons?sz=128&domain=45drives.com)

What is Split brain and why do you need to worry about it? - 45Drives

45drives



](https://www.45drives.com/community/articles/what-is-split-brain/)

[

![dl.acm.org favicon](https://www.google.com/s2/favicons?sz=128&domain=dl.acm.org)

Taxonomy of real faults in deep learning systems

dl.acm



](https://dl.acm.org/doi/10.1145/3377811.3380395)

Tìm kiếm retry storm, circuit breaker và graceful degradation để bổ sung ví dụ lỗi thực chiến OSI.

Searching

retry storm thundering herd problem

circuit breaker pattern error handling

graceful degradation vs fail fast

Reviewing sources · 19

[

![learn.microsoft.com favicon](https://www.google.com/s2/favicons?sz=128&domain=learn.microsoft.com)

Retry Storm Antipattern - Azure Architecture Center

learn.microsoft



](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/)

[

![en.wikipedia.org favicon](https://www.google.com/s2/favicons?sz=128&domain=en.wikipedia.org)

Thundering herd problem

en.wikipedia



](https://en.wikipedia.org/wiki/Thundering_herd_problem)

[

Thundering herds, noisy neighbours, and retry storms

blog.mads-hartmann



](https://blog.mads-hartmann.com/sre/2021/05/14/thundering-herd.html)

[

![youtube.com favicon](https://www.google.com/s2/favicons?sz=128&domain=youtube.com)

Mitigating Thundering Herds and Retry Storms

youtube



](https://www.youtube.com/watch?v=RAyvEqtrjpE)

[

Circuit Breaker Pattern for Error Handling and Dependency Failures

amitprakash



](https://www.amitprakash.me/blog/circuit-breaker-pattern-error-handling-dependency-failures)

[

Graceful Degradation vs. Fail Fast - by Systems

systemdr.substack



](https://systemdr.substack.com/p/graceful-degradation-vs-fail-fast)

[

![linkedin.com favicon](https://www.google.com/s2/favicons?sz=128&domain=linkedin.com)

Relevance of The Thundering Herd Problem in Disaster ...

linkedin



](https://www.linkedin.com/pulse/relevance-thundering-herd-problem-disaster-recovery-strategies-bapat-sszbc)

[

![youtube.com favicon](https://www.google.com/s2/favicons?sz=128&domain=youtube.com)

What Is The Circuit Breaker Error Handling Pattern? - YouTube

youtube



](https://www.youtube.com/watch?v=iKah9nociyE)

[

![jrothman.com favicon](https://www.google.com/s2/favicons?sz=128&domain=jrothman.com)

Graceful Degradation is Not What We Want; Quick Failure ...

jrothman



](https://www.jrothman.com/mpd/project-management/2009/06/graceful-degradation-is-not-what-we-want/)

[

![designgurus.io favicon](https://www.google.com/s2/favicons?sz=128&domain=designgurus.io)

How do you mitigate the thundering herd problem?

designgurus



](https://www.designgurus.io/answers/detail/how-do-you-mitigate-the-thundering-herd-problem)

[

![dev.to favicon](https://www.google.com/s2/favicons?sz=128&domain=dev.to)

Avoiding Meltdowns in Microservices: The Circuit Breaker Pattern

dev



](https://dev.to/lovestaco/avoiding-meltdowns-in-microservices-the-circuit-breaker-pattern-5666)

[

![fastly.com favicon](https://www.google.com/s2/favicons?sz=128&domain=fastly.com)

Fastly's Principles of Fault Isolation and Graceful Degradation

fastly



](https://www.fastly.com/blog/design-for-chaos-fastlys-principles-of-fault-isolation-and-graceful)

[

![dev.to favicon](https://www.google.com/s2/favicons?sz=128&domain=dev.to)

When APIs Fail: A Developer's Journey with Retries, Back ...

dev



](https://dev.to/kengowada/when-apis-fail-a-developers-journey-with-retries-back-off-and-jitter-1g2f)

[

![aerospike.com favicon](https://www.google.com/s2/favicons?sz=128&domain=aerospike.com)

The Circuit Breaker Pattern | Aerospike Documentation

aerospike



](https://aerospike.com/docs/develop/tutorials/circuit-breaker/)

[

![uberconf.com favicon](https://www.google.com/s2/favicons?sz=128&domain=uberconf.com)

Graceful Degradation is Not What We Want; Quick Failure ...

uberconf



](https://uberconf.com/blog/johanna_rothman/2009/06/graceful_degradation_is_not_what_we_want_quick_failure_is_better)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

Retries Strategies in Distributed Systems

geeksforgeeks



](https://www.geeksforgeeks.org/system-design/retries-strategies-in-distributed-systems/)

[

![geeksforgeeks.org favicon](https://www.google.com/s2/favicons?sz=128&domain=geeksforgeeks.org)

What is Circuit Breaker Pattern in Microservices? - GeeksforGeeks

geeksforgeeks



](https://www.geeksforgeeks.org/system-design/what-is-circuit-breaker-pattern-in-microservices/)

[

![codereliant.io favicon](https://www.google.com/s2/favicons?sz=128&domain=codereliant.io)

Failing with Dignity: A Deep Dive into Graceful Degradation

codereliant



](https://www.codereliant.io/p/failing-with-dignity)

[

![learn.microsoft.com favicon](https://www.google.com/s2/favicons?sz=128&domain=learn.microsoft.com)

Circuit Breaker Pattern - Azure Architecture Center | Microsoft Learn

learn.microsoft



](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)

Đang lưu ghi chú nghiên cứu phân loại lỗi network và phần mềm vào file để hoàn thiện bảng OSI thực chiến.



Tìm kiếm thuộc tính chất lượng phần mềm ISO 25010 và taxonomy lỗi từ nghiên cứu để hoàn thiện bảng OSI.

Searching

software quality attributes ISO 25010

error taxonomy research papers

fault injection testing distributed systems

Reviewing sources · 19

[

![iso25000.com favicon](https://www.google.com/s2/favicons?sz=128&domain=iso25000.com)

ISO/IEC 25010

iso25000



](https://iso25000.com/en/iso-25000-standards/iso-25010)

[

![iso.org favicon](https://www.google.com/s2/favicons?sz=128&domain=iso.org)

ISO/IEC 25010:2011 - Systems and software engineering

iso



](https://www.iso.org/standard/35733.html)

[

![blog.codacy.com favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.codacy.com)

An Exploration of the ISO/IEC 25010 Software Quality Model

blog.codacy



](https://blog.codacy.com/iso-25010-software-quality-model)

[

![blog.pacificcert.com favicon](https://www.google.com/s2/favicons?sz=128&domain=blog.pacificcert.com)

ISO/IEC 25010:2023 Guide to Software Product Quality ...

blog.pacificcert



](https://blog.pacificcert.com/iso-25010-software-product-quality-model/)

[

A taxonomy for advancing systematic error analysis in multi ...

pmc.ncbi.nlm.nih



](https://pmc.ncbi.nlm.nih.gov/articles/PMC11187420/)

[

![odr.chalmers.se favicon](https://www.google.com/s2/favicons?sz=128&domain=odr.chalmers.se)

Distributed Systems verification using fault injection approach

odr.chalmers



](https://odr.chalmers.se/bitstreams/c3596096-3e15-46f1-8ef4-0b6a94ce55f2/download)

[

![perforce.com favicon](https://www.google.com/s2/favicons?sz=128&domain=perforce.com)

What Is ISO 25010?

perforce



](https://www.perforce.com/blog/qac/what-is-iso-25010)

[

![arxiv.org favicon](https://www.google.com/s2/favicons?sz=128&domain=arxiv.org)

Resource for Error Analysis in Text Simplification

arxiv



](https://arxiv.org/html/2505.16392v1)

[

![uwspace.uwaterloo.ca favicon](https://www.google.com/s2/favicons?sz=128&domain=uwspace.uwaterloo.ca)

A Fault Injection Tool for Testing Distributed System with ...

uwspace.uwaterloo



](https://uwspace.uwaterloo.ca/items/9c08043b-2f85-4d5f-9e4f-1ce1ab17882f)

[

![quality.arc42.org favicon](https://www.google.com/s2/favicons?sz=128&domain=quality.arc42.org)

Shortcomings of ISO 25010

quality.arc42



](https://quality.arc42.org/articles/iso-25010-shortcomings)

[

![academia.edu favicon](https://www.google.com/s2/favicons?sz=128&domain=academia.edu)

(PDF) Towards an Error Taxonomy for Student Writing

academia



](https://www.academia.edu/7806094/Towards_an_Error_Taxonomy_for_Student_Writing)

[

![usenix.org favicon](https://www.google.com/s2/favicons?sz=128&domain=usenix.org)

CAFault: Enhance Fault Injection Technique in Practical ...

usenix



](https://www.usenix.org/system/files/atc25-chen-yuanliang.pdf)

[

2.1.2 Software Quality Attributes ISO25010 - Lecture2Go

lecture2go.uni-hamburg



](https://lecture2go.uni-hamburg.de/l2go/-/get/v/39642)

[

![sciencedirect.com favicon](https://www.google.com/s2/favicons?sz=128&domain=sciencedirect.com)

Development of a human error taxonomy for software ...

sciencedirect



](https://www.sciencedirect.com/science/article/am/pii/S0950584916302373)

[

![microsoft.github.io favicon](https://www.google.com/s2/favicons?sz=128&domain=microsoft.github.io)

Fault Injection Testing - Engineering Fundamentals Playbook

microsoft.github



](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/fault-injection-testing/)

[

![discovery.researcher.life favicon](https://www.google.com/s2/favicons?sz=128&domain=discovery.researcher.life)

Human Error Taxonomy Research Articles - Page 1 | R Discovery

discovery.researcher



](https://discovery.researcher.life/topic/human-error-taxonomy/18398162?page=1&topic_name=Human+Error+Taxonomy)

[

Fault injection testing for distributed object systems

ieeexplore.ieee



](https://ieeexplore.ieee.org/document/941680/)

[

Developing a systemic investigation method for engineering and ...

repository.tudelft



](https://repository.tudelft.nl/record/uuid:77a0d508-f505-44db-ab08-7d2e6a56f008)

[

![qodo.ai favicon](https://www.google.com/s2/favicons?sz=128&domain=qodo.ai)

What is Fault Injection Testing? Importance & Techniques

qodo



](https://www.qodo.ai/glossary/fault-injection-testing/)