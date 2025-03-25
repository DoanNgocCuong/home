
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


---
Dưới đây là phần **tổng hợp hai đoạn** bạn cung cấp, được dịch tiếng Việt đầy đủ, logic, và dễ hiểu — dùng được luôn cho mục **Related Work** hoặc mở đầu phần tổng quan:

---

## 🧠 Các hướng tiếp cận hệ thống hội thoại có trí nhớ dài hạn

### 1. **Ba hướng chính để trang bị trí nhớ dài hạn cho trợ lý hội thoại**

Để giúp các trợ lý hội thoại ghi nhớ và xử lý các tương tác dài hạn với người dùng, hiện nay có ba hướng nghiên cứu chính:

#### 📌 **(1) Long-context input trực tiếp**

Cách tiếp cận đầu tiên là **đưa toàn bộ lịch sử hội thoại dài vào LLM** như một đầu vào duy nhất (long-context input), cho phép mô hình xử lý tất cả thông tin một lượt  
→ Ưu điểm: đơn giản, không cần thiết kế lại kiến trúc.  
→ Nhược điểm: **tốn tài nguyên**, và dễ gặp hiện tượng **“lost-in-the-middle”** – mô hình **quên mất phần giữa** khi độ dài đầu vào vượt quá giới hạn xử lý hiệu quả _(Beltagy et al., 2020; Shi et al., 2023)_.

#### 📌 **(2) Tích hợp mô-đun trí nhớ (differentiable memory modules)**

Cách tiếp cận thứ hai là **thay đổi kiến trúc mô hình**, tích hợp thêm các **bộ nhớ học được (learnable memory modules)** như trong Memory Networks, MemGPT…  
→ Mô hình có khả năng lưu trữ, cập nhật và sử dụng lại các thông tin đã ghi nhớ.  
→ Tuy nhiên, cách này **cần huấn luyện lại từ đầu** và **khó triển khai với các API LLM thương mại** _(Weston et al., 2014; Wu et al., 2022)_.

#### 📌 **(3) Nén ngữ cảnh & truy xuất theo nhu cầu (Context Compression & Retrieval)**

Cách thứ ba là **nén hội thoại dài thành các đoạn ngắn dễ truy xuất**, thông qua:

- Tóm tắt (summary)
    
- Trích xuất facts hoặc keyphrase
    
- Chia đoạn logic theo topic  
    Sau đó sử dụng các kỹ thuật **Retrieval-Augmented Generation (RAG)** để tìm và đưa lại các đoạn cần thiết khi có câu hỏi.  
    → Đây là cách tiếp cận **phù hợp với LLM hiện đại (GPT-4, Claude, v.v.) vì có thể áp dụng dưới dạng plug-and-play**  
    → Cũng là cách tiếp cận chính được sử dụng trong **LONGMEMEVAL** và nhiều hệ thống thương mại hiện nay _(OpenAI, Coze, Gutiérrez et al., 2024)_.
    

---

### 2. **Trợ lý hội thoại cá nhân hóa có trí nhớ (Memory-based Personalized Dialogue Agents)**

Song song với các kỹ thuật ghi nhớ tổng quát, một nhánh quan trọng khác là phát triển các **trợ lý hội thoại cá nhân hóa**, có khả năng lưu giữ và sử dụng thông tin riêng biệt của từng người dùng trong các tương tác dài hạn.

- 🔹 **CoMemNN (Pei et al., 2021)**: một trong những mô hình đầu tiên **cập nhật hồ sơ người dùng dần theo hội thoại**.
    
- 🔹 **LD-Agent (Li et al., 2024b)**: sử dụng **bộ nhớ ngắn hạn – dài hạn** để lưu lại các thông tin hội thoại và truy xuất khi cần.
    
- 🔹 **MemoryBank (Zhong et al., 2024)**: mô hình cập nhật trí nhớ dựa trên **đường cong quên Ebbinghaus**, ưu tiên thông tin gần đây.
    
- 🔹 **Theanine (Kim et al., 2024)**: mô hình **truy xuất theo dòng thời gian**, có dùng **LLM phụ trợ để làm sạch** dữ liệu trước khi dùng.
    

🧩 Tuy nhiên, các phương pháp này thường dùng **retriever cố định**, với cách chia nhỏ (granularity) không thay đổi. Điều này **giới hạn khả năng thích ứng** với các dạng hội thoại khác nhau.

👉 Vì vậy, các nghiên cứu gần đây như **RMM** đề xuất cơ chế **retrieval thích ứng (adaptive)**, cho phép thay đổi cách chia nhỏ và truy xuất tuỳ vào ngữ cảnh câu hỏi – mở ra hướng mới trong hệ thống cá nhân hóa dài hạn.

---

Nếu bạn cần:

- Mình tóm phần này lại thành **1 slide PowerPoint** hoặc **mở đầu bài nghiên cứu**.
    
- Viết lại phần này theo **academic English chuẩn để đưa vào section “Related Work”**
    
- Vẽ sơ đồ so sánh 3 hướng tiếp cận + danh sách các mô hình tiêu biểu
    

👉 Mình làm ngay nha!