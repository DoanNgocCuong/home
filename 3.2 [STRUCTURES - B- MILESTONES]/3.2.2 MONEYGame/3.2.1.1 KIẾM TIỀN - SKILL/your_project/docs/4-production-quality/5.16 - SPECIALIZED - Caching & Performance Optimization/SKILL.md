# Caching & Performance Optimization — Production Best Practices

> **Domain:** 5.16 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

Caching is the most impactful performance optimization technique. It works at every layer:
- **Database level**: Query cache, index optimization
- **Application level**: In-memory cache
- **HTTP level**: Browser & CDN cache
- **Network level**: Compression, connection pooling

**Core Principle:** Avoid repeating expensive operations.

**Impact Examples:**
- Single database query: 5ms → cached: <1ms (5x improvement)
- API call: 200ms → cached: <10ms (20x improvement)
- Cold container start: 2s → warm: 50ms (40x improvement)

## 2. Core Principles

### 2.1 Cache Strategy Selection

| Strategy | Write Model | Use Case | Trade-off |
|----------|-------------|----------|-----------|
| **Cache-Aside** | App decides | Read-heavy, slow updates | Cache miss penalty |
| **Write-Through** | Cache then DB | Consistency critical | Write latency |
| **Write-Behind** | Cache then async | High throughput | Data loss risk |
| **Read-Through** | Cache handles | Transparent to app | Complexity |

### 2.2 Key Trade-offs
- **Consistency vs Latency**: Stale data vs slow responses
- **Cost vs Performance**: Memory usage vs query time
- **Complexity vs Benefit**: Maintenance overhead vs improvement

## 3. Best Practices

### 3.1 Cache-Aside Pattern (Most Common)

**Practice: App Checks Cache First**

```python
def get_user_profile(user_id):
    # Check cache (kiểm tra bộ nhớ cache)
    cache_key = f"user:{user_id}"
    cached = redis.get(cache_key)

    if cached:
        return json.loads(cached)  # Cache HIT

    # Cache MISS - fetch from DB
    user = db.query(User).filter_by(id=user_id).first()

    # Store in cache with 1 hour TTL
    redis.setex(cache_key, 3600, json.dumps(user.to_dict()))

    return user.to_dict()
```

**Advantages:**
- Selective caching (only what you need)
- Cache updates are simple
- Failed cache doesn't break app

**Disadvantages:**
- Thundering herd on cache miss
- Must implement cache miss logic

**Anti-pattern:** Caching without TTL, leading to stale data.

### 3.2 Cache Invalidation Strategies

**Practice: Smart Invalidation Instead of Just TTL**

```python
# Strategy 1: Time-based (đơn giản nhất)
redis.setex("user:123", 3600, user_data)  # 1 hour TTL

# Strategy 2: Event-based (tốt hơn)
def update_user(user_id, new_data):
    db.session.update(User, new_data)
    db.session.commit()

    # Invalidate cache immediately
    redis.delete(f"user:{user_id}")

    # Publish event
    publisher.publish(f"user.updated.{user_id}")

# Strategy 3: Dependency-based (most complex)
def get_recommendations(user_id):
    cache_key = f"recommendations:{user_id}"

    # Check if user/settings changed
    user_version = db.get_version(f"user:{user_id}")
    cached_version = redis.get(f"{cache_key}:version")

    if user_version != cached_version:
        # Regenerate recommendations
        recommendations = compute_recommendations(user_id)
        redis.set(cache_key, recommendations)
        redis.set(f"{cache_key}:version", user_version)

    return redis.get(cache_key)
```

**Invalidation Patterns:**
1. **TTL only**: Simple, stale data risk (kiểm soát tuổi của dữ liệu)
2. **Event-driven**: Requires messaging, more complex
3. **On-demand**: Compute version, check on read
4. **Refresh-ahead**: Proactively refresh before TTL expires

**Anti-pattern:** Manual cache invalidation (developer forgets to delete).

### 3.3 Redis as Distributed Cache

**Practice: Cluster Mode for High Availability**

```python
from redis.cluster import RedisCluster

# Cluster mode (tự động sharding & failover)
rc = RedisCluster(
    startup_nodes=[
        {"host": "redis1", "port": 6379},
        {"host": "redis2", "port": 6379},
        {"host": "redis3", "port": 6379}
    ],
    skip_full_coverage_check=True,
    decode_responses=True
)

# TTL & Eviction policies
rc.setex(key, 3600, value)  # Auto-expire after 1 hour

# Eviction policy: LRU (least recently used)
# redis.conf: maxmemory-policy allkeys-lru
```

**Eviction Policies:**
- `allkeys-lru`: Remove least recently used key (최고의 일반적 선택)
- `volatile-lru`: Same, but only keys with TTL
- `allkeys-lfu`: Least frequently used
- `volatile-ttl`: Remove key with nearest TTL

**Connection Pooling for Redis:**
```python
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50
)
r = redis.Redis(connection_pool=pool)
```

### 3.4 CDN Caching for Static Assets

**Practice: CloudFront/Cloudflare Configuration**

```
Scenario: Serving images from CDN
- First request: User → CDN (miss) → Origin (100ms) = 100ms
- Second request: User → CDN (hit) = 5ms (20x improvement)

Cache headers to origin:
Cache-Control: public, max-age=31536000  # 1 year for immutable assets
Cache-Control: public, max-age=3600       # 1 hour for HTML/CSS

ETag: "abc123def456"  # Check if content changed
```

**Best Practices:**
- Immutable assets (include version/hash in filename)
- Set aggressive TTLs for versioned assets
- Short TTLs for dynamic content
- Use gzip compression

**Cost Impact:**
- Origin bandwidth: $0.085/GB
- CDN bandwidth: $0.015/GB (80% cheaper)
- 1TB/month: $85 → $15 (82% savings)

### 3.5 HTTP Caching Headers

**Practice: Proper Cache-Control Headers**

```
# Immutable versioned assets (cache forever)
Cache-Control: public, max-age=31536000, immutable
ETag: "v1.2.3-abc123"

# Dynamic content (validate with server)
Cache-Control: public, max-age=0, must-revalidate
ETag: "current-version"

# Private user data (browsers only, no CDN)
Cache-Control: private, max-age=3600

# No cache (always fetch fresh)
Cache-Control: no-cache, must-revalidate
Pragma: no-cache
```

**Vary Header (for mobile vs desktop):**
```
Vary: Accept-Encoding, User-Agent  # Cache separate versions
```

### 3.6 Application-Level Caching

**Practice: Function-Level Caching with Expiration**

```python
from functools import lru_cache
import time

# Simple in-process cache
@lru_cache(maxsize=128)
def expensive_calculation(x, y):
    time.sleep(5)  # Simulate expensive operation
    return x + y

# Cache with TTL
class CachedFunction:
    def __init__(self, func, ttl=60):
        self.func = func
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}

    def __call__(self, *args):
        if args in self.cache:
            if time.time() - self.timestamps[args] < self.ttl:
                return self.cache[args]

        result = self.func(*args)
        self.cache[args] = result
        self.timestamps[args] = time.time()
        return result

@CachedFunction(ttl=300)
def get_exchange_rate(currency_pair):
    # Fetch from API
    return api.get(f"/rates/{currency_pair}")
```

**Anti-pattern:** Unbounded cache growth leading to memory leaks.

### 3.7 Database Query Caching

**Practice: Query Result Caching with Invalidation**

```python
class CachedQuery:
    def __init__(self, cache_ttl=300):
        self.cache_ttl = cache_ttl

    def get_all_products(self):
        cache_key = "products:all:v1"

        # Try cache
        cached = redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Database query
        products = db.session.query(Product).all()
        result = [p.to_dict() for p in products]

        # Cache result
        redis.setex(cache_key, self.cache_ttl, json.dumps(result))
        return result

    def update_product(self, product_id, data):
        # Update DB
        db.session.execute(
            update(Product).where(Product.id == product_id).values(**data)
        )
        db.session.commit()

        # Invalidate caches
        redis.delete("products:all:v1")  # All products cache
        redis.delete(f"product:{product_id}")  # Specific product

        # Publish event for other services
        publish_event("product.updated", product_id)
```

**N+1 Query Problem Prevention:**
```python
# BAD: N+1 queries
users = db.query(User).all()
for user in users:
    print(user.name, user.orders)  # N additional queries!

# GOOD: Eager loading with cache
users = db.query(User).options(
    joinedload(User.orders)
).all()

# Cache query with relationships
cache_key = "users:with:orders"
if not redis.get(cache_key):
    users = db.query(User).options(
        joinedload(User.orders)
    ).all()
    redis.setex(cache_key, 3600, serialize(users))
```

### 3.8 Connection Pooling

**Practice: Database Connection Pooling**

```python
from sqlalchemy import create_engine

# Pool configuration
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20,           # Connections in pool
    max_overflow=40,        # Additional connections allowed
    pool_recycle=3600,      # Recycle connection after 1 hour
    pool_pre_ping=True      # Verify connection before use
)

# For HTTP requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=100)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Connection pooling impact
# Without: ~50 requests/sec
# With pooling: ~500 requests/sec (10x improvement)
```

### 3.9 Cache Stampede Prevention

**Practice: Prevent Multiple Queries on Simultaneous Misses**

```python
import hashlib
import time

def get_user_data_with_lock(user_id):
    cache_key = f"user:{user_id}"
    lock_key = f"lock:{cache_key}"

    # Try to get from cache
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Try to acquire lock
    lock_id = hashlib.md5(str(time.time()).encode()).hexdigest()
    acquired = redis.set(lock_key, lock_id, nx=True, ex=5)

    if acquired:
        # Lock acquired, fetch data
        data = expensive_query(user_id)
        redis.setex(cache_key, 3600, json.dumps(data))
        redis.delete(lock_key)
        return data
    else:
        # Lock not acquired, wait for other thread
        for _ in range(50):
            time.sleep(0.1)
            cached = redis.get(cache_key)
            if cached:
                return json.loads(cached)

        # Fallback if still missing
        return expensive_query(user_id)

# Probabilistic early expiration (más elegante)
def get_with_probabilistic_refresh(key, ttl=3600):
    value = redis.get(key)
    if value:
        # Refresh probability increases near expiration
        ttl_remaining = redis.ttl(key)
        refresh_probability = (1 - ttl_remaining / ttl) ** 2

        if random.random() < refresh_probability:
            # Async refresh
            background_task.queue(refresh_cache_value, key)

        return value

    return compute_fresh_value(key, ttl)
```

### 3.10 Performance Profiling

**Practice: Identify Bottlenecks with Profiling**

```python
import cProfile
import pstats
from io import StringIO
import time

# CPU profiling
profiler = cProfile.Profile()
profiler.enable()

# Code to profile
expensive_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative').print_stats(10)  # Top 10 functions

# Memory profiling
from memory_profiler import profile

@profile
def process_data(data):
    result = []
    for item in data:
        result.append(expensive_transform(item))
    return result

# Line-by-line timing
import timeit

time_taken = timeit.timeit(
    lambda: function_to_test(),
    number=1000
)
print(f"Average: {time_taken / 1000 * 1000:.2f}ms")
```

**Key Metrics:**
- CPU usage per request
- Memory per request
- Database query time
- External API call time
- Cache hit rate (cache hit / total requests)

## 4. Decision Frameworks

### Cache TTL Selection
- **Never changes** (versioned assets): 1 year
- **Rarely changes** (product catalog): 1 day
- **Changes hourly** (trending data): 5-15 minutes
- **Real-time** (stock prices): 1-5 seconds or no cache

### Caching vs Database Optimization
1. **Try DB optimization first** (indexing is free)
2. **If still slow** → add cache layer
3. **If cache miss is expensive** → implement warming/prefetching

## 5. Checklist

- [ ] Cache strategy defined (cache-aside vs write-through)
- [ ] Cache invalidation strategy implemented
- [ ] Redis cluster running with auto-failover
- [ ] CDN configured for static assets
- [ ] HTTP cache headers properly set
- [ ] Cache hit rate monitored (target: >80%)
- [ ] Connection pooling configured
- [ ] N+1 query problems identified & fixed
- [ ] Cache stampede prevention implemented
- [ ] Performance profiling tools available
- [ ] Latency SLAs defined & monitored
- [ ] Cache memory limits set with eviction policy

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Cache without TTL | Stale data forever | Set appropriate TTL |
| Caching sensitive data | Security issue, privacy breach | Exclude PII from cache |
| Unbounded cache | OOM crashes | Set maxmemory, eviction policy |
| Cache-aside without lock | Thundering herd, DB overload | Implement distributed lock |
| Ignoring N+1 queries | 100x slower queries | Use eager loading |
| Not monitoring cache hit rate | Don't know if cache works | Track hit/miss ratio |
| Synchronous cache writes | Slow responses | Write cache async |
| Hard-coded cache keys | Cache invalidation failures | Use cache key versioning |

## 7. Tools & References

**Caching Solutions:**
- Redis, Memcached, Aerospike
- Varnish (reverse proxy), Nginx
- CloudFront, Cloudflare, Akamai

**Profiling & Monitoring:**
- Python: cProfile, memory_profiler, py-spy
- APM: DataDog, New Relic, Elastic
- Benchmarking: wrk, Apache JMeter, Locust

**Best Practices:**
- "Cache-Aside pattern" (AWS documentation)
- "Scaling to Millions of Requests" (Yelp Engineering)
- "High Performance Browser Networking" (O'Reilly book)
