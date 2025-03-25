
Tuyệt Quốc ơi! Hai bài này là **những baseline rất phù hợp** nếu bạn muốn tập trung vào hướng **"trợ lý hội thoại cá nhân hóa có trí nhớ" (Memory-based Personalized Dialogue Agents)**. Mình sẽ giúp bạn phát biểu rõ ràng lại **cách chọn và sử dụng 2 baseline này trong research**, và gợi ý hướng mở rộng trên từng cái.

---

## 🧱 **Baseline: Personalized Memory in Dialogue Agents**

Trong nhánh nghiên cứu về **ghi nhớ dài hạn theo từng người dùng**, chúng tôi chọn hai công trình nền tảng làm baseline:

---

### **1. CoMemNN – Cooperative Memory Network (Pei et al., 2021)**

📌 Link: [doi.org/10.1145/3442381.3449843](https://doi.org/10.1145/3442381.3449843)

**Ý tưởng chính**:  
CoMemNN là một trong những hệ thống đầu tiên đưa ra **hồ sơ người dùng động (incremental user profile)**, được cập nhật dần dần qua các lượt hội thoại.

- **Cơ chế ghi nhớ**: Tự động trích xuất thông tin cá nhân từ lời thoại và thêm vào "User Profile".
    
- **Cơ chế sử dụng**: Mỗi lần trò chuyện mới, hệ thống sử dụng profile để tạo ngữ cảnh và đưa ra phản hồi phù hợp.
    
- **Dữ liệu sử dụng**: Cần có annotation thủ công về persona/fact, phù hợp với hệ thống quy mô nhỏ.
    

🧩 **Điểm mạnh**:

- Là baseline tiêu biểu cho các hệ thống “ghi nhớ người dùng” không cần mô hình lớn.
    
- Có thể dễ dàng tích hợp vào pipeline hiện tại như một module tách riêng.
    

🧠 **Hướng mở rộng** bạn có thể làm:

- Dùng LLM để **tự động tạo profile** thay vì cần nhãn.
    
- Kết hợp profile với hệ thống RAG: truy xuất đoạn liên quan **+ thêm thông tin người dùng** → tăng cá nhân hóa.
    

---

### **2. Keep Me Updated! (Bae et al., 2022)**

📌 Link: [aclanthology.org/2022.findings-emnlp.276](https://aclanthology.org/2022.findings-emnlp.276)

**Ý tưởng chính**:  
Tác giả đề xuất một hệ thống có khả năng **cập nhật thông tin người dùng theo thời gian**, để phản hồi không bị lỗi thời.

- **Cơ chế**: Mỗi khi người dùng nói điều gì mới (ví dụ "giờ tôi sống ở Hà Nội"), hệ thống sẽ ghi đè/sửa thông tin cũ ("trước ở Đà Nẵng") trong profile.
    
- Hệ thống cũng có thể phản hồi như người thật: “Ồ, bạn chuyển nhà rồi à?”
    

🧩 **Điểm mạnh**:

- Là baseline hiếm hoi giải quyết bài toán **Knowledge Update** trong hội thoại.
    
- Hữu ích trong các hệ thống cần cập nhật liên tục (ngân hàng, bác sĩ ảo, trợ lý cá nhân...).
    

🧠 **Hướng mở rộng** bạn có thể làm:

- Kết hợp với LongMemEval – nhóm câu hỏi **Knowledge Update** là phù hợp nhất.
    
- Thay vì rule-based update → dùng LLM để phát hiện mâu thuẫn và sửa tự động.
    

---

## 🧠 Tổng kết cách dùng hai baseline này:

|Baseline|Điểm mạnh|Dùng cho năng lực nào trong LongMemEval|Cách bạn có thể mở rộng|
|---|---|---|---|
|**CoMemNN**|Xây dựng user profile qua hội thoại|Single-session-user, multi-session|Tự động hoá tạo profile bằng LLM|
|**Keep Me Updated**|Cập nhật hồ sơ người dùng theo thời gian|Knowledge Update, Temporal Reasoning|Phát hiện mâu thuẫn bằng LLM|

---

👉 Nếu Quốc muốn:

- Viết phần _Baseline_ này bằng tiếng Anh học thuật
    
- Tích hợp vào phần “Related Work” hoặc làm slide trình bày
    
- Viết lại hệ thống này bằng code LLM / LangChain demo
    

Mình triển khai ngay nhé!