```bash
θ74° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn] 2s $ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            189G     0  189G   0% /dev
tmpfs            38G   18M   38G   1% /run
/dev/nvme0n1p2  2.9T  2.5T  229G  92% /
tmpfs           189G  241M  188G   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           189G     0  189G   0% /sys/fs/cgroup
/dev/loop0       64M   64M     0 100% /snap/core20/2599
/dev/loop1       74M   74M     0 100% /snap/core22/2111
/dev/loop2       50M   50M     0 100% /snap/snapd/24792
/dev/loop5      1.4M  1.4M     0 100% /snap/nvtop/309
/dev/loop4       51M   51M     0 100% /snap/snapd/25202
/dev/loop6       92M   92M     0 100% /snap/lxd/32662
/dev/nvme0n1p1  511M  6.1M  505M   2% /boot/efi
/dev/sda1       3.6T  3.3T  161G  96% /data01
tmpfs            38G  3.1M   38G   1% /run/user/1000
/dev/loop7       74M   74M     0 100% /snap/core22/2133
/dev/loop3       64M   64M     0 100% /snap/core20/2669
θ77° 2d [ubuntu@mgc-dev2-3090:~/cuong_dn] $ 
```


Dựa trên kết quả kiểm tra, tôi sẽ giải thích chi tiết về tình trạng ổ đĩa và dung lượng trên server của bạn:

## **Tổng quan hệ thống:**

### **1. Ổ đĩa chính (NVMe SSD):**
- **Đường dẫn:** `/dev/nvme0n1p2` (ổ đĩa chính)
- **Dung lượng:** 2.9TB
- **Đã sử dụng:** 2.5TB 
- **Còn trống:** 229GB
- **Tỷ lệ sử dụng:** **92%** ⚠️ **CẢNH BÁO**

### **2. Ổ đĩa phụ (SATA):**
- **Đường dẫn:** `/dev/sda1` (mount tại `/data01`)
- **Dung lượng:** 3.6TB
- **Đã sử dụng:** 3.3TB
- **Còn trống:** 161GB  
- **Tỷ lệ sử dụng:** **96%** ⚠️ **CẢNH BÁO NGHIÊM TRỌNG**

### **3. Ổ đĩa khởi động (EFI):**
- **Đường dẫn:** `/dev/nvme0n1p1`
- **Dung lượng:** 511MB
- **Đã sử dụng:** 6.1MB
- **Còn trống:** 505MB
- **Tỷ lệ sử dụng:** 2% ✅ **Tốt**

## **Phân tích và khuyến nghị:**

### **🚨 Vấn đề nghiêm trọng:**
1. **Ổ chính (/) đã sử dụng 92%** - Cần dọn dẹp ngay
2. **Ổ dữ liệu (/data01) đã sử dụng 96%** - Rất nguy hiểm

### **📋 Hành động cần thực hiện ngay:**


[3 tools called]

Tôi không thể chạy các lệnh terminal trực tiếp, nhưng dựa trên kết quả `df -h` bạn đã cung cấp, đây là phân tích chi tiết:

## **🔥 Tình trạng khẩn cấp:**

### **1. Ổ đĩa chính (/) - 92% sử dụng:**
- **Còn lại:** Chỉ 229GB trống
- **Nguy cơ:** Hệ thống có thể bị treo khi hết dung lượng

### **2. Ổ đĩa dữ liệu (/data01) - 96% sử dụng:**
- **Còn lại:** Chỉ 161GB trống  
- **Nguy cơ:** Ứng dụng có thể không thể ghi dữ liệu

## **📋 Các lệnh cần chạy để kiểm tra chi tiết:**

```bash
# Kiểm tra dung lượng thư mục hiện tại
du -sh /home/ubuntu/cuong_dn
du -sh /home/ubuntu/cuong_dn/* | sort -hr | head -5

# Tìm các file lớn nhất
find /home -type f -size +1G -exec ls -lh {} \; 2>/dev/null | head -10

# Kiểm tra các thư mục lớn nhất
du -sh /home/* | sort -hr | head -10

# Kiểm tra log files (thường chiếm nhiều dung lượng)
du -sh /var/log/*
sudo journalctl --disk-usage

# Kiểm tra cache và temp files
du -sh /tmp /var/tmp /var/cache
```

## **🛠️ Các giải pháp khuyến nghị:**

### **Ngay lập tức:**
1. **Xóa log files cũ:**
   ```bash
   sudo journalctl --vacuum-time=7d
   sudo find /var/log -name "*.log" -mtime +30 -delete
   ```

2. **Dọn dẹp package cache:**
   ```bash
   sudo apt clean
   sudo apt autoremove
   ```

3. **Xóa temporary files:**
   ```bash
   sudo rm -rf /tmp/*
   sudo rm -rf /var/tmp/*
   ```

### **Dài hạn:**
1. **Mở rộng ổ đĩa** hoặc **thêm ổ đĩa mới**
2. **Di chuyển dữ liệu** từ ổ chính sang ổ dữ liệu
3. **Thiết lập log rotation** để tự động xóa log cũ
4. **Monitor dung lượng** thường xuyên

## **⚠️ Lưu ý quan trọng:**
- **96% sử dụng** là mức rất nguy hiểm
- Cần dọn dẹp **ngay lập tức** trước khi hệ thống gặp sự cố
- Nên backup dữ liệu quan trọng trước khi thực hiện dọn dẹp

Bạn có muốn tôi hướng dẫn chi tiết cách dọn dẹp từng bước không?