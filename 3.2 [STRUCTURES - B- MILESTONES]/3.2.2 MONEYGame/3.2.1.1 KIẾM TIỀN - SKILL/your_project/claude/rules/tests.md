<!-- .claude/rules/tests.md -->
---
paths:
  - tests/**
  - **/*.test.*
  - **/*.spec.*
---

Testing rules:
- Never modify tests to match incorrect implementation
- Test edge cases: null, empty, boundary values, error paths
- Mock external services, never call real APIs in tests
- Each test must be independent (no shared mutable state)
- Descriptive test names: "should [behavior] when [condition]"
- Test coverage: minimum 80% for new features
- Colocate tests next to source files (*.test.ts next to *.ts)
