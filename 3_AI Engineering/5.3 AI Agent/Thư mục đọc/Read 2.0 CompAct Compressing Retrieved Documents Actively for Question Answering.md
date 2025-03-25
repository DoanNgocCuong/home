
Dưới đây là tóm tắt bài báo “COMPACT: Compressing Retrieved Documents Actively for Question Answering.” Bài báo đề xuất **một framework mới** (gọi là COMPACT) nhằm **tóm gọn (compress)** những tài liệu (documents) mà hệ thống truy xuất được, sao cho vẫn giữ được các thông tin thiết yếu để trả lời câu hỏi, đồng thời cắt bớt những đoạn dư thừa. Kỹ thuật này **đặc biệt hữu ích** trong bối cảnh QA nhiều tài liệu (multi-document QA), nhất là khi văn bản gốc quá dài và mô hình ngôn ngữ phải xử lý rất nhiều token.

---

## 1. Bối cảnh và động lực

- Trong bài toán **retrieval-augmented generation (RAG)**, mô hình ngôn ngữ lớn (LLM) cần tham chiếu những tài liệu bên ngoài để nâng cao tính chính xác. Tuy nhiên, nếu đưa vào quá nhiều tài liệu (dẫn đến một ngữ cảnh rất dài) thì mô hình gặp khó khi phải xử lý “tràn ngữ cảnh,” dễ lẫn hoặc “quá tải” (hallucination).
- **Mục tiêu**: Cần cơ chế **“context compression”** – lọc và tóm lược những phần quan trọng liên quan đến câu hỏi, giảm token input, tiết kiệm chi phí tính toán, nhưng vẫn giữ được đủ dữ kiện để trả lời.
- Vấn đề là nhiều phương pháp tóm gọn trước đây (query-focused summarization, extractive approaches, v.v.) vẫn dễ rơi vào tình trạng bỏ sót thông tin quan trọng, nhất là khi phải tổng hợp từ **nhiều document** (multi-hop QA).

---

## 2. Phương pháp COMPACT

### 2.1 Active Compression

COMPACT chia các tài liệu dài thành **nhiều đoạn nhỏ** (segment). Sau đó thực hiện quy trình **“nén” theo vòng lặp**:

1. Nối **đoạn tóm gọn đã có (compressed text)** từ vòng trước với **1 segment mới**.
2. Dựa trên câu hỏi (question), mô hình “tóm gọn” phần cốt lõi của cả hai (đoạn đã tóm + segment mới).
3. Cuối cùng, mô hình quyết định **[COMPLETE] hay [INCOMPLETE]**:
    - Nếu **[INCOMPLETE]** (chưa đủ thông tin), tiếp tục lấy segment kế tiếp.
    - Nếu **[COMPLETE]** (đã đủ dữ liệu để trả lời), dừng lại.

Cách tiếp cận này cho phép mô hình dần dần “mở rộng” tóm gọn khi cần thêm thông tin, và **ngắt** khi đã đủ. Đây gọi là **“early termination”**.

### 2.2 Early Termination

COMPACT **không** nhất thiết phải duyệt qua hết tất cả tài liệu. Nếu mô hình xác định đã đủ “bằng chứng” để trả lời, nó dừng luôn, tránh bị nhiễu. Điều này có lợi:

- Tiết kiệm tính toán (không nén vòng lặp thừa).
- Đảm bảo “bối cảnh gọn” (nên mô hình đọc sẽ tập trung hơn).
- Tự động thích ứng với mức độ phức tạp của câu hỏi: câu đơn giản – dừng sớm, câu cần nhiều “hop” – tóm gọn nhiều hơn.

### 2.3 Huấn luyện (Dataset Construction)

Để dạy mô hình biết cách nén và xác định lúc nào “đủ,” tác giả dùng GPT-4o hướng dẫn (giống kiểu “teacher model”) trên dữ liệu HotpotQA:

1. **Chọn câu** (thuộc top-k document).
2. **Tóm tắt** các câu liên quan cho câu hỏi (không suy luận ra đáp án).
3. **Đánh giá** (evaluation): ghi `[COMPLETE]` nếu tóm tắt đã đủ nội dung trả lời, ngược lại `[INCOMPLETE]`.

Dựa vào đó, thu được bộ dữ liệu huấn luyện (gồm những instance có nhãn “đã đủ/thiếu” kèm tóm tắt cốt lõi) để fine-tune mô hình Mistral-7B Instruct.

---

## 3. Kết quả thực nghiệm

### 3.1 So sánh với nhiều baseline

- **So với “Raw Document”** (đưa thẳng tất cả top-k document vào LLM): COMPACT giảm đáng kể số token (tăng “compression rate” lên đến **47–50x**), đồng thời **thường trả lời tốt hơn** (đặc biệt ở multi-hop QA).
- **So với nhiều phương pháp tóm gọn trước** (RECOMP, LongLLMLingua, AutoCompressors…): COMPACT **vượt trội** về cả độ chính xác (F1, EM) và tỷ lệ nén.
- **So với LLM có “long context”** (InternLM, Llama-3.1 8B/128k, GPT-3.5 Turbo…): COMPACT vẫn thường cho kết quả tốt hơn hoặc tương đương, nhưng với số token ít hơn nhiều.

### 3.2 Mô-đun cắm (Plug-in) linh hoạt

- COMPACT có thể cắm **sau** nhiều loại retriever (BM25, Contriever…) và **trước** nhiều loại reader LLM (GPT-3.5, Llama2-13B, v.v.).
- Khi retriever lấy thêm top-30, top-40 (tức nhiều document), COMPACT vẫn giữ performance ổn định, không “chìm” do nhiễu.

### 3.3 Tối ưu chi phí (API cost)

- Thí nghiệm với GPT-3.5, GPT-4, Claude… cho thấy nếu ta đưa raw document (dài, 3000+ tokens) vào thì chi phí API cao. Dùng COMPACT thì token ngắn hơn (thường dưới 200 token), chi phí inference thấp hơn nhiều, lại tăng độ chính xác.

---

## 4. Kết luận

Bài báo **giới thiệu COMPACT**, một framework “active compression” mới cho RAG:

- **Ưu điểm**:
    
    1. Cho phép “nén” bối cảnh thành dạng ngắn nhất có thể nhưng vẫn “gom đủ manh mối.”
    2. Khả năng “early termination” – dừng vòng lặp tóm gọn khi đủ dữ liệu trả lời.
    3. Hoạt động tốt trong bài toán multi-hop QA phức tạp, tiết kiệm chi phí token và cải thiện chính xác so với baseline.
    4. Dễ “plug and play” cùng nhiều retriever và reader khác nhau.
- **Hạn chế**:
    
    1. Một số trường hợp phức tạp yêu cầu nhiều vòng lặp => thời gian inference lâu hơn.
    2. Còn phụ thuộc “chất lượng” dữ liệu huấn luyện (GPT-4o có thể sai khi gán nhãn COMPLETE/INCOMPLETE).

Dù vậy, **COMPACT** mở ra hướng triển vọng về “tóm gọn tài liệu” cho QA/LLM, giúp mô hình tập trung hơn vào những đoạn thiết yếu và vượt qua giới hạn ngữ cảnh dài.