<!-- .claude/skills/systematic-debugging/SKILL.md -->
---
name: systematic-debugging
description: Five-step root cause analysis. Use when debugging errors, test failures, or unexpected behavior.
allowed-tools: Read, Grep, Glob, Bash
---

# Systematic Debugging Protocol

## 5-Step Process (NEVER skip steps)
1. **REPRODUCE** — Confirm you can trigger the bug
2. **LOCATE** — Find the immediate error (logs, stack trace, test output)
3. **TRACE** — Follow the call chain UPWARD: "What called this?"
4. **ROOT** — Keep tracing until you find the ORIGINAL trigger
5. **FIX** — Fix at the ROOT, not the symptom

## Anti-patterns to AVOID
- ❌ Guessing the fix without reproducing
- ❌ Fixing the symptom instead of the cause
- ❌ Changing multiple things at once
- ❌ Skipping step 3 (most common mistake)

## CRITICAL RULE
If THREE consecutive fix attempts fail → STOP.
This signals an architectural problem. Flag it, don't keep patching.

## Common Debugging Commands
```bash
# Python
python -m pytest -xvs                    # Run with verbose
python -m pytest --tb=short              # Shorter traceback
python -c "import pdb; pdb.pm()"        # Post-mortem debug

# JavaScript/Node
node --inspect-brk index.js              # Chrome DevTools
console.log('VAR:', variable)            # Quick debug

# Docker
docker logs <container> --tail 100       # View logs
docker exec -it <container> sh           # Shell into container
```
