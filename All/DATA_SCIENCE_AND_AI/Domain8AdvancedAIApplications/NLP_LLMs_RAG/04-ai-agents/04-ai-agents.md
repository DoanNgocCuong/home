1. Tài liệu từ GG chuẩn Langchain, Langgraph: [Agentic Design Patterns - Google Tài liệu](https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/edit?tab=t.0#heading=h.pxcur8v2qagu)
2. Phần xây core em đang đề xuất là

* Agent core dùng langchain và langgraph

+ có hỗ trợ sẵn streaming event đồng bộ và bất đồng bộ về bên gọi tới (phần bất đồng bộ có thể cân nhắc Celery, Kafka, RabbitMQ)
+ có hỗ trợ mcp client để nối các tool nội bộ và tool ngoài
+ có hỗ trợ ghi log theo trace theo chuẩn Opentelemetry để trace log trên multi service
+ có hỗ trợ kết nối đến SQL db và non-SQL db (để làm AI Workflow và lưu trữ dữ liệu xử lý cho phía nghiệp vụ)

* Tool Hub: lưu trữ các tool nội bộ (save to memory, retrieval,..) theo chuẩn MCP Server
* Monitoring service: Langfuse, act as OTLP backend để nhận log từ nhiều service, lưu prompt, thống kê số lượng token
