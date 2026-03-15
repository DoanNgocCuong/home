# 📊 Báo Cáo Kết Quả Stress Test - Context Handling Robot API

**Ngày test:** 2025-12-02
**Test Tool:** Locust 2.42.6
**Target Server:** http://103.253.20.30:30020

---

## 🎯 Tổng Quan Test

### Test Configuration

- **Số Users:** 10 concurrent users
- **Spawn Rate:** 2 users/second
- **Duration:** 60 giây
- **Wait Time:** 1-3 giây giữa các requests

### API Endpoints Tested

1. **POST /v1/conversations/end** - Kết thúc conversation
2. **POST /v1/activities/suggest** - Gợi ý activities cho user

---

## 📈 Kết Quả Test

### Screenshot 1: Statistics Overview

![Test Results Overview](image/result/1764646884789.png)

### Screenshot 2: Detailed Metrics

![Detailed Metrics](image/result/1764646907322.png)



![1764649092830](image/result/1764649092830.png)![1764649092830](image/result/1764649092830.png)

---

## 📊 Phân Tích Chi Tiết

### 1. Performance Metrics

#### **POST /v1/conversations/end**

- **Total Requests:** [Số requests từ screenshot]
- **Failures:** [Số failures từ screenshot]
- **Failure Rate:** [Tỷ lệ %]
- **Average Response Time:** [ms]
- **Min Response Time:** [ms]
- **Max Response Time:** [ms]
- **Median (50th percentile):** [ms]
- **95th percentile:** [ms]
- **99th percentile:** [ms]
- **Requests per Second (RPS):** [req/s]

#### **POST /v1/activities/suggest**

- **Total Requests:** [Số requests từ screenshot]
- **Failures:** [Số failures từ screenshot]
- **Failure Rate:** [Tỷ lệ %]
- **Average Response Time:** [ms]
- **Min Response Time:** [ms]
- **Max Response Time:** [ms]
- **Median (50th percentile):** [ms]
- **95th percentile:** [ms]
- **99th percentile:** [ms]
- **Requests per Second (RPS):** [req/s]

#### **Aggregated (Tổng Hợp)**

- **Total Requests:** [Tổng số requests]
- **Total Failures:** [Tổng số failures]
- **Overall Failure Rate:** [Tỷ lệ %]
- **Average Response Time:** [ms]
- **Total RPS:** [req/s]

---

## ✅ Đánh Giá Kết Quả

### Performance Assessment

#### Response Time Analysis

- ✅ **Excellent** (< 200ms): [Số lượng requests]
- ✅ **Good** (200-500ms): [Số lượng requests]
- ⚠️ **Acceptable** (500-1000ms): [Số lượng requests]
- ❌ **Poor** (> 1000ms): [Số lượng requests]

#### Failure Analysis

- **Total Failures:** [Số lượng]
- **Failure Rate:** [%]
- **Main Failure Reasons:**
  - [Lý do 1 nếu có]
  - [Lý do 2 nếu có]

#### Throughput Analysis

- **Peak RPS:** [req/s]
- **Average RPS:** [req/s]
- **RPS Stability:** [Ổn định / Biến động]

---

## 🎯 Kết Luận

### ✅ Điểm Mạnh

1. [Điểm mạnh 1 - VD: Response time tốt, không có failures]
2. [Điểm mạnh 2 - VD: RPS ổn định]
3. [Điểm mạnh 3 - VD: Server xử lý tốt với 10 concurrent users]

### ⚠️ Điểm Cần Cải Thiện

1. [Điểm cần cải thiện 1 - VD: Response time ở 95th percentile hơi cao]
2. [Điểm cần cải thiện 2 - VD: Có một số failures cần kiểm tra]
3. [Điểm cần cải thiện 3 - VD: RPS có thể tăng thêm]

### 📋 Khuyến Nghị

1. **Ngắn hạn:**

   - [Khuyến nghị 1 - VD: Kiểm tra và fix các failures]
   - [Khuyến nghị 2 - VD: Tối ưu response time cho endpoint chậm]
2. **Dài hạn:**

   - [Khuyến nghị 1 - VD: Scale up server nếu cần xử lý nhiều users hơn]
   - [Khuyến nghị 2 - VD: Implement caching để giảm response time]

---

## 📊 So Sánh với Baseline

| Metric                | Baseline | Current Test | Status     |
| --------------------- | -------- | ------------ | ---------- |
| Average Response Time | [ms]     | [ms]         | ✅/⚠️/❌ |
| 95th Percentile       | [ms]     | [ms]         | ✅/⚠️/❌ |
| Failure Rate          | [%]      | [%]          | ✅/⚠️/❌ |
| RPS                   | [req/s]  | [req/s]      | ✅/⚠️/❌ |

---

## 🔍 Chi Tiết Kỹ Thuật

### Test Environment

- **Locust Version:** 2.42.6
- **Python Version:** [Version]
- **OS:** Windows
- **Network:** [Network details nếu có]

### Test Data

- **Conversation Logs:** Generated dynamically với 3-10 turns
- **User IDs:** Generated randomly với prefix "user_"
- **Bot Configuration:**
  - Bot ID: `talk_movie_preference`
  - Bot Type: `dd`

### Status Codes Accepted

- ✅ **200 OK** - Success
- ✅ **201 Created** - Success
- ✅ **202 Accepted** - Success (Async processing)

---

## 📝 Notes

- [Ghi chú 1 - VD: Test được chạy trong giờ cao điểm]
- [Ghi chú 2 - VD: Server có một số maintenance trong quá trình test]
- [Ghi chú 3 - VD: Cần test lại với số users cao hơn]

---

## 📎 Attachments

- Screenshot 1: Statistics Overview
- Screenshot 2: Detailed Metrics
- [CSV export nếu có]
- [HTML report nếu có]

---

**Report Generated:** [Ngày giờ]
**Tested By:** [Tên người test]
**Reviewed By:** [Tên người review]