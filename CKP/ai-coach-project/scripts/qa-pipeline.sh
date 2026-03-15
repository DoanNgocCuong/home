#!/bin/bash
# ============================================================
# 🧪 QA Pipeline — Auto test + review + ship
# Chạy 2 Claude agents song song: QA + Review
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LOG_DIR=".logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🧪 CoachGPT QA Pipeline                 ║${NC}"
echo -e "${BLUE}║  Agent 7: QA + Agent 8: Security Review  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"

PIDS=()

# --- Agent 7: QA Engineer ---
echo -e "\n${BLUE}▶${NC} Agent 7: QA Engineer"
(claude -p "
You are the QA Engineer for CoachGPT. Run comprehensive testing:

1. Install all dependencies:
   - pip install -e '.[dev]' --break-system-packages
   - cd frontend && npm install

2. Run backend tests:
   - pytest tests/ -v --tb=short --cov=app --cov-report=term
   - If any fail, FIX them and re-run (max 3 attempts)

3. Run linting:
   - ruff check app/
   - black --check app/

4. Run frontend build:
   - cd frontend && npm run build
   - cd frontend && npm run lint

5. Check for common issues:
   - Unused imports
   - Missing type hints
   - Hardcoded secrets or URLs
   - Missing error handling

6. Write QA report to docs/qa-report.md:
   - Test results summary
   - Coverage percentage
   - Issues found and fixed
   - Remaining warnings

7. Git commit the fixes + report
" --allowedTools "Read,Write,Edit,Bash(pip *),Bash(python *),Bash(pytest *),Bash(ruff *),Bash(black *),Bash(npm *),Bash(npx *),Bash(git *),Bash(mkdir *),Bash(ls *),Bash(cat *),Bash(cd *)" \
  > "$LOG_DIR/agent7_qa_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# --- Agent 8: Security Reviewer ---
echo -e "${BLUE}▶${NC} Agent 8: Security & Code Review"
(claude -p "
You are a paranoid Staff Engineer reviewing CoachGPT for production readiness.

Review ALL files in app/ and frontend/src/ for:

1. SECURITY:
   - SQL injection (check all queries use parameterized statements)
   - XSS vulnerabilities (check frontend renders)
   - JWT token handling (expiry, refresh, storage)
   - API key exposure (no hardcoded keys)
   - CORS configuration
   - Rate limiting on AI endpoints
   - Input validation on all endpoints

2. PERFORMANCE:
   - N+1 query patterns
   - Missing database indexes
   - Unbounded queries (missing LIMIT)
   - Memory leaks in WebSocket handlers
   - Frontend bundle size concerns

3. RELIABILITY:
   - Error handling completeness
   - Graceful degradation when Claude API is down
   - Database connection pool settings
   - Timeout configurations

4. Write security review to docs/security-review.md:
   - Critical issues (must fix before deploy)
   - Warnings (should fix)
   - Recommendations (nice to have)

5. If CRITICAL issues found, FIX THEM directly.

6. Git commit
" --allowedTools "Read,Write,Edit,Bash(git *),Bash(grep *),Bash(ls *),Bash(cat *),Bash(ruff *)" \
  > "$LOG_DIR/agent8_review_${TIMESTAMP}.log" 2>&1) &
PIDS+=($!)

# Wait for both
echo -e "\n${YELLOW}Both agents running. Waiting...${NC}"
FAILED=0
for i in "${!PIDS[@]}"; do
  pid=${PIDS[$i]}
  agent_num=$((i + 7))
  if wait "$pid"; then
    echo -e "  ${GREEN}✓${NC} Agent $agent_num completed"
  else
    echo -e "  ${RED}✗${NC} Agent $agent_num failed"
    FAILED=$((FAILED + 1))
  fi
done

# Final step: Ship
if [ $FAILED -eq 0 ]; then
  echo -e "\n${GREEN}✅ QA + Review passed! Creating PR...${NC}"
  claude -p "
  Create a GitHub PR for branch main → production:
  - Title: 'feat: CoachGPT AI Executive Coach — initial release'
  - Body: Include QA report summary from docs/qa-report.md
  - Include security review summary from docs/security-review.md
  - Add test coverage stats
  Use: gh pr create --title '...' --body '...'
  " --allowedTools "Bash(gh *),Bash(git *),Read"
else
  echo -e "\n${RED}⚠️  QA/Review had failures. Check logs before shipping.${NC}"
fi
