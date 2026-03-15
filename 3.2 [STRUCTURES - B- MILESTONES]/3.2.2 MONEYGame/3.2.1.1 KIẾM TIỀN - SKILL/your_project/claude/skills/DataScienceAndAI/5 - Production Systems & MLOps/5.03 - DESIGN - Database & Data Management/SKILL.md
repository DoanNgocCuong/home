# Database Design & Data Management Best Practices — Production Systems

> **Domain:** 5.03 | **Group:** DESIGN | **Lifecycle:** Design Time
> **Last Updated:** 2026-03-13
>
> *Cơ sở dữ liệu là trái tim hệ thống; thiết kế tốt giúp tránh nightmares vận hành*

---

## 1. Overview

Databases are the most important subsystem in most applications. They determine latency, throughput, reliability, and operational burden. Bad schema design creates technical debt that multiplies with scale. This domain covers choosing the right database, designing schemas, optimizing queries, managing connections, and deploying safely.

The database landscape is fragmented: PostgreSQL (relational, ACID), MongoDB (document, flexible schema), Redis (in-memory cache), Elasticsearch (search and analytics). There's no universal answer—it depends on access patterns, consistency requirements, and scale.

Database decisions made at design time compound over years. Choose carefully; make future changes easy.

---

## 2. Core Principles

1. **Start Simple, Migrate When Needed** — Begin with boring, proven databases (PostgreSQL). Migrate to specialized databases (Redis, Elasticsearch) only when profiling shows specific bottlenecks.

2. **Schema First, Code Second** — Design schema carefully before writing application code. Schema changes at scale are painful.

3. **Consistency vs. Availability** — Choose your consistency model based on requirements. Most services accept eventual consistency for higher availability.

4. **Observability is Non-Negotiable** — Monitor query performance, connection pools, replication lag, storage growth. Dark databases cause production nightmares.

5. **Data is Precious** — Backups, recovery, migration are critical. Plan these before you have data to lose.

---

## 3. Best Practices

### 3.1 Database Selection Guide

**Practice:** Choose database based on access patterns, not hype

| Database | Best For | Avoid If |
|----------|----------|----------|
| **PostgreSQL** | ACID, complex queries, general purpose | Very high write throughput (100k+/sec) |
| **MySQL** | Web applications, proven, simple | Need complex JSON, need window functions (older versions) |
| **MongoDB** | Flexible schema, rapid prototyping, document storage | Need complex joins, ACID across multiple docs |
| **Redis** | Caching, sessions, rate limiting, real-time | Durability critical (no disk, RAM only) |
| **Elasticsearch** | Full-text search, analytics, log aggregation | Transactional consistency required |
| **DynamoDB** | AWS-native, highly available, pay-per-request | Complex queries, cost-predictability |
| **Cassandra** | Massive scale (1000s of nodes), high write throughput, geographic distribution | Small team, complex queries |
| **Neo4j** | Graph queries (relationships), social networks | Simple relational data |

### 3.2 Schema Design (Normalization vs. Denormalization)

**Practice:** Normalize by default; denormalize based on query patterns

- **Normalization (Normal Forms):**
  - **1NF**: No repeated groups (each cell has scalar value)
  - **2NF**: No partial dependencies (all non-key attributes depend on entire primary key)
  - **3NF**: No transitive dependencies (non-key attributes depend only on primary key)
  - **BCNF**: Every determinant is a candidate key
  - **Benefits**: No redundancy, less storage, easier updates
  - **Drawback**: More joins required (slower queries)

- **Denormalization:**
  - Store redundant data (e.g., user's email in both `users` and `orders` tables)
  - Eliminates joins; faster reads
  - Trade-off: Updates require changes in multiple places; risk of inconsistency
  - Use when: Read-heavy queries, acceptable staleness

- **Strategy:**
  - **Write-heavy**: Normalize (avoid redundancy, updates are fast)
  - **Read-heavy**: Denormalize or create materialized views (reads are fast, updates cost more)
  - **Example:**
    ```
    Normalized:
    SELECT o.id, u.email FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.id = 123;

    Denormalized:
    SELECT id, user_email FROM orders WHERE id = 123;
    (But user_email is stored in orders table, must update both places)
    ```

- **JSONB for Semi-Structured Data (PostgreSQL):**
  - Store flexible structure (product details vary) alongside structured data
  - Example:
    ```
    CREATE TABLE products (
      id BIGINT PRIMARY KEY,
      name TEXT,
      attributes JSONB  -- flexible, can vary per product
    );

    SELECT * FROM products
    WHERE attributes @> '{"color": "red"}';
    ```
  - Benefits: Flexible schema, queryable, indexable
  - Drawback: Less normalized, harder to aggregate

### 3.3 Index Strategy

**Practice:** Index strategically; measure impact before and after

- **Index Types:**
  - **B-tree (Default)**: General purpose, range queries, equality, sorting
  - **Hash**: Fast equality, not range or sorting
  - **GiST**: Geometric, full-text search, spatial
  - **GIN**: Useful for arrays, full-text search, JSONB

- **When to Index:**
  - Column frequently used in WHERE clause: `INDEX ON users(email)`
  - Column used in JOIN: `INDEX ON orders(user_id)`
  - Column used in ORDER BY: `INDEX ON orders(created_at)`
  - Combination of columns (composite index): `INDEX ON orders(user_id, created_at)`

- **When NOT to Index:**
  - Low cardinality (few unique values): `gender`, `status`
  - Columns rarely queried
  - Columns that change frequently (slows writes)

- **Index Maintenance:**
  - Indexes consume storage (2-3x table size common)
  - Indexes slow writes (must update index on every insert/update)
  - Monitor unused indexes; drop them
  - Rebuild indexes periodically to defragment

- **Example:**
  ```sql
  -- Good: Frequently filtered on email
  CREATE INDEX idx_users_email ON users(email);

  -- Bad: Only 2 values (male/female), not selective
  CREATE INDEX idx_users_gender ON users(gender);

  -- Good: Composite index for common WHERE + ORDER BY
  CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);

  -- Find unused indexes:
  SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
  ```

### 3.4 Query Optimization (EXPLAIN ANALYZE)

**Practice:** Profile slow queries; use EXPLAIN ANALYZE to understand execution plans

- **Slow Query Threshold:**
  - < 1ms: Fast
  - 1-100ms: Acceptable
  - > 100ms: Investigate
  - > 1s: Critical

- **EXPLAIN ANALYZE (PostgreSQL):**
  ```sql
  EXPLAIN ANALYZE
  SELECT o.id, o.total, u.email
  FROM orders o
  JOIN users u ON o.user_id = u.id
  WHERE o.created_at > '2026-03-01';

  Output:
  Seq Scan on orders o  (cost=0.00..50000.00 rows=100000)
    Filter: (created_at > '2026-03-01')
    -> Index Scan using idx_orders_user_id on users u  (cost=0.29..0.31 rows=1)
  ```

- **Terms:**
  - **Seq Scan**: Full table scan (slow, should have index)
  - **Index Scan**: Using index (fast)
  - **cost**: Estimated execution cost (lower is better)
  - **rows**: Estimated rows returned (often wrong for EXPLAIN, but EXPLAIN ANALYZE shows actual)
  - **Buffers**: Memory reads (cache hits) vs disk reads

- **Optimization Techniques:**
  - Add index on frequently filtered column
  - Use LIMIT to fetch only needed rows
  - Avoid SELECT * (fetch only needed columns)
  - Use EXPLAIN ANALYZE to verify improvement
  - Example:
    ```sql
    -- Slow: Seq scan on 1 million rows
    SELECT * FROM orders WHERE user_id = 123;

    -- Fast: Add index
    CREATE INDEX idx_orders_user_id ON orders(user_id);
    SELECT id, total FROM orders WHERE user_id = 123 LIMIT 1000;
    ```

- **Common Antipatterns:**
  - WHERE with function call (prevents index use): `WHERE LOWER(email) = 'john@example.com'`
    - Fix: `WHERE email = 'john@example.com'` (case-insensitive collation)
  - OR in WHERE without index on all columns
  - SELECT * (fetches unused columns)
  - Unbound subqueries returning large results

### 3.5 Connection Pooling (PgBouncer, HikariCP)

**Practice:** Use connection pooling to share connections and reduce overhead

- **Why:** Creating database connection (TCP handshake, auth, startup) is expensive (10-100ms). Reuse connections.

- **Architecture:**
  ```
  App 1 \
  App 2 -- Connection Pool -- Database
  App 3 /
  (100 app connections to 20 DB connections)
  ```

- **PgBouncer (PostgreSQL):**
  ```
  listen_addr = localhost
  listen_port = 6432
  databases = myapp = host=localhost port=5432 dbname=myapp
  pool_mode = transaction  # Connection per transaction
  max_client_conn = 1000   # Max app connections
  default_pool_size = 25   # Connections to DB
  ```
  - Modes:
    - **Session**: Hold connection for session (least pooling)
    - **Transaction**: Release after transaction (best pooling)
    - **Statement**: Release after statement (avoid if transactions > 1 statement)

- **HikariCP (Java):**
  ```java
  HikariConfig config = new HikariConfig();
  config.setJdbcUrl("jdbc:postgresql://localhost/myapp");
  config.setMaximumPoolSize(20);  // Max connections
  config.setMinimumIdle(5);       // Min idle connections
  config.setLeakDetectionThreshold(60000);  // Detect leaks
  HikariDataSource ds = new HikariDataSource(config);
  ```

- **Tuning:**
  - Pool size: Typically cores * 2-4 (more than 20-30 rarely helps)
  - Monitor pool exhaustion (max_conn_age, statement_timeout)
  - Enable leak detection

### 3.6 Transaction Isolation Levels

**Practice:** Choose isolation level based on consistency requirements; understand trade-offs

- **Isolation Levels (ACID):**

  1. **READ UNCOMMITTED** (weakest):
     - Transactions see uncommitted changes from other transactions (dirty reads)
     - Rarely used
     - Example: Transaction A updates balance to 100, Transaction B reads 100 before A commits. A rolls back, but B saw the change.

  2. **READ COMMITTED** (default):
     - Transactions see only committed changes (no dirty reads)
     - Non-repeatable reads possible (same row read twice sees different values)
     - Good balance of consistency and concurrency
     - Example: Transaction A reads balance (100), Transaction B updates balance (200) and commits, Transaction A reads same balance again (200).

  3. **REPEATABLE READ**:
     - Same transaction always reads same value (snapshot isolation)
     - Phantom reads possible (new rows appear)
     - Example: SELECT COUNT(*) returns 10, another transaction inserts a row, SELECT COUNT(*) still returns 10 in same transaction.

  4. **SERIALIZABLE** (strongest):
     - Transactions execute as if serialized (one after another)
     - No dirty reads, non-repeatable reads, or phantom reads
     - Slowest, most conflicts
     - Example: Mutual exclusion guaranteed, but high overhead.

- **Guidance:**
  - **READ COMMITTED**: Default, use for most applications
  - **REPEATABLE READ**: For reports (snapshot of data)
  - **SERIALIZABLE**: For critical financial transactions
  - PostgreSQL implements REPEATABLE READ and SERIALIZABLE via MVCC (Multi-Version Concurrency Control), not locking

- **Example:**
  ```sql
  BEGIN ISOLATION LEVEL READ COMMITTED;
  SELECT balance FROM accounts WHERE id = 1;  -- Gets committed value
  COMMIT;
  ```

### 3.7 ACID vs. BASE

**Practice:** Use ACID for transactions requiring consistency; BASE for distributed eventual consistency

- **ACID (Atomicity, Consistency, Isolation, Durability):**
  - All-or-nothing (atomicity)
  - Consistent state before and after
  - Isolated from other transactions
  - Written to disk (durable)
  - Example: Transfer $100 from account A to B atomically (both succeed or both fail)

- **BASE (Basically Available, Soft state, Eventually consistent):**
  - Basically Available: Always responds (may fail after time)
  - Soft state: Data may be in transit (temporary inconsistency acceptable)
  - Eventually Consistent: Will converge to consistent state eventually
  - Example: Social media like (propagates within seconds, not immediate)

- **When to Use:**
  - **ACID**: Payments, financial transfers, inventory reservations (correctness critical)
  - **BASE**: Social media, analytics, caches (eventual consistency acceptable)
  - Most production systems are hybrid: ACID for critical data, BASE for non-critical

### 3.8 Sharding Strategies

**Practice:** Shard based on access patterns when single database hits limits

- **What:** Partition data across multiple databases by key

- **Sharding Keys:**
  - **User ID** (most common): All user's data on same shard
  - **Account ID**: Multi-tenant isolation
  - **Geographic Region**: Comply with data residency laws
  - Avoid: Timestamp (creates hot shards), random (data scattering)

- **Sharding Architectures:**
  - **Range Sharding**: `shard = user_id / 1_000_000` (user 1-1M → shard 1, 1M-2M → shard 2)
  - **Hash Sharding**: `shard = hash(user_id) % num_shards` (consistent distribution)
  - **Directory Sharding**: Lookup table maps key to shard (flexible, requires lookup)

- **Challenges:**
  - Cross-shard queries are expensive (query all shards, aggregate results)
  - Resharding (changing shard count) requires data migration
  - Uneven distribution (hot shards take more load)
  - Complex application logic (know which shard to query)

- **When to Shard:**
  - Only when single database hits performance limits (> 100GB, > 1000 QPS)
  - Complexity high; use when needed, not before

- **Example:**
  ```
  -- Hash sharding
  shard_id = hash(user_id) % 4
  user_id 1, 5, 9, 13 → shard 1 (1 % 4 = 1)
  user_id 2, 6, 10, 14 → shard 2 (2 % 4 = 2)
  ```

### 3.9 Replication (Master-Slave, Multi-Master)

**Practice:** Use replication for high availability and read scaling

- **Master-Slave (Master-Replica):**
  - Master: Accepts reads and writes
  - Slave: Accepts reads only, receives changes from master
  - Failover: If master fails, promote slave to master
  - Benefits: Read scaling (queries to slaves), high availability
  - Limitation: Write still limited to master
  - Typical setup: 1 master, 2-3 slaves for redundancy

- **Multi-Master (Multi-Primary):**
  - Multiple databases accept writes
  - Changes replicate to other primaries
  - More complex, risk of conflicts
  - Use: Geographic distribution, no single point of failure
  - Challenges: Conflict resolution, network partition handling

- **Replication Types:**
  - **Synchronous**: Master waits for replica to confirm (slower, safer)
  - **Asynchronous**: Master doesn't wait (faster, risk of data loss)
  - **Semi-Synchronous**: Master waits for at least one replica (balance)

- **Example (PostgreSQL Streaming Replication):**
  ```
  Master: primary_conninfo = 'host=master'
  Slave: Connects to master, receives WAL (write-ahead log), applies changes

  If master fails: pg_ctl promote (promote slave to master)
  ```

- **Lag Monitoring:**
  - Replica lag: Delay between master write and slave application
  - If lag > 1 second, queries might see stale data
  - Monitor with: `SELECT pg_last_xlog_receive_location();`

### 3.10 Backup & Recovery Strategy

**Practice:** Test backups regularly; plan recovery time objectives (RTO) and recovery point objectives (RPO)

- **RTO/RPO:**
  - **RTO** (Recovery Time Objective): Max time acceptable to restore (goal: 1 hour)
  - **RPO** (Recovery Point Objective): Max data loss acceptable (goal: 1 hour)

- **Backup Types:**
  - **Full Backup**: Entire database (slow, large storage)
  - **Incremental**: Only changes since last backup (fast, smaller)
  - **Continuous**: Write-ahead log (WAL) backup, can restore to any point in time

- **Backup Location:**
  - Never on same hardware (will fail together)
  - Off-site (cloud, different data center)
  - Multiple copies (3-2-1 rule: 3 copies, 2 media, 1 off-site)

- **Testing:**
  - Regular recovery drills (monthly)
  - Test restore to different environment
  - Measure RTO (actual restore time)

- **Example (PostgreSQL):**
  ```
  -- Full backup
  pg_dump myapp > backup.sql

  -- Continuous WAL archiving
  archive_command = 'cp %p /archive/%f'

  -- Point-in-time restore
  restore_command = 'cp /archive/%f %p'
  recovery_target_time = '2026-03-13 14:30:00'

  -- Verify
  pg_restore -d myapp_restore backup.sql
  ```

### 3.11 Zero-Downtime Migration Strategy

**Practice:** Plan migrations carefully; execute in stages with rollback plan

- **Stages:**
  1. Create new schema alongside old (parallel run)
  2. Dual write: Write to both old and new
  3. Dual read: Read from new, compare results (validation)
  4. Cutover: Redirect all reads to new
  5. Cleanup: Drop old schema after stability period

- **Example (Postgres to Aurora):**
  ```
  Week 1: Set up Aurora, start dual-write
  Week 2: Dual read, validate data consistency
  Week 3: Cutover during low-traffic window, keep Postgres running
  Week 4: Monitor Aurora, then decommission Postgres
  ```

- **Rollback Plan:**
  - Always have route back to old system
  - Monitor metrics closely during cutover
  - Automated rollback if errors spike

### 3.12 Connection Leak Prevention

**Practice:** Monitor connection count; close connections explicitly

- **Common Leaks:**
  - Exception thrown before connection.close() (use try-with-resources)
  - Forgot to close connection
  - Connection timeout not set (thread hangs forever)

- **Prevention:**
  ```java
  // Bad: Connection leak if exception thrown
  Connection conn = dataSource.getConnection();
  PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users");
  ResultSet rs = stmt.executeQuery();  // Exception here leaves connection open
  conn.close();

  // Good: Auto-close ensures cleanup
  try (Connection conn = dataSource.getConnection()) {
    PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users");
    ResultSet rs = stmt.executeQuery();
  }  // Auto-closed even if exception
  ```

- **Monitoring:**
  - Connection pool metrics: Active, idle, waiting
  - Alert if active connections > 80% of max
  - Example: "Active: 18/20, Idle: 2, Waiting: 5"

### 3.13 Deadlock Detection & Prevention

**Practice:** Understand deadlock scenarios; design to prevent them

- **Deadlock Example:**
  ```
  Transaction A: locks Row 1, waits for Row 2
  Transaction B: locks Row 2, waits for Row 1
  Result: Deadlock, both wait forever
  ```

- **Prevention:**
  - Always acquire locks in same order (all transactions lock Row 1 before Row 2)
  - Use short transactions (less time holding locks)
  - Reduce lock scope (lock only necessary rows)

- **Detection:**
  - PostgreSQL auto-detects and kills one transaction
  - Monitor deadlock count: `SELECT checkpoints_timed FROM pg_stat_bgwriter;`
  - Alert if deadlocks frequent

- **Resolution:**
  ```sql
  -- Monitor locks
  SELECT * FROM pg_locks WHERE pid != pg_backend_pid();

  -- Kill blocking session
  SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE query LIKE '%UPDATE users%';
  ```

### 3.14 Slow Query Monitoring

**Practice:** Enable slow query log; regularly review top queries

- **PostgreSQL:**
  ```
  log_min_duration_statement = 1000  -- Log queries > 1 second
  log_duration = on
  log_statement = 'all'
  ```

- **MySQL:**
  ```
  slow_query_log = 1
  long_query_time = 2  -- Log queries > 2 seconds
  ```

- **Analysis Tools:**
  - `pgBadger` (PostgreSQL log analyzer)
  - `MySQL slow log parser`
  - `Percona Toolkit`

- **Action:**
  - Identify top 10 slowest queries
  - Add indexes, optimize query
  - Measure impact (EXPLAIN ANALYZE before/after)

### 3.15 Database-Per-Service Pattern (Microservices)

**Practice:** Each service owns its database; no shared databases

- **Benefits:**
  - Service independence: Can change schema without coordinating
  - Can use different database technology (Service A: PostgreSQL, Service B: MongoDB)
  - Easy to scale service independently
  - Failure isolation: If one database fails, only that service affected

- **Challenges:**
  - No cross-database joins (must do in application)
  - Distributed transactions hard (use sagas or event sourcing)
  - Operational overhead (multiple databases to maintain)

- **Communication:**
  - Services don't query each other's databases
  - Use APIs or event streams for data exchange
  - Example: Order service publishes OrderCreated event; Inventory service subscribes

- **Schema:**
  ```
  order-db: orders, order_items
  inventory-db: inventory, stock_levels
  user-db: users, profiles

  Order service publishes: OrderCreated (user_id, order_id)
  Inventory service listens and updates stock
  ```

### 3.16 CQRS Read Models & Materialized Views

**Practice:** Create denormalized copies optimized for queries

- **Materialized View:**
  - Pre-computed query result stored as table
  - Updated when source data changes
  - Example: Sales report aggregates order data
  - Benefits: Fast queries (pre-aggregated)
  - Cost: Storage, update latency

- **CQRS Read Model:**
  - Separate database for reads, optimized for queries
  - Source of truth writes to different database
  - Read model updated asynchronously
  - Example: Elasticsearch index for search

- **Implementation:**
  ```
  Command Model (PostgreSQL):
  INSERT INTO orders (user_id, total, status) VALUES (1, 100, 'pending');

  Event Published: OrderCreated (user_id: 1, total: 100)

  Read Model (Elasticsearch):
  Index updated: { order_id: 1, user_name: "John", total: 100, timestamp: ... }

  Query: GET /orders?user_id=1 reads from Elasticsearch (fast)
  ```

- **Trade-offs:**
  - Eventually consistent (read model lags behind)
  - Extra complexity (maintain two models)
  - Use when: Query performance critical, tolerate staleness

---

## 4. Decision Frameworks

### Database Selection Decision Tree

```
Need complex queries, ACID?
├─ Yes → PostgreSQL or MySQL
│  ├─ Complex JSON? → PostgreSQL (JSONB)
│  └─ Simple schema? → MySQL
└─ No, need flexibility?
   ├─ Document-oriented? → MongoDB
   ├─ Cache/sessions? → Redis
   ├─ Full-text search? → Elasticsearch
   └─ Massive scale? → Cassandra or DynamoDB
```

### When to Normalize vs. Denormalize

```
Read-heavy? (10:1 reads to writes)
├─ Yes → Denormalize, create views
└─ No → Normalize (3NF+)

Updates frequent?
├─ Yes → Normalize (avoid redundancy)
└─ No → Denormalize acceptable
```

### Replication Strategy

```
High availability needed?
├─ Yes → Master-Slave (1 master, 2+ slaves)
│  └─ Geographic distribution?
│     ├─ Yes → Multi-master (accept complexity)
│     └─ No → Master-slave sufficient
└─ No → Single database

Write scale?
├─ > 10k QPS → Master-slave insufficient, consider sharding
└─ < 10k QPS → Master-slave sufficient
```

---

## 5. Checklist

- [ ] Database choice documented and justified
- [ ] Schema designed and normalized (at least 3NF)
- [ ] Primary keys on all tables
- [ ] Foreign keys defined where appropriate
- [ ] Indexes created for frequently queried columns
- [ ] Indexes reviewed for unused/redundant ones
- [ ] Query performance profiled (EXPLAIN ANALYZE)
- [ ] Connection pooling configured
- [ ] Connection pool size tuned
- [ ] Slow query logging enabled and monitored
- [ ] Transaction isolation level chosen and documented
- [ ] Backup strategy implemented and tested
- [ ] RTO/RPO defined and measured
- [ ] Replication configured for HA
- [ ] Replication lag monitored
- [ ] Deadlock prevention considered
- [ ] Migration strategy documented
- [ ] Rollback plan exists
- [ ] Monitoring/alerting set up (disk space, connections, lag, slow queries)
- [ ] Data retention/cleanup policy defined
- [ ] Security: Least privilege database users, encrypted connections (SSL), audit logging
- [ ] GDPR/compliance: Data deletion procedures, audit trail

---

## 6. Common Mistakes & Anti-Patterns

### Missing Indexes
Queries do full table scans on 1 million rows. Performance is terrible until someone adds index.

**Fix:** Profile queries. Add indexes on frequently filtered columns.

### Over-Indexing
Hundreds of indexes slow down writes and consume storage. Index maintenance becomes nightmare.

**Fix:** Remove indexes with idx_scans = 0. Monitor index usage.

### Ignoring Slow Queries
Slow queries silently degrade performance. No one notices until latency spike.

**Fix:** Enable slow query log. Review top 10 slowest queries weekly.

### No Connection Pooling
Applications create new connections for every request. Connection creation overhead dominates.

**Fix:** Implement connection pooling. Configure pool size.

### Shared Database Across Services
Schema changes require coordination. Services tightly coupled through data layer.

**Fix:** Database-per-service pattern.

### No Replication / HA
Single database instance is single point of failure. If it crashes, entire system down.

**Fix:** Set up master-slave replication. Automatic failover.

### Backup Never Tested
Backup exists but recovery fails. Discovered during actual crisis.

**Fix:** Test recovery monthly. Measure actual RTO.

### Data Loss Due to No Backups
Application or database error deletes important data. No recovery possible.

**Fix:** Enable backups. Off-site storage. 3-2-1 rule.

### N+1 Queries
Loop of queries: fetch users (1 query), loop through users, fetch user's orders (N queries). Unnecessary traffic.

**Fix:** Use JOIN or batch load. Or use pagination if unavoidable.

### Unbounded Queries
`SELECT *` from table with billions of rows. OOM, query timeout.

**Fix:** Add LIMIT. Use pagination. Fetch specific columns.

### Not Monitoring Database
Database runs out of space, no one notices until it crashes.

**Fix:** Monitor disk usage, connection count, slow queries. Alert at 80% usage.

### Strong Consistency When Eventual Is Fine
Using locks and transactions everywhere. Performance suffers.

**Fix:** Accept eventual consistency for non-critical data.

---

## 7. Tools & References

### Database Tools

**PostgreSQL:**
- `psql`: Command-line client
- `pgAdmin`: Web UI
- `pg_dump`: Backup
- `pgBackRest`: Advanced backup/recovery
- `pgBadger`: Log analysis

**MySQL:**
- `mysql`: Command-line client
- `MySQLWorkbench`: GUI
- `mysqldump`: Backup
- `Percona Toolkit`: Utilities
- `Percona Monitoring and Management`: Monitoring

**Monitoring:**
- `pgAdmin`: PostgreSQL admin
- `Datadog`: Cloud monitoring
- `New Relic`: APM and database monitoring
- `Grafana + Prometheus`: Open-source monitoring

### Connection Pooling & Proxies
- **PgBouncer**: PostgreSQL connection pooler
- **ProxySQL**: MySQL connection pooler
- **HikariCP**: Java connection pool
- **pgpool-II**: PostgreSQL middleware
- **Pgbarman**: PostgreSQL backup and recovery manager

### Optimization & Tuning
- **EXPLAIN ANALYZE**: Query planner analysis
- **index_advisor**: Recommend missing indexes
- **pgStatStatements**: Track query statistics
- **New Relic APM**: Query performance insights

### Authoritative References
- **PostgreSQL Documentation**: Comprehensive, authoritative
- **MySQL Documentation**: Official MySQL reference
- **Percona Best Practices**: Production MySQL
- **AWS RDS Best Practices**: Cloud database patterns
- **"Designing Data-Intensive Applications"** by Martin Kleppmann: Comprehensive DB design book
- **High Performance MySQL** by Schwartz: MySQL optimization
- **PostgreSQL 14 Documentation**: Latest features, capabilities

### Real-World Case Studies
- **Stripe** (PostgreSQL at massive scale)
- **Uber** (Sharding, multi-data center)
- **Twitter** (Cassandra, real-time)
- **LinkedIn** (Kafka, event-driven)
- **Slack** (Data architecture evolution)

---

**Last Updated:** 2026-03-13 | **Version:** 1.0
