---


---
# LangChain 1.2 VẤN ĐỀ ĐỒNG BỘ, BẤT ĐỒNG BỘ khi call API LLMs trong luồng. làm LangGraph Studio dừng vì nó không cho phép đợi LangChain 1.2 API LangGraph chạy, nhưng langgraph dev thì không. Nguyên nhân do code có những chỗ đứng đợi, còn LangGraph Studio không cho phép điều đó.
Bug: API work, nhưng UI LangGraph Bug:

```
curl --location 'http://127.0.0.1:8000/api/v1/agents/runs/wait' \
--header 'Content-Type: application/json' \
--data '{
    "agent_id": "todo_single_agent",
    "payload": {
      "user_input": "kế hoạch 5 năm",
      "context": ""
    }
  }'
```

=> Đã fix = 

```langgraph
langgraph dev --allow-blocking
```

---

Not a Studio link bug. The runs fail because Studio blocks synchronous calls. Logs show “Blocking call to time.sleep” from prompt fetch and OpenRouter retries. Your API works because it runs without this blocker; Studio’s dev server forbids blocking calls on the event loop.

Fix options (pick one):

- Quick run

  - In studio terminal:
    - Windows PowerShell:
      ```powershell
      langgraph dev --allow-blocking
      ```
    - Or set env then run:
      ```powershell
      $env:BG_JOB_ISOLATED_LOOPS="true"; langgraph dev
      ```
- Proper fix (later)

  - Replace any `time.sleep`, `requests`, or other sync I/O in LLM/prompt code with async versions, or wrap sync work:
    - Use `await asyncio.sleep(...)`
    - Use `httpx.AsyncClient` instead of `requests`
    - Or `await asyncio.to_thread(sync_func, ...)` for truly sync libs

Why this explains the symptoms

- Studio: detects blocking and aborts the LLM calls → “All models failed”.
- API: no blocker → calls succeed.

Try `--allow-blocking` now; if it works, we can schedule async refactor next.


---



Đây là lỗi về **Event Loop Blocking** trong Python asyncio. Để tôi giải thích tại sao:

## Nguyên nhân gốc rễ:

### 1. **Event Loop Architecture**

```python
# LangGraph Studio chạy với strict async event loop
async def main():
    # Event loop đang chờ async operations
    await some_async_function()
    # Nếu có sync blocking call → FREEZE toàn bộ event loop
```

### 2. **Code gốc có Blocking Operations**

Trong chatbot code của bạn có các blocking calls:

```python
# BaseLLM hoặc tool code
import time
import requests  # Synchronous HTTP calls

# Blocking operations:
time.sleep(0.1)  # Block event loop
response = requests.post(url, data=payload)  # Synchronous HTTP
```

### 3. **Khác biệt giữa API vs Studio**

```
Normal API Server:
├── Không có strict event loop monitoring
├── Blocking calls → Just slow, nhưng vẫn work
└── time.sleep(0.1) → OK, chỉ delay response

LangGraph Studio:
├── Strict async event loop với monitoring  
├── Blocking calls → DetectedBlocking → ABORT
└── time.sleep(0.1) → "Blocking call detected" → Kill operation
```

## Tại sao Studio strict hơn:

### **Event Loop Protection**

```python
# Studio có built-in protection
def detect_blocking_operation():
    if is_blocking_call_on_event_loop():
        raise RuntimeError("Blocking call detected!")
        # → "All models failed"
```

### **Performance Guarantee**

* Studio cần đảm bảo UI responsive
* Một blocking call có thể freeze toàn bộ UI
* Better to fail fast than freeze

## Cụ thể trong code bạn:

### **Possible blocking locations:**

1. **OpenRouter retries:**

```python
# Có thể trong BaseLLM
for attempt in range(MAX_RETRIES):
    try:
        response = openai_client.chat.completions.create(...)
    except:
        time.sleep(0.1)  # ← BLOCKING!
```

2. **Tool processing:**

```python
# Tool interface
import requests
response = requests.post(tool_url, json=payload)  # ← BLOCKING!
```

3. **Redis/RabbitMQ clients:**

```python
# Sync Redis calls
redis_client.get(task_id)  # ← BLOCKING!
```

## Solutions:

### **Quick fix (đã dùng):**

```bash
langgraph dev --allow-blocking
# Hoặc
$env:BG_JOB_ISOLATED_LOOPS="true"; langgraph dev
```

### **Proper fix (nên làm sau):**

```python
# Thay vì:
time.sleep(0.1)
# Dùng:
await asyncio.sleep(0.1)

# Thay vì:
import requests
response = requests.post(url, json=data)
# Dùng:
import httpx
async with httpx.AsyncClient() as client:
    response = await client.post(url, json=data)

# Wrap sync operations:
await asyncio.to_thread(sync_function, args)
```

## Tại sao API work mà Studio không:

```
API Server Process:
├── Runs in normal Python environment
├── No event loop protection
├── Blocking calls slow down but complete
└── Returns successful response

Studio Dev Server:
├── Runs with asyncio event loop monitoring
├── Detects blocking calls immediately  
├── Kills operations to protect event loop
└── Returns "All models failed" fallback
```

## Event Loop Visualization:

```
Normal Flow:
async_task_1 → async_task_2 → async_task_3 → Complete

With Blocking:
async_task_1 → [BLOCKING CALL] → (UI FREEZE) → async_task_2
                     ↓
              Studio detects → ABORT → Fallback response
```

**Tóm lại:** Studio có protection mechanism chống blocking calls để đảm bảo UI không bị freeze. Code bạn có sync operations nên bị Studio kill, nhưng API server bình thường vẫn chạy được dù chậm hơn.

---


Để tôi giải thích đơn giản hơn:

## Tưởng tượng như nhà hàng:

**API Server = Nhà hàng bình thường:**

* Bếp trưởng nấu món → chờ nguyên liệu → nấu tiếp
* Nếu chờ lâu thì khách đợi, nhưng vẫn có món

**LangGraph Studio = Nhà hàng cao cấp:**

* Có quy định nghiêm: "Không được để khách chờ quá 1 giây"
* Nếu bếp trưởng đứng chờ → Quản lý la: "Thôi, hủy món này!"

## Vấn đề trong code:

**Code có những chỗ "đứng chờ":**

```python
time.sleep(0.1)  # Đứng chờ 0.1 giây
requests.post(url)  # Đứng chờ server trả lời
```

## Tại sao khác nhau:

**API Server:** "Ok, chờ 0.1 giây cũng được, tôi kiên nhẫn"

**Studio:** "Không! Phát hiện đang chờ → Hủy ngay lập tức!"

## Fix tạm thời:

```bash
langgraph dev --allow-blocking
```

= Nói với Studio: "Được rồi, cho phép chờ đợi"

## Fix đúng cách (sau này):

Thay vì "đứng chờ" → dùng "chờ thông minh":

```python
# Thay vì đứng chờ
time.sleep(0.1)

# Dùng chờ thông minh  
await asyncio.sleep(0.1)
```

**Tóm lại:** Studio nghiêm khắc hơn API về việc chờ đợi. Code bạn có chỗ "đứng chờ" nên Studio từ chối, còn API thì chấp nhận.

Bạn đúng, về mặt kết quả cuối cùng thì đều là chờ. Nhưng cách chờ khác nhau về mặt kỹ thuật:

## Chờ "đần":

```python
time.sleep(0.1)
```

* Toàn bộ chương trình dừng lại 0.1 giây
* Không thể làm gì khác trong thời gian này
* Giống như bạn đứng chờ thang máy và không thể làm gì

## Chờ "thông minh":

```python
await asyncio.sleep(0.1)
```

* Chỉ cái task này chờ 0.1 giây
* Chương trình có thể chạy các task khác trong lúc chờ
* Giống như bạn đặt hẹn giờ báo thức rồi làm việc khác

## Tại sao Studio quan tâm:

**Studio chạy nhiều thứ cùng lúc:**

* UI cần update liên tục
* Nhiều request từ user
* Background tasks

**Nếu dùng `time.sleep()`:**

* Toàn bộ Studio đóng băng
* UI không click được
* Các request khác phải chờ

**Nếu dùng `await asyncio.sleep()`:**

* Chỉ task đó chờ
* UI vẫn hoạt động bình thường
* Request khác vẫn xử lý được

Về bản chất thì đúng là đều chờ 0.1 giây, nhưng một cách chờ làm đóng băng hệ thống, một cách chờ không làm đóng băng. Studio không chịu được cách chờ đóng băng.