# Continuous Improvement Loop cho RAG

## Tổng Quan

Continuous improvement là vòng lặp: **Monitor → Capture Failures → Curate → Fine-tune → A/B Test → Deploy → Repeat**.

Tất cả các tool từ phases trước (RAGAS, Langfuse, A/B testing) đều fit vào loop này.

## The Flywheel: Continuous Improvement Cycle

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Phase 1: MONITOR (Production Langfuse)                │
│  ├─ Track RAGAS metrics daily                           │
│  ├─ Monitor latency & cost                              │
│  └─ Alert on regressions                                │
│       ↓                                                   │
│  Phase 2: CAPTURE FAILURES                              │
│  ├─ Log failed queries (user feedback, low scores)      │
│  ├─ Identify failure patterns                           │
│  └─ Build failure dataset                               │
│       ↓                                                   │
│  Phase 3: CURATE DATASETS                               │
│  ├─ Clean failure dataset                               │
│  ├─ Add ground truth labels                             │
│  └─ Create test/eval dataset                            │
│       ↓                                                   │
│  Phase 4: OPTIMIZE                                      │
│  ├─ Adjust parameters (chunk size, embedding model)     │
│  ├─ Improve prompts                                     │
│  └─ Add reranking / fine-tune retriever                 │
│       ↓                                                   │
│  Phase 5: A/B TEST                                      │
│  ├─ Test improvement on control group                   │
│  ├─ Measure RAGAS metrics impact                        │
│  └─ Check cost/latency tradeoffs                        │
│       ↓                                                   │
│  Phase 6: DEPLOY                                        │
│  ├─ Gradually rollout to 100%                           │
│  ├─ Monitor for regressions                             │
│  └─ Keep old version for rollback                       │
│       ↓                                                   │
│  BACK TO PHASE 1 (repeat)                               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Phase 1: Monitor (Ongoing)

```python
# Daily RAGAS evaluation
from datetime import datetime, timedelta
from ragas import evaluate
import json

def daily_evaluation():
    """Run RAGAS on yesterday's production queries"""

    # Load production logs
    yesterday = datetime.now() - timedelta(days=1)
    with open("production_logs.jsonl") as f:
        logs = [
            json.loads(line) for line in f
            if json.loads(line)["timestamp"].startswith(yesterday.strftime("%Y-%m-%d"))
        ]

    # Convert to RAGAS format
    dataset = Dataset.from_dict({
        "question": [log["question"] for log in logs],
        "answer": [log["answer"] for log in logs],
        "contexts": [log["contexts"] for log in logs]
    })

    # Evaluate
    results = evaluate(dataset, metrics=[...])

    # Log metrics
    metrics_log = {
        "date": yesterday.isoformat(),
        "faithfulness": results["faithfulness"],
        "answer_relevancy": results["answer_relevancy"],
        "context_precision": results["context_precision"],
        "context_recall": results["context_recall"],
        "sample_size": len(logs)
    }

    with open("metrics_history.jsonl", "a") as f:
        f.write(json.dumps(metrics_log) + "\n")

    # Alert if metrics drop >5%
    prev_faithfulness = get_previous_metric("faithfulness")
    if (prev_faithfulness - results["faithfulness"]) > 0.05:
        send_alert(f"Faithfulness dropped from {prev_faithfulness:.2f} to {results['faithfulness']:.2f}")

# Schedule daily
schedule.every().day.at("03:00").do(daily_evaluation)
```

## Phase 2: Capture Failures

```python
# Log failures from production
def log_failure(
    question: str,
    answer: str,
    contexts: List[str],
    failure_reason: str = None,
    user_rating: int = None
):
    """Log query failure for later analysis"""

    failure = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "failure_reason": failure_reason,  # "hallucination", "incomplete", "irrelevant"
        "user_rating": user_rating  # 1-5 stars from user
    }

    with open("failure_log.jsonl", "a") as f:
        f.write(json.dumps(failure) + "\n")

# User feedback endpoint
@app.post("/feedback")
async def submit_feedback(query_id: str, rating: int, comment: str = None):
    """Capture user feedback"""

    # Get original query from Langfuse
    trace = langfuse.get_trace(query_id)

    # If low rating, log as failure
    if rating <= 2:  # 1-2 stars = failure
        log_failure(
            question=trace.input["question"],
            answer=trace.output["answer"],
            contexts=trace.output["contexts"],
            failure_reason=comment,
            user_rating=rating
        )

    # Log feedback to Langfuse for tracking
    langfuse.score_trace(query_id, "user_rating", rating)
```

## Phase 3: Curate Failure Dataset

```python
import json
from sklearn.cluster import DBSCAN
import numpy as np

def analyze_failure_patterns():
    """Identify patterns in failures"""

    # Load all failures
    with open("failure_log.jsonl") as f:
        failures = [json.loads(line) for line in f]

    # Cluster by failure reason
    failure_types = {}
    for failure in failures:
        reason = failure["failure_reason"]
        if reason not in failure_types:
            failure_types[reason] = []
        failure_types[reason].append(failure)

    # Print summary
    print("Failure Analysis:")
    print("─" * 50)
    for reason, failures in sorted(failure_types.items(), key=lambda x: -len(x[1])):
        print(f"{reason}: {len(failures)} cases")
        print(f"  Examples: {failures[0]['question'][:60]}...")
        print()

    return failure_types

# Curate dataset for fine-tuning/improvement
def create_improvement_dataset():
    """Create dataset from failures for focused optimization"""

    failure_types = analyze_failure_patterns()

    # Select top 3 failure types
    top_failures = sorted(
        failure_types.items(),
        key=lambda x: -len(x[1])
    )[:3]

    improvement_dataset = []
    for reason, failures in top_failures:
        # Sample up to 50 from each failure type
        sample = failures[:50]
        for failure in sample:
            improvement_dataset.append({
                "question": failure["question"],
                "answer": failure["answer"],
                "contexts": failure["contexts"],
                "failure_type": reason,
                "correct_answer": None,  # Manual annotation needed
                "correct_contexts": None  # Manual annotation needed
            })

    # Save for annotation/fine-tuning
    with open("improvement_dataset.json", "w") as f:
        json.dump(improvement_dataset, f, indent=2)

    print(f"Created improvement dataset with {len(improvement_dataset)} samples")
    return improvement_dataset
```

## Phase 4: Optimize

Choose optimization strategy based on failure type:

```python
failure_to_optimization = {
    "hallucination": {
        "actions": [
            "Add reranking (filter irrelevant docs)",
            "Strengthen prompt: 'Only use provided context'",
            "Use lower temperature (0.3 instead of 0.5)"
        ],
        "expected_impact": "+10-15% faithfulness"
    },

    "incomplete": {
        "actions": [
            "Increase top_k (retrieve 20 instead of 10)",
            "Add multi-query rewriting",
            "Improve embedding model (OpenAI vs local)"
        ],
        "expected_impact": "+10-20% recall"
    },

    "irrelevant": {
        "actions": [
            "Add reranking (prioritize relevant docs)",
            "Improve prompt: give examples",
            "Tune BM25 vs vector balance (alpha parameter)"
        ],
        "expected_impact": "+5-10% precision"
    },

    "no_context": {
        "actions": [
            "Expand knowledge base (ensure docs are comprehensive)",
            "Better chunk size (1024 instead of 512)",
            "Add semantic search with better embeddings"
        ],
        "expected_impact": "Depends on knowledge base quality"
    }
}
```

## Phase 5: A/B Test

```python
# Auto-generate A/B test from identified improvement
def create_ab_test_from_failure(failure_type: str) -> ABTest:
    """Automatically create A/B test"""

    optimization = failure_to_optimization[failure_type]

    return ABTest(
        test_id=f"improvement_{failure_type}_{datetime.now().strftime('%Y%m%d')}",
        name=f"Fix: {failure_type} issues",
        variant_a=load_current_config(),  # Current production
        variant_b=apply_optimizations(optimization["actions"]),  # Improved
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        sample_size_per_variant=500
    )

# Run test and validate
def run_optimization_test(failure_type: str):
    test = create_ab_test_from_failure(failure_type)
    ab_engine.create_test(test)

    # Run for 7 days
    # ... (during this time, queries are split A/B) ...

    # Analyze results
    results = ab_engine.get_results(test.test_id)

    return results
```

## Phase 6: Deploy

```python
def should_deploy(test_results, failure_type: str) -> bool:
    """Decide whether to deploy variant B"""

    # Criteria:
    # 1. Statistically significant improvement
    if test_results["confidence"] < 0.95:
        return False

    # 2. Improvement in target metric
    metric_improvement = (
        test_results["variant_b"]["avg_faithfulness"] -
        test_results["variant_a"]["avg_faithfulness"]
    )

    if metric_improvement < 0.03:  # < 3% improvement
        return False

    # 3. No regression in other metrics
    if (test_results["variant_b"]["avg_latency_ms"] >
        test_results["variant_a"]["avg_latency_ms"] * 1.2):  # >20% slower
        return False

    return True

# Gradual rollout
def gradual_deploy(config, total_traffic: float = 1.0):
    """Deploy with gradual traffic increase"""

    rollout_plan = [
        {"phase": 1, "traffic": 0.05, "days": 1},   # 5% for 1 day
        {"phase": 2, "traffic": 0.10, "days": 1},   # 10% for 1 day
        {"phase": 3, "traffic": 0.25, "days": 2},   # 25% for 2 days
        {"phase": 4, "traffic": 0.50, "days": 2},   # 50% for 2 days
        {"phase": 5, "traffic": 1.00, "days": 99},  # 100% forever
    ]

    for phase in rollout_plan:
        print(f"Phase {phase['phase']}: {phase['traffic']*100:.0f}% for {phase['days']} days")

        # Monitor metrics during rollout
        # If regression detected → rollback immediately

        await asyncio.sleep(phase["days"] * 24 * 3600)

    print("Deployment complete!")
```

## Integration: Full Continuous Improvement Loop

```python
import schedule
import asyncio

# Schedule weekly cycle
schedule.every().sunday.at("00:00").do(weekly_improvement_cycle)

async def weekly_improvement_cycle():
    """Run full continuous improvement cycle"""

    print("=== Starting Weekly Improvement Cycle ===\n")

    # Phase 1: Analyze metrics
    print("Phase 1: Monitoring production...")
    metrics = daily_evaluation()

    # Phase 2: Capture failures
    print("Phase 2: Analyzing failures...")
    failure_types = analyze_failure_patterns()

    # Phase 3: Curate dataset
    print("Phase 3: Creating improvement dataset...")
    improvement_dataset = create_improvement_dataset()

    # Phase 4: Identify top optimization
    print("Phase 4: Planning optimization...")
    top_failure = max(failure_types.items(), key=lambda x: -len(x[1]))[0]
    optimization = failure_to_optimization[top_failure]
    print(f"  → Targeting: {top_failure}")
    print(f"  → Actions: {optimization['actions']}")

    # Phase 5: Create and run A/B test
    print("Phase 5: Launching A/B test...")
    test = create_ab_test_from_failure(top_failure)
    ab_engine.create_test(test)
    print(f"  → Test ID: {test.test_id}")
    print(f"  → Duration: 7 days")
    print(f"  → Expected improvement: {optimization['expected_impact']}")

    # Wait 7 days
    print("\n  (Running A/B test for 7 days...)")

    # Phase 6: Deploy if successful
    print("Phase 6: Analyzing A/B test results...")
    test_results = ab_engine.get_results(test.test_id)

    if should_deploy(test_results, top_failure):
        print(f"  ✓ Deploying variant B!")
        print(f"    - Improvement: +{(test_results['variant_b']['avg_faithfulness'] - test_results['variant_a']['avg_faithfulness'])*100:.1f}%")
        gradual_deploy(test.variant_b)
    else:
        print(f"  ✗ Results not significant enough, keeping variant A")

    print("\n=== Cycle Complete ===\n")

# Run event loop
while True:
    schedule.run_pending()
    await asyncio.sleep(60)
```

## LLM-as-Judge Automation (Optional)

```python
from openai import OpenAI

async def auto_label_failures(failures: List[dict]):
    """Use LLM to auto-label failure types"""

    client = OpenAI()

    labeled = []
    for failure in failures:
        # Ask LLM to classify
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this RAG failure:

Question: {failure['question']}
Answer: {failure['answer']}
Context: {failure['contexts'][:2]}

Classify the failure reason:
- hallucination (answer contains false info)
- incomplete (answer missing info)
- irrelevant (answer doesn't match context)
- no_context (retriever returned empty)
- format (answer malformed)
- other

Return only the category."""
                }
            ]
        )

        failure_type = response.choices[0].message.content.strip()
        failure["auto_labeled_reason"] = failure_type
        labeled.append(failure)

    return labeled
```

## Key Takeaway

**Continuous improvement is a systematic process, not random tweaking.**

The flywheel:
1. **Monitor** - Track metrics daily
2. **Capture** - Log failures from production
3. **Curate** - Build dataset from failures
4. **Optimize** - Apply targeted improvements
5. **Test** - A/B test with statistical rigor
6. **Deploy** - Gradual rollout with monitoring
7. **Repeat** - Back to step 1

**Expected cycle:**
- Week 1: +10% improvement (easy wins)
- Month 2: +5-8% improvement (harder problems)
- Quarter 3: +3-5% improvement (diminishing returns)

**Investment:** 1-2 hours per week to run cycle.
**Result:** Compound improvements, 20-30% quality boost per quarter.
