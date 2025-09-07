# 🚀 Domain Progress Tracker Backend - FastAPI

**Backend API để scan và tính toán XP/Level cho các domain học tập**

## ⚡ **FastAPI Features:**
- **Auto-generated API docs** tại `/docs`
- **Type validation** với Pydantic models
- **Async support** cho performance tốt hơn
- **Modern Python** với type hints

## 🎯 Tính năng chính

### 📊 **Domain Analysis:**
- **Scan** tất cả domain folders trong `DATA SCIENCE AND AI/`
- **Tính XP** dựa trên số bài viết và số từ
- **Tính Level** theo hệ thống XP như Tag system
- **Tính Streak** dựa trên ngày viết bài

### 🎨 **Domain Colors:**
- **Domain 1**: Indigo - Mathematical Foundation
- **Domain 2**: Emerald - Programming & Software Engineering  
- **Domain 3**: Amber - Machine Learning Fundamentals
- **Domain 4**: Pink - Deep Learning & Neural Networks
- **Domain 5**: Blue - Data Engineering & Processing
- **Domain 6**: Violet - Production Systems & MLOps
- **Domain 7**: Red - Cloud & Infrastructure
- **Domain 8**: Teal - Advanced AI Applications

## 🛠️ Cài đặt và chạy

### **Phương pháp 1: Chạy với batch file (Khuyến nghị)**
```bash
# Double-click file start.bat
# Hoặc chạy trong Command Prompt:
cd "d:\vip_DOCUMENTS_OBS\home\backend"
.\start.bat
```

### **Phương pháp 2: Chạy thủ công**
```bash
cd "d:\vip_DOCUMENTS_OBS\home\backend"
pip install -r requirements.txt
python main.py
```

### **Phương pháp 3: Test API**
```bash
# Chạy server trước, sau đó:
python test_api.py
```

### **Phương pháp 4: Truy cập API Documentation**
```bash
# Sau khi chạy server, truy cập:
# http://localhost:8000/docs
```

## 🌐 API Endpoints

### **GET /api/domains**
Lấy danh sách tất cả domains với XP/Level
```json
{
  "success": true,
  "domains": {
    "Domain 1: Mathematical Foundation": {
      "xp": 2500,
      "level": 3,
      "color": "#4F46E5",
      "taskCount": 24,
      "streakDays": 15,
      "lastTaskDate": "2025-01-15T10:30:00"
    }
  },
  "count": 8,
  "last_scan": "2025-01-15T10:30:00"
}
```

### **POST /api/domains/refresh**
Refresh domain data (scan lại)
```json
{
  "success": true,
  "message": "Domains refreshed successfully",
  "domains": {...},
  "count": 8,
  "last_scan": "2025-01-15T10:30:00"
}
```

### **GET /api/domains/stats**
Lấy thống kê tổng quan
```json
{
  "success": true,
  "stats": {
    "total_domains": 8,
    "total_articles": 150,
    "total_xp": 25000,
    "total_levels": 45,
    "average_level": 5.6,
    "highest_level_domain": ["Domain 3", {"level": 8}],
    "most_articles_domain": ["Domain 2", {"taskCount": 35}]
  },
  "last_scan": "2025-01-15T10:30:00"
}
```

## 🧮 Công thức tính toán

### **XP Calculation:**
```
Base XP = Số bài viết × 100
Word Bonus = Tổng số từ ÷ 10
Total XP = Base XP + Word Bonus
```

### **Level Calculation:**
```
Level 0: 0-999 XP
Level 1: 1000-2499 XP  
Level 2: 2500-4749 XP
Level 3: 4750-8499 XP
...
Required XP for next level = 1000 × (1.5 ^ level)
```

### **Streak Calculation:**
- Đếm số ngày liên tiếp có bài viết
- Dựa trên ngày tạo file gần nhất

## 📁 Cấu trúc dự án

```
backend/
├── main.py           # Flask server chính
├── requirements.txt  # Python dependencies
├── start.bat        # Script khởi động
├── test_api.py      # Test script
└── README.md        # Hướng dẫn
```

## 🔧 Cấu hình

### **Thay đổi đường dẫn scan:**
Sửa trong file `main.py`:
```python
DATA_SCIENCE_PATH = r"D:\vip_DOCUMENTS_OBS\home\DATA SCIENCE AND AI"
```

### **Thay đổi công thức XP:**
Sửa function `calculate_xp_from_articles()` trong `main.py`

### **Thêm domain colors:**
Sửa dictionary `DOMAIN_COLORS` trong `main.py`

## 🎮 Cách sử dụng với Frontend

1. **Chạy backend server:**
   ```bash
   python main.py
   ```

2. **Frontend sẽ call API:**
   ```javascript
   // Fetch domains data
   const response = await fetch('http://localhost:8000/api/domains');
   const data = await response.json();
   
   // Map domains to tags format
   const tags = {};
   Object.entries(data.domains).forEach(([name, domain]) => {
     tags[name] = {
       xp: domain.xp,
       level: domain.level,
       color: domain.color,
       taskCount: domain.taskCount,
       streakDays: domain.streakDays,
       lastTaskDate: domain.lastTaskDate
     };
   });
   ```

3. **Hiển thị trong TagLevels component:**
   - Domains sẽ hiển thị như các tag bình thường
   - Có level, XP, progress bar
   - Có màu sắc riêng cho từng domain

## 🐛 Troubleshooting

### **Lỗi "Thư mục không tồn tại"**
- Kiểm tra đường dẫn `DATA_SCIENCE_PATH`
- Đảm bảo có quyền truy cập thư mục

### **Server không chạy**
- Kiểm tra Python version (>= 3.7)
- Cài đặt dependencies: `pip install -r requirements.txt`
- Kiểm tra port 8000 có bị chiếm không

### **API không trả về data**
- Kiểm tra đường dẫn scan
- Đảm bảo có file .md, .txt trong domain folders
- Xem log trong console

## 📄 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

---

**🎉 Backend sẵn sàng để tích hợp với Frontend!**
