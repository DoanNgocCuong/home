# Từ 1 tuần → 1 giờ: Pipeline tự động hóa dự án Software với Claude

## Tại sao 1 tuần thành 1 giờ là khả thi?

Một dự án 1 tuần của AI Engineer thường gồm:
- **~2 ngày**: Planning, spec, architecture
- **~3 ngày**: Implementation (code + debug)
- **~1 ngày**: Testing + QA
- **~1 ngày**: Review + Ship

Bottleneck không phải năng lực AI — mà là **con người ngồi approve từng bước**. Nếu loại bỏ human-in-the-loop ở mỗi micro-step, thời gian giảm 80-95%.

---

## Architecture tổng thể: 3 Layers

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: SPEC (5 phút)                        │
│  Con người viết 1 spec ngắn gọn                │
│  → CLAUDE.md + PRD markdown                     │
└───────────────┬─────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────┐
│  LAYER 2: AUTONOMOUS EXECUTION (45 phút)        │
│  Claude Code chạy hoàn toàn tự động             │
│  10+ parallel agents, auto-accept everything    │
└───────────────┬─────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────┐
│  LAYER 3: VERIFY & SHIP (10 phút)              │
│  Con người review output cuối cùng              │
│  → Approve PR → Deploy                          │
└─────────────────────────────────────────────────┘
```

---

## Bước 1: Setup một lần (làm 1 lần, dùng mãi)

### 1.1 Cài Claude Code + Permission Modes

```bash
# Cài Claude Code
npm install -g @anthropic-ai/claude-code

# CÓ 3 CẤP ĐỘ auto-accept:

# Level 1: Auto-accept edits only (an toàn nhất)
# Bấm Shift+Tab trong Claude Code → auto-accept file edits
# Claude vẫn hỏi khi chạy shell commands

# Level 2: Allowlist commands cụ thể (khuyên dùng)
# File: ~/.claude/settings.json
```

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(git *)",
      "Bash(bun *)",
      "Bash(pnpm *)",
      "Bash(tsc *)",
      "Bash(eslint *)",
      "Bash(prettier *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(cat *)",
      "Bash(ls *)",
      "Edit(*)",
      "Write(*)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)",
      "Bash(curl * | bash)",
      "Bash(chmod 777 *)"
    ]
  }
}
```

```bash
# Level 3: Full YOLO mode (CHỈ dùng trong container/VM)
claude --dangerously-skip-permissions

# ⚠️ CẢNH BÁO: 32% developers gặp unintended file modification
# 9% bị data loss. KHÔNG BAO GIỜ chạy trên máy chính.
```

### 1.2 Setup CLAUDE.md — "Bộ não" cho project

```markdown
# CLAUDE.md — đặt ở root project

## Project Context
- Tech stack: Next.js 15, TypeScript, Tailwind, Prisma, PostgreSQL
- Monorepo structure: apps/web, packages/ui, packages/db
- Testing: Vitest + Playwright

## Auto-Execution Rules
- LUÔN chạy `pnpm typecheck` sau mỗi file change
- LUÔN chạy `pnpm test` trước khi commit
- KHÔNG BAO GIỜ sửa file .env hoặc migration files mà không hỏi
- Khi gặp lỗi test, tự fix tối đa 3 lần rồi báo

## Architecture Decisions
- API routes dùng tRPC, không dùng REST
- State management: Zustand, không Redux
- Auth: NextAuth v5 với Prisma adapter

## Code Style
- Prefer named exports
- Luôn dùng TypeScript strict mode
- Error handling: Result pattern, không throw
```

### 1.3 Setup Git Worktrees cho parallel agents

```bash
# Tạo bare repo cho worktree pattern
git clone --bare your-repo.git .bare
echo "gitdir: ./.bare" > .git

# Tạo worktrees cho parallel agents
git worktree add ./agent-1 -b feature/agent-1 main
git worktree add ./agent-2 -b feature/agent-2 main
git worktree add ./agent-3 -b feature/agent-3 main
# ... tạo bao nhiêu tùy ý
```

---

## Bước 2: Pipeline "1 giờ" — Chạy thực tế

### Phase 1: Spec (5 phút — CON NGƯỜI làm)

Viết PRD ngắn gọn. Đây là bước DUY NHẤT con người cần làm kỹ:

```markdown
# Feature: User Dashboard with Analytics

## Problem
Users can't see their usage data. Churn rate 15%.

## Success Criteria
- [ ] Dashboard page at /dashboard
- [ ] Charts: daily active usage, feature adoption, billing
- [ ] Real-time data via WebSocket
- [ ] Mobile responsive
- [ ] Load time < 2s

## Technical Constraints
- Use existing tRPC API layer
- Recharts for visualization
- Data from existing analytics table in PostgreSQL

## Out of Scope
- Admin dashboard (separate project)
- Export to PDF
```

### Phase 2: Plan Review — tự động (5 phút)

```bash
# Chạy Claude ở headless mode với plan prompt
claude -p "Read the PRD at docs/dashboard-prd.md. \
  Create a detailed implementation plan with: \
  1. File structure \
  2. Component breakdown \
  3. API endpoints needed \
  4. Database queries \
  5. Test plan \
  Save to docs/dashboard-plan.md" \
  --allowedTools "Read,Write,Edit,Bash(ls *),Bash(cat *)"
```

### Phase 3: Parallel Implementation — tự động (30 phút)

Đây là magic. Chạy nhiều Claude sessions song song:

```bash
#!/bin/bash
# file: run-parallel.sh

# Agent 1: Database + API layer
claude -p "Implement the database queries and tRPC routes \
  as specified in docs/dashboard-plan.md. \
  Run tests after each file. \
  Commit when all tests pass." \
  --allowedTools "Read,Write,Edit,Bash(pnpm *),Bash(git *)" &

# Agent 2: UI Components
claude -p "Implement all React components for the dashboard \
  as specified in docs/dashboard-plan.md. \
  Use Recharts. Make responsive. \
  Run typecheck after each component." \
  --allowedTools "Read,Write,Edit,Bash(pnpm *),Bash(git *)" &

# Agent 3: WebSocket real-time layer
claude -p "Implement WebSocket server and client hooks \
  for real-time dashboard updates. \
  Follow docs/dashboard-plan.md. \
  Write integration tests." \
  --allowedTools "Read,Write,Edit,Bash(pnpm *),Bash(git *)" &

# Agent 4: E2E Tests
claude -p "Write Playwright E2E tests for dashboard \
  based on success criteria in docs/dashboard-prd.md. \
  Cover: load time, responsive, data accuracy." \
  --allowedTools "Read,Write,Edit,Bash(pnpm *),Bash(npx *)" &

# Đợi tất cả xong
wait
echo "All agents completed!"
```

**Hoặc dùng Code Conductor (recommended):**

```bash
# Install Code Conductor
npx code-conductor init

# Nó tự tạo worktrees, phân task, chạy parallel
# Mỗi agent isolated, không conflict nhau
```

### Phase 4: Integration + QA — tự động (15 phút)

```bash
# Merge tất cả branches
git checkout main
git merge feature/agent-1 feature/agent-2 feature/agent-3

# Chạy Claude QA agent
claude -p "Run full QA on the dashboard feature: \
  1. pnpm typecheck \
  2. pnpm test \
  3. pnpm test:e2e \
  4. Check for console errors \
  5. Check bundle size \
  If any fail, fix and re-run. \
  Create a QA report at docs/qa-report.md" \
  --allowedTools "Read,Write,Edit,Bash(pnpm *),Bash(npx *)"
```

### Phase 5: Ship — tự động (5 phút)

```bash
# Review + Ship agent
claude -p "Review all changes on this branch: \
  1. Check for security issues (XSS, SQL injection) \
  2. Check for performance issues (N+1, memory leaks) \
  3. If no critical issues, create PR with description \
  4. Include test results in PR body" \
  --allowedTools "Read,Write,Edit,Bash(git *),Bash(gh *),Bash(pnpm *)"
```

---

## Bước 3: "Auto Mode" mới nhất (March 2026)

Anthropic vừa ra **Claude Code Auto Mode** (research preview, March 12, 2026):

```bash
# Auto Mode — Claude TỰ quyết định permission
# Không cần --dangerously-skip-permissions
# Claude AI đánh giá mỗi action có cần human approval không
# An toàn hơn YOLO mode rất nhiều

# Enable trong settings
claude settings set auto-mode true
```

**Khác biệt quan trọng:**

| Mode | Ai quyết định? | Risk level |
|------|----------------|------------|
| Manual (default) | Human approve tất cả | Thấp nhất |
| Shift+Tab | Human approve commands | Thấp |
| Allowlist | Human define rules | Trung bình |
| Auto Mode (NEW) | Claude AI quyết định | Trung bình-cao |
| --dangerously-skip-permissions | Không ai review | CAO |

---

## Bước 4: Pro Tips — Từ kinh nghiệm thực tế

### Tip 1: CLAUDE.md càng chi tiết, output càng tốt

Garry Tan ship 100 PRs/tuần vì CLAUDE.md của ông cực kỳ chi tiết — architecture decisions, code patterns, anti-patterns, testing strategy đều có.

### Tip 2: Spec trước, code sau — LUÔN LUÔN

```
❌ "Build me a dashboard" → Agent chạy lung tung, kết quả tệ
✅ PRD + Plan → Agent chạy theo đúng spec → kết quả 10x
```

### Tip 3: Parallel agents cần isolated workspaces

```
❌ 3 agents cùng sửa 1 file → merge conflict
✅ 3 agents trên 3 worktrees → clean merge
```

### Tip 4: Hooks tự động hóa quality gates

```json
// .claude/hooks.json
{
  "afterEdit": {
    "command": "pnpm typecheck",
    "description": "Auto typecheck sau mỗi edit"
  },
  "beforeCommit": {
    "command": "pnpm test && pnpm lint",
    "description": "Auto test + lint trước commit"
  }
}
```

### Tip 5: Dùng subagents cho tasks phức tạp

```markdown
// Trong CLAUDE.md
## Subagent Rules
- Khi implement feature > 3 files, spawn subagent cho mỗi file
- Khi gặp bug, spawn research subagent trước khi fix
- Khi viết tests, spawn separate testing subagent
```

---

## Tổng kết: Timeline so sánh

```
TRUYỀN THỐNG (1 tuần = 40 giờ):
Day 1-2: Planning/Spec ............... 16h
Day 3-5: Implementation .............. 24h (sequential, manual)
Day 6:   Testing ..................... 8h
Day 7:   Review + Ship .............. 8h
                                       ────
                                       ~56h

VỚI CLAUDE PIPELINE (1 giờ):
Phase 1: Human viết PRD .............. 5 min
Phase 2: Auto plan review ............ 5 min
Phase 3: Parallel implementation ..... 30 min (10 agents song song)
Phase 4: Auto QA ..................... 15 min
Phase 5: Auto review + ship .......... 5 min
                                       ────
                                       ~60 min
```

**Công thức:**
> Thời gian = (Complexity / Parallel_Agents) + Spec_Quality_Penalty
>
> Spec tốt + 10 agents = 1 giờ
> Spec tệ + 10 agents = vẫn 1 tuần (vì agents chạy sai hướng)

---

## Rủi ro cần biết

1. **Context window overflow**: Mỗi agent có giới hạn ~200K tokens. Projects lớn cần chia nhỏ.
2. **Merge conflicts**: Parallel agents có thể conflict. Dùng worktrees + clear boundaries.
3. **Hallucinated APIs**: Claude có thể gọi API không tồn tại. CLAUDE.md cần list rõ available APIs.
4. **Security**: 32% developers gặp unintended file changes với --dangerously-skip-permissions. Dùng container.
5. **Cost**: 10 parallel Opus agents ≈ $5-15/giờ. Vẫn rẻ hơn 1 tuần engineer time.

---

## Tools & Resources

- [gstack](https://github.com/garrytan/gstack) — Garry Tan's 8-skill setup
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) — Full framework với 34+ workflows
- [Code Conductor](https://github.com/ryanmac/code-conductor) — Parallel agent orchestrator
- [Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Docs: Permissions](https://code.claude.com/docs/en/permissions)
- [Parallel Worktrees Skill](https://github.com/spillwavesolutions/parallel-worktrees)
