# Chất lượng Production cho Vận hành LLM dựa trên vLLM: Hướng dẫn Đẳng cấp Thế giới

**Tác giả:** Manus AI
**Ngày:** 15 tháng 12 năm 2025
**Đối tượng:** Thực tập sinh AI khao khát trở thành Kỹ sư MLOps Đẳng cấp Thế giới

---

## Giới thiệu

### Tư duy Đẳng cấp Thế giới

Việc chuyển đổi từ bằng chứng khái niệm (PoC) sang hệ thống Mô hình Ngôn ngữ Lớn (LLM) cấp production (vận hành thực tế) là một sự thay đổi cơ bản trong triết lý kỹ thuật. Một kỹ sư MLOps đẳng cấp thế giới hiểu rằng độ chính xác của mô hình chỉ là một thành phần tạo nên thành công của nó. Thước đo thực sự của chất lượng production nằm ở **độ tin cậy, khả năng mở rộng, hiệu quả và tính bảo mật** của hệ thống [1]. Tài liệu này đóng vai trò là một hướng dẫn toàn diện để thấm nhuần tư duy đó, sử dụng cấu hình `docker-compose.yml` được cung cấp làm trường hợp nghiên cứu để phê bình và cải thiện theo tiêu chuẩn đẳng cấp thế giới.

### Khung MECE

Để đảm bảo một phân tích hoàn chỉnh và không dư thừa, chúng ta sẽ áp dụng nguyên tắc **MECE**: **Mutually Exclusive, Collectively Exhaustive** (Không trùng lặp, Không bỏ sót). Khung này, được mượn từ tư vấn quản trị, đảm bảo rằng mọi khía cạnh của chất lượng production đều được bao phủ mà không bị chồng chéo. Chúng tôi phân loại toàn bộ phạm vi chất lượng production của LLM thành sáu trụ cột riêng biệt nhưng có liên kết với nhau:

| Trụ cột | Trọng tâm | Câu hỏi Cốt lõi |
| :--- | :--- | :--- |
| **I. Tối ưu hóa Hiệu năng & Tài nguyên** | Tối đa hóa tốc độ suy luận và hiệu quả. | Chúng ta có thể phục vụ các yêu cầu nhanh và hiệu quả đến mức nào? |
| **II. Độ tin cậy & Tính sẵn sàng cao** | Đảm bảo dịch vụ liên tục, chịu lỗi tốt. | Hệ thống có bị hỏng không, và nếu có, nó có thể phục hồi nhanh như thế nào? |
| **III. Khả năng quan sát & Giám sát** | Có được cái nhìn sâu sắc, khả thi về trạng thái hệ thống. | Điều gì đang xảy ra bên trong "hộp đen", và làm sao chúng ta biết? |
| **IV. Bảo mật & Tuân thủ** | Bảo vệ mô hình, dữ liệu và cơ sở hạ tầng. | Hệ thống có an toàn không, và nó có đáp ứng các yêu cầu pháp lý không? |
| **V. Triển khai & MLOps** | Tự động hóa và chuẩn hóa vòng đời vận hành. | Làm thế nào để chúng ta xây dựng, triển khai và quản lý các thay đổi một cách đáng tin cậy? |
| **VI. Đánh giá & Đảm bảo Chất lượng** | Xác thực chất lượng đầu ra của mô hình và giá trị kinh doanh. | Mô hình có cung cấp các câu trả lời đúng, có giá trị và không độc hại không? |

### Bối cảnh Hệ thống: Phân tích `qwen2.5_docker-compose.yml`

Cấu hình được cung cấp triển khai mô hình `Qwen/Qwen2.5-1.5B-Instruct-AWQ` sử dụng `vllm/vllm-openai:v0.6.6.post1`. Việc lựa chọn **vLLM** này là một quyết định đẳng cấp thế giới, vì nó tận dụng thuật toán **PagedAttention** để tăng đáng kể thông lượng so với các framework phục vụ truyền thống [2]. Tuy nhiên, cấu hình này chứa một số rủi ro production nghiêm trọng cần được giải quyết.

```yaml
services:
  vllm-qwen:
    # ...
    image: vllm/vllm-openai:v0.6.6.post1
    runtime: nvidia
    network_mode: host  # RỦI RO BẢO MẬT NGHIÊM TRỌNG
    # ...
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct-AWQ
      --host 0.0.0.0
      --port 30030
      --quantization awq
      --dtype half
      --gpu-memory-utilization 0.3 # ĐÁNH ĐỔI HIỆU NĂNG/ĐỘ TIN CẬY NGHIÊM TRỌNG
      --max-model-len 512
      --max-num-seqs 16
      --max-num-batched-tokens 512
      --enable-prefix-caching
      --enable-chunked-prefill
      --swap-space 4
      --trust-remote-code # RỦI RO BẢO MẬT NGHIÊM TRỌNG
      --disable-log-requests
    restart: always # KHÔNG ĐỦ CHO TÍNH SẴN SÀNG CAO
    
    ```


Các phần sau sẽ trình bày chi tiết cách chuyển đổi thiết lập ban đầu này thành một hệ thống production mạnh mẽ, đẳng cấp thế giới bằng cách giải quyết sáu trụ cột MECE.

---

## Trụ cột I: Tối ưu hóa Hiệu năng & Tài nguyên (Trang 2-5)

### Lợi thế của vLLM: PagedAttention

**vLLM** là tiêu chuẩn vàng cho việc phục vụ LLM nhờ cơ chế **PagedAttention**. Kỹ thuật này quản lý bộ nhớ đệm Key-Value (KV) một cách hiệu quả bằng cách xử lý nó giống như bộ nhớ ảo và phân trang, cho phép cấp phát bộ nhớ không liên tục. Điều này rất quan trọng vì bộ nhớ cần thiết cho bộ nhớ đệm KV tăng động theo độ dài chuỗi, dẫn đến phân mảnh bộ nhớ đáng kể trong các hệ thống truyền thống. PagedAttention cho phép **tối đa hóa việc sử dụng GPU** và **thông lượng cao** bằng cách phục vụ nhiều yêu cầu đồng thời hơn [3].

### Các Chỉ số Hiệu năng Chính (KPIs)

Việc phục vụ LLM đẳng cấp thế giới được đo lường bằng ba KPI chính:

1. **Time to First Token (TTFT):** Độ trễ giữa việc nhận yêu cầu và tạo ra token đầu ra đầu tiên. Đây là thước đo chính cho **trải nghiệm người dùng cảm nhận được**. Càng thấp càng tốt.
    
2. **Throughput (Tokens Per Second - TPS):** Tổng số token được tạo ra mỗi giây trên tất cả các yêu cầu đồng thời. Đây là thước đo chính cho **công suất hệ thống và hiệu quả chi phí**. Càng cao càng tốt.
    
3. **GPU Memory Utilization:** Tỷ lệ phần trăm bộ nhớ GPU được sử dụng tích cực cho trọng số mô hình và bộ nhớ đệm KV. Mức sử dụng cao (ví dụ: >90%) là mong muốn để đạt hiệu quả chi phí, nhưng phải cân bằng với độ tin cậy.
    

### Phân tích sâu: Tinh chỉnh tham số vLLM

Cấu hình được cung cấp cố gắng tối ưu hóa hiệu năng, nhưng đưa ra những sự đánh đổi đáng kể:

#### 1. Sự đánh đổi `gpu-memory-utilization`

Cài đặt `--gpu-memory-utilization 0.3` là **cực kỳ thận trọng**. Điều này có nghĩa là chỉ 30% bộ nhớ GPU được dành riêng cho trọng số mô hình và bộ nhớ đệm KV động, để lại 70% không sử dụng.

- **Phê bình:** Mặc dù an toàn, nhưng đây **không phải là hiệu quả chi phí đẳng cấp thế giới**. Trong môi trường production, bạn đang trả tiền cho toàn bộ GPU. Việc để 70% nhàn rỗi là lãng phí tài nguyên.
    
- **Giải pháp Đẳng cấp Thế giới:** Giá trị lý tưởng thường nằm trong khoảng từ **0.85 đến 0.95**. Điều này tối đa hóa thông lượng trong khi để lại một bộ đệm nhỏ cho chi phí hệ thống và ngăn ngừa lỗi Hết bộ nhớ (Out-of-Memory - OOM). Giá trị này phải được xác định thông qua **kiểm thử tải** nghiêm ngặt (xem bên dưới).
    

#### 2. Giới hạn Batching và Sequence

Các tham số `--max-model-len 512`, `--max-num-seqs 16`, và `--max-num-batched-tokens 512` xác định chiến lược batching (xử lý lô) của hệ thống.

- `--max-model-len 512`: Đây là độ dài ngữ cảnh tối đa (token đầu vào + đầu ra). Đối với trình phân loại cảm xúc đơn giản, điều này có thể đủ, nhưng nó hạn chế nghiêm trọng khả năng xử lý đầu vào dài hơn hoặc tạo ra phản hồi chi tiết của mô hình. Một hệ thống đẳng cấp thế giới nên điều chỉnh linh hoạt dựa trên ngữ cảnh tối đa của mô hình (ví dụ: 8192 cho Qwen2.5-1.5B) hoặc trường hợp sử dụng dự kiến.
    
- `--max-num-seqs 16`: Số lượng yêu cầu đồng thời tối đa (sequences) mà vLLM sẽ xử lý. Đây là giới hạn cứng về tính đồng thời.
    
- `--max-num-batched-tokens 512`: Số lượng token tối đa (đầu vào + đầu ra) có thể được xử lý trong một lần forward pass. Đây là điều khiển chính cho việc sử dụng GPU.
    

**Nguyên tắc Tinh chỉnh Đẳng cấp Thế giới:** Các tham số này phải được tinh chỉnh cùng nhau, không phải riêng lẻ, để tìm ra **điểm tối ưu** nhằm tối đa hóa TPS mà không vượt quá mục tiêu TTFT SLO.

#### 3. Các tính năng Caching Nâng cao

Việc bao gồm `--enable-prefix-caching` và `--enable-chunked-prefill` là một **thực hành đẳng cấp thế giới**.

- **Prefix Caching:** Cần thiết cho các ứng dụng như Retrieval-Augmented Generation (RAG) nơi prompt (ngữ cảnh được truy xuất) không đổi qua nhiều yêu cầu. Nó lưu trữ bộ nhớ đệm KV cho prompt, tiết kiệm thời gian tính toán lại và cải thiện đáng kể TTFT cho các yêu cầu tiếp theo [4].
    
- **Chunked Prefill:** Cho phép xử lý các prompt rất dài bằng cách chia nhỏ chúng thành các phần nhỏ hơn, ngăn chặn một yêu cầu dài chặn toàn bộ batch và cải thiện tính công bằng.
    

### Chiến lược Mở rộng (Scaling)

Tệp `docker-compose` ngụ ý việc triển khai đơn lẻ (single-instance). Một hệ thống đẳng cấp thế giới yêu cầu một chiến lược mở rộng mạnh mẽ:

|**Chiến lược**|**Mô tả**|**Trường hợp sử dụng**|
|---|---|---|
|**Vertical Scaling (Mở rộng theo chiều dọc)**|Nâng cấp lên GPU mạnh hơn (ví dụ: từ A10 lên H100).|Khi mô hình quá lớn đối với một GPU duy nhất, hoặc khi một instance có thể xử lý tải nhưng cần thông lượng cao hơn.|
|**Horizontal Scaling (Mở rộng theo chiều ngang)**|Chạy nhiều instance vLLM giống hệt nhau đằng sau bộ cân bằng tải.|**Bắt buộc cho Tính sẵn sàng cao (Trụ cột II)** và khi tổng lượng yêu cầu vượt quá khả năng của một GPU.|
|**Dynamic Batching**|Tính năng cốt lõi của vLLM, tối đa hóa việc sử dụng GPU bằng cách điền đầy batch với các yêu cầu.|Luôn được bật và tối ưu hóa thông qua các tham số tinh chỉnh ở trên.|

### Kiểm thử Tải và Đo điểm chuẩn (Benchmarking)

Trước bất kỳ quá trình triển khai nào, **kiểm thử tải nghiêm ngặt** là bắt buộc.

1. **Xác định Mục tiêu SLO:** ví dụ: TTFT < 500ms cho 99% yêu cầu; TPS > 100 token/giây.
    
2. **Công cụ:** Sử dụng các công cụ như **Locust** hoặc các script Python tùy chỉnh để mô phỏng các mẫu lưu lượng truy cập trong thế giới thực (ví dụ: độ dài prompt thay đổi, lưu lượng truy cập đột biến).
    
3. **Phương pháp luận:** Thay đổi hệ thống các tham số vLLM (đặc biệt là `--gpu-memory-utilization` và các giới hạn batching) trong khi giám sát các KPI để tìm cấu hình tối ưu đáp ứng SLO với chi phí thấp nhất.
    

---

## Trụ cột II: Độ tin cậy & Tính sẵn sàng cao (Trang 6-8)

### Xác định SLO và SLI

Độ tin cậy bắt đầu bằng các định nghĩa rõ ràng. **Service Level Objective (SLO)** là mục tiêu độ tin cậy (ví dụ: 99.9% thời gian hoạt động). **Service Level Indicator (SLI)** là chỉ số được sử dụng để đo lường nó (ví dụ: tỷ lệ phần trăm các yêu cầu thành công).

**SLO Đẳng cấp Thế giới cho Phục vụ LLM:**

- **Availability SLO:** 99.99% (Bốn số 9) thời gian hoạt động.
    
- **Latency SLO:** TTFT phân vị thứ 99 < 500ms.
    
- **Error Rate SLO:** < 0.1% yêu cầu trả về lỗi 5xx.
    

### Khả năng phục hồi của Container và Kiểm tra Sức khỏe

Chỉ thị `restart: always` trong `docker-compose.yml` là một **cách tiếp cận ngây thơ** đối với khả năng phục hồi. Nó chỉ xử lý các sự cố sập container, không xử lý các lỗi cấp ứng dụng hoặc hiệu suất bị suy giảm.

- **Phê bình:** Nếu tiến trình vLLM bị treo hoặc bắt đầu trả về phản hồi chậm, `restart: always` sẽ không kích hoạt khởi động lại. Hệ thống sẽ "hoạt động" nhưng không sử dụng được.
    
- **Giải pháp Đẳng cấp Thế giới: Điều phối:** Một hệ thống đẳng cấp thế giới sử dụng bộ điều phối container như **Kubernetes (K8s)**. K8s cung cấp hai đầu dò (probes) thiết yếu:
    
    1. **Liveness Probe:** Kiểm tra xem ứng dụng có đang chạy và khỏe mạnh không (ví dụ: một HTTP GET đơn giản đến `/health`). Nếu thất bại, K8s khởi động lại container.
        
    2. **Readiness Probe:** Kiểm tra xem ứng dụng có sẵn sàng phục vụ lưu lượng truy cập không (ví dụ: kiểm tra xem mô hình đã được tải đầy đủ và GPU có phản hồi không). Nếu thất bại, K8s ngừng gửi lưu lượng truy cập đến instance đó.
        

### Xử lý các lỗi liên quan đến GPU

Các vấn đề liên quan đến GPU là nguyên nhân phổ biến nhất gây ra lỗi phục vụ LLM.

- **Vấn đề Driver GPU:** Container phải có khả năng xác minh GPU có thể truy cập được. Kiểm tra readiness nên bao gồm lệnh gọi tới `nvidia-smi` hoặc một endpoint cụ thể của vLLM xác nhận ngữ cảnh CUDA đã được khởi tạo.
    
- **Lỗi OOM:** Nếu hệ thống hết bộ nhớ (do lưu lượng truy cập tăng đột biến bất ngờ hoặc cấu hình sai), tiến trình vLLM sẽ gặp sự cố. Tham số `gpu-memory-utilization` (Trụ cột I) là biện pháp phòng thủ chính, nhưng một hệ thống mạnh mẽ phải được cấu hình để khởi động lại container và có khả năng giảm quy mô lưu lượng truy cập đến node bị ảnh hưởng.
    

### Sự dư thừa và Chuyển đổi dự phòng (Failover)

Tính sẵn sàng cao (HA) yêu cầu chạy **nhiều bản sao (replicas)** của dịch vụ vLLM.

- **Dự phòng Active-Active:** Tất cả các bản sao đều tích cực phục vụ lưu lượng truy cập. Đây là tiêu chuẩn cho phục vụ LLM, vì nó cung cấp cả HA và phân phối tải. Một bộ cân bằng tải (ví dụ: NGINX, AWS ALB) phân phối các yêu cầu trên tất cả các instance khỏe mạnh.
    
- **Chuyển đổi dự phòng (Failover):** Nếu một instance không vượt qua kiểm tra Liveness/Readiness, bộ cân bằng tải sẽ tự động định tuyến lưu lượng truy cập đến các instance khỏe mạnh còn lại. Đây là chức năng cốt lõi của K8s hoặc bộ cân bằng tải chuyên dụng.
    

### Suy giảm chất lượng có kiểm soát (Graceful Degradation)

Trong trường hợp lỗi thảm khốc (ví dụ: sự cố GPU khu vực), một hệ thống đẳng cấp thế giới thực hiện **suy giảm chất lượng có kiểm soát** để duy trì một mức độ dịch vụ nhất định.

|**Mức độ Suy giảm**|**Hành động**|**Trải nghiệm Người dùng**|
|---|---|---|
|**Cấp độ 1 (Tải cao)**|Phục vụ phản hồi được lưu trong bộ nhớ đệm cho các truy vấn phổ biến; tăng tạm thời SLO về độ trễ.|Chậm trễ nhẹ, nhưng dịch vụ vẫn hoạt động.|
|**Cấp độ 2 (Lỗi một phần)**|Chuyển đổi dự phòng sang mô hình nhỏ hơn, dựa trên CPU (ví dụ: mô hình chưng cất hoặc trình phân loại dựa trên quy tắc đơn giản).|Giảm chất lượng/khả năng, nhưng chức năng cốt lõi (phân loại cảm xúc) được bảo tồn.|
|**Cấp độ 3 (Lỗi toàn bộ)**|Trả về thông báo lỗi rõ ràng, đầy đủ thông tin và chuyển hướng đến trang trạng thái tĩnh.|Không có dịch vụ, nhưng là một sự cố chuyên nghiệp, minh bạch.|

---

## Trụ cột III: Khả năng quan sát & Giám sát (Trang 9-11)

Khả năng quan sát là khả năng đặt các câu hỏi tùy ý về trạng thái bên trong hệ thống của bạn dựa trên dữ liệu mà nó tạo ra. Nó được xây dựng trên **Ba Trụ cột**: Logs (Nhật ký), Metrics (Chỉ số) và Traces (Vết) [5].

### Ghi log có cấu trúc (Structured Logging)

Cấu hình sử dụng `--disable-log-requests`, đây là một **phản mẫu (anti-pattern) nghiêm trọng** cho production. Mặc dù nó làm giảm khối lượng log, nhưng nó loại bỏ khả năng gỡ lỗi các vấn đề cụ thể của yêu cầu.

- **Ghi log Đẳng cấp Thế giới:**
    
    1. **Bật Ghi log:** Xóa `--disable-log-requests`.
        
    2. **Định dạng có cấu trúc:** Cấu hình vLLM để xuất log ở **định dạng JSON**. Điều này cho phép các hệ thống ghi log tập trung (ví dụ: ELK Stack, Loki, Datadog) phân tích cú pháp các trường như `request_id`, `prompt_length`, `latency`, và `status_code` một cách hiệu quả.
        
    3. **Ngữ cảnh hóa:** Mỗi mục log phải bao gồm một **Request ID** duy nhất (được tạo bởi client hoặc lớp ingress) để truy vết một yêu cầu duy nhất qua tất cả các dịch vụ.
        

### Thu thập Chỉ số (Metrics Collection)

Metrics là các điểm dữ liệu chuỗi thời gian được tổng hợp, sử dụng để giám sát xu hướng và cảnh báo.

#### 1. Chỉ số Hệ thống

Đây là các chỉ số cơ sở hạ tầng tiêu chuẩn, cần thiết để hiểu sức khỏe phần cứng bên dưới:

- **Chỉ số GPU:** Utilization (%), Memory Usage (GB), Temperature (°C), Power Draw (W).
    
- **Chỉ số Host:** CPU Load, Network I/O, Disk Usage.
    
- **Công cụ:** Sử dụng **Prometheus** với các exporter như `node_exporter` và `nvidia-smi_exporter` để thu thập dữ liệu này.
    

#### 2. Chỉ số Ứng dụng vLLM

vLLM hiển thị các chỉ số nội bộ quan trọng cần được giám sát:

|**Chỉ số**|**Mục đích**|**Ngưỡng Cảnh báo**|
|---|---|---|
|`vllm_request_queue_size`|Chỉ ra tồn đọng yêu cầu và khả năng bão hòa.|Cảnh báo nếu > 0 trong 5 phút.|
|`vllm_num_running_sequences`|Số lượng yêu cầu đồng thời đang được xử lý.|Cảnh báo nếu tiệm cận `--max-num-seqs`.|
|`vllm_kv_cache_usage_ratio`|Tỷ lệ phần trăm bộ nhớ đệm KV được sử dụng.|Cảnh báo nếu > 95% (cảnh báo trước OOM).|
|`vllm_time_to_first_token_seconds`|Đo lường trực tiếp SLO TTFT.|Cảnh báo nếu phân vị thứ 99 > 500ms.|

#### 3. Chỉ số Kinh doanh

Những chỉ số này liên kết hiệu suất kỹ thuật với kết quả kinh doanh:

- **Chi phí trên mỗi lần Suy luận:** Tổng chi phí GPU / Số lần suy luận thành công.
    
- **Độ chính xác Phân loại (Trụ cột VI):** Được giám sát theo thời gian thực để phát hiện sự trôi dạt mô hình (model drift).
    
- **Sự hài lòng của Người dùng:** Ngầm định (ví dụ: độ dài phiên) hoặc rõ ràng (ví dụ: like/dislike).
    

### Truy vết Phân tán (Distributed Tracing)

Đối với các kiến trúc vi dịch vụ phức tạp, **Truy vết Phân tán** (ví dụ: sử dụng OpenTelemetry) là bắt buộc. Nó theo dõi toàn bộ vòng đời của một yêu cầu, từ thiết bị của người dùng, qua bộ cân bằng tải, đến dịch vụ vLLM và quay lại. Điều này vô giá để gỡ lỗi các đợt tăng độ trễ do các bước nhảy mạng hoặc các phụ thuộc ngược dòng.

### Chiến lược Cảnh báo

Cảnh báo phải **có thể hành động** và **MECE** (tức là, một vấn đề sẽ kích hoạt một cảnh báo).

- **Mức độ Nghiêm trọng:** Xác định P1 (Nghiêm trọng, Gọi On-Call dậy), P2 (Cao, Điều tra trong giờ làm việc), và P3 (Thấp, Thông tin).
    
- **Mệt mỏi vì Cảnh báo (Alert Fatigue):** Tránh điều đó bằng cách đặt cảnh báo trên **SLOs** (triệu chứng) thay vì các chỉ số cấp thấp (nguyên nhân). Ví dụ: cảnh báo về "Vi phạm SLO Độ trễ" (P1) thay vì "Nhiệt độ GPU > 80°C" (P3, trừ khi nó trực tiếp gây ra P1).
    

---

## Trụ cột IV: Bảo mật & Tuân thủ (Trang 12-14)

Bảo mật là không thể thương lượng. Một lỗ hổng duy nhất có thể dẫn đến vi phạm dữ liệu, gián đoạn dịch vụ và tổn thất tài chính thảm khốc.

### Bảo mật Mạng: Rủi ro `network_mode: host`

Cấu hình sử dụng `network_mode: host`.

- **Phê bình:** Đây là một **lỗ hổng bảo mật nghiêm trọng** trong production. Nó có nghĩa là container chia sẻ ngăn xếp mạng của máy chủ, bỏ qua sự cô lập mạng. Bất kỳ cổng nào được mở bên trong container (như 30030) đều được hiển thị trực tiếp trên địa chỉ IP của máy chủ và container có thể truy cập tất cả các dịch vụ mạng của máy chủ.
    
- **Giải pháp Đẳng cấp Thế giới:**
    
    1. **Mạng Dành riêng:** Sử dụng mạng Docker chuyên dụng (hoặc Kubernetes CNI) để cô lập container.
        
    2. **Kiểm soát Ingress:** Đặt dịch vụ phía sau một reverse proxy/API Gateway xử lý chấm dứt SSL, giới hạn tốc độ và xác thực.
        
    3. **Tường lửa:** Thực hiện các quy tắc tường lửa nghiêm ngặt (Security Groups trong môi trường đám mây) để chỉ cho phép lưu lượng truy cập trên các cổng được yêu cầu (ví dụ: 443/80) từ các nguồn đáng tin cậy.
        

### Bảo mật API

API tương thích OpenAI của vLLM là một endpoint không được xác thực theo mặc định.

- **Xác thực (Authentication):** Tất cả các yêu cầu phải được xác thực. Sử dụng API Gateway để thực thi:
    
    - **API Keys:** Đơn giản, nhưng hiệu quả cho giao tiếp máy-máy.
        
    - **JWT (JSON Web Tokens):** Tiêu chuẩn cho các ứng dụng hướng tới người dùng, cho phép ủy quyền chi tiết.
        
- **Phân quyền (Authorization - RBAC):** Thực hiện Kiểm soát truy cập dựa trên vai trò. Không phải tất cả người dùng đều có quyền truy cập vào tất cả các mô hình hoặc tất cả các endpoint (ví dụ: chỉ quản trị viên mới có thể truy cập endpoint `/metrics`).
    
- **Giới hạn tốc độ (Rate Limiting):** Cần thiết để bảo vệ chống lại các cuộc tấn công Từ chối Dịch vụ (DoS) và đảm bảo sử dụng công bằng. Giới hạn yêu cầu mỗi giây cho mỗi khóa API hoặc ID người dùng.
    

### Quyền riêng tư Dữ liệu và PII

Vì mô hình là một trình phân loại cảm xúc, đầu vào của người dùng có thể chứa **Thông tin Nhận dạng Cá nhân (PII)**.

- **Làm sạch Dữ liệu:** Triển khai **Dịch vụ Biên tập PII** như một bước tiền xử lý. Dịch vụ này sử dụng một mô hình riêng biệt, độ tin cậy cao hoặc hệ thống dựa trên quy tắc để phát hiện và che giấu PII (tên, địa chỉ, số điện thoại) trước khi prompt đến dịch vụ vLLM.
    
- **Chính sách Ghi log:** Đảm bảo rằng log (Trụ cột III) được cấu hình để **không bao giờ** lưu trữ PII thô. Chỉ các prompt đã được biên tập mới được ghi lại.
    

### Bảo mật Mô hình: Chuỗi cung ứng và Sự tin cậy

Tham số `--trust-remote-code` là một **rủi ro bảo mật lớn**.

- **Phê bình:** Cờ này cho phép các tệp cấu hình của mô hình (ví dụ: `modeling_qwen2.py`) thực thi mã Python tùy ý trong quá trình tải mô hình. Nếu kho lưu trữ Hugging Face bị xâm phạm, máy chủ production của bạn sẽ bị xâm phạm.
    
- **Giải pháp Đẳng cấp Thế giới:**
    
    1. **Xóa `--trust-remote-code`:** Chỉ sử dụng nó trong quá trình phát triển/thử nghiệm.
        
    2. **Artifact cục bộ:** Tải xuống mô hình và tất cả các tệp mã/cấu hình cần thiết về một **kho lưu trữ artifact nội bộ, đáng tin cậy** (ví dụ: AWS S3, Azure Blob Storage).
        
    3. **Sử dụng đường dẫn cục bộ:** Thay đổi lệnh vLLM để tải mô hình từ đường dẫn cục bộ, đảm bảo mã đang được thực thi đã được kiểm toán và kiểm soát.
        

---

## Trụ cột V: Triển khai & MLOps (Trang 15-17)

MLOps là kỷ luật chuẩn hóa và hợp lý hóa toàn bộ vòng đời học máy. Việc triển khai đẳng cấp thế giới được xây dựng trên sự tự động hóa và tính nhất quán.

### Cơ sở hạ tầng dưới dạng Mã (IaC)

`docker-compose.yml` là một hình thức cấu hình dưới dạng mã, nhưng nó không đủ để quản lý một cụm GPU.

- **IaC Đẳng cấp Thế giới:** Sử dụng các công cụ như **Terraform** hoặc **Pulumi** để cung cấp cơ sở hạ tầng bên dưới (VMs, GPU instances, mạng, bộ cân bằng tải). Điều này đảm bảo môi trường có thể **tái tạo** và các thay đổi có thể **kiểm toán**.
    
- **K8s Manifests:** Sử dụng các tệp manifest Kubernetes YAML hoặc biểu đồ Helm để xác định việc triển khai vLLM, service và ingress. Điều này trừu tượng hóa cơ sở hạ tầng và cho phép khả năng di động.
    

### Đường ống CI/CD cho Dịch vụ LLM

Đường ống Tích hợp Liên tục/Triển khai Liên tục (CI/CD) tự động hóa quy trình từ khi cam kết mã (code commit) đến khi triển khai production.

|**Giai đoạn**|**Mục tiêu**|**Các Hoạt động Chính**|
|---|---|---|
|**CI (Tích hợp)**|Xây dựng và kiểm tra image dịch vụ.|1. Tối ưu hóa Dockerfile (multi-stage build). 2. Phân tích mã tĩnh. 3. Kiểm tra Đơn vị và Tích hợp. 4. Quét Image (kiểm tra lỗ hổng).|
|**CD (Triển khai)**|Triển khai dịch vụ lên production.|1. **Triển khai Canary:** Định tuyến một tỷ lệ nhỏ (ví dụ: 5%) lưu lượng truy cập trực tiếp đến phiên bản mới. 2. **Kiểm tra Sức khỏe Tự động:** Giám sát SLO (Trụ cột II) và Chỉ số Kinh doanh (Trụ cột III) trong 30 phút. 3. **Tự động Rollback:** Nếu bất kỳ chỉ số nào vi phạm ngưỡng, tự động chấm dứt phiên bản mới và hoàn nguyên về phiên bản ổn định trước đó.|

### Quản lý Cấu hình

Các đối số dòng lệnh vLLM là một dạng cấu hình. Việc quản lý cấu hình này trên các môi trường (Dev, Staging, Prod) là rất quan trọng.

- **Biến môi trường:** Thiết lập hiện tại sử dụng các biến môi trường cho `NVIDIA_VISIBLE_DEVICES`. Đây là thực hành tốt.
    
- **Quản lý Bí mật (Secrets Management):** Các khóa API, thông tin đăng nhập cơ sở dữ liệu và thông tin nhạy cảm khác **không bao giờ** được lưu trữ trong `docker-compose.yml` hoặc kiểm soát phiên bản. Sử dụng các trình quản lý bí mật chuyên dụng (ví dụ: HashiCorp Vault, AWS Secrets Manager, K8s Secrets).
    
- **ConfigMaps:** Trong K8s, sử dụng ConfigMaps để lưu trữ các tham số cấu hình không nhạy cảm (như các đối số lệnh vLLM) tách biệt với logic triển khai.
    

### Quản lý Vòng đời Mô hình

Artifact mô hình (`Qwen/Qwen2.5-1.5B-Instruct-AWQ`) và mã phục vụ (`vllm-openai:v0.6.6.post1`) phải được đánh phiên bản độc lập.

- **Đánh phiên bản Mô hình:** Mỗi khi mô hình được tinh chỉnh hoặc lượng tử hóa lại, nó phải nhận được thẻ phiên bản mới, bất biến (ví dụ: `qwen2.5-v1.0.1`).
    
- **Đánh phiên bản Mã Phục vụ:** Docker image cho dịch vụ vLLM cũng phải được đánh phiên bản (ví dụ: `vllm-service:20251215-01`).
    
- **Tách rời:** Cấu hình triển khai (IaC) nên chỉ định phiên bản mô hình nào và phiên bản dịch vụ nào sẽ kết hợp, cho phép cập nhật độc lập và rollback một trong hai thành phần.
    

---

## Trụ cột VI: Đánh giá & Đảm bảo Chất lượng (Trang 18-20)

Trụ cột cuối cùng đảm bảo rằng hệ thống không chỉ nhanh và đáng tin cậy mà còn **chính xác** và **có giá trị** đối với người dùng.

### Đánh giá Offline

Trước khi bất kỳ phiên bản mô hình mới nào được triển khai, nó phải vượt qua thử nghiệm offline nghiêm ngặt.

- **Đo điểm chuẩn cụ thể theo tác vụ:** Đối với trình phân loại cảm xúc, điều này có nghĩa là chạy mô hình trên một **bộ dữ liệu vàng** (golden dataset) gồm các đầu vào văn bản lớn, được quản lý và dán nhãn bởi con người.
    
- **Chỉ số:** Chỉ số chính là **F1-score** (cho phân loại), vì nó cân bằng giữa độ chính xác (precision) và độ phủ (recall). Báo cáo F1-score cho từng lớp cảm xúc để xác định điểm yếu.
    
- **Kiểm thử hồi quy:** Phiên bản mô hình mới phải hoạt động **ít nhất là tốt bằng** mô hình production hiện tại trên bộ dữ liệu vàng. Nếu nó hoạt động kém hơn, việc triển khai sẽ bị chặn.
    

### Đánh giá Online (A/B Testing)

Các chỉ số offline không phải lúc nào cũng tương quan với trải nghiệm người dùng trong thế giới thực. **A/B testing** là phương pháp đẳng cấp thế giới để đánh giá online.

- **Thiết lập:** Triển khai mô hình mới (Model B) cùng với mô hình production hiện tại (Model A). Định tuyến một tập hợp con nhỏ, ngẫu nhiên người dùng (ví dụ: 10%) đến Model B.
    
- **Chỉ số Online:** Giám sát các chỉ số sau cho cả hai nhóm:
    
    - **Tương tác của Người dùng:** Người dùng nhận được phản hồi của Model B có nhiều khả năng tiếp tục cuộc trò chuyện không?
        
    - **Phản hồi Rõ ràng:** Người dùng có cung cấp tỷ lệ "like" cao hơn cho Model B không?
        
    - **Tác động Kinh doanh:** Model B có dẫn đến tỷ lệ chuyển đổi cao hơn hoặc các chỉ số kinh doanh chính khác không?
        
- **Quyết định:** Chỉ khi Model B vượt trội hơn đáng kể so với Model A trên các chỉ số online đã xác định thì nó mới được thăng cấp lên 100% lưu lượng truy cập.
    

### An toàn và Lọc Độc hại (Guardrails)

LLM dễ tạo ra nội dung độc hại, thiên kiến hoặc không thực tế. Guardrails là điều cần thiết.

- **Input Guardrails:** Lọc các prompt của người dùng để tìm nội dung có hại (ví dụ: ngôn từ kích động thù địch, tự làm hại bản thân) trước khi chúng đến mô hình.
    
- **Output Guardrails:** Sử dụng một mô hình phân loại riêng biệt, nhỏ và có độ tin cậy cao để kiểm tra đầu ra của vLLM xem có độc hại không. Nếu đầu ra bị gắn cờ, hãy thay thế bằng phản hồi an toàn, chung chung (ví dụ: "Tôi không thể trả lời yêu cầu đó.").
    
- **Phòng thủ Prompt Injection:** Thực hiện các kỹ thuật để ngăn người dùng thao túng hướng dẫn của mô hình (ví dụ: sử dụng ghép nối đầu vào/đầu ra hoặc tường lửa LLM chuyên dụng).
    

### Con người tham gia vào vòng lặp (HITL)

Vòng phản hồi liên tục là bước cuối cùng để đạt được chất lượng đẳng cấp thế giới.

- **Thu thập Phản hồi:** Thu thập tất cả các trường hợp người dùng cung cấp phản hồi tiêu cực (ví dụ: "dislike") hoặc nơi bộ lọc độc hại được kích hoạt.
    
- **Đánh giá của Con người:** Một nhóm chú thích của con người xem xét các trường hợp bị gắn cờ này.
    
- **Phát hiện Trôi dạt Mô hình:** Dữ liệu được con người đánh giá được sử dụng để:
    
    1. **Huấn luyện lại Mô hình:** Kết hợp các ví dụ mới, khó vào tập huấn luyện.
        
    2. **Cập nhật Bộ dữ liệu vàng:** Thêm các ví dụ mới vào tập đánh giá offline để ngăn ngừa sự hồi quy trong tương lai.
        

---

## Kết luận và Các bước tiếp theo

Để đạt được chất lượng production đẳng cấp thế giới cho một hệ thống phục vụ LLM là một hành trình liên tục, không phải là đích đến. Nó đòi hỏi một cách tiếp cận toàn diện, dựa trên MECE, giải quyết Hiệu năng, Độ tin cậy, Khả năng quan sát, Bảo mật, Triển khai và Đánh giá một cách đồng thời.

`docker-compose.yml` được cung cấp là một điểm khởi đầu mạnh mẽ nhờ lựa chọn vLLM, nhưng nó hiện là một **cấu hình cấp phát triển**. Kỹ sư đẳng cấp thế giới phải ngay lập tức giải quyết các rủi ro nghiêm trọng:

1. **Bảo mật:** Loại bỏ `network_mode: host` và `--trust-remote-code`.
    
2. **Hiệu quả:** Kiểm thử tải nghiêm ngặt và tăng `--gpu-memory-utilization` lên >0.85.
    
3. **Độ tin cậy:** Di chuyển sang bộ điều phối container (Kubernetes) để thực hiện các probe Liveness/Readiness và HA thích hợp.
    
4. **Khả năng quan sát:** Bật ghi log và triển khai ngăn xếp chỉ số dựa trên Prometheus.
    

### Các Bước Hành động Cụ thể cho Thực tập sinh

Con đường trở thành một kỹ sư MLOps đẳng cấp thế giới của bạn bắt đầu ngay bây giờ. Trọng tâm trước mắt của bạn nên là những điều sau:

1. **Di chuyển sang Kubernetes:** Nghiên cứu và soạn thảo các tệp YAML Kubernetes Deployment, Service và Ingress để thay thế `docker-compose.yml`.
    
2. **Kiểm thử Tải:** Phát triển một script Python sử dụng thư viện như `locust` để đo điểm chuẩn cấu hình vLLM hiện tại và xác định giá trị `--gpu-memory-utilization` tối ưu.
    
3. **Ngăn xếp Quan sát:** Nghiên cứu cách triển khai `vllm_exporter` (một Prometheus exporter) cùng với dịch vụ vLLM để bắt đầu thu thập các chỉ số cụ thể của ứng dụng.
    

Bằng cách nắm vững sáu trụ cột này, bạn sẽ không chỉ triển khai một hệ thống chức năng mà còn là một hệ thống **kiên cường, hiệu quả chi phí, an toàn và liên tục cải tiến**—dấu hiệu của một chuyên gia MLOps đẳng cấp thế giới.

---

## Tài liệu tham khảo

[1] D. Sculley, et al. "Hidden Technical Debt in Machine Learning Systems." NIPS 2015.

[2] W. Kwon, et al. "vLLM: Efficient Memory Management for Large Language Model Serving with PagedAttention." arXiv:2309.06180.

[3] Predibase. "LLM Serving Guide: How to Build Faster Inference for Open Source LLMs."

[4] vLLM Documentation. "Prefix Caching."

[5] C. O'Connell, et al. "The Three Pillars of Observability: Logs, Metrics, and Traces." O'Reilly Media.

[6] Shahbhat. "From Code to Production: A Checklist for Reliable, Scalable, and Secure Deployments." Medium.

[7] Vellum. "The Four Pillars of Building LLM Applications for Production."

[8] Pezzo. "The 5 Pillars for taking LLM to production." Dev.to.

[9] Hivenet. "Production Checklist for Your LLM API."

[10] Latitude. "Essential Checklist for Deploying LLM Features to Production."

[11] Plexobject. "Building a Production-Grade Enterprise AI Platform with vLLM."

[12] Esplio Labs. "How to Deploy LLMs in Production: Strategies, Pitfalls, and Best Practices."

[13] ML Architects. "Reliably Running Your Own LLM in Production."

[14] LinkedIn. "How MECE framework simplifies AI engineering."