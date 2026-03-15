# Tối ưu DB: trong bài context Handling https://github.com/DoanNgocCuong/context-handling-bigmodule_PikaRobot_25112025/tree/main/stressTestDevProduction


Đang kiểm tra tại sao tăng pool size trong .env vẫn không hiệu quả:


[5 tools called]


Đang kiểm tra các nguyên nhân khác tại sao tăng pool size vẫn không hiệu quả:


[4 tools called]


Đã tăng pool size trong `.env` nhưng vẫn bị. Dưới đây là các nguyên nhân có thể:

## Phân tích: Tại sao tăng pool size vẫn bị?

### Nguyên nhân 1: Service chưa restart (khả năng cao)

Khi thay đổi `.env`, cần restart service để load giá trị mới:

```
Application startup:
├─ Load .env file → Settings object created
├─ Database engine created với pool_size từ settings
└─ Engine object được cache → Không tự động reload khi .env thay đổi
```

Giải pháp:
- Restart API service (FastAPI)
- Restart Worker service (RabbitMQ consumer)

---

### Nguyên nhân 2: PostgreSQL max_connections limit (khả năng rất cao)

PostgreSQL có giới hạn `max_connections` (mặc định thường là 100-200). Nếu bạn cấu hình 300 connections (100 + 200) nhưng PostgreSQL chỉ cho phép 100 → sẽ bị giới hạn.

Kiểm tra:

```sql
-- Kết nối vào PostgreSQL
SELECT name, setting, unit 
FROM pg_settings 
WHERE name = 'max_connections';

-- Xem số connections đang dùng
SELECT count(*) as active_connections 
FROM pg_stat_activity;
```

Nếu `max_connections = 100` nhưng bạn cần 300 → phải tăng PostgreSQL limit:

```sql
-- Trong postgresql.conf
max_connections = 500  # Tăng lên 500

-- Hoặc trong .env (nếu dùng Docker)
POSTGRES_MAX_CONNECTIONS=500
```

---

### Nguyên nhân 3: RabbitMQ prefetch_count = 1 (bottleneck)

```python
# src/app/background/rabbitmq_consumer.py:150
self.channel.basic_qos(prefetch_count=1)  # ⚠️ CHỈ 1 message/worker
```

Với `prefetch_count=1`:
- Mỗi worker chỉ xử lý 1 message tại một thời điểm
- Worker phải đợi message xong mới lấy message tiếp
- Với 200 requests → queue backlog → latency tăng

Giải pháp: Tăng `prefetch_count`:

```python
self.channel.basic_qos(prefetch_count=10)  # Xử lý 10 messages đồng thời
```

---

### Nguyên nhân 4: Redis single connection (bottleneck)

Nếu code dùng Redis cache và chỉ có 1 connection (singleton) → tất cả requests phải chờ nhau.

---

### Cách kiểm tra và xử lý

#### Bước 1: Verify giá trị đang được dùng

Thêm log để xem giá trị thực tế:

```python
# src/app/db/database_connection.py
logger.info(
    f"🔧 Database Pool Configuration:\n"
    f"   - pool_size: {settings.DB_POOL_SIZE}\n"
    f"   - max_overflow: {settings.DB_MAX_OVERFLOW}\n"
    f"   - Total max connections: {settings.DB_POOL_SIZE + settings.DB_MAX_OVERFLOW}\n"
    f"   - pool_timeout: {settings.DB_POOL_TIMEOUT}s"
)
```

Sau khi restart, kiểm tra log:

```
🔧 Database Pool Configuration:
   - pool_size: 100  ← Phải là 100 (không phải 50)
   - max_overflow: 200  ← Phải là 200 (không phải 100)
   - Total max connections: 300
```

Nếu vẫn thấy giá trị cũ → chưa restart hoặc `.env` chưa được load.

---

#### Bước 2: Kiểm tra PostgreSQL max_connections

```bash
# Kết nối vào PostgreSQL
psql -U postgres -d context_handling_db

# Check max_connections
SELECT name, setting FROM pg_settings WHERE name = 'max_connections';

# Check active connections
SELECT count(*) as active, 
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max_conns,
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') - count(*) as available
FROM pg_stat_activity;
```

Nếu `max_connections < 300` → phải tăng PostgreSQL limit.

---

#### Bước 3: Tăng RabbitMQ prefetch_count

```python
# src/app/background/rabbitmq_consumer.py:150
# Tăng từ 1 lên 10
self.channel.basic_qos(prefetch_count=10)
```

---

### Tóm tắt checklist

- [ ] Đã restart API service sau khi đổi `.env`?
- [ ] Đã restart Worker service sau khi đổi `.env`?
- [ ] PostgreSQL `max_connections` >= 300?
- [ ] RabbitMQ `prefetch_count` đã tăng từ 1 lên 10?
- [ ] Redis có connection pool (không phải singleton)?

---

### Khuyến nghị ngay

1. Tăng PostgreSQL max_connections:

```bash
# Kiểm tra file config
# Linux: /etc/postgresql/*/main/postgresql.conf
# Docker: environment variable POSTGRES_MAX_CONNECTIONS=500

# Sau khi set, restart PostgreSQL
```

2. Tăng RabbitMQ prefetch_count:

```python
# src/app/background/rabbitmq_consumer.py
self.channel.basic_qos(prefetch_count=10)  # Từ 1 → 10
```

3. Verify giá trị trong log:

Sau khi restart, kiểm tra log để đảm bảo pool size = 100 + 200 = 300.

Bạn muốn tôi tạo script để check các giá trị này không?





# Làm sao để tăng nó trong DB  và liệu có vấn đề rủi ro nào xảy ra ko ? 

```
sql  
ALTER SYSTEM SET max_connections = 500;  
SELECT pg_reload_conf();  
  
Tuy nhiên, thay đổi này cần khởi động lại server PostgreSQL để có hiệu lực hoàn toàn.  
Việc tăng max_connections giúp tăng số kết nối đồng thời tới DB, nhưng cần cân nhắc tài nguyên hệ thống để tránh gây quá tải.  
  
  
Làm như này lfa được rồi đúng ko  
thế so sánh tài nguyên khi để 100 và để 500
```


Đúng, câu lệnh SQL sau đây đã đúng cú pháp để tăng max_connections trong PostgreSQL:

sql

`ALTER SYSTEM SET max_connections = 500; SELECT pg_reload_conf();`

Tuy nhiên, bạn vẫn cần phải khởi động lại PostgreSQL để thay đổi có hiệu lực hoàn toàn.

Về so sánh tài nguyên khi để max_connections là 100 và 500:

- Mỗi kết nối PostgreSQL sử dụng một lượng bộ nhớ nhất định (bao gồm shared memory và private memory). Khi tăng max_connections từ 100 lên 500, tổng bộ nhớ dùng cho các kết nối cũng tăng lên đáng kể. Điều này làm giảm bộ nhớ có thể dùng cho các hoạt động khác như sorting, caching (work_mem, shared_buffers) và có thể dẫn đến giảm hiệu năng nếu bộ nhớ hệ thống không đủ.
    
- CPU và I/O cũng có thể chịu tải nhiều hơn khi số lượng kết nối đồng thời cao, gây khả năng quá tải hoặc chậm hệ thống.
    
- Trên thực tế, khi tăng max_connections lên quá cao, mỗi kết nối được cấp ít bộ nhớ hơn (như work_mem phải giảm để đủ bộ nhớ cho tất cả), làm giảm hiệu suất xử lý các truy vấn phức tạp.
    
- Vì vậy, việc nâng max_connections cần cân bằng với tổng tài nguyên hệ thống (RAM, CPU) và cách ứng dụng sử dụng connection pooling để tránh quá tải.
    

Tóm lại, từ 100 đến 500 kết nối là một sự thay đổi lớn về tài nguyên. Nếu bạn thiếu tài nguyên, điều này có thể ảnh hưởng tiêu cực hiệu năng PostgreSQL, nên cần:

- Giám sát bộ nhớ, CPU,
    
- Cân nhắc dùng connection pooling thay vì chỉ tăng max_connections,
    
- Tối ưu các tham số bộ nhớ như work_mem theo giá trị max_connections mới.
    

Thông tin chi tiết và khuyến nghị này dựa trên phân tích các ảnh hưởng về bộ nhớ và hiệu suất của max_connections trong PostgreSQL.[cybertec-postgresql+2](https://www.cybertec-postgresql.com/en/tuning-max_connections-in-postgresql/)​

1. [https://www.cybertec-postgresql.com/en/tuning-max_connections-in-postgresql/](https://www.cybertec-postgresql.com/en/tuning-max_connections-in-postgresql/)
2. [https://postgresqlco.nf/doc/en/param/max_connections/](https://postgresqlco.nf/doc/en/param/max_connections/)
3. [https://techcommunity.microsoft.com/blog/adforpostgresql/analyzing-the-limits-of-connection-scalability-in-postgres/1757266](https://techcommunity.microsoft.com/blog/adforpostgresql/analyzing-the-limits-of-connection-scalability-in-postgres/1757266)
4. [https://stackoverflow.com/questions/60147360/what-is-the-ideal-number-of-max-connections-for-a-postgres-database](https://stackoverflow.com/questions/60147360/what-is-the-ideal-number-of-max-connections-for-a-postgres-database)
5. [https://www.reddit.com/r/PostgreSQL/comments/7d748u/simultaneous_connection_limits/](https://www.reddit.com/r/PostgreSQL/comments/7d748u/simultaneous_connection_limits/)
6. [https://www.postgresql.org/docs/current/runtime-config-connection.html](https://www.postgresql.org/docs/current/runtime-config-connection.html)
7. [https://help.sonatype.com/en/postgresql-max-connections.html](https://help.sonatype.com/en/postgresql-max-connections.html)
8. [https://access.redhat.com/solutions/1190783](https://access.redhat.com/solutions/1190783)
9. [https://jfrog.com/community/data-science/troubleshooting-high-cpu-utilization-in-postgresql-databases-a-how-to-guide/](https://jfrog.com/community/data-science/troubleshooting-high-cpu-utilization-in-postgresql-databases-a-how-to-guide/)
10. [https://learn.microsoft.com/en-us/answers/questions/770985/postgres-flexible-server-max-connections-parameter](https://learn.microsoft.com/en-us/answers/questions/770985/postgres-flexible-server-max-connections-parameter)