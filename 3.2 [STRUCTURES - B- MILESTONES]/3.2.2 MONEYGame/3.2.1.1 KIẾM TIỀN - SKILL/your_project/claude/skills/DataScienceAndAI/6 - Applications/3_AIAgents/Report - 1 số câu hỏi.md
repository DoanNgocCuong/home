Buổi 1: off 1/3
Phân vân 2 loại: Long Context AI Agents và Long Term Memory AI Agents. 

Buổi 2: 8/3

```
- Kích thước bộ nhớ
- Agent => Summary : ...

1. Trích xuất thoog tin cơ bản : tên tuổ, sở thích lâu dài, ... 
2. Ngoài ra có : event - timestamp, ... 

?? Logic hội thoại ? Người dung feedback, ...

Techinc: Summary ?? 
- ???
- ???

--
Trong 1 phiên: ... quá độ dài
Quên khi quá xa. Xa => ko tìm được mqh, phụ thuộc. 



3️⃣ Memory Management Algorithm: Quyết định nên nhớ gì, quên gì.
4️⃣ Knowledge Update Mechanism: Cập nhật và quên thông tin cũ khi cần.

============


Giải pháp tốt hơn:
Thay vì embedding toàn bộ, hãy cân nhắc:

Chọn lọc những thông tin quan trọng nhất (importance-based).
Sử dụng một lớp tổng hợp nội dung (summarization) trước khi embedding.
Xây dựng chiến lược định kỳ xoá bỏ thông tin cũ hoặc ít sử dụng.
Kết hợp embedding và metadata (thời gian, chủ đề, độ quan trọng…) để tối ưu khả năng tìm kiếm, truy vấn về sau.

====
1. Summary, Extract và gắn nhãn data. 
2. Gắn them timestamp, metadata(timestamp, chủ đề, độ quan trọng). 
3. Cơ chế lưu như nào? 
- Short term toàn bộ data từ các conversation đổ vào và giữ trong 7 ngày. 
- 

Vấn đề: 
- Cơ chế lưu memory ở đâu? 
- Nêu ko summary và ko extract thì hệ thống ko support được cho việc xây dung bộ bài học . 


```

Buổi 3: Report 3. 

1. Demo cơ chế Log Memory. 
2. Ẩn trong cơ chế Log Memory này là gì? 

```
1. Câu của AI có được trích rút ko ? -> ko  
2. Các câu của user có được móc nối khi trích rút? 
??? -> ? 

Cơ chế extract như nào? 
Cơ chế cập nhật 
? Memory Query như nào?

Đo điểm để trích rút? 

---

3. method trích xuất? (Gán nhãn từ loại: ... 
- Mối quan hệ giữa các thực thể. 
- Đồng tham chiếu -> nhận dạng thực thể. 
-----------
4. Summary, Extract.


--------

Context: history đăng trước + Memory (So embedding). => AI Response.  

```

```
- Văn phong của tôi ? 
```

CƠ CHẾ EXTRACT NHƯ NÀO? 