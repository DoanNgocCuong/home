
>=> Bug này gặp ở cả:
+, M0, M1, M2 khi mình chạy worker nó bị vòng lặp vô hạn hỏng worker.
=> Làm mất rất nhiều thời gian vibe fix + sau phải tạm ngưng tính năng chạy ngầm vì vấn đề này để tạm test M0, M1,

### 🧾 Bug Report: Vòng lặp xử lý job mồ côi trong RabbitMQ Worker

#### 1. Mô tả sự cố

- Worker (`python -m workers.main`) chạy, kết nối RabbitMQ & Mem0 thành công.
- Khi có message trong queue `robot_ai_mem0_queue_doancuong`, log lặp liên tục:

  - `Processing extraction job: job_id=...`
  - `Error processing extraction job ...: Job not found: ...`
  - `Error updating job status to failed: Job not found: ...`
  - → Worker xử lý **cùng một job_id nhiều lần**, không bao giờ “hết việc”.

#### 2. Nguyên nhân gốc (Root Cause)

- Trong `workers/tasks/extraction_task.py`:
  - Hàm `process_extraction_job` nhận `job_id` từ message.
  - Dùng `JobService` đọc job từ DB, nhưng **không tìm thấy record** → raise `Job not found: <job_id>`.
- Trong `app/infrastructure/messaging/rabbitmq_service.py`:

```python
error_msg = str(e)
is_permanent_error = (
    "Permanent processing error" in error_msg
    or "attached to a different loop" in error_msg
)
...
if is_permanent_error:
    ch.basic_nack(..., requeue=False)
else:
    ch.basic_nack(..., requeue=True)
```

- Vì chuỗi `"Job not found"` **không match** 2 pattern trên:
  - `is_permanent_error = False`
  - `basic_nack(..., requeue=True)` → RabbitMQ **requeue message lại**.
- Kết quả:
  - Message “mồ côi” (không có job tương ứng trong DB) bị **retry vô hạn** → worker spam log, tốn tài nguyên, không bao giờ xử lý xong.

> “Job mồ côi” = message trong RabbitMQ có `job_id=...` nhưng trong DB (bảng jobs) không có record đó.

#### 3. Ảnh hưởng

- **Hiệu năng**:
  - Worker liên tục:
    - Kết nối Mem0,
    - Mở collection Milvus,
    - Chạy logic extract,
    - Rồi fail vì `Job not found`.
  - Tốn CPU, I/O (RabbitMQ, DB, Mem0/Milvus) cho những job **không bao giờ thành công được**.
- **Log**:
  - Log worker bị “ngập” bởi chuỗi lỗi lặp:
    - Khó đọc các lỗi thật sự khác.
- **Độ tin cậy**:
  - Queue có thể bị “nghẽn” bởi nhiều message lỗi kiểu này, làm chậm việc xử lý các message hợp lệ.

#### 4. Cách khắc phục đã thực hiện

**File:** `app/infrastructure/messaging/rabbitmq_service.py`

- Sửa điều kiện nhận diện **permanent error**:

```python
# Trước:
is_permanent_error = (
    "Permanent processing error" in error_msg
    or "attached to a different loop" in error_msg
)

# Sau (đã áp dụng):
is_permanent_error = (
    "Permanent processing error" in error_msg
    or "attached to a different loop" in error_msg
    or "Job not found" in error_msg
)
```

- Ý nghĩa:
  - Lỗi `"Job not found"` được coi là **lỗi vĩnh viễn (permanent)** → job này sẽ **không bao giờ thành công**, nên không có lý do để requeue.
  - Khi gặp lỗi này:
    - Worker log:
      - `Error processing extraction job ...: Job not found: ...`
      - `Permanent error detected, message will not be requeued: job_id=...`
    - Gọi:

      ```python
      ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
      ```

    - RabbitMQ **không requeue message** → message bị drop hoặc chuyển sang **dead-letter queue** (tuỳ cấu hình).

#### 5. Kết quả sau khi fix

Từ log sau fix:

- Mỗi job mồ côi:
  - Được xử lý **1 lần**:
    - `Processing extraction job: job_id=...`
    - `Error processing extraction job ...: Job not found: ...`
    - `Permanent error detected, message will not be requeued: job_id=...`
  - Không còn lặp lại vô hạn.
- Worker tiếp tục nhận message khác trong queue (nếu có), không bị “kẹt” trên 1 job forever.

#### 6. Hành động khuyến nghị tiếp theo

- **A. Dọn sạch dữ liệu xấu (nếu cần)**  
  - Các message mồ côi cũ:
    - Sau fix, khi worker xử lý lại từng cái, chúng sẽ **tự biến mất khỏi queue** (do `requeue=False`).
  - Nếu muốn sạch ngay lập tức:
    - Vào RabbitMQ Management UI → **Purge queue** `robot_ai_mem0_queue_doancuong`.

- **B. Ngăn sinh job mồ côi trong tương lai**

  Review luồng tạo job (ở API add/extract facts):

  1. Tạo record job trong DB (insert + commit).
  2. Chỉ khi DB commit OK mới `publish` message vào RabbitMQ.

  Cần đảm bảo:
  - Không `publish` trước khi commit DB.
  - Nếu insert job fail, **không publish**.

- **C. Cải thiện log & giám sát**

  - Thêm metric/alert:
    - Số lượng `"Job not found"` theo thời gian.
    - Nếu tăng đột biến → có thể đang có bug ở luồng tạo job.

---

Nếu bạn muốn, tôi có thể viết thêm một đoạn **section “Known Issue”** để đưa vào `IMPLEMENTATION_SUMMARY.md` hoặc docs nội bộ, mô tả ngắn gọn bug này để team dev/ops nắm và tránh tái diễn.