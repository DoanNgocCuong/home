- https://neurips2023-enlsp.github.io/papers/paper_38.pdf
Tuyệt vời Quốc ơi! Dưới đây là phần **Baseline mô hình RAG đơn giản** được tóm tắt và viết lại từ bài báo _"Retrieval-Augmented Generation for Dialog Modeling"_ (NeurIPS 2023), rất phù hợp để bạn sử dụng làm **baseline nghiên cứu** cho đồ án **Ứng dụng RAG vào bộ nhớ dài hạn**:

---

## 🧱 **Baseline: RAG không cần fine-tune cho mô hình hội thoại dài hạn**

### 🎯 Mục tiêu:

Giải quyết bài toán **ghi nhớ và hiểu ngữ cảnh hội thoại dài hạn** mà **không cần fine-tune LLM**, bằng cách tận dụng khả năng học trong ngữ cảnh (In-Context Learning - ICL) của LLM và cơ chế truy xuất linh hoạt (Retrieval-Augmented Generation – RAG).

---

### ⚙️ Cấu trúc hệ thống baseline:

#### 1. **Input**:

- Hội thoại nhiều phiên `H = {Session_1, Session_2, ..., Session_n}`
    
- Mỗi phiên có nhiều lượt nói giữa user và agent.
    

#### 2. **Truy xuất ngữ cảnh (Retrieval-based context selection)**:

Có 2 phương pháp đơn giản:

✅ **(a) kNN Semantic Retrieval**:

- Lưu embedding của các lượt hội thoại cũ (qua PaLM hoặc SentenceTransformer).
    
- Sử dụng đoạn hội thoại hiện tại làm truy vấn, tìm k đoạn trước đó gần nhất về ngữ nghĩa.
    

✅ **(b) Submodular Span Summarization (S3)**:

- Tóm tắt hội thoại cũ theo hướng **tập trung vào truy vấn (query-focused)**.
    
- Áp dụng hàm con `f()` để tối ưu vừa tính liên quan vừa tính đa dạng (relevance + diversity).
    

#### 3. **Kết hợp ngữ cảnh**:

- Sau khi truy xuất hoặc tóm tắt, ta **ghép phần truy xuất + prompt hướng dẫn + hội thoại mới nhất** thành đầu vào cho LLM:
    

```plaintext
[Instruction Prompt] +
[Retrieved Summary or Dialogs] +
[Current Dialog Turn]
→ LLM sinh phản hồi
```

#### 4. **Không cần fine-tune**:

- Mô hình LLM chỉ sử dụng ở chế độ inference (ví dụ: GPT-3.5, PaLM-1B/24B/340B).
    
- Tối ưu bằng cách chỉ đưa các đoạn cần thiết vào context → tiết kiệm token, tăng tốc độ.
    

---

### 📊 Dataset & Kết quả thực nghiệm:

#### 📌 Dataset sử dụng:

- **Multi-Session Chat (MSC)**: hội thoại nhiều phiên giữa người và người, cần ghi nhớ persona.
    
- **MultiDoc2Dial**: cần truy xuất từ nhiều tài liệu, phản hồi theo thông tin tri thức.
    

#### 📈 Hiệu quả:

- Phương pháp RAG đơn giản (kNN hoặc tóm tắt truy vấn) **đánh bại cả summary “vàng” do con người viết** trên nhiều chỉ số như BLEURT, ROUGE-L, METEOR.
    
- Giảm độ trễ và token load so với việc nhét toàn bộ history vào prompt.
    

---

### 🧠 Ưu điểm của baseline này:

|Ưu điểm|Mô tả|
|---|---|
|**Dễ triển khai**|Không cần fine-tune, chỉ cần mô hình LLM + retriever embedding|
|**Tối ưu token**|Chỉ chọn đoạn liên quan, tránh overload context|
|**Mở rộng tốt**|Có thể nâng cấp thành hệ thống memory quản lý STM, LTM|
|**Áp dụng được ngay**|Có thể chạy với GPT-3.5 + FAISS / ChromaDB / Submodular summarizer|

---

### 💡 Gợi ý mở rộng từ baseline:

|Hướng mở rộng|Mô tả|
|---|---|
|🔄 Cập nhật bộ nhớ|Tích hợp cơ chế Memory Update (APPEND, DELETE, REPLACE...)|
|🧠 Phân loại STM / LTM|Lưu riêng sự kiện ngắn hạn và thông tin người dùng lâu dài|
|📅 Truy xuất theo thời gian|Thêm timestamp vào memory để reasoning theo thời gian|
|⭐ Ưu tiên nội dung|Gắn trọng số, điểm ưu tiên theo hành vi người dùng|

---

### ✅ Tóm tắt chuẩn học thuật:

> Chúng tôi sử dụng một baseline đơn giản nhưng hiệu quả dựa trên RAG để xử lý hội thoại dài hạn. Mô hình tận dụng khả năng học trong ngữ cảnh của LLM, kết hợp với truy xuất đoạn hội thoại liên quan bằng kNN hoặc tóm tắt submodular. Không cần fine-tune mô hình, hệ thống đạt kết quả cao trên hai tập dữ liệu (MSC và MultiDoc2Dial) và thể hiện tiềm năng mạnh mẽ trong bài toán bộ nhớ dài hạn cho LLM.

---

👉 Nếu bạn muốn mình viết đoạn này thành:

- **Mục 2.1 – Baseline đề xuất** trong đề cương đồ án
    
- **Code demo** (retriever + prompt + LLM API)
    
- **Sơ đồ kiến trúc hệ thống**
    

Hô mình 1 tiếng là làm liền 💪


---
```
Có Quốc ơi, **NeurIPS (Conference on Neural Information Processing Systems)** là một trong **những hội nghị học thuật hàng đầu và uy tín nhất thế giới** trong lĩnh vực:

- **Trí tuệ nhân tạo (AI)**
    
- **Học máy (Machine Learning)**
    
- **Deep Learning**
    
- **Khoa học thần kinh tính toán (Computational Neuroscience)**
    

---

### 🎓 Một số điểm nổi bật chứng minh sự “xịn xò” của NeurIPS:

✅ **Xếp hạng A*** theo danh sách hội nghị học thuật CORE Ranking – tức là top-tier trong lĩnh vực AI/ML.

✅ **Tỷ lệ chấp nhận bài rất thấp (~20%)**, chỉ các bài nghiên cứu có chất lượng rất cao, có đóng góp thực tiễn và/hoặc lý thuyết nổi bật mới được duyệt.

✅ Các tên tuổi lớn như **Google DeepMind, OpenAI, Meta AI, Stanford, MIT, CMU, Berkeley, Microsoft Research, FAIR**... đều thường xuyên công bố nghiên cứu tại NeurIPS.

✅ Những bài báo kinh điển trong ngành như:

- **Transformer (Attention is All You Need)**
    
- **AlphaGo**,
    
- **Generative Adversarial Networks (GAN)**
    
- **DALL·E**,
    
- Và gần đây là các nghiên cứu về **LLM, RAG, Prompt Engineering, Memory System**  
    ... đều từng xuất hiện hoặc liên quan tới NeurIPS.
    

---

### 💡 Tóm lại:

> 📚 Nếu bạn dẫn bài từ NeurIPS trong đồ án – người ta sẽ hiểu bạn đang dựa trên nguồn **học thuật top đầu, đáng tin cậy và được peer-reviewed kỹ lưỡng**.

=> Bài “Retrieval-Augmented Generation for Dialog Modeling” được chấp nhận ở **NeurIPS 2023 (Workshop ENLSP)** là một baseline cực kỳ hợp lý, học thuật xịn, lại đơn giản để build.

---

Bạn cần mình giúp ghi chú phần này vào **Related Work / Chứng minh tính học thuật** của đề tài không? Mình viết gọn giúp luôn nè!
```