# Locust - STRESS TEST TOOL for Beginner [Lần đầu xài Locust Tool mình đã phải mất đến 5h ngồi đọc và set up. Sau khoảng 2 tháng không động đến lại quên và nay khi mò đến, mình đã viết lại report này]   - Có AI xịn trong tay, nhưng phải mất 5h mình mới gõ được đúng câu Prompt LONG MẠCH để con Claude nó hướng dẫn mình cách đọc UI :3

# # 📊 Hướng Dẫn Xem Báo Cáo Locust - Từng Bước Chi Tiết

## 🚀 BƯỚC 1: Chạy Test

### 1.1 Mở Terminal và chạy lệnh:

```bash  
locust -f simple_test.py --host http://103.253.20.30:30004  
```

### 1.2 Bạn sẽ thấy thông báo:

```  
[2025-09-01 14:30:15,123] INFO/locust.main: Starting web interface at http://127.0.0.1:8089 (accepting connections from all network interfaces)  
[2025-09-01 14:30:15,124] INFO/locust.main: Starting Locust 2.x.x  
```

## 🌐 BƯỚC 2: Mở Giao Diện Web

### 2.1 Mở trình duyệt và vào: `http://localhost:8089`

### 2.2 Bạn sẽ thấy màn hình khởi tạo:

```  
┌─────────────────────────────────────┐  
│           Start new load test        │  
├─────────────────────────────────────┤  
│ Number of users: [    10    ]      │  
│ Spawn rate:      [     2    ]      │  
│ Host:           http://103.253.20... │  
│                                     │  
│          [Start swarming]           │  
└─────────────────────────────────────┘  
```

### 2.3 Cấu hình đề xuất cho lần đầu:

* **Number of users** : `10` (10 user ảo)  
* **Spawn rate** : `2` (tăng 2 user mỗi giây)  
* Nhấn **"Start swarming"**

## 📈 BƯỚC 3: Theo Dõi Test Real-time

### 3.1 Sau khi nhấn "Start swarming", bạn sẽ thấy giao diện chính với 5 tabs:

```  
┌─Statistics─┬─Charts─┬─Failures─┬─Exceptions─┬─Download Data─┐  
│     ✓      │        │          │            │               │  
└────────────┴────────┴──────────┴────────────┴───────────────┘  
```

## 📊 TAB 1: STATISTICS (Quan trọng nhất!)

### 3.2 Trong tab Statistics, bạn sẽ thấy bảng như này:

```  
┌──────────┬────────────────────────┬──────────┬──────────┬────────┬────────┬────────┬─────────┬─────────┬─────┬─────┬──────────┬─────────────┐  
│   Type   │          Name          │ # Requests│ # Fails │ Median │ 90%ile │ 95%ile │  99%ile │ Average │ Min │ Max │Avg Size  │Current RPS  │  
├──────────┼────────────────────────┼──────────┼──────────┼────────┼────────┼────────┼─────────┼─────────┼─────┼─────┼──────────┼─────────────┤  
│   POST   │Simple Search - lãnh đạo│   247    │  1 (0%)  │  340   │  620   │  780   │  1200   │   380   │ 180 │1450 │  2.1 kB  │    8.5      │  
├──────────┼────────────────────────┼──────────┼──────────┼────────┼────────┼────────┼─────────┼─────────┼─────┼─────┼──────────┼─────────────┤  
│Aggregated│                        │   247    │  1 (0%)  │  340   │  620   │  780   │  1200   │   380   │ 180 │1450 │  2.1 kB  │    8.5      │  
└──────────┴────────────────────────┴──────────┴──────────┴────────┴────────┴────────┴─────────┴─────────┴─────┴─────┴──────────┴─────────────┘  
```

### 3.3 Cách đọc bảng này:

#### ✅ **KẾT QUẢ TỐT (Ví dụ trên):**

* **# Requests: 247** → Đã gửi 247 requests  
* **# Fails: 1 (0%)** → Chỉ 1 lỗi = 0.4% lỗi (RẤT TỐT!)  
* **Median: 340ms** → 50% requests dưới 340ms (NHANH!)  
* **95%ile: 780ms** → 95% requests dưới 780ms (CHẤP NHẬN ĐƯỢC!)  
* **99%ile: 1200ms** → 99% requests dưới 1.2 giây (OK!)  
* **Current RPS: 8.5** → Đang xử lý 8.5 requests/giây

#### ⚠️ **KẾT QUẢ CẦN CHÚ Ý:**

```  
│   POST   │Simple Search - lãnh đạo│   150    │ 8 (5%)   │  850   │ 1500   │ 2200   │  4500   │  1100   │ 200 │5200 │  2.1 kB  │    4.2      │  
```

* **# Fails: 8 (5%)** → 5% lỗi (HỚI CAO!)  
* **95%ile: 2200ms** → 95% requests dưới 2.2 giây (HỚI CHẬM!)

#### ❌ **KẾT QUẢ XẤU:**

```  
│   POST   │Simple Search - lãnh đạo│    80    │ 15 (19%) │ 1200   │ 3000   │ 4500   │  8000   │  1800   │ 300 │9500 │  2.1 kB  │    1.8      │  
```

* **# Fails: 15 (19%)** → 19% lỗi (NGUY HIỂM!)  
* **95%ile: 4500ms** → 4.5 giây (QUÁ CHẬM!)

## 📈 TAB 2: CHARTS (Biểu đồ thời gian thực)

### 3.4 Trong tab Charts, bạn sẽ thấy 3 biểu đồ:

#### **Biểu đồ 1: Response Times**

```  
Response Time (ms)  
        ↑  
   1500 |  
   1000 |     ╭─╮  
    500 |╭─╮ ╱   ╲ ╭─╮  
      0 |───╲─────╲╱───╲─── → Time  
```

* **Đường xanh lá (Median)** : Thời gian phản hồi trung bình  
* **Đường cam (95th percentile)** : 95% requests dưới đường này

#### **Biểu đồ 2: Requests per Second**

```  
RPS     ↑  
     15 |████████████████   
     10 |████████████████  
      5 |████████████████  
      0 |──────────────── → Time  
```

* **Càng thẳng càng tốt** = API ổn định  
* **Nếu giảm dần** = API không chịu nổi tải

#### **Biểu đồ 3: Number of Users**

```  
Users   ↑  
     10 |        ████████  
      5 |    ╱██████████  
      0 |───╱──────────── → Time  
```

* Hiển thị số user tăng dần theo spawn rate

## ❌ TAB 3: FAILURES (Nếu có lỗi)

### 3.5 Nếu có lỗi, bạn sẽ thấy:

```  
┌─────────┬────────────────────────┬───────────────────────────┬──────────────┐  
│  Method │          URL           │        Error Message       │ Occurrences  │  
├─────────┼────────────────────────┼───────────────────────────┼──────────────┤  
│  POST   │/search_jobs_and_gene...│ ConnectionError: HTTPSCon..│      3       │  
│  POST   │/search_jobs_and_gene...│ HTTP 500: Internal Server..│      2       │  
└─────────┴────────────────────────┴───────────────────────────┴──────────────┘  
```

**Các lỗi thường gặp:**

* **ConnectionError** : Mất kết nối mạng  
* **HTTP 500** : Lỗi server internal  
* **HTTP 404** : API endpoint không tồn tại  
* **TimeoutError** : API phản hồi quá chậm

## 🎯 BƯỚC 4: Đánh Giá Kết Quả

### 4.1 **Tiêu chí đánh giá cho API của bạn:**

#### ✅ **API HOẠT ĐỘNG TỐT:**

```  
✓ Error Rate: 0-1%  
✓ Median: < 500ms    
✓ 95%ile: < 1000ms  
✓ RPS: Ổn định, không giảm  
✓ Biểu đồ không có gai nhọn  
```

#### ⚠️ **API CHẤP NHẬN ĐƯỢC:**

```  
⚠ Error Rate: 1-3%  
⚠ Median: 500-800ms  
⚠ 95%ile: 1000-2000ms    
⚠ RPS: Dao động nhẹ  
```

#### ❌ **API CÓ VẤN ĐỀ:**

```  
✗ Error Rate: > 5%  
✗ Median: > 1000ms  
✗ 95%ile: > 3000ms  
✗ RPS: Giảm mạnh hoặc dừng  
```

## 💾 BƯỚC 5: Lưu Báo Cáo

### 5.1 Vào tab  **"Download Data"** :

* **Download request statistics CSV** : Số liệu chi tiết  
* **Download response times distribution CSV** : Phân bố thời gian  
* **Download exceptions CSV** : Chi tiết lỗi (nếu có)

### 5.2 File CSV sẽ chứa data để phân tích sau:

```csv  
Type,Name,Request Count,Failure Count,Median Response Time,Average Response Time,Min Response Time,Max Response Time,Average Content Size,Requests/s,Failures/s,50%,66%,75%,80%,90%,95%,98%,99%,99.9%,99.99%,100%  
POST,Simple Search - lãnh đạo,247,1,340,380,180,1450,2048,8.5,0.03,340,420,520,580,650,780,950,1200,1450,1450,1450  
```

## 🎯 BƯỚC 6: Quyết Định Tiếp Theo

### 6.1 **Nếu kết quả TỐT:**

* Tăng số user lên 20-30  
* Test lâu hơn (10-15 phút)  
* Thử với tải cao hơn

### 6.2 **Nếu có VẤN ĐỀ:**

* Giảm số user xuống 5  
* Kiểm tra server resources  
* Liên hệ team backend

## 📝 BƯỚC 7: Viết Báo Cáo Đơn Giản

### 7.1 **Template nhanh:**

```  
🎯 LOAD TEST REPORT - [Ngày test]

📊 CẤU HÌNH TEST:  
- API: search_jobs_and_generation_sendBE    
- Users: 10 concurrent  
- Duration: 5 minutes  
- Input: "lãnh đạo"

📈 KẾT QUẢ:  
- Total Requests: 247  
- Error Rate: 0.4% (✅ Tốt)  
- Response Times:  
  * Median: 340ms (✅ Nhanh)  
  * 95%ile: 780ms (✅ Chấp nhận được)    
  * 99%ile: 1200ms (✅ OK)  
- Throughput: 8.5 RPS

🎯 KẾT LUẬN:  
API hoạt động tốt với 10 users đồng thời.  
Có thể test với tải cao hơn.  
```

## 🔄 VÍ DỤ COMPLETE WORKFLOW

### Từ lúc chạy đến khi có báo cáo (5 phút):

1. **00:00** - Chạy `locust -f simple_test.py --host http://103.253.20.30:30004`  
2. **00:15** - Mở http://localhost:8089, set 10 users, spawn rate 2  
3. **00:30** - Nhấn "Start swarming", bắt đầu theo dõi  
4. **01:00** - Xem tab Statistics: 0% error, median 340ms → Tốt!  
5. **02:00** - Xem tab Charts: RPS ổn định, response time không gai → OK!  
6. **03:00** - Tiếp tục theo dõi, metrics vẫn stable  
7. **04:00** - Nhấn "Stop" để dừng test  
8. **04:30** - Vào "Download Data" tải CSV về  
9. **05:00** - Viết báo cáo: "API hoạt động tốt với 10 users"

**Vậy là xong! Bạn đã có báo cáo performance đầu tiên rồi!** 🎉

## 💡 LÚU Ý QUAN TRỌNG

* **Lần đầu test** : Chỉ 5-10 users, 2-3 phút là đủ  
* **Focus vào Error Rate** : Phải < 1%  
* **Focus vào 95%ile** : Phải < 1-2 giây  
* **Nếu OK** : Tăng dần users để tìm giới hạn  
* **Screenshot** : Chụp màn hình Statistics để lưu proof

![](https://fsds-content.s3.ap-southeast-1.amazonaws.com/uploads/366761efca158e85de4650a37ef5d75d3ff2c126d0acd27836482fff4ef55b0c.png)

![](https://fsds-content.s3.ap-southeast-1.amazonaws.com/uploads/f888e14c080fecf7a7ec016101ff8725c22c2bb153ad028eb79293b5657315d9.png)