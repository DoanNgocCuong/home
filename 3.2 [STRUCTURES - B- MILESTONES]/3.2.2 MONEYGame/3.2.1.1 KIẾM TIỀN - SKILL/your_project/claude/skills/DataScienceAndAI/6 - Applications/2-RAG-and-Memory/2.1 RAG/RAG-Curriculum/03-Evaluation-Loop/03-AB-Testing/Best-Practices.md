# A/B Testing RAG Configurations

## Tổng Quan

A/B testing cho phép bạn so sánh 2 RAG variants (A vs B) trên cùng một set queries và measure impact một cách scientific. Không có hứng, chỉ có data.

**Golden Rule:** Never ship RAG improvements mà chưa A/B test.

## What to Test?

```
┌─────────────────────────────────────────────────────────┐
│               RAG System Parameters                     │
├─────────────────────────────────────────────────────────┤
│ Retrieval:                                              │
│   - Embedding model (OpenAI vs Cohere vs Local)        │
│   - BM25 vs Vector vs Hybrid (alpha values)            │
│   - Top-K (retrieve 10 vs 20 vs 50 docs)               │
│   - Chunk size (512 vs 1024 vs 2048 tokens)            │
│                                                         │
│ Reranking:                                              │
│   - Reranker on vs off                                 │
│   - Reranker model (Cohere vs BGE vs ColBERT)          │
│   - Rerank top-K (top 10 vs top 20)                    │
│                                                         │
│ Generation:                                             │
│   - LLM model (gpt-4 vs gpt-3.5 vs Llama)              │
│   - Temperature (0.3 vs 0.5 vs 0.7)                    │
│   - Prompt template (v1 vs v2 vs v3)                   │
│   - Top-p sampling                                      │
│                                                         │
│ Post-processing:                                        │
│   - Response format (JSON vs markdown vs plain)        │
│   - Citation style (inline vs footnotes)               │
│   - Max response length                                │
└─────────────────────────────────────────────────────────┘
```

## Prioritization: What to Test First

```
High Impact, Easy to Test:
✓ Reranking on/off (+20-30% accuracy, minimal latency cost)
✓ Prompt templates (free to iterate, instant result)
✓ Top-K retrieval (10 vs 50, latency-quality tradeoff)

Medium Impact, Medium Effort:
✓ Embedding model swap (need to reindex, 1-2 days)
✓ Chunk size optimization (need to reindex, 1-2 days)
✓ LLM model swap (need server, cost change)

Low Impact, High Effort:
✗ Hybrid search alpha tuning (diminishing returns)
✗ Complex prompt engineering (testing overhead)
```

**Recommendation:** Start with reranking + prompt templates.

## A/B Testing Framework

```python
from dataclasses import dataclass
from typing import List
import random
from datetime import datetime

@dataclass
class ABTest:
    test_id: str
    name: str
    variant_a: dict  # Config for A
    variant_b: dict  # Config for B
    start_date: datetime
    end_date: datetime
    sample_size_per_variant: int

class ABTestingEngine:
    def __init__(self, langfuse_client):
        self.langfuse = langfuse_client
        self.tests = {}

    def create_test(self, test: ABTest):
        """Create new A/B test"""
        self.tests[test.test_id] = {
            "test": test,
            "results_a": [],
            "results_b": [],
            "metadata": {"created_at": datetime.now()}
        }

    def assign_variant(self, test_id: str, user_id: str) -> str:
        """Deterministically assign user to A or B"""
        hash_value = hash(f"{user_id}:{test_id}") % 2
        return "A" if hash_value == 0 else "B"

    async def query(self, test_id: str, question: str, user_id: str):
        """Run RAG query with A/B variant"""
        variant = self.assign_variant(test_id, user_id)
        config = (
            self.tests[test_id]["test"].variant_a
            if variant == "A"
            else self.tests[test_id]["test"].variant_b
        )

        # Run RAG with variant config
        result = await run_rag_with_config(question, config)

        # Log to Langfuse with variant tag
        trace = self.langfuse.trace(
            name=f"ab_test_{test_id}",
            input={"question": question},
            metadata={
                "variant": variant,
                "test_id": test_id,
                "user_id": user_id
            }
        )

        # Return result + variant info
        result["variant"] = variant
        result["test_id"] = test_id

        return result

    def get_results(self, test_id: str):
        """Analyze A/B test results"""
        test = self.tests[test_id]["test"]

        # Query results from Langfuse
        results_a = self.langfuse.get_traces(
            filters=[
                {"key": "metadata.variant", "value": "A"},
                {"key": "metadata.test_id", "value": test_id}
            ]
        )

        results_b = self.langfuse.get_traces(
            filters=[
                {"key": "metadata.variant", "value": "B"},
                {"key": "metadata.test_id", "value": test_id}
            ]
        )

        # Calculate metrics
        return {
            "test_id": test_id,
            "test_name": test.name,
            "variant_a": self._calculate_metrics(results_a),
            "variant_b": self._calculate_metrics(results_b),
            "winner": self._determine_winner(results_a, results_b),
            "confidence": self._calculate_confidence(results_a, results_b)
        }

    def _calculate_metrics(self, traces):
        """Calculate average metrics"""
        latencies = [t["duration"] for t in traces]
        faithfulness = [float(t["metadata"].get("faithfulness", 0)) for t in traces]
        relevancy = [float(t["metadata"].get("relevancy", 0)) for t in traces]

        return {
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "avg_faithfulness": sum(faithfulness) / len(faithfulness),
            "avg_relevancy": sum(relevancy) / len(relevancy),
            "sample_size": len(traces)
        }

    def _determine_winner(self, results_a, results_b):
        """Statistical significance test"""
        metrics_a = self._calculate_metrics(results_a)
        metrics_b = self._calculate_metrics(results_b)

        # Simple comparison (in production, use proper statistical tests)
        score_a = (
            metrics_a["avg_faithfulness"] * 0.5 +
            metrics_a["avg_relevancy"] * 0.3 -
            metrics_a["avg_latency_ms"] / 1000 * 0.2
        )

        score_b = (
            metrics_b["avg_faithfulness"] * 0.5 +
            metrics_b["avg_relevancy"] * 0.3 -
            metrics_b["avg_latency_ms"] / 1000 * 0.2
        )

        if abs(score_a - score_b) < 0.05:
            return "TIE"
        return "A" if score_a > score_b else "B"

    def _calculate_confidence(self, results_a, results_b):
        """Calculate confidence level"""
        # In production, use proper statistical test (t-test, chi-square)
        # Simplified here
        return 0.95 if len(results_a) >= 100 else 0.70
```

## Example A/B Test: Reranking

```python
from datetime import datetime, timedelta

# Define test
test = ABTest(
    test_id="rerank_001",
    name="Cohere Rerank-4 Impact",
    variant_a={
        "retrieval": {"top_k": 10, "method": "hybrid"},
        "reranking": False,  # No reranking
        "generation": {"model": "gpt-4"}
    },
    variant_b={
        "retrieval": {"top_k": 100, "method": "hybrid"},  # Retrieve more
        "reranking": True,  # Add reranking
        "reranker_model": "cohere-rerank-4",
        "generation": {"model": "gpt-4"}
    },
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7),
    sample_size_per_variant=500
)

# Run test
ab_engine = ABTestingEngine(langfuse)
ab_engine.create_test(test)

# For each query in production
for question in production_queries:
    result = await ab_engine.query(
        test_id="rerank_001",
        question=question,
        user_id=user_id
    )
    # Serve result to user

# After 7 days, get results
results = ab_engine.get_results("rerank_001")
print(results)
# Output:
# {
#   "variant_a": {
#     "avg_faithfulness": 0.80,
#     "avg_relevancy": 0.82,
#     "avg_latency_ms": 240
#   },
#   "variant_b": {
#     "avg_faithfulness": 0.86,  # +7.5%
#     "avg_relevancy": 0.88,     # +7.3%
#     "avg_latency_ms": 280      # +16.7% latency
#   },
#   "winner": "B",
#   "confidence": 0.95
# }
```

## Multi-Armed Bandit (Optional Improvement)

Instead of A/B (50-50 split), use **Thompson Sampling** để gradually shift traffic to better variant:

```python
# Week 1: 50% A, 50% B
# Week 2: 40% A, 60% B (B performing better)
# Week 3: 20% A, 80% B
# Week 4: 5% A, 95% B (B clear winner)
# Week 5: 100% B (A retired)
```

Pros: Minimize exposure to worse variant, maximize learning.
Cons: Takes longer to get statistical significance.

## Metrics to Track

```python
# Primary metrics (alignment with business)
faithfulness: 0.85    # Accuracy
relevancy: 0.88       # Relevance
user_satisfaction: 4.2/5.0

# Secondary metrics (operational)
latency: 250ms
cost_per_query: $0.01
token_usage: 2500

# Negative metrics (watch out)
hallucination_rate: 2%
timeout_rate: 0.1%
```

## Statistical Significance

```
Rule of Thumb:
- Sample size < 100 per variant: Not significant
- Sample size 100-500: Weak significance
- Sample size 500+: Good significance
- Sample size 1000+: Strong significance

Confidence Levels:
- 95% confidence: p-value < 0.05 (standard)
- 99% confidence: p-value < 0.01 (strict)
```

## Decision Framework

```
Is improvement statistically significant?
├─ Yes, winner is B
│  ├─ Large improvement (>5%): DEPLOY immediately
│  ├─ Small improvement (1-5%): Evaluate cost/benefit
│  └─ Slight improvement (<1%): Only deploy if no downsides
└─ No, results are inconclusive
   ├─ Run longer (more samples)
   ├─ Check for data quality issues
   └─ Consider test wasn't sensitive enough
```

## Key Takeaway

A/B testing transforms RAG optimization from guesswork to data science.

**Practical workflow:**
1. Pick one variable to test (reranker, prompt, embedding model)
2. Create A/B test with clear hypothesis
3. Run for 7 days (collect 500+ samples per variant)
4. Analyze results statistically
5. Deploy winner if significant
6. Iterate (next variable)

**Quick wins to test:**
- Reranking: +20-30% quality
- Prompt v2: +10-15% relevancy
- Top-K: +5% recall (at latency cost)

**Time investment:** 2 hours to setup framework, then 1 hour per test iteration.
**Expected ROI:** 15-25% overall quality improvement per quarter.
