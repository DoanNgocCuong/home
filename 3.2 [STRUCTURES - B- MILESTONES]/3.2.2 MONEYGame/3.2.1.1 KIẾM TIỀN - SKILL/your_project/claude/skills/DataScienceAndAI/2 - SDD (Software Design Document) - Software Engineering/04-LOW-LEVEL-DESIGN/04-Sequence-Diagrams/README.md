# Sequence Diagrams - Sơ đồ Tuần tự

## Sequence Diagram là gì?

**Sequence Diagram** là một loại diagram dùng để mô tả **thứ tự các bước** khi một use case hoặc process xảy ra. Nó cho thấy các actors (người dùng, objects) tương tác với nhau như thế nào theo thời gian.

### Tại sao cần Sequence Diagrams?

1. **Visualize flow**: Dễ hiểu luồng xử lý phức tạp
2. **Identify bottlenecks**: Nhìn thấy nơi có thể chậm
3. **Error handling**: Hiểu cách xử lý lỗi
4. **Communication**: Giải thích cho team dễ hơn
5. **Documentation**: Tài liệu cho developers

### Ví dụ đơn giản

```
User → Login Button → Auth Service → Database
 │         │              │             │
 │─enter email/pw──→      │             │
 │                   │─validate────────→│
 │                   │                  │
 │                   │←──user data──────│
 │                   │                  │
 │                   │─generate token   │
 │←─token───────────│
 │
 │─show dashboard
```

## Syntax Mermaid cho Sequence Diagrams

Mermaid là công cụ để vẽ diagrams bằng code. Dưới đây là syntax cơ bản:

### 1. Khai báo Participants (Tham gia viên)

```mermaid
sequenceDiagram
    participant User as User/Client
    participant Server as Backend Server
    participant DB as Database
```

**Giải thích:**
- `participant [variable] as [display name]`
- Variable dùng trong diagram
- Display name là tên hiển thị

### 2. Messages - Thông điệp

#### Synchronous Message (Chờ response)
```mermaid
sequenceDiagram
    Actor->>Server: Do something
    Server-->>Actor: Response
```

**Ký hiệu:**
- `->>`  : Solid arrow (synchronous)
- `->>` : Solid return
- `-->>` : Dashed return

#### Asynchronous Message (Không chờ)
```mermaid
sequenceDiagram
    Actor->>Server: Send and don't wait
    Server-->>Actor: Response later
```

### 3. Activation Box (Khoảng thời gian hoạt động)

```mermaid
sequenceDiagram
    Actor->>Server: Request
    activate Server
    Server->>DB: Query
    activate DB
    DB-->>Server: Result
    deactivate DB
    Server-->>Actor: Response
    deactivate Server
```

**Activation** dùng `activate` và `deactivate` để chỉ ra khi nào một object đang hoạt động.

### 4. Alt/Else - Điều kiện

```mermaid
sequenceDiagram
    User->>Server: Login
    activate Server
    alt Correct password
        Server->>DB: Update last_login
        Server-->>User: 200 OK - Token
    else Wrong password
        Server-->>User: 401 Unauthorized
    end
    deactivate Server
```

### 5. Loop - Vòng lặp

```mermaid
sequenceDiagram
    User->>Server: Upload 10 files
    activate Server
    loop For each file
        Server->>CloudStorage: Upload file
        CloudStorage-->>Server: OK
    end
    Server-->>User: All files uploaded
    deactivate Server
```

### 6. Notes - Ghi chú

```mermaid
sequenceDiagram
    User->>Server: Request
    Note right of Server: Validate input<br/>Check authentication
    Server->>DB: Query
    Note left of DB: Acquire lock<br/>Execute query
    DB-->>Server: Result
    Server-->>User: Response
```

## Ví dụ 1: User Login Flow

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Browser as 🌐 Browser/Client
    participant Gateway as 🚪 API Gateway
    participant Auth as 🔐 Auth Service
    participant DB as 💾 Database

    User->>Browser: 1. Nhập email & password
    Browser->>Gateway: 2. POST /api/auth/login

    activate Gateway
    Gateway->>Auth: 3. Gọi authenticate()
    deactivate Gateway

    activate Auth
    Auth->>DB: 4. SELECT user WHERE email=?
    activate DB
    DB-->>Auth: 5. Trả về user data
    deactivate DB

    Note right of Auth: Hash password & compare
    alt Password matches
        Auth->>DB: 6. INSERT refresh_token
        Auth->>Auth: 7. Generate JWT token
        Auth-->>Gateway: 8. Return token
        activate Gateway
        Gateway-->>Browser: 9. Return 200 OK + token
        deactivate Gateway
        Browser->>Browser: 10. Save token to localStorage
        Browser->>User: ✓ Login successful!
    else Password doesn't match
        Auth-->>Gateway: 8. Throw UnauthorizedException
        activate Gateway
        Gateway-->>Browser: 9. Return 401 Unauthorized
        deactivate Gateway
        Browser->>User: ✗ Invalid credentials
    end
    deactivate Auth
```

**Penjelasan flow:**
1. User memasukkan credentials
2. Browser mengirim POST request ke API
3. API Gateway meneruskan ke Auth Service
4. Auth Service query user dari database
5. Jika password cocok → generate token → return
6. Jika password salah → return error
7. Browser menyimpan token untuk request berikutnya

## Ví dụ 2: Payment Processing Flow

```mermaid
sequenceDiagram
    participant User as 👤 Customer
    participant Frontend as 💻 Web Frontend
    participant OrderSvc as 📦 Order Service
    participant PaymentSvc as 💳 Payment Service
    participant Stripe as 🏦 Stripe API
    participant DB as 💾 Database
    participant Email as 📧 Email Service

    User->>Frontend: 1. Click "Place Order"
    Frontend->>OrderSvc: 2. POST /orders

    activate OrderSvc
    OrderSvc->>DB: 3. Validate cart items
    activate DB
    DB-->>OrderSvc: 4. Items valid
    deactivate DB

    Note right of OrderSvc: Calculate total price<br/>Create order record

    OrderSvc->>PaymentSvc: 5. Process payment
    deactivate OrderSvc

    activate PaymentSvc
    PaymentSvc->>Stripe: 6. POST /v1/charges<br/>(card, amount)
    activate Stripe

    alt Payment successful
        Stripe-->>PaymentSvc: 7. Charge created ✓
        deactivate Stripe
        PaymentSvc->>DB: 8. Save transaction
        PaymentSvc-->>OrderSvc: 9. Payment confirmed
        deactivate PaymentSvc

        activate OrderSvc
        OrderSvc->>DB: 10. Update order status → PAID
        OrderSvc->>Email: 11. Send confirmation email
        OrderSvc-->>Frontend: 12. Return 201 Created
        deactivate OrderSvc

        Frontend->>User: ✓ Order placed! ID: #12345
    else Payment failed
        Stripe-->>PaymentSvc: 7. Error message
        deactivate Stripe
        PaymentSvc-->>OrderSvc: 9. Payment failed
        deactivate PaymentSvc

        activate OrderSvc
        OrderSvc->>DB: 10. Delete order
        OrderSvc-->>Frontend: 11. Return 402 Payment Required
        deactivate OrderSvc

        Frontend->>User: ✗ Payment failed. Try again.
    end
```

**Penjelasan flow:**
1. User klik "Place Order"
2. Frontend kirim request ke Order Service
3. Order Service validasi items dan hitung total
4. Kirim payment request ke Payment Service
5. Payment Service call Stripe API
6. Stripe proses charge (charge card)
7. Jika berhasil → update order status → send email
8. Jika gagal → delete order → return error
9. User melihat success/error message

## Ví dụ 3: File Upload Flow

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Frontend as 🌐 Frontend
    participant Gateway as 🚪 API Gateway
    participant FileSvc as 📂 File Service
    participant S3 as ☁️ AWS S3
    participant DB as 💾 Database
    participant Queue as 📨 Message Queue

    User->>Frontend: 1. Select file & click Upload

    Frontend->>Frontend: 2. Show progress bar
    Frontend->>Gateway: 3. POST /files/upload<br/>multipart/form-data

    activate Gateway
    Note right of Gateway: Check file size<br/>Check MIME type
    alt File invalid
        Gateway-->>Frontend: 401 Bad Request
        Frontend->>User: ✗ Invalid file
    else File valid
        Gateway->>FileSvc: 4. uploadFile(file)
        deactivate Gateway

        activate FileSvc
        Note right of FileSvc: Generate unique filename<br/>Create metadata

        FileSvc->>S3: 5. PUT /bucket/file-uuid
        activate S3
        S3-->>FileSvc: 6. File uploaded ✓
        deactivate S3

        FileSvc->>DB: 7. INSERT file record
        activate DB
        DB-->>FileSvc: 8. File metadata saved
        deactivate DB

        FileSvc->>Queue: 9. Publish "file.uploaded"<br/>event (async)
        Queue-->>FileSvc: 10. Event queued ✓

        FileSvc-->>Gateway: 11. Return fileId & URL
        activate Gateway
        Gateway-->>Frontend: 12. Return 201 Created
        deactivate Gateway

        Frontend->>User: ✓ File uploaded!<br/>URL: s3.../file-uuid

        par Background Processing
            Queue-->>Queue: Process event asynchronously
            Note over Queue: Generate thumbnail<br/>Scan for virus<br/>Create backup
        end
        deactivate FileSvc
    end
```

**Penjelasan flow:**
1. User pilih file dan upload
2. Frontend show progress bar
3. Kirim file ke API Gateway
4. API Gateway check file validity
5. Jika valid → kirim ke File Service
6. File Service upload ke S3
7. Simpan metadata ke database
8. Publish event ke message queue
9. Return file URL ke user
10. Background task (async) process event seperti generate thumbnail

## Best Practices untuk Sequence Diagrams

### 1. Keep it simple
```mermaid
sequenceDiagram
    A->>B: Request
    B-->>A: Response
```

Jangan terlalu banyak objects atau steps sekaligus.

### 2. Gunakan activation boxes
```mermaid
sequenceDiagram
    A->>B: Call
    activate B
    B->>C: Call
    activate C
    C-->>B: Return
    deactivate C
    B-->>A: Return
    deactivate B
```

Ini membuat jelas siapa yang sedang bekerja.

### 3. Label messages dengan jelas
```mermaid
sequenceDiagram
    A->>B: ✓ POST /api/login (email, password)
    B-->>A: ✓ 200 OK (token)
```

Sertakan HTTP method, status code, dan parameter jika penting.

### 4. Gunakan notes untuk penjelasan
```mermaid
sequenceDiagram
    A->>B: Request
    Note right of B: Validate<br/>Check auth<br/>Query DB
    B-->>A: Response
```

### 5. Gunakan alt/else untuk edge cases
```mermaid
sequenceDiagram
    A->>B: Process
    alt Success
        B-->>A: OK
    else Error
        B-->>A: Error
    end
```

Jangan lupakan error cases!

### 6. Gunakan loop untuk repetitive actions
```mermaid
sequenceDiagram
    A->>B: Start bulk operation
    loop For each item
        B->>C: Process item
    end
    B-->>A: Done
```

## Common Patterns

### Pattern 1: Request-Response (Sync)
```mermaid
sequenceDiagram
    Client->>Server: Request
    activate Server
    Server->>Server: Process
    Server-->>Client: Response
    deactivate Server
```

### Pattern 2: Async with callback
```mermaid
sequenceDiagram
    Client->>Server: Start job
    Note right of Server: Return job_id immediately
    Server-->>Client: 202 Accepted
    Server->>Worker: Process in background
    activate Worker
    Note right of Worker: Long-running task
    Worker-->>Callback: POST callback_url
    deactivate Worker
```

### Pattern 3: Multi-stage approval
```mermaid
sequenceDiagram
    User->>System: Submit request
    System->>Manager1: Request approval
    activate Manager1
    Manager1-->>System: Approve
    deactivate Manager1
    System->>Manager2: Request final approval
    activate Manager2
    Manager2-->>System: Approve
    deactivate Manager2
    System->>User: ✓ Request approved!
```

### Pattern 4: Retry mechanism
```mermaid
sequenceDiagram
    A->>B: Request (attempt 1)
    alt Success
        B-->>A: Response
    else Failure
        Note right of A: Wait 1 second
        A->>B: Request (attempt 2)
        alt Success
            B-->>A: Response
        else Failure
            A-->>A: Give up
        end
    end
```

## Sequence Diagram Checklist

Ketika membuat sequence diagram, pastikan:

- [ ] Semua actors/participants jelas terdaftar?
- [ ] Pesan (messages) berlabel dengan jelas?
- [ ] Thứ tự steps terlihat jelas?
- [ ] Activation boxes menunjukkan siapa yang bekerja?
- [ ] Error cases tercakup (alt/else)?
- [ ] Notes menjelaskan step yang kompleks?
- [ ] Tidak ada steps yang dilewatkan?
- [ ] Diagram tidak terlalu kompleks (max 10-15 steps)?
- [ ] Konsisten dengan class diagram dan implementation?

## Tools untuk membuat Sequence Diagrams

1. **Mermaid** (gratis, online): https://mermaid.live
2. **PlantUML** (gratis, open source): http://plantuml.com
3. **Lucidchart** (berbayar, powerful): https://www.lucidchart.com
4. **Draw.io** (gratis, online): https://draw.io
5. **Enterprise Architect** (berbayar, professional): https://www.sparxsystems.com

## Mermaid Examples Repository

Simpan diagram Mermaid Anda di file `.md` seperti ini:

```markdown
# Login Sequence

Description of the sequence...

\`\`\`mermaid
sequenceDiagram
    ... diagram code ...
\`\`\`

## Explanation

- Step 1: ...
- Step 2: ...
```

---

## Kesimpulan

Sequence Diagrams adalah cara visual yang powerful untuk:
- Menjelaskan workflow kompleks
- Mengidentifikasi bottlenecks
- Merencanakan error handling
- Berkomunikasi dengan team

Gunakan bersama dengan:
- **HLD** (arsitektur sistem)
- **LLD** (class diagrams, database schema)
- **Code** (implementation)

**Untuk full context, lihat juga:**
- `../README.md` - Low-Level Design overview
- `../02-Database-Schema-Design/README.md` - Database design
