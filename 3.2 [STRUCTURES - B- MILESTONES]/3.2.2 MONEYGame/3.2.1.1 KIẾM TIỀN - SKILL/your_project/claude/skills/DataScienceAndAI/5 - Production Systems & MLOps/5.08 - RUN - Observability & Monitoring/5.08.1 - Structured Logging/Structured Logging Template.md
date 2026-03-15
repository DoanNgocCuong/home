# Standard logging template


# Logging Standards — Chuẩn hóa Log cho các Service

> Tài liệu định nghĩa chuẩn viết log JSON cho tất cả các service trong hệ thống. Áp dụng cho mọi ngôn ngữ lập trình, mọi service.

**Version**: 2.0 · **Cập nhật**: 2026-03-06

**Changelog**:

- v2.0 (2026-03-06): Bổ sung OpenTelemetry alignment, Log Sampling Strategy, Cost Optimization, Performance Guidelines, Alerting, Correlation Strategy. Cải thiện Security section theo OWASP 2025. Thống nhất event naming conventions.
- v1.1 (2026-02-26): Thêm Body Logging Policy, gRPC logging, Body masking/truncation.
- v1.0 (2026-01-20): Phiên bản đầu tiên.



---

## Cách đọc tài liệu này

Tài liệu được chia thành **3 tầng** theo mức độ quan trọng:

|Tầng|Phần|Ai cần đọc|Bắt buộc?|
|---|---|---|---|
|🔴 **CORE**|Part 1–3|Mọi developer|**Có** — Đây là nền tảng. Không có phần này thì log vô dụng|
|🟡 **POLICY**|Part 4–5|Developer + Tech Lead|**Có** — Bảo vệ hệ thống khỏi rủi ro bảo mật và chi phí|
|🟢 **ADVANCED**|Part 6–7|Tech Lead + SRE/DevOps|Không bắt buộc ngay — Cần khi hệ thống scale hoặc migrate vendor|

> **Nếu bạn mới bắt đầu**: Đọc Part 1 để hiểu mental model → Part 2 để hiểu schema → Part 3 để xem ví dụ cho loại service bạn đang làm. Phần còn lại đọc khi cần.

---

## Mục lục

**🔴 CORE — Nền tảng (bắt buộc)**

- [Part 1: Tại sao & Tư duy](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-1-t%E1%BA%A1i-sao--t%C6%B0-duy)
- [Part 2: Schema — Cấu trúc JSON Log](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-2-schema--c%E1%BA%A5u-tr%C3%BAc-json-log)
- [Part 3: Log Types — Áp dụng cho từng loại service](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-3-log-types--%C3%A1p-d%E1%BB%A5ng-cho-t%E1%BB%ABng-lo%E1%BA%A1i-service)

**🟡 POLICY — Quy định vận hành (bắt buộc)**

- [Part 4: Security & Body Logging](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-4-security--body-logging)
- [Part 5: Correlation Strategy](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-5-correlation-strategy)

**🟢 ADVANCED — Nâng cao (khi cần)**

- [Part 6: Production Operations](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-6-production-operations)
- [Part 7: Ecosystem Integration](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#part-7-ecosystem-integration)

**📎 APPENDIX**

- [Appendix A: Checklist](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#appendix-a-checklist)
- [Appendix B: Quick Reference](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#appendix-b-quick-reference)
- [Tài liệu tham khảo](https://claude.ai/chat/cabcdeb4-12c0-4dbf-9799-7585fe55f068#t%C3%A0i-li%E1%BB%87u-tham-kh%E1%BA%A3o)

---

# 🔴 CORE — Nền tảng

---

## Part 1: Tại sao & Tư duy

### 1.1 Vấn đề: Log không cấu trúc = Debug mù

Hãy tưởng tượng 2 giờ sáng, hệ thống sập, và bạn thấy dòng log này:

```
2024-01-20 10:30:45 ERROR Something went wrong
```

Bạn biết gì? **Gần như không gì cả.** Không biết service nào, user nào, request nào, lỗi gì.

Bây giờ so sánh với:

```json
{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "ERROR",
  "message": "POST /api/orders - 500 Internal Server Error in 89ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SERVER_ERROR",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "status_code": "500",
  "duration_ms": "89",
  "error_type": "NullPointerException",
  "error_message": "Cannot invoke method on null object at OrderService.create()",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "correlation_id": "corr_xyz789",
  "service": "order-service",
  "environment": "prod"
}
```

Bây giờ bạn biết: **ai** (user_123), **ở đâu** (order-service, POST /api/orders), **chuyện gì** (NullPointerException), **nghiêm trọng thế nào** (500, ERROR), **liên quan đến gì** (corr_xyz789 để trace toàn bộ flow). Bạn có thể query trên Datadog trong 30 giây thay vì grep 2 tiếng.

### 1.2 Mục tiêu: Mọi log phải trả lời được 5 câu hỏi

Trước khi viết bất kỳ dòng log nào, hãy tự hỏi — log này trả lời được bao nhiêu câu:

|#|Câu hỏi|Field trả lời|
|---|---|---|
|1|**KHI NÀO** xảy ra?|`@timestamp`|
|2|**NGHIÊM TRỌNG** thế nào?|`level`|
|3|**CHUYỆN GÌ** xảy ra?|`message`, `event`|
|4|**Ở ĐÂU** trong hệ thống?|`service`, `log_type`, `feature`|
|5|**AI / CÁI GÌ** gây ra?|`user_id`, `request_id`, `error_type`|

Nếu log không trả lời được ít nhất 4/5 câu → log đó chưa đủ tốt.

### 1.3 Tại sao cần chuẩn hóa?

- **Truy vấn dễ dàng**: Log có cấu trúc JSON giúp filter, search nhanh trên Datadog/ELK — không cần fragile regex.
- **Correlation**: Liên kết log giữa các service qua `correlation_id`, `trace_id`, `span_id`.
- **Monitoring & Alerting**: Tạo dashboard, alert dựa trên các field chuẩn (`status_code`, `duration_ms`, `error_type`).
- **Debug**: Nhanh chóng xác định root cause khi có incident.
- **Cost Control**: Schema chuẩn giúp áp dụng sampling, tiered retention hiệu quả.
- **Compliance**: Đáp ứng yêu cầu audit trail theo OWASP, PCI-DSS.

### 1.4 Nguyên tắc thiết kế

|#|Nguyên tắc|Giải thích|
|---|---|---|
|1|**Machine-first, human-readable**|Log phải dễ parse bằng máy (JSON), nhưng `message` field phải dễ đọc cho người|
|2|**Schema-first**|Thống nhất field names trước khi implement. Không để mỗi team đặt tên khác nhau cho cùng một concept|
|3|**Opt-in sensitive data**|Body logging, PII fields là opt-in — phải chủ động bật, không phải mặc định|
|4|**Cost-aware**|Mọi quyết định log đều cân nhắc storage cost vs debug value|
|5|**Security by default**|Mask sensitive data trước khi log, không phụ thuộc log pipeline|

### 1.5 Format output

- **Format**: JSON — mỗi dòng log là một JSON object (không có newline trong JSON).
- **Encoding**: UTF-8.
- **Output**: Console (stdout). Không ghi file trực tiếp — để log collector/agent thu thập từ stdout.
- **Max log size**: Một log entry không nên vượt quá **25KB** (Datadog recommended). Entry > 256KB sẽ bị truncate bởi hầu hết các log backend.

### 1.6 Log Level — Khái niệm nền tảng nhất

Log level là thứ **quan trọng nhất** cần hiểu đúng. Hiểu sai log level = alerting noise, miss critical errors, hoặc tốn tiền vô ích.

#### Bảng quy định

|Level|Khi nào dùng|Event suffix|Production|
|---|---|---|---|
|`DEBUG`|Bắt đầu operation, thông tin chi tiết|`*_START`|**Tắt** (hoặc sample ≤1%)|
|`INFO`|Operation thành công, business events quan trọng|`*_SUCCESS`|Bật|
|`WARN`|Vấn đề có thể recover, cần chú ý, client errors|`*_CLIENT_ERROR`, `*_RETRY`|Bật|
|`ERROR`|Lỗi server, exception, cần xử lý ngay|`*_FAILED`, `*_SERVER_ERROR`, `*_TIMEOUT`|Bật|

#### Flow chuẩn cho mọi operation

```
DEBUG: *_START              ← Bắt đầu operation
         ↓
    [Xử lý logic]
         ↓
    ┌─── Thành công ──→ INFO:  *_SUCCESS
    │
    ├─── Client lỗi ──→ WARN:  *_CLIENT_ERROR  (4xx, validation)
    │
    ├─── Server lỗi ──→ ERROR: *_SERVER_ERROR   (5xx, exception)
    │
    └─── Thất bại ────→ ERROR: *_FAILED         (generic failure)
```

#### 4 quy tắc vàng

1. **KHÔNG dùng ERROR cho client errors (4xx)**: 4xx là lỗi của client, không phải lỗi hệ thống → dùng WARN. Nếu dùng ERROR sẽ gây noise cho alerting.
2. **KHÔNG dùng INFO cho request start**: Request start là debug information → dùng DEBUG. Production không cần log mọi request start.
3. **ERROR phải actionable**: Mọi ERROR log đều phải là thứ cần ai đó xử lý. Nếu không cần xử lý → dùng WARN.
4. **WARN cho degraded but functional**: Rate limit hit, retry thành công, fallback activated, cache miss → WARN.

---

## Part 2: Schema — Cấu trúc JSON Log

### 2.1 Fields bắt buộc (Required)

Tất cả log **PHẢI** có 8 field sau. Thiếu bất kỳ field nào = log không hợp lệ:


> Ghi chú về message: Message phải truyền tải được what happened trong 1 câu ngắn. Tốt: "Payment failed: card declined". Xấu: "Error occurred".

2.2 Fields context (Recommended — thêm khi có)



2.3 Fields tracing (APM integration)

Nếu sử dụng Datadog APM hoặc OpenTelemetry:



> Tip: Nếu dùng Datadog APM, trace_id và span_id sẽ được tự động inject vào log context bởi Datadog SDK. Không cần set thủ công.

2.4 Fields error (khi có lỗi)



> Quy tắc stack_trace: Chỉ log stack_trace ở ERROR level và không phải production (trừ khi cần thiết cho critical issues). Stack trace có thể leak sensitive information. Ở production, cân nhắc chỉ log top N frames.

2.5 Fields body (opt-in — xem Part 4)



2.6 Hướng dẫn xác định giá trị các field

log_type — Phân loại theo loại operation

Chọn MỘT giá trị phù hợp nhất dựa trên loại operation đang thực hiện, không phải endpoint:



feature — Phân loại theo business domain

Quy tắc xác định (ưu tiên từ trên xuống):

1. Dựa vào URL path prefix (khuyến nghị cho API):
    
    
    /api/auth/*     → AUTH
    /api/users/*    → USER
    /api/orders/*   → ORDER
    /api/payments/* → PAYMENT

    
2. Dựa vào module/package name:
    
    
    com.example.auth.*    → AUTH
    services/order/*      → ORDER

    
3. Dựa vào business function (cho job, event):
    
    
    Xử lý thanh toán     → PAYMENT
    Gửi notification     → NOTIFICATION

    

Quy ước đặt tên: UPPERCASE, ngắn gọn 1-2 từ, không ký tự đặc biệt.

Mapping phổ biến:



event — Tên event cụ thể

Format: {ACTION}_{RESULT} hoặc {COMPONENT}_{ACTION}_{RESULT}

Actions phổ biến:



Result suffixes (quan trọng — thống nhất toàn bộ hệ thống):



Ví dụ event names:


# API events
API_REQUEST_START            → Bắt đầu xử lý HTTP request
API_REQUEST_SUCCESS          → Response 2xx
API_REQUEST_CLIENT_ERROR     → Response 4xx
API_REQUEST_SERVER_ERROR     → Response 5xx

# Business events
LOGIN_START / LOGIN_SUCCESS / LOGIN_FAILED
ORDER_CREATE_START / ORDER_CREATE_SUCCESS / ORDER_CREATE_FAILED

# External API
EXTERNAL_API_REQUEST_START / _SUCCESS / _FAILED / _TIMEOUT / _RETRY

# Job
JOB_START / JOB_SUCCESS / JOB_FAILED


2.7 Quy tắc đặt tên

Field names

- snake_case: user_id, http_method, duration_ms, error_type
- Ngoại lệ: @timestamp (convention của logging frameworks), dd.trace_id (Datadog convention)
- Units trong tên: Thêm unit suffix khi giá trị là số — duration_ms (not duration), body_size_bytes hoặc rút gọn req_body_size (document rõ unit là bytes)
- Không dùng dot notation cho custom fields: Dot notation (user.name) có thể gây conflict với nested object parsing trong Datadog/ELK. Dùng underscore (user_name). Chỉ dùng dot notation cho Datadog reserved attributes (dd.trace_id, error.message).

Event names

- UPPER_SNAKE_CASE: LOGIN_SUCCESS, ORDER_CREATE_FAILED

Feature names

- UPPERCASE: AUTH, USER, ORDER

Service names

- lowercase-with-hyphens: user-service, payment-gateway, order-service

Value types



> Lưu ý: Việc dùng string cho numbers là trade-off. Ưu điểm: consistent type, tránh JSON number precision issues. Nhược điểm: cần cast khi query. Nếu team prefer native types (number cho duration_ms, boolean cho flags), cần document rõ và consistent.


Part 2.5: LLM Logging — Log Input/Output cho LLM APIs

Phần này hướng dẫn cách log input/output khi gọi LLM APIs (OpenAI, vLLM, Anthropic, etc.). Áp dụng cho log_type: "external_api" khi target service là LLM.

2.5.1 Tại sao cần log LLM input/output?

LLM applications khác với REST APIs thông thường ở chỗ:
- Input không chỉ là parameters mà là messages (conversation history)
- Output là generated text — không predictable
- Token usage là metrics quan trọng cho cost tracking
- Prompt engineering — cần debug xem prompt nào tạo ra kết quả tốt/xấu

2.5.2 Input/Output Extraction Pattern


# Extract input (user message) từ messages array
def extract_user_message(messages: list) -> str:
    """Extract last user message from messages array."""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""

# Extract output từ response
def extract_model_response(response: dict) -> str:
    """Extract model response content."""
    choices = response.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    ret


# ============ req_body (rút gọn) ============
import json
req_body_json = json.dumps({
    "messages": request_body.get("messages", []),
    "model": request_body.get("model")
}, ensure_ascii=False)

# ============ res_body (chỉ lấy content) ============
res_body = randomized_content or original_content


Log output:



Lý do:

- req_body: Rút gọn - chỉ cần messages + model để debug, không cần temperature, max_tokens, top_p...
- res_body: Chỉ lấy content - vì response đầy đủ là {"choices":[{"message":{"content":"encouraging"}}]}, log hết là冗余 (redundant)
2.5.3 Fields khuyên dùng cho LLM Logging



2.5.4 Ví dụ JSON Log

Request (DEBUG level)


{
  "@timestamp": "2024-01-20T10:30:45.100+07:00",
  "level": "DEBUG",
  "message": "POST /v1/chat/completions - Request to vLLM",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_START",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "req_body": "{\"model\":\"Qwen/Qwen2.5-1.5B-Instruct-AWQ\",\"messages\":[{\"role\":\"system\",\"content\":\"Classify emotion...\"},{\"role\":\"user\",\"content\":\"Previous Pika Robot's Response:...\"}],\"temperature\":0,\"max_tokens\":5}",
  "req_body_size": "512",
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}


Response (INFO level)


{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "INFO",
  "message": "vLLM /v1/chat/completions completed in 350ms - 200 OK",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_SUCCESS",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "status_code": "200",
  "duration_ms": "350",

  "req_body": "{\"messages\":[{\"role\":\"user\",\"content\":\"...\"}]}",
  "input_content": "Previous Pika Robot's Response: {{previous_question}}\nNow   Pika Robot's Response need check: 「すごい」はベトナム語で「tuyệt vời」...",
  
  "res_body": "{\"choices\":[{\"message\":{\"content\":\"encouraging\"}}]}",
  "output_content": "encouraging",
  
  "prompt_tokens": "133",
  "completion_tokens": "4",
  "total_tokens": "137",
  
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}


Error Response (ERROR level)


{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "ERROR",
  "message": "vLLM /v1/chat/completions failed in 500ms - 500 Internal Server Error",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_SERVER_ERROR",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "status_code": "500",
  "duration_ms": "500",
  "error_type": "RuntimeError",
  "error_message": "CUDA out of memory",
  "input_content": "Previous Pika Robot's Response:...",
  "prompt_tokens": "133",
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}


2.5.5 Best Practices

1. Log full req_body/res_body — đúng chuẩn Part 2.5, có masking + truncation
2. Extract input_content/output_content — tiện query nhanh, debug dễ
3. Log token usage — quan trọng cho cost tracking
4. Mask sensitive data — user input có thể chứa PII
5. Truncate nếu quá dài — prompt có thể > 4KB

2.5.6 Cost Optimization



2.5.7 References

Best Practices từ các nguồn



- OpenAI Chat Completions API: https://platform.openai.com/docs/api-reference/chat
- vLLM OpenAI Compatible API: https://docs.vllm.ai/en/latest/
- Anthropic Claude API: https://docs.anthropic.com/en/api/messages
- LangSmith Tracing: https://docs.langchain.com/langsmith
- Datadog LLM Observability: https://docs.datadoghq.com/llm_observability/

2.5.8 Câu hỏi: 


mấy trường phụ như kiểu input_content, output_content, token, ... hay là lưu riêng vào 1 meta data nhỉ, để cho nó chuẩn log BRO NGHĨ SAO, CÁC TÀI LIỆU BEST PRACTICES NGHĨ SAO?


Dựa trên các tài liệu quốc tế:
 Best Practices: FLAT FIELDS (khuyến nghị)




Lý do nên dùng Flat Fields

1. Datadog/ELK query đơn giản hơn
    
    # Flat
    input_content:*"tuyệt vời"*
    
    # Nested  
    metadata.input_content:*"tuyệt vời"*

    
2. OpenTelemetry GenAI conventions cũng dùng flat fields
    
3. Datadog Standard Attributes — ưu tiên flat


Giữ flat như trong tài liệu hiện tại là đúng chuẩn rồi! Không cần nested object, cứ để flat như trong tài liệu là OK!
** 



Part 3: Log Types — Áp dụng cho từng loại service

Phần này cho bạn xem cụ thể mỗi loại service cần log những field gì và log trông như thế nào. Chỉ cần đọc phần liên quan đến service bạn đang làm.

3.1 API Logging (log_type: "api")

Dùng cho: HTTP request/response vào service.

Fields bổ sung



Events chuẩn



Ví dụ — Request Start (DEBUG)


{
  "@timestamp": "2024-01-20T10:30:45.100+07:00",
  "level": "DEBUG",
  "message": "POST /api/orders - Request received",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_START",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "content_type": "application/json",
  "req_body": "{\"product_id\":\"prod_123\",\"quantity\":2,\"payment\":{\"card_number\":\"****1234\",\"cvv\":\"***\"}}",
  "req_body_size": "89",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "correlation_id": "corr_xyz789",
  "service": "order-service",
  "environment": "prod"
}


Ví dụ — Request Success (INFO)


{
  "@timestamp": "2024-01-20T10:30:45.273+07:00",
  "level": "INFO",
  "message": "POST /api/orders - 201 Created in 150ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SUCCESS",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "status_code": "201",
  "duration_ms": "150",
  "res_body": "{\"order_id\":\"ord_789\",\"status\":\"created\"}",
  "res_body_size": "45",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "correlation_id": "corr_xyz789",
  "service": "order-service",
  "environment": "prod"
}


Ví dụ — Server Error (ERROR)


{
  "@timestamp": "2024-01-20T10:30:45.273+07:00",
  "level": "ERROR",
  "message": "POST /api/orders - 500 Internal Server Error in 89ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SERVER_ERROR",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "status_code": "500",
  "duration_ms": "89",
  "error_type": "NullPointerException",
  "error_message": "Cannot invoke method on null object at OrderService.create()",
  "stack_trace": "java.lang.NullPointerException: ...",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "service": "order-service",
  "environment": "prod"
}


> Pattern: message format cho API log: "{METHOD} {ENDPOINT} - {STATUS_CODE} {REASON} in {DURATION}ms" cho response, "{METHOD} {ENDPOINT} - Request received" cho request.


3.2 WebSocket Logging (log_type: "websocket")

Dùng cho: WebSocket connections và messages.

Fields bổ sung



Events chuẩn



Ví dụ


{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "WebSocket client connected to /ws/chat",
  "log_type": "websocket",
  "feature": "CHAT",
  "event": "WEBSOCKET_CONNECT_SUCCESS",
  "ws_event": "connect",
  "session_id": "ws_abc123",
  "endpoint": "/ws/chat",
  "user_id": "user_123",
  "service": "chat-service",
  "environment": "prod"
}



3.3 External API Logging (log_type: "external_api")

Dùng cho: Gọi API/service bên ngoài (third-party, internal microservice qua HTTP).

Fields bổ sung



Events chuẩn



Ví dụ


{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "INFO",
  "message": "Stripe charge API completed in 350ms - 200 OK",
  "log_type": "external_api",
  "feature": "PAYMENT",
  "event": "EXTERNAL_API_REQUEST_SUCCESS",
  "target_service": "stripe",
  "target_endpoint": "https://api.stripe.com/v1/charges",
  "http_method": "POST",
  "status_code": "200",
  "duration_ms": "350",
  "correlation_id": "corr_xyz789",
  "service": "payment-service",
  "environment": "prod"
}



3.4 gRPC Logging (log_type: "grpc")

Dùng cho: gRPC calls giữa các microservices.

Fields bổ sung



Events chuẩn



gRPC Status → Log Level mapping




3.5 Job Logging (log_type: "job")

Dùng cho: Background jobs, scheduled tasks, queue consumers.

Fields bổ sung



Events chuẩn



Ví dụ


{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "Job daily_report_generator completed in 45s - 1500/1500 items processed",
  "log_type": "job",
  "feature": "REPORT",
  "event": "JOB_SUCCESS",
  "job_name": "daily_report_generator",
  "job_id": "job_xyz789",
  "duration_ms": "45000",
  "items_processed": "1500",
  "items_total": "1500",
  "trigger_type": "scheduled",
  "service": "report-service",
  "environment": "prod"
}



3.6 Event Logging (log_type: "event")

Dùng cho: Message broker events (Kafka, RabbitMQ, etc.).

Fields bổ sung



Events chuẩn




🟡 POLICY — Quy định vận hành


Part 4: Security & Body Logging

4.1 Dữ liệu KHÔNG BAO GIỜ được log

Dù ở bất kỳ môi trường nào, các loại data sau TUYỆT ĐỐI KHÔNG xuất hiện trong log:

- Password (dù đã hash), secret key, API key (full)
- Full credit card number (chỉ giữ last 4)
- Personal documents: CMND/CCCD, passport number, SSN
- Full JWT token, session token, refresh token
- Private keys, certificates
- Health records, biometric data

4.2 Dữ liệu cần MASK



4.3 Log Injection Prevention

Khi log data từ user input, phải sanitize để tránh log injection (CWE-117):

- PHẢI serialize qua JSON library chuẩn: Không concatenate string thủ công. JSON library sẽ tự escape \n, \r, \", etc.
- KHÔNG bao giờ dùng string interpolation trực tiếp cho user input vào log message.
- Giới hạn kích thước user input trước khi log.


// ❌ XẤU - Dễ bị log injection
logger.info("User login: " + username);

// ✅ TỐT - Dùng parameterized logging
logger.info("User login attempt", Map.of("username", sanitize(username)));


4.4 OWASP Security Logging Requirements (A09:2025)

Theo OWASP Top 10 2025 — A09 Security Logging and Alerting Failures:

- Log mọi security events (cả success và failure): login attempts, authorization failures, input validation failures, password changes.
- Encode log data đúng cách để tránh log injection attacks.
- Không log quá ít (miss attacks) và không log quá nhiều (noise, cost, potential PII leak).
- Audit trail phải có integrity controls: append-only, không cho phép tamper.

4.5 Retention policy



4.6 Body Logging Policy

Tại sao cần policy riêng?



Quy tắc chung: Body logging là opt-in (chủ động bật), không phải mặc định.

Khi nào NÊN log body



Khi nào KHÔNG log body



Quy tắc Truncation



Quy tắc Masking trong Body

Body PHẢI được mask trước khi log — trong application code, KHÔNG phụ thuộc log pipeline.



> Implementation: Mask bằng cách traverse JSON keys (recursive cho nested objects). Dùng regex pattern matching trên key names. Ưu tiên dùng library có sẵn thay vì tự implement.

Configuration

Body logging nên bật/tắt qua config, không cần deploy lại:


# application.yml
logging:
  body:
    enabled: true
    max-size-bytes: 2048
    mask-patterns:
      - password
      - token
      - secret
      - api_key
      - otp
      - cvv
    skip-endpoints:
      - /auth/login
      - /auth/token
      - /health
      - /metrics
    skip-content-types:
      - multipart/form-data
      - application/octet-stream

---Part 5: Correlation Strategy

egy
5.1 Tại sao cần correlation?

Trong hệ thống microservices, một user action có thể trigger nhiều service calls. Correlation giúp trace toàn bộ flow từ entry point đến downstream services.

es.
5.2 ID hierarchy


correlation_id   ← Business flow ID, xuyên suốt từ client đến tất cả services
  └── request_id ← Unique per HTTP request, sinh tại mỗi service
        └── trace_id / span_id  ← APM tracing (auto-injected bởi Datadog/OTel)



5.3 Quy tắc sinh và truyền ID


ng|
5.4 Implementation pattern


Client → API Gateway (sinh correlation_id)
  → Service A (nhận correlation_id, sinh request_id_A)
    → Service B (nhận correlation_id, sinh request_id_B)
    → Service C (nhận correlation_id, sinh request_id_C)


Mọi log trong flow đều có cùng ccorrelation_ido → dễ dàng query tất cả log liên quan:


Datadog query
@correlation_id:corr_xyz789



5.5 Fallback

Nếu request không có gX-Correlation-IDo header, service PHẢI tự sinh một correlation_id mới (không để trống).


--🟢 ADVANCED — Nâng cao


---Part 6: Production Operations

> Phần này dành cho khi hệ thống đã chạy production, có traffic thực tế, và bạn cần tối ưu cost, performance, alerting.

ng.
6.1 Log Sampling Strategy

egy

Tại sao cần sampling?

Một service xử lý 10,000 req/s sinh ~500 bytes/log → og430GB log/ngày/n chỉ từ 1 endpoint. Sampling giúp giảm volume 90-99% mà vẫn giữ được khả năng debug.

ug.

Nguyên tắc vàng

1. 

KHÔNG BAO GIỜ sample ERROR logs l: Mọi error đều phải được giữ 100%.
2. .
KHÔNG BAO GIỜ sample WARN logs l: Warnings là early signals, phải giữ 100%.
3. .
Sample INFO logs l: Tùy volume — giữ 10-100%.
4. .
Sample aggressively DEBUG logs l: Giữ 1-5% (hoặc tắt hẳn ở production).
5. .
Luôn giữ slow requestsue: Requests có sduration_ms > thresholds luôn được log đầy đủ.

đủ.

Level-based Sampling (khuyến nghị)


0%|

Tail-based Sampling (nâng cao)

Buffer log events cho mỗi request, sau khi request hoàn thành:

- Nếu có error → giữ TẤT CẢ logs của request đó (kể cả DEBUG)
- Nếu slow → giữ tất cả
- Nếu normal → sample hoặc drop DEBUG/INFO

> Tail-based sampling khó implement hơn nhưng cho kết quả debug tốt hơn nhiều vì bạn có full context cho error cases.

es.

Adaptive Sampling (cho high-traffic services)

Tự động điều chỉnh sample rate dựa trên traffic volume:

- Traffic bình thường: sample 50% INFO
- Traffic spike (>2x baseline): sample 10% INFO
- Traffic extreme (>5x baseline): sample 1% INFO

NFO

Implementation notes

- s
Include sample rate trong logg : Khi emit sampled log, thêm field i_sample_rate: "0.1"" để analysis tools có thể extrapolate.
- e.Consistent samplingpl: Dùng hash-based sampling (hash hrequest_ids) thay vì random — đảm bảo related logs cùng được giữ hoặc cùng bị drop.

op.
6.2 Cost Optimization

ion

Tiered Retention Strategy


ve|

Kỹ thuật giảm log volume

1. 

Tắt DEBUG ở productionct: Quick win lớn nhất — giảm 50-80% volume.
2. .
Không log health checkshe: s/healthe, t/metricst, c/readyr gọi mỗi vài giây → volume rất lớn, giá trị debug = 0.
3. .
Sample INFO logs l: Giữ 10-50% tuỳ endpoint importance.
4. .
Deduplicate errorsrr: Cùng một error lặp lại 1000 lần/phút → log lần đầu + counter, không log 1000 entries.
5. .
Strip null fieldsie: Không include field nếu value là null/empty — tiết kiệm 20-30% per entry.
6. .
Compact messagess: Message ngắn gọn, không verbose.
7. .
Metrics from logs l: Cho high-volume success cases, generate metrics (count, latency percentiles) thay vì giữ raw logs.

gs.

Cost estimation guide


Logs/day = requests/second × 86400 × (1 - sample_drop_rate)
Size/day = Logs/day × avg_bytes_per_entry

Ví dụ: 1000 req/s, sample 10% INFO, avg 500 bytes:
  ERROR/WARN (5%): 1000 × 0.05 × 86400 × 500 = 2.16 GB/day
  INFO (sampled 10%): 1000 × 0.95 × 0.1 × 86400 × 500 = 4.1 GB/day
  Total: ~6.3 GB/day

So với không sample: 1000 × 86400 × 500 = 43.2 GB/day
→ Tiết kiệm ~85% storage cost.



6.3 Performance Guidelines

nes

Async logging

- g
BẮT BUỘC B dùng async logging ở production. Logging KHÔNG được block application thread.
- Java: dùng dAsyncAppendere (Logback) hoặc hAsyncLoggero (Log4j2).
- Python: dùng dQueueHandlern hoặc background thread.
- Node.js: Hầu hết logging libraries (Pino, Winston) đã async by default.

lt.

Batching

- Log collector (Datadog Agent, Fluentd, Vector) nên batch logs trước khi gửi đến backend.
- Batch size: 5MB hoặc 5 giây (whichever comes first).

t).

Body serialization overhead

- Body masking + truncation ticó overheadrh: ~1-5ms per request (tuỳ body size).
- Nếu body logging gây latency đáng kể (>5ms), cân nhắc:
    - Chỉ log body khi  status_code >= 400=
    - Dùng async processing cho body masking
    - Cache compiled regex patterns cho masking

ing

Tránh log trong hot path

- h
KHÔNG log ở mỗi iterationat trong loops xử lý batch data. Log tổng kết sau khi xong.
- g.KHÔNG log binary data d: Encode base64 rồi log binary content là wasteful.
- l.Giới hạn stack trace depthde: Nếu log stack trace, chỉ giữ top 5-10 frames ở production.

on.

Benchmarks target


on|
6.4 Alerting Guidelines

nes

Alert dựa trên structured log fields


ng|

Nguyên tắc alerting

- g
Alert trên ERROR, không phải WARN W: WARN là informational, ERROR cần action. Chỉ alert WARN khi pattern indicates systemic issue.
- e.Percentage-based thresholds, không phải absolute countco: terror_rate > 5%  tốt hơn  error_count > 100> (vì traffic thay đổi).
- ).Tránh alert fatigueti: Mỗi alert phải có runbook hoặc action rõ ràng. Nếu team bỏ qua alert liên tục → alert đó cần re-evaluate.


---Part 7: Ecosystem Integration

ion
7.1 OpenTelemetry Alignment

ent

Tại sao align với OTel?

OpenTelemetry (OTel) là industry standard cho observability. ECS (Elastic Common Schema) đã merge vào OTel semantic conventions từ 2023. Align với OTel đảm bảo:

- Vendor-agnostic: dễ migrate giữa Datadog, ELK, Grafana, etc.
- Cross-signal correlation: logs ↔ traces ↔ metrics cùng schema.
- Future-proof: ecosystem đang converge về OTel.

el.

Field mapping: Custom → OTel → Datadog


d|

Migration path

1. 

Phase 1as: Giữ custom names, thêm Datadog pipeline remapper để map sang standard attributes.
2. .
Phase 2as: Service mới dùng OTel SDK — tự động emit đúng semantic conventions.
3. .
Phase 3as: Service cũ migrate sang OTel naming khi refactor.


--📎 APPENDIX


---Appendix A: Checklist

ist
A.1 Trước khi implement

ent

 Xác định đlog_type_, pfeaturea, và danh sách events cần log cho service.
ice.
 Xác định danh sách endpoints KHÔNG log body (auth, sensitive endpoints).
ts).
 Xác định content-types cần skip (binary, multipart).
rt).
 Xác định giới hạn truncation phù hợp với môi trường.
ờng.
 List sensitive field patterns cần mask trong body.
ody.
 Xác định sampling strategy cho production.
ion.
 Thiết lập correlation_id propagation pattern.

rn.
A.2 Trong khi implement

ent

 Tất cả log đều có đủ ó 8 required fieldsie (Part 2, Section 2.1).
.1).
  duration_mso có trong mọi response/complete events.
nts.
 Error logs có serror_type_ và error_messages.
ge.
  req_body_ đã được mask trước khi log.
log.
 Body bị skip với binary content-types.
pes.
  req_body_truncated: "true"t được set khi body bị cắt.
cắt.
  req_body_size_ luôn được log (kể cả khi body bị skip).
ip).
 Auth endpoints KHÔNG log body.
ody.
 Body logging có thể bật/tắt qua config.
fig.
 4xx responses dùng WARN level, KHÔNG dùng ERROR.
ROR.
 Logging là async, KHÔNG block application thread.
ead.
  correlation_ido được propagate qua header và include trong mọi log.
log.
 User input được serialize qua JSON library (chống log injection).

n).
A.3 Sau khi implement

ent

 Test log output đúng JSON format (mỗi dòng là valid JSON).
ON).
 Test với body chứa password/token → verify đã bị mask.
ask.
 Test với file upload → verify body bị skip.
kip.
 Test với large body (>2KB) → verify truncation + flag.
lag.
 Test auth endpoints → verify không log body.
ody.
 Test error case → verify có error_type, error_message, stack_trace.
ace.
 Test correlation_id → verify consistent across service calls.
lls.
 Verify log có thể parse bởi Datadog/ELK (test trên dev/staging).
ng).
 Review log volume estimate → confirm sampling strategy hợp lý.
 lý.
 Setup alerts dựa trên structured fields.


---Appendix B: Quick Reference

nce
Log Level


DEBUG → Bắt đầu (START)            → Production: TẮT hoặc sample 1%
INFO  → Thành công (_SUCCESS)        → Production: BẬT (sample nếu cần)
WARN  → Cảnh báo, client error       → Production: BẬT (100%)
ERROR → Lỗi server, cần xử lý       → Production: BẬT (100%, KHÔNG sample)



Event Naming


Format: {ACTION}_{RESULT} hoặc {COMPONENT}_{ACTION}_{RESULT}
Suffixes: _START | _SUCCESS | _CLIENT_ERROR | _SERVER_ERROR | _FAILED | _TIMEOUT | _RETRY



Body Logging Decision Tree


Request đến
  → Auth endpoint? → SKIP body
  → Binary content-type? → SKIP body
  → Body > 1MB? → SKIP body, log size only
  → Error (4xx/5xx)? → LOG body (masked, truncated)
  → Mutation (POST/PUT/PATCH/DELETE)? → LOG body (masked, truncated)
  → GET success? → SKIP body



Sampling Decision Tree


Log level?
  ERROR → KEEP 100%
  WARN  → KEEP 100%
  INFO  → SAMPLE 10-50%
  DEBUG → DROP (production) hoặc SAMPLE 1%



Template JSON tối thiểu


{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "POST /api/orders - 201 Created in 150ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SUCCESS",
  "service": "order-service",
  "environment": "prod"
}



Feature mapping


/auth/*     → AUTH          /notifications/* → NOTIFICATION
/users/*    → USER          /reports/*       → REPORT
/orders/*   → ORDER         /admin/*         → ADMIN
/payments/* → PAYMENT       /health          → SYSTEM
/products/* → PRODUCT



Datadog Standard Attributes mapping


service     → service (reserved)     error_type     → error.kind
environment → env (reserved)         error_message  → error.message
version     → version (reserved)     stack_trace    → error.stack
http_method → http.method            client_ip      → network.client.ip
status_code → http.status_code       user_id   
→ usr.


Tài liệu tham khảo

Industry Standards

1. OpenTelemetry Semantic Conventions — Industry standard cho field naming, là nền tảng cho tất cả log schema hiện đại.
2. OpenTelemetry Semantic Conventions for Logs
3. Elastic Common Schema (ECS) — Đã merge vào OTel semantic conventions từ 2023.
4. Datadog Standard Attributes — Mapping chuẩn nếu dùng Datadog.
5. Datadog Unified Service Tagging

Security

6. OWASP Logging Cheat Sheet — Must-read cho security logging requirements.
7. OWASP Logging Vocabulary — Standard event keywords cho security events.
8. OWASP Top 10 2025 — A09 Security Logging and Alerting Failures
9. OWASP Proactive Controls — C9: Implement Logging and Monitoring

Best Practices
ông hợp lệ:

|Field|Type|Mô tả|Ví dụ|
|---|---|---|---|
|`@timestamp`|string|Thời gian, ISO 8601 với timezone|`"2024-01-20T10:30:45.123+07:00"`|
|`level`|string|Log level|`"DEBUG"`, `"INFO"`, `"WARN"`, `"ERROR"`|
|`message`|string|Mô tả ngắn gọn, dễ đọc, actionable|`"User login successful"`|
|`log_type`|string|Phân loại theo loại operation|`"api"`, `"websocket"`, `"external_api"`, `"job"`|
|`feature`|string|Tính năng/business domain|`"AUTH"`, `"PAYMENT"`, `"ORDER"`|
|`event`|string|Tên event cụ thể|`"LOGIN_SUCCESS"`, `"ORDER_CREATED"`|
|`service`|string|Tên service (Datadog reserved)|`"user-service"`, `"payment-service"`|
|`environment`|string|Môi trường (Datadog reserved: `env`)|`"dev"`, `"staging"`, `"prod"`|

> **Ghi chú về `message`**: Message phải truyền tải được **what happened** trong 1 câu ngắn. Tốt: `"Payment failed: card declined"`. Xấu: `"Error occurred"`.

### 2.2 Fields context (Recommended — thêm khi có)

|Field|Type|Mô tả|
|---|---|---|
|`user_id`|string|ID người dùng đang thực hiện action|
|`request_id`|string|ID duy nhất của request (UUID), sinh tại entry point|
|`session_id`|string|Session ID (WebSocket, HTTP session)|
|`correlation_id`|string|ID để trace across services (xem Part 5)|
|`version`|string|Version của service (Datadog reserved)|

### 2.3 Fields tracing (APM integration)

Nếu sử dụng Datadog APM hoặc OpenTelemetry:

|Field|Type|Mô tả|Mapping|
|---|---|---|---|
|`dd.trace_id`|string|Datadog trace ID|Datadog APM|
|`dd.span_id`|string|Datadog span ID|Datadog APM|
|`trace_id`|string|Generic trace ID|OpenTelemetry `trace_id`|
|`span_id`|string|Generic span ID|OpenTelemetry `span_id`|

> **Tip**: Nếu dùng Datadog APM, trace_id và span_id sẽ được tự động inject vào log context bởi Datadog SDK. Không cần set thủ công.

### 2.4 Fields error (khi có lỗi)

|Field|Type|Mô tả|Datadog mapping|
|---|---|---|---|
|`error_type`|string|Tên exception/error class|`error.kind`|
|`error_message`|string|Error message|`error.message`|
|`stack_trace`|string|Stack trace (chỉ cho ERROR level)|`error.stack`|

> **Quy tắc stack_trace**: Chỉ log stack_trace ở **ERROR** level và **không phải production** (trừ khi cần thiết cho critical issues). Stack trace có thể leak sensitive information. Ở production, cân nhắc chỉ log top N frames.

### 2.5 Fields body (opt-in — xem Part 4)

|Field|Type|Mô tả|
|---|---|---|
|`query_params`|string|Query string (đã lọc sensitive params), ví dụ `"page=1&size=20"`|
|`content_type`|string|Content-Type của request|
|`req_body`|string|Request body sau khi mask + truncate|
|`req_body_size`|string|Kích thước request body (bytes)|
|`req_body_truncated`|string|`"true"` nếu body bị cắt bớt|
|`res_body`|string|Response body sau khi mask + truncate|
|`res_body_size`|string|Kích thước response body (bytes)|
|`res_body_truncated`|string|`"true"` nếu body bị cắt bớt|

### 2.6 Hướng dẫn xác định giá trị các field

#### `log_type` — Phân loại theo loại operation

Chọn **MỘT** giá trị phù hợp nhất dựa trên **loại operation đang thực hiện**, không phải endpoint:

|log_type|Khi nào dùng|Ví dụ|
|---|---|---|
|`api`|HTTP request/response đến service|REST API, GraphQL|
|`websocket`|WebSocket connection và message|Real-time chat, notifications|
|`external_api`|Gọi API/service bên ngoài|Call OpenAI, payment gateway, third-party|
|`grpc`|gRPC calls giữa microservices|Internal service-to-service|
|`job`|Background job, scheduled task, queue consumer|Cron job, Kafka consumer|
|`event`|Event publish/consume (message broker)|Kafka produce/consume, RabbitMQ|
|`database`|Database operations (chỉ khi cần debug)|Slow query logging|
|`cache`|Cache operations (chỉ khi cần debug)|Redis get/set miss/hit|

#### `feature` — Phân loại theo business domain

**Quy tắc xác định** (ưu tiên từ trên xuống):

1. **Dựa vào URL path prefix** (khuyến nghị cho API):
    
    ```
    /api/auth/*     → AUTH
    /api/users/*    → USER
    /api/orders/*   → ORDER
    /api/payments/* → PAYMENT
    ```
    
2. **Dựa vào module/package name**:
    
    ```
    com.example.auth.*    → AUTH
    services/order/*      → ORDER
    ```
    
3. **Dựa vào business function** (cho job, event):
    
    ```
    Xử lý thanh toán     → PAYMENT
    Gửi notification     → NOTIFICATION
    ```
    

**Quy ước đặt tên**: UPPERCASE, ngắn gọn 1-2 từ, không ký tự đặc biệt.

**Mapping phổ biến**:

|Path Pattern|Feature|
|---|---|
|`/auth/*`, `/login`, `/logout`, `/token`|`AUTH`|
|`/users/*`, `/profile/*`|`USER`|
|`/orders/*`, `/checkout/*`|`ORDER`|
|`/payments/*`, `/transactions/*`|`PAYMENT`|
|`/products/*`, `/catalog/*`|`PRODUCT`|
|`/notifications/*`|`NOTIFICATION`|
|`/reports/*`, `/analytics/*`|`REPORT`|
|`/admin/*`|`ADMIN`|
|`/health`, `/metrics`, `/ready`|`SYSTEM`|

#### `event` — Tên event cụ thể

**Format**: `{ACTION}_{RESULT}` hoặc `{COMPONENT}_{ACTION}_{RESULT}`

**Actions phổ biến**:

|Action|Mô tả|
|---|---|
|`CREATE`|Tạo mới resource|
|`UPDATE`|Cập nhật resource|
|`DELETE`|Xóa resource|
|`GET`|Lấy thông tin|
|`LIST`|Lấy danh sách|
|`LOGIN`|Đăng nhập|
|`LOGOUT`|Đăng xuất|
|`SEND`|Gửi (email, notification)|
|`PROCESS`|Xử lý|
|`VALIDATE`|Kiểm tra, xác thực|

**Result suffixes** (quan trọng — thống nhất toàn bộ hệ thống):

|Result|Mô tả|Log Level|Khi nào dùng|
|---|---|---|---|
|`_START`|Bắt đầu operation|DEBUG|Entry point của mọi operation|
|`_SUCCESS`|Thành công|INFO|Operation hoàn thành không lỗi|
|`_CLIENT_ERROR`|Lỗi từ phía client|WARN|HTTP 4xx, invalid input, validation fail|
|`_SERVER_ERROR`|Lỗi từ phía server|ERROR|HTTP 5xx, unhandled exception|
|`_FAILED`|Thất bại (generic)|ERROR|Non-HTTP failures (job fail, event processing fail)|
|`_TIMEOUT`|Timeout|ERROR|External call timeout, processing timeout|
|`_RETRY`|Đang retry|WARN|Retry attempt (chưa phải final failure)|

**Ví dụ event names**:

```
# API events
API_REQUEST_START            → Bắt đầu xử lý HTTP request
API_REQUEST_SUCCESS          → Response 2xx
API_REQUEST_CLIENT_ERROR     → Response 4xx
API_REQUEST_SERVER_ERROR     → Response 5xx

# Business events
LOGIN_START / LOGIN_SUCCESS / LOGIN_FAILED
ORDER_CREATE_START / ORDER_CREATE_SUCCESS / ORDER_CREATE_FAILED

# External API
EXTERNAL_API_REQUEST_START / _SUCCESS / _FAILED / _TIMEOUT / _RETRY

# Job
JOB_START / JOB_SUCCESS / JOB_FAILED
```

### 2.7 Quy tắc đặt tên

#### Field names

- **snake_case**: `user_id`, `http_method`, `duration_ms`, `error_type`
- **Ngoại lệ**: `@timestamp` (convention của logging frameworks), `dd.trace_id` (Datadog convention)
- **Units trong tên**: Thêm unit suffix khi giá trị là số — `duration_ms` (not `duration`), `body_size_bytes` hoặc rút gọn `req_body_size` (document rõ unit là bytes)
- **Không dùng dot notation cho custom fields**: Dot notation (`user.name`) có thể gây conflict với nested object parsing trong Datadog/ELK. Dùng underscore (`user_name`). Chỉ dùng dot notation cho Datadog reserved attributes (`dd.trace_id`, `error.message`).

#### Event names

- **UPPER_SNAKE_CASE**: `LOGIN_SUCCESS`, `ORDER_CREATE_FAILED`

#### Feature names

- **UPPERCASE**: `AUTH`, `USER`, `ORDER`

#### Service names

- **lowercase-with-hyphens**: `user-service`, `payment-gateway`, `order-service`

#### Value types

|Type|Convention|Ví dụ|Lý do|
|---|---|---|---|
|Boolean|String `"true"` / `"false"`|`"is_timeout": "true"`|Consistent type across all fields|
|Number|**String format**|`"duration_ms": "150"`|Tránh precision issues, consistent parsing|
|Null/Empty|**Không include field**|(bỏ qua field)|Tiết kiệm storage, tránh null handling|
|Timestamp|ISO 8601 với timezone|`"2024-01-20T10:30:45.123+07:00"`|Unambiguous, sortable|
|Arrays|**Không dùng**|—|Flatten thành separate fields hoặc comma-separated string|

> **Lưu ý**: Việc dùng string cho numbers là trade-off. Ưu điểm: consistent type, tránh JSON number precision issues. Nhược điểm: cần cast khi query. Nếu team prefer native types (number cho duration_ms, boolean cho flags), cần document rõ và consistent.

---

## Part 2.5: LLM Logging — Log Input/Output cho LLM APIs

Phần này hướng dẫn cách log input/output khi gọi LLM APIs (OpenAI, vLLM, Anthropic, etc.). Áp dụng cho `log_type: "external_api"` khi target service là LLM.

### 2.5.1 Tại sao cần log LLM input/output?

LLM applications khác với REST APIs thông thường ở chỗ:
- **Input không chỉ là parameters** mà là `messages` (conversation history)
- **Output là generated text** — không predictable
- **Token usage** là metrics quan trọng cho cost tracking
- **Prompt engineering** — cần debug xem prompt nào tạo ra kết quả tốt/xấu

### 2.5.2 Input/Output Extraction Pattern

```python
# Extract input (user message) từ messages array
def extract_user_message(messages: list) -> str:
    """Extract last user message from messages array."""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""

# Extract output từ response
def extract_model_response(response: dict) -> str:
    """Extract model response content."""
    choices = response.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""
```


```python

# ============ req_body (rút gọn) ============
import json
req_body_json = json.dumps({
    "messages": request_body.get("messages", []),
    "model": request_body.get("model")
}, ensure_ascii=False)

# ============ res_body (chỉ lấy content) ============
res_body = randomized_content or original_content

```
**Log output:**

| Field            | Value                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| `req_body`       | `{"messages":[{"role":"user","content":"Previous Pika Robot's..."}],"model":"Qwen/Qwen2.5-0.5B-Instruct"}` |
| `input_content`  | `Previous Pika Robot's Response: ...` (extract từ messages)                                                |
| `res_body`       | `encouraging`                                                                                              |
| `output_content` | `encouraging`                                                                                              |

**Lý do:**

- `req_body`: Rút gọn - chỉ cần `messages` + `model` để debug, không cần `temperature`, `max_tokens`, `top_p`...
- `res_body`: Chỉ lấy `content` - vì response đầy đủ là `{"choices":[{"message":{"content":"encouraging"}}]}`, log hết là冗余 (redundant)
### 2.5.3 Fields khuyên dùng cho LLM Logging

|Field|Type|Mô tả|Required|
|---|---|---|---|
|`model`|string|Tên model|`Khuyến nghị`|
|`req_body`|string|Full request JSON (đã mask)|`Có`|
|`res_body`|string|Full response JSON (đã mask)|`Có`|
|`input_content`|string|Extracted user message|Khuyến nghị|
|`output_content`|string|Extracted model response|Khuyến nghị|
|`prompt_tokens`|string|Input tokens (từ usage)|Khuyến nghị|
|`completion_tokens`|string|Output tokens (từ usage)|Khuyến nghị|
|`total_tokens`|string|Total tokens (từ usage)|Khuyến nghị|

### 2.5.4 Ví dụ JSON Log

#### Request (DEBUG level)

```json
{
  "@timestamp": "2024-01-20T10:30:45.100+07:00",
  "level": "DEBUG",
  "message": "POST /v1/chat/completions - Request to vLLM",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_START",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "req_body": "{\"model\":\"Qwen/Qwen2.5-1.5B-Instruct-AWQ\",\"messages\":[{\"role\":\"system\",\"content\":\"Classify emotion...\"},{\"role\":\"user\",\"content\":\"Previous Pika Robot's Response:...\"}],\"temperature\":0,\"max_tokens\":5}",
  "req_body_size": "512",
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}
```

#### Response (INFO level)

```json
{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "INFO",
  "message": "vLLM /v1/chat/completions completed in 350ms - 200 OK",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_SUCCESS",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "status_code": "200",
  "duration_ms": "350",

  "req_body": "{\"messages\":[{\"role\":\"user\",\"content\":\"...\"}]}",
  "input_content": "Previous Pika Robot's Response: {{previous_question}}\nNow   Pika Robot's Response need check: 「すごい」はベトナム語で「tuyệt vời」...",
  
  "res_body": "{\"choices\":[{\"message\":{\"content\":\"encouraging\"}}]}",
  "output_content": "encouraging",
  
  "prompt_tokens": "133",
  "completion_tokens": "4",
  "total_tokens": "137",
  
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}
```

#### Error Response (ERROR level)

```json
{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "ERROR",
  "message": "vLLM /v1/chat/completions failed in 500ms - 500 Internal Server Error",
  "log_type": "external_api",
  "feature": "LLM",
  "event": "EXTERNAL_API_REQUEST_SERVER_ERROR",
  "target_service": "vllm",
  "target_endpoint": "http://vllm:8000/v1/chat/completions",
  "http_method": "POST",
  "model": "Qwen/Qwen2.5-1.5B-Instruct-AWQ",
  "status_code": "500",
  "duration_ms": "500",
  "error_type": "RuntimeError",
  "error_message": "CUDA out of memory",
  "input_content": "Previous Pika Robot's Response:...",
  "prompt_tokens": "133",
  "request_id": "req_abc456",
  "service": "emotion-service",
  "environment": "prod"
}
```

### 2.5.5 Best Practices

1. **Log full req_body/res_body** — đúng chuẩn Part 2.5, có masking + truncation
2. **Extract input_content/output_content** — tiện query nhanh, debug dễ
3. **Log token usage** — quan trọng cho cost tracking
4. **Mask sensitive data** — user input có thể chứa PII
5. **Truncate nếu quá dài** — prompt có thể > 4KB

### 2.5.6 Cost Optimization

|Loại log|Production|Staging|Dev|
|--------|----------|-------|-----|
|Full req_body/res_body|Error only|✅|✅|
|input_content/output_content|Error only|✅|✅|
|token usage|✅ Always|✅|✅|

### 2.5.7 References

Best Practices từ các nguồn

| Nguồn                   | Cách log                                              |
| ----------------------- | ----------------------------------------------------- |
| **LangSmith**           | Log full `messages` + `response.content`              |
| **OpenAI SDK**          | Log `usage.prompt_tokens`, `usage.completion_tokens`  |
| **Datadog integration** | Log `messages` as `prompt`, `content` as `completion` |

- OpenAI Chat Completions API: https://platform.openai.com/docs/api-reference/chat
- vLLM OpenAI Compatible API: https://docs.vllm.ai/en/latest/
- Anthropic Claude API: https://docs.anthropic.com/en/api/messages
- LangSmith Tracing: https://docs.langchain.com/langsmith
- Datadog LLM Observability: https://docs.datadoghq.com/llm_observability/

### 2.5.8 Câu hỏi: 

```
mấy trường phụ như kiểu input_content, output_content, token, ... hay là lưu riêng vào 1 meta data nhỉ, để cho nó chuẩn log BRO NGHĨ SAO, CÁC TÀI LIỆU BEST PRACTICES NGHĨ SAO?
```

Dựa trên các tài liệu quốc tế:
 Best Practices: **FLAT FIELDS (khuyến nghị)**

|Cách|Ưu điểm|Nhược điểm|
|---|---|---|
|**Flat (top-level)**|✅ Query dễ: `input_content:*`|—|
|**Nested (metadata.*)**|✅ Gọn gàng|❌ Query phức tạp: `metadata.input_content:*`|

---

#### Lý do nên dùng Flat Fields

1. **Datadog/ELK query đơn giản hơn**
    ```
    # Flat
    input_content:*"tuyệt vời"*
    
    # Nested  
    metadata.input_content:*"tuyệt vời"*
    ```
    
2. **OpenTelemetry GenAI conventions** cũng dùng flat fields
    
3. **Datadog Standard Attributes** — ưu tiên flat


**Giữ flat như trong tài liệu hiện tại là đúng chuẩn rồi! Không cần nested object, cứ để flat như trong tài liệu là OK!
** 

|Field|Nên để ở đâu|
|---|---|
|`input_content`|**Flat** (top-level)|
|`output_content`|**Flat**|
|`prompt_tokens`|**Flat**|
|`completion_tokens`|**Flat**|
|`total_tokens`|**Flat**|

## Part 3: Log Types — Áp dụng cho từng loại service

Phần này cho bạn xem **cụ thể** mỗi loại service cần log những field gì và log trông như thế nào. Chỉ cần đọc phần liên quan đến service bạn đang làm.

### 3.1 API Logging (`log_type: "api"`)

**Dùng cho**: HTTP request/response vào service.

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`http_method`|string|Có|`"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, `"PATCH"`|
|`endpoint`|string|Có|URL path (không include query string, không include host)|
|`status_code`|string|Có*|HTTP status code (*cho response log)|
|`duration_ms`|string|Có*|Thời gian xử lý ms (*cho response log)|
|`client_ip`|string|Không|IP client (có thể mask nếu cần privacy)|
|`user_agent`|string|Không|User agent string|
|`content_type`|string|Không|Content-Type của request|
|`query_params`|string|Không|Query parameters (đã lọc sensitive)|
|`req_body`|string|Không*|Xem Part 4 — Body Logging Policy|
|`req_body_size`|string|Không|Size of request body in bytes|
|`req_body_truncated`|string|Không|`"true"` nếu body bị truncate|
|`res_body`|string|Không*|Xem Part 4 — Body Logging Policy|
|`res_body_size`|string|Không|Size of response body in bytes|
|`res_body_truncated`|string|Không|`"true"` nếu body bị truncate|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`API_REQUEST_START`|DEBUG|Nhận request|
|`API_REQUEST_SUCCESS`|INFO|Response 2xx|
|`API_REQUEST_CLIENT_ERROR`|WARN|Response 4xx|
|`API_REQUEST_SERVER_ERROR`|ERROR|Response 5xx hoặc unhandled exception|

#### Ví dụ — Request Start (DEBUG)

```json
{
  "@timestamp": "2024-01-20T10:30:45.100+07:00",
  "level": "DEBUG",
  "message": "POST /api/orders - Request received",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_START",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "content_type": "application/json",
  "req_body": "{\"product_id\":\"prod_123\",\"quantity\":2,\"payment\":{\"card_number\":\"****1234\",\"cvv\":\"***\"}}",
  "req_body_size": "89",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "correlation_id": "corr_xyz789",
  "service": "order-service",
  "environment": "prod"
}
```

#### Ví dụ — Request Success (INFO)

```json
{
  "@timestamp": "2024-01-20T10:30:45.273+07:00",
  "level": "INFO",
  "message": "POST /api/orders - 201 Created in 150ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SUCCESS",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "status_code": "201",
  "duration_ms": "150",
  "res_body": "{\"order_id\":\"ord_789\",\"status\":\"created\"}",
  "res_body_size": "45",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "correlation_id": "corr_xyz789",
  "service": "order-service",
  "environment": "prod"
}
```

#### Ví dụ — Server Error (ERROR)

```json
{
  "@timestamp": "2024-01-20T10:30:45.273+07:00",
  "level": "ERROR",
  "message": "POST /api/orders - 500 Internal Server Error in 89ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SERVER_ERROR",
  "http_method": "POST",
  "endpoint": "/api/orders",
  "status_code": "500",
  "duration_ms": "89",
  "error_type": "NullPointerException",
  "error_message": "Cannot invoke method on null object at OrderService.create()",
  "stack_trace": "java.lang.NullPointerException: ...",
  "user_id": "user_123",
  "request_id": "req_abc456",
  "service": "order-service",
  "environment": "prod"
}
```

> **Pattern**: message format cho API log: `"{METHOD} {ENDPOINT} - {STATUS_CODE} {REASON} in {DURATION}ms"` cho response, `"{METHOD} {ENDPOINT} - Request received"` cho request.

---

### 3.2 WebSocket Logging (`log_type: "websocket"`)

**Dùng cho**: WebSocket connections và messages.

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`ws_event`|string|Có|`"connect"`, `"disconnect"`, `"message_received"`, `"message_sent"`, `"error"`|
|`session_id`|string|Có|WebSocket session ID|
|`endpoint`|string|Có|WS endpoint path|
|`connection_duration_ms`|string|Không|Thời gian kết nối tổng (cho disconnect)|
|`close_code`|string|Không|WebSocket close code (1000, 1001, ...)|
|`close_reason`|string|Không|Close reason string|
|`message_type`|string|Không|`"text"`, `"binary"`|
|`message_size`|string|Không|Kích thước message (bytes)|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`WEBSOCKET_CONNECT_SUCCESS`|INFO|Client kết nối thành công|
|`WEBSOCKET_DISCONNECT`|INFO|Client ngắt kết nối (normal close)|
|`WEBSOCKET_MESSAGE_RECEIVED`|DEBUG|Nhận message từ client|
|`WEBSOCKET_MESSAGE_SENT`|DEBUG|Gửi message tới client|
|`WEBSOCKET_ERROR`|ERROR|Lỗi connection hoặc message processing|

#### Ví dụ

```json
{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "WebSocket client connected to /ws/chat",
  "log_type": "websocket",
  "feature": "CHAT",
  "event": "WEBSOCKET_CONNECT_SUCCESS",
  "ws_event": "connect",
  "session_id": "ws_abc123",
  "endpoint": "/ws/chat",
  "user_id": "user_123",
  "service": "chat-service",
  "environment": "prod"
}
```

---

### 3.3 External API Logging (`log_type: "external_api"`)

**Dùng cho**: Gọi API/service bên ngoài (third-party, internal microservice qua HTTP).

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`target_service`|string|Có|Tên service đích (ví dụ: `"stripe"`, `"openai"`, `"user-service"`)|
|`target_endpoint`|string|Có|URL đích (mask sensitive parts nếu cần)|
|`http_method`|string|Có|HTTP method|
|`status_code`|string|Có*|Response status (*cho response)|
|`duration_ms`|string|Có*|Thời gian gọi (*cho response)|
|`is_timeout`|string|Không|`"true"` nếu timeout xảy ra|
|`retry_count`|string|Không|Số lần retry đã thực hiện|
|`circuit_breaker_state`|string|Không|`"closed"`, `"open"`, `"half_open"`|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`EXTERNAL_API_REQUEST_START`|DEBUG|Bắt đầu gọi|
|`EXTERNAL_API_REQUEST_SUCCESS`|INFO|Response 2xx|
|`EXTERNAL_API_REQUEST_CLIENT_ERROR`|WARN|Response 4xx|
|`EXTERNAL_API_REQUEST_SERVER_ERROR`|ERROR|Response 5xx|
|`EXTERNAL_API_REQUEST_TIMEOUT`|ERROR|Timeout|
|`EXTERNAL_API_REQUEST_RETRY`|WARN|Retry attempt|

#### Ví dụ

```json
{
  "@timestamp": "2024-01-20T10:30:45.523+07:00",
  "level": "INFO",
  "message": "Stripe charge API completed in 350ms - 200 OK",
  "log_type": "external_api",
  "feature": "PAYMENT",
  "event": "EXTERNAL_API_REQUEST_SUCCESS",
  "target_service": "stripe",
  "target_endpoint": "https://api.stripe.com/v1/charges",
  "http_method": "POST",
  "status_code": "200",
  "duration_ms": "350",
  "correlation_id": "corr_xyz789",
  "service": "payment-service",
  "environment": "prod"
}
```

---

### 3.4 gRPC Logging (`log_type: "grpc"`)

**Dùng cho**: gRPC calls giữa các microservices.

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`grpc_method`|string|Có|Full method path: `"/package.Service/Method"`|
|`grpc_status_code`|string|Có*|gRPC status: `"OK"`, `"NOT_FOUND"`, `"INTERNAL"`, ...|
|`duration_ms`|string|Có*|Thời gian xử lý (*cho response)|
|`req_body`|string|Không|gRPC request payload (JSON representation, masked)|
|`res_body`|string|Không|gRPC response payload (JSON representation, masked)|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`GRPC_REQUEST_START`|DEBUG|Nhận gRPC call|
|`GRPC_REQUEST_SUCCESS`|INFO|gRPC call thành công (status OK)|
|`GRPC_REQUEST_CLIENT_ERROR`|WARN|Client errors (INVALID_ARGUMENT, NOT_FOUND, etc.)|
|`GRPC_REQUEST_SERVER_ERROR`|ERROR|Server errors (INTERNAL, UNAVAILABLE, etc.)|

#### gRPC Status → Log Level mapping

|gRPC Status|Log Level|
|---|---|
|`OK`|INFO|
|`CANCELLED`, `INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `PERMISSION_DENIED`, `UNAUTHENTICATED`, `FAILED_PRECONDITION`, `OUT_OF_RANGE`|WARN|
|`UNKNOWN`, `DEADLINE_EXCEEDED`, `RESOURCE_EXHAUSTED`, `ABORTED`, `UNIMPLEMENTED`, `INTERNAL`, `UNAVAILABLE`, `DATA_LOSS`|ERROR|

---

### 3.5 Job Logging (`log_type: "job"`)

**Dùng cho**: Background jobs, scheduled tasks, queue consumers.

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`job_name`|string|Có|Tên job (snake_case)|
|`job_id`|string|Không|ID của job instance/execution|
|`duration_ms`|string|Có*|Thời gian chạy (*cho complete)|
|`items_processed`|string|Không|Số items đã xử lý thành công|
|`items_failed`|string|Không|Số items lỗi|
|`items_total`|string|Không|Tổng số items|
|`trigger_type`|string|Không|`"scheduled"`, `"manual"`, `"event_driven"`|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`JOB_START`|INFO|Job bắt đầu|
|`JOB_SUCCESS`|INFO|Job hoàn thành thành công|
|`JOB_FAILED`|ERROR|Job thất bại|
|`JOB_PROGRESS`|DEBUG|Progress update (cho long-running jobs)|
|`JOB_PARTIAL_FAILURE`|WARN|Job hoàn thành nhưng có items lỗi|

#### Ví dụ

```json
{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "Job daily_report_generator completed in 45s - 1500/1500 items processed",
  "log_type": "job",
  "feature": "REPORT",
  "event": "JOB_SUCCESS",
  "job_name": "daily_report_generator",
  "job_id": "job_xyz789",
  "duration_ms": "45000",
  "items_processed": "1500",
  "items_total": "1500",
  "trigger_type": "scheduled",
  "service": "report-service",
  "environment": "prod"
}
```

---

### 3.6 Event Logging (`log_type: "event"`)

**Dùng cho**: Message broker events (Kafka, RabbitMQ, etc.).

#### Fields bổ sung

|Field|Type|Bắt buộc|Mô tả|
|---|---|---|---|
|`event_topic`|string|Có|Topic/queue name|
|`event_key`|string|Không|Message key (Kafka partition key)|
|`event_action`|string|Có|`"publish"`, `"consume"`|
|`event_offset`|string|Không|Message offset (Kafka)|
|`event_partition`|string|Không|Partition number|
|`duration_ms`|string|Không|Processing duration (cho consume)|

#### Events chuẩn

|Event|Level|Khi nào|
|---|---|---|
|`EVENT_PUBLISH_SUCCESS`|INFO|Publish message thành công|
|`EVENT_PUBLISH_FAILED`|ERROR|Publish thất bại|
|`EVENT_CONSUME_START`|DEBUG|Bắt đầu consume message|
|`EVENT_CONSUME_SUCCESS`|INFO|Consume và process thành công|
|`EVENT_CONSUME_FAILED`|ERROR|Consume hoặc process thất bại|

---

# 🟡 POLICY — Quy định vận hành

---

## Part 4: Security & Body Logging

### 4.1 Dữ liệu KHÔNG BAO GIỜ được log

Dù ở bất kỳ môi trường nào, các loại data sau **TUYỆT ĐỐI KHÔNG** xuất hiện trong log:

- Password (dù đã hash), secret key, API key (full)
- Full credit card number (chỉ giữ last 4)
- Personal documents: CMND/CCCD, passport number, SSN
- Full JWT token, session token, refresh token
- Private keys, certificates
- Health records, biometric data

### 4.2 Dữ liệu cần MASK

|Data|Cách mask|Ví dụ|
|---|---|---|
|Phone number|Giữ 4 số cuối|`"******5678"`|
|Email|Giữ first char + domain|`"n***@example.com"`|
|Credit card|Giữ 4 số cuối|`"****1234"`|
|IP address|Tuỳ policy: giữ nguyên hoặc mask 2 octet cuối|`"192.168.x.x"`|
|Bank account|Giữ 4 số cuối|`"****5678"`|

### 4.3 Log Injection Prevention

Khi log data từ user input, **phải** sanitize để tránh log injection (CWE-117):

- **PHẢI serialize qua JSON library chuẩn**: Không concatenate string thủ công. JSON library sẽ tự escape `\n`, `\r`, `\"`, etc.
- **KHÔNG bao giờ** dùng string interpolation trực tiếp cho user input vào log message.
- **Giới hạn kích thước** user input trước khi log.

```java
// ❌ XẤU - Dễ bị log injection
logger.info("User login: " + username);

// ✅ TỐT - Dùng parameterized logging
logger.info("User login attempt", Map.of("username", sanitize(username)));
```

### 4.4 OWASP Security Logging Requirements (A09:2025)

Theo OWASP Top 10 2025 — A09 Security Logging and Alerting Failures:

- **Log mọi security events** (cả success và failure): login attempts, authorization failures, input validation failures, password changes.
- **Encode log data đúng cách** để tránh log injection attacks.
- **Không log quá ít** (miss attacks) và **không log quá nhiều** (noise, cost, potential PII leak).
- **Audit trail phải có integrity controls**: append-only, không cho phép tamper.

### 4.5 Retention policy

|Environment|Logs có body/PII|Logs metadata only|
|---|---|---|
|Production|Tối đa **30 ngày**|Tối đa **90 ngày**|
|Staging|Tối đa **7 ngày**|Tối đa **30 ngày**|
|Development|Tối đa **3 ngày**|Tối đa **7 ngày**|

### 4.6 Body Logging Policy

#### Tại sao cần policy riêng?

|Tiêu chí|Metadata logging|Body logging|
|---|---|---|
|Performance impact|Không đáng kể|Có thể cao (serialize, mask, truncate)|
|Storage cost|Thấp (~200-500 bytes/entry)|Cao (có thể +2-4KB/entry)|
|Security risk|Thấp|**Cao** (có thể chứa PII, credentials)|
|Debug value|Vừa phải|**Rất cao** (thấy được actual data)|

**Quy tắc chung**: Body logging là **opt-in** (chủ động bật), không phải mặc định.

#### Khi nào NÊN log body

|Trường hợp|req_body|res_body|Lý do|
|---|---|---|---|
|`status_code >= 400`|✅|✅|Debug lỗi hiệu quả nhất|
|Mutation requests (`POST`/`PUT`/`PATCH`/`DELETE`)|✅|✅|Audit trail, business logic debug|
|DEBUG mode bật|✅|✅|Development/staging investigation|
|Slow requests (`duration_ms > threshold`)|✅|✅|Performance investigation|

#### Khi nào KHÔNG log body

|Trường hợp|Lý do|
|---|---|
|`content_type` là binary (`multipart/form-data`, `application/octet-stream`, `image/*`, `video/*`, `audio/*`)|Binary data vô dụng trong log text, kích thước lớn|
|`req_body_size > 1MB`|Quá lớn — skip hoàn toàn, chỉ log `req_body_size`|
|Auth endpoints (`/login`, `/token`, `/oauth/*`, `/auth/*`)|**LUÔN SKIP** — chứa credentials|
|Health check (`/health`, `/metrics`, `/ready`)|Không có giá trị debug, volume cao|
|`GET` requests (read-only, thường không có body)|Thường không có meaningful body|

#### Quy tắc Truncation

|Environment|Max Body Size|Flag khi truncate|
|---|---|---|
|dev/staging|4096 bytes|`req_body_truncated: "true"`|
|prod (error — status >= 400)|2048 bytes|`res_body_truncated: "true"`|
|prod (normal — status < 400)|1024 bytes|—|

#### Quy tắc Masking trong Body

Body PHẢI được mask **trước khi log** — trong application code, KHÔNG phụ thuộc log pipeline.

|Field pattern (case-insensitive)|Cách mask|Ví dụ output|
|---|---|---|
|`password`, `passwd`, `pwd`|Thay value bằng `"***"`|`"password":"***"`|
|`token`, `access_token`, `refresh_token`, `id_token`|Thay value bằng `"***"`|`"token":"***"`|
|`secret`, `api_key`, `apikey`, `api_secret`|Thay value bằng `"***"`|`"secret":"***"`|
|`otp`, `pin`, `cvv`, `cvc`|Thay value bằng `"***"`|`"otp":"***"`|
|`card_number`, `pan`, `credit_card`|Giữ 4 số cuối|`"card_number":"****1234"`|
|`Authorization` header|Thay bằng `"Bearer ***"`|`"Authorization":"Bearer ***"`|
|`ssn`, `social_security`|Thay bằng `"***"`|`"ssn":"***"`|

> **Implementation**: Mask bằng cách traverse JSON keys (recursive cho nested objects). Dùng regex pattern matching trên key names. Ưu tiên dùng library có sẵn thay vì tự implement.

#### Configuration

Body logging nên bật/tắt qua config, không cần deploy lại:

```yaml
# application.yml
logging:
  body:
    enabled: true
    max-size-bytes: 2048
    mask-patterns:
      - password
      - token
      - secret
      - api_key
      - otp
      - cvv
    skip-endpoints:
      - /auth/login
      - /auth/token
      - /health
      - /metrics
    skip-content-types:
      - multipart/form-data
      - application/octet-stream

---Part 5: Correlation Strategy

egy
5.1 Tại sao cần correlation?

Trong hệ thống microservices, một user action có thể trigger nhiều service calls. Correlation giúp trace toàn bộ flow từ entry point đến downstream services.

es.
5.2 ID hierarchy


correlation_id   ← Business flow ID, xuyên suốt từ client đến tất cả services
  └── request_id ← Unique per HTTP request, sinh tại mỗi service
        └── trace_id / span_id  ← APM tracing (auto-injected bởi Datadog/OTel)


```
5.3 Quy tắc sinh và truyền ID


ng|
5.4 Implementation pattern


Client → API Gateway (sinh correlation_id)
  → Service A (nhận correlation_id, sinh request_id_A)
    → Service B (nhận correlation_id, sinh request_id_B)
    → Service C (nhận correlation_id, sinh request_id_C)


Mọi log trong flow đều có cùng ccorrelation_ido → dễ dàng query tất cả log liên quan:


# Datadog query
@correlation_id:corr_xyz789


```
5.5 Fallback

Nếu request không có gX-Correlation-IDo header, service PHẢI tự sinh một correlation_id mới (không để trống).


--🟢 ADVANCED — Nâng cao


---Part 6: Production Operations

> Phần này dành cho khi hệ thống đã chạy production, có traffic thực tế, và bạn cần tối ưu cost, performance, alerting.

ng.
6.1 Log Sampling Strategy

egy

Tại sao cần sampling?

Một service xử lý 10,000 req/s sinh ~500 bytes/log → og430GB log/ngày/n chỉ từ 1 endpoint. Sampling giúp giảm volume 90-99% mà vẫn giữ được khả năng debug.

ug.

Nguyên tắc vàng

1. 

KHÔNG BAO GIỜ sample ERROR logs l: Mọi error đều phải được giữ 100%.
2. .
KHÔNG BAO GIỜ sample WARN logs l: Warnings là early signals, phải giữ 100%.
3. .
Sample INFO logs l: Tùy volume — giữ 10-100%.
4. .
Sample aggressively DEBUG logs l: Giữ 1-5% (hoặc tắt hẳn ở production).
5. .
Luôn giữ slow requestsue: Requests có sduration_ms > thresholds luôn được log đầy đủ.

đủ.

Level-based Sampling (khuyến nghị)


0%|

Tail-based Sampling (nâng cao)

Buffer log events cho mỗi request, sau khi request hoàn thành:

- Nếu có error → giữ TẤT CẢ logs của request đó (kể cả DEBUG)
- Nếu slow → giữ tất cả
- Nếu normal → sample hoặc drop DEBUG/INFO

> Tail-based sampling khó implement hơn nhưng cho kết quả debug tốt hơn nhiều vì bạn có full context cho error cases.

es.

Adaptive Sampling (cho high-traffic services)

Tự động điều chỉnh sample rate dựa trên traffic volume:

- Traffic bình thường: sample 50% INFO
- Traffic spike (>2x baseline): sample 10% INFO
- Traffic extreme (>5x baseline): sample 1% INFO

NFO

Implementation notes

- s
Include sample rate trong logg : Khi emit sampled log, thêm field i_sample_rate: "0.1"" để analysis tools có thể extrapolate.
- e.Consistent samplingpl: Dùng hash-based sampling (hash hrequest_ids) thay vì random — đảm bảo related logs cùng được giữ hoặc cùng bị drop.

op.
6.2 Cost Optimization

ion

Tiered Retention Strategy


ve|

Kỹ thuật giảm log volume

1. 

Tắt DEBUG ở productionct: Quick win lớn nhất — giảm 50-80% volume.
2. .
Không log health checkshe: s/healthe, t/metricst, c/readyr gọi mỗi vài giây → volume rất lớn, giá trị debug = 0.
3. .
Sample INFO logs l: Giữ 10-50% tuỳ endpoint importance.
4. .
Deduplicate errorsrr: Cùng một error lặp lại 1000 lần/phút → log lần đầu + counter, không log 1000 entries.
5. .
Strip null fieldsie: Không include field nếu value là null/empty — tiết kiệm 20-30% per entry.
6. .
Compact messagess: Message ngắn gọn, không verbose.
7. .
Metrics from logs l: Cho high-volume success cases, generate metrics (count, latency percentiles) thay vì giữ raw logs.

gs.

Cost estimation guide


Logs/day = requests/second × 86400 × (1 - sample_drop_rate)
Size/day = Logs/day × avg_bytes_per_entry

Ví dụ: 1000 req/s, sample 10% INFO, avg 500 bytes:
  ERROR/WARN (5%): 1000 × 0.05 × 86400 × 500 = 2.16 GB/day
  INFO (sampled 10%): 1000 × 0.95 × 0.1 × 86400 × 500 = 4.1 GB/day
  Total: ~6.3 GB/day

So với không sample: 1000 × 86400 × 500 = 43.2 GB/day
→ Tiết kiệm ~85% storage cost.


```
6.3 Performance Guidelines

nes

Async logging

- g
BẮT BUỘC B dùng async logging ở production. Logging KHÔNG được block application thread.
- Java: dùng dAsyncAppendere (Logback) hoặc hAsyncLoggero (Log4j2).
- Python: dùng dQueueHandlern hoặc background thread.
- Node.js: Hầu hết logging libraries (Pino, Winston) đã async by default.

lt.

Batching

- Log collector (Datadog Agent, Fluentd, Vector) nên batch logs trước khi gửi đến backend.
- Batch size: 5MB hoặc 5 giây (whichever comes first).

t).

Body serialization overhead

- Body masking + truncation ticó overheadrh: ~1-5ms per request (tuỳ body size).
- Nếu body logging gây latency đáng kể (>5ms), cân nhắc:
    - Chỉ log body khi  status_code >= 400=
    - Dùng async processing cho body masking
    - Cache compiled regex patterns cho masking

ing

Tránh log trong hot path

- h
KHÔNG log ở mỗi iterationat trong loops xử lý batch data. Log tổng kết sau khi xong.
- g.KHÔNG log binary data d: Encode base64 rồi log binary content là wasteful.
- l.Giới hạn stack trace depthde: Nếu log stack trace, chỉ giữ top 5-10 frames ở production.

on.

Benchmarks target


on|
6.4 Alerting Guidelines

nes

Alert dựa trên structured log fields


ng|

Nguyên tắc alerting

- g
Alert trên ERROR, không phải WARN W: WARN là informational, ERROR cần action. Chỉ alert WARN khi pattern indicates systemic issue.
- e.Percentage-based thresholds, không phải absolute countco: terror_rate > 5%  tốt hơn  error_count > 100> (vì traffic thay đổi).
- ).Tránh alert fatigueti: Mỗi alert phải có runbook hoặc action rõ ràng. Nếu team bỏ qua alert liên tục → alert đó cần re-evaluate.


---Part 7: Ecosystem Integration

ion
7.1 OpenTelemetry Alignment

ent

Tại sao align với OTel?

OpenTelemetry (OTel) là industry standard cho observability. ECS (Elastic Common Schema) đã merge vào OTel semantic conventions từ 2023. Align với OTel đảm bảo:

- Vendor-agnostic: dễ migrate giữa Datadog, ELK, Grafana, etc.
- Cross-signal correlation: logs ↔ traces ↔ metrics cùng schema.
- Future-proof: ecosystem đang converge về OTel.

el.

Field mapping: Custom → OTel → Datadog


d`|

Migration path

1. 

Phase 1as: Giữ custom names, thêm Datadog pipeline remapper để map sang standard attributes.
2. .
Phase 2as: Service mới dùng OTel SDK — tự động emit đúng semantic conventions.
3. .
Phase 3as: Service cũ migrate sang OTel naming khi refactor.


--📎 APPENDIX


---Appendix A: Checklist

ist
A.1 Trước khi implement

ent

 Xác định đlog_type_, pfeaturea, và danh sách events cần log cho service.
ice.
 Xác định danh sách endpoints KHÔNG log body (auth, sensitive endpoints).
ts).
 Xác định content-types cần skip (binary, multipart).
rt).
 Xác định giới hạn truncation phù hợp với môi trường.
ờng.
 List sensitive field patterns cần mask trong body.
ody.
 Xác định sampling strategy cho production.
ion.
 Thiết lập correlation_id propagation pattern.

rn.
A.2 Trong khi implement

ent

 Tất cả log đều có đủ ó 8 required fieldsie (Part 2, Section 2.1).
.1).
  duration_mso có trong mọi response/complete events.
nts.
 Error logs có serror_type_ và `error_messages.
ge`.
  req_body_ đã được mask trước khi log.
log.
 Body bị skip với binary content-types.
pes.
  req_body_truncated: "true"t được set khi body bị cắt.
cắt.
  req_body_size_ luôn được log (kể cả khi body bị skip).
ip).
 Auth endpoints KHÔNG log body.
ody.
 Body logging có thể bật/tắt qua config.
fig.
 4xx responses dùng WARN level, KHÔNG dùng ERROR.
ROR.
 Logging là async, KHÔNG block application thread.
ead.
  correlation_ido được propagate qua header và include trong mọi log.
log.
 User input được serialize qua JSON library (chống log injection).

n).
A.3 Sau khi implement

ent

 Test log output đúng JSON format (mỗi dòng là valid JSON).
ON).
 Test với body chứa password/token → verify đã bị mask.
ask.
 Test với file upload → verify body bị skip.
kip.
 Test với large body (>2KB) → verify truncation + flag.
lag.
 Test auth endpoints → verify không log body.
ody.
 Test error case → verify có error_type, error_message, stack_trace.
ace.
 Test correlation_id → verify consistent across service calls.
lls.
 Verify log có thể parse bởi Datadog/ELK (test trên dev/staging).
ng).
 Review log volume estimate → confirm sampling strategy hợp lý.
 lý.
 Setup alerts dựa trên structured fields.


---Appendix B: Quick Reference

nce
Log Level


DEBUG → Bắt đầu (_START)            → Production: TẮT hoặc sample 1%
INFO  → Thành công (_SUCCESS)        → Production: BẬT (sample nếu cần)
WARN  → Cảnh báo, client error       → Production: BẬT (100%)
ERROR → Lỗi server, cần xử lý       → Production: BẬT (100%, KHÔNG sample)


```
Event Naming


Format: {ACTION}_{RESULT} hoặc {COMPONENT}_{ACTION}_{RESULT}
Suffixes: _START | _SUCCESS | _CLIENT_ERROR | _SERVER_ERROR | _FAILED | _TIMEOUT | _RETRY


```
Body Logging Decision Tree


Request đến
  → Auth endpoint? → SKIP body
  → Binary content-type? → SKIP body
  → Body > 1MB? → SKIP body, log size only
  → Error (4xx/5xx)? → LOG body (masked, truncated)
  → Mutation (POST/PUT/PATCH/DELETE)? → LOG body (masked, truncated)
  → GET success? → SKIP body


```
Sampling Decision Tree


Log level?
  ERROR → KEEP 100%
  WARN  → KEEP 100%
  INFO  → SAMPLE 10-50%
  DEBUG → DROP (production) hoặc SAMPLE 1%


```
Template JSON tối thiểu


{
  "@timestamp": "2024-01-20T10:30:45.123+07:00",
  "level": "INFO",
  "message": "POST /api/orders - 201 Created in 150ms",
  "log_type": "api",
  "feature": "ORDER",
  "event": "API_REQUEST_SUCCESS",
  "service": "order-service",
  "environment": "prod"
}


```
Feature mapping


/auth/*     → AUTH          /notifications/* → NOTIFICATION
/users/*    → USER          /reports/*       → REPORT
/orders/*   → ORDER         /admin/*         → ADMIN
/payments/* → PAYMENT       /health          → SYSTEM
/products/* → PRODUCT


```
Datadog Standard Attributes mapping


service     → service (reserved)     error_type     → error.kind
environment → env (reserved)         error_message  → error.message
version     → version (reserved)     stack_trace    → error.stack
http_method → http.method            client_ip      → network.client.ip
status_code → http.status_code       user_id   
→ usr.

---

## Tài liệu tham khảo

### Industry Standards

1. [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/) — Industry standard cho field naming, là nền tảng cho tất cả log schema hiện đại.
2. [OpenTelemetry Semantic Conventions for Logs](https://opentelemetry.io/docs/specs/semconv/general/logs/)
3. [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/ecs-http.html) — Đã merge vào OTel semantic conventions từ 2023.
4. [Datadog Standard Attributes](https://docs.datadoghq.com/logs/log_configuration/attributes_naming_convention/) — Mapping chuẩn nếu dùng Datadog.
5. [Datadog Unified Service Tagging](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/)

### Security

6. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — **Must-read** cho security logging requirements.
7. [OWASP Logging Vocabulary](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html) — Standard event keywords cho security events.
8. [OWASP Top 10 2025 — A09 Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/)
9. [OWASP Proactive Controls — C9: Implement Logging and Monitoring](https://top10proactive.owasp.org/the-top-10/c9-security-logging-and-monitoring/)

### Best Practices

10. [Datadog: Optimize High-Volume Logs](https://www.datadoghq.com/blog/optimize-high-volume-logs/) — Sampling + cost optimization



---

# CÁC LỖI THƯỜNG GẶP 

## Lỗi: Khi 


**1. Vấn đề:** `TypeError: BoundLogger.info() got multiple values for argument 'event'` — structlog crash khi gọi logger.

**2. Nguyên nhân:** Trong structlog, positional argument đầu tiên được map nội bộ thành `event`. Khi viết `logger.info("some message", event="PIPELINE_START")`, Python nhận `event` hai lần — một từ positional, một từ keyword — nên raise TypeError.

**3. Best practice:** Bỏ hoàn toàn `event=` keyword, dùng positional string làm event name luôn:

```python
# Positional string chính là event — kwargs chỉ chứa context
logger.info("pipeline.stream.start", request_id=rid, user_id=uid)
logger.error("redis.push.failed", error=str(e), queue=queue_name)
```

Output JSON tự động có dạng `{"event": "pipeline.stream.start", "request_id": "abc", ...}` — sạch, dễ filter trên Datadog/ELK, và đúng convention của structlog.

Một tip nhỏ: naming convention `dot.separated` (như `pipeline.stream.start`) hoặc `snake_case` đều phổ biến, nhưng dot notation tiện hơn khi query trên observability platform vì dễ group theo prefix (`pipeline.*`).


---

Dùng **positional string** là best practice đúng chuẩn structlog:

```python
# ✅ Positional string = event name
logger.info("pipeline.stream.start", request_id=rid, user_id=uid)

# ❌ Keyword event= gây conflict nếu có positional string đi kèm
logger.info("some message", event="PIPELINE_START", request_id=rid)
```

Lý do đơn giản: structlog thiết kế `event` **là** positional argument đầu tiên. Dùng keyword `event=` tức là đi ngược lại API design của thư viện — dù nó vẫn chạy được khi không có positional string, nhưng rất dễ gây collision như lỗi bạn vừa gặp, và không ai trong cộng đồng structlog viết kiểu đó cả.

---
Hai cách này là **best practice của hai thư viện khác nhau** — không nên so trực tiếp:

**Python standard logging** → `extra={}` là đúng chuẩn:

```python
logger.info("API request success", extra={
    "event": "API_REQUEST_SUCCESS",
    "request_id": rid,
    "duration_ms": 120
})
```

`event` nằm trong dict `extra`, hoàn toàn an toàn — nó chỉ là một field data bình thường, không conflict gì cả vì `logging.info(msg, *args, **kwargs)` không reserve tên `event`.

**Structlog** → positional string là đúng chuẩn:

```python
logger.info("api.request.success", request_id=rid, duration_ms=120)
```

Kwargs truyền thẳng, gọn hơn, nhưng `event` bị reserve nên không được dùng làm keyword.

Tóm lại: **cả hai đều là best practice**, mỗi cái đúng trong ngữ cảnh thư viện của nó. Project đang dùng standard logging + `extra={}` thì cứ giữ nguyên, không có vấn đề gì. Chỉ cần đảm bảo toàn team follow cùng một convention là được.


---

Trong production Python projects hiện tại, **structlog được ưa chuộng hơn** rõ rệt, đặc biệt ở các dự án có observability stack (Datadog, ELK, Grafana).

Lý do chính là **ergonomics** — so sánh cùng một log line:

```python
# Standard logging — verbose, phải wrap trong extra={}
logger.info("LLM call completed", extra={
    "event": "LLM_CALL_SUCCESS",
    "model": "gpt-4",
    "duration_ms": 450,
    "tokens": 1200
})

# Structlog — kwargs trực tiếp, gọn hơn nhiều
logger.info("llm.call.success", model="gpt-4", duration_ms=450, tokens=1200)
```

Structlog thắng ở mấy điểm thực tế: kwargs truyền thẳng không cần wrapper `extra={}`, tự động bind context (request_id, user_id) một lần dùng xuyên suốt request qua `bind()`, và JSON output sạch mặc định không cần custom formatter.

Tuy nhiên, **standard logging vẫn hoàn toàn hợp lệ** — đặc biệt khi project đã chạy ổn, team quen rồi, hoặc không muốn thêm dependency. Nhiều project lớn vẫn dùng standard logging + custom JSON formatter mà không gặp vấn đề gì.

Với Pika project cụ thể của bạn, nếu đang dùng standard logging ổn thì không cần migrate. Nhưng nếu bắt đầu service mới hoặc refactor logging layer, structlog là lựa chọn phổ biến hơn trong cộng đồng FastAPI/microservices hiện tại.


---

Đây là MECE breakdown các cách ghi log trong Python:

---

**1. Print statements** — anti-pattern, không ai dùng trong production

```python
print(f"API call success, duration={450}ms")
```

Terminal output:

```
API call success, duration=450ms
```

Không level, không timestamp, không routing, không filter được. Chỉ dùng khi debug local nhanh.

---

**2. Standard logging — plain text**

```python
logger.info("API call success, model=gpt-4, duration=450ms")
```

Terminal output:

```
2025-03-09 10:23:45,123 INFO api.service - API call success, model=gpt-4, duration=450ms
```

Mọi context nhét hết vào string. Không parse được, không filter trên Datadog/ELK. Rất phổ biến ở các project nhỏ hoặc code cũ.

---

**3. Standard logging — structured với `extra={}`**

```python
logger.info("API call success", extra={
    "event": "LLM_CALL_SUCCESS",
    "model": "gpt-4",
    "duration_ms": 450
})
```

Terminal output (cần custom JSON formatter):

```json
{"timestamp": "2025-03-09T10:23:45.123Z", "level": "info", "message": "API call success", "event": "LLM_CALL_SUCCESS", "model": "gpt-4", "duration_ms": 450}
```

Verbose nhưng zero dependency, team nào cũng đọc được. Phù hợp project đã có sẵn logging layer ổn định.

---

**4. Structlog — positional string + kwargs**

```python
logger.info("llm.call.success", model="gpt-4", duration_ms=450)
```

Terminal output (JSON mặc định):

```json
{"event": "llm.call.success", "model": "gpt-4", "duration_ms": 450, "level": "info", "timestamp": "2025-03-09T10:23:45.123Z"}
```

Gọn nhất, JSON mặc định, có `bind()` để auto-attach context xuyên request. Best practice phổ biến nhất trong FastAPI/microservices hiện tại.

---

**5. Loguru — drop-in replacement**

```python
from loguru import logger
logger.info("LLM call success | model=gpt-4 duration_ms=450")
```

Terminal output (default — pretty format, có màu):

```
2025-03-09 10:23:45.123 | INFO     | __main__:handler:42 - LLM call success | model=gpt-4 duration_ms=450
```

Terminal output (sau khi config `serialize=True`):

```json
{"text": "LLM call success | model=gpt-4 duration_ms=450", "record": {"level": {"name": "INFO"}, "time": {"timestamp": 1741512225.123}, "message": "LLM call success | model=gpt-4 duration_ms=450"}}
```

API đẹp, zero config, auto-rotation. Nhưng singleton global logger nên khó control trong microservices lớn, và structured JSON output cần thêm config.

---

**Best practice theo context:**

Dự án mới, microservices, cần observability → **structlog** (option 4). Đây là lựa chọn phổ biến nhất trong cộng đồng production Python hiện tại. Lưu ý `event` là field chính trong JSON — đây là lý do không được dùng `event=` làm keyword.

Dự án đang chạy ổn với standard logging → **giữ option 3**, không cần migrate nếu không có pain point. `event` nằm trong `extra={}` nên an toàn, nhưng `message` và `event` bị tách rời — hơi redundant.

Script nhỏ, CLI tool, prototype nhanh → **Loguru** (option 5) cho nhanh.