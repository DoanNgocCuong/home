```
Nếu LLM gốc lỗi thì chuyển sang model dự phòng nhẹ hơn ?

+, Nếu sau 1.5s mà model chính chưa trả ra response, thì call đến model gpt-4o-mini

đồng thời báo log là "model chính đã lỗi, chuyển qua dùng model gpt-4o-mini" thay thế.

+, Trong quá trình model gpt-4o-mini đang chạy thì trong lúc đó 2 model: chính và model phụ này cái nào trả về trước thì lấy kết quả của cái đó

+, còn không sẽ trả .... (hiện tại ở code cũ, trong trường hợp fail call llms thì kết quả gì được trả ra?)
```

---
Hiện trạng: đoạn này không có retry/fallback. Nếu LLM chính lỗi (timeout, network, 4xx/5xx, JSON hỏng), `llm_base.get_response` sẽ ném exception (hoặc trả `None` tùy implement trong lớp LLM) và luồng phía trên phải tự bắt; bản thân hàm không trả giá trị fallback nào. Không có chờ song song hay chuyển sang model khác.

Để đáp ứng yêu cầu:  
- Đặt timeout 1.5s cho call model chính.  
- Chạy song song model chính và model phụ gpt-4o-mini sau 1.5s nếu chính chưa xong; ai về trước lấy kết quả đó.  
- Log cảnh báo: `"model chính đã lỗi, chuyển qua dùng model gpt-4o-mini"` khi bật nhánh fallback.  
- Nếu cả hai cùng fail hoặc cùng quá hạn: dùng response mặc định

Mô tả luồng đề xuất (logic, chưa code):  
1) Gọi model chính với timeout 1.5s (future A).  
2) Nếu A hoàn thành trong hạn → dùng kết quả, hủy job phụ (nếu đã kích hoạt).  
3) Nếu A chưa xong ở 1.5s → log cảnh báo, kích hoạt call gpt-4o-mini (future B).  
4) Chờ race A vs B; cái nào trả trước dùng cái đó; hủy future còn lại.  
5) Nếu cả A và B đều lỗi/timeout → trả response lỗi chuẩn hóa (kèm request_id).  

