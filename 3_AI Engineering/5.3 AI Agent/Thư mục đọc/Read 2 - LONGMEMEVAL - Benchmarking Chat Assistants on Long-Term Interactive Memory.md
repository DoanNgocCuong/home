Dưới đây là tóm tắt nội dung bài báo “LONGMEMEVAL: Benchmarking Chat Assistants on Long-Term Interactive Memory.” Bài báo tập trung đề xuất một bộ dữ liệu và phương pháp đánh giá nhằm kiểm tra khả năng “ghi nhớ dài hạn” của các trợ lý hội thoại (chat assistant) dựa trên mô hình ngôn ngữ lớn (LLM).

---

## 1. Động lực và bối cảnh

- **Vấn đề**: Các LLM ngày càng mạnh, hỗ trợ nhiều tác vụ hội thoại. Tuy nhiên, khi cần “cá nhân hoá” câu trả lời hoặc cần “ghi nhớ” nhiều phiên trò chuyện dài hạn với người dùng (vd: thông tin cá nhân, lịch sử hoạt động), các mô hình thường gặp khó khăn.
- **Khoảng trống**: Đã có một số nghiên cứu về RAG (Retrieval-Augmented Generation) hay memory-augmented chatbots, nhưng hầu hết đánh giá trên các bộ dữ liệu tương đối ngắn hoặc thiên về đối thoại người–người (thay vì người–máy). Chưa có tiêu chuẩn đánh giá toàn diện cho các năng lực “bộ nhớ dài hạn” trên kịch bản tương tác nhiều phiên thực tế.

---

## 2. Giới thiệu **LONGMEMEVAL**

**LONGMEMEVAL** là một bộ dữ liệu (benchmark) kiểm tra 5 khả năng cốt lõi của bộ nhớ dài hạn trong hệ thống trợ lý hội thoại:

1. **Information Extraction (IE)**: Trích xuất và “nhớ” lại chính xác các thông tin cụ thể xuất hiện rải rác trong hội thoại.
2. **Multi-Session Reasoning (MR)**: Tổng hợp thông tin từ nhiều phiên trò chuyện để trả lời câu hỏi phức tạp.
3. **Temporal Reasoning (TR)**: Suy luận về mặt thời gian, bao gồm thời điểm, thứ tự sự kiện.
4. **Knowledge Updates (KU)**: Nhận biết và cập nhật thông tin mới khi người dùng thay đổi dữ liệu cá nhân.
5. **Abstention (ABS)**: Từ chối trả lời khi thông tin không có sẵn trong lịch sử (hỏi về dữ liệu “chưa từng nhắc đến”).

### Cách xây dựng bộ dữ liệu

- Mỗi **câu hỏi (question)** kèm **phần trả lời chuẩn (golden answer)** được “giấu” trong một lịch sử hội thoại (hay “haystack”) rất dài (có thể tới 115 nghìn token trong **LONGMEMEVAL** phiên bản “S” hoặc 1.5 triệu token trong phiên bản “M”).
- Các **evidence sessions** (những đoạn hội thoại chứa dữ liệu then chốt) được chèn xen kẽ cùng nhiều đoạn hội thoại khác (vô thưởng vô phạt) để mô phỏng bối cảnh “needle in a haystack”.
- Các đoạn hội thoại được tạo ra nhờ cách kết hợp dữ liệu thực (chẳng hạn ShareGPT, UltraChat) và các đoạn tự mô phỏng (self-chat) giữa hai mô hình LLM (đã được human kiểm duyệt).
- Mỗi **câu hỏi** có thể yêu cầu nhớ thông tin từ 1 đến 6 session khác nhau trong lịch sử, có thể có thêm yếu tố thời gian (timestamp).

### Thống kê và độ khó

- Trung bình khoảng **115 nghìn tokens** (LONGMEMEVAL-S) hoặc **500 session ~ 1.5 triệu tokens** (LONGMEMEVAL-M) cho mỗi bài test.
- Bộ dữ liệu gồm 500 “bài test” (mỗi bài là một câu hỏi). Các câu hỏi đa dạng về loại (7 loại chính, tương ứng 5 năng lực cốt lõi).
- Thử nghiệm ban đầu cho thấy các mô hình lớn (ví dụ GPT-4, Llama 3.1) vẫn suy giảm độ chính xác đáng kể (từ 30%–60%) khi phải “đọc” toàn bộ lịch sử. Các dịch vụ thương mại (ChatGPT, Coze) cũng gặp khó.

---

## 3. Khung đánh giá và kết quả thí điểm

### 3.1 Thử nghiệm trên các hệ thống thương mại

- Tác giả tiến hành chat “từng bước” (session-by-session) với ChatGPT và Coze, rồi đặt câu hỏi cuối cùng. Kết quả:
    - **ChatGPT** (GPT-4o) và **Coze** (GPT-4o, GPT-3.5) đều bị giảm độ chính xác so với việc chỉ đơn giản “đọc offline” toàn bộ lịch sử một lần.
    - Dường như khi số session tăng, hai hệ thống có xu hướng ghi đè/làm mất mát thông tin cũ.

### 3.2 Thử nghiệm trên LLM có “long context” (đọc offline toàn bộ)

- Thử nghiệm GPT-4o, Llama 3.1 (8B & 70B) cùng mô hình Phi-3 Medium (128k context) trên **LONGMEMEVAL-S** (~115k tokens).
- Kết quả: khi so với “oracle” (chỉ đưa đúng những đoạn cần thiết), tỉ lệ trả lời đúng giảm mạnh (30%–60%).
- Cho thấy: kể cả LLM với ngữ cảnh dài thì vẫn cần cơ chế memory & retrieval tốt để xử lý lịch sử quá lớn.

---

## 4. Thiết kế giải pháp Memory-Augmented Chatbot

Bài báo đưa ra một **khung tổng quát** gồm 3 giai đoạn và 4 “điểm điều khiển”:

1. **Indexing**: Lưu trữ mỗi phiên (hoặc chia nhỏ hơn) dưới dạng cặp (key, value).
2. **Retrieval**: Tìm kiếm (top-k) các key phù hợp với query.
3. **Reading**: Mô hình LLM đọc và suy luận trên các đoạn (value) truy xuất được.

**4 điểm điều khiển**:

- **CP1 (Value)**: Lựa chọn mức độ chia nhỏ hoặc tóm tắt session (theo round/phiên hay trích xuất facts).
- **CP2 (Key)**: Có thể “mở rộng key” bằng cách gắn thêm summary, keyphrase, facts quan trọng… giúp tăng khả năng tìm kiếm.
- **CP3 (Query)**: Đặc biệt chú ý đến **temporal query** (dùng mốc thời gian) để lọc bớt dữ liệu cũ hoặc không liên quan.
- **CP4 (Reading Strategy)**: Áp dụng dạng prompt “Chain-of-Note” (CoN) hoặc định dạng cấu trúc (JSON) để mô hình trích rút thông tin trước rồi mới kết luận. Phòng ngừa lỗi khi LLM đọc nhiều đoạn dài.

### Một số kết quả thực nghiệm quan trọng

- **(CP1) Decomposition**: Thay vì lưu cả session, chia nhỏ theo “round” (mỗi lượt người dùng) giúp tăng khả năng tìm kiếm. Tuy nhiên, tóm tắt/facts quá nhiều cũng có rủi ro “mất thông tin”.
- **(CP2) Key expansion**: Thêm “facts, keyphrase, summary” vào key có thể tăng Recall@k và NDCG@k, dẫn đến tăng 4–5% độ chính xác cuối cùng.
- **(CP3) Thêm dữ liệu thời gian**: Nếu câu hỏi liên quan thời gian, trích xuất khung thời gian (time range) và lọc value giúp độ chính xác truy xuất tăng 7–11%. Model mạnh như GPT-4o “hiểu” thời gian tốt hơn model nhỏ.
- **(CP4) Reading**: Dù truy xuất đúng, LLM vẫn có thể sai do bối cảnh dài. Dùng “Chain-of-Note” + format JSON làm mô hình phân tách việc trích rút thông tin và lập luận. Cải thiện 5–10% so với prompt thông thường.

---

## 5. Kết luận

Bài báo giới thiệu **LONGMEMEVAL** – một bộ dữ liệu kiểm tra tổng quát nhiều khía cạnh của bộ nhớ dài hạn cho hệ thống hội thoại AI. Tác giả chỉ ra:

- Dữ liệu có quy mô rất lớn (trên 100k tokens / trường hợp), đa dạng loại câu hỏi (7 kiểu), bao quát 5 năng lực quan trọng (IE, MR, TR, KU, ABS).
- Qua thử nghiệm, các mô hình và dịch vụ hàng đầu vẫn gặp khó khi phải duy trì “state” lâu dài; do đó **bắt buộc cần thiết** tích hợp các kỹ thuật indexing–retrieval–reading tinh vi.
- Bài báo đề xuất một “khung thiết kế” (key, value, query, reading strategy) và chứng minh các kỹ thuật như chia nhỏ session, key expansion, xử lý time-aware, và “Chain-of-Note” đều giúp nâng cao độ chính xác.

**LONGMEMEVAL** là bước tiến lớn trong việc đánh giá khả năng “ghi nhớ dài hạn” của trợ lý hội thoại, tạo tiền đề cho các nghiên cứu sâu hơn về tối ưu hóa chi phí, thời gian, hoặc mở rộng sang nhiều dạng dữ liệu phức tạp hơn.


---

## 2.1 Câu hỏi 1: Đào sâu hơn cách làm 

![[Pasted image 20250322054315.png]]


Hình vẽ trong bài mô tả **quy trình “3 giai đoạn” (Indexing – Retrieval – Reading)** của một hệ thống “trợ lý hội thoại có bộ nhớ dài hạn,” đồng thời chỉ ra **4 điểm điều khiển (CP1–CP4)** quan trọng:

1. **(1) Indexing:**
    
    - Toàn bộ lịch sử trò chuyện (hoặc dữ liệu) được phân tách và lưu trữ dưới dạng cặp “Key–Value”.
    - **CP1: Key** là cách biểu diễn (representations) được dùng để tìm kiếm, ví dụ: câu tóm tắt, keyphrase, embedding, v.v.
    - **CP2: Value** là nội dung chính mà hệ thống thực sự cần truy hồi (ví dụ: các “đoạn hội thoại” hay “document chunks”).
    - Ý tưởng: Mỗi “value chunk” có kèm “key” để sau này khi có truy vấn (query), hệ thống dễ lọc và lấy ra đoạn nội dung phù hợp.
2. **(2) Retrieval:**
    
    - Khi người dùng (hoặc hệ thống) đưa ra **query**, ta so sánh query với **key** trong “chỉ mục” (index) để xếp hạng mức độ liên quan.
    - Lấy ra các “Value Chunk” top-k phù hợp nhất.
    - **CP3: Query** bao gồm việc xử lý/làm giàu (query expansion) và quản lý thông tin thời gian (time-aware) sao cho việc tìm kiếm chính xác hơn.
3. **(3) Reading:**
    
    - Các “value chunk” lấy được sẽ được đưa vào mô hình LLM cùng với **câu hỏi** để sinh ra câu trả lời cuối cùng.
    - **CP4: Reading Strategy** đề cập đến cách ta “cho mô hình đọc” những đoạn đã truy xuất. Ví dụ:
        - Prompt chuẩn bị dạng JSON, hoặc
        - Kỹ thuật “Chain-of-Note” (chia bước: đầu tiên mô hình tách rút thông tin cốt lõi, sau đó mới lập luận),
        - v.v.

Nói cách khác, sơ đồ minh hoạ một pipeline kiểu “Retrieval-Augmented Generation” nhưng chia nhỏ rõ ràng thành:

- **Indexing (Key–Value)**: lưu trữ dữ liệu, thiết kế khóa (Key) sao cho dễ tìm,
- **Retrieval (Query)**: so khớp query với Key để tìm Value liên quan,
- **Reading (LLM)**: mô hình đọc giá trị trả về và trả lời.

Bốn “điểm điều khiển” (Control Points CP1–CP4) là những khâu quan trọng mà ta có thể tối ưu để hệ thống trả lời chính xác, nhớ lâu, và xử lý dữ liệu lớn hiệu quả.


Dưới đây là một **ví dụ giả lập** (rút gọn) về cách hệ thống **Indexing – Retrieval – Reading** hoạt động, đồng thời minh họa 4 điểm điều khiển (CP1–CP4) trong thực tế:

---

## Bối cảnh giả định

- Bạn có một trợ lý AI (dựa trên LLM) hỗ trợ theo dõi quá trình tập luyện thể thao của bạn trong nhiều tuần lễ.
- Bạn thường xuyên trò chuyện với trợ lý, cung cấp thông tin số km chạy bộ, thời gian nghỉ, cân nặng, v.v.

### Lịch sử hội thoại

1. **Tuần 1**:
    
    - **User**: “Tuần này tôi chạy 15km. Tôi muốn tăng dần cường độ.”
    - **Assistant**: “Ok, vậy tuần sau hãy thử nâng lên 20km.”
2. **Tuần 2**:
    
    - **User**: “Tôi đã chạy được 18km. Nhưng có vẻ hơi mệt.”
    - **Assistant**: “Có thể bạn cần nghỉ xen kẽ 1 ngày sau mỗi 2 buổi chạy.”
3. **Tuần 3**:
    
    - **User**: “Tôi chạy 21km trong tuần này. Rất tốt!”
    - **Assistant**: “Chúc mừng! Hãy ghi nhật ký lại để xem tuần tiếp theo thế nào.”

… (và còn tiếp)

---

## 1) Indexing

### CP1: Key

- Mỗi phiên/đoạn hội thoại sẽ được “ghi chỉ mục” (index) sao cho khi cần tìm lại thông tin, hệ thống có thể dựa vào **key**.
- **Ví dụ**: Ta lấy **câu User** làm “Value” chính cần lưu, còn **key** có thể là:
    - Embedding (vector) được sinh ra từ toàn bộ nội dung tin nhắn,
    - hoặc một cụm từ tóm tắt như “User chạy 15km tuần 1” (v.v.).

**Giả sử** với Week 1, ta có:

- **Key** = `"tuần 1, chạy bộ, 15km, cường độ"` (có thể kết hợp vector embedding + từ khóa)
- **Value** = `"Tuần này tôi chạy 15km. Tôi muốn tăng dần cường độ."`

### CP2: Value

- “Value” là **nội dung gốc** dùng để phục vụ trả lời. Ở đây, mỗi lượt nói của User là một “value chunk.”
- Có thể chia nhỏ hơn nữa (mỗi câu 1 chunk) hoặc giữ nguyên cả phiên tùy bạn thiết kế.
- Nếu muốn **tóm gọn** (summarize) hoặc trích xuất “fact” để tiết kiệm dung lượng, ta vẫn phải đảm bảo không làm mất thông tin cần thiết.

**Ví dụ**:

- Tuần 2 → **Value** = “Tôi đã chạy được 18km. Nhưng có vẻ hơi mệt.”
- Key có thể mở rộng: `"tuần 2, chạy bộ, 18km, mệt mỏi"`

---

## 2) Retrieval

### CP3: Query

- Khi bạn hỏi: “Tôi đã chạy được bao nhiêu km mỗi tuần, và tuần nào tôi chạy nhiều nhất?”
- Hệ thống sẽ tạo một **truy vấn** (query) dựa trên chính câu hỏi này.
- Trong **temporal query** (liên quan thời gian), nếu model phát hiện từ khóa “mỗi tuần” và “tuần nào chạy nhiều nhất,” nó có thể chỉ tìm các **key** chứa cụm “chạy bộ” + “km” + “tuần #”.

**Quá trình tìm kiếm**:

1. So sánh **query embedding** với các **key** trong cơ sở dữ liệu.
2. Lấy top-k Value chunk liên quan, ví dụ:
    - Week 1 (15km), Week 2 (18km), Week 3 (21km), …

(Chúng ta có thể có thêm bước lọc thời gian, ví dụ: chỉ lấy các tuần <= “tuần hiện tại”)

---

## 3) Reading

### CP4: Reading Strategy

- Bây giờ, hệ thống có được 3 “value chunk” (tuần 1, 2, 3). Nó đưa những chunk này + câu hỏi vào LLM để tổng hợp ra kết quả.
    
- **Ví dụ** “Chain-of-Note” (CoN):
    
    1. **Bước 1**: Mô hình **trích rút** các con số liên quan từ mỗi chunk:
        - Tuần 1: 15km, tuần 2: 18km, tuần 3: 21km.
    2. **Bước 2**: Mô hình **suy luận**: “Tuần 3 có quãng đường dài nhất (21km).”
    3. **Bước 3**: Trả lời người dùng ngắn gọn: “Bạn đã chạy 15km, 18km, 21km… Nhiều nhất là tuần 3.”
- Nếu **không** dùng kỹ thuật này, mô hình có thể “lẫn” thông tin hoặc bỏ sót dữ liệu, đặc biệt khi có nhiều chunk.
    

---

## Tóm tắt:

- **Indexing** (1) & (2):
    - **CP1** (Key): quyết định dạng khóa (embedding, từ khóa, tóm tắt…).
    - **CP2** (Value): quyết định mức “chia nhỏ” dữ liệu (theo vòng hội thoại, theo câu, hay tóm tắt).
- **Retrieval** (3):
    - **CP3** (Query): mở rộng (query expansion), hiểu thời gian, từ khóa… để tìm chính xác.
- **Reading** (4):
    - **CP4** (Reading Strategy): chuỗi prompt hoặc kỹ thuật (Chain-of-Note, JSON format, v.v.) để LLM diễn giải tốt nhiều đoạn.

Qua ví dụ này, ta thấy rõ cách “Key–Value” được lưu và cách “Query–Reading Strategy” can thiệp để tối ưu việc tìm kiếm và tổng hợp thông tin.

---
## 2.2 Câu hỏi thêm 2:  Theo tôi hiểu là bạn sử dụng chiến lược Indexing Key - Value trong đó key = embedidng + từ khóa Value = toàn bộ text lúc search là hybrid search đúng chứ

**Đúng như bạn nói,** trong bài (và cả nhiều hệ thống RAG tương tự), một **cách phổ biến** là lưu trữ “Key” dưới dạng **kết hợp (embedding + từ khoá)**, rồi **Value** là toàn bộ text.

- **Key** thường gồm:
    1. **Embedding** (vector) để phục vụ “semantic search” (tìm kiếm theo ngữ nghĩa).
    2. **Từ khoá** (hoặc tóm tắt, fact...) để phục vụ “keyword / BM25 search” (hoặc hỗn hợp).

Khi hệ thống **tìm kiếm (retrieval)**, nó có thể chạy cả hai cơ chế:

- Tính “độ tương đồng embedding” (cosine similarity, v.v.)
- Tìm theo từ khoá (BM25 hay từ vựng đặc biệt)  
    Sau đó ta có thể **gộp** hai danh sách kết quả (thuật toán rank fusion) hoặc chọn lọc top-k phù hợp. Đó chính là **“hybrid search”**.

Tùy nhu cầu, **cách triển khai** có thể là:

1. **“Key merging”**: Trộn thẳng từ khóa/tóm tắt vào text để tạo **một “key” duy nhất** (có embedding + fulltext).
2. **“Rank merging”**: Lưu song song 2 loại key (embedding key + keyword key), khi cần truy vấn thì trả về 2 list kết quả rồi hợp nhất.

Cả hai chiến lược đều nhằm tăng khả năng tìm được văn bản chính xác (recall) và ưu tiên mức độ liên quan (precision). Nhiều bài thực nghiệm cho thấy cách phối hợp embedding + keyword thường hiệu quả hơn so với chỉ dùng đơn lẻ một trong hai.

--- 
## 2.3 Câu hỏi 3: Trong bài báo có nói dùng cách nào để extract từ khóa không ?

Trong bài báo, phần **Appendix E** (Implementation Details) có mô tả cách tác giả **extract keyphrase** từ mỗi “chunk” (một phiên hội thoại hoặc một lượt nói). Họ dùng một **prompt zero-shot** với mô hình _Llama 3.1 8B Instruct_, có nội dung như sau (được rút gọn):

```
Below is a transcript of a conversation between a human user and an AI assistant. 
Generate a list of keyphrases for the session. Separate each keyphrase with a semicolon. 
Dialogue content: {session}
```

Cụ thể:

1. **Mỗi phiên (hoặc lượt) hội thoại** được đưa vào prompt dưới dạng `Dialogue content`.
2. **Mô hình** Llama 3.1 8B Instruct **trích xuất ra** các **từ khóa nổi bật**, dưới dạng danh sách, ngăn cách bằng dấu chấm phẩy.
3. Những keyphrases này sau đó được nối (concatenate) vào Value hoặc ghép chung dưới dạng “document expansion” để làm Key.

Tóm lại, tác giả không dùng thuật toán keyword extraction truyền thống (như TF-IDF, TextRank, v.v.) mà **chỉ dùng prompt zero-shot** với mô hình ngôn ngữ lớn để trích xuất từ khóa. Kết quả thu được được họ báo cáo trong bảng ở phần phụ lục.


## 2.4 Tức là trích xuất sau khi hội thoại đã kết thúc hả ?

```
Trong bài, họ chạy **quy trình “extract keyphrase”** cho từng khối hội thoại (chunk) **sau khi** khối đó đã sẵn sàng (tức là sau khi người dùng và trợ lý đã kết thúc phiên hoặc ít nhất là kết thúc một lượt nói). Ta có thể coi đây là quá trình “post-hoc extraction”: khi **đoạn text** của một lượt/phiên đã hoàn chỉnh, họ đưa đoạn đó vào prompt để LLM trích xuất từ khóa.

- Về mặt triển khai, bài báo chủ yếu mô tả **quy trình** dưới góc nhìn “offline benchmark”: họ có toàn bộ dữ liệu hội thoại, sau đó chạy lần lượt các bước Indexing – Retrieval – Reading.
- Nếu áp dụng vào hệ thống “online memory”, ta cũng thường **chờ** người dùng nói xong (hay trợ lý trả lời xong) rồi mới trích xuất từ khóa/facts để cập nhật vào bộ nhớ.

Tóm lại, **không** phải họ trích xuất từng câu “ngay lập tức khi người dùng gõ”, mà **đợi** cho đoạn/lượt thoại hoàn tất, sau đó mới đưa vào LLM để sinh keyphrase.
```


![[Pasted image 20250322060614.png]]

Dưới đây là phần giải thích cụ thể cách đọc **Bảng 2** (Retrieval và End-to-End QA) trong bài báo, cũng như ý nghĩa từng cột:

---

## 1. Các cột về **Retrieval**

- **Metrics@5** và **Metrics@10**: Tác giả báo cáo hai chỉ số:
    - **Recall**@k: Tỉ lệ mà top-k kết quả trả về (từ bước tìm kiếm) có chứa **đoạn/bản ghi** thực sự cần để trả lời (các “evidence” quan trọng).
    - **NDCG**@k: Thước đo đánh giá mức độ xếp hạng (nếu “evidence” càng được xếp hạng cao, thì NDCG càng tốt).
- Bên trái cùng bảng là phần “Key Design” (cách tạo Key trong Indexing) và “Value = Round/Session” (cách chia “Value chunk”).

**Ví dụ**:

- Khi thấy “K = V + fact” có Recall@5 = 0.644 (với **Value = Round**), có nghĩa là nếu ta **key = [Value + facts rút ra]**, thì khi truy vấn, có 64.4% trường hợp hệ thống tìm thấy đúng “chunk” liên quan trong top 5 kết quả.

---

## 2. Các cột về **End-to-End QA**

Sau khi truy xuất (Retrieval), các top-k “chunk” được đưa vào LLM để trả lời. Bảng hiển thị **độ chính xác cuối** (QA accuracy) theo 2 mức k:

- **Top-5**: Chỉ lấy 5 đoạn được xếp hạng cao nhất đưa vào LLM
- **Top-10**: Lấy 10 đoạn.  
    Mục đích là so sánh xem đưa thêm chunk (top-10) có cải thiện câu trả lời so với chỉ top-5 hay không.

Ba cột “GPT-4o,” “L3.1 70B,” “L3.1 8B” chính là ba “độc giả” (reader LLM) khác nhau. Mỗi LLM sẽ có khả năng tổng hợp thông tin từ top-k chunk tốt hay kém, dẫn đến kết quả QA khác nhau.

---

## 3. Ý nghĩa từng “Key Design”

- **K = V**: Key trùng với Value. Tức là không tách bạch, dùng luôn toàn bộ nội dung text để làm khóa tìm kiếm.
- **K = summary, K = fact, K = keyphrase**: Key là phần tóm tắt, facts hay keywords rút gọn (không kèm đoạn gốc).
- **K = V + summary / V + fact / V + keyphrase**: Kết hợp cả đoạn gốc (Value) và phần tóm tắt/fact/keyword rút ra để mở rộng nội dung Key (document expansion).

---

## 4. Các hàng “Value = Round” và “Value = Session”

- **Value = Round**: Mỗi lượt nói của người dùng (hoặc mỗi câu) được cắt thành một “chunk” riêng.
- **Value = Session**: Dùng cả phiên hội thoại (gồm nhiều lượt nói) làm một chunk “Value”.

Cột “Value = Round” thường có nhiều chunk hơn (nhưng ngắn), còn “Value = Session” có số chunk ít hơn (nhưng dài).

---

## 5. Rút gọn các nhận xét

1. **Retrieval**:
    
    - Thường thấy “K = V + fact” (bôi đậm trong bảng) có Recall và NDCG cao hơn đáng kể so với K = V đơn thuần. Điều này chứng tỏ việc “document expansion” với facts (hoặc tóm tắt) làm Key giúp việc tìm kiếm chính xác hơn.
2. **End-to-End QA**:
    
    - Tương tự, “K = V + fact” có accuracy cao nhất ở hầu hết các cột (so với K = summary/keyphrase riêng lẻ).
    - Việc so sánh “Top-5” và “Top-10” giúp ta thấy mô hình GPT-4o, Llama-3.1 70B, 8B thay đổi hiệu quả ra sao khi bơm thêm chunk. Ví dụ GPT-4o thường tăng từ ~0.65 lên ~0.70 nếu lấy Top-10 thay vì Top-5.
3. **Value = Round** vs. **Value = Session**:
    
    - Nhìn chung, “Value = Round” có recall thấp hơn do độ ngắn (có nhiều chunk nhỏ, khó match), nhưng đôi khi “Value = Round” hỗ trợ mô hình QA trả lời chính xác hơn vì chunk gọn, mô hình ít bị loãng thông tin.
    - “Value = Session” thì retrieval recall có thể cao hơn (vì chunk to, dễ dính key), nhưng khi vào QA, có thể mô hình bị “khó tóm gọn” nên kết quả cuối có thể khác nhau.

---

### Kết luận chính từ bảng

- **Document expansion** (K = V + fact) **cải thiện cả retrieval** (Recall/NDCG) **lẫn kết quả QA**.
- Nếu chia **Value** thành từng **round** nhỏ thì có thể tốt cho giai đoạn tổng hợp, nhưng đòi hỏi key design cẩn thận (vì chunk nhỏ, retrieval cũng khó).
- Việc chọn top-5 hay top-10 chunk khi đưa vào LLM cũng ảnh hưởng đáng kể đến hiệu suất cuối, và mô hình LLM mạnh như GPT-4o thường tận dụng tốt hơn top-10 so với model nhỏ.

Như vậy, Bảng 2 minh họa chi tiết **các tổ hợp “Key Design” (K) và “Value Granularity”** sẽ ảnh hưởng thế nào đến cả hiệu năng truy xuất (retrieval) lẫn chất lượng trả lời cuối (end-to-end QA).


**Đúng vậy**, trong phương án **Key = V + fact** thì ta tạo **một chuỗi “Key”** bằng cách **ghép** (concatenate) phần **nội dung gốc (Value)** với các câu “fact” rút ra, rồi **mang cả chuỗi đó đi nhúng (embedding)** và lưu vào cơ sở dữ liệu để truy xuất.

Nói cách khác:

1. **Value**: nội dung gốc của đoạn (có thể là nguyên phiên hoặc chỉ một lượt).
2. **Fact**: các câu thông tin cốt lõi trích xuất (ví dụ, tóm tắt “người dùng vừa mua xe, tuần này chạy 15km,…”).
3. **Ghép (Value + fact)** thành một đoạn text duy nhất, rồi đưa text này qua mô hình embedding (VD: BERT, Stella V5, Contriever...).
4. **Lưu embedding** đó làm “Key” trong chỉ mục. Khi truy vấn, ta sẽ so sánh query embedding với embedding của “Key = (Value + fact)”.

Cách làm này giúp hệ thống tìm kiếm “match” tốt hơn, vì từ khoá cốt lõi (fact) cũng nằm trong chính “Key”, đồng thời vẫn giữ bối cảnh gốc (Value). Ta có thể coi đó là **một dạng “document expansion”** – thêm thông tin tóm lược, facts, keyphrase… vào văn bản gốc trước khi nhúng để tăng độ chính xác truy xuất.

---
## 2.6 Phân biệt fact với 2 cái summary và keyphrase?

Trong bài, tác giả thử nghiệm ba kiểu “thông tin rút gọn” (ngoài **Value** gốc) để tạo “Key”:

1. **Summary**
    
    - Là đoạn **tóm tắt** nội dung chính của phiên/đoạn hội thoại, thường được trình bày dưới dạng **vài câu văn hoàn chỉnh**, nêu ý chung, bối cảnh chung.
    - Ví dụ: “Người dùng thảo luận về việc chạy bộ 15km, muốn tăng cường độ trong tuần tới, cảm thấy hơi mệt, v.v.”
2. **Keyphrase**
    
    - Là một danh sách **từ khoá hoặc cụm từ ngắn** tách rời nhau (thường phân tách bằng dấu `;`).
    - Ví dụ: `chạy bộ; 15km; tăng cường độ; mệt mỏi`.
    - Thường súc tích hơn summary, chỉ tập trung vào keyword cốt lõi để phục vụ tìm kiếm “theo từ khoá”.
3. **Fact**
    
    - Thay vì viết tóm tắt “chung chung,” “fact” là các **phát biểu dạng câu đơn, nêu rõ sự kiện/thông tin cụ thể** về người dùng.
    - Ví dụ: “Người dùng đã chạy 15km.” “Người dùng cảm thấy mệt.”
    - Thường ở dạng câu ngắn, liệt kê thông tin dưới dạng “user facts” (đặc biệt cho bài toán cá nhân hoá: sở thích, thói quen, kết quả tập luyện, v.v.).

**Tóm lại**, cả **summary** và **fact** đều có thể coi là “đoạn tóm lược;” nhưng:

- **Summary**: viết thành **đoạn văn mô tả** tổng quan, có độ bao quát cao.
- **Fact**: chia nhỏ thành **nhiều câu đơn** (mỗi câu là một sự thật riêng).
- **Keyphrase**: chỉ là **cụm từ khóa** chứ không viết thành câu hoàn chỉnh.

Tuỳ mức độ “chi tiết” và “định dạng” mong muốn, ta chọn cách rút gọn khác nhau để **hỗ trợ truy xuất**. Kết quả thực nghiệm cho thấy “fact” thường hiệu quả hơn **summary** và **keyphrase** (theo bảng kết quả), vì nó vừa đủ cụ thể lại vẫn tách gọn thông tin quan trọng.


---
![[Pasted image 20250322063052.png]]

---
## 2.7 Sự khác nhau giữa fact và summary 

Dưới đây là **một ví dụ ngắn** minh họa sự khác nhau giữa **fact** (các dữ kiện rời) và **summary** (một đoạn tóm tắt) khi trích xuất nội dung:

---

### Đoạn hội thoại gốc

> **User**: “Tôi vừa chuyển từ iPhone 13 sang điện thoại Android, cụ thể là **Samsung Galaxy S23**. Tôi dùng iPhone 13 khoảng **1 năm** rồi, giờ đổi qua S23 thấy **camera đẹp** hơn hẳn.”

---

### **1) Facts**

Facts thường được biểu diễn dưới dạng **các câu thông tin rời rạc, ngắn gọn**, mỗi fact nêu một điểm quan trọng:

1. “Người dùng **đã dùng iPhone 13** trong 1 năm.”
2. “Người dùng **chuyển sang sử dụng Samsung Galaxy S23** (Android).”
3. “Người dùng **thấy camera Samsung S23 đẹp hơn**.”

**Đặc trưng**:

- Từng dòng fact là một **thực thể quan hệ** (VD: “User – chuyển sang – Galaxy S23”).
- Không có câu nối; tránh diễn giải, cảm xúc.
- Lượng thông tin tối thiểu, dễ “match” khi tìm kiếm.

---

### **2) Summary**

Phần tóm tắt (summary) thường là **một đoạn văn** mô tả chung những điểm chính trong hội thoại:

> “Người dùng cho biết họ đã **sử dụng iPhone 13** khoảng 1 năm trước khi **chuyển sang điện thoại Android**. Họ hiện dùng **Samsung Galaxy S23** và cảm thấy hài lòng, đặc biệt với **chất lượng camera** được đánh giá cao hơn so với iPhone 13.”

**Đặc trưng**:

- Viết thành **đoạn văn liên tục**, tương đối mạch lạc.
- Có thể lồng ghép các **mối quan hệ**, bối cảnh, và cả đánh giá (cảm xúc).
- Thích hợp cho việc **tóm gọn** nhiều ý, giúp mô hình đọc dễ hơn, nhưng có thể **lược bớt chi tiết**.

---

### **Tổng quan so sánh**

- **Fact**:
    
    - Tách riêng từng ý **cụ thể** (rút gọn, khách quan).
    - Hữu ích khi cần lưu trữ/tra cứu chính xác hoặc “lập chỉ mục” (index) theo từng quan hệ (VD: “A sở hữu B,” “A sử dụng C,”...).
- **Summary**:
    
    - Đoạn tóm lược **bao quát** nội dung, có tính mạch lạc.
    - Hữu ích cho **người đọc** hoặc LLM ở bước “đọc/hiểu” (reading), nhưng có thể **bỏ sót các chi tiết nhỏ** mà fact ghi lại.

```
1. Thay vì chỉ có: K = V + fact/V+ summary/V+keyphrase thì ta dùng cả K = V+fact+summary +keyphrase và sử dụng các method tốt hơn nữa để summary ???

**Áp dụng “hierarchical indexing”**:

- Thay vì key = “(V + fact + summary + keyphrase)” dạng phẳng, ta tách thành 2 tầng:
    - Tầng 1: Từ khoá/summaries tổng quát (để khoanh vùng).
    - Tầng 2: Chuẩn hoá fact/câu gốc (để lấy chính xác).
- Đọc RAG theo hai pha, giảm thời gian “cày” trên hàng chục nghìn “chunk.”

2. fine tuning model, sử dụng các history để fine tuning model làm tăng khả năng extract, 1 model LMa 3 - 3B thay vì llama3.1 8B của tác giả ...

3. ...
```

Giống cái a Huy 
```
- Raptor Chunk 
- LLMs Chunk 
-> a Huy kết hợp cả 2 
```

## 2.8 Đọc kỹ lại K = value + fact của họ 

Câu hỏi của bạn là về phần:

> **"K = V + fact" – quy trình này được thực hiện như nào trong toàn bộ pipeline? Có phải là V + fact được mang đi embedding không?**

## ✅ Tóm tắt ngắn gọn

**Có, đúng là `V + fact` được mang đi embedding** trong quá trình indexing — đây là kỹ thuật gọi là **Key Expansion (mở rộng khóa)** bằng cách **nối (`concat`) thông tin quan trọng như facts vào chính `value`** và dùng toàn bộ chuỗi đó như **key** trong cặp key-value. Điều này giúp tăng khả năng truy xuất đúng (retrieval) và cải thiện độ chính xác của trả lời câu hỏi.

---

## 🔍 Chi tiết quy trình K = V + fact

### 1. **Giải thích các khái niệm**

- `V`: Giá trị lưu trong memory (ví dụ: một đoạn hội thoại, một vòng chat, hoặc bản tóm tắt).
- `fact`: Những thông tin cá nhân được trích xuất từ `V` như sở thích, trải nghiệm, con số cụ thể, v.v.
- `K = V + fact`: Là **Key mở rộng**, được tạo ra bằng cách nối `fact` vào `value` rồi mang toàn bộ đi **embedding** để tạo thành key.

---

### 2. **Trong pipeline của hệ thống memory-augmented chat assistant**

Theo mô hình được mô tả trong Figure 3 (trang 4 của bài), pipeline có 3 bước chính:

#### **(1) Indexing:**

- Mỗi session được chia nhỏ (tốt nhất là theo từng vòng `round`).
- Từ mỗi vòng, ta tạo ra:
    - `value` (V): thường là đoạn hội thoại người dùng.
    - `fact`: trích xuất các thông tin có cấu trúc (user facts).
- **Sau đó, `key = V + fact`**: nối lại rồi nhúng embedding → lưu vào bộ nhớ key-value.

📌 **Việc này giúp "gợi ý" cho retriever biết cái gì quan trọng trong `V`.**

---

#### **(2) Retrieval:**

- Khi người dùng hỏi một câu (`query`), nó được nhúng thành embedding.
- Hệ thống tìm top-k `key` gần nhất trong vector space, lấy `value` tương ứng.

> 🧠 Việc mở rộng `K = V + fact` giúp tăng Recall@k và QA accuracy như được chứng minh trong Table 6 và Table 7.

---

#### **(3) Reading:**

- Các `value` được truy xuất sẽ được model đọc lại để suy luận và trả lời.
- Thường kết hợp với kỹ thuật như **Chain-of-Note** hoặc **JSON format** để tăng độ chính xác.

---

## 🧪 Kết quả thực nghiệm

Trong các bảng kết quả (như Table 6 trang 17):

- `K = V + fact` vượt trội hơn `K = V` hoặc `K = fact` về cả **retrieval** và **QA accuracy**.
- Đặc biệt hiệu quả khi dùng với value granularity = session hoặc round.

---

## ✅ Kết luận

- ✅ **`K = V + fact` được embedding trong indexing stage.**
- ✅ Cách này giúp retriever tìm chính xác hơn nhờ có thêm thông tin định hướng.
- ✅ Thích hợp với cả long context LLMs và memory-augmented agents.

Nếu bạn muốn mình vẽ sơ đồ minh hoạ pipeline "K = V + fact" hay viết lại đoạn code giả lập, mình cũng làm được luôn nhé.


```
Có 1 ý tưởng nữa là dùng method: LLMs + Raptor =>

Đề xuất cải thiện:

1. Method cũ: Đem từng Round / Session đi Prompt để extract Summary/Fact/Keyphrase thì gặp vấn đề ngắn quá hoặc dài quá => Đề xuất: Chunking cho Session và prompt để lấy fact:

Chunking thì có nhiều method. Kỳ trước a Huy là chunking cho câu hỏi dạng QA. Của mình sẽ cải thiện hội thoại bằng Chunking trong Conversation.

1.1 Chunking theo LLMs chunk
1.2 Raptor Chunking: Chunk r

- Các Session được sử dụng phương pháp: LLMs Chunking + Raptor Chunking => Flat ra để thành các Embedding.

1.1 Raptor flat: Tức là đem cả Chunk ban đầu + LLMs Chunking + Summary Chunk đi Flat trải rộng ra và Rerank

1.2 Hierarchical Indexing - luồng 2 pha:

- Pha 1 (Coarse Retrieval):

Tạo embedding cho “summary” (hoặc keyphrase) của từng chunk.

Query → so sánh & lấy top-K chunk theo summary.

- Pha 2 (Fine Retrieval):

Với K chunk ở trên, ta đi sâu vào “fine index” (có facts/câu gốc).

- Lấy top-K’ final.

Reading: Đưa top-K’ này vào LLM để sinh câu trả lời.

2. Phương pháp cũ chỉ đề xuất đến việc: K=V+summary / K=V+fact / K=V+keyphrase

=> Đề xuất: Mỗi loại key có thế mạnh riêng (VD: summary giỏi match ý tổng quát, keyphrase giỏi match keyword cụ thể...). Ta embedding toàn bộ: V+summary, V+fact, V+keyphrase kèm với top K.
```