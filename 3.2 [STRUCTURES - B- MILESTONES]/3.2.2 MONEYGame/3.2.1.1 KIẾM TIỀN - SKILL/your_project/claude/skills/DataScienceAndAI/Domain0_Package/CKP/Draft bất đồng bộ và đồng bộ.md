# MECE Analysis: LLM Fallback Logic Cases

## Tổng quan

- **Entry Point**: `predict()` method
- **Main Timeout**: 1.5s
- **Fallback Timeout**: 4.0s (FALLBACK_TIMEOUT)
- **Fallback Model**: gpt-4o-mini

---

## Level 1: Initial Conditions

### Case 1.1: first_message và start_message được set

- **Condition**: `kwargs.get("first_message") is not None AND kwargs.get("start_message") not in [None, ""]`
- **Logic**:
  - Return `INTENT_FALLBACK` ngay lập tức
  - Không gọi LLM
- **Result**: `INTENT_FALLBACK`

### Case 1.2: Normal flow (không có first_message/start_message)

- **Condition**: Không thỏa Case 1.1
- **Logic**: Tiếp tục với main task
- **Next**: Level 2

---

## Level 2: Main Task Execution (< 1.5s)

### Case 2.1: Main task thành công trong 1.5s

- **Condition**: `await asyncio.wait_for(main_task, timeout=1.5)` thành công
- **Logic**:
  - Return kết quả từ main task
  - Không kích hoạt fallback
- **Result**: Main LLM response
- **Trace**: Có trace trong Langfuse (main LLM)

### Case 2.2: Main task timeout sau 1.5s

- **Condition**: `asyncio.TimeoutError` trong 1.5s
- **Alert**: Send HIGH alert về LLM timeout
- **Next**: Level 3 (Fallback Decision)

### Case 2.3: Main task fail ngay (exception không phải timeout)

- **Condition**: Exception khác `asyncio.TimeoutError` trong 1.5s
- **Next**: Level 3 (Fallback Decision)

---

## Level 3: Fallback Decision

### Case 3.1: Có thể fallback (can_fallback = True)

- **Condition**: `fallback_llm is not None OR provider_name == "openai"`
- **Sub-cases**: Level 4 (_run_fallback_parallel)

### Case 3.2: Không thể fallback (can_fallback = False)

- **Condition**: `fallback_llm is None AND provider_name != "openai"`
- **Logic**:
  - Đợi main task hoàn thành với timeout 4s
  - Nếu thành công → return main result
  - Nếu fail/timeout → return `INTENT_FALLBACK`
- **Result**: Main result hoặc `INTENT_FALLBACK`
- **Trace**: Có trace main LLM (nếu thành công)

---

## Level 4: Parallel Execution (_run_fallback_parallel)

**Context**: Cả main_task và fallback_task đang chạy song song
**Timeout tổng**: 4s (FALLBACK_TIMEOUT)

### Case 4.1: Cả 2 tasks timeout sau 4s

- **Condition**: `asyncio.wait_for(asyncio.wait(...), timeout=4.0)` timeout
- **Logic**:
  - Cancel cả 2 tasks
  - Send CRITICAL alert về cả 2 timeout
- **Result**: `INTENT_FALLBACK`
- **Trace**: Cả 2 đều có trace (nhưng timeout)

### Case 4.2: Có ít nhất 1 task hoàn thành trong 4s

- **Condition**: Có task trong `done` set
- **Next**: Level 5 (Task Completion Handling)

---

## Level 5: First Completed Task Handling

### Case 5.1: Task đầu tiên hoàn thành THÀNH CÔNG

- **Condition**: `await completed_task` thành công
- **Sub-cases**: Level 6 (Which task completed first)

### Case 5.2: Task đầu tiên hoàn thành NHƯNG FAIL

- **Condition**: `await completed_task` raise Exception
- **Logic**: Đợi task còn lại
- **Next**: Level 7 (Remaining Task Handling)

---

## Level 6: Which Task Completed First (Success Case)

### Case 6.1: Main task về trước (thành công)

- **Condition**: `completed_task == main_task AND res = await completed_task thành công`
- **Logic**:
  - Return main result
  - Cancel fallback_task
- **Result**: Main LLM response
- **Trace**:
  - Main LLM: Complete trace
  - Fallback LLM: Cancelled (có trace nhưng cancelled)

### Case 6.2: Fallback task về trước (thành công)

- **Condition**: `completed_task == fallback_task AND res = await completed_task thành công`
- **Logic**:
  - Return fallback result (dùng luôn)
  - Check main task status:
    - **Nếu main đã done (fail/success)**: Chỉ log, không đợi
    - **Nếu main chưa done (đang chạy)**: Đợi main với timeout 4s để trace
      - Nếu main timeout sau 4s → cancel main
      - Nếu main thành công trong 4s → giữ trace
      - Nếu main fail trong 4s → log nhưng đã có result
- **Result**: Fallback LLM response
- **Trace**:
  - Fallback LLM: Complete trace
  - Main LLM: Trace (nếu đang chạy thì đợi để trace, nếu đã fail/success thì chỉ log)

---

## Level 7: Remaining Task Handling (First Task Failed)

### Case 7.1: Remaining task là MAIN và thành công

- **Condition**:
  - First completed task failed
  - `remaining_task == main_task`
  - `await asyncio.wait_for(remaining_task, timeout=4.0)` thành công
- **Logic**:
  - Return main result
  - Cancel fallback_task
- **Result**: Main LLM response
- **Trace**:
  - Main LLM: Complete trace
  - Fallback LLM: Failed + Cancelled

### Case 7.2: Remaining task là FALLBACK và thành công

- **Condition**:
  - First completed task failed (main task đã fail trước đó)
  - `remaining_task == fallback_task`
  - `await asyncio.wait_for(remaining_task, timeout=4.0)` thành công
- **Logic**:
  - Return fallback result
  - Check main task status:
    - **Nếu main đã done (fail)**: Không đợi vì main đã fail rồi, không cần trace thêm
    - **Nếu main chưa done (đang chạy)**: Đợi main với timeout 4s để trace (tương tự Case 6.2)
- **Result**: Fallback LLM response
- **Trace**:
  - Fallback LLM: Complete trace
  - Main LLM: Trace (nếu đang chạy thì đợi để trace, nếu đã fail thì không đợi)

### Case 7.3: Remaining task cũng FAIL

- **Condition**: `await asyncio.wait_for(remaining_task, timeout=4.0)` raise Exception
- **Logic**:
  - Cancel cả 2 tasks
  - Send CRITICAL alert về cả 2 failed
- **Result**: `INTENT_FALLBACK`
- **Trace**: Cả 2 đều có trace (nhưng failed)

---

## Level 8: Top-level Exception Handling

### Case 8.1: asyncio.CancelledError (từ bên ngoài)

- **Condition**: Task bị cancel bởi caller (ví dụ: phoneme classifier đã return)
- **Logic**: Return `INTENT_FALLBACK`
- **Result**: `INTENT_FALLBACK`
- **Note**: Đây là behavior mong muốn, không phải error

### Case 8.2: Exception khác (unexpected)

- **Condition**: Exception không được catch ở các level trên
- **Logic**:
  - Log error
  - Return `INTENT_FALLBACK`
- **Result**: `INTENT_FALLBACK`

---

## Summary Table

| Case ID       | Condition                                | Result                  | Trace Status                             | Alerts    |
| ------------- | ---------------------------------------- | ----------------------- | ---------------------------------------- | --------- |
| 1.1           | first_message/start_message set          | INTENT_FALLBACK         | None                                     | None      |
| 2.1           | Main success < 1.5s                      | Main response           | Main only                                | None      |
| 2.2           | Main timeout 1.5s → can_fallback=False  | Main or INTENT_FALLBACK | Main (if success)                        | None      |
| 2.3           | Main fail early → can_fallback=False    | Main or INTENT_FALLBACK | Main (if success)                        | None      |
| 3.2 (timeout) | Main timeout + no fallback               | Main or INTENT_FALLBACK | Main (if success)                        | None      |
| 3.2 (fail)    | Main fail + no fallback                  | Main or INTENT_FALLBACK | Main (if success)                        | None      |
| 4.1           | Both timeout 4s                          | INTENT_FALLBACK         | Both (timeout)                           | CRITICAL  |
| 6.1           | Main first (success)                     | Main response           | Both (main complete, fallback cancelled) | None      |
| 6.2           | Fallback first (success)                 | Fallback response       | Both (fallback complete, main trace)     | None      |
| 7.1           | First failed, main remaining success     | Main response           | Both (main complete, fallback failed)    | None      |
| 7.2           | First failed, fallback remaining success | Fallback response       | Both (fallback complete, main trace)     | None      |
| 7.3           | Both failed                              | INTENT_FALLBACK         | Both (failed)                            | CRITICAL  |
| 8.1           | CancelledError                           | INTENT_FALLBACK         | None                                     | None      |
| 8.2           | Unexpected exception                     | INTENT_FALLBACK         | None                                     | Error log |

---

## Key Design Decisions

1. **Trace Preservation & Smart Wait Logic**: Khi fallback về trước, chỉ đợi main task nếu main chưa done (đang chạy).
   - Nếu main đã success: Không đợi vì main đã chạy xong và trace xong rồi
   - Nếu main đã fail: Không đợi vì đã fail rồi, không cần trace thêm
   - Nếu main chưa done (đang chạy): Đợi với timeout 4s để trace (có thể thành công hoặc timeout/fail)
2. **Resource Management**: Cancel tasks không cần thiết để tránh tốn resource
3. **Timeout Strategy**:
   - Main: 1.5s initial timeout
   - Parallel: 4s total timeout cho cả 2 tasks
   - Main trace wait: 4s khi fallback về trước (chỉ nếu main chưa done)
4. **Alert Strategy**:
   - HIGH: Main timeout (normal fallback trigger)
   - CRITICAL: Both timeout hoặc both failed
5. **No Metadata Logging**: Fallback LLM không log metadata thủ công (chỉ trace timing)


---




Giải thích lại:

## Vấn đề hiện tại (block luồng)

Flow hiện tại khi fallback về trước:

```
1. Fallback hoàn thành → có result ✅
2. Đợi main task (tối đa 4s) ⏳ ← BLOCK ở đây
3. Sau khi đợi xong → return result ❌
```

Vấn đề: Dù đã có result từ fallback, user vẫn phải chờ thêm 4s.

## Giải pháp (không block)

Flow mới khi fallback về trước:

```
1. Fallback hoàn thành → có result ✅
2. Return result ngay lập tức ✅ ← Không đợi
3. Đợi main task ở background (để trace) 🔄 ← Chạy ngầm, không block
```

Lợi ích: User nhận result ngay; main vẫn được trace ở background.

## So sánh code

Trước (block):

```python
res = await completed_task  # Lấy result từ fallback

if completed_task == fallback_task:
    await self._handle_fallback_completed_first(...)  # ⏳ Đợi 4s ở đây
  
return res  # Chỉ return sau khi đợi xong
```

Sau (không block):

```python
res = await completed_task  # Lấy result từ fallback

if completed_task == fallback_task:
    # Tạo task chạy ở background, không đợi
    asyncio.create_task(self._wait_for_main_task_with_timeout(...))
  
return res  # ✅ Return ngay lập tức
```

## Ví dụ thời gian

Trước:

- t=0s: Fallback về, có result
- t=0-4s: Đợi main
- t=4s: Return result → User nhận sau 4s

Sau:

- t=0s: Fallback về, có result
- t=0s: Return result ngay → User nhận ngay
- t=0-4s: Main trace chạy ở background (không block)

Bạn muốn tôi implement giải pháp này không?

---



 git commit -m "[Small Update: Trace main_llms khi main_llms bị timeout 1.5s]

>> ---
>>
>> Vấn đề là: Khi main timeout 1.5s chạy song song fallback llms là openAI, nhưng log langfuse chỉ hiển thị log của fallback llms
>>
>> ---
>>
>> Update:
>>
>> 1. Khi main timeout 1.5s thì bật song song con llms fallback.
>>
>> - Nếu main về trước, lấy main và huỷ fallback
>> - Nếu fallback về trước, vẫn đợi main chạy tiếp để ra kết quả với timeout 4s
>>   Nếu main đã success → đã trace xong, không cần đợi
>>   Nếu main đã fail → đã fail, không cần đợi
>>   Nếu main đang chạy → đợi với timeout 4s để trace
>>
>> 2. Timeout tổng của 2 con này là 4s
>> 3. Tắt capture_in, capture_out của cả 2 con này
>>
>> ---
>>
>> Đã đáp ứng đầy đủ các yêu cầu. Logic đợi main đã được tối ưu: chỉ đợi nếu main đang chạy (chưa done), không đợi nếu main đã done.
>>
>> ---
>>
>> Đợi main hoàn thành để trace (tối đa 4s) có block luồng ko?
>>




Đang triển khai giải pháp không block luồng:

[6 tools called]

Đang kiểm tra các chỗ khác gọi `_handle_fallback_completed_first`:

[2 tools called]

Đã hoàn tất. Tóm tắt thay đổi:

## Đã implement giải pháp không block luồng

### Thay đổi chính:

1. **`_handle_fallback_completed_first`**:

   - Đổi từ `async def` → `def` (không cần await)
   - Tạo background task với `asyncio.create_task()` để trace main
   - Return ngay, không block
2. **`_run_fallback_parallel`**:

   - Bỏ `await` trước `_handle_fallback_completed_first()`
   - Return result ngay sau khi fallback về trước

### Kết quả:

**Trước:**

```python
res = await fallback_task  # Có result
await _handle_fallback_completed_first(...)  # ⏳ Đợi 4s
return res  # Return sau 4s
```

**Sau:**

```python
res = await fallback_task  # Có result
_handle_fallback_completed_first(...)  # ✅ Tạo background task, không đợi
return res  # ✅ Return ngay lập tức
```

### Lợi ích:

- User nhận result ngay (không chờ thêm 4s)
- Main vẫn được trace ở background
- Không block luồng chính
- Performance tốt hơn

Không có linter errors. Code đã sẵn sàng.


---



Đang kiểm tra code hiện tại để xem những gì đã thay đổi:

[3 tools called]

Những thay đổi đã thực hiện:

## Những thay đổi đã thực hiện

### 1. **Method `_handle_fallback_completed_first`** (dòng 472-490)

**Trước:**

```python
async def _handle_fallback_completed_first(...):
    """Xử lý khi fallback về trước: đợi main task với timeout để trace"""
    logging.info(...)
    await self._wait_for_main_task_with_timeout(main_task, conversation_id, timeout)
    # ⚠️ Block ở đây - đợi main xong mới return
```

**Sau:**

```python
def _handle_fallback_completed_first(...):  # ✅ Đổi từ async def → def
    """Xử lý khi fallback về trước: đợi main task ở background để trace (không block response)"""
    logging.info(...)
  
    # ✅ Tạo nested async function để chạy ở background
    async def _trace_main_in_background():
        try:
            await self._wait_for_main_task_with_timeout(main_task, conversation_id, timeout)
        except Exception as e:
            logging.debug(...)  # Ignore errors trong background task
  
    # ✅ Fire-and-forget: Tạo task chạy ở background, không await
    asyncio.create_task(_trace_main_in_background())
    # ✅ Return ngay, không block
```

**Thay đổi:**

- `async def` → `def` (không cần await)
- Tạo nested function `_trace_main_in_background()`
- Dùng `asyncio.create_task()` để chạy ở background
- Không await → không block

### 2. **Method `_run_fallback_parallel`** (dòng 584-585)

**Trước:**

```python
if completed_task == fallback_task:
    await self._handle_fallback_completed_first(...)  # ⚠️ Đợi ở đây
return res  # Chỉ return sau khi đợi xong
```

**Sau:**

```python
if completed_task == fallback_task:
    # ✅ Không await - gọi function bình thường (không async)
    self._handle_fallback_completed_first(main_task, conversation_id, timeout)
    # ✅ Return ngay lập tức, không đợi background task
return res  # ✅ Return ngay
```

**Thay đổi:**

- Bỏ `await` trước `_handle_fallback_completed_first()`
- Thêm comment giải thích: "return ngay, trace main ở background (không block)"

## So sánh flow

### **Trước (Block):**

```
1. Fallback hoàn thành → res = "fallback_result" ✅
2. Gọi _handle_fallback_completed_first() 
3. Đợi _wait_for_main_task_with_timeout() (tối đa 4s) ⏳
4. Return res ❌ (sau 4s)
```

### **Sau (Non-block):**

```
1. Fallback hoàn thành → res = "fallback_result" ✅
2. Gọi _handle_fallback_completed_first()
   - Tạo background task với asyncio.create_task()
   - Return ngay (không đợi) ✅
3. Return res ✅ (ngay lập tức)
4. Background task chạy ngầm để trace main 🔄 (không block response)
```

## Tác động

- Performance: User nhận result ngay, không chờ thêm 4s
- Functionality: Main vẫn được trace ở background
- Code: Giữ logic trace, chỉ đổi cách chạy (background thay vì blocking)

Đây là các thay đổi chính đã thực hiện.


---



```python
"""
Lớp BaseLLM - Quản lý tương tác với các mô hình ngôn ngữ lớn (LLM)

Mô tả:
    Lớp này cung cấp giao diện thống nhất để tương tác với các nhà cung cấp LLM khác nhau,
    bao gồm OpenAI và Google Gemini. Nó xử lý việc gửi tin nhắn, nhận phản hồi,
    và quản lý các lỗi timeout và retry.

Tính năng chính:
    - Hỗ trợ nhiều nhà cung cấp LLM (OpenAI, Gemini)
    - Xử lý timeout và retry tự động
    - Chuyển đổi định dạng tin nhắn cho từng nhà cung cấp
    - Logging chi tiết cho việc debug
    - Xử lý lỗi và fallback

Các biến môi trường:
    INTENT_FALLBACK: Giá trị fallback khi không thể phân loại intent
    TIMEOUT: Thời gian timeout cho mỗi request (mặc định: 5 giây)
    MAX_RETRIES: Số lần thử lại tối đa (mặc định: 3 lần)

Ví dụ sử dụng:
    # Khởi tạo với OpenAI
    openai_llm = BaseLLM(
        provider_setting={"api_key": "your_key", "base_url": "https://api.openai.com/v1"},
        provider_name="openai"
    )
  
    # Khởi tạo với Gemini
    gemini_llm = BaseLLM(
        provider_setting={"api_key": "your_gemini_key"},
        provider_name="gemini"
    )
  
    # Gửi tin nhắn
    response = await llm.predict(
        messages=[{"role": "user", "content": "Xin chào"}],
        params={"model": "gpt-4", "temperature": 0.7}
    )
"""

from typing import List, Optional
import traceback
import logging
import asyncio
import time
import os
import json
import re

# This client is already initialized in app/common/langfuse/__init__.py at module level
# which is more efficient than creating a new client each time
# from app.common.langfuse import langfuse_client

# Now import observe - it will use the client from __init__.py
from langfuse import observe, Langfuse
langfuse_client = Langfuse()

from ..providers.llm_providers import OpenAIProvider, GeminiProvider, GroqProvider
from ..utils.helpers import MessageConverter, JsonParser

# Import alert system
try:
    # Try absolute import first
    from app.common.alerts import AlertType, AlertLevel
    from app.common.alerts.helpers.send_alert_safe import send_alert_safe
    ALERT_ENABLED = True
except ImportError:
    # If failed, try relative import hoặc disable
    try:
        import sys
        from pathlib import Path
        # Add root to path
        root_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent
        if str(root_path) not in sys.path:
            sys.path.insert(0, str(root_path))
        from app.common.alerts import AlertType, AlertLevel
        from app.common.alerts.helpers.send_alert_safe import send_alert_safe
        ALERT_ENABLED = True
    except ImportError as e:
        logging.warning(f"[BaseLLM] Alert system not available: {e}")
        ALERT_ENABLED = False
        # Dummy functions để tránh error
        def send_alert_safe(*args, **kwargs):
            pass
        AlertType = type('AlertType', (), {'LLM_TIMEOUT': 'llm_timeout', 'LLM_BOTH_FAILED': 'llm_both_failed', 'LLM_RATE_LIMIT': 'llm_rate_limit', 'LLM_PROVIDER_DOWN': 'llm_provider_down'})
        AlertLevel = type('AlertLevel', (), {'HIGH': 'high', 'CRITICAL': 'critical'})

# Constants
INTENT_FALLBACK = os.getenv("INTENT_FALLBACK")
TIMEOUT = 5
MAX_RETRIES = 3
FALLBACK_MODEL = "gpt-4o-mini"
FALLBACK_TIMEOUT = 4.0  # Timeout cho fallback model (giây)
FALLBACK_PARAMS = {
  "max_tokens": 1024,
  "temperature": 0.0,
  "top_p": 1,
  "model": "gpt-4o-mini",
  "stream": False
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

class BaseLLM:
    """
    Lớp cơ sở để tương tác với các mô hình ngôn ngữ lớn (LLM)
  
    Lớp này cung cấp giao diện thống nhất để làm việc với các nhà cung cấp LLM khác nhau,
    xử lý việc chuyển đổi định dạng tin nhắn, quản lý timeout, retry và logging.
    """

    def __init__(self, provider_setting: dict, provider_name: str = None, **kwargs):
        """
        Khởi tạo đối tượng BaseLLM
    
        Args:
            provider_setting (dict): Cấu hình kết nối đến nhà cung cấp LLM
                - api_key (str): API key để xác thực
                - base_url (str): URL endpoint của API (cho OpenAI)
            provider_name (str, optional): Tên nhà cung cấp ('openai', 'gemini', etc.)
            **kwargs: Các tham số bổ sung
        
        Ví dụ:
            # Cấu hình OpenAI
            openai_llm = BaseLLM(
                provider_setting={
                    "api_key": "sk-...",
                    "base_url": "https://api.openai.com/v1"
                },
                provider_name="openai"
            )
        
            # Cấu hình Gemini
            gemini_llm = BaseLLM(
                provider_setting={"api_key": "AIza..."},
                provider_name="gemini"
            )
        """
        self.provider_setting = provider_setting
        self.provider_name = provider_name
    
        logging.info(f"[BaseLLM.__init__] Initializing BaseLLM with provider_name={provider_name}, provider_setting_keys={list(provider_setting.keys()) if isinstance(provider_setting, dict) else 'not_dict'}")
    
        # Initialize providers - only initialize the one we need (lazy initialization)
        self.openai_provider = None
        self.gemini_provider = None
        self.groq_provider = None
    
        # Initialize the provider based on provider_name
        if provider_name == 'openai':
            self.openai_provider = OpenAIProvider(provider_setting)
            logging.info(f"[BaseLLM.__init__] Successfully initialized OpenAIProvider")
        elif provider_name == 'gemini':
            self.gemini_provider = GeminiProvider(provider_setting)
            logging.info(f"[BaseLLM.__init__] Successfully initialized GeminiProvider")
        elif provider_name == 'groq':
            self.groq_provider = GroqProvider(provider_setting)
            logging.info(f"[BaseLLM.__init__] Successfully initialized GroqProvider")
        else:
            logging.warning(f"[BaseLLM.__init__] Unknown provider_name={provider_name}, no provider initialized")
        # Note: We don't initialize all providers to avoid validation errors
        # when provider_setting doesn't match the provider
    
        # Initialize utilities
        self.message_converter = MessageConverter()
        self.json_parser = JsonParser()

    async def get_response(self, messages: List, conversation_id: str = None, **params):
        """
        Gửi tin nhắn đến LLM và nhận phản hồi với cơ chế retry và timeout
        """
        logging.info(f"[BaseLLM]============= {str(conversation_id)} -messages: {json.dumps(messages, indent=4, ensure_ascii=False)}")
        start_time = time.time()
    
        for attempt in range(MAX_RETRIES):
            try:
                if self.provider_name == 'gemini':
                    return await self.gemini_provider.get_response(
                        messages, conversation_id, start_time, **params
                    )
                elif self.provider_name == 'groq':
                    return await self.groq_provider.get_response(
                        messages, conversation_id, start_time, **params
                    )
                elif self.provider_name == 'openai':
                    return await self.openai_provider.get_response(
                        messages, conversation_id, start_time, **params
                    )
                else:
                    raise ValueError(f"Provider name {self.provider_name} not supported")
                
            except asyncio.TimeoutError:
                logging.info(f"[BaseLLM] {str(conversation_id)} - Timeout occurred on attempt {attempt + 1}/{MAX_RETRIES}")
                if attempt == MAX_RETRIES - 1:
                    logging.info(f"[BaseLLM] {str(conversation_id)} - All {MAX_RETRIES} attempts failed due to timeout")
                await asyncio.sleep(0.1)
        
            except Exception as e:
                # Check for rate limit errors (HTTP 429)
                error_str = str(e).lower()
                error_str_full = str(e)  # Keep original case for status code extraction
                status_code = None
            
                # Try to extract status code from OpenAI/Groq errors
                # Method 1: Check if error has status_code attribute
                if hasattr(e, 'status_code'):
                    status_code = e.status_code
                # Method 2: Check response object
                elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                    status_code = e.response.status_code
                # Method 3: Extract from error message (e.g., "Error code: 401")
                elif 'error code:' in error_str_full.lower():
                    match = re.search(r'error code:\s*(\d+)', error_str_full, re.IGNORECASE)
                    if match:
                        status_code = int(match.group(1))
                # Method 4: Check error string patterns
                elif '429' in error_str or 'rate limit' in error_str:
                    status_code = 429
                elif '401' in error_str or 'invalid_api_key' in error_str or 'authentication' in error_str:
                    status_code = 401
                elif '403' in error_str or 'forbidden' in error_str:
                    status_code = 403
                elif '500' in error_str or '502' in error_str or '503' in error_str or '504' in error_str:
                    # Server errors
                    if '500' in error_str:
                        status_code = 500
                    elif '502' in error_str:
                        status_code = 502
                    elif '503' in error_str:
                        status_code = 503
                    elif '504' in error_str:
                        status_code = 504
            
                model_name = params.get("model", "unknown")
                provider_name = self.provider_name or "unknown"
            
                # Send alert for rate limit
                if status_code == 429 or 'rate limit' in error_str:
                    logging.warning(f"[BaseLLM] {conversation_id} - Rate limit detected: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_RATE_LIMIT,
                            level=AlertLevel.HIGH,
                            message="LLM rate limit detected. Switching to fallback.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "attempt": attempt + 1,
                                "max_retries": MAX_RETRIES,
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle (switch to fallback)
                    raise
            
                # Send alert for invalid API key (specific case)
                if status_code == 401 and ('invalid_api_key' in error_str or 'api key' in error_str):
                    logging.warning(f"[BaseLLM] {conversation_id} - Invalid API key detected: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_INVALID_API_KEY,
                            level=AlertLevel.CRITICAL,
                            message="LLM invalid API key detected.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle (switch to fallback)
                    raise
            
                # Send alert for authentication errors (401, 403)
                if status_code in [401, 403] or 'authentication' in error_str or 'forbidden' in error_str:
                    logging.warning(f"[BaseLLM] {conversation_id} - Authentication/Authorization error detected: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_PROVIDER_DOWN,
                            level=AlertLevel.HIGH,
                            message="LLM authentication/authorization error. Switching to fallback.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "status_code": status_code or "unknown",
                                "error_type": "authentication_error",
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle (switch to fallback)
                    raise
            
                # Check for token limit exceeded
                if 'token' in error_str and ('limit' in error_str or 'exceeded' in error_str or 'too many' in error_str):
                    logging.warning(f"[BaseLLM] {conversation_id} - Token limit exceeded: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_TOKEN_LIMIT_EXCEEDED,
                            level=AlertLevel.MEDIUM,
                            message="LLM token limit exceeded.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle
                    raise
            
                # Check for context overflow
                if 'context' in error_str and ('overflow' in error_str or 'too long' in error_str or 'exceeded' in error_str):
                    logging.warning(f"[BaseLLM] {conversation_id} - Context overflow detected: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_CONTEXT_OVERFLOW,
                            level=AlertLevel.MEDIUM,
                            message="LLM context window overflow.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle
                    raise
            
                # Send alert for server errors (5xx)
                if status_code in [500, 502, 503, 504]:
                    logging.warning(f"[BaseLLM] {conversation_id} - LLM provider server error detected: {e}")
                
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_PROVIDER_DOWN,
                            level=AlertLevel.HIGH,
                            message=f"LLM provider server error ({status_code}). Switching to fallback.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "status_code": status_code,
                                "error_type": "server_error",
                                "error": str(e)[:500]
                            },
                            component="base_llm"
                        )
                
                    # Re-raise để caller có thể handle (switch to fallback)
                    raise
            
                # Re-raise other errors
                raise

    # ==================== Helper Methods for Fallback Logic ====================
  
    async def _cancel_task_safe(self, task: asyncio.Task, task_name: str = "task") -> None:
        """Cancel task một cách an toàn, bỏ qua exceptions"""
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logging.debug(f"[BaseLLM] {task_name} cancelled successfully")
            except Exception:
                pass  # Ignore other errors when cancelling
  
    async def _cancel_both_tasks(self, main_task: asyncio.Task, fallback_task: asyncio.Task) -> None:
        """Cancel cả 2 tasks một cách an toàn"""
        await asyncio.gather(
            self._cancel_task_safe(main_task, "main_task"),
            self._cancel_task_safe(fallback_task, "fallback_task"),
            return_exceptions=True
        )
  
    def _send_both_timeout_alert(self, conversation_id: str, provider_name: str, model_name: str, timeout: float) -> None:
        """Send alert khi cả 2 LLM đều timeout"""
        if ALERT_ENABLED:
            send_alert_safe(
                alert_type=AlertType.LLM_TIMEOUT,
                level=AlertLevel.CRITICAL,
                message=f"Both main and fallback LLM timeout after {timeout}s. Using INTENT_FALLBACK.",
                context={
                    "conversation_id": conversation_id,
                    "provider": provider_name,
                    "model": model_name,
                    "fallback_model": FALLBACK_MODEL,
                    "timeout": f"{timeout}s"
                },
                component="base_llm"
            )
  
    def _send_both_failed_alert(self, conversation_id: str, provider_name: str, model_name: str, error: str) -> None:
        """Send alert khi cả 2 LLM đều fail"""
        if ALERT_ENABLED:
            send_alert_safe(
                alert_type=AlertType.LLM_BOTH_FAILED,
                level=AlertLevel.CRITICAL,
                message="Both main and fallback LLM failed. Using INTENT_FALLBACK.",
                context={
                    "conversation_id": conversation_id,
                    "provider": provider_name,
                    "model": model_name,
                    "fallback_model": FALLBACK_MODEL,
                    "error": error[:500]
                },
                component="base_llm"
            )
  
    async def _wait_for_main_task_with_timeout(
        self, 
        main_task: asyncio.Task, 
        conversation_id: str, 
        timeout: float = FALLBACK_TIMEOUT
    ) -> None:
        """
        Đợi main task hoàn thành với timeout, cancel nếu timeout.
        Dùng khi fallback đã về trước nhưng muốn trace main task.
        Chỉ đợi nếu main task chưa done (đang chạy). Nếu đã fail thì không đợi.
        """
        # Nếu main task đã done (fail hoặc success), không cần đợi
        if main_task.done():
            if main_task.exception() is not None:
                # Main đã fail, chỉ log
                logging.warning(f"[BaseLLM] {conversation_id} - Main task already failed: {str(main_task.exception())}, but fallback result already available")
            else:
                # Main đã success (nhưng fallback về trước), chỉ log
                logging.info(f"[BaseLLM] {conversation_id} - Main task already completed")
            return
    
        # Main task đang chạy, đợi với timeout để trace
        try:
            await asyncio.wait_for(main_task, timeout=timeout)
            logging.info(f"[BaseLLM] {conversation_id} - Main task completed (traced in Langfuse)")
        except asyncio.TimeoutError:
            logging.warning(f"[BaseLLM] {conversation_id} - Main task timeout after {timeout}s, cancelling to avoid resource waste")
            await self._cancel_task_safe(main_task, "main_task")
        except Exception as e:
            logging.warning(f"[BaseLLM] {conversation_id} - Main task failed: {str(e)}, but fallback result already available")
            # Main task failed nhưng đã được trace trong Langfuse
  
    async def _handle_main_completed_first(
        self,
        main_task: asyncio.Task,
        fallback_task: asyncio.Task,
        conversation_id: str
    ) -> None:
        """Xử lý khi main task về trước: cancel fallback task"""
        logging.info(f"[BaseLLM] {conversation_id} - Main task completed first, cancelling fallback task")
        await self._cancel_task_safe(fallback_task, "fallback_task")
  
    def _handle_fallback_completed_first(
        self,
        main_task: asyncio.Task,
        conversation_id: str,
        timeout: float = FALLBACK_TIMEOUT
    ) -> None:
        """Xử lý khi fallback về trước: đợi main task ở background để trace (không block response)"""
        logging.info(f"[BaseLLM] {conversation_id} - Fallback task completed first, using fallback result. Waiting for main task to complete in background (for tracing)")
    
        # Đợi main ở background để trace, không block response
        async def _trace_main_in_background():
            try:
                await self._wait_for_main_task_with_timeout(main_task, conversation_id, timeout)
            except Exception as e:
                # Ignore errors trong background task (đã có error handling trong _wait_for_main_task_with_timeout)
                logging.debug(f"[BaseLLM] {conversation_id} - Background main trace task error (ignored): {str(e)}")
    
        # Fire-and-forget: Chạy ở background, không await
        asyncio.create_task(_trace_main_in_background())
  
    async def _handle_both_tasks_timeout(
        self,
        main_task: asyncio.Task,
        fallback_task: asyncio.Task,
        conversation_id: str,
        provider_name: str,
        model_name: str,
        timeout: float = FALLBACK_TIMEOUT
    ) -> str:
        """Xử lý khi cả 2 tasks đều timeout: cancel cả 2, send alert, return INTENT_FALLBACK"""
        logging.warning(f"[BaseLLM] {conversation_id} - Both main and fallback tasks timeout after {timeout}s, cancelling both")
        await self._cancel_both_tasks(main_task, fallback_task)
        self._send_both_timeout_alert(conversation_id, provider_name, model_name, timeout)
        return INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
  
    async def _handle_first_task_failed(
        self,
        main_task: asyncio.Task,
        fallback_task: asyncio.Task,
        completed_task: asyncio.Task,
        conversation_id: str,
        provider_name: str,
        model_name: str,
        first_error: Exception,
        timeout: float = FALLBACK_TIMEOUT
    ) -> str:
        """Xử lý khi task đầu tiên fail: đợi task còn lại"""
        logging.warning(f"[BaseLLM] {conversation_id} - First completed task failed: {str(first_error)}")
    
        # Xác định task còn lại
        remaining_task = fallback_task if completed_task == main_task else main_task
    
        try:
            res = await asyncio.wait_for(remaining_task, timeout=timeout)
            logging.info(f"[BaseLLM] {conversation_id} - Remaining task succeeded")
        
            # Nếu remaining task là main và thành công, hủy fallback
            if remaining_task == main_task:
                await self._cancel_task_safe(fallback_task, "fallback_task")
            # Nếu remaining task là fallback và thành công, đợi main với timeout (nếu main chưa done)
            else:
                # Chỉ đợi main nếu main chưa done (đang chạy), không đợi nếu main đã fail
                await self._wait_for_main_task_with_timeout(main_task, conversation_id, timeout)
        
            return res
        except Exception as e2:
            # Cả 2 đều fail
            logging.warning(f"[BaseLLM] {conversation_id} - Both tasks failed. First: {str(first_error)}, Remaining: {str(e2)}")
            await self._cancel_both_tasks(main_task, fallback_task)
            self._send_both_failed_alert(conversation_id, provider_name, model_name, traceback.format_exc())
            return INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
  
    async def _run_fallback_parallel(
        self,
        main_task: asyncio.Task,
        fallback_task: asyncio.Task,
        conversation_id: str,
        provider_name: str,
        model_name: str,
        timeout: float = FALLBACK_TIMEOUT
    ) -> str:
        """
        Chạy main và fallback song song, xử lý race condition.
    
        Returns:
            str: Result từ task về trước, hoặc INTENT_FALLBACK nếu cả 2 đều fail/timeout
        """
        # Đợi một trong 2 task hoàn thành trước
        try:
            done, pending = await asyncio.wait_for(
                asyncio.wait(
                    {main_task, fallback_task},
                    return_when=asyncio.FIRST_COMPLETED
                ),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            # Cả 2 đều timeout
            return await self._handle_both_tasks_timeout(
                main_task, fallback_task, conversation_id, provider_name, model_name, timeout
            )
    
        # Lấy kết quả từ task hoàn thành đầu tiên
        completed_task = next(iter(done))
    
        try:
            res = await completed_task
        
            # Xử lý theo task nào về trước
            if completed_task == main_task:
                await self._handle_main_completed_first(main_task, fallback_task, conversation_id)
            else:
                # Fallback về trước: return ngay, trace main ở background (không block)
                self._handle_fallback_completed_first(main_task, conversation_id, timeout)
        
            return res
        except Exception as e:
            # Task đầu tiên fail, đợi task còn lại
            return await self._handle_first_task_failed(
                main_task, fallback_task, completed_task, conversation_id,
                provider_name, model_name, e, timeout
            )
  
    def _prepare_fallback_task(
        self,
        fallback_llm,
        provider_name: str,
        messages: list,
        conversation_id: str
    ) -> asyncio.Task:
        """Chuẩn bị fallback task và return task"""
        fallback_params = dict(FALLBACK_PARAMS)
        fallback_params["model"] = FALLBACK_MODEL
        fallback_llm_instance = fallback_llm if fallback_llm is not None else self
        fallback_provider_name = getattr(
            fallback_llm_instance, 
            'provider_name', 
            'openai' if provider_name == 'openai' else 'unknown'
        )
    
        fallback_task = asyncio.create_task(
            self._trace_fallback_llm_call(
                fallback_llm_instance, messages, conversation_id, 
                fallback_params, fallback_provider_name
            )
        )
    
        return fallback_task

    # ==================== Trace Methods ====================
  
    @observe(name="robot-v2.llm.main", capture_input=False, capture_output=True)
    async def _trace_main_llm_call(self, messages, conversation_id, params):
        """Trace main LLM call separately in Langfuse"""
        try:
            return await self.get_response(messages, conversation_id, **params)
        except Exception as e:
            # Error sẽ được tự động capture bởi @observe
            raise

    @observe(name="robot-v2.llm.fallback", capture_input=False, capture_output=True)
    async def _trace_fallback_llm_call(self, fallback_llm_instance, messages, conversation_id, fallback_params, fallback_provider_name="unknown"):
        """Trace fallback LLM call separately in Langfuse"""
        try:
            return await fallback_llm_instance.get_response(messages, conversation_id, **fallback_params)
        except Exception as e:
            # Error sẽ được tự động capture bởi @observe
            raise

    # @observe(name="robot-v2.llm.predict", capture_input=True, capture_output=True)
    async def predict(self, messages, params: dict, **kwargs):
        """
        Dự đoán phản hồi từ LLM với xử lý fallback và logging
    
        Được trace với # @observe để monitor LLM calls trong Langfuse.
        capture_input=True, capture_output=True để giảm overhead (chỉ trace timing và metadata).
    
        Args:
            messages: Danh sách tin nhắn để gửi đến LLM
            params (dict): Tham số cấu hình cho LLM (từ generation_params)
                - model (str): Tên mô hình (vd: "openai/gpt-oss-20b", "gpt-4o-mini")
                - temperature (float): Độ ngẫu nhiên
                - max_tokens (int): Số token tối đa
                - top_p (float): Top-p sampling
                - stream (bool): Có streaming hay không
            **kwargs: Các tham số bổ sung
                - conversation_id (str): ID cuộc hội thoại
                - first_message (str): Tin nhắn đầu tiên (nếu có)
                - start_message (str): Tin nhắn khởi đầu
                - fallback_llm (BaseLLM, optional): OpenAI provider instance để fallback sang gpt-4o-mini
            
        Returns:
            str: Phản hồi từ LLM hoặc giá trị fallback

        Hành vi timeout & fallback:
            - Gọi model chính, chờ tối đa 1.5s.
            - Nếu hết hạn/lỗi: log cảnh báo, kích hoạt song song model phụ gpt-4o-mini qua OpenAI provider.
            - Nếu có fallback_llm trong kwargs: dùng fallback_llm (OpenAI provider) để gọi gpt-4o-mini.
            - Nếu không có fallback_llm và provider hiện tại là openai: dùng self để gọi gpt-4o-mini.
            - Nếu không có fallback_llm và provider không phải openai: không fallback, trả về default.
            - Đua giữa main vs fallback: kết quả nào về trước được dùng, hủy task còn lại.
            - Nếu cả hai đều lỗi/timeout: trả về fallback chuẩn hóa.
        """
        try:
            model_name = params.get("model", "unknown")
            provider_name = self.provider_name or "unknown"
            conversation_id = kwargs.get('conversation_id', 'unknown')
            logging.info(f"[BaseLLM] {conversation_id} - Start predict | Provider: {provider_name} | Model: {model_name}")
        
            if kwargs.get("first_message") is not None and kwargs.get("start_message") not in [None, ""]:
                res = INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
            else:
                # Gọi model chính với timeout 1.5s
                # ✅ Dùng _trace_main_llm_call thay vì get_response trực tiếp
                main_task = asyncio.create_task(
                    self._trace_main_llm_call(messages, conversation_id, params)
                )
            
                # Xác định fallback_llm: ưu tiên fallback_llm từ kwargs, nếu không có thì check provider hiện tại
                fallback_llm = kwargs.get("fallback_llm")
                can_fallback = fallback_llm is not None or provider_name == "openai"
            
                # Log fallback_llm status để debug
                if fallback_llm is not None:
                    logging.info(f"[BaseLLM] {conversation_id} - fallback_llm available | provider={getattr(fallback_llm, 'provider_name', 'unknown')}")
                else:
                    logging.info(f"[BaseLLM] {conversation_id} - fallback_llm=None | can_fallback={can_fallback} | current_provider={provider_name}")
            
                try:
                    # Chờ model chính tối đa 1.5s
                    res = await asyncio.wait_for(main_task, timeout=1.5)
                    logging.info(f"[BaseLLM] {conversation_id} - Main model succeeded within timeout")
                except asyncio.TimeoutError:
                    # Model chính chậm >1.5s: kích hoạt fallback song song
                    # Send alert về LLM timeout
                    if ALERT_ENABLED:
                        send_alert_safe(
                            alert_type=AlertType.LLM_TIMEOUT,
                            level=AlertLevel.HIGH,
                            message="LLM main model timeout after 1.5s. Switching to fallback.",
                            context={
                                "conversation_id": conversation_id,
                                "provider": provider_name,
                                "model": model_name,
                                "timeout": "1.5s"
                            },
                            component="base_llm"
                        )
                
                    if can_fallback:
                        logging.warning(f"[BaseLLM] {conversation_id} - Main model timeout after 1.5s, starting fallback in parallel")
                    
                        # Chuẩn bị và chạy fallback task
                        fallback_task = self._prepare_fallback_task(
                            fallback_llm, provider_name, messages, conversation_id
                        )
                    
                        # Chạy cả 2 song song và xử lý race condition
                        res = await self._run_fallback_parallel(
                            main_task, fallback_task, conversation_id, 
                            provider_name, model_name, FALLBACK_TIMEOUT
                        )
                    else:
                        # Không thể fallback (không có fallback_llm và provider không phải openai)
                        logging.warning(f"[BaseLLM] {conversation_id} - Main model timeout, but cannot fallback (provider={provider_name}, fallback_llm=None)")
                        # Đợi main task hoàn thành để trace
                        try:
                            res = await asyncio.wait_for(main_task, timeout=FALLBACK_TIMEOUT)
                            logging.info(f"[BaseLLM] {conversation_id} - Main task eventually completed")
                        except Exception:
                            res = INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
                except Exception as e:
                    # Nếu main_task fail ngay (không phải timeout): cũng chạy fallback nếu có thể
                    if can_fallback:
                        logging.warning(f"[BaseLLM] {conversation_id} - Main model failed early, fallback to {FALLBACK_MODEL}: {traceback.format_exc()}")
                    
                        # Chuẩn bị và chạy fallback task
                        fallback_task = self._prepare_fallback_task(
                            fallback_llm, provider_name, messages, conversation_id
                        )
                    
                        # Chạy cả 2 song song và xử lý race condition
                        res = await self._run_fallback_parallel(
                            main_task, fallback_task, conversation_id,
                            provider_name, model_name, FALLBACK_TIMEOUT
                        )
                    else:
                        # Không thể fallback, đợi main hoàn thành để trace
                        try:
                            res = await asyncio.wait_for(main_task, timeout=FALLBACK_TIMEOUT)
                        except Exception:
                            res = INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
            
                if isinstance(res, str):
                    res = res.rstrip()
                
            logging.info(f"[BaseLLM] {conversation_id} - Predict: {res} | Provider: {provider_name} | Model: {model_name}")
            return res
        except asyncio.CancelledError:
            # CancelledError là bình thường khi task bị cancel do phoneme đã trả về kết quả hợp lệ trước
            # (khi chạy song song phoneme và LLM, nếu phoneme có kết quả thì cancel LLM task)
            # Không cần log như error vì đây là behavior mong muốn
            logging.debug(f"[BaseLLM] Task cancelled for {kwargs.get('conversation_id')} (phoneme classifier returned result first, LLM task cancelled)")
            res = INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
            return res
        except Exception as e:
            logging.error(f"[ERROR][BaseLLM] Request failed {kwargs.get('conversation_id')}: {traceback.format_exc()}")
            res = INTENT_FALLBACK if INTENT_FALLBACK is not None else "fallback"
            return res

    def parsing_json(self, data: str) -> dict:
        """
        Phân tích chuỗi JSON với xử lý các định dạng đặc biệt
        """
        try:
            return self.json_parser.parse(data)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            # Send alert for malformed response
            if ALERT_ENABLED:
                send_alert_safe(
                    alert_type=AlertType.LLM_MALFORMED_RESPONSE,
                    level=AlertLevel.MEDIUM,
                    message="LLM returned malformed response.",
                    context={
                        "provider": self.provider_name or "unknown",
                        "error": str(e)[:500],
                        "data_preview": data[:200] if data else "empty"
                    },
                    component="base_llm"
                )
            # Re-raise để caller có thể handle
            raise

```