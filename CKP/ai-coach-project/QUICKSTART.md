# 🚀 CoachGPT — Quick Start Guide
## Build toàn bộ project trong ~1 giờ với Claude parallel agents

---

## Prerequisites

```bash
# 1. Claude Code
npm install -g @anthropic-ai/claude-code

# 2. Python 3.12+
python --version  # >= 3.12

# 3. Node.js 20+
node --version  # >= 20

# 4. PostgreSQL 16 + Redis (hoặc dùng Docker)
docker --version

# 5. Git
git --version
```

---

## Step-by-Step (Tổng: ~60 phút)

### Step 0: Init project (2 phút)

```bash
# Clone hoặc tạo repo mới
mkdir coachgpt && cd coachgpt
git init

# Copy các file từ ai-coach-project/ vào đây:
# - CLAUDE.md
# - PRD.md
# - scripts/

# Start local DB
cat > docker-compose.yml << 'EOF'
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: coachgpt
      POSTGRES_USER: coach
      POSTGRES_PASSWORD: coach123
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
volumes:
  pgdata:
EOF

docker compose up -d

# Create .env
cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://coach:coach123@localhost:5432/coachgpt
REDIS_URL=redis://localhost:6379
ANTHROPIC_API_KEY=sk-ant-xxx  # ← Thay bằng key thật
JWT_SECRET=your-secret-key-change-this
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
EOF

git add -A && git commit -m "init: project setup"
```

### Step 1: Config Claude Code permissions (1 phút)

```bash
# Option A: Allowlist (recommended)
# Tạo file .claude/settings.json ở project root
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(python *)", "Bash(pip *)", "Bash(pytest *)",
      "Bash(ruff *)", "Bash(black *)", "Bash(alembic *)",
      "Bash(npm *)", "Bash(npx *)", "Bash(node *)",
      "Bash(git add *)", "Bash(git commit *)", "Bash(git checkout *)",
      "Bash(git merge *)", "Bash(git worktree *)", "Bash(git branch *)",
      "Bash(git status)", "Bash(git diff *)", "Bash(git log *)",
      "Bash(mkdir *)", "Bash(cp *)", "Bash(ls *)", "Bash(cat *)",
      "Bash(gh *)",
      "Edit(*)", "Write(*)", "Read(*)"
    ]
  }
}
EOF

# Option B: YOLO mode (chỉ trong Docker/VM!)
# claude --dangerously-skip-permissions
```

### Step 2: Run parallel agents (30-45 phút)

```bash
# 🚀 Launch 6 agents
./scripts/run-parallel.sh

# Monitor real-time (mở terminal khác)
tail -f .logs/agent*_*.log

# Hoặc xem từng agent:
tail -f .logs/agent1_*.log  # DB & Auth
tail -f .logs/agent2_*.log  # Coaching Engine
tail -f .logs/agent3_*.log  # Reminders
tail -f .logs/agent4_*.log  # Journal
tail -f .logs/agent5_*.log  # Goals & OKR
tail -f .logs/agent6_*.log  # Frontend
```

### Step 3: Merge (5 phút)

```bash
./scripts/merge-agents.sh
```

### Step 4: QA + Ship (10 phút)

```bash
./scripts/qa-pipeline.sh
```

### Step 5: Test locally (5 phút)

```bash
# Backend
pip install -e '.[dev]' --break-system-packages
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend (terminal khác)
cd frontend
npm install
npm run dev  # → http://localhost:5173

# Mở browser: http://localhost:5173
```

### Step 6: Deploy to Railway (5 phút)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway init
railway add --plugin postgresql
railway add --plugin redis
railway up

# Set env vars
railway variables set ANTHROPIC_API_KEY=sk-ant-xxx
railway variables set JWT_SECRET=your-production-secret

# Get URL
railway open
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent stuck > 15 min | Kill PID, check log, re-run single agent |
| Merge conflicts | `merge-agents.sh` auto-resolves via Claude |
| Tests failing after merge | `qa-pipeline.sh` auto-fixes up to 3 times |
| Claude API rate limit | Add 30s delay between agent launches |
| Context window overflow | Reduce prompt size, split into smaller tasks |

---

## Cost Estimate

| Item | Cost |
|------|------|
| Claude API (6 agents × ~50K tokens each) | ~$3-8 |
| Railway hosting (free tier) | $0-5/month |
| PostgreSQL (Railway free) | $0 |
| **Total to build + deploy** | **~$5-10** |

---

## Timeline Recap

```
00:00 - 00:02  Init project + Docker up
00:02 - 00:03  Configure Claude permissions
00:03 - 00:48  6 parallel agents building (~45 min)
00:48 - 00:53  Merge all branches
00:53 - 01:03  QA pipeline + Ship
01:03 - 01:08  Deploy to Railway
                ─────────────────
                ~1 hour total ✅
```
