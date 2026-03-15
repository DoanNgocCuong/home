<!-- .claude/rules/database.md -->
---
paths:
  - src/**/repository/**
  - src/**/migration/**
  - **/drizzle/**
  - **/flyway/**
  - **/prisma/**
---

Database rules:
- NEVER edit existing migration files — always create new
- Parameterized queries only (prevent SQL injection)
- Add index for columns in WHERE/JOIN clauses
- Use BIGINT for IDs, TIMESTAMPTZ for timestamps
- Test migrations with rollback before committing
- Use connection pooling (PgBouncer/ProxySQL for high load)
