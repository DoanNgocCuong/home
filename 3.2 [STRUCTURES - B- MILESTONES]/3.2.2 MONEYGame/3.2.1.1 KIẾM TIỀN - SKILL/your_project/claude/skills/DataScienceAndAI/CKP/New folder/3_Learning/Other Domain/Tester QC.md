Em gửi anh @Cuong Vu Cao report test web tối ưu mới cho part 2 ạ
Test phần tối ưu part 2
1. Tiêu chí:
- Gãy luồng
- Tốc độ: thời gian trả ra response của bot
- Độ chính xác: đang đánh giá về data/ content, câu hỏi có hợp lý? có đúng? có lặp? hay thiếu không? đánh giá phần câu nâng cấp. 
2. Method test: manual
3. Số lượng phiên test: 22 (mỗi phiên 25-30p), luân phiên các chủ đề 
4. Kết quả: dựa trên số lượt các vấn đề lỗi của mỗi phiên test trên tổng số phiên
- Gãy luồng: 27% (6 times /22 sessions)
- Độ chính xác
+ Vấn đề về data/ content : 27% (6 times /22 sessions)
+ Vấn đề về phần nâng cấp: 18% (4 times/ 22 sessions)
- Tốc độ: 
+ Phần Brainstoming: đánh giá chung thì call response ở nhanh (sau khi có speech to text thì chắc sẽ thêm thời gian để audio chạy xong).
+ Phần Expression: Thời gian xử lý, call API mỗi lần đến phần sửa câu khá lâu, trung bình 8-10s 
- Khác: 40% (9 times/ 22 sessions) - các vấn đề về flow học, call thiếu API, thiếu các phần học, bot phản hồi...
- Pass: 18% (4 times/ 22 sessions) - đi full luồng không có vấn đề gì
https://docs.google.com/spreadsheets/d/1Hdq8BuYVmGzg4ofPYcq3mqLvtJlXo0_pRrSDnRli2wQ/edit?gid=0#gid=0

Đánh giá sâu hơn về học thuật và nội dung bài học thì em nhờ chị @Thanh Hà Lưu  và bạn @Đào Hạ Vũ  trải nghiệm nhé ạ





----
```
Em note 1 xíu ạ:

Quá trình QC có thể là:
+, QC AI /Agents. (Người QC Prompt)
+, QC định tính User
+, QC người chi tiết + QC định lượng User để update
```