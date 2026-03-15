# RAG Overview: Retrieval-Augmented Generation

## RAG là gì?

RAG (Retrieval-Augmented Generation) là một kiến trúc kết hợp hai thành phần chính:

1. **Retrieval (Truy vấn)**: Tìm kiếm các tài liệu hoặc passage liên quan nhất từ một kho tài liệu lớn
2. **Generation (Sinh tạo)**: Sử dụng các tài liệu đã tìm được làm ngữ cảnh để LLM sinh ra câu trả lời chính xác hơn

Thay vì dựa hoàn toàn vào kiến thức huấn luyện của LLM (có thể lỗi thời hoặc không đầy đủ), RAG cho phép mô hình truy cập thông tin mới nhất từ các nguồn dữ liệu bên ngoài.

```
Người dùng hỏi
      ↓
Tìm kiếm tài liệu liên quan
      ↓
Kết hợp tài liệu + câu hỏi
      ↓
LLM sinh ra câu trả lời
      ↓
Trả lời người dùng
```

## Tại sao RAG quan trọng?

**1. Cập nhật kiến thức**
- LLM không cần fine-tuning khi dữ liệu thay đổi
- Thêm nguồn dữ liệu mới mà không cần huấn luyện lại

**2. Giảm hallucination**
- LLM dựa vào tài liệu thực tế thay vì "tưởng tượng"
- Có thể trích dẫn nguồn (source attribution)

**3. Tính minh bạch (Transparency)**
- Người dùng biết thông tin từ đâu
- Dễ dàng audit và verify

**4. Chi phí thấp hơn**
- Không cần fine-tuning toàn bộ mô hình
- Chỉ cần quản lý vector database và embedding

## Ba pha chính của RAG

### Pha 1: Offline/Ingestion (Xử lý dữ liệu)
```
Tài liệu gốc → Parsing → Chunking → Embedding → Lưu Vector DB
```
Chạy một lần hoặc khi dữ liệu thay đổi. Xây dựng kho kiến thức.

### Pha 2: Online/Retrieval (Truy vấn thời gian thực)
```
Câu hỏi người dùng → Embedding → Tìm kiếm Vector → Truy xuất chunk → Trả về LLM
```
Chạy mỗi lần người dùng hỏi. Tìm tài liệu phù hợp.

### Pha 3: Evaluation & Optimization (Đánh giá và tối ưu)
```
So sánh output → Đánh giá relevance → Điều chỉnh → Tối ưu lại
```
Đo lường chất lượng hệ thống và cải thiện.

## So sánh RAG với các phương pháp khác

| Phương pháp | Ưu điểm | Nhược điểm | Khi nào dùng |
|-------------|---------|-----------|-------------|
| **RAG** | Dữ liệu mới nhất, chi phí thấp, transparent | Cần vector DB, latency cao | Dữ liệu thay đổi, cần source citation |
| **Fine-tuning** | Mô hình học sâu, chi phí inference thấp | Đắt tiền, chậm update, cần GPU | Dữ liệu ổn định, style riêng |
| **Prompt Engineering** | Nhanh, rẻ, không cần infra | Phụ thuộc model knowledge, limited context | Prototype, simple tasks |
| **In-context Learning** | Flexible, không cần training | Token usage cao, limited examples | Few-shot learning |

**Thực tế**: Hầu hết các production system kết hợp cả ba. Ví dụ: Fine-tuned LLM + RAG + good prompt engineering.

## Kiến trúc RAG tổng quát

```
┌─────────────────────────────────────────────────────────────┐
│ OFFLINE PHASE (Chạy một lần)                                │
├─────────────────────────────────────────────────────────────┤
│ Documents → Parser → Chunker → Embedder → Vector Store      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ONLINE PHASE (Chạy mỗi query)                               │
├─────────────────────────────────────────────────────────────┤
│ User Query → Embedder → Retriever → Context Builder         │
│                                           ↓                  │
│                                         LLM ← Prompt        │
│                                           ↓                  │
│                                       Response              │
└─────────────────────────────────────────────────────────────┘
```

## Khi nào sử dụng RAG?

✅ **Dùng RAG**
- Dữ liệu thay đổi thường xuyên (news, products, logs)
- Cần trích dẫn nguồn (compliance, academic)
- Dữ liệu lớn và không thể fit vào LLM context
- Dữ liệu riêng tư hoặc proprietary

❌ **Không cần RAG**
- LLM đã biết thông tin cần thiết
- Dữ liệu rất nhỏ (fit vào prompt)
- Yêu cầu latency cực thấp (< 100ms)

## Tóm tắt các phase

| Phase | Nhiệm vụ | Tần suất | Output |
|-------|---------|---------|--------|
| Offline | Xử lý & lưu trữ documents | 1 lần/khi update | Vector DB sẵn sàng |
| Online | Truy vấn & sinh response | Mỗi user query | Answer + sources |
| Eval | Đánh giá chất lượng | Định kỳ | Metrics & improvements |

---

## Key Takeaway

RAG là giải pháp hoàn hảo khi bạn cần LLM biết về dữ liệu luôn thay đổi mà không muốn retrain model. Ba pha (Offline → Online → Eval) hoạt động như một hệ thống liên tục: Offline phase xây dựng kho kiến thức, Online phase trích xuất kiến thức khi được hỏi, Eval phase đảm bảo chất lượng. Hiểu rõ từng pha sẽ giúp bạn design hệ thống RAG hiệu quả.
