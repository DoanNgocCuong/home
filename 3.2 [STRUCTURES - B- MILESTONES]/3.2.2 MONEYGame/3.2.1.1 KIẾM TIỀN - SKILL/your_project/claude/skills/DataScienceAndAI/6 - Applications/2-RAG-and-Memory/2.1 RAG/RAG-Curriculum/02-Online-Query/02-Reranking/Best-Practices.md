# Reranking: Lọc Tài Liệu Dựa Trên Liên Quan

## Tổng Quan

Reranking là bước lọc thứ hai sau retrieval. Retriever của bạn có thể lấy 100 tài liệu "gần đúng", nhưng reranker sẽ xếp hạng lại chúng theo độ liên quan thực tế với query và context hiện tại.

**Sự khác biệt:**
- Retriever (bi-encoder): Nhanh, nhưng rough (~100-200ms cho 1000 docs)
- Reranker (cross-encoder): Chậm, nhưng chính xác (+20-35% improvement)

## Kiến Trúc Two-Stage Retrieval

```
Query: "Best practices for RAG systems"
         ↓
Step 1: BM25 + Vector (Bi-encoder)
        ✓ Fast: ~50ms
        ✓ Recall-focused: Retrieve top-100
         ↓
Step 2: Cross-Encoder Reranker
        ✓ Slow: ~200ms
        ✓ Precision-focused: Rerank top-100 → top-10
         ↓
Final Results: Top-10 documents (highest precision)
```

**Tại sao phải two-stage?**
- Direct reranking 10,000 documents: Không khả thi (quá chậm)
- Retrieve → Rerank: Thực tế nhất - balance giữa latency và accuracy

## Top Rerankers trong Production

### 1. Cohere Rerank-4 (Recommended)

```python
from cohere import Client

client = Client(api_key="YOUR_API_KEY")

# Rerank documents
results = client.rerank(
    query="What are best practices for RAG?",
    documents=[
        {"text": "RAG combines retrieval with generation..."},
        {"text": "Machine learning fundamentals..."},
        {"text": "Modern approaches to information retrieval..."},
    ],
    model="rerank-4-turbo",
    top_n=3  # Return top-3
)

# Output
for i, result in enumerate(results.results):
    print(f"{i+1}. Score: {result.relevance_score:.2f}")
    print(f"   {result.document['text'][:100]}...")
```

**Strengths:**
- Multilingual support (50+ languages)
- Retrieval-specific training
- Cost-effective: ~$0.001-0.002 per 1000 queries (with caching)

**Latency:** ~200-300ms per rerank call

### 2. BGE (BAAI General Embeddings) Reranker

```python
from sentence_transformers import CrossEncoder

# Open-source, self-hosted
model = CrossEncoder('BAAI/bge-reranker-v2-m3')

documents = [
    "RAG combines retrieval with generation...",
    "Machine learning fundamentals...",
]

scores = model.predict(
    [[query, doc] for doc in documents],
    show_progress_bar=False
)

# Sort by score
ranked = sorted(
    zip(documents, scores),
    key=lambda x: x[1],
    reverse=True
)
```

**Strengths:**
- Hoàn toàn open-source
- Tự host, không phí API
- Hỗ trợ multilingual

**Latency:** ~50-100ms per rerank call (trên GPU)

### 3. ColBERT v2 (Dense Passage Retrieval)

```python
from colbert.client.client import Client

colbert = Client(
    checkpoint="colbertv2.0",
    colbert_config=ColBERTConfig(doc_maxlen=300)
)

# ColBERT uses learned late interaction
results = colbert.search(
    query="RAG best practices",
    k=10,  # Top-10
    documents=all_documents
)
```

**Strengths:**
- Late interaction (more flexible than cross-encoder)
- Efficient indexing
- Good cho dense retrieval

## Impact: Định Lượng Cải Tiến

```
Baseline (BM25 + Vector, top-10):
    Precision@10: 0.65
    Recall@20: 0.72
    MRR: 0.58

After Adding Reranker:
    Precision@10: 0.78 (+20%)
    Recall@20: 0.85 (+18%)
    MRR: 0.71 (+22%)

Latency trade-off:
    Before: 50ms (retrieval)
    After: 50ms + 200ms = 250ms (acceptable for most apps)
```

## Implementation Pattern: LlamaIndex + Cohere

```python
from llama_index.postprocessor import CohereRerank
from llama_index.retrievers import BM25Retriever
from llama_index.llms import OpenAI

# Setup
llm = OpenAI(model="gpt-4")
bm25_retriever = BM25Retriever.from_defaults(
    docstore=docstore
)
reranker = CohereRerank(model="rerank-4-turbo")

# Retrieval pipeline
docs = bm25_retriever.retrieve("RAG best practices")
reranked_docs = reranker.postprocess_nodes(docs, query_str="...")

# Now send to LLM
response = llm.complete(
    prompt=f"Based on: {reranked_docs}\n\nAnswer: ..."
)
```

## Reranker Selection Matrix

| Criteria | Cohere Rerank-4 | BGE v2 | ColBERT |
|----------|-----------------|--------|---------|
| Latency | 200-300ms | 50-100ms | 100-150ms |
| Cost | $$ (API) | Free (self-host) | Free (self-host) |
| Multilingual | Excellent | Good | OK |
| Ease of Use | Highest | Medium | Lower |
| Accuracy | Highest | Very Good | Very Good |

**Recommendation:**
- **MVP/Demo:** BGE (free, good enough)
- **Production:** Cohere Rerank-4 (best quality, manageable cost)
- **High-throughput:** ColBERT (balanced latency & accuracy)

## Common Mistakes

❌ **Reranking 10,000 documents** → Quá chậm!
✓ Rerank top-100 sau retrieval → Balanced

❌ **Không cache reranker results** → Lãng phí compute
✓ Cache top-K reranked docs cho popular queries

❌ **Sử dụng cross-encoder như retriever** → Quá chậm!
✓ Use bi-encoder for retrieval, cross-encoder for reranking

## Key Takeaway

Reranking không phải luxury - nó nên là **standard practice** trong production RAG. Two-stage pipeline (retrieve top-100 → rerank top-10) cung cấp 20-35% precision improvement với latency vẫn chấp nhận được.

**Quick Win:** Thêm reranker vào hệ thống hiện tại của bạn với chỉ 10 dòng code - expected ROI: +25% accuracy với chi phí ~$100-200/tháng.
