Trong quá trình mình đi làm, có 1 dự án làm mình hết sức ấn tượng vì output, outcome của nó đã tạo ra. 

+, Ban đầu công ty cần phần đó, mình trong vòng 1 đêm tạo ra demo luôn và nó khá ấn tượng (cụ thể là phần memory)
+, Về sau phần này được đưa cho 1 anh A 2k để host OSS về nhưng bị vấn đề là cứ chạy được 1 tí là CPU cao vút. 
Sau đó anh ấy bận nên nghỉ và chuyển giao lại dự án cho tụi mình, mình cũng bận các dự án khác + team chưa ưu tiên phần này nên mình ko động. 

Về sau khi team Product cần tính năng này, sếp mìh đã nhờ 1 anh B - Senior 98 để host nó trên Platform. 
Với giá mìh ko nhớ rõ, hình như là free 3 tháng đầu, còn vè sau 500$ 1 tháng (đó là theo trí nhớ của mìh)

| Gói        | Giá / tháng | tối đa         | calls / tháng   | Một số quyền lợi chính                                                |
| ---------- | ----------- | -------------- | --------------- | --------------------------------------------------------------------- |
| Hobby      | Free        | 10.000 dữ liệu | 1.000 calls     | Unlimited end users, community support.                               |
| Starter    | 19 USD      | 50.000 dữ liệu | 5.000 calls     | Unlimited end users, community support.                               |
| Pro        | 249 USD     | Unlimited      | 50.000 calls    | Graph memory, advanced analytics, multi-project, private Slack.mem0+2 |
| Enterprise | Custom      | Unlimited      | Unlimited calls | On‑prem, SSO, audit logs, SLA, custom integrations.                   |

Sau đó mình xin được nhận phần này để xử lý bài OSS (với sự support của 1 anh DevOps để giúp mình dựng lên 1 bản original OSS như ngày xưa anh A đã dựng) 

+, Khi lần đầu test response time nó là 1s cho API search_facts, bước đầu đơn giản nhất là đổi embedding models và bỏ những phần thừa thì response time về 200ms. 

---
Khi đem đi test tải, vấn đề lộ rõ lại lỗi ngày xưa, đó là cứ được 10 CCU là nghẻo, CPU lúc không chạy đã chiếm tới 70%, còn lúc chạy thì CPU lên tới 223% (chi tiết mn có thể xem ở bảng bên dưới). 

Các bước quan trọng mình đã làm lúc đó 

1. Viết 1 file để check tài nguyên tiêu tốn real time 
2. Check bug 

### Chi tiết về các tài nguyên mình check real-time ở bên dưới

```
📊 Real-time stats for project containers (Ctrl+C to stop):

NAME                CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
X-server         2.35%     245.3MiB / 2GiB       11.98%    1.2MB / 890kB
milvus-standalone   5.12%     1.02GiB / 4GiB        25.50%    45.3MB / 12.1MB
milvus-etcd         0.15%     45.2MiB / 512MiB      8.83%     2.1MB / 1.8MB
milvus-minio        0.08%     85.6MiB / 1GiB        8.36%     12.5MB / 30.2MB
infinity-proxy      1.45%     320.1MiB / 2GiB       15.63%    890kB / 1.5MB
attu                0.02%     32.4MiB / 512MiB      6.33%     120kB / 45kB
```

Sau đó mình phát hiện 

## 🎯 Tổng Quan Evolution

| Version                    | Mô Tả                    | Max CCU | RPS    | P99 Latency | CPU mem0-server  | Status              |
| -------------------------- | -------------------------- | ------- | ------ | ----------- | ---------------- | ------------------- |
| **CKP2 (Ban đầu)** | Initial setup              | ~10     | ~6     | N/A         | 223% (treo)      | 🔴 Unstable         |
| **CKP3.3.1**         | Sau fix telemetry          | 30+     | ~20-21 | N/A         | 118%             | 🟡 Stable           |
| **CKP3.3.2**         | Telemetry complete disable | 100     | 35     | 2000ms      | 110%             | 🟡 Stable           |
| **CKP3.4**           | 2 workers + batch-size 256 | 100     | 42.5   | 700ms       | 158% (2 workers) | 🟢 Optimized        |
| **CKP3.5 (Final)**   | Batch-size 128 optimized   | 100     | ~42.5  | 700ms       | 78.6% (1 worker) | 🟢 Production Ready |
