---
description: Fix a bug or implement a feature from a description
argument-hint: [describe the bug or feature]
---

## Task
$ARGUMENTS

## Mandatory Workflow (DO NOT skip steps)

### Step 1 — EXPLORE (read-only)
- Identify ALL files that will be affected
- Read each file completely
- Understand existing patterns and conventions
- Check CLAUDE.md for project-specific rules

### Step 2 — PLAN (no edits yet)
- List every file to modify and what changes each needs
- Identify potential side effects on other modules
- Define how you will VERIFY the fix works

Present the plan and WAIT for approval before proceeding.

### Step 3 — TEST FIRST
- Write or update tests that capture the expected behavior
- Run tests — they SHOULD fail (proving the bug exists or feature is missing)

### Step 4 — IMPLEMENT
- Make the minimum changes needed
- Follow existing code patterns exactly
- Do NOT refactor unrelated code
- Do NOT add features not requested

### Step 5 — VERIFY
- Run the full test suite
- Confirm the new tests pass
- Confirm no existing tests broke
- If anything fails → fix it before finishing

## Rules
- Never change tests to match broken code
- Never modify files outside the planned scope without asking
- If 3 fix attempts fail → STOP and explain the root issue
