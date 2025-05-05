
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
    - BLEU Score: Đo lường mức độ trùng khớp giữa văn bản mô hình tạo ra và văn bản tham chiếu. Lý do: Đánh giá khả năng tạo ra câu trả lời tương đồng với dữ liệu mẫu.
    - ROUGE Score: Tập trung vào khả năng hồi tưởng, so sánh số lượng n-gram, từ hoặc câu từ văn bản tham chiếu có trong phản hồi của mô hình. Lý do: Đo lường khả năng mô hình nắm bắt thông tin chính xác từ câu hỏi.
    - F1-score: Kết hợp giữa Precision (độ chính xác) và Recall (khả năng hồi tưởng) để đo lường hiệu quả mô hình. Lý do: Đánh giá khả năng trả lời đúng cho các câu hỏi có đáp án cụ thể.
	- Judge: LLM Scoring. 


1. LLM mạnh hơn, hoặc người. 
2. Đánh giá: Faithfulness, Answer Relevancy (BLEU, ROUGH), Context Relevancy (LLM) . 
3. Bổ sung: Context Retention: Đánh giá khả năng duy trì ngữ cảnh qua các câu hỏi liên tiếp. Lý do: Kiểm tra tính mạch lạc và hiểu ngữ cảnh trong hội thoại dài.

- [Faithfulness - Ragas](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/#faithfullness-with-hhem-21-open)   []
## Faithfulness

`Faithfulness` metric measures the factual consistency of the generated answer against the given context. It is calculated from answer and retrieved context. The answer is scaled to (0,1) range. Higher the better.

The generated answer is regarded as faithful if all the claims made in the answer can be inferred from the given context. To calculate this, a set of claims from the generated answer is first identified. Then each of these claims is cross-checked with the given context to determine if it can be inferred from the context. The faithfulness score is given by:


![[Pasted image 20250103155417.png]]
# Đánh giá: 
- Độ chính xác 
- 