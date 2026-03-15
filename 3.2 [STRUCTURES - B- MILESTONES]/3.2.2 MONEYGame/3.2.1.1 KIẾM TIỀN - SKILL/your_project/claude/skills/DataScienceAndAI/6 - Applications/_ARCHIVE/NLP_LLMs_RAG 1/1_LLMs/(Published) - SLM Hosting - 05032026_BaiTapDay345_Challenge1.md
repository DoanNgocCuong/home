---
title: "BÀI TẬP DAY 3+4+5 Tuần 1 - CHALLENGE 1 - ACTION to Fresher AI Engineer: vLLM HOSTING + API Wrapper — Deploy SLM, LLM lên Production"
description: "Content for Day 34."
pubDate: "2026-03-04"
tags: ["challenge-1"]
---
# 🚀 BÀI TẬP DAY 3+4+5 - Tuần 1 - CHALLENGE 1 - ACTION to Fresher AI Engineer: vLLM HOSTING — Deploy SLM lên Production

## **Deadline nộp:** **Thứ 6, 11:59PM** (Thời gian làm: thứ 5, thứ 6) — Ace nộp bài dưới bài đăng nhé

---

## 1. Tầm quan trọng

- Bài tập buổi 1+2 ace đã biết viết API + đóng gói Docker. Đây là các kiến thức, kĩ năng căn bản nhất của 1 Engineer.
- Bài tập buổi 3+4. Giờ mình đi tiếp đến kỹ năng căn bản nhất của 1 AI Engineer là làm việc với models.
  Gồm có:
  +, Biết cách kéo 1 models có sẵn về để deploy.
  +, Tự training, finetune 1 models => Sau đó deploy.
  +, Level cao hơn: Build 1 workflow, luồng tự động/bán tự động cho việc: Loop (Lấy log sau 1 thời gian chạy -> Gán nhãn tiếp -> Lấy data đó để tiếp tục cải thiện model -> Chạy đánh giá -> Duyệt lên Production hay không -> Lên Production -> Lại thu log ... Level này chúng ta có thể gọi nó với cái tên: Continuous Training

> Continuous Training (CT) là quá trình tự động retrain và cập nhật ML models liên tục dựa trên dữ liệu mới trong production, đảm bảo model luôn chính xác và thích ứng với thay đổi

```bash
┌─────────────────────────────────────────────────────────────────┐
│                    CLOSED-LOOP CT PIPELINE                       │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ 1. DATA  │───▶│ 2. TRAIN │───▶│ 3. EVAL  │───▶│4. DECIDE │  │
│  │ COLLECT  │    │          │    │          │    │ PROMOTE? │  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│       ▲                                               │         │
│       │           ┌──────────┐    ┌──────────┐        │         │
│       │           │ 6. MON   │◀───│ 5. DEPLOY│◀───────┘         │
│       │           │ ITOR     │    │ (canary) │   YES             │
│       └───────────┴──────────┘    └──────────┘                  │
│            feedback loop                                         │
└─────────────────────────────────────────────────────────────────┘
```

Ace có thể đọc thêm về Continuous Training Pipeline mình sẽ publish sau 1-2 tuần nữa.
Ở bài tập 3+4 này mình muốn ace host được model lên Production đã.

---

- Sự khác biệt giữa `API Engineer` với `AI Engineer` nằm ở khả năng: triển khai và vận hành 1 hệ thống AI khép kín. Ở bài tập này, mình sẽ cùng ace rèn luyện kỹ năng này.

---

## 2. Sai Lầm Phổ Biến và Kiến thức nền tảng — Bảng Chi Tiết

| **#**    | **Sai lầm**                                                             | **Ví dụ sai**                                                                                           | **Hậu quả thực tế**                                                                                                                                                                                                                                                                                  | **Cách sửa đúng**                                                                                                                                                                                                                     | **Dẫn chứng**                                                                 |
| -------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **1** 🟢 | **Download model trong Dockerfile**                                      | `Dockerfile: RUN python -c "AutoModel.from_pretrained('Qwen/Qwen2.5-1.5B-Instruct')"`                         | Mỗi `docker build` mất 5-15 phút download 3GB. CICD timeout. Container restart → download lại từ đầu. HuggingFace down → service không start.                                                                                                                                                      | Mount model từ host:`-v ./models:/models`. Dùng `./scripts/download_model.sh` để download 1 lần bên ngoài. vLLM trỏ `--model /models/Qwen2.5-1.5B`.                                                                               | [vLLM Offline Mode](https://docs.vllm.ai/en/latest/serving/offline_inference.html)       |
| **2** 🟢 | **Expose vLLM port thẳng ra ngoài, không reverse proxy**              | `docker run -p 8000:8000 vllm/vllm-openai ...` + mở firewall 8000                                            | Bất kỳ ai biết IP đều gọi API được. 1 user spam → GPU 100% → toàn bộ user khác timeout. Không rate limit, không access log.                                                                                                                                                                    | vLLM chỉ listen `127.0.0.1:8000` internal. Nginx đứng trước làm reverse proxy + rate limit + log.                                                                                                                                       | [vLLM + Nginx](https://docs.vllm.ai/en/latest/deployment/nginx.html)                     |
| **3** 🟢 | **Không set `--max-model-len` — default 32K**                        | `vllm serve Qwen/Qwen2.5-1.5B-Instruct` (không có `--max-model-len`)                                      | vLLM allocate KV cache cho 32K tokens → cần 6-8GB VRAM riêng cache. GPU 8GB → OOM ngay lúc start. GPU 16GB chạy nhưng throughput thấp.                                                                                                                                                                 | Set `--max-model-len 2048` hoặc 4096 tùy use case. 99% chat request không cần 32K context. Giảm KV cache → nhiều concurrent request hơn.                                                                                              | [vLLM Engine Args](https://docs.vllm.ai/en/latest/serving/engine_args.html)              |
| **4** 🟡 | **`--dtype auto` trên GPU yếu / không dùng quantization**          | `vllm serve --dtype auto` trên GPU 4-6GB VRAM                                                                | Model float16 ~3GB + KV cache overhead → hết VRAM hoặc OOM. Inference chậm vì GPU phải swap memory.                                                                                                                                                                                                      | Dùng model AWQ sẵn:`Qwen/Qwen2.5-1.5B-Instruct-AWQ` + `--dtype half --quantization awq`. Giảm 60% VRAM. Trên GPU yếu, đây là bắt buộc.                                                                                            | [vLLM Quantization](https://docs.vllm.ai/en/latest/quantization/supported_hardware.html) |
| **5** 🟡 | **Health check không check model loaded — chỉ check container alive** | `GET /health → {"status": "ok"}` cứng không check gì                                                      | Model warm-up mất 30-60s. Load balancer thấy healthy → route traffic vào → user nhận 503. Docker Compose `depends_on` không đủ, api start trong khi vLLM vẫn đang load model.                                                                                                                     | vLLM có sẵn `/health` chỉ return 200 khi model loaded xong. Docker Compose: `healthcheck: curl http://vllm:8000/health`. FastAPI wrapper forward `/health` từ vLLM xuống.  [last9](https://last9.io/blog/docker-compose-health-checks/) | [vLLM Health](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)      |
| **6** 🟡 | **Sync endpoint block thread khi gọi vLLM**                             | `def chat(): response = requests.post("http://vllm:8000/...")`                                                | FastAPI chạy sync endpoint trong threadpool (mặc định 40 threads). Mỗi LLM request 2-10s → 40 concurrent request → hết thread → request thứ 41 queue/timeout. 100 CCU → service đứng hình.                                                                                                       | `async def chat()` + `httpx.AsyncClient` hoặc `AsyncOpenAI`. Async không block thread → handle hàng trăm concurrent request với cùng tài nguyên.  [dev](https://dev.to/igorbenav/fastapi-mistakes-that-kill-your-performance-2b8k)  | [FastAPI Async](https://fastapi.tiangolo.com/async/)                                     |
| **7** 🔴 | **Không set `--gpu-memory-utilization` — default 0.9 (90%)**         | Không config → vLLM chiếm 90% GPU                                                                            | Máy chạy thêm process khác (monitoring, training) → OOM, driver crash. Không có headroom cho peak load. GPU 4GB: model 1.5B weights ~1.9GB + 90% KV cache → hết sạch.[github](https://github.com/vllm-project/vllm/issues/1298)                                                                         | Set `--gpu-memory-utilization 0.7` hoặc 0.8. Để 10-20% headroom cho OS + peak. Monitor `nvidia-smi` → tune theo thực tế workload.                                                                                                     | [vLLM GPU Memory](https://docs.vllm.ai/en/latest/serving/engine_args.html)               |
| **8** 🔴 | **Không set timeout client-side + không giới hạn `max_tokens`**    | `await client.chat.completions.create(model="qwen", messages=msgs)` không `timeout`, không `max_tokens` | User gửi prompt dài, model generate không giới hạn → 1 request chiếm vLLM 30-60s. Các request sau queue hết. 1 request "đen" → cascade timeout toàn service.[stackoverflow](https://stackoverflow.com/questions/78473182/vllm-fastapi-async-streaming-response-fastapi-cant-handle-vllm-speed-and-bo) | Client:`httpx.AsyncClient(timeout=30.0)`. Request body: `max_tokens=512`. Mọi request đều có upper bound thời gian — không có request nào treo vô thời hạn.                                                                     | [OpenAI Timeout](https://platform.openai.com/docs/api-reference)                         |

---

> - 🟢 **Lỗi setup** (mắc trước khi run): #1 Download model, #2 Expose port, #3 max-model-len
> - 🟡 **Lỗi config** (mắc khi test): #4 Quantization, #5 Health check, #6 Sync vs Async
> - 🔴 **Lỗi production** (chỉ thấy khi có load thật): #7 GPU utilization, #8 Timeout

---

### vLLM — Inference Engine #1 cho LLM/SLM

**Tại sao quan trọng?**
Khi ae fine-tune xong một model hoặc muốn self-host model thay vì gọi API OpenAI, ae cần một inference engine. vLLM là lựa chọn phổ biến nhất hiện tại trong production vì 3 lý do: **PagedAttention** giúp quản lý GPU memory hiệu quả hơn hẳn so với naive inference, **continuous batching** gom nhiều request vào batch tự động → throughput cao gấp 2-4x, và **OpenAI-compatible API** — ae đổi URL từ `api.openai.com` sang `localhost:8000` là xong, client code gần như không đổi.

---

## 3. HƯỚNG DẪN LÀM BÀI TẬP

### 3.1 Có được dùng AI không?

Ace có thể dùng AI để hoàn thành bài tập. Nhưng video trình bày cần trình bày được để cho 1 người nghe có thể hiểu ace đang làm gì và làm như thế nào 1 cách tổng quát.

### 3.2 Gợi ý models:

- Mn có thể thực hành với: Model Qwen 2.5-1.5B cho bài tập này.
- Cụ thể:
  ```python
  Qwen/Qwen2.5-1.5B-Instruct-AWQ
  ```

Đây là model đang được sử dụng thực tế trên Production của team mình. Nó đủ nhỏ để chạy các tasks đơn giản, ví dụ task về phân loại intent:
Nó đáp ứng với response time siêu nhỏ 40-60ms với 100 CCU. Nó chạy đủ nhỏ với 1.5 GB VRAM - 4GB VRAM

#### Nếu ace không Có GPU

- **Cách 1 — Google Colab (Khuyến nghị):** Dùng Colab free/Pro, cài vLLM, chạy server trong notebook với `ngrok` tunnel ra public URL. Bài tập vẫn đầy đủ, chỉ khác là server chạy trên Colab thay vì local Docker.
- **Cách 2 — Ollama thay vLLM:** Ollama hỗ trợ CPU inference, cũng expose OpenAI-compatible API. `docker run -p 11434:11434 ollama/ollama` → `ollama pull qwen2.5:1.5b`. Chậm hơn vLLM trên GPU nhiều, nhưng đủ để học và demo. Bảng sai lầm vẫn áp dụng (trừ lỗi #3 và #7 liên quan GPU).
- **Cách 3 — llama.cpp server:** Build `llama-server` từ llama.cpp, load GGUF quantized model. Chạy CPU thuần. Nhẹ nhất trong 3 cách nhưng thiếu một số tính năng (continuous batching kém hơn).

> Dù chọn cách nào, ae vẫn phải hoàn thành đủ output bên dưới. Trong video demo, nói rõ ae dùng giải pháp nào và tại sao.

---

### 3.3 Hướng dẫn chi tiết

> **Lưu ý:** Không có hướng dẫn code chi tiết — các bạn tự implement, có thể sử dụng AI hoặc tham khảo tài liệu chính thức.

#### 3.3.1 CÁCH 1: Cách đơn giản nhất để serving với vLLM bằng 1 lệnh:

```bash
CUDA_VISIBLE_DEVICES=0 nohup python -m vllm.entrypoints.openai.api_server \
    --model 'Qwen/Qwen2.5-1.5B-Instruct-AWQ' \
    --host 0.0.0.0 \
    --port 3000 \
    --quantization awq \
    --dtype half \
    --gpu-memory-utilization 0.1 \
    --max-model-len 512 \
    --max-num-seqs 16 \
    --max-num-batched-tokens 512 \
    --enable-prefix-caching \
    --enable-chunked-prefill \
    --swap-space 4 \
    --trust-remote-code \
    --disable-log-requests > doanngoccuong_qwen2.5-1.5B-Instruct-AWQ_server.log 2>&1 &
```

Cách này: ✅ Hợp lệ, nhưng không phải best practice cho production => Chỉ chạy thử, dev, test. Bởi vì:

- không có restart khi crash, không có healthcheck/orchestration.
- Khi triển khai trên môi trường khác => Dễ xung đột: ependency, version Python/vLLM, ... (Docker ra đời vì để xử lý vấn đề này).
- Khó scale (thêm replica), khó deploy đồng bộ nhiều máy.

#### 3.3.2 Cách 2: Để triển khai chuẩn ace đóng Docker, Docker compose . Ví dụ: docker-compose-vllm.yml:

```
services:
  vllm-qwen:
    container_name: vllm-qwen
    image: vllm/vllm-openai:v0.6.6.post1
    runtime: nvidia
    ports:
      - "3000:3000"
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
    command: >
      --model Qwen/Qwen2.5-1.5B-Instruct-AWQ
      --host 0.0.0.0
      --port 3000
      --quantization awq
      --dtype half
      --gpu-memory-utilization 0.1
      --max-model-len 512
      --max-num-seqs 16
      --max-num-batched-tokens 512
      --enable-prefix-caching
      --enable-chunked-prefill
      --swap-space 4
      --trust-remote-code
      --disable-log-requests
    restart: always
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

Chạy:

```bash
docker compose -f docker-compose-vllm-only.yml up --build
```

```bash
docker compose -f docker-compose-vllm-only.yml up --build -d
```

Đây là cách triển khai chuẩn Production. Cùng so sánh cách này với cách 1 bên trên:

###### Bảng so sánh: Chạy vLLM trên host (Cách 1) vs Docker Compose (Cách 2)

| Tiêu chí                                | Cách 1: nohup trên host                                                                      | Cách 2: Docker / Docker Compose                                            |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Lệnh / Cấu hình**              | Một lệnh:`CUDA_VISIBLE_DEVICES=0 nohup python -m vllm.entrypoints.openai.api_server ... &` | File `docker-compose-vllm.yml` + `docker compose up -d`                 |
| **Restart khi crash**               | Không — process chết là hết, phải chạy tay lại                                         | Có —`restart: always` (hoặc tương đương) trong Compose            |
| **Healthcheck / orchestration**     | Không — không có cơ chế “ready” cho LB/scheduler                                       | Có — có thể thêm `healthcheck`; tương thích K8s/Docker Swarm      |
| **Isolation (dependency, version)** | Không — dùng chung Python/vLLM/CUDA trên máy, dễ đụng app khác                        | Có — mỗi container có image riêng, môi trường tách biệt           |
| **Scale (thêm replica)**           | Khó — SSH từng máy, cài đặt tay, chạy lệnh nohup từng nơi                           | Dễ — cùng image, chạy thêm container (hoặc pod) theo Compose/K8s      |
| **Deploy đồng bộ nhiều máy**   | Khó — dễ lệch version Python/vLLM, thiếu “build một lần chạy mọi nơi”              | Dễ — một image + một file Compose = môi trường giống nhau mọi máy |
| **Reproducible (dev = prod)**       | Khó — môi trường mỗi máy có thể khác nhau                                            | Tốt — cùng image + Compose → môi trường giống nhau                  |
| **Portable**                        | Phụ thuộc máy — phải cài Python, vLLM, CUDA đúng version từng host                    | Tốt — chỉ cần Docker + NVIDIA Container Toolkit trên mọi host         |
| **Kiểm soát tài nguyên**        | Khó — không có limit RAM/CPU chuẩn hóa                                                   | Có —`mem_limit`, `cpus`, `deploy.resources` trong Compose           |
| **Phù hợp**                       | Dev, test, demo, chạy thử nhanh                                                              | Production, staging, đồng bộ nhiều máy                                 |
| **Kết luận**                      | Hợp lệ nhưng**không** phải best practice cho production                             | **Chuẩn production** — restart, isolation, scale, deploy đồng bộ |

---

#### 3.3.3 Triển khai LLMs với API Wrapper:

Ace thử tư duy xem có vấn đề gì với cách triển khai bên trên.

1. Khi phía BE gửi cho ace 1 đoạn text loằng ngoằng và ace cần TIỀN XỬ LÝ trước khi đưa vào LLMs. Hoặc bên phía BE yêu cầu output trả ra theo 1 số format đặc biệt, ví dụ thêm kí tự `<green>` `<green>`, `<end>`, ... để support cho các tasks vụ đặc biệt.
   Hoặc chúng ta phải HẬU XỬ LÝ output của LLMs để mapping với 1 số thứ khác.
   (Ví dụ có 1 task vụ yêu cầu: Khi LLMs nhận được câu của user thì cần detect xem nó thuộc loại intent gì, sau đó mapping intent đó với 1 kho các biểu cảm, cảm xúc của nhân vật. Chẳng hạn:
   +, intent: happy => mapping với nhân vật: nhảy/múa/ca hát
   +, intent: sad => mapping với nhân vật: khóc, buồn, ...
   thì cách xử lý của bạn là gì ?
2. Khi sếp yêu cầu bạn báo cáo log và response time của model tự self host này.
   => Lúc đó bạn có 1 cách là có thể nhờ bên đang call đến LLMs của bạn để tracing, ghi log hộ.
   Mình cũng từng gặp vấn đề này. Tuy nhiên: Vấn đề lúc đó xảy ra là:
   +, Bên service BE call đến bên mình với P95 response time là 0.2 s trong khi lúc mình tự testing 100 CCU P99 có 0.1s mặc dù trong cùng 1 mạng.
   => Nhưng mình lúc đó lại không có log, cũng ko có tracing được để mà phản bác lại là service của mình ổn.
3. Hoặc công ty bạn là 1 công ty cung cấp dịch vụ API host sẵn => sếp yêu cầu bạn host 1 con SLM lên sau đó bán cho khách:

- Gói Free được 50 request/ngày, gói Pro được 5.000. Nếu để mọi người gọi thẳng vào vLLM — không ai bị chặn cả, gói Free dùng thoải mái không giới hạn, cuối tháng không biết mỗi khách hàng tốn bao nhiêu để ra hóa đơn. ?
  Bạn xử lý như nào ?

Từ 1, 2, và 3 => Nhu cầu là chúng ta sẽ sử dụng 1 API Wrapper để bọc vào LLMs của mình.
(Giống như việc chúng ta dựng 1 API mà bên trong là đang call đến API LLMs của OpenAI)
Ace hiểu đoạn này chứ.

##### Vậy API Wrapper là gì?

1. Hãy tưởng tượng vLLM là một đầu bếp giỏi — chỉ biết nấu ăn, không biết giao tiếp với khách, không biết thu tiền, không biết khách dị ứng gì. API Wrapper chính là người phục vụ đứng giữa — tiếp nhận yêu cầu của khách, kiểm tra xem khách có đặt bàn chưa, lọc yêu cầu không hợp lệ, rồi mới chuyển xuống bếp — và khi bếp trả món ra, người phục vụ còn trang trí, kiểm tra lại trước khi mang ra cho khách.
2. Nói kỹ thuật hơn: API Wrapper là một service trung gian đứng giữa client (người dùng / app) và vLLM (AI engine), chịu trách nhiệm toàn bộ business logic, bảo mật, observability — những thứ vLLM không làm và không nên làm.

```bash
| Việc cần làm                                   | vLLM làm được không? | Ai làm? |
| ---------------------------------------------- | -------------------- | ------- |
| Sinh text, inference model                     | ✅                    | vLLM    |
| Validate input đúng format                     | ❌                    | Wrapper |
| Xác thực API key, phân quyền                   | ❌                    | Wrapper |
| Kiểm tra quota / rate limit                    | ❌                    | Wrapper |
| Business logic (mapping emotion, RAG, filter…) | ❌                    | Wrapper |
| Log JSON: latency, token, user_id              | ❌                    | Wrapper |
| Health check sâu (vLLM có sống không?)         | ❌                    | Wrapper |
| Timeout & fallback khi vLLM chậm/down          | ❌                    | Wrapper |
```

```bash
Client (app / web / service khác)
        ↓  POST /v1/chat/completions
   ┌─────────────────────────────┐
   │      API Wrapper (FastAPI)  │  ← ae viết layer này
   │  validate → log → timeout  │
   │  business logic → health   │
   └─────────────────────────────┘
        ↓  proxy request
   ┌─────────────────────────────┐
   │     vLLM Server             │  ← Cách 2 đã làm
   │  Qwen 2.5-1.5B-AWQ         │
   └─────────────────────────────┘
```

Bài tập của ae là cần triển khai cái này:

Cấu trúc thư mục tham khảo:
####### Kiểu 1

```bash
slm-hosting-challenge1-weaction/                          # Tên repo tự đặt
├── app/                              # FastAPI wrapper code
│   ├── __init__.py
│   ├── main.py                       # FastAPI app + lifespan
│   ├── routers/
│   │   └── chat.py                   # Chat completion endpoint
│   ├── models/
│   │   └── schemas.py                # Request/Response models
│   └── services/
│       └── vllm_client.py            # Async client gọi vLLM
├── docker/
│   ├── Dockerfile                    # FastAPI wrapper image
│   └── docker-compose.yml            # Full stack: vLLM + API + Nginx
├── scripts/
│   └── download_model.sh             # Script download model 1 lần
├── utils/                            # Screenshot dẫn chứng
│   ├── 1-chat-completion.png         # POST /v1/chat/completions success
│   ├── 2-health-check.png            # GET /health khi model loaded
│   ├── 3-health-fail.png             # GET /health khi vLLM down
│   ├── 4-rate-limit.png              # Nginx trả 429 khi spam
│   ├── 5-structured-log.png          # JSON log output
│   └── 6-docker-compose-up.png       # docker-compose up healthy
├── requirements.txt
├── .dockerignore
├── .env.example                      # Template biến môi trường
├── README.md                         # Hướng dẫn setup nhanh
└── AVOIDANCE_TABLE.md                # Proof tránh ≥ 6/8 lỗi
```

####### Kiểu 2

```bash
🎯 FOLDER STRUCTURE CHUẨN CHO BÀI TẬP vLLM HOSTING
(FastAPI Wrapper + Docker + Nginx | Production-Ready | Fresher-Friendly)

slm-hosting-challenge1-weaction/                       # Repo name: slm-hosting-yourname
│
├── 📦 app/                                  ## FASTAPI WRAPPER (Core app)
│   ├── __init__.py
│   ├── main.py                             ## FastAPI(app) + lifespan (vllm_client startup)
│   │
│   ├── api/                                ## HTTP LAYER (Routes + Middleware)
│   │   ├── __init__.py
│   │   ├── dependencies.py                 ## Depends(get_vllm_client, logger)
│   │   └── v1/                            ## API VERSION v1 (future v2/)
│   │       ├── __init__.py
│   │       ├── router.py                  ## APIRouter("/v1").include_router(chat_router)
│   │       ├── endpoints/                 ## Feature endpoints
│   │       │   ├── __init__.py
│   │       │   ├── chat.py               ## POST /v1/chat/completions (async proxy)
│   │       │   └── health.py             ## GET /v1/health (deep vLLM check)
│   │       │                                ## GET /v1/models (proxy vLLM)
│   │       └── schemas/                   ## ✅ Pydantic API contracts (v1-specific)
│   │           ├── __init__.py
│   │           ├── base.py                ## BaseModel extensions
│   │           ├── chat.py                ## ChatCompletionRequest/Response
│   │           └── health.py              ## HealthResponse
│   │
│   ├── domains/                          ## BUSINESS LOGIC (Application layer)
│   │   ├── __init__.py
│   │   └── vllm_service.py                ## Proxy logic + emotion mapping + RAG prep
│   │
│   └── core/                             ## CROSS-CUTTING (Config + Utils)
│       ├── __init__.py
│       ├── config.py                      ## Pydantic Settings (VLLM_URL, LOG_LEVEL)
│       ├── logging.py                     ## Structured JSON logger (structlog)
│       └── exceptions.py                  ## Custom exceptions (VllmTimeoutError...)
│
├── 🛡️ nginx/                             ## REVERSE PROXY (Production edge)
│   └── nginx.conf                         ## proxy_pass api:8080 + rate_limit 10r/s
│
├── 🐳 docker/                            ## INFRA (Multi-container)
│   ├── Dockerfile                         ## FastAPI multi-stage build
│   ├── docker-compose.yml                 ## vllm + api + nginx (healthcheck chain)
│   └── .dockerignore                      ## Exclude .git, node_modules
│
├── 📋 scripts/                           ## ONE-TIME SETUP
│   └── download_model.sh                  ## huggingface-cli download → ./models/
│
├── docs/                                
│   ├── RUNBOOK.md                         ## Operational runbook, incident response, common issue, avoidance note
│   ├── screenshots/                       ## ✅ PROOF (AVOIDANCE_TABLE)
│   │   ├── 1-chat-success.png             ## curl POST /v1/chat/completions
│   │   ├── 2-health-ok.png                ## curl GET /v1/health (model_loaded: true)
│   │   ├── 3-health-fail.png              ## vLLM down → degraded
│   │   ├── 4-rate-limit.png               ## Nginx trả 429 khi spam
│   │   ├── 5-json-log.png                 ## docker logs → structured JSON
│   │   └── 6-compose-healthy.png          ## docker-compose up all green
│
├── 📄 requirements.txt                    ## Production deps (fastapi, httpx, pydantic...)
├── 📄 .env.example                        ## VLLM_URL=http://vllm:8000
├── 📄 README.md                           ## 1. ./scripts/download_model.sh
└── .gitignore                             ## __pycache__, .env, models/
```

---

## 4. Output Submission - Comment dưới bài đăng

### Output 1: Push Code GitHub Public + ĐẶT TÊN THEO FORMAT: "... - challenge1-weaction" để dễ nhận diện nhau + đầy đủ với README.md

+, docs/RUNBOOK.md Trong Repo ghi rõ các sai lầm đã tránh được

Ví dụ: github/DoanNgocCuong/fastapi_dockercompose_challenge1_weaction.git

### Output 2: Video Demo ~5 Phút (YouTube Video Publish)

##### Gợi ý:

Quay *Video trình bày** chi tiết, mục đích để chia sẻ với mọi người để người nghe bất kì có thể hiểu về dự án của bạn.
=> Giúp tập trình bày khi mn đi phỏng vấn, đi làm, báo cáo

1. Giới thiệu dự án:

- Mục đích của việc làm cái này? Có thể ứng dụng vào việc gì?
- Chọn model nào, tại sao chọn, hardware đang dùng (GPU hay CPU alternative)

2. Demo:

- Về mặt Product: Trình bày ứng dụng của dự án:
- Technical:
  +, `docker-compose up` → show logs vLLM loading model → health check pass
  +, Demo `curl POST /v1/chat/completions` — hỏi 1 câu tiếng Việt, show response
  +,  Trình bày được flow data'
  +, 2-3 config quan trọng nhất trong `docker-compose.yml` (max-model-len, gpu-memory-utilization, volume mount)

### Output 3: Review Vòng Tròn

Quy trình: **Người 1 review Người 2, Người 2 review Người 3, … người cuối review Người 1**.
Nhắc nhở thành viên chưa nộp

Nội dung comment cần kiểm tra:

1. Github đã đủ các yêu cầu
2. Video Youtube

### Output 4: Điền link báo cáo + Feedback

1. Điền báo cáo vào sheet: https://docs.google.com/spreadsheets/d/18RGv8EJW-A-2yWYV2y0-9oiWEXVt-r2GW1qTXJ_GF6k/edit?gid=22262218#gid=22262218
   Link Github và Video của đồng đội vào sheet.
2. Điền feedback:
   Ace điền giúp Cường form feedback này để Cường hỗ trợ ace tốt nhất nhé. Thanks: [https://forms.gle/pHYsYKELCFptRKN9A](https://forms.gle/pHYsYKELCFptRKN9A)

---

> Lời chúc: Thêm 1 dự án. Chúc mừng ace!
> Hoàn thành bài tập Day 4+5 là ae đã biết self-host LLM/SLM — kỹ năng mà nhiều `API Engineer` đi làm 1-2 năm vẫn chưa từng làm.