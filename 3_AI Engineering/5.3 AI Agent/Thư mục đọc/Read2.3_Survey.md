
Trong các tài liệu bạn đã đọc, “thủy tổ” (người đầu tiên đặt nền móng) cho **Long-Term Memory AI** trong bối cảnh hệ thống hội thoại có thể truy hồi và ghi nhớ thông tin qua nhiều lượt tương tác – thường được gọi là **Memory-Augmented Conversational Systems** – không được nêu rõ một cá nhân cụ thể, nhưng có thể tạm chia lịch sử hình thành thành 3 cột mốc lớn:

---

### 🧠 **1. Giai đoạn đặt nền móng: QA có trí nhớ ngắn hạn (trước 2019)**

- Các hệ thống hồi đáp dựa trên **single-turn QA**, tức chỉ trả lời từng câu hỏi độc lập, không “nhớ” lịch sử hội thoại.
    
- Ví dụ như các mô hình như BiDAF++, BERT-QA hay DrQA.
    
- Hệ thống bắt đầu sử dụng embedding để mã hóa ngữ cảnh, nhưng chưa có khả năng lưu và truy hồi thông tin từ các phiên hội thoại cũ.
    

---

### 🧠 **2. Giai đoạn tích hợp trí nhớ: Conversational Memory (2019–2022)**

- Bắt đầu xuất hiện các mô hình như:
    
    - **ORConvQA** (Open-Retrieval Conversational QA) – kết hợp cơ chế hồi tưởng dữ liệu từ các phiên trước.
        
    - **History Selection Module** trong các hệ CMRC (Conversational Machine Reading Comprehension) – lựa chọn các đoạn lịch sử hội thoại liên quan để giúp mô hình hiểu ngữ cảnh của câu hỏi hiện tại.
        
- Đây là giai đoạn các nhà nghiên cứu thấy rõ **vấn đề co-reference**, cập nhật thông tin theo thời gian, và sự phức tạp của hội thoại đa lượt.
    

---

### 🧠 **3. Giai đoạn hiện đại: Memory-Augmented Chat Assistants (2023–nay)**

- Các hệ thống như:
    
    - **MemoryBank** (Zhong et al., 2024)
        
    - **PerLTQA** (Du et al., 2024)
        
    - **LoCoMo** (Maharana, 2024)
        
    - Và **LongMemEval** – được phát triển bởi Di Wu et al., là benchmark mạnh nhất hiện nay cho khả năng ghi nhớ dài hạn.
        
- Các hệ thống bắt đầu áp dụng:
    
    - Chia nhỏ phiên hội thoại (session decomposition)
        
    - Tăng cường key-value store
        
    - Nhận diện sự kiện có thời gian để reasoning chính xác
        

---

### 📌 Gợi ý: Ai là "thủy tổ"?

Nếu phải chọn một “thủy tổ” tiêu biểu cho giai đoạn hiện đại, có thể nhắc đến:

- **Zhong et al. (2024)** với **MemoryBank** – hệ thống đầu tiên thiết kế cụ thể cho trí nhớ dài hạn cá nhân hóa trong hội thoại.
    
- Hoặc **Di Wu et al. (2024)** – với **LongMemEval**, benchmark đầu tiên đưa ra tiêu chuẩn rõ ràng và toàn diện cho việc đánh giá trí nhớ hội thoại dài hạn.
    

---

Quốc có muốn mình tóm tắt các mốc này dưới dạng infographic đơn giản không? Hoặc viết lại thành ngôn ngữ lớp 8 dễ hiểu hơn?