# gstack — Garry Tan's Claude Code Operating System
> Source: https://github.com/garrytan/gstack
> Author: Garry Tan, President & CEO of Y Combinator
> Stars: 14.2k+ | License: MIT

## Tại sao quan trọng?
Garry Tan — CEO Y Combinator, nhà đầu tư hàng đầu thế giới — đã tạo ra gstack vì ông không muốn AI coding tools bị mắc kẹt trong **một chế độ chung chung**. Ông muốn **chuyển đổi cognitive mode** theo nhu cầu.

## 6 Skill Modes (6 "não bộ" khác nhau)

### 1. /plan-ceo-review — Founder/CEO Mode (Brian Chesky Mode)
- **Không** implement theo literal request
- **Hỏi:** "Sản phẩm này thực sự là gì?"
- Tìm **10-star version** ẩn trong mỗi request
- VD: "Upload ảnh" → thực ra là "giúp seller tạo listing bán được hàng"

### 2. /plan-eng-review — Eng Manager Mode
- Architecture, data flow, state transitions
- Failure modes, edge cases, trust boundaries
- **Buộc vẽ diagram** → lộ hidden assumptions
- Biến ý tưởng thành **buildable plan**

### 3. /review — Paranoid Staff Engineer Mode
- Tìm bugs mà CI không bắt được
- N+1 queries, race conditions, trust boundaries
- "Tưởng tượng production incident TRƯỚC khi nó xảy ra"
- Tích hợp Greptile (YC company) cho automated PR review

### 4. /ship — Release Engineer Mode
- Sync main → run tests → push → open PR
- Cho branch đã READY, không phải để quyết định build gì
- "Momentum matters — AI should not procrastinate"

### 5. /browse — QA Engineer Mode
- Cho agent "đôi mắt" — browse real URLs, take screenshots
- Full QA pass trong ~60 giây
- Persistent Chromium session via Playwright

### 6. /qa — QA Lead Mode
- Đọc git diff → tự tìm affected pages → test
- 4 modes: Diff-aware, Full, Quick, Regression

### 7. /retro — Engineering Manager Mode
- Phân tích commit history, work patterns, shipping velocity
- Team-aware: praise + growth opportunities cho từng contributor

## Philosophy của Garry Tan
> "Planning is not review. Review is not shipping. Founder taste is not engineering rigor. If you blur all of that together, you usually get a mediocre blend of all four."

> "I want explicit gears."

## Áp dụng cho PikaRobot Investment
- Dùng `/plan-ceo-review` mindset khi đánh giá product vision
- Dùng `/plan-eng-review` mindset khi thẩm định tech architecture
- Dùng `/review` mindset khi due diligence code quality
- KPI tracking → lấy cảm hứng từ `/retro` metrics

## Parallel Execution Model
- 10 Claude Code sessions cùng lúc, mỗi session 1 cognitive mode
- "One person, ten parallel agents" — cách Garry Tan build software
