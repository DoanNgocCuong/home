# Project Name

## Stack
- Backend: [language + framework]
- Frontend: [framework]
- Database: [DB engine]
- Infra: [Docker/K8s/etc]
- AI/ML: [if applicable]

## Commands
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Dev server: `[command]`
- DB migrate: `[command]`

## Structure
- `src/api/` — API endpoints and controllers
- `src/services/` — Business logic layer
- `src/models/` — Data models and schemas
- `src/utils/` — Shared utilities
- `tests/` — Tests (mirror src/ structure)
- `infra/` — Infrastructure configs (Docker, K8s, CI)

## Architecture Decisions
- [Key decision 1 — e.g. "CQRS via Mediator, not MVC"]
- [Key decision 2 — e.g. "Event-driven between services via Redis Streams"]
- [Key decision 3 — e.g. "Feature flags in LaunchDarkly, not env vars"]

## Conventions
1. [Most critical — e.g. "Result<T,E> pattern for errors, never throw for control flow"]
2. [Second — e.g. "DB migrations: never edit existing files, always create new"]
3. [Third — e.g. "Conventional commits: feat/fix/refactor(scope): description"]
4. [Fourth — e.g. "All API inputs validated with Zod/Pydantic/Bean Validation"]
5. [Fifth — e.g. "No secrets in code — use env vars or secret manager"]

## Verification
After ANY code change, run: `[test command]`
If tests fail → fix before marking done.
If build fails → fix before committing.

## Mistakes Claude Keeps Making
<!-- Add each time Claude repeats an error. This is the MOST VALUABLE section. -->
<!-- Example entries: -->
<!-- - STOP using `throw new Error()` for expected failures → use Result type -->
<!-- - STOP adding unnecessary dependencies → check existing utils first -->
<!-- - STOP editing migration files → create new migration instead -->
