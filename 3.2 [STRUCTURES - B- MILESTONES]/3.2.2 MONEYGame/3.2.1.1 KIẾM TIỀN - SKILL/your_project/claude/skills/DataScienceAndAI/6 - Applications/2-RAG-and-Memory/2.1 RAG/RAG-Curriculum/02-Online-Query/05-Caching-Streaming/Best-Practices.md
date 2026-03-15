# Caching & Streaming cho RAG

## Tổng Quan

Caching và streaming không phải optional - chúng là **essential** cho production RAG systems với cost tối ưu và UX tốt.

**Impact:**
- Caching: 60-75% cost reduction
- Streaming: 50% latency perception reduction (users feel faster)

## Prompt Caching: Cost Savings

OpenAI, Anthropic, Google đều cung cấp prompt caching. Ý tưởng đơn giản: LLM provider caches token embeddings của prompt/context thường xuyên lặp.

### How Prompt Caching Works

```
Request 1:
  System prompt (shared): 100 tokens
  Company docs (retrieved): 5000 tokens
  User query: 50 tokens
  → First hit: Process all 5150 tokens

Request 2 (same docs, different user query):
  System prompt (cached): 100 tokens  [HIT - reuse embeddings]
  Company docs (cached): 5000 tokens  [HIT - reuse embeddings]
  User query: 60 tokens  [NEW - process]
  → Second hit: Process only 60 new tokens
  → Savings: ~95% of input cost!
```

### OpenAI Prompt Caching Implementation

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# System prompt + documents (cache this)
system_prompt = """You are helpful assistant. Answer based on documents."""
company_docs = """# Company Handbook\n... [5000 tokens of docs]"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}  # Cache this
                },
                {
                    "type": "text",
                    "text": company_docs,
                    "cache_control": {"type": "ephemeral"}  # Cache this
                },
                {
                    "type": "text",
                    "text": "User query: What is our vacation policy?"  # Not cached
                }
            ]
        }
    ]
)

# Check cache usage
print(f"Cache creation: {response.usage.cache_creation_input_tokens}")
print(f"Cache read: {response.usage.cache_read_input_tokens}")
print(f"Input: {response.usage.input_tokens}")
```

**Cost Calculation:**
```
Cache write: $0.000005 per token
Cache read: $0.0000015 per token

Scenario:
- 100 RAG queries per day, same documents
- Cache 5000 tokens of docs

Day 1: 5000 tokens * $0.000005 = $0.025
Days 2-365: (60 new tokens + 5000 cached) * $0.0000015 * 364
         = (60 * $0.000005) + (5000 * $0.0000015) * 364
         = $0.0003 + $0.00263 per day
         = ~$1 for whole year

Savings: 96% compared to no caching ($25 without caching)
```

### Anthropic Prompt Caching

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are helpful assistant.",
        },
        {
            "type": "text",
            "text": """Company handbook: [5000 tokens of docs]""",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "What is RAG?",
        }
    ],
)

print(f"Usage: {response.usage}")
# usage.cache_creation_input_tokens: how many tokens cached
# usage.cache_read_input_tokens: how many tokens read from cache
```

## Semantic Caching: Smart Caching Beyond String Match

Semantic caching caches LLM responses berdasarkan query meaning, bukan exact string match.

### Example: Semantic Cache dengan Redis + Embeddings

```python
import redis
import json
from sentence_transformers import SentenceTransformer

# Setup
redis_client = redis.Redis(host='localhost', port=6379)
encoder = SentenceTransformer('all-MiniLM-L6-v2')
SIMILARITY_THRESHOLD = 0.95

class SemanticCache:
    def __init__(self, redis_client, encoder, threshold=0.95):
        self.redis = redis_client
        self.encoder = encoder
        self.threshold = threshold

    def get(self, query: str):
        """Get cached response if similar query exists"""
        query_embedding = self.encoder.encode(query)

        # Search Redis for similar embeddings
        # (Pseudo-code - use redis-py with vectors)
        results = self.redis.search(query_embedding, top_k=5)

        for cached_query, cached_embedding, cached_response in results:
            similarity = self._cosine_similarity(
                query_embedding, cached_embedding
            )
            if similarity > self.threshold:
                return cached_response  # Hit!

        return None  # Miss

    def set(self, query: str, response: str):
        """Cache query and response"""
        embedding = self.encoder.encode(query).tolist()
        self.redis.hset(
            f"semantic_cache:{query}",
            mapping={
                "embedding": json.dumps(embedding),
                "response": response,
                "timestamp": time.time()
            }
        )

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Usage
cache = SemanticCache(redis_client, encoder)

query = "What is Retrieval Augmented Generation?"

# Try cache
cached = cache.get(query)
if cached:
    return cached

# Cache miss - call LLM
response = llm.complete(query)
cache.set(query, response)
return response
```

**When cached query is asked slightly differently:**
```
Query 1: "Explain RAG"
Query 2: "What is Retrieval Augmented Generation?"
Query 3: "Tell me about RAG systems"

All 3 return same cached response (similarity > 0.95)
Savings: 2/3 of LLM calls
```

## Document-Level Caching

Cache embeddings dan retrieval results, bukan LLM responses.

```python
from functools import lru_cache
import hashlib

class DocumentCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_embeddings(self, doc_id: str):
        """Get cached embeddings for document"""
        key = f"doc_embeddings:{doc_id}"
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def cache_embeddings(self, doc_id: str, embeddings: list):
        """Cache document embeddings"""
        key = f"doc_embeddings:{doc_id}"
        self.redis.setex(
            key,
            ex=86400 * 7,  # 7 days TTL
            value=json.dumps(embeddings.tolist())
        )

    def get_retrieval_results(self, query: str, top_k: int = 10):
        """Get cached retrieval results"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        key = f"retrieval:{query_hash}:k{top_k}"
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def cache_retrieval(self, query: str, results: list, top_k: int = 10):
        """Cache retrieval results"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        key = f"retrieval:{query_hash}:k{top_k}"
        self.redis.setex(
            key,
            ex=3600,  # 1 hour TTL
            value=json.dumps(results)
        )

# Usage
cache = DocumentCache(redis_client)

# Check cache first
results = cache.get_retrieval_results("What is RAG?")
if not results:
    # Cache miss - retrieve from vector DB
    results = vector_db.search("What is RAG?", top_k=10)
    cache.cache_retrieval("What is RAG?", results)

return results
```

## Streaming Responses with vLLM

Streaming cho users cảm thấy response "nhanh hơn" vì họ thấy text generate real-time.

### SSE (Server-Sent Events) Streaming

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import json

app = FastAPI()
client = OpenAI(base_url="http://localhost:8000/v1", api_key="token")

@app.post("/query")
async def query_stream(question: str):
    """Stream RAG response to client"""

    # Retrieve documents
    docs = retriever.retrieve(question)
    context = "\n".join([d.text for d in docs])

    # Stream LLM response
    async def generate():
        with client.chat.completions.create(
            model="Llama-2-7b",
            messages=[
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {question}"
                }
            ],
            stream=True,  # Enable streaming
            max_tokens=500
        ) as stream:
            for chunk in stream:
                token = chunk.choices[0].delta.content
                if token:
                    # Send as Server-Sent Event
                    yield f"data: {json.dumps({'token': token})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### Frontend: Consume Streaming Response

```javascript
// JavaScript
fetch('/query?question=What+is+RAG', {
    method: 'POST'
})
.then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    function read() {
        reader.read().then(({done, value}) => {
            if (done) return;

            const text = decoder.decode(value);
            const lines = text.split('\n');

            lines.forEach(line => {
                if (line.startsWith('data: ')) {
                    const json = JSON.parse(line.slice(6));
                    document.getElementById('answer').innerHTML += json.token;
                }
            });

            read();  // Continue reading
        });
    }
    read();
});
```

**User Experience:**
```
Without Streaming:
[waiting 2 seconds...]
"RAG is retrieval augmented generation..."

With Streaming:
"R" (immediate feedback)
"RA"
"RAG"
"RAG is"
"RAG is retrieval..."
(feels like 2x faster!)
```

## Combining Cache + Streaming

Best practice: Check caches, stream if hit, stream LLM if miss.

```python
@app.post("/query-smart")
async def query_smart(question: str):
    # Try semantic cache first (fastest)
    cached = semantic_cache.get(question)
    if cached:
        async def cached_response():
            # Stream cached response character by character
            for char in cached:
                yield f"data: {json.dumps({'token': char})}\n\n"
                await asyncio.sleep(0.001)  # Simulate streaming
        return StreamingResponse(cached_response())

    # Cache miss - retrieve and stream
    docs = retriever.retrieve(question)

    async def generate():
        # Stream LLM response
        for chunk in client.chat.completions.create(..., stream=True):
            token = chunk.choices[0].delta.content
            yield f"data: {json.dumps({'token': token})}\n\n"

        # After generation, cache for next time
        semantic_cache.set(question, full_response)

    return StreamingResponse(generate())
```

## Key Takeaway

Caching + Streaming = ngắt từ "wait for response" thành "stream while generating":

1. **Prompt Caching:** 60-75% cost savings (enterprise feature)
2. **Semantic Caching:** Smart cache hit detection beyond exact match
3. **Document Caching:** Cache retrieval results (cheap, effective)
4. **Streaming:** UX improvement (feels 2x faster)

**Production stack:**
- OpenAI/Anthropic API → Use prompt caching
- Self-hosted vLLM → Implement semantic cache + streaming
- Both → Combine for maximum impact

**Time investment:** 4-6 hours untuk setup. **ROI:** 10-20x cost reduction + UX improvement.
