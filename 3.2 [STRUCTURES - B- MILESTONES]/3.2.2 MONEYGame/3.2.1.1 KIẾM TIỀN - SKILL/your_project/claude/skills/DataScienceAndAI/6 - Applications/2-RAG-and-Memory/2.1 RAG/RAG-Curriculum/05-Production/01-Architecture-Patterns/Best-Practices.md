# Production RAG Architecture: Folder Structure & Design Patterns

## Tổng Quan

Production RAG systems cần clean architecture. Không phải `script.py` - cần module structure, clear separation of concerns, API design patterns.

Bài học này dạy cách organize code như một team.

## Recommended Folder Structure

```
my-rag-system/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── config/
│   ├── settings.yaml          # Env config (models, APIs, thresholds)
│   ├── prompts.yaml           # All prompt templates
│   └── logging.yaml           # Logging configuration
│
├── src/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── document_loader.py # Load PDFs, web pages, etc
│   │   ├── splitter.py        # Chunk documents
│   │   └── indexer.py         # Embed & index into vector DB
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── retriever.py       # Vector + BM25 hybrid search
│   │   ├── reranker.py        # Reranking logic
│   │   └── query_processor.py # Query rewriting, expansion
│   │
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── llm_client.py      # LLM API calls (vLLM, OpenAI)
│   │   └── response_builder.py # Format output, citations
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── ragas_evaluator.py # RAGAS metrics
│   │   └── tracing.py         # Langfuse integration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging utilities
│       ├── cache.py           # Redis caching
│       └── errors.py          # Custom exceptions
│
├── tests/
│   ├── __init__.py
│   ├── test_retrieval.py
│   ├── test_generation.py
│   └── test_e2e.py            # End-to-end tests
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_embedding_comparison.ipynb
│   └── 03_evaluation.ipynb
│
└── scripts/
    ├── build_index.py         # One-time indexing script
    ├── evaluate.py            # Run RAGAS evaluation
    └── deploy.sh              # Deployment script
```

## Module 1: Ingestion Pipeline

```python
# src/ingestion/document_loader.py
from pathlib import Path
from llama_index import SimpleDirectoryReader, Document

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def load_documents(self) -> List[Document]:
        """Load documents from various sources"""
        loader = SimpleDirectoryReader(str(self.data_dir))
        documents = loader.load_data()
        return documents

    def load_from_urls(self, urls: List[str]) -> List[Document]:
        """Load from web URLs"""
        from llama_index.readers.web import SimpleWebPageReader
        loader = SimpleWebPageReader()
        documents = loader.load_data(urls)
        return documents

# src/ingestion/splitter.py
from llama_index.text_splitter import SentenceSplitter

class DocumentSplitter:
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 20):
        self.splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        chunks = []
        for doc in documents:
            split_docs = self.splitter.split_text(doc.text)
            for text in split_docs:
                chunks.append(Document(text=text, metadata=doc.metadata))
        return chunks

# src/ingestion/indexer.py
from llama_index import VectorStoreIndex, Document
from weaviate import Client

class DocumentIndexer:
    def __init__(self, vector_db_host: str = "http://localhost:8080"):
        self.client = Client(vector_db_host)

    def index_documents(self, documents: List[Document]) -> str:
        """Create vector index from documents"""
        index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True
        )
        return index.storage_context

# src/ingestion/__init__.py - Export public API
from .document_loader import DocumentLoader
from .splitter import DocumentSplitter
from .indexer import DocumentIndexer

__all__ = ["DocumentLoader", "DocumentSplitter", "DocumentIndexer"]
```

## Module 2: Retrieval Pipeline

```python
# src/retrieval/retriever.py
from typing import List
from llama_index import VectorStoreIndex

class HybridRetriever:
    def __init__(self, vector_index: VectorStoreIndex, bm25_index=None):
        self.vector_index = vector_index
        self.bm25_index = bm25_index

    def retrieve(self, query: str, top_k: int = 10, alpha: float = 0.7):
        """Hybrid search: vector + BM25"""
        # This is simplified - use actual hybrid logic
        vector_results = self.vector_index.as_retriever(
            similarity_top_k=top_k
        ).retrieve(query)

        # Optionally combine with BM25
        if self.bm25_index:
            bm25_results = self.bm25_index.retrieve(query, top_k)
            # Combine using RRF or other fusion method
            combined = self._fuse_results(vector_results, bm25_results)
            return combined

        return vector_results

    def _fuse_results(self, vector_results, bm25_results):
        """Reciprocal Rank Fusion"""
        # Simplified RRF
        scores = {}
        for i, result in enumerate(vector_results):
            scores[result.id] = scores.get(result.id, 0) + 1/(i+1)
        for i, result in enumerate(bm25_results):
            scores[result.id] = scores.get(result.id, 0) + 1/(i+1)

        sorted_results = sorted(scores.items(), key=lambda x: -x[1])
        return sorted_results

# src/retrieval/reranker.py
from cohere import Client as CohereClient

class Reranker:
    def __init__(self, api_key: str):
        self.client = CohereClient(api_key=api_key)

    def rerank(self, query: str, documents: List[str], top_k: int = 10):
        """Rerank documents using Cohere"""
        results = self.client.rerank(
            query=query,
            documents=documents,
            model="rerank-4-turbo",
            top_n=top_k
        )
        return results

# src/retrieval/query_processor.py
class QueryProcessor:
    def __init__(self, llm):
        self.llm = llm

    def rewrite_query(self, query: str, num_rewrites: int = 3) -> List[str]:
        """Generate query variations"""
        prompt = f"""Generate {num_rewrites} variations of this search query:
"{query}"

Return only the queries, one per line."""

        response = self.llm.complete(prompt)
        queries = [q.strip() for q in response.text.split('\n') if q.strip()]
        return queries
```

## Module 3: Generation Pipeline

```python
# src/generation/llm_client.py
from typing import Optional

class LLMClient:
    def __init__(self, model: str, base_url: Optional[str] = None):
        self.model = model

        if base_url:  # Self-hosted vLLM
            from openai import OpenAI
            self.client = OpenAI(base_url=base_url, api_key="token")
        else:  # OpenAI API
            from openai import OpenAI
            self.client = OpenAI()

    def complete(self, prompt: str, temperature: float = 0.3) -> str:
        """Generate response"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=500
        )
        return response.choices[0].message.content

    def stream(self, prompt: str, temperature: float = 0.3):
        """Stream response"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

# src/generation/response_builder.py
class ResponseBuilder:
    def __init__(self, prompt_template_path: str):
        import yaml
        with open(prompt_template_path) as f:
            self.templates = yaml.safe_load(f)

    def build_rag_prompt(self, question: str, contexts: List[str]) -> str:
        """Build RAG prompt from template"""
        template = self.templates["rag_prompt"]

        context_text = "\n".join([f"- {c}" for c in contexts])
        prompt = template.format(context=context_text, question=question)
        return prompt

    def build_response(self, answer: str, sources: List[str]) -> dict:
        """Format final response"""
        return {
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.now().isoformat()
        }
```

## Module 4: API Design

```python
# src/main.py - FastAPI application
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json

app = FastAPI(title="RAG System", version="1.0")

from src.retrieval import HybridRetriever, Reranker
from src.generation import LLMClient, ResponseBuilder

# Initialize
retriever = HybridRetriever(...)
reranker = Reranker(...)
llm = LLMClient(model="gpt-4")
response_builder = ResponseBuilder("config/prompts.yaml")

# Request/Response models
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    latency_ms: float

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Synchronous query endpoint"""
    import time
    start = time.time()

    # Retrieve
    documents = retriever.retrieve(request.query, top_k=request.top_k)

    # Rerank
    reranked = reranker.rerank(
        request.query,
        [d.text for d in documents],
        top_k=5
    )

    # Generate
    contexts = [d.text for d in documents[:5]]
    prompt = response_builder.build_rag_prompt(request.query, contexts)
    answer = llm.complete(prompt)

    latency_ms = (time.time() - start) * 1000

    return QueryResponse(
        answer=answer,
        sources=[d.metadata.get("source", "unknown") for d in documents[:5]],
        latency_ms=latency_ms
    )

@app.post("/query-stream")
async def query_stream(request: QueryRequest):
    """Streaming endpoint"""
    documents = retriever.retrieve(request.query, top_k=request.top_k)
    contexts = [d.text for d in documents[:5]]
    prompt = response_builder.build_rag_prompt(request.query, contexts)

    async def generate():
        for token in llm.stream(prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}
```

## Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY src/ ./src
COPY config/ ./config

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Vector Database
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # LLM Server (vLLM)
  vllm:
    build:
      context: .
      dockerfile: Dockerfile.vllm
    environment:
      - CUDA_VISIBLE_DEVICES=0
    ports:
      - "8001:8000"

  # RAG Application
  rag-app:
    build: .
    environment:
      - VECTOR_DB_URL=http://weaviate:8080
      - REDIS_URL=redis://redis:6379
      - LLM_BASE_URL=http://vllm:8000
    ports:
      - "8000:8000"
    depends_on:
      - weaviate
      - redis
      - vllm
```

## Configuration Management

```yaml
# config/settings.yaml
ingestion:
  chunk_size: 1024
  chunk_overlap: 20
  batch_size: 32

retrieval:
  top_k: 10
  hybrid_alpha: 0.7
  embedding_model: "text-embedding-3-large"

reranking:
  enabled: true
  model: "cohere-rerank-4"
  top_k: 5

generation:
  model: "gpt-4"
  temperature: 0.3
  max_tokens: 500

evaluation:
  ragas_sample_size: 100
  schedule: "weekly"

logging:
  level: "INFO"
  langfuse_enabled: true
```

## Key Takeaway

Production RAG requires **modular, well-organized code**:

1. **Separation of Concerns:** Ingestion, retrieval, generation are separate modules
2. **Config-Driven:** Settings in YAML, not hardcoded
3. **API Design:** FastAPI with clear request/response models
4. **Docker:** Containerized, reproducible deployment
5. **Monitoring:** Health checks, error handling

**Time investment:** 2-3 days to set up properly.
**Payoff:** Easy to test, scale, update, and debug.

Never compromise on architecture - it pays dividends.
