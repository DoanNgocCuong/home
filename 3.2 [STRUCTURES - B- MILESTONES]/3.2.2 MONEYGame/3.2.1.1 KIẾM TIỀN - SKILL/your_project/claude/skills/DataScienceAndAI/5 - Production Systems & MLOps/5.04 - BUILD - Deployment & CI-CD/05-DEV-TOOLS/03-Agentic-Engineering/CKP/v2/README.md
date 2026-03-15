# 🏗️ Best Practice `.claude/` Folder — Quick Start Guide

> Based on: Boris Cherny (creator Claude Code), HumanLayer, Trail of Bits,
> ChrisWiles, Anthropic internal teams, shanraisshan (8.7k⭐)

## Structure

```
your-project/
├── CLAUDE.md                          ← Project memory (loaded EVERY session)
│
├── .claude/
│   ├── settings.json                  ← Permissions + hooks (commit to git)
│   ├── settings.local.json            ← Personal overrides (gitignored)
│   │
│   ├── commands/                      ← Slash commands (user-triggered)
│   │   ├── commit.md                  ← /commit — smart conventional commit
│   │   ├── review.md                  ← /review — code review last changes
│   │   ├── fix.md                     ← /fix [description] — bug fix workflow
│   │   └── plan.md                    ← /plan [feature] — design before coding
│   │
│   ├── agents/                        ← Sub-agents (auto or manual trigger)
│   │   ├── code-reviewer.md           ← Proactive review after code changes
│   │   └── systematic-debugger.md     ← Root cause analysis for hard bugs
│   │
│   ├── skills/                        ← Knowledge (progressive disclosure)
│   │   ├── project-architecture/
│   │   │   └── SKILL.md               ← System design, service map, ADRs
│   │   └── systematic-debugging/
│   │       └── SKILL.md               ← Debug commands, error patterns
│   │
│   └── rules/                         ← Path-scoped rules (auto-loaded)
│       ├── api.md                     ← Loads when editing API files
│       ├── database.md                ← Loads when editing DB/migration files
│       └── tests.md                   ← Loads when editing test files
│
└── .gitignore                         ← Add: .claude/settings.local.json
```

## How It Works

| Component | When Active | Token Cost | Purpose |
|-----------|-------------|------------|---------|
| **CLAUDE.md** | Every session, every turn | ~500-800 tokens | Universal project context |
| **settings.json** | Background (permissions/hooks) | 0 (not in context) | Automation & safety |
| **commands/** | When user types `/command` | On-demand | Repeatable workflows |
| **agents/** | Auto-trigger or Task() call | Separate context window | Specialized expertise |
| **skills/** | Metadata always, full on-demand | ~100 tokens/skill startup | Deep knowledge |
| **rules/** | When file path matches | On-demand | Path-specific conventions |

## Setup Steps

### 1. Copy this folder into your project
```bash
cp -r best-practice-claude/.claude your-project/
cp best-practice-claude/CLAUDE.md your-project/
```

### 2. Customize CLAUDE.md
Replace ALL placeholders `[...]` with your actual:
- Tech stack and commands
- Directory structure
- Coding conventions
- Build/test commands

### 3. Customize skills
Edit `.claude/skills/project-architecture/SKILL.md` with your actual architecture.
Edit `.claude/skills/systematic-debugging/SKILL.md` with your actual debug commands.

### 4. Customize rules (optional)
Edit path patterns in `.claude/rules/*.md` to match your directory structure.

### 5. Update .gitignore
```bash
echo ".claude/settings.local.json" >> .gitignore
echo ".claude/agent-memory-local/" >> .gitignore
echo ".claude/worktrees/" >> .gitignore
```

### 6. Commit to git
```bash
git add CLAUDE.md .claude/
git commit -m "chore: add Claude Code configuration"
```

## Daily Usage

```
Shift+Tab ×2  → Plan Mode (think before code)
Shift+Tab     → Auto-Accept (let Claude work)
/commit       → Smart conventional commit
/review       → Review recent changes
/fix [desc]   → Fix with Explore→Plan→Test→Implement
/plan [feat]  → Design before building
/clear        → Reset context between tasks
/compact      → Compress context at 50% usage
/context      → Check token usage
#             → Quick-add note to CLAUDE.md
```

## Key Principles

1. **CLAUDE.md < 80 lines** — every extra line hurts ALL instructions
2. **Rules for path-specific** — only load when relevant → saves context
3. **Skills for deep knowledge** — progressive disclosure, not upfront cost
4. **Agents for isolation** — separate context window, no pollution
5. **Commands for workflows** — deterministic entry points
6. **Hooks for formatting** — 100% reliable, zero Claude instruction cost
7. **`/clear` between tasks** — fresh context = smarter Claude
8. **Commit CLAUDE.md to git** — whole team benefits

## Sources
- Boris Cherny: https://howborisusesclaudecode.com/
- HumanLayer: https://www.humanlayer.dev/blog/writing-a-good-claude-md
- Trail of Bits: https://github.com/trailofbits/claude-code-config
- ChrisWiles: https://github.com/ChrisWiles/claude-code-showcase
- shanraisshan: https://github.com/shanraisshan/claude-code-best-practice
- Anthropic official: https://code.claude.com/docs/en/best-practices
