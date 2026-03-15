
# Stage 2 – Query Understanding & Router (SLM-based)

> **Ý tưởng tổng quát (bản dễ hiểu cho non-tech):**  
> Hãy tưởng tượng cả hệ thống là một công ty:
> - **Stage 1** là bộ phận lễ tân – nhận mọi “yêu cầu” từ khách (user), gom lại thành hồ sơ input chuẩn (ContextPackV1).  
> - **Stage 3 + Stage 4** là “sếp + đội thi công” – suy nghĩ, lập kế hoạch chi tiết rồi thực sự đi làm việc trên web, công cụ, dữ liệu…  
> - **Stage 2** chính là **“thư ký thông minh”**, đứng giữa, đọc yêu cầu của khách rồi quyết định:
>   - Việc nào chỉ là **câu hỏi đơn giản, an toàn, 1–2 bước, chỉ cần đọc/tóm tắt/lấy vài số liệu** → thư ký **tự xử luôn**, cho nhanh, không phiền sếp.  
>   - Việc nào là **nhiệm vụ phức tạp, nhiều bước, có hành động trên web, có dính đến form, tài khoản, tiền, dữ liệu nhạy cảm…** → thư ký **không dám quyết**, mà chuyển lên “sếp” (Stage 3) để suy nghĩ kỹ, lập plan rõ ràng, rồi mới giao cho đội thi công (Stage 4).
>
> Về mặt kỹ thuật:
> - Stage 2 dùng **một model nhỏ (SLM)** để đọc `user_query` và:
>   - hiểu *intent* (user đang muốn *tìm hiểu* hay *bảo hệ thống làm cái gì đó*),
>   - bóc một số thông tin đơn giản (ticker, vendor, time range…),
>   - gắn các “cờ” về rủi ro (có nhắc tới tiền/tài khoản/form… không?),
>   - đánh giá mức độ phức tạp (có nhiều bước “bước 1/bước 2/sau đó…” không?),
>   - tự chấm điểm “tự tin” (`slm_confidence` – nó cảm thấy mình hiểu rõ đến mức nào).
> - Sau đó, Stage 2 dùng **một bộ rule CỨNG** (rule-based) để quyết định route:
>   - Nếu thỏa điều kiện **đơn giản + an toàn + SLM rất tự tin + chỉ dùng tool đọc-only/micro-action** → gán `RoutingDecision.path = "FAST_PATH"`.
>     - Lúc này query sẽ đi thẳng sang **Stage 4 – Simple Fast Executor** để gọi tool đơn giản (tóm tắt, giải thích, lấy số liệu, scroll chút xíu…) và trả lời luôn.
>   - Chỉ cần có **bất kỳ dấu hiệu phức tạp/rủi ro** (multi-step, action thực sự, form, tài khoản, tiền…) → gán `RoutingDecision.path = "AGENT_PATH"`.
>     - Lúc này query sẽ đi sang **Stage 3 – Planner (LLM)** để được “sếp” lập ExecutionPlan nhiều bước, set gate/policy/budget, rồi mới sang Stage 4 Agent Executor thi công.
>
> Nguyên tắc thiết kế:
> - Stage 2 **chỉ làm phân loại & phân luồng**, không làm việc nặng:
>   - Không đọc DOM sâu,
>   - Không lập kế hoạch multi-step,
>   - Không gọi tool nguy hiểm (form-fill, submit, trade…).
> - Stage 2 **ưu tiên an toàn**:
>   - Nếu lỡ “quá cẩn thận” → query đơn giản vẫn bị đẩy sang Stage 3 → chỉ tốn thêm token, chấp nhận được.
>   - Ngược lại, tuyệt đối tránh để query phức tạp/rủi ro chui vào nhánh fast path.
> - Nhờ đó, hệ thống vừa:
>   - **nhanh hơn** cho những request nhỏ, dễ, an toàn,
>   - vừa **kiểm soát tốt rủi ro** cho những task agent phức tạp.

Stage 2 **không dùng LLM to**, không đọc DOM sâu, không lập kế hoạch nhiều bước.  
Nó chỉ dùng **SLM + rule** để phân loại và phân luồng.

---

## 1. Explain pipeline – Tổng quan Stage 2

### 1.1. Stage 2 nhận gì và trả gì?

**Đầu vào (từ Stage 1):**

- `user_query`  
  - Chuỗi text câu hỏi/bút lệnh của người dùng.
- `ContextPackV1` (Stage 2 chủ yếu dùng mỗi `user_query`, nhưng cần context để log / pass-through):
  - URL/tab hiện tại,
  - metadata cơ bản (title, domain, v.v.).

**Đầu ra (cho Stage 3/4):**

1. `TaskSpecV1` – “hồ sơ ý định” đã được chuẩn hóa:

```jsonc
TaskSpecV1 {
  "user_query": "...",                 // Câu hỏi gốc
  "intent": "research | action | research_then_action | unknown",
  "entities": { ... },                 // ticker, vendor, time_range... (nếu bóc được)
  "constraints": { ... },              // no_submit, view_only, max_items... (đơn giản)
  "risk_flags": ["payment", "account", ...],

  "meta": {
    "has_action_word": true/false,
    "has_multi_step_pattern": true/false,
    "action_type": "none | ui_assist | form_fill | submit | trade | ...",
    "is_single_step": true/false,
    "slm_confidence": 0.0-1.0
  }
}
```

2. `RoutingDecision` – kết quả route của Stage 2:

```jsonc
RoutingDecision {
  "path": "FAST_PATH" | "AGENT_PATH"
}
```

- `FAST_PATH`  → gửi `TaskSpecV1` sang **Stage 4 – Simple Fast Executor** (gọi tool safe, đọc-only, micro-action).
- `AGENT_PATH` → gửi `TaskSpecV1` sang **Stage 3 – Planner LLM** (lập plan chi tiết) → rồi mới xuống Stage 4 Agent Executor.

> Mặc định **mọi query** sẽ vào `AGENT_PATH`.  
> Chỉ khi thỏa TẤT CẢ rule an toàn + SLM tự tin cao thì mới được “nâng cấp” thành `FAST_PATH`.

---

### 1.2. Bảng tóm tắt module → vai trò

| Module                | Vai trò chính                                                                 | Input                                   | Output                          |
|-----------------------|-------------------------------------------------------------------------------|-----------------------------------------|----------------------------------|
| `S2_IntentClassifier` | SLM đọc `user_query`, phân loại intent, bóc entity/constraint đơn giản, gắn risk/complexity flag, tính `slm_confidence`. | `user_query`                            | cấu trúc tạm (intent + flags…)  |
| `S2_TaskSpecBuilder`  | Gói kết quả từ classifier thành `TaskSpecV1` chuẩn hóa.                      | output từ `S2_IntentClassifier`         | `TaskSpecV1`                    |
| `S2_RuleRouter`       | Rule-based engine quyết `RoutingDecision.path = FAST_PATH / AGENT_PATH` dựa trên `TaskSpecV1.meta`. | `TaskSpecV1`                            | `RoutingDecision`               |
| (Downstream) Stage 3  | Nhận `TaskSpecV1` khi `path = AGENT_PATH`, dùng LLM để sinh `PlanBundleV1`.   | `TaskSpecV1`                            | `PlanBundleV1`                  |
| (Downstream) Stage 4  | Ở mode simple: nhận `TaskSpecV1` khi `path = FAST_PATH` và gọi tool read-only; Ở mode agent: nhận `PlanBundleV1` và thi công ExecutionPlan nhiều bước. | `TaskSpecV1` hoặc `PlanBundleV1`        | Kết quả cuối cho user           |

---

### 1.3. Bảng mode thực thi A/B/C/D (góc nhìn Stage 2)

Ở các spec trước, ExecModeV1 của hệ thống có 4 mode:

- A = `RESEARCH_ONLY`
- B = `ACTION_ONLY`
- C = `HYBRID` (research rồi action)
- D = `CLARIFY_OR_FALLBACK`

**Stage 2 không trực tiếp quyết A/B/C/D**, nhưng:

- `TaskSpecV1.intent` là “bản dịch ý định” tương ứng 4 mode này, để Stage 3/4 dùng:
  - `intent = research`            → phù hợp `RESEARCH_ONLY`
  - `intent = action`              → phù hợp `ACTION_ONLY`
  - `intent = research_then_action`→ phù hợp `HYBRID`
  - `intent = unknown`             → tương ứng `CLARIFY_OR_FALLBACK` (Stage 3 có thể sinh clarifying question)

Stage 2 nhiệm vụ chính:

- Xác định **intent 4 mode** dựa trên câu hỏi,
- Không làm planning, không tự chọn chiến thuật thực thi chi tiết.

---

### 1.4. Các kiểu outcome của Stage 2 (RoutingDecision.path)

Stage 2 chỉ có **2 outcome chính**:

| RoutingDecision.path | Ý nghĩa                                                         | Gửi cho ai?                                 |
|----------------------|-----------------------------------------------------------------|---------------------------------------------|
| `FAST_PATH`          | Query đơn giản, an toàn, chỉ cần 1–2 thao tác read-only / micro-action. Có thể xử lý trực tiếp mà không cần LLM planner. | Gửi `TaskSpecV1` sang **Stage 4 – Simple Fast Executor** |
| `AGENT_PATH`         | Query phức tạp hoặc có rủi ro (multi-step, action thực sự, liên quan tiền/tài khoản/biểu mẫu…). Cần LLM planner và policy. | Gửi `TaskSpecV1` sang **Stage 3 – Planner (LLM)**         |

> Nếu Stage 4 Simple Executor ở FAST_PATH bị lỗi (tool hỏng, input edge-case), hệ thống có thể **fallback** bằng cách gửi lại `TaskSpecV1` sang Stage 3 để đi đường AGENT_PATH (logic fallback thuộc Stage 4, Stage 2 chỉ log `path` ban đầu).

---

### 1.5. Pipeline Stage 2 (theo từng bước + module)

```text
+============================================================+
|                  STAGE 2 – SLM QUERY ROUTER                |
+============================================================+

[Input từ Stage 1]
  - user_query
  - ContextPackV1 (Stage 2 dùng chủ yếu user_query)

   |
   v
+-------------------------+
|  (2.1) S2_IntentClassifier (SLM)
+-------------------------+
| - Đọc user_query        |
| - Xác định intent:      |
|    research / action /  |
|    research_then_action |
|    / unknown            |
| - Bóc đơn giản:         |
|    entities, constraints|
| - Gắn risk_flags thô    |
| - Đánh dấu:             |
|    has_action_word?     |
|    has_multi_step?      |
|    action_type?         |
|    is_single_step?      |
| - Tính slm_confidence   |
+-----------+-------------+
            |
            v
+-------------------------+
|  (2.2) S2_TaskSpecBuilder
+-------------------------+
| - Gói thành TaskSpecV1  |
|   (intent, entities,    |
|    constraints,         |
|    risk_flags, meta)    |
+-----------+-------------+
            |
            v
+-------------------------+
|  (2.3) S2_RuleRouter    |
+-------------------------+
| - Đọc TaskSpecV1.meta   |
| - Áp rule CỨNG để quyết |
|   path = FAST_PATH      |
|   hay AGENT_PATH        |
+-----------+-------------+
            |
     +------+------ +
     |             |
     v             v
+------------------------+     +---------------------------+
| OUTPUT A – FAST_PATH   |     | OUTPUT B – AGENT_PATH     |
| - TaskSpecV1           |     | - TaskSpecV1              |
| - path = FAST_PATH     |     | - path = AGENT_PATH       |
+-----------+------------+     +-------------+-------------+
            |                                    |
            v                                    v
+============================+      +==============================+
| STAGE 4 – Simple Fast Exec |      | STAGE 3 – Planner (LLM)     |
+============================+      +==============================+
| - Gọi tool safe (read-only |      | - Sinh PlanBundleV1 (plan,  |
|   / micro-action)          |      |   gates, budget, ...)       |
| - Trả kết quả cuối         |      +--------------+--------------+
+----------------------------+                     |
                                                   v
                                      +==============================+
                                      | STAGE 4 – Agent Executor     |
                                      +==============================+
                                      | - Thi công ExecutionPlan     |
                                      | - Trả kết quả cuối           |
                                      +------------------------------+
```

---

### 1.6. Giải thích về fast path (yêu cầu, phân quyền, góc nhìn “thư ký – sếp”)

**Fast path** là “làn đường cao tốc” cho những yêu cầu **đơn giản & an toàn**:

- Không cần gọi LLM planner,
- Không cần vẽ ExecutionPlan nhiều bước,
- Chỉ cần gọi 1 tool đơn giản (read-only hoặc micro-action rất nhẹ) là trả lời được ngay.

#### 1.6.1. Vì sao cần fast path?

- Có rất nhiều câu hỏi kiểu:
  - “Tóm tắt trang này trong 3 ý.”  
  - “Giải thích giúp mình EV/EBIT là gì.”  
  - “Cho mình ROE 3 năm gần nhất của MIG và BMI.”  
- Nếu cứ bắt những câu như vậy đi qua toàn bộ pipeline Stage 3 (LLM planner) + Stage 4 agent, thì:
  - **tốn token**,  
  - **tăng latency**,  
  - **phức tạp hoá log & monitoring** không cần thiết.
- Fast path cho phép:
  - “Việc vặt, an toàn” → xử ngay tại Stage 2 + Stage 4 simple,  
  - “Việc lớn, rủi ro / multi-step” → vẫn đi đường Stage 3 + 4 đầy đủ.

#### 1.6.2. Điều kiện để được vào fast path

Để một query được **Stage 2 cho phép đi fast path**, tất cả các điều kiện dưới đây phải **đồng thời đúng**:

1. **Intent phù hợp**  
   - Thường là `research` → user chỉ cần đọc/hiểu/tóm tắt/lấy thông tin.
   - Có thể là `action` nhưng chỉ en phép loại **micro-action UI rất nhẹ**, ví dụ:
     - cuộn trang (`scroll`),
     - mở một link (`open_link`),
     - chuyển tab, focus, highlight text…
   - Mọi loại action “thật” (điền form, submit, mua/bán, đăng ký, login…) đều bị loại khỏi fast path.

2. **Không có hành động nguy hiểm trong câu chữ**  
   - Query **không chứa** từ/cụm từ thể hiện hành động mạnh, ví dụ:
     - “điền form”, “gửi form”, “submit”,  
     - “mua”, “bán”, “đặt lệnh”,  
     - “đăng ký”, “đăng nhập”, “login”, “OTP”, “thanh toán”, “chuyển tiền”…
   - Nếu có từ khóa action nhưng chỉ thuộc nhóm UI assist nhỏ (ví dụ “kéo xuống”, “scroll”, “mở link đầu tiên”…), có thể vẫn cho fast path nhưng phải nằm trong allowlist micro-action.

3. **Không có dấu hiệu multi-step phức tạp**  
   - Query **không chứa** pattern multi-step rõ ràng như:
     - “bước 1/bước 2/bước 3”,
     - “đầu tiên…, sau đó…, rồi…, cuối cùng…”,
     - “… rồi lấy kết quả đó điền vào …”.
   - Nếu có, tức là user đang mô tả một **quy trình nhiều bước** → bắt buộc phải đi qua Stage 3 để lập plan.

4. **Không có risk nhạy cảm**  
   - `risk_flags` từ SLM **không** được chứa các loại rủi ro như:
     - `payment` (thanh toán, tiền bạc),
     - `account` (tài khoản đăng nhập),
     - `credential` (mật khẩu, token…),
     - `legal_high_risk` (tình huống pháp lý nhạy cảm),
     - hoặc bất kỳ flag nào team định nghĩa là “nguy hiểm”.

5. **SLM phải tự tin cao về phân loại**  
   - `slm_confidence ≥ CONF_THRESH_FAST_PATH` (ví dụ 0.8–0.9):
     - Nếu SLM “lấp lửng” (confidence thấp) → **không fast path**, cho đi AGENT_PATH.
   - Confidence không phải “chân lý”, nhưng là tín hiệu: SLM có cảm thấy query này thực sự là loại đơn giản nó quen xử lý hay không.

6. **Tool dự kiến sử dụng phải nằm trong allowlist SAFE**  
   - Chỉ dùng những tool mà team đã đánh dấu là **read-only hoặc micro-action an toàn**, ví dụ:
     - `SummarizeActiveTab` → tóm tắt nội dung tab hiện tại.
     - `ExplainConcept` → giải thích khái niệm tài chính, chỉ dựa trên knowledge base.
     - `FinAI.BasicMetrics` → lấy vài chỉ số (ROE, P/E…) từ data nội bộ.
     - `KG.SimpleLookup` → lookup đơn giản trên knowledge graph.
     - `Browser.Scroll`, `Browser.OpenLink` → hỗ trợ UI nhỏ, không submit gì ra ngoài.
   - Tuyệt đối **không** cho fast path gọi:
     - tool điền form, submit form,
     - tool đặt lệnh, mua/bán,
     - tool liên quan tiền, thanh toán, đăng ký tài khoản,…

> Chỉ khi **6 điều kiện trên đều đạt**, Stage 2 mới set:  
> `RoutingDecision.path = "FAST_PATH"`.

#### 1.6.3. Phân quyền: Stage 2 được làm gì, không được làm gì?

Góc nhìn tổ chức:

- **Stage 2 (thư ký)** chỉ được quyền:
  - Tự xử **việc vặt, việc đọc-only, việc an toàn nội bộ**, ví dụ:
    - tóm tắt trang,
    - giải thích khái niệm,
    - lấy vài chỉ số từ FinAI,
    - scroll/mở link/đổi tab cho user xem dễ hơn,
    - lưu note nội bộ.
- **Stage 2 KHÔNG có quyền**:
  - tự ý điền form đăng ký,
  - submit bất kỳ form nào,
  - thực hiện giao dịch (mua/bán, đặt lệnh),
  - động chạm tới tài khoản, mật khẩu, OTP, thanh toán,
  - tự ý “sáng tạo quy trình nhiều bước” trên web.

Mọi việc **có rủi ro thực sự** (ảnh hưởng tiền, tài khoản, pháp lý…) đều phải:

1. Được Stage 2 nhận diện là phức tạp/rủi ro → route `AGENT_PATH`.  
2. Được Stage 3 (LLM planner) lập kế hoạch và kiểm tra kĩ.  
3. Được Stage 4 Agent Executor thi công **theo plan**, dưới sự giám sát của policy/gate/budget.

#### 1.6.4. Nguyên tắc “sai thì sai về phía an toàn”

- Nếu router Stage 2 **quá cẩn thận**:
  - Một số query đơn giản đáng ra có thể fast path lại bị đẩy sang AGENT_PATH.  
  - Hệ quả: chậm hơn một chút, tốn thêm token → chấp nhận được.
- Nếu router Stage 2 **quá thoáng**:
  - Query phức tạp/rủi ro bị cho đi fast path.  
  - Hệ quả: dễ gây lỗi, hành vi khó kiểm soát, rủi ro cao.
- Vì vậy, thiết kế mặc định:
  - **Không chắc thì đẩy sang AGENT_PATH**.  
  - Fast path là “đặc quyền” dành cho các query **rất rõ ràng, rất an toàn**.

---

### 1.7. Sequence diagram (ASCII)

```text
User         Stage1              Stage2                      Stage3                 Stage4
 |             |                   |                            |                     |
 |-- Query --->|                   |                            |                     |
 |             |-- user_query ---->|                            |                     |
 |             |  ContextPackV1    |                            |                     |
 |             |                   |                            |                     |
 |             |                   |-- S2_IntentClassifier      |                     |
 |             |                   |   (SLM: intent + flags)    |                     |
 |             |                   |                            |                     |
 |             |                   |-- S2_TaskSpecBuilder       |                     |
 |             |                   |   -> TaskSpecV1            |                     |
 |             |                   |                            |                     |
 |             |                   |-- S2_RuleRouter            |                     |
 |             |                   |   -> RoutingDecision       |                     |
 |             |                   |                            |                     |
 |             |                   |==== path = FAST_PATH ==========================> |
 |             |                   |                            |   Simple Executor   |
 |             |                   |--------------------------->|-- safe tool ------>|
 |             |                   |                            |<-- answer ----------|
 |             |                   |<---------------------------|                     |
 |             |<------------------|                                                |
 |<---------------- Answer to user --------------------------------------------------|
 |             |                   |                            |                     |
 |             |                   |==== path = AGENT_PATH =========================>|
 |             |                   |                            |    Planner (LLM)    |
 |             |                   |--------------------------->|-- build plan ----->|
 |             |                   |                            |   PlanBundleV1      |
 |             |                   |                            |-------------------> |
 |             |                   |                            | Agent Executor      |
 |             |                   |                            |-- execute steps --->|
 |             |                   |                            |<-- final result ----|
 |             |                   |<---------------------------|                     |
 |             |<------------------|                                                |
 |<---------------- Answer to user --------------------------------------------------|
```

---

## 2. Chi tiết module Stage 2

### 2.1. `S2_IntentClassifier` (SLM)

**Mục tiêu:**

- Dùng **một SLM nhỏ** để:
  - phân loại **intent** 4 mode,
  - bóc entity/constraint đơn giản,
  - gắn vài `risk_flags` và `complexity flags`,
  - cho điểm `slm_confidence`.

**Input:**

- `user_query: string`

**Output (khái niệm):**

```jsonc
{
  "intent": "research | action | research_then_action | unknown",
  "entities": {
    "tickers": ["MIG", "BMI"],
    "vendor": "Vietstock",
    "time_range": "3y"
  },
  "constraints": {
    "no_submit": true,
    "view_only": true
  },
  "risk_flags": ["external_side_effect"],

  "complexity": {
    "has_action_word": true,
    "has_multi_step_pattern": true,
    "action_type": "form_fill",
    "is_single_step": false
  },

  "slm_confidence": 0.86
}
```

> Lưu ý: Đây là **cấu trúc logic**. Thực tế implement có thể khác (dict, Pydantic model…), nhưng phải chứa đủ các field đã bàn trong cuộc trao đổi.

---

### 2.2. `S2_TaskSpecBuilder`

**Mục tiêu:**

- Chuẩn hóa output của SLM thành `TaskSpecV1` – format chung cho các stage sau (Stage 3, Stage 4).

**Input:**

- Output thô từ `S2_IntentClassifier`.

**Output:**

```jsonc
TaskSpecV1 {
  "user_query": "...",
  "intent": "...",
  "entities": { ... },
  "constraints": { ... },
  "risk_flags": [ ... ],
  "meta": {
    "has_action_word": true/false,
    "has_multi_step_pattern": true/false,
    "action_type": "...",
    "is_single_step": true/false,
    "slm_confidence": 0.0-1.0
  }
}
```

**Nhiệm vụ:**

- Đảm bảo các trường luôn tồn tại (kể cả rỗng) → downstream code dễ xử lý.
- Chuẩn hóa enum/string (`intent`, `action_type`, `risk_flags`…).
- Log lại `TaskSpecV1` phục vụ debug / training sau này.

---

### 2.3. `S2_RuleRouter`

**Mục tiêu:**

- Quyết định:

```jsonc
RoutingDecision {
  "path": "FAST_PATH" | "AGENT_PATH"
}
```

**Input:**

- `TaskSpecV1`

**Logic (tóm tắt):**

- **Mặc định**: `path = AGENT_PATH` (đi full Stage 3 + 4).
- Chỉ set `path = FAST_PATH` nếu TẤT CẢ các điều kiện sau đúng:

  1. `intent == "research"`  
     - Hoặc `intent == "action"` nhưng `action_type == "ui_assist"` *và* `is_single_step == true`.

  2. `meta.has_action_word == false`  
     (hoặc chỉ chứa từ khóa thuộc nhóm UI assist an toàn như scroll/mở link).

  3. `meta.has_multi_step_pattern == false`.

  4. Không có `risk_flags` thuộc nhóm nhạy cảm:
     - `payment`, `account`, `credential`, `legal_high_risk`, …

  5. `meta.slm_confidence >= CONF_THRESH_FAST_PATH` (ví dụ 0.8–0.9).

  6. Tool dự kiến sử dụng nằm trong **allowlist SAFE** (được định nghĩa bên Stage 4 simple executor).

- Nếu **bất kỳ** điều kiện nào fail → giữ `AGENT_PATH`.

> Tư duy: “Sai thì sai theo hướng an toàn”:  
> - Lỡ đẩy query đơn giản sang AGENT_PATH → tốn token.  
> - Lỡ đẩy query phức tạp sang FAST_PATH → tiềm ẩn bug/risk.  
> → Nên router phải bảo thủ.

---

## 3. Ví dụ input/output & pipeline cho 2 trường hợp

### 3.1. Ví dụ 1 – Query đơn giản → FAST_PATH

**User query:**

> “Tóm tắt nội dung trang này trong 3 ý chính giúp mình.”

**Bước 1 – Stage 1:**

- Nhận raw input, tạo `ContextPackV1` (URL, title, text của trang).

**Bước 2 – Stage 2:**

1. `S2_IntentClassifier`:
   - intent: `research`
   - entities: `{}`
   - constraints: `{ "max_bullets": 3 }`
   - risk_flags: `[]`
   - complexity:
     - has_action_word: false
     - has_multi_step_pattern: false
     - action_type: "none"
     - is_single_step: true
   - slm_confidence: 0.93

2. `S2_TaskSpecBuilder` → `TaskSpecV1`:

```jsonc
TaskSpecV1 {
  "user_query": "Tóm tắt nội dung trang này trong 3 ý chính giúp mình.",
  "intent": "research",
  "entities": {},
  "constraints": { "max_bullets": 3 },
  "risk_flags": [],
  "meta": {
    "has_action_word": false,
    "has_multi_step_pattern": false,
    "action_type": "none",
    "is_single_step": true,
    "slm_confidence": 0.93
  }
}
```

3. `S2_RuleRouter`:

- intent = research → OK.
- Không action nguy hiểm → OK.
- Không multi-step → OK.
- Không risk_flags nhạy cảm → OK.
- slm_confidence = 0.93 ≥ 0.8 → OK.
- Tool dự kiến = `SummarizeActiveTab` (trong allowlist SAFE) → OK.

→ `RoutingDecision.path = "FAST_PATH"`

**Bước 3 – Stage 4 (Simple Fast Executor):**

- Nhận `TaskSpecV1` + `ContextPackV1`.
- Gọi tool `SummarizeActiveTab(max_bullets=3)`.
- Trả lại cho user 3 bullet tóm tắt nội dung trang.

**Pipeline rút gọn:**

```text
User -> Stage1 -> Stage2 (SLM + Router: FAST_PATH)
     -> Stage4 Simple (SummarizeActiveTab) -> Answer
```

Không hề đi qua Stage 3, không lập kế hoạch phức tạp.

---

### 3.2. Ví dụ 2 – Query hybrid phức tạp → AGENT_PATH

**User query:**

> “Giúp mình nghiên cứu gói datafeed Vietstock phù hợp cho FinAI và điền sẵn form đăng ký (đừng submit).”

**Bước 1 – Stage 1:**

- Lưu `user_query`, tạo `ContextPackV1` (URL trang Vietstock datafeed nếu đã mở…).

**Bước 2 – Stage 2:**

1. `S2_IntentClassifier`:

- intent: `research_then_action`
- entities:
  - vendor: `"Vietstock"`
  - product_domain: `"datafeed"`
- constraints:
  - `{ "no_submit": true }`
- risk_flags:
  - `["external_side_effect"]` (vì có form đăng ký trên trang ngoài)
- complexity:
  - has_action_word: true        (có “điền form đăng ký”)
  - has_multi_step_pattern: true (research gói + điền form)
  - action_type: "form_fill"
  - is_single_step: false
- slm_confidence: 0.88

2. `S2_TaskSpecBuilder` → `TaskSpecV1`:

```jsonc
TaskSpecV1 {
  "user_query": "Giúp mình nghiên cứu gói datafeed Vietstock phù hợp cho FinAI và điền sẵn form đăng ký (đừng submit).",
  "intent": "research_then_action",
  "entities": {
    "vendor": "Vietstock",
    "product_domain": "datafeed"
  },
  "constraints": {
    "no_submit": true
  },
  "risk_flags": ["external_side_effect"],
  "meta": {
    "has_action_word": true,
    "has_multi_step_pattern": true,
    "action_type": "form_fill",
    "is_single_step": false,
    "slm_confidence": 0.88
  }
}
```

3. `S2_RuleRouter` kiểm tra:

- intent = `research_then_action` → **không** phải research thuần → loại FAST_PATH.
- has_action_word = true, action_type = form_fill → action thực sự → loại FAST_PATH.
- has_multi_step_pattern = true → multi-step → loại FAST_PATH.
- risk_flags chứa `external_side_effect` → loại FAST_PATH.

→ **Không thỏa điều kiện fast path**, nên giữ:

```jsonc
RoutingDecision { "path": "AGENT_PATH" }
```

**Bước 3 – Stage 3 (Planner LLM):**

- Nhận `TaskSpecV1` từ Stage 2.
- Dựa trên intent + entities + constraints + context, sinh `PlanBundleV1`, ví dụ (mô tả miệng):

  - Bước 1: Hiểu nhu cầu datafeed cho FinAI (loại dữ liệu, tần suất, thị trường…).  
  - Bước 2: Đọc trang Vietstock datafeed, trích thông tin các gói liên quan.  
  - Bước 3: So sánh các gói theo tiêu chí FinAI (phù hợp sản phẩm, chi phí, pháp lý…).  
  - Bước 4: Điền trước form đăng ký với gói được khuyến nghị **nhưng không submit** (tôn trọng `no_submit`).  

- PlanBundleV1 còn kèm theo:
  - ExecutionPlan (các step RETRIEVE / FETCH_DATA / COMPUTE / ACT),
  - gates/policy (có thể thêm confirm),
  - budget estimate, v.v. (chi tiết thuộc Stage 3 spec).

**Bước 4 – Stage 4 (Agent Executor):**

- Nhận `PlanBundleV1`.
- Thực thi từng step theo plan:
  - RETRIEVE: tóm tắt yêu cầu module FinAI.
  - FETCH_DATA: parse bảng gói datafeed trên trang Vietstock.
  - COMPUTE: so sánh, chọn gói phù hợp.
  - ACT: điền form đăng ký (không submit, do constraint).

- Trả lại cho user:
  - Gợi ý gói datafeed phù hợp,
  - Giải thích ngắn lý do chọn,
  - (Optional) thông báo “form đã được điền sẵn, bạn kiểm tra rồi tự submit nếu muốn”.

**Pipeline rút gọn:**

```text
User -> Stage1 -> Stage2 (SLM + Router: AGENT_PATH)
     -> Stage3 Planner (LLM sinh PlanBundleV1)
     -> Stage4 Agent Executor (thi công theo plan) -> Answer
```

Ở đây, Stage 2 làm đúng vai trò “thư ký”: nhận diện đây là yêu cầu **hybrid phức tạp + có action + có rủi ro**, nên không cho đi fast path, mà bắt đi **đường đầy đủ Stage 3 + 4**.

---

Tài liệu này mô tả Stage 2 theo đúng những gì đã bàn trong trao đổi:  
- Dùng **một SLM** cho phần Query Understanding + risk/complexity tagging.  
- Dùng **Rule-based Router** để cẩn trọng quyết FAST_PATH vs AGENT_PATH.  
- Không bịa thêm module/khái niệm ngoài các khối đã nói: `TaskSpecV1`, `RoutingDecision`, Stage 3 planner và Stage 4 executor.
