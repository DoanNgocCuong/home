# RAGAS Framework: Evaluation Metrics cho RAG

## Tổng Quan

RAGAS (Retrieval-Augmented Generation Assessment) là framework mới nhất (2023) để đánh giá RAG systems mà không cần human annotations. Nó dùng LLM-as-Judge để tính 4 metrics core.

**Game-changer:** Trước đây, bạn cần manual evaluation. Giờ bạn có automated evaluation.

## 4 Core Metrics của RAGAS

### 1. Faithfulness (0-1)

**Definition:** Có bao nhiêu thông tin trong answer được dựa trên context được cung cấp?

**Metric:**
```
Faithfulness = (Statements in answer grounded in context) / (Total statements in answer)
```

**Example:**
```
Context: "Paris is the capital of France"
Question: "What is the capital of France?"

Answer 1: "Paris"
Faithfulness = 1.0 (100% grounded)

Answer 2: "Paris is known as the City of Love"
Faithfulness = 0.5 (half grounded, "City of Love" is not in context)

Answer 3: "Paris, which has a population of 2.2M"
Faithfulness = 0.5 (Paris is grounded, population is not)
```

### 2. Answer Relevancy (0-1)

**Definition:** Answer có trả lời question không?

**Metric:**
```
Relevancy = (Mean cosine similarity between question +
             regenerated questions from answer) / expected_max
```

**Explanation:**
- LLM tạo ra 3-5 questions mà answer này có thể trả lời
- Nếu generated questions tương tự original question → relevant

**Example:**
```
Question: "What is machine learning?"
Answer: "Machine learning is a subset of AI..."

Generated questions from answer:
- "What is machine learning?" (similarity: 0.98) ✓
- "Is ML part of AI?" (similarity: 0.85) ✓
- "How does ML work?" (similarity: 0.75) ✓

Answer Relevancy = mean([0.98, 0.85, 0.75]) = 0.86
```

### 3. Context Precision (0-1)

**Definition:** Retriever có lấy documents đúng không? (False Positives)

**Metric:**
```
Precision = (Number of relevant docs in top-K) / K
```

**Example:**
```
Retrieved documents (top-5):
1. "RAG combines retrieval with generation" ✓ relevant
2. "Machine learning basics" ✗ not relevant
3. "Vector databases for retrieval" ✓ relevant
4. "Transformer architecture" ✗ not relevant
5. "Information retrieval best practices" ✓ relevant

Context Precision = 3/5 = 0.6
```

### 4. Context Recall (0-1)

**Definition:** Retriever có miss important documents không? (False Negatives)

**Metric:**
```
Recall = (Relevant statements in retrieved context) / (Relevant statements in full corpus)
```

**Example:**
```
Full corpus has 10 statements relevant to question "What is RAG?"
Retrieved documents contain 7 of those 10 statements

Context Recall = 7/10 = 0.7
```

## How RAGAS Calculates These

RAGAS sử dụng LLM (GPT-3.5/4, Claude, etc.) để judge metrics:

```python
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Metrics score giữa 0-1
# 0.8+ = Good
# 0.6-0.8 = Acceptable
# <0.6 = Needs improvement
```

## Implementation: Calculate RAGAS Metrics

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness
)
from datasets import Dataset

# Your evaluation dataset
eval_data = {
    "question": [
        "What is RAG?",
        "How does vector search work?",
        "What is prompt caching?"
    ],
    "answer": [
        "RAG combines retrieval with generation...",
        "Vector search uses embeddings...",
        "Prompt caching caches token embeddings..."
    ],
    "contexts": [
        [
            "Retrieval-Augmented Generation (RAG) combines...",
            "RAG improves factuality by..."
        ],
        [
            "Vector embeddings represent text numerically...",
            "Similarity search finds nearest neighbors..."
        ],
        [
            "Prompt caching reduces costs by 60-75%...",
            "Cache write costs $0.000005 per token..."
        ]
    ],
    "ground_truth": [
        "RAG is a technique combining retrieval with generation",
        "Vector search embeds queries and documents, finds nearest neighbors",
        "Prompt caching caches LLM token embeddings for reuse"
    ]
}

# Create Dataset
dataset = Dataset.from_dict(eval_data)

# Define metrics
metrics = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
]

# Run evaluation
results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm="gpt-4",  # Or claude-3-sonnet
    embeddings="all-MiniLM-L6-v2"
)

# Results
print(results)
# Output:
# faithfulness: 0.85
# answer_relevancy: 0.88
# context_precision: 0.75
# context_recall: 0.82
```

## Interpretation Guide

### Perfect Score (1.0):
- Answer is fully grounded in context
- Answer directly addresses question
- Retrieved documents are all relevant
- No relevant documents were missed

### Good Score (0.8-0.9):
- Minor irrelevancies or ungrounded statements
- Good coverage of question
- Most retrieved documents relevant
- Small gaps in coverage

### Acceptable Score (0.6-0.8):
- Some hallucinations present
- Partially answers question
- Mix of relevant and irrelevant docs
- Notable gaps in context

### Poor Score (<0.6):
- Significant hallucinations
- Doesn't address question well
- Many irrelevant retrieved docs
- Missing key relevant information

## Debugging Low Scores

**Low Faithfulness?**
```
→ Problem: LLM hallucinating (answer not grounded in context)
→ Solution:
  1. Rerank retrieved documents (add cross-encoder)
  2. Adjust prompt to emphasize "only use provided context"
  3. Use smaller LLM with better instruction following
```

**Low Answer Relevancy?**
```
→ Problem: Answer doesn't match question
→ Solution:
  1. Improve retrieval (hybrid search, multi-query)
  2. Better prompt engineering (be more explicit)
  3. Add few-shot examples
```

**Low Context Precision?**
```
→ Problem: Retrieved documents include irrelevant ones
→ Solution:
  1. Add reranking (Cohere Rerank-4, BGE)
  2. Tune retriever (embedding model, BM25 weight)
  3. Implement multi-query with deduplication
```

**Low Context Recall?**
```
→ Problem: Relevant documents not retrieved
→ Solution:
  1. Increase top_k (retrieve top-50 instead of top-10)
  2. Better embedding model (OpenAI/Cohere vs free models)
  3. Add multi-query rewriting
  4. Expand knowledge base (ensure docs are comprehensive)
```

## Running RAGAS on Your Production Data

```python
import json
from datetime import datetime

# Log production queries
def log_rag_output(question, answer, contexts):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "user_feedback": None  # Placeholder
    }
    with open("rag_logs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Weekly RAGAS evaluation
def weekly_evaluation():
    # Load production logs
    with open("rag_logs.jsonl") as f:
        logs = [json.loads(line) for line in f]

    # Sample 100 recent logs
    sample = logs[-100:]

    # Convert to dataset format
    dataset = Dataset.from_dict({
        "question": [log["question"] for log in sample],
        "answer": [log["answer"] for log in sample],
        "contexts": [log["contexts"] for log in sample]
    })

    # Evaluate
    results = evaluate(dataset, metrics=[...])

    # Log results
    with open("evaluation_history.jsonl", "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "metrics": results
        }) + "\n")

    # Alert if metrics drop
    if results["faithfulness"] < 0.8:
        send_alert(f"Faithfulness dropped to {results['faithfulness']}")

# Schedule weekly
schedule.every().wednesday.at("02:00").do(weekly_evaluation)
```

## RAGAS vs Human Evaluation

```
Metric                  RAGAS Score   Human Agreement
─────────────────────────────────────────────────────
Faithfulness           0.85          82% agreement
Answer Relevancy       0.88          85% agreement
Context Precision      0.75          78% agreement
Context Recall         0.82          80% agreement
```

RAGAS không perfect, nhưng tốt đủ để:
1. Track trends (↓ if system degrades)
2. Compare variants (A/B testing)
3. Automate monitoring (no manual labor)

## Key Takeaway

RAGAS cung cấp automated, reproducible evaluation cho RAG systems:

**4 metrics to track:**
- **Faithfulness:** LLM không hallucinate?
- **Answer Relevancy:** Answer đúng câu hỏi?
- **Context Precision:** Retrieved docs relevant?
- **Context Recall:** Có miss important docs?

**Quick start:**
```python
# 5 minutes to setup
from ragas import evaluate
results = evaluate(dataset, metrics=[...])
print(results)  # Done!
```

**Practical tip:** Chạy RAGAS weekly trên production logs. Set up alerts khi metrics drop. Use results để prioritize optimizations (low faithfulness → focus on prompt/reranking, low recall → focus on retrieval).

**Next step:** A/B test các optimizations, measure impact với RAGAS metrics.
