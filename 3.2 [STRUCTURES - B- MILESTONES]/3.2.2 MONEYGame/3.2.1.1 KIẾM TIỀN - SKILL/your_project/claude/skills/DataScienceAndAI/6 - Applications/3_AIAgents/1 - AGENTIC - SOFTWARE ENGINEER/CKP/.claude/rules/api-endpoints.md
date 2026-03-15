<!-- .claude/rules/api-endpoints.md -->
---
paths:
  - src/**/controller/**
  - src/**/api/**
  - src/**/routes/**
---

API endpoint rules:
- Validate ALL input (Pydantic schema or Bean Validation)
- Consistent error response: { code, message, details, correlationId }
- Log request at DEBUG, errors at ERROR with correlation ID
- Rate limiting on public endpoints
- Never return raw database errors to client
- REST: kebab-case endpoints (/user-sessions not /userSessions)
