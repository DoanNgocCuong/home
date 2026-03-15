# Mô tả Logic Cơ Chế Fallback LLM

## Tổng quan

Cơ chế fallback được triển khai trong `BaseLLM.predict()` để đảm bảo hệ thống luôn có phản hồi ngay cả khi model chính gặp sự cố. Fallback tự động chuyển sang `gpt-4o-mini` (OpenAI) khi model chính timeout > 1.5s hoặc gặp lỗi.

---

## 1. Khởi tạo và Chuẩn bị

### 1.1. Constants

```python
FALLBACK_MODEL = "gpt-4o-mini"
FALLBACK_TIMEOUT = 4.0  # Timeout cho fallback model (giây)
FALLBACK_PARAMS = {
    "max_tokens": 1024,
    "temperature": 0.0,
    "top_p": 1,
    "model": "gpt-4o-mini",
    "stream": False
}
```

### 1.2. Truyền OpenAI Provider

- `RobotV2Service._process_with_ai()` lấy OpenAI provider từ `llm_manager`
- Truyền vào `process()` qua `fallback_llm` trong kwargs
- Flow: `_process_with_ai()` → `policies_workflow.process()` → `classify_intent()` → `classify_by_llm()` → `llm_base.predict()`

### 1.3. Kiểm tra điều kiện fallback

```python
fallback_llm = kwargs.get("fallback_llm")  # OpenAI provider từ llm_manager
can_fallback = fallback_llm is not None or provider_name == "openai"
```

**Logic:**

- Nếu có `fallback_llm` (OpenAI provider) → có thể fallback
- Nếu provider hiện tại là `"openai"` → có thể dùng `self` để fallback
- Nếu không → không thể fallback

---

## 2. Flow Xử Lý Chính

### 2.1. Bước 1: Gọi Model Chính với Timeout 1.5s

```python
main_task = asyncio.create_task(
    self.get_response(messages=messages, conversation_id=conversation_id, **params)
)

try:
    res = await asyncio.wait_for(main_task, timeout=1.5)
    # ✅ Success: Main model trả về trong 1.5s → return kết quả
except asyncio.TimeoutError:
    # ❌ Timeout: Main model chậm > 1.5s → vào nhánh fallback (2.2)
except Exception as e:
    # ❌ Error: Main model fail ngay (< 1.5s) → vào nhánh fallback (2.3)
```

---

### 2.2. Nhánh Timeout (> 1.5s)

**Trường hợp:** Model chính chậm, không trả về trong 1.5s

**Xử lý:**

1. Kiểm tra `can_fallback`:

   - Nếu `False` → trả về `INTENT_FALLBACK` ngay
   - Nếu `True` → tiếp tục
2. Tạo fallback task:

   ```python
   fallback_params = dict(FALLBACK_PARAMS)  # gpt-4o-mini params
   fallback_llm_instance = fallback_llm if fallback_llm is not None else self

   fallback_task = asyncio.create_task(
       fallback_llm_instance.get_response(
           messages=messages,
           conversation_id=conversation_id,
           **fallback_params
       )
   )
   ```
3. **Race Condition** - Chạy song song main_task và fallback_task:

   ```python
   done, pending = await asyncio.wait(
       {main_task, fallback_task},
       return_when=asyncio.FIRST_COMPLETED
   )
   ```

   - `done`: Task hoàn thành đầu tiên (có thể là main hoặc fallback)
   - `pending`: Task còn lại (vẫn đang chạy)
4. Xử lý kết quả:

   **A. Nếu main_task completed trước:**

   - Cancel main_task
   - Chờ fallback_task hoàn thành với timeout 4s
   - Nếu fallback_task thành công trong 4s → dùng kết quả
   - Nếu fallback_task timeout > 4s → trả về `INTENT_FALLBACK`
   - Nếu fallback_task fail (exception) → trả về `INTENT_FALLBACK`

   **B. Nếu fallback_task completed trước:**

   - Cancel main_task
   - Lấy result từ fallback_task
   - Nếu thành công → dùng kết quả
   - Nếu fail → trả về `INTENT_FALLBACK`

---

### 2.3. Nhánh Exception (Lỗi ngay, không phải timeout)

**Trường hợp:** Model chính gặp lỗi ngay (ví dụ: Invalid API Key, Network Error, ...)

**Xử lý:**

1. Kiểm tra `can_fallback`:

   - Nếu `False` → trả về `INTENT_FALLBACK` ngay
   - Nếu `True` → tiếp tục
2. Tạo và chờ fallback_task với timeout 4s:

   ```python
   fallback_task = asyncio.create_task(
       fallback_llm_instance.get_response(...)
   )

   try:
       res = await asyncio.wait_for(fallback_task, timeout=4.0)  # Chờ fallback với timeout 4s
   except asyncio.TimeoutError:
       # Fallback timeout > 4s → trả về INTENT_FALLBACK
   except Exception:
       # Cả main và fallback đều fail → trả về INTENT_FALLBACK
   ```
3. Không có race condition vì main_task đã fail ngay

---

## 3. Điểm Quan Trọng

### 3.1. Fallback Provider Selection

| Điều kiện                                              | Provider dùng cho fallback                 |
| --------------------------------------------------------- | ------------------------------------------- |
| `fallback_llm` có trong kwargs                         | Dùng `fallback_llm` (OpenAI provider)    |
| `fallback_llm` = None và `provider_name` = "openai"  | Dùng `self` (OpenAI provider hiện tại) |
| `fallback_llm` = None và `provider_name` != "openai" | Không thể fallback                        |

### 3.2. Model Fallback

- Luôn dùng model `gpt-4o-mini` cho fallback
- Params: `temperature=0.0`, `max_tokens=1024`, `top_p=1`, `stream=False`

### 3.3. Timeout

- **Main model timeout:** **1.5 giây**
  - Sau 1.5s, nếu main model chưa xong → kích hoạt fallback song song
- **Fallback model timeout:** **4 giây**
  - Khi chờ fallback_task hoàn thành, áp dụng timeout 4s
  - Nếu fallback không trả về trong 4s → trả về `INTENT_FALLBACK`
  - Đảm bảo hệ thống không chờ quá lâu nếu cả main và fallback đều chậm

### 3.4. Race Condition Logic

- Khi main timeout và fallback được kích hoạt, cả 2 chạy song song
- Task nào hoàn thành trước (main hoặc fallback) → dùng task đó
- Task còn lại sẽ bị cancel để tránh lãng phí tài nguyên

---

## 4. Flow Diagram

```
┌─────────────────────────────────────────┐
│  BaseLLM.predict()                      │
│                                         │
│  1. Tạo main_task với timeout 1.5s     │
│  2. Kiểm tra can_fallback               │
└─────────────┬───────────────────────────┘
              │
              ├─► Main thành công (< 1.5s)
              │   └─► Return result ✅
              │
              ├─► Main timeout (> 1.5s)
              │   ├─► can_fallback = False?
              │   │   └─► Return INTENT_FALLBACK ❌
              │   │
              │   └─► can_fallback = True?
              │       ├─► Tạo fallback_task (gpt-4o-mini)
              │       ├─► Race: main_task vs fallback_task
              │       │
              │       ├─► Main completed first?
              │       │   ├─► Cancel main
              │       │   └─► Chờ fallback (timeout 4s)
              │       │       ├─► Fallback thành công (< 4s) → return result ✅
              │       │       └─► Fallback timeout (> 4s) → return INTENT_FALLBACK ❌
              │       │
              │       └─► Fallback completed first?
              │           ├─► Cancel main
              │           └─► Return fallback result ✅
              │
              └─► Main exception (lỗi ngay)
                  ├─► can_fallback = False?
                  │   └─► Return INTENT_FALLBACK ❌
                  │
                  └─► can_fallback = True?
                      ├─► Tạo fallback_task
                      ├─► Chờ fallback_task (timeout 4s)
                      │
                      ├─► Fallback thành công (< 4s)?
                      │   └─► Return result ✅
                      │
                      ├─► Fallback timeout (> 4s)?
                      │   └─► Return INTENT_FALLBACK ❌
                      │
                      └─► Fallback exception (lỗi)?
                          └─► Return INTENT_FALLBACK ❌
```

---

## 5. Logging

Các log quan trọng để theo dõi fallback:

1. **Khởi tạo:**

   - `fallback_llm available | provider=openai` (nếu có fallback_llm)
   - `fallback_llm=None | can_fallback={bool}` (nếu không có)
2. **Main model:**

   - `Main model succeeded within timeout` (thành công)
   - `model chính đã lỗi, chuyển qua dùng model gpt-4o-mini` (timeout)
   - `Main model failed early, fallback to gpt-4o-mini` (exception)
3. **Fallback process:**

   - `Main task completed first, waiting for fallback task (timeout=4.0s)` (race: main trước, chờ fallback với timeout 4s)
   - `Main task failed early, waiting for fallback task (timeout=4.0s)` (exception: chờ fallback với timeout 4s)
   - `Fallback task completed first, using fallback result` (race: fallback trước)
   - `Fallback task succeeded` (fallback thành công trong thời gian timeout)
   - `Fallback task timeout after 4.0s` (fallback quá chậm, timeout sau 4s)
4. **Kết quả:**

   - `Predict: {result} | Provider: {provider} | Model: {model}`
   - ⚠️ **Lưu ý:** Provider/Model trong log này hiện tại vẫn hiển thị main model, chưa cập nhật khi dùng fallback

---

## 6. Ví dụ thực tế (từ log)

```
Time        Event
──────────────────────────────────────────────────────────
06:46:45,128 fallback_llm available | provider=openai
06:46:45,138 Start predict | Provider: groq | Model: openai/gpt-oss-20b
06:46:45,478 [GroqProvider] Error: Invalid API Key
06:46:45,543 Main model failed early, fallback to gpt-4o-mini
06:46:45,593 Main task failed early, waiting for fallback task
06:46:45,618 [BaseLLM] Messages log (gọi OpenAI API)
06:46:46,552 Fallback task succeeded
06:46:46,562 Predict: fallback | Provider: groq | Model: openai/gpt-oss-20b
```

**Phân tích:**

- Provider chính: Groq (model: gpt-oss-20b)
- Main fail: Invalid API Key (exception, không phải timeout)
- Fallback: Dùng OpenAI provider, model gpt-4o-mini
- Kết quả: OpenAI trả về intent "fallback" (đúng, vì user nói "tớ đồng ý" không liên quan câu hỏi)

---

## 7. Ưu điểm của cơ chế này

1. **Tự động:** Không cần can thiệp thủ công, tự động chuyển khi main model fail
2. **Nhanh:** Timeout 1.5s cho main model ngắn, đảm bảo phản hồi nhanh cho user
3. **Song song:** Khi timeout, main và fallback chạy đồng thời, task nào xong trước dùng trước
4. **Linh hoạt:** Hỗ trợ nhiều provider (groq, gemini, ...) vẫn có thể fallback sang OpenAI
5. **An toàn:** Luôn có fallback default (INTENT_FALLBACK) nếu cả 2 đều fail
6. **Giới hạn thời gian:** Timeout 4s cho fallback model tránh chờ quá lâu nếu cả main và fallback đều chậm

---

## 8. Hạn chế và cải thiện

### Hạn chế hiện tại:

1. **Logging:** Provider/Model trong log cuối không phản ánh đúng provider/model thực tế được dùng khi fallback

### Đề xuất cải thiện:

1. Track `used_provider` và `used_model` để log chính xác khi dùng fallback
   - Hiện tại: `Predict: fallback | Provider: groq | Model: openai/gpt-oss-20b`
   - Nên có: `Predict: fallback | Provider: openai | Model: gpt-4o-mini (fallback)`

### Đã được cải thiện:

- ✅ **Timeout fallback:** Đã thêm timeout 4s cho fallback model (trước đây không có timeout)