# Tool Registry Spec (User cá nhân) — Agentic Comet-like Browser (v2)

Ngày: 2025-12-12  
Phiên bản: **v2** (tối ưu Core Tools + bổ sung tool con cho browser/form/tab/upload/captcha)  
Phạm vi: Bộ **tool/skill** dành cho người dùng cá nhân, tối ưu cho 3 nhu cầu chính:
- **A. Travel & concierge cá nhân**
- **B. Shopping (deal + spec intelligence)**
- **C. Creator & solo business ops**

---

## Changelog (v1 → v2)
- Bổ sung **tab/window lifecycle**: `browser_new_tab`, `browser_switch_tab`, `browser_close_tab`, `browser_list_tabs`
- Bổ sung **form primitives**: `browser_select_option`, `browser_check`, `browser_uncheck`, `browser_press_key`, `browser_upload_file`
- Bổ sung **text-first extraction**: `browser_read_text` (trích text theo selector, ít phụ thuộc schema)
- Bổ sung **anti-bot handoff**: `human_solve_challenge` (CAPTCHA/2FA/OTP: agent dừng và nhờ user xử lý)
- Chuẩn hoá “tool result envelope” và thêm **risk_level + permission_scope** theo tool
- Tách rõ: **Tool (Primitive)** vs **Skill (Workflow)** để router gọi ổn định hơn

---

## 1) Quy ước đặt tên & an toàn

### 1.1. Quy ước đặt tên
- Tool theo chuẩn **`verb_object`** (ví dụ: `browser_click`, `user_profile_get`)
- Skill theo chuẩn **`domain_verb_task`** (ví dụ: `travel_plan_itinerary`, `shopping_track_price`)

### 1.2. Permission scopes (để Gatekeeper dễ kiểm soát)
- `READ_ONLY`: chỉ đọc, không thay đổi trạng thái hệ thống
- `WRITE_NON_DESTRUCTIVE`: điền form/draft, không submit/publish/pay
- `SUBMIT`: submit form (visa/apply/contact…), gửi dữ liệu ra ngoài
- `PUBLISH`: đăng bài, gửi comment, public actions
- `PAYMENT`: hành động tốn tiền (pay/place order/book)
- `DESTRUCTIVE`: xoá/huỷ/đổi thông tin có thể khó khôi phục

> Nguyên tắc: Tool có scope từ `SUBMIT` trở lên thường phải kèm `requires_confirmation=true`.

### 1.3. Guardrails tối thiểu (khuyến nghị bắt buộc)
- Không tự động **PAYMENT / SUBMIT / PUBLISH / DESTRUCTIVE** nếu chưa có xác nhận người dùng.
- Các thao tác “nhạy cảm” phải đi qua `request_user_confirmation`.
- Nếu gặp **CAPTCHA/OTP/2FA**, agent phải dừng và gọi `human_solve_challenge`.

---

## 2) Bảng phân loại tool

| Nhóm | Mục tiêu | Loại | Tool/Skill |
|---|---|---|---|
| Browser Navigation | Điều hướng & quản lý tab | Tool | `browser_navigate`, `browser_new_tab`, `browser_switch_tab`, `browser_close_tab`, `browser_list_tabs`, `browser_wait` |
| Browser Interaction | Click/Type/Scroll/Keys/Select/Checkbox | Tool | `browser_click`, `browser_type`, `browser_scroll`, `browser_press_key`, `browser_select_option`, `browser_check`, `browser_uncheck` |
| Files in Browser | Upload/Download | Tool | `browser_upload_file`, `browser_download` |
| Capture & Extraction | Ảnh chụp, DOM, text, extract schema | Tool | `browser_screenshot`, `browser_get_dom`, `browser_read_text`, `browser_extract` |
| Search & Compare | Tìm nguồn + chuẩn hoá so sánh | Tool | `web_search`, `normalize_compare` |
| User Data | Hồ sơ sở thích & ràng buộc | Tool | `user_profile_get`, `user_profile_set` |
| Files & Docs | Lưu/đọc giấy tờ, media | Tool | `files_store`, `files_get`, `files_tag` |
| Auth | Kết nối OAuth/token | Tool | `auth_oauth_connect` |
| Watch & Notify | Theo dõi thay đổi + thông báo | Tool | `watch_create`, `watch_poll`, `notify_send` |
| Safety Gate | Xác nhận & xử lý anti-bot | Tool | `request_user_confirmation`, `human_solve_challenge` |
| Travel Pack | Lập kế hoạch/đặt dịch vụ/monitor | Skill | `travel_plan_itinerary`, `travel_search_options`, `travel_fill_forms`, `travel_monitor_trip` |
| Shopping Pack | So sánh/track giá/checkout | Skill | `shopping_extract_specs`, `shopping_track_price`, `shopping_compare_options`, `shopping_prepare_checkout` |
| Creator Pack | Research → plan → đăng bài | Skill | `creator_collect_research`, `creator_plan_calendar`, `creator_schedule_post`, `creator_triage_inbox` |

---

## 3) Tool Spec (Primitive Tools)

> Mỗi tool dưới đây mô tả: **Chức năng** (what), **Nhiệm vụ** (how/constraints), **Kết quả** (outputs), **Ví dụ**.  
> Ngoài ra có thêm 2 thuộc tính để team dev “gating” dễ: `permission_scope`, `risk_level`.

### 3.0. Tool Result Envelope (chuẩn dùng chung)

#### ToolResultV2
```json
{
  "status": "ok|error",
  "trace_id": "uuid",
  "permission_scope": "READ_ONLY|WRITE_NON_DESTRUCTIVE|SUBMIT|PUBLISH|PAYMENT|DESTRUCTIVE",
  "risk_level": "low|medium|high",
  "current_url": "optional",
  "artifacts": [{"type":"screenshot|html|download|text|json", "ref":"..."}],
  "data": {},
  "error": { "code":"...", "message":"..." }
}
```

---

## 3A) Browser Navigation / Tab Management

### 3A.1. `browser_navigate`
- **Chức năng:** Mở URL trong tab hiện tại.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE` (vì thay đổi trạng thái trình duyệt)
- **risk_level:** low
- **Nhiệm vụ:** hỗ trợ `wait_until` (domcontentloaded/networkidle).
- **Ví dụ:**
```json
{ "url":"https://example.com/flights", "wait_until":"networkidle" }
```

### 3A.2. `browser_new_tab`
- **Chức năng:** Mở tab mới (có thể kèm URL).
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "url":"https://example.com/hotels" }
```

### 3A.3. `browser_switch_tab`
- **Chức năng:** Chuyển tab theo `tab_id`.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "tab_id":"tab-3" }
```

### 3A.4. `browser_list_tabs`
- **Chức năng:** Liệt kê tab đang mở (id + title + url).
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "include_favicons": false }
```

### 3A.5. `browser_close_tab`
- **Chức năng:** Đóng tab.
- **permission_scope:** `DESTRUCTIVE`
- **risk_level:** medium
- **requires_confirmation:** khuyến nghị **true** nếu đóng tab có form đang điền.
- **Ví dụ:**
```json
{ "tab_id":"tab-3" }
```

### 3A.6. `browser_wait`
- **Chức năng:** Chờ điều kiện (timeout, selector xuất hiện, network idle).
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "until":"selector", "selector":".results", "timeout_ms":15000 }
```

---

## 3B) Browser Interaction / Form Primitives

### 3B.1. `browser_click`
- **Chức năng:** Click element theo selector.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":"button#search" }
```

### 3B.2. `browser_type`
- **Chức năng:** Nhập text vào input/textarea.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":"input[name='destination']", "text":"Tokyo", "clear_first":true }
```

### 3B.3. `browser_scroll`
- **Chức năng:** Scroll trang.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "amount_px": 1200 }
```

### 3B.4. `browser_press_key`
- **Chức năng:** Gửi phím (Enter/Escape/Tab/ArrowDown…).
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "keys":["TAB","TAB","ENTER"] }
```

### 3B.5. `browser_select_option`
- **Chức năng:** Chọn option cho `<select>` hoặc dropdown đã xác định selector.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":"select#cabin", "value":"economy" }
```

### 3B.6. `browser_check` / `browser_uncheck`
- **Chức năng:** Tick/untick checkbox.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":"input#agree_terms" }
```

---

## 3C) Files in Browser

### 3C.1. `browser_upload_file`
- **Chức năng:** Upload file vào input type=file (visa docs, KYC, media…).
- **permission_scope:** `SUBMIT` (vì file sẽ rời máy user)
- **risk_level:** high
- **requires_confirmation:** **true**
- **Ví dụ:**
```json
{ "selector":"input[type='file']#passport", "file_ref":"file://passport.png" }
```

### 3C.2. `browser_download`
- **Chức năng:** Tải file từ URL hoặc click-to-download.
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "url":"https://example.com/booking.pdf" }
```

---

## 3D) Capture & Extraction

### 3D.1. `browser_screenshot`
- **Chức năng:** Chụp ảnh màn hình.
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "full_page": true }
```

### 3D.2. `browser_get_dom`
- **Chức năng:** Lấy DOM/HTML (toàn trang hoặc theo selector).
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":"#product-details" }
```

### 3D.3. `browser_read_text`
- **Chức năng:** Trích **text thuần** theo selector (dùng cho “đọc nhanh”, kiểm tra điều khoản).
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "selector":".cancellation-policy" }
```

### 3D.4. `browser_extract`
- **Chức năng:** Trích thông tin theo **schema JSON**.
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Nhiệm vụ:** trả `confidence` + `missing_fields`.
- **Ví dụ:**
```json
{
  "schema": { "price_total":"number", "currency":"string", "cancellation_policy":"string" },
  "source": { "type":"dom", "selector":"#checkout-summary" }
}
```

---

## 3E) Search & Compare

### 3E.1. `web_search`
- **Chức năng:** Tìm kiếm web theo query.
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{ "query":"carry-on size ANA 2025", "locale":"vi-VN", "max_results":5 }
```

### 3E.2. `normalize_compare`
- **Chức năng:** Chuẩn hoá nhiều lựa chọn về cùng schema để so sánh.
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ:**
```json
{
  "schema": {"total_cost":"number","warranty_months":"number","return_days":"number"},
  "items":[
    {"source":"storeA","raw":{"price":100,"ship":5,"warranty":"12m"}},
    {"source":"storeB","raw":{"price":98,"delivery":12,"warranty_months":24}}
  ]
}
```

---

## 3F) User Data / Files / Auth

### 3F.1. `user_profile_get` / `user_profile_set`
- **Chức năng:** Lưu & lấy preference của user.
- **permission_scope:** `READ_ONLY` (get) / `WRITE_NON_DESTRUCTIVE` (set)
- **risk_level:** medium (vì liên quan dữ liệu cá nhân)
- **Ví dụ (set):**
```json
{ "set": { "travel.preferred_airlines":["VN","NH"], "shopping.budget_vnd":25000000 } }
```

### 3F.2. `files_store` / `files_get` / `files_tag`
- **Chức năng:** Quản lý file (passport, booking, media…).
- **permission_scope:** `WRITE_NON_DESTRUCTIVE` (store/tag) / `READ_ONLY` (get)
- **risk_level:** medium
- **Ví dụ (store):**
```json
{ "file_path":"file://passport.png", "tags":["travel","passport"], "note":"scan 2025" }
```

### 3F.3. `auth_oauth_connect`
- **Chức năng:** Kết nối OAuth/token tới provider.
- **permission_scope:** `SUBMIT`
- **risk_level:** high
- **requires_confirmation:** **true**
- **Ví dụ:**
```json
{ "provider":"google", "scopes":["youtube.upload","openid","email"] }
```

---

## 3G) Watch & Notify

### 3G.1. `watch_create` / `watch_poll`
- **Chức năng:** Theo dõi thay đổi (giá, booking status…).
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Ví dụ (create):**
```json
{
  "target": { "url":"https://store.com/p/123", "selector":"#price" },
  "trigger_rules": [{ "op":"<=", "value": 19990000 }],
  "frequency":"6h"
}
```

### 3G.2. `notify_send`
- **Chức năng:** Gửi thông báo (push/in-app/email tuỳ sản phẩm).
- **permission_scope:** `WRITE_NON_DESTRUCTIVE`
- **risk_level:** low
- **Ví dụ:**
```json
{ "channel":"push", "title":"Giá đã giảm", "message":"Sản phẩm X xuống 19.99M" }
```

---

## 3H) Safety Gate / Anti-bot Handoff

### 3H.1. `request_user_confirmation`
- **Chức năng:** User duyệt trước hành động nhạy cảm (SUBMIT/PUBLISH/PAYMENT/DESTRUCTIVE).
- **permission_scope:** `READ_ONLY` (tool này chỉ “hỏi”, không hành động)
- **risk_level:** low
- **Output:**
```json
{ "approved": true, "user_edits": {}, "reason": "" }
```
- **Ví dụ:**
```json
{
  "action_summary":"Đặt vé HAN→NRT ngày 2026-02-10",
  "cost_estimate": { "amount": 12500000, "currency":"VND" },
  "fields_to_submit": { "name":"...", "passport_no":"..." },
  "risks":["Không hoàn/đổi vé", "Hành lý 7kg"]
}
```

### 3H.2. `human_solve_challenge`
- **Chức năng:** Dừng workflow và yêu cầu user xử lý CAPTCHA/OTP/2FA hoặc xác minh “tôi không phải bot”.
- **permission_scope:** `READ_ONLY`
- **risk_level:** low
- **Nhiệm vụ:** trả trạng thái “resolved/failed/timeout”.
- **Ví dụ:**
```json
{ "challenge_type":"captcha", "page_hint":"Login checkout", "timeout_ms":120000 }
```

---

## 4) Skill Spec (Workflow Skills)

> Skills là tool “cấp cao” (nhiều bước) — triển khai nội bộ bằng primitives.  
> Với MVP user cá nhân, ưu tiên skills để ổn định & dễ đo chất lượng.

---

## 4A) Travel Pack

### 4A.1. `travel_plan_itinerary`
- **Chức năng:** Lập lịch trình theo constraint.
- **Nhiệm vụ:** lấy preference từ `user_profile_get`, dùng `web_search`/`browser_extract`, trả tradeoffs.
- **Kết quả:** `{itinerary, tradeoffs, plan_score, status}`
- **Ví dụ:**
```json
{ "origin":"HAN", "destination":"NRT", "dates":{"from":"2026-02-10","to":"2026-02-14"}, "budget_vnd":30000000 }
```

### 4A.2. `travel_search_options`
- **Chức năng:** Tìm & chuẩn hoá lựa chọn bay/khách sạn.
- **Kết quả:** `{options, normalized_terms, status}`
- **Ví dụ:** `{ "type":"flight", "route":"HAN-NRT", "date":"2026-02-10", "pax":1 }`

### 4A.3. `travel_fill_forms`
- **Chức năng:** Điền form visa/booking/arrival card.
- **Nhiệm vụ:** dùng `browser_upload_file` nếu cần; **bắt buộc** `request_user_confirmation` trước submit.
- **Kết quả:** `{filled_preview_ref, submit_ready, status}`
- **Ví dụ:** `{ "form_url":"https://visa.gov/apply", "docs":["passport_ref"], "profile_keys":["name","dob"] }`

### 4A.4. `travel_monitor_trip`
- **Chức năng:** Theo dõi delay/gate/booking status.
- **Kết quả:** `{watch_id, alerts, status}`
- **Ví dụ:** `{ "booking_refs":["file://booking.pdf"], "frequency":"1h" }`

---

## 4B) Shopping Pack

### 4B.1. `shopping_extract_specs`
- **Chức năng:** Trích spec theo category schema.
- **Kết quả:** `{spec_json, confidence, status}`
- **Ví dụ:** `{ "product_url":"https://store.com/laptop/abc", "category":"laptop_gaming_v1" }`

### 4B.2. `shopping_track_price`
- **Chức năng:** Theo dõi giá + ship + coupon.
- **Kết quả:** `{watch_id, last_price, status}`
- **Ví dụ:** `{ "url":"https://store.com/p/123", "target_price_vnd":19990000, "frequency":"6h" }`

### 4B.3. `shopping_compare_options`
- **Chức năng:** So sánh nhiều lựa chọn.
- **Kết quả:** `{comparison_table, recommendation, status}`
- **Ví dụ:** `{ "items":[{"url":"..."},{"url":"..."}], "schema":"shopping_compare_v1" }`

### 4B.4. `shopping_prepare_checkout`
- **Chức năng:** Chuẩn bị checkout (add-to-cart, điền địa chỉ), **không pay** khi chưa confirm.
- **Nhiệm vụ:** nếu gặp CAPTCHA/OTP thì gọi `human_solve_challenge`.
- **Kết quả:** `{checkout_ready, final_cost_breakdown, status}`
- **Ví dụ:** `{ "selected_option":{"url":"...","variant":"16GB/1TB"}, "address_ref":"file://addr.json" }`

---

## 4C) Creator Pack

### 4C.1. `creator_collect_research`
- **Chức năng:** Gom nguồn, trích ý chính, lưu note có trích dẫn.
- **Kết quả:** `{notes_ref, citations_map, status}`
- **Ví dụ:** `{ "topic":"AI browser trends 2025", "max_sources":8, "note_schema":"creator_notes_v1" }`

### 4C.2. `creator_plan_calendar`
- **Chức năng:** Lập lịch nội dung theo cadence/pillar.
- **Kết quả:** `{calendar, backlog, status}`
- **Ví dụ:** `{ "channels":["youtube","tiktok"], "cadence":"3_per_week", "pillars":["tech","build-in-public"] }`

### 4C.3. `creator_schedule_post`
- **Chức năng:** Tạo draft / lên lịch đăng qua web UI.
- **Nhiệm vụ:** publish phải confirm; gặp 2FA → `human_solve_challenge`.
- **Kết quả:** `{draft_links, publish_ready, status}`
- **Ví dụ:**
```json
{
  "channel":"youtube",
  "title":"...",
  "description":"...",
  "media_refs":["file://video.mp4"],
  "schedule_time":"2025-12-15T19:00:00+07:00"
}
```

### 4C.4. `creator_triage_inbox`
- **Chức năng:** Phân loại comment/inbox, đề xuất trả lời theo guideline.
- **Nhiệm vụ:** không tự xoá/block nếu chưa confirm.
- **Kết quả:** `{triage, suggested_replies, status}`
- **Ví dụ:** `{ "thread_urls":["...","..."], "policy_ref":"file://reply_policy.md" }`

---

## 5) MVP Core Tools — đã “đủ” chưa?

### 5.1. Bộ core tối thiểu (đủ chạy A/B/C)
- Tab/navigation: `browser_navigate`, `browser_new_tab`, `browser_switch_tab`, `browser_list_tabs`, `browser_wait`
- Interaction: `browser_click`, `browser_type`, `browser_scroll`, `browser_press_key`, `browser_select_option`, `browser_check/uncheck`
- Capture/extract: `browser_screenshot`, `browser_get_dom`, `browser_read_text`, `browser_extract`
- Files/auth: `browser_upload_file`, `browser_download`, `files_store/get`, `auth_oauth_connect`
- Watch/notify: `watch_create/poll`, `notify_send`
- Safety: `request_user_confirmation`, `human_solve_challenge`

### 5.2. Tool “nice-to-have” (để tăng độ bền)
- `browser_retry(action, policy)` (wrapper để xử lý flakiness)
- `browser_detect_state()` (đang login? có modal? có error banner?)
- `browser_extract_table()` (khi gặp bảng giá/spec dạng table)

---

## 6) Phụ lục

### 6.1. ConfirmResultV1
```json
{ "approved": true, "user_edits": {}, "reason": "" }
```
