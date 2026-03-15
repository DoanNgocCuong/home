---
name: Full Production Readiness
overview: Checklist toàn diện để đưa service lên production, cover đầy đủ 18 categories từ Production Risk Handbook và Production Quality standards, bao gồm Timeout/Resilience, Security, Testing, CI/CD, DR/Backup, SLO/SLA, Incident Management, và Infrastructure.
todos:
  - id: a1-uvicorn-timeout
    content: "A1: Configure Uvicorn timeout-keep-alive in Dockerfile"
    status: pending
  - id: b1-db-pool-timeout
    content: "B1: Reduce DB_POOL_TIMEOUT from 30s to 10s"
    status: pending
  - id: b2-db-statement-timeout
    content: "B2: Add DB query statement_timeout in database_connection.py"
    status: pending
  - id: b3-db-pool-monitoring
    content: "B3: Monitor DB connection pool usage in health_check_service"
    status: pending
    dependencies:
      - b1-db-pool-timeout
  - id: c1-rabbitmq-timeout
    content: "C1: Add RabbitMQ connection timeout in rabbitmq_publisher"
    status: pending
  - id: c2-rabbitmq-fire-forget
    content: "C2: Make RabbitMQ publish fire-and-forget in endpoint_conversation_events"
    status: pending
  - id: c3-llm-timeout
    content: "C3: Add LLM call timeout with ThreadPoolExecutor"
    status: pending
  - id: d1-llm-backoff
    content: "D1: Add exponential backoff for LLM rate limit with tenacity"
    status: pending
    dependencies:
      - c3-llm-timeout
  - id: d2-llm-fallback
    content: "D2: Verify LLM fallback values return 0 or neutral"
    status: pending
  - id: d3-circuit-breaker
    content: "D3: Verify Circuit Breaker opens after 5 failures"
    status: pending
  - id: e1-google-chat-alerts
    content: "E1: Setup Google Chat alerts for P0 events (DB pool, RabbitMQ)"
    status: pending
    dependencies:
      - b3-db-pool-monitoring
  - id: e2-response-metrics
    content: "E2: Add response time metrics with Prometheus"
    status: pending
  - id: e3-tracing
    content: "E3: Verify Langfuse distributed tracing is configured"
    status: pending
  - id: g1-json-threadpool
    content: "G1: Move CPU-bound JSON parsing to thread pool with asyncio.to_thread"
    status: pending
  - id: g2-conversation-threadpool
    content: "G2: Move conversation formatting to thread pool"
    status: pending
  - id: h1-secret-key
    content: "H1: Validate and enforce SECRET_KEY in config_settings"
    status: pending
  - id: h2-api-auth
    content: "H2: Add API authentication with HTTPBearer"
    status: pending
  - id: h3-input-validation
    content: "H3: Verify Pydantic input validation for all endpoints"
    status: pending
  - id: h4-secrets-mgmt
    content: "H4: Ensure secrets loaded from environment variables only"
    status: pending
  - id: i1-pytest-setup
    content: "I1: Setup pytest infrastructure with directory structure"
    status: pending
  - id: i2-unit-tests
    content: "I2: Write unit tests for critical services (LLM, FriendshipScore, AgentSelection)"
    status: pending
    dependencies:
      - i1-pytest-setup
  - id: i3-integration-tests
    content: "I3: Write integration tests with TestContainers"
    status: pending
    dependencies:
      - i2-unit-tests
  - id: j1-ci-pipeline
    content: "J1: Setup CI pipeline with lint, test, security scan"
    status: pending
    dependencies:
      - i2-unit-tests
  - id: j2-cd-pipeline
    content: "J2: Setup CD pipeline with canary deployment"
    status: pending
    dependencies:
      - j1-ci-pipeline
  - id: k1-db-backup
    content: "K1: Setup automated database backups with script"
    status: pending
  - id: k2-restore-test
    content: "K2: Test restore process monthly"
    status: pending
    dependencies:
      - k1-db-backup
  - id: k3-dr-plan
    content: "K3: Document DR plan with RTO/RPO"
    status: pending
  - id: l1-sli-definition
    content: "L1: Define Service Level Indicators (Availability, Latency, Error Rate)"
    status: pending
  - id: l2-slo-definition
    content: "L2: Define Service Level Objectives with error budget"
    status: pending
    dependencies:
      - l1-sli-definition
  - id: l3-slo-monitoring
    content: "L3: Implement SLO monitoring with Prometheus"
    status: pending
    dependencies:
      - l2-slo-definition
  - id: m1-oncall-rotation
    content: "M1: Establish on-call rotation schedule"
    status: pending
  - id: m2-runbooks
    content: "M2: Create runbooks for top 5 common incidents"
    status: pending
  - id: m3-incident-response
    content: "M3: Define incident response process with severity levels"
    status: pending
  - id: n1-env-example
    content: "N1: Create .env.example file with all required variables"
    status: pending
  - id: n2-secrets-rotation
    content: "N2: Implement secrets rotation script"
    status: pending
  - id: o1-error-schema
    content: "O1: Standardize error response schema across all endpoints"
    status: pending
  - id: o2-api-versioning
    content: "O2: Implement API versioning with /api/v1 prefix"
    status: pending
  - id: o3-openapi-export
    content: "O3: Export OpenAPI spec and enable Swagger UI in dev"
    status: pending
  - id: o4-pagination
    content: "O4: Add pagination for list endpoints"
    status: pending
  - id: p1-docker-hardening
    content: "P1: Docker hardening with non-root user and multi-stage build"
    status: pending
  - id: p2-k8s-probes
    content: "P2: Kubernetes deployment with readiness and liveness probes"
    status: pending
  - id: q1-lint-format
    content: "Q1: Setup linting and formatting with ruff, black, mypy"
    status: pending
  - id: q2-precommit
    content: "Q2: Setup pre-commit hooks"
    status: pending
    dependencies:
      - q1-lint-format
  - id: q3-coverage
    content: "Q3: Enforce code coverage > 70% in CI"
    status: pending
    dependencies:
      - i2-unit-tests
  - id: r1-debt-doc
    content: "R1: Document known technical debt in docs/technical_debt.md"
    status: pending
  - id: r2-debt-metrics
    content: "R2: Track debt metrics with SonarQube"
    status: pending
    dependencies:
      - r1-debt-doc
  - id: f1-optimize-queries
    content: "F1: Optimize DB queries in activities/suggest with batch loading"
    status: pending
  - id: f2-db-indexes
    content: "F2: Add database indexes for PromptTemplate"
    status: pending
---

Link: D:\GIT\context-handling-bigmodule_PikaRobot_25112025\docs\4_TimeOut_Fallback_Alert\P3_Plan2_full_production_readiness_368a62a1.plan copy.md

# Full Production Readiness Checklist

## Tổng quan

Plan này mở rộng từ "Timeout & Resilience" thành **Full Production Readiness Checklist**, cover đầy đủ các rủi ro production từ 2 tài liệu:

- [docs/3_TaiLieuProductionQuality_11122025/template/2.0_PRODUCT_QUALITY.md](docs/3_TaiLieuProductionQuality_11122025/template/2.0_PRODUCT_QUALITY.md)
- [docs/3_TaiLieuProductionQuality_11122025/template/PRODUCTION_RISK_ALL_IN_ONE_HANDBOOK.md](docs/3_TaiLieuProductionQuality_11122025/template/PRODUCTION_RISK_ALL_IN_ONE_HANDBOOK.md)

**Thời gian ước tính:** 2-3 tuần (phân chia theo priority)---

## MECE Framework - 18 Categories

Checklist được phân loại theo **18 categories** đảm bảo **Mutually Exclusive** và **Collectively Exhaustive**:

### LAYER 1: IMMEDIATE SURVIVAL (P0 - 24-48h)

- **Category A:** Application Server Timeout
- **Category B:** Database Resilience
- **Category C:** External Services Resilience
- **Category H:** Security Basics (Critical only)

### LAYER 2: OPERATIONAL RESILIENCE (P1 - 1 tuần)

- **Category D:** Fallback & Recovery
- **Category E:** Observability & Alerting
- **Category G:** CPU-Bound Operations Management
- **Category I:** Testing Strategies (Basics)
- **Category K:** Disaster Recovery & Backup (Basics)
- **Category L:** SLO/SLI/SLA (Definition)

### LAYER 3: PRODUCTION EXCELLENCE (P2 - 2-3 tuần)

- **Category F:** Performance Optimization
- **Category J:** CI/CD Pipeline
- **Category M:** Incident Management & On-Call
- **Category N:** Configuration Management
- **Category O:** API Design & Documentation
- **Category P:** Infrastructure & Containerization
- **Category Q:** Code Quality
- **Category R:** Technical Debt Management

---

## CATEGORY A: APPLICATION SERVER TIMEOUT (P0)

**Status:** Not implemented**Files:** [`src/Dockerfile`](src/Dockerfile)

### A1: Configure Uvicorn timeout-keep-alive

```dockerfile
CMD ["uvicorn", "app.main_app:app", \
     "--host", "0.0.0.0", \
     "--port", "30020", \
     "--timeout-keep-alive", "55", \
     "--timeout-graceful-shutdown", "10"]
```

**Verification:** Kill client connection → Server tự đóng connection sau 55s---

## CATEGORY B: DATABASE RESILIENCE (P0)

**Status:** Partially implemented**Files:** [`src/app/core/config_settings.py`](src/app/core/config_settings.py), [`src/app/db/database_connection.py`](src/app/db/database_connection.py)

### B1: Reduce DB_POOL_TIMEOUT from 30s to 10s

```python
# config_settings.py
DB_POOL_TIMEOUT: int = 10  # Change from 30
```



### B2: Add DB query statement_timeout

```python
# database_connection.py
engine = create_engine(
    settings.DATABASE_URL,
    # ... existing ...
    connect_args={"options": "-c statement_timeout=10000"}  # 10s
)
```



### B3: Monitor DB connection pool usage

```python
# health_check_service.py
pool = db.bind.pool
if pool.checkedout() + pool.overflow() > pool.size() * 0.8:
    logger.warning("DB pool nearly exhausted")
    send_alert()
```

**Verification:** Request fails after 10s when pool exhausted---

## CATEGORY C: EXTERNAL SERVICES RESILIENCE (P0)

**Status:** Partially implemented**Files:** [`src/app/background/rabbitmq_publisher.py`](src/app/background/rabbitmq_publisher.py), [`src/app/api/v1/endpoints/endpoint_conversation_events.py`](src/app/api/v1/endpoints/endpoint_conversation_events.py), [`src/app/services/utils/llm_analysis_utils.py`](src/app/services/utils/llm_analysis_utils.py)

### C1: Add RabbitMQ connection timeout

```python
# rabbitmq_publisher.py
self.connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        socket_timeout=5,
        blocked_connection_timeout=5
    )
)
```



### C2: Make RabbitMQ publish fire-and-forget

```python
# endpoint_conversation_events.py
asyncio.create_task(publish_conversation_event(...))
```



### C3: Add LLM call timeout

```python
# llm_analysis_utils.py
with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(self.client.chat.completions.create, ...)
    response = future.result(timeout=15)
```

**Verification:** API returns 202 immediately even if RabbitMQ down; LLM timeout after 15s---

## CATEGORY D: FALLBACK & RECOVERY (P1)

**Status:** Partially implemented**Files:** [`src/app/services/utils/llm_analysis_utils.py`](src/app/services/utils/llm_analysis_utils.py)

### D1: Add exponential backoff for LLM rate limit

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def _invoke_llm(self, ...):
    # ... existing code ...
```

**Dependencies:** `pip install tenacity`

### D2: Verify LLM fallback values

Ensure existing fallback logic returns `0` or `"neutral"` on error.

### D3: Verify Circuit Breaker is working

Test: 5 consecutive failures → Circuit opens → Fallback to default**Verification:** Rate limit 429 → Retry with backoff 2s, 4s, 8s---

## CATEGORY E: OBSERVABILITY & ALERTING (P1)

**Status:** Partially implemented**Files:** [`src/app/main_app.py`](src/app/main_app.py), [`src/app/utils/alerts/alert_manager.py`](src/app/utils/alerts/alert_manager.py)

### E1: Setup Google Chat alerts for P0 events

```python
# health_check_service.py
from app.utils.alerts.alert_manager import get_alert_manager

if pool_exhausted:
    alert_manager = get_alert_manager()
    alert_manager.send_alert_fire_and_forget(
        alert_type=AlertType.SYSTEM_ERROR,
        level=AlertLevel.CRITICAL,
        message="Database connection pool exhausted"
    )
```



### E2: Add response time metrics

```python
# main_app.py
from prometheus_client import Histogram

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'path', 'status']
)

# In RequestLoggingMiddleware:
request_duration.labels(method, path, status).observe(process_time)
if process_time > 5.0:
    logger.warning(f"Slow request: {method} {path} took {process_time:.2f}s")
```

**Dependencies:** `pip install prometheus-client`

### E3: Setup distributed tracing

Verify `LANGFUSE_ENABLED`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` are configured.**Verification:** Metrics endpoint `/metrics` shows request duration; Google Chat alert when pool > 80%---

## CATEGORY F: PERFORMANCE OPTIMIZATION (P2)

**Status:** Not implemented**Files:** [`src/app/services/agent_selection/agent_selection_service.py`](src/app/services/agent_selection/agent_selection_service.py)

### F1: Optimize DB queries in `/activities/suggest`

Batch load all prompts in one query instead of multiple queries, build lookup dict for O(1) access.

### F2: Add database indexes

```sql
CREATE INDEX IF NOT EXISTS idx_prompt_template_friendship_level 
ON prompt_template_for_level_friendship(friendship_level);

CREATE INDEX IF NOT EXISTS idx_prompt_template_agent_category 
ON prompt_template_for_level_friendship(agent_category);
```

**Verification:** Reduce DB queries from ~10 to ~2-3; Response time reduced by 30-50%---

## CATEGORY G: CPU-BOUND OPERATIONS MANAGEMENT (P1)

**Status:** Not implemented**Files:** [`src/app/api/v1/endpoints/endpoint_conversation_events.py`](src/app/api/v1/endpoints/endpoint_conversation_events.py), [`src/app/services/utils/llm_analysis_utils.py`](src/app/services/utils/llm_analysis_utils.py)

### G1: Move CPU-bound JSON parsing to thread pool

```python
import asyncio

async def parse_large_json(json_str: str) -> dict:
    return await asyncio.to_thread(json.loads, json_str)
```



### G2: Move conversation formatting to thread pool

```python
async def format_conversation_async(conversation_log: List[Dict]) -> str:
    return await asyncio.to_thread(format_conversation_for_llm, conversation_log)
```

**Verification:** Large JSON/conversation formatting không block event loop---

## CATEGORY H: SECURITY & ACCESS CONTROL (P0 + P1)

**Status:** Not implemented**Files:** [`src/app/main_app.py`](src/app/main_app.py), [`src/app/core/config_settings.py`](src/app/core/config_settings.py)

### H1: Validate và enforce SECRET_KEY (P0)

```python
# config_settings.py
SECRET_KEY: str = Field(..., min_length=32)

if SECRET_KEY == "default_secret_key_change_in_production":
    raise ValueError("SECRET_KEY must be changed for production")
```



### H2: Add API authentication (P1)

```python
# main_app.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path.startswith("/api"):
        auth = request.headers.get("Authorization")
        if not auth or not verify_token(auth):
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return await call_next(request)
```



### H3: Input validation & sanitization (P1)

Verify Pydantic models validate all user input. Add custom validators for sensitive fields.

### H4: Secrets management (P1)

```python
# Use environment variables, never hardcode
GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
RABBITMQ_PASSWORD: str = Field(..., env="RABBITMQ_PASSWORD")
```

**Verification:** SECRET_KEY validation fails on startup if default; API returns 401 without valid token---

## CATEGORY I: TESTING STRATEGIES (P1)

**Status:** Not implemented**Files:** New directory `src/tests/`

### I1: Setup pytest infrastructure (P1)

```bash
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```

Create directory structure:

```javascript
src/tests/
├── unit/              # 70% of tests
├── integration/       # 20% of tests
├── e2e/               # 10% of tests
├── fixtures/
└── conftest.py
```



### I2: Write unit tests for critical services (P1)

Priority services to test:

- [`src/app/services/friendship_score_calculation_service.py`](src/app/services/friendship_score_calculation_service.py)
- [`src/app/services/agent_selection/agent_selection_service.py`](src/app/services/agent_selection/agent_selection_service.py)
- [`src/app/services/utils/llm_analysis_utils.py`](src/app/services/utils/llm_analysis_utils.py)
```python
# tests/unit/test_llm_analysis_utils.py
import pytest
from unittest.mock import Mock, patch

def test_analyze_user_questions_success():
    # ... mock LLM response ...
    result = analyzer.analyze_user_questions(formatted_conversation)
    assert result == 3

def test_analyze_user_questions_timeout():
    # ... mock timeout ...
    result = analyzer.analyze_user_questions(formatted_conversation)
    assert result == 0  # Fallback value
```




### I3: Write integration tests (P2)

```python
# tests/integration/test_conversation_events_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def test_db():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres.get_connection_url()

def test_create_conversation_event_success(test_client, test_db):
    response = test_client.post("/v1/conversations/end", json={...})
    assert response.status_code == 201
```

**Dependencies:** `pip install pytest pytest-asyncio pytest-mock testcontainers`**Verification:** `pytest` runs successfully; Coverage > 70% for critical modules---

## CATEGORY J: CI/CD PIPELINE (P2)

**Status:** Not implemented**Files:** New file `.github/workflows/ci.yml` (hoặc `.gitlab-ci.yml`)

### J1: Setup CI pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
            - uses: actions/checkout@v3
            - name: Run ruff
        run: ruff check src/
            - name: Run black
        run: black --check src/
            - name: Run mypy
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    steps:
            - uses: actions/checkout@v3
            - name: Run pytest
        run: pytest --cov=app --cov-report=xml
            - name: Upload coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
            - uses: actions/checkout@v3
            - name: Run Bandit (SAST)
        run: bandit -r src/
            - name: Run Safety (dependency scan)
        run: safety check
            - name: Run Trivy (secrets scan)
        run: trivy fs .

  build:
    runs-on: ubuntu-latest
    steps:
            - uses: actions/checkout@v3
            - name: Build Docker image
        run: docker build -t context-handling:${{ github.sha }} .
            - name: Push to registry
        run: docker push context-handling:${{ github.sha }}
```



### J2: Setup CD pipeline

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
            - name: Deploy to staging
        run: kubectl set image deployment/context-handling context-handling=context-handling:${{ github.sha }} -n staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
            - name: Deploy canary (10%)
        run: kubectl set image deployment/context-handling-canary context-handling=context-handling:${{ github.sha }} -n production
            - name: Wait 10min
        run: sleep 600
            - name: Check metrics
        run: |
          ERROR_RATE=$(curl -s prometheus/query?query=error_rate)
          if [ $ERROR_RATE > 0.05 ]; then
            echo "High error rate, rolling back"
            exit 1
          fi
            - name: Deploy full (100%)
        run: kubectl set image deployment/context-handling context-handling=context-handling:${{ github.sha }} -n production
```

**Dependencies:** GitHub Actions hoặc GitLab CI, Kubernetes cluster**Verification:** Pipeline runs on every commit; Automated deployment to staging; Canary deployment to production---

## CATEGORY K: DISASTER RECOVERY & BACKUP (P1)

**Status:** Not implemented**Files:** New scripts in `scripts/backup/`

### K1: Setup automated database backups (P1)

```bash
# scripts/backup/backup_db.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
DATABASE_URL=$DATABASE_URL

pg_dump $DATABASE_URL | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep last 30 daily backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# Upload to S3 (3-2-1 rule: offsite backup)
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://my-bucket/backups/
```

Schedule with cron:

```cron
0 2 * * * /app/scripts/backup/backup_db.sh
```



### K2: Test restore process (P1)

```bash
# scripts/backup/restore_db.sh
#!/bin/bash
BACKUP_FILE=$1

gunzip -c $BACKUP_FILE | psql $DATABASE_URL
```



### K3: Document DR plan (P1)

Create `docs/disaster_recovery_plan.md`:

- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 24 hours
- Backup retention: 30 days
- Restore procedures
- Contact list

**Verification:** Daily automated backups; Restore tested monthly; DR plan documented---

## CATEGORY L: SLO/SLI/SLA (P1)

**Status:** Not implemented**Files:** New file `docs/slo_sla.md`

### L1: Define Service Level Indicators (SLI) (P1)

```markdown
# SLIs for Context Handling Service

| SLI                 | Measurement                          | Target |
|---------------------|--------------------------------------|--------|
| Availability        | % of successful requests             | 99.5%  |
| Latency (P50)       | Median response time                 | < 200ms|
| Latency (P99)       | 99th percentile response time        | < 2s   |
| Error Rate          | % of 5xx responses                   | < 1%   |
| Throughput          | Requests per second                  | > 100  |
```



### L2: Define Service Level Objectives (SLO) (P1)

```markdown
# SLOs for Context Handling Service

- **Availability SLO:** 99.5% uptime over 30-day rolling window
- **Latency SLO:** P99 latency < 2 seconds for all API endpoints
- **Error Rate SLO:** < 1% error rate over 7-day rolling window

**Error Budget:**
- Monthly error budget: 0.5% * 30 days * 24 hours = 3.6 hours
```



### L3: Implement SLO monitoring (P2)

```python
# main_app.py
from prometheus_client import Gauge

slo_availability = Gauge('slo_availability_percent', 'Current availability %')
slo_error_budget = Gauge('slo_error_budget_remaining_hours', 'Remaining error budget in hours')

# Calculate in background task
async def calculate_slo():
    while True:
        availability = calculate_availability_last_30_days()
        slo_availability.set(availability)
        
        error_budget_remaining = calculate_error_budget_remaining()
        slo_error_budget.set(error_budget_remaining)
        
        await asyncio.sleep(300)  # Every 5 minutes
```

**Verification:** SLIs/SLOs documented; Metrics tracked in Prometheus; Alerts when error budget < 20%---

## CATEGORY M: INCIDENT MANAGEMENT & ON-CALL (P2)

**Status:** Not implemented**Files:** New files in `docs/runbooks/`

### M1: Establish on-call rotation (P2)

```markdown
# docs/oncall_rotation.md

## On-call Schedule

- **Primary On-call:** Rotates weekly (Mon-Sun)
- **Secondary On-call:** Backup for primary
- **Escalation timeout:** 5 minutes

## Current Rotation

| Week        | Primary   | Secondary |
|-------------|-----------|-----------|
| Dec 23-29   | Engineer A| Engineer B|
| Dec 30-Jan 5| Engineer B| Engineer C|
```



### M2: Create runbooks for common incidents (P2)

```markdown
# docs/runbooks/high_latency.md

## Runbook: High Latency Alert

**Trigger:** P99 latency > 5 seconds for 5 minutes

**Diagnosis Steps:**
1. Check Grafana dashboard: [link]
2. Verify DB pool usage: `psql -c "SELECT * FROM pg_stat_activity"`
3. Check RabbitMQ queue depth: `rabbitmqctl list_queues`
4. Check LLM circuit breaker status: [logs]

**Remediation:**
- If DB pool exhausted: Restart application to reset pool
- If RabbitMQ queue backlog: Scale workers: `docker-compose up --scale worker=5`
- If LLM circuit open: Wait 60s for recovery, or manually close: [command]

**Escalation:**
- If not resolved in 15 minutes, escalate to Secondary On-call
- If critical (affecting > 50% users), escalate to Engineering Manager
```



### M3: Define incident response process (P2)

```markdown
# docs/incident_response.md

## Incident Severity Levels

| Level | Definition                          | Response Time | Example                |
|-------|-------------------------------------|---------------|------------------------|
| P0    | Complete outage, all users affected | < 15 minutes  | Service down           |
| P1    | Major degradation, > 50% users      | < 30 minutes  | High error rate        |
| P2    | Minor degradation, < 10% users      | < 1 hour      | Slow response time     |
| P3    | No user impact                      | Next business day | Log errors         |

## Incident Flow

1. **Detect:** Alert triggers
2. **Acknowledge:** On-call acknowledges within 5 minutes
3. **Diagnose:** Follow runbook
4. **Mitigate:** Apply remediation
5. **Communicate:** Update status page
6. **Resolve:** Confirm fix
7. **Post-mortem:** Write RCA within 48 hours
```

**Verification:** On-call rotation established; Runbooks for top 5 incidents; Incident response process documented---

## CATEGORY N: CONFIGURATION MANAGEMENT (P2)

**Status:** Partially implemented**Files:** [`src/app/core/config_settings.py`](src/app/core/config_settings.py), [`src/.env.example`](src/.env.example)

### N1: Create `.env.example` file (P2)

```bash
# .env.example
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<CHANGE_THIS_IN_PRODUCTION>

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=100
DB_POOL_TIMEOUT=10

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=<CHANGE_THIS>

# External APIs
GROQ_API_KEY=<YOUR_API_KEY>
MEMORY_API_KEY=<YOUR_API_KEY>

# Alerts
GOOGLE_CHAT_WEBHOOK_URL=<YOUR_WEBHOOK_URL>
```



### N2: Implement secrets rotation (P2)

```python
# scripts/rotate_secrets.py
import boto3
from datetime import datetime

def rotate_secret(secret_name):
    """Rotate secret in AWS Secrets Manager"""
    client = boto3.client('secretsmanager')
    
    # Generate new secret
    response = client.rotate_secret(
        SecretId=secret_name,
        RotationLambdaARN='arn:aws:lambda:...',
        RotationRules={'AutomaticallyAfterDays': 30}
    )
    
    print(f"Secret {secret_name} rotated at {datetime.now()}")

if __name__ == "__main__":
    rotate_secret("context-handling/groq-api-key")
    rotate_secret("context-handling/rabbitmq-password")
```

**Verification:** `.env.example` documented; Secrets rotation automated monthly---

## CATEGORY O: API DESIGN & DOCUMENTATION (P2)

**Status:** Partially implemented**Files:** [`src/app/main_app.py`](src/app/main_app.py), [`src/app/api/v1/`](src/app/api/v1/)

### O1: Standardize error response schema (P2)

```python
# schemas/error_schema.py
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    error_code: str           # e.g., "DB_CONNECTION_FAILED"
    message: str              # Human-readable message
    details: Optional[dict]   # Additional context
    timestamp: str
    request_id: str

# In endpoints:
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message=str(exc),
            timestamp=datetime.now().isoformat(),
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )
```



### O2: Implement API versioning (P2)

```python
# main_app.py
app.include_router(router_v1, prefix="/api/v1")
# Future: app.include_router(router_v2, prefix="/api/v2")
```



### O3: Export OpenAPI spec (P2)

```python
# main_app.py
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()
```

Enable Swagger UI in development:

```python
if settings.DEBUG:
    app.docs_url = "/docs"
    app.redoc_url = "/redoc"
else:
    app.docs_url = None  # Disable in production
```



### O4: Add pagination for list endpoints (P2)

```python
# schemas/pagination.py
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

# In endpoint:
@router.get("/activities")
async def list_activities(pagination: PaginationParams = Depends()):
    offset = (pagination.page - 1) * pagination.page_size
    items = repository.get_all(limit=pagination.page_size, offset=offset)
    total = repository.count()
    
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "page_size": pagination.page_size,
        "total_pages": (total + pagination.page_size - 1) // pagination.page_size
    }
```

**Verification:** Error responses follow standard schema; API versioned at `/api/v1`; OpenAPI spec exported; Pagination implemented---

## CATEGORY P: INFRASTRUCTURE & CONTAINERIZATION (P2)

**Status:** Partially implemented**Files:** [`src/Dockerfile`](src/Dockerfile), `k8s/deployment.yaml` (new)

### P1: Docker hardening (P2)

```dockerfile
# Dockerfile (multi-stage build)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry export -f requirements.txt > requirements.txt

FROM python:3.11-slim
# Create non-root user
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Copy dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:30020/v1/health')"

CMD ["uvicorn", "app.main_app:app", "--host", "0.0.0.0", "--port", "30020"]
```



### P2: Kubernetes deployment with probes (P2)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: context-handling
spec:
  replicas: 3
  selector:
    matchLabels:
      app: context-handling
  template:
    metadata:
      labels:
        app: context-handling
    spec:
      containers:
            - name: context-handling
        image: context-handling:latest
        ports:
                - containerPort: 30020
        
        # Resource limits
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        
        # Readiness probe (when to start receiving traffic)
        readinessProbe:
          httpGet:
            path: /v1/health
            port: 30020
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3
        
        # Liveness probe (when to restart container)
        livenessProbe:
          httpGet:
            path: /v1/health
            port: 30020
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
        
        # Environment variables from ConfigMap/Secrets
        envFrom:
                - configMapRef:
            name: context-handling-config
                - secretRef:
            name: context-handling-secrets
```

**Verification:** Docker image runs as non-root; Health check passes; Kubernetes pods restart on liveness failure---

## CATEGORY Q: CODE QUALITY (P2)

**Status:** Not implemented**Files:** New files `pyproject.toml`, `.pre-commit-config.yaml`

### Q1: Setup linting & formatting (P2)

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
select = ["E", "F", "W", "I", "N"]
ignore = ["E501"]

[tool.black]
line-length = 120

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```



### Q2: Setup pre-commit hooks (P2)

```yaml
# .pre-commit-config.yaml
repos:
    - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
            - id: black
  
    - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
            - id: ruff
  
    - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
            - id: mypy
        additional_dependencies: [types-requests]
```

Install: `pre-commit install`

### Q3: Enforce code coverage (P2)

```yaml
# .github/workflows/ci.yml
- name: Check coverage
  run: |
    pytest --cov=app --cov-report=term --cov-fail-under=70
```

**Verification:** Linting passes; Formatting applied; Type checking passes; Coverage > 70%---

## CATEGORY R: TECHNICAL DEBT MANAGEMENT (P2)

**Status:** Not implemented**Files:** New file `docs/technical_debt.md`

### R1: Document known technical debt (P2)

```markdown
# docs/technical_debt.md

## Technical Debt Inventory

| ID    | Description                          | Impact | Effort | Priority |
|-------|--------------------------------------|--------|--------|----------|
| TD-001| Blocking LLM calls (not async)       | High   | Medium | P1       |
| TD-002| No caching for prompt templates      | Medium | Low    | P2       |
| TD-003| Agent selection logic too complex    | Medium | High   | P2       |
| TD-004| Missing type hints in old code       | Low    | Low    | P3       |

## Debt Reduction Plan

- **Q1 2025:** Fix TD-001 (async LLM calls)
- **Q2 2025:** Fix TD-002 (caching)
- **Allocate 20% of sprint capacity for debt reduction**
```



### R2: Track debt metrics (P2)

```yaml
# SonarQube analysis
sonar-scanner \
  -Dsonar.projectKey=context-handling \
  -Dsonar.sources=src/ \
  -Dsonar.host.url=http://sonarqube:9000
```

**Verification:** Technical debt documented; Debt reduction plan established; Metrics tracked---

## IMPLEMENTATION TIMELINE

### Week 1 (P0 - Critical):

- Category A: Application Server Timeout
- Category B: Database Resilience
- Category C: External Services Resilience (partial)
- Category H: Security Basics (SECRET_KEY validation)

### Week 2 (P1 - High):

- Category C: External Services (LLM timeout)
- Category D: Fallback & Recovery
- Category E: Observability & Alerting
- Category G: CPU-Bound Operations
- Category I: Testing Basics (setup + unit tests)
- Category K: Backup Basics
- Category L: SLO/SLI Definition

### Week 3 (P2 - Medium):

- Category F: Performance Optimization
- Category J: CI/CD Pipeline
- Category M: Incident Management
- Category N: Configuration Management
- Category O: API Design
- Category P: Infrastructure
- Category Q: Code Quality
- Category R: Technical Debt

---

## DEPENDENCIES

```bash
# Required packages
pip install tenacity prometheus-client pytest pytest-asyncio pytest-mock testcontainers

# Optional (for CI/CD)
pip install black ruff mypy bandit safety pre-commit
```

---

## VERIFICATION CHECKLIST

### Immediate (P0):

- [ ] API returns 202 immediately even if RabbitMQ down
- [ ] Request fails after 10s when DB pool exhausted
- [ ] SECRET_KEY validation fails if default

### Week 1 (P1):

- [ ] LLM timeout after 15s with fallback
- [ ] Google Chat alert when pool > 80%
- [ ] Large JSON parsing không block event loop
- [ ] pytest runs successfully with > 70% coverage
- [ ] Daily automated DB backups
- [ ] SLIs/SLOs documented

### Week 2-3 (P2):

- [ ] CI pipeline runs on every commit
- [ ] Canary deployment to production
- [ ] On-call rotation established
- [ ] Runbooks for top 5 incidents
- [ ] Error responses follow standard schema
- [ ] Docker image runs as non-root
- [ ] Linting passes in CI

---

## MONITORING DASHBOARD

Key metrics to track in Grafana:

```promql
# Availability
rate(http_request_total{status=~"2xx|3xx"}[5m]) / rate(http_request_total[5m])

# Latency P99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Error Rate
rate(http_request_total{status=~"5xx"}[5m]) / rate(http_request_total[5m])

# DB Pool Usage
db_connection_pool_checkedout / db_connection_pool_size

# RabbitMQ Queue Depth
rabbitmq_queue_messages{queue="conversation_events"}
```

---