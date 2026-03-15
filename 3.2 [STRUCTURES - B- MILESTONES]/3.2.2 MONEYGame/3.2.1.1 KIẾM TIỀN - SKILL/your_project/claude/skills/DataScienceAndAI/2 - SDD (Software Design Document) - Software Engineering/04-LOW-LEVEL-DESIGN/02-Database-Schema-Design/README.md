# Database Schema Design - Thiết Kế Schema Cơ Sở Dữ Liệu

## Database Schema là gì?

Database Schema là bản thiết kế của cơ sở dữ liệu - định nghĩa các bảng (tables), cột (columns), kiểu dữ liệu (data types), constraints, indexes, và mối quan hệ giữa các bảng.

**Schema trả lời các câu hỏi:**
- Những bảng nào sẽ tồn tại?
- Mỗi bảng có những cột nào?
- Kiểu dữ liệu của mỗi cột là gì?
- Cột nào là primary key? Foreign key?
- Cần những index nào để tối ưu performance?

## Ví dụ đơn giản

```sql
-- Bảng users
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng posts
CREATE TABLE posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng comments
CREATE TABLE comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Normalization - Chuẩn hoá dữ liệu

Normalization là quá trình tổ chức dữ liệu trong database để loại bỏ dư thừa (redundancy) và các dị thường (anomalies).

### 1NF - First Normal Form (Dạng chuẩn thứ nhất)

**Quy tắc:** Mỗi cột chỉ chứa **một giá trị đơn** (atomic value), không có lặp lại các nhóm.

❌ **Không tuân thủ 1NF:**
```sql
-- BAD: Cột phone chứa multiple values
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    phones VARCHAR(100)  -- "123456, 789012, 345678"
);
```

✅ **Tuân thủ 1NF:**
```sql
-- GOOD: Mỗi hàng chỉ có một giá trị
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE user_phones (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    phone VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Cách kiểm tra:** Bất kỳ cột nào cũng không được chứa danh sách giá trị hay mảng.

### 2NF - Second Normal Form (Dạng chuẩn thứ hai)

**Quy tắc:** Phải đạt 1NF + **mỗi cột phụ (non-key) phải phụ thuộc vào toàn bộ primary key**, không được phụ thuộc vào một phần của primary key (partial dependency).

❌ **Không tuân thủ 2NF:**
```sql
-- BAD: Composite primary key (course_id, student_id)
-- Nhưng instructor_name phụ thuộc vào course_id (không phụ thuộc student_id)
CREATE TABLE enrollments (
    course_id INT,
    student_id INT,
    instructor_name VARCHAR(100),  -- Phụ thuộc vào course_id, không student_id
    grade VARCHAR(2),
    PRIMARY KEY (course_id, student_id)
);
```

✅ **Tuân thủ 2NF:**
```sql
CREATE TABLE courses (
    id INT PRIMARY KEY,
    instructor_name VARCHAR(100)
);

CREATE TABLE enrollments (
    course_id INT,
    student_id INT,
    grade VARCHAR(2),
    PRIMARY KEY (course_id, student_id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

**Cách kiểm tra:** Nếu primary key là composite (2+ cột), hãy kiểm tra xem tất cả non-key columns có phụ thuộc vào **toàn bộ** primary key không.

### 3NF - Third Normal Form (Dạng chuẩn thứ ba)

**Quy tắc:** Phải đạt 2NF + **không có transitive dependency** (một cột phụ thuộc vào cột không phải primary key).

❌ **Không tuân thủ 3NF:**
```sql
-- BAD: student_city phụ thuộc vào student_state (không phải primary key)
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    student_state VARCHAR(50),
    student_city VARCHAR(50)  -- city phụ thuộc state
);
```

✅ **Tuân thủ 3NF:**
```sql
CREATE TABLE states (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    state_id INT,
    FOREIGN KEY (state_id) REFERENCES states(id)
);
```

**Cách kiểm tra:** Hãy hỏi: "Cột này phụ thuộc vào primary key hay phụ thuộc vào cột khác?" Nếu phụ thuộc vào cột khác, hãy tách ra.

### So sánh 1NF, 2NF, 3NF

| Đặc điểm | 1NF | 2NF | 3NF |
|---------|-----|-----|-----|
| Atomic values | ✓ | ✓ | ✓ |
| No partial dependency | - | ✓ | ✓ |
| No transitive dependency | - | - | ✓ |
| Dư thừa dữ liệu | Cao | Vừa | Thấp |
| Performance | Nhanh | Vừa | Chậm hơn |

## Denormalization - Bỏ chuẩn hoá

Denormalization là việc **cố ý** thêm dữ liệu dư thừa vào database để tăng hiệu suất (performance).

Khi nào **NÊN** denormalize:

1. **Read-heavy queries**: Hệ thống có nhiều read hơn write
2. **Complex joins**: Phải join nhiều bảng gây chậm
3. **Real-time reporting**: Cần tính toán nhanh
4. **Caching mốn không**: Dữ liệu không thay đổi thường xuyên

### Ví dụ Denormalization

❌ **Normalized (3NF) - Slow for reading:**
```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Query: SELECT product.name, category.name FROM products
-- JOIN categories ON products.category_id = categories.id
-- Cần JOIN, chậm nếu có nhiều products
```

✅ **Denormalized - Fast for reading:**
```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    category_id INT,
    category_name VARCHAR(100),  -- Copy dữ liệu từ categories table
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Query: SELECT name, category_name FROM products
-- Không cần JOIN, nhanh hơn
```

**Tradeoff:** Khi update category_name, phải update cả products table.

## Indexing Strategies - Chiến lược Indexing

Index giúp tăng tốc độ query bằng cách tạo một cấu trúc dữ liệu dạng cây để tìm kiếm nhanh.

### Loại Index

#### 1. Primary Key Index (Tự động)
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT
    -- Index này tự động được tạo
);
```

#### 2. Unique Index
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE  -- Tự động tạo UNIQUE index
);

-- Hoặc tạo explicit:
CREATE UNIQUE INDEX idx_email ON users(email);
```

#### 3. Single Column Index
```sql
CREATE TABLE posts (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    created_at TIMESTAMP
);

-- Index cho frequent WHERE clause
CREATE INDEX idx_user_id ON posts(user_id);
CREATE INDEX idx_created_at ON posts(created_at);
```

#### 4. Composite Index (Multi-column)
```sql
-- Index cho query: SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC
CREATE INDEX idx_user_created ON posts(user_id, created_at DESC);
```

**Lưu ý:** Thứ tự cột trong composite index rất quan trọng!

#### 5. Full-Text Index (Cho search)
```sql
CREATE TABLE articles (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT
);

-- Index cho full-text search
CREATE FULLTEXT INDEX idx_fulltext ON articles(title, content);

-- Usage: SELECT * FROM articles WHERE MATCH(title, content) AGAINST('keyword');
```

### Khi nào tạo Index?

| Tình huống | Nên tạo? | Ví dụ |
|-----------|---------|------|
| Cột trong WHERE clause | ✓ | `WHERE user_id = 5` |
| Cột trong ORDER BY | ✓ | `ORDER BY created_at DESC` |
| Cột trong JOIN | ✓ | `ON users.id = posts.user_id` |
| Cột trong SELECT nhiều lần | ✓ | Frequent column |
| Cột ít được query | ✗ | Rarely queried column |
| Cột với low cardinality | ✗ | Boolean, gender, status |
| Cột hay được UPDATE | ✗ | Slows down writes |

### Index Trade-offs

**Pros:**
- Tăng tốc độ query (SELECT)

**Cons:**
- Tăng thời gian INSERT, UPDATE, DELETE (phải update index)
- Chiếm thêm disk space
- Phải maintain index

## Common Patterns (Mẫu phổ biến)

### Pattern 1: Soft Delete

Thay vì xóa dữ liệu, ta đánh dấu là deleted.

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255),
    deleted_at TIMESTAMP NULL,  -- NULL = not deleted
    INDEX idx_deleted_at (deleted_at)
);

-- Để xóa user:
UPDATE users SET deleted_at = NOW() WHERE id = 123;

-- Để query non-deleted users:
SELECT * FROM users WHERE deleted_at IS NULL;

-- Để restore user:
UPDATE users SET deleted_at = NULL WHERE id = 123;
```

**Lợi ích:**
- Dữ liệu không bị mất
- Có thể restore
- Keep historical data

**Nhược điểm:**
- Mọi query phải thêm WHERE deleted_at IS NULL
- Disk space thêm

### Pattern 2: Audit Trail (Lịch sử thay đổi)

Giữ lịch sử mọi thay đổi.

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Audit table
CREATE TABLE user_audit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    old_email VARCHAR(255),
    new_email VARCHAR(255),
    old_name VARCHAR(100),
    new_name VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_changed (user_id, changed_at)
);

-- Trigger: Automatically log changes
CREATE TRIGGER user_audit_trigger
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_audit (user_id, old_email, new_email, old_name, new_name, changed_by)
    VALUES (NEW.id, OLD.email, NEW.email, OLD.name, NEW.name, CURRENT_USER());
END;
```

### Pattern 3: Polymorphic Associations

Một cột "belongs to" multiple types.

```sql
CREATE TABLE comments (
    id BIGINT PRIMARY KEY,
    content TEXT,
    created_by BIGINT,
    -- Có thể comment trên posts hoặc articles
    commentable_type VARCHAR(50),  -- 'Post' hoặc 'Article'
    commentable_id BIGINT,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_commentable (commentable_type, commentable_id)
);

-- Query: SELECT * FROM comments WHERE commentable_type = 'Post' AND commentable_id = 123;
```

### Pattern 4: Tree Structure (Bố-con hierarchy)

Cho nested comments, categories, ...

```sql
CREATE TABLE categories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    parent_id BIGINT,  -- NULL cho root categories
    FOREIGN KEY (parent_id) REFERENCES categories(id),
    INDEX idx_parent_id (parent_id)
);

-- Hierarchy:
-- Electronics (id=1, parent_id=NULL)
--   Computers (id=2, parent_id=1)
--     Laptops (id=3, parent_id=2)
--     Desktops (id=4, parent_id=2)
--   Phones (id=5, parent_id=1)

-- Query: Get all descendants of Computers
-- Có thể dùng recursive query:
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 as level
    FROM categories
    WHERE id = 2  -- Computers

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree;
```

### Pattern 5: Time-Series Data

Cho events, logs, metrics, ...

```sql
CREATE TABLE events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    event_type VARCHAR(50),
    event_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_created (user_id, created_at),
    INDEX idx_event_created (event_type, created_at)
);

-- Partition by month (cho old data)
-- Thay vì có 1 bảng lớn, ta có nhiều bảng nhỏ
-- events_2026_01, events_2026_02, ...
```

### Pattern 6: JSON Column (NoSQL in SQL)

Lưu structured data mà không cần tách bảng.

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255),
    profile JSON,  -- Lưu profile data dưới dạng JSON
    INDEX idx_email (email)
);

-- Data:
{
    "id": 1,
    "email": "john@example.com",
    "profile": {
        "firstName": "John",
        "lastName": "Doe",
        "preferences": {
            "theme": "dark",
            "notifications": true
        }
    }
}

-- Query:
SELECT * FROM users WHERE JSON_EXTRACT(profile, '$.preferences.theme') = 'dark';
```

## Ví dụ: Blog System Schema

```sql
-- Users
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_deleted_at (deleted_at)
);

-- Categories
CREATE TABLE categories (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_slug (slug)
);

-- Posts
CREATE TABLE posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    content LONGTEXT NOT NULL,
    excerpt VARCHAR(500),
    featured_image_url VARCHAR(255),
    view_count INT DEFAULT 0,
    is_published BOOLEAN DEFAULT false,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    INDEX idx_user_id (user_id),
    INDEX idx_category_id (category_id),
    INDEX idx_slug (slug),
    INDEX idx_published (is_published, published_at DESC),
    INDEX idx_created (created_at DESC),
    FULLTEXT INDEX idx_fulltext (title, content)
);

-- Comments
CREATE TABLE comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_id BIGINT NULL,  -- For nested comments
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_approved (is_approved),
    INDEX idx_created (created_at)
);

-- Tags
CREATE TABLE tags (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_slug (slug)
);

-- Post-Tag Junction Table (Many-to-Many)
CREATE TABLE post_tags (
    post_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    INDEX idx_tag_id (tag_id)
);

-- Likes
CREATE TABLE likes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_post_user (post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Post Audit (History)
CREATE TABLE post_audit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    action VARCHAR(50),  -- 'CREATE', 'UPDATE', 'PUBLISH', 'DELETE'
    old_title VARCHAR(255),
    new_title VARCHAR(255),
    old_content LONGTEXT,
    new_content LONGTEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_post_changed (post_id, changed_at),
    INDEX idx_action (action)
);
```

## Database Design Checklist

- [ ] Mọi table có primary key?
- [ ] Mọi relationship có foreign key?
- [ ] Schema normalized đến 3NF (trừ intentional denormalization)?
- [ ] Có index cho frequently queried columns?
- [ ] Có index cho JOIN columns?
- [ ] Performance bottlenecks được xác định?
- [ ] Data types chính xác (INT vs BIGINT, VARCHAR vs TEXT)?
- [ ] Null constraints đúng?
- [ ] Unique constraints được đặt?
- [ ] Audit trail hoặc soft delete cho important tables?
- [ ] Documentation rõ ràng về schema?

---

**Tiếp theo:** Xem `/04-Sequence-Diagrams/README.md` để học về sequence diagrams.
