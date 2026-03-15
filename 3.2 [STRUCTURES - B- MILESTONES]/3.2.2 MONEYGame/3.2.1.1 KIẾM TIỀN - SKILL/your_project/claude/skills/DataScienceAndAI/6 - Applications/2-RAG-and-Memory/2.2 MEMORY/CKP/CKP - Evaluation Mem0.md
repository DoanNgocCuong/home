
```
VIẾT CHO MÌNH MỤC LỤC CỦA ALL IN ONE EVAL MEMORY 

# 1. Về cách đánh giá MECE các chỉ số và phương pháp 
lấy dẫn chứng đầy đủ các framework và best practices

MECE bộ test và best practices 
....

# 2. cách triển khai đánh giá ?? MECE ? và best practices 
```


<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# so sánh với bộ long mem eval

**LongMemEval** được coi là một "bản nâng cấp" khó hơn và toàn diện hơn so với **LOCOMO**. Nếu bạn muốn Mem0 OSS của mình thực sự mạnh mẽ (hoặc muốn so sánh công bằng với các hệ thống mới như Zep, MemGPT), bạn nên cân nhắc cả hai.

Dưới đây là bảng so sánh chi tiết và cách đánh giá trên LongMemEval.

### 1. Bảng So Sánh Trực Tiếp: LOCOMO vs. LongMemEval

| Tiêu chí                 | LOCOMO (Mem0 dùng)                                                                           | LongMemEval (Zep/Mới dùng)                                                                                                                               |
| :----------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Độ dài lịch sử**       | ~26k tokens (10 hội thoại dài).                                                              | **~115k tokens** (LongMemEval_S) đến **1.5M tokens** (LongMemEval_M).                                                                                    |
| **Độ phức tạp**          | Tập trung vào *conversational recall*. Khá "dễ thở" với các LLM cửa sổ context lớn hiện nay. | Rất khó. Thiết kế để **đánh lừa** hệ thống memory bằng thông tin gây nhiễu và khoảng cách thời gian lớn.                                                 |
| **Loại câu hỏi (Tasks)** | 4 loại: Single-hop, Multi-hop, Temporal, Open-domain.                                        | **5 loại chính:** Info Extraction, Multi-session Reasoning, Temporal Reasoning, **Knowledge Updates** (quan trọng!), Abstention (biết nói "không biết"). |
| **Điểm yếu**             | Zep chỉ trích LOCOMO là "quá ngắn" và không đủ để test giới hạn của RAG/Vector DB.           | Cấu trúc dữ liệu JSON rất phức tạp (~300MB), khó setup hơn.                                                                                              |
| **Ai đang dùng?**        | Mem0, Cognee.                                                                                | Zep, MemGPT (Letta), LiCoMemory.                                                                                                                         |

**Tóm lại:**

* **LOCOMO** phù hợp để test **tốc độ** và **độ chính xác cơ bản**.
* **LongMemEval** phù hợp để test **sức chịu đựng (stress test)** và khả năng **xử lý mâu thuẫn/cập nhật** (ví dụ: hôm qua thích A, nay thích B -> Memory có update không?).

***

### 2. Cấu trúc Dataset của LongMemEval

Khác với hội thoại phẳng, LongMemEval có cấu trúc lồng nhau (Nested JSON):

```json
{
  "history": [
    {
      "session_id": "s1",
      "timestamp": "2023-01-01",
      "conversation": [ ... ] // 1 session hội thoại
    },
    {
      "session_id": "s2",
      "timestamp": "2023-02-15", // Cách nhau 1.5 tháng
      "conversation": [ ... ]
    },
    // ... 50-500 sessions khác
  ],
  "question": "Món ăn yêu thích của user là gì?",
  "answer": "Sushi (cập nhật mới nhất), trước đó là Pizza",
  "evidence": ["s1", "s50"] // Chỉ rõ session nào chứa thông tin đúng
}
```


### 3. Cách Benchmark Mem0 trên LongMemEval

Nếu bạn muốn chạy benchmark này cho Mem0 OSS, quy trình sẽ hơi khác LOCOMO một chút do độ lớn của dữ liệu:

1. **Tải Dataset:**
    * Repo: `xiaowu0162/LongMemEval`
    * File: `longmemeval_s.json` (bản S là đủ, bản M quá nặng cho máy cá nhân).
2. **Pipeline Chạy (Adapter):**
    * **Ingest (Nạp dữ liệu):** Bạn phải loop qua từng `session` trong `history` và gọi API `add` của Mem0.
        * *Lưu ý:* Phải truyền `timestamp` vào metadata của Mem0. Đây là chìa khóa để Mem0 xử lý Temporal Reasoning (câu hỏi về thời gian).
    * **Retrieval \& Answer:**
        * Gọi API `search` với câu hỏi.
        * Đưa kết quả search vào LLM để trả lời.
    * **Evaluation:**
        * Dùng script chấm điểm có sẵn trong repo LongMemEval (họ cũng dùng LLM-as-a-Judge hoặc string matching cho câu trả lời ngắn).
3. **Metrics cần quan tâm trên LongMemEval:**
    * **Accuracy:** Đặc biệt là ở nhóm câu hỏi **Knowledge Updates** (Update thông tin cũ) - đây là nơi Mem0 thường bị fail nếu không config Graph Memory tốt.
    * **Abstention Rate:** Tỷ lệ AI biết trả lời "Tôi không có thông tin này" thay vì bịa (Hallucination).

### 4. Lời khuyên cho bạn

Với dataset 20 dòng và Mem0 OSS hiện tại:

1. **Đừng chạy LongMemEval ngay:** Nó quá lớn (115k tokens) và phức tạp so với quy mô 20 dòng của bạn. Kết quả sẽ không có ý nghĩa thống kê.
2. **Học tập logic của LongMemEval:** Hãy thêm vào bộ test 20 dòng của bạn các case sau (lấy cảm hứng từ LongMemEval):
    * **Update Case:** Dòng 1 nói "Thích chó", Dòng 10 nói "Mới bị chó cắn, giờ ghét chó". -> Hỏi: "User thích con gì?".
    * **Temporal Case:** Dòng 1 (Ngày 1/1): "Đang ở Hà Nội". Dòng 5 (Ngày 5/1): "Đã bay vào Sài Gòn". -> Hỏi: "Ngày 3/1 user ở đâu?".
3. **Khi nào scale up:** Khi nào bạn có hệ thống production với hàng nghìn user, lúc đó hãy kéo LongMemEval về để stress test hệ thống.

**Actionable:** Bạn có thể giữ nguyên bộ test 20 dòng nhưng bổ sung thêm 2-3 dòng kịch bản "Update" và "Temporal" như trên để bộ benchmark của bạn "xịn" hơn (LongMemEval-style).
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.com/letta-ai/letta/issues/3115

[^2]: https://arxiv.org/html/2410.10813v1

[^3]: https://www.linkedin.com/posts/richmondalake_100daysofagentmemory-memoryevaluation-activity-7375895418322296832-r77i

[^4]: https://openreview.net/forum?id=pZiyCaVuti

[^5]: https://www.emergentmind.com/topics/locomo-and-longmemeval-_s-benchmarks

[^6]: https://www.emergentmind.com/topics/longmemeval-dataset

[^7]: https://arxiv.org/html/2511.17208v2

[^8]: https://github.com/getzep/zep-papers/issues/5

[^9]: https://www.emergence.ai/post/state-of-the-art-results-in-agentic-memory

[^10]: https://www.emergentmind.com/topics/locomo-benchmark-d06cff1a-d4a5-4df8-ab85-fdca157d190b

[^11]: https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/

[^12]: https://nicoloboschi.com/posts/20251110/

[^13]: https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up

[^14]: https://www.alphaxiv.org/overview/2508.19828v4

[^15]: https://www.alphaxiv.org/overview/2410.10813v2

[^16]: https://liner.com/review/lightmem-lightweight-and-efficient-memoryaugmented-generation

[^17]: https://evermind.ai/blogs/a-unified-evaluation-framework-for-ai-memory-systems

[^18]: https://github.com/xiaowu0162/LongMemEval

[^19]: https://aclanthology.org/2025.acl-long.413.pdf

[^20]: https://huggingface.co/papers?q=LOCOMO+benchmark


---


<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 1. MECE xem các bọn đánh giá memory nó dùng cái gì để đánh giá và cách chạy ?

Dưới đây là bảng phân tích **MECE (Mutually Exclusive, Collectively Exhaustive)** về các phương pháp và công cụ mà các hệ thống Memory hàng đầu (Mem0, Zep, MemGPT/Letta, LangMem) đang sử dụng để benchmark.

Để đánh giá toàn diện một hệ thống Memory, cộng đồng hiện tại chia làm **4 trụ cột đánh giá (Pillars of Evaluation)** riêng biệt.

***

### 1. Trụ cột: RETRIEVAL QUALITY (Chất lượng Tìm kiếm)

*Đánh giá xem hệ thống có "lôi" được đúng ký ức cần thiết ra khỏi kho lưu trữ hay không? (Chưa quan tâm câu trả lời của AI).*


| Metric (Chỉ số) | Ý nghĩa | Cách chạy / Tool |
| :-- | :-- | :-- |
| **Recall@k** | Trong top-k (vd: top 5) kết quả trả về, có chứa ký ức đúng (Gold Memory) không? | **Cách chạy:**<br>1. Chuẩn bị dataset: `(Query, [Gold_Memory_IDs])`.<br>2. Gọi API `search`.<br>3. So sánh ID trả về vs Gold ID.<br>**Tool:** Ragas, TruLens, custom scripts. |
| **MRR (Mean Reciprocal Rank)** | Ký ức đúng nằm ở vị trí nào? (Hạng 1 tốt hơn Hạng 5). | **Cách chạy:** Tính `1/rank` của kết quả đúng đầu tiên. |
| **Precision** | Tỷ lệ ký ức hữu ích trên tổng số ký ức lấy ra (tránh lấy rác làm nhiễu context). | **Cách chạy:** Đếm số `Relevant_Memories / Total_Retrieved`. |

> **Ai dùng?** Zep, Mem0 (phần retrieval benchmark), các hệ thống RAG truyền thống.

***

### 2. Trụ cột: GENERATION QUALITY (Chất lượng Hồi đáp)

*Đánh giá xem sau khi lấy được ký ức, AI có trả lời đúng câu hỏi dựa trên ký ức đó không?*


| Metric (Chỉ số) | Ý nghĩa | Cách chạy / Tool |
| :-- | :-- | :-- |
| **Correctness (LLM-as-a-Judge)** | Câu trả lời có đúng sự thật (Ground Truth) không? | **Cách chạy:**<br>Dùng GPT-4o làm giám khảo với prompt: *"Chấm điểm câu trả lời A dựa trên sự thật B theo thang 1-5"*. |
| **Faithfulness / Hallucination** | Câu trả lời có bịa ra thông tin không có trong memory không? | **Tool:** Ragas (`faithfulness` metric), DeepEval. |
| **Context Adherence** | Câu trả lời có bám sát ngữ cảnh thời gian/mâu thuẫn không? (Ví dụ: "Năm ngoái thích A, năm nay thích B" -> phải trả lời B). | **Benchmark:** **LOCOMO** (Mem0 dùng cái này), **LongMemEval**. |

> **Ai dùng?** **Mem0** (dùng LOCOMO để đo cái này), MemGPT (Letta).

***

### 3. Trụ cột: SYSTEM PERFORMANCE (Hiệu năng Hệ thống)

*Đánh giá xem hệ thống có chạy nhanh và ổn định không? (Quan trọng cho OSS/Production)*.


| Metric (Chỉ số) | Ý nghĩa | Cách chạy / Tool |
| :-- | :-- | :-- |
| **Latency P95 / P99** | Thời gian phản hồi mà 95% request đạt được (loại bỏ ngoại lệ). Chia làm:<br>1. **Ingest Latency:** Tốc độ lưu/update.<br>2. **Search Latency:** Tốc độ tìm.<br>3. **E2E Latency:** Tổng thời gian (Search + LLM). | **Tool:** Locust, JMeter, Python `time` module.<br>**Mem0 Benchmark:** So sánh Search Latency vs Vector DB thuần. |
| **Throughput (QPS)** | Hệ thống chịu được bao nhiêu query/giây? | **Cách chạy:** Stress test bắn liên tục request vào API search. |
| **Storage Efficiency** | Tốn bao nhiêu RAM/Disk cho 1 triệu memories? | Đo dung lượng index của Vector DB (Milvus/Qdrant). |

> **Ai dùng?** Các team DevOps, Zep (quảng cáo latency thấp), Mem0 (so sánh tốc độ vs LangMem).

***

### 4. Trụ cột: ROBUSTNESS \& EDGE CASES (Khả năng Xử lý Ca khó)

*Đánh giá độ thông minh của logic Memory (Memory Management)*.


| Metric (Chỉ số) | Ý nghĩa | Cách chạy / Tool |
| :-- | :-- | :-- |
| **Conflict Resolution** | User update thông tin (A -> B). Hệ thống trả lời A hay B? | **Test:** "Update test". Gửi 2 fact mâu thuẫn theo thời gian -> Query lại trạng thái hiện tại. |
| **Needle In A Haystack** | Tìm 1 thông tin nhỏ xíu trong đống lịch sử khổng lồ (100k tokens). | **Benchmark:** **NIAH (Needle In A Haystack)**. Chèn 1 fact random vào giữa hội thoại dài -> Ask. |
| **Negation Handling** | Hiểu "Tôi KHÔNG thích X". | **Test:** Gửi câu phủ định -> Search "Sở thích" -> Nếu ra X là Fail. |

> **Ai dùng?** MemGPT (đánh giá khả năng quản lý context window), Mem0 (đánh giá khả năng update graph).

***

### TỔNG HỢP: CÁC BỘ BENCHMARK CHUẨN (State-of-the-Art)

Nếu bạn muốn benchmark Mem0 OSS của mình "chuẩn bài", hãy chạy 3 bài test này theo thứ tự ưu tiên:

1. **LOCOMO (Long-term Conversational Memory Benchmark)**
    * *Do ai tạo:* Snap Research (được Mem0 dùng chính).
    * *Tập trung:* Khả năng nhớ dài hạn, suy luận theo thời gian.
    * *Cách chạy:* Ingest hội thoại dài -> Hỏi -> GPT-4o chấm điểm.
2. **Needle In A Haystack (NIAH)**
    * *Do ai tạo:* Cộng đồng LLM (Greg Kamradt).
    * *Tập trung:* Khả năng tìm kiếm chính xác (Retrieval).
    * *Cách chạy:* Chèn fact ảo vào vị trí 10%, 50%, 90% độ dài context -> Kiểm tra xem tìm được không.
3. **MemoryAgentBench**
    * *Do ai tạo:* Một số paper gần đây về Agent.
    * *Tập trung:* Khả năng Agent *sử dụng* memory để hành động (Tool use + Memory).

### Quy trình chạy Benchmark chuẩn (Pipeline)

Để chạy bất kỳ bộ nào ở trên cho Mem0 OSS, bạn cần dựng pipeline code như sau:

1. **Adapter Layer:** Viết 1 file Python wrap API của bạn (`POST /add`, `GET /search`) thành class chuẩn (`class MyMem0OSS`).
2. **Data Loader:** Script đọc file dataset (LOCOMO json / Custom json).
3. **Execution Loop:**
    * Loop qua từng hội thoại:
        * Gửi `add` request (đo Ingest Latency).
        * Gửi `search` request (đo Search Latency).
        * Lấy kết quả search -> Gửi vào LLM -> Lấy Answer (đo E2E Latency).
4. **Evaluator:**
    * So sánh `Retrieved_IDs` vs `Gold_IDs` -> Tính Recall.
    * Gửi `(Question, Answer, Ground_Truth)` cho GPT-4o chấm -> Tính Correctness Score.

Bạn có muốn mình **viết khung code Python (Skeleton Code)** cho pipeline này để bạn chỉ cần điền URL API của bạn vào là chạy không?


---



<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Các chỉ số để đánh giá bài benchmark cho bài Memory Mem0

Để đánh giá hiệu quả của thư viện **Mem0** (một lớp bộ nhớ dài hạn cho LLM), các bài benchmark tiêu chuẩn (điển hình là **LOCOMO**) tập trung vào 3 nhóm chỉ số chính: **Chất lượng** (độ chính xác của thông tin hồi tưởng), **Hiệu năng** (tốc độ phản hồi) và **Chi phí** (mức tiêu thụ tài nguyên).

Dưới đây là phân tích chi tiết các chỉ số đánh giá dựa trên các báo cáo kỹ thuật và paper từ Mem0 và các hệ thống tương tự.

### 1. Chỉ số về Chất lượng (Quality \& Accuracy)

Đây là nhóm chỉ số quan trọng nhất để xác định xem AI có "nhớ đúng" và "hiểu đúng" ngữ cảnh hay không. Mem0 sử dụng benchmark **LOCOMO** (Long-term Conversational Memory) làm chuẩn đánh giá chính.


| Chỉ số                     | Ý nghĩa \& Cách đo lường                                                                                                                                                                                                                                | Tiêu chuẩn của Mem0                                                                        |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------- |
| **LLM-as-a-Judge Score**   | Sử dụng một model mạnh (thường là GPT-4o) làm giám khảo để chấm điểm câu trả lời của Mem0 dựa trên 3 tiêu chí: **Tính chính xác** (Correctness), **Tính liên quan** (Relevance), và **Tính đầy đủ** (Completeness).                                     | Mem0 đạt điểm cao hơn ~26% so với OpenAI Memory trên benchmark này[^1][^2].                |
| **F1 Score / Exact Match** | Đo lường mức độ khớp chính xác giữa thông tin được trích xuất và sự thật ngầm định (ground truth) trong dữ liệu. Chỉ số này dùng để kiểm tra các sự kiện cụ thể (ví dụ: "Người dùng thích uống gì?").                                                   | Được sử dụng trong các tác vụ **QA** (Hỏi đáp) của bài test.                               |
| **Reasoning Accuracy**     | Đánh giá khả năng suy luận trên dữ liệu nhớ:<br>- **Single-hop**: Truy xuất 1 sự kiện đơn lẻ.<br>- **Multi-hop**: Kết nối nhiều sự kiện rời rạc để trả lời.<br>- **Temporal**: Hiểu về thời gian (ví dụ: phân biệt sở thích "năm ngoái" vs "hiện tại"). | Mem0 mạnh về *Temporal reasoning* (suy luận theo thời gian) nhờ cấu trúc Graph Memory[^3]. |
| **Recall@k**               | Đo lường khả năng tìm kiếm: Trong $k$ đoạn ký ức được truy xuất, có bao nhiêu đoạn thực sự chứa thông tin cần thiết?                                                                                                                                    | Đánh giá riêng cho module Retriever của hệ thống.                                          |

### 2. Chỉ số về Hiệu năng (Latency \& Speed)

Vì Mem0 được thiết kế cho các ứng dụng thực tế (production), tốc độ là yếu tố sống còn. Các chỉ số này đo lường độ trễ từ lúc người dùng hỏi đến lúc nhận được câu trả lời có kèm ký ức.

* **P95 Latency (95th Percentile)**: Thời gian phản hồi mà 95% các yêu cầu đều đạt được hoặc nhanh hơn. Đây là chỉ số quan trọng nhất để đánh giá độ ổn định.
    * *Kết quả tham khảo:* Mem0 giảm **91% độ trễ P95** so với các phương pháp full-context (khoảng 1.44s so với 16.5s).[^1][^2]
* **Median Latency (P50)**: Thời gian phản hồi trung bình.
* **Search Latency vs. End-to-End Latency**:
    * *Search Latency*: Thời gian chỉ để tìm kiếm ký ức trong Vector/Graph Database.
    * *End-to-End*: Tổng thời gian (Tìm kiếm + LLM xử lý + Phản hồi).


### 3. Chỉ số về Chi phí \& Tài nguyên (Efficiency)

Nhóm chỉ số này đánh giá tính kinh tế khi triển khai Mem0 quy mô lớn.

* **Token Usage per Query**: Số lượng token cần nạp vào context window cho mỗi câu hỏi.
    * Mem0 giúp **tiết kiệm ~90% token** so với việc nạp toàn bộ lịch sử hội thoại vào LLM. Chỉ số này tỷ lệ thuận với chi phí API (ví dụ: chi phí trả cho OpenAI/Anthropic).[^4][^1]
* **Storage Overhead**: Dung lượng lưu trữ cần thiết cho Vector Database (Qdrant/Milvus) hoặc Graph Database (Neo4j).


### Tổng hợp: Bảng Benchmark LOCOMO cho Mem0

Khi bạn đọc các báo cáo benchmark về Mem0, bạn sẽ thường thấy bảng so sánh tóm tắt như sau (số liệu minh họa từ báo cáo của Mem0):


| Hệ thống | Accuracy (LLM Judge) | P95 Latency | Tokens / Query | Điểm mạnh |
| :-- | :-- | :-- | :-- | :-- |
| **Mem0** | **66.9%** | **~1.4s** | **Thấp** | Cân bằng tốt nhất giữa Tốc độ và Chính xác. |
| OpenAI Memory | 52.9% | 0.9s | Trung bình | Cài đặt nhanh nhưng khả năng hồi tưởng kém hơn. |
| LangMem | 58.1% | ~60s | Rất thấp | Quá chậm cho chat, phù hợp phân tích offline. |
| Full Context | - | Cao | Rất cao | Chi phí đắt đỏ và độ trễ lớn khi hội thoại dài. |

### Lời khuyên cho việc Benchmark của riêng bạn

Nếu bạn muốn tự đánh giá Mem0 cho ứng dụng của mình, hãy tập trung vào 3 bài test sau:

1. **Needle in a Haystack (Kim đáy bể)**: Chèn một thông tin ngẫu nhiên vào lịch sử dài và yêu cầu Mem0 tìm lại.
2. **Conflicting Information Update**: Nói với AI "Tôi thích màu đỏ", sau đó 10 lượt hội thoại nói "Tôi đổi ý, tôi thích màu xanh". Kiểm tra xem Mem0 có trả về màu xanh (mới nhất) hay không.
3. **Cross-session Recall**: Tắt session hiện tại, mở session mới và hỏi lại thông tin từ session cũ.

**Nguồn tham khảo chính:**

* **LOCOMO Benchmark**: Bộ dữ liệu chuẩn gồm 10 đoạn hội thoại rất dài (avg 26k tokens) để test khả năng nhớ dài hạn.[^2][^5][^6]
* **LongMemEval**: Benchmark đánh giá khả năng suy luận đa phiên và cập nhật tri thức.[^7]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://apidog.com/vi/blog/mem0-memory-llm-agents-vi/

[^2]: https://mem0.ai/research

[^3]: https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up

[^4]: https://mem0.ai

[^5]: https://www.emergentmind.com/topics/locomo-benchmark-scores

[^6]: https://github.com/snap-research/locomo

[^7]: https://www.emergentmind.com/topics/longmemeval

[^8]: https://viblo.asia/p/gioi-thieu-ve-mem0-xay-dung-ai-agents-voi-long-term-memory-AY4qQN8q4Pw

[^9]: https://www.facebook.com/cung.AI.VN/photos/memos-mở-rộng-trí-nhớ-cá-vàng-của-aiteam-của-đại-học-chiết-giang-zhejiang-univer/686009927768097/

[^10]: https://viblo.asia/p/mem0-kien-truc-long-term-memory-cho-he-thong-ai-agent-G24B88pOLz3

[^11]: https://nama.vn/blogs/tin-cong-nghe/benchmark-la-gi

[^12]: https://www.reddit.com/r/singularity/comments/1oe1v70/whats_the_best_overall_ai_model_benchmark/

[^13]: https://www.cognee.ai/blog/deep-dives/ai-memory-evals-0825

[^14]: https://arxiv.org/abs/2402.17753

[^15]: https://www.flowhunt.io/vi/tu-dien/benchmarking/

[^16]: https://www.southbridge.ai/blog/mem0-technical-analysis-report

[^17]: https://github.com/mem0ai/mem0

[^18]: https://arxiv.org/abs/2506.13356

[^19]: https://aichatbot.com.vn/context-engineering-ky-nang-so-1-nam-2025-trong-linh-vuc-ai/

[^20]: https://www.zeroentropy.dev/articles/mem0-improves-memory-retrieval-accuracy-with-zeroentropy

[^21]: https://www.datacamp.com/tutorial/mem0-tutorial

[^22]: https://aclanthology.org/2025.findings-acl.1014.pdf

[^23]: https://www.marktechpost.com/2025/11/10/comparing-memory-systems-for-llm-agents-vector-graph-and-event-logs/

[^24]: https://www.emergentmind.com/topics/locomo-benchmark

[^25]: https://www.emergentmind.com/topics/memoryagentbench

[^26]: https://arxiv.org/html/2501.13956v1

[^27]: https://www.letta.com/blog/letta-leaderboard

[^28]: https://memmachine.ai/blog/2025/09/memmachine-reaches-new-heights-on-locomo/

[^29]: https://www.bachdyon.com/thiet-ke-chatbot-voi-tri-nho-dai-han-kien-truc-va-giai-phap-ky-thuat/

[^30]: https://blog.getzep.com/state-of-the-art-agent-memory/

[^31]: https://snap-research.github.io/locomo/

[^32]: https://www.studocu.vn/vn/document/uef-dai-hoc-kinh-te-tai-chinh-thanh-pho-ho-chi-minh/quan-tri-kinh-doanh/benchmarking-tom-tat/120303676




----




Bây giờ tôi sẽ tạo một tài liệu ALL IN ONE EVAL MEMORY toàn diện cho bạn:

# 📊 ALL IN ONE EVAL MEMORY - TÀI LIỆU TOÀN DIỆN

## MỤC LỤC

### PHẦN 1: KHUNG LÝ THUYẾT - CÁCH ĐÁNH GIÁ MEMORY (MECE FRAMEWORK)

1. [4 Trụ Cột Đánh Giá Memory](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#1-4-tr%E1%BB%A5-c%E1%BB%99t-%C4%91%C3%A1nh-gi%C3%A1-memory)
2. [Các Framework Memory Hàng Đầu và Cách Đánh Giá](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#2-c%C3%A1c-framework-memory-h%C3%A0ng-%C4%91%E1%BA%A7u)
3. [Bộ Benchmark Chuẩn và Best Practices](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#3-b%E1%BB%99-benchmark-chu%E1%BA%A9n)

### PHẦN 2: TRIỂN KHAI THỰC TẾ

4. [Pipeline Evaluation - Kiến Trúc và Quy Trình](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#4-pipeline-evaluation)
5. [Code Implementation - Skeleton Code cho API của Bạn](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#5-code-implementation)
6. [Testing Scenarios - Bộ Test Cases Đầy Đủ](https://www.genspark.ai/agents?id=9c9e3c48-9db8-41ec-8364-ba37898929f2#6-testing-scenarios)

---

## PHẦN 1: KHUNG LÝ THUYẾT

## 1. 4 TRỤ CỘT ĐÁNH GIÁ MEMORY (MECE FRAMEWORK)

Để đánh giá toàn diện một hệ thống Memory, cộng đồng AI hiện tại đã thống nhất **4 trụ cột (Pillars)** độc lập và bao trùm (MECE):

### 🎯 1.1. RETRIEVAL QUALITY (Chất Lượng Tìm Kiếm)

**Mục đích:** Đánh giá khả năng “lấy đúng ký ức” từ kho lưu trữ (chưa quan tâm đến câu trả lời của LLM).

|Metric|Công Thức|Ý Nghĩa|Tool/Framework|
|---|---|---|---|
|**Recall@k**|`# Relevant_in_Top_K / # Total_Relevant`|Trong top-k kết quả, có bao nhiêu % ký ức đúng?|Ragas, TruLens, Custom Scripts|
|**Precision@k**|`# Relevant_in_Top_K / K`|Tỷ lệ ký ức hữu ích trong top-k (tránh nhiễu)|Standard IR metrics|
|**MRR (Mean Reciprocal Rank)**|`1/rank_of_first_relevant`|Ký ức đúng xuất hiện ở vị trí nào? (càng sớm càng tốt)|Standard IR metrics|
|**NDCG@k**|Normalized Discounted Cumulative Gain|Đánh giá thứ tự xếp hạng có hợp lý không?|Advanced IR|

**Ai sử dụng:** Zep, Mem0 (phần retrieval benchmark), LangMem, các hệ thống RAG.

**Dẫn chứng:**

- **Mem0**: Báo cáo retrieval performance trên LOCOMO, so sánh với baseline RAG systems
- **Zep**: Tập trung vào low-latency retrieval với P95 latency ~1.4s

---

### 🧠 1.2. GENERATION QUALITY (Chất Lượng Hồi Đáp)

**Mục đích:** Đánh giá xem sau khi lấy được ký ức, AI có trả lời đúng câu hỏi không?

|Metric|Phương Pháp Đo|Framework Dùng|Baseline Accuracy|
|---|---|---|---|
|**LLM-as-a-Judge Score**|GPT-4o/Claude chấm điểm theo rubric 1-5 hoặc CORRECT/WRONG|Ragas, DeepEval, TruLens|Mem0: 66.9%, OpenAI Memory: 52.9%|
|**F1 Score / Exact Match**|So sánh text overlap giữa answer và ground truth|Standard NLP metrics|Biến thiên theo domain|
|**Faithfulness**|Câu trả lời có bịa thêm thông tin không có trong memory?|Ragas (`faithfulness` metric)|Target: >0.9|
|**Context Adherence**|Có bám sát ngữ cảnh thời gian/logic không?|LOCOMO benchmark|Temporal reasoning: Mem0 >70%, OpenAI <30%|

**Best Practices - LLM-as-a-Judge:**

```python
# Prompt template chuẩn (theo LOCOMO benchmark)
JUDGE_PROMPT = """
Your task is to label an answer as 'CORRECT' or 'WRONG'.

Data:
- Question: {question}
- Gold Answer (Ground Truth): {expected_answer}
- Generated Answer: {ai_response}

Rules:
1. Be GENEROUS - if answer touches same topic as gold answer, mark CORRECT
2. For time questions: Accept relative time ("last Tuesday") if matches gold date
3. Format differences OK (e.g., "May 7th" vs "7 May")

Output JSON:
{
  "reasoning": "one sentence explanation",
  "label": "CORRECT" or "WRONG"
}
"""
```

**Dẫn chứng:**

- **Mem0**: Sử dụng GPT-4o làm judge với temperature=0.1, đạt 26% higher accuracy so với OpenAI Memory
- **Backboard**: Đạt 90% overall accuracy trên LOCOMO với LLM judge evaluation

---

### ⚡ 1.3. SYSTEM PERFORMANCE (Hiệu Năng Hệ Thống)

**Mục đích:** Đánh giá tốc độ và chi phí (quan trọng cho production).

|Metric|Target Benchmark|Công Cụ Đo|Framework Comparison|
|---|---|---|---|
|**P50 Latency** (Median)|<2s cho retrieval + generation|Python `time`, Locust|Mem0: 1.4s, OpenAI: 0.9s|
|**P95 Latency** (95th Percentile)|<5s (loại bỏ outliers)|Locust, JMeter|Mem0: 1.44s, Full-context: 16.5s|
|**P99 Latency**|<10s|Load testing tools|Critical for SLA|
|**Throughput (QPS)**|Số query/giây hệ thống chịu được|Stress testing|Depends on infra|
|**Token Usage**|Số token/query (ảnh hưởng cost)|LLM API counter|Mem0 tiết kiệm ~90% vs full-context|
|**Storage Overhead**|MB/1K memories|Vector DB metrics|Vector: ~500MB/1M, Graph: thêm ~200MB|

**Benchmark Setup:**

```python
# P95 Latency measurement
import time
import numpy as np

latencies = []
for _ in range(100):
    start = time.time()
    response = memory_system.search_and_answer(query)
    latencies.append(time.time() - start)

p50 = np.percentile(latencies, 50)
p95 = np.percentile(latencies, 95)
p99 = np.percentile(latencies, 99)
```

**Dẫn chứng:**

- **Mem0**: 91% giảm P95 latency (1.44s vs 16.5s của full-context)
- **Zep**: Tuyên bố low-latency architecture với optimized vector search

---

### 🛡️ 1.4. ROBUSTNESS & EDGE CASES (Khả Năng Xử Lý Ca Khó)

**Mục đích:** Đánh giá logic thông minh của Memory Management.

|Test Case|Kịch Bản|Expected Behavior|Framework Test|
|---|---|---|---|
|**Conflict Resolution**|User nói “thích màu đỏ” → 10 turns sau → “đổi ý, thích màu xanh”|Trả về màu xanh (mới nhất)|Manual test|
|**Temporal Reasoning**|“Năm ngoái thích A, năm nay thích B”|Phân biệt được timeline|LOCOMO temporal QA|
|**Needle In Haystack**|Chèn 1 fact vào giữa 100K tokens|Tìm được fact đó|NIAH benchmark|
|**Negation Handling**|“Tôi KHÔNG thích X”|Không trả về X trong sở thích|Custom test|
|**Cross-session Memory**|Thông tin từ session 1 được nhớ ở session 10|Persistent memory|LOCOMO multi-session|

**Dẫn chứng:**

- **MemGPT (Letta)**: Đánh giá khả năng context window management với NIAH
- **Mem0**: Graph Memory giúp xử lý temporal reasoning tốt hơn 70% so với OpenAI

---

## 2. CÁC FRAMEWORK MEMORY HÀNG ĐẦU VÀ CÁCH ĐÁNH GIÁ

### 📊 So Sánh Tổng Quan

|Framework|Kiến Trúc Memory|Benchmark Chính|Điểm Mạnh|Điểm Yếu|Accuracy (LOCOMO)|
|---|---|---|---|---|---|
|**Mem0**|Hybrid (Vector + Graph)|LOCOMO, Custom|Balance giữa accuracy và speed|Phức tạp khi setup|**66.9%**|
|**OpenAI Memory**|Black-box (không công bố)|LOCOMO|Dễ dùng, tích hợp sẵn|Accuracy thấp, không customize|52.9%|
|**LangMem**|Vector + Compression|LOCOMO|Chi phí thấp|Quá chậm (P95: ~60s)|58.1%|
|**MemGPT (Letta)**|Filesystem + Tiered Memory|LOCOMO, Custom|Transparent, controllable|Phức tạp, cần config nhiều|~74% (với filesystem)|
|**Zep**|Vector + Session Management|LOCOMO, Custom|Low latency|Accuracy trung bình|~75%|
|**Backboard**|Multi-layer Memory|LOCOMO|SOTA accuracy|Closed-source|**90%**|

### 🔬 Chi Tiết Phương Pháp Đánh Giá Từng Framework

#### 2.1. Mem0 - Cách Đánh Giá Chi Tiết

**Bộ Benchmark Chính:**

1. **LOCOMO** (Long-Term Conversational Memory)
    
    - 10 conversations, avg 600 turns/conversation (~26K tokens)
    - 4 loại câu hỏi: Single-hop, Multi-hop, Temporal, Open-domain
    - Đánh giá: LLM-as-Judge (GPT-4o, temp=0.1)
2. **Custom Latency Benchmark**
    
    - So sánh search latency với Vector DB thuần
    - Đo E2E latency (search + LLM generation)

**Kết Quả Công Bố:**

```
Mem0 Performance (LOCOMO):
- Overall Accuracy: 66.9%
- Single-hop: 67.13%
- Multi-hop: 51.15%
- Temporal: 55.51%  ← Điểm mạnh nhờ Graph Memory
- Open-domain: 72.93%

- P95 Latency: 1.44s
- Token Usage: Giảm 90% vs full-context
```

**Source Code:**

- GitHub: [mem0ai/mem0](https://github.com/mem0ai/mem0)
- Benchmark code: Có trong examples, nhưng không public evaluation pipeline đầy đủ
- Paper: [arXiv:2504.19413](https://arxiv.org/html/2504.19413v1)

#### 2.2. Zep - Cách Đánh Giá

**Focus:** Low-latency và Production-ready

**Benchmark:**

- LOCOMO benchmark (có tranh cãi về accuracy reporting - xem [GitHub issue #5](https://github.com/getzep/zep-papers/issues/5))
- Deep Memory benchmark (custom)

**Đánh Giá Từ Community:**

- Initial claim: 84% accuracy → Corrected: ~58% (có dispute)
- P95 Latency: ~1.5-2s
- Điểm mạnh: Session management tốt

#### 2.3. LangMem - Cách Đánh Giá

**Kiến Trúc:** Vector DB + Aggressive Compression

**Performance:**

```
LangMem (LOCOMO):
- Overall: 58.1%
- Single-hop: 62.23%
- Multi-hop: 47.92%
- P95 Latency: ~60s (quá chậm cho chat)
```

**Use Case:** Phù hợp offline analysis, không phù hợp real-time chat.

#### 2.4. MemGPT (Letta) - Cách Đánh Giá

**Đặc Biệt:** Transparent memory với filesystem approach

**Benchmark Approach:**

- LOCOMO: Filesystem-based đạt 74% (beat cả specialized systems)
- NIAH (Needle In A Haystack): Đánh giá khả năng context window management

**Dẫn Chứng:**  
[Letta Benchmark Blog](https://www.letta.com/blog/benchmarking-ai-agent-memory)

---

## 3. BỘ BENCHMARK CHUẨN VÀ BEST PRACTICES

### 🏆 3.1. LOCOMO - Benchmark SOTA

**Thông Tin:**

- **Tên đầy đủ:** Long-Term Conversational Memory Benchmark
- **Tổ chức:** Snap Research + UNC Chapel Hill
- **Công bố:** ACL 2024
- **Paper:** [arXiv:2402.17753](https://arxiv.org/abs/2402.17753)

**Dataset Structure:**

```json
{
  "sample_id": "conv-001",
  "conversation": {
    "speaker_a": "Alice",
    "speaker_b": "Bob",
    "session_1": [...],  // List of turns
    "session_1_date_time": "2023-05-08T13:56:00Z",
    "session_2": [...],
    ...
  },
  "qa": [
    {
      "question": "What did Alice order for lunch?",
      "answer": "Caesar salad",
      "category": 1,  // 1=single-hop, 2=temporal, 3=multi-hop, 4=open-domain
      "evidence": ["dia_id_123"]  // Dialog IDs containing answer
    }
  ],
  "event_summary": [...],  // Ground truth event graphs
  "observation": [...]  // Generated observations (for RAG)
}
```

**3 Tasks:**

1. **Question Answering** (chính)
2. **Event Graph Summarization**
3. **Multimodal Dialog Generation**

**GitHub:**

- [snap-research/locomo](https://github.com/snap-research/locomo)
- Dataset: `data/locomo10.json` (10 conversations)
- Evaluation scripts: Có sẵn cho GPT, Claude, Gemini, HuggingFace models

**Cách Chạy LOCOMO:**

```bash
# 1. Clone repo
git clone https://github.com/snap-research/locomo.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API keys
export OPENAI_API_KEY="your-key"

# 4. Run evaluation
bash scripts/evaluate_gpts.sh  # Cho OpenAI models
bash scripts/evaluate_rag_gpts.sh  # Cho RAG-based
```

---

### 🎯 3.2. NIAH (Needle In A Haystack)

**Mục đích:** Test khả năng tìm kiếm chính xác trong context dài.

**Cách Hoạt Động:**

1. Chèn 1 “needle” (fact ngẫu nhiên) vào vị trí X% trong context dài
2. Hỏi về needle đó
3. Kiểm tra xem model có tìm được không

**Biến Thể:**

```
Needle Position: [10%, 30%, 50%, 70%, 90%]
Context Length: [1K, 10K, 50K, 100K, 200K tokens]
→ Tạo ra heatmap 5x5 để đánh giá
```

**Implementation:**

```python
def needle_in_haystack_test(memory_system, needle_position=0.5):
    # 1. Tạo haystack (context dài)
    haystack = generate_long_context(num_tokens=100000)
    
    # 2. Chèn needle
    needle = "The secret code is XJ-9274"
    insert_pos = int(len(haystack) * needle_position)
    full_context = haystack[:insert_pos] + needle + haystack[insert_pos:]
    
    # 3. Ingest vào memory
    memory_system.add(full_context)
    
    # 4. Query
    query = "What is the secret code?"
    response = memory_system.search(query)
    
    # 5. Check
    return "XJ-9274" in response
```

**Frameworks Sử Dụng:**

- MemGPT/Letta: Primary benchmark
- OpenCompass: [NIAH Evaluation Guide](https://opencompass.readthedocs.io/en/latest/advanced_guides/needleinahaystack_eval.html)

---

### 🧩 3.3. MemoryAgentBench

**Đặc Điểm:** Benchmark cho Agent với Memory (không chỉ chatbot)

**4 Competencies:**

1. **Memory Formation:** Có extract được info quan trọng không?
2. **Memory Retrieval:** Tìm lại đúng lúc không?
3. **Memory Update:** Xử lý conflicting info thế nào?
4. **Memory Application:** Sử dụng memory để ra quyết định

**Paper:** [arXiv:2507.05257](https://arxiv.org/html/2507.05257v1)

**Use Case:** Phù hợp với multi-step agent tasks (booking, planning, research).

---

### 📋 3.4. Best Practices - Quy Trình Benchmark Chuẩn

**Pipeline 5 Bước:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: DATA PREPARATION                                       │
│  • Load benchmark dataset (LOCOMO/Custom)                       │
│  • Parse conversations + questions + ground truth               │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: MEMORY INGESTION                                       │
│  • Create isolated assistant per conversation (optional)        │
│  • Ingest turns with metadata (timestamps, speaker_id)          │
│  • Measure: Ingest latency, storage overhead                    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: RETRIEVAL EVALUATION                                   │
│  • For each question: search(query)                             │
│  • Compare retrieved IDs vs gold evidence IDs                   │
│  • Metrics: Recall@k, Precision@k, MRR                          │
│  • Measure: Search latency (P50/P95/P99)                        │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: GENERATION EVALUATION                                  │
│  • Generate answer using LLM + retrieved memory                 │
│  • Measure: E2E latency, token usage                            │
│  • Compare with ground truth                                    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: SCORING & ANALYSIS                                     │
│  • LLM-as-Judge: GPT-4o chấm CORRECT/WRONG                      │
│  • Calculate accuracy by category (single/multi/temporal)       │
│  • Generate report: JSON + visualization                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## PHẦN 2: TRIỂN KHAI THỰC TẾ

## 4. PIPELINE EVALUATION - KIẾN TRÚC VÀ QUY TRÌNH

### 🏗️ 4.1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      YOUR API ENDPOINTS                          │
│                                                                  │
│  POST /memories      ← Ingest conversation                      │
│  POST /search        ← Retrieve relevant memories               │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EVALUATION FRAMEWORK                            │
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │ Data Loader  │→ │ Test Runner  │→ │  Evaluator   │       │
│  └──────────────┘   └──────────────┘   └──────────────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│   LOCOMO JSON        API Calls          LLM Judge              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESULTS OUTPUT                              │
│  • Per-conversation JSON files                                  │
│  • Aggregate metrics (accuracy, latency)                        │
│  • Visualization (charts, heatmaps)                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. CODE IMPLEMENTATION - SKELETON CODE CHO API CỦA BẠN

### 🚀 5.1. Full Evaluation Pipeline

Tôi sẽ viết skeleton code cho API của bạn:

```python
#!/usr/bin/env python3
"""
Memory System Evaluation Framework
Hỗ trợ đánh giá API Memory System trên LOCOMO benchmark

Author: AI Assistant
Date: 2026-01-05
"""

import asyncio
import aiohttp
import json
import time
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Endpoints của bạn
API_BASE_URL = "http://103.253.20.30:8889"
ADD_MEMORY_ENDPOINT = f"{API_BASE_URL}/memories"
SEARCH_ENDPOINT = f"{API_BASE_URL}/search"

# OpenAI API cho LLM Judge
OPENAI_API_KEY = "your-openai-key"

# Dataset path
LOCOMO_DATA_PATH = "./data/locomo10.json"

# Output directory
OUTPUT_DIR = "./results"

# Test parameters
TOP_K = 3
SCORE_THRESHOLD = 0.7
TIMEOUT = 30.0

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Turn:
    """Một turn trong conversation"""
    speaker: str
    text: str
    dia_id: str
    img_url: Optional[str] = None
    
@dataclass
class Question:
    """Một câu hỏi benchmark"""
    question: str
    answer: str
    category: int  # 1=single-hop, 2=temporal, 3=multi-hop, 4=open-domain
    evidence: List[str]  # Dialog IDs chứa câu trả lời

@dataclass
class Conversation:
    """Một conversation đầy đủ"""
    sample_id: str
    speaker_a: str
    speaker_b: str
    sessions: List[List[Turn]]
    session_timestamps: List[str]
    questions: List[Question]
    
# ============================================================================
# 1. DATA LOADER
# ============================================================================

class LOCOMODataLoader:
    """Load và parse LOCOMO dataset"""
    
    @staticmethod
    def load_dataset(path: str) -> List[Conversation]:
        """Load LOCOMO JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conversations = []
        for sample in data:
            conv = LOCOMODataLoader._parse_conversation(sample)
            conversations.append(conv)
        
        return conversations
    
    @staticmethod
    def _parse_conversation(sample: dict) -> Conversation:
        """Parse một conversation sample"""
        conv_data = sample['conversation']
        
        # Extract sessions
        sessions = []
        timestamps = []
        session_num = 1
        
        while f'session_{session_num}' in conv_data:
            session_key = f'session_{session_num}'
            timestamp_key = f'session_{session_num}_date_time'
            
            # Parse turns trong session
            turns = []
            for turn_data in conv_data[session_key]:
                turn = Turn(
                    speaker=turn_data['speaker'],
                    text=turn_data['text'],
                    dia_id=turn_data['dia_id'],
                    img_url=turn_data.get('img_url')
                )
                turns.append(turn)
            
            sessions.append(turns)
            timestamps.append(conv_data.get(timestamp_key, ''))
            session_num += 1
        
        # Parse questions
        questions = []
        for qa in sample.get('qa', []):
            # Filter category 5 (adversarial) như các framework khác
            if qa['category'] != 5:
                question = Question(
                    question=qa['question'],
                    answer=qa['answer'],
                    category=qa['category'],
                    evidence=qa.get('evidence', [])
                )
                questions.append(question)
        
        return Conversation(
            sample_id=sample['sample_id'],
            speaker_a=conv_data['speaker_a'],
            speaker_b=conv_data['speaker_b'],
            sessions=sessions,
            session_timestamps=timestamps,
            questions=questions
        )

# ============================================================================
# 2. API CLIENT - ADAPTER CHO API CỦA BẠN
# ============================================================================

class MemoryAPIClient:
    """Wrapper cho API của bạn"""
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        
    async def add_memory(self, 
                         messages: List[Dict],
                         user_id: str,
                         run_id: str) -> Dict:
        """
        Gọi POST /memories để ingest conversation
        
        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            user_id: ID của user (ví dụ: "Đoàn Ngọc Cường")
            run_id: ID của session/conversation (ví dụ: "conv_001_session_1")
        
        Returns:
            Response từ API
        """
        payload = {
            "messages": messages,
            "user_id": user_id,
            "run_id": run_id
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/memories",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def search(self,
                     query: str,
                     user_id: str,
                     top_k: int = 3,
                     limit: int = 10,
                     score_threshold: float = 0.7) -> Dict:
        """
        Gọi POST /search để tìm kiếm memories
        
        Args:
            query: Câu hỏi cần tìm
            user_id: ID của user
            top_k: Số kết quả trả về
            limit: Limit cho internal retrieval
            score_threshold: Ngưỡng điểm similarity
        
        Returns:
            Response từ API với list of memories
        """
        payload = {
            "query": query,
            "user_id": user_id,
            "top_k": top_k,
            "limit": limit,
            "score_threshold": score_threshold
        }
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(
                f"{self.base_url}/search",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                result = await response.json()
                
        latency = time.time() - start_time
        result['_latency'] = latency
        
        return result

# ============================================================================
# 3. LLM JUDGE EVALUATOR
# ============================================================================

class LLMJudge:
    """GPT-4o làm giám khảo chấm điểm"""
    
    JUDGE_PROMPT_TEMPLATE = """
Your task is to label an answer to a question as 'CORRECT' or 'WRONG'. 

You will be given:
(1) a question
(2) a 'gold' (ground truth) answer
(3) a generated answer

The gold answer is usually concise. The generated answer might be much longer, 
but you should be GENEROUS with your grading - as long as it touches on the 
same topic as the gold answer, it should be counted as CORRECT.

For time-related questions:
- The gold answer will be a specific date/time
- The generated answer might use relative time ("last Tuesday", "next month")
- Be generous - if it refers to the same time period, mark CORRECT
- Format differences are OK (e.g., "May 7th" vs "7 May")

Now evaluate this:

Question: {question}
Gold Answer: {expected_answer}
Generated Answer: {ai_response}

Provide a short (one sentence) explanation of your reasoning, then finish with 
CORRECT or WRONG.

Return your response in JSON format with two keys:
- "reasoning": your explanation
- "label": "CORRECT" or "WRONG"

Do NOT include both CORRECT and WRONG in your response.
"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.1):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        
    async def evaluate(self,
                       question: str,
                       expected_answer: str,
                       ai_response: str) -> Dict:
        """
        Chấm điểm một câu trả lời
        
        Returns:
            {
                "label": "CORRECT" or "WRONG",
                "reasoning": "...",
                "is_correct": True/False
            }
        """
        prompt = self.JUDGE_PROMPT_TEMPLATE.format(
            question=question,
            expected_answer=expected_answer,
            ai_response=ai_response
        )
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a precise evaluator."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature,
                "response_format": {"type": "json_object"}
            }
            
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                result = await response.json()
                
        content = result['choices'][0]['message']['content']
        evaluation = json.loads(content)
        
        # Thêm flag is_correct
        evaluation['is_correct'] = evaluation['label'].upper() == 'CORRECT'
        
        return evaluation

# ============================================================================
# 4. TEST RUNNER
# ============================================================================

class MemoryBenchmarkRunner:
    """Chạy benchmark đầy đủ"""
    
    def __init__(self,
                 api_client: MemoryAPIClient,
                 judge: LLMJudge,
                 output_dir: str = "./results"):
        self.api_client = api_client
        self.judge = judge
        self.output_dir = output_dir
        
        # Statistics
        self.results = []
        self.latencies = []
        
    async def run_conversation(self, conversation: Conversation) -> Dict:
        """
        Chạy benchmark cho một conversation
        
        Pipeline:
        1. Ingest tất cả sessions
        2. Run questions
        3. Evaluate với LLM Judge
        
        Returns:
            Results dict với metrics
        """
        print(f"\n{'='*80}")
        print(f" Conversation: {conversation.sample_id}")
        print(f"{'='*80}\n")
        
        user_id = f"{conversation.speaker_a}_{conversation.speaker_b}"
        
        # Step 1: Ingest sessions
        print(f"📥 Ingesting {len(conversation.sessions)} sessions...")
        
        for idx, (session, timestamp) in enumerate(zip(
            conversation.sessions, 
            conversation.session_timestamps
        ), 1):
            run_id = f"{conversation.sample_id}_session_{idx}"
            
            # Convert turns to messages format
            messages = []
            for turn in session:
                role = "user" if turn.speaker == conversation.speaker_a else "assistant"
                messages.append({
                    "role": role,
                    "content": turn.text
                })
            
            # Ingest
            await self.api_client.add_memory(
                messages=messages,
                user_id=user_id,
                run_id=run_id
            )
            
            print(f"   ✓ Session {idx}/{len(conversation.sessions)} - {len(messages)} turns")
        
        # Step 2: Run questions
        print(f"\n❓ Running {len(conversation.questions)} questions...\n")
        
        question_results = []
        
        for q_idx, question in enumerate(conversation.questions, 1):
            print(f"   Question {q_idx}/{len(conversation.questions)} [category {question.category}]")
            print(f"   Q: {question.question}")
            
            # Search
            search_result = await self.api_client.search(
                query=question.question,
                user_id=user_id,
                top_k=TOP_K,
                score_threshold=SCORE_THRESHOLD
            )
            
            search_latency = search_result.get('_latency', 0)
            self.latencies.append(search_latency)
            
            # Extract answer từ memories (giả sử API trả về list memories)
            # TODO: Điều chỉnh theo format response thực tế của API bạn
            memories = search_result.get('results', [])
            ai_response = self._generate_answer_from_memories(
                question.question, 
                memories
            )
            
            print(f"   A: {ai_response}")
            print(f"   Expected: {question.answer}")
            print(f"   Latency: {search_latency:.2f}s")
            
            # Evaluate
            evaluation = await self.judge.evaluate(
                question=question.question,
                expected_answer=question.answer,
                ai_response=ai_response
            )
            
            result_symbol = "✅ CORRECT" if evaluation['is_correct'] else "❌ WRONG"
            print(f"   {result_symbol}")
            print(f"   Reasoning: {evaluation['reasoning']}\n")
            
            # Save result
            question_result = {
                "question": question.question,
                "expected_answer": question.answer,
                "category": question.category,
                "ai_response": ai_response,
                "evaluation": evaluation,
                "latency": search_latency,
                "memories_retrieved": len(memories)
            }
            question_results.append(question_result)
        
        # Calculate metrics
        correct_count = sum(1 for r in question_results if r['evaluation']['is_correct'])
        accuracy = correct_count / len(question_results) * 100
        
        print(f"\n{'='*80}")
        print(f" Conversation {conversation.sample_id} Results:")
        print(f"   Accuracy: {correct_count}/{len(question_results)} ({accuracy:.1f}%)")
        print(f"   Avg Latency: {np.mean(self.latencies[-len(question_results):]):.2f}s")
        print(f"{'='*80}\n")
        
        return {
            "sample_id": conversation.sample_id,
            "total_questions": len(question_results),
            "correct": correct_count,
            "accuracy": accuracy,
            "results": question_results
        }
    
    def _generate_answer_from_memories(self, 
                                       question: str, 
                                       memories: List[Dict]) -> str:
        """
        Sinh câu trả lời từ memories retrieved
        
        TODO: 
        - Nếu API của bạn đã trả về câu trả lời sẵn → dùng trực tiếp
        - Nếu chỉ trả về memories → cần gọi LLM để sinh answer
        
        Ví dụ đơn giản: Concatenate memories
        """
        if not memories:
            return "I don't have enough information to answer that question."
        
        # Giả sử mỗi memory có field 'content' hoặc 'text'
        context = "\n".join([m.get('content', m.get('text', '')) for m in memories])
        
        # Option 1: Trả về context trực tiếp (simple)
        # return context
        
        # Option 2: Gọi LLM để sinh answer (recommended)
        # answer = await call_llm_to_generate_answer(question, context)
        # return answer
        
        # Placeholder
        return f"Based on the memories: {context[:200]}..."
    
    async def run_full_benchmark(self, conversations: List[Conversation]) -> Dict:
        """Chạy benchmark cho tất cả conversations"""
        
        print(f"\n🚀 Starting LOCOMO Benchmark")
        print(f"   Total conversations: {len(conversations)}")
        print(f"   API: {self.api_client.base_url}\n")
        
        all_results = []
        
        for idx, conv in enumerate(conversations, 1):
            print(f"\n>>> Conversation {idx}/{len(conversations)}")
            
            try:
                result = await self.run_conversation(conv)
                all_results.append(result)
            except Exception as e:
                print(f"❌ Error processing conversation {conv.sample_id}: {e}")
                continue
        
        # Aggregate metrics
        return self._compute_aggregate_metrics(all_results)
    
    def _compute_aggregate_metrics(self, results: List[Dict]) -> Dict:
        """Tính toán metrics tổng hợp"""
        
        total_questions = sum(r['total_questions'] for r in results)
        total_correct = sum(r['correct'] for r in results)
        overall_accuracy = total_correct / total_questions * 100
        
        # Per-category breakdown
        category_stats = {1: [], 2: [], 3: [], 4: []}  # single, temporal, multi, open-domain
        
        for result in results:
            for q_result in result['results']:
                cat = q_result['category']
                category_stats[cat].append(q_result['evaluation']['is_correct'])
        
        category_accuracy = {}
        for cat, correct_list in category_stats.items():
            if correct_list:
                acc = sum(correct_list) / len(correct_list) * 100
                category_accuracy[cat] = {
                    "category_name": self._get_category_name(cat),
                    "questions": len(correct_list),
                    "correct": sum(correct_list),
                    "accuracy": acc
                }
        
        # Latency stats
        p50 = np.percentile(self.latencies, 50)
        p95 = np.percentile(self.latencies, 95)
        p99 = np.percentile(self.latencies, 99)
        
        aggregate = {
            "total_conversations": len(results),
            "total_questions": total_questions,
            "total_correct": total_correct,
            "overall_accuracy": overall_accuracy,
            "category_breakdown": category_accuracy,
            "latency_stats": {
                "mean": np.mean(self.latencies),
                "p50": p50,
                "p95": p95,
                "p99": p99
            },
            "per_conversation_results": results
        }
        
        # Print summary
        print(f"\n{'='*80}")
        print(f" 📊 FINAL RESULTS")
        print(f"{'='*80}\n")
        print(f"Overall Accuracy: {total_correct}/{total_questions} ({overall_accuracy:.1f}%)")
        print(f"\nPer-Category Accuracy:")
        for cat, stats in category_accuracy.items():
            print(f"   {stats['category_name']:20s}: {stats['correct']}/{stats['questions']:3d} ({stats['accuracy']:5.1f}%)")
        
        print(f"\nLatency Statistics:")
        print(f"   Mean:  {np.mean(self.latencies):.2f}s")
        print(f"   P50:   {p50:.2f}s")
        print(f"   P95:   {p95:.2f}s")
        print(f"   P99:   {p99:.2f}s")
        print(f"\n{'='*80}\n")
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.output_dir}/benchmark_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(aggregate, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}\n")
        
        return aggregate
    
    @staticmethod
    def _get_category_name(cat: int) -> str:
        names = {
            1: "Single-hop",
            2: "Temporal",
            3: "Multi-hop",
            4: "Open-domain"
        }
        return names.get(cat, f"Category-{cat}")

# ============================================================================
# 5. MAIN - ENTRY POINT
# ============================================================================

async def main():
    """Main entry point"""
    
    # 1. Load dataset
    print("📂 Loading LOCOMO dataset...")
    loader = LOCOMODataLoader()
    conversations = loader.load_dataset(LOCOMO_DATA_PATH)
    print(f"   Loaded {len(conversations)} conversations\n")
    
    # 2. Initialize components
    api_client = MemoryAPIClient(base_url=API_BASE_URL, timeout=TIMEOUT)
    judge = LLMJudge(api_key=OPENAI_API_KEY)
    runner = MemoryBenchmarkRunner(
        api_client=api_client,
        judge=judge,
        output_dir=OUTPUT_DIR
    )
    
    # 3. Run benchmark
    results = await runner.run_full_benchmark(conversations)
    
    print("✅ Benchmark completed!")
    
    return results

if __name__ == "__main__":
    # Run
    asyncio.run(main())
```

---

## 6. TESTING SCENARIOS - BỘ TEST CASES ĐẦY ĐỦ

### 🧪 6.1. Unit Tests cho Từng Component

```python
"""
Unit tests cho Memory System
tests/test_memory_components.py
"""

import pytest
import asyncio
from memory_evaluator import MemoryAPIClient, LLMJudge

# ============================================================================
# 1. Test Conflict Resolution
# ============================================================================

@pytest.mark.asyncio
async def test_conflict_resolution():
    """
    Test: User thay đổi sở thích
    
    Timeline:
    - Turn 1: "Tôi thích màu đỏ"
    - Turn 10: "Tôi đổi ý, tôi thích màu xanh"
    - Query: "Sở thích màu sắc của tôi là gì?"
    
    Expected: Trả về "màu xanh" (latest)
    """
    client = MemoryAPIClient(API_BASE_URL)
    
    # Ingest
    messages = [
        {"role": "user", "content": "Tôi thích màu đỏ"},
        {"role": "assistant", "content": "Được rồi, tôi nhớ rồi!"},
        # ... 8 turns khác
        {"role": "user", "content": "Tôi đổi ý, tôi thích màu xanh"},
        {"role": "assistant", "content": "OK, cập nhật rồi"}
    ]
    
    await client.add_memory(
        messages=messages,
        user_id="test_user_conflict",
        run_id="conflict_test_1"
    )
    
    # Query
    result = await client.search(
        query="Sở thích màu sắc của tôi là gì?",
        user_id="test_user_conflict"
    )
    
    # Assert
    response_text = str(result).lower()
    assert "xanh" in response_text, "Should return latest preference (xanh)"
    assert "đỏ" not in response_text or response_text.index("xanh") < response_text.index("đỏ"), \
        "xanh should appear before đỏ if both mentioned"

# ============================================================================
# 2. Test Temporal Reasoning
# ============================================================================

@pytest.mark.asyncio
async def test_temporal_reasoning():
    """
    Test: Phân biệt sự kiện theo thời gian
    
    Timeline:
    - Session 1 (May 2023): "Tôi đi Đà Lạt"
    - Session 2 (June 2023): "Tôi đi Nha Trang"
    - Query: "Tháng 6 năm 2023 tôi đi đâu?"
    
    Expected: "Nha Trang"
    """
    client = MemoryAPIClient(API_BASE_URL)
    
    # Session 1: May
    await client.add_memory(
        messages=[
            {"role": "user", "content": "Tôi vừa đi Đà Lạt về"}
        ],
        user_id="test_user_temporal",
        run_id="temporal_may_2023"
    )
    
    # Session 2: June
    await client.add_memory(
        messages=[
            {"role": "user", "content": "Tôi vừa đi Nha Trang về"}
        ],
        user_id="test_user_temporal",
        run_id="temporal_june_2023"
    )
    
    # Query với temporal context
    result = await client.search(
        query="Tháng 6 năm 2023 tôi đi đâu?",
        user_id="test_user_temporal"
    )
    
    response_text = str(result).lower()
    assert "nha trang" in response_text
    assert "đà lạt" not in response_text, "Should not return earlier trip"

# ============================================================================
# 3. Test Needle In Haystack
# ============================================================================

@pytest.mark.asyncio
async def test_needle_in_haystack():
    """
    Test: Tìm thông tin cụ thể trong conversation dài
    
    Setup:
    - 100 turns về nhiều topics
    - Turn 50: "Mã bí mật là XJ-9274"
    - Query: "Mã bí mật là gì?"
    
    Expected: "XJ-9274"
    """
    client = MemoryAPIClient(API_BASE_URL)
    
    # Tạo haystack
    messages = []
    for i in range(100):
        if i == 49:  # Turn 50 (0-indexed)
            messages.append({
                "role": "user",
                "content": "À đúng rồi, mã bí mật là XJ-9274 nhé"
            })
        else:
            messages.append({
                "role": "user",
                "content": f"Đây là câu số {i+1} nói về chủ đề ngẫu nhiên"
            })
    
    await client.add_memory(
        messages=messages,
        user_id="test_user_niah",
        run_id="niah_test"
    )
    
    # Query
    result = await client.search(
        query="Mã bí mật là gì?",
        user_id="test_user_niah"
    )
    
    response_text = str(result)
    assert "XJ-9274" in response_text

# ============================================================================
# 4. Test Negation Handling
# ============================================================================

@pytest.mark.asyncio
async def test_negation_handling():
    """
    Test: Hiểu câu phủ định
    
    Setup:
    - "Tôi KHÔNG thích cà phê"
    - Query: "Tôi có thích cà phê không?"
    
    Expected: "không" / "no" / "không thích"
    """
    client = MemoryAPIClient(API_BASE_URL)
    
    await client.add_memory(
        messages=[
            {"role": "user", "content": "Tôi KHÔNG thích cà phê"}
        ],
        user_id="test_user_negation",
        run_id="negation_test"
    )
    
    result = await client.search(
        query="Tôi có thích cà phê không?",
        user_id="test_user_negation"
    )
    
    response_text = str(result).lower()
    assert "không" in response_text or "no" in response_text

# ============================================================================
# 5. Test Cross-Session Memory
# ============================================================================

@pytest.mark.asyncio
async def test_cross_session_memory():
    """
    Test: Memory persist qua nhiều sessions
    
    Setup:
    - Session 1: "Tôi tên là Cường"
    - Session 2: (10 turns về topic khác)
    - Session 3: Query "Tên tôi là gì?"
    
    Expected: "Cường"
    """
    client = MemoryAPIClient(API_BASE_URL)
    user_id = "test_user_cross_session"
    
    # Session 1
    await client.add_memory(
        messages=[{"role": "user", "content": "Tôi tên là Cường"}],
        user_id=user_id,
        run_id="session_1"
    )
    
    # Session 2 (noise)
    await client.add_memory(
        messages=[
            {"role": "user", "content": f"Topic khác turn {i}"}
            for i in range(10)
        ],
        user_id=user_id,
        run_id="session_2"
    )
    
    # Session 3: Query
    result = await client.search(
        query="Tên tôi là gì?",
        user_id=user_id
    )
    
    response_text = str(result)
    assert "Cường" in response_text or "cuong" in response_text.lower()

# ============================================================================
# 6. Test Latency Under Load
# ============================================================================

@pytest.mark.asyncio
async def test_latency_under_load():
    """
    Test: P95 latency với concurrent requests
    
    Target: P95 < 5s
    """
    client = MemoryAPIClient(API_BASE_URL)
    
    # Prepare test data
    user_id = "test_user_latency"
    await client.add_memory(
        messages=[{"role": "user", "content": f"Info {i}"} for i in range(50)],
        user_id=user_id,
        run_id="latency_test"
    )
    
    # Concurrent queries
    latencies = []
    
    async def query_once():
        result = await client.search(
            query="Test query",
            user_id=user_id
        )
        return result.get('_latency', 0)
    
    # Run 100 concurrent requests
    tasks = [query_once() for _ in range(100)]
    latencies = await asyncio.gather(*tasks)
    
    # Calculate P95
    import numpy as np
    p95 = np.percentile(latencies, 95)
    
    print(f"P95 Latency: {p95:.2f}s")
    assert p95 < 5.0, f"P95 latency {p95:.2f}s exceeds 5s threshold"

# ============================================================================
# 7. Test LLM Judge Consistency
# ============================================================================

@pytest.mark.asyncio
async def test_llm_judge_consistency():
    """
    Test: LLM Judge có chấm điểm consistent không?
    
    Chạy cùng 1 test case 10 lần → agreement rate > 90%
    """
    judge = LLMJudge(api_key=OPENAI_API_KEY)
    
    question = "What is the capital of France?"
    expected = "Paris"
    
    test_cases = [
        ("Paris", True),  # Exact match
        ("The capital is Paris", True),  # Contains correct answer
        ("It's Paris", True),  # Informal
        ("London", False),  # Wrong
        ("I don't know", False)  # No answer
    ]
    
    for ai_response, expected_correct in test_cases:
        # Run 10 times
        results = []
        for _ in range(10):
            eval_result = await judge.evaluate(
                question=question,
                expected_answer=expected,
                ai_response=ai_response
            )
            results.append(eval_result['is_correct'])
        
        # Check consistency
        agreement_rate = sum(results) / len(results)
        
        if expected_correct:
            assert agreement_rate > 0.9, f"Judge inconsistent for correct answer: {ai_response}"
        else:
            assert agreement_rate < 0.1, f"Judge inconsistent for wrong answer: {ai_response}"

```

### 🎭 6.2. Integration Test với LOCOMO Mini

```python
"""
Mini LOCOMO test với 1 conversation nhỏ
tests/test_integration_mini_locomo.py
"""

MINI_LOCOMO_DATA = {
    "sample_id": "test-001",
    "conversation": {
        "speaker_a": "Alice",
        "speaker_b": "Bob",
        "session_1": [
            {"speaker": "Alice", "text": "Tớ là Alice, tớ làm AI Engineer", "dia_id": "d001"},
            {"speaker": "Bob", "text": "Chào Alice! Cậu làm về mảng gì?", "dia_id": "d002"},
            {"speaker": "Alice", "text": "Tớ làm LLM và RAG", "dia_id": "d003"}
        ],
        "session_1_date_time": "2023-05-01T10:00:00Z",
        "session_2": [
            {"speaker": "Alice", "text": "Tuần trước tớ đi Đà Lạt", "dia_id": "d004"},
            {"speaker": "Bob", "text": "Thế à? Vui không?", "dia_id": "d005"},
            {"speaker": "Alice", "text": "Rất vui! Tớ thích thời tiết ở đó", "dia_id": "d006"}
        ],
        "session_2_date_time": "2023-05-08T14:00:00Z"
    },
    "qa": [
        {
            "question": "Alice làm nghề gì?",
            "answer": "AI Engineer",
            "category": 1,  # single-hop
            "evidence": ["d001"]
        },
        {
            "question": "Alice làm về mảng gì cụ thể?",
            "answer": "LLM và RAG",
            "category": 1,
            "evidence": ["d003"]
        },
        {
            "question": "Alice đi đâu vào tuần trước session 2?",
            "answer": "Đà Lạt",
            "category": 2,  # temporal
            "evidence": ["d004"]
        }
    ]
}

@pytest.mark.asyncio
async def test_mini_locomo_integration():
    """Chạy full pipeline với 1 conversation nhỏ"""
    
    # 1. Setup
    client = MemoryAPIClient(API_BASE_URL)
    judge = LLMJudge(api_key=OPENAI_API_KEY)
    
    # 2. Parse data (giống LOCOMODataLoader)
    conv = MINI_LOCOMO_DATA
    user_id = f"{conv['conversation']['speaker_a']}_{conv['conversation']['speaker_b']}"
    
    # 3. Ingest sessions
    for session_num in [1, 2]:
        session_key = f"session_{session_num}"
        turns = conv['conversation'][session_key]
        
        messages = []
        for turn in turns:
            role = "user" if turn['speaker'] == "Alice" else "assistant"
            messages.append({"role": role, "content": turn['text']})
        
        await client.add_memory(
            messages=messages,
            user_id=user_id,
            run_id=f"{conv['sample_id']}_session_{session_num}"
        )
    
    # 4. Run questions
    results = []
    for qa in conv['qa']:
        # Search
        search_result = await client.search(
            query=qa['question'],
            user_id=user_id
        )
        
        # TODO: Generate answer (simplified - just use first memory)
        memories = search_result.get('results', [])
        ai_response = memories[0]['content'] if memories else "Không biết"
        
        # Evaluate
        evaluation = await judge.evaluate(
            question=qa['question'],
            expected_answer=qa['answer'],
            ai_response=ai_response
        )
        
        results.append(evaluation['is_correct'])
    
    # 5. Assert
    accuracy = sum(results) / len(results) * 100
    print(f"Mini LOCOMO Accuracy: {accuracy:.1f}%")
    
    assert accuracy >= 66.0, f"Accuracy {accuracy:.1f}% below Mem0 baseline (66.9%)"
```

---

## 7. CHECKLIST TRIỂN KHAI

### ✅ Phase 1: Setup Cơ Bản (1-2 ngày)

- [ ] Clone LOCOMO dataset từ [snap-research/locomo](https://github.com/snap-research/locomo)
- [ ] Cài đặt dependencies (`requirements.txt`)
- [ ] Setup OpenAI API key cho LLM Judge
- [ ] Test API endpoints (`/memories`, `/search`) với curl
- [ ] Chạy unit test cơ bản (conflict, negation)

### ✅ Phase 2: Adapter Layer (1 ngày)

- [ ] Implement `MemoryAPIClient` class
- [ ] Test connection với API của bạn
- [ ] Điều chỉnh format request/response match với API spec
- [ ] Handle error cases (timeout, 4xx, 5xx)

### ✅ Phase 3: Evaluation Pipeline (2-3 ngày)

- [ ] Implement `LOCOMODataLoader`
- [ ] Implement `LLMJudge` với GPT-4o
- [ ] Implement `MemoryBenchmarkRunner`
- [ ] Test với Mini LOCOMO (1 conversation)
- [ ] Chạy full LOCOMO (10 conversations)

### ✅ Phase 4: Analysis & Optimization (1-2 ngày)

- [ ] Generate metrics report (accuracy, latency)
- [ ] So sánh với baselines (Mem0, OpenAI, Zep)
- [ ] Identify failure cases (xem question nào sai)
- [ ] Optimize system dựa trên findings

---

## 8. KẾT LUẬN VÀ KHUYẾN NGHỊ

### 🎯 Key Takeaways

1. **MECE Framework:** 4 trụ cột độc lập - Retrieval, Generation, Performance, Robustness
2. **Benchmark Chuẩn:** LOCOMO là gold standard cho conversational memory (được Mem0, Zep, Backboard sử dụng)
3. **LLM-as-Judge:** GPT-4o với temperature=0.1 là phương pháp evaluation được chấp nhận rộng rãi
4. **Baselines:** Mem0 (66.9%), Zep (~75%), Backboard (90%) - Target của bạn nên aim ≥65% để competitive

### 💡 Best Practices

1. **Isolated Testing:** Tạo assistant/user riêng cho mỗi conversation để tránh memory leak
2. **Timestamp Metadata:** Luôn attach timestamp vào memories để support temporal reasoning
3. **Generous Grading:** LLM Judge nên lenient - chấm CORRECT nếu answer “touches same topic”
4. **P95 Latency:** Target <5s, optimal <2s cho production
5. **Incremental Testing:** Chạy mini-test trước khi chạy full benchmark (tiết kiệm cost)

### 🚀 Next Steps

Sau khi có kết quả benchmark:

1. **So sánh với SOTA:** Đặt kết quả của bạn vào bảng leaderboard
2. **Failure Analysis:** Review từng câu sai → tìm pattern → fix
3. **Ablation Study:** Test từng component riêng (vector search, graph, reranking…)
4. **Publish Results:** Nếu đạt SOTA → viết blog post/paper

---

## PHỤ LỤC

### A. API Response Format (Cần điều chỉnh theo API của bạn)

```json
{
  "results": [
    {
      "content": "Text của memory",
      "score": 0.95,
      "metadata": {
        "timestamp": "2023-05-08T13:56:00Z",
        "run_id": "session_1"
      }
    }
  ],
  "total": 5
}
```

### B. Useful Links

- [LOCOMO Dataset](https://github.com/snap-research/locomo)
- [Mem0 Paper](https://arxiv.org/html/2504.19413v1)
- [Backboard Benchmark Implementation](https://github.com/Backboard-io/Backboard-Locomo-Benchmark)
- [Ragas Documentation](https://docs.ragas.io/)
- [DeepEval Documentation](https://docs.confident-ai.com/)

### C. Cost Estimation

**Full LOCOMO Benchmark:**

- Conversations: 10
- Questions: ~250
- LLM Judge calls: ~250 × GPT-4o = ~$5-10
- Total time: 30-60 minutes (với concurrent processing)

---

**Tác giả:** AI Assistant  
**Ngày:** 2026-01-05  
**Phiên bản:** 1.0

---

Bạn có muốn tôi:

1. ✍️ Viết thêm code cho phần generate answer từ memories (integrate với LLM)?
2. 📊 Tạo visualization script để plot accuracy heatmap?
3. 🔧 Customize cho format API cụ thể của bạn (cần xem response example)?
4. 🧪 Viết thêm advanced test cases (multi-agent, RAG comparison)?