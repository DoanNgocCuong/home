
https://arxiv.org/pdf/2305.10250

Dưới đây là phần tóm tắt chi tiết nội dung bài báo “MemoryBank: Enhancing Large Language Models with Long-Term Memory” (Zhong et al., 2023). Bài báo tập trung vào vấn đề xây dựng một cơ chế “bộ nhớ dài hạn” (long-term memory) cho các mô hình ngôn ngữ lớn (LLMs), giúp mô hình duy trì ngữ cảnh lâu hơn, có khả năng “nhớ” lại và diễn giải thông tin từ các cuộc trò chuyện trước, cũng như rút ra “chân dung người dùng” (user portrait). Nội dung chính được chia thành các phần như sau:

---

## 1. Giới thiệu

- **Bối cảnh**: Các mô hình ngôn ngữ lớn (LLMs) như GPT-3, ChatGPT, GPT-4, ChatGLM,… đã đạt được những thành tựu quan trọng, có khả năng giải quyết nhiều tác vụ ngôn ngữ phức tạp. Tuy nhiên, **hạn chế rõ rệt** nằm ở việc các LLM không có một cơ chế “bộ nhớ dài hạn” thực sự, nên thường quên bối cảnh của những đoạn hội thoại cũ. Điều này trở thành **rào cản** lớn trong các ứng dụng đòi hỏi duy trì tương tác lâu dài với người dùng, như:
    
    - Trợ lý cá nhân (AI companion, trợ lý ảo).
        
    - Chăm sóc tâm lý và tinh thần (liệu pháp tâm lý, hỗ trợ cảm xúc).
        
    - Thư ký riêng, giúp xử lý các công việc kéo dài, ghi nhớ lịch sử tương tác.
        
- **Đề xuất**: Tác giả giới thiệu **MemoryBank**, một cơ chế bổ sung “bộ nhớ dài hạn” cho các LLM. MemoryBank có khả năng lưu trữ, cập nhật, truy xuất và tóm lược thông tin sự kiện cũng như đặc điểm người dùng (user portrait). Bộ nhớ này:
    
    1. Giúp LLM gọi lại (recall) các chi tiết đã nói trong quá khứ.
        
    2. Cập nhật để mô hình ngày càng hiểu hơn về người dùng.
        
    3. Mô phỏng “quên” bớt thông tin cũ, ít quan trọng, dựa trên thuyết **Đường cong quên Ebbinghaus**.
        
- **Ứng dụng minh họa**: Bài báo xây dựng một chatbot tên **SiliconFriend** có khả năng trò chuyện lâu dài (AI Companion). SiliconFriend được triển khai trên cả mô hình đóng (ChatGPT) và mở (ChatGLM, BELLE). Ngoài cơ chế bộ nhớ, SiliconFriend còn được tinh chỉnh bằng dữ liệu hội thoại tâm lý, nhằm tăng tính thấu cảm (empathy) và khả năng hỗ trợ người dùng về mặt tinh thần.
    

---

## 2. Cơ chế MemoryBank

MemoryBank được thiết kế như một **cơ chế “bộ nhớ”** tách rời, gồm ba thành phần chính:

1. **Memory Storage (kho lưu trữ)**
    
    - Lưu trữ toàn bộ các đoạn hội thoại trước đó, tổ chức theo ngày/ phiên làm việc.
        
    - Được tóm tắt theo tầng (hierarchical summarization):
        
        - **Daily event summaries**: Tóm lược những nội dung cốt lõi xảy ra trong ngày.
            
        - **Global event summary**: Tóm lược ở mức cao hơn, phản ánh các xu hướng, “câu chuyện tổng quát” sau nhiều ngày.
            
    - **User Portrait (chân dung người dùng)**: Mỗi ngày, hệ thống tự động suy luận và lưu lại thông tin về tính cách, sở thích, trạng thái của người dùng, rồi hợp nhất dần qua thời gian.
        
2. **Memory Retrieval (truy xuất ký ức)**
    
    - Khi người dùng đặt câu hỏi mới, mô hình cần truy xuất ký ức liên quan từ kho lưu trữ.
        
    - Sử dụng mô hình **dense retrieval** kiểu DPR (Dense Passage Retrieval) hoặc FAISS indexing.
        
    - Mọi mẩu hội thoại quá khứ được mã hóa thành vector. Câu truy vấn hiện tại cũng được mã hóa, rồi tính độ tương đồng để tìm ra những “mẩu ký ức” liên quan nhất.
        
3. **Memory Updating (cập nhật bộ nhớ)**
    
    - Để mô phỏng tính “hữu hạn” của trí nhớ giống con người, nhóm tác giả áp dụng ý tưởng từ **Đường cong quên Ebbinghaus**, cho thấy mức độ ghi nhớ của con người suy giảm dần theo thời gian.
        
    - Mỗi “mảnh ký ức” có một **độ mạnh (memory strength) S**, bắt đầu là 1 khi mới được tạo. Mỗi lần nó được người dùng hoặc mô hình nhắc lại (retrieved), giá trị S tăng lên.
        
    - Thời gian trôi qua (t) làm giảm khả năng được nhớ lại. Tính xác suất quên bằng công thức R=e−t/SR = e^{-t/S}. Mảnh ký ức ít được “nhắc” (retrieved) hoặc đã quá lâu sẽ bị “phai mờ” (có khả năng quên cao).
        
    - Quá trình này giúp mô hình “quên” dần thông tin ít quan trọng, cũ kỹ, tránh tình trạng kích thước bộ nhớ tăng vô hạn.
        

Nhờ cơ chế trên, MemoryBank có tiềm năng giúp mô hình:

- Nhớ được **chính xác** và **có chọn lọc** các sự kiện, thông tin cá nhân của người dùng.
    
- Duy trì **ngữ cảnh liên tục** trong các cuộc trò chuyện dài ngày, dài phiên.
    

---

## 3. Ứng dụng: SiliconFriend – Chatbot Trò Chuyện Dài Hạn

Để minh họa, nhóm tác giả xây dựng **SiliconFriend** – một AI chatbot có khả năng bám sát cuộc trò chuyện lâu dài với người dùng, phù hợp kịch bản:

- Bạn đồng hành ảo (AI companion).
    
- Tư vấn tâm lý, hỗ trợ cảm xúc, đưa ra lời khuyên.
    

### 3.1 Tinh chỉnh trên dữ liệu hội thoại tâm lý

- Để chatbot thấu cảm hơn, nhóm thu thập **38.000 mẫu hội thoại tâm lý**. Các đoạn này đến từ nhiều nguồn khác nhau (sàn tâm sự trực tuyến, ví dụ).
    
- Sau đó, sử dụng phương pháp **LoRA** (Low-Rank Adaptation) để tinh chỉnh (fine-tune) trên hai mô hình nguồn mở (ChatGLM, BELLE).
    
    - LoRA giúp giảm số tham số phải huấn luyện, tiết kiệm tài nguyên mà vẫn cải thiện mô hình hiệu quả.
        
    - Với ChatGPT (đóng mã nguồn), không thể fine-tune trực tiếp, do đó sử dụng ChatGPT ở dạng API (hoặc tương tác hội thoại) và kết hợp với MemoryBank.
        

### 3.2 Tích hợp MemoryBank

- SiliconFriend ghi lại mọi đoạn hội thoại vào **Memory Storage**.
    
- Khi người dùng tương tác, chatbot sẽ gọi **Memory Retrieval** để tìm lại những thông tin liên quan (chân dung người dùng, sự kiện,...). Từ đó, mô hình trả lời dựa trên **ngữ cảnh cũ**.
    
- Nếu có bật tính năng “quên” dựa trên Ebbinghaus, mô hình sẽ dần **xóa bớt** hoặc giảm trọng số những ký ức cũ, ít khi được nhắc.
    

### 3.3 Minh họa chức năng

- **Khả năng hỗ trợ tâm lý**: Khi người dùng than phiền về chuyện buồn, trầm cảm hoặc căng thẳng, SiliconFriend có thể đưa ra lời khuyên, an ủi, thể hiện sự thông cảm (empathy), nhờ được fine-tune trên dữ liệu tâm lý.
    
- **Gợi lại thông tin cũ**: Nếu hôm trước mô hình từng gợi ý quyển sách, hôm sau người dùng hỏi lại “Cuốn sách mà bạn từng khuyên tôi hôm qua là gì?”, chatbot có thể truy xuất ra câu trả lời chính xác, thay vì “quên”.
    
- **Nhớ cá tính người dùng**: SiliconFriend ghi nhận thông tin người dùng thuộc tuýp tính cách nào (ví dụ: hướng nội, nhạy cảm,…), sở thích, mối bận tâm. Các lượt tương tác sau, nó có thể cá nhân hóa lời khuyên (ví dụ: “Bạn có nói bạn rất thích môn yoga, thế nên hôm nay bạn có thể thử…”).
    

---

## 4. Thực nghiệm

Tác giả thực hiện hai kiểu đánh giá: **định tính** và **định lượng**.

### 4.1 Đánh giá định tính

- **So sánh** SiliconFriend với các mô hình gốc (chưa tích hợp MemoryBank) trong bối cảnh trò chuyện tư vấn tâm lý.
    
- **Khả năng nhớ**: Người dùng hỏi về chi tiết cũ (“Bạn gợi ý tôi đọc quyển sách gì lần trước nhỉ?”). Kết quả: SiliconFriend truy xuất đúng câu trả lời.
    
- **Khả năng dùng “chân dung người dùng”**: Chatbot đưa ra gợi ý hoặc phản hồi tùy thuộc tính cách, sở thích mà nó ghi nhận được.
    

### 4.2 Đánh giá định lượng

- Tạo **“kho ký ức” 10 ngày** gồm 15 người dùng ảo (mỗi người một cá tính khác nhau).
    
- Mỗi ngày trò chuyện về vài chủ đề. Sau đó viết **194 câu hỏi kiểm tra** xem chatbot có nhớ chính xác thông tin (điều gì đã xảy ra ở ngày trước,…).
    
- Bảng đánh giá dựa trên 4 chỉ số:
    
    1. **Retrieval Accuracy**: có lấy đúng đoạn ký ức không.
        
    2. **Response Correctness**: câu trả lời có chính xác không.
        
    3. **Contextual Coherence**: câu trả lời có gắn với bối cảnh, trả lời trôi chảy không.
        
    4. **Model Ranking**: so sánh mô hình ChatGLM, BELLE, ChatGPT tích hợp MemoryBank.
        
- **Kết quả**:
    
    - SiliconFriend ChatGPT nói chung cao nhất về độ đúng đắn, mạch lạc.
        
    - SiliconFriend ChatGLM, BELLE cũng có khả năng nhớ tốt nhưng chất lượng câu trả lời đôi khi kém mạch lạc hơn ChatGPT, nhất là về diễn đạt và tính chính xác chi tiết.
        

---

## 5. Nghiên cứu liên quan (Related Works)

- **LLMs**: Trong vài năm qua, mô hình GPT-3, GPT-4, ChatGPT,… hay các mô hình mở như LLaMa, ChatGLM, Alpaca,… tiến rất xa về “kiến thức tổng quát” và khả năng sinh văn bản.
    
- **Bộ nhớ mở rộng**: Có một số nghiên cứu trước đó về memory-augmented neural networks, như Neural Turing Machines (NTM), Memory Networks,… nhằm tăng khả năng lưu trữ. Tuy nhiên, các công trình này **chưa** giải quyết đầy đủ bài toán “ghi nhớ dài hạn” theo kiểu trò chuyện nhiều ngày, đồng thời chưa mô phỏng được “quên” có chọn lọc.
    
- **Đường cong Ebbinghaus**: Là lý thuyết tâm lý lâu đời về cách con người quên dần thông tin. Nhóm tác giả vận dụng nó để triển khai cơ chế quên cho AI một cách đơn giản và khả thi.
    

---

## 6. Kết luận

Bài báo giới thiệu **MemoryBank** – cơ chế bộ nhớ dài hạn cho LLM, gồm:

1. **Kho lưu trữ** (nhật ký hội thoại, tóm tắt sự kiện, chân dung người dùng).
    
2. **Bộ truy xuất** (dense retrieval) chọn thông tin liên quan để đưa vào lời nhắc (prompt).
    
3. **Bộ cập nhật** với cơ chế “quên” dựa trên Ebbinghaus, giúp AI có trí nhớ tự nhiên, không “phình to” vô hạn.
    

Tác giả triển khai thử nghiệm thành công trên mô hình **SiliconFriend** (dùng ChatGPT, ChatGLM, BELLE).

- Kết quả cho thấy mô hình có khả năng nhớ tốt, phản hồi nhất quán hơn.
    
- Đặc biệt, khi được tinh chỉnh trên dữ liệu hội thoại tâm lý, mô hình có thể đưa ra phản hồi mang tính hỗ trợ, khuyến khích và thấu hiểu hơn.
    

**Hướng mở rộng**:

- Có thể tích hợp MemoryBank vào mọi LLM (cả đóng lẫn mở).
    
- Nghiên cứu mô hình “quên” phức tạp hơn, có thể chia nhỏ loại thông tin hay xét mức độ ưu tiên “giữ”/“xóa” chi tiết.
    
- Thử nghiệm trên lĩnh vực khác như trợ lý văn phòng, AI giảng dạy (tương tác dài hạn với học sinh),…
    

---

## Tóm tắt ngắn gọn

Bài báo đề xuất **MemoryBank** – cơ chế “bộ nhớ dài hạn” giúp LLM lưu trữ, tổng hợp và truy xuất các thông tin quan trọng trong các cuộc hội thoại dài ngày, đồng thời mô phỏng tính “quên” bớt thông tin cũ, ít dùng. Thử nghiệm với chatbot SiliconFriend cho thấy mô hình có thể:

1. **Gọi lại** chính xác những sự kiện, thông tin, sở thích người dùng từ nhiều ngày trước.
    
2. **Hiểu rõ hơn** về tính cách, tâm lý người dùng, nhờ tổng hợp và lưu trữ “chân dung người dùng” liên tục.
    
3. **Cá nhân hóa** câu trả lời, xây dựng lời khuyên tâm lý phù hợp.
    

Kết quả thực nghiệm cả về định tính lẫn định lượng chứng minh MemoryBank là giải pháp hiệu quả để khắc phục nhược điểm “quên ngữ cảnh dài hạn” của các mô hình ngôn ngữ lớn hiện nay, đặc biệt trong các tình huống đòi hỏi tương tác lâu dài và mang yếu tố cá nhân.
