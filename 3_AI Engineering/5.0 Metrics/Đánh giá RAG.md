
Bash
1. CÁCH TẠO BỘ TEST (câu hỏi và câu trả lời 10 điểm):
+, Các tiêu chí của 1 câu hỏi và câu đáp án soạn sẵn 10 điểm (chi tiết bên dưới): Độ chính xác 3 điểm, tính mạch lạc 2 điểm, phù hợp ngữ cảnh 2 điểm, tính đầy đủ của câu hỏi 2 điểm, tốc độ phản hồi 1 điểm. 
+, Mỗi đoạn (4-5 câu) => tạo 12 câu hỏi 
    +, Thể loại: trắc nghiệm, tự luận, tình huống 
    +, Mức độ: 
        - Actual Questions: Câu hỏi yêu cầu thông tin cụ thể, chi tiết.
        - Ambiguous Questions: Câu hỏi mơ hồ, không rõ ràng, yêu cầu mô hình phải phán đoán hoặc làm rõ. 
        - Requests for Clarification: Câu hỏi yêu cầu làm rõ một thông tin trước đó. 
    +, Build: mỗi loại câu hỏi gồm 4 câu ở 4 mức độ trên. 
--------------------------------------------------------------------------
--------------------------------------------------------------------------
2. Metrics ĐÁNH GIÁ: 
+, Human: Độ chính xác 3 điểm, tính mạch lạc 2 điểm, phù hợp ngữ cảnh 2 điểm, tính đầy đủ của câu hỏi 2 điểm, tốc độ phản hồi 1 điểm. 

+, Metrics Logic: BLEU Score, ROUGE Scor
    BLEU Score: Đo lường mức độ trùng khớp giữa văn bản mô hình tạo ra và văn bản tham chiếu. Lý do: Đánh giá khả năng tạo ra câu trả lời tương đồng với dữ liệu mẫu.
    ROUGE Score: Tập trung vào khả năng hồi tưởng, so sánh số lượng n-gram, từ hoặc câu từ văn bản tham chiếu có trong phản hồi của mô hình. Lý do: Đo lường khả năng mô hình nắm bắt thông tin chính xác từ câu hỏi.
    Context Retention: Đánh giá khả năng duy trì ngữ cảnh qua các câu hỏi liên tiếp. Lý do: Kiểm tra tính mạch lạc và hiểu ngữ cảnh trong hội thoại dài.
    F1-score: Kết hợp giữa Precision (độ chính xác) và Recall (khả năng hồi tưởng) để đo lường hiệu quả mô hình. Lý do: Đánh giá khả năng trả lời đúng cho các câu hỏi có đáp án cụ thể.

