# RAG CURRICULUM — Full-Stack Production RAG

> **Giáo trình RAG** cho Challenge 30 Ngày — Fresher AI Engineer
>
> Tổ chức theo 3 pha chính của RAG Pipeline: **Offline → Online → Evaluation Loop**

---

## Folder Structure

```
RAG-Curriculum/
│
├── 00-Overview/                          # Tổng quan RAG & Architecture
│   ├── RAG-Overview.md                   # RAG là gì, tại sao cần RAG
│   ├── RAG-Architecture.md               # Kiến trúc 3 pha: Offline → Online → Eval
│   └── Framework-Comparison.md           # So sánh LlamaIndex vs LangChain vs Haystack
│
├── 01-Offline-Ingestion/                 # PHASE 1: Offline Pipeline
│   ├── 01-Document-Parsing/              # Parse PDF, HTML, DOCX → clean text
│   ├── 02-Chunking-Strategies/           # Recursive, Semantic, Late, Contextual
│   ├── 03-Embedding-Models/              # BGE-M3, Jina v3, OpenAI, Cohere
│   ├── 04-Vector-Database/               # Qdrant, Milvus, Chroma, Pinecone
│   └── 05-Metadata-Enrichment/           # NER, summaries, keywords
│
├── 02-Online-Query/                      # PHASE 2: Online Pipeline
│   ├── 01-Retrieval-Strategies/          # Hybrid search, HyDE, Multi-query
│   ├── 02-Reranking/                     # Cross-encoder, Cohere Rerank, BGE
│   ├── 03-Prompt-Engineering-RAG/        # Prompt template, context optimization
│   ├── 04-LLM-Serving/                   # vLLM, TGI, Ollama, SGLang
│   └── 05-Caching-Streaming/             # Prompt caching, semantic caching
│
├── 03-Evaluation-Loop/                   # PHASE 3: Evaluation & Continuous Improvement
│   ├── 01-RAGAS-Metrics/                 # Faithfulness, Relevancy, Precision, Recall
│   ├── 02-Observability-Tracing/         # Langfuse, LangSmith, Phoenix
│   ├── 03-AB-Testing/                    # Config comparison, gradual rollout
│   └── 04-Continuous-Improvement/        # Dataset curation, feedback loop
│
├── 04-Advanced-RAG/                      # Kiến trúc RAG nâng cao
│   ├── 01-GraphRAG/                      # Microsoft GraphRAG, Knowledge Graph
│   ├── 02-Agentic-RAG/                   # LLM-as-Agent, tool use, multi-step
│   ├── 03-Self-RAG-Corrective/           # Self-correction, hallucination check
│   ├── 04-Raptor-RAG/                    # Hierarchical retrieval
│   └── 05-LightRAG/                      # Graph + Vector hybrid
│
├── 05-Production/                        # Production-grade RAG
│   ├── 01-Architecture-Patterns/         # Folder structure, module separation
│   ├── 02-Performance-Optimization/      # Latency, throughput, connection pool
│   └── 03-Cost-Optimization/             # Token optimization, caching strategies
│
├── 06-Week2-Exercises/                   # BÀI TẬP TUẦN 2
│   ├── Exercise-2.1-RAG-End-to-End.md    # Bài 2.1: Build RAG Pipeline
│   └── Exercise-2.2-Evaluation-Loop.md   # Bài 2.2: Evaluation + Langfuse
│
└── 07-References/                        # Tài liệu tham khảo tổng hợp
    └── References.md
```

---

## Triết lý tổ chức

**Tại sao chia 3 pha?**

Mọi hệ thống RAG production đều vận hành theo 3 pha:

1. **Offline (Ingestion)** — Chạy khi có document mới: Parse → Chunk → Embed → Store
2. **Online (Query)** — Chạy mỗi khi user hỏi: Retrieve → Rerank → Generate → Response
3. **Evaluation Loop** — Chạy liên tục: Measure → Trace → Compare → Improve

Pha 1 và 2 là "build", pha 3 là "improve". Không có pha 3 thì RAG chỉ là prototype, không phải production.

---

## Tech Stack khuyến nghị (2025-2026)

| Component | Recommended | Alternative |
|-----------|------------|-------------|
| **Framework** | LlamaIndex (RAG-native) | Haystack (production), LangChain (orchestration) |
| **Embedding** | BGE-M3 (open-source) | Jina v3 (long doc), OpenAI text-3-large (quality) |
| **Vector DB** | Qdrant (self-host) | Milvus (scale), Chroma (prototype) |
| **Reranker** | BGE Reranker (open-source) | Cohere Rerank-4 (quality) |
| **LLM Serving** | vLLM + Qwen 2.5 | Ollama (local dev) |
| **Tracing** | Langfuse (open-source) | LangSmith (LangChain ecosystem) |
| **Evaluation** | RAGAS | Custom LLM-as-Judge |

---

## Liên kết với lộ trình 30 ngày

| Tuần | Focus | Bài tập |
|------|-------|---------|
| **Tuần 1** | Foundation | 1.1 Docker + FastAPI → 1.2 vLLM Hosting |
| **Tuần 2** | Application (RAG) | **2.1 RAG End-to-End → 2.2 Evaluation + Langfuse** |
| **Tuần 3** | Optimization | 3.1 Fine-tuning LoRA → 3.2 Continuous Training |
| **Tuần 4** | Production & Capstone | 4.1 Production Quality → 4.2 Capstone |
