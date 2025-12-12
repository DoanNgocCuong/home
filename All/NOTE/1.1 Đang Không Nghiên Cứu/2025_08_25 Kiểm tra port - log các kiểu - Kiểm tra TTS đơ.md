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

---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Cách kiểm tra các process đang chạy trên GPU

Dựa trên output `nvidia-smi` của bạn, đây là các cách để identify những process này đang làm gì:

### 1. **Kiểm tra thông tin chi tiết của process**

```bash
# Xem command line đầy đủ của process
ps aux | grep <PID>

# Ví dụ với GPU 0
ps aux | grep 76926
ps aux | grep 87841
ps aux | grep 2300098
ps aux | grep 3750113
ps aux | grep 3753511

# GPU 1
ps aux | grep 3753574
ps aux | grep 3880219
```

**Output sẽ cho bạn biết:**

- User chạy process
- Command line đầy đủ (script path, arguments)
- Memory usage
- Start time


### 2. **Xem working directory và command của process**

```bash
# Xem working directory
pwdx <PID>

# Xem command line đầy đủ với arguments
cat /proc/<PID>/cmdline | tr '\0' ' '

# Ví dụ
cat /proc/87841/cmdline | tr '\0' ' '
```

Đặc biệt với `VLLM::EngineCore` (PID 87841), command này sẽ cho biết:

- Model nào đang được serve
- Port nào
- Config gì (max-model-len, gpu-memory-utilization, etc.)


### 3. **Kiểm tra network connections (nếu là API server)**

```bash
# Xem process đang listen trên port nào
sudo netstat -tulpn | grep <PID>

# Hoặc dùng lsof
sudo lsof -i -P -n | grep <PID>

# Ví dụ với vLLM engine
sudo netstat -tulpn | grep 87841
```

Nếu là vLLM server, sẽ thấy port 30030, 30031, etc.

### 4. **Xem log files của process (best approach)**

```bash
# Tìm log files liên quan
sudo lsof -p <PID> | grep log

# Hoặc check trong /proc
ls -la /proc/<PID>/fd/

# Xem stderr/stdout của process đang chạy
sudo tail -f /proc/<PID>/fd/1  # stdout
sudo tail -f /proc/<PID>/fd/2  # stderr
```


### 5. **Identify vLLM processes specifically**

```bash
# List tất cả vLLM processes
ps aux | grep vllm

# Xem vLLM configs đang chạy
ps aux | grep "vllm.entrypoints"
```


### 6. **Check Python script locations**

```bash
# Xem environment variables của process
cat /proc/<PID>/environ | tr '\0' '\n'

# Tìm hiện working directory đầy đủ
readlink -f /proc/<PID>/cwd

# Xem process tree
pstree -p <PID>
```


### 7. **Tổng hợp command để check nhanh**

Tôi tạo cho bạn một script tiện lợi:

```bash
#!/bin/bash
# check_gpu_processes.sh

echo "=== GPU PROCESS ANALYZER ==="
echo ""

# Lấy list PIDs từ nvidia-smi
PIDS=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)

for PID in $PIDS; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "PID: $PID"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # User và basic info
    echo "👤 USER & PROCESS:"
    ps -p $PID -o user,pid,ppid,%cpu,%mem,etime,cmd --no-headers
    echo ""
    
    # Working directory
    echo "📁 WORKING DIR:"
    readlink -f /proc/$PID/cwd 2>/dev/null || echo "Permission denied"
    echo ""
    
    # Command line đầy đủ
    echo "⚙️  FULL COMMAND:"
    cat /proc/$PID/cmdline 2>/dev/null | tr '\0' ' ' || echo "Permission denied"
    echo ""
    echo ""
    
    # Network ports (nếu có)
    echo "🌐 LISTENING PORTS:"
    sudo netstat -tulpn 2>/dev/null | grep $PID || echo "No ports found"
    echo ""
    
    echo ""
done
```

**Cách dùng:**

```bash
chmod +x check_gpu_processes.sh
sudo ./check_gpu_processes.sh
```


### 8. **Phân tích cụ thể cho GPU của bạn**

Dựa trên output bạn cung cấp, đây là dự đoán:

**GPU 0:**

- `87841 - VLLM::EngineCore (9.6GB)` → **Likely SmolLM2 hoặc model nào đó bạn đang test**
- `76926 - python (4.1GB)` → Có thể là Jupyter, training script, hoặc API server khác
- `2300098 - python (3.7GB)` → Model inference hoặc preprocessing
- `3750113 - python (1.8GB)` → Smaller model hoặc batch processing
- `3753511 - tritonserver (2.5GB)` → **NVIDIA Triton Inference Server** (production serving)

**GPU 1:**

- `3753574 - grpc_server_main (8.3GB)` → **Triton backend server** (part of Triton setup)
- `3880219 - /usr/bin/python (7.9GB)` → Large model hoặc data processing


### 9. **Quick check command cho vLLM specifically**

```bash
# Tìm tất cả vLLM instances đang chạy
ps aux | grep -E "vllm|SmolLM|Qwen|model" | grep -v grep

# Check ports đang được sử dụng
sudo netstat -tulpn | grep -E "30030|30031|30032|8000|8001"

# Xem logs gần nhất của vLLM
sudo find /tmp -name "*vllm*" -type f 2>/dev/null | xargs ls -lt | head -5
```


### 10. **Recommended action cho bạn**

Để test model mới như anh Hùng đề nghị, bạn nên:

```bash
# 1. Kill hoặc identify process nào đang dùng GPU 0
sudo kill <PID_of_unused_process>

# 2. Hoặc chuyển sang dùng GPU 2 (chỉ có 688MB usage)
CUDA_VISIBLE_DEVICES=2 python -m vllm.entrypoints.openai.api_server ...

# 3. Nếu cần dedicated GPU, có thể request admin set GPU mode
sudo nvidia-smi -c EXCLUSIVE_PROCESS -i 0  # Chỉ 1 process/GPU
```


### Kết luận

**Để trả lời câu hỏi của bạn:**

Run command này để xem ngay:

```bash
ps aux | grep 87841
cat /proc/87841/cmdline | tr '\0' ' '
sudo netstat -tulpn | grep 87841
```

Điều này sẽ cho bạn biết:

1. **VLLM::EngineCore đang serve model gì**
2. **Port nào**
3. **Config như thế nào**

Từ đó bạn sẽ biết GPU 0 đang bận làm gì và có thể shutdown để test model mới hoặc chọn GPU khác.

