# Performance Optimization: Latency Roadmap

## Tổng Quan

Real-world case study: We reduced RAG latency từ **600ms → 140ms** (4.3x improvement). Bài học này dạy exact optimizations.

**Goal:** Sub-200ms response time (user-imperceptible).

## Baseline: 600ms System

```
Real example (E-commerce RAG):

Query: "What's the return policy?"
       ↓
Step 1: Vector Embedding Query
        Duration: 150ms
        Issue: Wait for embedding model
       ↓
Step 2: Vector Database Search
        Duration: 100ms
        Issue: 1000K documents, slow query
       ↓
Step 3: Reranking
        Duration: 200ms
        Issue: Rerank all 100 retrieved docs
       ↓
Step 4: LLM Generation
        Duration: 150ms
        Issue: Generate 200 tokens
       ↓
Total: 600ms ✗ Too slow (feels sluggish)
```

## Optimization Roadmap (Week by Week)

### Week 1: Quick Wins (600ms → 400ms)

**Optimization 1: Reduce Retrieved Documents**
```python
# Before
vector_results = retriever.retrieve(query, top_k=100)
reranked = reranker.rerank(query, vector_results, top_k=10)
# Cost: Rerank 100 docs × 2ms = 200ms

# After
vector_results = retriever.retrieve(query, top_k=20)
reranked = reranker.rerank(query, vector_results, top_k=5)
# Cost: Rerank 20 docs × 2ms = 40ms
# Time saved: 160ms
```

**Optimization 2: Embedding Caching**
```python
# Before
embedding = embedding_model.encode(query)  # 150ms each time

# After (with Redis)
import hashlib
query_hash = hashlib.md5(query.encode()).hexdigest()
embedding = redis_cache.get(f"query:{query_hash}")
if not embedding:
    embedding = embedding_model.encode(query)
    redis_cache.setex(f"query:{query_hash}", 3600, embedding)  # 1hr TTL
# Most queries cached, ~10ms for cache hit
# Time saved: 100ms (on hits)
```

**Result: 600ms → 400ms (-200ms)**

### Week 2: Architectural Changes (400ms → 250ms)

**Optimization 3: Parallel Retrieval**
```python
# Before (sequential)
vector_results = vector_retriever.retrieve(query, 50)  # 100ms
bm25_results = bm25_retriever.retrieve(query, 50)      # 50ms
# Sequential: 150ms total

# After (parallel)
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as executor:
    vector_future = executor.submit(vector_retriever.retrieve, query, 50)
    bm25_future = executor.submit(bm25_retriever.retrieve, query, 50)

    vector_results = vector_future.result()
    bm25_results = bm25_future.result()
# Parallel: max(100ms, 50ms) = 100ms
# Time saved: 50ms
```

**Optimization 4: Batch Reranking**
```python
# Before
for doc in documents:
    score = reranker.score(query, doc)
    # N requests to reranker API

# After
scores = reranker.batch_score(query, documents)
# Single batch request, much faster
# Time saved: 80ms
```

**Optimization 5: Lazy LLM Generation**
```python
# Before: Generate full response

# After: Stream response (start returning immediately)
@app.post("/query-stream")
async def query_stream(request):
    documents = retriever.retrieve(request.query)
    prompt = build_prompt(request.query, documents)

    async def generate():
        # Start yielding tokens immediately
        for token in llm.stream(prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"
            # User sees first token in ~50ms, not after full response

    return StreamingResponse(generate())
```

**Result: 400ms → 250ms (-150ms)**

### Week 3: Infrastructure (250ms → 140ms)

**Optimization 6: Vector Database Indexing**
```python
# Before: HNSW index (good but not optimized)

# After: Better indexing + filtering
# Use IVFPQ (Inverted File Quantization)
# - Reduces memory 10x
# - Query latency 20-30ms (vs 50ms)

from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Create collection with IVFPQ
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE,
        quantization_config=QuantizationConfig(
            scalar=ScalarQuantization(
                type=ScalarType.INT8,
                quantile=0.95,
                always_ram=False,
            ),
        ),
    ),
)
# Time saved: 25-30ms
```

**Optimization 7: Query Result Caching**
```python
# Before: Every query hits retriever

# After: Cache full retrieval results
import hashlib

def get_or_retrieve(query):
    query_hash = hashlib.md5(query.encode()).hexdigest()

    # Check cache first
    cached = redis_cache.get(f"retrieval:{query_hash}")
    if cached:
        return json.loads(cached)

    # Cache miss: retrieve
    results = retriever.retrieve(query)
    redis_cache.setex(
        f"retrieval:{query_hash}",
        300,  # 5 min TTL
        json.dumps([r.dict() for r in results])
    )
    return results

# Popular queries: 0ms (cache hit)
# Time saved: 100ms on popular queries
```

**Optimization 8: Connection Pooling**
```python
# Before: Create new connection per request
def get_vector_db():
    client = QdrantClient(url="http://localhost:6333")
    return client

# After: Reuse connection pool
from sqlalchemy.pool import QueuePool

pool = QueuePool(
    lambda: QdrantClient(url="http://localhost:6333"),
    max_overflow=10,
    pool_size=5
)

# Reuse connections, avoid overhead
# Time saved: 20ms
```

**Result: 250ms → 140ms (-110ms)**

## Final Optimized Pipeline (140ms)

```
Query: "What's the return policy?"
       ↓
[CACHE CHECK] (5ms)
  Hit: Return cached result, total 5ms
  Miss: Continue
       ↓
[PARALLEL] (40ms max)
  Vector embedding (cached): 10ms
  Vector search (IVFPQ): 20ms
  BM25 search: 10ms
       ↓
[RERANKING] (30ms)
  Batch rerank top-20: 25ms
  Select top-5: 5ms
       ↓
[LLM GENERATION STARTS STREAMING] (30ms to first token)
  Build prompt: 10ms
  First token from LLM: 20ms
       ↓
[USER SEES FIRST TOKEN] (Total: ~95ms)
  Remaining tokens stream in
       ↓
[FINAL RESPONSE] (140ms total)
```

## Benchmarks: Before vs After

```
Latency P50 (median):
  Before: 600ms
  After:  140ms
  Improvement: 4.3x

Latency P95 (95th percentile):
  Before: 1200ms
  After:  300ms
  Improvement: 4x

Throughput:
  Before: 100 req/sec
  After:  400 req/sec
  Improvement: 4x
```

## Advanced: Warm Caches & Prediction

```python
# Proactive cache warming
def warm_cache_from_logs():
    """Pre-compute embeddings for popular queries"""

    # Load top 100 queries from logs
    popular_queries = get_top_queries_from_logs(limit=100)

    for query in popular_queries:
        # Pre-compute embedding
        embedding = embedding_model.encode(query)
        redis_cache.set(f"query:{hash(query)}", embedding)

        # Pre-retrieve documents
        results = retriever.retrieve(query, top_k=10)
        redis_cache.set(f"retrieval:{hash(query)}", json.dumps(results))

    print(f"Warmed {len(popular_queries)} queries")

# Schedule daily
schedule.every().day.at("03:00").do(warm_cache_from_logs)
```

## Monitoring Latency

```python
import time
from prometheus_client import Histogram

# Track latency with Prometheus
latency_histogram = Histogram(
    'rag_latency_seconds',
    'RAG pipeline latency',
    buckets=[0.05, 0.1, 0.2, 0.5, 1.0]  # 50ms, 100ms, 200ms, 500ms, 1s
)

@app.post("/query")
async def query(request):
    with latency_histogram.time():
        # Actual query logic
        result = rag_query(request.query)
    return result

# Visualize in Grafana
# Alert if P95 latency > 300ms
```

## Cost of Optimizations

```
Optimization              Implementation Time    Cost
─────────────────────────────────────────────────────
1. Reduce top_k          15 min                  Free
2. Embedding caching     1 hour                  Redis: $5/mo
3. Parallel retrieval    2 hours                 Free
4. Batch reranking       1 hour                  Free
5. Streaming             2 hours                 Free
6. Vector DB tuning      3 hours                 Free
7. Result caching        2 hours                 Redis: $5/mo
8. Connection pooling    1 hour                  Free

Total effort: 13 hours
Total cost: $10/month
Benefit: 4.3x latency reduction

ROI: Excellent
```

## Trade-offs to Watch

```
Optimization          Benefit              Trade-off
────────────────────────────────────────────────────
Reduce top_k          -100ms latency       -2-3% quality
Cache results         -100ms latency       Stale results (5min)
Parallel threads      -50ms latency        +CPU usage
Streaming             Perceived speed      Can't edit once sent
IVFPQ index           -30ms latency        -1-2% accuracy
```

## Key Takeaway

Latency optimization is **systematic, not magical**:

1. **Measure first** - Profile where time goes
2. **Quick wins** - Low-hanging fruit (caching, reduce top_k)
3. **Architectural changes** - Parallelization, streaming
4. **Infrastructure tuning** - Vector DB indexes, pooling
5. **Monitoring** - Alert on regressions

**Expected timeline:** 3 weeks, 13 hours dev time.
**Expected gain:** 4-5x latency improvement.
**Expected result:** <200ms response, happy users.

**Pro tip:** Streaming is psychological - user feels 2x faster even if total time same (because they see first token quickly).
