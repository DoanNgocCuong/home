# Deployment & CI/CD Best Practices — Production Engineering Essentials

> **Domain:** 5.04 | **Group:** BUILD | **Lifecycle:** Build Time
> **Last Updated:** 2026-03-13
> **Scope:** CI/CD Pipeline Design, Deployment Strategies, Infrastructure Automation

---

## 1. Overview

Continuous Integration and Continuous Deployment (CI/CD) form the backbone of modern production engineering. This domain covers the automated pipelines, deployment strategies, and infrastructure-as-code practices that enable rapid, reliable, and safe releases to production.

**CI/CD Maturity Levels:**
- **Level 1:** Manual builds, manual deployments, unreliable processes
- **Level 2:** Automated builds, manual gate deployments, inconsistent environments
- **Level 3:** Automated builds & tests, semi-automated deployments, environment parity
- **Level 4:** Full automation, self-service deployments, feature flags, instant rollbacks
- **Level 5:** AI-driven optimization, predictive deployments, self-healing pipelines

**Key Goals:**
- Reduce deployment lead time (ideally minutes, not weeks)
- Increase deployment frequency safely (dozens per day)
- Lower change failure rate and MTTR (Mean Time To Recovery)
- Achieve zero-downtime deployments with instant rollback capability

---

## 2. Core Principles

### 2.1 Automation Over Manual Processes
Every manual step is a potential failure point. Automate the entire pipeline from code commit to production monitoring.

### 2.2 Fail Fast, Learn Faster
Short feedback loops (minutes, not hours) enable quick detection and remediation of issues. Build comprehensive testing into every stage.

### 2.3 Infrastructure as Code (IaC)
Treat infrastructure declarations like source code: version controlled, reviewed, tested, and reproducible.

### 2.4 Progressive Delivery
Roll out changes gradually (canary, blue-green) to detect issues before they impact all users.

### 2.5 Immutable Artifacts
Build once, promote the same artifact through environments. No mid-deployment changes.

### 2.6 Observability-Driven Deployments
Every deployment must include monitoring hooks. Cannot deploy safely without visibility.

---

## 3. Best Practices

### 3.1 CI/CD Pipeline Architecture

**Practice: GitHub Actions-Based Pipeline (Example)**

```yaml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test -- --coverage
      - name: Build artifact
        run: npm run build
      - name: Upload to registry
        run: docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: kubectl apply -f k8s/staging.yaml

  deploy-prod:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: kubectl apply -f k8s/prod.yaml
      - name: Run smoke tests
        run: ./scripts/smoke-tests.sh
```

- **What:** Automated pipeline that builds, tests, and deploys on every commit
- **Why:** Eliminates manual steps, enforces consistency, creates audit trail
- **How:** Configure workflow triggers, use environment secrets, implement gates between stages
- **Anti-pattern:** Manual kubectl commands, deploying from local machines, skipping test stages

---

### 3.2 Deployment Strategies

**Practice: Blue-Green Deployment**

Architecture:
```
Load Balancer
    ├─ Blue (Current Production)   [v1.2.0]
    ├─ Green (New Staging)         [v1.3.0]
    └─ Traffic: 100% → Blue

After validation:
    └─ Traffic: 100% → Green (instant switch)
    └─ Rollback: 100% → Blue (instant switch)
```

- **What:** Two identical production environments; traffic switches atomically
- **Why:** Zero-downtime deployments with instant rollback capability
- **How:** Maintain dual infra, validate thoroughly in green before switch, keep both versions running
- **Anti-pattern:** Overlapping deployments, unclear traffic routing, unable to rollback

**Practice: Canary Deployment**

```
Deployment Stages:
1. Deploy v1.3.0 to 5% of traffic (canary group)
2. Monitor error rate, latency, business metrics for 15 minutes
3. If healthy: 25% traffic
4. If healthy: 50% traffic
5. If healthy: 100% traffic (full rollout)
6. If unhealthy at any stage: Rollback to v1.2.0
```

- **What:** Gradual rollout to percentage of users with continuous monitoring
- **Why:** Catches issues affecting only specific user segments before widespread impact
- **How:** Use service mesh (Istio), feature flags, weighted routing; automate metric checks
- **Anti-pattern:** Fixed 5% without metrics-driven decisions, lack of monitoring during canary

**Practice: Rolling Updates (Kubernetes)**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 1 extra pod during update
      maxUnavailable: 0  # Always have 4 pods available
  template:
    spec:
      containers:
      - image: my-app:v1.3.0
```

- **What:** Progressively replace old pods with new version
- **Why:** Maintains availability, distributes load during update
- **How:** Configure maxSurge/maxUnavailable, use readiness probes for pod health
- **Anti-pattern:** maxUnavailable > 0 (breaks availability), insufficient test coverage

---

### 3.3 Feature Flags (Progressive Feature Rollout)

**Practice: LaunchDarkly / Unleash Integration**

```python
# Python example with LaunchDarkly SDK
from ldclient import get_client

client = get_client('sdk-key-prod')

def process_payment(user_id, amount):
    # New payment processor behind feature flag
    if client.variation('use-stripe-v2', {'key': user_id}, False):
        return process_with_stripe_v2(amount)  # New code path
    else:
        return process_with_stripe_v1(amount)  # Legacy code path
```

- **What:** Runtime feature toggles decoupled from deployments
- **Why:** Enable/disable features per user/cohort without redeployment
- **How:** Integrate feature flag SDK, use flag data in decision points, monitor metrics by flag
- **Anti-pattern:** Feature flags left in code permanently, flags not deleted after full rollout

---

### 3.4 Version Control Strategies

**Practice: GitFlow vs Trunk-Based Development**

| Aspect | GitFlow | Trunk-Based |
|--------|---------|-------------|
| Main branches | main, develop, release, hotfix | main only |
| Release cadence | Planned releases (quarterly) | Continuous (daily+) |
| Merges/reviews | Long-lived branches, heavy review | Short-lived branches, fast review |
| Production hotfixes | hotfix branch | Emergency PR to main |
| Best for | Traditional waterfall, regulated industries | DevOps, continuous deployment |

**GitFlow Example (Regulated Environment):**
```
main (v1.2.0) ← Only version-tagged releases
develop (features integrated here)
  ├─ feature/payment-v2 ← 2-week development
  ├─ feature/reporting ← parallel feature
  └─ release/1.3.0 ← 1-week stabilization before prod
```

**Trunk-Based Example (High-Velocity Team):**
```
main (deployable at any commit)
  ├─ feat/payment-v2 (3 days, merged Friday)
  ├─ feat/reporting (2 days, deployed same day)
  └─ (all commits deployable, feature flags control visibility)
```

- **What:** Process for managing code branches and releases
- **Why:** Affects deployment frequency, review overhead, risk tolerance
- **How:** Document strategy in CONTRIBUTING.md, enforce via branch protection rules
- **Anti-pattern:** GitFlow in startup (too slow), Trunk-based without feature flags (premature exposure)

---

### 3.5 Semantic Versioning & Artifact Versioning

**Practice: Semantic Versioning (SemVer)**

Format: `MAJOR.MINOR.PATCH` + pre-release identifiers

```
v1.2.3-rc.1+build.20240113
│ │ │ │   │         └─ Build metadata (not version-ordered)
│ │ │ │   └─ Pre-release (lower priority than release)
│ │ │ └─ PATCH (bug fixes, no API changes)
│ │ └─ MINOR (backward-compatible features)
│ └─ MAJOR (breaking changes)
```

Changelog example:
```
## [1.3.0] - 2026-03-13
### Added
- Payment processor v2 with instant settlement
- Webhook retry logic with exponential backoff

### Changed
- Deprecated old Payment API (will remove in v2.0.0)
- Increased default cache TTL to 5 minutes

### Fixed
- Race condition in concurrent payment processing
- Memory leak in WebSocket listener

### Security
- Updated cryptography to 41.0.7 (CVE-2023-XXXX)
```

- **What:** Standardized versioning scheme (MAJOR.MINOR.PATCH)
- **Why:** Communicates compatibility guarantees to consumers
- **How:** Increment MAJOR on breaking changes, MINOR on features, PATCH on fixes
- **Anti-pattern:** Version numbers without meaning (1.0.0 → 1.0.1 → 2.1.4), unstable major versions

**Container Image Versioning:**
```
registry.example.com/payment-service:
  ├─ v1.3.0 (immutable release tag)
  ├─ 1.3 (points to latest 1.3.x patch)
  ├─ latest (unstable, changes on each build)
  ├─ sha-abc1234 (commit SHA for pinning)
  └─ main-20260313-abc1234 (branch-build combo)
```

---

### 3.6 Docker Image Optimization

**Practice: Multi-Stage Builds**

```dockerfile
# Stage 1: Build dependencies (~800MB)
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install

# Stage 2: Build application
FROM node:18-alpine AS compiler
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production runtime (~50MB)
FROM node:18-alpine AS runtime
WORKDIR /app
RUN apk add --no-cache dumb-init
COPY --from=compiler /app/dist ./dist
COPY --from=compiler /app/node_modules ./node_modules
COPY --from=compiler /app/package.json ./
EXPOSE 3000
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

Final image: **50MB** (vs 800MB with single stage)

- **What:** Use multiple FROM statements to minimize final image size
- **Why:** Faster uploads/downloads, reduced attack surface, cheaper storage
- **How:** Separate build tools (compiler, tests) from runtime, copy only necessities
- **Anti-pattern:** Installing dev dependencies in final stage, large image layers

**Layer Caching Optimization:**
```dockerfile
FROM python:3.11-slim

# Cache invalidation order (rarely-changing to frequently-changing):
COPY requirements.txt .          # Change ~monthly
RUN pip install -r requirements.txt

COPY . .                          # Change per commit
RUN python -m pytest

COPY config.json .               # Change frequently
CMD ["python", "app.py"]
```

---

### 3.7 Container Registry Management

**Practice: Registry Organization & Retention**

```
gcr.io/my-project/
├─ backend/
│  ├─ payment-service:v1.3.0 (2GB, 1 year old) → DELETE
│  ├─ payment-service:v1.4.0 (2GB, 6 months) → KEEP
│  ├─ payment-service:v1.5.0 (2.1GB, prod) → KEEP
│  └─ payment-service:1.5 (symlink to v1.5.0) → KEEP
│
├─ frontend/
│  ├─ web-app:main-20240101 (500MB, 2+ months) → DELETE (use main digest)
│  ├─ web-app:main-20260313 (510MB, today) → KEEP
│  └─ web-app:v2.1.0 (510MB, release) → KEEP
```

- **What:** Policy-based cleanup of old images based on age, tag patterns, usage
- **Why:** Reduce storage costs, speed up deployments, maintain security patch currency
- **How:** Tag consistently (version + branch + timestamp), implement retention policies
- **Anti-pattern:** Keeping all images (storage bloat), tagging with `latest` only

---

### 3.8 Infrastructure as Code (Terraform / Pulumi)

**Practice: Terraform Configuration**

```hcl
# main.tf - Database infrastructure

terraform {
  backend "gcs" {
    bucket = "my-company-tf-state"
    prefix = "prod/database"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_sql_database_instance" "postgres" {
  name             = "prod-payments-db-${var.environment}"
  database_version = "POSTGRES_15"
  deletion_protection = true

  settings {
    tier              = "db-custom-4-16384" # 4 vCPU, 16GB RAM
    availability_type = "REGIONAL"          # HA with failover
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      backup_retention_days          = 30
    }
  }
}

resource "google_sql_database" "app_db" {
  name     = "app_db"
  instance = google_sql_database_instance.postgres.name
}

output "database_url" {
  value       = google_sql_database_instance.postgres.public_ip_address
  sensitive   = false
  description = "Connection endpoint"
}
```

Benefits:
- **Version Control:** Infra changes tracked in Git with pull request reviews
- **Reproducibility:** New staging environment spun up identically in minutes
- **Documentation:** Infrastructure declarations serve as executable docs
- **Auditability:** Change history and who approved what changes

- **What:** Infrastructure defined as code, version-controlled and reviewed like application code
- **Why:** Reproducible environments, audit trail, faster recovery from disasters
- **How:** Version IaC files, test with `terraform plan`, store state securely, enforce code review
- **Anti-pattern:** Infrastructure changes via manual CLI commands, unversioned state files

---

### 3.9 Deployment Rollback Strategies

**Practice: Instant Rollback with Blue-Green**

```bash
# Pre-deployment: verify green environment fully healthy
kubectl rollout status deployment/app-green -n prod

# Deploy new version to green
kubectl set image deployment/app-green \
  app=registry.io/app:v1.3.0 -n prod

# Run smoke tests against green
./scripts/smoke-tests.sh http://green-endpoint

# Switch traffic (instant rollback if needed)
kubectl patch service app \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for 5 minutes
sleep 300 && if [ $ERROR_RATE -gt 0.5% ]; then
  kubectl patch service app \
    -p '{"spec":{"selector":{"version":"blue"}}}'  # Rollback
fi
```

- **What:** Ability to revert to previous version in seconds with zero data loss
- **Why:** Minimize impact when unexpected issues arise in production
- **How:** Maintain previous version running, use atomic traffic switching, automate rollback decisions
- **Anti-pattern:** Killing old version immediately after deploy, manual rollback procedures

---

### 3.10 Zero-Downtime Database Migrations

**Practice: Expand-Contract Pattern**

```sql
-- Step 1: EXPAND (backward compatible, deploy code first)
ALTER TABLE payments ADD COLUMN processor_v2 VARCHAR(50);
ALTER TABLE payments ADD COLUMN processor_v2_processed_at TIMESTAMP;

-- Code update: Write to both old AND new columns
INSERT INTO payments (processor, processor_v2) VALUES ('stripe', 'stripe_v2');

-- Step 2: MIGRATE (backfill historical data)
UPDATE payments SET processor_v2 = processor WHERE processor_v2 IS NULL;

-- Code update: Read from new column, fall back to old if NULL
SELECT processor_v2 COALESCE processor FROM payments WHERE id = ?

-- Step 3: CONTRACT (deploy code that only uses new column)
ALTER TABLE payments DROP COLUMN processor;
```

Migration timeline:
```
Deploy Code v1    (writes to both)
   ↓
Wait 24h + backfill ← Ensures all rows migrated
   ↓
Deploy Code v2    (reads only from new)
   ↓
Drop old column   (no more readers)
```

- **What:** Structured approach to schema changes without downtime
- **Why:** Production databases cannot stop; 99.999% availability requires no locks
- **How:** Use expand-contract, deploy code before schema, verify 100% migration before cleanup
- **Anti-pattern:** Direct column renames with ALTER TABLE ... RENAME, single-step migrations

---

### 3.11 Environment Promotion Strategy

```
Promotion Pipeline:
Local Dev
    ↓ (git push)
PR Environment (ephemeral, 1h)
    ↓ (merge to main)
Staging Environment (persistent, parity with prod)
    ↓ (manual promotion)
Canary (5% of prod)
    ↓ (metric-driven)
Production (100%)
```

**Staging Environment Parity Checklist:**
- [ ] Same Kubernetes version, node types, resource limits
- [ ] Same database version and configuration (read replicas, backup settings)
- [ ] Same external service integrations (payment processor, analytics)
- [ ] Same observability stack (same APM, logging, metrics)
- [ ] Same network policies and firewall rules
- [ ] Same data volumes (1:1 copy of production data if possible)

---

### 3.12 Secret Management in Pipelines

**Practice: Vault-Based Secret Injection**

```yaml
# .github/workflows/deploy.yml

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3

      # Authenticate to Vault, fetch secrets
      - uses: hashicorp/vault-action@v1
        with:
          url: ${{ secrets.VAULT_ADDR }}
          method: jwt
          role: github-actions-prod
          path: jwt
          jwtPayloadAddClaims: true
          secrets: |
            secret/data/prod/database db_password |DB_PASSWORD;
            secret/data/prod/apikeys stripe_key |STRIPE_SECRET_KEY;

      # Secrets available in environment, never logged
      - name: Deploy
        run: |
          kubectl set env deployment/app \
            DB_PASSWORD=$DB_PASSWORD \
            STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
```

Anti-patterns to avoid:
- Hardcoding secrets in Dockerfiles, Git, or CI config files
- Logging environment variables
- Committing `.env` files
- Using GitHub secrets in PR logs (visible to external contributors)

---

### 3.13 Artifact Versioning & Traceability

**Practice: Full Artifact Provenance**

```json
{
  "artifact": "payment-service:v1.3.0",
  "build_timestamp": "2026-03-13T14:23:45Z",
  "git_commit": "abc1234def567890",
  "git_branch": "main",
  "ci_build_id": "github-actions-12345",
  "scanned_by": ["trivy:v0.45.0", "snyk:v1.1250.0"],
  "vulnerabilities": {
    "critical": 0,
    "high": 2,
    "medium": 15
  },
  "test_coverage": 87.3,
  "performance_benchmark": {
    "p95_latency_ms": 245,
    "throughput_rps": 5200
  }
}
```

- **What:** Immutable record of artifact origin, build parameters, quality metrics
- **Why:** Enables traceability for production incidents, compliance audits, rollback decisions
- **How:** Generate during build, embed in image labels, store in artifact registry
- **Anti-pattern:** Artifacts without timestamps, builds without test results

---

### 3.14 Smoke Tests Post-Deployment

**Practice: Automated Health Checks**

```bash
#!/bin/bash
# scripts/smoke-tests.sh - Run immediately after deployment

set -e
ENDPOINT="${1:-https://app.example.com}"
TIMEOUT=300

echo "Running smoke tests against $ENDPOINT..."

# 1. Health check endpoint (< 500ms)
if ! curl -sf "$ENDPOINT/health" -m 2 | grep -q "ok"; then
  echo "FAIL: Health endpoint not responding"
  exit 1
fi

# 2. Critical user flow (payment)
RESPONSE=$(curl -s -X POST "$ENDPOINT/api/v1/payments" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -d '{"amount": 100, "currency": "USD"}')

if echo "$RESPONSE" | grep -q "success"; then
  echo "PASS: Payment flow working"
else
  echo "FAIL: Payment flow broken"
  echo "Response: $RESPONSE"
  exit 1
fi

# 3. Authentication (login/logout)
LOGIN=$(curl -s "$ENDPOINT/api/v1/login" \
  -d "email=test@example.com&password=$TEST_PASSWORD")

if echo "$LOGIN" | jq -e '.token' > /dev/null; then
  echo "PASS: Authentication working"
else
  echo "FAIL: Authentication broken"
  exit 1
fi

# 4. Database connectivity (query latency)
DB_TIME=$(curl -s "$ENDPOINT/api/v1/users/current" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -w '%{time_total}' -o /dev/null)

if (( $(echo "$DB_TIME < 0.5" | bc -l) )); then
  echo "PASS: Database latency acceptable ($DB_TIME s)"
else
  echo "WARN: Elevated database latency ($DB_TIME s)"
fi

echo "All smoke tests passed!"
```

---

## 4. Decision Frameworks

### 4.1 Deployment Strategy Selection

| Requirement | Blue-Green | Canary | Rolling | Manual |
|-----------|-----------|--------|---------|--------|
| Zero downtime | ✓ | ✓ | ✓ | ✗ |
| Instant rollback | ✓ | ✓ | ✗ | ✗ |
| Resource-efficient | ✗ (2x infra) | ✗ (1.5x) | ✓ | ✓ |
| Detects bugs early | ✓ | ✓✓ | ✓ | ✗ |
| Complexity | Medium | High | Medium | Low |
| Best for | Stateless apps | User impact | K8s native | Legacy |

**Decision Tree:**
```
Planning deployment?
├─ Are you using Kubernetes?
│  └─ Use Rolling Updates (native, efficient)
├─ Need instant rollback + can afford 2x infrastructure?
│  └─ Use Blue-Green (safest)
├─ Want to catch issues affecting user subsets?
│  └─ Use Canary (most sophisticated)
└─ Legacy infrastructure, small user base?
   └─ Acceptable to use manual procedures
```

### 4.2 Versioning Strategy Selection

| Context | Strategy | Benefits | Drawbacks |
|---------|----------|----------|-----------|
| SaaS, internal APIs | Trunk-based + feature flags | High velocity, fast feedback | Requires discipline, flag management |
| Library, SDK (public APIs) | GitFlow + SemVer | Clear contracts, stable releases | Slower release cycles |
| Regulated (healthcare, finance) | GitFlow + hotfix branches | Auditability, controlled releases | Complex branching |
| Microservices | Trunk-based + canary | Independent deployments | Harder distributed debugging |

---

## 5. Checklist

### Before Every Production Deployment
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code reviewed and approved
- [ ] Security scan (SAST/DAST) completed, 0 critical vulns
- [ ] Database migrations tested on staging (if applicable)
- [ ] Feature flags configured for new behavior
- [ ] Runbook updated with deployment steps and rollback procedure
- [ ] Monitoring/alerting configured for new metrics
- [ ] Stakeholders (product, customer support) informed of changes
- [ ] Deployment window scheduled (off-peak, if possible)
- [ ] Rollback plan documented and tested

### Post-Deployment Validation
- [ ] Smoke tests passing
- [ ] Error rate unchanged (< expected variance)
- [ ] Latency within SLA (p95, p99)
- [ ] Database queries performing normally
- [ ] External service integrations responding
- [ ] Logging showing expected traffic patterns
- [ ] Business metrics (conversions, revenue) normal
- [ ] Customer support channel quiet (no unusual complaints)
- [ ] Canary/production traffic balanced (if using canary)

### Infrastructure & Environment Parity
- [ ] Production and staging have same Kubernetes versions
- [ ] Same database versions and configurations
- [ ] Same environment variables and secrets injected
- [ ] Same resource requests/limits applied
- [ ] Same network policies, ingress rules configured
- [ ] Same disaster recovery and backup policies

---

## 6. Common Mistakes & Anti-Patterns

### 6.1 "Manual is Faster"
Thinking: "We're small, manual deployments are faster than setting up CI/CD"

Reality: Manual deployments are **slower and riskier**. Human steps introduce:
- Human errors (wrong version, wrong environment)
- Lack of auditability
- Key-person dependencies
- No rollback automation
- Unpredictable timing

**Solution:** Invest 3-5 days in basic GitHub Actions setup. ROI is immediate.

### 6.2 Deploying from Local Machine
Thinking: "I'll deploy directly from my laptop"

Issues:
- Circumvents code review, testing
- No audit trail (who deployed what when?)
- Environmental differences (local secrets != prod)
- Breaks team's shared understanding of current production state

**Solution:** All production deployments go through CI/CD, never kubectl from local machine.

### 6.3 Keeping All Old Container Images
Thinking: "Keep images for quick rollback"

Reality:
- Storage costs explode (enterprise registries charge per GB)
- Slower image pulls due to registry congestion
- Old images carry old vulnerabilities
- Unclear which images are actually in use

**Solution:** Retention policy (keep last 3 releases + last 30 days), use commit SHA tagging for rollback.

### 6.4 Testing Only Happy Path in CI
Thinking: "We test locally, CI is just for build"

Problem: Local machine != CI environment != staging != production

**Solution:** Reproduce production conditions in CI (same database version, same load, same concurrency).

### 6.5 Deploying Untested Migrations
Thinking: "Database changes happen in SQL scripts, not part of testing"

Risk: Schema changes block deployments, data loss, locking entire database

**Solution:** Test migrations on production-scale data, use expand-contract for zero-downtime, automate rollback.

### 6.6 Feature Flags Left Forever
Thinking: "Keep the flag just in case we need to disable it"

Problem:
- Code becomes unreadable with flag checks everywhere
- Old code paths become unmaintained and break
- Flags proliferate, become hard to track
- Undefined behavior when both code paths exist

**Solution:** Remove feature flag code within 2 weeks after full rollout. Clean up flag definitions monthly.

### 6.7 Deploying Without Monitoring
Thinking: "We'll check logs if something breaks"

Reality: By the time you notice logs, users have already noticed the problem.

**Solution:** Deploy WITH monitoring dashboards open, auto-rollback on critical metrics (error rate > 1%, latency > 2σ from baseline).

---

## 7. Tools & References

### CI/CD Platforms
- **GitHub Actions:** GitHub-native, generous free tier, great for open source
- **GitLab CI:** Built-in, excellent for self-hosted, powerful caching
- **Jenkins:** Self-hosted, highly customizable, steeper learning curve
- **CircleCI:** SaaS, strong Docker support, performance insights
- **ArgoCD:** Kubernetes-native, GitOps paradigm, declarative deployments

### Deployment Tools
- **Kubernetes (kubectl):** Industry standard orchestration
- **Helm:** Kubernetes package manager, templating for multi-env
- **Flux:** GitOps for Kubernetes, declarative, auditomated reconciliation
- **Spinnaker:** Multi-cloud deployment orchestration, advanced strategies

### Infrastructure as Code
- **Terraform:** Multi-cloud, HCL language, excellent documentation
- **Pulumi:** Python/Go/TS infrastructure, programmatic approach
- **CloudFormation:** AWS-native, but vendor-locked
- **Ansible:** Imperative, simple YAML, good for configuration management

### Container Registry
- **Docker Hub:** Public, free tier, legacy
- **Google Container Registry (GCR):** Tightly integrated with GCP
- **Amazon Elastic Container Registry (ECR):** Tightly integrated with AWS
- **Azure Container Registry (ACR):** Tightly integrated with Azure

### Secrets Management
- **HashiCorp Vault:** Industry-standard, multi-cloud, sophisticated auth
- **AWS Secrets Manager:** AWS-native, automatic rotation
- **Google Secret Manager:** GCP-native, simple API
- **GitHub Secrets:** Simple but not recommended for multiple repos
- **Sealed Secrets:** Kubernetes-native, encrypts secrets in Git

### Testing & Validation
- **Smoke Testing:** Custom bash/shell scripts (as shown above)
- **Contract Testing (Pact):** Consumer-driven contracts for APIs
- **Load Testing:** Locust (Python), k6 (Go), JMeter (Java)
- **Monitoring:** Datadog, New Relic, Prometheus + Grafana

**References:**
- *Accelerate* by Forsgren et al. — Data-driven DevOps, DORA metrics
- *The DevOps Handbook* — Practical deployment patterns
- Martin Fowler's articles on deployment strategies (bluegreen, canary)
- *The Phoenix Project* — Business impact of deployment practices
- Google SRE Book — Production readiness, deployment safety

---

**Key Takeaway:** Successful production engineering makes deployment safe and frequent. Invest in automation, monitoring, and progressive delivery strategies. Your deployment frequency is directly tied to business agility and customer satisfaction.

---

*For Vietnamese engineers (dành cho kỹ sư Cường):*
- **CI/CD:** Quy trình tích hợp liên tục (Continuous Integration) và triển khai liên tục (Continuous Deployment)
- **Blue-Green:** Hai môi trường giống hệt nhau, chuyển traffic nguyên tử (atomic switch)
- **Canary:** Triển khai dần dần, theo dõi kỹ lưỡng từng bước
- **Feature flags:** Cờ để bật/tắt tính năng mà không cần triển khai lại
- **Infrastructure as Code:** Khai báo infrastructure như mã nguồn, kiểm soát phiên bản
- **Zero-downtime:** Không có thời gian ngừng dịch vụ khi triển khai
