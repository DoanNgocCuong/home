# Chiến Lược Truy Xuất (Retrieval Strategies)

## Tổng Quan

Ở Phase 2 (Online/Query), chiến lược truy xuất quyết định chất lượng của tài liệu được gửi tới LLM. Không phải tất cả các truy vấn đều bình đẳng - một số cần BM25, số khác cần vector embeddings, và những truy vấn phức tạp nhất cần kết hợp cả hai.

Nguyên tắc thực hành tốt nhất: **Bắt đầu với Hybrid, thêm Reranking, sau đó Multi-Query**.

## 1. Hybrid Search: BM25 + Vector Embeddings

Hybrid search kết hợp sức mạnh của lexical search (BM25) và semantic search (embeddings vector). Đây là chiến lược phổ biến nhất trong production.

**Tại sao Hybrid lại hiệu quả?**
- BM25: Xuất sắc với keyword matching, rare terms, exact phrases
- Vector: Hiểu ngữ nghĩa, paraphrases, synonyms
- Kết hợp: Bao phủ cả hai loại truy vấn

**Implementation với Weaviate (recommended):**

```python
from weaviate.classes.query import MetadataQuery

# Hybrid search - RRF (Reciprocal Rank Fusion)
response = client.graphql_raw_query(
    """
    {
      Get {
        Document(
          hybrid: {
            query: "machine learning best practices"
            alpha: 0.7  # 0.7 = 70% vector, 30% BM25
          }
          limit: 10
        ) {
          content
          _score
        }
      }
    }
    """
)
```

**Tuning `alpha` parameter:**
- `alpha: 0.5` - Cân bằng (recommended for most cases)
- `alpha: 0.7` - Semantic-heavy (concept search, paraphrases)
- `alpha: 0.3` - Keyword-heavy (specific terms, rare words)

## 2. Multi-Query Rewriting

Một truy vấn người dùng có thể không phải query tối ưu cho retriever. Multi-Query tạo ra các biến thể của truy vấn gốc để tăng recall.

**Concept:**
```
User Query: "How to optimize LLM inference?"
           ↓
    LLM Rewriter
           ↓
    Query 1: "LLM inference optimization techniques"
    Query 2: "Reducing latency in large language models"
    Query 3: "Efficient serving of neural networks"
           ↓
    Retrieve from all 3 queries → Deduplicate → Rerank
```

**Implementation với LlamaIndex:**

```python
from llama_index.retrievers import QueryFusionRetriever

# Multi-query with 3 rewrites
retriever = QueryFusionRetriever.from_defaults(
    llm=llm,
    retrievers=[vector_retriever, bm25_retriever],
    num_queries=3,  # Generate 3 rewrites
    mode="reciprocal_rerank"  # RRF for combining results
)

results = retriever.retrieve(
    "How to optimize LLM inference?"
)
```

**Khi nào sử dụng Multi-Query:**
- Complex questions (3+ concepts)
- Ambiguous queries
- Rare terminology
- Trade-off: +20% recall nhưng +3 lần latency

## 3. HyDE (Hypothetical Document Embeddings)

HyDE sinh ra một tài liệu giả định có thể trả lời truy vấn, sau đó dùng embedding của tài liệu giả để tìm các tài liệu thực tế tương tự.

**Tại sao hiệu quả:**
- Query embeddings thường không tối ưu (quá ngắn, không đủ context)
- Document embeddings được sinh từ nội dung đầy đủ (tốt hơn)
- HyDE khiến query embedding "trông giống" document embedding

**Implementation:**

```python
from llama_index.retrievers import HyDERetriever
from llama_index.llms import OpenAI

hyde_retriever = HyDERetriever.from_defaults(
    llm=OpenAI(model="gpt-4"),
    retriever=vector_retriever,
    prompt_template="""Please write a passage to answer the question: {query}"""
)

# HyDE sinh tài liệu giả, sau đó retrieve tương tự
results = hyde_retriever.retrieve("What is retrieval augmented generation?")
```

**Output của HyDE:**
```
Input Query: "What is RAG?"
↓
Generated Doc: "Retrieval-Augmented Generation (RAG) is a technique that combines
information retrieval with generative models. It first retrieves relevant
documents from a knowledge base, then uses them to augment the prompt for
the language model..."
↓
Embed generated doc → Find similar real documents
```

## 4. Query Rewriting (Structured Queries)

Một số vector database hỗ trợ metadata filtering. Query Rewriting chuyển truy vấn tự nhiên thành structured queries.

**Example:**
```python
# Query: "Find high-revenue projects from 2024"
# Rewrite to:
{
  "query": "projects",
  "filter": {
    "year": {"$eq": 2024},
    "revenue": {"$gt": 1000000}
  }
}
```

## Roadmap Thực Hành: Từ Đơn Giản đến Phức Tạp

```
Week 1: Hybrid Search (BM25 + Vector)
        ✓ Setup Weaviate/Qdrant
        ✓ Tune alpha parameter
        ✓ Benchmark on your dataset

Week 2: Add Reranking (Cross-Encoder)
        ✓ Implement cohere-rerank-4
        ✓ Measure +precision improvement
        ✓ Optimize for latency budget

Week 3: Optional - Multi-Query
        ✓ Only if recall < 0.7
        ✓ Add caching to offset latency
        ✓ Monitor token usage

Week 4: Optional - HyDE
        ✓ Try with semantic-heavy queries
        ✓ Compare against Multi-Query
        ✓ Decide which to keep
```

## Key Takeaway

Hybrid Search + Reranking là combo mạnh nhất cho hầu hết production RAG systems. Chỉ thêm Multi-Query hoặc HyDE nếu:
1. Recall score < 0.7
2. Bạn có latency budget để chịu (+3 lần retrieval time)
3. Queries của bạn phức tạp (3+ concepts)

**Metric để theo dõi:** Precision@K, Recall, NDCG, MRR. Không chỉ có one metric.
