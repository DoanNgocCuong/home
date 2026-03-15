---
paths:
  - src/**/repository/**
  - src/**/repositories/**
  - src/**/models/**
  - src/**/schema/**
  - src/**/migration*/**
  - src/**/migrations/**
  - prisma/**
  - drizzle/**
  - db/**
  - "**/flyway/**"
  - "**/alembic/**"
---

# Database Rules

## Migrations
- NEVER edit an existing migration file — always create a new one
- Test migrations can be rolled back: migrate up then down then up
- Name migrations descriptively: `add_index_users_email` not `migration_042`
- Each migration does ONE thing — don't combine schema changes

## Queries
- ALWAYS use parameterized queries — never string concatenation (SQL injection)
- Add indexes for columns used in WHERE, JOIN, ORDER BY clauses
- Limit result sets — never `SELECT *` without WHERE in production code
- Use transactions for multi-step operations that must be atomic

## Types & Conventions
- IDs: use BIGINT or UUID (never INT — will overflow)
- Timestamps: use TIMESTAMPTZ (with timezone), never TIMESTAMP
- Money: use DECIMAL/NUMERIC, never FLOAT
- Booleans: default to FALSE, name as `is_active` / `has_verified`

## Performance
- Check query plans for new queries: EXPLAIN ANALYZE
- Watch for N+1: prefer JOINs or batch loading
- Add connection pooling configuration
- Set query timeouts to prevent long-running queries
