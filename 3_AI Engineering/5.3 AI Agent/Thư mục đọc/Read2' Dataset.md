
```
Số lượng bộ dữ liệu gồm bao nhiêu mẫu. 
Mỗi mẫu gồm gì ?
```

LongMemEval là một bộ dữ liệu gồm **500 mẫu**, mỗi mẫu chứa các thành phần chính sau:

- **question_id:** ID duy nhất cho mỗi câu hỏi.
    
- **question_type:** Loại câu hỏi (ví dụ: single-session-user, multi-session).
    
- **question:** Nội dung câu hỏi.
    
- **answer:** Câu trả lời mong đợi.
    
- **question_date:** Ngày đặt câu hỏi.
    
- **haystack_sessions:** Danh sách các phiên trò chuyện giữa người dùng và trợ lý, mỗi phiên gồm nhiều lượt trao đổi với thông tin về vai trò (user/assistant) và nội dung.
    
- **answer_session_ids:** Danh sách ID của các phiên chứa bằng chứng hỗ trợ cho câu trả lời.
    

Mỗi mẫu được thiết kế để đánh giá khả năng ghi nhớ và xử lý thông tin của trợ lý trò chuyện trong các tình huống khác nhau.