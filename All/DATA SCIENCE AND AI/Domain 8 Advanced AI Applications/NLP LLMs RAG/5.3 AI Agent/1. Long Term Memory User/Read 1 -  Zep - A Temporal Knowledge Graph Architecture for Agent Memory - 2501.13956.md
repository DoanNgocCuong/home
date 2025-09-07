[2501.13956](https://arxiv.org/pdf/2501.13956)

# Tóm tắt PDF: ZEP - Kiến trúc Đồ thị Kiến thức Thời gian cho Bộ nhớ của Đại lý

## Tổng quana
Tài liệu giới thiệu **Zep**, một dịch vụ lớp bộ nhớ mới được thiết kế cho các đại lý AI, cho thấy sự vượt trội so với hệ thống MemGPT hiện có trong nhiều bài kiểm tra. Zep đặc biệt hiệu quả trong việc tích hợp kiến thức động từ nhiều nguồn khác nhau, khắc phục những hạn chế của các hệ thống truy xuất tài liệu tĩnh.

## Các chủ đề chính và ý tưởng cốt lõi

1. **Bài kiểm tra Truy xuất Bộ nhớ Sâu (DMR)**:
   - Zep vượt trội hơn MemGPT với điểm số 94.8% so với 93.4% của MemGPT trong bài kiểm tra DMR, cho thấy khả năng truy xuất bộ nhớ được cải thiện, phù hợp với các ứng dụng doanh nghiệp thực tế.

2. **Tích hợp Kiến thức Động**:
   - Khác với các khuôn khổ RAG truyền thống, Zep tích hợp cả dữ liệu hội thoại không có cấu trúc và dữ liệu doanh nghiệp có cấu trúc, duy trì các mối quan hệ lịch sử thông qua thành phần chính của nó, **Graphiti**.

3. **Cấu trúc Đồ thị Kiến thức Tầng bậc**:
   - Bộ nhớ của Zep được cung cấp bởi một đồ thị kiến thức động, nhận thức thời gian, bao gồm ba tầng con:
     - **Tầng Episode**: Lưu trữ dữ liệu đầu vào thô.
     - **Tầng Thực thể Ngữ nghĩa**: Chứa các thực thể được trích xuất từ các episode.
     - **Tầng Cộng đồng**: Đại diện cho các cụm thực thể liên kết, cung cấp cái nhìn toàn diện về đồ thị kiến thức.

4. **Mô hình Hai Thời gian**:
   - Zep sử dụng mô hình hai thời gian để xử lý các cập nhật thông tin động, cho phép trích xuất thời gian chính xác và vô hiệu hóa các cạnh. Điều này giúp hệ thống quản lý các cuộc hội thoại đang tiến triển hiệu quả.

5. **Cơ chế Truy xuất Bộ nhớ**:
   - Quy trình truy xuất bao gồm ba bước: Tìm kiếm, Xếp hạng lại và Tạo, làm việc cùng nhau để cung cấp ngữ cảnh liên quan cho các đại lý AI dựa trên truy vấn của người dùng.

## Các điểm chính và điểm nổi bật

- **Cải tiến Hiệu suất**:
  - Zep cho thấy sự cải thiện đáng kể về độ chính xác (lên tới 18.5%) và giảm độ trễ phản hồi (90%) trong các nhiệm vụ quan trọng của doanh nghiệp so với các triển khai cơ bản, đặc biệt trong các nhiệm vụ lý luận thời gian phức tạp.

- **Bài kiểm tra Đánh giá**:
  - Tài liệu chi tiết các đánh giá sử dụng các bài kiểm tra DMR và LongMemEval, nhấn mạnh khả năng của Zep trong việc xử lý các cuộc hội thoại dài hơn, mạch lạc hơn phản ánh các tình huống thực tế.

- **Phát hiện Cộng đồng**:
  - Zep cập nhật động các cấu trúc cộng đồng thông qua một thuật toán lan truyền nhãn, đảm bảo đại diện cộng đồng hiệu quả khi dữ liệu mới vào đồ thị.

- **Hướng nghiên cứu trong tương lai**:
  - Tác giả đề xuất một số hướng nghiên cứu trong tương lai, bao gồm việc khám phá các ontologies cụ thể theo miền và cải thiện độ tin cậy của các bài kiểm tra bộ nhớ để phản ánh tốt hơn các ứng dụng doanh nghiệp.

## Kết luận
Zep đại diện cho một bước tiến quan trọng trong các hệ thống bộ nhớ LLM, tích hợp bộ nhớ sự kiện và ngữ nghĩa cùng với các tóm tắt thực thể và cộng đồng, đạt được hiệu suất hàng đầu trong khi giảm chi phí vận hành và độ trễ. Những phát hiện nhấn mạnh nhu cầu về các bài kiểm tra mạnh mẽ hơn để đánh giá khả năng của các hệ thống bộ nhớ trong các ứng dụng thực tế. 

---

Tóm tắt này cung cấp cái nhìn rõ ràng về các ý tưởng cốt lõi và điểm nổi bật của PDF, giúp hiểu rõ hơn về những đóng góp của Zep cho các hệ thống bộ nhớ của đại lý AI.


### Tác Động của Các Mô Hình Ngôn Ngữ Lớn Dựa Trên Transformer đến Ngành Công Nghiệp và Cộng Đồng Nghiên Cứu

Tác động của các mô hình ngôn ngữ lớn (LLMs) dựa trên transformer đến ngành công nghiệp và cộng đồng nghiên cứu đã thu hút được sự chú ý đáng kể trong những năm gần đây. Một ứng dụng chính của LLMs là phát triển các tác nhân trò chuyện. Tuy nhiên, khả năng của các tác nhân này bị giới hạn bởi cửa sổ ngữ cảnh của LLMs, việc sử dụng ngữ cảnh hiệu quả và kiến thức thu được trong quá trình tiền huấn luyện. Do đó, cần có thêm ngữ cảnh để cung cấp kiến thức ngoài miền (OOD) và giảm thiểu hiện tượng "hallucination".

### Tăng Cường Tạo Sinh Dữ Liệu (RAG)

Tăng cường tạo sinh dữ liệu (RAG) đã nổi lên như một lĩnh vực quan tâm chính trong các ứng dụng dựa trên LLM. RAG tận dụng các kỹ thuật truy xuất thông tin (IR) đã được phát triển trong suốt năm mươi năm qua để cung cấp kiến thức miền cần thiết cho LLMs. Các phương pháp hiện tại sử dụng RAG đã tập trung vào kiến thức miền rộng và các tập dữ liệu tĩnh lớn—tức là, nội dung tài liệu được thêm vào một tập hợp hiếm khi thay đổi. Để các tác nhân có thể trở nên phổ biến trong cuộc sống hàng ngày của chúng ta, tự động giải quyết các vấn đề từ đơn giản đến phức tạp, họ sẽ cần truy cập vào một tập hợp dữ liệu lớn liên tục phát triển từ các tương tác của người dùng với tác nhân, cùng với dữ liệu kinh doanh và thế giới liên quan. Chúng tôi coi việc trang bị cho các tác nhân với "bộ nhớ" rộng và động này là một yếu tố xây dựng quan trọng để hiện thực hóa tầm nhìn này, và chúng tôi lập luận rằng các phương pháp RAG hiện tại không phù hợp cho tương lai này. Vì toàn bộ lịch sử hội thoại, tập dữ liệu kinh doanh và nội dung miền cụ thể khác không thể phù hợp hiệu quả trong các cửa sổ ngữ cảnh của LLM, cần phát triển các phương pháp mới cho bộ nhớ của tác nhân.

### Sử Dụng Đồ Thị Kiến Thức để Nâng Cao Bộ Nhớ Tác Nhân LLM

Việc thêm bộ nhớ cho các tác nhân sử dụng LLM không phải là một ý tưởng mới—khái niệm này đã được khám phá trước đây trong MemGPT. Gần đây, các Đồ thị Kiến thức (KGs) đã được sử dụng để nâng cao các kiến trúc RAG nhằm giải quyết nhiều thiếu sót của các kỹ thuật IR truyền thống. Trong bài báo này, chúng tôi giới thiệu Zep, một dịch vụ lớp bộ nhớ được cung cấp bởi Graphiti, một động cơ đồ thị kiến thức nhạy cảm với thời gian. Zep tiếp nhận và tổng hợp cả dữ liệu tin nhắn không cấu trúc và dữ liệu kinh doanh có cấu trúc. Động cơ KG Graphiti cập nhật động đồ thị kiến thức với thông tin mới theo cách không mất mát, duy trì một dòng thời gian của các sự kiện và mối quan hệ, bao gồm cả thời gian hiệu lực của chúng. Cách tiếp cận này cho phép đồ thị kiến thức đại diện cho một thế giới phức tạp, đang phát triển.

Vì Zep là một hệ thống sản xuất, chúng tôi đã tập trung mạnh mẽ vào độ chính xác, độ trễ và khả năng mở rộng của các cơ chế truy xuất bộ nhớ của nó. Chúng tôi đánh giá hiệu quả của các cơ chế này bằng cách sử dụng hai chuẩn mực hiện có: một nhiệm vụ Truy xuất Bộ nhớ Sâu (DMR) từ MemGPT, cũng như chuẩn LongMemEval.

### Xây Dựng Đồ Thị Kiến Thức

Trong Zep, bộ nhớ được cung cấp bởi một đồ thị kiến thức động nhạy cảm với thời gian G = (N, E, φ), trong đó N đại diện cho các nút, E đại diện cho các cạnh, và φ : E → N × N đại diện cho một hàm tác động chính thức. Đồ thị này bao gồm ba cấp bậc phân cấp của các đồ thị con: một đồ thị con tập phim, một đồ thị con thực thể ngữ nghĩa và một đồ thị con cộng đồng.

- **Đồ Thị Con Tập Phim Ge**: Các nút tập phim (tập phim), ni ∈ Ne, chứa dữ liệu đầu vào thô dưới dạng tin nhắn, văn bản hoặc JSON. Các tập phim phục vụ như một kho dữ liệu không mất mát từ đó các thực thể ngữ nghĩa và mối quan hệ được trích xuất. Các cạnh tập phim, ei ∈ Ee ⊆ φ∗(Ne × Ns), kết nối các tập phim với các thực thể ngữ nghĩa mà chúng tham chiếu.

- **Đồ Thị Con Thực Thể Ngữ Nghĩa Gs**: Đồ thị con thực thể ngữ nghĩa xây dựng dựa trên đồ thị con tập phim. Các nút thực thể (thực thể), ni ∈ Ns, đại diện cho các thực thể được trích xuất từ các tập phim và được giải quyết với các thực thể đồ thị hiện có. Các cạnh thực thể (cạnh ngữ nghĩa), ei ∈ Es ⊆ φ∗(Ns × Ns), đại diện cho các mối quan hệ giữa các thực thể được trích xuất từ các tập phim.

- **Đồ Thị Con Cộng Đồng Gc**: Đồ thị con cộng đồng tạo thành cấp cao nhất của đồ thị kiến thức Zep. Các nút cộng đồng (cộng đồng), ni ∈ Nc, đại diện cho các cụm các thực thể liên kết chặt chẽ. Các cộng đồng chứa các tóm tắt cấp cao về các cụm này và đại diện cho một cái nhìn tổng quát hơn, liên kết hơn về cấu trúc của Gs. Các cạnh cộng đồng, ei ∈ Ec ⊆ φ∗(Nc × Ns), kết nối các cộng đồng với các thành viên thực thể của chúng.

Việc lưu trữ đồng thời cả dữ liệu tập phim thô và thông tin thực thể ngữ nghĩa trích xuất phản ánh các mô hình tâm lý học về bộ nhớ con người. Các mô hình này phân biệt giữa bộ nhớ tập phim, đại diện cho các sự kiện riêng biệt, và bộ nhớ ngữ nghĩa, ghi lại các liên kết giữa các khái niệm và ý nghĩa của chúng. Cách tiếp cận này cho phép các tác nhân LLM sử dụng Zep phát triển các cấu trúc bộ nhớ tinh vi và tinh tế hơn, phù hợp hơn với sự hiểu biết của chúng ta về các hệ thống bộ nhớ con người. Các đồ thị kiến thức cung cấp một phương tiện hiệu quả để đại diện cho các cấu trúc bộ nhớ này, và việc triển khai của chúng tôi về các đồ thị con tập phim và ngữ nghĩa tách biệt lấy cảm hứng từ các phương pháp tương tự trong AriGraph. Việc sử dụng các nút cộng đồng để đại diện cho các cấu trúc cấp cao và các khái niệm miền xây dựng dựa trên công việc từ GraphRAG, cho phép hiểu biết toàn cầu toàn diện hơn về miền.

---
Dưới đây là tóm tắt nội dung và các điểm chính của bài báo “ZEP: A TEMPORAL KNOWLEDGE GRAPH ARCHITECTURE FOR AGENT MEMORY” (mã arXiv: 2501.13956v1). Bài báo mô tả hệ thống Zep – một “memory layer” (lớp bộ nhớ) dành cho các mô hình ngôn ngữ lớn (LLM), giúp mô hình ghi nhớ và truy xuất thông tin từ các đoạn hội thoại cũng như dữ liệu doanh nghiệp một cách hiệu quả hơn. Tác giả so sánh Zep với MemGPT và các phương pháp RAG (Retrieval-Augmented Generation) khác trong bối cảnh sử dụng cho các ứng dụng “chatbot” và “AI agent” phức tạp.

---

## 1. Bối cảnh và động lực

- **Vấn đề**: Các mô hình ngôn ngữ lớn (LLMs) khi triển khai trong các “chatbot” hay “AI agent” thường gặp hạn chế về dung lượng ngữ cảnh (context window) và khả năng cập nhật thông tin động. Khi độ dài hội thoại hoặc dữ liệu doanh nghiệp trở nên lớn, việc đưa trực tiếp tất cả vào “prompt” là không khả thi.
- **Giải pháp truyền thống**: Nhiều hệ thống áp dụng RAG (Retrieval-Augmented Generation) – tức là tìm kiếm (retrieval) các mẩu thông tin quan trọng trong “corpus” hoặc “document store” rồi chèn vào ngữ cảnh (prompt). Tuy nhiên, hầu hết chỉ tập trung vào kho dữ liệu “tĩnh” (static) hay các văn bản không thay đổi thường xuyên.
- **Điểm mới**: Trong thực tế doanh nghiệp, dữ liệu liên tục thay đổi (thông tin khách hàng, các sự kiện, luồng hội thoại dài, v.v.). Để chatbot hay AI agent “nhớ” và lập luận được với lượng thông tin “động” này, ta cần một lớp “bộ nhớ dài hạn” hiệu quả. Bài báo giới thiệu Zep, một dịch vụ memory layer sử dụng “Temporal Knowledge Graph” (đồ thị tri thức có tính thời gian) để quản lý và tìm kiếm thông tin.

---

## 2. Kiến trúc Zep

Zep sử dụng **Graphiti** – một công cụ xây dựng đồ thị tri thức có tính thời gian (temporal), chia dữ liệu thành ba lớp:

1. **Episode Subgraph** (các “episode”):
    
    - Mỗi “episode” là một đơn vị dữ liệu thô, ví dụ: một tin nhắn, một đoạn text, hay một JSON.
    - Thông tin ở đây mang tính “episodic” – giống khái niệm “bộ nhớ sự kiện” (episodic memory) trong tâm lý học.
2. **Semantic Entity Subgraph** (các thực thể và quan hệ):
    
    - Từ những “episode” (tin nhắn), hệ thống trích xuất **thực thể** (entity) và **mối quan hệ** (fact/edge) giữa các thực thể đó (ví dụ: “A làm việc tại công ty B từ năm 2020 đến 2022”).
    - Thêm bước “entity resolution” để gộp những thực thể trùng nhau (nhưng có thể được nhắc với tên hơi khác) thành một node duy nhất.
    - Thông tin thời gian (thời điểm có hiệu lực, lúc bắt đầu/kết thúc) được lưu cùng các quan hệ để theo dõi thay đổi của sự thật (“fact”) theo thời gian.
3. **Community Subgraph** (các cụm cộng đồng):
    
    - Hệ thống gom nhóm các thực thể, mối quan hệ lại thành “cộng đồng” (community) – về cơ bản là các cụm các node liên quan chặt chẽ.
    - Mỗi cộng đồng có một “summary” (tóm tắt) mô tả khái quát các thực thể và thông tin bên trong.

Với cấu trúc này, Zep duy trì được lịch sử thay đổi của thông tin, vừa có thể linh hoạt trả lời các câu hỏi mang tính thời gian (ví dụ: “A đã làm việc ở đâu vào năm ngoái?”) vừa có thể tóm tắt/khái quát bằng các summary.

---

## 3. Cơ chế lưu trữ và truy xuất (Memory Retrieval)

Zep áp dụng chiến lược tìm kiếm (search) nhiều bước:

1. **Tạo index (xây dựng embeddings, BM25, v.v.)**:
    
    - Mỗi “fact” và mỗi “thực thể” đều có embedding (vector) để phục vụ tìm kiếm theo độ tương đồng cosine.
    - Ngoài ra, tên hoặc mô tả (summary) của thực thể, fact có thể dùng cho tìm kiếm full-text (BM25).
    - Có thể sử dụng tìm kiếm theo khoảng cách trên đồ thị (breadth-first search) để truy xuất thông tin gần các nút quan trọng.
2. **Kết hợp, xếp hạng lại (reranker)**:
    
    - Sau khi lấy được danh sách kết quả theo nhiều cách (cosine, BM25, BFS), Zep áp dụng các thuật toán như RRF (Reciprocal Rank Fusion), MMR (Maximal Marginal Relevance), hoặc mô hình cross-encoder để xếp hạng lại, ưu tiên các kết quả quan trọng nhất.
3. **Kết hợp dữ liệu thành “context string”**:
    
    - Từ top-N “edges” (fact) và “nodes” (entity) được xếp hạng cao, Zep xây dựng một đoạn văn bản (context) có cấu trúc, để đưa vào prompt cho LLM. Đoạn này thường bao gồm:
        - Các fact kèm thời gian hiệu lực
        - Thông tin tóm tắt về thực thể
        - Tóm lược cộng đồng nếu cần

Cách làm này giúp “nối dài” bộ nhớ của LLM mà không cần tải toàn bộ lịch sử vào ngữ cảnh. Hơn nữa, do Zep có khả năng ghi nhận và vô hiệu hóa (invalidate) các fact cũ khi có mâu thuẫn mới, nó cho phép cập nhật thông tin động khá hiệu quả.

---

## 4. Thực nghiệm và đánh giá

### 4.1 Deep Memory Retrieval (DMR)

- **DMR** (giới thiệu trong MemGPT) có 500 cuộc hội thoại nhiều phiên (multi-session).
- Zep đạt **94.8%** độ chính xác khi dùng GPT-4-turbo (và 98.2% khi dùng một biến thể GPT-4o-mini), nhỉnh hơn so với MemGPT (93.4%).
- Tuy nhiên, bộ DMR chỉ có hội thoại khá ngắn (khoảng 60 tin nhắn mỗi cuộc), chưa thực sự kiểm tra khả năng “siêu dài hạn”.

### 4.2 LongMemEval (LME)

- **LongMemEval** có các đoạn hội thoại dài hơn nhiều (trung bình 115.000 tokens), mô phỏng tình huống doanh nghiệp thực tế phức tạp.
- Zep cải thiện kết quả so với baseline (dùng toàn bộ hội thoại) ở hầu hết các loại câu hỏi, đặc biệt:
    - Loại câu “multi-session,” “preference,” “temporal reasoning” tăng đáng kể.
    - Độ trễ (latency) giảm đến 90% so với việc nhét toàn bộ hội thoại vào prompt (vì prompt của Zep ngắn gọn hơn).

Những kết quả này cho thấy Zep hỗ trợ LLM tốt hơn khi phải ghi nhớ hoặc truy xuất thông tin từ hội thoại dài, hoặc cần các suy luận thời gian phức tạp.

---

## 5. Kết luận và hướng nghiên cứu

- **Zep** là một bước tiến trong việc xây dựng bộ nhớ “sống” (dynamic memory) cho các tác vụ hội thoại AI.
- Kết quả của Zep trên DMR và LongMemEval cho thấy tính hiệu quả về độ chính xác (so với MemGPT, so với tóm tắt truyền thống) và tiết kiệm chi phí (ít token hơn, độ trễ thấp hơn).
- Cách tiếp cận **“Temporal Knowledge Graph”** (Graphiti) cho phép đại diện cho thông tin thay đổi theo thời gian (ngày bắt đầu, ngày kết thúc), và đảm bảo không bị mất dữ liệu gốc (non-lossy).
- Các khả năng mở rộng:
    1. Kết hợp Zep với các mô hình trích xuất thực thể/fact được huấn luyện đặc thù hơn (fine-tuned) để giảm chi phí suy luận.
    2. Xây dựng thêm các “ontologies” (định nghĩa lớp, kiểu quan hệ) cho từng ngành/lĩnh vực cụ thể.
    3. Xây dựng benchmark mới, sát với thực tế doanh nghiệp hơn, đánh giá khả năng kết hợp hội thoại và dữ liệu có cấu trúc.
    4. Phân tích sâu về hiệu năng (latency, throughput, chi phí hạ tầng) của kiến trúc GraphRAG/Zep.

---

## Tóm tắt ngắn gọn

Bài báo mô tả **Zep**, một dịch vụ “memory layer” cho mô hình ngôn ngữ, sử dụng đồ thị tri thức mang tính thời gian (Graphiti). Mục tiêu là giúp LLM “nhớ” thông tin hội thoại và dữ liệu cập nhật liên tục, từ đó trả lời chính xác hơn, tránh lãng phí token, độ trễ thấp. Bằng cách dùng tầng đồ thị gồm “episode,” “entity-fact,” và “community,” Zep lưu được lịch sử, cập nhật mối quan hệ khi có dữ liệu mới, hỗ trợ suy luận thời gian. Thử nghiệm trên hai bộ DMR và LongMemEval cho thấy Zep vừa cải thiện độ chính xác, vừa giảm đáng kể thời gian xử lý so với các phương pháp tóm tắt hoặc MemGPT.

---

**Nếu bạn cần thêm chi tiết nào khác (ví dụ: phân tích thuật toán, mã pseudo code, so sánh kỹ về MemGPT, hoặc hướng dẫn triển khai), hãy cho tôi biết!**



## LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory


**Keywords:** long-term memory, retrieval-augmented generation

**Abstract:**

Recent large language model (LLM)-driven chat assistant systems have integrated memory components to track user-assistant chat histories, enabling more accurate and personalized responses. However, their long-term memory capabilities in sustained interactions remain underexplored. This paper introduces LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long-term memory systems, with commercial chat assistants and long-context LLMs showing 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term memory design into four design choices across the indexing, retrieval, and reading stages. Built upon key experimental insights, we propose several memory designs including session decomposition for optimizing value granularity, fact-augmented key expansion for enhancing the index structure, and time-aware query expansion for refining the search scope. Experiment results show that these optimizations greatly improve both memory recall and downstream question answering on LongMemEval. Overall, our study provides valuable resources and guidance for advancing the long-term memory capabilities of LLM-based chat assistants, paving the way toward more personalized and reliable conversational AI.


Các hệ thống trợ lý trò chuyện ngôn ngữ lớn gần đây (LLM) có các thành phần bộ nhớ tích hợp để theo dõi lịch sử trò chuyện có sự hỗ trợ của người dùng, cho phép các phản hồi chính xác và cá nhân hóa hơn. Tuy nhiên, khả năng bộ nhớ dài hạn của họ trong các tương tác bền vững vẫn chưa được khai thác. Bài viết này giới thiệu Longmemeval, một điểm chuẩn toàn diện được thiết kế để đánh giá năm khả năng bộ nhớ dài hạn cốt lõi của các trợ lý trò chuyện: trích xuất thông tin, lý luận đa phiên, lý luận thời gian, cập nhật kiến ​​thức và kiêng khem. Với 500 câu hỏi được quản lý tỉ mỉ được nhúng trong lịch sử trò chuyện hỗ trợ người dùng có thể mở rộng, Longmemeval đưa ra một thách thức đáng kể đối với các hệ thống bộ nhớ dài hạn hiện có, với các trợ lý trò chuyện thương mại và LLM bối cảnh dài cho thấy độ chính xác giảm 30% khi ghi nhớ thông tin qua các tương tác được duy trì. Sau đó, chúng tôi trình bày một khung thống nhất phân chia thiết kế bộ nhớ dài hạn thành bốn lựa chọn thiết kế trên các giai đoạn lập chỉ mục, truy xuất và đọc. Được xây dựng dựa trên những hiểu biết thử nghiệm quan trọng, chúng tôi đề xuất một số thiết kế bộ nhớ bao gồm phân tách phiên để tối ưu hóa mức độ chi tiết giá trị, mở rộng chính được thực hiện để tăng cường cấu trúc chỉ số và mở rộng truy vấn thời gian để tinh chỉnh phạm vi tìm kiếm. Kết quả thử nghiệm cho thấy các tối ưu hóa này cải thiện đáng kể cả việc thu hồi bộ nhớ và trả lời câu hỏi hạ nguồn trên longmemeval. Nhìn chung, nghiên cứu của chúng tôi cung cấp các nguồn lực và hướng dẫn có giá trị để thúc đẩy khả năng bộ nhớ dài hạn của các trợ lý trò chuyện dựa trên LLM, mở đường cho AI trò chuyện cá nhân hóa và đáng tin cậy hơn.

Đúng vậy, trong benchmark LongMemEval, các khả năng như trích xuất thông tin (information extraction), suy luận đa phiên (multi-session reasoning), suy luận thời gian (temporal reasoning), cập nhật kiến thức (knowledge updates) và từ chối trả lời (abstention) được sử dụng để đánh giá hiệu suất của các trợ lý trò chuyện trong việc ghi nhớ và xử lý thông tin dài hạn. citeturn0search1

Cụ thể:

- **Trích xuất thông tin (Information Extraction)**: Khả năng nhớ lại thông tin cụ thể từ lịch sử tương tác dài, bao gồm cả chi tiết được đề cập bởi người dùng hoặc trợ lý.
    
- **Suy luận đa phiên (Multi-Session Reasoning)**: Khả năng tổng hợp thông tin từ nhiều phiên lịch sử để trả lời các câu hỏi phức tạp liên quan đến việc tổng hợp và so sánh.
    
- **Suy luận thời gian (Temporal Reasoning)**: Nhận thức về các khía cạnh thời gian của thông tin người dùng, bao gồm cả các đề cập thời gian rõ ràng và siêu dữ liệu dấu thời gian trong các tương tác.
    
- **Cập nhật kiến thức (Knowledge Updates)**: Khả năng nhận biết các thay đổi trong thông tin cá nhân của người dùng và cập nhật kiến thức về người dùng một cách động theo thời gian.
    
- **Từ chối trả lời (Abstention)**: Khả năng từ chối trả lời các câu hỏi liên quan đến thông tin không được đề cập trong lịch sử tương tác, tức là thông tin không được nhắc đến trong lịch sử tương tác.
    

Các khả năng này được sử dụng như các tiêu chí đánh giá để đo lường hiệu suất của hệ thống trong việc xử lý và ghi nhớ thông tin trong các tương tác dài hạn. citeturn0search2
# [[2402.16288] PerLTQA: A Personal Long-Term Memory Dataset for Memory Classification, Retrieval, and Synthesis in Question Answering](https://arxiv.org/abs/2402.16288?utm_source=chatgpt.com)
Long-term memory plays a critical role in personal interaction, considering long-term memory can better leverage world knowledge, historical information, and preferences in dialogues. Our research introduces PerLTQA, an innovative QA dataset that combines semantic and episodic memories, including world knowledge, profiles, social relationships, events, and dialogues. This dataset is collected to investigate the use of personalized memories, focusing on social interactions and events in the QA task. PerLTQA features two types of memory and a comprehensive benchmark of 8,593 questions for 30 characters, facilitating the exploration and application of personalized memories in Large Language Models (LLMs). Based on PerLTQA, we propose a novel framework for memory integration and generation, consisting of three main components: Memory Classification, Memory Retrieval, and Memory Synthesis. We evaluate this framework using five LLMs and three retrievers. Experimental results demonstrate that BERT-based classification models significantly outperform LLMs such as ChatGLM3 and ChatGPT in the memory classification task. Furthermore, our study highlights the importance of effective memory integration in the QA task.

Bộ nhớ dài hạn đóng một vai trò quan trọng trong tương tác cá nhân, xem xét bộ nhớ dài hạn có thể tận dụng kiến ​​thức thế giới, thông tin lịch sử và sở thích trong các cuộc đối thoại tốt hơn. Nghiên cứu của chúng tôi giới thiệu Perltqa, một bộ dữ liệu QA sáng tạo kết hợp các ký ức ngữ nghĩa và tình tiết, bao gồm kiến ​​thức thế giới, hồ sơ, mối quan hệ xã hội, sự kiện và đối thoại. Bộ dữ liệu này được thu thập để điều tra việc sử dụng các ký ức được cá nhân hóa, tập trung vào các tương tác và sự kiện xã hội trong nhiệm vụ QA. Perltqa có hai loại bộ nhớ và điểm chuẩn toàn diện là 8,593 câu hỏi cho 30 ký tự, tạo điều kiện cho việc thăm dò và áp dụng các ký ức được cá nhân hóa trong các mô hình ngôn ngữ lớn (LLM). Dựa trên Perltqa, chúng tôi đề xuất một khung mới để tích hợp và tạo bộ nhớ, bao gồm ba thành phần chính: phân loại bộ nhớ, truy xuất bộ nhớ và tổng hợp bộ nhớ. Chúng tôi đánh giá khung này bằng năm LLM và ba người nhận lại. Kết quả thử nghiệm chứng minh rằng các mô hình phân loại dựa trên BERT vượt trội so với các LLM như chatglm3 và chatgpt trong tác vụ phân loại bộ nhớ. Hơn nữa, nghiên cứu của chúng tôi nhấn mạnh tầm quan trọng của việc tích hợp bộ nhớ hiệu quả trong nhiệm vụ QA.