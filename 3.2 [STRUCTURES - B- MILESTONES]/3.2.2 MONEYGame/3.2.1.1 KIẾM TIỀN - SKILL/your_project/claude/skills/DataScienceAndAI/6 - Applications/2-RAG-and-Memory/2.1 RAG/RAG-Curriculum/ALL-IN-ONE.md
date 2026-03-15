
# PHẦN A: CLAUDE - RAG ALL-IN-ONE: Production Guide cho AI Engineer

> **Tài liệu tổng hợp toàn diện** — Kiến trúc, Best Practices, Benchmarks, Folder Structure
>
> Cập nhật: March 2026 | Phiên bản: 1.0
>
> Tác giả: Doan Ngoc Cuong & AI Team

---

## MỤC LỤC

1. [Kiến trúc High-Level Design](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#1-ki%E1%BA%BFn-tr%C3%BAc-high-level-design)
2. [Phase 1: Offline Ingestion Pipeline](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#2-phase-1-offline-ingestion-pipeline)
3. [Phase 2: Online Query Pipeline](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#3-phase-2-online-query-pipeline)
4. [Phase 3: Evaluation Loop Continuous](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#4-phase-3-evaluation-loop-continuous)
5. [Production Benchmarks &amp; Metrics](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#5-production-benchmarks--metrics)
6. [Recommended Tech Stack 2026](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#6-recommended-tech-stack-2026)
7. [Folder Structure Best Practices](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#7-folder-structure-best-practices)
8. [Advanced RAG Architectures](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#8-advanced-rag-architectures)
9. [Cost Analysis &amp; Optimization](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#9-cost-analysis--optimization)
10. [References](https://claude.ai/local_sessions/local_c1dab5ad-c3f1-4fed-b235-c5df643b3a6a#10-references)

---

## 1. KIẾN TRÚC HIGH-LEVEL DESIGN

### 1.1 Tổng quan 3 Pha

Mọi hệ thống RAG production đều vận hành theo 3 pha. Không có ngoại lệ.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES (Raw Documents)                     │
│            PDFs, HTML, DOCX, JSON, Database, API, Crawl             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
         ╔═════════════════╧═══════════════════════╗
         ║   PHASE 1: OFFLINE INGESTION PIPELINE   ║
         ║   (Chạy batch khi có document mới)      ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   Document    Chunking    Embedding        ║
         ║   Parsing  →  Strategy →  Model     →  Vector DB
         ║      ↓                                     ║
         ║   Metadata Enrichment (NER, tags, summary) ║
         ║                                            ║
         ╚════════════════════╤═══════════════════════╝
                              │
                    Knowledge Base Ready
                              │
         ╔════════════════════╧═══════════════════════╗
         ║   PHASE 2: ONLINE QUERY PIPELINE           ║
         ║   (Real-time mỗi khi user hỏi)            ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   User Query                               ║
         ║      ↓                                     ║
         ║   Query Processing (rewrite, expand)       ║
         ║      ↓                                     ║
         ║   Hybrid Retrieval (Vector + BM25)         ║
         ║      ↓                                     ║
         ║   Reranking (cross-encoder)                ║
         ║      ↓                                     ║
         ║   Context Assembly + Prompt Template       ║
         ║      ↓                                     ║
         ║   LLM Generation (streaming)               ║
         ║      ↓                                     ║
         ║   Response + Sources + Tracing             ║
         ║                                            ║
         ╚════════════════════╤═══════════════════════╝
                              │
         ╔════════════════════╧═══════════════════════╗
         ║   PHASE 3: EVALUATION LOOP CONTINUOUS      ║
         ║   (Chạy liên tục, không ngừng cải thiện)  ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   Langfuse Tracing  →  RAGAS Metrics       ║
         ║      ↓                                     ║
         ║   Monitor Quality (Faithfulness, Relevancy)║
         ║      ↓                                     ║
         ║   Capture Failures → Curate Eval Dataset   ║
         ║      ↓                                     ║
         ║   A/B Test Configs → Deploy Improvements   ║
         ║                                            ║
         ╚════════════════════════════════════════════╝
```

### 1.2 Data Flow Chi Tiết — Ví Dụ Thực Tế

```
OFFLINE (chạy 1 lần khi upload document):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report.pdf (5MB, 200 trang)
    → PyMuPDF Parser (giữ heading, table, page number)
    → RecursiveCharacterTextSplitter (512 tokens, overlap 50)
    → 400 chunks (mỗi chunk ~2KB text + metadata)
    → BGE-M3 Embedding (1024-dim vector mỗi chunk)
    → Qdrant Vector DB (HNSW index, cosine similarity)
    + Metadata: {source, page, section, date, author}

ONLINE (chạy real-time mỗi query):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User: "Báo cáo nói gì về revenue Q4?"
    → Cache check: miss                          [5ms]
    → BGE-M3 encode query → vector               [25ms]
    → Qdrant: hybrid search top-20                [15ms]
    → BGE-reranker-v2-m3: rerank → top-5          [80ms]
    → Prompt template + 5 contexts                [5ms]
    → vLLM (Qwen 2.5): generate + stream          [50ms TTFT]
    → Response: answer + source references
    → Langfuse: log trace                          [async]
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Total: ~180ms to first token, ~400ms full response

EVALUATION (chạy hàng ngày/tuần):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    → Pull 100 random traces from Langfuse
    → Run RAGAS: Faithfulness=0.85, Relevancy=0.82
    → Compare vs baseline (last week: 0.80, 0.78)
    → Identify: 12 queries faithfulness < 0.5
    → Root cause: missing context from legal section
    → Fix: add legal docs to ingestion pipeline
    → Re-eval → Faithfulness=0.89 ✓
```

### 1.3 Latency Budget — Mỗi component được bao nhiêu ms?

```
Production Target: P95 < 2.5 giây (end-to-end)
Optimized Target:  P50 < 200ms (to first token)

┌─────────────────────────────┬──────────┬──────────┬──────────────┐
│ Component                   │ Baseline │ Optimized│ Budget       │
├─────────────────────────────┼──────────┼──────────┼──────────────┤
│ Cache check                 │    5ms   │    5ms   │ < 10ms       │
│ Query embedding             │  150ms   │   25ms   │ < 30ms       │
│ Vector search               │  100ms   │   15ms   │ < 20ms       │
│ BM25 search (parallel)      │   50ms   │   10ms   │ < 15ms       │
│ Reranking (top-20 → top-5)  │  200ms   │   80ms   │ < 100ms      │
│ Prompt construction         │   10ms   │    5ms   │ < 10ms       │
│ LLM TTFT (first token)      │  200ms   │   50ms   │ < 80ms       │
│ LLM full generation         │  500ms   │  200ms   │ < 300ms      │
├─────────────────────────────┼──────────┼──────────┼──────────────┤
│ TOTAL (to first token)      │  715ms   │  180ms   │ < 250ms      │
│ TOTAL (full response)       │ 1215ms   │  390ms   │ < 500ms      │
└─────────────────────────────┴──────────┴──────────┴──────────────┘

Optimization roadmap: 1215ms → 390ms = 3.1x improvement
```

---

## 2. PHASE 1: OFFLINE INGESTION PIPELINE

### 2.1 Document Parsing

 **Nhiệm vụ** : PDF/HTML/DOCX → clean text + metadata

 **Best Practice 2026** : Dùng hybrid multimodal parsing (text + vision model cho complex layouts).

| Format               | Tool khuyến nghị                  | Lý do                          |
| -------------------- | --------------------------------- | ------------------------------ |
| PDF (text-based)     | PyMuPDF (fitz)                    | Nhanh nhất, giữ được structure |
| PDF (scanned/images) | Unstructured + Tesseract OCR      | Handle được image-in-PDF       |
| PDF (complex layout) | Vision LM (GPT-4V, Qwen-VL)       | Tables, charts, diagrams       |
| HTML                 | BeautifulSoup + MarkdownConverter | Giữ heading hierarchy          |
| DOCX                 | python-docx                       | Native support                 |

 **Rule** : Output luôn convert sang Markdown — preserves structure tốt nhất cho chunking.

```python
# Production document parsing pattern
from pathlib import Path
import fitz  # PyMuPDF

class DocumentParser:
    def parse_pdf(self, path: Path) -> list[dict]:
        doc = fitz.open(str(path))
        chunks = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            chunks.append({
                "text": text,
                "metadata": {
                    "source": path.name,
                    "page": page_num + 1,
                    "total_pages": len(doc),
                }
            })
        return chunks
```

### 2.2 Chunking Strategy

 **Best Practice 2026** : RecursiveCharacterTextSplitter, 400-512 tokens, overlap 10-20%.

| Strategy                      | Accuracy (benchmark)  | Speed       | Cost        | Khi nào dùng                            |
| ----------------------------- | --------------------- | ----------- | ----------- | ----------------------------------------- |
| **Recursive 512-token** | 69%                   | Rất nhanh  | Rất thấp  | **Default — bắt đầu từ đây** |
| Recursive 400-token           | 88-89%                | Nhanh       | Thấp       | Khi cần accuracy cao hơn                |
| Semantic Chunking             | 54-92% (biến thiên) | Chậm 3-5x  | Cao         | Chỉ khi budget cho phép                 |
| Late Chunking                 | ~85%                  | Trung bình | Trung bình | Long docs + Jina v3                       |
| Structure-Aware               | ~80%                  | Nhanh       | Thấp       | Markdown/HTML có heading                 |

 **Benchmark Feb 2026 (Vecta)** : Recursive 512-token đạt 69% trên 50 bài paper. Semantic chunking chỉ đạt 54% vì tạo fragments 43 tokens quá nhỏ.

 **Rule thực tế** : Bắt đầu recursive 512 → đo RAGAS → nếu Context Precision < 0.7 → thử 400 token → nếu vẫn thấp → thử semantic.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,           # Sweet spot: 400-512
    chunk_overlap=50,         # 10% overlap
    separators=["\n\n", "\n", ". ", " ", ""],  # Priority order
    length_function=len,
)
chunks = splitter.split_text(document_text)
```

### 2.3 Embedding Model

 **Best Practice 2026** : BGE-M3 (self-hosted) cho speed + cost, Qwen3-Embedding-8B cho accuracy max.

| Model               | MTEB Score | Latency     | Dimension | Vietnamese  | License     | Deploy    |
| ------------------- | ---------- | ----------- | --------- | ----------- | ----------- | --------- |
| **BGE-M3**    | 63.0       | <30ms       | 1024      | Tốt        | MIT         | Self-host |
| Qwen3-Embedding-8B  | 70.58      | ~50ms       | 4096      | Tốt        | Apache 2.0  | Self-host |
| OpenAI text-3-large | 64.6       | ~40ms (API) | 3072      | Trung bình | Proprietary | API       |
| Jina v3             | ~62        | Chậm nhất | 1024      | Tốt        | Proprietary | API       |
| Cohere embed-v4.0   | 65.2       | Trung bình | 1024      | Tốt        | Proprietary | API       |

 **Recommendation cho production Vietnam** :

* **Budget/Speed first** : BGE-M3 — MIT license, self-host, <30ms, tiếng Việt tốt
* **Accuracy first** : Qwen3-Embedding-8B — MTEB 70.58, Apache 2.0, self-host
* **Không muốn quản lý infra** : OpenAI text-embedding-3-large

```python
# BGE-M3 deployment với FastAPI (production pattern)
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

def encode(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(
        texts,
        batch_size=32,
        max_length=512,
    )["dense_vecs"]
    return embeddings.tolist()
```

### 2.4 Vector Database

 **Best Practice 2026** : Qdrant (self-host) cho majority use cases.

| Database         | P50 Latency   | P99 Latency    | QPS            | Scale    | Chi phí        |
| ---------------- | ------------- | -------------- | -------------- | -------- | --------------- |
| **Qdrant** | **8ms** | **25ms** | **1500** | Millions | $40-500/mo      |
| Milvus           | 12ms          | 35ms           | 1200           | Billions | $100-1000/mo    |
| Weaviate         | 15ms          | 40ms           | 800            | Millions | $50-500/mo      |
| Pinecone         | 20ms          | 50ms           | 500            | Millions | $70-960/mo      |
| Chroma           | ~30ms         | ~80ms          | 300            | <1M      | Free (dev only) |

 **Tại sao Qdrant?** : Rust-based → memory-safe, nhanh nhất. HNSW + scalar quantization. Filtering mạnh. Self-host dễ bằng Docker. Community active.

```yaml
# docker-compose.yml — Qdrant production
services:
  qdrant:
    image: qdrant/qdrant:v1.12.0
    ports:
      - "6333:6333"
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
    deploy:
      resources:
        limits:
          memory: 4G
```

### 2.5 Metadata Enrichment

 **Best Practice** : Thêm metadata = tăng precision khi filter.

```python
# Minimum metadata cho mỗi chunk
metadata = {
    "source": "report_q4_2025.pdf",    # Truy xuất nguồn
    "page": 15,                          # Vị trí cụ thể
    "section": "Financial Summary",      # Heading hierarchy
    "date": "2025-12-01",               # Filter theo thời gian
    "doc_type": "quarterly_report",      # Filter theo loại
    "chunk_index": 42,                   # Thứ tự chunk
    "total_chunks": 400,                 # Context
}
```

 **Nâng cao** : NER extraction (người, tổ chức, địa điểm), auto-generated keywords, summary per chunk.

---

## 3. PHASE 2: ONLINE QUERY PIPELINE

### 3.1 Retrieval Strategy

 **Best Practice 2026** : Hybrid Search (Vector + BM25) → Reranking. Đây là standard.

```
User Query
    ↓
┌───────────────────────────────────┐
│   Query Processing                │
│   • Rewrite query (optional)     │
│   • Expand query (multi-query)   │
│   • Embed query → vector         │
└───────────┬───────────────────────┘
            ↓
    ┌───────┴───────┐
    ↓               ↓
┌────────┐    ┌────────┐
│ Vector │    │  BM25  │     ← Parallel execution
│ Search │    │ Search │
│ top-20 │    │ top-20 │
└───┬────┘    └───┬────┘
    └───────┬─────┘
            ↓
    ┌───────────────┐
    │ Reciprocal    │     ← Fuse results
    │ Rank Fusion   │
    │ (RRF)         │
    └───────┬───────┘
            ↓
    ┌───────────────┐
    │ Reranker      │     ← Cross-encoder scoring
    │ top-20 → top-5│
    └───────┬───────┘
            ↓
    Top 5 contexts → LLM
```

 **Tại sao Hybrid?** : Vector search bắt semantic similarity ("revenue" ≈ "doanh thu"). BM25 bắt exact match ("Q4 2025" phải chính xác). Kết hợp cả hai → robust hơn.

 **Impact thực tế** : Hybrid + Reranking tăng 20-48% retrieval quality so với vector-only.

```python
# Reciprocal Rank Fusion implementation
def reciprocal_rank_fusion(
    results_list: list[list[dict]],
    k: int = 60
) -> list[dict]:
    """Fuse multiple result lists using RRF"""
    scores = {}
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc["id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    sorted_docs = sorted(scores.items(), key=lambda x: -x[1])
    return [{"id": doc_id, "rrf_score": score} for doc_id, score in sorted_docs]
```

### 3.2 Reranking — Mandatory cho Production

 **Best Practice 2026** : Không có reranking = không phải production RAG.

| Reranker                     | Latency                  | Accuracy Gain    | Cost             | Deploy       |
| ---------------------------- | ------------------------ | ---------------- | ---------------- | ------------ |
| **BGE-reranker-v2-m3** | **50-100ms (GPU)** | +15-20% Hit Rate | Free (self-host) | GPU required |
| Cohere Rerank 3.5            | ~600ms (API)             | +15-20% Hit Rate | $0.003/query     | API          |
| ZeroEntropy zerank-1         | 150-315ms                | +28% NDCG@10     | API pricing      | API          |
| ms-marco-MiniLM-L-6-v2       | 80-150ms                 | +10-15%          | Free             | CPU ok       |

 **Recommendation** :

* **Có GPU** : BGE-reranker-v2-m3 — 50-100ms, free, best value
* **Không có GPU** : Cohere Rerank 3.5 — reliable, managed
* **Budget tight** : ms-marco-MiniLM — chạy được trên CPU

 **Impact** : Reranking giảm hallucination 35%, tăng Hit Rate 15-20%.

```python
# Two-stage retrieval pattern (production)
from FlagEmbedding import FlagReranker

reranker = FlagReranker("BAAI/bge-reranker-v2-m3", use_fp16=True)

def retrieve_and_rerank(query: str, top_k_retrieve: int = 20, top_k_final: int = 5):
    # Stage 1: Fast retrieval (bi-encoder)
    candidates = vector_search(query, top_k=top_k_retrieve)  # 15ms

    # Stage 2: Accurate reranking (cross-encoder)
    pairs = [[query, doc["text"]] for doc in candidates]
    scores = reranker.compute_score(pairs)                     # 80ms

    # Sort by reranker score, take top-5
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    return [doc for doc, score in ranked[:top_k_final]]
```

### 3.3 Prompt Engineering cho RAG

 **Best Practice** : Prompt template tách file YAML, không hardcode.

```yaml
# config/prompts.yaml
rag_qa:
  system: |
    Bạn là trợ lý AI trả lời dựa trên tài liệu được cung cấp.
    Quy tắc:
    1. CHỈ trả lời dựa trên context bên dưới
    2. Nếu không tìm thấy câu trả lời → nói "Tôi không tìm thấy thông tin này trong tài liệu"
    3. Trích dẫn nguồn: [Nguồn: tên_file, trang X]
    4. Trả lời ngắn gọn, chính xác

  user: |
    Context:
    {context}

    Câu hỏi: {question}

    Trả lời:

rag_refuse:
  response: |
    Tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn trong tài liệu hiện có.
    Bạn có thể thử:
    1. Diễn đạt lại câu hỏi
    2. Hỏi về chủ đề cụ thể hơn
```

 **POWER Framework cho prompt** :

* **P**urpose: Mục đích rõ ràng
* **O**utput format: Định dạng trả lời
* **W**hat data: Context nào được dùng
* **E**xecution rules: Quy tắc (refuse khi không biết, cite sources)
* **R**esult criteria: Tiêu chí đánh giá

### 3.4 LLM Serving

 **Best Practice 2026** : vLLM cho production, Ollama cho dev local.

| Framework      | TTFT (1 user)     | TTFT (128 users) | Throughput  | GPU Memory                | Use case             |
| -------------- | ----------------- | ---------------- | ----------- | ------------------------- | -------------------- |
| **vLLM** | **10-80ms** | **<100ms** | Cao nhất   | Tối ưu (PagedAttention) | **Production** |
| Ollama         | 65-200ms          | 673ms+           | Thấp       | Cơ bản                  | Dev/local            |
| SGLang         | ~50ms             | ~120ms           | Cao         | Tốt                      | Structured output    |
| TGI            | ~100ms            | ~200ms           | Trung bình | Trung bình               | Deprecated (2025+)   |

 **vLLM thắng vì** : PagedAttention (quản lý KV-cache như virtual memory) → handle concurrent users tốt hơn 6x so với Ollama.

```yaml
# docker-compose.yml — vLLM production
services:
  vllm:
    image: vllm/vllm-openai:latest
    command: >
      --model Qwen/Qwen2.5-7B-Instruct
      --max-model-len 4096
      --gpu-memory-utilization 0.85
      --dtype auto
      --port 8000
    ports:
      - "8001:8000"
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

### 3.5 Caching Strategy

 **Best Practice** : 3 tầng caching = giảm 60-75% cost.

```
Layer 1: Query Cache (Redis)
    → Cache exact query → result
    → TTL: 5 phút
    → Hit rate: 30-40% (popular queries)

Layer 2: Semantic Cache
    → Cache similar queries (cosine > 0.95)
    → TTL: 15 phút
    → Hit rate: 20-30% (paraphrased queries)

Layer 3: Embedding Cache (Redis)
    → Cache query → embedding vector
    → TTL: 1 giờ
    → Hit rate: 50-60% (repeated terms)

Combined: 60-75% requests không cần full pipeline
```

```python
# 3-layer caching pattern
import hashlib
import redis

cache = redis.Redis(host="redis", port=6379)

async def cached_rag_query(query: str):
    # Layer 1: Exact match
    query_hash = hashlib.md5(query.encode()).hexdigest()
    cached = cache.get(f"rag:exact:{query_hash}")
    if cached:
        return json.loads(cached)  # ~5ms

    # Layer 2: Semantic match
    query_embedding = embed(query)
    similar = find_similar_cached_query(query_embedding, threshold=0.95)
    if similar:
        return similar  # ~15ms

    # Layer 3: Embedding cache
    cached_embedding = cache.get(f"rag:embed:{query_hash}")
    if cached_embedding:
        query_embedding = json.loads(cached_embedding)
    else:
        query_embedding = embed(query)
        cache.setex(f"rag:embed:{query_hash}", 3600, json.dumps(query_embedding))

    # Full pipeline (cache miss)
    result = full_rag_pipeline(query, query_embedding)

    # Cache result
    cache.setex(f"rag:exact:{query_hash}", 300, json.dumps(result))
    return result
```

---

## 4. PHASE 3: EVALUATION LOOP CONTINUOUS

### 4.1 RAGAS Metrics — Production Targets

| Metric                      | Đo gì                                   | Target | Minimum | Cách tính                                                          |
| --------------------------- | ----------------------------------------- | ------ | ------- | -------------------------------------------------------------------- |
| **Faithfulness**      | Response có đúng với context?         | >0.8   | >0.7    | LLM check: mỗi claim trong answer có evidence trong context không |
| **Answer Relevancy**  | Response có trả lời đúng câu hỏi?  | >0.8   | >0.7    | LLM generate questions từ answer, so sánh cosine với query gốc   |
| **Context Precision** | Top-K chunks có relevant không?         | >0.7   | >0.5    | % chunks relevant trong top-K (ranking matters)                      |
| **Context Recall**    | Có thiếu thông tin quan trọng không? | >0.7   | >0.5    | % ground-truth info covered bởi retrieved chunks                    |

 **Domain-specific** : Medical/Legal cần Faithfulness > 0.9 (sai = nguy hiểm).

```python
# RAGAS evaluation script
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluation dataset (minimum 20 samples)
eval_data = {
    "question": ["Revenue Q4 là bao nhiêu?", ...],
    "answer": ["Revenue Q4 đạt 5.2 tỷ", ...],
    "contexts": [["Chunk 1...", "Chunk 2..."], ...],
    "ground_truth": ["Revenue Q4 đạt 5.2 tỷ USD", ...],
}

result = evaluate(
    dataset=eval_data,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(result)
# {'faithfulness': 0.85, 'answer_relevancy': 0.82, 'context_precision': 0.78}
```

### 4.2 Observability — Langfuse (Self-host, MIT License)

 **Tại sao Langfuse?** : Open-source, self-host được, MIT license, tích hợp LlamaIndex/LangChain native.

```yaml
# docker-compose.yml — Langfuse self-host
services:
  langfuse:
    image: langfuse/langfuse:2
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://langfuse:password@postgres:5432/langfuse
      - NEXTAUTH_SECRET=your-secret-key
      - SALT=your-salt
    depends_on:
      - postgres
```

 **Trace structure cho RAG** :

```
Trace: "user-query-abc123"
├── Span: "query_processing" (5ms)
│   └── metadata: {original_query, rewritten_query}
├── Span: "retrieval" (30ms)
│   ├── Span: "vector_search" (15ms)
│   └── Span: "bm25_search" (10ms)
├── Span: "reranking" (80ms)
│   └── metadata: {input_docs: 20, output_docs: 5}
├── Generation: "llm_call" (200ms)
│   └── metadata: {model, tokens_in, tokens_out, cost}
└── Score: {faithfulness: 0.9, relevancy: 0.85}
```

### 4.3 A/B Testing RAG Configs

 **Best Practice** : Test 1 biến tại 1 thời điểm.

| Biến cần test | Config A    | Config B      | Metric đo        |
| --------------- | ----------- | ------------- | ----------------- |
| Chunk size      | 512 tokens  | 400 tokens    | Context Precision |
| Top-K retrieval | 10          | 20            | Context Recall    |
| Reranker        | Cohere 3.5  | BGE-v2-m3     | Faithfulness      |
| Embedding       | BGE-M3      | Qwen3-8B      | Answer Relevancy  |
| Prompt template | v1 (simple) | v2 (detailed) | Faithfulness      |

```python
# A/B test pattern
import random

def rag_query_with_ab_test(query: str, user_id: str):
    # Deterministic assignment based on user_id
    variant = "A" if hash(user_id) % 2 == 0 else "B"

    if variant == "A":
        config = {"chunk_size": 512, "reranker": "cohere", "top_k": 10}
    else:
        config = {"chunk_size": 400, "reranker": "bge", "top_k": 10}

    result = rag_pipeline(query, config)

    # Log to Langfuse with variant tag
    langfuse.trace(name=f"ab-test-{variant}", metadata=config, output=result)
    return result
```

### 4.4 Continuous Improvement Loop

```
1. MONITOR (daily)
   → Pull RAGAS scores from Langfuse
   → Alert nếu Faithfulness drop > 5%

2. CAPTURE FAILURES (weekly)
   → Filter traces có Faithfulness < 0.5
   → Phân loại: retrieval fail? generation hallucinate? context thiếu?

3. CURATE DATASET (weekly)
   → Thêm failure cases vào eval dataset
   → Verify ground truth bằng human review
   → Target: 50-100 eval pairs (growing over time)

4. OPTIMIZE (bi-weekly)
   → Test fix: thêm docs? đổi chunking? thêm metadata filter?
   → Run RAGAS trên eval dataset
   → So sánh trước/sau

5. A/B TEST (bi-weekly)
   → Deploy fix cho 10% traffic
   → Monitor 3-5 ngày
   → Nếu tốt hơn → rollout 100%

6. DEPLOY & REPEAT
```

---

## 5. PRODUCTION BENCHMARKS & METRICS

### 5.1 Latency Benchmarks Thực Tế (2026)

```
┌──────────────────────────────────────────────────────────────┐
│ Component            │ Tool           │ P50    │ P99        │
├──────────────────────┼────────────────┼────────┼────────────┤
│ Embedding            │ BGE-M3         │ <30ms  │ ~50ms      │
│ Embedding            │ Jina v3 (API)  │ ~60ms  │ ~120ms     │
│ Embedding            │ OpenAI (API)   │ ~40ms  │ ~100ms     │
├──────────────────────┼────────────────┼────────┼────────────┤
│ Vector Search        │ Qdrant         │ 8ms    │ 25ms       │
│ Vector Search        │ Milvus         │ 12ms   │ 35ms       │
│ Vector Search        │ Pinecone       │ 20ms   │ 50ms       │
├──────────────────────┼────────────────┼────────┼────────────┤
│ Reranking            │ BGE-v2-m3 GPU  │ ~80ms  │ ~120ms     │
│ Reranking            │ Cohere 3.5 API │ ~600ms │ ~800ms     │
│ Reranking            │ MiniLM (CPU)   │ ~100ms │ ~200ms     │
├──────────────────────┼────────────────┼────────┼────────────┤
│ LLM TTFT             │ vLLM (1 user)  │ ~50ms  │ ~100ms     │
│ LLM TTFT             │ vLLM (128 usr) │ ~80ms  │ <100ms     │
│ LLM TTFT             │ Ollama (1 usr) │ ~200ms │ ~400ms     │
│ LLM TTFT             │ Ollama (128)   │ ~673ms │ ~1000ms+   │
└──────────────────────┴────────────────┴────────┴────────────┘
```

### 5.2 Accuracy Benchmarks

```
Production-Ready RAGAS Scores:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Faithfulness:       ≥ 0.80 (Medical/Legal: ≥ 0.90)
Answer Relevancy:   ≥ 0.80
Context Precision:  ≥ 0.70
Context Recall:     ≥ 0.70

Impact của từng optimization:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
+ Hybrid Search:     +10-15% Context Recall
+ Reranking:         +15-20% Hit Rate, -35% Hallucination
+ Metadata Filtering: +5-10% Context Precision
+ Prompt Engineering: +10-15% Faithfulness
+ Query Rewriting:    +5-10% Answer Relevancy
```

---

## 6. RECOMMENDED TECH STACK 2026

### Production Stack — Recommend #1

```
┌──────────────────────────────────────────────────────────────┐
│                  Langfuse (Tracing & Eval)                   │
│                  Self-host, MIT License                      │
├──────────────────────────────────────────────────────────────┤
│                  FastAPI (API Layer)                         │
│                  + Pydantic v2 + Structured Logging          │
├──────────┬──────────────┬────────────────────────────────────┤
│  Phase 1 │   Phase 2    │    Phase 2 (continued)             │
│          │              │                                    │
│ BGE-M3   │ Qdrant       │  vLLM + Qwen 2.5-7B                │
│ Embedding│ Vector DB    │  LLM Backend                       │
│ <30ms    │ 8ms P50      │  50ms TTFT                         │
├──────────┤              ├────────────────────────────────────┤
│ Recursive│ BGE-reranker │  RAGAS                             │
│ 512-token│ v2-m3 (GPU)  │  Evaluation                        │
│ Chunking │ 80ms         │  Metrics                           │
├──────────┼──────────────┼────────────────────────────────────┤
│          │   Redis      │                                    │
│          │   3-layer    │  Prometheus + Grafana              │
│          │   Caching    │  Monitoring                        │
└──────────┴──────────────┴────────────────────────────────────┘
```

### Quick Reference Card

| Component             | Choice                 | Lý do                               |
| --------------------- | ---------------------- | ------------------------------------ |
| **Embedding**   | BGE-M3 (self-host)     | <30ms, MIT, Vietnamese tốt, MTEB 63 |
| **Vector DB**   | Qdrant                 | 8ms P50, Rust, HNSW, Docker easy     |
| **Reranker**    | BGE-reranker-v2-m3     | 80ms GPU, free, +20% accuracy        |
| **LLM Serving** | vLLM                   | 50ms TTFT, PagedAttention, 6x Ollama |
| **LLM Model**   | Qwen 2.5-7B-Instruct   | Balance quality/speed, Vietnamese ok |
| **Chunking**    | Recursive 512-token    | 69% accuracy, fast, proven           |
| **Tracing**     | Langfuse               | Open-source, self-host, MIT          |
| **Eval**        | RAGAS                  | Standard, reference-free             |
| **Cache**       | Redis                  | 3-layer caching, mature              |
| **Search**      | Hybrid (Vector + BM25) | +20% recall vs vector-only           |
| **API**         | FastAPI                | Async, Pydantic, auto-docs           |

---

## 7. FOLDER STRUCTURE BEST PRACTICES

### 7.1 Hai trường phái — Chọn cái nào?

**Trường phái A: Module-by-RAG-Phase (RAG-Centric)**

Tổ chức theo 3 pha của RAG pipeline. Mỗi pha là 1 module.

**Trường phái B: Clean DDD Architecture (Domain-Centric)**

Tổ chức theo Domain-Driven Design với 4 layers: Presentation → Application → Domain → Infrastructure.

### 7.2 So Sánh Chi Tiết

| Tiêu chí               | Module-by-Phase (A)                       | Clean DDD (B)                             |
| ------------------------ | ----------------------------------------- | ----------------------------------------- |
| **Dễ hiểu**      | Rất dễ — nhìn folder = hiểu pipeline | Khó ban đầu — cần hiểu DDD concepts |
| **Learning curve** | 30 phút                                  | 1-2 tuần                                 |
| **Team size**      | 1-5 người                               | 5-50+ người                             |
| **Phù hợp cho**  | RAG-focused product                       | Multi-domain platform                     |
| **Thay đổi DB**  | Phải sửa nhiều chỗ                    | Chỉ sửa infrastructure layer            |
| **Test**           | Integration test chủ yếu                | Unit test domain dễ dàng                |
| **Scale code**     | Tốt đến ~20K LOC                       | Tốt đến 200K+ LOC                      |
| **RAG-specific**   | Tối ưu cho RAG                          | Generic, áp dụng mọi project           |

### 7.3 RECOMMENDATION: Khi Nào Dùng Cái Nào?

```
Bạn đang build:
├── RAG service đơn lẻ (1 domain, 1 pipeline)?
│   → Module-by-Phase (A) ✓
│
├── RAG là 1 phần của platform lớn hơn?
│   (có users, orders, payments, + RAG)
│   → Clean DDD (B) ✓
│
├── Team < 5 người, MVP/startup?
│   → Module-by-Phase (A) ✓
│
├── Team > 10 người, enterprise?
│   → Clean DDD (B) ✓
│
└── Fresher đang học?
    → Module-by-Phase (A) trước → DDD sau ✓
```

### 7.4 Option A: Module-by-RAG-Phase (RECOMMENDED cho RAG Project)

```bash
my-rag-system/
├── README.md
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .dockerignore
├── .gitignore
│
├── config/                           # ═══ CONFIGURATION ═══
│   ├── settings.yaml                 # Env config: models, thresholds, URLs
│   ├── prompts.yaml                  # All prompt templates (YAML/Jinja2)
│   └── logging.yaml                  # Structured logging config
│
├── src/                              # ═══ APPLICATION SOURCE ═══
│   ├── __init__.py
│   ├── main.py                       # FastAPI app + lifespan events
│   │
│   ├── ingestion/                    # ═══ PHASE 1: OFFLINE ═══
│   │   ├── __init__.py
│   │   ├── document_loader.py        # Load PDF/HTML/DOCX → clean text
│   │   ├── splitter.py               # Chunking strategies
│   │   ├── embedder.py               # Embedding model wrapper
│   │   ├── indexer.py                # Embed & store into vector DB
│   │   └── metadata.py              # Metadata extraction & enrichment
│   │
│   ├── retrieval/                    # ═══ PHASE 2: ONLINE ═══
│   │   ├── __init__.py
│   │   ├── retriever.py              # Hybrid search (vector + BM25)
│   │   ├── reranker.py               # Cross-encoder reranking
│   │   └── query_processor.py        # Query rewriting, expansion
│   │
│   ├── generation/                   # ═══ PHASE 2: GENERATION ═══
│   │   ├── __init__.py
│   │   ├── llm_client.py             # LLM API calls (vLLM/OpenAI)
│   │   ├── response_builder.py       # Prompt template + format output
│   │   └── guardrails.py            # Output validation, refuse logic
│   │
│   ├── evaluation/                   # ═══ PHASE 3: EVAL LOOP ═══
│   │   ├── __init__.py
│   │   ├── ragas_evaluator.py        # RAGAS metrics runner
│   │   ├── tracing.py                # Langfuse integration
│   │   └── ab_test.py               # A/B test config routing
│   │
│   ├── api/                          # ═══ API ENDPOINTS ═══
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── query.py              # POST /query, POST /query-stream
│   │   │   ├── ingest.py             # POST /ingest
│   │   │   └── health.py             # GET /health, GET /metrics
│   │   └── schemas/
│   │       └── models.py             # Pydantic request/response
│   │
│   └── core/                         # ═══ SHARED UTILITIES ═══
│       ├── __init__.py
│       ├── config.py                 # Pydantic BaseSettings
│       ├── clients.py                # DB clients, LLM client init
│       ├── logger.py                 # Structured JSON logging
│       ├── cache.py                  # Redis 3-layer caching
│       └── errors.py                 # Custom exceptions
│
├── tests/                            # ═══ TESTS ═══
│   ├── __init__.py
│   ├── conftest.py                   # Shared fixtures
│   ├── test_ingestion/
│   │   ├── test_splitter.py          # Chunking unit tests
│   │   └── test_embedder.py
│   ├── test_retrieval/
│   │   ├── test_retriever.py         # Retrieval accuracy tests
│   │   └── test_reranker.py
│   ├── test_generation/
│   │   └── test_response_builder.py
│   └── test_e2e.py                   # End-to-end: query → response
│
├── eval/                             # ═══ EVALUATION DATA ═══
│   ├── dataset.json                  # 50-100 eval pairs
│   ├── results/                      # Historical eval results
│   └── run_eval.py                   # RAGAS evaluation script
│
├── notebooks/                        # ═══ EXPERIMENTS ═══
│   ├── 01_chunking_comparison.ipynb
│   ├── 02_embedding_benchmark.ipynb
│   └── 03_eval_analysis.ipynb
│
├── scripts/                          # ═══ UTILITY SCRIPTS ═══
│   ├── build_index.py                # CLI: python scripts/build_index.py
│   ├── evaluate.py                   # CLI: python scripts/evaluate.py
│   ├── warm_cache.py                 # Pre-warm Redis cache
│   └── deploy.sh                     # Deployment script
│
├── data/                             # ═══ DATA (gitignored) ═══
│   ├── raw/                          # Original documents
│   └── processed/                    # Cleaned text (optional)
│
└── .github/
    └── workflows/
        ├── test.yml                  # PR: lint + test
        ├── build.yml                 # Build Docker image
        └── eval.yml                  # Weekly RAGAS evaluation
```

 **Triết lý** : Nhìn folder structure = hiểu RAG pipeline. `ingestion/` = Phase 1, `retrieval/` + `generation/` = Phase 2, `evaluation/` = Phase 3. Ai cũng đọc được, onboard nhanh.

### 7.5 Option B: Clean DDD Architecture (cho Platform lớn)

```bash
my-platform/
├── app/
│   ├── main.py
│   │
│   ├── api/                          # PRESENTATION LAYER
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── query.py          # RAG endpoints
│   │   │   │   ├── users.py          # User management
│   │   │   │   └── health.py
│   │   │   └── schemas/
│   │   └── middleware/
│   │
│   ├── domains/                      # DOMAIN LAYER (DDD Bounded Contexts)
│   │   ├── rag/                      # ═══ RAG BOUNDED CONTEXT ═══
│   │   │   ├── domain/
│   │   │   │   ├── entities.py       # Document, Chunk, Query (pure logic)
│   │   │   │   ├── value_objects.py  # ChunkSize, EmbeddingVector
│   │   │   │   └── events.py        # DocumentIngested, QueryProcessed
│   │   │   │
│   │   │   ├── application/
│   │   │   │   ├── services/
│   │   │   │   │   ├── ingestion_service.py
│   │   │   │   │   ├── retrieval_service.py
│   │   │   │   │   └── generation_service.py
│   │   │   │   └── repositories/
│   │   │   │       ├── document_repository.py   # Abstract interface
│   │   │   │       └── vector_repository.py     # Abstract interface
│   │   │   │
│   │   │   └── infrastructure/
│   │   │       ├── qdrant_repository.py         # Concrete: Qdrant
│   │   │       ├── embedding_adapter.py         # Concrete: BGE-M3
│   │   │       ├── llm_adapter.py               # Concrete: vLLM
│   │   │       └── models.py                    # ORM models
│   │   │
│   │   ├── users/                    # ═══ USER BOUNDED CONTEXT ═══
│   │   │   ├── domain/
│   │   │   ├── application/
│   │   │   └── infrastructure/
│   │   │
│   │   └── shared/                   # Shared domain logic
│   │
│   ├── infrastructure/               # INFRASTRUCTURE LAYER
│   │   ├── db/
│   │   ├── cache/
│   │   ├── messaging/
│   │   └── external/
│   │
│   └── core/                         # CROSS-CUTTING
│       ├── config.py
│       ├── security.py
│       └── logging.py
│
├── tests/
├── infrastructure/                   # IaC (Terraform, Helm)
├── docker/
└── docs/
```

 **Khi nào cần DDD** : Khi RAG chỉ là 1 feature trong platform lớn hơn (có user management, billing, analytics...). Team > 10 người, mỗi team own 1 bounded context.

### 7.6 Migration Path: A → B

```
Bước 1 (Month 1-3):  Bắt đầu với Option A (Module-by-Phase)
                      Focus: ship RAG MVP nhanh
                      Team: 1-3 người

Bước 2 (Month 3-6):  Thêm features (users, analytics)
                      Option A bắt đầu chật
                      Chuẩn bị refactor

Bước 3 (Month 6+):   Migrate sang Option B (Clean DDD)
                      RAG trở thành 1 bounded context
                      Mỗi domain tự chủ
                      Team: 5-15 người
```

---

## 8. ADVANCED RAG ARCHITECTURES

### 8.1 Landscape 2026

```
                    ┌──────────────────┐
                    │   Vanilla RAG    │  ← Bắt đầu từ đây
                    │ (Vector + BM25)  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
    ┌─────────────┐  ┌────────────┐  ┌────────────┐
    │  GraphRAG   │  │ Agentic RAG│  │  Self-RAG  │
    │ (Microsoft) │  │(LLM agent) │  │(self-check)│
    └──────┬──────┘  └─────┬──────┘  └─────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           ↓
                ┌──────────────────┐
                │  Adaptive RAG    │  ← Tương lai
                │ (chọn strategy   │
                │  dựa trên query) │
                └──────────────────┘
```

| Architecture             | Khi nào dùng                              | Accuracy gain | Latency cost | Complexity  |
| ------------------------ | ------------------------------------------- | ------------- | ------------ | ----------- |
| **Vanilla RAG**    | Mọi project, bắt đầu từ đây          | Baseline      | Baseline     | Thấp       |
| **GraphRAG**       | Multi-hop reasoning, data có relationships | +15-25%       | +2-3x        | Cao         |
| **Agentic RAG**    | Complex queries, tool use needed            | +20-30%       | +3-5x        | Rất cao    |
| **Self-RAG**       | High-stakes (medical, legal)                | +10-15%       | +1.5-2x      | Trung bình |
| **Corrective RAG** | Noisy retrieval, unreliable docs            | +10-15%       | +1.2x        | Trung bình |
| **LightRAG**       | Fast + graph, balanced                      | +15-20%       | +1.3x        | Trung bình |

 **Recommendation cho Fresher** : Master Vanilla RAG trước (Week 2). Advanced RAG là Month 2-3.

---

## 9. COST ANALYSIS & OPTIMIZATION

### 9.1 Cost Per Query Breakdown

```
1 query "What is the return policy?" trên 100K-doc corpus:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Component           │ Unoptimized    │ Optimized       │ Savings
────────────────────┼────────────────┼─────────────────┼────────
Embedding (API)     │ $0.0002        │ $0.00 (cached)  │ 100%
Vector Search       │ $0.0001        │ $0.0001         │ 0%
Reranking (API)     │ $0.003         │ $0.001 (cached) │ 67%
LLM Generation      │ $0.01          │ $0.003 (cache)  │ 70%
Infrastructure      │ $0.001         │ $0.001          │ 0%
────────────────────┼────────────────┼─────────────────┼────────
Total per query     │ $0.014         │ $0.004          │ 71%
```

### 9.2 Monthly Cost cho 100K Queries

| Setup                                   | Monthly Cost     | Notes                                      |
| --------------------------------------- | ---------------- | ------------------------------------------ |
| **Self-hosted (open-source all)** | $40-200/mo       | BGE-M3 + Qdrant + vLLM + bare metal/VPS    |
| **Hybrid (self-host + API)**      | $500-1,500/mo    | Self-host embed+vector, API for LLM+rerank |
| **Full API**                      | $1,500-5,000/mo  | OpenAI embed + Pinecone + Cohere + GPT-4   |
| **Enterprise (managed)**          | $5,000-20,000/mo | Managed services, SLAs, support            |

### 9.3 Cost Optimization Strategies

```
Strategy                    │ Savings │ Implementation
────────────────────────────┼─────────┼──────────────────────
1. Self-host embeddings     │ 50-70%  │ BGE-M3 trên GPU $40/mo
2. 3-layer Redis caching    │ 60-75%  │ Redis $5-10/mo
3. Self-host vector DB      │ 40-60%  │ Qdrant Docker
4. Prompt caching           │ 40-50%  │ Provider feature
5. Reduce top-K retrieval   │ 10-20%  │ Config change, free
6. Use smaller LLM          │ 50-80%  │ Qwen 2.5-7B vs GPT-4
────────────────────────────┼─────────┼──────────────────────
Combined                    │ 70-90%  │ 1-2 weeks setup
```

---

## 10. REFERENCES

### Frameworks

* LlamaIndex: https://docs.llamaindex.ai/
* LangChain: https://python.langchain.com/
* Haystack: https://haystack.deepset.ai/
* RAGAS: https://docs.ragas.io/
* Langfuse: https://langfuse.com/docs
* LightRAG: https://github.com/HKUDS/LightRAG

### Models & Tools

* BGE-M3: https://huggingface.co/BAAI/bge-m3
* BGE-reranker-v2-m3: https://huggingface.co/BAAI/bge-reranker-v2-m3
* Qwen3-Embedding: https://huggingface.co/Qwen/Qwen3-Embedding-8B
* vLLM: https://docs.vllm.ai/
* Qdrant: https://qdrant.tech/documentation/

### Benchmarks & Research

* MTEB Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
* Vecta Chunking Benchmark (Feb 2026)
* Qdrant Benchmarks: https://qdrant.tech/benchmarks/
* RAGAS Paper: https://arxiv.org/abs/2309.15217
* GraphRAG: https://arxiv.org/abs/2404.16130

### Vietnamese Resources

* RAG Techniques: https://github.com/NirDiamant/RAG_Techniques
* Viblo RAG Series: https://viblo.asia/p/chatgpt-series-5-tim-hieu-ve-retrieval-augmented-generation-rag-Ny0VGRd7LPA

---

> **Tài liệu này là living document** — cập nhật khi có benchmark mới, tool mới, hoặc best practice thay đổi.
>
> Phiên bản tiếp theo dự kiến: April 2026 (thêm Agentic RAG hands-on, MCP integration)
>



---

# PHẦN B: RAG - GRAPH RAG

**Tác giả:** Manus AI

**Ngày:** 12 tháng 3 năm 2026

## Tóm Tắt

Retrieval-Augmented Generation (RAG) đã cơ bản thay đổi bối cảnh của các Mô Hình Ngôn Ngữ Lớn (LLMs), giải quyết những hạn chế vốn có của chúng về tính kịp thời của kiến thức và độ chính xác thực tế. Bằng cách tích hợp các nguồn kiến thức bên ngoài, động, các hệ thống RAG cung cấp một cơ chế mạnh mẽ để neo các đầu ra LLM vào thông tin có thể xác minh, giảm thiểu các vấn đề như "ảo giác" [1]. Tài liệu này cung cấp một cuộc khảo sát toàn diện về mô hình RAG, truy vết sự tiến hóa của nó từ các khái niệm cơ bản đến các kiến trúc dựa trên đồ thị tinh vi đại diện cho những tiến bộ hàng đầu của lĩnh vực. Chúng tôi sẽ phân tích sự tiến triển từ "Naive RAG" đến "Advanced RAG" và các framework "Modular RAG" có khả năng thích ứng cao [2] [3]. Lõi của tài liệu này là một cuộc điều tra chi tiết về Graph RAG, bao gồm phân tích kỹ thuật các framework nổi bật và một cuộc khảo sát sâu về HippoRAG lấy cảm hứng từ sinh học thần kinh và người kế thừa của nó, HippoRAG 2 [9] [10]. Thông qua một đánh giá toàn diện các bài báo nghiên cứu chính, kết quả điểm chuẩn và chi tiết triển khai thực tế, tài liệu này nhằm phục vụ như một hướng dẫn xác định cho các kỹ sư AI, từ những người mới bắt đầu đến các chuyên gia dày dạn kinh nghiệm, để hiểu sâu sắc và kỹ thuật về cách xây dựng, đánh giá và triển khai các hệ thống RAG và Graph RAG tiên tiến nhất.

## 1. Sự Ra Đời của Retrieval-Augmented Generation

Các Mô Hình Ngôn Ngữ Lớn đã thể hiện những khả năng phi thường trong việc hiểu và tạo ra văn bản giống con người, cung cấp năng lượng cho một thế hệ ứng dụng AI mới. Tuy nhiên, kiến thức của chúng vốn là tĩnh, bị giới hạn trong các tập dữ liệu rộng lớn nhưng hữu hạn mà chúng được huấn luyện trên [1]. Sự hạn chế này dẫn đến hai thách thức quan trọng: vấn đề **knowledge cutoff** (ngưỡng kiến thức), nơi các mô hình không biết về các sự kiện hoặc thông tin xuất hiện sau ngày đào tạo của chúng, và xu hướng **hallucination** (ảo giác), nơi chúng tạo ra thông tin có vẻ hợp lý nhưng không chính xác về mặt thực tế hoặc vô nghĩa [1].

Retrieval-Augmented Generation (RAG) được giới thiệu như một giải pháp thanh lịch và mạnh mẽ cho những thách thức này. Lần đầu tiên được đề xuất bởi Lewis et al. trong bài báo năm 2020 của họ, RAG tăng cường khả năng của LLMs bằng cách động truy xuất thông tin liên quan từ các cơ sở kiến thức bên ngoài tại thời gian suy luận và cung cấp thông tin này làm bối cảnh cho mô hình trong quá trình tạo [1]. Ý tưởng đơn giản nhưng sâu sắc này cho phép LLMs truy cập thông tin cập nhật và neo các phản hồi của chúng vào các sự kiện có thể xác minh, cải thiện đáng kể độ chính xác và độ tin cậy của chúng.

Tài liệu này sẽ điều hướng toàn bộ hệ sinh thái RAG, bắt đầu với các nguyên tắc cơ bản của nó và tiến bộ thông qua các đổi mới tăng dần dẫn đến các hệ thống phức tạp và mạnh mẽ đang được sử dụng ngày nay [3]. Chúng tôi sẽ tuân theo một đường dẫn có cấu trúc tương tự như sự tiến hóa của các hệ thống bộ nhớ, từ việc nhớ lại đơn giản đến suy luận liên kết phức tạp.

### 1.1. Sự Tiến Hóa của RAG: Một Khung Công Việc Ba Mô Hình

Sự phát triển của RAG có thể được hiểu thông qua ba mô hình riêng biệt nhưng liên kết với nhau, mỗi mô hình xây dựng dựa trên mô hình trước để tạo ra các hệ thống chính xác hơn, hiệu quả hơn và linh hoạt hơn [3].

#### 1.1.1. Naive RAG: Bản Thiết Kế Nền Tảng

Naive RAG, triển khai sớm nhất và đơn giản nhất, thiết lập quy trình "Retrieve-Read" cốt lõi làm nền tảng cho tất cả các hệ thống RAG [3]. Quá trình này thường được chia thành ba giai đoạn cơ bản:

1.  **Lập Chỉ Mục (Indexing)**: Giai đoạn ngoại tuyến này chuẩn bị cơ sở kiến thức để truy xuất. Một kho tài liệu (ví dụ: tệp văn bản, PDF, trang web) được tải và phân tích cú pháp thành các phân đoạn nhỏ hơn, dễ quản lý hơn hoặc "chunks" [3]. Một mô hình nhúng sau đó được sử dụng để chuyển đổi mỗi chunk thành một biểu diễn vectơ số, nắm bắt ý nghĩa ngữ nghĩa của nó. Các vectơ này sau đó được lưu trữ trong một cơ sở dữ liệu vectơ chuyên dụng, lập chỉ mục chúng để tìm kiếm độ tương tự hiệu quả.

2.  **Truy Xuất (Retrieval)**: Tại thời gian suy luận, truy vấn của người dùng cũng được chuyển đổi thành vectơ bằng cách sử dụng cùng một mô hình nhúng. Hệ thống sau đó truy vấn cơ sở dữ liệu vectơ để tìm các chunk được lập chỉ mục có vectơ tương tự nhất (ví dụ: theo độ tương tự cosine hoặc tích vô hướng) với vectơ truy vấn [3]. Các chunk liên quan nhất hàng đầu k được truy xuất từ cơ sở dữ liệu.

3.  **Tạo (Generation)**: Các chunk văn bản được truy xuất được nối với truy vấn người dùng ban đầu, thường sử dụng một mẫu lời nhắc cụ thể. Văn bản kết hợp này sau đó được chuyển đến LLM, sử dụng bối cảnh được cung cấp để tạo ra một phản hồi có cơ sở thực tế và liên quan.

Mặc dù tính đơn giản của nó giúp dễ dàng triển khai, Naive RAG dễ bị một số vấn đề, chủ yếu xuất phát từ giai đoạn truy xuất. Những thách thức như độ chính xác thấp (truy xuất các chunk không liên quan) và độ nhớ lại thấp (không truy xuất tất cả các chunk liên quan) có thể làm lạc hướng giai đoạn tạo, dẫn đến các câu trả lời không tối ưu hoặc thậm chí ảo giác [3].

#### 1.1.2. Advanced RAG: Thêm Một Lớp Tinh Tế

Để vượt qua những hạn chế của phương pháp Naive RAG, cộng đồng đã phát triển các kỹ thuật Advanced RAG [3]. Mô hình này giới thiệu các lớp tối ưu hóa trước và sau bước truy xuất cốt lõi, nhằm cải thiện chất lượng, mức độ liên quan và hiệu quả của toàn bộ đường ống [3].

**Tối Ưu Hóa Trước Truy Xuất**

Những kỹ thuật này tập trung vào việc tinh chỉnh dữ liệu trước khi nó được truy xuất và tối ưu hóa chính truy vấn để hiệu quả hơn.

*   **Chiến Lược Chunking và Lập Chỉ Mục**: Cách các tài liệu được chia thành các phần có tác động đáng kể đến chất lượng truy xuất. Thay vì các chunk có kích thước cố định, các kỹ thuật nâng cao sử dụng chunking nhận thức nội dung (ví dụ: chia theo câu, đoạn văn hoặc các phần logic) [4]. Hơn nữa, thay vì một chỉ mục vectơ duy nhất, có thể sử dụng nhiều chiến lược lập chỉ mục. Ví dụ, có thể tạo một chỉ mục phân cấp trong đó các bản tóm tắt của các phần lớn hơn trỏ đến các chunk nhỏ hơn, chi tiết hơn, cho phép một quá trình truy xuất từ thô đến tinh.

*   **Biến Đổi Truy Vấn**: Các truy vấn của người dùng thường không rõ ràng hoặc thiếu đủ bối cảnh để truy xuất hiệu quả. Các kỹ thuật biến đổi truy vấn viết lại hoặc mở rộng truy vấn của người dùng để cải thiện độ chính xác của nó [3]. Điều này có thể liên quan đến việc sử dụng LLM để diễn đạt lại truy vấn, mở rộng nó với các từ đồng nghĩa hoặc các thuật ngữ liên quan, hoặc thậm chí phân tách một truy vấn phức tạp thành nhiều truy vấn con được thực hiện độc lập.

**Tối Ưu Hóa Sau Truy Xuất**

Sau khi một tập hợp các chunk ứng viên được truy xuất, những kỹ thuật này được áp dụng để tinh chỉnh và xử lý lại chúng trước khi chúng được gửi đến LLM tạo.

*   **Xếp Hạng Lại (Re-ranking)**: Truy xuất ban đầu từ cơ sở dữ liệu vectơ dựa trên độ tương tự ngữ nghĩa, nhưng điều này không phải lúc nào cũng tương đương với mức độ liên quan cho truy vấn cụ thể [3]. Một bước xếp hạng lại giới thiệu một mô hình tinh vi hơn (thường là một LLM nhỏ hơn, chuyên biệt hoặc một cross-encoder) để đánh giá lại các chunk được truy xuất hàng đầu k. Công cụ xếp hạng lại này có thể xem xét nội dung truy vấn và chunk sâu hơn, sắp xếp lại các chunk để đặt những chunk liên quan nhất ở trên cùng.

*   **Nén Bối Cảnh (Context Compression)**: Để vừa thêm thông tin liên quan vào cửa sổ bối cảnh hạn chế của LLM và giảm tiếng ồn, các kỹ thuật nén bối cảnh được sử dụng. Điều này liên quan đến việc xác định và loại bỏ các câu không liên quan hoặc dư thừa từ các chunk được truy xuất. Một LLM có thể được nhắc để thực hiện tóm tắt này, trích xuất chỉ những sự kiện nổi bật nhất từ mỗi chunk liên quan đến truy vấn, do đó tạo ra một bối cảnh ngắn gọn hơn và mạnh mẽ hơn cho bước tạo cuối cùng.

Advanced RAG đại diện cho một bước nhảy vọt đáng kể trong sự trưởng thành, biến đường ống truy xuất đơn giản thành một quá trình nhiều giai đoạn với các vòng kiểm soát chất lượng và tối ưu hóa tích hợp.

#### 1.1.3. Modular RAG: Kỷ Nguyên Linh Hoạt và Chuyên Môn Hóa

Modular RAG đại diện cho biên giới hiện tại trong sự tiến hóa của các kiến trúc RAG [2] [3]. Mô hình này tách ra khỏi một đường ống tuyến tính cố định và chấp nhận một phương pháp linh hoạt hơn, plug-and-play. Nó phân tách quá trình RAG thành một loạt các mô-đun có thể trao đổi được, mỗi mô-đun chịu trách nhiệm cho một nhiệm vụ cụ thể. Tính mô-đun này cho phép xây dựng các hệ thống RAG có độ chuyên môn cao và thích ứng có thể được điều chỉnh theo các ứng dụng phức tạp, thực tế [2] [3].

Đổi mới chính của Modular RAG là giới thiệu các mô-đun mới, chuyên biệt và khả năng sắp xếp chúng theo những cách động hơn, bao gồm các quy trình lặp lại và song song.

*   **Các Mô-đun Chuyên Biệt**: Ngoài các thành phần truy xuất và tạo cốt lõi, Modular RAG giới thiệu các mô-đun như:
    *   **Mô-đun Tìm Kiếm**: Mô-đun này có thể giao tiếp với nhiều công cụ tìm kiếm khác nhau ngoài cơ sở dữ liệu vectơ đơn giản, bao gồm các công cụ tìm kiếm truyền thống (như Google hoặc Bing) hoặc cơ sở dữ liệu có cấu trúc (như SQL hoặc cơ sở dữ liệu đồ thị).
    *   **Mô-đun Bộ Nhớ**: Để duy trì bối cảnh trong các cuộc trò chuyện nhiều lượt, một mô-đun bộ nhớ được kết hợp. Nó tận dụng lịch sử hội thoại để tinh chỉnh các truy vấn và bối cảnh hóa các phản hồi, tạo ra trải nghiệm đối thoại hợp lý và tự nhiên hơn.
    *   **Mô-đun Hợp Nhất**: Mô-đun này chịu trách nhiệm hợp nhất và tổng hợp thông tin từ nhiều nguồn hoặc nhiều truy vấn một cách thông minh. Nó có thể kết hợp kết quả từ các truy xuất khác nhau hoặc trộn thông tin được truy xuất cho các truy vấn con thành một bối cảnh thống nhất.

*   **Quy Trình Làm Việc Thích Ứng và Lặp Lại**: Modular RAG cho phép luồng điều khiển phức tạp hơn. Ví dụ, một hệ thống **Adaptive RAG** có thể trước tiên cố gắng trả lời một truy vấn bằng cách sử dụng một phương pháp truy xuất đơn giản. Nếu nó xác định rằng bối cảnh được truy xuất không đủ, nó có thể sau đó kích hoạt một quy trình làm việc phức tạp hơn, chẳng hạn như phân tách truy vấn và thực hiện tìm kiếm web [4]. Quá trình tinh chỉnh lặp lại này, trong đó hệ thống có thể truy xuất, tạo, phản ánh và truy xuất lại, bắt chước một quá trình nghiên cứu giống con người hơn và dẫn đến các đầu ra chất lượng cao hơn đáng kể.

Phương pháp mô-đun, linh hoạt này đánh dấu một sự thay đổi đáng kể từ một đường ống dữ liệu tĩnh đến một khung công việc suy luận động, mở đường cho các kiến trúc dựa trên đồ thị tinh vi hơn mà chúng tôi sẽ khám phá tiếp theo.

## 2. Bước Nhảy Đến Suy Luận Liên Kết: Giới Thiệu Về Graph RAG

Mặc dù Advanced RAG và Modular RAG cải thiện đáng kể chất lượng thông tin được truy xuất, chúng vẫn phần lớn hoạt động trên các bộ sưu tập các chunk văn bản độc lập, không có cấu trúc [5]. Hạn chế cơ bản này làm cho chúng khó có thể xuất sắc trong các nhiệm vụ yêu cầu hiểu các mối quan hệ phức tạp giữa các phần thông tin khác nhau - một dấu hiệu của trí thông minh con người được gọi là **suy luận liên kết** [5]. Để trả lời các câu hỏi phức tạp, con người tự nhiên duyệt qua một mạng lưới tinh thần các khái niệm liên kết. Ví dụ, để trả lời "Quận nào là nơi sinh của chính trị gia Erik Hort là một phần của?", trước tiên người ta phải tìm nơi sinh của Erik Hort (Montebello) và sau đó tìm quận mà Montebello thuộc về (Quận Rockland). Các hệ thống RAG tiêu chuẩn gặp khó khăn với loại suy luận nhiều bước này vì hai sự kiện cần thiết có thể nằm trong các tài liệu hoàn toàn riêng biệt, không liên quan về mặt ngữ nghĩa.

Đây là nơi **Graph RAG** xuất hiện như một mô hình biến đổi [5]. Graph RAG tận dụng sức mạnh của **Đồ Thị Kiến Thức (KGs)** để biểu diễn thông tin một cách rõ ràng như một mạng lưới các thực thể liên kết (nút) và các mối quan hệ của chúng (cạnh). Bằng cách làm như vậy, nó vượt ra ngoài độ tương tự ngữ nghĩa đơn giản và cho phép một hệ thống suy luận trên các kết nối có cấu trúc trong dữ liệu, trực tiếp giải quyết thách thức suy luận nhiều bước [5].

### 2.1. Tại Sao Đồ Thị Kiến Thức?

Một Đồ Thị Kiến Thức cung cấp một biểu diễn phong phú hơn và rõ ràng hơn nhiều về một lĩnh vực kiến thức so với một bộ sưu tập đơn giản các chunk văn bản [5]. Cấu trúc này cung cấp một số lợi thế chính cho truy xuất:

*   **Các Mối Quan Hệ Rõ Ràng**: KGs làm cho các mối quan hệ giữa các thực thể rõ ràng và có thể duyệt được. Điều này cho phép một hệ thống truy xuất theo dõi các kết nối từ một thực thể này sang thực thể khác, hiệu quả thực hiện các truy vấn nhiều bước [5].

*   **Sự Phong Phú Bối Cảnh**: Bằng cách nắm bắt bối cảnh của cách các thực thể liên quan, KGs cung cấp một mức độ hiểu biết sâu hơn so với các chunk văn bản cô lập.

*   **Giảm Sự Mơ Hồ**: Các thực thể trong một KG thường được chuẩn hóa, có nghĩa là các đề cập khác nhau của cùng một thực thể (ví dụ: "Apple Inc.", "Apple", "công ty ở Cupertino") có thể được giải quyết thành một nút duy nhất, giảm sự mơ hồ [5].

*   **Tích Hợp Dữ Liệu**: KGs cung cấp một khung công việc tự nhiên để tích hợp cả dữ liệu có cấu trúc (từ cơ sở dữ liệu) và dữ liệu không có cấu trúc (từ văn bản), tạo ra một cơ sở kiến thức thống nhất.

Bằng cách tăng cường đường ống RAG với một đồ thị kiến thức, các hệ thống Graph RAG có thể thực hiện suy luận tinh vi hơn, giống con người hơn, dẫn đến các câu trả lời chính xác hơn và toàn diện hơn cho các truy vấn phức tạp [5].

### 2.2. Kiến Trúc của Một Hệ Thống Graph RAG

Một hệ thống Graph RAG điển hình, mặc dù khác nhau trong triển khai cụ thể, thường bao gồm một số thành phần cốt lõi hoạt động cùng nhau để tận dụng kiến thức có cấu trúc của đồ thị [5] [6].

#### 2.2.1. Giai Đoạn Ngoại Tuyến: Xây Dựng Đồ Thị Kiến Thức

Nền tảng của bất kỳ hệ thống Graph RAG nào là Đồ Thị Kiến Thức chính nó. Đồ thị này thường được xây dựng trong một quá trình ngoại tuyến từ một kho tài liệu nguồn [6].

1.  **Trích Xuất Thực Thể và Mối Quan Hệ**: Quá trình bắt đầu bằng cách sử dụng một LLM mạnh mẽ để đọc qua văn bản nguồn và trích xuất thông tin chính [6]. LLM được nhắc để xác định các thực thể (ví dụ: người, tổ chức, địa điểm) và các mối quan hệ kết nối chúng. Điều này thường được thực hiện bằng cách sử dụng phương pháp "Open Information Extraction" (OpenIE), trong đó LLM không bị ràng buộc bởi một lược đồ được xác định trước và có thể xác định bất kỳ bộ ba chủ đề-vị từ-đối tượng liên quan nào (ví dụ: `(Cinderella, attended, the royal ball)`).

2.  **Lắp Ráp Đồ Thị**: Các bộ ba được trích xuất sau đó được sử dụng để xây dựng đồ thị. Mỗi thực thể duy nhất trở thành một nút, và mỗi mối quan hệ trở thành một cạnh có hướng giữa các nút tương ứng [6].

3.  **Làm Giàu Nút và Cạnh**: Đồ thị thường được làm giàu với thông tin bổ sung. Ví dụ, các chunk văn bản ban đầu mà từ đó các bộ ba được trích xuất có thể được đính kèm vào các nút hoặc cạnh dưới dạng các thuộc tính. Hơn nữa, các nhúng vectơ thường được tạo cho các nút (và đôi khi là các mối quan hệ), nắm bắt ý nghĩa ngữ nghĩa của chúng. Điều này tạo ra một cấu trúc lai hỗ trợ cả duyệt đồ thị và tìm kiếm ngữ nghĩa [6].

4.  **Phát Hiện Cộng Đồng và Tóm Tắt (Nâng Cao)**: Một số framework Graph RAG nâng cao, như GraphRAG của Microsoft, thực hiện các bước ngoại tuyến bổ sung. Họ có thể chạy các thuật toán đồ thị như phát hiện cộng đồng (ví dụ: thuật toán Leiden) để xác định các cụm các thực thể được kết nối chặt chẽ. Các bản tóm tắt sau đó có thể được tạo cho các cộng đồng này, tạo ra các mức độ trừu tượng phân cấp trong cơ sở kiến thức [6].

#### 2.2.2. Giai Đoạn Trực Tuyến: Truy Xuất và Tạo

Khi người dùng gửi một truy vấn, giai đoạn trực tuyến bắt đầu [5].

1.  **Truy Xuất Đồ Thị Con**: Đây là lõi của quá trình truy xuất Graph RAG. Thay vì chỉ tìm các chunk tương tự, mục tiêu là truy xuất một đồ thị con liên quan - một phần của đồ thị kiến thức chính chứa thông tin cần thiết để trả lời truy vấn [5]. Đây là một quá trình nhiều bước:
    *   **Xác Định Nút Hạt Giống**: Hệ thống trước tiên xác định các điểm bắt đầu liên quan nhất trong đồ thị dựa trên truy vấn của người dùng. Điều này có thể được thực hiện bằng cách thực hiện tìm kiếm vectơ trên các nút của đồ thị để tìm các thực thể có sự tương tự ngữ nghĩa với truy vấn [5].
    *   **Duyệt Đồ Thị**: Bắt đầu từ các nút hạt giống, hệ thống duyệt qua đồ thị, theo dõi các mối quan hệ để khám phá các nút được kết nối. Duyệt này có thể là một mở rộng đơn giản một hoặc hai bước, hoặc nó có thể được hướng dẫn bởi các thuật toán tinh vi hơn như Personalized PageRank (như chúng ta sẽ thấy trong HippoRAG) để xác định mức độ liên quan của các đường dẫn khác nhau [5].

2.  **Tuần Tự Hóa/Mã Hóa Đồ Thị Thành Văn Bản**: Sau khi một đồ thị con liên quan đã được truy xuất, nó cần được chuyển đổi thành một định dạng mà LLM tạo có thể hiểu. Đây là một bước quan trọng. Một phương pháp đơn giản là tuyến tính hóa đồ thị, chuyển đổi các nút và cạnh thành một định dạng văn bản có cấu trúc (ví dụ: "[Thực Thể 1] -> [Mối Quan Hệ] -> [Thực Thể 2]"). Các phương pháp nâng cao hơn cũng có thể bao gồm văn bản ban đầu liên quan đến các nút và cạnh để cung cấp bối cảnh phong phú hơn [5].

3.  **Tạo**: Cuối cùng, văn bản đồ thị con được tuần tự hóa được chuyển đến LLM, cùng với truy vấn ban đầu. LLM sử dụng bối cảnh có cấu trúc, liên kết này để tổng hợp một câu trả lời toàn diện và có cơ sở thực tế. Vì bối cảnh rõ ràng chứa các mối quan hệ giữa các thực thể, LLM có thể dễ dàng theo dõi các bước logic cần thiết cho suy luận nhiều bước [5].

Kiến trúc này đại diện cho một sự thay đổi cơ bản từ việc truy xuất các sự kiện cô lập đến truy xuất kiến thức liên kết, cho phép một lớp hệ thống RAG mạnh mẽ hơn và thông minh hơn.

## 3. Một Cuộc Khảo Sát Các Framework Graph RAG Nổi Bật

Khung khái niệm của Graph RAG đã truyền cảm hứng cho nhiều triển khai, mỗi triển khai có cách tiếp cận độc đáo của riêng nó đối với xây dựng đồ thị, truy xuất và tích hợp với LLMs [5] [6] [7] [8]. Phần này cung cấp một cái nhìn tổng quan về một số framework chính và bài báo đã định hình lĩnh vực này.

### 3.1. GraphRAG của Microsoft

GraphRAG của Microsoft là một trong những triển khai nổi tiếng nhất, cung cấp một bản thiết kế chi tiết để tận dụng các đồ thị kiến thức trong RAG [6]. Quá trình của nó được chia thành hai giai đoạn chính: lập chỉ mục và truy vấn [6].

*   **Lập Chỉ Mục**: Đường ống lập chỉ mục là một quá trình phức tạp, nhiều bước. Nó bắt đầu với phân đoạn văn bản và sau đó sử dụng LLM để trích xuất các thực thể, mối quan hệ và tuyên bố từ văn bản để xây dựng một đồ thị kiến thức ban đầu. Một đổi mới chính là việc sử dụng sau đó của phân cụm phân cấp (cụ thể là thuật toán Leiden) trên đồ thị này để xác định các cộng đồng của các nút được kết nối chặt chẽ. Hệ thống sau đó tạo các bản tóm tắt văn bản cho mỗi cộng đồng, tạo ra một sự hiểu biết đa cấp, phân cấp về tập dữ liệu [6].

*   **Truy Vấn**: GraphRAG hỗ trợ hai quy trình truy vấn riên biệt:
    *   **Tìm Kiếm Toàn Cầu**: Đối với các câu hỏi rộng, toàn diện về toàn bộ tập dữ liệu (ví dụ: "Các chủ đề chính trong bộ sưu tập tài liệu này là gì?"), hệ thống tận dụng các bản tóm tắt cộng đồng được tạo trước để cung cấp một câu trả lời cấp cao [6].
    *   **Tìm Kiếm Cục Bộ**: Đối với các câu hỏi cụ thể về một thực thể cụ thể (ví dụ: "John Doe đã làm việc trên những dự án nào?"), hệ thống bắt đầu tại nút thực thể tương ứng và mở rộng đến các hàng xóm gần nhất và các khái niệm liên quan để truy xuất một đồ thị con tập trung và liên quan về bối cảnh [6].

Cách tiếp cận kép này cho phép GraphRAG của Microsoft xử lý hiệu quả một loạt các loại truy vấn, từ tóm tắt cấp cao đến truy xuất sự kiện cụ thể.

### 3.2. GRAG: Truy Xuất Đồ Thị - Tạo Được Tăng Cường

Framework GRAG, được đề xuất bởi Hu et al. (2024), được thiết kế đặc biệt để giải quyết những thách thức của việc truy xuất và suy luận trên các tài liệu có mạng lưới, chẳng hạn như các mạng lưới trích dẫn học tập [7]. Nó giới thiệu một chiến lược chia để trị mới cho truy xuất đồ thị con hiệu quả và một phương pháp hai chế độ xem cho việc tạo [7].

*   **Truy Xuất Đồ Thị Con Hiệu Quả**: Thuật toán truy xuất của GRAG được tối ưu hóa để tìm cấu trúc đồ thị con liên quan nhất trong thời gian tuyến tính, làm cho nó cực kỳ hiệu quả cho các đồ thị lớn [7].

*   **Tạo Chế Độ Xem Kép**: Để cung cấp cho LLM một sự hiểu biết toàn diện về thông tin được truy xuất, GRAG mã hóa đồ thị con theo hai cách: một **chế độ xem văn bản**, tuyến tính hóa nội dung của các nút, và một **chế độ xem đồ thị**, đại diện cho cấu trúc tôpô của đồ thị con [7]. Biểu diễn kép này đảm bảo rằng LLM hiểu cả *cái gì* thông tin là và *cách* nó được kết nối.

### 3.3. KG-RAG: Xây Dựng Đồ Thị Kiến Thức Tại Chỗ

Được đề xuất bởi Sanmartin (2024), KG-RAG tập trung vào việc nâng cao các Tác Nhân Mô Hình Ngôn Ngữ Lớn (LMAs) bằng cách tích hợp chúng với các đồ thị kiến thức có thể được xây dựng tại chỗ từ văn bản không có cấu trúc [8]. Điều này đặc biệt hữu ích trong các tình huống mà một đồ thị kiến thức được quản lý, được tạo trước không có sẵn [8].

Một đóng góp chính của KG-RAG là một thuật toán truy xuất mới được gọi là **Chain of Explorations (CoE)**. Thay vì truy xuất một lần, CoE tận dụng khả năng suy luận của LLM để khám phá đồ thị kiến thức một cách tuần tự [8]. LLM có thể quyết định đường dẫn nào để theo dõi hoặc nút nào để khám phá tiếp theo dựa trên thông tin nó đã thu thập cho đến nay, dẫn đến một quá trình truy xuất thông tin năng động hơn và hiệu quả hơn.

## 4. HippoRAG: Một Hệ Thống Bộ Nhớ Lấy Cảm Hứng Từ Sinh Học Thần Kinh

Mặc dù các framework Graph RAG được thảo luận ở trên tiến bộ đáng kể trạng thái của truy xuất bằng cách kết hợp kiến thức có cấu trúc, **HippoRAG** của gia đình mô hình giới thiệu một quan điểm độc đáo và mạnh mẽ, rút ra cảm hứng trực tiếp từ sinh học thần kinh của bộ nhớ dài hạn con người [9]. Phương pháp này, được phát triển bởi Gutiérrez et al., nhằm mục đích bắt chước chặt chẽ hơn cách bộ não con người sắp xếp, liên kết và truy xuất thông tin, đặc biệt tập trung vào vai trò của hồi hộp [9].

### 4.1. Cảm Hứng: Bộ Nhớ Dài Hạn Con Người

Bộ nhớ con người không phải là một cửa hàng khóa-giá trị đơn giản. Nó là một mạng lưới động, liên kết. Hồi hộp, một cấu trúc quan trọng trong não, được cho là hoạt động như một "chỉ mục", tạo và lưu trữ các con trỏ đến các khía cạnh khác nhau của một bộ nhớ được phân phối trên toàn bộ vỏ não [9]. Khi chúng ta nhớ lại một bộ nhớ, hồi hộp kích hoạt mạng lưới các con trỏ này, liên kết các phần rời rạc của thông tin thành một tổng thể hợp lý. Thuộc tính tự liên kết này cho phép chúng ta thực hiện những kỳ tích suy luận nhiều bước và nhớ lại bối cảnh. HippoRAG là một nỗ lực để xây dựng một tương tự nhân tạo của hệ thống này cho LLMs [9].

### 4.2. HippoRAG: Thế Hệ Đầu Tiên

Framework HippoRAG ban đầu giới thiệu một kiến trúc mới với ba thành phần chính được thiết kế để phản ánh các đối tác sinh học của chúng [9]:

1.  **Vỏ Não Nhân Tạo (LLM)**: Mô Hình Ngôn Ngữ Lớn chính nó được coi là vỏ não, kho lưu trữ khổng lồ kiến thức tổng quát và nơi ngồi của suy luận và tạo cấp cao [9].

2.  **Chỉ Mục Hồi Hộp Nhân Tạo (KG + PPR)**: Đây là đổi mới cốt lõi. Một Đồ Thị Kiến Thức được xây dựng từ các tài liệu nguồn bằng cách sử dụng OpenIE, tương tự như các phương pháp Graph RAG khác. Tuy nhiên, cơ chế truy xuất là khác biệt. Nó sử dụng thuật toán **Personalized PageRank (PPR)** [9]. PPR là một thuật toán duyệt đồ thị đo lường tầm quan trọng của các nút từ quan điểm của một tập hợp "nút hạt giống" nhất định. Trong HippoRAG, các thực thể được trích xuất từ truy vấn của người dùng được sử dụng để xác định các nút hạt giống trong KG. PPR sau đó mô phỏng một "bước ngẫu nhiên" từ các hạt giống này, truyền năng lượng kích hoạt trên toàn bộ đồ thị. Các nút gần hơn và được kết nối nhiều hơn với các hạt giống nhận được điểm số cao hơn, hiệu quả xác định đồ thị con liên quan nhất cho truy vấn [9].

3.  **Các Vùng Parahippocampal Nhân Tạo (Bộ Mã Hóa Truy Xuất)**: Một mô hình transformer câu tiêu chuẩn hoạt động như cầu nối giữa vỏ não (LLM) và chỉ mục hồi hộp (KG). Nó chịu trách nhiệm ánh xạ các khái niệm từ truy vấn của LLM đến các nút tương ứng trong KG [9].

Mặc dù HippoRAG thể hiện một khả năng đáng chú ý để thực hiện suy luận nhiều bước (liên kết), vượt trội hơn đáng kể so với RAG tiêu chuẩn trên các nhiệm vụ như vậy, nó có một điểm yếu quan trọng. Sự phụ thuộc của nó vào việc trích xuất chỉ các thực thể được đặt tên từ truy vấn cho việc xác định nút hạt giống (một phương pháp "tập trung vào khái niệm") có nghĩa là nó thường bỏ lỡ thông tin bối cảnh quan trọng từ truy vấn, dẫn đến hiệu suất kém hơn trên các tác vụ nhớ lại thực tế đơn giản và hiểu rõ ý nghĩa so với tìm kiếm vectơ tiêu chuẩn [10].

### 4.3. HippoRAG 2: Từ RAG Đến Một Hệ Thống Bộ Nhớ Thực Sự

HippoRAG 2 được phát triển để giải quyết những hạn chế của người tiền nhiệm và tạo ra một khung công việc mạnh mẽ hơn xuất sắc trên tất cả các kích thước chính của bộ nhớ: nhớ lại thực tế, hiểu rõ ý nghĩa và liên kết [10]. Nó giữ lại kiến trúc lấy cảm hứng từ sinh học thần kinh cốt lõi nhưng giới thiệu ba cải tiến quan trọng dẫn đến cải thiện hiệu suất toàn diện [10].

#### 4.3.1. Những Cải Tiến Kiến Trúc Chính

1.  **Tích Hợp Dense-Sparse (Thêm Các Nút Đoạn Văn)**: KG ban đầu của HippoRAG bao gồm chỉ "các nút cụm từ" (khái niệm). HippoRAG 2 tăng cường đồ thị bằng cách cũng bao gồm **các nút đoạn văn**, đại diện cho các chunk văn bản ban đầu [10]. Sau đó, nó tạo các cạnh "contains" liên kết mỗi nút đoạn văn với các nút cụm từ được trích xuất từ nó. Điều này tạo ra một đồ thị lai tích hợp biểu diễn "thưa thớt" ngắn gọn của các khái niệm với thông tin bối cảnh phong phú "dày đặc" của các đoạn văn ban đầu, được lấy cảm hứng từ các lý thuyết mã hóa dày đặc và thưa thớt của não [10].

2.  **Bối Cảnh Hóa Sâu Hơn (Khớp Truy Vấn-Với-Triple)**: Để vượt qua sự mù quáng bối cảnh của HippoRAG ban đầu, HippoRAG 2 thay đổi cách nó xác định các nút hạt giống. Thay vì chỉ trích xuất các thực thể từ truy vấn, nó sử dụng nhúng của **toàn bộ truy vấn** để tìm **các bộ ba** (chủ đề-vị từ-đối tượng) tương tự nhất trong đồ thị [10]. Phương pháp "Query-to-Triple" này cung cấp một tín hiệu bối cảnh phong phú hơn nhiều để bắt đầu duyệt đồ thị, vì các bộ ba vốn nắm bắt một sự kiện hoặc mối quan hệ hoàn chỉnh.

3.  **Bộ Nhớ Nhận Dạng (Lọc Dựa Trên LLM)**: Rút ra một sự song song khác với bộ nhớ con người, HippoRAG 2 giới thiệu một bước "nhận dạng". Sau khi truy xuất truy vấn-với-triple ban đầu, một LLM được sử dụng để lọc các bộ ba được truy xuất. LLM được nhắc để đánh giá xem mỗi bộ ba có thực sự liên quan đến truy vấn của người dùng hay không [10]. Điều này hoạt động như một cổng kiểm soát chất lượng, loại bỏ các bộ ba nhiễu hoặc không liên quan trước khi chúng được sử dụng làm hạt giống cho thuật toán Personalized PageRank tốn kém, cải thiện cả độ chính xác và hiệu quả của truy xuất.

#### 4.3.2. Đường Ống HippoRAG 2

*   **Lập Chỉ Mục Ngoại Tuyến**: Quá trình ngoại tuyến liên quan đến việc trích xuất các bộ ba từ các đoạn văn bằng cách sử dụng LLM, xây dựng KG với cả các nút cụm từ và nút đoạn văn, và phát hiện các từ đồng nghĩa để liên kết các khái niệm liên quan [10].

*   **Truy Xuất Trực Tuyến**: Khi một truy vấn được nhận, hệ thống thực hiện khớp truy vấn-với-triple để nhận được một tập hợp các bộ ba hạt giống ứng viên. "Bộ Nhớ Nhận Dạng" LLM sau đó lọc tập hợp này. Các bộ ba độ liên quan cao còn lại, cùng với các nút đoạn văn tương tự nhất, được sử dụng làm hạt giống cho thuật toán Personalized PageRank [10]. PPR chạy trên đồ thị tích hợp, và các điểm PageRank cuối cùng được sử dụng để xếp hạng các đoạn văn. Các đoạn văn được xếp hạng cao nhất sau đó được cấp cho mô hình QA cho việc tạo câu trả lời cuối cùng.

Những cải tiến này tập hợp lại tạo ra một hệ thống không chỉ là một lý luận nhiều bước mạnh mẽ mà còn là một công cụ nhớ lại thực tế mạnh mẽ và hiểu rõ ý nghĩa, như được chứng minh bởi hiệu suất điểm chuẩn của nó.

## 5. Phân Tích So Sánh và Hiệu Suất Điểm Chuẩn

Những lợi thế lý thuyết của các kiến trúc RAG khác nhau được hiểu rõ nhất thông qua bằng chứng thực nghiệm [10]. Bài báo HippoRAG 2 cung cấp một đánh giá toàn diện trên một loạt các tập dữ liệu, so sánh hiệu suất của nó với các đường cơ sở đơn giản, các mô hình nhúng lớn và các framework RAG được tăng cường cấu trúc khác. Phần này phân tích những kết quả điểm chuẩn chính đó để cung cấp một sự hiểu biết định lượng về nơi mỗi kiến trúc xuất sắc và gặp khó khăn [10].

### 5.1. Hiệu Suất Trả Lời Câu Hỏi Từ Đầu Đến Cuối

Thước đo cuối cùng của một hệ thống RAG là chất lượng của các câu trả lời cuối cùng của nó. Bảng sau đây cho thấy các điểm F1 cho nhiệm vụ QA từ đầu đến cuối trên bảy điểm chuẩn khác nhau, được phân loại theo loại suy luận mà chúng yêu cầu: Simple QA (NQ, PopQA), Multi-Hop QA (MuSiQue, 2Wiki, HotpotQA, LV-Eval) và Discourse Understanding (NarrativeQA) [10]. Mô hình Llama-3.3-70B-Instruct mạnh mẽ được sử dụng làm trình tạo cho tất cả các hệ thống để đảm bảo so sánh công bằng các thành phần truy xuất.

| Phương Pháp | NQ | PopQA | MuSiQue | 2Wiki | HotpotQA | LV-Eval | NarrativeQA | Trung Bình |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Không Truy Xuất | 54.9 | 32.5 | 26.1 | 42.8 | 47.3 | 6.0 | 12.9 | 38.4 |
| BM25 | 59.0 | 49.9 | 28.8 | 51.2 | 63.4 | 5.9 | 18.3 | 47.7 |
| NV-Embed-v2 (7B) | 61.9 | 55.7 | 45.7 | 61.5 | 75.3 | 9.8 | 25.7 | 57.0 |
| RAPTOR | 50.7 | 56.2 | 28.9 | 52.1 | 69.5 | 5.0 | 21.4 | 48.8 |
| GraphRAG | 46.9 | 48.1 | 38.5 | 58.6 | 68.6 | 11.2 | 23.0 | 49.6 |
| HippoRAG | 55.3 | 55.9 | 35.1 | 71.8 | 63.5 | 8.4 | 16.3 | 53.1 |
| **HippoRAG 2** | **63.3** | **56.2** | **48.6** | **71.0** | **75.5** | **12.9** | **25.9** | **59.8** |

*Bảng 1: Hiệu suất QA (điểm F1) trên các điểm chuẩn RAG sử dụng Llama-3.3-70B-Instruct làm trình đọc QA. Nguồn: [10]*

#### Phân Tích Kết Quả QA:

*   **Sự Thống Trị của HippoRAG 2**: Điều đáng chú ý nhất là HippoRAG 2 là framework được tăng cường cấu trúc duy nhất liên tục vượt trội so với đường cơ sở RAG tiêu chuẩn mạnh nhất (NV-Embed-v2, một mô hình nhúng 7B tham số mạnh mẽ) [10]. Nó đạt được điểm trung bình cao nhất và cho thấy những lợi ích đáng kể trong các nhiệm vụ đa bước và hiểu rõ diễn ngôn phức tạp nhất.

*   **Thất Bại của Các RAG Có Cấu Trúc Khác**: Các phương pháp có cấu trúc khác như RAPTOR và GraphRAG, mặc dù sáng tạo, cho thấy sự sụt giảm hiệu suất đáng kể so với RAG tiêu chuẩn trên các điểm chuẩn này [10]. Điều này có khả năng là vì các cơ chế tóm tắt của chúng, mặc dù hữu ích cho việc hiểu rõ ý nghĩa, có thể giới thiệu tiếng ồn hoặc mất các chi tiết quan trọng, điều này làm hại cho hiệu suất trên các nhiệm vụ QA thực tế và nhiều bước.

*   **Lợi Ích Liên Kết**: Trên các tập dữ liệu nhiều bước (MuSiQue, 2Wiki, LV-Eval), HippoRAG 2 cho thấy một lợi thế rõ ràng, đạt được cải tiến trung bình 7% so với mô hình nhúng tốt nhất [10]. Điều này trực tiếp xác nhận giả thuyết rằng duyệt đồ thị của nó vượt trội hơn so với tìm kiếm ngữ nghĩa đơn thuần cho suy luận liên kết.

*   **Không Có Sự Đánh Đổi**: Quan trọng, không giống như người tiền nhiệm HippoRAG, HippoRAG 2 đạt được những lợi ích liên kết này mà không hy sinh hiệu suất trên việc nhớ lại thực tế đơn giản (NQ, PopQA) [10]. Nó thậm chí còn vượt trội một chút so với đường cơ sở trên các nhiệm vụ này, chứng minh rằng các cải tiến kiến trúc của nó đã thành công giải quyết những điểm yếu của thế hệ đầu tiên.

### 5.2. Hiệu Suất Truy Xuất (Recall@5)

Mặc dù hiệu suất QA từ đầu đến cuối là mục tiêu cuối cùng, đánh giá giai đoạn truy xuất trong cách ly là rất quan trọng để chẩn đoán hiệu suất hệ thống [10]. Bảng sau đây cho thấy số liệu Recall@5, đo lường xem các đoạn văn cơ sở sự thật cần thiết để trả lời câu hỏi có hiện diện trong 5 tài liệu được truy xuất hàng đầu hay không [10].

| Phương Pháp | NQ | PopQA | MuSiQue | 2Wiki | HotpotQA | Trung Bình |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| BM25 | 56.1 | 35.7 | 43.5 | 65.3 | 74.8 | 55.1 |
| NV-Embed-v2 (7B) | 75.4 | 51.0 | 69.7 | 76.5 | 94.5 | 73.4 |
| RAPTOR | 68.3 | 48.7 | 57.8 | 66.2 | 86.9 | 65.6 |
| HippoRAG (tái tạo) | 44.4 | 53.8 | 53.2 | 90.4 | 77.3 | 63.8 |
| **HippoRAG 2** | **78.0** | **51.7** | **74.7** | **90.4** | **96.3** | **78.2** |

*Bảng 2: Hiệu suất truy xuất (passage recall@5) trên các điểm chuẩn RAG. Nguồn: [10]*

#### Phân Tích Kết Quả Truy Xuất:

*   **Độ Chính Xác Truy Xuất Vượt Trội**: HippoRAG 2 liên tục đạt được độ nhớ lại truy xuất cao nhất, với điểm trung bình 78.2, vượt trội đáng kể so với hệ thống tốt nhất tiếp theo (NV-Embed-v2 ở 73.4) [10]. Điều này chứng minh rằng các cải tiến kiến trúc trực tiếp dẫn đến một giai đoạn truy xuất chính xác và toàn diện hơn.

*   **Sức Mạnh Duyệt Đồ Thị**: Những cải tiến nổi bật nhất được nhìn thấy trên các tập dữ liệu nhiều bước. Trên MuSiQue, HippoRAG 2 đạt được độ nhớ lại 74.7, đầy đủ 5 điểm cao hơn đường cơ sở NV-Embed-v2 mạnh mẽ [10]. Điều này cho thấy sức mạnh của duyệt Personalized PageRank để tìm các phần thông tin liên kết mà tìm kiếm ngữ nghĩa đơn thuần bỏ lỡ.

*   **Độ Bền Vững**: Thực tế là HippoRAG 2 cũng đạt được độ nhớ lại cao nhất trên tập dữ liệu QA đơn giản (NQ) tiếp tục nhấn mạnh tính bền vững của nó [10]. Tích hợp các nút đoạn văn và bối cảnh hóa được cải thiện cho phép nó hoạt động tốt như, hoặc tốt hơn, tìm kiếm vectơ thuần túy trên sân nhà của nó, đồng thời cũng cung cấp những lợi ích của duyệt đồ thị.

Những kết quả điểm chuẩn này cung cấp bằng chứng định lượng mạnh mẽ rằng HippoRAG 2 đại diện cho một bước tiến đáng kể trong sự phát triển của các hệ thống RAG. Bằng cách kết hợp một cách suy tư duyệt dựa trên đồ thị với các kỹ thuật truy xuất ngữ nghĩa nâng cao, nó tạo ra một hệ thống lớn hơn tổng các bộ phận của nó, đạt được một trạng thái mới trong suy luận toàn diện và truy xuất kiến thức cho LLMs [10].

## 6. Từ Lý Thuyết Đến Thực Hành: Triển Khai và Đánh Giá Các Hệ Thống RAG

Hiểu biết kiến trúc tiến hóa của RAG là bước đầu tiên. Đối với một kỹ sư AI, thách thức thực sự và cơ hội nằm trong việc triển khai, tối ưu hóa và đánh giá chặt chẽ các đường ống RAG này, từ các hệ thống dựa trên vectơ nâng cao đến các kiến trúc đồ thị phức tạp [3] [4]. Phần này chuyển từ lý thuyết sang thực tế, cung cấp một hướng dẫn chi tiết để xây dựng và đánh giá các đường ống RAG cấp sản xuất, từ các hệ thống vectơ nâng cao đến các kiến trúc dựa trên đồ thị phức tạp.

### 6.1. Hướng Dẫn Thực Tế Để Triển Khai Advanced RAG

Xây dựng trên bản thiết kế Naive RAG, triển khai một hệ thống Advanced RAG liên quan đến một loạt các lựa chọn và sự đánh đổi có chủ đích trong các giai đoạn trước truy xuất và sau truy xuất [3] [4]. Chúng tôi sẽ khám phá những kỹ thuật này bằng cách sử dụng Python và các framework phổ biến như LangChain và LlamaIndex, cung cấp các khối xây dựng mô-đun cho các đường ống tinh vi này.

#### 6.1.1. Trước Truy Xuất: Làm Chủ Chunking và Biến Đổi Truy Vấn

Chất lượng của những gì bạn truy xuất bị giới hạn cơ bản bởi chất lượng của những gì bạn lập chỉ mục và cách bạn yêu cầu nó. Đây là nơi các tối ưu hóa trước truy xuất trở nên quan trọng [3] [4].

**Chiến Lược Chunking Thông Minh**

Mục tiêu của chunking là tạo ra các đơn vị tự chứa, có ý nghĩa ngữ nghĩa. Lựa chọn chiến lược chunking là một sự đánh đổi giữa bảo toàn bối cảnh và độ chính xác truy xuất [3] [4].

*   **Chia Nhỏ Văn Bản Ký Tự Đệ Quy**: Đây thường là điểm bắt đầu được khuyến nghị. Nó cố gắng chia văn bản dựa trên một danh sách phân cấp các bộ phân tách (ví dụ: `["\n\n", "\n", " ", ""]`) và cố gắng giữ các đoạn, sau đó là câu, sau đó là từ lại với nhau miễn là có thể. Phương pháp này mạnh mẽ và thường bảo toàn các ranh giới ngữ nghĩa tốt hơn so với một công cụ chia nhỏ kích thước cố định [3] [4].

    ```python
    # Ví dụ sử dụng LangChain
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200, # Sự chồng lấp giúp duy trì bối cảnh giữa các chunk
        length_function=len
    )
    chunks = text_splitter.split_text(long_document_text)
    ```

*   **Chunking Ngữ Nghĩa**: Một kỹ thuật nâng cao hơn liên quan đến việc chia văn bản dựa trên độ tương tự ngữ nghĩa. Tài liệu được chia thành các câu riêng lẻ, và sau đó các câu được nhóm thành các chunk dựa trên độ tương tự nhúng vectơ của chúng [3] [4]. Một chunk mới được bắt đầu khi khoảng cách ngữ nghĩa giữa các câu liên tiếp vượt quá một ngưỡng nhất định. Điều này đảm bảo rằng mỗi chunk có tính kết hợp cao và tập trung vào một chủ đề duy nhất.

**Biến Đổi Truy Vấn Để Nâng Cao Truy Xuất**

Truy vấn của người dùng hiếm khi tối ưu cho cơ sở dữ liệu vectơ. Biến đổi truy vấn hoạt động như một lớp tiền xử lý để tinh chỉnh truy vấn cho kết quả truy xuất tốt hơn [3] [4].

*   **Nhúng Tài Liệu Giả Thuyết (HyDE)**: Kỹ thuật này liên quan đến việc sử dụng LLM để tạo ra một câu trả lời hoặc tài liệu giả thuyết cho truy vấn của người dùng *trước* truy xuất [3]. Nhúng của tài liệu giả thuyết này, phong phú về bối cảnh và từ khóa, sau đó được sử dụng để truy vấn cơ sở dữ liệu vectơ. Điều này thường dẫn đến các truy xuất liên quan hơn so với sử dụng nhúng của truy vấn người dùng thưa thớt [3].

*   **Truy Xuất Nhiều Truy Vấn**: Thay vì một truy vấn duy nhất, LLM có thể được sử dụng để tạo ra một số biến thể của truy vấn của người dùng từ các quan điểm khác nhau [3]. Mỗi truy vấn này sau đó được chạy so với truy xuất, và các kết quả được tổng hợp. Điều này mở rộng tìm kiếm và tăng cơ hội tìm thấy thông tin liên quan, cải thiện độ nhớ lại.

    ```python
    # Ví dụ khái niệm sử dụng LangChain
    from langchain.retrievers.multi_query import MultiQueryRetriever
    from langchain_openai import ChatOpenAI

    question = "Những nguyên nhân chính của cuộc khủng hoảng tài chính năm 2008 là gì?"
    llm = ChatOpenAI(temperature=0)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=vector_db.as_retriever(), llm=llm
    )
    ```

#### 6.1.2. Sau Truy Xuất: Xếp Hạng Lại và Nén Cho Độ Chính Xác

Sau khi bạn có một tập hợp các tài liệu ứng viên, các kỹ thuật sau truy xuất tinh chỉnh tập hợp này để tạo bối cảnh mạnh nhất cho LLM tạo [3] [4].

**Xếp Hạng Lại Cross-Encoder**

Tìm kiếm độ tương tự vectơ (bi-encoder) nhanh nhưng có thể không chính xác. Một bước xếp hạng lại giới thiệu một mô hình **cross-encoder** mạnh mẽ hơn nhưng chậm hơn [3]. Một cross-encoder lấy cả truy vấn và một tài liệu ứng viên làm một đầu vào duy nhất và xuất ra một điểm liên quan. Điều này cho phép phân tích sâu hơn nhiều, từng token, về mối quan hệ giữa truy vấn và tài liệu [3].

Quy trình làm việc điển hình là trước tiên truy xuất một tập hợp lớn hơn các tài liệu (ví dụ: 50 hàng đầu) bằng cách sử dụng tìm kiếm vectơ nhanh và sau đó sử dụng cross-encoder chậm hơn nhưng chính xác hơn để xếp hạng lại 50 tài liệu này và chọn 3-5 hàng đầu cho bối cảnh cuối cùng [3].

**Nén Bối Cảnh**

Để tối đa hóa tiện ích của cửa sổ bối cảnh hạn chế của LLM, điều cần thiết là loại bỏ "rác" không liên quan từ các tài liệu được truy xuất. Một `ContextualCompressionRetriever` có thể được sử dụng để bao bọc một truy xuất cơ sở. Sau khi truy xuất, nó chuyển các tài liệu thông qua một `DocumentCompressor` lặp lại nội dung và trích xuất chỉ các phần liên quan đến truy vấn [3].

```python
# Ví dụ khái niệm sử dụng LangChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, 
    base_retriever=vector_db.as_retriever()
)

compressed_docs = compression_retriever.get_relevant_documents(
    "Tác giả nói gì về AI trong phần giới thiệu?"
)
```

Bằng cách kết hợp những kỹ thuật nâng cao này, các kỹ sư có thể xây dựng các hệ thống RAG cực kỳ hiệu quả và mạnh mẽ vượt trội hơn đáng kể so với phương pháp Naive RAG, out-of-the-box [3] [4].

### 6.2. Hướng Dẫn Thực Tế Để Triển Khai Graph RAG

Triển khai một hệ thống Graph RAG là một quá trình phức tạp hơn so với một đường ống RAG tiêu chuẩn, vì nó yêu cầu một giai đoạn ngoại tuyến bổ sung cho việc xây dựng đồ thị kiến thức [5] [6]. Tuy nhiên, phần thưởng là một hệ thống có khả năng suy luận sâu hơn nhiều. Chúng tôi sẽ đi bộ qua các bước chính bằng cách sử dụng Python, LangChain và cơ sở dữ liệu đồ thị như Neo4j [5] [6].

#### 6.2.1. Giai Đoạn Ngoại Tuyến: Xây Dựng Đồ Thị Kiến Thức Với LLM

Bước đầu tiên là chuyển đổi các tài liệu không có cấu trúc của bạn thành một đồ thị kiến thức có cấu trúc. Đây là nơi sức mạnh của các LLM hiện đại như trích xuất dữ liệu có cấu trúc phát huy tác dụng [5] [6].

1.  **Thiết Lập Cơ Sở Dữ Liệu Đồ Thị**: Trước tiên, bạn cần một cơ sở dữ liệu đồ thị đang chạy. Neo4j là một lựa chọn phổ biến và tích hợp tốt với LangChain. Bạn có thể thiết lập một phiên bản miễn phí trên [Neo4j Aura](https://neo4j.com/cloud/aura-db/) hoặc chạy nó cục bộ thông qua Docker [5] [6].

2.  **Sử Dụng LLM Để Trích Xuất Đồ Thị**: `LLMGraphTransformer` trong LangChain là một công cụ mạnh mẽ cho việc này. Bạn cấp cho nó các tài liệu, và nó sử dụng LLM để tự động trích xuất các thực thể (nút) và mối quan hệ (cạnh) và cấu trúc chúng dưới dạng tài liệu đồ thị [5] [6].

    ```python
    # Ví dụ sử dụng LangChain và Neo4j
    import os
    from langchain_experimental.graph_transformers.llm import LLMGraphTransformer
    from langchain_openai import ChatOpenAI
    from langchain_core.documents import Document
    from langchain_community.graphs import Neo4jGraph

    # --- Kết Nối Đến Neo4j --- #
    url = "neo4j+s://your-aura-db-id.databases.neo4j.io"
    username = "neo4j"
    password = "your-password"
    graph = Neo4jGraph(url=url, username=username, password=password)

    # --- LLM Để Trích Xuất --- #
    # Sử dụng một mô hình mạnh mẽ để có kết quả trích xuất tốt hơn
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    # --- Công Cụ Biến Đổi --- #
    # Bạn có thể tùy chọn chỉ định các nút và mối quan hệ được phép để hướng dẫn LLM
    llm_transformer = LLMGraphTransformer(llm=llm)

    # --- Xử Lý Tài Liệu --- #
    # Giả sử 'documents' là một danh sách các đối tượng Document của LangChain
    documents = [Document(page_content="Marie Curie, một nhà vật lý và nhà hóa học, là một người tiên phong trong nghiên cứu phóng xạ. Cô ấy hợp tác với chồng của mình, Pierre Curie.")]

    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    # --- Nhập Vào Neo4j --- #
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True, # Điều này giúp sắp xếp đồ thị
        include_source=True
    )
    ```

Quá trình này điền vào cơ sở dữ liệu Neo4j của bạn với các nút và mối quan hệ ẩn trong văn bản của bạn, tạo nền tảng có cấu trúc cho hệ thống Graph RAG của bạn [5] [6].

#### 6.2.2. Giai Đoạn Trực Tuyến: Truy Vấn Đồ Thị

Với đồ thị được xây dựng, bạn có thể bây giờ truy vấn nó tại thời gian suy luận. Sức mạnh của Graph RAG nằm trong khả năng kết hợp tìm kiếm ngữ nghĩa với duyệt đồ thị có cấu trúc [5] [6].

**Ngôn Ngữ Tự Nhiên Đến Cypher Với `GraphCypherQAChain`**

Đối với các câu hỏi yêu cầu duyệt đồ thị và hiểu cấu trúc của nó, bạn có thể sử dụng một chuỗi tự động dịch câu hỏi ngôn ngữ tự nhiên của người dùng thành truy vấn Cypher (ngôn ngữ truy vấn của Neo4j) [5] [6].

```python
# Ví dụ sử dụng GraphCypherQAChain của LangChain
from langchain.chains import GraphCypherQAChain

# Chuỗi sẽ sử dụng LLM để viết truy vấn Cypher, thực hiện nó và tổng hợp câu trả lời
chain = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=ChatOpenAI(model="gpt-4-turbo", temperature=0),
    verbose=True # Đặt thành True để xem truy vấn Cypher được tạo
)

# Hỏi một câu hỏi yêu cầu suy luận trên cấu trúc đồ thị
result = chain.invoke({"query": "Marie Curie đã hợp tác với ai?"})
print(result["result"])

# Đầu ra dự kiến sẽ hiển thị truy vấn Cypher được tạo:
# MATCH (p1:Person {id: 'Marie Curie'})-[:COLLABORATED_WITH]->(p2:Person) RETURN p2.id
# Và câu trả lời cuối cùng: "Marie Curie đã hợp tác với Pierre Curie."
```

Chuỗi này trừu tượng hóa sự phức tạp của việc viết các truy vấn đồ thị, cho phép bạn có một giao diện ngôn ngữ tự nhiên cho đồ thị kiến thức của bạn. Nó hiệu quả thực hiện suy luận nhiều bước mà các hệ thống RAG tiêu chuẩn không thể [5] [6].

**Kết Hợp Với Tìm Kiếm Vectơ**

Đối với một hệ thống Graph RAG hoàn chỉnh, bạn thường sẽ kết hợp các truy vấn có cấu trúc này với tìm kiếm ngữ nghĩa trên các thuộc tính nút. Điều này cho phép bạn xử lý cả các câu hỏi cụ thể, thực tế (tốt nhất cho duyệt đồ thị) và các truy vấn rộng hơn, ngữ nghĩa hơn (tốt nhất cho tìm kiếm vectơ) [5] [6]. Một mô hình phổ biến là trước tiên thực hiện tìm kiếm vectơ để tìm các nút "hạt giống" liên quan nhất và sau đó sử dụng các nút đó làm điểm bắt đầu cho một truy vấn Cypher khám phá khu vực lân cận cục bộ của chúng trong đồ thị.

### 6.3. Nhiệm Vụ Quan Trọng Của Đánh Giá: Số Liệu và Framework

Xây dựng một hệ thống RAG là một quá trình lặp lại. Mà không có đánh giá mạnh mẽ, không thể biết liệu những thay đổi của bạn có cải thiện hệ thống hay làm cho nó tệ hơn hay không [11]. Chuyển từ "kiểm tra vibe" chủ quan sang một vòng lặp đánh giá có hệ thống, dựa trên số liệu là dấu hiệu của một thực hành kỹ sư AI chuyên nghiệp [11].

Tuy nhiên, đánh giá các hệ thống RAG là khó khăn nổi tiếng vì sự tương tác phức tạp giữa truy xuất và trình tạo. Một khung đánh giá toàn diện phải đánh giá hệ thống từ nhiều góc độ, phân chia vấn đề thành các thành phần cốt lõi của đường ống RAG [11].

#### 6.3.1. Bộ Ba RAG: Một Khung Khái Niệm Để Đánh Giá

Quá trình đánh giá RAG có thể được tổ chức khái niệm xung quanh ba mối quan hệ chính, thường được gọi là **Bộ Ba RAG** [11]:

1.  **Truy Vấn ↔ Bối Cảnh Được Truy Xuất**: Trục này đánh giá hiệu suất của **truy xuất**. Các câu hỏi cốt lõi ở đây là: Thông tin được truy xuất có liên quan đến truy vấn không? Nó có đủ để trả lời truy vấn không? Nó ngắn gọn, hay có quá nhiều tiếng ồn? [11]

2.  **Bối Cảnh Được Truy Xuất ↔ Câu Trả Lời Được Tạo**: Trục này đánh giá **tính trung thực** của **trình tạo**. Câu hỏi chính là: Câu trả lời được tạo có được neo chắc chắn về mặt thực tế trong bối cảnh được cung cấp không? Hệ thống phải không ảo giác hoặc phát minh ra thông tin không được hỗ trợ bởi các tài liệu được truy xuất [11].

3.  **Truy Vấn ↔ Câu Trả Lời Được Tạo**: Điều này đánh giá chất lượng từ đầu đến cuối của hệ thống từ quan điểm của người dùng. Câu hỏi chính là: Câu trả lời cuối cùng có thỏa mãn truy vấn của người dùng không? Điều này đánh giá mức độ liên quan và tính chính xác tổng thể của đầu ra [11].

#### 6.3.2. Các Số Liệu Đánh Giá Chính

Dựa trên Bộ Ba RAG, chúng tôi có thể xác định một tập hợp các số liệu cốt lõi để đo lường hiệu suất một cách định lượng. Những số liệu này có thể được phân loại rộng rãi thành các số liệu cấp thành phần (truy xuất/trình tạo) và các số liệu từ đầu đến cuối [11].

**Số Liệu Đánh Giá Truy Xuất:**

Những số liệu này đánh giá chất lượng của các tài liệu được trả về bởi hệ thống truy xuất [11].

*   **Độ Chính Xác Bối Cảnh**: Điều này đo lường tỷ lệ tín hiệu trên tiếng ồn. Trong số các tài liệu được truy xuất, bao nhiêu tài liệu thực sự liên quan? Điểm số độ chính xác thấp cho biết rằng truy xuất đang kéo vào rất nhiều thông tin không liên quan, điều này có thể làm nhầm lẫn trình tạo [11].

*   **Độ Nhớ Lại Bối Cảnh**: Điều này đo lường khả năng của truy xuất để tìm tất cả thông tin cần thiết. Các tài liệu được truy xuất có chứa tất cả thông tin cần thiết để trả lời câu hỏi không? Độ nhớ lại thấp là nguyên nhân phổ biến của các câu trả lời không hoàn chỉnh hoặc không chính xác [11].

**Số Liệu Đánh Giá Trình Tạo và Từ Đầu Đến Cuối:**

Những số liệu này đánh giá câu trả lời được tạo cuối cùng [11].

*   **Tính Trung Thực**: Đây có lẽ là số liệu RAG quan trọng nhất. Nó đo lường mức độ nhất quán về mặt thực tế của câu trả lời được tạo với bối cảnh được truy xuất. Điểm số tính trung thực cao có nghĩa là mô hình không tạo ra những thứ. Nó thường được đo bằng cách nhắc LLM khác để kiểm tra tính nhất quán thực tế [11].

*   **Mức Độ Liên Quan Của Câu Trả Lời**: Số liệu này đo lường mức độ liên quan của câu trả lời được tạo với truy vấn của người dùng. Có thể câu trả lời trung thực với bối cảnh nhưng không thực sự giải quyết câu hỏi của người dùng. Số liệu này giúp bắt các trường hợp như vậy [11].

*   **Tính Chính Xác Của Câu Trả Lời**: Điều này đo lường tính chính xác thực tế của câu trả lời được tạo so với một câu trả lời cơ sở sự thật. Đây là một số liệu mạnh mẽ nhưng yêu cầu một tập dữ liệu được quản lý với các câu trả lời đúng đã biết, điều này có thể tốn kém để tạo [11].

#### 6.3.3. RAGAS: Một Framework Để Đánh Giá Tự Động

Tính toán các số liệu này theo cách thủ công là tẻ nhạt và không có khả năng mở rộng. Đây là nơi các framework đánh giá tự động như **RAGAS** (Retrieval Augmented Generation Assessment) trở nên không thể thiếu [11]. RAGAS là một thư viện Python mã nguồn mở cung cấp một bộ công cụ để đánh giá các đường ống RAG bằng cách sử dụng các số liệu được mô tả ở trên [11].

Lợi thế chính của RAGAS là nó tận dụng các LLM để thực hiện đánh giá, cho phép một đánh giá tinh tế, không có tham chiếu. Ví dụ, để đo lường tính trung thực, RAGAS sẽ lấy câu trả lời được tạo và bối cảnh, và nhắc LLM khác để kiểm tra tính nhất quán thực tế [11]. Điều này cho phép đánh giá liên tục, tự động trong quá trình phát triển.

```python
# Ví dụ khái niệm về sử dụng RAGAS để đánh giá
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from datasets import Dataset

# Giả sử 'data_samples' là một từ điển với các câu hỏi, câu trả lời, bối cảnh, v.v. của bạn
dataset = Dataset.from_dict(data_samples)

# Chạy đánh giá
result = evaluate(
    dataset = dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)

df = result.to_pandas()
print(df)
```

Bằng cách tích hợp một framework như RAGAS vào quy trình phát triển, các kỹ sư có thể chuyển từ đoán mò sang một phương pháp dựa trên dữ liệu, lặp lại và cải thiện các hệ thống RAG của họ một cách có hệ thống dựa trên phản hồi định lượng [11].

## 7. Kết Luận: Con Đường Từ Truy Xuất Đến Suy Luận

Hành trình của Retrieval-Augmented Generation, từ những khởi đầu đơn giản của nó đến các kiến trúc tinh vi, lấy cảm hứng từ sinh học thần kinh ngày nay, là một bằng chứng cho tốc độ nhanh chóng và không ngừng của đổi mới trong lĩnh vực AI [9] [10]. Chúng tôi đã truy vết sự tiến hóa này thông qua ba mô hình chính:

1.  **Naive RAG**, thiết lập bản thiết kế "retrieve-read" cơ bản, cung cấp một cách đơn giản nhưng hiệu quả để neo các LLM vào kiến thức bên ngoài [1] [3].

2.  **Advanced RAG**, giới thiệu các lớp tối ưu hóa quan trọng, chẳng hạn như chunking thông minh, biến đổi truy vấn và xếp hạng lại, để cải thiện đáng kể độ chính xác và chất lượng của quá trình truy xuất [3] [4].

3.  **Modular và Graph RAG**, đại diện cho trạng thái hiện đại nhất. Mô hình này vượt ra ngoài việc truy xuất các chunk văn bản cô lập để suy luận trên kiến thức liên kết, có cấu trúc. Bằng cách tận dụng các đồ thị kiến thức, những hệ thống này có thể thực hiện loại suy luận nhiều bước, liên kết mà là đặc trưng của các phương pháp dựa trên đồ thị [5] [6] [7] [8].

Trong bối cảnh Graph RAG, **gia đình HippoRAG** nổi bật. Bằng cách rút ra cảm hứng trực tiếp từ cấu trúc của bộ nhớ con người, đặc biệt là vai trò của hồi hộp, HippoRAG 2 đã thể hiện một khả năng độc đáo để xuất sắc trên tất cả các kích thước quan trọng của một hệ thống bộ nhớ nhân tạo [10]. Các kết quả điểm chuẩn của nó cho thấy rằng nó không chỉ đạt được hiệu suất tiên tiến nhất trong các nhiệm vụ suy luận liên kết phức tạp là đặc trưng của các phương pháp dựa trên đồ thị mà còn làm như vậy mà không hy sinh hiệu suất trên các nhiệm vụ nhớ lại thực tế cơ bản và hiểu rõ ý nghĩa mà các Graph RAG trước đó đã gặp khó khăn [10]. Điều này làm cho HippoRAG 2 trở thành một khung công việc thực sự toàn diện và mạnh mẽ, đẩy ranh giới của những gì có thể được thực hiện với tăng cường kiến thức không tham số cho LLMs [10].

Đối với kỹ sư AI, sự tiến hóa này cung cấp một lộ trình rõ ràng. Mặc dù Naive RAG là một điểm khởi đầu tuyệt vời, xây dựng các hệ thống cấp sản xuất yêu cầu chấp nhận các kỹ thuật của Advanced RAG và, đối với các ứng dụng yêu cầu suy luận sâu, liều mạo vào thế giới của Graph RAG [3] [4] [5] [6]. Tính khả dụng của các framework mã nguồn mở mạnh mẽ như LangChain, LlamaIndex và RAGAS đã dân chủ hóa khả năng xây dựng và, quan trọng nhất, đánh giá những hệ thống phức tạp này, cho phép một quy trình kỹ sư dựa trên dữ liệu và chuyên nghiệp [3] [11].

### 7.1. Các Hướng Đi Tương Lai

Lĩnh vực RAG vẫn còn xa từ tĩnh. Một số hướng nghiên cứu thú vị hứa hẹn sẽ đẩy khả năng của những hệ thống này thậm chí còn xa hơn:

*   **Xây Dựng và Bảo Trì Đồ Thị Tự Động**: Mặc dù các công cụ để xây dựng KG đã cải thiện, quá trình vẫn còn phức tạp. Công việc tương lai có khả năng sẽ tập trung vào việc tạo ra các hệ thống tự chủ hơn có thể xây dựng, tinh chỉnh và cập nhật động các đồ thị kiến thức từ nhiều nguồn dữ liệu với sự can thiệp con người tối thiểu [5] [6].

*   **Tích Hợp Sâu Hơn Của Suy Luận và Truy Xuất**: Ranh giới giữa truy xuất và suy luận sẽ tiếp tục mờ đi. Chúng tôi có thể mong đợi thấy nhiều hệ thống hơn, như KG-RAG's "Chain of Explorations", nơi LLM là một người tham gia tích cực trong quá trình truy xuất, hướng dẫn tìm kiếm thông qua một không gian thông tin phức tạp [8].

*   **RAG Đa Phương Tiện**: Các nguyên tắc của RAG không bị giới hạn ở văn bản. Các hệ thống tương lai sẽ ngày càng kết hợp thông tin đa phương tiện, xây dựng các đồ thị kiến thức liên kết văn bản, hình ảnh và các loại dữ liệu khác, cho phép các truy vấn và suy luận trên các phương thức khác nhau [5] [6].

*   **Học Tập Liên Tục và Động Lực Bộ Nhớ**: Như HippoRAG 2 gợi ý, mục tiêu cuối cùng là một hệ thống bắt chước các khả năng học tập liên tục của bộ nhớ con người. Điều này bao gồm không chỉ thêm thông tin mới mà còn tăng cường, suy yếu và thậm chí quên thông tin dựa trên việc sử dụng và phản hồi, dẫn đến một hệ thống kiến thức thực sự động và thích ứng [9] [10].

Con đường từ truy xuất đơn giản đến suy luận thực sự đang tiến hành tốt. Khi những công nghệ này trưởng thành, chúng sẽ mở khóa một thế hệ ứng dụng AI mới không chỉ có kiến thức và chính xác hơn mà còn có khả năng hiểu thế giới phức tạp, liên kết mà chúng ta sống [9] [10].

## 8. Tài Liệu Tham Khảo

[1] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Nogueira, R., ... & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive nlp tasks. *Advances in Neural Information Processing Systems, 33*, 9459-9474. [https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)

[2] Prompt Engineering Guide. (2024). *Retrieval Augmented Generation (RAG) for LLMs*. [https://www.promptingguide.ai/research/rag](https://www.promptingguide.ai/research/rag)

[3] Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., ... & Wang, H. (2023). Retrieval-augmented generation for large language models: A survey. *arXiv preprint arXiv:2312.10997*. [https://arxiv.org/abs/2312.10997](https://arxiv.org/abs/2312.10997)

[4] Jain, M. (2024). *2024 was mostly about RAG. The Survey*. Medium. [https://medium.com/@j13mehul/2024-was-mostly-about-rag-c744bd0a2654](https://medium.com/@j13mehul/2024-was-mostly-about-rag-c744bd0a2654)

[5] Neo4j. (2023). *GraphRAG: Knowledge Graph-Based RAG*. [https://neo4j.com/developer/genai/graph-rag/](https://neo4j.com/developer/genai/graph-rag/)

[6] Zilliz. (2024). *GraphRAG Explained: Enhancing RAG with Knowledge Graphs*. [https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1](https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1)

[7] Hu, Z., et al. (2024). GRAG: Graph Retrieval-Augmented Generation. *arXiv preprint arXiv:2405.16506*. [https://arxiv.org/abs/2405.16506](https://arxiv.org/abs/2405.16506)

[8] Sanmartin, R. (2024). KG-RAG: A Pipeline for Bridging the Gap Between Knowledge and Creativity. *arXiv preprint arXiv:2405.12035*. [https://arxiv.org/abs/2405.12035](https://arxiv.org/abs/2405.12035)

[9] Gutiérrez, B. J., et al. (2024). HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. *arXiv preprint arXiv:2405.17543*. [https://arxiv.org/abs/2405.17543](https://arxiv.org/abs/2405.17543)

[10] Gutiérrez, B. J., Shu, Y., Qi, W., Zhou, S., & Su, Y. (2025). From RAG to Memory: Non-Parametric Continual Learning for Large Language Models. *arXiv preprint arXiv:2502.14802*. [https://arxiv.org/abs/2502.14802](https://arxiv.org/abs/2502.14802)

[11] Es, S., et al. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. *arXiv preprint arXiv:2309.15217*. [https://arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217)
