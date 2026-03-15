# 📊 Giải Thích Metrics trong Locust Test

## 🔢 Các Thông Số Cơ Bản

### **10 Users (10 Concurrent Users)**

**Ý nghĩa:**

- Có **10 users** đang chạy test **đồng thời** (concurrent)
- Mỗi user là một "virtual user" giả lập một người dùng thật
- Mỗi user sẽ thực thi các tasks một cách độc lập

**Ví dụ:**

```
User 1: Gửi request → Đợi 2 giây → Gửi request tiếp
User 2: Gửi request → Đợi 1.5 giây → Gửi request tiếp
User 3: Gửi request → Đợi 2.5 giây → Gửi request tiếp
...
User 10: Gửi request → Đợi 1 giây → Gửi request tiếp
```

### **RPS 5 (Requests Per Second = 5)**

**Ý nghĩa:**

- **RPS = Requests Per Second** = Số requests được gửi mỗi giây
- **RPS 5** = Trung bình **5 requests/giây** được gửi đến server

**Cách tính:**

```
RPS = Tổng số requests / Thời gian test (giây)
```

## 🔗 Mối Quan Hệ Giữa Users và RPS

### Công Thức Ước Tính:

```
RPS ≈ Số Users / Thời gian đợi trung bình (giây)
```

### Trong Code Hiện Tại:

```python
wait_time = between(1, 3)  # Đợi 1-3 giây giữa các requests
```

**Giải thích:**

- Mỗi user đợi trung bình: **(1 + 3) / 2 = 2 giây** giữa các requests
- Mỗi user gửi: **1 request / 2 giây = 0.5 requests/giây**
- Với **10 users**: **10 × 0.5 = 5 RPS** ✅

### Ví Dụ Thực Tế:

| Users | Wait Time | RPS Ước Tính | Giải Thích                    |
| ----- | --------- | --------------- | ------------------------------- |
| 10    | 1-3 giây | ~5 RPS          | 10 users × 0.5 req/s = 5 RPS   |
| 20    | 1-3 giây | ~10 RPS         | 20 users × 0.5 req/s = 10 RPS  |
| 50    | 1-3 giây | ~25 RPS         | 50 users × 0.5 req/s = 25 RPS  |
| 100   | 1-3 giây | ~50 RPS         | 100 users × 0.5 req/s = 50 RPS |

## 📈 Các Metrics Khác Trong Locust

### 1. **# reqs (Number of Requests)**

- Tổng số requests đã gửi từ đầu test
- Ví dụ: `# reqs: 150` = Đã gửi 150 requests

### 2. **# fails (Number of Failures)**

- Số requests bị lỗi
- Ví dụ: `# fails: 3` = Có 3 requests bị lỗi
- **Failure Rate** = `# fails / # reqs × 100%`

### 3. **Avg (Average Response Time)**

- Thời gian response trung bình (milliseconds)
- Ví dụ: `Avg: 250ms` = Trung bình server trả về sau 250ms

### 4. **Min / Max**

- **Min**: Thời gian response nhanh nhất
- **Max**: Thời gian response chậm nhất
- Ví dụ: `Min: 120ms, Max: 680ms`

### 5. **Median (50th Percentile)**

- 50% requests có response time ≤ giá trị này
- Ví dụ: `Median: 245ms` = 50% requests ≤ 245ms

### 6. **95%ile (95th Percentile)**

- 95% requests có response time ≤ giá trị này
- Ví dụ: `95%ile: 450ms` = 95% requests ≤ 450ms

### 7. **99%ile (99th Percentile)**

- 99% requests có response time ≤ giá trị này
- Ví dụ: `99%ile: 680ms` = 99% requests ≤ 680ms

## 🎯 Ví Dụ Kết Quả Thực Tế

```
Type     Name                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
POST     POST /v1/conversations/end      150     0(0.00%) |    250     120     680    245 |    2.50        0.00
POST     POST /v1/activities/suggest    150     0(0.00%) |    180     100     450    175 |    2.50        0.00
--------|------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                     300     0(0.00%) |    215     100     680    210 |    5.00        0.00
```

**Giải thích:**

- **# reqs: 300** = Tổng 300 requests (150 mỗi endpoint)
- **# fails: 0** = Không có lỗi nào ✅
- **Avg: 215ms** = Response time trung bình 215ms
- **req/s: 5.00** = Đang gửi 5 requests/giây
- **95%ile: ~450ms** = 95% requests ≤ 450ms

## 🔍 Phân Tích Kết Quả

### ✅ Kết Quả Tốt:

- **Failure Rate < 1%**: Hệ thống ổn định
- **Avg Response Time < 500ms**: Phản hồi nhanh
- **RPS ổn định**: Không có biến động lớn

### ⚠️ Cần Chú Ý:

- **Failure Rate 1-5%**: Có một số lỗi, cần kiểm tra
- **Avg Response Time 500-1000ms**: Hơi chậm
- **RPS giảm khi tăng users**: Có thể có bottleneck

### ❌ Vấn Đề Nghiêm Trọng:

- **Failure Rate > 5%**: Nhiều lỗi, cần dừng test
- **Avg Response Time > 1000ms**: Rất chậm
- **RPS = 0**: Server không phản hồi

## 🚀 Cách Tăng RPS

### Phương Pháp 1: Tăng Số Users

```powershell
# Từ 10 users → 20 users
locust -f locustfile.py --host=... -u 20 -r 4
# RPS sẽ tăng từ ~5 → ~10
```

### Phương Pháp 2: Giảm Wait Time

```python
# Trong locustfile.py
wait_time = between(0.5, 1.5)  # Thay vì 1-3 giây
# RPS sẽ tăng gấp đôi
```

### Phương Pháp 3: Cả Hai

```python
# Tăng users + Giảm wait time
wait_time = between(0.5, 1.5)
# Chạy với 50 users
# RPS có thể đạt 25-50
```

## 📊 Bảng So Sánh Scenarios

| Scenario | Users | Spawn Rate | Wait Time | RPS Ước Tính | Use Case             |
| -------- | ----- | ---------- | --------- | --------------- | -------------------- |
| Light    | 10    | 2          | 1-3s      | ~5              | Test cơ bản        |
| Medium   | 50    | 5          | 1-3s      | ~25             | Test thông thường |
| Heavy    | 100   | 10         | 1-3s      | ~50             | Stress test          |
| Extreme  | 200   | 20         | 0.5-1.5s  | ~100+           | Load test cực đại |

## 💡 Tips

1. **Bắt đầu nhỏ**: Test với 10 users trước, sau đó tăng dần
2. **Quan sát RPS**: Nếu RPS không tăng khi tăng users → có bottleneck
3. **Xem Response Time**: Nếu tăng đột ngột → server quá tải
4. **Monitor Failures**: Nếu failures tăng → dừng test ngay

## 🔗 Tài Liệu Tham Khảo

- [Locust Documentation](https://docs.locust.io/)
- [Understanding RPS](https://docs.locust.io/en/stable/what-is-locust.html)