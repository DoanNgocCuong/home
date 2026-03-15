# Tối Ưu Hóa Concurrency và Số Lượng Worker (RabbitMQ)

## 🎯 Vấn Đề Hiện Tại: Xử Lý Từng Message Một

Bạn quan sát thấy worker chỉ xử lý từng `conversation_id` một. Điều này là do cấu hình **Quality of Service (QoS)** mặc định của RabbitMQ/Pika.

Trong file `rabbitmq_consumer.py` (hoặc tương đương), bạn có thể đã thấy dòng này:

```python
# Set QoS: Process 1 message at a time
self.channel.basic_qos(prefetch_count=1) 
```

`prefetch_count=1` nghĩa là worker chỉ nhận 1 message từ queue, và chỉ nhận message tiếp theo sau khi đã `ack` (xác nhận xử lý xong) message hiện tại. Điều này đảm bảo tính an toàn và tránh mất message, nhưng giới hạn tốc độ xử lý.

---

## 1. LÀM SAO ĐỂ TĂNG TỐC ĐỘ XỬ LÝ SONG SONG?

Có hai cách chính để tăng tốc độ xử lý song song:

### A. Tăng `prefetch_count` (Tăng Concurrency Trong 1 Worker)

`prefetch_count` là số lượng message tối đa mà một worker có thể nhận và giữ trong bộ nhớ đệm (buffer) trước khi xác nhận xử lý.

**Cập Nhật Code:**

```python
# File: src/app/background/rabbitmq_consumer.py

# Thay đổi:
# self.channel.basic_qos(prefetch_count=1) 

# Thành:
CONCURRENCY_PER_WORKER = 10 # Ví dụ: cho phép 1 worker xử lý 10 message cùng lúc
self.channel.basic_qos(prefetch_count=CONCURRENCY_PER_WORKER) 
```

**Cơ chế:**

- Worker sẽ nhận 10 message từ queue.
- Worker sẽ dùng **10 thread hoặc process** (tùy thuộc vào framework bạn dùng: Celery, Python `threading`, `multiprocessing`, `asyncio`) để xử lý 10 message này song song.
- **Lưu ý quan trọng:** Việc tăng `prefetch_count` chỉ có tác dụng nếu code xử lý của bạn (tính score, update DB) là **thread-safe** và **non-blocking** (ví dụ: dùng `asyncio` hoặc `multiprocessing`). Nếu code là blocking (I/O-bound), bạn cần dùng `multiprocessing` hoặc `threading` để tận dụng.

### B. Tăng Số Lượng Worker Process (Tăng Concurrency Tổng Thể)

Đây là cách hiệu quả và dễ quản lý nhất. Mỗi worker là một process độc lập, chạy trên một core CPU.

**Cập Nhật Docker Compose:**

```yaml
# File: docker-compose.yml

services:
  # ... (app service)

  # Worker Process (Consumer)
  worker:
    build: .
    # ... (dependencies)
    # Thay vì chỉ chạy 1 worker:
    # command: python src/worker.py
  
    # Chạy 5 worker process:
    deploy:
      replicas: 5  # <-- Tăng số lượng worker process lên 5
    command: python src/worker.py
    volumes:
      - .:/app
```

**Cơ chế:**

- 5 process worker độc lập sẽ cùng lắng nghe queue.
- RabbitMQ sẽ tự động phân phối message cho 5 worker này (Round-robin).
- **Tổng Concurrency:** `Total Concurrency = Số lượng Worker Process * Concurrency Per Worker` (ví dụ: 5 * 10 = 50 message cùng lúc).

---

## 2. LÀM SAO ĐỂ BIẾT SỐ LƯỢNG WORKER TỐI ƯU?

Số lượng worker tối ưu phụ thuộc vào 3 yếu tố chính: **Phần cứng**, **Loại tác vụ**, và **Mục tiêu CCU**.

### A. Phân Tích Tác Vụ (Your Use Case)

| Yếu Tố              | Mô Tả                 | Ảnh Hưởng               |
| :-------------------- | :---------------------- | :------------------------- |
| **Tính Score** | Tính toán (CPU-bound) | Cần nhiều core CPU       |
| **Update DB**   | I/O (I/O-bound)         | Cần nhiều thread/process |
| **Fetch Data**  | I/O (I/O-bound)         | Cần nhiều thread/process |

**Kết luận:** Tác vụ của bạn là **Hybrid (CPU + I/O)**. Cần cân bằng giữa số core CPU và số lượng process/thread.

### B. Công Thức Tối Ưu (Dựa trên Phần Cứng)

Giả sử Server có **N** core CPU.

1. **Số lượng Worker Process (W):**

   - **Quy tắc:** `W ≈ N` (Nếu tác vụ là CPU-bound)
   - **Quy tắc:** `W ≈ 2N + 1` (Nếu tác vụ là I/O-bound)
   - **Với Hybrid:** Bắt đầu với `W = 2N`
2. **Concurrency Per Worker (`prefetch_count` - C):**

   - **Quy tắc:** `C` nên đủ lớn để giữ CPU bận rộn, nhưng không quá lớn để gây quá tải.
   - **Bắt đầu:** `C = 5` đến `10`

**Ví dụ:** Server có 4 core CPU.

- **Worker Process (W):** `2 * 4 = 8`
- **Concurrency Per Worker (C):** `10`
- **Tổng Concurrency:** `8 * 10 = 80`

### C. Chạy Benchmark (Theo Yêu Cầu)

Bạn cần chạy benchmark để tìm ra con số chính xác.

**Mục tiêu:** 100 CCU (Concurrent Users) và 500 requests.

1. **Setup:**

   - Bắt đầu với cấu hình: `W=4` (4 worker process) và `C=10` (`prefetch_count=10`).
   - Tổng concurrency: 40.
2. **Chạy Load Test:**

   - Dùng công cụ như `Locust` hoặc `JMeter` để bắn 500 requests liên tục (hoặc 100 CCU) vào API `POST /conversations/end`.
   - **Đo lường:**
     - **Latency:** Thời gian xử lý trung bình của worker (từ lúc nhận message đến lúc PROCESSED).
     - **CPU Usage:** CPU của worker process.
     - **Queue Length:** Chiều dài queue (nếu queue dài ra, cần thêm worker).
3. **Tối Ưu Hóa:**

   - **Nếu CPU < 80%:** Tăng `W` (số lượng worker process) lên 6, 8, 10...
   - **Nếu CPU > 90%:** Giảm `C` (prefetch_count) hoặc tăng `W` (nếu còn core).
   - **Nếu Queue dài:** Tăng `W` (thêm worker).

---

## 3. CẤU HÌNH DEV VÀ PRODUCTION

| Cấu Hình                   | Dev            | Production            | Lý Do                                                      |
| :--------------------------- | :------------- | :-------------------- | :---------------------------------------------------------- |
| **Worker Process (W)** | 1 - 2          | `2N` (N = số core) | Dev: Tiết kiệm tài nguyên. Prod: Tối ưu hiệu năng.  |
| **Concurrency (C)**    | 1              | 5 - 10                | Dev: Dễ debug (xử lý tuần tự). Prod: Tăng throughput. |
| **Hardware**           | Shared/Low-end | Dedicated/High-end    | Prod cần phần cứng mạnh hơn.                           |
| **Logging**            | DEBUG          | INFO/ERROR            | Dev: Log chi tiết. Prod: Log lỗi.                         |

**Ví dụ Cấu Hình Dev (Dễ Debug):**

- `worker` service: `deploy: replicas: 1`
- `prefetch_count`: `1`

**Ví dụ Cấu Hình Prod (Tối Ưu):**

- `worker` service: `deploy: replicas: 8`
- `prefetch_count`: `10`

---

## 🚀 TÓM TẮT HÀNH ĐỘNG

1. **Code:** Cập nhật `prefetch_count` trong `rabbitmq_consumer.py` thành một giá trị ban đầu (ví dụ: 10).
2. **Deploy:** Cập nhật `docker-compose.yml` để chạy nhiều worker process (ví dụ: 4-8 replicas).
3. **Benchmark:** Chạy load test 100 CCU / 500 requests để đo lường và tinh chỉnh số lượng worker process và `prefetch_count` cho phù hợp với phần cứng thực tế.

**Bạn cần tôi tạo file code mẫu cho việc cập nhật `prefetch_count` và `docker-compose.yml` không?**

---

# Cách kiểm tra số core CPU 

```
1d [ubuntu@mgc-dev2-3090:~/cuong_dn/context-handling-bigmodule_PikaRobot_25112025] main(+11/-8,+6/-1)* ± nproc
96
1d [ubuntu@mgc-dev2-3090:~/cuong_dn/context-handling-bigmodule_PikaRobot_25112025] main(+11/-8,+6/-1)* ± lscpu
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Byte Order:                         Little Endian
Address sizes:                      46 bits physical, 48 bits virtual
CPU(s):                             96
On-line CPU(s) list:                0-95
Thread(s) per core:                 2
Core(s) per socket:                 24
Socket(s):                          2
NUMA node(s):                       2
Vendor ID:                          GenuineIntel
CPU family:                         6
Model:                              85
Model name:                         Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz
Stepping:                           4
CPU MHz:                            1000.009
BogoMIPS:                           5000.00
Virtualization:                     VT-x
L1d cache:                          1.5 MiB
L1i cache:                          1.5 MiB
L2 cache:                           48 MiB
L3 cache:                           66 MiB
NUMA node0 CPU(s):                  0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46
                                    ,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90
                                    ,92,94
NUMA node1 CPU(s):                  1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47
                                    ,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91
                                    ,93,95
Vulnerability Gather data sampling: Mitigation; Microcode
Vulnerability Itlb multihit:        KVM: Mitigation: Split huge pages
Vulnerability L1tf:                 Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vuln
                                    erable
Vulnerability Mds:                  Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Meltdown:             Mitigation; PTI
Vulnerability Mmio stale data:      Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Retbleed:             Mitigation; IBRS
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccom
                                    p
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitizati
                                    on
Vulnerability Spectre v2:           Mitigation; IBRS; IBPB conditional; STIBP conditional; RSB filling
                                    ; PBRSB-eIBRS Not affected; BHI Not affected
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Mitigation; Clear CPU buffers; SMT vulnerable
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat 
                                    pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx p
                                    dpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good n
                                    opl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 mo
                                    nitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dc
                                    a sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave a
                                    vx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb cat_l3 cd
                                    p_l3 invpcid_single pti intel_ppin ssbd mba ibrs ibpb stibp tpr_sh
                                    adow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 hl
                                    e avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq r
                                    dseed adx smap clflushopt clwb intel_pt avx512cd avx512bw avx512vl
                                     xsaveopt xsavec xgetbv1 xsaves cqm_llc cqm_occup_llc cqm_mbm_tota
                                    l cqm_mbm_local dtherm ida arat pln pts pku ospke md_clear flush_l
                                    1d arch_capabilities
1d [ubuntu@mgc-dev2-3090:~/cuong_dn/context-handling-bigmodule_PikaRobot_25112025] main(+11/-8,+6/-1)* ± 
```



