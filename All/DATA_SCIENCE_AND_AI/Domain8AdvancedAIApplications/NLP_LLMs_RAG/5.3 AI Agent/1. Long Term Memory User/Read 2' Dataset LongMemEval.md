
```
Số lượng bộ dữ liệu gồm bao nhiêu mẫu. 
Mỗi mẫu gồm gì ?
```

- Link: [xiaowu0162/LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory (ICLR 2025)](https://github.com/xiaowu0162/LongMemEval)
- 

Để giúp bạn hiểu rõ hơn về ba tệp dữ liệu trong LongMemEval, chúng ta có thể hình dung như sau:

1. **longmemeval_s.json:**
    
    - **Mô tả:** Tệp này chứa các cuộc trò chuyện giữa người dùng và trợ lý ảo, với mỗi cuộc trò chuyện bao gồm khoảng 30-40 phiên trao đổi. Tổng cộng, các phiên này chiếm khoảng 115.000 từ hoặc ký tự.
        
    - **Mục đích:** Được thiết kế để kiểm tra khả năng của trợ lý ảo trong việc nhớ và xử lý thông tin từ một lượng lịch sử trò chuyện vừa phải.
        
2. **longmemeval_m.json:**
    
    - **Mô tả:** Tệp này chứa các cuộc trò chuyện dài hơn, với mỗi cuộc bao gồm khoảng 500 phiên trao đổi. Tưởng tượng rằng bạn đã trò chuyện với trợ lý ảo hàng ngày trong gần hai năm, và tệp này ghi lại toàn bộ những cuộc trò chuyện đó.
        
    - **Mục đích:** Nhằm đánh giá khả năng của trợ lý ảo trong việc xử lý và nhớ lại thông tin từ một lịch sử trò chuyện rất dài và phức tạp.
        
3. **longmemeval_oracle.json:**
    
    - **Mô tả:** Tệp này chỉ chứa những phiên trò chuyện có liên quan trực tiếp đến câu hỏi hoặc thông tin cần thiết. Nếu coi toàn bộ lịch sử trò chuyện như một cuốn sách, thì tệp này chỉ bao gồm những trang quan trọng nhất liên quan đến nội dung cần kiểm tra.
        
    - **Mục đích:** Được sử dụng để đánh giá khả năng của trợ lý ảo khi chỉ cung cấp những thông tin cần thiết, giúp xác định hiệu suất tối đa có thể đạt được trong điều kiện lý tưởng.
        

Tóm lại, ba tệp này đại diện cho các mức độ phức tạp khác nhau trong việc kiểm tra khả năng ghi nhớ và xử lý thông tin của trợ lý ảo: từ lịch sử trò chuyện vừa phải, rất dài, đến chỉ chứa thông tin cốt lõi.

LongMemEval là một bộ dữ liệu gồm **500 mẫu**, mỗi mẫu chứa các thành phần chính sau:

- **question_id:** ID duy nhất cho mỗi câu hỏi.
    
- **question_type:** Loại câu hỏi (ví dụ: single-session-user, multi-session).
    
- **question:** Nội dung câu hỏi.
    
- **answer:** Câu trả lời mong đợi.
    
- **question_date:** Ngày đặt câu hỏi.
    
- **haystack_sessions:** Danh sách các phiên trò chuyện giữa người dùng và trợ lý, mỗi phiên gồm nhiều lượt trao đổi với thông tin về vai trò (user/assistant) và nội dung.
    
- **answer_session_ids:** Danh sách ID của các phiên chứa bằng chứng hỗ trợ cho câu trả lời.
    

Mỗi mẫu được thiết kế để đánh giá khả năng ghi nhớ và xử lý thông tin của trợ lý trò chuyện trong các tình huống khác nhau.