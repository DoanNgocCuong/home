# CLAUDE CODE - COMPLETE SETUP CHO AI ENGINEER

> Tổng hợp từ: shanraisshan/claude-code-best-practice + Checklist sai lầm + Skills Repos
> Phiên bản: 2026

---

## 1. FOLDER STRUCTURE CHUẨN

```
.claude/
├── CLAUDE.md              # Project memory (< 150 dòng)
├── settings.json          # Team shared (commit vào git)
├── settings.local.json    # Personal (gitignore)
├── commands/              # Custom slash commands
│   ├── commit.md
│   ├── review.md
│   ├── implement.md
│   └── research.md
├── agents/                # Sub-agents
│   ├── coder.md
│   ├── researcher.md
│   ├── reviewer.md
│   └── debugger.md
├── skills/                # Domain knowledge
│   ├── 01-python/
│   ├── 02-fastapi/
│   └── 03-react/
├── hooks/                 # Auto-scripts
│   └── post-tool-use.js
└── rules/                 # Path-specific rules
    ├── api-endpoints.md
    └── database.md
```

---

## 2. CLAUDE.md - TEMPLATE TỐI ƯU

```markdown
# [Project Name]

## Tech Stack
- Backend: Python 3.11, FastAPI
- Frontend: React 18, TypeScript
- Database: PostgreSQL, Redis
- Infra: Docker, K8s, AWS

## Key Commands
- Dev: `make dev`
- Test: `pytest -x`
- Build: `make build`

## Structure
- `src/api/` - REST endpoints
- `src/core/` - Business logic
- `src/services/` - Microservices

## Conventions
- Async/await for I/O
- Type hints everywhere
- REST: kebab-case endpoints

## Common Mistakes
- [Thêm khi Claude sai]
```

### Nguyên tắc VÀNG:
- **< 150 dòng** (HumanLayer khuyến nghị 60 dòng)
- **KHÔNG** dùng `@file` imports
- **Cập nhật** "Common Mistakes" ngay khi Claude lặp lỗi

---

## 3. SETTINGS.JSON - PERMISSIONS

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm *)",
      "Bash(python -m pytest *)",
      "Bash(python *)",
      "Bash(docker *)",
      "Bash(git add:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(make *)",
      "Glob(*)",
      "Grep(*)",
      "Read(*)",
      "Edit(*)",
      "Write(*)"
    ],
    "deny": [
      "Bash(rm -rf /node_modules)",
      "Bash(sudo *)",
      "Bash(git push --force*)",
      "Edit(.env*)",
      "Edit(**/secrets/**)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || ruff format \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

---

## 4. COMMANDS TEMPLATES

### /commit.md
```markdown
---
description: Smart conventional commit
allowed-tools: Bash(git add:*), Bash(git commit:*)
model: haiku
---
!`git diff --cached --stat`
!`git diff --cached`

Create conventional commit. Format: type(scope): description
Types: feat, fix, refactor, docs, test, chore, perf
If $ARGUMENTS, use as message directly.
```

### /review.md
```markdown
---
description: Review code changes
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
model: sonnet
---
## Context
- Changes: !`git diff HEAD~1`
- Files: !`git diff --name-only HEAD~1`

Review for:
1. Security vulnerabilities
2. Logic errors
3. Performance issues
4. Convention violations
Output: Priority (Critical → Warning → Suggestion)
```

### /implement.md
```markdown
---
description: Implement feature from spec
argument-hint: [feature-name]
---
## Task
Implement: $ARGUMENTS

## Workflow
1. PLAN first - identify files
2. Write tests FIRST
3. Implement
4. Run tests
5. Verify against spec
```

---

## 5. AGENTS TEMPLATES

### coder.md
```yaml
---
name: coder
description: Expert Python/TypeScript developer
model: sonnet
tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
  - Task
maxTurns: 50
skills:
  - python-best-practices
---

# Coder Agent

## Expertise
- Python, TypeScript, FastAPI, React
- PostgreSQL, Redis, Docker

## Guidelines
- Async by default
- Type hints everywhere
- Follow existing patterns
- Write tests with code
```

### researcher.md
```yaml
---
name: researcher
description: Expert researcher for AI topics
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
maxTurns: 30
---

# Researcher Agent

## Guidelines
- Cite authoritative sources
- Provide examples
- Focus actionable insights
- Update to 2025-2026
```

### debugger.md
```yaml
---
name: systematic-debugger
description: Root cause analysis for bugs
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Debugger Agent

## Protocol
1. Reproduce symptom
2. Find immediate cause
3. Trace upward - full call chain
4. Keep tracing to ORIGINAL trigger
5. Fix ROOT, not symptom

CRITICAL: If 3 fix attempts fail → flag as architectural
```

---

## 6. SKILLS REPOSITORIES

### Install Commands:

```bash
# Antigravity Awesome Skills (1200+ skills)
npx antigravity-awesome-skills --claude

# AI Research Skills (85 skills)
npx @orchestra-research/ai-research-skills
```

### Top Skills từ Antigravity:

| Skill | Use Case |
|-------|----------|
| `@brainstorming` | Plan trước khi implement |
| `@architecture` | System design |
| `@test-driven-development` | TDD workflow |
| `@doc-coauthoring` | Viết docs |
| `@lint-and-validate` | Quality checks |
| `@create-pr` | Tạo PR |
| `@debugging-strategies` | Debug systematically |
| `@api-design-principles` | API design |
| `@security-auditor` | Security review |

### AI Research Skills by Category:

| Category | Skills |
|----------|--------|
| Fine-Tuning | Axolotl, LLaMA-Factory, Unsloth, PEFT |
| Post-Training | TRL, GRPO, DPO, SimPO |
| Inference | vLLM, llama.cpp, SGLang, TensorRT-LLM |
| Optimization | Flash Attention, bitsandbytes, AWQ, GGUF |
| Agents | LangChain, LlamaIndex, CrewAI |
| RAG | Chroma, FAISS, Pinecone, Qdrant |
| Observability | LangSmith, Phoenix |

---

## 7. HOOKS EXAMPLES

### Auto-format sau khi edit:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Stop hook - chạy tests trước khi kết thúc:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ \"$STOP_HOOK_ACTIVE\" != \"1\" ]; then export STOP_HOOK_ACTIVE=1 && npm test 2>&1 | tail -5; fi"
          }
        ]
      }
    ]
  }
}
```

---

## 8. MONOREPO STRUCTURE

```
/monorepo/
├── CLAUDE.md                    # Shared conventions
├── services/
│   ├── orchestration/
│   │   └── CLAUDE.md           # Queue patterns
│   ├── conversation-ai/
│   │   └── CLAUDE.md           # AI pipeline
│   └── context-handling/
│       └── CLAUDE.md           # Memory patterns
├── frontend/
│   └── CLAUDE.md               # React conventions
└── infra/
    └── CLAUDE.md               # K8s, Docker
```

**Nguyên tắc:**
- Root: shared conventions
- Sub: service-specific rules
- Mỗi file < 150 dòng

---

## 9. BORIS CHERRY'S 42 TIPS

### Productivity:
1. **Git Worktrees**: 3-5 worktrees song song
2. **Plan Mode**: `Shift+Tab` x2 trước khi code
3. **Opus**: Cho complex tasks
4. **Slash commands**: Cho inner-loop
5. **5-10 sessions**: Teleport giữa sessions
6. **`ultrathink`**: Trigger deep reasoning
7. **`/compact`**: Ở 50% context
8. **Small tasks**: Vanilla > complex workflows

### Customization:
9. **Plugins**: Via `/plugin`
10. **Permissions**: Wildcard syntax
11. **Sandbox**: Giảm permission prompts
12. **Status Line**: Custom context/cost
13. **Output Styles**: Explanatory mode

---

## 10. QUICK START

```bash
# 1. Cài đặt
curl -fsSL https://claude.ai/install.sh | bash

# 2. Verify
claude --version
claude doctor

# 3. Tạo cấu trúc
mkdir -p .claude/{commands,agents,skills,hooks,settings}

# 4. Init CLAUDE.md
claude /init

# 5. Config permissions
/permissions

# 6. Install LSPs
/plugin install pyright@claude-code-lsps
/plugin install typescript-lsp@claude-code-lsps
```

---

## 11. SAI LẦM PHỔ BIẾN CẦN TRÁNH

### CLAUDE.md:
| Sai lầm | Cách sửa |
|---------|----------|
| Quá dài (>500 dòng) | < 200 dòng, tách sub-CLAUDE.md |
| Dùng @file imports | List path dạng text |
| Không cập nhật khi sai | Thêm vào "Common Mistakes" |
| Sensitive data | Dùng env vars |

### Context:
| Sai lầm | Cách sửa |
|---------|----------|
| Không /clear | /clear giữa tasks |
| Đợi auto-compact | /compact thủ công ở 50% |
| Paste full log | Grep relevant lines |
| Session > 2h | Chia 30 phút/sprint |

### Workflow:
| Sai lầm | Cách sửa |
|---------|----------|
| Không Plan | Shift+Tab x2 → Plan Mode |
| Accept first solution | "scrap this, elegant solution" |
| Không commit | Commit mỗi unit of work |
| Micromanage | "Fix failing CI tests" |

---

## 12. MODEL SELECTION

| Task | Model | Thinking |
|------|-------|----------|
| Commit, format | Haiku | — |
| Daily coding, bug fix | Sonnet | think |
| Design decisions | Sonnet | think hard |
| Architecture, debugging | Opus | ultrathink |
| Code review | Sonnet | think |
| Read-only research | Haiku | — |

---

## 13. KEYBOARD SHORTCUTS

| Shortcut | Action |
|----------|--------|
| Shift+Tab | Cycle: Normal → Auto-Accept → Plan |
| Ctrl+G | Open plan in editor |
| Ctrl+O | Toggle verbose (xem thinking) |
| Ctrl+B | Launch background agent |
| Esc Esc | Undo last action |
| # | Quick-add to CLAUDE.md |

---

## 14. COMMANDS REFERENCE

| Command | Use Case |
|---------|----------|
| /init | Init CLAUDE.md |
| /memory | Xem/edit memory |
| /context | Check token usage |
| /compact [focus] | Compact context |
| /clear | Reset context |
| /plan | Read-only analysis |
| /model | Đổi model/effort |
| /permissions | Config wildcards |
| /doctor | Debug issues |
| /plugin | Install LSPs |
| /sandbox | Enable isolation |

---

## 15. RESOURCES

- [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) - 8.7k stars
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) - 1200+ skills
- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - 85 AI skills
- [Boris Cherny Twitter](https://twitter.com/bcherry)
- [HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

---

*Setup hoàn chỉnh cho AI Engineer. Copy-paste và customize theo project.*
