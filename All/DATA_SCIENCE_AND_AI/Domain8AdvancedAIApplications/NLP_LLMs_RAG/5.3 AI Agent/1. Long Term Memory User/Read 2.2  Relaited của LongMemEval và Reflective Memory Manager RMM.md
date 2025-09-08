```
Long-TermMemoryMethods Toequipchatassistantswithlong-termmemorycapabilities, three major techniques are commonly explored. The first approach involves directly adapting LLMs to process extensive history information as long-context inputs (Beltagy et al., 2020; Kitaev et al., 2020; Fu et al., 2024; An et al., 2024). While this method avoids the need for complex architectures, it is inefficient and susceptible to the “lost-in-the-middle” phenomenon, where the ability of LLMs to utilize contextual information weakens as the input length grows (Shi et al., 2023; Liu et al., 2024). A second line of research integrates differentiable memory modules into language models, proposing specialized architectural designs and training strategies to enhance memory capabilities (Weston et al., 2014; Wu et al., 2022; Zhong et al., 2022; Wang et al., 2023). Lastly, several studies approach long-term memory from the perspective of context compression, developing techniques 3 Published as a conference paper at ICLR 2025 to condense lengthy histories into compact representations, whether in the form of LLM internal representations (Mu et al., 2023; Chevalier et al., 2023), discrete tokens (Jiang et al., 2023; Xu et al., 2024), or retrievable text segments via retrieval-augmented generation (RAG, Shi et al. (2024); Wang et al. (2023); Sarthi et al. (2024); Chen et al. (2023a); Guti´ errez et al. (2024)). Although LONGMEMEVAL can evaluate any memory system, we will take an online context compression perspective, where each history interaction session is sequentially processed, stored, and accessed on-demand through indexing and retrieval mechanisms (§4). This formulation aligns with current literature (Zhong et al., 2024; Guti´ errez et al., 2024) and commercial systems (OpenAI, 2024; Coze, 2024). Its plug-and-play nature also facilitates the integration into existing chat assistant systems
```

```
Memory-based Personalized Dialogue Agents. The development of memory-based personalized dialogue agents has further enhanced long-term interactions by enabling systems to retain and utilize information from past conversations (Bae et al., 2022). Early approaches, such as CoMemNN (Pei et al., 2021), introduce mechanisms to incrementally enrich user profiles during dialogues. However, collecting substantial annotations for training a personalized system for long-term use is hard (Tseng et al., 2024). Recent advancements focus on integrating LLMs with memory modules. For instance, the LD-Agent framework (Li et al., 2024b) employs long-, short-term memory banks to manage conversational history for retrieval. MemoryBank (Zhong et al., 2024) incorporates a memory updating mechanism inspired by the Ebbinghaus Forgetting Curve, enabling models to retrieve relevant memories considering recency. Theanine (Kim et al., 2024) introduces timeline-based retrieval and utilizes an additional LLM for refinement. These methods typically deploy fixed retrievers with a pre-defined granularity. In contrast, the proposed RMM approach facilitates adaptive retrieval with a revised retrieval granularity
```




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


---
Tuyệt vời. Mình sẽ viết một survey thật chi tiết về các hướng nghiên cứu Long-Term Memory trong hệ thống hội thoại, từ giai đoạn sơ khai đến các kỹ thuật hiện đại như memory modules, context compression, và các hệ personalized memory. Bài viết sẽ phân tích các cột mốc quan trọng, các baseline nổi bật, và những benchmark mới nhất như LongMemEval, nhằm giúp bạn có nền tảng vững chắc để phát triển thành một bài báo khoa học.

Mình sẽ trình bày lại theo dạng academic report chuẩn, bao gồm các mục tiêu khảo sát, phân loại các phương pháp, so sánh, và gợi ý hướng mở rộng. Mình sẽ gửi lại bản đầy đủ sau khi hoàn tất.

# Giới thiệu

Các hệ thống hỏi-đáp (QA) và đối thoại sớm thường **không có cơ chế bộ nhớ dài hạn**, xử lý mỗi truy vấn độc lập mà không lưu lại thông tin cuộc hội thoại trước đó. Chẳng hạn, mô hình đọc hiểu BiDAF (Bi-Directional Attention Flow) và các biến thể cải tiến (BiDAF++) được dùng cho SQuAD và các bộ dữ liệu QA trước năm 2019 chỉ chú trọng việc tìm đáp án trong một đoạn văn bản ngắn, không lưu giữ ngữ cảnh hội thoại ([BERT with History Answer Embedding for Conversational Question Answering](https://arxiv.org/pdf/1905.05412#:~:text=4,representation%20generated%20when%20answering%20previous)). Tương tự, hệ thống DrQA của Facebook (2017) thực hiện QA mở trên Wikipedia bằng cách truy xuất và đọc tài liệu, nhưng mỗi câu hỏi đều được trả lời tách biệt, không có ký ức về các câu hỏi trước đó ([BERT with History Answer Embedding for Conversational Question Answering](https://arxiv.org/pdf/1905.05412#:~:text=,JASIS%2C%2038%3A389%E2%80%93404%2C%201987)). Khi các trợ lý ảo và chatbot trở nên phổ biến, hạn chế “_trí nhớ cá vàng_” này bộc lộ rõ: mô hình dễ lặp lại câu hỏi, quên thông tin người dùng cung cấp trước đó, hoặc không thể duy trì tính nhất quán qua nhiều lượt tương tác. Do đó, **trí nhớ dài hạn trong hội thoại** (long-term memory) đã trở thành một hướng nghiên cứu quan trọng, hướng đến việc giúp hệ thống **ghi nhớ thông tin xuyên suốt các phiên trò chuyện** và cá nhân hóa phản hồi theo lịch sử tương tác.

**Memory-Augmented Conversational Systems** (hệ thống đối thoại tăng cường bộ nhớ) là các mô hình được thiết kế để khắc phục hạn chế trên bằng cách tích hợp một thành phần bộ nhớ vào pipeline đối thoại ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=integrated%20memory%20components%20to%20track,context%20LLMs)). Điều này cho phép chatbot _ghi nhớ và sử dụng lại_ các thông tin trước đó – ví dụ như sở thích, tiểu sử người dùng, tình huống đã xảy ra – nhằm tạo ra phản hồi chính xác hơn và có tính cá nhân hóa. Bài survey này sẽ trình bày chi tiết sự phát triển của lĩnh vực này: từ những mô hình QA _tiền 2019_ không có trí nhớ dài hạn, đến các hệ thống _hiện đại (2023-nay)_ có khả năng ghi nhớ đa phiên, cập nhật kiến thức và suy luận thời gian. Chúng tôi phân tích ba hướng tiếp cận chính để tích hợp bộ nhớ: (1) đưa toàn bộ ngữ cảnh dài vào đầu vào mô hình (long-context input), (2) sử dụng module bộ nhớ phân biệt có thể huấn luyện cùng mô hình (differentiable memory modules), và (3) nén ngữ cảnh và truy hồi thông tin khi cần (context compression & retrieval). Bên cạnh đó, chúng tôi điểm qua các mô hình tiêu biểu ở mỗi giai đoạn như BiDAF++, DrQA, ORConvQA, MemoryBank, Theanine, LD-Agent…, so sánh một số hệ thống nền tảng (baseline) nổi bật như MemNN, **Keep Me Updated** và **LD-Agent**, cũng như các bộ dữ liệu và benchmark đánh giá trí nhớ đối thoại (LongMemEval, LOCOMO, v.v.) cùng các tiêu chí đánh giá quan trọng (khả năng nhớ – recall, ảo giác – hallucination, cập nhật kiến thức – knowledge update, suy luận thời gian – temporal reasoning, _abstention_...). Cuối cùng, chúng tôi thảo luận những hướng mở rộng đầy hứa hẹn, chẳng hạn kết hợp cơ chế **RAG** (Retrieval-Augmented Generation) với cập nhật bộ nhớ động, truy hồi thích ứng, hay sử dụng mô hình ngôn ngữ lớn (LLM) như một module hỗ trợ quản lý trí nhớ.

# Các hướng tiếp cận chính để tích hợp trí nhớ dài hạn

Có ba cách tiếp cận phổ biến nhằm trang bị khả năng nhớ dài hạn cho hệ thống hội thoại: (1) **Mở rộng ngữ cảnh đầu vào (long-context input)** – cung cấp cho mô hình một chuỗi hội thoại rất dài để nó tự tìm thông tin cần nhớ; (2) **Module bộ nhớ khả vi (differentiable memory)** – thiết kế một kiến trúc mạng nơ-ron với thành phần bộ nhớ ngoài có thể đọc/ghi trong quá trình huấn luyện; (3) **Nén và truy hồi ngữ cảnh (context compression & retrieval)** – tóm tắt hoặc lưu trữ thông tin quan trọng từ hội thoại vào một kho bộ nhớ ngoài, và truy vấn nó khi cần thiết cho phản hồi. Dưới đây, chúng tôi phân tích chi tiết từng hướng tiếp cận, cùng các ví dụ mô hình tiêu biểu.

## Tiếp cận 1: Mở rộng ngữ cảnh đầu vào

Cách đơn giản nhất để mô hình “nhớ” là **cung cấp toàn bộ lịch sử hội thoại trong phần input** của nó, nhằm cho phép mô hình tự truy xuất những chi tiết cần thiết. Trong các hệ QA/hội thoại truyền thống, điều này thường tương đương với việc nối chuỗi các lượt hỏi-đáp trước vào câu hỏi hiện tại. Ví dụ, trên bộ dữ liệu hội thoại ngữ cảnh CoQA/QuAC, mô hình BiDAF++ đã được cải tiến để chấp nhận thêm 2 lượt hỏi-đáp trước đó làm ngữ cảnh, bên cạnh đoạn văn cần đọc ([BERT with History Answer Embedding for Conversational Question Answering](https://arxiv.org/pdf/1905.05412#:~:text=4,representation%20generated%20when%20answering%20previous)). Việc đơn giản nối thêm lịch sử như vậy giúp mô hình trả lời tốt hơn các câu hỏi phụ thuộc bối cảnh (ví dụ đại từ, tham chiếu đến thông tin nhắc ở câu hỏi trước). Tương tự, trong đối thoại mở, một số mô hình dựa trên BERT/GPT ban đầu cũng thực hiện bằng cách **prepend** toàn bộ nội dung cuộc trò chuyện trước đó vào prompt đầu vào ở mỗi lượt đáp.

Cùng với sự phát triển của các Transformer có cửa sổ ngữ cảnh lớn, hướng tiếp cận này ngày càng tỏ ra hữu dụng hơn. Các mô hình ngôn ngữ lớn (LLM) hiện nay như GPT-4 hay Claude có thể chấp nhận ngữ cảnh dài hàng chục nghìn token, cho phép lưu giữ nguyên vẹn nội dung nhiều phiên trò chuyện trước đó. Tuy nhiên, cách làm này **đối mặt với những hạn chế**: (i) Chi phí tính toán tăng lên đáng kể khi độ dài input lớn, gây chậm trễ và tốn tài nguyên; (ii) Mặc dù input rất dài, mô hình vẫn có thể **“quên”** các chi tiết quan trọng hoặc **giảm độ chính xác** khi phải xử lý quá nhiều thông tin không liên quan. Nghiên cứu gần đây cho thấy ngay cả các chat GPT có ngữ cảnh mở rộng vẫn sụt giảm ~30% độ chính xác khi phải ghi nhớ thông tin trải dài qua một cuộc trò chuyện kéo dài ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=meticulously%20curated%20questions%20embedded%20within,augmented%20key)). Nguyên nhân là cơ chế tự chú ý có khuynh hướng tập trung vào nội dung gần thời điểm hiện tại, còn các chi tiết từ rất lâu về trước dù nằm trong input cũng có thể bị lu mờ. Do đó, mở rộng ngữ cảnh đầu vào _chưa phải giải pháp tối ưu_ cho trí nhớ dài hạn, đặc biệt khi hội thoại kéo dài hàng trăm lượt.

Một số cải tiến đã được đề xuất trong hướng này nhằm giúp mô hình tận dụng ngữ cảnh dài hiệu quả hơn. Chẳng hạn, **Transformer-XL** (Dai et al., 2019) giới thiệu cơ chế ghi nhớ các trạng thái ẩn và tái sử dụng chúng ở các phân đoạn sau, tạo một dạng _bộ nhớ ngắn hạn trượt_ hỗ trợ kết nối ngữ cảnh dài. **Compressive Transformer** (Rae et al., 2019) tiến thêm bước nữa khi nén các trạng thái cũ lại (ví dụ lấy mẫu hoặc trung bình) thay vì bỏ hẳn, giúp mô hình có “ký ức tóm lược” về những đoạn rất xa. Mặc dù vậy, các kỹ thuật này vẫn hoạt động trong khuôn khổ trọng số mô hình và độ dài ngữ cảnh cố định, chứ chưa cung cấp một kho nhớ linh hoạt có thể tùy ý đọc ghi.

Tóm lại, cung cấp ngữ cảnh hội thoại dài vào trực tiếp mô hình là cách dễ dàng triển khai (không cần thay đổi kiến trúc), và có hiệu quả nhất định trong các tình huống hội thoại ngắn hoặc trung bình. Nhưng với các tương tác lâu dài, đa phiên, phương pháp này bộc lộ hạn chế về cả hiệu năng lẫn độ tin cậy. Điều đó dẫn tới nhu cầu về những kiến trúc có **bộ nhớ ngoài** rõ rệt hơn, nằm ngoài chuỗi input đơn thuần – vốn là nội dung của hai hướng tiếp cận sau.

## Tiếp cận 2: Module bộ nhớ khả vi (Differentiable Memory)

Hướng tiếp cận thứ hai tích hợp trí nhớ dài hạn ngay trong **kiến trúc của mô hình** dưới dạng một module bộ nhớ đặc biệt có thể đọc/ghi thông tin. Khác với việc nhồi nhét mọi thứ vào input, ở đây mô hình có một **bộ nhớ rời** (external memory) – ví dụ một ma trận hoặc dải ô nhớ – cho phép lưu trạng thái cuộc thoại và truy xuất lại khi cần thông qua cơ chế attention hoặc đọc-ghi khả vi (differentiable read/write). Ý tưởng này được tiên phong bởi Weston et al. (2014) với mô hình **Memory Networks**, kết hợp giữa một thành phần suy luận (inference) và một thành phần bộ nhớ dài hạn ([[1410.3916] Memory Networks](https://arxiv.org/abs/1410.3916#:~:text=,chaining%20multiple%20supporting%20sentences%20to)). Bộ nhớ này có thể coi như một **cơ sở tri thức động**: tại mỗi bước, mô hình có thể ghi các thông tin mới vào các ô nhớ, và khi trả lời thì thực hiện chu trình chú ý lên bộ nhớ để _chọn lọc các đoạn liên quan_ phục vụ suy luận. Trên các tác vụ QA đơn giản, Memory Network đã chứng tỏ khả năng **xâu chuỗi lập luận nhiều bước** nhờ đọc từ nhiều ô nhớ (chẳng hạn trả lời câu hỏi cần 2-3 câu hỗ trợ) ([[1410.3916] Memory Networks](https://arxiv.org/abs/1410.3916#:~:text=these%20models%20in%20the%20context,understanding%20the%20intension%20of%20verbs)).

Tiếp nối hướng này, nhiều kiến trúc bộ nhớ khả vi khác ra đời: **End-to-End Memory Network** (Sukhbaatar et al., 2015) tối ưu hóa Memory Network bằng cơ chế attention đa lượt; **Dynamic Memory Network** (Kumar et al., 2016) áp dụng thành công cho hiểu ngôn ngữ và phân tích cảm xúc; đặc biệt là mô hình **Differentiable Neural Computer (DNC)** của DeepMind, một bộ nhớ ngoài có mô đun đọc/ghi được điều khiển bởi một mạng LSTM ([Differentiable neural computer - Wikipedia](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=In%20artificial%20intelligence%20%2C%20a,1)) ([Differentiable neural computer - Wikipedia](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=DNC%20indirectly%20takes%20inspiration%20from,by%20finding%20a%20%2052)). DNC được ví như _máy Turing thần kinh_, có thanh ghi nhớ và bộ điều khiển học cách ghi nhớ chuỗi dữ liệu và truy vấn khi cần. Graves et al. (2016) cho thấy DNC có thể học cách **lưu trữ và truy hồi thông tin dạng đồ thị tuần tự**, ví dụ ghi lại một tuyến đường và sau đó xuất ra đường đi ngắn nhất, hay tạo ra lời giải cho bài toán dường như cần khả năng “lập trình” ([Differentiable neural computer - Wikipedia](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=So%20far%2C%20DNCs%20have%20been,video%20commentaries%20or%20semantic%20text)). Những mô hình này **gián tiếp chứng minh** mạng nơ-ron có khả năng mô phỏng hành vi nhớ và suy luận phi tuyến tính nếu được trang bị bộ nhớ ngoài đủ mạnh.

Trong bối cảnh hội thoại, module bộ nhớ khả vi hứa hẹn giúp chatbot **nhớ các thông tin từ các lượt trước** mà không cần mang toàn bộ nội dung đó trong ngữ cảnh mỗi lần. Thay vào đó, thông tin sẽ được viết vào bộ nhớ (ví dụ vector ẩn đại diện cho câu thoại quan trọng) và sau đó đọc ra khi phải phản hồi. Một ví dụ đơn giản: một **Memory Network** có thể lưu trữ các phát ngôn của người dùng dưới dạng vector trong ô nhớ, và mỗi lần trả lời, mô hình truy tìm vector nào có liên quan nhất đến câu hỏi hiện tại để sử dụng ([[1410.3916] Memory Networks](https://arxiv.org/abs/1410.3916#:~:text=memory%20component%3B%20they%20learn%20how,chaining%20multiple%20supporting%20sentences%20to)). Về nguyên tắc, phương pháp này có thể mở rộng trí nhớ tùy ý (chỉ cần tăng số ô nhớ) và mô hình có thể học cách ghi đè hoặc làm mờ dần các ô ít quan trọng – tương tự cơ chế quên có chủ đích.

Tuy nhiên, **thách thức lớn** của hướng tiếp cận này nằm ở việc _huấn luyện_ và _quy mô_. Việc huấn luyện end-to-end để mô hình vừa làm tốt nhiệm vụ đối thoại, vừa tối ưu cách đọc/ghi bộ nhớ không hề dễ dàng, đặc biệt trên dữ liệu hội thoại tự nhiên phức tạp. Kết quả là các kiến trúc bộ nhớ khả vi từng thành công trên nhiệm vụ giả lập (như bài toán bAbI của Facebook) lại ít được sử dụng trong các hệ thống hội thoại mở rộng thực tế. Thay vào đó, cộng đồng chuyển sang các phương pháp dùng bộ nhớ ngoài nhưng _không train chung với mô hình_, tức là hướng (3) dưới đây. Gần đây, một số nghiên cứu cố gắng kết hợp LLM với module nhớ khả vi – ví dụ **PlugLM** (Cheng et al., 2022) chèn một bộ nhớ key-value có thể cập nhật vào mô hình pretrained để tách rời phần lưu trữ kiến thức khỏi tham số mô hình ([Language model with Plug-in Knowldge Memory | OpenReview](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=of%20knowledge%20PLM%20needs%20to,also%20keep%20absorbing%20new%20knowledge)). Dù có kết quả khả quan trong cập nhật kiến thức mới mà không tái huấn luyện toàn bộ mô hình ([Language model with Plug-in Knowldge Memory | OpenReview](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=adaptation%20setting%2C%20PlugLM%20could%20be,task%20knowledge)), cách làm này vẫn hiếm khi áp dụng trực tiếp trong đối thoại mở. Nói tóm lại, module bộ nhớ khả vi là một hướng mang nhiều tiềm năng về mặt lý thuyết, nhưng độ phức tạp khi huấn luyện và tích hợp khiến nó chưa phổ biến bằng cách tiếp cận dựa trên truy hồi thông tin.

## Tiếp cận 3: Nén ngữ cảnh và truy hồi thông tin

Hiện nay, **phổ biến nhất** trong các hệ thống đối thoại có trí nhớ dài hạn là hướng tiếp cận dựa trên **bộ nhớ ngoài kết hợp truy hồi (retrieval)**. Thay vì giữ toàn bộ lịch sử trong input hay thiết kế một module nhớ phức tạp bên trong, phương pháp này tách biệt hẳn một **kho lưu trữ thông tin hội thoại** (conversation memory repository) dưới dạng văn bản hoặc vector, và sử dụng các thuật toán truy hồi (thường qua embedding và so khớp ngữ nghĩa) để lấy ra những mẩu thông tin cần thiết cho mỗi lượt đối thoại. Cách tiếp cận này chịu ảnh hưởng từ thành công của mô hình **open-domain QA** và **retrieval-augmented generation (RAG)**, nơi mô hình language model được bổ trợ bởi một cơ chế tìm kiếm tri thức bên ngoài. Điểm khác biệt là ở đây, kho lưu trữ không phải tri thức chung cố định (như Wikipedia) mà chính là _những gì đã diễn ra trong cuộc hội thoại trước đó_.

Quy trình chung thường gồm các bước: (i) **Lưu trữ**: mỗi khi kết thúc một phiên hoặc một số lượt thoại, hệ thống sẽ trích xuất các thông tin cốt lõi (ví dụ: sự kiện vừa xảy ra, tính cách hoặc sở thích người dùng được đề cập, câu hỏi chưa được trả lời,...) và lưu vào bộ nhớ dài hạn. Việc lưu trữ này có thể ở dạng văn bản thô (như tập các câu tóm tắt) hoặc vector embedding (như trung bình biểu diễn của câu nói). (ii) **Truy vấn**: khi đối thoại tiếp tục, trước khi tạo câu trả lời, mô hình sẽ truy vấn bộ nhớ để lấy ra những mẩu thông tin liên quan đến ngữ cảnh hiện tại. Chẳng hạn, nếu người dùng hỏi lại “_Hôm trước bạn hứa gì với tôi?_”, hệ thống sẽ tìm trong bộ nhớ mục nào chứa nội dung lời hứa. (iii) **Sử dụng**: các kết quả truy hồi được đưa vào mô hình (như một đoạn context thêm vào prompt của LLM) để sinh ra phản hồi cuối cùng. Cơ chế này tương tự pipeline _retrieve-then-read_ đã thành công trong QA mở ([[2005.11364] Open-Retrieval Conversational Question Answering](https://arxiv.org/abs/2005.11364#:~:text=retrieval%20conversational%20question%20answering%20,the%20reranker%20component%20contributes%20to)), chỉ khác là “corpus” ở đây chính là lịch sử hội thoại quá khứ.

**Ưu điểm chính** của hướng này là khả năng mở rộng và kiểm soát: Ta có thể duy trì một bộ nhớ rất lớn (hàng nghìn sự kiện) mà không làm “quá tải” mô hình tại thời điểm sinh đầu ra, bởi vì luôn chỉ một phần nhỏ (ví dụ 5-10 đoạn) được truy hồi làm ngữ cảnh mỗi lượt. Đồng thời, ta có thể **cập nhật** hoặc **điều chỉnh** nội dung bộ nhớ độc lập với mô hình (vì nó nằm ngoài), giúp dễ dàng thêm thông tin mới, xóa thông tin lỗi thời, hay sửa sai nếu chatbot ghi nhớ nhầm. Những hệ thống hội thoại dài hạn mạnh gần đây hầu hết đều theo kiến trúc này, kết hợp với nhiều kỹ thuật tinh vi để tăng chất lượng tóm tắt và truy hồi.

Một ví dụ tiêu biểu là **ORConvQA** (Open-Retrieval Conversational QA) của Qu et al. (2020). Thay vì giả định câu trả lời luôn nằm trong một đoạn văn cho trước như CoQA, ORConvQA cho phép mô hình **truy tìm bằng chứng** từ một tập tài liệu lớn trước khi trả lời ([[2005.11364] Open-Retrieval Conversational Question Answering](https://arxiv.org/abs/2005.11364#:~:text=passage,We%20further%20show%20that%20our)). Hệ thống của họ gồm ba thành phần Transformer: truy hồi (retriever), tái xếp hạng, và đọc hiểu, cho phép tìm kiếm thông tin qua nhiều lượt hỏi đáp. Kết quả chỉ ra rằng việc tích hợp _history modeling_ (mô hình hóa lịch sử hội thoại) vào cả truy hồi lẫn đọc hiểu giúp cải thiện đáng kể độ chính xác ([[2005.11364] Open-Retrieval Conversational Question Answering](https://arxiv.org/abs/2005.11364#:~:text=to,the%20reranker%20component%20contributes%20to)) – minh chứng cho lợi ích của việc lưu và sử dụng ngữ cảnh từ các lượt trước. ORConvQA là cầu nối từ QA thuần túy sang đối thoại có trí nhớ, cho thấy **kết hợp retrieval với context hội thoại** là hướng đi hữu ích.

Trong đối thoại mở, dự án **BlenderBot 2.0** của Facebook (Roller et al., 2021) lần đầu tiên giới thiệu một chatbot có khả năng **“nhớ” các cuộc trò chuyện trước đó**. Cụ thể, BlenderBot 2.0 lưu lại _tóm tắt_ của mỗi phiên tương tác với người dùng trong một cơ sở dữ liệu bộ nhớ lâu dài. Khi gặp lại người dùng đó hoặc trong phiên kế tiếp, bot sẽ truy vấn cơ sở này để tìm các thông tin liên quan (ví dụ: tên người dùng, sở thích đã đề cập) và điều chỉnh phản hồi cho phù hợp. Song song, BlenderBot 2.0 còn tích hợp tìm kiếm Internet, nhưng điểm mấu chốt là nó chứng minh được việc **ghi nhớ và truy xuất dữ kiện từ các phiên trước** giúp bot trở nên tự nhiên và nhất quán hơn hẳn so với phiên bản trước đó (BlenderBot 1) vốn chỉ nhớ trong phạm vi phiên hiện tại. Đây là một minh họa sớm cho hiệu quả của memory augmentation trong đối thoại.

Để quản lý bộ nhớ hiệu quả, các nghiên cứu gần đây tập trung vào **kỹ thuật tóm tắt và cập nhật bộ nhớ**. Thay vì lưu tất cả mọi câu, hệ thống sẽ **tóm tắt ngắn gọn** những thông tin quan trọng sau mỗi phiên. Bae et al. (2022) – trong hệ thống **“Keep Me Updated!”** – sử dụng một mô-đun tóm tắt để trích xuất các câu **tiểu sử người dùng** sau mỗi phiên trò chuyện và lưu chúng vào bộ nhớ ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=interlocutors%20revealed%20in%20the%20previous,in%02coming%20summary%20is%20%E2%80%9CJust%20got)) ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=For%20example%2C%20if%20the%20previous,additional%20condi%02tion%20for%20generating%20chatbot)). Quan trọng hơn, họ thiết kế cơ chế **quản lý bộ nhớ động**: mỗi khi có thông tin mới, hệ thống so sánh với các câu nhớ cũ và thực hiện bốn thao tác có thể – _giữ nguyên (PASS), thay thế (REPLACE), thêm mới (APPEND), hoặc xóa bỏ (DELETE)_ – nhằm loại bỏ mâu thuẫn hoặc trùng lặp ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=Specifically%2C%20the%20memory%20management%20mechanism,%E2%80%9CJust%20got%20positive%20results%20from)). Chẳng hạn, nếu bộ nhớ có câu “Chưa xét nghiệm COVID” và phiên mới phát hiện “Vừa nhận kết quả dương tính COVID”, mô-đun sẽ _thay thế_ câu cũ bằng câu mới trong bộ nhớ ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=find%20and%20eliminate%20the%20information,in%20sub%02sequent%20sessions%2C%20a%20relevant)). Nhờ đó, bộ nhớ luôn được duy trì _cập nhật_ và _nhất quán_ với tình trạng hiện tại của người dùng. Thí nghiệm cho thấy cách tiếp cận này giúp chatbot duy trì được **tính chính xác của trí nhớ** qua nhiều phiên, cải thiện tính gắn kết và tự nhiên trong đối thoại dài ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=With%20extensive%20experiments%20and%20ablations%2C,date)).

Một hướng khác để nén thông tin là sử dụng LLM tự động tạo **bản tóm tắt đệ quy**. Wang et al. (2023) đề xuất phương pháp _Recursively Summarizing_ với GPT-4: chia hội thoại rất dài thành các đoạn nhỏ, lần lượt dùng LLM tóm tắt từng đoạn, rồi lại tóm tắt tiếp các bản tóm tắt để tạo nên một _“siêu tóm tắt”_ cuối cùng làm bộ nhớ ([[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models](https://arxiv.org/abs/2308.15022#:~:text=long%20conversation%2C%20these%20chatbots%20fail,consistent%20responses%20in%20a%20long)). Mô hình đối thoại sẽ tham khảo các tóm tắt này thay vì toàn bộ chi tiết cuộc trò chuyện. Kỹ thuật đệ quy này giúp lưu giữ được ý chính của những hội thoại hàng trăm lượt dưới dạng vài đoạn văn súc tích. Thú vị là nhóm tác giả nhận thấy phương pháp của họ có thể **kết hợp cộng hưởng** với cả LLM có ngữ cảnh dài (8K-16K) lẫn mô hình tích hợp retrieval, giúp nâng cao hiệu quả trên các hội thoại cực dài ([[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models](https://arxiv.org/abs/2308.15022#:~:text=consistent%20response%20with%20the%20help,scripts%20will%20be%20released%20later)). Điều này gợi ý hướng tương lai: kết hợp giữa tóm tắt và truy hồi một cách thích ứng.

Đối với pha **truy hồi**, hầu hết các hệ thống dùng **embedding không gian**: lưu các memory dưới dạng vector nhúng và sử dụng _khoảng cách ngữ nghĩa_ để tìm kiếm. Độ chính xác truy hồi phụ thuộc nhiều vào cách biểu diễn và tổ chức bộ nhớ. Pan et al. (2024) trong công trình **SeCom** nhấn mạnh tầm quan trọng của **“đơn vị bộ nhớ”**: họ so sánh lưu trữ theo từng lượt thoại, theo từng phiên, và theo đoạn tóm tắt, nhận thấy mỗi cách có ưu nhược điểm riêng ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=To%20deliver%20coherent%20and%20personalized,retrieval%20accuracy%20across%20different%20granularities)) ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=Building%20on%20these%20insights%2C%20we,as%20DialSeg711%2C%20TIAGE%2C%20and%20SuperDialSeg)). SeCom đề xuất một chiến lược kết hợp: dùng một mô hình phân đoạn chủ đề để chia hội thoại thành các **đoạn sự kiện ngắn**, lưu mỗi đoạn như một bản ghi bộ nhớ, đồng thời áp dụng kỹ thuật **“nén thông tin nhiễu”** để lọc bớt phần không liên quan trong mỗi đoạn trước khi lưu ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=Building%20on%20these%20insights%2C%20we,as%20DialSeg711%2C%20TIAGE%2C%20and%20SuperDialSeg)). Kết quả, cách lưu trữ theo đoạn chủ đề giúp tăng chất lượng truy hồi trên các benchmark hội thoại dài như LOCOMO, vì nó cân bằng giữa chi tiết và tổng quát. Bên cạnh đó, một số cải tiến khác gồm **truy hồi theo thời gian** (ưu tiên các sự kiện gần đây nếu câu hỏi chứa mốc thời gian – xem Wu et al. 2023) hay **mở rộng truy vấn bằng tri thức** (ví dụ nếu hỏi “anh ấy” thì truy vấn mở rộng “anh ấy” = tên cụ thể từ bộ nhớ). Những tối ưu này đã được tổng kết trong nghiên cứu LongMemEval, đề xuất khung “Indexing-Retrieval-Reading” cho thiết kế bộ nhớ, trong đó: **đánh chỉ mục** tối ưu bằng cách lưu trữ theo phiên nhỏ (session decomposition) và mở rộng khóa bằng dữ kiện, **truy hồi** tối ưu bằng cách cân nhắc ngữ cảnh thời gian, và **đọc** hiệu quả bằng cách kết hợp bộ nhớ vào input LLM ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=showing%20a%2030,term)).

Gần đây, xuất hiện những hệ thống trí nhớ tiên tiến tận dụng sức mạnh LLM: ví dụ **MemoryBank** (Zhong et al., 2023) và **THEANINE** (Ong et al., 2024). MemoryBank tích hợp một **cơ chế cập nhật bộ nhớ lấy cảm hứng từ đường cong lãng quên của Ebbinghaus** – nghĩa là mô phỏng việc ký ức phai nhạt dần theo thời gian nếu không nhắc lại ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)). Cụ thể, MemoryBank cho phép AI “quên” bớt những ký ức ít quan trọng hoặc lâu không dùng, và **củng cố** những ký ức hay được truy xuất, nhờ đó bộ nhớ hoạt động hiệu quả và giống người hơn ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Updating)). Họ triển khai MemoryBank trên một chatbot bạn đồng hành (SiliconFriend), cho thấy bot có thể **tiếp thu và thích nghi với tính cách người dùng** qua thời gian, đồng thời nhớ được các sự kiện cốt lõi trong quá khứ (ví dụ sở thích, mục tiêu người dùng) nhờ cơ chế này ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=psychological%20counseling%2C%20and%20secretarial%20assistance,the%20memory%2C%20thereby%20offering%20a)) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,memory%20works%20through%20repeated%20retrieval)). Trong khi đó, THEANINE lại chọn cách **không xóa bỏ ký ức cũ**, thay vào đó quản lý một **đồ thị ký ức theo dòng thời gian** nối các sự kiện theo quan hệ nhân quả và thời gian ([[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management](https://arxiv.org/abs/2406.10996#:~:text=to%20improve%20retrieval%20quality%2C%20we,human%20efforts%20when%20assessing%20agent)). Mỗi khi cần tạo phản hồi, mô hình sẽ lần theo _timeline_ các sự kiện liên quan, tạo nên một ngữ cảnh diễn giải vì sao người dùng có trạng thái hiện tại. Cách này nhấn mạnh tầm quan trọng của **ngữ cảnh tiến hóa**: ví dụ, thay vì chỉ biết “người dùng thích du lịch”, bot còn biết _lịch sử_ trước đây người dùng đã từng _sợ đi máy bay rồi sau đó mới thích du lịch_ – từ đó phản hồi tinh tế hơn. THEANINE cho thấy việc **liên kết các mảnh memory** thành chuỗi có thể giúp mô hình hiểu rõ sự thay đổi và nhất quán trong tính cách người dùng theo thời gian, mà không cần xóa ký ức cũ (vốn cũng mang thông tin hữu ích về thay đổi hành vi) ([[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management](https://arxiv.org/abs/2406.10996#:~:text=constantly%20memorize%20perceived%20information%20and,Along)) ([[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management](https://arxiv.org/abs/2406.10996#:~:text=conversations,human%20efforts%20when%20assessing%20agent)).

Cuối cùng, framework **LD-Agent** (Hao Li et al., 2024) đại diện cho xu hướng tích hợp _đa thành phần_: hệ thống này chia tác vụ thành **3 mô-đun** độc lập – (i) **nhận thức sự kiện** (event perception) để tóm tắt sự kiện chính mỗi phiên vào bộ nhớ dài hạn, (ii) **trích xuất persona** động cho cả người dùng và chatbot, và (iii) **tạo phản hồi** (response generation) có điều kiện trên ngữ cảnh hiện tại + bộ nhớ sự kiện truy hồi + persona đã nhận diện ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)). Bộ nhớ sự kiện của LD-Agent bao gồm hai phần: **bộ nhớ dài hạn** chứa lịch sử các sự kiện tóm tắt qua nhiều phiên (được lưu với dấu thời gian và phân đoạn theo chủ đề), và **bộ nhớ ngắn hạn** cho phiên hiện tại (đảm bảo thông tin mới nhất luôn được chú trọng) ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)) ([](https://openreview.net/pdf?id=lwCxVgVYoK#:~:text=200%20The%20event%20memory%20module,Specifically%2C%20this%20involves%20recording)). Khi phản hồi, hệ thống dùng một cơ chế truy hồi theo chủ đề để lấy ra các sự kiện cũ liên quan từ bộ nhớ dài hạn, kết hợp với nội dung ngắn hạn, cùng với hồ sơ persona đã cập nhật, rồi đưa vào mô-đun sinh. Cách tiếp cận module hóa này giúp dễ dàng tinh chỉnh từng phần (ví dụ thay mô hình tóm tắt sự kiện khác tốt hơn, hoặc áp dụng kỹ thuật LoRA để cập nhật persona linh hoạt), đồng thời cho thấy tầm quan trọng của việc **quản lý đồng thời kiến thức sự kiện và thông tin cá nhân** cho đối thoại dài hạn. Các thí nghiệm của LD-Agent chỉ ra rằng việc tích hợp cả hai loại bộ nhớ (sự kiện + persona) giúp chatbot đạt độ tự nhiên và chính xác cao hơn rõ rệt trên nhiều benchmark khác nhau ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=generation,various%20illustrative%20benchmarks%2C%20models%2C%20and)).

Tổng kết lại, cách tiếp cận nén và truy hồi ngữ cảnh hiện là hướng **ưu việt nhất** để hiện thực hóa trí nhớ dài hạn trong đối thoại. Nó tận dụng được sức mạnh của các mô hình pretrained (bằng cách cung cấp cho chúng “context mở rộng” khi cần), đồng thời tránh được các hạn chế về độ dài và quên thông tin do tự mô hình xử lý. Các nghiên cứu đang tiếp tục cải tiến ở cả khâu tóm tắt (để lưu đúng và đủ thông tin cần nhớ) lẫn khâu truy hồi (để tìm chính xác thông tin khi cần đến). Phần tiếp theo, chúng tôi sẽ so sánh một số hệ thống tiêu biểu thuộc hướng này và các baseline liên quan, trước khi đi vào đánh giá tổng thể trên các benchmark.

# So sánh các hệ thống tiêu biểu có bộ nhớ hội thoại

Để minh họa cụ thể sự khác biệt giữa các hướng tiếp cận và hiệu quả của trí nhớ dài hạn, bảng dưới đây so sánh **một số hệ thống tiêu biểu** từ trước đến nay:

- **MemNN (Memory Network, 2015)**: Đây là baseline kiểu (2) – mô hình có bộ nhớ khả vi. MemNN lưu trữ các phát ngôn trước dưới dạng vector trong bộ nhớ và sử dụng attention để chọn ra vector liên quan nhất khi trả lời ([[1410.3916] Memory Networks](https://arxiv.org/abs/1410.3916#:~:text=,chaining%20multiple%20supporting%20sentences%20to)). Mô hình này hoạt động tốt trên các bài toán giả lập ngắn (như bAbI) nhưng chưa được chứng minh hiệu quả trên đối thoại mở phức tạp. **Ưu điểm**: có khả năng suy luận nhiều bước nhờ đọc nhiều ô nhớ; **Nhược điểm**: khó huấn luyện end-to-end, không tự động cập nhật khi thông tin thay đổi (cần ghi đè thủ công).
    
- **Baseline không nhớ (No Memory)**: Đây là hệ thống kiểu trả lời độc lập từng lượt, ví dụ DrQA hoặc các model seq2seq không cung cấp lịch sử vào input. Hệ thống này hoàn toàn _quên_ mọi thứ sau mỗi lượt, nên **không thể** trả lời các câu hỏi phụ thuộc ngữ cảnh trước (vd: “Anh ấy” là ai?) và dễ trả lời lặp lại. Kết quả đối thoại thường kém tự nhiên và không duy trì được mạch thông tin.
    
- **Keep Me Updated (Bae et al., 2022)**: Hệ thống này thuộc hướng (3) – dùng bộ nhớ ngoài văn bản với cập nhật động. Nó tóm tắt thông tin người dùng sau mỗi phiên và thực hiện các phép cập nhật (thêm/xóa/thay thế) để bộ nhớ luôn nhất quán ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=Specifically%2C%20the%20memory%20management%20mechanism,%E2%80%9CJust%20got%20positive%20results%20from)). **Ưu điểm**: đảm bảo thông tin mới nhất luôn được ghi nhớ, tránh mâu thuẫn (nhờ chiến lược cập nhật) ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=find%20and%20eliminate%20the%20information,in%20sub%02sequent%20sessions%2C%20a%20relevant)); cho thấy _càng nhiều phiên_ thì bot càng nhớ tốt hơn và tương tác tự nhiên hơn ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=With%20extensive%20experiments%20and%20ablations%2C,date)). **Hạn chế**: chỉ lưu thông tin dưới dạng văn bản ngắn nên đôi khi mất chi tiết, và chưa xử lý tốt trường hợp nhiều thông tin khác loại (vì tất cả lưu chung một nơi).
    
- **LD-Agent (Hao Li et al., 2024)**: Đại diện tiên tiến cho hướng (3) với cấu trúc module hóa. LD-Agent có **bộ nhớ hai tầng** (dài hạn + ngắn hạn) và thêm **mô-đun persona** riêng ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)). Nhờ đó, nó không chỉ nhớ sự kiện mà còn duy trì được tính cách, thông tin nhân khẩu của cả người dùng và agent. **Ưu điểm**: kiến trúc linh hoạt, truy hồi theo chủ đề giúp tìm đúng sự kiện; persona động giúp đối thoại nhất quán vai; đạt kết quả tốt trên nhiều tác vụ (hỏi đáp, trò chuyện nhiều chủ đề) ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=generation,various%20illustrative%20benchmarks%2C%20models%2C%20and)). **Nhược điểm**: phức tạp, cần dữ liệu huấn luyện phong phú (ví dụ dữ liệu gán nhãn persona).
    
- **Theanine (NAACL 2025)**: Mô hình này cũng thuộc (3) nhưng với cách quản lý memory đặc biệt (đồ thị timeline) ([[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management](https://arxiv.org/abs/2406.10996#:~:text=to%20improve%20retrieval%20quality%2C%20we,human%20efforts%20when%20assessing%20agent)). **Ưu**: không xóa ký ức cũ, do đó sử dụng được cả bối cảnh lâu dài để suy luận sự thay đổi; dùng LLM tạo _memory timeline_ giúp giải thích được mạch sự kiện. Tuy nhiên, do không xóa nên **thách thức** là kiểm soát kích thước bộ nhớ và tránh retrieval nhầm từ những ký ức quá cũ không còn đúng.
    
- **MemoryBank (AAAI 2023)**: Hệ thống (3) với cơ chế quên có chọn lọc. **Ưu**: giống não người hơn – tự động làm mờ các memory ít quan trọng, củng cố memory quan trọng ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)). Ngoài ra, MemoryBank lưu trữ đa dạng: _log hội thoại chi tiết, bản tóm tắt sự kiện định kỳ, và hồ sơ người dùng_ (user portrait) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Storage%3A%20The%20Warehouse%20of,Memories)) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=level%20overviews%20of%20daily%20events,tailor%20its%20responses%20over%20time)), do đó cung cấp ngữ cảnh rất phong phú cho mô hình. Kết quả cho thấy chatbot tích hợp MemoryBank có thể **thể hiện sự thấu hiểu và ghi nhớ** vượt trội, như nhớ sở thích người dùng qua nhiều tuần lễ ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=psychological%20counseling%2C%20and%20secretarial%20assistance,the%20memory%2C%20thereby%20offering%20a)) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,tailor%20its%20responses%20over%20time)). Điểm cần cải tiến là đảm bảo cơ chế quên không vô tình loại bỏ thông tin cần thiết nếu thời gian kéo dài (cân bằng giữa quên và nhớ đúng).
    

Nhìn chung, **xu hướng phát triển** cho thấy sự chuyển dịch từ các mô hình không nhớ hoặc nhớ ngắn hạn (BiDAF++, DrQA) sang các hệ thống có bộ nhớ ngày càng thông minh hơn (Keep Me Updated, MemoryBank, Theanine, LD-Agent). Bảng so sánh trên nhấn mạnh vai trò của các thành phần như **cập nhật bộ nhớ** (update), **cấu trúc hóa thông tin** (theo sự kiện, theo persona), cũng như những phương pháp lấy cảm hứng từ tâm lý học (quên có chọn lọc) để nâng cao chất lượng tương tác dài hạn. Phần tiếp theo, chúng tôi sẽ giới thiệu các **benchmark và tiêu chí đánh giá** được đề xuất nhằm đo lường một cách hệ thống khả năng ghi nhớ dài hạn của các mô hình đối thoại này.

# Benchmark và tiêu chí đánh giá trí nhớ trong hội thoại

Để đánh giá khách quan khả năng ghi nhớ và sử dụng thông tin dài hạn, các nhà nghiên cứu đã xây dựng một số **benchmark chuyên biệt** cũng như sử dụng các bộ dữ liệu hội thoại có yếu tố nhớ. Dưới đây là các bộ dữ liệu và tiêu chí nổi bật:

- **LongMemEval (Wu et al., 2024)** – Đây là một bộ đánh giá toàn diện đầu tiên tập trung vào **5 kỹ năng trí nhớ lõi** của trợ lý chat ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,on%20memorizing%20information%20across%20sustained)). Năm kỹ năng đó bao gồm: (1) **Nhớ và trích thông tin** (Information Extraction) – kiểm tra xem mô hình có nhớ chính xác các chi tiết được đề cập trước đó hay không; (2) **Suy luận đa phiên** (Multi-session reasoning) – đánh giá khả năng kết nối thông tin qua nhiều phiên trò chuyện rời (ví dụ: người dùng nói A ở tuần trước và B ở tuần này, liệu bot có kết hợp A và B để trả lời?); (3) **Suy luận thời gian** (Temporal reasoning) – kiểm tra hiểu biết về trình tự thời gian, nguyên nhân-kết quả theo thời gian (ví dụ sự kiện X xảy ra sau Y thì hệ quả ra sao); (4) **Cập nhật kiến thức** (Knowledge updates) – đánh giá việc bot có sử dụng thông tin mới thay cho thông tin cũ khi chúng mâu thuẫn (giống bài toán cập nhật trí nhớ COVID ở trên); (5) **Abstention (từ chối)** – xem mô hình có biết từ chối trả lời khi không chắc do thiếu trí nhớ hay không (tránh trường hợp đoán bừa/hallucinate) ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,term)). LongMemEval gồm 500 câu hỏi được gài cẩn thận vào các lịch sử hội thoại dài, mỗi câu hỏi tương ứng kiểm tra một khía cạnh trên. Kết quả thực nghiệm cho thấy các chatbot hiện tại (kể cả mô hình lớn với ngữ cảnh dài) **giảm hiệu suất tới ~30%** khi phải ghi nhớ thông tin trải dài, so với các câu hỏi ngắn hạn ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=meticulously%20curated%20questions%20embedded%20within,augmented%20key)). Điều này khẳng định độ khó của bài toán và sự cần thiết của các phương pháp memory augmentation. LongMemEval hiện được coi là thước đo tiêu chuẩn, khuyến khích các nghiên cứu tương lai cải thiện cả 5 kỹ năng kể trên để tiến tới trợ lý đối thoại đáng tin cậy hơn ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=interactions,term)).
    
- **LOCOMO (Maharana et al., 2024)** – Là viết tắt của _Long Conversation Model_, đây được báo cáo là bộ dữ liệu hội thoại _dài nhất_ hiện nay, với trung bình **300 lượt thoại (9k token)** mỗi hội thoại ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=%28i%29%20LOCOMO%C2%A0%28Maharana%20et%C2%A0al,on%20the%20recently%20released%20official)). LOCOMO mô phỏng các cuộc trò chuyện liên tục, nhiều chủ đề, đòi hỏi mô hình phải duy trì tương tác mạch lạc trong thời gian rất dài. Để đánh giá, tác giả dùng GPT-4 sinh ra các câu hỏi kiểm tra về nội dung đã nói từ rất sớm trong phiên, nhằm xem bot có nhớ hay không ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=%28i%29%20LOCOMO%C2%A0%28Maharana%20et%C2%A0al,on%20the%20recently%20released%20official)). Ngoài ra, LOCOMO còn đo lường mức độ trôi chảy và nhất quán qua thước đo **GPT4Score** và các chỉ số ngôn ngữ tự nhiên (BLEU, ROUGE) cho phản hồi của mô hình ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=long,in%20performance%20improvements%20up%20to)) ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=Methods%20LOCOMO%20Long,44)). Cùng với LOCOMO, một số biến thể như **Long-MT-Bench+** cũng được dùng – đây là mở rộng của bộ đánh giá Multi-Turn Dialogue (MT-Bench) dành riêng cho hội thoại dài. Các kết quả baseline trên LOCOMO cho thấy nếu mô hình chỉ dùng lịch sử rất ngắn (hoặc không lịch sử) thì điểm số trả lời đúng rất thấp (~25-50), trong khi dùng full history nâng lên ~54 ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=match%20at%20L389%20LOCOMO%20Zero,77%203%2C288)). Tuy nhiên, dùng full history phiến diện cũng gây mỏi model (13,000 token) và không nhất thiết tối ưu. Do vậy LOCOMO được dùng để thử nghiệm các chiến lược nhớ: thí dụ SeCom trên LOCOMO đạt **GPT4Score ~69**, cao hơn hẳn so với mô hình không module nhớ (~24) ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=LOCOMO%20Zero%20History%2024,77%203%2C288)) ([On Memory Construction and Retrieval for Personalized Conversational Agents](https://arxiv.org/html/2502.05589v2#:~:text=Methods%20LOCOMO%20Long,44)). Điều này xác nhận lợi ích rõ rệt của memory đối với hội thoại siêu dài.
    
- **Các bộ dữ liệu personalized và multi-session**: Trước khi có các benchmark trên, một số bộ dữ liệu hội thoại được tạo ra nhằm kiểm tra một phần khía cạnh của trí nhớ. **Persona-Chat (Zhang et al., 2018)** cung cấp cho mỗi nhân vật một hồ sơ sở thích (5 câu mô tả) và yêu cầu mô hình trò chuyện giữ đúng persona này. Đây là kiểm tra khả năng **nhớ thông tin hồ sơ tĩnh** – gần với memory ngắn hạn (vì persona không đổi). **MuTual (Cui et al., 2020)** và **DSTC7,8** cung cấp các đoạn hội thoại yêu cầu suy luận logic giữa các lượt – gián tiếp đòi hỏi nhớ nội dung trước. **QuAC, CoQA (2018)** như đã đề cập, đánh giá khả năng trả lời dựa vào nhiều lượt hỏi trước (context co-reference). Tuy nhiên, các dataset này thường chỉ kéo dài tối đa vài chục lượt trong một phiên, và không đánh giá xuyên phiên hay cập nhật. Gần đây, một số dataset hướng đến **đa phiên**: ví dụ **MSC (Multi-Session Chat)** (Xu et al., 2022) nối 2-3 phiên PersonaChat lại để xem bot có nhớ thông tin giữa các phiên; hay **CareCall-Mem** (Bae et al., 2022) – dữ liệu tiếng Hàn mà nhóm Keep Me Updated xây dựng – gồm 5 phiên trò chuyện giữa bot và một người dùng hư cấu với các thông tin cá nhân thay đổi theo thời gian (sức khỏe, thói quen) ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=3,We%20extend%20this)) ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=single,Sessions%207%2C665%20Session%201%202%2C812)). Các dataset này phục vụ huấn luyện và đánh giá mô hình trong bối cảnh **thông tin người dùng thay đổi**: ví dụ phiên 1 nói “ghét vận động”, phiên 3 lại nói “đang học bơi” thì bot phải hiểu sở thích đã thay đổi. Tiêu chí đánh giá gồm độ tự nhiên, tính gắn kết, và quan trọng là **độ chính xác của thông tin** mà bot nói ra so với hồ sơ thực tế (tránh nhầm thông tin cũ).
    
- **Tiêu chí đánh giá**: Dựa trên các benchmark trên, ta có thể liệt kê những tiêu chí chính để đánh giá chất lượng trí nhớ dài hạn của hệ thống hội thoại:
    
    - _Chính xác thông tin đã nhớ (Memory Recall)_: Kiểm tra tỉ lệ thông tin đúng được bot nhắc lại khi cần. Ví dụ, user đã nói họ sinh năm 1990, sau 10 lượt bot đề cập lại đúng năm sinh hay không. Tiêu chí này đo bằng câu hỏi trực tiếp (như LongMemEval) hoặc so khớp với log quá khứ.
        
    - _Phản hồi nhất quán, không ảo giác (Consistency & No-hallucination)_: Đánh giá xem bot có mâu thuẫn với chính nó hoặc với thực tế đã biết không, và có bịa đặt thông tin không có trong bộ nhớ không. Nếu bot _quên_ một chi tiết và tự chế ra, đó là điểm trừ lớn. Thước đo có thể bằng kiểm tra logic (ví dụ Persona-Chat yêu cầu không nói sai persona), hoặc nhờ đánh giá của mô hình/human xem câu trả lời có căn cứ quá khứ hay không.
        
    - _Cập nhật kiến thức kịp thời (Knowledge Update Accuracy)_: Khi người dùng cung cấp thông tin mới hoặc đính chính, bot có phản ánh đúng sự thay đổi trong các lượt sau không. Tiêu chí này thường đánh giá theo kịch bản: ví dụ như bài toán COVID test ở trên – sau khi user báo dương tính, bot phải quên thông tin “chưa xét nghiệm” trước đó. Có thể đo bằng truy vấn sau update xem bot trả lời dựa trên thông tin nào.
        
    - _Suy luận theo dòng thời gian (Temporal Reasoning)_: Bot có hiểu mối quan hệ thời gian giữa các sự kiện trong trí nhớ không. Ví dụ, user nói “năm 2020 tôi tốt nghiệp”, sau đó hỏi “2 năm sau tôi làm gì” – bot phải biết 2 năm sau 2020 là 2022 và tìm trong memory xem 2022 có sự kiện gì (hoặc trả lời chưa biết nếu không có). Khả năng này thường đo bằng các câu hỏi yêu cầu kết hợp mốc thời gian (như trong LongMemEval) ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,on%20memorizing%20information%20across%20sustained)).
        
    - _Khả năng từ chối khi không nhớ (Abstention)_: Một hệ thống tốt cần biết giới hạn trí nhớ của mình, tức là nếu thông tin không có trong bộ nhớ thì nên xin lỗi hoặc từ chối hơn là bịa. Tiêu chí này đánh giá tỷ lệ bot **không đoán bừa**. LongMemEval đưa ra các tình huống mà câu hỏi ngoài phạm vi những gì đã nói, yêu cầu bot phải phản hồi kiểu “Tôi không nhớ rõ…” thay vì cung cấp thông tin sai ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,term)).
        

Ngoài ra, các tiêu chí tổng quan như **độ hài lòng người dùng, độ tự nhiên của hội thoại, điểm đánh giá của giám khảo** cũng rất quan trọng, nhưng chúng chịu ảnh hưởng nhiều yếu tố ngoài trí nhớ (như kỹ năng ngôn ngữ chung của mô hình). Do đó, các benchmark chuyên biệt cố gắng cô lập ảnh hưởng của trí nhớ để đánh giá công bằng giữa các giải pháp.

# Hướng mở rộng và kết luận

**Trí nhớ dài hạn cho hệ thống đối thoại** vẫn là một bài toán mở với nhiều hướng nghiên cứu tiềm năng. Dựa trên các xu hướng hiện tại, có thể gợi ý một số hướng phát triển chính sau:

- **Kết hợp chặt chẽ giữa truy hồi và cập nhật tri thức**: Hiện nay, retrieval augmented generation (RAG) đã phổ biến trong QA mở, nhưng thường với _knowledge base_ tĩnh. Mở rộng hơn, ta có thể tích hợp RAG vào đối thoại sao cho **kho tri thức được cập nhật liên tục trong quá trình trò chuyện**. Ví dụ, khi người dùng cung cấp một thông tin mới, hệ thống ngay lập tức thêm nó vào _bộ nhớ tri thức_ và các lượt sau truy hồi có thể lấy ra. Điều này đòi hỏi giải quyết bài toán đồng bộ giữa thành phần ghi nhớ và thành phần tìm kiếm. Một hướng là phát triển các phương pháp **index động**: cập nhật chỉ mục bộ nhớ theo thời gian thực, hoặc sử dụng mô hình học tăng cường để quyết định khi nào cần _re-index_.
    
- **Truy hồi thích ứng và có hướng dẫn**: Thay vì luôn truy hồi một cách máy móc top-k đoạn giống như hiện nay, mô hình có thể học cách **đặt truy vấn thông minh** hoặc **chọn lọc** tùy tình huống. Chẳng hạn, nếu câu hỏi của người dùng rất rõ ràng (như hỏi tên đã cho trước đó), một truy vấn thẳng sẽ hiệu quả; nhưng nếu câu hỏi mơ hồ, mô hình có thể tự sinh ra một truy vấn rõ hơn dựa trên ngữ cảnh – tương tự kỹ thuật _query rewriting_ ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Query%20Rewriting)). Ngoài ra, mô hình nên học _khi nào_ thì cần truy hồi: đôi khi, câu hỏi hiện tại không liên quan gì đến quá khứ, việc truy hồi chỉ thêm nhiễu. Có thể dùng một module phụ (như một classifier) để quyết định có truy hồi memory không ở mỗi lượt. Một ý tưởng khác là cho chính LLM **hướng dẫn việc truy hồi**: ví dụ trước khi trả lời, mô hình tự suy luận "Để trả lời, tôi cần nhớ X", sau đó dùng suy luận này làm chìa khóa tìm kiếm bộ nhớ. Đây là một dạng _chain-of-thought for retrieval_ đầy hứa hẹn.
    
- **Sử dụng mô hình ngôn ngữ phụ trợ cho quản lý trí nhớ**: Thay vì các rule cứng (như 4 thao tác của Keep Me Updated), ta có thể dùng một LLM nhỏ hoặc các prompt đặc biệt cho chính LLM lớn để quản lý memory. Ví dụ, có thể triển khai một _“Memory Manager Agent”_ chạy song song: agent này dùng LLM để định kỳ đọc lịch sử và viết tóm tắt, lưu vào vector DB; khi cần thì hỗ trợ truy vấn vector DB và cung cấp kết quả cho LLM chính. Cách tiếp cận kiến trúc agent này đã được Park et al. (2023) thử nghiệm trong **Generative Agents**, nơi nhiều agent LLM tương tác với nhau và có bộ nhớ sự kiện được ghi lại và suy diễn bằng LLM. Một ứng dụng khác là dùng LLM để **đánh giá và chỉnh sửa** memory: ví dụ dùng GPT-4 đọc toàn bộ memory log và phát hiện mâu thuẫn hoặc lỗi để sửa (một dạng reviewer). Nhìn chung, tận dụng khả năng ngôn ngữ đa năng của LLM cho việc quản trị trí nhớ có thể đem lại linh hoạt hơn so với cách làm thuần heuristic.
    
- **Mở rộng sang đa mô hình và tri thức thế giới**: Trí nhớ hội thoại không chỉ gồm lời thoại – trong nhiều ứng dụng, nó cần nhớ cả các **thông tin thị giác, cảm biến, hay tri thức ngoài**. Hướng mở là tích hợp **bộ nhớ chung cho đa mô hình**: ví dụ một robot trợ lý nhà thông minh cần nhớ hôm qua camera thấy gì, ai đã ghé thăm, đồ vật đặt ở đâu... cùng với hội thoại với chủ nhà. Điều này đặt ra bài toán lưu trữ và truy hồi các **đại diện đa mô hình** (hình ảnh, âm thanh) bên cạnh văn bản. Tương tự, kết hợp **knowledge graph** hoặc cơ sở tri thức vào memory: ví dụ khi người dùng nói sở thích, bot có thể lưu vào một _knowledge graph node_ về người dùng, liên kết với các node hoạt động tương ứng. Việc kết hợp cấu trúc tri thức có thể giúp bot suy luận logic và nhất quán hơn (tránh mâu thuẫn thực tế). Một hướng là mỗi khi memory update, đồng thời cập nhật knowledge graph, và dùng graph embedding để hỗ trợ retrieval song song.
    
- **Đánh giá và giảm thiểu nhiễu do trí nhớ sai**: Khi tích hợp bộ nhớ, một nguy cơ là _nhớ sai hoặc nhớ mơ hồ_ có thể dẫn đến phản hồi sai (hallucination do memory). Do đó, cần cơ chế **đánh giá độ tin cậy của memory**. Một hướng là kèm theo mỗi mẩu memory một độ tin cậy (confidence score) và thời gian, để mô hình ưu tiên dùng thông tin mới và có độ tin cậy cao. Nếu memory quá cũ, mô hình có thể cảnh báo. Một hướng khác là huấn luyện mô hình **phát hiện mâu thuẫn** giữa memory và message hiện tại: nếu phát hiện user nói điều trái ngược hẳn với memory cũ, có thể kích hoạt một _quy trình xác minh_, hỏi lại người dùng để chắc chắn trước khi cập nhật.
    

Tóm lại, **hệ thống đối thoại tích hợp trí nhớ dài hạn** đang dần trở nên khả thi nhờ các tiến bộ trong cả mô hình ngôn ngữ lớn lẫn kỹ thuật quản lý tri thức. Từ những mô hình QA đơn lượt đơn giản, chúng ta đã chứng kiến sự ra đời của các chatbot có khả năng ghi nhớ hàng trăm lượt thoại, cá nhân hóa theo người dùng, và cập nhật hiểu biết theo thời gian. Dù vẫn còn những thách thức về tối ưu và độ tin cậy, hướng nghiên cứu này hứa hẹn đem lại các trợ lý ảo **nhớ lâu, hiểu sâu và phản hồi tự nhiên** hơn – một bước tiến lớn tới **AI đối thoại mang tính cá nhân và đáng tin cậy** trong tương lai gần. Các nghiên cứu mới như LongMemEval đang tạo nền tảng để **đánh giá có hệ thống** các tiến bộ, còn các ý tưởng kết hợp memory và LLM (MemoryBank, THEANINE, LD-Agent) đang mở đường cho thế hệ mô hình hội thoại thông minh kế tiếp. Chúng ta có thể kỳ vọng trong tương lai, sự kết hợp giữa **cửa sổ ngữ cảnh lớn** và **bộ nhớ ngoài linh hoạt** sẽ giúp xóa nhòa ranh giới về trí nhớ trong đối thoại, cho phép các hệ thống AI trò chuyện một cách mạch lạc và hiểu biết qua _nhiều tháng, nhiều năm_ tương tác với con người.

**Tài liệu tham khảo:**

1. Wu, D. _et al._ (2024). _LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory_. **ICLR 2025 (preprint)** ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,term)) ([[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813#:~:text=meticulously%20curated%20questions%20embedded%20within,augmented%20key)).
    
2. Qu, C. _et al._ (2020). _Open-Retrieval Conversational Question Answering_. **SIGIR 2020** ([[2005.11364] Open-Retrieval Conversational Question Answering](https://arxiv.org/abs/2005.11364#:~:text=retrieval%20conversational%20question%20answering%20,the%20reranker%20component%20contributes%20to)).
    
3. Bae, S. _et al._ (2022). _Keep Me Updated! Memory Management in Long-term Conversations_. **Findings of EMNLP 2022** ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=Specifically%2C%20the%20memory%20management%20mechanism,%E2%80%9CJust%20got%20positive%20results%20from)) ([](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=find%20and%20eliminate%20the%20information,in%20sub%02sequent%20sessions%2C%20a%20relevant)).
    
4. Li, H. _et al._ (2025). _Hello Again! LLM-powered Personalized Agent for Long-term Dialogue (LD-Agent)_. **NAACL 2025 (to appear)** ([[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)).
    
5. Zhong, W. _et al._ (2023). _MemoryBank: Enhancing Large Language Models with Long-Term Memory_. **arXiv:2305.10250** ([[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)) ([Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Updating)).
    
6. Ong, K.T. _et al._ (2025). _THEANINE: Timeline-based Memory Management for Lifelong Dialogue Agents_. **NAACL 2025 (to appear)** ([[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management](https://arxiv.org/abs/2406.10996#:~:text=to%20improve%20retrieval%20quality%2C%20we,human%20efforts%20when%20assessing%20agent)).
    
7. Weston, J. _et al._ (2015). _Memory Networks_. **ICLR 2015** ([[1410.3916] Memory Networks](https://arxiv.org/abs/1410.3916#:~:text=,chaining%20multiple%20supporting%20sentences%20to)).
    
8. Graves, A. _et al._ (2016). _Hybrid computing using a neural network with dynamic external memory (DNC)_. **Nature 538, 471–476 (2016)** ([Differentiable neural computer - Wikipedia](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=DNC%20indirectly%20takes%20inspiration%20from,by%20finding%20a%20%2052)).
    
9. Seo, M. _et al._ (2017). _Bidirectional Attention Flow for Machine Comprehension (BiDAF)_. **ICLR 2017** ([BERT with History Answer Embedding for Conversational Question Answering](https://arxiv.org/pdf/1905.05412#:~:text=4,representation%20generated%20when%20answering%20previous)).
    
10. Chen, D. _et al._ (2017). _Reading Wikipedia to Answer Open-Domain Questions (DrQA)_. **ACL 2017** ([BERT with History Answer Embedding for Conversational Question Answering](https://arxiv.org/pdf/1905.05412#:~:text=,JASIS%2C%2038%3A389%E2%80%93404%2C%201987)).




```
Trích dẫn

[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

BERT with History Answer Embedding for Conversational Question Answering

4.2.1 Competing Methods. We consider all the methods on the QuAC leaderboard as baselines. The competing methods are: • BiDAF++ [3]: BiDAF++ augments BiDAF [14] with self-attention and contextualized embeddings. • BiDAF++ w/ 2-Context [3]: It incorporates 2 history turns in BiDAF++ by encoding the dialog turn # in question embeddings and concatenating marker embeddings to passage embeddings. • FlowQA [7]: It considers conversation history by integrating intermediate representation generated when answering previous

](https://arxiv.org/pdf/1905.05412#:~:text=4,representation%20generated%20when%20answering%20previous)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

BERT with History Answer Embedding for Conversational Question Answering

[2] D. Chen, A. Fisch, J. Weston, and A. Bordes. Reading Wikipedia to Answer Open-Domain Questions. In ACL, 2017. [3] E. Choi, H. He, M. Iyyer, M. Yatskar, W. Yih, Y. Choi, P. Liang, and L. S. Zettlemoyer. QuAC: Question Answering in Context. In EMNLP, 2018. [4] W. B. Croft and R. H. Thompson. I3R: A new approach to the design of document retrieval systems. JASIS, 38:389–404, 1987.

](https://arxiv.org/pdf/1905.05412#:~:text=,JASIS%2C%2038%3A389%E2%80%93404%2C%201987)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

integrated memory components to track user-assistant chat histories, enabling more accurate and personalized responses. However, their long-term memory capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs

](https://arxiv.org/abs/2410.10813#:~:text=integrated%20memory%20components%20to%20track,context%20LLMs)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key

](https://arxiv.org/abs/2410.10813#:~:text=meticulously%20curated%20questions%20embedded%20within,augmented%20key)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

> Abstract:We describe a new class of learning models called memory networks. Memory networks reason with inference components combined with a long-term memory component; they learn how to use these jointly. The long-term memory can be read and written to, with the goal of using it for prediction. We investigate these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to

](https://arxiv.org/abs/1410.3916#:~:text=,chaining%20multiple%20supporting%20sentences%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to answer questions that require understanding the intension of verbs.

](https://arxiv.org/abs/1410.3916#:~:text=these%20models%20in%20the%20context,understanding%20the%20intension%20of%20verbs)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

In artificial intelligence , a differentiable neural computer (DNC) is a memory augmented 47 architecture (MANN), which is typically (but not by definition) recurrent in its implementation. The model was published in 2016 by Alex Graves et al. of 49.[ 1 ]

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=In%20artificial%20intelligence%20%2C%20a,1)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

DNC indirectly takes inspiration from Von-Neumann architecture , making it likely to outperform conventional architectures in tasks that are fundamentally algorithmic that cannot be learned by finding a 52.

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=DNC%20indirectly%20takes%20inspiration%20from,by%20finding%20a%20%2052)[

![Favicon](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)en.wikipedia.org

Differentiable neural computer - Wikipedia

So far, DNCs have been demonstrated to handle only relatively simple tasks, which can be solved using conventional programming. But DNCs don't need to be programmed for each problem, but can instead be trained. This attention span allows the user to feed complex data structures such as 54 sequentially, and recall them for later use. Furthermore, they can learn aspects of symbolic reasoning and apply it to working memory. The researchers who published the method see promise that DNCs can be trained to perform complex, structured tasks[ 1 ][ 2 ] and address big-data applications that require some sort of reasoning, such as generating video commentaries or semantic text

](https://en.wikipedia.org/wiki/Differentiable_neural_computer#:~:text=So%20far%2C%20DNCs%20have%20been,video%20commentaries%20or%20semantic%20text)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[1410.3916] Memory Networks

memory component; they learn how to use these jointly. The long-term memory can be read and written to, with the goal of using it for prediction. We investigate these models in the context of question answering (QA) where the long-term memory effectively acts as a (dynamic) knowledge base, and the output is a textual response. We evaluate them on a large-scale QA task, and a smaller, but more complex, toy task generated from a simulated world. In the latter, we show the reasoning power of such models by chaining multiple supporting sentences to

](https://arxiv.org/abs/1410.3916#:~:text=memory%20component%3B%20they%20learn%20how,chaining%20multiple%20supporting%20sentences%20to)[

openreview.net

Language model with Plug-in Knowldge Memory | OpenReview

of knowledge PLM needs to solve certain task. In this paper, we introduce PlugLM, a pre-training model with differentiable plug-in memory(DPM). The key intuition behind is to decouple the knowledge storage from model parameters with an editable and scalable key-value memory and leverage knowledge in an explainable manner by knowledge retrieval in the DPM. We conduct extensive experiments under various settings to justify this design choice. In domain adaptation setting, PlugLM could be easily adapted to different domains with plugable in-domain memory---obtaining 3.95 F1 improvements across four domains, without any in-domain training. PlugLM could also keep absorbing new knowledge

](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=of%20knowledge%20PLM%20needs%20to,also%20keep%20absorbing%20new%20knowledge)[

openreview.net

Language model with Plug-in Knowldge Memory | OpenReview

adaptation setting, PlugLM could be easily adapted to different domains with plugable in-domain memory---obtaining 3.95 F1 improvements across four domains, without any in-domain training. PlugLM could also keep absorbing new knowledge after pre-training is done by knowledge updating operation in the DPM without re-training. Finally, we show that by incorporating training samples into DPM with knowledge prompting, PlugLM could further be improved by the instruction of in-task knowledge.

](https://openreview.net/forum?id=Plr5l7r0jY6#:~:text=adaptation%20setting%2C%20PlugLM%20could%20be,task%20knowledge)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

retrieval conversational question answering (ORConvQA) setting, where we learn to retrieve evidence from a large collection before extracting answers, as a further step towards building functional conversational search systems. We create a dataset, OR-QuAC, to facilitate research on ORConvQA. We build an end- to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our system can make a substantial improvement when we enable history modeling in all system components. Moreover, we show that the reranker component contributes to

](https://arxiv.org/abs/2005.11364#:~:text=retrieval%20conversational%20question%20answering%20,the%20reranker%20component%20contributes%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

passage. These simplifications neglect the fundamental role of retrieval in conversational search. To address this limitation, we introduce an open- retrieval conversational question answering (ORConvQA) setting, where we learn to retrieve evidence from a large collection before extracting answers, as a further step towards building functional conversational search systems. We create a dataset, OR-QuAC, to facilitate research on ORConvQA. We build an end- to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our

](https://arxiv.org/abs/2005.11364#:~:text=passage,We%20further%20show%20that%20our)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2005.11364] Open-Retrieval Conversational Question Answering

to-end system for ORConvQA, featuring a retriever, a reranker, and a reader that are all based on Transformers. Our extensive experiments on OR-QuAC demonstrate that a learnable retriever is crucial for ORConvQA. We further show that our system can make a substantial improvement when we enable history modeling in all system components. Moreover, we show that the reranker component contributes to

](https://arxiv.org/abs/2005.11364#:~:text=to,the%20reranker%20component%20contributes%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

interlocutors revealed in the previous conversation is abstractively summarized and stored in memory. Specifically, the memory management mechanism decides which information to keep in memory. For this purpose, we define four pairwise operations (PASS, REPLACE, APPEND, and DELETE) to find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=interlocutors%20revealed%20in%20the%20previous,in%02coming%20summary%20is%20%E2%80%9CJust%20got)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from COVID test”, the two sentences are contradictory, in which the former needs to be replaced in memory by the latter. Through this process, only valid information remains in new memory. Then, in subsequent sessions, a relevant information from this memory is retrieved and given as additional condition for generating chatbot

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=For%20example%2C%20if%20the%20previous,additional%20condi%02tion%20for%20generating%20chatbot)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

Specifically, the memory management mechanism decides which information to keep in memory. For this purpose, we define four pairwise operations (PASS, REPLACE, APPEND, and DELETE) to find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=Specifically%2C%20the%20memory%20management%20mechanism,%E2%80%9CJust%20got%20positive%20results%20from)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

find and eliminate the information that can cause confusion or redundancy in later conversations. For example, if the previous memory sentence is “Haven’t got COVID tested yet” and the new incoming summary is “Just got positive results from COVID test”, the two sentences are contradictory, in which the former needs to be replaced in memory by the latter. Through this process, only valid information remains in new memory. Then, in subsequent sessions, a relevant

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=find%20and%20eliminate%20the%20information,in%20sub%02sequent%20sessions%2C%20a%20relevant)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

With extensive experiments and ablations, we show that the proposed memory management mechanism becomes more advantageous in terms of memorability as the sessions proceed, leading to better engagingness and humanness in multisession dialogues. Our contributions are as follows: 1. We make a step towards long-term conversations with dynamic memory that must be kept up-to-date.

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=With%20extensive%20experiments%20and%20ablations%2C,date)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

long conversation, these chatbots fail to recall past information and tend to generate inconsistent responses. To address this, we propose to recursively generate summaries/ memory using large language models (LLMs) to enhance long- term memory ability. Specifically, our method first stimulates LLMs to memorize small dialogue contexts and then recursively produce new memory using previous memory and following contexts. Finally, the chatbot can easily generate a highly consistent response with the help of the latest memory. We evaluate our method on both open and closed LLMs, and the experiments on the widely-used public dataset show that our method can generate more consistent responses in a long-

](https://arxiv.org/abs/2308.15022#:~:text=long%20conversation%2C%20these%20chatbots%20fail,consistent%20responses%20in%20a%20long)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2308.15022] Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models

consistent response with the help of the latest memory. We evaluate our method on both open and closed LLMs, and the experiments on the widely-used public dataset show that our method can generate more consistent responses in a long- context conversation. Also, we show that our strategy could nicely complement both long-context (e.g., 8K and 16K) and retrieval-enhanced LLMs, bringing further long-term dialogue performance. Notably, our method is a potential solution to enable the LLM to model the extremely long context. The code and scripts will be released later.

](https://arxiv.org/abs/2308.15022#:~:text=consistent%20response%20with%20the%20help,scripts%20will%20be%20released%20later)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

To deliver coherent and personalized experiences in long-term conversations, existing approaches typically perform retrieval augmented response generation by constructing memory banks from conversation history at either the turn-level, session-level, or through summarization techniques. In this paper, we present two key findings: (1) The granularity of memory unit matters: Turn-level, session-level, and summarization-based methods each exhibit limitations in both memory retrieval accuracy and the semantic quality of the retrieved content. (2) Prompt compression methods, such as LLMLingua-2, can effectively serve as a denoising mechanism, enhancing memory retrieval accuracy across different granularities.

](https://arxiv.org/html/2502.05589v2#:~:text=To%20deliver%20coherent%20and%20personalized,retrieval%20accuracy%20across%20different%20granularities)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

Building on these insights, we propose SeCom, a method that constructs the memory bank at segment level by introducing a conversation Se gmentation model that partitions long-term conversations into topically coherent segments, while applying Com pression based denoising on memory units to enhance memory retrieval. Experimental results show that SeCom exhibits a significant performance advantage over baselines on long-term conversation benchmarks LOCOMO and Long-MT-Bench+. Additionally, the proposed conversation segmentation method demonstrates superior performance on dialogue segmentation datasets such as DialSeg711, TIAGE, and SuperDialSeg.

](https://arxiv.org/html/2502.05589v2#:~:text=Building%20on%20these%20insights%2C%20we,as%20DialSeg711%2C%20TIAGE%2C%20and%20SuperDialSeg)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key expansion for indexing, and time-aware query expansion for refining the search scope. Extensive experiments show that these optimizations greatly improve both memory recall and downstream question answering on LongMemEval. Overall, our study provides valuable resources and guidance for advancing the long-term

](https://arxiv.org/abs/2410.10813#:~:text=showing%20a%2030,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://ar5iv.labs.arxiv.org&sz=32)ar5iv.labs.arxiv.org

[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory

personality over time by synthesizing information from previous interactions. To mimic anthropomorphic behaviors and selectively preserve memory, MemoryBank incorporates a memory updating mechanism, inspired by the Ebbinghaus Forgetting Curve theory. This mechanism permits the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory, thereby offering a more human-like memory mechanism and enriched user experience. MemoryBank is versatile in accommodating both closed-source models like ChatGPT and open- source models such as ChatGLM. To validate MemoryBank’s effectiveness, we exemplify its application through the creation of an LLM-based chatbot named

](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=personality%20over%20time%20by%20synthesizing,based%20chatbot%20named)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Memory Updating

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Updating)[

![Favicon](https://www.google.com/s2/favicons?domain=https://ar5iv.labs.arxiv.org&sz=32)ar5iv.labs.arxiv.org

[2305.10250] MemoryBank: Enhancing Large Language Models with Long-Term Memory

psychological counseling, and secretarial assistance. Recognizing the necessity for long-term memory, we propose MemoryBank, a novel memory mechanism tailored for LLMs. MemoryBank enables the models to summon relevant memories, continually evolve through continuous memory updates, comprehend, and adapt to a user’s personality over time by synthesizing information from previous interactions. To mimic anthropomorphic behaviors and selectively preserve memory, MemoryBank incorporates a memory updating mechanism, inspired by the Ebbinghaus Forgetting Curve theory. This mechanism permits the AI to forget and reinforce memory based on time elapsed and the relative significance of the memory, thereby offering a

](https://ar5iv.labs.arxiv.org/html/2305.10250#:~:text=psychological%20counseling%2C%20and%20secretarial%20assistance,the%20memory%2C%20thereby%20offering%20a)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

* Selective Forgetting: Drawing inspiration from the Ebbinghaus Forgetting Curve, MemoryBank ensures that not all stored memories remain equally strong. Over time, if a memory isn’t recalled or reinforced, its strength decays and it may eventually be pruned from active storage. This selective forgetting keeps the memory bank relevant and uncluttered. * Reinforcement of Key Memories: Conversely, memories that are frequently accessed are reinforced. Each time a memory is recalled, its “strength” is boosted, ensuring that important details persist over longer periods — mirroring how human memory works through repeated retrieval.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,memory%20works%20through%20repeated%20retrieval)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

to improve retrieval quality, we argue that such memories provide rich, important contextual cues for RG (e.g., changes in user behaviors) in long-term conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along with THEANINE, we introduce TeaFarm, a counterfactual-driven evaluation scheme, addressing the limitation of G-Eval and human efforts when assessing agent

](https://arxiv.org/abs/2406.10996#:~:text=to%20improve%20retrieval%20quality%2C%20we,human%20efforts%20when%20assessing%20agent)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

constantly memorize perceived information and properly retrieve it for response generation (RG). While prior studies focus on getting rid of outdated memories to improve retrieval quality, we argue that such memories provide rich, important contextual cues for RG (e.g., changes in user behaviors) in long-term conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along

](https://arxiv.org/abs/2406.10996#:~:text=constantly%20memorize%20perceived%20information%20and,Along)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.10996] Towards Lifelong Dialogue Agents via Timeline-based Memory Management

conversations. We present THEANINE, a framework for LLM-based lifelong dialogue agents. THEANINE discards memory removal and manages large-scale memories by linking them based on their temporal and cause-effect relation. Enabled by this linking structure, THEANINE augments RG with memory timelines - series of memories representing the evolution or causality of relevant past events. Along with THEANINE, we introduce TeaFarm, a counterfactual-driven evaluation scheme, addressing the limitation of G-Eval and human efforts when assessing agent

](https://arxiv.org/abs/2406.10996#:~:text=conversations,human%20efforts%20when%20assessing%20agent)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue

the Long-term Dialogue Agent (LD-Agent), which incorporates three independently tunable modules dedicated to event perception, persona extraction, and response generation. For the event memory module, long and short-term memory banks are employed to separately focus on historical and ongoing sessions, while a topic- based retrieval mechanism is introduced to enhance the accuracy of memory retrieval. Furthermore, the persona module conducts dynamic persona modeling for both users and agents. The integration of retrieved memories and extracted personas is subsequently fed into the generator to induce appropriate responses. The effectiveness, generality, and cross-domain capabilities of LD-Agent are

](https://arxiv.org/abs/2406.05925#:~:text=the%20Long,Agent%20are)[

openreview.net

200 The event memory module is designed to perceive 201 historical events to generate coherent responses 202 across interval time. As shown in Figure 2, this 203 event memory module is segmented into two major 204 sub-modules that focus separately on long-term 205 and short-term memory. 206 2.2.1 Long-term Memory 207 Memory Storage. The long-term memory mod208 ule aims to extract and encode events from past 209 sessions. Specifically, this involves recording

](https://openreview.net/pdf?id=lwCxVgVYoK#:~:text=200%20The%20event%20memory%20module,Specifically%2C%20this%20involves%20recording)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2406.05925] Hello Again! LLM-powered Personalized Agent for Long-term Dialogue

generation. For the event memory module, long and short-term memory banks are employed to separately focus on historical and ongoing sessions, while a topic- based retrieval mechanism is introduced to enhance the accuracy of memory retrieval. Furthermore, the persona module conducts dynamic persona modeling for both users and agents. The integration of retrieved memories and extracted personas is subsequently fed into the generator to induce appropriate responses. The effectiveness, generality, and cross-domain capabilities of LD-Agent are empirically demonstrated across various illustrative benchmarks, models, and

](https://arxiv.org/abs/2406.05925#:~:text=generation,various%20illustrative%20benchmarks%2C%20models%2C%20and)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Memory Storage: The Warehouse of Memories

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Memory%20Storage%3A%20The%20Warehouse%20of,Memories)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

level overviews of daily events and key interactions, much like how humans remember “the gist” of an experience rather than every minute detail. * User Portraits: Beyond mere conversation logs, MemoryBank constructs dynamic user portraits. These profiles encapsulate a user’s personality traits, recurring preferences, and evolving interests, enabling the LLM to tailor its responses over time.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=level%20overviews%20of%20daily%20events,tailor%20its%20responses%20over%20time)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

* User Portraits: Beyond mere conversation logs, MemoryBank constructs dynamic user portraits. These profiles encapsulate a user’s personality traits, recurring preferences, and evolving interests, enabling the LLM to tailor its responses over time.

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=,tailor%20its%20responses%20over%20time)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained

](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,on%20memorizing%20information%20across%20sustained)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

capabilities in sustained interactions remain underexplored. We introduce LongMemEval, a comprehensive benchmark designed to evaluate five core long-term memory abilities of chat assistants: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. With 500 meticulously curated questions embedded within freely scalable user-assistant chat histories, LongMemEval presents a significant challenge to existing long- term memory systems, with commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions. We then present a unified framework that breaks down the long-term

](https://arxiv.org/abs/2410.10813#:~:text=capabilities%20in%20sustained%20interactions%20remain,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

[2410.10813] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

interactions. We then present a unified framework that breaks down the long-term memory design into three stages: indexing, retrieval, and reading. Built upon key experimental insights, we propose several memory design optimizations including session decomposition for value granularity, fact-augmented key expansion for indexing, and time-aware query expansion for refining the search scope. Extensive experiments show that these optimizations greatly improve both memory recall and downstream question answering on LongMemEval. Overall, our study provides valuable resources and guidance for advancing the long-term

](https://arxiv.org/abs/2410.10813#:~:text=interactions,term)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

(i) LOCOMO (Maharana et al., 2024), which is the longest conversation dataset to date, with an average of 300 turns with 9K tokens per sample. For the test set, we prompt GPT-4 to generate QA pairs for each session as in Alonso et al. (2024). We also conduct evaluation on the recently released official

](https://arxiv.org/html/2502.05589v2#:~:text=%28i%29%20LOCOMO%C2%A0%28Maharana%20et%C2%A0al,on%20the%20recently%20released%20official)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

long-conversation benchmark LOCOMO. Interestingly, there is a significant performance disparity in Turn-Level and Session-Level methods when using different retrieval models. For instance, switching from the MPNet-based retriever to the BM25-based retriever results in performance improvements up to

](https://arxiv.org/html/2502.05589v2#:~:text=long,in%20performance%20improvements%20up%20to)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

Methods LOCOMO Long-MT-Bench+ GPT4Score BLEU Rouge2 BERTScore GPT4Score BLEU Rouge2 BERTScore SeCom 69.33 7.19 13.74 88.60 88.81 13.80 19.21 87.72 Denoise 59.87 6.49 12.11 88.16 87.51 12.94 18.73 87.44

](https://arxiv.org/html/2502.05589v2#:~:text=Methods%20LOCOMO%20Long,44)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

match at L389 LOCOMO Zero History 24.86 1.94 17.36 3.72 13.24 85.83 0.00 0 Full History 54.15 6.26 27.20 12.07 22.39 88.06 210.34 13,330 Turn-Level (MPNet) 57.99 6.07 26.61 11.38 21.60 88.01 54.77 3,288

](https://arxiv.org/html/2502.05589v2#:~:text=match%20at%20L389%20LOCOMO%20Zero,77%203%2C288)[

![Favicon](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)arxiv.org

On Memory Construction and Retrieval for Personalized Conversational Agents

LOCOMO Zero History 24.86 1.94 17.36 3.72 13.24 85.83 0.00 0 Full History 54.15 6.26 27.20 12.07 22.39 88.06 210.34 13,330 Turn-Level (MPNet) 57.99 6.07 26.61 11.38 21.60 88.01 54.77 3,288

](https://arxiv.org/html/2502.05589v2#:~:text=LOCOMO%20Zero%20History%2024,77%203%2C288)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

3.2 Dataset Construction To study this task, we build a new dataset based on CareCall dataset2(Bae et al., 2022), which consists of single sessions of open-domain dialogues between bots and users. We choose this dataset because the sessions contain various topics that are likely to change in a short period of time, such as user’s health, sleep, and diet, as well as those in a relatively longer period of time, such as family, pets, and frequently visited places. We extend this

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=3,We%20extend%20this)[

![Favicon](https://www.google.com/s2/favicons?domain=https://aclanthology.org&sz=32)aclanthology.org

single-session dataset to a multi-session setting, which is a similar procedure presented in MSC (Xu et al., 2022a). Our resulting dataset contains more persona updates than other datasets (Xu et al., 2 https://github.com/naver-ai/carecall-corpus Statistics Sessions 7,665 Session 1 2,812

](https://aclanthology.org/2022.findings-emnlp.276.pdf#:~:text=single,Sessions%207%2C665%20Session%201%202%2C812)[

![Favicon](https://www.google.com/s2/favicons?domain=https://medium.com&sz=32)medium.com

Augmenting LLMs with Retrieval, Tools, and Long-term Memory | by Alaa Dania Adimi | InfinitGraph | Mar, 2025 | Medium

Query Rewriting

](https://medium.com/@ja_adimi/augmenting-llms-with-retrieval-tools-and-long-term-memory-b9e1e6b2fc28#:~:text=Query%20Rewriting)
```