# Chunking Strategies: Deep Dive

## Tại sao chunking quan trọng?

Chunking là art & science của RAG. Sai chunking → sai context → sai answers.

```
Document: 10,000 tokens
        ↓
Chunking Strategy
        ↓
Option A: 100 chunks × 100 tokens (precise, little context)
Option B: 20 chunks × 500 tokens (rich context, harder to find)
Option C: 10 chunks × 1000 tokens (huge chunks, might miss exact answer)
```

**Trade-off**: Chunk size ↔ (retrieval precision × context richness)

## Benchmark Data (Vecta, Feb 2026)

```
Chunking Strategy | Retrieval Accuracy | Latency | Memory | Ideal use case
─────────────────────────────────────────────────────────────────────────
Recursive 512     | 69%                | 45ms   | 4GB    | Default choice
Semantic          | 71%                | 120ms  | 5GB    | Complex docs
Late Chunking     | 73%                | 200ms  | 6GB    | Dense reasoning
Contextual        | 68%                | 80ms   | 5GB    | Structured data
Structure-Aware   | 72%                | 100ms  | 5GB    | PDFs/reports
```

**Key insight**: Semantic > Late Chunking > Structure-Aware > Contextual > Recursive. Nhưng Recursive là best balance (speed × accuracy × simplicity).

## 1. Recursive Chunking (Default)

**Khái niệm**: Chia text dựa trên delimiters (newlines, sentences) từ tổng quát → chi tiết

```
Document
    ↓
Split on "\n\n" (paragraphs)
    ↓
Chunks too big? Split on "\n" (lines)
    ↓
Chunks too big? Split on ". " (sentences)
    ↓
Chunks too big? Split on " " (words)
    ↓
Final chunks
```

**Ưu điểm:**
- ✓ Fast (O(n) linear)
- ✓ Preserve logical boundaries (sentences, paragraphs)
- ✓ Simple, no ML needed
- ✓ Works for all languages

**Nhược điểm:**
- ✗ May break mid-concept
- ✗ Overlap handling awkward
- ✗ Doesn't understand semantics

**Code (LangChain)**:
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,           # target size in characters
    chunk_overlap=50,         # overlap between chunks
    separators=[
        "\n\n",  # Try paragraph first
        "\n",    # Then lines
        ". ",    # Then sentences
        " ",     # Then words
        ""       # Finally characters
    ]
)

chunks = splitter.split_text(text)
```

**Code (LlamaIndex)**:
```python
from llama_index.core.text_splitter import SentenceSplitter

splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
    backup_chunk_size=256,  # If sentence is > 512, use smaller
)

chunks = splitter.split_text(text)
```

**Recommendation**: Start here. 512 tokens, 20% overlap = 69% accuracy per Vecta benchmark.

---

## 2. Semantic Chunking (Smarter)

**Khái niệm**: Chunk dựa trên semantic similarity, không character count

```
Sentence 1: "The company was founded in 2020."
Sentence 2: "It focused on AI research."
Sentence 3: "The market grew 300% in 2021."  ← Big semantic jump
Sentence 4: "Competition from tech giants increased."  ← Semantically close to 3
    ↓
Chunk 1: Sentences 1-2
Chunk 2: Sentences 3-4
```

**Algorithm**:
1. Split into sentences
2. Embed each sentence
3. Calculate cosine distance between consecutive sentences
4. When distance > threshold → split

**Ưu điểm:**
- ✓ Semantically coherent chunks
- ✓ Better for reasoning tasks
- ✓ 71% accuracy (better than recursive)
- ✓ Respects topic boundaries

**Nhược điểm:**
- ✗ Slower (need embeddings for all sentences)
- ✗ Threshold tuning required
- ✗ More memory

**Code (LlamaIndex)**:
```python
from llama_index.core.text_splitter import SentenceSplitter

splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
    # Semantic chunking enabled by default
)

chunks = splitter.split_text(text)
```

**Code (Custom with LangChain)**:
```python
import numpy as np
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_chunk(text, threshold=0.5):
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        similarity = np.dot(embeddings[i], embeddings[i-1])

        if similarity < threshold:  # Big semantic jump
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])

    chunks.append(" ".join(current_chunk))
    return chunks

chunks = semantic_chunk(text)
```

**When to use**: Complex technical documents, when accuracy > speed

---

## 3. Late Chunking (Advanced)

**Khái niệm**: Delay chunking until retrieval time. Embed full document, then find relevant chunks on-the-fly.

```
Traditional:
Document → Chunk → Embed chunks → Store → Retrieve chunks → LLM

Late Chunking:
Document → Embed full doc → Store chunking info →
    Retrieve at query time → Extract relevant chunks → LLM
```

**Ưu điểm:**
- ✓ Highest accuracy (73%) - full document context
- ✓ No information loss at chunking boundary
- ✓ Can chunk differently for different queries

**Nhược điểm:**
- ✗ Slowest (200ms+ per query)
- ✗ More complex implementation
- ✗ Not suitable for real-time

**When to use**: Offline analysis, batch processing, when latency < 1 second acceptable

**Implementation**:
```python
# At index time: store full documents as single embedding
for doc in documents:
    doc_embedding = embedder.encode(doc.text)
    vector_db.add(
        text=doc.text,
        embedding=doc_embedding,
        metadata={"doc_id": doc.id}
    )

# At query time: chunk retrieved documents
retrieved_doc = vector_db.search(query_embedding)[0]
chunks = semantic_chunk(retrieved_doc['text'])  # Chunk now
relevant_chunks = rerank(chunks, query)
```

---

## 4. Contextual Chunking (Structured)

**Khái niệm**: Thêm context (parent heading, previous/next chunk) vào mỗi chunk

```
Input:
## Section A
Paragraph 1
Paragraph 2
## Section B
Paragraph 3

Output chunks:
Chunk 1: "Section A | Paragraph 1 | Paragraph 2"
Chunk 2: "Section B | Paragraph 3"
        ↓
LLM biết chunk 2 thuộc Section B
```

**Code (Custom)**:
```python
def contextual_chunk(text, chunk_size=512):
    """Add parent heading context to chunks"""
    lines = text.split('\n')
    chunks = []
    current_heading = "Introduction"
    current_chunk = []

    for line in lines:
        if line.startswith('#'):
            current_heading = line.lstrip('#').strip()
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    "text": f"[{current_heading}]\n{chunk_text}",
                    "heading": current_heading
                })
                current_chunk = []
        else:
            current_chunk.append(line)
            if len('\n'.join(current_chunk)) > chunk_size:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    "text": f"[{current_heading}]\n{chunk_text}",
                    "heading": current_heading
                })
                current_chunk = []

    return chunks
```

**When to use**: Hierarchical documents (reports, textbooks, documentation)

---

## 5. Structure-Aware Chunking

**Khái niệm**: Preserve document structure (tables, code blocks, headings)

```
Input:
## Analysis
Table with 5 columns
200 rows

❌ Bad: Split table into chunks (loses table meaning)
✓ Good: Keep table as single chunk (or split by logical groups)
```

**Tools**:
- LlamaIndex: `SimpleDirectoryReader` → auto structure-aware
- Unstructured: `partition_pdf` → returns element objects (Table, Text, Image)

**Code**:
```python
from llama_index.core import SimpleDirectoryReader

# Auto structure-aware
documents = SimpleDirectoryReader("./data").load_data()
# Returns Document objects with structure metadata

# Manual approach
def structure_aware_chunk(elements):
    """elements: [{"type": "heading", "text": ...}, ...]"""
    chunks = []
    current_section = []

    for elem in elements:
        if elem['type'] in ['h1', 'h2']:
            if current_section:
                chunks.append('\n'.join(current_section))
            current_section = [elem['text']]
        elif elem['type'] == 'table':
            # Keep table as atomic unit
            current_section.append(f"[TABLE]\n{elem['text']}\n[/TABLE]")
        else:
            current_section.append(elem['text'])

    return chunks
```

---

## Decision Tree: Chọn chunking strategy nào?

```
1. Bạn cần high accuracy?
   YES → Semantic (71%) hoặc Late Chunking (73%)
   NO → continue

2. Latency < 100ms required?
   YES → Recursive (45ms)
   NO → Semantic OK (120ms)

3. Document có structure (tables, code)?
   YES → Structure-Aware
   NO → continue

4. Dữ liệu hierarchical (sections, subsections)?
   YES → Contextual
   NO → Recursive

DEFAULT → Recursive 512 tokens, 20% overlap
```

---

## Practical Tips

**Chunk size tuning**:
```
Long context model (Claude, GPT-4): 512-1024 tokens/chunk
Short context model (others): 256-512 tokens/chunk
QA over small docs: 128-256 tokens/chunk
```

**Overlap tuning**:
```
No overlap: 10% miss important boundary info
10% overlap: Good balance
20% overlap: Better coverage, more tokens
30%+ overlap: Overkill, wastes tokens
```

**Testing**:
```python
# Calculate actual retrieval quality
from ragas.metrics import context_precision

for strategy_name, chunks in strategies.items():
    precision = context_precision(chunks, queries, answers)
    print(f"{strategy_name}: {precision:.2%}")
```

---

## Common Mistakes

**❌ Fixed character size**
```python
# Bad: "import" might be split into "im" "port"
chunks = [text[i:i+512] for i in range(0, len(text), 512)]

# Good: Use token-based, preserve boundaries
splitter.split_text(text)
```

**❌ No overlap**
```python
# Bad: "Next step is..." might be at chunk boundary, lose context
chunks = [text[i:i+512] for i in range(0, len(text), 512)]

# Good: Add 50 tokens overlap
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50
)
```

**❌ Not testing on YOUR data**
```python
# Bad: Use default 512 everywhere
# Good: Test 256, 512, 1024 on your actual data, measure accuracy
```

---

## Key Takeaway

Chunking là critical bottleneck. Default (Recursive 512, 20% overlap) gives 69% accuracy and fast speed. Nếu cần tốt hơn → Semantic (71%) hay Late Chunking (73%) nhưng slower. Luôn preserve document structure, thêm context, và test trên data của bạn. Benchmark data từ Vecta là guideline, not gospel. Implement với LlamaIndex hoặc LangChain built-in tools, đừng reinvent chunker. Đây là phần mà nhỏ thay đổi có impact lớn.
