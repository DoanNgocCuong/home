# Docker Configuration: Sai lầm thường gặp & Best Practices

> **Scope:** Dockerfile, docker-compose.yml, `environment:`, `.env` — toàn bộ configuration layer cho production microservices.

---

## Nguyên tắc cốt lõi

1. **Container port cố định, chỉ thay đổi host port bên ngoài.**
2. **Mỗi file chịu trách nhiệm riêng, không overlap.**
3. **Một nguồn sự thật duy nhất cho mỗi config value.**

|File|Chịu trách nhiệm|Ví dụ|
|---|---|---|
|`Dockerfile`|Container port, runtime command (hardcode)|`EXPOSE 8000`, `--port 8000`|
|`.env`|Host port + app config (secrets, URLs, tuning)|`API_PORT=30001`, `DATABASE_URL=...`|
|`docker-compose.yml`|Port mapping, service wiring, network topology|`"${API_PORT:-30001}:8000"`|
|`environment:`|Override / default cho biến có thể thiếu|`ENVIRONMENT: production`|

---

## Phần 1: Danh sách sai lầm

### Sai lầm 1 — Dùng biến cho container port trong Dockerfile

```dockerfile
# ❌ Sai
ARG APP_PORT=8000
EXPOSE ${APP_PORT}
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${APP_PORT}"]
```

**Hậu quả:** Ai đó đổi `APP_PORT` trong `.env` nhưng quên rebuild image → app listen port khác với port được map trong docker-compose → request không tới app. Container start thành công, health check có thể pass, nhưng traffic không vào. Bug cực khó trace.

```dockerfile
# ✅ Đúng — hardcode, không dùng biến
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Sai lầm 2 — Định nghĩa container port trong .env

```env
# ❌ Không cần
CONTAINER_PORT=8000
APP_PORT=8000

# ✅ Chỉ host port
LESSON_API_PORT=30001
```

**Hậu quả:** Thêm layer indirection không cần thiết. Container port cố định `8000` — biến nó thành configurable = thêm chỗ để sai.

---

### Sai lầm 3 — Host port và container port dùng cùng port lạ

```yaml
# ❌ Container listen 30020 — tại sao?
ports:
  - "${PORT:-30020}:30020"
```

**Hậu quả:** Bên trong container chỉ có 1 app, không conflict — không có lý do dùng port lạ. Dùng port chuẩn (`8000` cho HTTP) dễ đọc hơn, consistent với mọi project.

```yaml
# ✅ Container dùng port chuẩn, host port tuỳ chỉnh
ports:
  - "${PORT:-30020}:8000"
```

---

### Sai lầm 4 — `environment:` trùng lặp với `.env`

```yaml
services:
  api:
    env_file:
      - .env                                        # Đã load tất cả biến
    environment:
      LOGGING_LEVEL: INFO                           # ❌ đã có trong .env
      ENVIRONMENT: production                       # ❌ đã có trong .env
      HOST: 0.0.0.0                                 # ❌ đã có trong .env
      UVICORN_WORKERS: ${UVICORN_WORKERS:-4}        # ❌ đã có trong .env
      DB_POOL_SIZE: ${DB_POOL_SIZE:-15}             # ❌ đã có trong .env
      DB_MAX_OVERFLOW: ${DB_MAX_OVERFLOW:-10}       # ❌ đã có trong .env
```

**Hậu quả:** Cùng biến định nghĩa ở 2 nơi. Khi cần thay đổi, phải sửa cả 2. Nếu quên 1 chỗ, `environment:` override `.env` âm thầm → config drift khó debug. Team member mới không biết source of truth nằm ở đâu.

```yaml
# ✅ Nếu .env đã đầy đủ — chỉ cần env_file
services:
  api:
    env_file:
      - .env
    ports:
      - "${API_PORT:-30001}:8000"
```

---

### Sai lầm 5 — Không phân biệt `ports` vs `env_file` vs `environment:`

Ba directive này phục vụ mục đích hoàn toàn khác nhau:

|Directive|Ai dùng|Mục đích|Ví dụ|
|---|---|---|---|
|`ports`|Client bên ngoài|Network routing: host → container|`"30001:8000"`|
|`env_file`|App bên trong container|Load toàn bộ config từ file|`.env`|
|`environment:`|App bên trong container|Override / default cho biến cụ thể|`ENVIRONMENT: production`|

Request flow:

```
Client → Host:30001 → Docker NAT → Container:8000 → Uvicorn
                                                       ↓
                                             Đọc env vars (DATABASE_URL, REDIS_URL, ...)
                                             Nguồn: .env (qua env_file) + environment: (override)
```

`ports` cho network layer. `env_file` + `environment:` cho application layer. Thiếu `ports` → không ai gọi được service. Thiếu `env_file` → app không biết connect DB ở đâu.

---

### Sai lầm 6 — Expose port cho internal services

```yaml
# ❌ Tại sao expose Redis và DB ra host?
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  db:
    image: postgres:16
    ports:
      - "5432:5432"
```

**Hậu quả:** Redis và PostgreSQL chỉ cần truy cập từ các service khác trong cùng Docker network. Expose ra host tạo attack surface không cần thiết.

```yaml
# ✅ Chỉ expose service cần external access
services:
  api:
    ports:
      - "${API_PORT:-30001}:8000"    # ✅ Cần expose cho client

  redis:
    image: redis:7
    # Không ports — gọi qua: redis://redis:6379

  db:
    image: postgres:16
    # Không ports — gọi qua: postgresql://db:5432/mydb
```

Nếu cần debug từ host, dùng `docker exec` hoặc tạm thêm `ports` rồi xoá sau.

---

### Sai lầm 7 — Hardcode secrets trong `environment:`

```yaml
# ❌ Secrets visible trong docker-compose.yml (commit vào git)
services:
  api:
    environment:
      DATABASE_URL: postgresql://admin:SuperSecret123@db:5432/mydb
      SECRET_KEY: my-jwt-secret-key
      REDIS_PASSWORD: redis123
```

**Hậu quả:** Secrets nằm trong file được version control. Ai có access repo đều đọc được password.

```yaml
# ✅ Secrets chỉ nằm trong .env (gitignore)
services:
  api:
    env_file:
      - .env    # .env nằm trong .gitignore
```

```env
# .env (không commit vào git)
DATABASE_URL=postgresql://admin:SuperSecret123@db:5432/mydb
SECRET_KEY=my-jwt-secret-key
```

```gitignore
# .gitignore
.env
.env.production
```

---

### Sai lầm 8 — Dùng host port cho service-to-service communication

```env
# ❌ Dùng localhost + host port
DATABASE_URL=postgresql://user:pass@localhost:35432/mydb
REDIS_URL=redis://localhost:36379/0
EMOTION_SERVICE_URL=http://localhost:30002
```

**Hậu quả:** `localhost` trong container trỏ về chính container đó, không phải host machine. Ngay cả khi dùng `host.docker.internal`, vẫn đi vòng qua host thay vì dùng Docker network — chậm hơn và fragile hơn.

```env
# ✅ Service name = hostname trong Docker network
DATABASE_URL=postgresql://user:pass@db:5432/mydb
REDIS_URL=redis://redis:6379/0
EMOTION_SERVICE_URL=http://emotion-service:8000
```

---

## Phần 2: `environment:` trong docker-compose — Khi nào cần, khi nào thừa

### 2.1 Cơ chế hoạt động

Docker compose load biến theo thứ tự ưu tiên (cao → thấp):

1. `environment:` trong docker-compose.yml (cao nhất — override mọi thứ)
2. Shell environment variables trên host
3. `env_file:` (.env file)

Nghĩa là: nếu cùng biến tồn tại ở cả `.env` và `environment:`, giá trị trong `environment:` thắng.

### 2.2 Khi nào cần `environment:`

**Trường hợp 1 — Default an toàn cho biến có thể thiếu:**

```yaml
environment:
  UVICORN_WORKERS: ${UVICORN_WORKERS:-4}     # Default 4 nếu .env không set
  DB_POOL_SIZE: ${DB_POOL_SIZE:-15}          # Default 15 nếu .env không set
```

**Trường hợp 2 — Cưỡng chế giá trị cho environment cụ thể:**

```yaml
# docker-compose.prod.yml
environment:
  ENVIRONMENT: production    # Không ai được đổi thành "development"
  DEBUG: "false"             # Không bao giờ bật debug trong production
```

**Trường hợp 3 — Biến infrastructure không thuộc app config:**

```yaml
environment:
  HOST: 0.0.0.0              # Container networking, không phải app logic
```

### 2.3 Khi nào KHÔNG cần `environment:`

Nếu `.env` đã có đầy đủ và bạn không cần override hay default → bỏ `environment:` hoàn toàn:

```yaml
# ✅ Clean — .env là single source of truth
services:
  api:
    build: .
    env_file:
      - .env
    ports:
      - "${API_PORT:-30001}:8000"
```

### 2.4 Bảng quyết định

|Tình huống|Dùng `env_file`|Dùng `environment:`|
|---|---|---|
|App config (DB URL, secrets, tuning)|✅|✗|
|Biến đã có trong .env|✅|✗ (redundant)|
|Default cho biến có thể thiếu|✅|✅ `${VAR:-default}`|
|Force override cho prod/staging|—|✅|
|Infrastructure vars (HOST, network)|—|✅|
|Secrets|✅ (.env trong .gitignore)|❌ (lộ trong yaml)|

---

## Phần 3: Best Practices Checklist

### 3.1 Dockerfile

- [ ] Container port hardcode (không dùng ARG/ENV cho port)
- [ ] `EXPOSE` khớp với port trong CMD
- [ ] Dùng port chuẩn: `8000` cho HTTP, `5432` cho PostgreSQL, `6379` cho Redis
- [ ] CMD dùng exec form: `CMD ["uvicorn", ..., "--port", "8000"]`

### 3.2 `.env`

- [ ] Chỉ chứa host port, không chứa container port
- [ ] Naming convention: `{SERVICE_NAME}_PORT=XXXXX`
- [ ] Secrets chỉ nằm trong `.env`, không trong docker-compose.yml
- [ ] `.env` nằm trong `.gitignore`
- [ ] Service-to-service URL dùng Docker service name, không dùng localhost
- [ ] Có `.env.example` (không có secrets) để team member mới setup

### 3.3 `docker-compose.yml`

- [ ] Port mapping: `"${SERVICE_PORT:-default}:8000"` (host biến, container cố định)
- [ ] Internal services (DB, Redis, MQ) không có `ports:`
- [ ] `env_file: .env` là primary config source
- [ ] `environment:` chỉ dùng cho override/default, không duplicate `.env`
- [ ] Mỗi service có network riêng hoặc shared network rõ ràng
- [ ] `restart: unless-stopped` cho production services

### 3.4 `environment:` trong docker-compose

- [ ] Không duplicate biến đã có trong `.env`
- [ ] Chỉ dùng cho: default an toàn, force override, infrastructure vars
- [ ] Không chứa secrets (dùng `.env` thay thế)
- [ ] Nếu `.env` đã đầy đủ → bỏ `environment:` block

---

## Phần 4: Template chuẩn

### 4.1 Single service

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```env
# .env
API_PORT=30001
DATABASE_URL=postgresql://user:pass@db:5432/mydb
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change-me-in-production
LOG_LEVEL=INFO
UVICORN_WORKERS=4
```

```yaml
# docker-compose.yml
services:
  api:
    build: .
    container_name: my_api
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "${API_PORT:-30001}:8000"
    networks:
      - app_network

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  redis:
    image: redis:7-alpine
    networks:
      - app_network

networks:
  app_network:
    driver: bridge

volumes:
  postgres_data:
```

### 4.2 Multi-service (Pika stack)

```env
# .env
LESSON_API_PORT=30001
EMOTION_SERVICE_PORT=30002
ORCHESTRATION_PORT=30003
CONTEXT_HANDLING_PORT=30020

DATABASE_URL=postgresql://user:pass@db:5432/pika
REDIS_URL=redis://redis:6379/0
```

```yaml
# docker-compose.yml
services:
  lesson-api:
    build: ./lesson-api
    env_file: .env
    ports:
      - "${LESSON_API_PORT:-30001}:8000"

  emotion-service:
    build: ./emotion-service
    env_file: .env
    ports:
      - "${EMOTION_SERVICE_PORT:-30002}:8000"

  orchestration:
    build: ./orchestration
    env_file: .env
    ports:
      - "${ORCHESTRATION_PORT:-30003}:8000"

  context-handling:
    build: ./context-handling
    env_file: .env
    ports:
      - "${CONTEXT_HANDLING_PORT:-30020}:8000"
```

Mọi container đều listen `8000`. Service-to-service gọi `http://emotion-service:8000`. Chỉ host port khác nhau để expose ra ngoài.

---

## Phần 5: Request flow tổng quan

```
Browser / Client
    │
    ▼
Host:30001                ← .env: API_PORT=30001
    │
    ▼ (Docker NAT)
Container:8000            ← Dockerfile: CMD [..., "--port", "8000"]
    │
    ▼
Uvicorn / App
    │  Đọc config từ env vars (nguồn: .env qua env_file)
    │
    ├──→ db:5432          ← DATABASE_URL=postgresql://...@db:5432/mydb
    ├──→ redis:6379       ← REDIS_URL=redis://redis:6379/0
    └──→ emotion:8000     ← EMOTION_URL=http://emotion-service:8000
         (Docker network, service name resolution)
```