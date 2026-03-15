# Xử lý Concurrent User_ID: Thread Safety và Row-level Locking

## 📋 TÓM TẮT

Khi nhiều threads xử lý messages song song, hệ thống đảm bảo **thread safety** và **data integrity** thông qua:

1. **DB Session Isolation**: Mỗi thread có DB session riêng
2. **Row-level Locking**: `SELECT FOR UPDATE` để lock row khi update cùng `user_id`
3. **Connection Pool**: Đủ connections cho nhiều threads

---

## 🔍 3 TRƯỜNG HỢP

### Trường hợp 1: 2 user_id KHÁC NHAU

**Ví dụ:**

- Thread 1: xử lý `user_id = "user_A"`
- Thread 2: xử lý `user_id = "user_B"`

**Kết quả:**

```
✅ Xử lý song song HOÀN TOÀN (không conflict)
- Thread 1: Lock row user_A → Update → Commit → Unlock
- Thread 2: Lock row user_B → Update → Commit → Unlock
- Không có waiting, không có conflict
```

**Giải thích:**

- Mỗi thread lock row khác nhau
- Không có conflict về dữ liệu
- Xử lý song song 100%

---

### Trường hợp 2: 2 messages CÙNG user_id

**Ví dụ:**

- Thread 1: xử lý `user_id = "user_A"` (Message 1)
- Thread 2: xử lý `user_id = "user_A"` (Message 2)

**Kết quả:**

```
✅ Xử lý tuần tự với row-level lock (đảm bảo data integrity)

Timeline:
T0: Thread 1 bắt đầu → SELECT FOR UPDATE user_A → Lock thành công
T1: Thread 2 bắt đầu → SELECT FOR UPDATE user_A → CHỜ (lock bị block)
T2: Thread 1 commit → Unlock row
T3: Thread 2 nhận lock → SELECT FOR UPDATE user_A → Lock thành công
T4: Thread 2 commit → Unlock row

Kết quả:
- Thread 1: Xử lý xong trước
- Thread 2: Xử lý xong sau (nhưng có đầy đủ dữ liệu mới nhất)
- Không bị lost update ✅
```

**Giải thích:**

- `SELECT FOR UPDATE` lock row trong transaction
- Thread 2 phải chờ Thread 1 commit
- Đảm bảo không bị lost update (race condition)

---

### Trường hợp 3: Nhiều user_id KHÁC NHAU

**Ví dụ:**

- Thread 1: `user_id = "user_A"`
- Thread 2: `user_id = "user_B"`
- Thread 3: `user_id = "user_C"`
- ...
- Thread 10: `user_id = "user_J"`

**Kết quả:**

```
✅ Tất cả xử lý song song 100%
- Mỗi thread lock row riêng
- Không có waiting
- Performance tối đa
```

---

## 🔒 CƠ CHẾ BẢO VỆ

### 1. DB Session Isolation

**File: `src/app/background/rabbitmq_consumer.py`**

```python
def _process_message(self, delivery_tag: int, body: bytes):
    # ✅ Mỗi thread tạo DB session riêng
    db = SessionLocal()  # Thread-safe session factory
  
    # Mỗi thread có transaction riêng
    # Isolation level: READ COMMITTED (PostgreSQL default)
```

**Kết quả:**

- Thread 1 có transaction riêng
- Thread 2 có transaction riêng
- Không ảnh hưởng lẫn nhau

---

### 2. Row-level Locking với SELECT FOR UPDATE

**File: `src/app/repositories/friendship_status_repository.py`**

#### a) `apply_score_change()` - Update friendship_score

```python
def apply_score_change(self, user_id: str, score_change: float):
    # ✅ Lock row để tránh concurrent updates
    status = (
        self.db.query(self.model)
        .filter(self.model.user_id == user_id)
        .with_for_update()  # Row-level lock
        .first()
    )
  
    # Update score (thread-safe vì đã lock)
    status.friendship_score += score_change
    self.db.commit()  # Unlock sau khi commit
```

**Ví dụ với 2 threads cùng user_id:**

```
Thread 1:
  1. SELECT ... WHERE user_id='user_A' FOR UPDATE
     → Lock row user_A ✅
  2. friendship_score = 100 + 10 = 110
  3. COMMIT → Unlock row

Thread 2 (chờ Thread 1):
  1. SELECT ... WHERE user_id='user_A' FOR UPDATE
     → WAITING (row bị lock) ⏳
  2. (Sau khi Thread 1 commit) → Lock thành công ✅
  3. friendship_score = 110 + 20 = 130 (đúng!)
  4. COMMIT → Unlock row
```

---

#### b) `update_topic_metrics()` - Update topic_metrics JSONB

```python
def update_topic_metrics(self, user_id: str, topic_id: str, ...):
    # ✅ Lock row để tránh concurrent updates
    friendship = (
        self.db.query(self.model)
        .filter(self.model.user_id == user_id)
        .with_for_update()  # Row-level lock
        .first()
    )
  
    # Update JSONB (thread-safe vì đã lock)
    topic_metrics = friendship.topic_metrics or {}
    topic_metrics[topic_id]["score"] += score_change
    friendship.topic_metrics = topic_metrics
  
    # Force SQLAlchemy detect JSONB changes
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(friendship, "topic_metrics")
  
    self.db.commit()  # Unlock sau khi commit
```

**Ví dụ với 2 threads cùng user_id, khác topic:**

```
Thread 1: Update topic "movie"
  1. SELECT ... WHERE user_id='user_A' FOR UPDATE → Lock ✅
  2. topic_metrics["movie"]["score"] += 10
  3. COMMIT → Unlock

Thread 2: Update topic "dreams"
  1. SELECT ... WHERE user_id='user_A' FOR UPDATE → WAITING ⏳
  2. (Sau Thread 1) → Lock ✅
  3. topic_metrics["dreams"]["score"] += 20
  4. COMMIT → Unlock

Kết quả: 
- Cả 2 topics được update đúng
- Không bị mất dữ liệu ✅
```

---

### 3. Connection Pool

**File: `src/app/db/database_connection.py`**

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,      # 50 connections
    max_overflow=settings.DB_MAX_OVERFLOW, # 100 additional
    # Total: 150 connections max
)
```

**Kết quả:**

- Mỗi thread lấy 1 connection từ pool
- 10 threads = 10 connections (đủ)
- Connection được trả về pool sau khi commit/close

---

## 📊 SO SÁNH

### Không có SELECT FOR UPDATE (❌)

```
Thread 1: Read score = 100
Thread 2: Read score = 100 (cùng lúc)
Thread 1: Write score = 100 + 10 = 110
Thread 2: Write score = 100 + 20 = 120

Kết quả: Mất update của Thread 1! ❌
Final score = 120 (thiếu +10)
```

### Có SELECT FOR UPDATE (✅)

```
Thread 1: SELECT FOR UPDATE → Lock row
Thread 1: Read score = 100
Thread 1: Write score = 100 + 10 = 110
Thread 1: COMMIT → Unlock

Thread 2: SELECT FOR UPDATE → Wait (row locked)
Thread 2: (Sau Thread 1) → Lock row
Thread 2: Read score = 110 (đúng!)
Thread 2: Write score = 110 + 20 = 130
Thread 2: COMMIT → Unlock

Kết quả: Không mất update! ✅
Final score = 130 (đúng!)
```

---

## ✅ KẾT LUẬN

### User_id khác nhau:

- ✅ Xử lý song song 100%
- ✅ Không có waiting
- ✅ Performance tối đa

### Cùng user_id:

- ✅ Xử lý tuần tự với row-level lock
- ✅ Không bị lost update
- ✅ Data integrity đảm bảo

### Tổng hợp:

```
10 threads xử lý 10 messages:
- 5 user_id khác nhau → 5 threads xử lý song song
- 5 user_id giống nhau → 5 threads xử lý tuần tự (với lock)

Kết quả:
- Performance: Tốt (tận dụng song song khi có thể)
- Data integrity: Đảm bảo (lock khi cần)
```

---

## 🔗 LIÊN QUAN

- `SELECT FOR UPDATE`: Row-level locking (đã implement)
- `DB Session Isolation`: Mỗi thread có session riêng
- `Connection Pool`: Đủ connections cho nhiều threads
- `ThreadPoolExecutor`: Xử lý messages song song


---



Kiểm tra cách xử lý khi 2 user_id (hoặc cùng user_id) được xử lý song song:

[4 tools called]

Tóm tắt cách xử lý khi 2 user_id được xử lý song song:

[3 tools called]

Tạo tài liệu giải thích cách xử lý khi 2 user_id được xử lý song song:

[2 tools called]

Tóm tắt cách xử lý khi 2 user_id được xử lý song song:

## Cách xử lý khi 2 user_id được xử lý song song

### 1) DB session isolation — mỗi thread có session riêng

```python
# src/app/background/rabbitmq_consumer.py:226
db = SessionLocal()  # Mỗi thread tạo session riêng
```

Kết quả:

- Thread 1: DB session riêng, transaction riêng
- Thread 2: DB session riêng, transaction riêng
- Không ảnh hưởng lẫn nhau

---

### 2) Row-level locking — SELECT FOR UPDATE

#### a) Trường hợp 1: 2 user_id khác nhau

```
Thread 1: user_id = "user_A" → Lock row user_A ✅
Thread 2: user_id = "user_B" → Lock row user_B ✅

Kết quả: Xử lý song song 100% (không conflict)
```

#### b) Trường hợp 2: 2 messages cùng user_id

```
Thread 1: user_id = "user_A" → SELECT FOR UPDATE → Lock ✅
Thread 2: user_id = "user_A" → SELECT FOR UPDATE → CHỜ ⏳
         (chờ Thread 1 commit)

Sau khi Thread 1 commit:
Thread 2: Lock thành công → Xử lý với data mới nhất ✅

Kết quả: Không bị lost update!
```

---

### 3) Code đã implement

#### File: `src/app/repositories/friendship_status_repository.py`

```python
# apply_score_change() - Line 54-59
status = (
    self.db.query(self.model)
    .filter(self.model.user_id == user_id)
    .with_for_update()  # ✅ Row-level lock
    .first()
)

# update_topic_metrics() - Line 110-114
friendship = (
    self.db.query(self.model)
    .filter(self.model.user_id == user_id)
    .with_for_update()  # ✅ Row-level lock
    .first()
)
```

---

## Ví dụ cụ thể

### Scenario: 10 messages, 5 user_id khác nhau

```
Messages:
- Message 1-2: user_id = "user_A"
- Message 3-4: user_id = "user_B"  
- Message 5-6: user_id = "user_C"
- Message 7-8: user_id = "user_D"
- Message 9-10: user_id = "user_E"

Xử lý:
✅ Thread 1-2: Lock user_A → Xử lý tuần tự (2 messages cùng user)
✅ Thread 3-4: Lock user_B → Xử lý tuần tự
✅ Thread 5-6: Lock user_C → Xử lý tuần tự
✅ Thread 7-8: Lock user_D → Xử lý tuần tự
✅ Thread 9-10: Lock user_E → Xử lý tuần tự

Kết quả:
- 5 groups xử lý song song (user khác nhau)
- Mỗi group xử lý tuần tự (user giống nhau)
- Performance: Tối đa khi user_id khác nhau
- Data integrity: Đảm bảo khi user_id giống nhau
```

---

## Kết luận

1. User_id khác nhau: xử lý song song, không conflict
2. Cùng user_id: xử lý tuần tự với lock, không bị lost update
3. DB session: mỗi thread có session riêng, isolated
4. Row-level lock: `SELECT FOR UPDATE` đảm bảo data integrity

Đã tạo tài liệu chi tiết tại:
`docs/1_TaiLieuRobot_T2_24112025 - Robot/Tài liệu 3.18.5 Xử lý Concurrent User_ID - Thread Safety.md`

Cần giải thích thêm phần nào?