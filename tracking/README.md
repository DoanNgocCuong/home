# 🚀 Advanced Writing Tracker

**Theo dõi toàn bộ bài viết trong hệ thống với khả năng quét thư mục thực tế**

## 🎯 Tính năng chính

### 📁 **Quét thư mục thực tế**
- Quét toàn bộ thư mục `D:\vip_DOCUMENTS_OBS\home`
- Hỗ trợ tất cả định dạng: `.md`, `.txt`, `.html`, `.docx`, `.doc`, `.rtf`
- Tự động phát hiện và phân loại bài viết
- Quét cả thư mục con hoặc chỉ thư mục hiện tại

### 📊 **Dashboard nâng cao**
- **Tổng số bài viết**: Đếm tất cả file được phát hiện
- **Streak hiện tại**: Số ngày liên tiếp viết bài
- **Streak dài nhất**: Kỷ lục streak cao nhất
- **Tuần này**: Số bài viết trong tuần hiện tại
- **Thư mục đã quét**: Số thư mục chứa bài viết
- **Lần quét cuối**: Thời gian quét gần nhất

### 🔍 **Tìm kiếm và lọc**
- Tìm kiếm theo tiêu đề và đường dẫn
- Lọc theo thể loại (Kỹ thuật, Cá nhân, Kinh doanh, Giáo dục, Khác)
- Lọc theo thời gian (Hôm nay, Tuần này, Tháng này, Năm nay)
- Sắp xếp theo nhiều tiêu chí

### 📈 **Biểu đồ trực quan**
- **Line chart**: Tiến độ viết theo tháng
- **Pie chart**: Phân bố theo thể loại
- **Bar chart**: Số bài viết theo thư mục

### 📋 **Quản lý bài viết**
- Hiển thị dạng lưới hoặc danh sách
- Phân trang tự động
- Chi tiết bài viết với modal popup
- Copy đường dẫn file
- Mở file trực tiếp

### 💾 **Xuất/Nhập dữ liệu**
- Xuất ra CSV hoặc JSON
- Nhập dữ liệu từ file
- Backup và restore

## 🛠️ Cài đặt và chạy

### **Phương pháp 1: Chạy với Python Server (Khuyến nghị)**

1. **Cài đặt dependencies:**
```bash
cd "d:\vip_DOCUMENTS_OBS\home\tracking"
pip install -r requirements.txt
```

2. **Chạy server:**
```bash
python server.py
```

3. **Mở trình duyệt:**
```
http://localhost:5000
```

### **Phương pháp 2: Chạy đơn giản với batch file**

1. **Double-click file `start.bat`**
2. **Chờ server khởi động**
3. **Mở trình duyệt:** http://localhost:5000

### **Phương pháp 3: Chạy trực tiếp (Demo)**

1. Mở file `index.html` trong trình duyệt
2. Sử dụng dữ liệu mẫu để test

### **Phương pháp 4: Chạy Python script riêng**

```bash
# Scan thư mục và tạo file JSON
python scan_articles.py "D:\vip_DOCUMENTS_OBS\home"

# Hoặc chạy interactive mode
python scan_articles.py
```

## 🎮 Cách sử dụng

### **1. Quét thư mục**
1. Nhập đường dẫn thư mục (mặc định: `D:\vip_DOCUMENTS_OBS\home`)
2. Chọn có bao gồm thư mục con hay không
3. Nhấn "Quét bài viết"
4. Đợi quá trình quét hoàn thành

### **2. Theo dõi tiến độ**
- Xem thống kê tổng quan ở đầu trang
- Kiểm tra biểu đồ tiến độ
- Theo dõi streak viết bài

### **3. Tìm kiếm và lọc**
- Sử dụng thanh tìm kiếm để tìm bài viết
- Chọn bộ lọc thể loại và thời gian
- Sắp xếp theo tiêu chí mong muốn

### **4. Xem chi tiết**
- Click vào bài viết để xem thông tin chi tiết
- Copy đường dẫn hoặc mở file
- Xem thống kê từng bài viết

## 🔧 Cấu hình

### **Thay đổi đường dẫn mặc định**
Sửa trong file `server.py`:
```python
DEFAULT_SCAN_PATH = r"D:\vip_DOCUMENTS_OBS\home"  # Thay đổi đường dẫn
```

### **Thêm định dạng file mới**
Sửa trong file `server.py`:
```python
SUPPORTED_EXTENSIONS = {'.txt', '.md', '.docx', '.doc', '.html', '.rtf', '.py', '.js'}  # Thêm định dạng
```

### **Tùy chỉnh phân loại**
Sửa function `_guess_category` trong `server.py` để thêm từ khóa phân loại mới.

## 📁 Cấu trúc dự án

```
tracking/
├── index.html          # Giao diện chính
├── styles.css          # CSS styling
├── script.js           # JavaScript logic
├── server.py           # Python Flask server
├── scan_articles.py    # Python script scan độc lập
├── requirements.txt    # Python dependencies
├── start.bat          # Script khởi động dễ dàng
└── README.md          # Hướng dẫn sử dụng
```

## 🌐 API Endpoints

### **POST /api/scan**
Quét thư mục bài viết
```json
{
  "folder_path": "D:\\vip_DOCUMENTS_OBS\\home",
  "include_subfolders": true
}
```

### **GET /api/status**
Lấy trạng thái quét
```json
{
  "is_scanning": false,
  "last_scan_time": "2025-01-15T10:30:00",
  "article_count": 150
}
```

### **GET /api/articles**
Lấy danh sách bài viết
```json
{
  "success": true,
  "articles": [...],
  "count": 150,
  "last_scan": "2025-01-15T10:30:00"
}
```

### **GET /api/stats**
Lấy thống kê
```json
{
  "total_articles": 150,
  "current_streak": 7,
  "longest_streak": 30,
  "this_week": 5,
  "total_folders": 25,
  "categories": {...},
  "monthly_data": [...]
}
```

### **GET /api/export/csv**
Xuất dữ liệu ra CSV

### **GET /api/export/json**
Xuất dữ liệu ra JSON

## 🎨 Tính năng nâng cao

### **Auto-refresh**
- Tự động làm mới dữ liệu mỗi 30 giây
- Theo dõi thay đổi file trong thời gian thực

### **Responsive Design**
- Tương thích với mobile và desktop
- Giao diện thích ứng với mọi kích thước màn hình

### **Performance**
- Quét file nhanh chóng
- Lazy loading cho danh sách bài viết
- Caching dữ liệu

## 🚀 Tính năng sắp tới

- [ ] **Real-time file monitoring**: Theo dõi thay đổi file tự động
- [ ] **Advanced search**: Tìm kiếm full-text trong nội dung
- [ ] **Word count analysis**: Phân tích chi tiết số từ
- [ ] **Writing goals**: Đặt mục tiêu viết lách
- [ ] **Export to multiple formats**: PDF, Word, etc.
- [ ] **Cloud sync**: Đồng bộ dữ liệu với cloud
- [ ] **Collaboration**: Chia sẻ với team
- [ ] **Analytics**: Báo cáo chi tiết

## 🐛 Troubleshooting

### **Lỗi "Thư mục không tồn tại"**
- Kiểm tra đường dẫn thư mục
- Đảm bảo có quyền truy cập thư mục

### **Lỗi "Không thể đọc file"**
- Kiểm tra encoding của file
- Đảm bảo file không bị khóa

### **Server không chạy**
- Kiểm tra Python version (>= 3.7)
- Cài đặt lại dependencies: `pip install -r requirements.txt`

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

---

**🎉 Chúc bạn viết lách hiệu quả với Advanced Writing Tracker!**
