# Technical Writing Best Practices

## Mục lục
1. [Nguyên tắc cơ bản](#nguyên-tắc-cơ-bản)
2. [Cấu trúc tài liệu](#cấu-trúc-tài-liệu)
3. [Ngôn ngữ & Phong cách](#ngôn-ngữ--phong-cách)
4. [Định dạng & Trình bày](#định-dạng--trình-bày)
5. [Checklist trước khi publish](#checklist-trước-khi-publish)

---

## Nguyên tắc cơ bản

### 1. Viết rõ ràng (Clarity)
- Sử dụng câu ngắn, đơn giản
- Tránh jargon không cần thiết
- Mỗi câu nên có một ý chính
- Định nghĩa các thuật ngữ khi sử dụng lần đầu

### 2. Viết súc tích (Conciseness)
- Loại bỏ từ thừa, cụm từ rỗng
- Không lặp lại cùng một ý
- Sử dụng từ ngắn gọn khi có thể
- Tránh câu bị động phức tạp

### 3. Viết chính xác (Accuracy)
- Kiểm tra thông tin trước khi viết
- Đảm bảo code/ví dụ chạy được
- Sử dụng số liệu cụ thể, trích dẫn nguồn
- Cập nhật tài liệu khi có thay đổi

### 4. Viết có cấu trúc (Structure)
- Sử dụng headings rõ ràng
- Chia nhỏ thành các section logic
- Sử dụng bullet points cho danh sách
- Mỗi đoạn nên có một ý chính

---

## Cấu trúc tài liệu

### Header/Meta
```
---
title: [Tên bài viết]
description: [Mô tả ngắn 1-2 câu]
author: [Tên tác giả]
date: [Ngày tạo/cập nhật]
tags: [danh-sách-tags]
---
```

### Cấu trúc bài viết
1. **Introduction** - Giới thiệu, mục đích
2. **Prerequisites** - Điều kiện tiên quyết (nếu có)
3. **Main Content** - Nội dung chính
   - Chia thành các section nhỏ
   - Mỗi section = một chủ đề
4. **Examples** - Ví dụ minh họa
5. **Summary/Kết luận** - Tóm tắt, next steps

### Headings
- Sử dụng heading levels đúng cách (H1 → H2 → H3)
- Heading nên là danh từ hoặc cụm danh từ
- Không skip levels (H1 → H3 bỏ qua H2)

---

## Ngôn ngữ & Phong cách

### Giọng điệu
- **Chuyên nghiệp**: Trang trọng nhưng thân thiện
- **Hướng người đọc**: "Bạn sẽ...", "Chúng ta sẽ..."
- **Chủ động**: Sử dụng câu chủ động
- **Nhất quán**: Giữ same tone xuyên suốt

### Từ vựng
| Nên dùng | Tránh dùng |
|----------|------------|
| sử dụng | tận dụng, khai thác |
| tạo | khởi tạo, thiết lập |
| xem | quan sát, theo dõi |
| tìm | tìm kiếm, truy xuất |
| bắt đầu | bắt đầu tiến hành |

### Câu
- Độ dài lý tưởng: 15-25 từ
- Tối đa: 40 từ
- Một câu = một ý

---

## Định dạng & Trình bày

### Code Blocks
- Luôn chỉ định ngôn ngữ: ```javascript, ```python
- Thêm comment giải thích
- Format nhất quán (indent, spacing)

### Tables
- Sử dụng khi so sánh >2 items
- Có header rõ ràng
- Căn lề phù hợp

### Lists
- Bullet: Khi thứ tự không quan trọng
- Numbered: Khi có thứ tự/sequence
- Thống nhất punctuation trong list

### Links
- Anchor text mô tả nội dung (không dùng "click here")
- Kiểm tra link không bị broken

---

## Checklist trước khi publish

### Nội dung
- [ ] Kiểm tra chính tả và ngữ pháp
- [ ] Xác minh thông tin, số liệu
- [ ] Đảm bảo ví dụ/code chạy được
- [ ] Kiểm tra logic và flow

### Format
- [ ] Headings đúng level
- [ ] Code blocks có language specified
- [ ] Images có alt text
- [ ] Links hoạt động

### SEO (nếu cần)
- [ ] Title có keywords
- [ ] Meta description đầy đủ
- [ ] URL thân thiện

---

## Tài liệu tham khảo

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)
- [Write the Docs](https://www.writethedocs.org/)
