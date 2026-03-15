Anh tóm lại đơn giản thế này:

- **Agent gateway** giống như một lễ tân nhận những câu hỏi, yêu cầu từ người dùng.
    
- Lễ tân này không tự trả lời hết tất cả mà sẽ gửi yêu cầu đó đến **nhiều phòng ban chuyên môn** (các server MCP phía sau), mỗi phòng ban xử lý một việc riêng (ví dụ: lấy tài liệu AWS, sinh sơ đồ, truy xuất mã nguồn...).
    
- Mỗi phòng ban trả lại kết quả cho lễ tân.
    
- Lễ tân sẽ **tổng hợp các câu trả lời từ các phòng ban**, chọn lọc, ghép lại, và gửi kết quả cuối cùng cho người dùng.
    

**Nghĩa là:**

- Người dùng/AI agent hỏi → gateway chuyển câu hỏi cho nhiều server chuyên môn → các server trả lời → gateway tổng hợp và gửi đáp án hoàn chỉnh về lại cho người dùng/agent.
    

Giống như một hệ thống nhiều chuyên gia, mỗi người phụ trách một mảng, còn gateway là người điều phối/tổng hợp mọi thứ lại cho bạn!

1. [https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)

---
![](image/Pasted%20image%2020251105160658.png)