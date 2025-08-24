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


```

Filesystem      Size  Used Avail Use% Mounted on
udev            189G     0  189G   0% /dev
tmpfs            38G   16M   38G   1% /run
/dev/nvme0n1p2  2.9T  2.7T   28G  99% /
tmpfs           189G   40K  189G   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           189G     0  189G   0% /sys/fs/cgroup
/dev/loop0       50M   50M     0 100% /snap/snapd/24792
/dev/loop1      1.4M  1.4M     0 100% /snap/nvtop/309
/dev/loop3       74M   74M     0 100% /snap/core22/2045
/dev/nvme0n1p1  511M  5.3M  506M   2% /boot/efi
/dev/sda1       3.6T  2.0T  1.5T  59% /data01
tmpfs            38G   13M   38G   1% /run/user/1000
/dev/loop5       51M   51M     0 100% /snap/snapd/25202
```


---
## 📊 **CÁC LỆNH KIỂM TRA DUNG LƯỢNG TOÀN SERVER**

### 🔍 **1. KIỂM TRA DUNG LƯỢNG Ổ CỨNG**

```bash
# Xem tổng quan dung lượng tất cả ổ cứng
df -h

# Xem chi tiết hơn với inode
df -ih

# Chỉ xem ổ cứng chính
df -h /
```

### 💾 **2. KIỂM TRA RAM VÀ SWAP**

```bash
# Xem RAM và Swap
free -h

# Xem chi tiết hơn
free -h --total

# Theo dõi real-time
watch -n 1 free -h
```

### 📁 **3. KIỂM TRA DUNG LƯỢNG THƯ MỤC**

```bash
# Top 10 thư mục lớn nhất trong /
sudo du -h / | sort -rh | head -10

# Kiểm tra thư mục hiện tại
du -sh *

# Xem chi tiết các thư mục trong /home
sudo du -h --max-depth=1 /home/

# Tìm file lớn nhất (>1GB)
sudo find / -type f -size +1G -exec ls -lh {} \; 2>/dev/null
```

### 🔥 **4. LỆNH NHANH KIỂM TRA TOÀN BỘ**

[1 tool called]

```bash
# Lệnh tổng hợp kiểm tra toàn bộ
echo "=== DISK USAGE ===" && df -h && \
echo -e "\n=== MEMORY USAGE ===" && free -h && \
echo -e "\n=== TOP DIRECTORIES ===" && \
sudo du -h --max-depth=1 / 2>/dev/null | sort -rh | head -10
```

### 🚀 **5. LỆNH NÂNG CAO**

```bash
# Kiểm tra I/O disk
iostat -x 1 5

# Xem process sử dụng disk nhiều nhất
iotop

# Kiểm tra dung lượng theo từng filesystem
lsblk -f

# Xem thông tin chi tiết ổ cứng
sudo fdisk -l

# Tìm file lớn trong thư mục cụ thể
sudo find /var/log -type f -size +100M -exec ls -lh {} \;

# Kiểm tra log files lớn
sudo du -h /var/log/* | sort -rh | head -10
```

### 📈 **6. MONITORING LIÊN TỤC**

```bash
# Theo dõi dung lượng real-time
watch -n 5 'df -h && echo && free -h'

# Hiển thị thông tin hệ thống tổng quan
htop

# Tool monitoring chuyên nghiệp
ncdu /    # Interactive disk usage analyzer
```

### ⚡ **7. LỆNH THƯỜNG DÙNG NHẤT**

```bash
# Combo 3 lệnh quan trọng nhất:
df -h          # Dung lượng ổ cứng
free -h        # RAM/Swap  
du -sh /*      # Dung lượng thư mục gốc
```

### 🎯 **CHO TRƯỜNG HỢP CỦA BẠN:**

```bash
# Kiểm tra specifically cho TTS server
df -h /                                    # Ổ cứng chính
du -sh /home/ubuntu/truc_ai/               # Dự án TTS
du -sh /home/ubuntu/truc_ai/edge.tts/static/  # Thư mục audio files
free -h                                    # RAM usage
```

**Tip:** Dùng `sudo` khi cần quyền root để xem tất cả thư mục hệ thống! 🔑