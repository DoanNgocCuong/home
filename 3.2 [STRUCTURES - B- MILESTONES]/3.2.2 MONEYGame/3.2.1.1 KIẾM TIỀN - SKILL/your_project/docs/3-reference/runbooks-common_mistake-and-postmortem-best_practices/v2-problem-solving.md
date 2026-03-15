# 🔧 [PROB-ID]: [Tên vấn đề ngắn gọn]

> **1 câu:** [Mô tả vấn đề / mục tiêu — dưới góc nhìn người dùng hoặc hệ thống]

| Field | Value |
|-------|-------|
| **ID** | PROB-YYYY-MM-DD-[slug] |
| **Type** | 🐛 Bug / 🚀 Feature / ⚡ Perf / 🔧 Refactor |
| **Severity** | 🔴 SEV-1 / 🟠 SEV-2 / 🟡 SEV-3 / 🔵 SEV-4 |
| **Status** | 🔍 Investigating → 🧪 Experimenting → 🛠️ Implementing → ✅ Resolved |
| **Owner** | @username |
| **Started** | YYYY-MM-DD HH:MM |
| **Resolved** | YYYY-MM-DD HH:MM |
| **Duration** | Xh Ym |
| **Related** | [PR / Ticket / Slack / Doc links] |

---

# ═══════════════════════════════════════════════
# PHASE 1: VẤN ĐỀ — Chuyện gì đang xảy ra?
# ═══════════════════════════════════════════════

> _"Định nghĩa đúng vấn đề = giải quyết 50% vấn đề."_
> _Giải quyết triệu chứng ≠ Giải quyết nguyên nhân._

## 1.1 Trigger — Phát hiện vấn đề

**Phát hiện qua:** [ ] Alert / [ ] User report / [ ] Monitoring / [ ] Code review / [ ] Testing / [ ] Tự phát hiện

**Symptom — Người dùng / hệ thống thấy gì:**

```
[Paste error message / log / mô tả behavior bất thường]
```

**Expected vs Actual:**

| | Expected | Actual |
|--|----------|--------|
| Behavior | [Hệ thống nên làm gì] | [Hệ thống đang làm gì] |
| Metric | [Baseline bình thường] | [Giá trị bất thường] |

**Reproduce steps:**

```bash
# Các bước reproduce — càng cụ thể càng tốt
# Step 1:
# Step 2:
# Step 3:
# → Kết quả:
```

## 1.2 Problem Statement — Phát biểu vấn đề

> ⚠️ **Luật:** Viết SYMPTOM trước. Chưa viết ROOT CAUSE ở bước này.
> Tách rõ: Mô tả (What) ≠ Nguyên nhân (Why) ≠ Giải pháp (How).

**Problem Statement (1-3 câu):**

```
[WHO] đang gặp vấn đề [WHAT] khi [CONTEXT/WHEN].
Điều này gây ra [IMPACT — ảnh hưởng cụ thể, đo được nếu có].
Vấn đề xuất hiện từ [WHEN] và ảnh hưởng đến [SCOPE — bao nhiêu user / service / feature].
```

**Impact nhanh:**

| Category | Details |
|----------|---------|
| Users affected | ~X users (Y% of total) |
| Features affected | [List] |
| Revenue / SLA | [Ước tính nếu có] |

## 1.3 Context & Constraints — Bối cảnh và ràng buộc

> _Hiểu bối cảnh trước khi nhảy vào fix._

- **Hệ thống liên quan:** [Service A, Service B, Database X, ...]
- **Thay đổi gần đây:** [Deploy vX.Y.Z? Config change? Infra change?]
- **Ràng buộc:** [Deadline? Resource? Dependency? Không được downtime?]
- **Đã có ai fix trước chưa?:** [Link ticket / doc cũ nếu có]

---

# ═══════════════════════════════════════════════
# PHASE 2: NGUYÊN NHÂN — Tại sao xảy ra?
# ═══════════════════════════════════════════════

> _"Nghi ngờ suy nghĩ của chính mình. Trong mọi cuộc tìm giải pháp,_
> _đầu tiên hãy luôn nghĩ giải pháp của mình SAI."_
> _— First Principles: Bóc tách từng lớp, không chấp nhận bề mặt._

## 2.1 Hypothesis Generation — Đặt giả thuyết

> Liệt kê TẤT CẢ nguyên nhân có thể. Chưa cần đúng, cần ĐỦ.
> Dùng MECE: các giả thuyết không chồng chéo, bao phủ hết khả năng.

| # | Giả thuyết | Khả năng (%) | Cách kiểm chứng | Status |
|---|-----------|--------------|------------------|--------|
| H1 | [Nguyên nhân có thể 1] | [High/Med/Low] | [Lệnh / test / log check] | ⏳/✅/❌ |
| H2 | [Nguyên nhân có thể 2] | [High/Med/Low] | [Lệnh / test / log check] | ⏳/✅/❌ |
| H3 | [Nguyên nhân có thể 3] | [High/Med/Low] | [Lệnh / test / log check] | ⏳/✅/❌ |

## 2.2 Investigation Log — Kiểm chứng từng giả thuyết

> Format: `[HH:MM] Giả thuyết → Hành động → Kết quả → Kết luận`
> Viết LIVE. Không cần đẹp. Cần ĐÚNG và ĐỦ.

```
[HH:MM] ── Test H1: [Giả thuyết 1] ──
         Action: [Lệnh / thao tác cụ thể]
         Result: [Output thực tế]
         → ❌ LOẠI / ✅ XÁC NHẬN / ⚠️ CẦN THÊM DATA

[HH:MM] ── Test H2: [Giả thuyết 2] ──
         Action: [Lệnh / thao tác cụ thể]
         Result: [Output thực tế]
         → ❌ / ✅ / ⚠️

[HH:MM] 💡 Insight: [Phát hiện bất ngờ trong quá trình debug]
         → Điều này dẫn đến giả thuyết mới H4: [...]

[HH:MM] ── Test H4: [Giả thuyết mới] ──
         Action: [...]
         Result: [...]
         → ✅ XÁC NHẬN — Đây là root cause
```

**Debug commands đã dùng (lưu lại để sau dùng):**

```bash
# [Paste các lệnh hữu ích]
```

## 2.3 Root Cause — 5 Whys

> Hỏi "Tại sao?" cho đến khi tìm được điều CÓ THỂ FIX.

```
Symptom: [Triệu chứng ban đầu]

Why 1: Tại sao [symptom]?
  → Vì [A]

Why 2: Tại sao [A]?
  → Vì [B]

Why 3: Tại sao [B]?
  → Vì [C]

Why 4: Tại sao [C]?
  → Vì [D]

Why 5: Tại sao [D]?
  → ✅ ROOT CAUSE: [Điều có thể fix được]
```

**Contributing Factors (làm vấn đề tệ hơn / khó phát hiện hơn):**

| Factor | Ảnh hưởng | Preventable? |
|--------|-----------|--------------|
| [VD: Thiếu alert cho metric X] | Phát hiện trễ 15 phút | ✅ |
| [VD: Không có staging test] | Không catch trước deploy | ✅ |
| [VD: External dependency down] | Ngoài kiểm soát | ❌ |

---

# ═══════════════════════════════════════════════
# PHASE 3: GIẢI PHÁP — Các hướng xử lý (MECE)
# ═══════════════════════════════════════════════

> _"Không chỉ fix — mà phải tạo đòn bẩy mới từ chính vấn đề."_
> _Liệt kê TẤT CẢ options → Đánh giá → Chọn → Giải thích tại sao loại các cái khác._

## 3.1 Solution Space — Các phương án

| # | Option | Mô tả (1-2 câu) | Effort | Risk | Leverage | Trade-off |
|---|--------|------------------|--------|------|----------|-----------|
| A | [Tên] | [Mô tả] | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | [Pro / Con] |
| B | [Tên] | [Mô tả] | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | [Pro / Con] |
| C | [Tên] | [Mô tả] | 🟢/🟡/🔴 | 🟢/🟡/🔴 | 🟢/🟡/🔴 | [Pro / Con] |

> **Tiêu chí đánh giá:**
> - 🎯 Impact: Giải quyết triệt để vấn đề không?
> - ⏳ Urgency: Cần fix ngay hay có thể chờ?
> - 💪 Effort: Nguồn lực, thời gian cần bỏ ra?
> - 🔁 Leverage: Làm 1 lần dùng N lần? Có reuse được không?
> - ⚠️ Risk: Tệ nhất xảy ra là gì? Rollback được không?

## 3.2 Decision — Chọn phương án

> **Chọn: Option [X]**

| Item | Detail |
|------|--------|
| **Chọn** | Option [X]: [Tên] |
| **Lý do chọn** | [Tại sao option này tốt nhất cho context hiện tại] |
| **Rejected** | Option [Y] vì [lý do cụ thể], Option [Z] vì [lý do cụ thể] |
| **Rollback plan** | [Nếu option X fail thì làm gì?] |

---

# ═══════════════════════════════════════════════
# PHASE 4: THỬ NGHIỆM — Validate trước khi ship
# ═══════════════════════════════════════════════

> _Mỗi thử nghiệm = 1 giả thuyết + 1 test + 1 kết luận._
> _Fail nhanh, fail nhỏ, fail nhiều → tìm ra đáp án đúng._

## Experiment 1: [Tên thử nghiệm]

| Item | Detail |
|------|--------|
| **Giả thuyết** | Nếu làm [X] thì sẽ [Y] |
| **Setup** | _(xem code block bên dưới)_ |
| **Expected** | [Kết quả mong đợi] |
| **Actual** | [Kết quả thực tế] |
| **Kết luận** | ✅ Confirm / ❌ Reject — [Giải thích] |

```bash
# Setup / commands
```

```
# Output thực tế
```

---

## Experiment 2: [Tên thử nghiệm]

| Item | Detail |
|------|--------|
| **Giả thuyết** | [...] |
| **Setup** | _(xem code block)_ |
| **Expected** | [...] |
| **Actual** | [...] |
| **Kết luận** | ✅ / ❌ — [...] |

```bash
# Setup
```

```
# Output
```

---

# ═══════════════════════════════════════════════
# PHASE 5: TRIỂN KHAI — Implementation
# ═══════════════════════════════════════════════

## 5.1 Changes — Các thay đổi

**Files changed:**

| File | Change | Why |
|------|--------|-----|
| `path/to/file.py` | [Mô tả ngắn] | [Lý do] |
| `path/to/file2.py` | [Mô tả ngắn] | [Lý do] |

**Key code diff:**

```python
# ❌ BEFORE:
[code cũ — giải thích tại sao sai]

# ✅ AFTER:
[code mới — giải thích tại sao đúng]
```

## 5.2 Deploy steps

```bash
# Step 1: [Lệnh]
# Step 2: [Lệnh]
# Step 3: [Lệnh]
```

---

# ═══════════════════════════════════════════════
# PHASE 6: KIỂM TRA — Verify fix đã work
# ═══════════════════════════════════════════════

> ⚠️ Chạy TOÀN BỘ checklist **trước khi** đóng ticket.

## 6.1 Verification commands

```bash
# 1. Health check
# 2. Error rate check
# 3. Latency check
# 4. Specific scenario test
```

## 6.2 Verification checklist

- [ ] Symptom ban đầu đã hết (test lại reproduce steps)
- [ ] Error rate < [threshold] trong [X] phút liên tục
- [ ] Latency P99 trong ngưỡng bình thường
- [ ] Không có side effect mới
- [ ] Rollback plan đã test (nếu cần)
- [ ] Stakeholders đã được notify

## 6.3 Metrics Before vs After

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| [Error rate] | [X%] | [Y%] | < Z% |
| [Latency P99] | [Xms] | [Yms] | < Zms |
| [Throughput] | [X rps] | [Y rps] | > Z rps |
| [Custom] | [baseline] | [improved] | [target] |

---

# ═══════════════════════════════════════════════
# PHASE 7: ĐÚC KẾT — Kaizen & Knowledge Capture
# ═══════════════════════════════════════════════

> _"Không đo lường — Không cải tiến."_
> _Viết phần này SAU KHI resolve. Đúc kết từ Phase 1-6 thành knowledge tái sử dụng._

---

## 7.1 Common Mistakes — Các lỗi đã mắc

> Format: ❌ Sai (tại sao sai) → ✅ Đúng (tại sao đúng) → 🔍 Detect (cách tìm trong code)

### M-01: [Tên lỗi]

**Severity:** 🔴/🟠/🟡/🔵

❌ **Sai — Đừng làm thế này:**
```python
# [Code / approach sai]
```
> **Tại sao sai:** [Giải thích mechanism — VD: "Block event loop vì GIL contention"]

**Dấu hiệu nhận biết:**
```
[Error message / log pattern / metric bất thường khi lỗi này xảy ra]
```

✅ **Đúng — Làm thế này:**
```python
# [Code / approach đúng]
```
> **Tại sao đúng:** [Giải thích — VD: "Async LPUSH chỉ tốn ~1ms, không block"]

🔍 **Detect trong codebase:**
```bash
grep -rn "[pattern sai]" src/ --include="*.py"
```

---

### M-02: [Tên lỗi]

**Severity:** 🔴/🟠/🟡/🔵

❌ **Sai:**
```python
```

✅ **Đúng:**
```python
```

🔍 **Detect:**
```bash
```

---

## 7.2 Best Practices Checklist — Rút ra từ vấn đề này

> ✅ Must-have — Bắt buộc | ⚠️ Should-have — Nên có | 💡 Nice-to-have

### [Category 1 — VD: Architecture]

- [ ] ✅ [Practice 1 — mô tả cụ thể, actionable]
- [ ] ✅ [Practice 2]
- [ ] ⚠️ [Practice 3]

### [Category 2 — VD: Error Handling]

- [ ] ✅ [Practice 4]
- [ ] 💡 [Practice 5]

### Verification commands cho checklist:
```bash
# Lệnh verify các best practices trên
```

---

## 7.3 Action Items — Ngăn tái phát

| # | Action | Priority | Owner | Due | Status | Ticket |
|---|--------|----------|-------|-----|--------|--------|
| 1 | [Ngắn hạn — VD: Thêm alert] | P1 | @name | YYYY-MM-DD | ⏳ | #123 |
| 2 | [Trung hạn — VD: Refactor module X] | P2 | @name | YYYY-MM-DD | ⏳ | #124 |
| 3 | [Dài hạn — VD: Thêm chaos test] | P3 | @name | YYYY-MM-DD | ❌ | #125 |

**Detection improvements (phát hiện sớm hơn lần sau):**

- [ ] Alert: `[metric] > [threshold] for [duration]`
- [ ] Dashboard: `[tên panel mới]`
- [ ] Log: `[thêm log gì, ở đâu]`
- [ ] Test: `[scenario mới cần cover]`

---

## 7.4 Lessons Learned

**Làm tốt ✅ (lặp lại):**
- [Điều gì work tốt trong quá trình xử lý]

**Cần cải thiện ⚠️ (fix process):**
- [Điều gì chưa tốt, cần thay đổi quy trình]

**Câu hỏi mở ❓ (research thêm):**
- [Điều chưa trả lời được]

---

## 7.5 Quick Reference Card

> Copy-paste vào onboarding doc / team wiki.

```
╔══════════════════════════════════════════════════════════╗
║  [SYSTEM] — Quick Ref from PROB-YYYY-MM-DD-[slug]       ║
╠══════════════════════════════════════════════════════════╣
║  🔴 M-01: [Tên lỗi] → [1 câu fix]                      ║
║  🟠 M-02: [Tên lỗi] → [1 câu fix]                      ║
╠══════════════════════════════════════════════════════════╣
║  ✅ BP-01: [Best practice 1 câu]                         ║
║  ✅ BP-02: [Best practice 1 câu]                         ║
╠══════════════════════════════════════════════════════════╣
║  Debug: [1 lệnh debug hữu ích nhất]                     ║
║  Doc: [link tới file này]                                ║
╚══════════════════════════════════════════════════════════╝
```

---

# APPENDIX

## A. Relevant logs

```
[Paste log quan trọng — REDACT PII / secrets trước khi paste]
```

## B. System diagram / Architecture

```
[ASCII diagram hoặc link tới hình]
```

## C. References

- [Link 1 — mô tả]
- [Link 2 — mô tả]

## D. Communication log

| Time | Channel | Message |
|------|---------|---------|
| HH:MM | [Slack / Email] | [Tóm tắt thông báo] |

---

# REPORT FORMAT (Dùng khi báo cáo cho stakeholder)

> Copy section này khi cần gửi report ngắn gọn cho manager / team khác.

```
1. VẤN ĐỀ:    [1-2 câu từ Problem Statement]
   IMPACT:     [Users affected, SLA, Revenue]
   METRICS:    [Key metric before → after]

2. NGUYÊN NHÂN: [Root cause 1-2 câu]
   DẪN CHỨNG:   [Log / metric / data cụ thể]

3. GIẢI PHÁP:  [Đã làm gì để fix]
   DẪN CHỨNG:   [Metrics after fix]

4. PREVENT:    [Action items ngắn gọn]
```

---

*Created by `@owner` on `YYYY-MM-DD` · Last updated: `YYYY-MM-DD`*
*Naming: `PROB-YYYY-MM-DD-[slug].md` — VD: `PROB-2026-03-10-langfuse-hierarchy.md`*