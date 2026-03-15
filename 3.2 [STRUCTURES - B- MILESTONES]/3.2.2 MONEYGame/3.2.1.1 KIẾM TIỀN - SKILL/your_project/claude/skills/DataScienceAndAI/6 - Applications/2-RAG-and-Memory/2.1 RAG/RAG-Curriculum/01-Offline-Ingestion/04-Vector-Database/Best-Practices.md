# Vector Database: Selection & Deployment

## Vector DB là gì?

Chuyên biệt database để store & query vectors (embeddings). Khác biệt với SQL DB:

```
Traditional SQL DB:     Vector DB:
SELECT * FROM users    SELECT chunks WHERE
WHERE age > 30         similarity(query_vec, chunk_vec) > 0.8

Exact match logic      Approximate nearest neighbor search
```

**Tại sao cần specialized DB?**
- HNSW/IVF indexes: fast similarity search
- Metadata filtering: filter while searching
- High dimensionality: 1024-dim vectors
- Scalability: millions of vectors

## Top Vector Databases 2025-2026

### 1. Qdrant (Balanced, Popular)

**Specs:**
- Index: HNSW (Hierarchical Navigable Small World)
- Distributed: Yes (clustering support)
- Metadata filtering: Yes, complex queries
- Languages: Python, Go, JavaScript SDKs
- Self-host/Cloud: Both

**Ưu điểm:**
- ✓ Production-ready, battle-tested
- ✓ Good balance: speed + features
- ✓ Complex metadata filtering
- ✓ Payload filtering while searching
- ✓ Open source + cloud version
- ✓ Vietnamese support (UTF-8)

**Nhược điểm:**
- ✗ Memory usage higher than Milvus
- ✗ Less suited for ultra-large scale (100M+ vectors)

**Setup (Docker):**
```bash
docker run -p 6333:6333 \
  -e QDRANT_API_KEY="your_key" \
  qdrant/qdrant
```

**Python code:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect to Qdrant
client = QdrantClient(
    url="http://localhost:6333",
    api_key="your_key"  # if auth enabled
)

# Create collection (like table)
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1024,  # embedding dimension
        distance=Distance.COSINE  # similarity metric
    )
)

# Add vectors with metadata
points = [
    PointStruct(
        id=1,
        vector=[0.23, -0.45, ...],  # 1024-dim
        payload={
            "text": "Document chunk...",
            "source": "report.pdf",
            "page": 1,
            "date": "2025-03-11"
        }
    ),
    # More points...
]

client.upsert(
    collection_name="documents",
    points=points
)

# Search with metadata filtering
results = client.search(
    collection_name="documents",
    query_vector=[0.12, -0.34, ...],
    query_filter={
        "must": [
            {"range": {"page": {"gte": 0, "lte": 10}}}
        ]
    },
    limit=5  # top-5 similar
)

for hit in results:
    print(f"ID: {hit.id}, Score: {hit.score:.3f}")
    print(f"Text: {hit.payload['text']}")
```

**Best for:** Most use cases, when balanced features needed

---

### 2. Milvus (High Performance, Enterprise)

**Specs:**
- Indexes: HNSW, IVF, PQ (Quantization)
- Distributed: Built-in (horizontal scaling)
- Capacity: 100B+ vectors (tested)
- Cloud version: Zilliz Cloud

**Ưu điểm:**
- ✓ Extreme scale: tested with 100B vectors
- ✓ PQ quantization: 100x compression
- ✓ High throughput (100K+ QPS)
- ✓ GPU support: CUDA acceleration
- ✓ Complex filtering

**Nhược điểm:**
- ✗ Steeper learning curve
- ✗ More complex deployment
- ✗ Smaller community than Qdrant

**Setup (Docker):**
```bash
docker-compose up -d milvus etcd minio
```

**Python code:**
```python
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530")

# Create collection
schema = client.create_schema()
schema.add("id", DataType.INT64, is_primary=True)
schema.add("embedding", DataType.FLOAT_VECTOR, dim=1024)
schema.add("text", DataType.VARCHAR, max_length=65535)
schema.add("source", DataType.VARCHAR, max_length=255)

client.create_collection(
    collection_name="documents",
    schema=schema
)

# Create index (HNSW for speed)
index_params = client.prepare_index_params()
index_params.add_index(field_name="embedding", metric_type="COSINE")
client.create_index("documents", index_params)

# Insert data
data = [
    {"id": 1, "embedding": [0.23, -0.45, ...], "text": "...", "source": "..."},
    # More...
]
client.insert(collection_name="documents", data=data)

# Search
results = client.search(
    collection_name="documents",
    data=[[0.12, -0.34, ...]],  # query vector
    filter='source like "report%"',  # metadata filter
    limit=5,
    output_fields=["text", "source"]
)

for hit in results[0]:
    print(f"Distance: {hit['distance']:.3f}")
    print(f"Text: {hit['entity']['text']}")
```

**Best for:** Enterprise, ultra-large scale, GPU acceleration needed

---

### 3. Weaviate (Graph-aware, Semantic)

**Specs:**
- Focus: Semantic search + graph relationships
- Index: HNSW + graph structure
- Multi-modal: text + image vectors
- GraphQL API: Complex queries

**Ưu điểm:**
- ✓ Graph relationships: understand connections
- ✓ Multi-modal: good for image + text
- ✓ Rich query language (GraphQL)
- ✓ Built-in modules (summarization, Q&A)

**Nhược điểm:**
- ✗ Steeper learning curve (GraphQL)
- ✗ Slower than pure vector DBs
- ✗ More memory overhead

**Setup:**
```bash
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:latest
```

**Python code:**
```python
import weaviate
from weaviate.classes.config import Configure

client = weaviate.connect_to_local()

# Define schema (class)
client.collections.create(
    name="Document",
    vectorizer_config=Configure.Vectorizer.none(),  # use pre-computed embeddings
    properties=[
        {"name": "text", "data_type": "text"},
        {"name": "source", "data_type": "text"},
    ]
)

# Add objects
collection = client.collections.get("Document")
collection.data.insert({
    "text": "Document chunk...",
    "source": "report.pdf",
    "vector": [0.23, -0.45, ...]
})

# Search (GraphQL-style)
results = collection.query.near_vector(
    near_vector=[0.12, -0.34, ...],
    limit=5,
    where={
        "path": ["source"],
        "operator": "Like",
        "valueString": "report%"
    }
)

for obj in results.objects:
    print(f"Text: {obj.properties['text']}")
```

**Best for:** Semantic graph relationships, multi-modal search

---

### 4. Chroma (Simple, Lightweight)

**Specs:**
- Embedded: Python library, no separate server
- Persistence: SQLite
- Index: HNSW built-in
- Size: Lightweight (~50MB)

**Ưu điểm:**
- ✓ Simple: 5 lines of code to get started
- ✓ No deployment: embedded
- ✓ Good for prototypes

**Nhược điểm:**
- ✗ Not for production: single-threaded
- ✗ Limited scale: millions max
- ✗ No distributed support
- ✗ Metadata filtering limited

**Code:**
```python
import chromadb

# Create/connect client
client = chromadb.Client()

# Create collection
collection = client.create_collection(name="documents")

# Add documents
collection.add(
    ids=["1", "2", "3"],
    embeddings=[[0.23, -0.45, ...], [...], [...]],
    metadatas=[
        {"source": "report.pdf", "page": 1},
        {"source": "report.pdf", "page": 2},
        {"source": "other.pdf", "page": 1},
    ],
    documents=[
        "Document text 1...",
        "Document text 2...",
        "Document text 3..."
    ]
)

# Query
results = collection.query(
    query_embeddings=[[0.12, -0.34, ...]],
    n_results=5,
    where={"source": "report.pdf"}  # Simple filtering
)

for i, text in enumerate(results["documents"][0]):
    print(f"Rank {i+1}: {text}")
```

**Best for:** Prototypes, small-scale RAG, learning

---

### 5. Pinecone (Managed, Serverless)

**Specs:**
- Fully managed: No ops needed
- Distributed: Handled automatically
- Cost: Pay per pod (vectors stored)
- Index types: Approximated (HNSW-like)

**Ưu điểm:**
- ✓ Zero ops: just use API
- ✓ Auto-scaling: handle load
- ✓ High reliability (99.9% uptime)
- ✓ Simple API

**Nhược điểm:**
- ✗ Cost: $0.25/1M vectors/month minimum
- ✗ Lock-in: vendor-specific
- ✗ Limited metadata filtering
- ✗ Higher latency than self-hosted

**Code:**
```python
import pinecone

# Initialize
index_name = "documents"
pinecone.init(api_key="your_key", environment="us-west1-gcp")

# Connect to index
index = pinecone.Index(index_name)

# Upsert vectors
index.upsert(vectors=[
    ("1", [0.23, -0.45, ...], {"source": "report.pdf", "page": 1}),
    ("2", [0.12, -0.34, ...], {"source": "report.pdf", "page": 2}),
])

# Query
results = index.query(
    vector=[0.10, -0.35, ...],
    top_k=5,
    filter={"source": "report.pdf"}  # Simple filtering
)

for match in results["matches"]:
    print(f"Score: {match['score']:.3f}, ID: {match['id']}")
```

**Cost**: 100K documents × 1024-dim = 100M tokens
- Storage: $0.25/month (for 1M vectors) × 100 = $25/month
- Queries: negligible for most workloads

**Best for:** When you want zero ops, willing to pay premium

---

## Comparison Table

| Aspect | Qdrant | Milvus | Weaviate | Chroma | Pinecone |
|--------|--------|--------|----------|--------|----------|
| **Setup** | Easy | Medium | Medium | Very Easy | API only |
| **Scale** | 100M | 100B | 100M | 10M | Unlimited |
| **Latency** | 10-50ms | 5-30ms | 50-100ms | 20-100ms | 100-200ms |
| **Cost/100K docs** | ~$10/mo compute | ~$5/mo compute | ~$10/mo | Free | ~$1/mo |
| **Metadata filter** | ✓✓ | ✓ | ✓✓ | ✓ | ✓ |
| **Multi-modal** | ✓ | ✓ | ✓✓ | ✗ | ✗ |
| **For MVP** | ✓ | ✗ | ✗ | ✓ | ✓ |
| **For production** | ✓✓ | ✓✓ | ✓ | ✗ | ✓ |

---

## Indexing Deep Dive

### HNSW (Hierarchical Navigable Small World)
```
Pros:
- Fast search (10-50ms for 1M vectors)
- Memory efficient
- Good accuracy (99%+ recall)

Cons:
- Slower index building
- Doesn't compress
- Memory: ~50 bytes per vector overhead

Use: Default choice for most
```

### IVF (Inverted File)
```
Pros:
- Fast indexing
- Less memory
- Good for very large scale

Cons:
- Slower search than HNSW
- Accuracy-latency trade-off harder
- Needs parameter tuning (n_clusters)

Use: Ultra-large scale (1B+ vectors)
```

### PQ (Product Quantization)
```
Pros:
- Extreme compression (100x)
- Fast search
- Small memory footprint

Cons:
- Accuracy loss (85-90% recall)
- Complex to tune

Use: When storage is constraint
```

---

## Decision Tree: Chọn Vector DB nào?

```
1. Prototype / Learning?
   YES → Chroma (embedded, simple)
   NO → continue

2. Production at scale (> 10M vectors)?
   YES → Milvus (scalability)
   NO → continue

3. Want zero ops / don't want to manage infra?
   YES → Pinecone
   NO → continue

4. Complex metadata filtering important?
   YES → Qdrant
   NO → continue

5. Graph relationships matter?
   YES → Weaviate
   NO → Qdrant (default)
```

---

## Self-hosted vs Managed

| Aspect | Self-hosted | Managed |
|--------|------------|---------|
| Setup | 1-2 days | 5 mins |
| Cost | Low (10-20$/mo) | High (100-1000$/mo) |
| Control | Full | Limited |
| Scaling | Manual | Automatic |
| Uptime | Your responsibility | 99.9% SLA |

**Recommendation**: Start with self-hosted Qdrant (good balance), move to Pinecone if ops becomes burden

---

## Common Mistakes

**❌ Wrong distance metric**
```python
# Bad: use Euclidean for normalized vectors
vectors_config = VectorParams(size=1024, distance=Distance.EUCLID)

# Good: use Cosine for normalized embeddings
vectors_config = VectorParams(size=1024, distance=Distance.COSINE)
```

**❌ Not indexing before search**
```python
# Bad: search on raw data
results = db.search(query_vector)  # slow, O(n)

# Good: create index first
db.create_index(index_type="HNSW")
results = db.search(query_vector)  # fast, O(log n)
```

**❌ Memory unbounded**
```python
# Bad: load all 100M vectors in memory
vectors = db.get_all()

# Good: paginate
for page in range(0, total_count, 10000):
    vectors = db.get_page(page, 10000)
```

---

## Vietnamese in Vector DB

All major DBs handle UTF-8 correctly. Qdrant is particularly good for Vietnamese:

```python
# Vietnamese metadata
payload = {
    "tiêu_đề": "Báo cáo quý IV 2025",
    "ngôn_ngữ": "vi",
    "ngày_tạo": "2025-03-11"
}
```

---

## Key Takeaway

For most RAG projects: **Qdrant** (balanced, production-ready, good filtering). For ultra-large scale: **Milvus**. For zero ops: **Pinecone**. For learning: **Chroma**. Use HNSW index by default (good balance speed/accuracy). Test your specific query patterns before choosing. Self-hosted infra if have ops capacity, otherwise go managed. Metadata filtering is key to retrieval quality → choose DB with flexible filtering.
