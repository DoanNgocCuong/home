---
description: Smart conventional commit from staged changes
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
model: haiku
---

## Current state
- Status: !`git status --short`
- Staged diff: !`git diff --cached --stat`
- Diff detail: !`git diff --cached`
- Branch: !`git branch --show-current`

## Rules
- Format: type(scope): concise description
- Types: feat, fix, refactor, docs, test, chore, perf, ci
- Scope: most affected module/package
- Description: imperative mood, lowercase, no period
- Body: only if change is non-obvious

If $ARGUMENTS provided, use as commit message directly.
Otherwise, analyze the diff and create the most accurate message.
