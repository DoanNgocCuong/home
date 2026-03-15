# Database Fundamentals

---

## 1. SQL vs NoSQL

### SQL (Relational)
- Structured data, schema cố định
- ACID transactions
- JOIN giữa các bảng
- Ví dụ: PostgreSQL, MySQL, Oracle

### NoSQL
- Flexible schema
- Horizontal scaling dễ hơn
- Nhiều loại: Document, Key-Value, Column, Graph

| Loại | Ví dụ | Use case |
|------|-------|----------|
| Document | MongoDB, CouchDB | User profiles, catalog |
| Key-Value | Redis, DynamoDB | Caching, sessions |
| Column | Cassandra, HBase | Time-series, analytics |
| Graph | Neo4j, Amazon Neptune | Social network, recommendations |

### Khi nào chọn gì?
- **SQL**: data có quan hệ phức tạp, cần ACID, schema ổn định
- **NoSQL**: data lớn, cần scale nhanh, schema thay đổi nhiều

---

## 2. ACID vs BASE

### ACID (SQL thường dùng)
- **A**tomicity: transaction thành công hoàn toàn hoặc rollback hoàn toàn
- **C**onsistency: data luôn hợp lệ theo rules
- **I**solation: transactions không ảnh hưởng nhau
- **D**urability: data đã commit thì không mất

### BASE (NoSQL thường dùng)
- **B**asically **A**vailable: hệ thống luôn sẵn sàng
- **S**oft state: state có thể thay đổi theo thời gian
- **E**ventually consistent: cuối cùng data sẽ nhất quán

---

## 3. Indexing

Index giống mục lục sách — giúp tìm data nhanh hơn mà không cần scan toàn bộ bảng.

**B-Tree Index**: default, tốt cho range queries và equality. **Hash Index**: tốt cho exact match, O(1) lookup. **Full-text Index**: tìm kiếm text.

**Trade-off**: index tăng tốc đọc nhưng làm chậm write (vì phải update index). Không nên index mọi thứ.

---

## 4. Sharding (Partitioning)

Chia data ra nhiều databases/machines.

### Horizontal Sharding
Chia theo rows. VD: User ID 1-1M ở shard 1, 1M-2M ở shard 2.

### Sharding Strategies
- **Range-based**: theo range (dễ hotspot)
- **Hash-based**: hash(key) % num_shards (phân bố đều)
- **Directory-based**: lookup table chỉ data ở shard nào

### Vấn đề với Sharding
- JOIN across shards rất khó
- Resharding khi thêm shard phức tạp
- Celebrity/hotspot problem

---

## 5. Replication

Sao chép data sang nhiều nodes để availability & read performance.

- **Single-Leader**: 1 leader nhận writes, replicate sang followers
- **Multi-Leader**: nhiều leaders (dùng cho multi-datacenter)
- **Leaderless**: quorum reads/writes (Cassandra, DynamoDB)

---

## 6. Database Scaling Strategies (theo thứ tự)

1. **Indexing** - thêm index cho queries chậm
2. **Read replicas** - tách read traffic sang replicas
3. **Caching** - cache hot data (Redis)
4. **Vertical scaling** - nâng cấp hardware
5. **Sharding** - chia data (phương án cuối, phức tạp nhất)

---

## Checklist Tự Kiểm Tra

- [ ] Chọn được SQL hay NoSQL cho một use case cụ thể và giải thích tại sao
- [ ] Giải thích ACID với ví dụ chuyển tiền ngân hàng
- [ ] Biết khi nào nên/không nên thêm index
- [ ] Hiểu 3 chiến lược sharding và trade-offs
- [ ] Biết thứ tự scale database (index → replicas → cache → vertical → sharding)
