1. JSONB (hiện tại — nên giữ):

- Có thể query: WHERE memories_extracted @> '[{"id": "mem_123"}]'

- GIN index hỗ trợ truy vấn nhanh

- PostgreSQL tự nén hiệu quả

- Storage: ~20–30% overhead so với TEXT, nhưng có lợi khi query

- Phù hợp với dữ liệu có cấu trúc

1. TEXT (không nên):

- Không thể query trực tiếp (phải CAST → chậm)

- Không có index hiệu quả

- Phải parse mỗi lần đọc

- Chỉ tiết kiệm chút storage, mất khả năng query

Đổi sang TEXT thay vì JSONB. Lưu ý: TEXT(JSONB) không phải cú pháp PostgreSQL; chúng ta dùng TEXT để lưu JSON dưới dạng string. Cập nhật code: