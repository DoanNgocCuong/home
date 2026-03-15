# RAG Architecture: Kiến trúc chi tiết 3 pha

## Tổng quan hệ thống

RAG hoạt động như một lò xo: Offline phase "nén" dữ liệu thành vectors, Online phase "giải phóng" chúng khi cần.

```
┌──────────────────────────────────────────────────────────────────┐
│ DATA SOURCES (Raw Documents)                                     │
│ PDFs, HTML, DOCX, JSON, Database, Real-time Streams             │
└────────────────────┬─────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ PHASE 1: OFFLINE INGESTION (Setup once, update periodically)  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│  │   Document   │──→   │   Chunking   │──→   │  Embedding   │   │
│  │   Parsing    │      │  Strategy    │      │    Model     │   │
│  └──────────────┘      └──────────────┘      └──────────────┘   │
│                                                     ↓             │
│                                          ┌──────────────────┐    │
│                                          │  Vector Database │    │
│                                          │  (Qdrant/Milvus)│    │
│                                          └──────────────────┘    │
│                                                     ↑             │
│  ┌──────────────┐      ┌──────────────┐                         │
│  │   Metadata   │──→   │  Enrichment  │─────────────────────→   │
│  │ Extraction   │      │  (NER, Tags) │                         │
│  └──────────────┘      └──────────────┘                         │
│                                                                   │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                      Knowledge Base Ready
                            ↓

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ PHASE 2: ONLINE RETRIEVAL (Real-time per query)               ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
│                                                                   │
│  User Query                                                      │
│      ↓                                                           │
│  ┌─────────────────────┐                                         │
│  │  Query Encoding     │ (Convert query to embedding vector)    │
│  │  Embedding Model    │                                        │
│  └──────────┬──────────┘                                         │
│             ↓                                                    │
│  ┌──────────────────────┐                                        │
│  │  Vector Search       │ (Find K nearest vectors)              │
│  │  (Similarity Score)  │                                        │
│  └──────────┬──────────┘                                         │
│             ↓                                                    │
│  ┌──────────────────────┐                                        │
│  │  Retrieve Chunks     │ (Get documents + metadata)            │
│  │  + Metadata Filtering│ (Filter by date, category, etc)      │
│  └──────────┬──────────┘                                         │
│             ↓                                                    │
│  ┌──────────────────────┐                                        │
│  │  Context Builder     │ (Format for LLM prompt)              │
│  │  (Re-ranking, etc)   │                                        │
│  └──────────┬──────────┘                                         │
│             ↓                                                    │
│  ┌──────────────────────┐      ┌──────────────┐                │
│  │  LLM Prompt          │ ──→  │   LLM        │                │
│  │  Query + Context     │      │  (Generate)  │                │
│  └──────────────────────┘      └──────┬───────┘                │
│                                       ↓                          │
│                                  Final Answer                    │
│                                       ↓                          │
│                                  User Response                   │
│                                                                   │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ PHASE 3: EVALUATION & OPTIMIZATION (Continuous improvement)  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
│                                                                   │
│  Metrics Collection:                                             │
│  • Retrieval: Precision@K, MRR, NDCG                            │
│  • Generation: ROUGE, BERTScore, LLM eval                       │
│  • User feedback: Thumbs up/down, ratings                       │
│                                                                   │
│  Optimize:                                                       │
│  • Adjust chunking strategy                                     │
│  • Change embedding model                                       │
│  • Tune retrieval parameters (K, threshold)                    │
│  • Update metadata extraction                                   │
│                                                                   │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Chi tiết từng component

### 1. Document Parser (Phân tích tài liệu)

**Nhiệm vụ**: Trích xuất text từ các format khác nhau

```
Input: PDF/HTML/DOCX/JSON
        ↓
     Parser
        ↓
Output: Structured text + metadata
```

**Các format thường gặp:**

- **PDF**: Multimodal (text + images) → Dùng PyMuPDF hoặc Unstructured
- **HTML**: Structure-aware parsing → Maintain heading hierarchy
- **DOCX**: Preserve formatting → Use python-docx

### 2. Chunking Strategy (Chia nhỏ documents)

**Tại sao cần chunking:**
- LLM có context window hạn chế
- Chunk nhỏ → tìm kiếm chính xác hơn
- Chunk lớn → context phong phú hơn

**Các chiến lược chính:**

```
Original Document
        ↓
    Chunking
        ↓
┌─────────┬─────────┬─────────┐
│ Chunk 1 │ Chunk 2 │ Chunk 3 │  (với overlap)
└─────────┴─────────┴─────────┘
        ↓
Vector Embedding
        ↓
Vector Database
```

**Thường dùng 512 tokens/chunk, overlap 20% → balanced accuracy**

### 3. Embedding Model (Vector hóa)

**Tại sao cần:**
- Vectors cho phép tìm kiếm similarity-based
- Semantic search thay vì keyword search
- Xử lý được synonyms, paraphrasing

```
Text Chunk
    ↓
Embedding Model (BGE-M3, Jina, OpenAI)
    ↓
Vector [0.23, -0.45, 0.67, ..., 0.12]  (dimension: 1024)
    ↓
Stored in Vector DB
```

**Tiêu chí chọn model:**
- MTEB score (semantic similarity)
- Language support (Vietnamese?)
- Dimension (1024 vs 768, trade-off cost/quality)
- Speed (tokens/second)

### 4. Vector Database (Lưu trữ vectors)

**Đặc điểm:**
- Indexing: HNSW, IVF, PQ (trade-off: speed vs accuracy)
- Query: Fast similarity search
- Metadata filtering: Filter while searching
- Scaling: Single-node hoặc distributed

```
Query Vector [0.23, -0.45, 0.67, ...]
        ↓
Index Search (HNSW/IVF)
        ↓
Top K Similar Vectors
        ↓
Retrieve Associated Data + Metadata
        ↓
Return to LLM
```

### 5. Metadata Enrichment (Bổ sung thông tin)

**Thêm thông tin hữu ích:**
- Named Entities (người, địa điểm, tổ chức)
- Keywords
- Summary
- Document type, date, source
- Category/tags

**Ưu điểm:**
- Metadata filtering tăng precision
- Traceability: "từ document nào"
- Context: LLM hiểu tài liệu tốt hơn

### 6. Retriever & Re-ranking (Truy xuất chính xác)

**Retriever:** Lấy top-K chunks từ vector DB
**Re-ranker:** Sắp xếp lại dựa trên relevance model

```
Vector DB → Top 20 chunks (fast, approximate)
        ↓
Re-ranker (slow, accurate)
        ↓
Top 5 chunks (best quality)
        ↓
LLM Prompt
```

**Benefit:** Balance speed vs quality

## Data Flow: Ví dụ thực tế

```
OFFLINE:
Report.pdf (5MB)
    → PyMuPDF Parser
    → 200 chunks (512 tokens)
    → BGE-M3 Embedding (1024-dim)
    → Qdrant Vector DB (indexed with HNSW)
    + Metadata: date, author, section, summary

ONLINE:
"Báo cáo nói gì về revenue Q4?"
    → BGE-M3 Embedding
    → Qdrant: Find 10 most similar chunks
    → Filter: date >= Q4 start
    → Re-rank: 5 best chunks
    → Prompt: "Context: [5 chunks]\nQuestion: ...\nAnswer:"
    → LLM generates answer
    → Return: answer + source references

EVAL:
Did answer match ground truth?
    → ROUGE score: 0.72
    → User feedback: thumbs up
    → Iterate: adjust chunking or embedding model
```

## Performance Considerations

**Latency Breakdown (typical):**
- Query embedding: 10-50ms
- Vector search: 5-20ms
- Re-ranking: 50-200ms
- LLM generation: 500-2000ms
- **Total: 600-2300ms (bị dominated by LLM)**

**Optimization:**
- Parallel search + re-rank
- Cache embeddings
- Batch queries
- Use faster LLM for re-ranking

---

## Key Takeaway

RAG architecture gồm ba pha rõ ràng: Offline xây dựng kiến thức (parse → chunk → embed → store), Online trích xuất (search → filter → rank → prompt → generate), Eval đảm bảo chất lượng (metrics → optimize → iterate). Mỗi component (parser, chunker, embedder, retriever, reranker, LLM) có thể được tối ưu độc lập. Học kiến trúc này sẽ giúp bạn debug khi hệ thống không hoạt động đúng.
