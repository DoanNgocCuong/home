
[NẾU MỌI NGƯỜI CẦN TRIỂN KHAI, CỨ PING EM]
----
Chatbot RAG
Hiểu 1 cách tóm tắt: 

+, Tài liệu nội bộ của mình được Chunking thành các phần nhỏ. Sau đó đem Embedding từng Chunk trước, lưu vào Vector DB 

+, Khi user Query 1 câu. Câu đó của User được Embedding lại và so sánh với Embedding trong Vector DB để tìm kiếm Vector tương đồng => Từ đó trả ra top K (K=3, 5, 10, ... mình lựa chọn, tuning), top K tài liệu liên quan => Top K này được xào nấu thành Context

+, Câu của User và câu Context liên quan => Đưa qua LLMs để response ra câu trả lời. 

----
Trong quá trình triển khai cũng sẽ có nhiều thứ, theo kinh nghiệm ít ỏi của em thì có: 
1. Có nhiều phương pháp Chunking, gần 10 cái: từ chunking theo dấu câu. Chunking theo đoạn, chunking theo ngữ nghĩa, dùng LLMs để chunking, ... Hoặc nếu ít thì Chunking bằng. 
[Chunking là bước đầu trước khi tiến hành Embedding từng Chunk. Cái lấy top K chính là top K chunking này]. 
2. Ở mỗi step đẻ ra rất nhiều method tối ưu: 
- Về độ chính xác: Làm sao cải thiện được Context lấy ra. (Context thì gồm chất lượng các Chunking và việc lựa chọn top K, cách kết nối top K với nhau, cải thiện truy vấn embedding, model embedding, ...)
- Về Response Time: Tối ưu query Vector sao cho nhanh, LLms phản hồi sao cho nhanh, model LLMs nào, Cách sắp xếp Vector như nào để query được nhanh

----
Hiểu sâu hơn và triển khai mn có thể xem thêm tại đây: 
- 1 repo em mới làm gần đây cho 1 bạn ở HCM: 
https://github.com/DoanNgocCuong/MiniProj_RAG3_RAG6_LegalChatbot_16032025 
- Hiểu thêm về từng phần kỹ thuật: https://viblo.asia/p/chatgpt-series-5-tim-hieu-ve-retrieval-augmented-generation-rag-Ny0VGRd7LPA
- Bài report của AI Việt Nam: https://www.facebook.com/aivietnam.edu.vn/posts/project-v%E1%BB%81-llm-65-trang-x%C3%A2y-d%E1%BB%B1ng-h%E1%BB%87-th%E1%BB%91ng-v%E1%BB%81-s%E1%BB%A9c-kho%E1%BA%BB-d%C3%B9ng-llamaindex-h%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-/854855683423818
- Kho tài liệu về RAG từ cơ bản đến nâng cao: https://www.facebook.com/share/p/1LQVStLCk7/
- RAG Techniques: https://github.com/NirDiamant/RAG_Techniques

#nhathuong #gosinga
#wecommit100x             ----  #wecommit100xhabit
#x3nangsuat
#TheAnhEnglish
#AIO
#codemely #ai_team
#doanngoccuong