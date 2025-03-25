
2. Related Work Long-term Conversations for LLMs. LLMs have demonstrated the ability to engage in extended, coherent dialogues, yet maintaining context and consistency over long-term interactions remains a challenge. Maharana et al. (2024) introduced the LoCoMo dataset to assess LLMs’ performance in sustained dialogues, showing their struggles with long-range temporal and causal understanding. Existing solutions can be broadly categorized into two approaches: (1) Architectural modifications, such as enhancing attention mechanisms (Liu et al., 2024a; Zhang et al., 2024a), optimizing KV caches (Li et al., 2024c; Liu et al., 2025), and refining position embeddings (Zhao et al., 2024; Zheng et al., 2024). These methods require white-box access to model internals, making them infeasible for 2 In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents proprietary or API-based LLMs. (2) Summarization-based methods, which condense long contexts into structured events or topics for direct conditioning or retrieval (Jiang et al., 2024; Li et al., 2024a; Lu et al., 2023; Wang et al., 2023). RMM falls into this category but explicitly addresses the issue of fragmented topics arising from fixed granularity and incorporates retrospective reflection to refine the retrieval process, encouraging more coherent and contextual responses. Memory-based Personalized Dialogue Agents. The development of memory-based personalized dialogue agents has further enhanced long-term interactions by enabling systems to retain and utilize information from past conversations (Bae et al., 2022). Early approaches, such as CoMemNN (Pei et al., 2021), introduce mechanisms to incrementally enrich user profiles during dialogues. However, collecting substantial annotations for training a personalized system for long-term use is hard (Tseng et al., 2024). Recent advancements focus on integrating LLMs with memory modules. For instance, the LD-Agent framework (Li et al., 2024b) employs long-, short-term memory banks to manage conversational history for retrieval. MemoryBank (Zhong et al., 2024) incorporates a memory updating mechanism inspired by the Ebbinghaus Forgetting Curve, enabling models to retrieve relevant memories considering recency. Theanine (Kim et al., 2024) introduces timeline-based retrieval and utilizes an additional LLM for refinement. These methods typically deploy fixed retrievers with a pre-defined granularity. In contrast, the proposed RMM approach facilitates adaptive retrieval with a revised retrieval granularity
---
Tuyệt, Quốc đang ở phần **Related Work** và muốn hiểu rõ các baseline hiện tại cho bài toán **Long-term Memory trong LLMs**. Dưới đây là phần tóm tắt và phân loại các hướng tiếp cận **baseline**, chia thành 2 nhóm chính như trong paper:

---

## 🧠 1. **Long-term Conversations for LLMs** – duy trì hội thoại dài

### 💡 Mục tiêu:

Giúp LLM nhớ được thông tin xuyên suốt các lượt trò chuyện dài (long-context).

### 🔧 Có 2 hướng chính:

---

### 📐 A. **Architectural modifications** – sửa “bên trong” mô hình

> ⚠️ Yêu cầu truy cập mô hình gốc → không dùng được với API như GPT, Gemini

Gồm các kỹ thuật như:

- **Better attention**: cải tiến attention để nhớ xa hơn (Liu et al., 2024a)
    
- **KV cache optimization**: nén/lưu lại thông tin các lượt cũ để sử dụng tiếp (Li et al., 2024c; Liu et al., 2025)
    
- **Better positional embeddings**: mã hóa vị trí tốt hơn để model hiểu thứ tự (Zhao et al., 2024)
    

---

### 📄 B. **Summarization-based methods** – tóm tắt nội dung dài

> ⚡ Phù hợp với API-based LLMs

Gồm:

- **Topic/Key-point summary**: trích thông tin chính từ các session thành dạng có cấu trúc.
    
- **Memory retrieval**: dùng các đoạn đã tóm tắt để truy xuất lại khi cần.
    

Tiêu biểu:

- **Jiang et al. (2024)**, **Lu et al. (2023)**, **Wang et al. (2023)** – các kỹ thuật RAG với tóm tắt đa bước.
    
- **Li et al. (2024a)** – khung retrieve-then-reason.
    
- **RMM** – là một dạng đặc biệt trong nhóm này, giải quyết nhược điểm "granularity cứng" và dùng hồi tưởng để cải thiện chọn lọc memory.
    

---

## 🤖 2. **Memory-based Personalized Dialogue Agents** – trợ lý cá nhân hóa có trí nhớ

### 💡 Mục tiêu:

Giúp trợ lý AI **hiểu rõ người dùng theo thời gian** và giữ được “phong cách trò chuyện riêng”.

---

### 🧱 Các baseline nổi bật:

|Tên mô hình|Điểm nổi bật|
|---|---|
|**CoMemNN (2021)**|Mô hình đầu tiên xây dựng **profile cá nhân** qua nhiều lượt hội thoại.|
|**LD-Agent (2024)**|Tạo **memory bank** chia theo ngắn hạn – dài hạn. Truy xuất dựa trên **keyphrase**.|
|**MemoryBank (2024)**|Ghi nhớ theo **đường cong quên (Ebbinghaus)**, truy xuất theo thời gian gần đây.|
|**Theanine (2024)**|Truy xuất theo **timeline**, sử dụng thêm một LLM để **refine lại** đoạn truy xuất.|

---

### ❌ Điểm yếu chung:

- Đều dùng **retriever cố định + granularity cố định** (theo session hoặc turn).
    
- Không thể **tự điều chỉnh** cách truy xuất theo ngữ cảnh khác nhau hoặc người dùng khác nhau.
    

---

## ✅ Điểm mới của **RMM (Reflective Memory Management)** so với baseline:

|Tính năng|RMM có?|Các baseline có?|
|---|---|---|
|Ghi nhớ theo chủ đề linh hoạt|✅|❌ (cứng nhắc theo session/turn)|
|Học từ lỗi truy xuất (RL)|✅|❌|
|Không cần fine-tune retriever|✅|❌|
|Hỗ trợ API-based LLM|✅|Một số không|

---

Nếu Quốc muốn mình:

- Vẽ 1 bảng so sánh rõ nét hơn giữa RMM và các baseline?
    
- Tư vấn chọn baseline phù hợp nhất để so sánh trong paper?
    
- Viết phần “Related Work” mẫu tiếng Anh theo format academic?
    

Mình làm ngay!