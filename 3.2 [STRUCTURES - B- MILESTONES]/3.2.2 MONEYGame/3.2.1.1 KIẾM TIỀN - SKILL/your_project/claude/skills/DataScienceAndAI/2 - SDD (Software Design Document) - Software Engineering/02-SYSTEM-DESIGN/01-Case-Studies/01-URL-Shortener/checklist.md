# Checklist Ôn Tập - URL Shortener

## Câu hỏi cơ bản
- [ ] Tại sao cần URL shortener? Liệt kê 3 use cases thực tế
- [ ] Read:Write ratio là bao nhiêu? Tại sao?
- [ ] 301 vs 302 redirect — khi nào dùng cái nào?

## Câu hỏi thiết kế
- [ ] So sánh 3 cách tạo short URL (hash, counter, KGS) — ưu nhược mỗi cái?
- [ ] Base62 encoding hoạt động thế nào? Tại sao 7 ký tự là đủ?
- [ ] Nếu 2 users gửi cùng 1 long URL, short URL có giống nhau không? Tại sao?
- [ ] Làm sao xử lý khi short key bị collision?

## Câu hỏi scale
- [ ] Cần bao nhiêu storage cho 5 năm? Tính thử
- [ ] Tại sao dùng cache? Cache cái gì?
- [ ] Database nên shard theo key nào?
- [ ] Nếu QPS tăng 10x, thay đổi gì trong architecture?

## Câu hỏi nâng cao
- [ ] Làm sao track analytics mà không ảnh hưởng redirect latency?
- [ ] Rate limiting implement ở đâu? Bằng gì?
- [ ] Nếu KGS chết thì sao? Backup plan?
- [ ] Làm sao expire old URLs hiệu quả?

## Bài tập thực hành
- [ ] Vẽ lại architecture diagram từ đầu (không nhìn)
- [ ] Estimate QPS và storage cho 1 billion URLs
- [ ] Giải thích design cho partner trong 5 phút
