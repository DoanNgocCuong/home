
Dưới đây là tóm tắt nội dung chính của bài báo “Retaining Key Information under High Compression Ratios: Query-Guided Compressor for LLMs”:

---

**1. Động lực nghiên cứu**

- Các mô hình ngôn ngữ lớn (LLMs) ngày càng cho phép đưa vào ngữ cảnh (context) rất dài để xử lý các tác vụ như hỏi-đáp đa tài liệu, tóm tắt văn bản, v.v.
- Tuy nhiên, khi đưa nhiều tài liệu hoặc ngữ cảnh quá dài vào mô hình, chi phí suy luận (inference cost), độ trễ (latency), và lượng thông tin dư thừa (redundant information) đều tăng lên đáng kể.
- Giải pháp thường gặp là nén (compress) ngữ cảnh dài thành ngắn hơn nhưng vẫn phải giữ lại những thông tin quan trọng. Vấn đề: rất nhiều phương pháp nén khi tăng tỷ lệ nén (compression ratio) quá cao sẽ dẫn đến việc mất mát thông tin quan trọng, khiến chất lượng đầu ra giảm mạnh.

**2. Vấn đề “mất thông tin chủ chốt” khi nén**

- Các công trình trước đây (ví dụ LongLLMLingua, AutoCompressor, v.v.) cho thấy rằng nếu nén quá nhiều, hiệu quả mô hình giảm đáng kể, đôi khi còn trở về ngang mức “đóng sách” (closed-book) – tức là chỉ dùng mỗi câu hỏi, không kèm tài liệu.
- Nguyên nhân cốt lõi do trong quá trình nén, nhiều thông tin then chốt (đặc biệt là những gì liên quan trực tiếp đến câu hỏi/query) bị mất.
- Một thí nghiệm trong bài chỉ ra rằng nếu cố ý “cấy” lại thông tin quan trọng (chẳng hạn thêm thẳng câu trả lời) vào phần đã nén, hiệu quả sẽ ít giảm hơn rất nhiều. Điều đó khẳng định tầm quan trọng của việc bảo toàn thông tin liên quan query.

**3. Giải pháp: “Query-Guided Compressor” (QGC)**

- Bài báo đề xuất phương pháp QGC, tập trung tận dụng thông tin “trọng tâm” do câu hỏi (query) xác định.
- Thay vì nén “không có định hướng” hoặc chỉ xóa các token “có vẻ ít quan trọng” trong văn bản, QGC dùng chính câu hỏi để hướng dẫn quá trình nén từ đầu đến cuối.

Cách hoạt động gồm bốn khối chính:

1. **Query-Guided Context Encoder**
    
    - Dùng một encoder (Transformer) để mã hoá _chung_ cả query và văn bản, cho phép văn bản “nhìn thấy” query để biết token nào quan trọng hơn.
2. **Query-Guided Pooling Layer**
    
    - Tách văn bản ban đầu thành các n-gram (chẳng hạn mỗi n-gram gồm n token).
    - Tính mức độ liên quan giữa mỗi token trong n-gram với “vector trung bình” đại diện của query (bằng dot-product).
    - Lấy trọng số theo độ liên quan đó để gộp (pool) thành một vector duy nhất cho n-gram.
3. **Query-Document Reviewing Layer**
    
    - Sau khi nén mỗi n-gram thành một vector, ta “soát xét” lại bằng một mô-đun transformer khác, lần nữa nhìn cả query lẫn văn bản gốc, để hiệu chỉnh thêm thông tin.
    - Nhờ đó hạn chế thiếu sót thông tin quan trọng.
4. **Semantic Alignment Layer**
    
    - Các vector nén cuối cùng được ánh xạ (align) về không gian embedding của mô hình ngôn ngữ đích (LLM).
    - Khi đưa vào LLM, các vector này đóng vai trò như phần “ngữ cảnh” đã nén, ngắn hơn đáng kể so với văn bản gốc.

Ngoài ra, QGC còn đưa ra cơ chế “Dynamic Compression”:

- Tận dụng điểm xếp hạng (score) giữa truy vấn và từng tài liệu để ấn định mức nén khác nhau.
- Tài liệu ít liên quan hơn sẽ được nén mạnh hơn (thậm chí bị loại bỏ hẳn nếu độ liên quan quá thấp).
- Tài liệu rất quan trọng thì nén ít để giữ được nhiều nội dung cốt lõi.

**4. Kết quả thực nghiệm**

- Thử nghiệm trên các tập dữ liệu hỏi-đáp đa tài liệu: NaturalQuestions, TriviaQA, HotpotQA.
- So sánh với nhiều phương pháp nén khác (LongLLMLingua, AutoCompressor, Selective-Context, ICAE, v.v.) và với các phương pháp đơn giản chỉ “chọn lọc” (reranker).
- QGC thường đạt:
    - _Hiệu suất_ (độ chính xác, EM/F1) cao hơn hoặc ngang bằng so với các baseline,
    - _Tỷ lệ nén_ (compression ratio) cao hơn nhiều,
    - _Tốc độ suy luận_ (throughput) tăng đáng kể do đầu vào mô hình ngắn hơn.
- Phân tích chi tiết cho thấy QGC giảm thiểu việc mất thông tin quan trọng: khi tăng tỷ lệ nén (lên gấp 3-4 lần, hoặc cao hơn) thì độ chính xác của mô hình chỉ suy giảm rất nhẹ so với mô hình gốc.

**5. Kết luận và hướng phát triển**

- QGC là giải pháp nén bám sát query, nhờ đó bảo toàn được những nội dung cốt lõi phục vụ việc trả lời câu hỏi (hay các tác vụ khác liên quan).
- Phương pháp không cần fine-tune toàn bộ mô hình LLM; chỉ huấn luyện riêng bộ nén (compressor). Điều này giúp giảm chi phí huấn luyện.
- Nghiên cứu tương lai:
    - Áp dụng QGC cho các mô hình lớn hơn hoặc các tác vụ khác, ví dụ tóm tắt đa tài liệu, QA phức tạp, v.v.
    - Kết hợp các kỹ thuật mở rộng ngữ cảnh của LLM (như kéo dài positional embedding) với cơ chế nén để đạt thêm hiệu quả.

---

**Tóm lại**, bài báo xoay quanh việc **nén ngữ cảnh dài trong mô hình ngôn ngữ lớn** mà **vẫn giữ được thông tin quan trọng nhất định bởi câu hỏi (query) quyết định**. Phương pháp QGC tập trung tận dụng mạnh mẽ nội dung của query để sắp xếp, nén, và tái chiếu thông tin tài liệu, từ đó giúp mô hình thu được kết quả hỏi-đáp (hoặc các nhiệm vụ khác) tốt hơn ngay cả khi tỷ lệ nén rất cao.

Nếu bạn cần thêm chi tiết về thuật toán, mô hình Transformer, hoặc mã giả (pseudo-code) để triển khai, hãy cho tôi biết thêm nhé!