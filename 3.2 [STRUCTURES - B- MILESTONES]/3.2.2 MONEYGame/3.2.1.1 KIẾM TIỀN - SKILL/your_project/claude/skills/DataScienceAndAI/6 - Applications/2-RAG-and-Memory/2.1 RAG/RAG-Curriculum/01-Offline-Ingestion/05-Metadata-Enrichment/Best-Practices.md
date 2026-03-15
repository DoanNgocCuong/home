# Metadata Enrichment: Best Practices

## Metadata là gì?

Data about data. Thêm context, structure, attributes vào mỗi chunk.

```
Chunk text: "The revenue increased 40% YoY."

Minimal metadata:
{
  "source": "report.pdf",
  "page": 5
}

Rich metadata:
{
  "source": "report.pdf",
  "page": 5,
  "section": "Financial Results",
  "section_level": 2,
  "date": "2025-03-11",
  "company": "Acme Corp",
  "year": 2025,
  "quarter": "Q4",
  "entities": ["Acme Corp", "40%"],
  "keywords": ["revenue", "growth", "YoY"],
  "summary": "Revenue growth metric",
  "chunk_type": "key_finding"
}
```

**Tại sao metadata quan trọng?**

1. **Filtering**: "Only search Q4 2025 documents"
2. **Ranking**: "Prioritize official reports over memos"
3. **Context**: LLM biết document type, date, authority
4. **Traceability**: "From where exactly?"

## Metadata Extraction Strategies

### 1. NER (Named Entity Recognition)

**Extract**: People, organizations, locations, numbers, dates

```python
import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("Apple Inc. reported revenue of $365B in Q4 2024.")

entities = {
    "organizations": [],
    "locations": [],
    "quantities": [],
}

for ent in doc.ents:
    if ent.label_ == "ORG":
        entities["organizations"].append(ent.text)
    elif ent.label_ == "GPE":
        entities["locations"].append(ent.text)
    elif ent.label_ in ["MONEY", "DATE"]:
        entities["quantities"].append((ent.text, ent.label_))

print(entities)
# {'organizations': ['Apple Inc.'], 'quantities': [('$365B', 'MONEY'), ('Q4 2024', 'DATE')]}
```

**Vietnamese NER:**
```python
# Use pyvi + PyDantic (Vietnamese NLP stack)
from pyvi import ViTokenizer
import spacy

# Vietnamese model (phải cài: python -m spacy download vi_core_news_sm)
nlp_vi = spacy.load("vi_core_news_sm")

text = "Công ty Apple Inc. báo cáo doanh thu 365 tỷ đô trong Q4 2024."
doc_vi = nlp_vi(text)

for ent in doc_vi.ents:
    print(f"{ent.text}: {ent.label_}")
# Output: Apple Inc.: ORG, Q4 2024: DATE, ...
```

**Code integration:**
```python
def extract_entities(text, language="en"):
    if language == "en":
        nlp = spacy.load("en_core_web_sm")
    else:
        nlp = spacy.load("vi_core_news_sm")

    doc = nlp(text)

    entities = {
        "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
        "persons": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "locations": [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]],
        "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"],
        "quantities": [ent.text for ent in doc.ents if ent.label_ in ["MONEY", "QUANTITY"]],
    }

    return {k: v for k, v in entities.items() if v}  # Remove empty
```

**Use case**: Filter by company, person, date

---

### 2. Automatic Summarization

**Extract**: Short summary of chunk (1-2 sentences)

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text = "The quarterly earnings report shows...[1000 tokens]..."

summary = summarizer(text, max_length=50, min_length=10)[0]['summary_text']
print(summary)  # "Q4 earnings exceeded expectations by 15%."
```

**Fast alternative (extractive vs abstractive):**
```python
from sumy.parsers import PlaintextParser
from sumy.nlp.tokenizer import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

parser = PlaintextParser.from_string(text, Tokenizer("english"))
summarizer = LsaSummarizer()
summary = summarizer(parser.document, sentences_count=2)

for sentence in summary:
    print(sentence)
```

**Code:**
```python
def summarize_chunk(text, max_length=50):
    try:
        # Try fast extractive summarization first
        from sumy.summarizers.lsa import LsaSummarizer
        # ... code above
    except:
        # Fallback: use first sentence
        sentences = text.split(". ")
        return sentences[0] + "."

metadata["summary"] = summarize_chunk(chunk_text)
```

**Use case**: Show snippet in search results, context for LLM

---

### 3. Keyword Extraction

**Extract**: Important keywords from chunk

```python
from keybert import KeyBERT

kw_model = KeyBERT(model="all-MiniLM-L6-v2")

text = "Apple Inc. reported Q4 2024 revenue growth of 15% YoY..."

keywords = kw_model.extract_keywords(text, language="english")
# [('Apple Inc.', 0.87), ('Q4 2024', 0.84), ('revenue growth', 0.82), ...]

metadata["keywords"] = [kw[0] for kw in keywords[:5]]  # Top 5
```

**Alternative (TF-IDF):**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=10)
X = vectorizer.fit_transform([text])
keywords = vectorizer.get_feature_names_out()
```

**Use case**: Tag documents, search by keyword, faceted search

---

### 4. Question Generation (Advanced)

**Extract**: Potential questions this chunk answers

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

text = "Apple reported Q4 2024 revenue of $119.6B, up 15% YoY."

input_text = f"generate question: {text}"
inputs = tokenizer.encode(input_text, return_tensors="pt")
outputs = model.generate(inputs, max_length=64)
questions = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(questions)
# "What was Apple's Q4 2024 revenue? How much did revenue grow?"
```

**Use case**: Improve semantic search, generate FAQs

---

### 5. Document Type Classification

**Extract**: Document category (report, FAQ, email, news)

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification")

text = "The quarterly earnings report shows...[text]..."

categories = ["financial_report", "FAQ", "news", "email", "legal_doc"]

result = classifier(text, categories)
document_type = result['labels'][0]  # Most probable

metadata["document_type"] = document_type
metadata["confidence"] = result['scores'][0]
```

**Rule-based alternative (faster):**
```python
def classify_document_type(text, title=""):
    text_lower = text.lower()
    title_lower = title.lower()

    if "frequently asked" in text_lower or "FAQ" in title_lower:
        return "faq"
    elif "earnings" in text_lower or "revenue" in text_lower:
        return "financial_report"
    elif "legal" in text_lower or "agreement" in text_lower:
        return "legal"
    else:
        return "general"
```

**Use case**: Route queries, apply domain-specific logic

---

## Complete Enrichment Pipeline

```python
from datetime import datetime
import spacy
from keybert import KeyBERT

class MetadataEnricher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.kw_model = KeyBERT()

    def enrich(self, chunk_text, source="unknown", page=None):
        """Add rich metadata to a chunk"""

        metadata = {
            # Basic
            "source": source,
            "page": page,
            "timestamp": datetime.now().isoformat(),

            # Content analysis
            "length_chars": len(chunk_text),
            "length_tokens": len(chunk_text.split()),

            # NER
            "entities": self._extract_entities(chunk_text),

            # Keywords
            "keywords": self._extract_keywords(chunk_text),

            # Type
            "chunk_type": self._classify_chunk_type(chunk_text),

            # Summary
            "summary": self._summarize(chunk_text),
        }

        return metadata

    def _extract_entities(self, text):
        doc = self.nlp(text)
        return {
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"],
            "persons": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
            "locations": [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]],
        }

    def _extract_keywords(self, text):
        keywords = self.kw_model.extract_keywords(text)
        return [kw[0] for kw in keywords[:5]]

    def _classify_chunk_type(self, text):
        text_lower = text.lower()
        if any(word in text_lower for word in ["question", "answer", "FAQ"]):
            return "qa"
        elif any(word in text_lower for word in ["revenue", "profit", "earnings"]):
            return "financial"
        else:
            return "general"

    def _summarize(self, text):
        sentences = text.split(". ")
        return sentences[0] + "." if sentences else text[:100]

# Usage
enricher = MetadataEnricher()

chunk = "Apple Inc. reported Q4 2024 revenue of $119.6B, up 15% YoY..."
metadata = enricher.enrich(chunk, source="earnings_2024.pdf", page=5)

print(metadata)
# {
#   "source": "earnings_2024.pdf",
#   "page": 5,
#   "entities": {"organizations": ["Apple Inc."]},
#   "keywords": ["revenue", "Q4 2024", "Apple"],
#   "chunk_type": "financial",
#   "summary": "Apple reported Q4 2024 revenue...",
#   ...
# }
```

---

## Metadata-based Filtering

**Retriever with filtering:**
```python
# Example: Find revenue info from Q4 reports
results = vector_db.search(
    query_vector=query_embedding,
    filter={
        "must": [
            {"chunk_type": "financial"},
            {"keywords": {"contains": "revenue"}},
            {"year": 2025},
        ]
    },
    limit=5
)
```

**Benefits:**
- Precision: Only relevant documents
- Compliance: Filter by date (recent documents)
- Authority: Filter by source type (official reports > emails)

---

## Performance Optimization

**Don't enrich everything:**
```python
# Bad: Enrich 100K chunks (expensive)
for chunk in all_chunks:
    metadata = enricher.enrich(chunk)

# Good: Enrich sample, extrapolate
sample_size = min(1000, len(all_chunks))
sample_metadata = [enricher.enrich(chunk) for chunk in all_chunks[:sample_size]]
# Use patterns from sample for remaining chunks
```

**Batch processing:**
```python
from concurrent.futures import ThreadPoolExecutor

def enrich_batch(chunks, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        metadata_list = list(executor.map(enricher.enrich, chunks))
    return metadata_list
```

---

## When Metadata Matters Most

**High impact:**
1. ✓ **Date filtering**: "Only search recent documents"
2. ✓ **Authority filtering**: "Prefer official reports"
3. ✓ **Document type**: "Search only in FAQs"
4. ✓ **Entity filtering**: "Find about this company"

**Lower impact:**
- Summaries (nice to have in UI, not critical for retrieval)
- Keywords (helpful but not essential)

---

## Common Mistakes

**❌ Over-enriching**
```python
# Bad: Extract 50 features per chunk
metadata = {
    "entity_1": ..., "entity_2": ..., ..., "entity_50": ...
}

# Good: Extract 5-10 most useful features
metadata = {
    "entities": [...],
    "keywords": [...],
    "document_type": "...",
    "date": "...",
}
```

**❌ Not validating extracted metadata**
```python
# Bad: Trust NER output blindly
entities = ner_model.extract(text)

# Good: Validate & clean
entities = [e for e in ner_model.extract(text) if len(e) > 2]
```

**❌ Breaking on extraction failure**
```python
# Bad: Pipeline crashes if summarization fails
metadata["summary"] = summarizer.summarize(text)

# Good: Graceful degradation
try:
    metadata["summary"] = summarizer.summarize(text)
except Exception:
    metadata["summary"] = text[:100]  # Fallback
```

---

## Vietnamese Metadata

Ensure UTF-8 everywhere:

```python
# Vietnamese enrichment
enricher = MetadataEnricher()
enricher.nlp = spacy.load("vi_core_news_sm")  # Vietnamese model

text = "Công ty Apple báo cáo doanh thu Q4 2024 là 119.6 tỷ đô..."
metadata = enricher.enrich(text)

# Results: entities include "Apple", "Q4 2024", "119.6 tỷ đô"
```

---

## Key Takeaway

Metadata transforms RAG từ "find similar text" thành "find relevant documents by context". Extract entities (company, person, date), keywords, document type, summary. Use metadata for filtering (improve precision), ranking (prioritize authority), context (help LLM). Don't over-extract (5-10 features enough). Batch process cho performance. Focus on high-impact metadata: dates, types, entities. Graceful degradation nếu extraction fails.
