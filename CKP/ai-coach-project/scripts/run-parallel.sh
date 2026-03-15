#!/bin/bash
# ============================================================
# 🚀 CoachGPT — Parallel Agent Pipeline
# Chạy 6 Claude Code agents song song trên git worktrees
#
# Usage: ./scripts/run-parallel.sh
# Prerequisites: Claude Code installed, git repo initialized
# ============================================================

set -euo pipefail

PROJECT_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_DIR="$PROJECT_ROOT/.worktrees"
LOG_DIR="$PROJECT_ROOT/.logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 CoachGPT Parallel Agent Pipeline     ║${NC}"
echo -e "${BLUE}║  6 agents × isolated worktrees           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"

# ============================================================
# Step 1: Setup worktrees
# ============================================================
echo -e "\n${YELLOW}[1/4] Setting up git worktrees...${NC}"

mkdir -p "$WORKTREE_DIR" "$LOG_DIR"

BRANCHES=(
  "agent/db-auth"
  "agent/coaching-engine"
  "agent/reminders"
  "agent/journal"
  "agent/goals-okr"
  "agent/frontend"
)

for branch in "${BRANCHES[@]}"; do
  dir_name=$(echo "$branch" | sed 's|agent/||')
  worktree_path="$WORKTREE_DIR/$dir_name"

  if [ -d "$worktree_path" ]; then
    echo -e "  ${GREEN}✓${NC} Worktree exists: $dir_name"
  else
    git worktree add "$worktree_path" -b "$branch" main 2>/dev/null || \
    git worktree add "$worktree_path" "$branch" 2>/dev/null
    echo -e "  ${GREEN}✓${NC} Created worktree: $dir_name"
  fi
done

# ============================================================
# Step 2: Launch 6 parallel agents
# ============================================================
echo -e "\n${YELLOW}[2/4] Launching 6 Claude agents in parallel...${NC}"
echo -e "  Logs: $LOG_DIR/"

PIDS=()

# --- Agent 1: Database & Auth ---
echo -e "  ${BLUE}▶${NC} Agent 1: Database & Auth"
(cd "$WORKTREE_DIR/db-auth" && claude -p "
You are building the database and auth layer for CoachGPT (AI Executive Coach).

Read CLAUDE.md for project rules.
Read PRD.md section 4.2 for database schema.

Tasks (in order):
1. Create pyproject.toml with all dependencies
2. Create app/config.py (pydantic-settings)
3. Create app/database.py (async SQLAlchemy engine)
4. Create ALL 10 SQLAlchemy models in app/models/
5. Create alembic.ini + initial migration
6. Create app/api/auth.py (register, login, Google OAuth, JWT)
7. Create app/middleware/auth.py (JWT verification)
8. Write unit tests for all models + auth endpoints
9. Run ruff check + pytest — fix any failures
10. Git commit with descriptive message

IMPORTANT: Follow CLAUDE.md rules strictly. Use SQLAlchemy 2.0 syntax.
" --allowedTools "Read,Write,Edit,Bash(python *),Bash(pip *),Bash(alembic *),Bash(ruff *),Bash(black *),Bash(pytest *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent1_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 2: AI Coaching Engine ---
echo -e "  ${BLUE}▶${NC} Agent 2: AI Coaching Engine"
(cd "$WORKTREE_DIR/coaching-engine" && claude -p "
You are building the AI Coaching Engine for CoachGPT.

Read CLAUDE.md for project rules.
Read PRD.md sections 3.1 and 4.4 for coaching features.

Tasks (in order):
1. Create app/services/ai/claude_client.py — Anthropic SDK wrapper
2. Create app/services/ai/context_builder.py — builds user context for prompts
3. Create app/services/ai/safety_detector.py — detect crisis keywords
4. Create app/services/coaching/grow_model.py — GROW model state machine
5. Create app/services/coaching/powerful_questions.py — 200+ questions bank
6. Create app/services/coaching/session_manager.py — conversation management
7. Create app/services/ai/coaching_engine.py — orchestrates everything
8. Create ALL prompt templates in app/prompts/ (base_coach.md, grow_*.md, etc.)
9. Create app/api/coaching.py — API endpoints
10. Create app/websocket/coaching_ws.py — WebSocket handler
11. Write unit tests (mock Claude API)
12. Run ruff check + pytest — fix failures
13. Git commit

IMPORTANT: AI must NEVER give direct advice. Only ask powerful questions.
Use GROW model: Goal → Reality → Options → Will.
" --allowedTools "Read,Write,Edit,Bash(python *),Bash(pip *),Bash(ruff *),Bash(black *),Bash(pytest *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent2_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 3: Reminders & Check-ins ---
echo -e "  ${BLUE}▶${NC} Agent 3: Reminders & Check-ins"
(cd "$WORKTREE_DIR/reminders" && claude -p "
You are building the Reminders & Check-in system for CoachGPT.

Read CLAUDE.md for project rules.
Read PRD.md section 3.2 for reminder features.

Tasks (in order):
1. Create app/services/reminders/scheduler.py — APScheduler integration
2. Create app/services/reminders/check_in.py — check-in logic
3. Create app/api/reminders.py — CRUD + check-in submission
4. Create reminder job functions:
   - Morning check-in (configurable time per user timezone)
   - Energy tracking (3x/day)
   - Commitment reminders
   - Weekly review trigger
   - Monthly reflection trigger
5. Create WebSocket notification for reminders
6. Write tests for scheduler + API
7. Run ruff + pytest
8. Git commit

IMPORTANT: All scheduling must be timezone-aware. Use APScheduler AsyncIOScheduler.
" --allowedTools "Read,Write,Edit,Bash(python *),Bash(pip *),Bash(ruff *),Bash(black *),Bash(pytest *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent3_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 4: Journal & Reflection ---
echo -e "  ${BLUE}▶${NC} Agent 4: Journal & Reflection"
(cd "$WORKTREE_DIR/journal" && claude -p "
You are building the Journal & Reflection system for CoachGPT.

Read CLAUDE.md for project rules.
Read PRD.md section 3.3 for journal features.

Tasks (in order):
1. Create app/services/journal/prompts.py — daily prompt generator (30+ unique prompts)
2. Create app/services/journal/pattern_analyzer.py — AI analysis of journal entries
3. Create app/api/journal.py — CRUD + prompt + pattern endpoints
4. Implement:
   - Daily journal with rich text
   - Decision journal (decision + reasoning + outcome tracking)
   - Gratitude log (3 items/day)
   - Pattern recognition across entries (themes, emotions, recurring topics)
5. Write tests
6. Run ruff + pytest
7. Git commit

IMPORTANT: Pattern analysis uses Claude API with temperature 0.3.
Journal entries support markdown formatting.
" --allowedTools "Read,Write,Edit,Bash(python *),Bash(pip *),Bash(ruff *),Bash(black *),Bash(pytest *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent4_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 5: Goals & OKR ---
echo -e "  ${BLUE}▶${NC} Agent 5: Goals & OKR + Analytics"
(cd "$WORKTREE_DIR/goals-okr" && claude -p "
You are building the Goals/OKR system and Analytics for CoachGPT.

Read CLAUDE.md for project rules.
Read PRD.md sections 3.4 and 3.5 for features.

Tasks (in order):
1. Create app/services/goals/okr_manager.py — OKR CRUD + progress tracking
2. Create app/services/goals/alignment_checker.py — AI alignment analysis
3. Create app/api/goals.py — CRUD + check-in + alignment endpoints
4. Create app/api/analytics.py — energy heatmap, mood trends, insights, accountability
5. Create app/api/dashboard.py — aggregated dashboard endpoint
6. Implement:
   - OKR hierarchy (Objective → Key Results)
   - Weekly check-in flow with coaching prompts
   - Accountability score calculation
   - Energy heatmap data (day × hour matrix)
   - Mood trend analysis
7. Write tests
8. Run ruff + pytest
9. Git commit

IMPORTANT: Analytics endpoints must be fast (<200ms). Pre-compute where possible.
Accountability score = completed_commitments / total_commitments × 100.
" --allowedTools "Read,Write,Edit,Bash(python *),Bash(pip *),Bash(ruff *),Bash(black *),Bash(pytest *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent5_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 6: Frontend ---
echo -e "  ${BLUE}▶${NC} Agent 6: Frontend (React)"
(cd "$WORKTREE_DIR/frontend" && claude -p "
You are building the React frontend for CoachGPT (AI Executive Coach).

Read CLAUDE.md for project rules.
Read PRD.md for all features.

Tasks (in order):
1. Scaffold React app: npx create-vite frontend --template react-ts
2. Install: tailwindcss, zustand, @tanstack/react-query, recharts, lucide-react, react-router-dom
3. Create routing setup (React Router v6)
4. Create pages:
   - Login.tsx (Google OAuth button + email/password)
   - Dashboard.tsx (energy heatmap, mood chart, OKR progress, accountability score)
   - Coaching.tsx (chat UI with WebSocket, message bubbles, typing indicator)
   - Journal.tsx (entry list, create form, daily prompt, pattern insights)
   - Goals.tsx (OKR cards, progress bars, check-in modal)
5. Create components:
   - ChatBubble.tsx (user vs AI styling)
   - EnergyHeatmap.tsx (Recharts)
   - MoodChart.tsx (line chart)
   - OKRCard.tsx (progress ring)
   - CheckInModal.tsx
6. Create hooks:
   - useAuth.ts (JWT + Google OAuth)
   - useWebSocket.ts (coaching real-time)
   - useApi.ts (tanstack-query wrapper)
7. Responsive design (mobile-first)
8. Run npm run build — fix errors
9. Git commit

IMPORTANT: Tailwind only, no custom CSS. Mobile-first responsive.
Use Zustand for state. Use tanstack-query for API calls.
" --allowedTools "Read,Write,Edit,Bash(npm *),Bash(npx *),Bash(node *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *)" \
  > "$LOG_DIR/agent6_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# ============================================================
# Step 3: Wait for all agents
# ============================================================
echo -e "\n${YELLOW}[3/4] All 6 agents running in parallel. Waiting...${NC}"
echo -e "  Monitor logs: tail -f $LOG_DIR/agent*_${TIMESTAMP}.log"
echo ""

FAILED=0
for i in "${!PIDS[@]}"; do
  pid=${PIDS[$i]}
  agent_num=$((i + 1))
  if wait "$pid"; then
    echo -e "  ${GREEN}✓${NC} Agent $agent_num completed successfully"
  else
    echo -e "  ${RED}✗${NC} Agent $agent_num failed (check log)"
    FAILED=$((FAILED + 1))
  fi
done

# ============================================================
# Step 4: Summary
# ============================================================
echo -e "\n${YELLOW}[4/4] Summary${NC}"
if [ $FAILED -eq 0 ]; then
  echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║  ✅ All 6 agents completed successfully! ║${NC}"
  echo -e "${GREEN}║  Next: ./scripts/merge-agents.sh         ║${NC}"
  echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
else
  echo -e "${RED}╔══════════════════════════════════════════╗${NC}"
  echo -e "${RED}║  ⚠️  $FAILED agent(s) failed              ║${NC}"
  echo -e "${RED}║  Check logs in: $LOG_DIR/                ║${NC}"
  echo -e "${RED}╚══════════════════════════════════════════╝${NC}"
fi
