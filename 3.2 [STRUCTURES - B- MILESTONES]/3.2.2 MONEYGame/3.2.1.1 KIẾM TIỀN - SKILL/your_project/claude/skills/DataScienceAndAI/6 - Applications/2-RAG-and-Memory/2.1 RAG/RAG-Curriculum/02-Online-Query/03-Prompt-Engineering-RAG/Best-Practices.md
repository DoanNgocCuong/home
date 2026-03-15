# Prompt Engineering cho RAG Systems

## Tổng Quan

Prompt kém có thể làm hỏng một RAG system tuyệt vời. Tài liệu truy xuất tốt không có ích nếu LLM không biết cách sử dụng chúng. Bài học này dạy cách thiết kế prompt để tối ưu hóa generation quality trong RAG context.

## Core Principles

1. **Be Explicit About Context** - Lặp lại tài liệu là retrieved, không phải training data
2. **Role Definition** - Định nghĩa LLM role rõ ràng
3. **Format Specification** - Chỉ định format output (JSON, markdown, etc.)
4. **Uncertainty Handling** - Dạy model khi nào nói "I don't know"
5. **Citation** - Yêu cầu trích dẫn explicit từ tài liệu

## POWER Framework

POWER là framework mạnh mẽ để thiết kế RAG prompts:

**P**urpose - Tác vụ cụ thể là gì?
**O**utput - Output nên trông như thế nào?
**W**ording - Dùng ngôn ngữ nào? (formal/casual)
**E**xamples - Cho examples của output tốt
**R**oles - LLM và retriever có roles gì?

## Production-Ready Prompt Template (YAML)

```yaml
rag_prompt_v1:
  role: |
    You are an AI assistant specialized in answering questions about
    [DOMAIN]. You have access to a knowledge base of [DOMAIN] documents.

  instruction: |
    Answer the following question based ONLY on the provided documents.
    If the documents do not contain enough information to answer,
    respond with "I don't have enough information to answer this question."

    Always cite your sources using [Source: Document Title].

  context_template: |
    ## Retrieved Documents:
    {% for doc in documents %}
    ### Document {{ loop.index }}: {{ doc.title }}
    {{ doc.content }}

    {% endfor %}

  output_format: |
    ## Answer
    [Your answer here]

    ## Sources
    - Document 1
    - Document 2

    ## Confidence Level
    [High/Medium/Low]

  examples:
    - question: "What is machine learning?"
      answer: |
        Machine learning is a subset of artificial intelligence...
        [Source: Machine Learning Fundamentals, Chapter 1]

        Confidence Level: High

  temperature: 0.3  # Lower = more focused on facts
  max_tokens: 500
```

## Implementation with LlamaIndex

```python
from llama_index import PromptTemplate
from llama_index.llms import OpenAI

# Define RAG prompt
rag_prompt_str = """\
You are an expert Q&A assistant. Your job is to answer questions about
the provided documents.

Context information is below.
-----
{context_str}
-----

Given the context information and not prior knowledge, answer the question.
Always cite the document title when referencing a source.

If the documents don't contain information to answer the question, say:
"I don't have enough information to answer this question."

Question: {query_str}
Answer: """

rag_prompt = PromptTemplate(rag_prompt_str)

# Use in query engine
query_engine = index.as_query_engine(
    text_qa_template=rag_prompt,
    similarity_top_k=5,
    response_mode="tree_summarize"
)

response = query_engine.query("What are RAG best practices?")
```

## Context Window Optimization

LLMs có limited context windows. Tối ưu hóa ngôn ngữ là crucial:

```python
# ❌ BAD: Tảng lớn dài dòng
context = """
Document 1: The quick brown fox jumps over the lazy dog.
This is a traditional sentence used for typing practice.
It contains all 26 letters of the English alphabet. ...
[1000 more words]
"""

# ✓ GOOD: Ngắn gọn, trực tiếp
context = """
**Doc 1 - Typing Practice**: Contains all English letters.

**Doc 2 - Keyboard History**: Mechanical keyboards are...

**Doc 3 - Speed Records**: World record is 216 WPM...
"""
```

**Context Window Budget:**
```
Total Context Window: 4096 tokens
- System Prompt: 100 tokens (2%)
- Retrieved Context: 2000 tokens (49%)
- Query: 100 tokens (2%)
- History (if any): 500 tokens (12%)
- Response: 1000 tokens (24%) ← Space for generation
═════════════════════════════════
Available for context: ~2000 tokens
```

## Handling "I Don't Know" Gracefully

```python
# Add explicit instruction
confidence_prompt = """\
After answering, add a confidence level:

High: Information is clearly stated in documents
Medium: Information is implied or partially present
Low: Information is not well-covered in documents

If confidence would be Very Low (< 30%),
respond: "I don't have reliable information on this topic."
"""

# Implementation
def should_respond(confidence: str, threshold: float = 0.3) -> bool:
    confidence_map = {"High": 1.0, "Medium": 0.6, "Low": 0.2}
    return confidence_map.get(confidence, 0) >= threshold
```

## Citation Strategy

**Option 1: Inline Citations**
```
RAG combines retrieval with generation [Source: RAG_Paper_2020.pdf, page 3].
It improves factuality [Source: RAG_Evaluation_2021.pdf].
```

**Option 2: Footnotes**
```
RAG combines retrieval with generation[1].
It improves factuality[2].

[1] RAG_Paper_2020.pdf, page 3
[2] RAG_Evaluation_2021.pdf
```

**Option 3: Structured**
```json
{
  "answer": "RAG combines retrieval with generation",
  "sources": [
    {
      "document": "RAG_Paper_2020.pdf",
      "page": 3,
      "quote": "RAG combines retrieval with generation"
    }
  ]
}
```

**Recommendation:** Option 1 (inline) cho user-facing, Option 3 (JSON) cho programmatic.

## Common Anti-Patterns

❌ **Vague context instructions**
```
"Use these documents: [all 20 documents]"
```
✓ **Explicit instructions**
```
"Answer using only the following documents.
Cite document title. Say 'I don't know' if not covered."
```

❌ **No output format**
```
"Answer the question"
```
✓ **Structured format**
```
"Respond in JSON: {answer: string, sources: string[], confidence: 'High'|'Medium'|'Low'}"
```

❌ **Mixing retriever + training knowledge**
```
"Use these documents AND your knowledge"
```
✓ **Clear source of truth**
```
"Use ONLY these documents. Ignore training knowledge."
```

## Prompt Versioning

```yaml
# versions/v1_baseline.yaml
temperature: 0.5
top_p: 0.9
template: "Answer based on context..."

# versions/v2_factual.yaml
temperature: 0.3  # More focused
top_p: 0.8
template: "Answer ONLY from documents..."
instruction: "Prioritize factuality over completeness"

# versions/v3_citations.yaml
extends: v2_factual
instruction: |
  Add [Doc: Title] after each factual claim.
  Use document titles, not page numbers.
```

## Testing Your Prompt

```python
test_cases = [
    {
        "query": "What is RAG?",
        "expected_coverage": ["retrieval", "generation", "augmented"],
        "should_cite": True,
        "max_length": 300
    },
    {
        "query": "What is Klingon technology?",  # Not in docs
        "expected_response": "I don't have information",
        "should_cite": False
    }
]

for test in test_cases:
    response = query_engine.query(test["query"])
    assert all(word in response.lower()
               for word in test["expected_coverage"])
```

## Key Takeaway

Prompt quality trong RAG tương đương với retrieval quality. Chốt cốt là:

1. **Be explicit** - Rõ ràng context từ retrieval, không phải training
2. **Format output** - Định dạng cụ thể (JSON, markdown, etc.)
3. **Handle uncertainty** - Dạy model nói "I don't know"
4. **Cite sources** - Yêu cầu trích dẫn explicit
5. **Version & test** - Iterate trên prompt như code

**Practical tip:** Prompt templates thay đổi chậm hơn retrieval strategies. Viết một lần, optimize thường xuyên. Sử dụng YAML cho version control dễ hơn.
