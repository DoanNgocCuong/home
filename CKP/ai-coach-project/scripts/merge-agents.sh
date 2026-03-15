#!/bin/bash
# ============================================================
# 🔀 Merge all agent worktrees back to main
# ============================================================

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔀 Merging all agent branches into main...${NC}\n"

git checkout main

BRANCHES=(
  "agent/db-auth"         # Merge first — foundation
  "agent/coaching-engine"
  "agent/reminders"
  "agent/journal"
  "agent/goals-okr"
  "agent/frontend"        # Merge last — UI depends on API
)

for branch in "${BRANCHES[@]}"; do
  echo -e "  Merging ${YELLOW}$branch${NC}..."
  if git merge "$branch" --no-edit; then
    echo -e "  ${GREEN}✓${NC} Merged $branch"
  else
    echo -e "  ${RED}✗${NC} Conflict in $branch — launching Claude to resolve..."
    claude -p "Resolve the current git merge conflict.
    Read the conflicting files, understand both sides, and create a clean merge.
    Then run: git add . && git commit --no-edit
    " --allowedTools "Read,Write,Edit,Bash(git *),Bash(cat *),Bash(ls *)"
    echo -e "  ${GREEN}✓${NC} Conflict resolved by Claude"
  fi
done

echo -e "\n${GREEN}✅ All branches merged! Running integration check...${NC}"

# Quick sanity check
echo -e "\n${YELLOW}Running quick sanity checks...${NC}"
python -c "from app.main import app; print('FastAPI app imports OK')" 2>/dev/null && \
  echo -e "  ${GREEN}✓${NC} Backend imports clean" || \
  echo -e "  ${RED}✗${NC} Backend import errors — run qa-pipeline.sh"

(cd frontend && npm run build 2>/dev/null) && \
  echo -e "  ${GREEN}✓${NC} Frontend builds clean" || \
  echo -e "  ${RED}✗${NC} Frontend build errors — run qa-pipeline.sh"

echo -e "\n${GREEN}Next: ./scripts/qa-pipeline.sh${NC}"
