- 
- Chunk theo ký tự + sentences 
- Nhúng câu/nhúng từ. -> chọn model -> ra biểu diễn vector
1. Documents => Vector Database 
(1 vector nhỏ là vector câu hay từ, hay đoạn, hoặc vector là 1 chunk, ..)  
2. Search và Retrieval 
- Pha indexing , ...
- Vector indexing, ... <Modul indexing>, 
- Indexing: có các cái nào gần => phân cấp => co lại gần nhau => tăng khả năng search? 
- (search theo nhiều cách, dựa vào indexing để search cho nhanh, ...)
------------
indexing - quan trọng để tìm kiếm nhanh, 


```
**Chunking theo phân cấp** (hierarchical chunking) là một kỹ thuật tổ chức thông tin thành các nhóm (hoặc "chunk") theo cấp độ khác nhau, từ tổng quát đến chi tiết hơn. Cách tiếp cận này giúp não bộ dễ dàng nắm bắt và xử lý thông tin phức tạp bằng cách chia nhỏ chúng thành các phần có cấu trúc rõ ràng và logic. 

### Các bước thực hiện chunking theo phân cấp:


### Ví dụ về chunking theo phân cấp:

**Cấp 1**: Hệ thống động vật  
→ **Cấp 2**: Động vật có xương sống | Động vật không xương sống  
→ **Cấp 3 (cho động vật có xương sống)**: Động vật lưỡng cư | Động vật có vú | Động vật bò sát  

**Lợi ích của chunking theo phân cấp**:
- Giúp người học dễ dàng tiếp thu kiến thức từng phần, không bị quá tải thông tin.
- Tăng cường khả năng ghi nhớ thông qua sự phân loại và tổ chức rõ ràng.
- Giúp việc giảng dạy hoặc học tập trở nên logic và hệ thống hơn.

Kỹ thuật này đặc biệt hữu ích trong việc giảng dạy hoặc học tập các môn học có khối lượng thông tin lớn như sinh học, lịch sử, hoặc toán học.
``

==============
Đánh chỉ mục indexing theo đơn giản nhất là các chunking 
=> chỉ mục theo các phân cấp (document indexing, paragraph indexing, ...)
Phân cấp >> indexing nhanh hơn phân cụm 

- Document, paragraph, senttences, 
LỰA CHỌN BIỂU DIỄN BẰNG VECTOR , SAU ĐÓ INDEXING VECTOR? 
MODEL NÀO ĐANG TỐT ĐỂ LẤY THÔNG TIN NHIỀU MỨC: 

-----------
search từ trên xuống hay từ dưới lên. 
- nếu từ trên xuống thì
=====================

1. Chốt lại Embedding như nào d, title, paragraph, sentences => Indexing nhanh => Search mới nhanh, Retrieval mới nhanh (kỹ thuật học biểu diễn query và biểu diễn documents => cùng 1 kiểu). 
2. BERT học biểu diễn mức tokenizer, Học biểu diễn câu, semantic, đơn vị chunking nhỏ (câu) - ... theo chiều dài chunking 256-512-...
(mức câu, câu dài, câu ngắn, liên quan đến câu trước - ... mất thông tin), ...

+, Mức từ : BM25
+, Mức câu: nhúng, model: BAAI/bge-en-1.5
+, Bi-encoder, Cross-encoder 
(sentences -> bert (sq2sq) -> pooling -> vector)
 Cách thức pooling: học(cặp câu tương đồng cặp embedding) để nó ra hay tính trung bình, hay min, Bi-encoder để search, cross-encoder để reranks???
+, Context: A B -> LLM: A ... B ...
RERANK+ REFINE: (summary của các phần chunk được chẳng hạn, ... summary context đủ context cho LLM ko nhiễu, coi mỗi câu là 1 nút, vẽ đồ thị các cạnh trọng số. TÓM TẮT HƯỚNG CÂU HỎI - TÓM TẮT THEO HƯỚNG CỦA CÂU HỎI)


==============

vVector từ ko ổn, vector câu vì nó có nghĩa, 