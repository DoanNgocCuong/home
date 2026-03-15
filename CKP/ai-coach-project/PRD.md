# PRD: AI Executive Coach — "CoachGPT"
## Personal AI Coaching Assistant cho Founder/CEO

---

## 1. Problem Statement

Founder/CEO thường cô đơn ở vị trí lãnh đạo. Họ cần một "executive coach" luôn sẵn sàng 24/7 để:
- Đặt câu hỏi đúng thay vì đưa lời khuyên (coaching methodology)
- Nhắc nhở mục tiêu, habits, và commitments
- Giúp reflect và ra quyết định quan trọng
- Track năng lượng và trạng thái tinh thần

**Giải pháp:** AI Coach sử dụng phương pháp coaching chuyên nghiệp (ICF-aligned), kết hợp nhắc nhở thông minh và journaling để mở khóa tiềm năng lãnh đạo.

---

## 2. Target User

**Primary Persona:** Founder/CEO startup giai đoạn early-stage đến Series A
- 25-45 tuổi
- Quản lý 5-50 người
- Đang đối mặt: scaling team, fundraising, product-market fit, burnout
- Chưa có budget cho executive coach ($500-2000/tháng)
- Quen dùng AI tools (ChatGPT, Claude, Notion AI)

---

## 3. Core Features

### 3.1 AI Coaching Engine (Core)
- **Coaching Conversations:** AI đặt câu hỏi mở theo phương pháp GROW model
  - Goal → Reality → Options → Will
- **Powerful Questions:** Hệ thống 200+ câu hỏi coaching theo context
- **Active Listening Simulation:** Paraphrase, reflect feelings, summarize
- **Challenge Mode:** Khi user stuck, AI đặt câu hỏi provocative để breakthrough
- **No-Advice Rule:** AI KHÔNG đưa lời khuyên trực tiếp — chỉ đặt câu hỏi và mirror

### 3.2 Smart Reminders & Check-ins
- **Morning Check-in:** "Hôm nay mục tiêu #1 của bạn là gì?"
- **Energy Tracking:** 3x/ngày hỏi năng lượng (1-10) + mood
- **Commitment Reminders:** Track những gì user cam kết sẽ làm
- **Weekly Review:** Tổng hợp tuần — wins, challenges, learnings
- **Monthly Reflection:** Deep reflection về OKR progress

### 3.3 Journaling & Reflection
- **Daily Journal Prompts:** Câu hỏi reflection khác nhau mỗi ngày
- **Decision Journal:** Ghi lại quyết định quan trọng + reasoning
- **Gratitude Log:** 3 điều biết ơn mỗi ngày
- **Pattern Recognition:** AI phát hiện patterns từ journal entries qua thời gian

### 3.4 Goal & OKR Tracking
- **OKR Setup:** Giúp define Objectives + Key Results
- **Weekly OKR Check-in:** Progress update + coaching around blockers
- **Alignment Check:** OKR có align với vision dài hạn không?
- **Pivot Detection:** Nhận biết khi cần pivot mục tiêu

### 3.5 Dashboard & Analytics
- **Energy Heatmap:** Visualize năng lượng theo ngày/tuần/tháng
- **Mood Trends:** Trend line mood + correlation với events
- **Coaching Insights:** Top themes, breakthroughs, recurring blocks
- **Accountability Score:** % commitments hoàn thành

---

## 4. Technical Architecture

### 4.1 Tech Stack
```
Backend:    Python 3.12 + FastAPI + SQLAlchemy + Alembic
Database:   PostgreSQL 16 (primary) + Redis (cache + sessions)
AI Engine:  Anthropic Claude API (coaching conversations)
Frontend:   React 18 + TypeScript + Tailwind + Vite
Messaging:  WebSocket (real-time) + Scheduled jobs (APScheduler)
Auth:       JWT + OAuth2 (Google login)
Testing:    Pytest + Playwright (E2E)
```

### 4.2 Database Schema (Core Tables)
```
users              — user profile, preferences, timezone
conversations      — coaching sessions, context
messages           — individual messages in conversations
reminders          — scheduled check-ins & reminders
journal_entries    — daily journals, decision journals
energy_logs        — energy/mood tracking data points
goals              — OKR objectives
key_results        — measurable key results under goals
commitments        — action items user commits to
coaching_insights  — AI-generated patterns & insights
```

### 4.3 API Endpoints (Main)
```
Auth:
  POST   /api/auth/register
  POST   /api/auth/login
  POST   /api/auth/google
  GET    /api/auth/me

Coaching:
  POST   /api/coaching/session          — start new session
  POST   /api/coaching/message          — send message, get AI response
  GET    /api/coaching/sessions         — list sessions
  GET    /api/coaching/session/{id}     — get session detail

Reminders:
  GET    /api/reminders                 — list active reminders
  POST   /api/reminders                 — create reminder
  PATCH  /api/reminders/{id}            — update/snooze
  POST   /api/reminders/check-in       — submit check-in response

Journal:
  POST   /api/journal                   — create entry
  GET    /api/journal                   — list entries (paginated)
  GET    /api/journal/prompts           — get today's prompt
  GET    /api/journal/patterns          — AI pattern analysis

Goals:
  CRUD   /api/goals                     — OKR management
  CRUD   /api/goals/{id}/key-results    — Key Results
  POST   /api/goals/check-in           — weekly OKR check-in
  GET    /api/goals/alignment           — alignment analysis

Analytics:
  GET    /api/analytics/energy          — energy heatmap data
  GET    /api/analytics/mood            — mood trends
  GET    /api/analytics/insights        — coaching insights
  GET    /api/analytics/accountability  — commitment completion rate

Dashboard:
  GET    /api/dashboard                 — aggregated dashboard data
```

### 4.4 AI Coaching Prompt Architecture
```
System Prompt Layers:
  1. Base Coaching Identity — ICF-aligned coach persona
  2. GROW Model Framework — structured questioning flow
  3. User Context Injection — goals, recent journals, energy data
  4. Conversation Memory — recent session summaries
  5. Powerful Questions Bank — context-appropriate questions
  6. Safety Rails — detect crisis, suggest professional help
```

---

## 5. Parallel Agent Execution Plan

### Đây là phần quan trọng nhất — cách chia project cho 6 parallel Claude agents:

```
┌─────────────────────────────────────────────────┐
│           PHASE 0: SPEC & PLAN (5 min)          │
│  Human viết PRD này → Claude plan review        │
└───────────────┬─────────────────────────────────┘
                │
    ┌───────────▼───────────┐
    │  PHASE 1: PARALLEL    │
    │  6 agents, 30-45 min  │
    └───────────┬───────────┘
                │
  ┌─────┬──────┼──────┬─────┬──────┐
  ▼     ▼      ▼      ▼     ▼      ▼
┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│ A1 ││ A2 ││ A3 ││ A4 ││ A5 ││ A6 │
│DB+ ││Core││Rem ││Jour││Goal││Fron│
│Auth││AI  ││inder│nal ││OKR ││tend│
└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘
   │     │     │     │     │     │
   └─────┴─────┴──┬──┴─────┴─────┘
                   │
    ┌──────────────▼──────────────┐
    │  PHASE 2: INTEGRATION       │
    │  1 agent, 15 min            │
    │  Merge + Fix conflicts      │
    └──────────────┬──────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  PHASE 3: QA + SHIP         │
    │  2 agents parallel, 10 min  │
    │  Agent 7: Test suite        │
    │  Agent 8: Review + PR       │
    └─────────────────────────────┘
```

### Agent Assignments:

**Agent 1 — Database & Auth (worktree: agent-db-auth)**
```
Files: models/, alembic/, auth/, middleware/
Tasks:
  - SQLAlchemy models cho 10 tables
  - Alembic migrations
  - JWT auth + Google OAuth
  - User middleware
  - Unit tests cho models
```

**Agent 2 — AI Coaching Engine (worktree: agent-coaching)**
```
Files: services/coaching/, prompts/, services/ai/
Tasks:
  - Claude API integration
  - GROW model conversation flow
  - Powerful questions bank (200+ questions)
  - Context injection pipeline
  - Conversation memory management
  - Safety detection
```

**Agent 3 — Reminders & Check-ins (worktree: agent-reminders)**
```
Files: services/reminders/, api/reminders/, jobs/
Tasks:
  - Reminder CRUD API
  - APScheduler jobs (morning, energy, weekly)
  - Check-in submission flow
  - Timezone-aware scheduling
  - WebSocket notifications
```

**Agent 4 — Journal & Reflection (worktree: agent-journal)**
```
Files: services/journal/, api/journal/
Tasks:
  - Journal CRUD API
  - Daily prompt generator
  - Decision journal with reasoning capture
  - Pattern recognition (AI analysis of entries)
  - Gratitude log
```

**Agent 5 — Goals & OKR (worktree: agent-goals)**
```
Files: services/goals/, api/goals/, api/analytics/
Tasks:
  - OKR CRUD API
  - Weekly check-in flow
  - Alignment analysis logic
  - Accountability scoring
  - Analytics endpoints (energy, mood, insights)
```

**Agent 6 — Frontend (worktree: agent-frontend)**
```
Files: frontend/
Tasks:
  - React app scaffold (Vite + TS + Tailwind)
  - Auth pages (login, register)
  - Dashboard page (charts, metrics)
  - Coaching chat UI (real-time WebSocket)
  - Journal & Goals pages
  - Responsive mobile layout
```

---

## 6. Deploy Recommendation

### So sánh các options:

| Platform | Cost | Ưu điểm | Nhược điểm | Phù hợp? |
|----------|------|----------|-------------|-----------|
| **Local Docker** | $0 | Nhanh nhất, full control, iterate thoải mái | Không share được, không test mobile | Tốt cho dev |
| **Railway** | $0-5/mo | Deploy 1 click, free tier đủ dùng, có URL thật | Limited resources, cold start | ⭐ RECOMMENDED |
| **Render** | $0-7/mo | Free PostgreSQL, auto-deploy từ Git | Slow cold start (30s), limited free tier | Tốt |
| **AWS/GCP** | $20-50/mo | Production-grade, full control | Overkill cho practice, setup phức tạp | Chưa cần |

### ⭐ Em recommend: Railway

**Lý do:**
1. **Deploy = 1 lệnh:** `railway up` — không cần Dockerfile, tự detect Python
2. **Free PostgreSQL + Redis:** Không setup gì thêm
3. **URL thật ngay lập tức:** `coachgpt-xxx.up.railway.app` — test trên điện thoại được
4. **Auto-deploy từ GitHub:** Push code → auto deploy, giống production thật
5. **$5 credit free/tháng:** Đủ cho practice project
6. **Dễ teardown:** Xóa project = xóa hết, không sợ bị charge

**Workflow thực tế:**
```
Local Docker (dev) → Push GitHub → Railway auto-deploy (staging)
```

---

## 7. Success Criteria

- [ ] User có thể đăng ký, login (Google OAuth)
- [ ] Coaching chat hoạt động real-time (WebSocket)
- [ ] AI đặt câu hỏi theo GROW model, KHÔNG đưa lời khuyên
- [ ] Morning check-in tự động gửi notification
- [ ] Energy tracking 3x/ngày với heatmap visualization
- [ ] Journal entries với AI pattern recognition
- [ ] OKR setup + weekly check-in flow
- [ ] Dashboard với charts (energy, mood, accountability)
- [ ] Mobile responsive
- [ ] Full test suite (unit + integration + E2E)
- [ ] Deploy được trên Railway
- [ ] Toàn bộ build bằng Claude parallel agents pipeline

---

## 8. File Structure

```
coachgpt/
├── CLAUDE.md                    # AI instructions
├── PRD.md                       # This file
├── docker-compose.yml           # Local dev environment
├── pyproject.toml               # Python dependencies
├── alembic.ini                  # DB migration config
├── alembic/
│   └── versions/                # Migration files
├── app/
│   ├── main.py                  # FastAPI app entry
│   ├── config.py                # Settings (pydantic-settings)
│   ├── database.py              # DB connection
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── reminder.py
│   │   ├── journal.py
│   │   ├── energy_log.py
│   │   ├── goal.py
│   │   ├── key_result.py
│   │   ├── commitment.py
│   │   └── coaching_insight.py
│   ├── api/                     # API routes
│   │   ├── auth.py
│   │   ├── coaching.py
│   │   ├── reminders.py
│   │   ├── journal.py
│   │   ├── goals.py
│   │   ├── analytics.py
│   │   └── dashboard.py
│   ├── services/                # Business logic
│   │   ├── ai/
│   │   │   ├── claude_client.py
│   │   │   ├── coaching_engine.py
│   │   │   ├── context_builder.py
│   │   │   └── safety_detector.py
│   │   ├── coaching/
│   │   │   ├── grow_model.py
│   │   │   ├── powerful_questions.py
│   │   │   └── session_manager.py
│   │   ├── reminders/
│   │   │   ├── scheduler.py
│   │   │   └── check_in.py
│   │   ├── journal/
│   │   │   ├── prompts.py
│   │   │   └── pattern_analyzer.py
│   │   └── goals/
│   │       ├── okr_manager.py
│   │       └── alignment_checker.py
│   ├── prompts/                 # AI prompt templates
│   │   ├── base_coach.md
│   │   ├── grow_goal.md
│   │   ├── grow_reality.md
│   │   ├── grow_options.md
│   │   ├── grow_will.md
│   │   ├── challenge_mode.md
│   │   └── safety_rails.md
│   ├── middleware/
│   │   ├── auth.py
│   │   └── rate_limit.py
│   └── websocket/
│       └── coaching_ws.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── frontend/                    # React app
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Coaching.tsx
│   │   │   ├── Journal.tsx
│   │   │   └── Goals.tsx
│   │   ├── components/
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── EnergyHeatmap.tsx
│   │   │   ├── MoodChart.tsx
│   │   │   └── OKRCard.tsx
│   │   └── hooks/
│   │       ├── useWebSocket.ts
│   │       └── useAuth.ts
│   └── vite.config.ts
├── scripts/
│   ├── run-parallel.sh          # 🔥 Launch 6 Claude agents
│   ├── merge-agents.sh          # Merge all worktrees
│   └── qa-pipeline.sh           # Auto QA + ship
└── railway.json                 # Railway deploy config
```
