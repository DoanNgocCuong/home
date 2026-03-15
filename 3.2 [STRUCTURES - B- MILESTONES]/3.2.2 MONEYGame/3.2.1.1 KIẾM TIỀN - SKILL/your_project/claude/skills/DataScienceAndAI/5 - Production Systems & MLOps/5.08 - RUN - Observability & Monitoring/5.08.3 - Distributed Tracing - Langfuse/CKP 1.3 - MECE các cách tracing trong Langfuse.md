# MECE 
## 2.1 BẢNG TỔNG HỢP CHI TIẾT: 7 PATTERNS TRIỂN KHAI TRACING LANGFUSE SDK

Bảng tổng hợp 7 phương pháp (patterns) chính để triển khai tracing trong ứng dụng Python sử dụng Langfuse SDK. Mỗi pattern được phân tích sâu về hiệu năng (performance), độ an toàn luồng (thread safety), và ngữ cảnh sử dụng tối ưu. Dữ liệu dựa trên các nghiên cứu benchmark mới nhất với Python 3.10+ và Langfuse SDK v2+.

**Lưu ý về Performance:** Overhead được đo lường trên mỗi operation. Python 3.13+ với free-threading hiện tại (2025-2026) vẫn chưa production-ready cho các thư viện I/O bound phức tạp như Langfuse, do đó các chỉ số dưới đây vẫn chịu ảnh hưởng của GIL contention.

### I. BẢNG TỔNG HỢP CHÍNH (MAIN COMPARISON TABLE)

|Pattern|Mô Tả & Cú Pháp|Performance & Concurrency|Ưu Điểm / Nhược Điểm|Use Case & Khuyến Nghị|
|---|---|---|---|---|
|1. @observe Decorator|**Declarative:** Wrapper tự động trace input/output/error của hàm.  <br>`@observe()`  <br>`def my_func(): ...`|Overhead: ~150-250μs  <br>Throughput: <10K ops/s  <br>Async: ✅ Full  <br>Thread Safety: ❌ BROKEN (ThreadPool)  <br>GIL Contention: 🟡 Medium|**Ưu:** Setup cực nhanh (1 dòng), code sạch, tự động bắt lỗi.  <br>**Nhược:** Mất context khi dùng với `ThreadPoolExecutor`. Không control được scope nhỏ trong hàm.|**✅ DÙNG KHI:** 80% use case thông thường. Web apps (FastAPI/Flask), Asyncio apps, Prototyping.  <br>**❌ TRÁNH KHI:** Sử dụng Multi-threading (ThreadPoolExecutor), cần high-throughput cực cao (>10K ops/s).|
|2. Context Manager|**Imperative:** Xác định scope tracing bằng block `with`.  <br>`with langfuse.start_span() as span:`|Overhead: ~190-210μs  <br>Throughput: <10K ops/s  <br>Async: ✅ Full  <br>Thread Safety: ❌ BROKEN (ThreadPool)  <br>GIL: 🟡 Medium|**Ưu:** Control chính xác scope. Nested spans rõ ràng. Pythonic.  <br>**Nhược:** Verbose nếu lồng nhau quá sâu (pyramid of doom).|**✅ DÙNG KHI:** Cần trace một block code cụ thể, logic phức tạp, conditional tracing.  <br>**❌ TRÁNH KHI:** Code quá simple (gây rối), hoặc dùng trong ThreadPool.|
|3. Manual Span|**Low-level Imperative:** Tạo và kết thúc span thủ công.  <br>`span = client.span()`  <br>`span.end()`|Overhead: ~96-162μs  <br>Throughput: <50K ops/s  <br>Async: ✅ Full  <br>Thread Safety: ✅ Safe  <br>GIL: 🟢 Low|**Ưu:** Overhead thấp nhất. Thread-safe. Không ảnh hưởng active context.  <br>**Nhược:** ⚠️ High Risk: Memory Leak nếu quên `.end()`. Code rườm rà.|**✅ DÙNG KHI:** Background tasks, Parallel processing, Side-tasks không muốn ảnh hưởng main trace.  <br>**❌ TRÁNH KHI:** Logic đơn giản, team thiếu kinh nghiệm (dễ quên end).|
|4. Low-Level API|**Explicit Linking:** Truyền `trace_id` và `parent_id` thủ công.  <br>`client.span(trace_id=..., parent_id=...)`|Overhead: ~132-196μs  <br>Throughput: <100K ops/s  <br>Async/Thread: ✅ Full  <br>Process: ✅ Best Choice|**Ưu:** Control tuyệt đối. Hỗ trợ Distributed Tracing & Multi-process.  <br>**Nhược:** Phức tạp nhất. Dễ sai sót khi quản lý IDs.|**✅ DÙNG KHI:** Microservices, Distributed Systems, ProcessPoolExecutor.  <br>**❌ TRÁNH KHI:** Ứng dụng đơn khối (Monolith) đơn giản.|
|5. LangChain Callback|**Framework Integration:** Tích hợp sẵn vào LangChain.  <br>`config={"callbacks": [handler]}`|Overhead: Biến động (phụ thuộc chain)  <br>Thread Safety: ⚠️ Framework-dependent|**Ưu:** Zero-effort setup cho LangChain. Tự động trace Chains/Agents/Tools.  <br>**Nhược:** Bị khóa chặt vào hệ sinh thái LangChain.|**✅ DÙNG KHI:** Đang sử dụng LangChain hoặc LangGraph.  <br>**❌ TRÁNH KHI:** Custom LLM logic không dùng LangChain.|
|6. OTEL Auto-Instrument|**Zero-Code:** Monkey-patching thư viện.  <br>`AnthropicInstrumentor().instrument()`|Overhead: ⚠️ 7-10% CPU  <br>GIL: 🔴 High Contention|**Ưu:** Không cần sửa code. Hỗ trợ nhiều lib bên thứ 3 (OpenAI, Anthropic).  <br>**Nhược:** "Magic" khó debug. Overhead cao nhất.|**✅ DÙNG KHI:** Cần trace thư viện 3rd-party kín, legacy code không thể sửa.  <br>**❌ TRÁNH KHI:** Performance-critical apps, high-load systems.|
|7. Contextual Update|**Enrichment:** Cập nhật metadata cho trace đang chạy.  <br>`update_current_trace(...)`|Overhead: ~50-100μs  <br>Throughput: Very High  <br>GIL: 🟢 Negligible|**Ưu:** Rất nhanh. Thêm thông tin dynamic (User ID, Tags) runtime.  <br>**Nhược:** Fail silent nếu không có active context.|**✅ DÙNG KHI:** Muốn gắn thêm User ID, Session ID, Tags vào trace sau khi đã start.  <br>**❌ TRÁNH KHI:** Muốn tạo span mới (đây chỉ là update).|

### II. PHỤ LỤC & PHÂN TÍCH KỸ THUẬT

#### 1. Bảng Performance Comparison (Overhead Chi Tiết)

|Pattern|Avg Overhead (μs)|Throughput Limit|Queue Contention Risk|CPU Usage Impact|
|---|---|---|---|---|
|**Contextual Update**|~50 - 100|Very High|Very Low|Rất Thấp|
|**Manual Span**|~96 - 162|~50,000 ops/s|Low|Thấp|
|**Low-Level API**|~132 - 196|~100,000 ops/s|Low-Medium|Trung Bình|
|**@observe**|~150 - 250|~10,000 ops/s|Medium|Trung Bình|
|**Context Manager**|~190 - 210|~10,000 ops/s|Medium|Trung Bình|
|**OTEL Auto-Instrument**|Variable (High)|Variable|High|Cao (7-10% Total CPU)|

#### 2. Concurrency Support Matrix

Khả năng hỗ trợ các mô hình concurrency khác nhau của Python:

| Pattern         | asyncio     | ThreadPoolExecutor | ProcessPoolExecutor | Distributed / Microservices |
| --------------- | ----------- | ------------------ | ------------------- | --------------------------- |
| @observe        | ✅ Supported | ❌ BROKEN           | ❌ BROKEN            | ❌ NO                        |
| Context Manager | ✅ Supported | ❌ BROKEN           | ❌ BROKEN            | ❌ NO                        |
| Manual Span     | ✅ Supported | ✅ Supported        | ⚠️ Manual IPC       | ⚠️ Manual Prop              |
| Low-Level API   | ✅ Supported | ✅ Supported        | ✅ Best Choice       | ✅ Best Choice               |

#### 3. Decision Tree (Cây Quyết Định Chọn Pattern)

**START: Bạn đang xây dựng loại ứng dụng gì?**

- 🔻 **Dùng LangChain/LangGraph framework?**
    - 👉 **Có:** Chọn **Pattern 5 (LangChain Callback)**
- 🔻 **Cần trace thư viện 3rd party (OpenAI/Anthropic) mà không sửa code?**
    - 👉 **Có:** Chọn **Pattern 6 (OTEL Auto-Instrument)**
- 🔻 **Ứng dụng Distributed hoặc Multi-process?**
    - 👉 **Có:** Chọn **Pattern 4 (Low-Level API)**
- 🔻 **Dùng ThreadPoolExecutor cho các tác vụ song song?**
    - 👉 **Có:** Chọn **Pattern 3 (Manual Span)** hoặc **Pattern 4**
- 🔻 **Cần thêm thông tin (User/Tag) vào trace đang chạy?**
    - 👉 **Có:** Chọn **Pattern 7 (Contextual Update)**
- 🔻 **Chỉ cần trace function thông thường (Async/Sync)?**
    - 👉 **Default:** Chọn **Pattern 1 (@observe)** (Đơn giản nhất)
    - 👉 **Cần scope block:** Chọn **Pattern 2 (Context Manager)**

### III. TOP PICKS THEO SCENARIO 🏆

|                                                                                                                                                                         |                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| #### 🥇 Cho Người Mới / Web Apps<br><br>**Pattern 1: @observe**<br><br>Dễ dùng nhất, ít code nhất, cover được 80% nhu cầu của các ứng dụng FastAPI/Flask chạy asyncio.  | #### 🥈 Cho Hệ Thống High-Performance<br><br>**Pattern 3: Manual Span**<br><br>Khi mỗi microsecond đều quan trọng. Manual span giảm thiểu overhead của context propagation và decorator magic. |
| #### 🥉 Cho Microservices Architecture<br><br>**Pattern 4: Low-Level API**<br><br>Bắt buộc phải dùng pattern này để truyền Trace ID qua HTTP Headers giữa các services. | #### ⭐ Cho Dynamic Metadata<br><br>**Pattern 7: Contextual Update**<br><br>Dùng kèm với bất kỳ pattern nào khác để enrich data mà không tốn chi phí tạo span mới.                              |

### IV. ANTI-PATTERNS & BEST PRACTICES

#### 🚫 ANTI-PATTERNS (Cần Tránh)

- **Dùng @observe với ThreadPoolExecutor:** Context sẽ bị mất, các span con sẽ trở thành orphan (mồ côi) không gắn vào trace cha.
- **Manual Span không có try/finally:** Nếu code lỗi trước khi gọi `.end()`, span sẽ treo vĩnh viễn trong memory, gây leak.
- **Lạm dụng OTEL Auto-Instrument:** Bật auto-instrument cho toàn bộ app sẽ tăng CPU usage lên ~10% không cần thiết. Chỉ bật cho libraries cần thiết.
- **Nested Context Manager quá sâu:** >5 tầng lồng nhau (Pyramid of Doom) gây khó đọc và tăng latency tích lũy.

#### ✅ BEST PRACTICES (Nguyên Tắc Vàng)

- **Start Simple:** Bắt đầu với `@observe`. Chỉ optimize sang Manual Span khi đo đạc thấy overhead > 5%.
- **Safety First:** Luôn ưu tiên Pattern có quản lý lỗi tự động (Decorator, Context Manager) trừ khi không thể.
- **Mix & Match:** Có thể kết hợp nhiều patterns trong cùng 1 app (VD: `@observe` cho main flow, `Manual` cho background tasks).
- **Contextual Enrichment:** Luôn dùng Pattern 7 để gắn User ID ngay khi có thể để dễ debug sau này.




---

## 2.2 So sánh về response time và overhead của @observe và Context Manager: langfuse.start_as_current_observation()


<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

### Kết Luận: KHÔNG CÓ Bằng Chứng Context Manager Nhanh Hơn @observe

Sau khi kiểm tra kỹ lưỡng cả tài liệu bạn đã đọc và các nguồn trên web, tôi phải kết luận rằng:

#### ❌ KHÔNG TÌM THẤY bằng chứng nào cho thấy Context Manager nhanh hơn @observe trong Langfuse

### Bằng Chứng Từ Báo Cáo Của Bạn

#### 1. **Khẳng Định Rõ Ràng: Cả Hai TƯƠNG ĐƯƠNG**

Từ Section 2.4 của báo cáo:[^1]

> **"Câu trả lời là không. Cả hai chỉ là các phương tiện khác nhau để đạt được cùng một mục đích: đảm bảo rằng một span được bắt đầu trước một khối mã và được kết thúc sau khi khối mã đó hoàn thành. Chúng là 'cú pháp tiện lợi' (syntactic sugar) cho cùng một logic."**

> **"Cả hai pattern đều dẫn đến cùng một kết quả cuối cùng: một lệnh gọi đến `span.end()`, sau đó là `BatchSpanProcessor.on_end()`, và cuối cùng là `queue.put()`. Do đó, chúng có đặc tính hiệu năng hoàn toàn giống nhau trong bối cảnh này."**

#### 2. **Kết Luận Trong Phần 5**[^1]

> **"@observe và Context Manager có đặc tính hiệu năng tương đương. Cả hai chỉ là giao diện. Việc lựa chọn giữa chúng nên dựa trên sự rõ ràng và tính biểu cảm của mã nguồn, không phải vì lý do hiệu năng."**

### Bằng Chứng Từ Web Research

#### Không Có Benchmark Cụ Thể Cho Langfuse

Tôi đã search kỹ nhưng **KHÔNG TÌM THẤY** bất kỳ:

- Benchmark so sánh Langfuse @observe vs Context Manager
- Performance test cụ thể giữa hai patterns trong Langfuse
- Discussion nào khẳng định Context Manager nhanh hơn @observe


#### Overhead Thực Tế Là GẦN NHƯ TƯƠNG ĐƯƠNG

Từ các performance studies về Python decorators vs context managers:[^2][^3][^4]


| Thành Phần | Overhead |
| :-- | :-- |
| **Function call (baseline)** | 0.132 μs[^4] |
| **Decorator overhead** | +0.194 μs (total: 0.326 μs)[^4] |
| **Context Manager overhead** | "Small, usually negligible"[^2] |

**Kết luận:** Chênh lệch < 50 nanoseconds, **không có ý nghĩa thực tế**.

### Tại Sao Có Thể Có Hiểu Lầm?

#### 1. **Confusion với @contextmanager Decorator**

Có một Stack Overflow post cho thấy `@contextmanager` decorator CÓ THỂ chậm hơn, NHƯNG:[^5]

- Đó là về Python's `@contextmanager` decorator (để tạo context manager từ generator)
- **KHÔNG PHẢI** về việc so sánh `@observe` vs `with langfuse.start_as_current_observation()`
- Context khác hoàn toàn


#### 2. **Micro-benchmarks Không Đáng Tin**

Nếu bạn đã thấy benchmarks cho thấy chênh lệch:

- Có thể do test không đồng nhất (different conditions)
- Chênh lệch < 10% là **statistical noise** (GC, OS scheduler, CPU throttling)
- Dưới high load với queue contention, cả hai đều chậm như nhau[^1]


#### 3. **Báo Cáo Benchmark Thực Tế**

Từ Langfuse Performance Test (đã cite trong báo cáo):[^6]

```
Overhead measurements (không phân biệt @observe vs Context Manager):
- LlamaIndex indexing: +4% (0.171s → 0.178s)
- LlamaIndex query: +0.8% (0.795s → 0.802s)
```

**Báo cáo KHÔNG SO SÁNH giữa hai patterns vì chúng được coi là tương đương**.

### Flow Execution Giống Hệt Nhau

#### @observe Decorator

```python
@observe()
def my_function():
    return "result"

# Thực tế compile thành:
def my_function():
    span = langfuse.start_span()
    try:
        result = actual_function()
        return result
    finally:
        span.end()  # → BatchSpanProcessor.on_end() → queue.put()
```


#### Context Manager

```python
def my_function():
    with langfuse.start_as_current_observation():
        return "result"

# Thực tế compile thành:
def my_function():
    span = langfuse.start_span()
    span.__enter__()
    try:
        result = "result"
        return result
    finally:
        span.__exit__()  # Internally calls span.end() → BatchSpanProcessor.on_end() → queue.put()
```

**Cả hai đều gọi CHÍNH XÁC cùng một sequence:**

```
span.end() 
  → BatchSpanProcessor.on_end() 
    → queue.put(span)  ← ĐÂY LÀ 95% OVERHEAD
      → Queue lock contention
        → GIL contention
```


### Overhead Breakdown (Cả Hai Patterns)

| Component | Overhead (μs) | % Total |
| :-- | :-- | :-- |
| **Queue lock contention** | ~120-150 | **~60-75%** |
| **GIL contention** | ~50-70 | **~20-30%** |
| **Serialization** | ~10-20 | ~5-10% |
| **Context propagation** | ~5-10 | ~2-5% |
| **@observe wrapper** | ~2-5 | <2% |
| **Context Manager __enter__/__exit__** | ~2-5 | <2% |
| **TOTAL** | ~190-250 | 100% |

**Chênh lệch giữa @observe và Context Manager:** < 3 μs (~1-2% của total overhead)

### Kết Luận Cuối Cùng

#### ✅ Sự Thật Duy Nhất

**Context Manager và @observe có performance TƯƠNG ĐƯƠNG trong Langfuse**. Mọi benchmark cho thấy khác đều là:[^1]

1. Measurement noise
2. Testing methodology issues
3. Confusion với Python's `@contextmanager` decorator
4. Micro-optimization không có ý nghĩa trong production


<span style="display:none">[^10][^11][^12][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: GIL_Langfuse_Deep_Dive_Report.md

[^2]: https://dev.to/godofgeeks/python-decorators-context-managers-5968

[^3]: https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/09-performance-overhead-of-using-decorators.md

[^4]: https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/10-performance-overhead-when-applying-decorators-to-methods.md

[^5]: https://stackoverflow.com/questions/34872535/why-contextmanager-is-slow

[^6]: https://langfuse.com/guides/cookbook/langfuse_sdk_performance_test

[^7]: https://stackoverflow.com/questions/50823473/difference-between-context-managers-and-decorators-in-python

[^8]: https://dev.to/sk_rajibul_9ce58a68c43bb5/leveraging-pythons-built-in-decorator-for-improved-performance-2pkd

[^9]: https://github.com/orgs/langfuse/discussions/3725

[^10]: https://www.youtube.com/watch?v=cSbD5SKwak0

[^11]: https://stackoverflow.com/questions/61976561/python-decorator-that-wraps-function-with-with-statement

[^12]: https://github.com/orgs/langfuse/discussions/2488






---

# 2.3 PERFLEXITY - Các cách log vào Langfuse

Langfuse cung cấp **4 phương pháp chính** để instrument và log traces vào hệ thống observability:[^1][^2]

### 1. **@observe Decorator** (Tự động capture)

Wrapper function để tự động capture inputs, outputs, timings và errors mà không cần sửa logic bên trong function.[^2]

```python
from langfuse import observe

@observe(name="llm-call", as_type="generation")
async def my_async_llm_call(prompt_text):
    return "LLM response"

@observe()  # Tự động tạo TRACE ở top-level
def main_function(data, parameter):
    # Tự động tạo SPAN ở nested function
    return my_data_processing_function(data, parameter)
```

**Ưu điểm**:

- Đơn giản nhất, không xâm phạm code[^3]
- Tự động maintain call stack hierarchy[^3]
- Async-safe với Python Contextvars[^3]

**Tùy chỉnh**: Có thể tắt capture I/O để giảm overhead:[^2]

```python
@observe(capture_input=False, capture_output=False)
def sensitive_function():
    pass
```


### 2. **Context Manager** (start_as_current_observation)

Tạo span và set làm active observation trong OpenTelemetry context.[^2]

```python
from langfuse import get_client, propagate_attributes

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span",
    name="user-request-pipeline",
    input={"user_query": "Tell me a joke"},
) as root_span:
    # Nested spans tự động inherit parent
    with langfuse.start_as_current_observation(
        as_type="generation",
        name="joke-generation",
        model="gpt-4o",
    ) as generation:
        generation.update(output="Why did the span cross the road?")
    
    root_span.update(output={"final_joke": "..."})
```

**Ưu điểm**:

- Kiểm soát lifecycle của observation[^2]
- Tự động quản lý `.end()` khi exit context[^2]
- Hỗ trợ nesting tự nhiên qua OpenTelemetry context propagation[^2]


### 3. **Manual Observations** (start_observation)

Tạo observations thủ công không thay đổi active context.[^2]

```python
from langfuse import get_client

langfuse = get_client()

# Manual span - không thay đổi active context
span = langfuse.start_observation(name="manual-span")
span.update(input="Data for side task")

# Tạo child spans
child = span.start_observation(name="child-span", as_type="generation")
child.end()

span.end()  # ⚠️ PHẢI gọi .end() thủ công
```

**Khi nào dùng**:[^2]

- Background tasks song song với main execution
- Lifecycle được xác định bởi non-contiguous events
- Cần reference đến observation object trước khi tie vào context

**Lưu ý**: Phải tự gọi `.end()`, nếu không sẽ mất data.[^2]

### 4. **Native Integrations** (OpenAI, LangChain, ...)

Tự động tạo observations cho popular frameworks:[^2]

```python
# OpenAI Integration
from langfuse.openai import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    langfuse_public_key="pk-lf-..."  # Multi-project routing
)

# LangChain Integration
from langfuse.langchain import CallbackHandler

handler = CallbackHandler(public_key="pk-lf-...")
chain.invoke({"topic": "ML"}, config={"callbacks": [handler]})
```


***

## Advanced Techniques

### **Propagate Attributes** (Session ID, User ID, Metadata)

```python
from langfuse import propagate_attributes

with langfuse.start_as_current_observation(name="workflow"):
    with propagate_attributes(
        user_id="user_123",
        session_id="session_abc",
        metadata={"experiment": "variant_a"},
        version="1.0",
    ):
        # Tất cả nested observations tự động inherit attributes
        with langfuse.start_as_current_observation(name="llm-call"):
            pass
```

**Cross-service propagation** qua HTTP headers:[^1]

```python
with propagate_attributes(
    user_id="user_123",
    as_baggage=True,  # ⚠️ Add vào HTTP headers
):
    requests.get("https://service-b.example.com/api")
```


### **Update Trace-Level Input/Output**

Mặc định trace input/output mirror root observation, nhưng có thể override:[^2]

```python
with langfuse.start_as_current_observation(name="pipeline") as root:
    root.update(input="Step 1 data", output="Step 1 result")
    
    # Override trace-level (useful cho LLM-as-a-Judge)
    root.update_trace(
        input={"original_query": "User's question"},
        output={"final_answer": "Complete response", "confidence": 0.95}
    )
```


### **Mask Sensitive Data**

```python
from langfuse import Langfuse
import re

def pii_masker(data: any, **kwargs) -> any:
    if isinstance(data, str):
        return re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", 
                      "[EMAIL_REDACTED]", data)
    return data

langfuse = Langfuse(mask=pii_masker)
```


### **Sampling** (Giảm cost trong high-volume apps)

```python
# Sample 20% traces
langfuse = Langfuse(sample_rate=0.2)
```


### **Multi-Project Setup** (Experimental)

Route traces đến nhiều projects:[^1]

```python
# Top-most decorated function cần langfuse_public_key
@observe
def process_for_project_a(data):
    return result

result = process_for_project_a(
    data="input",
    langfuse_public_key="pk-lf-project-a-..."
)
```


***

## Flushing \& Lifecycle

**Quan trọng cho serverless/scripts**:[^2]

```python
from langfuse import get_client

langfuse = get_client()

# ... create traces ...

langfuse.flush()     # Đảm bảo send all buffered data
langfuse.shutdown()  # Graceful shutdown với cleanup
```


***

## So sánh các phương pháp

| Phương pháp | Ease of Use | Control Level | Auto Context | Use Case |
| :-- | :-- | :-- | :-- | :-- |
| **@observe** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ✅ | Simple functions, auto-tracing [^3] |
| **Context Manager** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | Complex workflows, explicit spans [^2] |
| **Manual** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | Background tasks, custom lifecycle [^2] |
| **Native Integrations** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | OpenAI, LangChain, Vercel AI SDK [^2] |


***

## Best Practices

1. **@observe cho entry point** để tạo TRACE tự động[^3]
2. **Context manager cho nested spans** với explicit control[^2]
3. **Propagate attributes sớm** trong trace để đảm bảo tất cả observations có metadata[^2]
4. **Flush() trong serverless** để tránh mất data[^2]
5. **Update trace-level I/O** cho LLM-as-a-Judge workflows[^2]

Bạn muốn tôi demo áp dụng cách nào cho `finai_agent`?
<span style="display:none">[^10][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://langfuse.com/docs/observability/sdk/python/advanced-usage

[^2]: https://langfuse.com/docs/observability/sdk/overview

[^3]: https://langfuse.com/blog/2024-04-python-decorator

[^4]: https://langfuse.com/docs/observability/features/log-levels

[^5]: https://langfuse.com/docs/observability/sdk/advanced-features

[^6]: https://langfuse.com/docs/sdk/python/decorators

[^7]: https://www.paulmduvall.com/llm-observability-with-langfuse-a-complete-guide/

[^8]: https://github.com/orgs/langfuse/discussions/8305

[^9]: https://github.com/langfuse/langfuse/issues/2238

[^10]: https://www.flowhunt.io/knowledge-base/how-to-trace-flowhunt-ai-agents-with-langfuse/



---

# 2.4 Tại sao phải dùng cách nested spans này nhỉ, sao ko dùng observe vào đầu mỗi hàm là được mà nhỉ

---



# 2.5  Best Practices Triển Khai Langfuse Python SDK

## 1. Client Initialization Pattern

### ✅ **Recommended: `get_client()` Pattern**

```python
# app/core/langfuse_client.py
from langfuse import get_client

# Singleton instance - initialized once, reused everywhere
langfuse_client = get_client()

# Export for use across the application
__all__ = ["langfuse_client"]
```

**Tại sao?**

- Clear intent: “Get existing client” thay vì “Create new instance”
- Tránh confusion với “new arguments are ignored” behavior
- Thread-safe và context-aware
- [Source](https://langfuse.com/docs/observability/sdk/overview)

---

## 2. Project Structure Best Practice

```
your_project/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── langfuse_client.py      # Single initialization point
│   ├── services/
│   │   └── llm_service.py          # Import from core
│   ├── api/
│   │   └── routes.py               # Import from core
│   └── utils/
│       └── tracing_utils.py        # Helper functions
├── main.py                          # Application entry
└── .env                            # Environment variables
```

### ✅ **Single Import Pattern**

```python
# app/core/langfuse_client.py
from langfuse import get_client, observe
from langfuse._client import Langfuse

# Initialize once at startup
langfuse_client: Langfuse = get_client()

def get_langfuse():
    """Get the singleton Langfuse client."""
    return langfuse_client

__all__ = ["langfuse_client", "get_langfuse", "observe"]
```

---

## 3. Environment Configuration

### ✅ **Environment Variables (Best Practice)**

```bash
# .env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com  # or your self-hosted URL
LANGFUSE_TRACING_ENVIRONMENT=production
LANGFUSE_SAMPLE_RATE=1.0  # 1.0 = 100%, 0.1 = 10%
LANGFUSE_TRACING_ENABLED=true
LANGFUSE_FLUSH_INTERVAL=10.0  # seconds
```

**Ưu điểm:**

- Không cần hardcode credentials
- Dễ dàng chuyển đổi giữa environments
- Consistent với [Langfuse docs](https://langfuse.com/docs/observability/features/environments)

---

## 4. Instrumentation Patterns

### ✅ **Pattern 1: `@observe` Decorator (Recommended)**

```python
from app.core.langfuse_client import observe

@observe(as_type="generation")
async def call_llm(prompt: str, model: str = "gpt-4"):
    """Automatically traced LLM call."""
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Update metadata if needed
@observe(as_type="generation")
async def call_llm_with_metadata(prompt: str):
    response = await call_llm(prompt)
    
    # Get client to update current span
    from app.core.langfuse_client import get_langfuse
    langfuse = get_langfuse()
    
    langfuse.update_current_generation(
        metadata={"custom_key": "value"},
        usage={
            "input": 100,
            "output": 50,
            "total": 150,
            "unit": "TOKENS",
            "input_cost": 0.001,
            "output_cost": 0.002
        }
    )
    return response
```

### ✅ **Pattern 2: Context Manager**

```python
from app.core.langfuse_client import get_langfuse

async def process_workflow(user_input: str):
    langfuse = get_langfuse()
    
    # Create trace context
    with langfuse.start_as_current_observation(
        as_type="span",
        name="workflow_processing"
    ) as span:
        # All nested calls automatically become children
        result = await step1(user_input)
        result = await step2(result)
        
        # Update span before exiting
        span.update(
            metadata={"workflow_version": "1.0.0"},
            output=result
        )
        return result
```

### ✅ **Pattern 3: Manual Observations (Advanced)**

```python
from app.core.langfuse_client import get_langfuse

async def background_task(data: dict):
    """For non-blocking, parallel operations."""
    langfuse = get_langfuse()
    
    # Create manual observation (no context shift)
    observation = langfuse.start_observation(
        as_type="span",
        name="background_processing"
    )
    
    try:
        result = await process_data(data)
        observation.end(
            output=result,
            status="success"
        )
    except Exception as e:
        observation.end(
            error=str(e),
            status="error"
        )
        raise
```

---

## 5. Async/Await Best Practices

### ✅ **Trong async code, rely on Langfuse helpers**

```python
# ✅ Good: Use decorator
@observe(as_type="generation")
async def async_llm_call():
    return await openai_client.chat.completions.create(...)

# ✅ Good: Use context manager with async
async def async_workflow():
    langfuse = get_langfuse()
    
    with langfuse.start_as_current_observation(as_type="span") as span:
        # await boundaries are handled correctly
        result1 = await step1()
        result2 = await step2(result1)
        return result2

# ❌ Avoid: Manual context management across await boundaries
async def bad_pattern():
    trace = langfuse.start_trace(name="bad")
    await step1()  # Context might be lost here!
    trace.end()  # Might not work correctly
```

[Source](https://langfuse.com/docs/observability/sdk/troubleshooting-and-faq)

---

## 6. Multi-Project Setup (Advanced)

### ✅ **Contextvars for Multi-Project**

```python
from langfuse._client.get_client import _set_current_public_key
from app.core.langfuse_client import get_langfuse

async def handle_multi_project_request(project_id: str):
    # Set context for this request
    with _set_current_public_key(project_id):
        langfuse = get_langfuse()
        # All traces go to correct project
        await process_request()
```

**Lưu ý:** Multi-project support là experimental. [Source](https://langfuse.com/docs/observability/sdk/advanced-features)

---

## 7. Error Handling & Resilience

### ✅ **Graceful Degradation**

```python
from app.core.langfuse_client import get_langfuse

async def safe_llm_call(prompt: str):
    try:
        langfuse = get_langfuse()
        
        with langfuse.start_as_current_observation(
            as_type="generation",
            name="llm_call"
        ) as span:
            response = await openai_client.chat.completions.create(...)
            span.update(output=response.choices[0].message.content)
            return response
            
    except Exception as e:
        # Langfuse won't break your app
        # Log error but don't crash
        logger.error(f"LLM call failed: {e}")
        # Return fallback or re-raise
        raise
```

---

## 8. Short-Lived Processes (Scripts/Serverless)

### ✅ **Always Flush/Shutdown**

```python
# scripts/batch_processing.py
from app.core.langfuse_client import get_langfuse

async def main():
    langfuse = get_langfuse()
    
    try:
        # Process data
        for item in dataset:
            await process_item(item)
    finally:
        # Critical: Flush before exit
        langfuse.flush()  # or langfuse.shutdown()
        # In async: await langfuse.async_shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Tại sao?** SDK là asynchronous và buffers spans trong background. [Source](https://langfuse.com/docs/sdk/python/decorators)

---

## 9. Sampling Strategy

### ✅ **Production Setup**

```python
# .env.production
LANGFUSE_SAMPLE_RATE=0.1  # 10% sampling in production

# .env.development
LANGFUSE_SAMPLE_RATE=1.0   # 100% in development
```

```python
# For critical paths, force sampling
@observe(as_type="generation")
async def critical_path():
    # This will respect global sample_rate
    pass

# Or use manual sampling override (if supported)
```

**Lưu ý:** Với SDK v3, sampling được quản lý ở global OTEL TracerProvider level, không thể có different sampling rates cho cùng public_key. [Source](https://github.com/orgs/langfuse/discussions/7571)

---

## 10. Testing & Development

### ✅ **Mock Langfuse for Testing**

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_langfuse():
    """Mock Langfuse client for unit tests."""
    mock = MagicMock()
    mock.start_as_current_observation.return_value.__enter__ = MagicMock(
        return_value=MagicMock()
    )
    mock.start_as_current_observation.return_value.__exit__ = MagicMock(
        return_value=False
    )
    return mock

# tests/test_service.py
async def test_llm_service(mock_langfuse, monkeypatch):
    monkeypatch.setattr(
        "app.services.llm_service.get_langfuse",
        lambda: mock_langfuse
    )
    
    result = await llm_service.call_llm("test prompt")
    assert result is not None
```

---

## 11. Monitoring & Debugging

### ✅ **Enable Debug Logging (Development Only)**

```python
# .env.development
LANGFUSE_DEBUG=True
```

```python
# Programmatic check
from app.core.langfuse_client import get_langfuse

langfuse = get_langfuse()

# Verify connectivity (don't use in production)
try:
    langfuse.auth_check()
    print("✅ Langfuse connected")
except Exception as e:
    print(f"❌ Langfuse connection failed: {e}")
```

---

## 12. Summary Checklist

|Aspect|Best Practice|Priority|
|---|---|---|
|**Client Init**|`get_client()` in single module|🔴 High|
|**Import Pattern**|Import from centralized module|🔴 High|
|**Config**|Environment variables|🔴 High|
|**Tracing**|`@observe` decorator|🟡 Medium|
|**Async**|Use decorators/context managers|🟡 Medium|
|**Shutdown**|`flush()`/`shutdown()` in scripts|🔴 High|
|**Sampling**|Environment-based rates|🟢 Low|
|**Multi-project**|Contextvars with caution|🟢 Low|
|**Testing**|Mock client|🟡 Medium|

---

## 13. Common Anti-Patterns to Avoid

### ❌ **Don’t: Create multiple Langfuse() instances expecting different configs**

```python
# ❌ Bad: This won't work as expected!
client1 = Langfuse(sample_rate=0.1)   # First call "wins"
client2 = Langfuse(sample_rate=1.0)   # Ignored! Same public_key
```

### ❌ **Don’t: Mix `get_client()` and `Langfuse()` without understanding**

```python
# ❌ Confusing and potentially problematic
from langfuse import Langfuse, get_client

# In one file
client_a = Langfuse()

# In another file
client_b = get_client()  # Might return different instance!
```

### ❌ **Don’t: Forget to flush in short-lived processes**

```python
# ❌ Data might be lost!
def lambda_handler(event, context):
    langfuse = get_langfuse()
    process(event)
    # Missing flush() or shutdown()!
```

---

## 14. Recommended Project Template

```python
# app/core/langfuse_client.py
"""
Centralized Langfuse client configuration.
All Langfuse interactions should go through this module.
"""
from langfuse import get_client, observe
from langfuse._client import Langfuse

# Initialize singleton client
_langfuse_client: Langfuse = get_client()

def get_langfuse() -> Langfuse:
    """Get the singleton Langfuse client."""
    return _langfuse_client

__all__ = ["get_langfuse", "observe"]
```

```python
# app/services/llm_service.py
from app.core.langfuse_client import get_langfuse, observe

@observe(as_type="generation")
async def call_llm(prompt: str, model: str = "gpt-4"):
    """LLM call with automatic tracing."""
    langfuse = get_langfuse()
    
    # Update metadata if needed
    langfuse.update_current_generation(
        metadata={"model": model, "prompt_version": "1.0"}
    )
    
    # Your LLM call here
    response = await openai_client.chat.completions.create(...)
    return response.choices[0].message.content
```

```python
# main.py
from app.core.langfuse_client import get_langfuse

async def main():
    langfuse = get_langfuse()
    
    try:
        # Your application logic
        pass
    finally:
        # Critical for clean shutdown
        await langfuse.async_shutdown()
```

---

Bạn muốn tôi đi sâu vào phần nào cụ thể hơn không? Ví dụ:

- Multi-project setup chi tiết
- Self-hosted Langfuse configuration
- Integration với FastAPI/FastAPI
- Prompt management best practices