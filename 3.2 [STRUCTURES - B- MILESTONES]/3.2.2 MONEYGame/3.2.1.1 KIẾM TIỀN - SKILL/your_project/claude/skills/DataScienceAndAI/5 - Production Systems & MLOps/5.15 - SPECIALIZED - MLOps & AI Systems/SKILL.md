# MLOps & AI Systems — Production Best Practices

> **Domain:** 5.15 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

MLOps (Machine Learning Operations) extends DevOps principles to ML systems, addressing the unique challenges of model lifecycle management. Unlike traditional software, ML systems have:
- **Data dependencies** (quality impacts model behavior)
- **Probabilistic outputs** (not deterministic)
- **Performance degradation** (model & data drift)
- **Continuous retraining** requirements
- **Regulatory compliance** (AI safety, fairness)

**Key Definition:** MLOps = versioning + testing + deployment + monitoring + retraining loop.

## 2. Core Principles

### 2.1 Model Lifecycle Management
- **Reproducibility**: Tất cả (all) experiments phải có thể tái hiện lại
- **Traceability**: Track từ raw data → trained model → deployment
- **Automation**: Minimize manual steps trong pipeline
- **Governance**: Control ai được phép deploy models nào
- **Observability**: Monitor cả model và data quality sau khi deploy

### 2.2 Production-Ready ML
ML code chỉ là ~5-10% của production system. Còn lại là:
- Data pipeline (40%)
- Feature engineering (20%)
- Infrastructure (15%)
- Testing & validation (10%)

## 3. Best Practices

### 3.1 Model Serving Architecture

**Practice: Choose Appropriate Serving Framework**

| Framework | Use Case | Latency | Throughput |
|-----------|----------|---------|-----------|
| **vLLM** | LLM inference, high throughput | <200ms | 100+ req/s |
| **TGI** | Transformer batching, optimized LLM | <150ms | 50+ req/s |
| **Triton** | Multi-model, diverse frameworks | <100ms | 1000+ req/s |
| **TorchServe** | PyTorch models, simple deploy | <200ms | 100+ req/s |

**Example: vLLM for LLM Service**
```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-2-7b-hf",
    tensor_parallel_size=2,  # Phân tán (distribute) across 2 GPUs
    gpu_memory_utilization=0.9
)

sampling_params = SamplingParams(temperature=0.7, top_p=0.9)
outputs = llm.generate(prompts, sampling_params)
```

**Anti-pattern:** Serving models without batching, causing underutilized GPUs.

### 3.2 Model Versioning & Tracking

**Practice: Use MLflow or Weights & Biases for End-to-End Tracking**

```python
import mlflow
from mlflow.models.signature import infer_signature

mlflow.start_run()

# Log parameters
mlflow.log_params({
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 100
})

# Train model
model = train_model(...)

# Log metrics
mlflow.log_metrics({"accuracy": 0.95, "f1": 0.92})

# Log model with signature
signature = infer_signature(X_train, model.predict(X_train))
mlflow.sklearn.log_model(model, "model", signature=signature)

mlflow.end_run()
```

**Traceability Elements:**
- Model parameters
- Training data version (commit hash)
- Model artifacts
- Evaluation metrics
- Hyperparameters
- Hardware specs

**Anti-pattern:** Saving models as "final.pkl", "final_v2.pkl", "final_REAL.pkl" without metadata.

### 3.3 Feature Store Management

**Practice: Centralized Feature Versioning (Feast)**

```python
from feast import FeatureStore

fs = FeatureStore(repo_path="./feature_repo")

# Define feature view
features = fs.get_online_features(
    entity_df=user_df,
    features=[
        "user_features:total_spent",
        "user_features:purchase_frequency"
    ]
).to_dict()
```

**Benefits:**
- Tái sử dụng (reuse) features across models
- Version control cho features
- Training-serving skew detection
- Point-in-time correctness

### 3.4 A/B Testing for Models

**Practice: Canary Deployment with Traffic Split**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: recommendation-model
spec:
  hosts:
    - recommendation
  http:
    - match:
        - headers:
            user-segment:
              exact: "canary"
      route:
        - destination:
            host: recommendation-v2  # New model
          weight: 100
    - route:
        - destination:
            host: recommendation-v1  # Stable model
          weight: 95
        - destination:
            host: recommendation-v2
          weight: 5  # 5% traffic to new model
```

**Metrics to Track:**
- Conversion rate (chỉ số chuyển đổi)
- Revenue impact
- Latency increase
- Error rate
- User engagement

**Anti-pattern:** Deploying new models to 100% traffic without validation.

### 3.5 Model Monitoring & Drift Detection

**Practice: Implement Data & Concept Drift Monitoring**

**Data Drift:** Input features change distribution
```python
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

# Compare production data vs training data
dashboard = Dashboard(tabs=[
    DataDriftTab(
        reference_data=training_data,
        current_data=production_data,
        columns=["feature_1", "feature_2"]
    )
])
dashboard.save("drift_report.html")
```

**Concept Drift:** Relationship between features & target changes
```python
# Monitor prediction accuracy over time
rolling_accuracy = (
    predictions.groupby(pd.Grouper(freq='D'))
    .apply(lambda x: (x['pred'] == x['actual']).mean())
)

# Alert if accuracy drops >5%
if rolling_accuracy.iloc[-1] < baseline_accuracy - 0.05:
    trigger_retraining()
```

**Anti-pattern:** Only monitoring model metrics, ignoring data quality.

### 3.6 GPU Optimization for Inference

**Practice: Optimize Throughput with Batching & Quantization**

```python
# Quantization reduces model size 4x, improves latency 2-3x
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model = AutoModelForSequenceClassification.from_pretrained("bert-base")

# Quantize to INT8 (lượng tử hóa)
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# INT8: 384MB → 96MB model size
```

**Batch Size Selection:**
- Measure latency & throughput at different batch sizes
- Sweet spot: where GPU is 85-95% utilized
- Too small: underutilized GPUs
- Too large: memory OOM

### 3.7 LLM-Specific Operations

**Practice: Prompt Management & Token Optimization**

```python
from langfuse import Langfuse

client = Langfuse()

# Log prompt execution
trace = client.trace(
    name="customer_support",
    input={"query": user_input}
)

# Use structured prompts
system_prompt = """You are a customer support agent.
- Be concise and helpful
- Escalate to human if issue > 5 mins
- Never share customer data"""

completion = client.generation(
    name="llm_response",
    prompt=system_prompt + user_input,
    model="gpt-4",
    parent_trace_id=trace.id
)
```

**Cost Control for LLMs:**
- Implement input/output token limits
- Use prompt caching (Anthropic Claude, OpenAI GPT-4)
- Route simple queries to smaller models
- Implement rate limiting per user/org

**Example Cost Calculation:**
- 1M input tokens: $15 (OpenAI GPT-4)
- 1M output tokens: $45
- Average response: 200 tokens input + 300 output = $0.00975/request
- 1000 requests/day = $9.75/day cost

### 3.8 Vector Database for RAG

**Practice: RAG with Vector Storage for Semantic Search**

```python
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

# Initialize vector store
embeddings = OpenAIEmbeddings()
vector_db = Pinecone.from_documents(
    documents=chunked_docs,
    embedding=embeddings,
    index_name="document-index"
)

# Retrieve similar documents (truy xuất tài liệu tương tự)
results = vector_db.similarity_search(
    "What are our return policies?",
    k=5  # Top 5 similar documents
)
```

**Popular Vector Databases:**
- **Pinecone**: Managed, serverless, simple
- **Milvus**: Open-source, self-hosted, production-grade
- **Qdrant**: Built for production, strong on filtering
- **Weaviate**: GraphQL API, good for relationships

### 3.9 Observability & Debugging

**Practice: Use Langfuse/LangSmith for LLM Observability**

```python
from langsmith import wrappers, Client

client = Client()

# Automatic tracing
@wrappers.wrap_openai
def answer_question(question):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# All calls automatically logged with:
# - Input/output tokens
# - Model version
# - Latency
# - Cost
# - User feedback loop
```

**Metrics to Track:**
- Token usage (input/output)
- Latency per request
- Error rates & types
- User satisfaction (thumbs up/down)
- Cost per request

### 3.10 AI Safety & Guardrails

**Practice: Implement Output Validation & Filtering**

```python
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# Constrain output format
response_schemas = [
    ResponseSchema(
        name="answer",
        description="The answer to the question"
    ),
    ResponseSchema(
        name="confidence",
        description="Confidence score 0-1"
    )
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Guardrails for safety
def filter_unsafe_output(response):
    unsafe_patterns = [
        r"execute.*code",
        r"delete.*database",
        r"credit card.*\d{4}"
    ]

    for pattern in unsafe_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return "I cannot help with that request"

    return response
```

**Responsible AI Checklist:**
- [ ] Bias testing (across demographics)
- [ ] Adversarial robustness testing
- [ ] PII redaction in logs
- [ ] Rate limiting per user
- [ ] Content moderation
- [ ] Explainability for high-stakes decisions

## 4. Decision Frameworks

### When to Retrain Model?
1. **Performance drops >5%** → urgent
2. **Data drift detected** → within 1 week
3. **Concept drift confirmed** → immediate
4. **New data available** → schedule weekly/monthly

### Batch vs Real-Time Inference?
- **Real-time**: <100ms latency required, <10k QPS, online features
- **Batch**: overnight refresh OK, 1M+ predictions, static features

### Model Compression Strategy?
1. **Quantization** (50% latency improvement, <5% accuracy loss)
2. **Pruning** (30% size reduction, minimal accuracy loss)
3. **Distillation** (5x smaller, 90% accuracy retention)

## 5. Checklist

- [ ] Model versioning system in place (MLflow/W&B)
- [ ] A/B testing framework implemented
- [ ] Data drift monitoring active
- [ ] Model performance degradation alerts configured
- [ ] Retraining pipeline automated
- [ ] Serving infrastructure supports current SLA
- [ ] Feature store for feature versioning
- [ ] Cost tracking per model enabled
- [ ] Observability dashboard set up
- [ ] Safety guardrails implemented
- [ ] Model explainability documented
- [ ] Rollback procedure tested

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Training-serving skew | Models fail in production | Use same preprocessing pipeline for both |
| No data versioning | Cannot debug model failures | Track data commit hash, schema changes |
| Manual model deployment | High error rate, slow rollbacks | CI/CD pipeline for models |
| Ignoring data drift | Model accuracy gradually drops | Implement drift detection & auto-retrain |
| GPU underutilization | Wasted infrastructure costs | Implement batching, right-size instances |
| No guardrails | Safety issues, toxic outputs | Add content moderation, output validation |

## 7. Tools & References

**Model Training & Tracking:**
- MLflow, Weights & Biases, Kubeflow
- Neptune, Guild AI, Polyaxon

**Model Serving:**
- vLLM, TensorFlow Serving, Triton, BentoML, KServe

**Feature Management:**
- Feast, Tecton, FeatureStore.ai, Hopsworks

**Monitoring & Observability:**
- Evidently, WhyLabs, DataRobot, Langfuse, LangSmith

**MLOps Platforms:**
- Databricks, SageMaker, Vertex AI, Anyscale

**Key Reading:**
- "Machine Learning Operations: Best Practices" (Google Cloud)
- "MLOps.community" best practices
- Chip Huyen's ML Systems Design course
