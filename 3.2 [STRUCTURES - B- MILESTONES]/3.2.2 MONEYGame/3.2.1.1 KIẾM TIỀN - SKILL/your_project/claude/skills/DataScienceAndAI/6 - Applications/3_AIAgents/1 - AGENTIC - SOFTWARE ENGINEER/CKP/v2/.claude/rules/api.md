---
paths:
  - src/**/controller/**
  - src/**/controllers/**
  - src/**/api/**
  - src/**/routes/**
  - src/**/endpoints/**
  - app/api/**
  - pages/api/**
---

# API Endpoint Rules

These rules apply to ALL API endpoint files.

## Input Validation
- EVERY endpoint MUST validate input before processing
- Use the project's validation library (Zod, Pydantic, Bean Validation, etc.)
- Never trust client-side validation — always re-validate server-side

## Response Format
- Use consistent error shape: `{ code, message, details }`
- Include correlation/request ID in error responses for debugging
- Never expose raw database errors, stack traces, or internal paths to clients

## Security
- Authentication: verify token/session before processing
- Authorization: check user has permission for this specific resource
- Rate limiting: public endpoints MUST have rate limits
- Never log sensitive data (passwords, tokens, PII)

## Logging
- Log request entry at DEBUG level
- Log errors at ERROR level with correlation ID
- Include enough context to reproduce the issue
