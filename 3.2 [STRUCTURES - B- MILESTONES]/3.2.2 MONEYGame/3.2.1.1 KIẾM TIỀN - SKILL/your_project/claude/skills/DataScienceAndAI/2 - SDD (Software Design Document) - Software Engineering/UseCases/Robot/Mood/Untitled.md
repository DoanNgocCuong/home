### **Bản Mô Tả Chi Tiết Bài Toán & Phân Tích Giải Pháp Tối Ưu Hóa Hiệu Năng LLM**

**Mục tiêu:** Đạt độ trễ phản hồi **P99 $\le$ 50ms** cho tác vụ phân loại nhị phân (celebrate) và đa nhãn (emotion) trong hệ thống tương tác robot Pika.

#### **1. Bối cảnh Bài toán (Context)**

Chúng tôi phát triển robot tương tác Pika. Sau khi LLM chính tạo ra câu trả lời bằng văn bản, một hệ thống phụ (side-car) phải nhanh chóng gán hai tag:

1. **`emotion_name`**: Tag cảm xúc (ví dụ: `happy`, `curious`, `proud`) để điều khiển biểu cảm và servo của robot.
2. **`celebrate`**: Tag nhị phân (`yes`/`no`) chỉ được gán `yes` khi Pika xác nhận trẻ trả lời **đúng** một câu hỏi kiến thức khách quan.

**Ràng buộc Cốt lõi:** Toàn bộ quá trình phân loại phải hoàn thành trong **dưới 50ms** để đảm bảo hành động của robot đồng bộ với lời nói.

#### **2. Kiến trúc Hiện tại (Side-car Architecture)**

- **Luồng:** `LLM Chính (Pika) sinh Text` $\rightarrow$ `LLM Phụ (Tagger) phân tích Text` $\rightarrow$ `Robot Hành động`.
- **Input cho Tagger:** `pika_response` và `user_last_message` (ngữ cảnh).

#### **3. Dữ liệu Thực nghiệm & Phân tích Điểm nghẽn**

Chúng tôi đã thử nghiệm self-host các mô hình ngôn ngữ nhỏ (SLM) trên phần cứng NVIDIA RTX 3090 với framework vLLM.

|Mô hình|Phần cứng|Framework|Median Latency (ms)|P99 Latency (ms)|Kết luận|
|---|---|---|---|---|---|
|Qwen-0.6B|RTX 3090|vLLM|$\approx$ 75ms|$\approx$ 430ms|**Thất bại:** Median $\le$ 50ms không đạt. P99 không ổn định dưới tải.|
|SmolLM-135M|RTX 3090|vLLM|$\approx$ 170ms|N/A|**Thất bại:** Overhead của Python/vLLM quá lớn so với kích thước mô hình.|
|Groq (Llama-3-8B)|LPU|Groq API|$\approx$ 60-80ms|$\approx$ 100ms|**Tốt nhất hiện tại:** Ổn định, nhưng chưa đạt mục tiêu < 50ms.|

**Điểm nghẽn Cốt lõi:**

- **Median Latency:** Bị giới hạn bởi **Python Overhead** và **tốc độ suy luận thuần túy** của mô hình chưa được biên dịch.
- **Tail Latency (P99):** Bị giới hạn bởi **Context Switching** và **Quản lý Bộ nhớ** trên GPU consumer (RTX 3090) khi chạy dưới tải.

#### **4. Các Giải pháp Đã Thử và Đã Tối ưu**

|Giải pháp|Kết quả|Lý do Tối ưu|
|---|---|---|
|**Tách API**|Tách thành 2 API (`Emotion` và `Celebrate`) và gọi song song.|Giảm thời gian chờ đợi tổng thể xuống $\max(T_{emotion}, T_{celebrate})$.|
|**Tối ưu Prompt**|Viết prompt ngắn gọn, yêu cầu JSON, sử dụng Groq.|Giảm token đầu vào, tăng tốc độ xử lý, đạt $\approx$ 60ms.|
|**Self-host SLM**|Thử nghiệm Qwen-0.6B, SmolLM-135M.|**Thất bại:** Không đạt SLA P99 do overhead và thiếu ổn định.|

#### **5. Các Giải pháp Chưa Thử nghiệm (Đề xuất Tư vấn)**

Chúng tôi đang tìm kiếm xác nhận và kinh nghiệm thực tế về các giải pháp sau, được phân loại theo mức độ đột phá:

|Nhóm Giải pháp|Phương án|Mục tiêu|Cần Tư vấn|
|---|---|---|---|
|**Tối ưu Hóa Cấp độ Kernel**|**TensorRT-LLM (Biên dịch Mô hình)**|Đạt P99 $\le$ 50ms.|Kinh nghiệm thực tế về việc biên dịch Phi-3-mini/Llama-3-8B bằng TensorRT-LLM. Tỷ lệ tăng tốc thực tế so với vLLM.|
|**Kiến trúc Đột phá**|**Kiến trúc Tiền Quyết định (Pre-determination)**|Loại bỏ hoàn toàn độ trễ của luồng phụ.|Kinh nghiệm triển khai mô hình phân loại ý định (intent classifier) cực nhanh (sub-5ms) để _chỉ đạo_ LLM chính.|
|**Mô hình Chuyên biệt**|**Fine-tune SLM + Biên dịch**|Đạt độ chính xác cao nhất với tốc độ tối đa.|Kinh nghiệm fine-tuning Llama-3-8B/Phi-3-mini cho tác vụ phân loại nhị phân/đa nhãn. Tác động của fine-tuning lên tốc độ suy luận.|
|**Phần cứng Chuyên dụng**|**NVIDIA L4/A10G**|Cải thiện P99 và xử lý đồng thời.|So sánh hiệu năng P99 thực tế của L4 so với RTX 3090 cho tác vụ suy luận LLM dưới tải.|

**Câu hỏi Trọng tâm:**

1. Với dữ liệu P99 $\approx$ 430ms trên RTX 3090, liệu việc chuyển sang **TensorRT-LLM trên L4** có đủ để đảm bảo P99 $\le$ 50ms không, hay chúng tôi buộc phải sử dụng **Groq LPU**?
2. Giải pháp **Kiến trúc Tiền Quyết định** (phân loại ý định trước khi Pika sinh text) có phải là con đường kiến trúc tối ưu nhất về lâu dài cho các ứng dụng thời gian thực không?

**Tác giả:** Manus AI (Đại diện Kỹ sư AI) **Ngày:** 08/12/2025