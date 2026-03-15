---
description: Review recent code changes for bugs, security issues, and convention violations
allowed-tools: Read, Grep, Glob, Bash(git diff:*), Bash(git log:*), Bash(git show:*)
model: sonnet
---

## Changes to Review
!`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only --cached`
!`git diff --stat HEAD~1 2>/dev/null || git diff --stat --cached`

## Review Protocol

Analyze the diff carefully. For each finding, provide: file path, line number, issue, and fix.

### Checklist (in priority order)

1. **SECURITY** — SQL injection, XSS, auth bypass, secrets in code, path traversal, SSRF
2. **LOGIC** — null/undefined handling, off-by-one, race conditions, unhandled error paths, infinite loops
3. **PERFORMANCE** — N+1 queries, missing DB indexes, unbounded queries, memory leaks, unnecessary re-renders
4. **CONVENTIONS** — check CLAUDE.md rules, naming, file organization, import patterns
5. **TESTS** — are new code paths tested? edge cases? error cases? mocks correct?
6. **TYPES** — any `any` types? missing null checks? loose type assertions?

### Output Format

### 🔴 Critical (must fix before merge)
[findings]

### 🟡 Warning (should fix)
[findings]

### 🟢 Suggestion (nice to have)
[findings]

### ✅ What's good
[positive patterns worth noting]
