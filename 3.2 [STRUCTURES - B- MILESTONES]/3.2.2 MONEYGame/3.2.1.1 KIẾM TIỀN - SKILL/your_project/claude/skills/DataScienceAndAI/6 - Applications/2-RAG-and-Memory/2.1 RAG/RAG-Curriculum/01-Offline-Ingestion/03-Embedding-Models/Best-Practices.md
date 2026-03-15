# Embedding Models: Selection & Deployment 2025-2026

## Embedding models là gì?

Convert text → vector (list of numbers) representing semantic meaning.

```
Text: "The company reported record revenue."
        ↓
Embedding Model (e.g., BGE-M3)
        ↓
Vector: [0.23, -0.45, 0.67, 0.12, ..., 0.08]  (1024 dimensions)
        ↓
Store in Vector DB
        ↓
Can do similarity search
```

**Tại sao có nhiều models?**
- Trade-off: quality vs speed vs cost vs language support vs dimensionality
- Different use cases need different models

## Top Embedding Models 2025-2026

### 1. BGE-M3 (Open-source King)

**Specs:**
- Dimensions: 1024
- Languages: 100+ (including Vietnamese)
- MTEB score: 64.68 (very good for open-source)
- Size: 568MB
- Speed: ~1000 tokens/sec

**Ưu điểm:**
- ✓ Best open-source overall
- ✓ Multilingual (100+ languages, including Vietnamese)
- ✓ Free, run locally
- ✓ Dense + sparse + colbert retrieval
- ✓ Long context (8192 tokens)

**Nhược điểm:**
- ✗ Slower than OpenAI
- ✗ Requires GPU (or very slow on CPU)
- ✗ Memory: ~1.5GB

**Deployment:**
```python
from sentence_transformers import SentenceTransformer

# Local GPU
model = SentenceTransformer("BAAI/bge-m3", device="cuda")
embeddings = model.encode(
    ["Text 1", "Text 2"],
    batch_size=32,
    show_progress_bar=True
)

# Using Jina API (hosted, no GPU needed)
from jinaai.readers import JinaReader
import jinaai

jinaai.auth.token = "your_token"
embedder = jinaai.EmbeddingModels.bge_m3

result = embedder.embed_texts(["Text 1", "Text 2"])
```

**Best for:** Vietnamese projects, multilingual RAG, offline/self-hosted

---

### 2. Jina AI v3 (Long Documents King)

**Specs:**
- Dimensions: 1024
- Context window: 262,144 tokens (!)
- MTEB score: 65.71
- Language: English (multilingual in progress)
- Speed: ~2000 tokens/sec (API)

**Ưu điểm:**
- ✓ Handles LONG documents natively
- ✓ No chunking needed for many use cases
- ✓ Hosted API (no GPU needed)
- ✓ Fast API latency (~50ms)

**Nhược điểm:**
- ✗ Cost: ~$0.0001 per 1K tokens
- ✗ English-focused (Vietnamese support in v4?)
- ✗ Network dependency

**Deployment:**
```python
# Using Jina API
import requests

url = "https://api.jina.ai/v1/embeddings"
headers = {
    "Authorization": f"Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "model": "jina-embeddings-v3",
    "input": ["Long document text..."] * 100,
}

response = requests.post(url, headers=headers, json=data)
embeddings = response.json()['data']
```

**Cost analysis:**
- 100K documents × 500 tokens avg = 50M tokens
- Cost: 50M × $0.0001 / 1K = $5 (one-time)
- vs BGE-M3: $0 + GPU cost

**Best for:** Long-form documents, when Jina has better language support, cost not critical

---

### 3. OpenAI text-embedding-3-large (Quality Gold Standard)

**Specs:**
- Dimensions: 3072
- MTEB score: 64.90 (optimized for English)
- API latency: ~100ms
- Cost: $0.13 per 1M tokens

**Ưu điểm:**
- ✓ Best English quality (optimized by OpenAI)
- ✓ Fast API
- ✓ Dimension reduction supported (can use 256-dim)
- ✓ Stable, battle-tested

**Nhược điểm:**
- ✗ Cost: $0.13/1M tokens (vs free for BGE-M3)
- ✗ API dependency (rate limits, latency)
- ✗ Limited to 8191 tokens per request
- ✗ Proprietary

**Code:**
```python
from openai import OpenAI

client = OpenAI(api_key="your_key")

response = client.embeddings.create(
    input=["Text 1", "Text 2"],
    model="text-embedding-3-large",
    dimensions=1024  # Reduce from 3072 for cost
)

embeddings = [item.embedding for item in response.data]
```

**Cost per 100K docs (500 tokens avg):**
- Raw: 50M tokens × $0.13/1M = $6.50
- With dimension reduction: similar cost

**Best for:** Production systems, when quality > cost, English-only

---

### 4. Cohere embed-v4 (Multimodal in v5)

**Specs:**
- Dimensions: 1024
- MTEB score: 63.27
- Input types: Text, images (v5)
- Cost: $0.10 per 1M tokens

**Ưu điểm:**
- ✓ Multimodal (v5): text + images in same space
- ✓ Search-friendly (optimized for retrieval)
- ✓ Fast API

**Nhược điểm:**
- ✗ Lower MTEB than competitors
- ✗ Less adoption
- ✗ Multilingual support weaker

**Code:**
```python
import cohere

co = cohere.ClientV2(api_key="your_key")

response = co.embed(
    texts=["Text 1", "Text 2"],
    model="embed-english-v3.0",
    input_type="search_document"  # or "search_query"
)

embeddings = [item.embedding for item in response.embeddings]
```

**Best for:** Multimodal RAG, image + text retrieval

---

## MTEB Benchmark Comparison (Feb 2026)

| Model | MTEB | Language | Dims | Speed | Cost | Vietnamese |
|-------|------|----------|------|-------|------|------------|
| **BGE-M3** | 64.68 | 100+ | 1024 | Medium | Free | ✓ Good |
| **Jina v3** | 65.71 | EN | 1024 | Fast | ¢ Low | ✗ No |
| **OpenAI 3-large** | 64.90 | EN | 3072 | Fast | $ | ✗ No |
| **Cohere v4** | 63.27 | EN | 1024 | Fast | ¢ | ✗ No |

**MTEB ≠ RAG performance!** Higher MTEB = better semantic understanding, but RAG success depends on chunking + retrieval strategy.

---

## Decision Tree: Chọn embedding model nào?

```
1. Dữ liệu tiếng Việt?
   YES → BGE-M3 (best support)
   NO → continue

2. Documents > 10K tokens (need long context)?
   YES → Jina v3
   NO → continue

3. Cost không quan trọng, chỉ cần best quality?
   YES → OpenAI text-embedding-3-large
   NO → continue

4. GPU/infra sẵn?
   YES → BGE-M3 (free)
   NO → OpenAI hoặc Jina (API)

DEFAULT → BGE-M3 (best all-rounder)
```

---

## Deployment Options

### Self-hosted (BGE-M3)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

def embed_batch(texts, batch_size=32):
    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )

# Production: use async
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def embed_async(texts):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=2) as executor:
        embeddings = await loop.run_in_executor(
            executor,
            embed_batch,
            texts
        )
    return embeddings
```

**Infrastructure:**
- GPU: NVIDIA A100 (40GB) → 1000+ embeddings/sec
- Memory: 1.5GB for model + batch
- Cost: ~$2/hour on cloud

### API-based (OpenAI, Jina)

```python
from openai import OpenAI

client = OpenAI(api_key="key")

def embed_with_retry(texts, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                input=texts,
                model="text-embedding-3-large"
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# Batch processing
from tqdm import tqdm

def embed_all_documents(docs, batch_size=100):
    embeddings = []
    for i in tqdm(range(0, len(docs), batch_size)):
        batch = docs[i:i+batch_size]
        batch_embeddings = embed_with_retry([d['text'] for d in batch])
        embeddings.extend(batch_embeddings)
    return embeddings
```

---

## Vietnamese Embedding: Special Case

**Recommendation: BGE-M3**

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

# Vietnamese texts
texts = [
    "Công ty báo cáo doanh thu kỷ lục.",
    "Công ty công bố thu nhập đạt mức cao.",
]

embeddings = model.encode(texts)

# Check similarity (should be high, same meaning)
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print(f"Similarity: {similarity:.2%}")  # Should be 80%+ for synonyms
```

**Test on Vietnamese data before choosing!**

---

## Performance Tuning

**Batching:**
```python
# Bad: embed one by one
for text in texts:
    emb = model.encode(text)

# Good: batch embed
embeddings = model.encode(texts, batch_size=32)
# 10x faster
```

**Quantization** (reduce storage):
```python
# Reduce 1024-dim vector to 256-dim (75% storage save)
# with minimal accuracy loss

embeddings_full = model.encode(texts)
embeddings_reduced = embeddings_full[:, :256]

# Or use OpenAI dimension reduction
response = client.embeddings.create(
    input=texts,
    model="text-embedding-3-large",
    dimensions=256  # From 3072
)
```

---

## Common Mistakes

**❌ Wrong input_type**
```python
# Bad: mix query & document embeddings
query_emb = model.encode("What is revenue?")  # query
doc_emb = model.encode("Revenue was $5M")     # document
# Different spaces, bad retrieval

# Good: specify type
query_emb = embedder.encode(
    "What is revenue?",
    prompt_name="search_query"
)
doc_emb = embedder.encode(
    "Revenue was $5M",
    prompt_name="search_document"
)
```

**❌ Not normalizing**
```python
# Bad: use raw vectors
similarity = dot_product(emb1, emb2)  # Unstable

# Good: normalize first
import numpy as np
emb1_norm = emb1 / np.linalg.norm(emb1)
emb2_norm = emb2 / np.linalg.norm(emb2)
similarity = np.dot(emb1_norm, emb2_norm)  # Stable
```

---

## Jina Deployment Deep Dive

Since Jina is popular for long documents:

```python
# 1. Get API key from jina.ai
# 2. Install client
# pip install jina-client

import requests

class JinaEmbedder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.jina.ai/v1/embeddings"

    def embed(self, texts):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.url,
            headers=headers,
            json={
                "model": "jina-embeddings-v3",
                "input": texts,
            }
        )

        return [item['embedding'] for item in response.json()['data']]

# Usage
embedder = JinaEmbedder(api_key="your_key")
embeddings = embedder.embed(["Long document...", "Another doc..."])
```

---

## Key Takeaway

BGE-M3 is your default choice: best for Vietnamese, free, open-source, strong MTEB score. OpenAI text-embedding-3-large nếu quality + stability > cost. Jina v3 nếu documents rất dài (> 8K tokens) và cost OK. Test embedding quality trên YOUR data before committing (not just MTEB benchmark). Deployment: self-hosted với GPU nếu có infra; otherwise API-based. Batch processing, normalize vectors, specify input type (query vs document).
