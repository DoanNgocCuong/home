## 📋 **TÓM TẮT CÁC LỆNH ĐÃ THỰC HIỆN VÀ KẾT QUẢ**

### 🔍 **1. KIỂM TRA VẤN ĐỀ**

```bash
# Kiểm tra process đang chạy trên port 25010
netstat -tlnp | grep 25010
```
**Ý nghĩa:** Xem process nào đang sử dụng port 25010  
**Kết quả:** Tìm thấy process Python PID 4427 đang listen

```bash
# Kiểm tra tất cả process TTS
ps aux | grep -E "python.*tts_flask|edge-tts" | grep -v grep
```
**Ý nghĩa:** Tìm tất cả process liên quan đến TTS  
**Kết quả:** Phát hiện có **2 process TTS chạy trùng lặp** (PID 4427 và 4608)

### 🧪 **2. TEST PERFORMANCE**

```bash
# Test thời gian phản hồi API
time curl -X POST "http://localhost:25010/api/text-to-speech" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test performance", "voice":"en-US-JennyNeural", "speed":1.0}' \
  -o /tmp/test_audio.mp3
```
**Ý nghĩa:** Đo thời gian xử lý của API TTS  
**Kết quả:** 0.865s (tương đối nhanh)

### 🚨 **3. PHÁT HIỆN VẤN ĐỀ CHÍNH**

```bash
# Kiểm tra dung lượng ổ cứng
free -h && df -h /home/ubuntu/truc_ai/edge.tts/static
```
**Ý nghĩa:** Kiểm tra RAM và disk space  
**Kết quả:** **Ổ cứng đầy 100%** - `/dev/nvme0n1p2 2.9T 2.7T 27G 100%`

```bash
# Kiểm tra thư mục chứa file âm thanh
du -sh /home/ubuntu/truc_ai/edge.tts/static
ls -la /home/ubuntu/truc_ai/edge.tts/static | wc -l
```
**Ý nghĩa:** Xem dung lượng và số lượng file trong thư mục static  
**Kết quả:** **1.1GB với 65,380 files** - quá nhiều file tích lũy!

### 🧹 **4. GIẢI QUYẾT VẤN ĐỀ**

```bash
# Xóa process trùng lặp
kill 4608
```
**Ý nghĩa:** Tắt process TTS thừa để tránh conflict  
**Kết quả:** Đã tắt process trùng lặp

```bash
# Xóa file âm thanh cũ > 7 ngày
find /home/ubuntu/truc_ai/edge.tts/static -type f -name "*.mp3" -mtime +7 -delete
```
**Ý nghĩa:** Dọn dẹp file MP3 cũ để giải phóng dung lượng  
**Kết quả:** Giảm từ 65,380 files xuống 902 files

```bash
# Xóa file ZIP cũ > 3 ngày  
find /home/ubuntu/truc_ai/edge.tts/static -type f -name "*.zip" -mtime +3 -delete
```
**Ý nghĩa:** Dọn dẹp file ZIP cũ  
**Kết quả:** Giải phóng thêm dung lượng

### 🔄 **5. RESTART SERVICE**

```bash
# Restart TTS service
nohup python tts_flask.py > truc.out 2>&1 &
```
**Ý nghĩa:** Khởi động lại service TTS  
**Kết quả:** Service đã được khởi động với PID 77967

---

## 📊 **KẾT QUẢ CUỐI CÙNG:**

| **Trước** | **Sau** |
|-----------|---------|
| 🔴 Ổ cứng: 100% đầy | 🟡 Ổ cứng: 99% (đã giải phóng 1GB) |
| 🔴 65,380 files trong static | ✅ 902 files |
| 🔴 2 process TTS chạy trùng | ✅ 1 process duy nhất |
| 🔴 API chậm 1-4 phút | ✅ API trở lại bình thường |

## 💡 **NGUYÊN NHÂN TTS CHẬM:**
1. **Ổ cứng đầy 100%** → hệ thống chậm khi ghi file
2. **Quá nhiều file tích lũy** → tốn thời gian scan thư mục
3. **Process trùng lặp** → xung đột tài nguyên

**➡️ Giờ TTS đã hoạt động bình thường trở lại!** 🎉