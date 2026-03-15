# Cost Optimization: 60-75% Savings Strategy

## Tổng Quan

RAG systems có thể rất đắt - particularly LLM API calls. Bài học này dạy cách **cut 60-75% of costs** qua prompt caching, semantic caching, embedding caching.

Real case study: Reduced monthly LLM bill từ **$5,000 → $1,200** (76% savings).

## Cost Breakdown: Real Example

```
Monthly Traffic: 100K queries
Avg tokens per query: 2500 (input) + 250 (output)

Provider: OpenAI GPT-4
- Input: $0.000005 per token
- Output: $0.000015 per token

Cost per query:
  Input:  2500 × $0.000005 = $0.0125
  Output: 250 × $0.000015 = $0.00375
  Total:  $0.015625

Monthly cost: 100K × $0.015625 = $1,562.50

Pain point: Most queries are similar (company FAQs, documentation)
→ Many repeated retrievals and generation
→ Could save 60-75% if we reuse!
```

## Strategy 1: Prompt Caching (60-75% Savings)

**How it works:**
```
OpenAI charges per new token processed:
  - Write to cache: $0.000005 per token
  - Read from cache: $0.0000015 per token (70% cheaper)

System prompt (100 tokens, static):
  Week 1: Write to cache = $0.0005
  Weeks 2-4: Read from cache = $0.00045 total
  Monthly: Write once, read 99 times

Company docs (5000 tokens, per-query):
  Scenario A (no cache): 100K queries × $0.025 = $2500
  Scenario B (cache): 1st query $0.025 (write), rest read from cache
                      = $0.025 + (99,999 × $0.0075) = $750
  Savings: $1750/month (70%)
```

**Implementation:**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are helpful assistant",
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": company_docs_5000_tokens,
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": f"Answer: {user_question}"
                    # This part NOT cached (changes per query)
                }
            ]
        }
    ]
)

# Track savings
cache_created = response.usage.cache_creation_input_tokens  # $0.000005
cache_read = response.usage.cache_read_input_tokens         # $0.0000015
input_tokens = response.usage.input_tokens                  # Regular rate

total_cost = (cache_created * 0.000005 +
              cache_read * 0.0000015 +
              input_tokens * 0.000005)
```

## Strategy 2: Semantic Caching (40-60% Savings)

**Concept:**
```
Vanilla caching: Exact string match only
  Query 1: "What is RAG?"
  Query 2: "Tell me about retrieval augmented generation"
  → Different strings → No cache hit → Run both

Semantic caching: Similarity-based
  Query 1 & 2 both mean same thing (similarity > 0.95)
  → Use cached response from Query 1
  → Savings: -50% on similar queries
```

**Implementation with Redis:**
```python
from sentence_transformers import SentenceTransformer
import redis
import json
import hashlib
import numpy as np

class SemanticCache:
    def __init__(self, redis_host="localhost", threshold=0.92):
        self.redis = redis.Redis(host=redis_host)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight
        self.threshold = threshold

    def _cosine_similarity(self, a, b):
        """Calculate cosine similarity"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get(self, query: str) -> str:
        """Get cached response if similar query exists"""

        # Encode current query
        query_embedding = self.encoder.encode(query)

        # Get all cached queries
        keys = self.redis.keys("cache:*")
        for key in keys:
            cached_data = json.loads(self.redis.get(key))
            cached_embedding = np.array(cached_data["embedding"])

            # Check similarity
            similarity = self._cosine_similarity(query_embedding, cached_embedding)

            if similarity > self.threshold:
                # Hit! Return cached response
                self.redis.expire(key, 3600)  # Extend TTL
                return cached_data["response"]

        return None  # No similar query found

    def set(self, query: str, response: str, ttl: int = 3600):
        """Cache query and response"""

        embedding = self.encoder.encode(query).tolist()
        query_hash = hashlib.md5(query.encode()).hexdigest()

        self.redis.setex(
            f"cache:{query_hash}",
            ttl,
            json.dumps({
                "query": query,
                "embedding": embedding,
                "response": response
            })
        )

# Usage in RAG
cache = SemanticCache()

# Try semantic cache first
cached_response = cache.get(user_query)
if cached_response:
    return cached_response  # Hit! No LLM call needed

# Cache miss - call LLM
response = llm.complete(prompt)
cache.set(user_query, response)
return response
```

**Cost impact:**
```
Scenario: FAQ system, 100K monthly queries

Popular queries (10% of traffic = 10K):
  - Variations of same question ("What's return policy?", "How do I return?")
  - Semantic cache hit rate: 80%
  - Savings: 10K × 0.8 × $0.015625 = $125

Unpopular queries (90% of traffic):
  - More varied
  - Semantic cache hit rate: 20%
  - Savings: 90K × 0.2 × $0.015625 = $281.25

Total monthly savings: $406.25 (26%)
Combined with prompt caching: 26% + 70% = 96%... wait, that's double-counting.

Realistic combined savings:
  Prompt caching on 70% of cost: saves $1094
  Semantic cache on remaining 30%: saves $234
  Total: $1328/month (85% of original $1562)
  New cost: $234/month
```

## Strategy 3: Embedding Caching (30-40% Savings)

Embeddings are expensive too (especially with paid APIs like OpenAI).

```python
# Before: Embed query every time
def retrieve(query: str):
    # OpenAI embedding: $0.00002 per 1K tokens
    query_embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-3-large"
    )
    # For every query: ~$0.000002 (tiny but adds up)

# After: Cache embeddings
import hashlib

def retrieve_cached(query: str):
    query_hash = hashlib.md5(query.encode()).hexdigest()

    # Try cache
    cached = redis.get(f"embedding:{query_hash}")
    if cached:
        query_embedding = json.loads(cached)
        return vector_db.search(query_embedding)

    # Cache miss
    query_embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-3-large"
    )

    # Cache for 7 days
    redis.setex(
        f"embedding:{query_hash}",
        7 * 24 * 3600,
        json.dumps(query_embedding)
    )

    return vector_db.search(query_embedding)

# Savings on 100K queries:
#   Popular 10K (50% have embeddings cached): 5K × $0.000002 = $0.01
#   That's tiny per month, but combined strategies add up
```

## Strategy 4: Document-Level Caching (50% on retrieval cost)

Retrieval itself has costs (vector DB reads, data transfer).

```python
# Instead of retrieving docs every time for same query...

def get_top_documents_cached(query: str, top_k: int = 10) -> List[Document]:
    """Cache retrieval results"""

    cache_key = f"docs:{hashlib.md5(query.encode()).hexdigest()}:k{top_k}"

    # Try cache
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Retrieve from vector DB
    docs = vector_db.search(query, top_k=top_k)

    # Cache for 6 hours (docs don't change often)
    redis.setex(
        cache_key,
        6 * 3600,
        json.dumps([d.dict() for d in docs])
    )

    return docs
```

## Combined Strategy: Full Cost Optimization

```python
class CostOptimizedRAG:
    def __init__(self, redis_host="localhost"):
        self.redis = redis.Redis(host=redis_host)
        self.semantic_cache = SemanticCache()

    async def query(self, user_query: str, user_id: str = None):
        """Query with full cost optimization"""

        # Layer 1: Semantic cache (response-level)
        # If user asked similar question before, reuse response
        cached_response = self.semantic_cache.get(user_query)
        if cached_response:
            return cached_response

        # Layer 2: Document cache (retrieval-level)
        cache_key = f"docs:{hashlib.md5(user_query.encode()).hexdigest()}"
        docs = self.redis.get(cache_key)
        if docs:
            docs = json.loads(docs)
        else:
            # Retrieve fresh
            docs = await self.retrieve(user_query)
            # Cache for 6 hours
            self.redis.setex(cache_key, 6*3600, json.dumps(docs))

        # Layer 3: Prompt with caching
        # Use OpenAI prompt caching for docs + system prompt
        response = self.llm.complete(
            prompt=self.build_prompt_with_caching(user_query, docs)
        )

        # Cache final response for semantic queries
        self.semantic_cache.set(user_query, response)

        return response

# Cost savings breakdown:
#   Semantic cache: 25% of queries saved (response-level)
#   Doc cache: 50% of remaining queries saved (retrieval-level)
#   Prompt caching: 70% savings on remaining token costs
#
#   Total: 25% + (75% × 50%) + (37.5% × 70%) = 68% savings
```

## ROI Analysis: Cost vs Implementation

```
Current system cost: $5,000/month

Implementation cost breakdown:
  Prompt caching (OpenAI feature):    4 hours, $0/month
  Redis cache setup:                  8 hours, $50/month
  Semantic cache implementation:      16 hours, $0
  Monitoring & optimization:          8 hours/month, $0

Total dev time: 36 hours (~1 week)
Total monthly cost: $50 (Redis)

Savings: $5,000 - $1,200 = $3,800/month
ROI: 3,800 / (50 + hourly_rate×8) = positive within 1 month

Example with $50/hr rate:
  Dev cost: 36 × $50 = $1,800
  Monthly savings: $3,800
  Payback period: 0.47 months (2 weeks)
  Year 1 savings: $45,600 - $1,800 = $43,800

Excellent ROI!
```

## Monitoring Cost

```python
import time
from datetime import datetime, timedelta

class CostMonitor:
    def __init__(self):
        self.costs = []

    def log_query(self, query_cost: float, cache_hit: bool, cache_type: str):
        """Log cost and cache stats"""
        self.costs.append({
            "timestamp": datetime.now(),
            "cost": query_cost,
            "cache_hit": cache_hit,
            "cache_type": cache_type  # "semantic", "doc", "prompt"
        })

    def daily_report(self):
        """Generate daily cost report"""
        today = [c for c in self.costs
                if c["timestamp"].date() == datetime.now().date()]

        total_cost = sum(c["cost"] for c in today)
        cache_hits = sum(1 for c in today if c["cache_hit"])
        cache_hit_rate = cache_hits / len(today) if today else 0

        report = f"""
        Daily Report ({datetime.now().date()})
        ═══════════════════════════════════════
        Total cost: ${total_cost:.2f}
        Queries: {len(today)}
        Cache hit rate: {cache_hit_rate*100:.1f}%

        Cache breakdown:
          - Semantic: {sum(1 for c in today if c['cache_type']=='semantic')}
          - Document: {sum(1 for c in today if c['cache_type']=='doc')}
          - Prompt: {sum(1 for c in today if c['cache_type']=='prompt')}
        """

        # Alert if cost spike
        if total_cost > expected_daily_cost * 1.5:
            send_alert(f"Cost spike: ${total_cost:.2f} (2x expected)")

        return report

# Schedule daily
schedule.every().day.at("23:00").do(cost_monitor.daily_report)
```

## Key Takeaway

**Cost optimization is low-hanging fruit in RAG systems.**

Three strategies, increasing ROI:

1. **Prompt Caching** (60-70% savings)
   - Effort: 4 hours
   - Savings: Immediate, ongoing
   - Only for OpenAI/Anthropic APIs

2. **Semantic Caching** (25-40% additional)
   - Effort: 16 hours
   - Savings: $200-400/month
   - Works with any LLM

3. **Document Caching** (30-50% additional)
   - Effort: 8 hours
   - Savings: Small but combined effect large
   - Always worth doing

**Combined potential:** 60-75% reduction (in real scenario, 76%).

**Timeline:** 1 week development.
**ROI:** Payback in 2 weeks, compound savings for rest of year.

**Pro tip:** Start with prompt caching (free), layer in others. Monitor with cost_monitor to track savings.
