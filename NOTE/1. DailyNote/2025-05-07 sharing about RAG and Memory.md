
![[Pasted image 20250625112252.png]]

# 1. Các khái niệm cần nắm 

## 1.1 Prompting 

![[Pasted image 20250507012327.png]]

1. Bản chất là khi dùng web chat của ChatGPT nó đã có sẵn: SYSTEM PROMPT / 1 loạt các chuỗi xử lý bên trong đó rồi. 

2. Khi mà prompting từ đầu thì nó sẽ có 3 phần: System Prompt - User Prompt - AI Assistant

![[Pasted image 20250507012428.png]]

=> Các task của tụi em khi mà viết Prompt cho sản phẩm thì bản chất là viết cái: system prompt 
và trả ra cho ae dev thường là ở dạng JSON. 
# 2. RAG


- Vấn đề gặp phải: Model ko có sẵn những thông tin bên ngoài chẳng hạn như: dữ liệu nội bộ, thông tin mới cập nhật, ...  -> Có các hướng xử lý như: Fine tuning, ... rất tốn kém => RAG ra đời. 
- Có vấn đề -> Có giải pháp mới. 

1. Có 1 số cases -> mn ném PDF lên chatGPT => bản chất là gì? là thêm CONTEXT cho user prompt (tức là prompt của mn). 
2. Tôi muốn tự triển khai thì nó như nào, models bên trong xử lý như nào? 


## 2.1 Cách thức hoạt động của RAG - Retrieval Augmented Generation (RAG system)

1. **Truy xuất** (Retrieval): Khi người dùng đặt câu hỏi, hệ thống tìm kiếm các tài liệu liên quan từ cơ sở dữ liệu ngoài.
2. **Tăng cường** (Augmentation): Thông tin được truy xuất được thêm vào prompt của LLM.
3. **Tạo ra** (Generation): LLM sử dụng cả kiến thức sẵn có và thông tin mới để tạo câu trả lời.

![[Pasted image 20250507014056.png]]

## 2.2 Vector DB nó giống gì và khác gì với DB truyền thống ? 
#### Seeding 1 Link: ![# Loại Database giúp Generative AI bùng nổ | Vector Database Wecommit](https://youtu.be/qslGfiM67dE?feature=shared)


---
1. Tài liệu to quá => Chunking 

![](https://sspark.ai/cfimages?u1=LtzY2MzII01zESdxOrXlQzo4SJ%2Fxm53W61oKp%2FW%2FnbEy7Pxr4eGreAwdZ1oU3bUJIVrxLhUW%2FZQFTCHRZF86jVx4ml2b9p2WAet2G8nMbEssfPhI1Lio&u2=P35BqyDBRZ%2ByuN%2BJ&width=512)


![](https://d3lkc3n5th01x7.cloudfront.net/wp-content/uploads/2024/08/26051537/Advanced-RAG.png)

```
**Giai đoạn 1: Lập chỉ mục dữ liệu (Data Indexing)**

- Chia nhỏ tài liệu thành các đoạn (chunks)
- Tạo vector embedding cho mỗi đoạn
- Lưu trữ các vector này trong cơ sở dữ liệu vector

**Giai đoạn 2: Truy xuất và tạo sinh (Retrieval & Generation)**

- Nhận câu hỏi từ người dùng
- Chuyển đổi câu hỏi thành vector embedding
- Tìm kiếm Top-K đoạn văn bản liên quan nhất từ cơ sở dữ liệu vector
- Kết hợp các đoạn văn bản với câu hỏi để tạo prompt cho LLM
- LLM tạo ra câu trả lời dựa trên thông tin được cung cấp
```

- Demo: - Demo: [DoanNgocCuong/MiniProj_RAG3_RAG6_LegalChatbot_16032025: Support Project Graduation for 1 friend. RAG on Legal Docs in vietnamese - xài LLMs 4omini - Deploy Server - Chạy with no Memory and Add Memory in the Future. --- - Phân vân là : lưu tài liệu nội bộ của nó trên qdant hay milvus (deploy database trên server luôn) - Cân nhắc để có thể tích hợp mem0 và supabase vào làm memory Cho cả chatbot và RAG](https://github.com/DoanNgocCuong/MiniProj_RAG3_RAG6_LegalChatbot_16032025)
- Demo: [RAG Chatbot](http://103.253.20.13:30001/chat)

## 2.3 Nhiều method để phát triển cho từng pha: [RUC-NLPIR/FlashRAG: ⚡FlashRAG: A Python Toolkit for Efficient RAG Research (WWW2025 Resource)](https://github.com/RUC-NLPIR/FlashRAG)

1. Indexing: đánh chỉ mục -> như VectorDB thông thường nó cũng có indexing -> các kỹ thuật khác nhau ()
2. Chunking khác nhau: chunking theo split overlaf (fix sized), chunking theo semantic (NLP chunking theo ngữ nghĩa của 2 câu gần nhất), LLMs chunking, Raptor RAG (Summary từng đoạn chunking lên để thêm vào chunk)
Có hẳn 1 đồ án tốt nghiệp về cái này: [DoanNgocCuong/Research_RAG5_SpProjGraduation_aHuy_T122024: The official implementation of RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://github.com/DoanNgocCuong/Research_RAG5_SpProjGraduation_aHuy_T122024)

3. Model Embedding: cải thiện cho tiếng việt, ...
4. Viết lại câu Query  (Kiểu giống bài game mn đang làm, câu query được viết lại dưới dạng dễ nắm bắt hơn trước khi cho qua model embedidng), hoặc Routiin: các câu hỏi khác nhau đi luồng khác nhau, ...
5. Search: indexing như nào cho dễ search? Hybrid Search (Search theo keyword và embedding search), với Graph thì có PPR Graph Search (Personal Page Rank)
6. Retrieve: Sau khi search được rồi thì hậu xử lý các đoạn Relevant Chunk như nào? Reranking Model để xếp hạng thứ tự các đoạn chunking 
7. ....

![](https://www.marktechpost.com/wp-content/uploads/2024/04/Screenshot-2024-04-01-at-12.44.59-PM.png)

SOTA 

![[Pasted image 20250507021516.png]]

### Seeding 2: Đọc thêm HippoRAG2 tại linkedin: [RAG RESEARCH phần 1 | LinkedIn](https://www.linkedin.com/pulse/rag-research-ph%25E1%25BA%25A7n-1-cuong-doan-ngoc-x4nyc/?trackingId=R50iYA54QJKhNQhtb75XHQ%3D%3D)

Các chỉ số cần đo đạc (KPIs & Metrics)

|Nhóm|Chỉ số|Công thức/ cách đo|Ý nghĩa trong đồ án|
|---|---|---|---|
|**1. Chất lượng truy vấn (Retrieval)**|**Recall@k**|𝑅@k = (# câu trả lời đúng nằm trong top-k) / (# câu hỏi tham chiếu)|Đảm bảo Vector DB lấy được đoạn tri thức cần thiết cho LLM.|
||**Precision@k**|𝑃@k = (# đoạn có liên quan trong top-k) / k|Đánh giá độ “sạch” của ngữ cảnh gửi vào LLM.|
||**MRR (Mean Reciprocal Rank)**|1 /|Q|
||**Semantic Similarity**|Cosine (query vs chunk) trung bình|Giúp so sánh các phiên bản embedding model.|
|**2. Chất lượng sinh (Generation)**|**Exact Match (EM)**|% câu trả lời trùng khớp toàn phần|Dễ hiểu với bộ câu hỏi trắc nghiệm đúng-sai.|
||**F1 Score**|2·Precision·Recall /(Precision+Recall) trên token|Phù hợp khi đáp án dài, nhiều chi tiết.|
||**BLEU / ROUGE-L**|Thư viện `sacrebleu`, `rouge-score`|Cho phép so sánh chất lượng ngôn ngữ giữa các mô hình 1B vs 3B.|
||**Faithfulness / Groundedness**|% câu trả lời có **citation** tới đúng nguồn RAG|Quan trọng để giảm “hallucination”.|
|**3. Hiệu năng hệ thống**|**Latency (p95)**|Thời gian (ms) từ khi người dùng gửi ➜ nhận|Mục tiêu < 2 s đối với truy vấn **exact-match**, < 10 s với suy luận LLM.|
||**Throughput**|Số truy vấn phục vụ/giây trên 1 nút|Kiểm tra năng lực docker Qdrant + Ollama trên cùng máy.|
||**Memory Footprint**|RAM dùng cho: Qdrant + Embedding + LLM|Xác định cấu hình tối thiểu (≈ 16 GB là đủ?).|
||**GPU utilization**|%, Temp, VRAM|Nếu thử nghiệm LLM 7B đẩy sang GPU.|
|**4. Chi phí**|**Cost/Query**|(Điện + khấu hao phần cứng)/# truy vấn|Minh chứng rằng giải pháp offline rẻ hơn cloud API.|
||**TCO 1 năm**|CAPEX + OPEX|Phục vụ phần đề xuất triển khai thực tế.|
|**5. Trải nghiệm người dùng**|**SUS (System Usability Scale)**|Khảo sát 10 câu (1–5) ➜ quy đổi 0-100|Đánh giá mức “dễ dùng” của giao diện.|
||**CSAT / NPS**|⭐ đánh giá ≥ 4 / 5 → CSAT|Sau thử nghiệm với học viên.|
||**Task Completion Rate**|% tình huống mô phỏng được giải đúng trong ≤ N phút|Chỉ ra hiệu quả học tập khi dùng chatbot.|


## 2.4 Multimodal RAG 

![[Pasted image 20250507021054.png]]

![](https://mlrwd9rnffxq.i.optimole.com/cb:641c.2be21/w:1920/h:1080/q:90/f:best/sm:0/https://vectorize.io/wp-content/uploads/2024/10/multimodal-featured.png)

- **Tạo embedding cho nhiều loại dữ liệu**: Chuyển đổi văn bản, hình ảnh, âm thanh thành vector
- **Mô hình đa phương thức (Multimodal Models)**: Sử dụng các mô hình có khả năng xử lý nhiều loại dữ liệu
- **Vector thống nhất (Unified Vectors)**: Tạo ra các biểu diễn vector thống nhất cho các loại dữ liệu khác nhau
- **Kết hợp thông tin đa phương thức**: Truy xuất và kết hợp thông tin từ nhiều loại dữ liệu khác nhau


# 3. RAG với MEMORY REAL PERSONALIZATION (tạm gọi là Memory of AI About User để phân biệt với RAG - Knowledge outside of AI). 

- Đọc thêm tại: [ResearchProject_Memory-AugmentedAIAgents_GraduationProject/CheckPoint/1. Long Term Memory User at main · DoanNgocCuong/ResearchProject_Memory-AugmentedAIAgents_GraduationProject](https://github.com/DoanNgocCuong/ResearchProject_Memory-AugmentedAIAgents_GraduationProject/tree/main/CheckPoint/1.%20Long%20Term%20Memory%20User)
- Demo: - [Mem0 Chat Assistant](http://103.253.20.13:25048/)
	- [Memory Database Explorer](http://103.253.20.13:25049/)

![[Pasted image 20250507030640.png]]


## 3.1 Giống và khác: 

- Chung bản chất: 
	- Đều là LƯU TRỮ (SAVE and INDEXING) VÀ TRUY XUẤT (RETRIEVAL AND GENERATION)

- Khác nhau 


| Đặc điểm               | RAG                                         | Memory                                            |
| ---------------------- | ------------------------------------------- | ------------------------------------------------- |
| **Nguồn dữ liệu**      | Tài liệu bên ngoài (PDF, web, sách, v.v.)   | Dữ liệu từ tương tác trước đó của người dùng      |
| **Mục tiêu chính**     | Cung cấp thông tin chính xác từ tài liệu    | Tạo trải nghiệm cá nhân hóa và liên tục           |
| **Tính thời gian**     | Có thể tĩnh (không thay đổi theo thời gian) | Động, phát triển theo thời gian với mỗi tương tác |
| **Tính cá nhân**       | Thường chia sẻ giữa các người dùng          | Riêng tư và cụ thể cho từng người dùng            |
| **Khả năng nhận thức** | Không có khả năng tự nhận thức              | Có thể có cơ chế tự cải thiện và tự nhận thức     |

| Đặc điểm                | RAG                                               | Memory (Mem0)                                      |
| ----------------------- | ------------------------------------------------- | -------------------------------------------------- |
| **Nguồn thông tin**     | Dữ liệu bên ngoài (tài liệu, cơ sở dữ liệu)       | Tương tác trước đó với người dùng                  |
| **Mục đích chính**      | Tăng cường độ chính xác bằng thông tin mới        | Cá nhân hóa trải nghiệm dựa trên lịch sử tương tác |
| **Thời điểm xử lý**     | Tại thời điểm suy luận (inference time)           | Liên tục học và cập nhật theo thời gian            |
| **Phạm vi tập trung**   | Tìm kiếm thông tin liên quan đến câu hỏi hiện tại | Xây dựng và duy trì hồ sơ người dùng toàn diện     |
| **Nhận thức thời gian** | Không nhất thiết phải có ngữ cảnh thời gian       | Có khả năng theo dõi thứ tự thời gian của sự kiện  |
| **Cấu trúc dữ liệu**    | Thường là cơ sở dữ liệu vector đơn giản           | Kết hợp đồ thị và vector để biểu diễn quan hệ      |
| **Ví dụ ứng dụng**      | Trả lời câu hỏi dựa trên tài liệu công ty         | Trợ lý cá nhân nhớ sở thích người dùng             |
## 3.2. Framework opensource: Mem0 - Cách thức hoạt động của Mem0
1. **Xử lý bộ nhớ**: Sử dụng LLM để tự động trích xuất và lưu trữ thông tin quan trọng từ cuộc trò chuyện
2. **Quản lý bộ nhớ**: Cập nhật liên tục và giải quyết mâu thuẫn trong thông tin để duy trì độ chính xác
3. **Kiến trúc lưu trữ kép**: Kết hợp cơ sở dữ liệu vector và đồ thị để lưu trữ và theo dõi mối quan hệ
4. **Hệ thống truy xuất thông minh**: Sử dụng tìm kiếm ngữ nghĩa và truy vấn đồ thị để tìm bộ nhớ liên quan

## 3.3 Thuỷ tổ của Memory (Fact > Summary > Keyphrase)

![[Pasted image 20250507023337.png]]


[Memory Operations - Mem0](https://docs.mem0.ai/core-concepts/memory-operations)

![](https://mintlify.s3.us-west-1.amazonaws.com/mem0/images/add_architecture.png)

![](https://mintlify.s3.us-west-1.amazonaws.com/mem0/images/search_architecture.png)


[2410.10813](https://arxiv.org/pdf/2410.10813)

Graph đọc lấy ý tưởng có thể sẽ khá giống Hippo RAG 2 đang đọc: 

![[Pasted image 20250507023648.png]]
# 3. Next Presentation: Workflows, Agents 

- App The Coach mới: ...figma 

![[Pasted image 20250507014718.png]]


1 cách tổng quan nhất về tháp AI Agents 


![[Pasted image 20250423100353.png]]


---
# Update
- Vấn đề là: Kỹ thuật tốt, khả năng trình bày năng lượng. tuy nhiên, chưa mạch lạc nhiều chỗ conflict.

1. Tool: Paper AI => CHƯA RÕ MỤC ĐÍCH CUỐI CÙNG NGAY TỪ ĐẦU KHIẾN NGƯỜI NGHE PHẢI CHẠY THEO.
2. BỊ VỘI QUÁ, BỊ NÓI NHANH Ở NHIỀU CHỖ.
    
3. QUAN TRỌNG: Quên offer: Share group Facebook 1 phút thôi -)) Cơ mà quên mất.
---
1. Dự tính ban đầu là nói về RAG trước -> quay xe sang chuyển sang nói về Memory => Dẫn đến nhiều thông tin trong phần viết đầu bị thừa khi phải nói tổng quan
=> Sau: fix cứng phần sẽ nói + SLIDE. => Dẫn đến ko seeding được gì (Vector Embedding Wecommit100x, github cá nhân  ...)
2. Lỗi lướt text và lướt Obsidant 
3. Diễn giải 1 cách siêu dễ hiểu ? (a Trúc)
![[Pasted image 20250507105900.png]]
4. Ko đưa mắt để ý mọi người?
5. Điểm okela: nắm rõ các phần và có thể trả lời được các cases của ae do có chuẩn bị hết rồi. 
---
Hiểu cách nó hoạt động -> Dùng ngon hơn ?? 