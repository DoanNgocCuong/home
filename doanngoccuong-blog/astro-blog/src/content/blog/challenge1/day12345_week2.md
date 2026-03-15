---
title: "Week 2 - Challenge 1: RAG Pipeline"
description: "Build & Evaluate hệ thống RAG Production - Action to Fresher AI Engineer"
pubDate: "2026-03-09"
updatedDate: "2026-03-12"
tags: ["RAG", "AI", "Challenge", "challenge-1", "week-2"]
---
# BÀI TẬP WEEK 2 - CHALLENGE 1 - WEACTION to Fresher AI Engineer - RAG PIPELINE — Build & Evaluate hệ thống RAG Production

> **Deadline nộp:** **Chủ nhật, 11:59PM** (Thời gian làm: Thứ 2 → Chủ nhật) — Ace nộp bài dưới bài đăng nhé

> Bài này được Cường soạn từ 20h tối - 3h rưỡi sáng ngày 11-12/3/2026 - Chúc ace học tốt nhé!

---

## 1. Tầm quan trọng

* Tuần 1 ace đã biết viết API + Docker (bài 1+2) và host SLM lên Production (bài 3+4+5). Đây là các kiến thức, kĩ năng căn bản nhất.
* Tuần 2 mình đi tiếp đến bài toán phổ biến nhất trong Applied AI:  **RAG** . Theo khảo sát 3,000 job listings AI ([Flex.ai, 2025](https://www.flex.ai/blog/the-state-of-ai-hiring-in-2025-insights-from-3-000-job-listings)), **~65% yêu cầu kinh nghiệm RAG** — nhiều hơn cả fine-tuning (~25%), nhiều hơn cả MLOps (~30%).

65% lấy từ đâu, các bạn có thể đọc ở đây:

* [The State of AI Hiring in 2025: Insights from 3,000 Job Listings — Flex.ai](https://www.flex.ai/blog/the-state-of-ai-hiring-in-2025-insights-from-3-000-job-listings)
* [Top 10 Most In-Demand AI Engineering Skills and Salary Ranges in 2026 — Second Talent](https://www.secondtalent.com/resources/most-in-demand-ai-engineering-skills-and-salary-ranges/)
* [AI Engineer Job Outlook 2025 — 365 Data Science](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/)

### 1.1 Tại sao RAG quan trọng ?

Hình dung thế này: sếp ace bảo  *"làm chatbot trả lời câu hỏi về nội quy công ty, 200 trang"* . Ace sẽ nghĩ đến 3 cách:

| Cách                  | Làm thế nào                                                                       | Vấn đề                                                                                                                                                   | Kết luận                         |
| ---------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Nhét hết vào prompt | Copy 200 trang vào mỗi lần hỏi                                                   | 200 trang ≈ 100K tokens. Tốn ~$1/câu hỏi, chậm 30s, vượt context limit hầu hết model. Hỏi 100 câu/ngày = $100/ngày chỉ cho 1 chatbot nội bộ | Không khả thi                    |
| Fine-tune model        | Train model học thuộc nội quy                                                     | Cần 2-4 tuần chuẩn bị data + training. Sếp sửa 1 dòng nội quy → train lại từ đầu. GPU tốn hàng ngàn đô                                    | Quá chậm, quá đắt             |
| **RAG**          | Embed 200 trang 1 lần, mỗi câu hỏi chỉ lấy 3-5 đoạn liên quan đưa cho LLM | Setup 1-2 ngày. Sửa nội quy → re-embed file đó trong 30 giây. LLM đọc 500 tokens thay vì 100K. Self-host thì chi phí gần bằng 0               | **Cách duy nhất hợp lý** |

### 1.2 Mọi hệ thống RAG production đều vận hành theo 3 pha: Offline, Online, Eval

#### Baseline pipeline

```
┌─────────────────────────────────────────────────────┐
│              RAG PIPELINE — BASELINE                 │
│                                                      │
│  OFFLINE:  Tài liệu → Chunks → Embed → Vector DB   │
│                                                      │
│  ONLINE:   Câu hỏi → Tìm chunks → Prompt → LLM    │
│                         gần nhất     ↓               │
│                                   Answer + Sources   │
│                                                      │
│  EVAL:     20 câu test → Chạy pipeline → Điểm RAGAS│
└─────────────────────────────────────────────────────┘
```

#### Advance RAG pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA SOURCES (Raw Documents)                     │
│            PDFs, HTML, DOCX, JSON, Database, API, Crawl             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
         ╔═════════════════╧═══════════════════════╗
         ║   PHASE 1: OFFLINE INGESTION PIPELINE   ║
         ║   (Chạy batch khi có document mới)      ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   Document    Chunking    Embedding        ║
         ║   Parsing  →  Strategy →  Model     →  Vector DB
         ║      ↓                                     ║
         ║   Metadata Enrichment (NER, tags, summary) ║
         ║                                            ║
         ╚════════════════════╤═══════════════════════╝
                              │
                    Knowledge Base Ready
                              │
         ╔════════════════════╧═══════════════════════╗
         ║   PHASE 2: ONLINE QUERY PIPELINE           ║
         ║   (Real-time mỗi khi user hỏi)            ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   User Query                               ║
         ║      ↓                                     ║
         ║   Query Processing (rewrite, expand)       ║
         ║      ↓                                     ║
         ║   Hybrid Retrieval (Vector + BM25)         ║
         ║      ↓                                     ║
         ║   Reranking (cross-encoder)                ║
         ║      ↓                                     ║
         ║   Context Assembly + Prompt Template       ║
         ║      ↓                                     ║
         ║   LLM Generation (streaming)               ║
         ║      ↓                                     ║
         ║   Response + Sources + Tracing             ║
         ║                                            ║
         ╚════════════════════╤═══════════════════════╝
                              │
         ╔════════════════════╧═══════════════════════╗
         ║   PHASE 3: EVALUATION LOOP CONTINUOUS      ║
         ║   (Chạy liên tục, không ngừng cải thiện)  ║
         ╠════════════════════════════════════════════╣
         ║                                            ║
         ║   Langfuse Tracing  →  RAGAS Metrics       ║
         ║      ↓                                     ║
         ║   Monitor Quality (Faithfulness, Relevancy)║
         ║      ↓                                     ║
         ║   Capture Failures → Curate Eval Dataset   ║
         ║      ↓                                     ║
         ║   A/B Test Configs → Deploy Improvements   ║
         ║                                            ║
         ╚════════════════════════════════════════════╝
```

---

### 1.3 Yêu cầu về mức độ triển khai

> Trong dự án này: các bạn có thể chọn 1 trong 3 mức độ triển khai ở bảng bên dưới:

| Mức                                  | Mô tả                              | Yêu cầu cụ thể                                                                                                                                                                                                                                                              | Ai nên làm                                                                       |
| :------------------------------------ | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------- |
| **⭐ BASELINE (Bắt buộc)**    | RAG chạy được, đo được       | Vector search (cosine) + Recursive chunking 512 tokens + 1 embedding model (BGE-M3/Jina-v3-embedding)  + Qdrant + vLLM/Ollama +`POST /query`trả answer + sources + RAGAS 2 metrics (Faithfulness, Answer Relevancy) + Docker Compose chạy full stack + Eval dataset 20 câu | **Tất cả ace**— đây là mức tối thiểu để bài nộp đạt chuẩn    |
| **⭐⭐ STANDARD (Nên có)**    | RAG chất lượng tốt hơn rõ rệt | Baseline + Hybrid search (Vector + BM25/BM42) + Reranking (BGE-reranker hoặc Cohere) + Prompt template tách file YAML + Similarity threshold (refuse khi không tìm thấy) + Metadata trong chunks (source, page, section)                                                   | **Ace muốn portfolio mạnh**— đây là mức nhà tuyển dụng ấn tượng |
| **⭐⭐⭐ ADVANCED (Nâng cao)** | Production-grade                     | Standard + Langfuse tracing toàn pipeline + RAGAS 4 metrics + A/B test 2 configs (so sánh chunk_size hoặc có/không rerank) + Structured JSON logging + Query rewrite/expansion + Streaming response                                                                        | **Ace muốn đi đầu**— mức này ngang junior engineer                    |

---

## 2. SAI LẦM THƯỜNG GẶP VỀ TƯ DUY THIẾT KẾ

> Một số tư duy sai khi thiết kế pipeline các bạn cần tránh:

| # | Sai lầm tư duy                                            | Fresher thường nghĩ                                                | Thực tế production                                                                                                                                                                                                                                                                                                                               | Cách tư duy đúng                                                                                                                                                                                            |
| :- | :---------------------------------------------------------- | :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 | **Nghĩ RAG là một model**                          | "RAG là model mới à? Dùng RAG thay GPT được không?"           | RAG không phải model. RAG là một**pipeline**— chuỗi các bước: parse → chunk → embed → store → retrieve → generate. Model (GPT, Qwen, Llama) chỉ là**1 bước**trong pipeline đó (bước generate). Nói "dùng RAG" giống nói "dùng dây chuyền sản xuất" — nó là cả hệ thống, không phải 1 linh kiện | **RAG = Retrieval-Augmented Generation = pipeline lấy data rồi đưa cho LLM.**LLM là engine, RAG là cả chiếc xe. Hiểu sai chỗ này → hiểu sai mọi thứ phía sau                                    |
| 1 | **Cứ nhét tài liệu vào là LLM sẽ hiểu**       | "Mình có PDF rồi, parse xong nhét vào vector DB là xong"        | PDF parse ra lẫn header/footer/page number, chunk cắt giữa câu, metadata không có → retrieval trả rác → LLM trả lời dựa trên rác                                                                                                                                                                                                    | 80% chất lượng RAG nằm ở**data preparation** , không phải LLM. Clean data trước, đọc thử vài chunk xem con người có hiểu không — nếu người không hiểu thì LLM cũng không hiểu |
| 2 | **Retrieval đúng = Answer đúng**                  | "Retrieve đúng chunk rồi thì LLM sẽ trả lời đúng thôi"      | LLM vẫn bịa thêm, hiểu sai context, hoặc trả lời lan man dù chunk đúng. Ngược lại, retrieval sai thì LLM giỏi mấy cũng không cứu được                                                                                                                                                                                        | **70% lỗi RAG nằm ở retrieval.**Khi answer sai, debug retrieval TRƯỚC (chunks lấy có đúng không?), rồi mới debug generation (LLM hiểu sai chunk?)                                                  |
| 3 | **Demo 5 câu thấy ổn = RAG tốt**                  | "Hỏi thử 5 câu → trả lời đúng → ship thôi"                  | Lên production, user hỏi câu khó, câu mập mờ, câu ngoài tài liệu → vỡ trận. 5 câu dễ không đại diện cho 500 câu thật                                                                                                                                                                                                         | **Không có eval dataset + metric = không biết RAG tốt hay dở.**Tối thiểu 20 câu test đa dạng: dễ, khó, và câu không có đáp án trong tài liệu                                              |
| 4 | **RAG thay thế được fine-tuning**                 | "Có RAG rồi thì không cần fine-tune model nữa"                  | RAG bổ sung kiến thức ("LLM không biết info X"). Fine-tuning bổ sung kỹ năng ("LLM không biết reasoning theo style Y"). Ví dụ: RAG cho LLM đọc tài liệu y khoa → LLM vẫn không biết reasoning y khoa                                                                                                                           | **RAG = bổ sung kiến thức, Fine-tuning = bổ sung kỹ năng.**Hai thứ khác nhau, bổ trợ nhau, không thay thế nhau                                                                                      |
| 5 | **Chunk nhỏ = chính xác hơn**                     | "Chunk size 100 tokens cho chính xác, chunk lớn bị nhiễu"        | Chunk quá nhỏ → câu bị cắt giữa chừng, mất ngữ cảnh, LLM không hiểu. Chunk quá lớn → lẫn nhiều info không liên quan                                                                                                                                                                                                            | **Không có chunk size "đúng"**— chỉ có chunk size phù hợp với data cụ thể. Bắt đầu 512 tokens làm baseline, đo metric, rồi thử 256 và 1024 so sánh                                   |
| 6 | **Model embedding xịn nhất = retrieval tốt nhất** | "Top 1 MTEB leaderboard thì cứ dùng, khỏi nghĩ"                  | Model top MTEB train trên tiếng Anh → tiếng Việt tệ. Model tốt cho short text → tệ cho long paragraph. Leaderboard ≠ data thực tế của bạn                                                                                                                                                                                            | **Embedding model phải match ngôn ngữ + độ dài + domain**của data thật. Test trên 10-20 query thật trước khi chọn, đừng tin leaderboard mù quáng                                         |
| 7 | **User hỏi gì thì RAG phải trả lời được**    | "RAG phải luôn có answer, trả lời 'không biết' là thất bại" | Khi không có context liên quan mà vẫn cố trả lời → hallucination → user tin câu trả lời sai → tệ hơn không có RAG                                                                                                                                                                                                                | **RAG tốt phải biết nói "Tôi không biết"**— đây là feature, không phải bug. Set similarity threshold, dưới ngưỡng thì refuse thay vì bịa                                              |
| 8 | **Build xong pipeline là xong**                      | "Ship RAG → move on sang task khác"                                 | Tài liệu thay đổi, user hỏi kiểu mới, quality drift dần. Không ai biết RAG đang xuống chất lượng cho đến khi user complain                                                                                                                                                                                                        | **RAG production là vòng lặp: build → đo → cải thiện → đo lại.**Không phải project có deadline xong, mà là system cần maintain liên tục                                                      |

## 3. HƯỚNG DẪN LÀM BÀI TẬP

### 3.1 Có được dùng AI không?

Ace có thể dùng AI để hoàn thành bài tập. Nhưng video trình bày cần trình bày được để cho 1 người nghe có thể hiểu ace đang làm gì và làm như thế nào 1 cách tổng quát.

### 3.2 Gợi ý tài liệu để RAG:

Ace có thể dùng bất kỳ tài liệu nào: luật, hợp đồng, sách giáo khoa, documentation kỹ thuật, ... Gợi ý:

* 5-10 file PDF/DOCX tiếng Việt (hoặc tiếng Anh)
* Tối thiểu 20 trang text (đủ để chunking có ý nghĩa)
* Có nhiều chủ đề/section (test retrieval precision)

### 3.3 HIGH-LEVEL DESIGN — Kiến trúc tổng quát

> Kiến trúc này mình dùng AI để giúp các bạn có cái nhìn tổng quát về 1 hệ thống RAG.
>
> +, Ở phần 1 mình đã trình bày kiến trúc baseline và kiến trúc mở rộng advanced rùi.
>
> +, Ở phần này mình sẽ đi sâu hơn để xem trong mỗi phần advanced nó lại có nhiều cách thức khác nhau như nào. (ngoài ra còn nhiều cách hơn nữa).
>
> +, Khi vào dự án thật, các bạn nên bắt đầu từ baseline và mở rộng dần ra.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION RAG ARCHITECTURE                           │
│                                                                         │
│  "3 Pha — mỗi pha có nhiều lựa chọn, mỗi lựa chọn có trade-off"      │
└─────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
 PHASE 1: OFFLINE INGESTION — "Nén data thành vectors"
═══════════════════════════════════════════════════════════════════════════

  Documents (PDF, HTML, DOCX)
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 1.1: DOCUMENT PARSING                                         │
  │                                                                      │
  │  "Trích xuất text sạch từ raw files"                                │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  PyMuPDF4LLM     │  │  Docling (IBM)   │  │  Unstructured    │  │
  │  │  (pymupdf4llm)   │  │                  │  │  + Tesseract     │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ Speed:  0.12s/doc│  │ Speed:  ~2s/doc  │  │ Speed:  1.3s/doc │  │
  │  │ Output: Markdown │  │ Output: Markdown │  │ Output: Elements │  │
  │  │ OCR:    ❌        │  │ OCR:    ✅ (AI)  │  │ OCR:    ✅ Tess. │  │
  │  │ Tables: ⚠️ Basic │  │ Tables: ✅ 97.9% │  │ Tables: ✅ ~75%  │  │
  │  │ Images: ❌        │  │ Images: ✅       │  │ Images: ✅       │  │
  │  │ Install: pip     │  │ Install: pip     │  │ Install: Heavy   │  │
  │  │ Formats: PDF     │  │ Formats: PDF,    │  │ Formats: PDF,    │  │
  │  │                  │  │  DOCX, HTML,     │  │  DOCX, HTML,     │  │
  │  │                  │  │  PPTX, Images    │  │  CSV, Markdown   │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  Khi nào dùng cái nào?                                              │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ PDF text-only, cần nhanh  → PyMuPDF4LLM (0.12s, best speed) │  │
  │  │ PDF có bảng/hình phức tạp → Docling (97.9% table accuracy)  │  │
  │  │ Multi-format + OCR legacy → Unstructured (ecosystem lớn)     │  │
  │  └────────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND cho bài tập: PyMuPDF4LLM — nhanh, output Markdown    │
  │    sạch, giữ heading hierarchy. Upgrade → Docling nếu có tables.   │
  │                                                                      │
  │  Refs: [PDF Benchmark 2025](https://procycons.com/en/blogs/         │
  │        pdf-data-extraction-benchmark/)                               │
  │        [7 PDF Extractors Test](https://dev.to/onlyoneaman/          │
  │        i-tested-7-python-pdf-extractors-2025-edition-akm)           │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 1.2: CHUNKING STRATEGY                                        │
  │                                                                      │
  │  "Chia document thành đoạn nhỏ để tìm kiếm chính xác"             │
  │                                                                      │
  │  ┌────────────────┐ ┌────────────────┐ ┌──────────────┐ ┌────────┐ │
  │  │ Recursive      │ │ Semantic       │ │ LLM-based /  │ │ Struct-│ │
  │  │ Character      │ │ Chunking       │ │ Agentic      │ │ ure-   │ │
  │  │                │ │                │ │ Chunking     │ │ Aware  │ │
  │  ├────────────────┤ ├────────────────┤ ├──────────────┤ ├────────┤ │
  │  │Accuracy:       │ │Accuracy:       │ │Accuracy:     │ │Acc:    │ │
  │  │ 69% (baseline) │ │ 54-92%         │ │ 80-87%       │ │ ~80%   │ │
  │  │ (Vecta bench)  │ │ (biến thiên    │ │ (clinical    │ │        │ │
  │  │                │ │  cao, phụ thuộc│ │  study 2025) │ │        │ │
  │  │Speed: ★★★★★   │ │  embed model)  │ │              │ │Speed:  │ │
  │  │Cost:  Free     │ │Speed: ★★★     │ │Speed: ★★    │ │ ★★★★  │ │
  │  │                │ │Cost:  Embed    │ │Cost:  LLM    │ │Cost:   │ │
  │  │Config:         │ │  API/GPU       │ │  API call    │ │ Free   │ │
  │  │ 512 tokens     │ │               │ │  per chunk   │ │        │ │
  │  │ + 50 overlap   │ │Cần embedding  │ │              │ │Cần     │ │
  │  │                │ │model để detect│ │LLM quyết     │ │heading │ │
  │  │Đơn giản,       │ │topic boundary │ │định ranh      │ │cấu trúc│ │
  │  │deterministic   │ │               │ │giới chunk    │ │sẵn     │ │
  │  │                │ │Variance cao:  │ │dựa trên ngữ  │ │        │ │
  │  │                │ │output phụ     │ │nghĩa         │ │        │ │
  │  │                │ │thuộc nhiều    │ │              │ │        │ │
  │  │                │ │vào model      │ │Tốn nhất,     │ │        │ │
  │  │                │ │               │ │nhưng chunk   │ │        │ │
  │  │                │ │               │ │quality cao   │ │        │ │
  │  └────────────────┘ └────────────────┘ └──────────────┘ └────────┘ │
  │                                                                      │
  │  Khi nào dùng cái nào?                                              │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ Bắt đầu / Baseline        → Recursive 512 tokens + overlap  │  │
  │  │ RAGAS Context Prec < 0.7  → Semantic Chunking (upgrade)     │  │
  │  │ Tài liệu đặc thù (legal, │                                  │  │
  │  │   medical, mixed-topic)   → LLM-based Chunking              │  │
  │  │ Docs có heading rõ ràng   → Structure-Aware (Markdown H1-H3)│  │
  │  └────────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND: Recursive 512 tokens — deterministic, nhanh,         │
  │    reproducible. Đây là baseline. Measure trước, optimize sau.      │
  │                                                                      │
  │  Refs: [Chunking Strategies 2026](https://www.firecrawl.dev/blog/   │
  │        best-chunking-strategies-rag)                                 │
  │        [9 Strategies Tested](https://langcopilot.com/posts/         │
  │        2025-10-11-document-chunking-for-rag-practical-guide)        │
  │        [Agentic Chunking IBM](https://www.ibm.com/think/topics/     │
  │        agentic-chunking)                                             │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 1.3: EMBEDDING MODEL                                          │
  │                                                                      │
  │  "Chuyển text → vector số để máy so sánh semantic"                  │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  BGE-M3          │  │  Jina v3         │  │  OpenAI          │  │
  │  │  (BAAI)          │  │  (Jina AI)       │  │  text-3-large    │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ MTEB:  63.0      │  │ MTEB:  65.5      │  │ MTEB:  64.6      │  │
  │  │ Dim:   1024      │  │ Dim:   1024      │  │ Dim:   3072      │  │
  │  │ Params: 568M     │  │ Params: 570M     │  │ Params: N/A      │  │
  │  │ MaxLen: 8192     │  │ MaxLen: 8192     │  │ MaxLen: 8191     │  │
  │  │ Viet:  ★★★★     │  │ Viet:  ★★★★★    │  │ Viet:  ★★★      │  │
  │  │ Lang:  100+      │  │ Lang:  89        │  │ Lang:  ~100      │  │
  │  │                  │  │                  │  │                  │  │
  │  │ License: MIT     │  │ License: Apache  │  │ License: Prop    │  │
  │  │ Cost: FREE       │  │ Cost: FREE*      │  │ Cost: $0.13/1M   │  │
  │  │                  │  │                  │  │       tokens     │  │
  │  │ Self-host:       │  │ Self-host:       │  │ Self-host: ❌     │  │
  │  │  ✅ NVIDIA NIM   │  │  ✅ Infinity     │  │  (API only)      │  │
  │  │  ✅ Ollama       │  │  Server          │  │                  │  │
  │  │  ✅ HF TEI      │  │  (Docker GPU)    │  │                  │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  ┌─────────────────────────────────────────────────────────────────┐ │
  │  │              Jina v3 — SELF-HOST VÀ FREE                       │ │
  │  │                                                                 │ │
  │  │  Nhiều ace hỏi: "Jina v3 có self-host được không?"            │ │
  │  │  → CÓ! Dùng Infinity Embedding Server:                        │ │
  │  │                                                                 │ │
  │  │  Docker image: michaelf34/infinity:latest                      │ │
  │  │  Command:                                                       │ │
  │  │    v2 --model-id jinaai/jina-embeddings-v3                     │ │
  │  │       --batch-size 128 --port 18081 --engine torch             │ │
  │  │                                                                 │ │
  │  │  GPU: ~3-4GB VRAM (1 GPU)                                      │ │
  │  │  API: OpenAI-compatible endpoint                                │ │
  │  │  Bonus: Infinity cũng serve được reranker models!              │ │
  │  │                                                                 │ │
  │  │  → Model weights FREE trên HuggingFace (Apache 2.0)           │ │
  │  │  → Jina API cũng có free tier                                  │ │
  │  │  → Self-host = FREE forever, không giới hạn requests          │ │
  │  └─────────────────────────────────────────────────────────────────┘ │
  │                                                                      │
  │  So sánh chi tiết BGE-M3 vs Jina v3:                                │
  │  ┌─────────────────────────────────────────────────────────────────┐ │
  │  │ Tiêu chí           │ BGE-M3           │ Jina v3              │ │
  │  │ ────────────────────┼──────────────────┼────────────────────  │ │
  │  │ Accuracy (MTEB)     │ 63.0             │ 65.5 (+2.5)         │ │
  │  │ Vietnamese quality  │ Tốt              │ Tốt hơn (89 langs)  │ │
  │  │ Self-host Docker    │ NVIDIA NIM,      │ Infinity Server,     │ │
  │  │                     │ Ollama, HF TEI   │ HuggingFace TEI     │ │
  │  │ Self-host latency   │ <30ms/query      │ ~30-60ms/query      │ │
  │  │                     │ (NVIDIA NIM      │ (Infinity, phụ thuộc│ │
  │  │                     │  optimized)      │  batch-size & GPU)  │ │
  │  │ API option          │ Không có API     │ Jina API (free tier)│ │
  │  │                     │ chính thức       │                     │ │
  │  │ Cost (self-host)    │ FREE (MIT)       │ FREE (Apache 2.0)   │ │
  │  │ Sparse vectors      │ ✅ (hybrid)      │ ✅ (Late Interact.) │ │
  │  │ Ecosystem           │ Rộng hơn (NIM,   │ Infinity Server     │ │
  │  │                     │  Ollama, TEI)    │                     │ │
  │  └─────────────────────────────────────────────────────────────────┘ │
  │                                                                      │
  │  ★ RECOMMEND cho bài tập:                                           │
  │    Có GPU → Jina v3 self-host via Infinity (accuracy cao nhất,     │
  │             Vietnamese tốt nhất, Docker sẵn, FREE)                  │
  │    Có GPU → BGE-M3 cũng tốt (ecosystem rộng hơn, latency thấp)    │
  │    Không GPU → Jina v3 API (free tier) hoặc OpenAI API             │
  │                                                                      │
  │  Refs: [Jina v3 HuggingFace](https://huggingface.co/jinaai/        │
  │        jina-embeddings-v3)                                           │
  │        [Infinity Server](https://github.com/michaelfeil/infinity)   │
  │        [BGE-M3 HuggingFace](https://huggingface.co/BAAI/bge-m3)    │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 1.4: VECTOR DATABASE                                          │
  │                                                                      │
  │  "Lưu vectors + tìm kiếm similarity siêu nhanh"                    │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  Qdrant          │  │  Chroma          │  │  Milvus          │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ Lang: Rust       │  │ Lang: Python     │  │ Lang: Go/C++     │  │
  │  │ P50:   8ms       │  │ P50:   ~30ms     │  │ P50:   12ms      │  │
  │  │ Scale: Millions  │  │ Scale: <1M       │  │ Scale: 10B+      │  │
  │  │ Hybrid: ✅ BM42  │  │ Hybrid: ❌        │  │ Hybrid: ✅       │  │
  │  │ Filter: ★★★★★   │  │ Filter: ★★★     │  │ Filter: ★★★★    │  │
  │  │ Docker: ✅ Easy   │  │ Docker: ✅ Easy   │  │ Docker: ⚠️ Heavy │  │
  │  │ Production: ✅    │  │ Production: ❌    │  │ Production: ✅   │  │
  │  │ Dashboard: ✅     │  │ Dashboard: ❌     │  │ Dashboard: ✅    │  │
  │  │                  │  │                  │  │  (Attu)          │  │
  │  │ RAM: ~500MB      │  │ RAM: ~200MB      │  │ RAM: ~2GB+       │  │
  │  │                  │  │ (embedded mode)  │  │ (etcd+minio+     │  │
  │  │                  │  │                  │  │  standalone)     │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  Khi nào dùng cái nào?                                              │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ Production + Hybrid search → Qdrant (Rust, nhanh, BM42 built │  │
  │  │   in, payload filter mạnh, Docker 1 container)               │  │
  │  │ Prototype nhanh, <1M docs  → Chroma (embedded mode, no server│  │
  │  │   cần, pip install xong chạy luôn)                           │  │
  │  │ Scale 10B+ vectors         → Milvus (nhưng overkill cho     │  │
  │  │   fresher, Docker Compose phức tạp: etcd + minio + milvus)  │  │
  │  └────────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND: Qdrant — Rust-based, nhanh nhất, built-in hybrid    │
  │    search (BM42), payload filtering mạnh, Docker 1 lệnh là chạy.  │
  │    `docker run -p 6333:6333 qdrant/qdrant:v1.12.0`                 │
  │                                                                      │
  │  Refs: [Qdrant Hybrid Search](https://qdrant.tech/articles/         │
  │        hybrid-search/)                                               │
  │        [BM42 — Qdrant](https://qdrant.tech/articles/bm42/)         │
  └──────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
 PHASE 2: ONLINE QUERY — "Trích xuất khi user hỏi"
═══════════════════════════════════════════════════════════════════════════

  User Query: "Báo cáo nói gì về revenue Q4?"
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 2.1: RETRIEVAL STRATEGY                                       │
  │                                                                      │
  │  "Tìm chunks liên quan nhất — bước quyết định 70% chất lượng RAG" │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  Vector Only     │  │  Hybrid Search   │  │  Multi-Query     │  │
  │  │  (Dense Cosine)  │  │  (Vector + BM25) │  │  + Hybrid        │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ Recall: ~0.72    │  │ Recall: ~0.91    │  │ Recall: ~0.95    │  │
  │  │ Precision: ~0.68 │  │ Precision: ~0.87 │  │ Precision: ~0.89 │  │
  │  │ Speed:   ★★★★★  │  │ Speed:   ★★★★   │  │ Speed:   ★★★    │  │
  │  │ Complexity: Low  │  │ Complexity: Med  │  │ Complexity: High │  │
  │  │                  │  │                  │  │                  │  │
  │  │ Miss exact       │  │ Fusion: RRF      │  │ Cần extra LLM   │  │
  │  │ keywords:        │  │ (Reciprocal Rank │  │ call để rewrite  │  │
  │  │ "Điều 15" fail  │  │  Fusion)         │  │ query thành 3-5  │  │
  │  │ "mã số thuế"    │  │                  │  │ biến thể trước   │  │
  │  │ fail             │  │ Dense bắt nghĩa │  │ khi search       │  │
  │  │                  │  │ BM25 bắt keyword │  │                  │  │
  │  │                  │  │ → Best balance   │  │ +200-400ms       │  │
  │  │                  │  │                  │  │ latency          │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  Hybrid Search hoạt động thế nào?                                   │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ User Query                                                     │  │
  │  │     ├──→ Dense Search (embedding) ──→ Top-50 results          │  │
  │  │     └──→ BM25 Search (keywords)  ──→ Top-50 results          │  │
  │  │                    │                                           │  │
  │  │                    ▼                                           │  │
  │  │            RRF Fusion (merge 2 ranked lists)                   │  │
  │  │                    │                                           │  │
  │  │                    ▼                                           │  │
  │  │            Top-20 candidates → Reranker                       │  │
  │  └────────────────────────────────────────────────────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND: Hybrid Search (Vector + BM25 + RRF)                  │
  │    → Qdrant built-in hybrid (BM42) hoặc custom BM25 + RRF         │
  │    → Minimum viable: Vector only cũng OK cho bài tập              │
  │                                                                      │
  │  Refs: [Hybrid Search RAG](https://app.ailog.fr/en/blog/guides/    │
  │        hybrid-search-rag)                                            │
  │        [Qdrant Reranking Tutorial](https://qdrant.tech/             │
  │        documentation/advanced-tutorials/reranking-hybrid-search/)   │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 2.2: RERANKING                                                │
  │                                                                      │
  │  "Lọc lại top-K cho chính xác hơn"                                 │
  │                                                                      │
  │  Retrieve top-20 (fast, approximate)                                │
  │      ↓                                                              │
  │  Rerank → top-5 (slow, precise)                                     │
  │      ↓                                                              │
  │  Impact: +20-35% Hit Rate, -35% Hallucination                      │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  BGE-reranker    │  │  Cohere Rerank   │  │  No Reranking    │  │
  │  │  v2-m3 (GPU)     │  │  3.5 (API)       │  │  (baseline)      │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ Latency:         │  │ Latency:         │  │ Latency: 0ms     │  │
  │  │  50-100ms (GPU)  │  │  ~600ms (API)    │  │                  │  │
  │  │ Cost: FREE       │  │ Cost: $0.003/req │  │ Cost: FREE       │  │
  │  │ Accuracy: ★★★★  │  │ Accuracy: ★★★★★ │  │ Accuracy: ★★    │  │
  │  │ Need: GPU        │  │ Need: API key    │  │ Need: nothing    │  │
  │  │                  │  │                  │  │                  │  │
  │  │ Self-host:       │  │ 32K context      │  │ Mất 20-35%      │  │
  │  │ Infinity Server  │  │ window           │  │ accuracy so với │  │
  │  │ hoặc HF TEI     │  │ Multilingual     │  │ có reranking    │  │
  │  │                  │  │ top-tier         │  │                  │  │
  │  │ Deploy cùng      │  │                  │  │                  │  │
  │  │ Infinity với     │  │                  │  │                  │  │
  │  │ embedding!       │  │                  │  │                  │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND:                                                        │
  │    Có GPU → BGE-reranker-v2-m3 (self-host, free, có thể deploy    │
  │             trên cùng Infinity Server với Jina v3 embedding!)       │
  │    Không GPU → skip rerank (nice-to-have cho bài tập,             │
  │                must-have production)                                 │
  │                                                                      │
  │  Refs: [Top 7 Rerankers 2025](https://www.analyticsvidhya.com/     │
  │        blog/2025/06/top-rerankers-for-rag/)                         │
  │        [Best Reranker Models 2026](https://docs.bswen.com/blog/    │
  │        2026-02-25-best-reranker-models/)                            │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 2.3: LLM GENERATION                                           │
  │                                                                      │
  │  "Dùng LLM từ Week 1 để generate answer"                           │
  │                                                                      │
  │  Ace dùng CHÍNH vLLM + Qwen 2.5 đã host ở bài tập Week 1!        │
  │  → Đây là lý do bài tập được thiết kế nối tiếp nhau.              │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  vLLM (Week 1)   │  │  Ollama (local)  │  │  OpenAI API      │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ TTFT: 50ms       │  │ TTFT: 200ms      │  │ TTFT: ~100ms     │  │
  │  │ Cost: Self-host  │  │ Cost: Self-host  │  │ Cost: API        │  │
  │  │ Throughput:       │  │ Throughput:       │  │ Throughput:       │  │
  │  │  ★★★★★          │  │  ★★              │  │  ★★★★★          │  │
  │  │ (PagedAttention, │  │ (single request  │  │ (rate limited)   │  │
  │  │  continuous      │  │  optimized)      │  │                  │  │
  │  │  batching)       │  │                  │  │                  │  │
  │  │                  │  │                  │  │                  │  │
  │  │ API: OpenAI-     │  │ API: OpenAI-     │  │ API: OpenAI      │  │
  │  │ compatible       │  │ compatible       │  │ native           │  │
  │  │ GPU: Required    │  │ GPU: Optional    │  │ GPU: N/A         │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND: Reuse vLLM từ Week 1 (OpenAI-compatible API)        │
  │    Không có GPU → Ollama (qwen2.5:1.5b) hoặc OpenAI API đều OK   │
  │                                                                      │
  │  Lưu ý về Prompt Template:                                          │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ - Tách file YAML, KHÔNG hardcode trong code                   │  │
  │  │ - "CHỈ trả lời dựa trên context. Không tìm thấy → nói       │  │
  │  │    không biết. Trích dẫn nguồn."                              │  │
  │  │ - Response format: {"answer": "...", "sources": [...]}        │  │
  │  │ - Similarity threshold: score < 0.3 → auto refuse            │  │
  │  └────────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
 PHASE 3: EVALUATION LOOP — "Đo → Cải thiện → Lặp lại"
═══════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 3.1: EVALUATION METRICS (RAGAS)                               │
  │                                                                      │
  │  "Không đo = không biết RAG tốt hay dở"                            │
  │                                                                      │
  │  4 Metrics cốt lõi:                                                 │
  │  ┌───────────────────────┐  ┌───────────────────────┐              │
  │  │ Faithfulness          │  │ Answer Relevancy      │              │
  │  │ "Answer đúng với      │  │ "Answer trả lời đúng  │              │
  │  │  context không?"      │  │  câu hỏi không?"      │              │
  │  │                       │  │                       │              │
  │  │  Target: > 0.7        │  │  Target: > 0.7        │              │
  │  │  Ideal:  > 0.8        │  │  Ideal:  > 0.8        │              │
  │  │                       │  │                       │              │
  │  │  Đo: LLM check từng  │  │  Đo: LLM generate     │              │
  │  │  claim trong answer   │  │  câu hỏi ngược từ     │              │
  │  │  có trong context?    │  │  answer, so với query  │              │
  │  └───────────────────────┘  └───────────────────────┘              │
  │  ┌───────────────────────┐  ┌───────────────────────┐              │
  │  │ Context Precision     │  │ Context Recall        │              │
  │  │ "Top-K chunks có      │  │ "Có thiếu info quan   │              │
  │  │  relevant không?"     │  │  trọng không?"        │              │
  │  │                       │  │                       │              │
  │  │  Target: > 0.7        │  │  Target: > 0.7        │              │
  │  │                       │  │                       │              │
  │  │  Thấp → retrieval     │  │  Thấp → cần nhiều    │              │
  │  │  hoặc reranking kém  │  │  chunks hơn, hoặc     │              │
  │  │                       │  │  chunking kém         │              │
  │  └───────────────────────┘  └───────────────────────┘              │
  │                                                                      │
  │  ★ Tối thiểu cho bài tập: Faithfulness + Answer Relevancy         │
  │    Nâng cao: + Context Precision + Context Recall                   │
  │                                                                      │
  │  Refs: [RAGAS Documentation](https://docs.ragas.io/)               │
  └──────────────────────────────────────────────────────────────────────┘
      ↓
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STEP 3.2: TRACING & OBSERVABILITY                                  │
  │                                                                      │
  │  "Nhìn thấy từng step trong pipeline — debug mà không có trace     │
  │   = mò kim đáy bể"                                                  │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
  │  │  Langfuse        │  │  LangSmith       │  │  Structured      │  │
  │  │  (Self-host)     │  │  (SaaS)          │  │  Logging         │  │
  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤  │
  │  │ License: MIT     │  │ License: Prop    │  │ License: N/A     │  │
  │  │ Cost: FREE       │  │ Cost: Freemium   │  │ Cost: FREE       │  │
  │  │ Self-host: ✅     │  │ Self-host: ❌     │  │ Self-host: ✅     │  │
  │  │ UI Dashboard: ✅  │  │ UI Dashboard: ✅  │  │ UI: ❌            │  │
  │  │ LLM cost track: ✅│  │ LLM cost track:✅ │  │ LLM cost: ❌     │  │
  │  │ Trace timeline: ✅│  │ Trace timeline:✅ │  │ Trace: ❌        │  │
  │  │                  │  │                  │  │                  │  │
  │  │ Docker Compose:  │  │ Cloud only       │  │ Python logging   │  │
  │  │ langfuse/langfuse│  │ smith.langchain  │  │ + JSON format    │  │
  │  │ :2 + PostgreSQL  │  │ .com             │  │                  │  │
  │  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
  │                                                                      │
  │  ★ RECOMMEND: Langfuse (Docker self-host, MIT, free)               │
  │    Minimum viable: Structured JSON logging cũng OK cho bài tập    │
  └──────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
 LATENCY BUDGET — Mỗi step được bao nhiêu ms?
═══════════════════════════════════════════════════════════════════════════

  Target: P95 < 2.5 giây (end-to-end bao gồm LLM generation)

  Component              │ Budget      │ Tool cụ thể
  ───────────────────────┼─────────────┼──────────────────
  Query embedding        │ < 30ms      │ BGE-M3 / Jina v3
  Vector search          │ < 20ms      │ Qdrant
  BM25 search (parallel) │ < 15ms      │ Qdrant BM42 / Rank-BM25
  Reranking (optional)   │ < 100ms     │ BGE-reranker (GPU)
  Prompt construction    │ < 10ms      │ YAML template
  LLM TTFT              │ < 80ms      │ vLLM
  LLM full generation   │ < 300ms     │ vLLM streaming
  ───────────────────────┼─────────────┼──────────────────
  TOTAL to first token   │ < 250ms     │
  TOTAL full response    │ < 500ms     │
```

---

### 3.4 Hướng dẫn chi tiết

> **Lưu ý:** Không có hướng dẫn code chi tiết — các bạn tự implement, có thể sử dụng AI hoặc tham khảo tài liệu chính thức.
>
> +, Giống như lúc đi làm thui, toàn bộ các bài toán sẽ mới và vừa làm vừa học, research và triển khai. Hiện nay có AI sẽ giúp tăng tốc điều này cho mọi người |
>
> +, Có khó khăn/mắc ở đâu mọi người nhắn riêng / nhắn nhóm luôn nhé. Cố gắng nhen!

#### 3.4.1 STEP BY STEP

**Bước 0 — Setup infrastructure (Docker Compose):**

* Qdrant: `qdrant/qdrant:v1.12.0` port 6333
* Embedding: Infinity Server + Jina v3 (hoặc BGE-M3), xem Docker Compose bên dưới
* Redis: `redis:7-alpine` port 6379 (optional, cho caching)
* vLLM: reuse từ Week 1 (hoặc Ollama nếu không có GPU)
* RAG API: FastAPI service (ace viết)
* (Optional) Langfuse: `langfuse/langfuse:2` port 3000

**Docker Compose mẫu — Embedding Server (Jina v3 + Infinity):**

```yaml
services:
  jina-embedding:
    container_name: jina-embedding
    image: michaelf34/infinity:0.0.77
    restart: always
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 3G
          devices:
            - driver: nvidia
              device_ids: ["0"]
              capabilities: [gpu]
    ports:
      - "18081:18081"
    volumes:
      - ./hf_cache:/app/.cache
    environment:
      - CUDA_VISIBLE_DEVICES=0
    command: v2 --model-id jinaai/jina-embeddings-v3 --batch-size 128 --port 18081 --engine torch
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:18081/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 120s
```

**Bước 1 — Ingestion Pipeline:**

* Load documents (PDF/DOCX) → parse text (PyMuPDF4LLM hoặc Docling)
* Chunk: RecursiveCharacterTextSplitter, 512 tokens, overlap 50
* Embed: Jina v3 via Infinity (hoặc BGE-M3, hoặc Jina API)
* Store: Qdrant collection + metadata (source, page, section)

**Bước 2 — Query Pipeline:**

* User gửi query qua `POST /query`
* Embed query → search Qdrant top-20 (hybrid nếu có BM25)
* (Optional) Rerank → top-5
* Build prompt từ template + top contexts
* Call vLLM → generate answer + sources
* Return response

**Bước 3 — Evaluation:**

* Tạo eval dataset: 20 cặp (question, ground_truth)
* Chạy RAGAS: đo Faithfulness + Answer Relevancy
* Report kết quả trong README

#### 3.4.2 Nếu ace không có GPU

* **Embedding** : Dùng Jina v3 API (free tier) thay vì self-host
* **LLM** : Dùng Ollama (`ollama pull qwen2.5:1.5b`) hoặc OpenAI API
* **Reranking** : Skip (không bắt buộc cho bài tập)

> Dù chọn giải pháp nào, ae vẫn phải hoàn thành đủ output bên dưới. Trong video demo, nói rõ ae dùng giải pháp nào và tại sao.

---

### 3.5 Folder Structure — Output Project

```bash
rag-project-weaction/                        # Repo name
│
├── src/                                      ## APPLICATION CODE
│   ├── __init__.py
│   ├── main.py                              ## FastAPI app + lifespan
│   │
│   ├── ingestion/                           ## PHASE 1: OFFLINE
│   │   ├── __init__.py
│   │   ├── document_loader.py              ## Load PDF/DOCX → text
│   │   ├── splitter.py                     ## Chunking logic
│   │   ├── embedder.py                     ## Jina v3 / BGE-M3 wrapper
│   │   └── indexer.py                      ## Embed + store Qdrant
│   │
│   ├── retrieval/                           ## PHASE 2: ONLINE
│   │   ├── __init__.py
│   │   ├── retriever.py                    ## Vector search (+ BM25)
│   │   ├── reranker.py                     ## Cross-encoder (optional)
│   │   └── query_processor.py              ## Query rewrite (optional)
│   │
│   ├── generation/                          ## PHASE 2: GENERATION
│   │   ├── __init__.py
│   │   ├── llm_client.py                   ## Async client → vLLM
│   │   └── response_builder.py             ## Prompt template + format
│   │
│   ├── evaluation/                          ## PHASE 3: EVAL
│   │   ├── __init__.py
│   │   └── ragas_evaluator.py              ## RAGAS metrics runner
│   │
│   ├── api/                                 ## API ENDPOINTS
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── query.py                    ## POST /query
│   │   │   ├── ingest.py                   ## POST /ingest
│   │   │   └── health.py                   ## GET /health
│   │   └── schemas/
│   │       └── models.py                   ## Pydantic request/response
│   │
│   └── core/                                ## SHARED
│       ├── __init__.py
│       ├── config.py                        ## Pydantic BaseSettings
│       └── logger.py                        ## Structured JSON logging
│
├── config/                                  ## CONFIGURATION
│   ├── settings.yaml                        ## chunk_size, model name, top_k
│   └── prompts.yaml                         ## Prompt templates (YAML)
│
├── docker/                                  ## INFRASTRUCTURE
│   ├── Dockerfile                           ## FastAPI multi-stage build
│   ├── docker-compose.yml                   ## qdrant + embedding + vllm + rag-api
│   └── .dockerignore
│
├── eval/                                    ## EVALUATION
│   ├── dataset.json                         ## 20+ cặp (question, ground_truth)
│   └── results/                             ## RAGAS results history
│
├── data/                                    ## DOCUMENTS (gitignored)
│   └── raw/                                 ## PDF/DOCX files để RAG
│
├── scripts/
│   ├── ingest.py                            ## CLI: python scripts/ingest.py
│   └── evaluate.py                          ## CLI: python scripts/evaluate.py
│
├── docs/
│   └── screenshots/                         ## Screenshots proof
│       ├── 1-ingest-success.png             ## Ingest documents thành công
│       ├── 2-query-response.png             ## POST /query → answer + sources
│       ├── 3-health-check.png               ## GET /health — all services OK
│       ├── 4-qdrant-dashboard.png           ## Qdrant collection có data
│       ├── 5-ragas-scores.png               ## RAGAS evaluation output
│       └── 6-docker-compose-up.png          ## All containers healthy
│
├── requirements.txt
├── .env.example                             ## QDRANT_URL, EMBEDDING_URL, VLLM_URL, ...
├── README.md                                ## Setup guide + RAGAS results
└── .gitignore
```

---

## 4. Output Submission - Comment dưới bài đăng

### Output 1: Push Code GitHub Public đầy đủ với README.md + Đặt tên dự án: ... - weaction

* `docker-compose up` → tất cả services start thành công
* `POST /ingest` → ingest documents vào Qdrant
* `POST /query` → hỏi câu hỏi → trả answer + sources
* `GET /health` → all services healthy
* `eval/` → chứa eval dataset + RAGAS results

**README.md phải có:**

* Architecture diagram (có thể dùng ASCII art)
* Tech stack đã chọn + lý do chọn
* Setup instructions (3 bước: clone → docker-compose up → ingest → query)
* RAGAS evaluation results (Faithfulness, Answer Relevancy — minimum)

### Output 2: Video Demo ~5 Phút (YouTube Video Publish)

##### Gợi ý:

Quay **Video trình bày** chi tiết, mục đích để chia sẻ với các bạnể người nghe bất kì có thể hiểu về dự án của bạn. => Giúp tập trình bày khi các bạn đi phỏng vấn, đi làm, báo cáo

1. **Giới thiệu dự án:**
   * RAG là gì? Mục đích của hệ thống này?
   * Tech stack đã chọn: embedding model nào, vector DB nào, LLM nào — **tại sao chọn** (refer đến bảng so sánh)
   * Data: tài liệu gì, bao nhiêu trang, bao nhiêu chunks
2. **Demo:**
   * Về mặt Product: Hỏi 2-3 câu → show answer + sources
   * Technical:
     * `docker-compose up` → show all containers healthy
     * Demo ingest pipeline: upload docs → chunking → embedding → store
     * Demo query pipeline: POST /query → show response với sources
     * Show RAGAS scores: Faithfulness, Answer Relevancy
     * Trình bày data flow xuyên suốt 3 pha

### Output 3: Review Vòng Tròn

Quy trình:  **Người 1 review Người 2, Người 2 review Người 3, … người cuối review Người 1** .

Nội dung comment cần kiểm tra:

1. Github đã đủ các yêu cầu (folder structure, docker-compose, eval results)
2. Video Youtube demo đủ 3 pha
3. RAGAS scores: Faithfulness > 0.7? Answer Relevancy > 0.7?

### Output 4: Điền link báo cáo + Feedback

1. Điền báo cáo vào sheet: https://docs.google.com/spreadsheets/d/18RGv8EJW-A-2yWYV2y0-9oiWEXVt-r2GW1qTXJ_GF6k/edit?gid=22262218#gid=22262218
   Link Github và Video của đồng đội vào sheet.
2. Điền feedback:
   Ace điền giúp Cường form feedback này để Cường hỗ trợ ace tốt nhất nhé. Thanks: [https://forms.gle/pHYsYKELCFptRKN9A](https://forms.gle/pHYsYKELCFptRKN9A)

---

> **Lời chúc:** Hoàn thành bài tập Week 2 là ae đã build được 1 hệ thống RAG production — bài toán mà hầu hết công ty AI ở Việt Nam đang cần. Đây là kỹ năng lõi của AI Engineer, và ae đã có nó trong portfolio.
>
> **Tip:** Bài tập này connect trực tiếp với Week 1 — ae dùng lại vLLM đã host để làm LLM backend cho RAG. Tuần 3 sẽ dùng lại RAG pipeline này để fine-tune và optimize. Mỗi tuần build trên tuần trước.

---
