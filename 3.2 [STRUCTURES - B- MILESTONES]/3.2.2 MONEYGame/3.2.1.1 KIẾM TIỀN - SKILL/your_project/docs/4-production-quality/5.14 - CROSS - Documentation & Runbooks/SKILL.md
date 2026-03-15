# Documentation & Runbooks — Production Best Practices

> **Domain:** 5.14 | **Group:** CROSS | **Lifecycle:** Cross-Cutting
> **Last Updated:** 2026-03-13

## 1. Overview

Documentation is the connective tissue of production systems. Without clear runbooks, architecture decisions, and operational knowledge, teams waste time solving the same problems repeatedly and knowledge evaporates when engineers leave. This domain covers documentation strategies, runbook structure, decision recording, and maintaining documentation freshness.

**Vietnamese:** Documentation không phải luxury, là necessity. Runbook tốt là sự khác biệt giữa 5 phút incident vs 5 giờ incident.

## 2. Core Principles

- **Documentation as Code:** Treat docs like application code—version control, review, test
- **Know Your Audience:** Different docs for operators vs engineers vs support teams
- **Runbooks > Tribal Knowledge:** Procedures must be explicit, testable, not in people's heads
- **Keep It Fresh:** Stale docs are worse than no docs; have staleness detection
- **Architecture Decisions Matter:** Record *why*, not just *what*; enable better future decisions
- **Searchability First:** Organize by problem/symptom, not by system component

## 3. Best Practices

### 3.1 Documentation Structure

**Practice: README-Driven Development**
- **What:** Write README before code; use it as design document
- **Why:** Forces clarity on purpose, usage, architecture before implementation; serves as quick-start
- **How:**
  ```markdown
  # MyApp: Real-time Notification Service

  ## What Is It?
  Pub-sub notification system using WebSockets and Redis. Delivers <100ms latency for user notifications.

  ## Quick Start
  ```bash
  docker run -e REDIS_URL=redis://localhost myapp:latest
  curl http://localhost:3000/health
  ```

  ## Architecture
  - **API Layer:** Express.js handling WebSocket upgrades
  - **Message Queue:** Redis pub-sub for fanout
  - **Persistence:** PostgreSQL for notification history (7-day retention)
  - **Scaling:** Horizontal by adding Redis Sentinel, stateless API servers

  ## Dependencies
  | Service | Version | Purpose | SLA |
  |---------|---------|---------|-----|
  | Redis | 7.x | Message queue | 99.99% availability |
  | PostgreSQL | 14.x | Audit log | 99.9% availability |

  ## Configuration
  - `REDIS_URL`: Connection string (required)
  - `LOG_LEVEL`: debug/info/warn/error (default: info)
  - `NOTIFICATION_TTL`: Days to retain (default: 7)

  ## How to Deploy
  See [DEPLOYMENT.md](docs/DEPLOYMENT.md)

  ## Troubleshooting
  See [RUNBOOKS.md](docs/RUNBOOKS.md)

  ## Contributing
  See [CONTRIBUTING.md](docs/CONTRIBUTING.md)
  ```
  - Keep in root, within 50 lines
  - Link to detailed docs, don't duplicate
  - Real dependencies and configuration, not aspirational
- **Anti-pattern:** Empty README, outdated setup instructions, aspirational docs that don't match reality

**Practice: Architecture Decision Records (ADRs)**
- **What:** Structured records of architectural decisions, alternatives considered, tradeoffs
- **Why:** Prevents "why did we do this?" questions, enables better future decisions, institutional memory
- **How:**
  ```markdown
  # ADR 0001: Use WebSockets Instead of Server-Sent Events (SSE)

  **Date:** 2024-03-01
  **Status:** Accepted | Superseded by ADR-0010 | Rejected

  ## Context
  Need to deliver real-time notifications with <100ms latency to web clients.
  Current HTTP polling causes 20% CPU spike during peak load.

  ## Decision
  Adopt WebSockets for bidirectional communication.

  ## Alternatives Considered
  1. **HTTP Long-Polling:** Simpler but high connection overhead, polling delays
  2. **Server-Sent Events:** Unidirectional only, doesn't meet future requirements for client→server
  3. **gRPC:** Type-safe, but overkill for web browsers (no native gRPC)
  4. **MQTT:** Good for IoT, unnecessary complexity for web
  5. **WebSockets:** Native browser support, bidirectional, <100ms latency ✓

  ## Consequences
  **Positive:**
  - Latency reduced from 5-10s (polling) to <100ms
  - 30% reduction in API calls during peak load
  - Foundation for future client→server features

  **Negative:**
  - Stateful connections harder to scale horizontally (need Redis pub-sub)
  - Client library updates required across products
  - Connection lifecycle management complexity

  ## Implementation Notes
  - Use Socket.io for cross-browser compatibility and fallbacks
  - Redis pub-sub for fanout across service replicas
  - Connection heartbeat every 30s to detect stale connections

  ## Related
  - ADR-0002: Redis for Distributed Pub-Sub
  - ADR-0003: PostgreSQL for Notification History
  ```
  - Keep in `/docs/adr/` directory
  - Use Lightweight ADR: status | date | decision | consequences
  - Decisions become immutable once made; amendments create new ADRs
- **Anti-pattern:** No ADRs (tribal knowledge), ADRs written after decision already locked in, not reviewing ADRs during code review

### 3.2 Runbooks & Operational Procedures

**Practice: Incident Runbook Structure**
- **What:** Step-by-step procedures for resolving specific incidents
- **Why:** During incident, operators are stressed; explicit procedures prevent mistakes, reduce MTTR
- **How:**
  ```markdown
  # Runbook: Database Replication Lag > 60 seconds

  ## Severity
  **High:** Notifications delayed, eventual consistency violated, user-facing impact

  ## Detection
  - Alert fires when `postgresql_replication_lag_seconds > 60`
  - Check dashboard: Monitoring → PostgreSQL → Replication Lag
  - Manual check: `psql -c "SELECT now() - pg_last_xact_replay_timestamp() as lag;"`

  ## Prerequisites
  - VPN connected to production network
  - SSH access to database server
  - Read permission on RDS console (for AWS)
  - Slack access to #incidents channel

  ## Diagnosis
  1. **Check replication status:**
     ```bash
     ssh prod-db-01.internal
     psql -c "SELECT slot_name, restart_lsn, confirmed_flush_lsn FROM pg_replication_slots;"
     ```
     If slots are missing → replication broken

  2. **Check network:**
     ```bash
     ping replica-01.internal
     tcpdump -i eth0 host replica-01 and port 5432
     ```
     If no packets → network/firewall issue

  3. **Check replica write load:**
     ```bash
     # On replica
     SELECT now() - pg_last_xact_replay_timestamp() as lag;
     SELECT client_addr, query FROM pg_stat_activity WHERE wait_event IS NOT NULL;
     ```
     High load queries on replica = lagging replicas are normal if they're catching up

  4. **Check primary write load:**
     ```bash
     # On primary
     SELECT total_time, calls, mean_time, query FROM pg_stat_statements
     ORDER BY total_time DESC LIMIT 5;
     ```
     Sudden spike in writes? Check for runaway job.

  ## Resolution Steps

  ### Option A: Replica Catching Up (Lag Normal)
  - Lag from high write load is temporary; wait 5-10 minutes for replica to catch up
  - No action needed unless lag continues > 5 minutes
  - Proceed to Step 3 if still lagging

  ### Option B: Network Issue
  1. Verify network connectivity:
     ```bash
     mtr -c 100 replica-01.internal
     ```
  2. Check firewall rules:
     ```bash
     aws ec2 describe-security-groups --group-id sg-xxx
     ```
  3. Restart replica networking:
     ```bash
     aws rds reboot-db-instance --db-instance-identifier prod-replica-01
     ```
     This triggers automatic reboot with 2-5 minute downtime

  ### Option C: Replication Slot Issue
  1. **Check stuck slot:**
     ```sql
     SELECT * FROM pg_replication_slots WHERE slot_type='physical' AND restart_lsn IS NOT NULL;
     ```
  2. **If WAL file backing slot is missing:**
     ```bash
     # Get oldest needed LSN
     SELECT pg_wal_lsn_diff(pg_current_wal_insert_lsn(), '0/0')::bigint;
     ```
  3. **Drop and recreate slot:**
     ```sql
     SELECT pg_drop_replication_slot('slot_name');
     -- On replica: pg_basebackup -D /var/lib/postgresql -h primary -R
     ```
     This requires ~10 minutes for full base backup

  ### Option D: Critical Lag (> 5 minutes)
  1. **Kill long-running replica queries:**
     ```bash
     ssh replica-01.internal
     psql -c "SELECT pg_cancel_backend(pid) FROM pg_stat_activity
              WHERE query LIKE 'SELECT%' AND wait_event IS NOT NULL;"
     ```
  2. **If still lagging, failover to new replica:**
     - Contact DBA team
     - Run failover runbook: [Runbook: Failover Primary Database](failover.md)

  ## Validation
  - [ ] Replication lag dropped below 10 seconds
  - [ ] Replica responsive to queries (< 100ms query time)
  - [ ] Primary write throughput normal (< 5k tx/sec)

  ## Escalation
  - **5 min lag:** Page on-call DBA
  - **10 min lag:** Page DBA + Engineering Lead
  - **15 min lag:** Declare SEV-1 incident, notify VP Engineering

  ## Post-Incident
  - [ ] Slack update in #incidents with resolution
  - [ ] Create incident postmortem within 24 hours
  - [ ] Check if similar issues in other services

  ## References
  - PostgreSQL Replication: https://www.postgresql.org/docs/current/warm-standby.html
  - AWS RDS Replication: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html
  - Previous incident: [INC-2024-003](incidents/inc-2024-003.md)
  ```
  - Structure: Severity → Detection → Prerequisites → Diagnosis → Resolution → Validation → Escalation
  - Written for 3am operator under stress; be explicit, no assumptions
  - Test runbooks quarterly by running through them in staging
- **Anti-pattern:** Vague procedures ("check logs"), no step-by-step diagnosis, no runbook testing, procedures that require expertise to interpret

**Practice: Incident Postmortem Template**
- **What:** Structured analysis of incident: what happened, why, what to prevent recurrence
- **Why:** Learning from failures, pattern recognition, continuous improvement
- **How:**
  ```markdown
  # Incident Postmortem: Database Replication Lag > 60s

  **Incident ID:** INC-2024-025
  **Date:** 2024-03-10
  **Duration:** 18 minutes (14:32-14:50 UTC)
  **Severity:** High (notifications delayed, customer impact)
  **Author:** oncall-dba@example.com
  **Attendees:** DBA, Backend Lead, Ops Lead

  ## Executive Summary
  A long-running batch job (daily user archive) created write spike on primary database.
  Replica lagged >60s, triggering alerts. Resolved by pausing batch job and allowing replica to catch up.

  ## Timeline
  - 14:32 UTC: Alert fires "database replication lag > 60s"
  - 14:35 UTC: On-call DBA pages in, diagnosis begins
  - 14:40 UTC: Root cause identified (batch job exceeded normal write load)
  - 14:45 UTC: Batch job paused, replica begins catching up
  - 14:50 UTC: Lag returns to normal (<1s), incident resolved

  ## Root Cause Analysis (5 Whys)
  1. **Why did replication lag?** Write load exceeded replica disk I/O capacity
  2. **Why was write load high?** Batch job scaling issue (too many parallel workers)
  3. **Why did batch job increase parallelism?** Code change in PR #4521 increased workers from 4 to 16
  4. **Why wasn't this caught in staging?** Staging database smaller; batch load wasn't representative
  5. **Why no load testing?** Load testing checklist missing from batch job merge requirements

  ## Impact Assessment
  - **Duration:** 18 minutes
  - **User Impact:** Notifications delayed by 30-60 seconds for 2.1% of active users
  - **Business Impact:** $5k estimated marketing campaign notifications delayed
  - **Data Loss:** None (replication fully caught up after incident)

  ## Contributing Factors
  1. Batch job size not tested against production database load
  2. Replica I/O not monitored as distinct metric (only overall CPU/RAM alerting)
  3. Runbook for this scenario existed but not followed (checked logs instead of running diagnosis)

  ## What Went Well
  - Alert triggered immediately (good alerting threshold)
  - On-call DBA responded within 3 minutes
  - Clear escalation path was followed
  - Batch job pause was low-risk fix

  ## Action Items

  | Action | Owner | Due | Priority |
  |--------|-------|-----|----------|
  | Add replica disk I/O monitoring | DBA-Team | 2024-03-17 | P0 |
  | Batch job load test in staging before deploy | Backend-Team | 2024-03-20 | P0 |
  | Add load testing to batch job merge checklist | Backend-Team | 2024-03-17 | P1 |
  | Test replication lag runbook (INC-025-runbook) | Ops-Team | 2024-03-15 | P1 |
  | Review batch job parallelism algorithm | Backend-Team | 2024-03-24 | P2 |

  ## Lessons Learned
  - Batch jobs need same load testing rigor as API endpoints
  - Staging environment must mirror production scale for realistic testing
  - Runbooks are only effective if followed; training needed
  - Proactive replica monitoring (disk I/O, CPU) catches issues earlier

  ## Follow-Up
  - Batch job PR #4521 will be reverted pending rewrite with proper scaling
  - Next engineering meeting agenda: "Batch Job Testing Strategy"
  - Monitoring improvements tracked in Jira: PLATFORM-1234
  ```
  - File in `/incidents/` with date-based naming
  - Blameless: focus on systemic issues, not individual fault
  - Action items should be added to backlog and tracked
  - Share in team channels; make searchable
- **Anti-pattern:** Blame-focused postmortems, action items never tracked, same incidents recurring quarterly

### 3.3 Knowledge Organization & Searchability

**Practice: Documentation Architecture (Docs-as-Code)**
- **What:** Documentation stored in Git alongside code, built and deployed like application
- **Why:** Version control, peer review, automation, prevents drift from code
- **How:**
  ```bash
  # Directory structure
  docs/
  ├── README.md                  # Overview, quick links
  ├── GETTING_STARTED.md         # Setup & first deploy
  ├── ARCHITECTURE.md            # System design, diagrams
  ├── DEPLOYMENT.md              # How to deploy (dev/staging/prod)
  ├── API.md                     # API documentation (OpenAPI)
  ├── RUNBOOKS/
  │   ├── high-cpu-usage.md
  │   ├── database-lag.md
  │   ├── service-timeout.md
  │   └── failover-database.md
  ├── INCIDENT_RESPONSE/
  │   ├── severity-levels.md
  │   ├── escalation.md
  │   └── postmortem-template.md
  ├── OPERATIONS/
  │   ├── monitoring.md
  │   ├── alerting.md
  │   ├── oncall-rotation.md
  │   └── maintenance-windows.md
  ├── adr/                       # Architecture Decision Records
  │   ├── 0001-websockets.md
  │   ├── 0002-redis-pubsub.md
  │   └── 0003-postgresql.md
  └── diagrams/                  # Architecture diagrams (Mermaid, PlantUML)
      ├── system-architecture.mmd
      ├── data-flow.mmd
      └── deployment-pipeline.mmd

  # CI/CD: Build docs on every commit
  # .github/workflows/docs.yml
  name: Build & Deploy Docs
  on: [push]
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Build docs with MkDocs
          run: pip install mkdocs && mkdocs build
        - name: Deploy to documentation site
          run: aws s3 sync site/ s3://docs.example.com/
  ```
  - Tools: MkDocs (Python), Docusaurus (JavaScript), Hugo (Go), Sphinx (reStructuredText)
  - Peer review: PR review includes docs changes
  - Search: built-in full-text search in documentation sites
- **Anti-pattern:** Docs in wiki without version control, docs in multiple places, no automated build/deploy

**Practice: Diagram-as-Code**
- **What:** Diagrams defined in text format, version controlled and rendered as images
- **Why:** Sync diagrams with code changes, easy collaboration, diffs are readable
- **How:**
  ```mermaid
  # docs/diagrams/system-architecture.mmd
  graph TD
    A[Client] -->|HTTPS| LB[Load Balancer]
    LB -->|HTTP| API1[API Server 1]
    LB -->|HTTP| API2[API Server 2]
    API1 -->|Query| PG[PostgreSQL Primary]
    API2 -->|Query| PG
    PG -->|Replication| REP[Replica]
    API1 -->|Pub/Sub| RD[Redis Cluster]
    API2 -->|Pub/Sub| RD
    RD -->|Cache| API1
    RD -->|Cache| API2
    API1 -->|Log| ELK[ELK Stack]
    API2 -->|Log| ELK

    style API1 fill:#e1f5ff
    style API2 fill:#e1f5ff
    style PG fill:#fff3e0
    style REP fill:#fff3e0
    style RD fill:#f3e5f5
  ```
  - Tools: Mermaid (JavaScript), PlantUML (Java), Excalidraw (visual), Graphviz
  - Include in documentation: rendered as SVG/PNG on build
  - Update diagrams during code review if architecture changes
- **Anti-pattern:** PNG/JPEG diagrams without source (can't edit), diagrams in presentations only, no version history

### 3.4 Documentation Freshness & Maintenance

**Practice: Staleness Detection & Enforcement**
- **What:** Automated checks to prevent documentation from drifting from reality
- **Why:** Stale docs are worse than no docs; outdated runbooks waste time during incidents
- **How:**
  ```markdown
  # docs/deployment.md
  **Last verified:** 2024-03-01
  **Verified by:** oncall-ops
  **Next verification due:** 2024-04-01

  _If this date is older than 30 days, this document is STALE and should not be trusted._
  ```
  - CI/CD check: warn if any doc last-verified > 30 days old
  - Monthly rotation: on-call engineer verifies one runbook works end-to-end
  - Automated checks in code:
  ```bash
  # Check docs frontmatter
  #!/bin/bash
  for doc in docs/**/*.md; do
    last_verified=$(grep "Last verified:" "$doc" | cut -d: -f2)
    verified_date=$(date -d "$last_verified" +%s)
    today=$(date +%s)
    days_old=$(( ($today - $verified_date) / 86400 ))

    if [ $days_old -gt 30 ]; then
      echo "WARN: $doc is $days_old days old, needs verification"
    fi
  done
  ```
  - Use `git log` to detect stale docs:
  ```bash
  find docs -name "*.md" -exec sh -c 'echo "Last updated: $(git log -1 --format=%ci $1)" "$1"' \;
  ```
- **Anti-pattern:** No tracking of doc age, runbooks never tested, docs update notification lost in backlog

**Practice: Documentation Review in Code Review**
- **What:** Merge checklist includes documentation audit
- **Why:** Code changes often require documentation updates; easy to forget if not part of review
- **How:**
  ```markdown
  # Pull Request Checklist
  - [ ] Code changes
  - [ ] Unit tests added
  - [ ] Integration tests pass
  - [ ] Documentation updated or not needed
    - [ ] README.md updated if user-facing changes
    - [ ] API documentation (OpenAPI) updated if endpoints changed
    - [ ] Runbook updated if operational behavior changed
    - [ ] ADR created if architectural decision made
    - [ ] CHANGELOG.md entry added
  - [ ] Security checklist reviewed
  - [ ] Performance impact considered
  ```
  - Reviewer comment: "What's the documentation impact of this change?"
  - Require documentation PR before merging code if doc change needed
- **Anti-pattern:** Code review doesn't mention docs, docs lagging behind code, no process to catch missing docs

### 3.5 API Documentation

**Practice: OpenAPI/Swagger Documentation**
- **What:** Machine-readable API specification with automatic documentation generation
- **Why:** Single source of truth for API contract, enables code generation, interactive documentation
- **How:**
  ```yaml
  # docs/openapi.yaml
  openapi: 3.0.0
  info:
    title: Notification API
    version: 1.0.0
  servers:
    - url: https://api.example.com/v1
  paths:
    /notifications:
      get:
        summary: List notifications for user
        parameters:
          - name: limit
            in: query
            schema:
              type: integer
              default: 50
          - name: offset
            in: query
            schema:
              type: integer
              default: 0
        responses:
          '200':
            description: List of notifications
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    notifications:
                      type: array
                      items:
                        $ref: '#/components/schemas/Notification'
                    total:
                      type: integer
          '401':
            description: Unauthorized (missing auth token)
      post:
        summary: Create notification
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NotificationCreate'
        responses:
          '201':
            description: Notification created
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Notification'
  components:
    schemas:
      Notification:
        type: object
        properties:
          id:
            type: string
            format: uuid
          title:
            type: string
          message:
            type: string
          created_at:
            type: string
            format: date-time
      NotificationCreate:
        type: object
        required:
          - title
          - message
        properties:
          title:
            type: string
          message:
            type: string
  ```
  - Generate interactive Swagger UI automatically
  - Use in CI/CD: validate requests/responses against spec
  - Tools: Swagger Editor (edit), SwaggerHub (managed), ReDoc (docs generation)
- **Anti-pattern:** Outdated API docs, no spec synchronization with code, docs in wiki with manual updates

## 4. Decision Frameworks

**Documentation by Audience:**
| Audience | Format | Location | Update Frequency |
|----------|--------|----------|------------------|
| New engineers | Onboarding guide + videos | Wiki + README | Quarterly |
| On-call ops | Runbooks + checklists | Git + searchable site | Monthly verification |
| API consumers | OpenAPI spec + Swagger UI | Interactive docs site | On deployment |
| Incident responders | Postmortems + decision log | Knowledge base | After each incident |
| Architects | ADRs + system diagrams | Git + documentation site | When decisions made |

## 5. Checklist

- [ ] README in project root with quick start and architecture overview
- [ ] All ADRs documented in `/docs/adr/` with status and consequences
- [ ] Runbooks exist for all SEV-1 and SEV-2 incident scenarios
- [ ] Runbooks tested end-to-end quarterly
- [ ] API documented in OpenAPI spec with Swagger UI deployed
- [ ] Deployment procedure documented and tested
- [ ] Incident response plan and postmortem template documented
- [ ] On-call rotation documented with escalation paths
- [ ] Architecture diagrams kept in sync with code (diagram-as-code)
- [ ] Documentation freshness tracked (< 30 days since last verified)
- [ ] All documentation in Git with version history
- [ ] Search functionality across all internal documentation
- [ ] Documentation reviewed as part of code review process
- [ ] Knowledge base indexed and searchable by problem/symptom
- [ ] Incident postmortems archived and searchable

## 6. Common Mistakes & Anti-Patterns

1. **Runbooks written after incident over** → Write during incident for maximum accuracy
2. **Documentation only in Confluence** → Version control lost, history inaccessible
3. **API docs out of sync with code** → Use generated docs from code annotations
4. **Stale docs never updated** → Set verification deadlines, make it someone's responsibility
5. **Same problem solved 5 times** → Searchable knowledge base prevents duplicated effort
6. **Runbook assumes tribal knowledge** → Write for new team member, be explicit
7. **No incident postmortems** → Great way to prevent recurring issues
8. **ADRs written but never referenced** → Link to ADRs during code review and architecture discussions
9. **Documentation scattered across tools** → Single source of truth (Git-based documentation site)
10. **Diagrams not updated with code** → Version control diagrams with code, review together

## 7. Tools & References

**Documentation Generators:**
- MkDocs, Docusaurus, Hugo, Sphinx, ReadTheDocs (hosting)

**Diagram Tools:**
- Mermaid, PlantUML, Excalidraw, Graphviz, draw.io

**API Documentation:**
- OpenAPI/Swagger, AsyncAPI (async APIs), GraphQL schema documentation

**Knowledge Management:**
- Confluence, Notion, GitBook (wiki style with Git sync)

**Incident Management:**
- PagerDuty, Opsgenie (on-call + incident tracking), Jira Service Management

**Standards:**
- RFC 3986 (URI), JSON Schema, Semantic Versioning (SemVer)

---

**Vietnamese Note:** Tốt nhất là code tự nói. Nhưng code không thể nói "tại sao". Documentation nói "tại sao". (Code speaks best. But code cannot say "why". Documentation speaks "why".)
