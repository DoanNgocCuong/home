# Nhìn lại Quá trình 6h brainstorm và chuẩn bị giải pháp + 2h code full medium repo (ko theo Mem0 luôn -)))

1. # 1. Step 1: Research best practices Perflexity, Gemini, => Manus ra tài liệu All In One về Memory => Dùng nó để ra tài liệu cụ thể hơn cho dự án cần giải  (4h hôm trước + 10h - 12h sáng 20/12)
2. # 2. Step 2: Bài toán của mình + High Architect - Folder Structure - Data Flow + Source code zip + Template SDD => Mang vào Claude Ra SDD cho bài toán cần giải.   (Bấm nút và đợi)
3. # 3. Step 3: Mang ngược vào Manus để cho các giải pháp tối ưu hơn => Mang SDD + Phần SDD đã tối ưu vào Cursor gen code  (Bấm và đợi)
4. # 4. Check kết quả: Để nó tự code + Yêu cầu thêm: (1h-3h chiều)

+, Viết file test
+, Viết thêm pyproject.toml (có bug thì nhờ thằng Perflexity search cách fix xong import cho thằng Cursor nó check) (fix mãi fix mãi mới được)
+, Viết báo cáo
+, Viết thêm .env.example
+, Check xem có cơ chế tự động tạo bảng chưa của DB ? oke code
+, Chạy unicorn xong ko kết nối được với DB
=> Cho vào Cursor nó sửa để connect được với Postgres, Milvus, Redis done

=> Thế là check được API luôn rồi

```
curl --location 'http://localhost:30033/api/v1/extract_facts' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": "user_123",
    "conversation_id": "conv_456",
    "conversation": [
      {
        "role": "user",
        "content": "Tôi tên là Nguyễn Văn A, sống ở Hà Nội. Tôi thích đọc sách và chơi đàn guitar."
      },
      {
        "role": "assistant",
        "content": "Xin chào Nguyễn Văn A! Tôi đã ghi nhận thông tin của bạn."
      }
    ],
    "metadata": {
      "source": "test",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  }'
```

```
{
    "status": "success",
    "message": "Extracted 3 facts successfully",
    "data": {
        "facts_count": 3,
        "fact_ids": [
            "4abaf811-880a-4e47-a58f-507ba5e06bc9",
            "07e90571-f7d4-49f9-93a5-12c0ef19b1e0",
            "15483779-0043-42bc-8881-50226308bfda"
        ],
        "facts": [
            {
                "id": "4abaf811-880a-4e47-a58f-507ba5e06bc9",
                "content": "Nguyễn Văn A sống ở Hà Nội.",
                "category": "relationship",
                "confidence": 1.0,
                "created_at": "2025-12-20T08:02:52.502681"
            },
            {
                "id": "07e90571-f7d4-49f9-93a5-12c0ef19b1e0",
                "content": "Nguyễn Văn A thích đọc sách.",
                "category": "preference",
                "confidence": 1.0,
                "created_at": "2025-12-20T08:02:52.502681"
            },
            {
                "id": "15483779-0043-42bc-8881-50226308bfda",
                "content": "Nguyễn Văn A thích chơi đàn guitar.",
                "category": "preference",
                "confidence": 1.0,
                "created_at": "2025-12-20T08:02:52.502681"
            }
        ]
    }
}
```

---

```
curl --location 'http://localhost:30033/api/v1/search_facts' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": "user_123",
    "query": "Người dùng thích gì?",
    "limit": 10,
    "score_threshold": 0.4
  }'
```

```
{
    "status": "success",
    "data": {
        "query": "Người dùng thích gì?",
        "results_count": 5,
        "results": [
            {
                "fact_id": "15483779-0043-42bc-8881-50226308bfda",
                "content": "Nguyễn Văn A thích chơi đàn guitar.",
                "category": "preference",
                "score": 0.6195762395858764,
                "created_at": "2025-12-20T01:02:52.502681+00:00",
                "related_facts": []
            },
            {
                "fact_id": "5f4a32b0-37e0-4003-9f66-736497237d6b",
                "content": "Nguyễn Văn A thích chơi đàn guitar.",
                "category": "preference",
                "score": 0.6195762395858764,
                "created_at": "2025-12-20T00:58:16.229158+00:00",
                "related_facts": []
            },
            {
                "fact_id": "07e90571-f7d4-49f9-93a5-12c0ef19b1e0",
                "content": "Nguyễn Văn A thích đọc sách.",
                "category": "preference",
                "score": 0.6179321557283401,
                "created_at": "2025-12-20T01:02:52.502681+00:00",
                "related_facts": []
            },
            {
                "fact_id": "a444bdee-4b63-40f5-b485-7907b0bb4325",
                "content": "Nguyễn Văn A thích đọc sách.",
                "category": "preference",
                "score": 0.6179321557283401,
                "created_at": "2025-12-20T00:58:16.229158+00:00",
                "related_facts": []
            },
            {
                "fact_id": "f51e02b3-e550-4453-bf8a-2672020f4b57",
                "content": "Nguyễn Văn A likes reading books.",
                "category": "preference",
                "score": 0.2810041785240173,
                "created_at": "2025-12-20T00:52:55.954358+00:00",
                "related_facts": []
            }
        ]
    }
}
```

---