
**TL;DR — Tự host DB/Storage “miễn phí” chỉ là phần nổi của tảng băng. Ngoài tiền thuê máy chủ chính, bạn cần chi thêm cho máy chủ dự phòng, sao lưu, băng thông, giám sát, bảo mật và đặc biệt là lương DevOps/SRE trực 24/7. Tổng chi phí sở hữu (TCO) thường cao hơn thuê dịch vụ managed—trừ khi đội của bạn đã có quy trình vận hành bài bản. Dưới đây là bảng bóc tách chi phí và vài gợi ý tối ưu.**

---

## 1. Chi phí hạ tầng (Infrastructure cost)

|Hạng mục|Ví dụ đơn giá|Ghi chú|
|---|---|---|
|**Máy chủ Postgres chính**|Supabase self-host “Medium” ≈ 60 USD/tháng ([Supabase self-host pricing guide — Restack](https://www.restack.io/docs/supabase-knowledge-supabase-self-host-pricing))|giá máy chủ nguyên bản, chưa HA|
|**Replica/Standby**|thêm 60 USD/tháng (tối thiểu)|yêu cầu của kiến trúc HA ([PostgreSQL: Documentation: 17: Chapter 26. High Availability, Load Balancing, and Replication](https://www.postgresql.org/docs/current/high-availability.html))|
|**Object storage cho backup**|S3 Standard ~0,023 USD/GB-tháng ([Amazon S3 Pricing - Cloud Object Storage - AWS](https://aws.amazon.com/s3/pricing/?utm_source=chatgpt.com))||
|**Dịch vụ Backup quản lý**|AWS Backup tính theo dung lượng; free tier 5 GB đầu tiên ([AWS Backup Pricing|Centralized Cloud Backup|
|**Băng thông ra (egress)**|Supabase Pro: $0,09/GB ([Pricing & Fees|Supabase]([https://supabase.com/pricing](https://supabase.com/pricing)))|
|**Chỉ số, index cho Vector DB**|chỉ số lớn → chi phí lưu trữ & compute tăng mạnh ([How to Evaluate the Cost of a Vector Database?](https://incubity.ambilio.com/how-to-evaluate-the-cost-of-a-vector-database/?utm_source=chatgpt.com))||

> **Tóm lại:** hệ thống “1 primary + 1 replica + 200 GB backup” dễ chạm mốc ~150 USD/tháng chỉ riêng cloud bill, chưa gồm log, monitor hay dự phòng đa vùng.

---

## 2. Chi phí vận hành (Operations cost)

### 2.1 Lương DevOps / SRE & on-call 24/7

- Lương SRE trung bình tại US ~140 800 USD/năm (≈ 8 900 USD/tháng) ([Site Reliability Engineer Salary in United States 2025 – Jobicy](https://jobicy.com/salaries/usa/site-reliability-engineer))
    
- Các gói “DevOps-as-a-Service” on-call 24×7 từ hãng outsourcer bắt đầu **≥ 4 000 USD/tháng** cho hạng Silver ([DevOps as a Service | DevOps engineering company DEDICATTED](https://dedicatted.com/what-we-do/devops/devops-as-a-service?utm_source=chatgpt.com))
    

> **Chi phí nhân công** thường lớn gấp nhiều lần tiền server, đặc biệt khi phải duy trì trực ca đêm, luân phiên.

### 2.2 Monitoring, logging, alerting

Các SaaS như Datadog, Grafana Cloud… thường tính **~10–30 USD/host/tháng** + phí lưu log; không kể công cấu hình và diễn giải cảnh báo.

### 2.3 Bảo mật, update & compliance

- Vá bảo mật định kỳ, khôi phục PITR, kiểm soát quyền… (theo best-practice HA của PostgreSQL) ([PostgreSQL: Documentation: 17: Chapter 26. High Availability, Load Balancing, and Replication](https://www.postgresql.org/docs/current/high-availability.html))
    
- Nếu phải tuân PCI/SOC2, chi phí audit & giấy tờ tăng đáng kể.
    

---

## 3. “Hidden cost” khi sự cố (Downtime cost)

Một nghiên cứu 2024 cho biết ngành sản xuất ô-tô thiệt hại **≈ 2,3 triệu USD mỗi giờ downtime** – tăng gấp đôi so với 2019 ([SENSEYE PREDICTIVE MAINTENANCE The True Cost of Downtime 2024 - Siemens](https://assets.new.siemens.com/siemens/assets/api/uuid%3A1b43afb5-2d07-47f7-9eb7-893fe7d0bc59/TCOD-2024_original.pdf?utm_source=chatgpt.com)). Kể cả startup nhỏ, mất dịch vụ vài giờ vào giờ cao điểm có thể gây:

- Refund, mất khách, giảm NPS
    
- Tăng thêm giờ OT cho đội DevOps
    
- Thiệt hại thương hiệu khó đo.
    

---

## 4. So sánh Self-host vs Managed

|Tiêu chí|Self-host|Managed (Supabase Cloud, RDS, Neon,…)|
|---|---|---|
|**CapEx/Opex trực tiếp**|rẻ khi load nhỏ|cao hơn (dịch vụ tính phí)|
|**Nhân công vận hành**|Phải tự lo (SRE, on-call)|Nhà cung cấp lo, đội bạn focus tính năng|
|**Khả năng mở rộng**|Phải tự scale, tuning|1-click scale up, auto-failover|
|**HA/DR**|Tự dựng replica, backup|Tích hợp sẵn multi-AZ, snapshot|
|**TCO dài hạn**|Thấp nếu đã có đội DevOps, cao nếu chưa|Dễ dự báo, ít “chi phí bất ngờ”|

Nguồn DigitalOcean & Rapydo phân tích chi phí và độ phức tạp vận hành tương ứng ([What are Managed vs Self-Managed Databases? Choosing the Right Database ...](https://www.digitalocean.com/resources/articles/managed-vs-self-managed-databases?utm_source=chatgpt.com), [AWS RDS vs. Self-Managed Databases: A Comprehensive Comparison - Rapydo](https://www.rapydo.io/blog/aws-rds-vs-self-managed-databases-a-comprehensive-comparison?utm_source=chatgpt.com)).

---

## 5. Gợi ý tối ưu cho đội nhỏ

1. **Pha trộn**: Dùng managed DB cho môi trường production, tự host bản clone để R&D, test tính năng.
    
2. **Tự động hóa**: IaC (Terraform, Ansible) + CI/CD giảm công update; chỉ phải on-call “best-effort”.
    
3. **Giảm HA mức 1**: Nếu SLA nội bộ chưa yêu cầu 99,9 %, có thể chạy 1 primary + backup snapshot (khôi phục 15–30 phút) thay vì replica realtime.
    
4. **Theo dõi TCO định kỳ**: mỗi quý rà soát bill, thời gian on-call, downtime; so sánh lại với giá managed hiện tại.
    
5. **Đầu tư kỹ năng MLOps / DevOps**: Khi khối lượng & SLA tăng, việc học bài bản (các khoá MLOps, SRE) sẽ “tiết kiệm” hơn thuê ngoài dài hạn.
    

---

### Kết luận

**“Open-source ≠ free”**. Bạn hoàn toàn có thể start với self-host Supabase, Milvus, Qdrant… nhưng nên tính đủ:

- **Server × n** (HA),
    
- **Backup & egress**,
    
- **Giám sát – bảo mật**,
    
- **Nhân công trực 24/7**,
    
- **Rủi ro downtime**.
    

Nếu đội chưa sẵn DevOps chuyên trách, lựa chọn managed dịch vụ hoặc hybrid thường rẻ và an toàn hơn cho sản phẩm giai đoạn early.