# CLAUDE.md — CoachGPT: AI Executive Coach

## Project Overview
AI Personal Coach cho Founder/CEO. Sử dụng phương pháp coaching ICF-aligned (GROW model).
AI KHÔNG đưa lời khuyên — chỉ đặt câu hỏi mở và mirror.

## Tech Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, APScheduler
- Database: PostgreSQL 16, Redis
- AI: Anthropic Claude API (claude-sonnet-4-20250514)
- Frontend: React 18, TypeScript, Vite, Tailwind CSS
- Auth: JWT + Google OAuth2
- Real-time: WebSocket (FastAPI native)
- Testing: Pytest, httpx (async), Playwright (E2E)
- Deploy: Docker Compose (local), Railway (staging)

## Architecture Rules

### API Design
- LUÔN dùng Pydantic v2 models cho request/response
- LUÔN return consistent response format: `{"data": ..., "error": null}`
- LUÔN dùng async/await cho database operations
- Pagination: cursor-based, không dùng offset
- Rate limiting: 60 req/min cho general, 20 req/min cho AI endpoints

### Database
- Models dùng SQLAlchemy 2.0 mapped_column syntax
- LUÔN có created_at, updated_at trên mọi table
- Soft delete (deleted_at) cho user-generated content
- UUID cho primary keys, không dùng auto-increment integer
- Foreign keys LUÔN có index

### AI/Coaching Engine
- System prompt = base_coach.md + GROW stage prompt + user context
- User context = recent goals + today's energy + last 5 journal entries
- Conversation memory = last 10 messages + session summary
- KHÔNG BAO GIỜ đưa lời khuyên trực tiếp trong coaching mode
- Detect crisis keywords → redirect to professional help + hotline
- Max 4000 tokens per response
- Temperature: 0.7 cho coaching, 0.3 cho analysis

### Frontend
- Component naming: PascalCase
- Hooks prefix: use* (useAuth, useWebSocket, useCoaching)
- State management: Zustand (không Redux)
- API calls: tanstack-query (react-query)
- Charts: Recharts
- Tailwind only — không custom CSS files

### Code Style
- Python: Black formatter, Ruff linter, isort
- TypeScript: ESLint + Prettier
- Prefer named exports
- Type hints bắt buộc cho Python
- Docstrings cho mọi public function

### Testing
- Unit tests: mọi service function
- Integration tests: mọi API endpoint
- E2E: critical flows (login → coaching → journal → goals)
- Minimum 80% coverage
- Mock Claude API trong tests (không gọi API thật)

## Auto-Execution Rules (for autonomous mode)
- Sau mỗi file Python: chạy `ruff check` + `black --check`
- Sau mỗi model change: chạy `alembic revision --autogenerate`
- Sau mỗi API endpoint: viết test tương ứng
- Trước commit: chạy `pytest` — phải pass hết
- Khi gặp lỗi test: tự fix tối đa 3 lần, nếu không được thì log vào TODO.md

## Critical Don'ts
- KHÔNG sửa .env files
- KHÔNG commit API keys
- KHÔNG dùng SQLAlchemy legacy Query API (dùng select() statements)
- KHÔNG dùng print() — dùng structlog
- KHÔNG hardcode URLs — dùng config.py
