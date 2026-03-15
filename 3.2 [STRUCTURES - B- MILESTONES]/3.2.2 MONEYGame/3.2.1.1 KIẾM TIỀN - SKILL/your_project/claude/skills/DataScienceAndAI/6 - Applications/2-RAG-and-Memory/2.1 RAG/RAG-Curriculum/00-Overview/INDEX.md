# RAG Phase 1: Offline/Ingestion Pipeline - Curriculum Index

## Overview Section (00-Overview/)

These foundational guides explain RAG concepts and compare different approaches.

### 1. RAG-Overview.md (6.1 KB)
**What you'll learn:**
- RAG definition and why it matters
- Three phases of RAG (Offline, Online, Eval)
- Comparison with fine-tuning, prompt engineering, and in-context learning
- When to use RAG vs alternatives
- Simple ASCII architecture diagram

**Key sections:**
- RAG là gì? (Definition)
- Tại sao RAG quan trọng? (Benefits)
- Ba pha chính (Three phases)
- So sánh RAG với các phương pháp khác (Comparison table)
- Khi nào sử dụng RAG (Decision guide)

---

### 2. RAG-Architecture.md (13 KB)
**What you'll learn:**
- Detailed 3-phase architecture with data flow diagrams
- Component explanation (Parser, Chunker, Embedder, Vector DB, Retriever, LLM)
- How components connect and communicate
- Performance breakdown (latency analysis)

**Key sections:**
- Tổng quan hệ thống (System overview with ASCII diagrams)
- Chi tiết từng component (Component deep-dive)
- Data flow: Ví dụ thực tế (Real-world example)
- Performance Considerations (Latency breakdown)

---

### 3. Framework-Comparison.md (9.0 KB)
**What you'll learn:**
- Top 5 RAG frameworks 2025-2026 (LlamaIndex, LangChain, Haystack, RAGFlow, LightRAG)
- Philosophy and design patterns of each
- Strengths and weaknesses
- Token overhead and performance metrics
- Decision tree for choosing framework
- Real-world token usage comparison

**Key sections:**
- LlamaIndex (Data-focused)
- LangChain (Composable blocks)
- Haystack (Production pipelines)
- RAGFlow (No-code)
- LightRAG (Minimal, fast)
- Comparison table
- Decision tree
- Vietnamese RAG specific

---

## Offline Ingestion Section (01-Offline-Ingestion/)

These guides cover the 5 critical steps in building your knowledge base.

### 1. Document Parsing (01-Document-Parsing/Best-Practices.md - 8.2 KB)
**What you'll learn:**
- Parsing different document formats (PDF, HTML, DOCX)
- Tools: PyMuPDF, Unstructured, DeepDoc, Trafilatura, python-docx
- Structure-aware parsing
- Metadata extraction
- Common pitfalls and solutions
- Vietnamese encoding handling

**Key sections:**
- Document Parsing là gì? (Why it matters)
- Các format phổ biến (PDF, HTML, DOCX)
- Metadata Extraction
- Workflow: End-to-end
- Common Pitfalls
- Vietnamese-specific Issues

**Benchmark:** PyMuPDF 50p/s vs Unstructured 5p/s (trade-off quality vs speed)

---

### 2. Chunking Strategies (02-Chunking-Strategies/Best-Practices.md - 12 KB)
**What you'll learn:**
- 5 chunking strategies (Recursive, Semantic, Late Chunking, Contextual, Structure-Aware)
- Benchmark data from Vecta Feb 2026 (69-73% accuracy range)
- Trade-offs: chunk size, overlap, precision vs context
- Code examples for LlamaIndex and LangChain
- Decision tree for choosing strategy

**Key sections:**
- Tại sao chunking quan trọng
- Benchmark Data (Vecta Feb 2026)
- 5 Chunking Strategies with code
- Decision Tree
- Practical Tips (size, overlap, testing)
- Common Mistakes

**Recommendation:** Default Recursive 512 tokens with 20% overlap = 69% accuracy, fast

---

### 3. Embedding Models (03-Embedding-Models/Best-Practices.md - 11 KB)
**What you'll learn:**
- Top embedding models 2025-2026: BGE-M3, Jina v3, OpenAI text-embedding-3-large, Cohere embed-v4
- MTEB benchmark scores
- Self-hosted vs API deployment
- Language support (especially Vietnamese)
- Cost analysis
- Jina deployment guide

**Key sections:**
- Embedding models là gì
- Top 4 models with specs
- MTEB Comparison
- Decision Tree
- Deployment Options (self-hosted vs API)
- Vietnamese Embedding
- Performance Tuning

**Recommendation:** BGE-M3 for best all-rounder (multilingual, free, strong MTEB)

---

### 4. Vector Database (04-Vector-Database/Best-Practices.md - 13 KB)
**What you'll learn:**
- Top 5 vector databases: Qdrant, Milvus, Weaviate, Chroma, Pinecone
- Indexing algorithms: HNSW, IVF, PQ
- Self-hosted vs managed trade-offs
- Metadata filtering strategies
- Performance benchmarks
- Scaling considerations

**Key sections:**
- Vector DB là gì
- Top 5 databases with setup
- Comparison Table
- Indexing Deep Dive
- Decision Tree
- Self-hosted vs Managed

**Recommendation:** Qdrant for most (balanced features), Milvus for ultra-scale

---

### 5. Metadata Enrichment (05-Metadata-Enrichment/Best-Practices.md - 13 KB)
**What you'll learn:**
- Metadata extraction strategies: NER, summarization, keyword extraction, question generation
- Document type classification
- Why metadata matters for retrieval quality
- Complete enrichment pipeline
- Metadata-based filtering
- Performance optimization

**Key sections:**
- Metadata là gì
- 5 Enrichment Strategies (with code)
- Complete Enrichment Pipeline
- Metadata-based Filtering
- Performance Optimization
- When Metadata Matters Most

**Impact:** Enables 80% reduction in false positives with proper filtering

---

## Quick Reference Table

| Component | Default Choice | Alternative | Speed | Quality |
|-----------|---|---|---|---|
| **Parser** | PyMuPDF (simple) | Unstructured (complex) | Fast | Medium-High |
| **Chunker** | Recursive 512 | Semantic | Fast | High |
| **Embedder** | BGE-M3 | OpenAI text-3-large | Slow | Excellent |
| **Vector DB** | Qdrant | Milvus (big) | Medium | High |
| **Metadata** | NER + Keywords | All 5 strategies | Medium | High |

---

## Learning Path

1. **Start here**: RAG-Overview.md (10 min read)
2. **Understand architecture**: RAG-Architecture.md (15 min)
3. **Pick framework**: Framework-Comparison.md (10 min)
4. **Then dive deep into each component**:
   - Document Parsing (10 min)
   - Chunking Strategies (15 min) ⭐ Most important
   - Embedding Models (10 min)
   - Vector Database (15 min)
   - Metadata Enrichment (10 min)

**Total time**: ~1-2 hours reading
**Hands-on**: Build a simple RAG pipeline with your own documents

---

## Key Metrics to Remember

- **Chunking**: 512 tokens, 20% overlap = baseline (69% accuracy)
- **Semantic chunking**: +2% accuracy gain (71%)
- **Vector DB latency**: 5-50ms for search
- **Total query latency**: 600-2300ms (dominated by LLM)
- **Cost per 100K documents**: $1-25/month depending on choices

---

## Vietnamese Focus

All files include Vietnamese language support guidance:
- BGE-M3: 100+ languages including Vietnamese ✓
- UTF-8 encoding throughout ✓
- NER with Vietnamese models ✓
- Document parsing with Vietnamese examples ✓

---

## Next Steps (Not in Phase 1)

After mastering Phase 1 (Offline Ingestion), Phase 2 (Online Retrieval) covers:
- Real-time query embedding
- Vector search optimization
- Re-ranking strategies
- LLM prompt engineering
- Response streaming and caching

Phase 3 (Evaluation) covers:
- RAGAS metrics
- A/B testing
- Continuous improvement loops
- Observability and tracing
