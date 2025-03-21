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
```
Theo tôi hiểu là bạn sử dụng chiến lược Indexing Key - Value trong đó key = embedidng + từ khóa Value = toàn bộ text lúc search là hybrid search đúng chứ
```


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