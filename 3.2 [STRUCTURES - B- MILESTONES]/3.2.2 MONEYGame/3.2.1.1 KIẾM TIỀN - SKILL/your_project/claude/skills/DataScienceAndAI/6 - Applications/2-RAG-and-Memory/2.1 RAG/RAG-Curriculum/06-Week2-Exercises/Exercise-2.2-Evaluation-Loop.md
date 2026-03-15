
# Bài 2.2 — Evaluation Loop: Đo, Trace, So sánh, Cải thiện

**Hạn nộp:** Cuối thứ 6-7 tuần này (học từ thứ 5)

## Mục tiêu Bài Tập

Biến RAG pipeline từ bài 2.1 thành **production-grade** bằng cách:

- Thiết lập observability layer (Langfuse) để trace từng step của RAG
- Xây dựng evaluation dataset + chạy RAGAS metrics (Faithfulness, Answer Relevancy, Context Precision, Context Recall)
- Thực hiện A/B test trên config variations (chunk size, reranker, embedding model)
- So sánh kết quả, chọn best config, document improvement over time

Sau bài này, bạn sẽ hiểu cách **đo lường RAG quality một cách khoa học** thay vì "cảm giác".

**Level:** Advanced — Yêu cầu hoàn thành bài 2.1 trước.

---

## Prerequisite

✅ RAG pipeline từ bài 2.1 chạy ổn định (docker-compose up không error)
✅ Hiểu cơ bản về evaluation metrics (accuracy, precision, recall)
✅ FastAPI & async code comfort level (từ bài 1.1)
✅ 20+ test cases prepared (question + ground_truth + expected_context)

---

## Tech Stack Mới

| Component | Tool | Chú thích |
|-----------|------|----------|
| Observability | Langfuse (Docker self-host) | Trace pipeline steps, visualize latency |
| Evaluation Metrics | RAGAS library | Automated metric calculation |
| Reranker (Optional) | bge-reranker-large | Reorder retrieval results by relevance |
| A/B Testing | Custom metrics comparison | Compare 2+ config variants |
| Storage | PostgreSQL (included in Langfuse Docker) | Persist traces & eval results |

---

## Bảng Các Sai Lầm Thường Gặp (8 Lỗi Fresher)

| # | Sai Lầm | Ví Dụ | Hậu Quả | Cách Sửa | Mức Độ Ảnh Hưởng | Dẫn Chứng |
|---|--------|-------|--------|----------|-----------------|----------|
| 1 | Không có eval dataset → không biết RAG tốt hay dở | Deploy RAG, người dùng chỉ nói "tốt", không có số liệu | Không biết cải thiện nên, không có baseline để so sánh config. RAG có thể đang tệ mà bạn không hay. | Tạo eval dataset 20+ cặp (question, ground_truth, relevant_contexts). Lưu dưới dạng JSON/CSV | **Rất Cao** | Không eval dataset = lái mù |
| 2 | Eval dataset quá nhỏ (<10 cặp) → kết quả không đáng tin | Có 5 test cases, accuracy 100%. Deploy, user phàn nàn | Statistical significance thấp. 5 cases không đủ cover diversity, kết quả có thể random luck | Tối thiểu 20 test cases, cover ≥ 3 categories/domains | **Cao** | Fluke rate cao với small datasets |
| 3 | Chỉ đo accuracy, không đo faithfulness → không phát hiện hallucination | Score cao nhưng response có fabricated info (VD: cite non-existent document, invent numbers). Manual check thấy issue nhưng metric không bắt | Metric misleading, ship buggy RAG. User lose trust khi phát hiện hallucination | Dùng RAGAS 4 metrics: Faithfulness (answer faithful to context?), Answer Relevancy (answer đáp ứng question?), Context Precision (retrieved context relevant?), Context Recall (did we retrieve all relevant docs?) | **Rất Cao** | Single metric → incomplete picture |
| 4 | Trace chỉ log input/output, không trace từng bước | Log chỉ có {question, response}, không biết retrieval lấy gì, reranker làm gì, generation consume bao lâu | Khi response tệ, không biết fix ở đâu. Latency 5s nhưng không biết bottleneck (retrieval? embedding? generation?) | Trace mỗi step: query_embedding → retrieval (top-5) → reranking (top-3) → prompt_construction → generation (token by token). Dùng Langfuse SDK | **Cao** | Debugging blind nếu không trace step-by-step |
| 5 | Không track latency breakdown → không biết bottleneck ở đâu | API response chậm, nhưng không biết đó là vLLM slow hay Qdrant slow hay embedding slow | Không biết optimize cái gì. Có thể waste time optimize non-bottleneck component | Track latency per step: `embedding_time`, `retrieval_time`, `reranking_time`, `generation_time`. Bar chart show breakdown | **Trung Bình** | Performance optimization cần data |
| 6 | A/B test bằng cảm giác thay vì metrics | "Cảm giác prompt v2 tốt hơn v1". Deploy v2. User report quality giảm | Subjective judgement sai. Có thể v1 objective-wise tốt hơn nhưng cảm giác v2 hơn (bias) | Test 2 config trên chung eval dataset, so sánh metrics. VD: `avg_faithfulness(v1) = 0.82 vs v2 = 0.79` → v1 better | **Cao** | Metric-driven >> gut-feeling |
| 7 | Không lưu eval results history → không thấy improvement over time | Chạy eval hôm nay, kết quả 0.75. Tuần sau chạy lại, kết quả 0.80. Không biết là lợi ích từ config nào | Không track progress, không biết "sprint này cải thiện bao nhiêu?" | Lưu mỗi eval run: timestamp, config, metrics. Build dashboard (Langfuse + custom chart) show trend over time | **Trung Bình** | Progress tracking motivates team, guides roadmap |
| 8 | Ground truth trong eval dataset sai/thiếu → metric cao nhưng thực tế RAG sai | Ground truth: "Python là ngôn ngữ lập trình". RAG trả: "Python là loài rắn". Metric: high relevancy (từ khóa "Python" match). Nhưng answer sai hoàn toàn | Metric misleading, ground truth garbage → evaluation garbage. High false confidence | Quality check eval dataset: 2-3 người review từng cặp, flag ambiguous cases. Document rationale cho ground truth | **Rất Cao** | Eval dataset quality = foundation of everything |

---

## Hands-On Exercise: 3 Phase

### Phase 1: Langfuse Integration (Thứ 5)

**Mục tiêu:** Setup Langfuse self-hosted, integrate SDK vào RAG pipeline để trace mỗi step.

#### Step 1.1: Setup Langfuse Docker

```yaml
# docker-compose.yml (add to existing)
services:
  langfuse-postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: langfuse
      POSTGRES_DB: langfuse
    volumes:
      - langfuse_postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  langfuse:
    image: langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: "postgresql://langfuse:password@langfuse-postgres:5432/langfuse"
      NEXTAUTH_SECRET: "test-secret-key-do-not-use-in-production"
      NEXTAUTH_URL: "http://localhost:3000"
    depends_on:
      - langfuse-postgres

volumes:
  langfuse_postgres:
```

```bash
docker-compose up langfuse langfuse-postgres -d
# Wait 30s for startup
# Open http://localhost:3000 in browser, create account
```

#### Step 1.2: Integrate Langfuse SDK into RAG Pipeline

```bash
pip install langfuse
```

**Updated main.py:**

```python
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import httpx
import jinja2
import time
from langfuse import Langfuse

# Initialize Langfuse
langfuse = Langfuse(
    public_key="pk_....",  # Get from Langfuse UI
    secret_key="sk_....",  # Get from Langfuse UI
    host="http://localhost:3000"
)

app = FastAPI()

# Load models
embedding_model = SentenceTransformer("bge-m3")
qdrant = QdrantClient(url="http://localhost:6333", api_key="test-api-key")
vllm_client = httpx.AsyncClient(base_url="http://localhost:8000")
env = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))
prompt_template = env.get_template("rag_prompt.j2")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    similarity_threshold: float = 0.3

@app.post("/query")
async def query(req: QueryRequest):
    # Create trace for this request
    trace = langfuse.trace(
        name="rag_query",
        input={"question": req.question},
        user_id="user_123"  # Replace with real user ID in production
    )

    start_time = time.time()

    # Step 1: Embed query
    embedding_start = time.time()
    query_embedding = embedding_model.encode(
        req.question, convert_to_tensor=False
    ).tolist()
    embedding_time = time.time() - embedding_start

    trace.span(
        name="embedding",
        input={"question": req.question},
        output={"embedding_dim": len(query_embedding)},
        duration_ms=embedding_time * 1000
    )

    # Step 2: Retrieve from Qdrant
    retrieval_start = time.time()
    search_result = qdrant.search(
        collection_name="rag_documents",
        query_vector=query_embedding,
        limit=req.top_k,
        score_threshold=req.similarity_threshold
    )
    retrieval_time = time.time() - retrieval_start

    trace.span(
        name="retrieval",
        input={"query_embedding_dim": len(query_embedding), "top_k": req.top_k},
        output={
            "chunks_retrieved": len(search_result),
            "top_score": search_result[0].score if search_result else 0
        },
        duration_ms=retrieval_time * 1000
    )

    # Step 3: Handle no results
    if not search_result:
        trace.span(
            name="no_context_handler",
            output={"message": "no_relevant_context"},
            duration_ms=1
        )
        response_text = "Xin lỗi, tôi không tìm thấy thông tin liên quan."
        trace.update(
            output={"response": response_text},
            metadata={"retrieval_success": False}
        )
        return {
            "response": response_text,
            "sources": [],
            "metadata": {"chunks_found": 0}
        }

    # Step 4: Extract context
    retrieved_chunks = []
    source_refs = []
    for hit in search_result:
        chunk_text = hit.payload.get("text", "")
        doc_name = hit.payload.get("document_name", "unknown")
        chunk_idx = hit.payload.get("chunk_index", 0)
        retrieved_chunks.append(chunk_text)
        source_refs.append({
            "document": doc_name,
            "chunk_id": chunk_idx,
            "score": hit.score
        })

    # Step 5: Prompt construction
    context = "\n\n".join(retrieved_chunks)
    prompt = prompt_template.render(
        question=req.question,
        context=context,
        max_length=200
    )

    trace.span(
        name="prompt_construction",
        input={"context_length": len(context)},
        output={"prompt_length": len(prompt)},
        duration_ms=1
    )

    # Step 6: Call vLLM
    generation_start = time.time()
    response = await vllm_client.post(
        "/v1/chat/completions",
        json={
            "model": "qwen2.5",
            "messages": [
                {"role": "system", "content": "You are a helpful Vietnamese AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
            "temperature": 0.3,
        }
    )
    generation_time = time.time() - generation_start

    response_data = response.json()
    generated_text = response_data["choices"][0]["message"]["content"]

    trace.span(
        name="generation",
        input={"prompt_length": len(prompt)},
        output={"response_length": len(generated_text)},
        duration_ms=generation_time * 1000
    )

    # Update trace with final result
    total_time = time.time() - start_time
    trace.update(
        output={
            "response": generated_text,
            "sources": source_refs,
            "latency_breakdown": {
                "embedding_ms": embedding_time * 1000,
                "retrieval_ms": retrieval_time * 1000,
                "generation_ms": generation_time * 1000,
                "total_ms": total_time * 1000
            }
        },
        metadata={
            "chunks_retrieved": len(search_result),
            "top_retrieval_score": search_result[0].score,
            "model": "qwen2.5"
        }
    )

    return {
        "response": generated_text,
        "sources": source_refs,
        "metadata": {
            "retrieval_score": search_result[0].score,
            "chunks_found": len(search_result),
            "latency_ms": total_time * 1000
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Yêu cầu đạt:**
- ✅ Langfuse UI accessible tại http://localhost:3000
- ✅ After querying `/query`, traces appear in Langfuse dashboard
- ✅ Each trace có ≥ 5 spans: embedding, retrieval, prompt_construction, generation, latency_breakdown
- ✅ Screenshot Langfuse trace detail (show latency breakdown)

---

### Phase 2: RAGAS Evaluation (Thứ 5-6)

**Mục tiêu:** Tạo eval dataset, chạy RAGAS 4 metrics, analyze results.

#### Step 2.1: Create Eval Dataset

File `eval_dataset.json`:

```json
[
  {
    "question": "Qwen 2.5 là mô hình ngôn ngữ nào của công ty nào?",
    "ground_truth": "Qwen 2.5 là mô hình ngôn ngữ (LLM) được phát triển bởi Alibaba. Đó là phiên bản cải tiến của Qwen 2, với khả năng xử lý tốt hơn cho các tác vụ lập trình và reasoning.",
    "contexts": [
      "Qwen 2.5 được phát triển bởi Alibaba Cloud. Mô hình này được tối ưu hóa cho các tác vụ lập trình, reasoning, và xử lý ngôn ngữ tự nhiên.",
      "Qwen 2.5 là phiên bản mới nhất của dòng mô hình Qwen. So với Qwen 2, Qwen 2.5 có khả năng coding tốt hơn và context window lên tới 32K token."
    ]
  },
  {
    "question": "Làm thế nào để setup FastAPI server?",
    "ground_truth": "Để setup FastAPI server, bạn cần: 1) pip install fastapi uvicorn, 2) Viết code: from fastapi import FastAPI; app = FastAPI(); @app.get('/'); async def read_root(): return {'Hello': 'World'}, 3) Chạy: uvicorn main:app --reload --port 8000",
    "contexts": [
      "FastAPI là framework Python hiện đại để xây dựng API. Để bắt đầu: cài đặt fastapi và uvicorn, viết endpoint, chạy bằng lệnh uvicorn main:app.",
      "Ví dụ FastAPI minimal: from fastapi import FastAPI; app = FastAPI(); @app.get('/'); async def root(): return {'msg': 'Hello'}. Chạy bằng: uvicorn main:app --reload"
    ]
  },
  {
    "question": "Docker Compose dùng để làm gì?",
    "ground_truth": "Docker Compose là tool định nghĩa và chạy nhiều Docker container cùng lúc bằng file YAML. Nó cho phép bạn định nghĩa services, networks, volumes trong 1 file docker-compose.yml và start tất cả bằng 1 lệnh 'docker-compose up'.",
    "contexts": [
      "Docker Compose giúp orchestrate nhiều containers. Bạn viết docker-compose.yml với services, mỗi service tương ứng 1 container image. Lệnh 'docker-compose up' sẽ start tất cả.",
      "Tại sao dùng Docker Compose? Nó giúp manage dependencies giữa containers, setup networks, volumes, environment variables tự động. Develop local dễ giống production."
    ]
  },
  # ... add 17 more test cases total 20
]
```

**Quality Checklist cho Eval Dataset:**
- [ ] 20+ test cases cover ≥ 3 categories (technical, conceptual, procedural)
- [ ] Ground truth là 1-3 sentences đầy đủ thông tin (không abbreviate)
- [ ] Contexts là 2+ relevant paragraphs từ documents
- [ ] Không có typo hoặc unclear language trong ground truth
- [ ] 2-3 người review từng cặp, vote "pass/fail"

#### Step 2.2: Run RAGAS Evaluation

```bash
pip install ragas
```

```python
# evaluate_ragas.py
import json
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

# Load eval dataset
with open("eval_dataset.json") as f:
    eval_data = json.load(f)

# Convert to RAGAS format
ragas_data = {
    "question": [item["question"] for item in eval_data],
    "answer": [],  # Will be filled by RAG system
    "ground_truth": [item["ground_truth"] for item in eval_data],
    "contexts": [item["contexts"] for item in eval_data]
}

# Generate answers from RAG system
import httpx
for q in ragas_data["question"]:
    response = httpx.post(
        "http://localhost:8001/query",
        json={"question": q}
    ).json()
    ragas_data["answer"].append(response["response"])

# Convert to Dataset
dataset = Dataset.from_dict(ragas_data)

# Evaluate
scores = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ],
    llm=langfuse_compatible_llm,  # Use vLLM or local LLM
    embeddings=embedding_model
)

# Save results
results = {
    "eval_dataset_size": len(eval_data),
    "timestamp": str(datetime.now()),
    "metrics": {
        "faithfulness": scores["faithfulness"],
        "answer_relevancy": scores["answer_relevancy"],
        "context_precision": scores["context_precision"],
        "context_recall": scores["context_recall"],
        "average": (scores["faithfulness"] + scores["answer_relevancy"]
                    + scores["context_precision"] + scores["context_recall"]) / 4
    },
    "per_sample": [
        {
            "question": q,
            "faithfulness": scores["faithfulness"][i],
            "answer_relevancy": scores["answer_relevancy"][i],
            "context_precision": scores["context_precision"][i],
            "context_recall": scores["context_recall"][i]
        }
        for i, q in enumerate(ragas_data["question"])
    ]
}

with open("eval_results_baseline.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Evaluation Complete")
print(f"Average Score: {results['metrics']['average']:.3f}")
print(f"Faithfulness: {results['metrics']['faithfulness']:.3f}")
print(f"Answer Relevancy: {results['metrics']['answer_relevancy']:.3f}")
print(f"Context Precision: {results['metrics']['context_precision']:.3f}")
print(f"Context Recall: {results['metrics']['context_recall']:.3f}")
```

**Understanding RAGAS Metrics:**

| Metric | Definition | Ideal Range | What It Detects |
|--------|-----------|-------------|-----------------|
| **Faithfulness** | Does answer follow from context? (not hallucinated) | 0.7-1.0 | Hallucination detection |
| **Answer Relevancy** | Does answer actually answer the question? | 0.7-1.0 | Off-topic answers |
| **Context Precision** | Are all retrieved contexts relevant to question? | 0.7-1.0 | Retrieval quality (low recall false positives) |
| **Context Recall** | Did we retrieve all documents needed to answer? | 0.7-1.0 | Retrieval coverage (did we miss important docs?) |

**Yêu cầu đạt:**
- ✅ `eval_results_baseline.json` created with all 4 metrics
- ✅ Average score calculated
- ✅ Per-sample scores documented
- ✅ Screenshot RAGAS report

---

### Phase 3: A/B Test & Improvement (Thứ 6-7)

**Mục tiêu:** Test 2+ configuration variants, compare metrics, choose best one.

#### Step 3.1: Setup A/B Testing Variants

**Variant A (Baseline):** chunk_size=500, no reranker

**Variant B:** chunk_size=800, with BGE-reranker

**Variant C:** chunk_size=400, embedding model = OpenAI (different embedder)

```python
# ab_test_config.py
VARIANTS = {
    "A_baseline": {
        "chunk_size": 500,
        "chunk_overlap": 50,
        "embedding_model": "bge-m3",
        "retrieval_top_k": 5,
        "use_reranker": False,
        "reranker_top_k": None,
    },
    "B_larger_chunks_reranker": {
        "chunk_size": 800,
        "chunk_overlap": 100,
        "embedding_model": "bge-m3",
        "retrieval_top_k": 8,  # Retrieve more, then rerank
        "use_reranker": True,
        "reranker_top_k": 5,
    },
    "C_small_chunks": {
        "chunk_size": 400,
        "chunk_overlap": 50,
        "embedding_model": "bge-m3",
        "retrieval_top_k": 5,
        "use_reranker": False,
        "reranker_top_k": None,
    }
}
```

#### Step 3.2: Create Per-Variant RAG Pipeline

Refactor `main.py` để accept config:

```python
from ab_test_config import VARIANTS

class RAGPipeline:
    def __init__(self, variant_name: str):
        self.config = VARIANTS[variant_name]
        self.embedding_model = SentenceTransformer(self.config["embedding_model"])

        if self.config["use_reranker"]:
            from sentence_transformers.cross_encoders import CrossEncoder
            self.reranker = CrossEncoder('bge-reranker-large')
        else:
            self.reranker = None

    async def query(self, question: str):
        # Embedding
        query_embedding = self.embedding_model.encode(question).tolist()

        # Retrieval
        results = qdrant.search(
            collection_name="rag_documents",
            query_vector=query_embedding,
            limit=self.config["retrieval_top_k"]
        )

        # Reranking (if enabled)
        if self.reranker:
            pairs = [[question, hit.payload["text"]] for hit in results]
            scores = self.reranker.predict(pairs)
            # Sort by reranker score
            results = [r for _, r in sorted(zip(scores, results), reverse=True)][:self.config["reranker_top_k"]]

        # Rest of pipeline...
        # (embedding → retrieval → reranking → prompt → generation)

# Setup 3 pipelines
pipeline_a = RAGPipeline("A_baseline")
pipeline_b = RAGPipeline("B_larger_chunks_reranker")
pipeline_c = RAGPipeline("C_small_chunks")

@app.post("/query/{variant}")
async def query(variant: str, req: QueryRequest):
    pipeline = {"A": pipeline_a, "B": pipeline_b, "C": pipeline_c}[variant]
    return await pipeline.query(req.question)
```

#### Step 3.3: Run RAGAS on Each Variant

```python
# run_ab_test.py
import json
from datetime import datetime

ab_results = {}

for variant_name in ["A_baseline", "B_larger_chunks_reranker", "C_small_chunks"]:
    print(f"\n🧪 Testing {variant_name}...")

    # Generate answers using variant
    answers = []
    for q in ragas_data["question"]:
        response = httpx.post(
            f"http://localhost:8001/query/{variant_name[0]}",
            json={"question": q}
        ).json()
        answers.append(response["response"])

    # Evaluate
    dataset = Dataset.from_dict({
        "question": ragas_data["question"],
        "answer": answers,
        "ground_truth": ragas_data["ground_truth"],
        "contexts": ragas_data["contexts"]
    })

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=llm_eval,
        embeddings=embedding_model
    )

    ab_results[variant_name] = {
        "config": VARIANTS[variant_name],
        "metrics": {
            "faithfulness": float(scores["faithfulness"]),
            "answer_relevancy": float(scores["answer_relevancy"]),
            "context_precision": float(scores["context_precision"]),
            "context_recall": float(scores["context_recall"]),
            "average": float((scores["faithfulness"] + scores["answer_relevancy"]
                             + scores["context_precision"] + scores["context_recall"]) / 4)
        }
    }

    print(f"  ✅ Average Score: {ab_results[variant_name]['metrics']['average']:.3f}")

# Save results
with open("ab_test_results.json", "w") as f:
    json.dump(ab_results, f, indent=2)

# Print comparison table
print("\n" + "="*80)
print("A/B Test Summary")
print("="*80)
for variant, result in ab_results.items():
    print(f"\n{variant}:")
    print(f"  Avg Score:        {result['metrics']['average']:.3f}")
    print(f"  Faithfulness:     {result['metrics']['faithfulness']:.3f}")
    print(f"  Answer Relevancy: {result['metrics']['answer_relevancy']:.3f}")
    print(f"  Context Precision:{result['metrics']['context_precision']:.3f}")
    print(f"  Context Recall:   {result['metrics']['context_recall']:.3f}")
```

**Yêu cầu đạt:**
- ✅ Test 2+ variants, min 3
- ✅ `ab_test_results.json` with all metrics for each variant
- ✅ Determine winner (highest avg score)
- ✅ Screenshot comparison table

---

## Output Deliverables

### ✅ Deliverable 1: GitHub Repository (Extended from 2.1)

Push code to `evaluation-loop` branch:

```
evaluation-loop/
├── docker-compose.yml                    # Add Langfuse services
├── main.py                               # With Langfuse tracing, variant support
├── ingest_documents.py                   # From 2.1
├── ab_test_config.py                     # Config variants A/B/C
├── evaluate_ragas.py                     # RAGAS evaluation script
├── run_ab_test.py                        # A/B test runner
├── eval_dataset.json                     # 20+ test cases (quality checked)
├── eval_results_baseline.json            # RAGAS results for baseline
├── ab_test_results.json                  # A/B comparison results
├── AVOIDANCE_TABLE.md                    # 6+/8 mistake avoidance
├── EVALUATION_REPORT.md                  # Full report (see below)
├── .env                                  # Langfuse keys
├── requirements.txt                      # +langfuse, +ragas
└── README.md                             # Updated setup & eval instructions
```

**Docker requirement:** `docker-compose up` phải chạy ≥ 6 services (Qdrant, vLLM, Embedding, FastAPI, Langfuse, PostgreSQL).

### ✅ Deliverable 2: AVOIDANCE_TABLE.md

Chứng minh ≥ 6/8 mistakes được handle:

```markdown
# Evaluation Loop: Avoidance of Common Mistakes

| # | Mistake | Status | Evidence |
|---|---------|--------|----------|
| 1 | Have eval dataset | ✅ | eval_dataset.json: 20 test cases |
| 2 | Eval dataset ≥ 10 cases | ✅ | Same file: 20 cases (not 10) |
| 3 | Multiple metrics (not just accuracy) | ✅ | RAGAS: Faithfulness, Answer Relevancy, Context Precision, Context Recall |
| 4 | Trace each step | ✅ | Langfuse spans: embedding, retrieval, reranking, prompt_construction, generation |
| 5 | Track latency breakdown | ✅ | Langfuse: duration_ms per span, latency_breakdown in response |
| 6 | A/B test with metrics | ✅ | ab_test_results.json: 3 variants, all 4 metrics compared |
| 7 | Save eval history | ⏳ | Partial: Single run saved; future work = track runs over time |
| 8 | Quality-check ground truth | ✅ | eval_dataset.json: 2 reviewers approved all 20 cases |
```

### ✅ Deliverable 3: EVALUATION_REPORT.md

Detailed markdown report:

```markdown
# RAG Evaluation Report — Week 2 Exercise 2.2

## Executive Summary

- **Baseline Config:** chunk_size=500, no reranker
- **Best Config:** B_larger_chunks_reranker (avg score 0.81 vs 0.78 baseline)
- **Improvement:** +3.8% RAGAS score
- **Recommendation:** Deploy Variant B for production

## 1. Evaluation Dataset

- **Size:** 20 test cases
- **Categories:** 7 technical, 8 conceptual, 5 procedural
- **Quality:** 3/3 reviewers approved all 20 cases
- **Coverage:** Diverse domains (FastAPI, Docker, LLM concepts, RAG techniques)

### Sample Cases
| Q# | Question | Ground Truth Length | Contexts Count |
|----|-----------|--------------------|-----------------|
| 1 | Qwen 2.5 là gì? | 45 words | 2 docs |
| 2 | Setup FastAPI? | 38 words | 2 docs |
| ... | | | |

## 2. RAGAS Metrics (Baseline: Variant A)

| Metric | Score | Interpretation |
|--------|-------|-----------------|
| Faithfulness | 0.82 | 82% of answers grounded in context (good) |
| Answer Relevancy | 0.75 | 75% of answers relevant to question (acceptable) |
| Context Precision | 0.79 | 79% of retrieved contexts relevant (good) |
| Context Recall | 0.76 | 76% coverage of required context (acceptable) |
| **Average** | **0.78** | **Overall: Good** |

### Per-Sample Breakdown
Lowest scores (focus areas for improvement):
- Q8: faithfulness 0.65 (answer slightly hallucinated, missing "Alibaba")
- Q15: answer_relevancy 0.58 (answered related but not direct question)

## 3. Latency Breakdown (Langfuse Trace Analysis)

Average latency per request (Variant A, n=20 queries):
- Embedding: 120ms
- Retrieval: 45ms
- Prompt Construction: 2ms
- Generation: 850ms
- **Total: 1017ms (1.0 second)**

Bottleneck: Generation (84% of total time) — expected, due to LLM inference.

## 4. A/B Test Results

### Metrics Comparison

| Variant | Avg Score | Faithfulness | Answer Rel. | Context Prec. | Context Rec. | Avg Latency |
|---------|-----------|--------------|-------------|---------------|--------------|-------------|
| A (baseline) | 0.780 | 0.82 | 0.75 | 0.79 | 0.76 | 1017ms |
| B (reranker) | **0.815** | **0.85** | **0.81** | **0.81** | **0.79** | 1180ms |
| C (small chunks) | 0.752 | 0.78 | 0.71 | 0.77 | 0.74 | 945ms |

### Winner: Variant B (chunk_size=800 + reranker)
- **+3.8% avg score** vs baseline
- **+3% faithfulness** (better hallucination prevention)
- **+6% answer relevancy** (more direct answers)
- **+2% context precision/recall** (better retrieval)
- Trade-off: +163ms latency (acceptable for quality gain)

### Variant C Analysis
- Fastest (945ms), but **lowest quality** (0.752 avg)
- Too-small chunks (400 tokens) lose semantic coherence
- Not recommended for production

## 5. Lessons Learned & Recommendations

### Key Findings
1. **Larger chunks + reranking > larger chunks alone** → reranker crucial for quality
2. **Smaller chunks faster but lower quality** → trade-off must be explicit
3. **Faithfulness is main concern** (8 cases with hallucination) → need better prompt or retrieval
4. **Answer Relevancy varies** → some queries need clarification prompting

### Action Items
- ✅ Deploy Variant B to staging
- ⏳ Investigate Q8 & Q15 failures for prompt improvement
- ⏳ Consider using reranker that costs less (BGE vs commercial)
- ⏳ Track metrics weekly, set threshold (min 0.80 avg)

## 6. Next Steps

- Monitor Variant B in staging (1 week)
- Collect real user feedback on response quality
- Iterate on prompt based on failure analysis
- Re-run eval monthly with new test cases
```

### ✅ Deliverable 4: 5-Minute Demo Video

Record demo (~5 minutes):

1. **(30s)** Show Langfuse dashboard: open http://localhost:3000, show traces for 1-2 queries with latency breakdown
2. **(1m)** RAGAS evaluation: run script, show scores loading, final metrics printed
3. **(1.5m)** A/B comparison: show ab_test_results.json or markdown table, explain winner & why
4. **(1m)** Code walkthrough: highlight key sections (reranker integration, Langfuse SDK usage, RAGAS metric setup)
5. **(1m)** Conclusion: lessons learned, what you'd do differently next time

---

## Peer Review

**Checklist:**
- [ ] Repo can be cloned & docker-compose up works (6+ services)
- [ ] Langfuse accessible, contains ≥ 20 traces with step details
- [ ] `eval_dataset.json` has ≥ 20 test cases, quality checked
- [ ] RAGAS scores calculated, all 4 metrics present
- [ ] A/B test results documented, clear winner identified
- [ ] AVOIDANCE_TABLE covers ≥ 6/8 mistakes
- [ ] EVALUATION_REPORT professional, actionable
- [ ] Video demo clear, covers all 3 phases

---

## Evaluation Rubric

| Criteria | Weight | Excellent | Good | Needs Work |
|----------|--------|-----------|------|------------|
| **Phase 1: Langfuse Integration** | 25% | All steps traced, latency breakdown complete, 20+ traces | 3/4 steps traced, latency partial | <2 steps traced |
| **Phase 2: RAGAS Evaluation** | 30% | 20+ eval cases, all 4 metrics, per-sample analysis | 15+ cases, 3/4 metrics | <15 cases, <3 metrics |
| **Phase 3: A/B Test** | 25% | 3+ variants, clear winner, recommendation justified | 2 variants, comparison shown | 1 variant only |
| **Documentation** | 15% | Report detailed, actionable, professional | Report adequate, some sections | Minimal documentation |
| **Code Quality** | 5% | Clean, well-commented, easy to extend | Mostly clean | Messy, hard to follow |

**Passing:** ≥ 70% (14/20 points)

---

## Tips & Tricks

1. **RAGAS Model Selection:** RAGAS cần LLM cho evaluation (default: OpenAI). Để self-hosted:
   ```python
   from langfuse.callback import CallbackHandler
   scores = evaluate(
       dataset,
       metrics=[...],
       llm=vllm_local_llm,  # Use your vLLM instance
       embeddings=embedding_model
   )
   ```

2. **Reranker Cost:** BGE-reranker-large (1.7B params) có thể heavy. Alternative: BGE-reranker-small (380M, 95% quality).

3. **Langfuse Free Tier:** Langfuse Cloud = free 1M traces/month. Self-hosted = unlimited, but need PostgreSQL management.

4. **Eval Dataset Quality:** Ground truth sai = garbage metrics. Spend 1-2 hours reviewing 20 cases properly; it saves 10 hours of debugging later.

5. **A/B Test Statistical Significance:** Với 20 cases:
   - Difference < 2% = not significant (could be noise)
   - Difference > 5% = significant
   - Difference 2-5% = investigate further

6. **Latency Breakdown:** If generation is bottleneck (usual case), can't optimize retrieval much. Focus on prompt quality instead.

---

## Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [RAGAS GitHub](https://github.com/explodinggradients/ragas)
- [BGE Reranker Models](https://huggingface.co/BAAI/bge-reranker-large)
- [RAG Evaluation Best Practices](https://langfuse.com/docs/guides/rag-evaluation)

---

**Deadline:** Cuối thứ 6-7 tuần này (sau khi nhận bài vào thứ 5).
**Questions?** Post lên Discord #week2-exercises hoặc schedule 1:1 với instructor.
