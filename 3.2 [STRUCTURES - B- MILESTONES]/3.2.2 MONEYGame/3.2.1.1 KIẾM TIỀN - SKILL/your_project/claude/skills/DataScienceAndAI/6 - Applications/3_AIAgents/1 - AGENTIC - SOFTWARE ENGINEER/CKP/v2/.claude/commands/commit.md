---
description: Create a smart conventional commit from current changes
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*), Bash(git diff:*)
model: haiku
---

## Current State
- Status: !`git status --short`
- Branch: !`git branch --show-current`
- Staged: !`git diff --cached --stat`
- Unstaged: !`git diff --stat`

## Staged Diff
!`git diff --cached`

## Task
Create a conventional commit from the staged changes.

Format: `type(scope): concise imperative description`

Types: feat, fix, refactor, docs, test, chore, perf, ci, style, build
Scope: most affected module/directory (optional for small changes)
Description: imperative mood, lowercase, no period, max 72 chars

Add body ONLY if the change is non-obvious (explain WHY, not WHAT).

If nothing is staged, stage all relevant changes first (skip .env, node_modules, etc).
If $ARGUMENTS is provided, use it as the commit message directly.
