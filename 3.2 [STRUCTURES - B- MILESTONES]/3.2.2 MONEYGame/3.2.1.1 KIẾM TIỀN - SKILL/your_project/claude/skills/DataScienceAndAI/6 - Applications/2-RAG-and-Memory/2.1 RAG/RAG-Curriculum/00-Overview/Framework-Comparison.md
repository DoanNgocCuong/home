# So sánh các RAG Frameworks 2025-2026

## Tổng quan

Năm 2025-2026, có 5 framework chính dominate RAG landscape. Mỗi cái có philosophy khác nhau.

## LlamaIndex

**Philosophy**: "Data framework for LLMs" - tập trung vào dữ liệu, không phụ thuộc model

### Ưu điểm
- **Structure-aware parsing**: Hiểu document hierarchy (headings, tables)
- **Smart chunking**: Semantic chunking built-in, không cần custom code
- **Node relationships**: Biểu diễn document as graph, không chỉ vector
- **Multi-modal support**: Handle PDF images, audio metadata
- **Vietnamese support**: Tốt hơn competitors nhờ community

### Nhược điểm
- **Heavy dependencies**: Nhiều imports, ~ 500MB khi cài full
- **Slower inference**: Overhead từ abstraction layers
- **Steeper learning curve**: Concepts như Node, Index, Query Engine không intuitive

### Khi nào dùng
- Complex document structures (technical docs, reports)
- Vietnamese content
- Khi bạn muốn "let framework handle it"

### Code snippet

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Build index (auto chunking, embedding, storage)
embed_model = OpenAIEmbedding(model="text-embedding-3-large")
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model
)

# Query
response = index.as_query_engine().query("What's the revenue?")
```

**Token overhead**: ~1.5x due to metadata in prompts

---

## LangChain

**Philosophy**: "Composable building blocks" - mix & match components freely

### Ưu điểm
- **Flexibility**: Mỗi step có control tuyệt đối
- **Ecosystem**: 200+ integrations (tools, agents, models)
- **Lightweight**: Core library nhỏ (~50MB), thêm component khi cần
- **Wide adoption**: Largest community, most tutorials

### Nhược điểm
- **DIY spirit**: Phải tự code chunking, retrieval logic
- **Inconsistent APIs**: Một số component API khác nhau
- **Maintenance burden**: Khi framework update, custom code break
- **Overhead**: Chain of Thought prompts sử dụng nhiều tokens

### Khi nào dùng
- Nếu bạn muốn full control
- Agents, tool-use (LangChain tốt nhất)
- Prototype nhanh

### Code snippet

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Load
loader = DirectoryLoader("./data")
documents = loader.load()

# Chunk (you choose strategy)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# Embed & store
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(chunks, embeddings)

# Query
retriever = vector_store.as_retriever(k=5)
context = retriever.invoke("Revenue?")
```

**Token overhead**: ~1.2x (flexible, you can optimize)

---

## Haystack

**Philosophy**: "Production-ready pipelines" - tập trung vào scalability & monitoring

### Ưu điểm
- **Pipeline abstraction**: Declarative YAML pipelines
- **Monitoring & observability**: Built-in logging, metrics
- **Hybrid retrieval**: BM25 + semantic in one pipeline
- **Scalability**: Designed for distributed systems
- **Type-safe**: Strong typing, validation

### Nhược điểm
- **Smaller community**: Ít tutorials, ít integrations vs LangChain
- **Steeper learning curve**: Pipeline concept takes time
- **Slower for MVP**: Overkill nếu bạn chỉ cần simple RAG
- **Less flexible**: Phải follow pipeline paradigm

### Khi nào dùng
- Production systems cần monitoring
- Large-scale retrieval (millions of documents)
- Hybrid search (BM25 + semantic)

### Code snippet (simplified)

```python
from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Setup
doc_store = InMemoryDocumentStore()
retriever = InMemoryBM25Retriever(doc_store)

# Pipeline (declarative)
pipeline = Pipeline()
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", PromptBuilder(...))

# Run
result = pipeline.run({"retriever": {"query": "Revenue?"}})
```

**Token overhead**: ~1.0x (optimized for production)

---

## RAGFlow

**Philosophy**: "RAG as a product" - UI-first, no-code RAG

### Ưu điểm
- **Visual interface**: Drag-drop RAG construction (like Zapier for RAG)
- **No coding needed**: Non-technical users can build RAG
- **Built-in tools**: Parsing, chunking, embedding all included
- **Workflow builder**: Complex logic without code

### Nhược điểm
- **Limited customization**: Can't do advanced tweaks
- **Locked ecosystem**: Depend on RAGFlow's components
- **Performance overhead**: Web UI → slower
- **Debugging harder**: Black-box execution
- **New/immature**: Less battle-tested than others

### Khi nào dùng
- Business users, non-technical teams
- Quick prototypes (1-2 days)
- Internal tools, not customer-facing

**Token overhead**: ~1.5x

---

## LightRAG

**Philosophy**: "Minimal dependencies, maximum efficiency" - lightweight & fast

### Ưu điểm
- **Tiny footprint**: ~10MB, 0 ML dependencies
- **Fast inference**: Minimal overhead
- **Simple API**: 3-4 functions, learn in 10 mins
- **Good for edge**: Works on low-resource devices

### Nhược điểm
- **Fewer features**: No advanced chunking strategies
- **Limited integrations**: Only popular models
- **Small community**: Fewer examples
- **Less mature**: Fewer edge cases handled

### Khi nào dùng
- Embedded systems, edge devices
- Simple RAG on mobile
- When speed matters more than features
- Learning (understand core concepts)

### Code snippet

```python
from lightrag import RAG

# That's it!
rag = RAG(
    documents="./data",
    embedding_model="bge-m3",
    vector_db="qdrant"
)

response = rag.query("Revenue?")
```

**Token overhead**: ~1.0x (minimal)

---

## Comparison Table

| Aspect | LlamaIndex | LangChain | Haystack | RAGFlow | LightRAG |
|--------|-----------|-----------|----------|---------|----------|
| **Ease of use** | Medium | Medium-Hard | Hard | Easy | Very Easy |
| **Flexibility** | Medium | Very High | High | Low | Low |
| **Performance** | Slow (1.5x) | Medium (1.2x) | Fast (1.0x) | Slow (1.5x) | Fast (1.0x) |
| **Production ready** | Yes | Yes | Very Yes | No | Medium |
| **Community** | Large | Largest | Medium | Small | Small |
| **Vietnamese support** | Good | Medium | Medium | Medium | Poor |
| **Learning curve** | Medium | Medium | Hard | Easy | Very Easy |
| **For MVP** | ✓ | ✓ | ✗ | ✓ | ✓ |
| **For production** | ✓ | ✓ | ✓✓ | ✗ | Medium |
| **For agents** | Medium | ✓✓ | Medium | ✗ | ✗ |

---

## Decision Tree: Chọn framework nào?

```
1. Bạn muốn no-code?
   YES → RAGFlow
   NO → continue

2. Bạn là data scientist / ML engineer?
   YES → continue
   NO → LangChain (ecosystem) hoặc RAGFlow

3. Bạn cần production scalability?
   YES → Haystack
   NO → continue

4. Dữ liệu phức tạp (PDFs, Vietnamese)?
   YES → LlamaIndex
   NO → continue

5. Bạn cần tối ưu latency / cost?
   YES → LightRAG
   NO → LangChain (flexibility)
```

---

## Real-world: Token Usage Comparison

**Scenario**: Query "What was Q4 revenue?" trên 100-page annual report

| Framework | Embedding tokens | LLM prompt tokens | Total | Cost (gpt-4-turbo) |
|-----------|------------------|------------------|-------|-------------------|
| LlamaIndex | 45 | 2,150 | 2,195 | ~$0.12 |
| LangChain | 45 | 1,900 | 1,945 | ~$0.10 |
| Haystack | 45 | 1,850 | 1,895 | ~$0.10 |
| RAGFlow | 45 | 2,200 | 2,245 | ~$0.12 |
| LightRAG | 45 | 1,820 | 1,865 | ~$0.09 |

**Reality**: Sau tối ưu, tất cả khác nhau < 20% tokens. Chọn framework dựa vào developer experience, không phải tokens.

---

## Đặc biệt: Vietnamese RAG

```
Language Support Score (0-10):
LlamaIndex: 7/10 (tốt nhất)
LangChain: 6/10
Haystack: 5/10
RAGFlow: 5/10
LightRAG: 3/10
```

Recommendation: Nếu làm tiếng Việt → LlamaIndex + BGE-M3 (embedding) + Qdrant (vector DB)

---

## Key Takeaway

Không có framework "tốt nhất". LangChain để tối đa flexibility, LlamaIndex để dữ liệu phức tạp, Haystack để production scalability, RAGFlow để non-technical users, LightRAG để tối ưu speed. Đối với most people: LangChain hoặc LlamaIndex. Nghe feedback từ team bạn, prototype với cái dễ nhất trước, sau đó optimize nếu cần. Phần lớn RAG không fail vì framework, mà fail vì chunking/embedding strategy → focus vào Phase 1 of this curriculum!
