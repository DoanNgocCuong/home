# Production Readiness — Production Best Practices

> **Domain:** 5.10 | **Group:** RUN | **Lifecycle:** Run Time
> **Last Updated:** 2026-03-13

---

## 1. Overview

Production readiness is a structured process to ensure systems are mature, observable, and resilient before launch. Google's SRE book establishes this framework; teams following it reduce incident severity by 60-80%. This skill covers checklists, launch criteria, operational maturity, and post-launch validation.

**Tiếng Việt:** Sự sẵn sàng cho sản xuất (production readiness) là quá trình có cấu trúc để đảm bảo hệ thống trưởng thành, khả quan sát, và tàng lạc trước khi phát hành.

---

## 2. Core Principles

1. **Shift Left** — Begin readiness checks early (design phase), not launch day
2. **Operational Maturity Matters** — Code quality is necessary but not sufficient
3. **Automate Everything** — Manual runbooks don't scale; automate recovery
4. **Test in Production** — Staging ≠ production; use feature flags and canary deployment
5. **Blameless Culture** — Post-mortems focus on systems, not people
6. **Continuous Improvement** — Readiness is not one-time; improve after every incident

---

## 3. Best Practices

### 3.1 Production Readiness Review (PRR)

**Practice:** Formal review before every major deployment

**Participants:**
- Tech lead (author of system)
- SRE or ops engineer
- Security engineer
- Database administrator (for data-heavy services)

**Scope:** 2-4 hours, covers all checklist items below

**Output:** Signed-off readiness document, or list of blockers to fix

**Timing:** 1-2 weeks before planned launch

---

### 3.2 Launch Readiness Criteria

**Service MUST NOT launch without:**

1. **Reliability** (5.07)
   - [ ] SLO defined and achievable (e.g., 99.5% uptime)
   - [ ] Error rate monitoring < 1% baseline
   - [ ] Circuit breakers for all external dependencies
   - [ ] Retry logic with exponential backoff
   - [ ] Graceful degradation strategy documented

2. **Observability** (5.08)
   - [ ] Structured logging deployed (JSON format)
   - [ ] Traces collected via OpenTelemetry or similar
   - [ ] Key metrics instrumented (latency, errors, throughput)
   - [ ] SLI/SLO dashboard created
   - [ ] Alert rules configured with runbooks

3. **Error Handling** (5.09)
   - [ ] Exception hierarchy designed
   - [ ] API error responses follow RFC 7807
   - [ ] Error codes documented
   - [ ] Dead letter queues for async operations
   - [ ] Stack traces logged internally, not exposed to users

4. **Capacity & Performance**
   - [ ] Load test completed (peak load for 1 hour)
   - [ ] p99 latency < SLO threshold
   - [ ] Horizontal scaling tested (add/remove instances)
   - [ ] Database query performance reviewed (no N+1)
   - [ ] Memory/CPU baselines established

5. **Security** (covered in 6.XX)
   - [ ] Security review completed
   - [ ] Input validation on all APIs
   - [ ] No hardcoded secrets
   - [ ] HTTPS only
   - [ ] Access control tested
   - [ ] Data encryption at rest and in transit

6. **Data & Backup**
   - [ ] Database backup strategy defined and tested
   - [ ] Recovery time tested (can restore from backup in X minutes)
   - [ ] Data retention policy defined
   - [ ] Compliance (GDPR, CCPA) addressed

7. **Runbooks & Documentation**
   - [ ] Runbook for each alert
   - [ ] How to manually trigger failover
   - [ ] How to scale service up/down
   - [ ] How to roll back deployment
   - [ ] On-call escalation path documented

---

### 3.3 Pre-Production Checklist (Google SRE Book)

**Infrastructure & Deployment:**
- [ ] All services have unique names (no conflicts)
- [ ] Configuration management system deployed (Terraform, CloudFormation, etc.)
- [ ] Deployment process automated (no manual steps)
- [ ] Canary deployment strategy configured
- [ ] Rollback automation tested (< 5 minutes to rollback)
- [ ] Version control for all configuration

**Operations:**
- [ ] On-call rotation established (minimum 3 people)
- [ ] On-call support tools configured (paging, alerting, escalation)
- [ ] Incident response process documented
- [ ] Post-mortem process established
- [ ] Monitoring and alerting accessible 24/7
- [ ] SLO tracking visible to team

**Development & Quality:**
- [ ] Code review process enforced
- [ ] Automated tests running (unit, integration, e2e)
- [ ] Test coverage > 80% for critical paths
- [ ] Performance benchmarks established
- [ ] Security scanning automated (SAST, dependency scanning)

**Disaster Recovery:**
- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Failover tested within last 30 days
- [ ] Backup restoration tested
- [ ] Multi-region readiness (if applicable)

---

### 3.4 Operational Maturity Model

**Level 1 (Initial):**
- Manual deployments
- Reactive monitoring only
- No runbooks
- Ad-hoc incident response
- Frequent manual interventions

**Level 2 (Managed):**
- Automated deployments
- Basic monitoring and alerting
- Runbooks for common issues
- Post-mortems conducted
- Some automation for recovery

**Level 3 (Optimized):** ← Target for production readiness
- Fully automated CI/CD
- Comprehensive observability (logs, metrics, traces)
- Runbooks with automation (playbooks)
- Chaos engineering practiced
- Self-healing infrastructure
- Predictive scaling

---

### 3.5 Runbook Requirements

**Every Alert Needs a Runbook:**

**Minimum Runbook Contents:**
1. **What it means:** Explain the alert in plain English
2. **Severity:** Critical? Page on-call? Or just FYI?
3. **Quick diagnosis:** 3-5 commands/queries to understand problem
4. **Common causes:** 80% of cases, in order of likelihood
5. **Resolution steps:** Numbered, clear actions
6. **Escalation:** When to contact database team? security?
7. **Post-incident:** What to investigate after fix

**Example Runbook (Database CPU High):**

```
## Alert: Database CPU > 80%

### What It Means
Database server is running CPU-intensive queries.
If sustained, queries will time out and user requests fail.

### Quick Diagnosis
1. SSH to database server
2. Run: `top -b -n 1 | head -20`  # See top processes
3. Run: `mysql -e "SHOW PROCESSLIST;"`  # See queries
4. Check application logs for slow query logs

### Common Causes (in order of likelihood)
1. **Full table scan** (missing index)
   - Query joins large table without index
   - Fix: Add index on join key

2. **Sudden traffic spike**
   - More requests than usual
   - Fix: Trigger auto-scaling, or use circuit breaker to reduce load

3. **Long-running migration**
   - ALTER TABLE, index creation running
   - Fix: Wait or kill migration

### Resolution Steps
1. Check if it's auto-scaling issue:
   - Is traffic > baseline? Check dashboards
   - If yes: Auto-scaling should kick in (wait 2 min)

2. Check for slow queries:
   - Run: `mysql -e "SELECT * FROM mysql.slow_log;"`
   - Identify slow query
   - Add index if missing: `CREATE INDEX idx_name ON table(column);`

3. If still high:
   - Temporarily reduce connections:
     `max_connections = 100` (reduce from 500)
   - Kill long-running query: `KILL 123;`
   - Page database team if step 2 added index

### Escalation
- After 15 min: Page database engineer (@db-oncall)
- After 30 min: Page database architect

### Post-Incident
- Was index added? Add to deployment checklist
- Was traffic spike expected? Update capacity plan
- Did auto-scaling work? Verify configurations
```

---

### 3.6 On-Call Setup

**Essentials:**
- **Rotation:** 3-5 engineers per on-call rotation (one primary, one backup)
- **Duration:** 1 week per engineer (prevents burnout)
- **Hours:** During business hours initially; 24/7 if business-critical
- **Tools:** Paging system (PagerDuty, Opsgenie), Slack integration
- **Compensation:** Extra pay or time off in lieu
- **Support:** On-call engineer can escalate to team lead/architect

**Example SLA:**
- P1 (critical): Page on-call, respond in 15 minutes
- P2 (high): Page on-call, respond in 1 hour
- P3 (medium): Create ticket, respond next business day
- P4 (low): Informational only

---

### 3.7 Incident Response Plan

**Incident Response Phases:**

1. **Detection** (5 min)
   - Alert fires
   - On-call notified via PagerDuty

2. **Initial Response** (15 min)
   - On-call reads runbook
   - Diagnoses problem
   - Attempts fix

3. **Escalation** (if needed)
   - If > 30 min: Page tech lead
   - If > 60 min: Page engineering manager
   - Assemble war room (video call + shared docs)

4. **Mitigation** (during incident)
   - Immediate action: circuit breaker? scale down? rollback?
   - Status updates every 15 minutes
   - Update status page

5. **Resolution**
   - Fix deployed or rollback completed
   - Monitor for 15 minutes
   - Declare resolved

6. **Post-Mortem** (within 48 hours)
   - What happened? (timeline)
   - Why did it happen? (root cause)
   - How do we prevent next time? (action items)

---

### 3.8 Capacity Planning

**Practice:** Forecast infrastructure needs 3-12 months ahead

**Factors:**
- Growth rate (X% per month)
- Seasonality (peak in Q4 for e-commerce)
- New features (may increase load)
- Concurrency limits (database connections, API quotas)

**Process:**
1. Measure current capacity (p99 latency, CPU, memory at peak)
2. Forecast demand (traffic growth models)
3. Calculate headroom (40-60% utilization target)
4. Plan procurement (takes 6-12 weeks for hardware)

**Example:**
```
Current: 100 RPS, 50% CPU, 80% memory
Growth: 20% per month
In 3 months: 172 RPS (need 86% capacity)
In 6 months: 296 RPS (need 148% capacity → over limit)

Action: Add new database replica/shard in 4 months
```

---

### 3.9 Performance Baseline

**Practice:** Establish "normal" performance before launch

**Collect:**
- Response time: p50, p95, p99
- Throughput: requests/second at peak
- Resource usage: CPU, memory, disk, network
- Database: query latency, connection count
- Cache: hit rate, eviction rate

**Document:**
- At 10 RPS, p99 latency = 50ms
- At 100 RPS, p99 latency = 200ms
- At 1000 RPS, p99 latency = timeout (fail)
- Conclusion: System designed for max 500 RPS

**Use:** Capacity planning, alerting thresholds, scaling triggers

---

### 3.10 Security Review Checklist

**Critical:**
- [ ] Input validation on all APIs (SQL injection, XSS prevention)
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] HTTPS only (no HTTP)
- [ ] Access control: verify user permissions before returning data
- [ ] Rate limiting to prevent abuse/brute force
- [ ] Data encryption at rest (database)
- [ ] Data encryption in transit (TLS)
- [ ] Secrets management (AWS Secrets Manager, HashiCorp Vault)
- [ ] Dependency scanning for known vulnerabilities

**Important:**
- [ ] Logging doesn't contain sensitive data (passwords, tokens)
- [ ] Error messages don't leak implementation details
- [ ] CORS properly configured (not `*`)
- [ ] CSRF tokens on state-changing operations
- [ ] SQL queries parameterized (no string concatenation)

---

### 3.11 Dependency Audit

**Practice:** Catalog and monitor all external dependencies

**Types:**
- External APIs (payment processor, weather service)
- Internal services (user service, product service)
- Databases (primary, replicas, cache)
- Message queues (Kafka, RabbitMQ)
- CDN, DNS, load balancer

**Audit:**
- [ ] SLO for each dependency documented
- [ ] Fallback behavior if dependency fails
- [ ] Circuit breaker configured
- [ ] Health check monitoring
- [ ] Timeout configured
- [ ] Retry strategy designed
- [ ] Dependency failure impact (does it break service?)

**Example:**
```
Dependency: Payment Processor (Stripe)
SLO: 99.9% uptime
Fallback: Offline mode (queue payments, retry later)
Circuit Breaker: Yes (5% error threshold)
Timeout: 10s connection, 30s read
Retry: 3 attempts, exponential backoff
Impact: High (payment processing blocked)
```

---

### 3.12 Rollback Plan

**Practice:** Every deployment must have < 5 minute rollback

**Strategies:**
1. **Blue-Green Deployment:** Two production environments, switch between
2. **Canary Deployment:** Route 5% → new version, 95% → old
3. **Feature Flags:** Deploy code, but disable feature
4. **Database Migrations:** Only add columns (no schema breaking changes)

**Test Rollback:**
- In staging, deploy new version
- Verify it works
- Roll back
- Verify rollback completes in < 5 minutes
- Verify data is consistent after rollback

**Anti-pattern:** Rollback takes 2 hours; user impact unknown

---

### 3.13 Monitoring Coverage

**Practice:** Instrument enough to debug any issue

**Checklist:**
- [ ] Request latency (p50, p95, p99) by endpoint
- [ ] Error rate by endpoint
- [ ] Database query latency and count
- [ ] Cache hit rate, eviction rate
- [ ] External API call latency and errors
- [ ] Queue depth and processing time
- [ ] Resource usage (CPU, memory, disk, network)
- [ ] Business metrics (orders/sec, revenue/sec, user signups/sec)

**Anti-pattern:** Only monitoring CPU and memory (blind to application issues)

---

### 3.14 Documentation Completeness

**Minimum Documentation:**
1. **Architecture Diagram:** Services, databases, cache, external APIs
2. **Data Flow Diagram:** How requests flow through system
3. **Runbooks:** For every alert
4. **Troubleshooting Guide:** How to debug common issues
5. **API Documentation:** Endpoints, parameters, responses
6. **Deployment Guide:** How to deploy, rollback, scale
7. **Incident Response Process:** How to handle outages
8. **Glossary:** Domain-specific terms

---

### 3.15 Load Test Results

**Practice:** Validate system can handle peak load

**Test Plan:**
1. **Baseline:** Verify system works at 10% of peak load
2. **Ramp Up:** Gradually increase load to peak
3. **Sustained:** Hold peak load for 1 hour
4. **Spike:** Brief 2x peak load, verify recovery
5. **Soak Test:** Run for 24 hours at 80% peak load

**Metrics to Validate:**
- p99 latency doesn't exceed SLO
- Error rate stays < 1%
- No memory leaks (memory stable over 24h)
- Database connections stable
- No cascading failures

**Tools:** Locust, k6, JMeter, Gatling

---

### 3.16 Feature Flag Strategy

**Practice:** Decouple deployment from release

- **Dark Launch:** Feature code deployed but disabled for all users
- **Canary Release:** Enable for 5% of users, monitor
- **Progressive:** 25% → 50% → 100%
- **A/B Testing:** 50/50 split, measure impact
- **Rollback:** Flip flag off, instant rollback (no redeployment)

**Benefits:**
- Fast rollback (seconds vs minutes)
- Risk reduction (test with real users)
- A/B testing capabilities

---

### 3.17 A/B Testing Setup

**Practice:** Measure impact of changes with statistical confidence

**Components:**
1. **Control:** Old version
2. **Treatment:** New version
3. **Random Assignment:** User randomly assigned to control/treatment
4. **Measurement:** Metrics collected for each group
5. **Analysis:** Statistical test (t-test, chi-square)

**Requirements:**
- Consistent assignment (same user → same version always)
- Logging of variant for all events
- Analysis dashboard
- Minimum sample size calculator

---

### 3.18 Post-Launch Monitoring Plan

**First 24 Hours:**
- [ ] Manual monitoring: On-call watches dashboards continuously
- [ ] Alerts responding correctly?
- [ ] Performance as expected?
- [ ] No unexpected errors?

**First Week:**
- [ ] Daily review of metrics vs baseline
- [ ] User reports of issues?
- [ ] Any unexpected load patterns?

**First Month:**
- [ ] Performance stable?
- [ ] SLO being met?
- [ ] Any incidents? Post-mortems completed?
- [ ] Capacity plan adjusted if needed?

---

## 4. Decision Frameworks

**Is this system production-ready?**

Answer these questions:
1. Can you diagnose any issue in < 15 minutes? (Observability)
2. Can you roll back in < 5 minutes? (Rollback plan)
3. Have you load tested to peak? (Performance baseline)
4. Can you handle dependency failure? (Circuit breaker, fallback)
5. Do you know who to page? (On-call setup)
6. Have you documented everything? (Runbooks, architecture)

If all "yes", launch. If any "no", fix it first.

---

## 5. Checklist

- [ ] PRR completed and signed off
- [ ] SLO defined and achievable
- [ ] Load test completed at peak load
- [ ] p99 latency meets SLO
- [ ] Monitoring and alerting deployed
- [ ] Runbooks for all alerts
- [ ] On-call rotation established
- [ ] Incident response plan documented
- [ ] Runbook links in every alert
- [ ] Rollback tested (< 5 minutes)
- [ ] Capacity plan created
- [ ] Security review passed
- [ ] Dependency audit completed
- [ ] Database backup tested
- [ ] Feature flags configured
- [ ] A/B testing setup ready
- [ ] Architecture documented
- [ ] Post-launch monitoring plan
- [ ] Status page configured
- [ ] Customer support briefed

---

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Skipping PRR | Launches unprepared services | Make PRR mandatory |
| No runbooks | MTTR doubles | Automate runbook creation |
| Manual deployments | High error rate, slow rollback | Automate CI/CD |
| Load test too light | Fails under peak load | Test at 150% peak |
| On-call without paging | Delayed response | Use PagerDuty, Opsgenie |
| Runbook has steps but no automation | MTTR high, error-prone | Automate recovery steps |
| Capacity plan ignored | Cascading failures under growth | Review quarterly, adjust |
| No post-mortems | Repeat same mistakes | Conduct blameless post-mortems |

---

## 7. Tools & References

**Deployment:** Terraform, CloudFormation, Helm, Spinnaker
**Monitoring:** Prometheus, Grafana, Datadog, New Relic
**Incident Response:** PagerDuty, Opsgenie, Slack, Incident.io
**Load Testing:** Locust, k6, JMeter, Gatling
**Feature Flags:** LaunchDarkly, Unleash, Split.io
**A/B Testing:** Optimizely, VWO, Statsig
**Documentation:** Confluence, Notion, Markdown + Git
**References:** Google SRE Book (Ch. 2-4, 20), AWS Well-Architected Framework

---

**Completion:** You have completed the RUN TIME domain (5.07 - 5.10)
