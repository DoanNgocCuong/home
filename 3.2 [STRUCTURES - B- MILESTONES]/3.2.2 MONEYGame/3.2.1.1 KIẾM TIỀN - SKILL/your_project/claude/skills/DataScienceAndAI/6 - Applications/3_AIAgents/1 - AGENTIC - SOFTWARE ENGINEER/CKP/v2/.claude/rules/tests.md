---
paths:
  - tests/**
  - test/**
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/*_test.*"
  - __tests__/**
---

# Testing Rules

## Golden Rule
NEVER modify a test to match incorrect implementation.
If a test fails, the CODE is wrong until proven otherwise.

## Test Quality
- Each test must be independent — no shared mutable state between tests
- Test names describe behavior: `should return 404 when user not found`
- Test ONE thing per test — if a test fails, you should know exactly what broke
- Cover the happy path, edge cases, AND error paths

## Edge Cases to Always Test
- Null / undefined / empty string inputs
- Boundary values (0, -1, MAX_INT, empty array, single element)
- Concurrent access (if applicable)
- Network failures / timeouts (mock these)
- Invalid auth / permission denied

## Mocking
- Mock external services — NEVER call real APIs in tests
- Mock at the boundary (HTTP client, DB client), not deep internals
- Verify mock interactions when the side effect IS the behavior

## Test Organization
- Mirror the src/ directory structure
- Colocate tests with source when possible (file.ts → file.test.ts)
- Group related tests with describe/context blocks
- Setup/teardown in beforeEach/afterEach, not in test body
