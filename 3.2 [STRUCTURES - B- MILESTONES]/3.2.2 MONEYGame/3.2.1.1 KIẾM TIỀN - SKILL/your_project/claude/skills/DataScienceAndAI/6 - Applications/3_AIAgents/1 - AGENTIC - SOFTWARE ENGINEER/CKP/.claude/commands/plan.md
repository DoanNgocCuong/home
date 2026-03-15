---
description: Create a detailed implementation plan before writing any code
argument-hint: [feature or task description]
---

## Task
$ARGUMENTS

## Planning Protocol (NO code edits allowed)

### 1. Understand
- What EXACTLY is being asked?
- What does "done" look like?
- What are the acceptance criteria?

### 2. Research
- Grep the codebase for related patterns: `rg "relevant_pattern" src/`
- Read existing implementations of similar features
- Check CLAUDE.md and .claude/rules/ for constraints

### 3. Design
For each file to be created or modified:
- **File**: path
- **Changes**: what specifically changes
- **Why**: rationale for this approach
- **Risk**: what could go wrong

### 4. Verify Strategy
- What tests will confirm this works?
- What edge cases need coverage?
- What command runs the verification?

### 5. Effort Estimate
- Files to change: [count]
- New files: [count]
- Estimated complexity: [low/medium/high]
- Suggested approach: [single session / split into subtasks]

## Output
Present the complete plan as a numbered checklist.
DO NOT implement anything. Wait for approval.
