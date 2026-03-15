# Observability & Tracing cho RAG Systems

## Tổng Quan

Tracing là "X-ray" cho RAG pipelines. Mỗi request đi qua retrieval → reranking → generation. Bạn cần biết chuyện gì xảy ra ở mỗi bước.

**Langfuse** (open-source, tự host được) là **recommended choice** năm 2026.

## Why Observability Matters

```
Production RAG System:
User Query
    ↓
Retrieval [latency: 150ms, docs: 10]
    ↓
Reranking [latency: 200ms, top_score: 0.92]
    ↓
Generation [latency: 500ms, tokens: 250]
    ↓
Final Response

Questions you need to answer:
- Which step is slow? (latency bottleneck)
- Are retrieved docs relevant? (quality check)
- Is LLM generating hallucinations? (faithfulness)
- How much token are we using? (cost tracking)
```

Observability tools trả lời những câu hỏi này.

## Comparison: Langfuse vs LangSmith vs Phoenix

| Aspect | Langfuse | LangSmith | Phoenix |
|--------|----------|-----------|---------|
| Open-source | ✓ | ✗ | ✓ |
| Self-hosted | ✓ Easy | ✗ | ✓ Easy |
| Cloud | ✓ Managed | ✓ Managed | ✗ |
| Cost | Free tier generous | $$$ | Free |
| LLM integration | LlamaIndex, LangChain | LangChain only | Framework agnostic |
| Tracing depth | Deep | Medium | Medium |
| **Recommendation** | **Best overall** | Enterprise | Budget |

**Recommendation:** Langfuse cho most teams (free + self-host option).

## Langfuse: Complete Setup

### Installation

```bash
# Install Langfuse
pip install langfuse

# For self-hosting (recommended)
docker run -e DATABASE_URL="postgresql://..." -p 3000:3000 langfuse/langfuse
# Visit http://localhost:3000
```

### Integration with LlamaIndex

```python
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index import VectorStoreIndex, Settings

# Initialize callback handler
langfuse_handler = LlamaIndexCallbackHandler(
    public_key="pk_...",
    secret_key="sk_...",
    host="https://your-langfuse-instance.com"  # or http://localhost:3000
)

# Add to LlamaIndex
Settings.callback_manager.add_handler(langfuse_handler)

# Now every LlamaIndex operation is traced
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")

# Automatically logged to Langfuse!
```

### Integration with FastAPI + Custom RAG

```python
from fastapi import FastAPI
from langfuse import Langfuse
import json

app = FastAPI()
langfuse = Langfuse(
    public_key="pk_...",
    secret_key="sk_...",
    host="http://localhost:3000"  # Self-hosted
)

@app.post("/query")
async def rag_query(question: str):
    # Trace the entire pipeline
    trace = langfuse.trace(
        name="rag_pipeline",
        input={"question": question},
        user_id="user_123",  # Track per-user
        metadata={"model": "gpt-4", "version": "1.0"}
    )

    try:
        # Step 1: Retrieval
        retrieval_span = trace.span(
            name="retrieval",
            input={"question": question}
        )

        retrieved_docs = retrieve(question)

        retrieval_span.end(
            output={
                "num_docs": len(retrieved_docs),
                "top_scores": [d.score for d in retrieved_docs[:3]]
            }
        )

        # Step 2: Reranking
        reranking_span = trace.span(
            name="reranking",
            input={"num_docs": len(retrieved_docs)}
        )

        reranked_docs = rerank(retrieved_docs, question)

        reranking_span.end(
            output={
                "num_docs": len(reranked_docs),
                "best_score": reranked_docs[0].score
            }
        )

        # Step 3: Generation
        generation_span = trace.span(
            name="generation",
            input={"num_docs": len(reranked_docs)}
        )

        answer = generate(question, reranked_docs)

        generation_span.end(
            output={
                "answer": answer,
                "length": len(answer.split())
            }
        )

        # End trace
        trace.end(
            output={"answer": answer},
            level="SUCCESS"
        )

        return {"answer": answer}

    except Exception as e:
        # Log errors
        trace.end(
            output={"error": str(e)},
            level="ERROR"
        )
        raise

```

## What to Trace & Monitor

### 1. Latency Breakdown

```python
# Track latency per step
retrieval_latency: 150ms
reranking_latency: 200ms
generation_latency: 500ms
total_latency: 850ms

# Track over time
Baseline (Week 1): 850ms
After optimization (Week 2): 600ms
Improvement: 29% ↓
```

### 2. Quality Metrics

```python
# Track retrieval quality
retrieved_precision@10: 0.78
retrieved_recall: 0.82

# Track LLM output quality
faithfulness: 0.85
answer_relevancy: 0.88
```

### 3. Token Usage & Cost

```python
# Track tokens
input_tokens: 2500
output_tokens: 250
total_tokens: 2750

# Calculate cost
cost_per_1m_tokens: $0.15  # gpt-4
daily_cost: (avg_tokens_per_query * queries_per_day * cost) / 1M
# e.g., (2750 * 1000 * 0.15) / 1M = $0.4125 per day
```

### 4. Error Tracking

```python
# Types of errors to monitor
hallucination_rate: 15%  # LLM makes up facts
no_context_rate: 5%     # Retriever returns empty
timeout_rate: 0.5%      # Requests timeout
```

## Example: Langfuse Dashboard Queries

### Query 1: Latency Trends

```sql
-- What's our average latency per day?
SELECT
    DATE(created_at) AS date,
    AVG(duration) AS avg_latency_ms,
    PERCENTILE_CONT(0.95)(duration) AS p95_latency_ms
FROM
    traces
WHERE
    name = 'rag_pipeline'
GROUP BY
    DATE(created_at)
ORDER BY
    date DESC
```

### Query 2: Cost Analysis

```sql
-- Daily LLM cost
SELECT
    DATE(created_at) AS date,
    SUM(input_tokens) AS total_input,
    SUM(output_tokens) AS total_output,
    (SUM(input_tokens) * 0.00003 + SUM(output_tokens) * 0.00006) AS cost_usd
FROM
    generations
WHERE
    DATE(created_at) >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY
    DATE(created_at)
```

### Query 3: Quality Regressions

```sql
-- Alert if average score drops below threshold
SELECT
    DATE(created_at) AS date,
    AVG(CAST(metadata->>'faithfulness' AS FLOAT)) AS avg_faithfulness
FROM
    traces
WHERE
    name = 'rag_pipeline'
    AND DATE(created_at) >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY
    DATE(created_at)
HAVING
    AVG(CAST(metadata->>'faithfulness' AS FLOAT)) < 0.80
```

## Production Langfuse Architecture

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Langfuse Server
  langfuse:
    image: langfuse/langfuse:latest
    environment:
      DATABASE_URL: "postgresql://langfuse:password@db:5432/langfuse"
      NEXTAUTH_SECRET: "your-secret"
      NEXTAUTH_URL: "https://langfuse.yourdomain.com"
    ports:
      - "3000:3000"
    depends_on:
      - db

  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: langfuse
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Your RAG Application
  rag_app:
    build: .
    environment:
      LANGFUSE_HOST: "http://langfuse:3000"
      LANGFUSE_PUBLIC_KEY: "pk_..."
      LANGFUSE_SECRET_KEY: "sk_..."
    depends_on:
      - langfuse
    ports:
      - "8000:8000"

volumes:
  postgres_data:
```

## Common Patterns: What to Log

```python
# Pattern 1: User Feedback Loop
@app.post("/query/{query_id}/feedback")
async def log_feedback(query_id: str, rating: int, feedback: str):
    # Link feedback to original trace
    langfuse.score_trace(
        trace_id=query_id,
        name="user_rating",
        value=rating,
        comment=feedback
    )

# Pattern 2: A/B Test Tracking
def rag_query_ab_test(question: str, variant: str):
    trace = langfuse.trace(
        name="rag_ab_test",
        input={"question": question},
        metadata={"variant": variant}  # "A" or "B"
    )
    # ... run query ...
    trace.end()

# Pattern 3: Cost Budgeting
daily_budget = 50  # USD
daily_spent = 0

def check_budget():
    if daily_spent > daily_budget:
        langfuse.span(
            name="budget_exceeded",
            level="WARNING"
        )
        # Stop accepting queries
```

## Key Takeaway

**Observability is non-negotiable for production RAG.**

Use Langfuse to:
1. **Debug** - Find bottlenecks (latency, quality)
2. **Monitor** - Track metrics over time
3. **Optimize** - A/B test variations
4. **Cost control** - Monitor token usage & spending

**Setup time:** 30 minutes (LlamaIndex) to 2 hours (custom FastAPI).

**ROI:** Catch quality regressions before users notice. Optimize what actually matters (data-driven, not guessing).

**Pro tip:** Start simple (log latency, token count). Add RAGAS metrics weekly. Build dashboard for stakeholders.
