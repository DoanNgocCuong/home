1. Có gì ko biết cứ gpt ko phải nhớ: 
- Quay lại commit trước đó: `git reset --hard fff1206`
- **Gỡ commit gần nhất nhưng giữ lại thay đổi (soft reset)**: `git reset --soft HEAD^`
- **Gỡ commit gần nhất và loại bỏ luôn thay đổi (hard reset)**:
3. Đánh dấu phiên bản: demo, deploy 1.1, ....

#### Bug:
- `GH013: Repository rule violations found for refs/heads/main`. Điều này có nghĩa là GitHub đã phát hiện vi phạm quy tắc bảo vệ repository (repo), chẳng hạn như đẩy thông tin bí mật (secrets) lên. <**Sử dụng `.gitignore`**: Nếu bạn có các file chứa thông tin nhạy cảm hoặc không muốn chúng bị đẩy lên GitHub, hãy thêm các file đó vào file `.gitignore` để Git không theo dõi chúng.>
	- **Xóa thông tin nhạy cảm khỏi lịch sử commit** (nếu cần):`git reset --soft HEAD~1`  - ngược của cái này là : 
	- Bạn có thể dùng lệnh để xoá commit nhạy cảm - gpt
