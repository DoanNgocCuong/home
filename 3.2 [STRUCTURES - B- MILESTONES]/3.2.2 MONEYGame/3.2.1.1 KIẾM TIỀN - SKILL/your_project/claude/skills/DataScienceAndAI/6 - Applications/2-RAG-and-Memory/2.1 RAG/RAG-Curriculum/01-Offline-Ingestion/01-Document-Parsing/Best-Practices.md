# Document Parsing: Best Practices

## Document Parsing là gì?

Convert từ raw document file (PDF, HTML, DOCX, etc) thành structured text mà LLM có thể hiểu.

```
Input: Report.pdf (binary)
        ↓
Parser
        ↓
Output: {
  "text": "...",
  "metadata": {"title": "...", "pages": 10},
  "structure": [{"type": "heading", "level": 1, ...}]
}
```

**Tại sao quan trọng?**
- Sai parsing → sai data → sai answers
- Giữ structure → semantic chunking hiệu quả hơn
- Extract metadata → metadata filtering chính xác

## Các format phổ biến

### 1. PDF (Phức tạp nhất)

**Vấn đề**: PDF là format display, không semantic
- Scanned PDFs (image) → cần OCR
- Text PDFs → có text nhưng layout bị hỏng
- Mixed (text + images) → multimodal

**Giải pháp:**

**PyMuPDF (fitz)** - Nhanh, lightweight
```python
import fitz  # PyMuPDF

pdf = fitz.open("document.pdf")
text = ""
for page in pdf:
    text += page.get_text()
```
✓ Nhanh (50 pages/giây)
✓ Nhẹ (5MB)
✗ Mất layout, images

**Unstructured** - Multimodal, layout-aware
```python
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf("document.pdf")
# Returns: Title, Heading, Text, Image, Table
for el in elements:
    print(f"{el.type}: {el.text}")
```
✓ Giữ structure (headings, tables)
✓ Handle images → OCR
✗ Chậm (5 pages/giây), nặng (200MB)

**DeepDoc** - Semantic layout understanding
```python
from deepdoc.pdf_parser import PdfParser

parser = PdfParser()
docs = parser.parse("document.pdf")
# Biết heading hierarchy, table structure
```
✓ Semantic understanding
✓ Table extraction tốt
✗ Chậm, cần config

**Recommendation**:
- Simple PDFs (text) → PyMuPDF
- Complex/scanned PDFs → Unstructured
- Tables/structured data → DeepDoc

### 2. HTML (Layout-aware parsing)

**Problem**: Raw HTML có noise (ads, scripts, navigation)

**BeautifulSoup** - Lightweight
```python
from bs4 import BeautifulSoup

html = open("page.html").read()
soup = BeautifulSoup(html, "html.parser")

# Remove noise
for tag in soup.find_all(["script", "style", "nav"]):
    tag.decompose()

text = soup.get_text()
```

**Trafilatura** - Content extraction focused
```python
import trafilatura

html = open("page.html").read()
text = trafilatura.extract(html)
# Automatically finds main content
```
✓ Removes ads/navigation automatically
✓ Keeps article structure
✓ Fast

**Structure preservation**:
```python
from html.parser import HTMLParser

class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.structure = []

    def handle_starttag(self, tag, attrs):
        if tag in ['h1', 'h2', 'h3', 'p', 'table']:
            self.structure.append((tag, 'start'))

    def handle_data(self, data):
        if data.strip():
            self.structure.append(('text', data.strip()))

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'p', 'table']:
            self.structure.append((tag, 'end'))

# Use để preserve heading hierarchy
```

### 3. DOCX (Office documents)

**python-docx** - Standard library
```python
from docx import Document

doc = Document("report.docx")
text = ""
structure = []

for para in doc.paragraphs:
    text += para.text + "\n"
    structure.append({
        "type": "paragraph",
        "text": para.text,
        "style": para.style.name  # Preserve heading level
    })

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text += cell.text + "\n"
```

✓ Giữ formatting (headings, bold)
✓ Tables support
✓ Light & fast

## Metadata Extraction

**Quan trọng**: Metadata giúp filter và traceability

```python
# From document itself
metadata = {
    "source": "report.pdf",
    "page_count": pdf.page_count,
    "title": extract_title(text),  # First heading
    "author": extract_author(pdf.metadata),
    "creation_date": pdf.metadata.get("creation_date"),
}

# Computed
metadata.update({
    "language": detect(text),  # textblob hoặc langdetect
    "document_type": classify_doc_type(text),  # rule-based: report, FAQ, legal
    "key_topics": extract_topics(text),  # NER hoặc keyword extraction
})
```

**Best practice**: Bao gồm metadata trong chunking step

## Workflow: End-to-end

```python
from pathlib import Path
import fitz
import trafilatura
from bs4 import BeautifulSoup
from docx import Document

def parse_document(filepath):
    """Parse any document type"""
    path = Path(filepath)
    metadata = {"source": str(path)}

    if path.suffix.lower() == ".pdf":
        text = parse_pdf(path)
    elif path.suffix.lower() in [".html", ".htm"]:
        text = parse_html(path)
    elif path.suffix.lower() == ".docx":
        text = parse_docx(path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    # Add metadata
    metadata.update({
        "char_count": len(text),
        "title": text.split('\n')[0][:100],  # First line
    })

    return {
        "text": text,
        "metadata": metadata
    }

def parse_pdf(filepath):
    pdf = fitz.open(filepath)
    text = ""
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def parse_html(filepath):
    with open(filepath, encoding='utf-8') as f:
        html = f.read()
    return trafilatura.extract(html) or BeautifulSoup(html).get_text()

def parse_docx(filepath):
    doc = Document(filepath)
    return '\n'.join([para.text for para in doc.paragraphs])

# Usage
doc = parse_document("report.pdf")
print(f"Parsed {len(doc['text'])} chars from {doc['metadata']['source']}")
```

## Common Pitfalls

**❌ Pitfall 1**: Parsing headers/footers → contaminate data
```python
# ✗ Bad: Includes page number "Page 1" everywhere
text = fitz.open("doc.pdf")[0].get_text()

# ✓ Good: Filter headers/footers
import pymupdf4llm
text_dict = pymupdf4llm.to_markdown("doc.pdf")
```

**❌ Pitfall 2**: Losing document structure
```python
# ✗ Bad: All text as one block
chunks = [text[i:i+512] for i in range(0, len(text), 512)]

# ✓ Good: Preserve structure
docs = parse_with_structure(text)
# {heading: "Section 1", content: "...", level: 1}
```

**❌ Pitfall 3**: Not handling encoding
```python
# ✗ Bad: Assumes UTF-8
with open(file) as f:
    text = f.read()

# ✓ Good: Detect encoding
import chardet
with open(file, 'rb') as f:
    encoding = chardet.detect(f.read())['encoding']
with open(file, encoding=encoding) as f:
    text = f.read()
```

## Performance Considerations

| Format | Tool | Speed | Quality | Notes |
|--------|------|-------|---------|-------|
| Text PDF | PyMuPDF | 50 p/s | Medium | Good for simple |
| Text PDF | Unstructured | 5 p/s | High | Layout aware |
| Scanned PDF | Unstructured | 2 p/s | High | Needs OCR |
| HTML | Trafilatura | 200/s | High | Fast, clean |
| DOCX | python-docx | 500/s | High | Fast, reliable |

**Batch processing**:
```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

files = list(Path("./documents").glob("*.pdf"))

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(parse_document, files)

docs = list(results)
```

## Vietnamese-specific Issues

Tiếng Việt có diacritics → encoding must be UTF-8 everywhere

```python
# ✓ Always explicit encoding
with open("tieng_viet.txt", encoding='utf-8') as f:
    text = f.read()

# When using Unstructured
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf("tieng_viet.pdf", languages=["vit"])
```

---

## Key Takeaway

Document parsing là foundation của RAG pipeline. Tốn 20% thời gian implementation nhưng 80% impact nếu sai. Luôn preserve document structure (headings, tables), extract metadata, handle encoding đúng. Nếu không chắc format, use Unstructured (xử hết mọi case); nếu biết format, dùng tool chuyên biệt (PyMuPDF cho PDF, Trafilatura cho HTML). Batch process nếu có nhiều files. Test output thử tay trước khi scale.
