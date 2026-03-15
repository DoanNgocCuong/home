
# Bài 2.1 — RAG End-to-End: Từ Document đến Response

**Hạn nộp:** Cuối thứ 4 tuần này (học từ thứ 2)

## Mục tiêu Bài Tập

Xây dựng **RAG pipeline hoàn chỉnh** sử dụng embedding model + vector DB + LLM đã host từ bài 1.2. Sau bài này, bạn sẽ biết cách:

- Parse và chunking documents thông minh (không quá to, không quá nhỏ)
- Generate embeddings bằng multilingual model (hỗ trợ tiếng Việt)
- Store + retrieve vectors từ Qdrant hiệu quả
- Integrate vLLM generation với retrieval result
- Trả response kèm source references (để avoid hallucination perception)

**Level:** Intermediate — Đã quen Docker + FastAPI từ Week 1.

---

## Prerequisite

✅ Docker Compose chạy từ bài 1.2 (vLLM + Qwen 2.5)
✅ FastAPI baseline từ bài 1.1
✅ Hiểu cơ bản về embeddings và vector similarity
✅ Có 10+ documents test (PDF hoặc markdown) về một chủ đề (ví dụ: AI safety, Python best practices, etc.)

---

## Tech Stack

| Component | Tool | Chú thích |
|-----------|------|----------|
| Vector DB | Qdrant (Docker) | Self-hosted, dễ setup |
| Embedding Model | BGE-M3 hoặc sentence-transformers | Hỗ trợ tiếng Việt, multilingual |
| Generation Model | vLLM + Qwen 2.5 (từ bài 1.2) | Existing inference server |
| API Layer | FastAPI | Extend từ bài 1.1 |
| Document Parsing | PyPDF2 hoặc python-docx | Parse PDF/Word docs |
| Chunking | LangChain RecursiveCharacterTextSplitter | Config flexible |

---

## Bảng Các Sai Lầm Thường Gặp (8 Lỗi Fresher)

| # | Sai Lầm | Ví Dụ | Hậu Quả | Cách Sửa | Mức Độ Ảnh Hưởng | Dẫn Chứng |
|---|--------|-------|--------|----------|-----------------|----------|
| 1 | Chunk quá lớn (>1000 tokens) hoặc quá nhỏ (<100 tokens) | Chunk 1500+ tokens, hoặc sentence-level chunks 20 từ | Quá lớn: retrieve nhiều noise, prompt context window vượt. Quá nhỏ: mất semantic coherence, retrieve 50+ chunks cho 1 query | Dùng `RecursiveCharacterTextSplitter(chunk_size=400-600, chunk_overlap=50)`. Test chunk size bằng eval metrics | **Cao** | Qwen 2.5 context 32K nhưng retrieval >10K chunks = chậm, và retrieval <5 tokens = không có ý nghĩa |
| 2 | Dùng embedding model không hỗ trợ tiếng Việt | Chọn `sentence-transformers/all-MiniLM-L6-v2` (English-only) cho Vietnamese docs | Embedding quality tệ, retrieval sai hoàn toàn (VD: query "bảo mật" không match document tiếng Việt về security) | Dùng `bge-m3` hoặc `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`. Test NDCG@5 trên Vietnamese dataset | **Rất Cao** | Embedding model English-only có 99% mismatch với Vietnamese semantic |
| 3 | Không có overlap giữa chunks → mất context ở biên | Chunk mỗi 512 tokens, không overlap. Một câu quan trọng bị split giữa 2 chunks | Retrieval bị thiếu context cần thiết ở điểm giao tiếp chunks. VD: "Cách 1 là..., Cách 2 là..." bị split thành "Cách 1 là ..." | "..." | Thiết lập `chunk_overlap=50-100` tokens. Verify bằng cách print từng chunk và kiểm tra semantic integrity | **Trung Bình** | Biên chunks thường chứa transition words quan trọng |
| 4 | Hardcode prompt thay vì dùng template file | System message + prompt được viết cứng trong Python code | Khó maintain, khó A/B test prompt. Mỗi lần thay prompt phải deploy lại | Dùng Jinja2 template file hoặc config YAML. Load lúc startup, re-render cho mỗi query với variables | **Trung Bình** | Prompt engineering là iterative, nên cần flexibility |
| 5 | Không handle "không tìm thấy context liên quan" → hallucination | Retrieve được 0 chunks, nhưng vẫn generate response từ LLM training data | LLM sẽ "confabulate" (bịa đặt) thông tin, user nhận được wrong answer với confident tone | Kiểm tra: `if len(retrieved_chunks) == 0 or avg_similarity < 0.3: return {response: "Không tìm thấy thông tin liên quan", source: []}`. Hoặc prompt LLM: "Nếu context không cung cấp đủ thông tin, hãy nói 'Tôi không biết' thay vì đoán" | **Rất Cao** | Hallucination là #1 issue trong production RAG systems |
| 6 | Trả response không kèm source/reference | API trả chỉ `{response: "..."}` không có `source` | User không biết information từ đâu, không thể verify. Độ tin cậy giảm dù RAG đúng | Luôn return: `{response: "...", sources: [{document: "file.pdf", chunk_id: 3, page: 5}, ...]}`. Client có thể highlight source trong UI | **Cao** | Source transparency là best practice trong RAG, giúp user verify |
| 7 | Load embedding model mỗi request → chậm, lãng phí resource | `model = SentenceTransformer('bge-m3')` được gọi trong request handler | Mỗi request mất 3-5 giây chỉ để load model từ disk. Tổng latency 5-10s cho một query (không chấp nhận được) | Load model 1 lần khi FastAPI startup, lưu vào global variable hoặc dependency injection. Dùng `@lru_cache` nếu test nhiều model | **Rất Cao** | Embedding model load lần đầu là bottleneck lớn nhất |
| 8 | Không metadata filtering → search toàn bộ vector DB cho mọi query | Retrieve top-5 từ 100K vectors mỗi query, không filter theo category/date | Query cụ thể ("documents từ 2024") nhưng kết quả lẫn lộn những documents cũ. Latency cao vì phải scan toàn bộ | Thêm metadata vào Qdrant (document_id, source, date, category). Query dùng filter: `retrieve(query, filter={'date': {'gte': '2024-01-01'}})` | **Trung Bình** | Cần khi dataset lớn (10K+ documents) |

---

## Hands-On Exercise: 3 Phase

### Phase 1: Offline Document Ingestion (Thứ 2-3)

**Mục tiêu:** Parse 10+ documents → chunk thông minh → embed → lưu vào Qdrant.

**Step 1.1: Setup Qdrant Docker**

```yaml
# docker-compose.yml (thêm vào existing từ bài 1.2)
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      QDRANT_API_KEY: "test-api-key"

volumes:
  qdrant_storage:
```

```bash
docker-compose up qdrant -d
# Verify: curl http://localhost:6333/health
```

**Step 1.2: Build Ingestion Script**

```python
# ingest_documents.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
import PyPDF2
import hashlib
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load embedding model (multilingual, hỗ trợ Việt)
embedding_model = SentenceTransformer("bge-m3")  # 1024-dim vectors
qdrant = QdrantClient(url="http://localhost:6333", api_key="test-api-key")

# Initialize Qdrant collection
collection_name = "rag_documents"
try:
    qdrant.get_collection(collection_name)
except:
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )

# Chunking config
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

# Ingest documents
documents_dir = Path("./documents")
point_id = 0
points_batch = []

for doc_path in documents_dir.glob("*.pdf"):  # or *.md
    print(f"Processing {doc_path.name}")

    # Parse document
    if doc_path.suffix == ".pdf":
        with open(doc_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "".join([page.extract_text() for page in reader.pages])
    else:  # markdown
        text = doc_path.read_text()

    # Chunk text
    chunks = splitter.split_text(text)

    for chunk_idx, chunk in enumerate(chunks):
        # Generate embedding
        embedding = embedding_model.encode(chunk, convert_to_tensor=False).tolist()

        # Create metadata
        metadata = {
            "document_name": doc_path.name,
            "chunk_index": chunk_idx,
            "text": chunk,
            "document_hash": hashlib.md5(doc_path.read_bytes()).hexdigest(),
        }

        # Create point for Qdrant
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=metadata
        )
        points_batch.append(point)
        point_id += 1

        # Upload in batches
        if len(points_batch) >= 32:
            qdrant.upsert(
                collection_name=collection_name,
                points=points_batch
            )
            points_batch = []

# Final batch
if points_batch:
    qdrant.upsert(collection_name=collection_name, points=points_batch)

print(f"✅ Ingested {point_id} chunks from {len(list(documents_dir.glob('*')))} documents")
```

**Yêu cầu đạt:**
- ✅ Chạy script, ingest 10+ documents (≥ 100 chunks total)
- ✅ Qdrant collection chứa metadata đầy đủ (document_name, chunk_index, text)
- ✅ Verify: `curl "http://localhost:6333/collections/rag_documents"` hiển thị point count

---

### Phase 2: Online Query + Generation (Thứ 4)

**Mục tiêu:** Build FastAPI endpoint `/query` → retrieve → generate → return response + sources.

```python
# main.py (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import httpx
import jinja2

app = FastAPI()

# Load models at startup
embedding_model = SentenceTransformer("bge-m3")
qdrant = QdrantClient(url="http://localhost:6333", api_key="test-api-key")
vllm_client = httpx.AsyncClient(base_url="http://localhost:8000")

# Load prompt template
env = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))
prompt_template = env.get_template("rag_prompt.j2")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    similarity_threshold: float = 0.3

class QueryResponse(BaseModel):
    response: str
    sources: list[dict]
    metadata: dict

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    # Step 1: Embed query
    query_embedding = embedding_model.encode(req.question, convert_to_tensor=False).tolist()

    # Step 2: Retrieve top-k chunks from Qdrant
    search_result = qdrant.search(
        collection_name="rag_documents",
        query_vector=query_embedding,
        limit=req.top_k,
        score_threshold=req.similarity_threshold
    )

    # Step 3: Handle no results
    if not search_result:
        return QueryResponse(
            response="Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở dữ liệu.",
            sources=[],
            metadata={"retrieval_score": 0, "chunks_found": 0}
        )

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

    # Step 5: Construct prompt using template
    context = "\n\n".join(retrieved_chunks)
    prompt = prompt_template.render(
        question=req.question,
        context=context,
        max_length=200
    )

    # Step 6: Call vLLM for generation
    response = await vllm_client.post(
        "/v1/chat/completions",
        json={
            "model": "qwen2.5",
            "messages": [
                {"role": "system", "content": "You are a helpful Vietnamese AI assistant. Answer based on the provided context."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
            "temperature": 0.3,
        }
    )

    response_data = response.json()
    generated_text = response_data["choices"][0]["message"]["content"]

    return QueryResponse(
        response=generated_text,
        sources=source_refs,
        metadata={
            "retrieval_score": search_result[0].score if search_result else 0,
            "chunks_found": len(search_result),
            "model": "qwen2.5"
        }
    )

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Template Jinja2:** `templates/rag_prompt.j2`

```jinja2
Bạn là một trợ lý AI hữu ích. Trả lời câu hỏi dựa trên context được cung cấp.
Nếu context không chứa đủ thông tin, hãy nói "Tôi không có thông tin về điều này".

Context:
{{ context }}

Câu hỏi: {{ question }}

Trả lời (tối đa {{ max_length }} từ):
```

**Yêu cầu đạt:**
- ✅ FastAPI server chạy trên port 8001 (hoặc port khác, không conflict vLLM 8000)
- ✅ POST `/query` trả response + sources
- ✅ Test: `curl -X POST http://localhost:8001/query -H "Content-Type: application/json" -d '{"question": "Câu hỏi test"}'`
- ✅ Source refs đầy đủ: document, chunk_id, similarity score

---

### Phase 3: Basic Evaluation (Thứ 5)

**Mục tiêu:** Tạo 10 test case, đánh giá response quality bằng tay (manual evaluation).

Tạo file `eval_dataset.json`:

```json
[
  {
    "question": "Qwen 2.5 là gì?",
    "expected_answer_keywords": ["language model", "Alibaba", "open source"],
    "expected_sources_count_min": 1
  },
  {
    "question": "Cách setup Docker Compose?",
    "expected_answer_keywords": ["docker-compose.yml", "services", "up"],
    "expected_sources_count_min": 1
  }
]
```

**Evaluation Script:**

```python
# evaluate.py
import json
import httpx
from collections import defaultdict

with open("eval_dataset.json") as f:
    test_cases = json.load(f)

results = defaultdict(list)

for i, test in enumerate(test_cases):
    response = httpx.post(
        "http://localhost:8001/query",
        json={"question": test["question"], "top_k": 5}
    ).json()

    # Manual eval metrics
    answer = response["response"].lower()
    sources_count = len(response["sources"])

    # Check keywords
    keywords_found = sum(
        1 for kw in test["expected_answer_keywords"]
        if kw.lower() in answer
    )

    # Log results
    results["pass" if keywords_found >= 2 else "fail"].append({
        "question": test["question"],
        "response": answer,
        "keywords_matched": keywords_found,
        "sources_count": sources_count,
        "expected_min": test["expected_sources_count_min"]
    })

    print(f"[{i+1}/10] {test['question']}")
    print(f"  → Keywords: {keywords_found}/3, Sources: {sources_count}\n")

print(f"\n📊 Summary: {len(results['pass'])} Pass, {len(results['fail'])} Fail")
```

**Yêu cầu đạt:**
- ✅ Chạy 10+ test cases
- ✅ Ghi lại: Question, Response, Keywords Match, Sources Count
- ✅ Tính Accuracy: `pass_count / total_count`
- ✅ Document kết quả trong `EVALUATION_RESULTS.md`

---

## Output Deliverables

### ✅ Deliverable 1: GitHub Repository

Push code lên GitHub (repo public), branch `rag-pipeline`:

```
rag-pipeline/
├── docker-compose.yml          # Qdrant + vLLM + Embedding svc
├── ingest_documents.py         # Document ingestion script
├── main.py                      # FastAPI /query endpoint
├── templates/
│   └── rag_prompt.j2          # Prompt template
├── documents/                  # 10+ test documents (PDF/MD)
├── eval_dataset.json          # 10+ test cases
├── evaluate.py                # Manual evaluation script
├── requirements.txt           # Dependencies
├── README.md                  # Setup & usage instructions
└── .env                       # (gitignore: API keys nếu có)
```

**Requirement chính:** `docker-compose up` phải chạy được 3 service (Qdrant + vLLM + FastAPI) mà không error.

### ✅ Deliverable 2: AVOIDANCE_TABLE.md

Tạo file `AVOIDANCE_TABLE.md` chứng minh bạn đã handle **ít nhất 6/8 sai lầm**:

```markdown
# RAG Pipeline: Avoidance of Common Mistakes

## Tracked Mistakes (6/8)

| # | Mistake | Status | Evidence |
|---|---------|--------|----------|
| 1 | Chunk size (400-600 tokens, 50 overlap) | ✅ | Line 35 ingest_documents.py: RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) |
| 2 | Multilingual embedding model | ✅ | Line 8 ingest_documents.py: SentenceTransformer("bge-m3") |
| 3 | Chunk overlap handling | ✅ | Same as #1, separators config ensures sentence boundary respect |
| 4 | Prompt templating | ✅ | templates/rag_prompt.j2 - Jinja2 template, loaded at startup in main.py line 20 |
| 5 | No-context handling | ✅ | main.py line 42-47: if not search_result, return explicit "không tìm thấy" message |
| 6 | Source references | ✅ | main.py line 53-59: source_refs contains document, chunk_id, similarity score for each result |
| 7 | Model caching | ✅ | main.py line 13-16: embedding_model & qdrant loaded at app startup, reused for all requests |
| 8 | Metadata filtering | ⏳ | Partial: payloads have document_name, chunk_index; full filter not implemented yet |

## Not Implemented
- #8 Metadata filtering: Future work - need more complex Qdrant filters for date/category
```

### ✅ Deliverable 3: 5-Minute Demo Video

Quay video demo (~5 phút) cho thấy:

1. **(30s)** Docker containers chạy: `docker-compose ps`
2. **(1m)** Ingest documents: chạy script, show Qdrant dashboard (vector count)
3. **(1.5m)** Query demo: submit 3-4 questions, show responses + sources
4. **(1m)** Show code structure: highlight key sections (template, no-context handling, caching)
5. **(1m)** Q&A và lessons learned

**Format:** MP4, up lên YouTube unlisted hoặc link vào README.

---

## Peer Review Vòng Tròn

**Quy trình:**
1. Nộp link GitHub + video vào sheet chung (do instructor cung cấp)
2. Mỗi bạn review 2 bạn khác (random assign)
3. Checklist review:

   - [ ] Repo có thể `git clone` được
   - [ ] `docker-compose up` chạy không error (3+ services)
   - [ ] POST `/query` trả response + sources
   - [ ] AVOIDANCE_TABLE cover ≥ 6/8 mistakes
   - [ ] Video demo rõ ràng, cover toàn bộ pipeline
   - [ ] Docs (README) đầy đủ, dễ follow

4. Comment trực tiếp trên GitHub Issues hoặc Google Sheet

---

## Evaluation Rubric

| Criteria | Weight | Excellent | Good | Needs Work |
|----------|--------|-----------|------|------------|
| **Phase 1: Ingestion** | 25% | 10+ docs, correct chunking, metadata complete | 8+ docs, mostly correct chunking | <8 docs, missing metadata |
| **Phase 2: RAG Pipeline** | 40% | All 3 steps work (retrieve→generate→return), sources included, template used, no-context handled | 2/3 steps work, sources sometimes missing | Only 1 step works, no sources |
| **Phase 3: Evaluation** | 15% | 10+ test cases, documented results, accuracy calculated | 5-9 test cases, partial documentation | <5 test cases |
| **Code Quality** | 15% | Clean, commented, follows style, easy to follow | Mostly clean, some comments | Messy, hard to understand |
| **Docker Setup** | 5% | `docker-compose up` works perfectly, 3+ services | 2/3 services work | Services don't communicate or won't start |

**Passing:** ≥ 70% (14/20 points)

---

## Tips & Tricks

1. **Embedding Model Performance:** `bge-m3` là heavy (~2GB RAM). Nếu máy yếu, dùng `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` (380MB, đủ tốt).

2. **Qdrant Self-Hosted vs Cloud:** Self-hosted dễ test local, nhưng production nên dùng Qdrant Cloud (managed) hoặc self-host with persistence volume.

3. **Prompt Engineering:** Prompt template rất ảnh hưởng RAG quality. Iterate on template là phần quan trọng nhất (Phase 3 của bài 2.2 sẽ focus vào đây).

4. **Debugging Retrieval:** Nếu retrieval kết quả tệ:
   - Check chunk quality: `print(chunks[0][:200])`
   - Check embedding: query embedding vs top-5 chunk embeddings, tính cosine similarity bằng tay
   - Check Qdrant payload: `qdrant.scroll(collection_name="rag_documents", limit=5)`

5. **Load Testing:** Nếu ingest 1K+ documents, batch upsert thành 32-64 chunks/batch (không làm lần lượt).

---

## Resources

- [Qdrant Quick Start](https://qdrant.tech/documentation/quick_start/)
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [LangChain RecursiveCharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_loaders/parsers/recursive_text_splitter)
- [vLLM OpenAI-Compatible API](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

---

**Deadline:** Cuối thứ 4 tuần này (sau khi nhận bài vào thứ 2).
**Questions?** Post lên Discord #week2-exercises hoặc email instructor.
