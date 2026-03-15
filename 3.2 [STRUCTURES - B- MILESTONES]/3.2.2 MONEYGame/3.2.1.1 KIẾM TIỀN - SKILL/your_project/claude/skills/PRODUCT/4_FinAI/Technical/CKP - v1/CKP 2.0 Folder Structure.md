
# 6 Modules Quick Reference Guide
## Comet AI Browser - MVP Enterprise Architecture

---

## 📦 Module Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│ USER INPUT (Text, URL, Page Context)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────▼───────────────┐
        │  STAGE 1: UnifiedInputCore     │
        │  ├─ Validate input             │
        │  ├─ Normalize text             │
        │  ├─ Extract URLs               │
        │  ├─ Detect language            │
        │  ├─ Safety precheck            │
        │  └─ Attach context             │
        └────────────────┬────────────────┘
                         │
                    NormalizedInput
                         │
        ┌────────────────▼──────────────────┐
        │  STAGE 2: QueryUnderstanding      │
        │  ├─ Intent classification         │
        │  ├─ Slot filling                 │
        │  ├─ Entity extraction            │
        │  ├─ Policy checks (PII/injection)│
        │  ├─ SLM fallback (optional)      │
        │  └─ Task specification           │
        └────────────────┬──────────────────┘
                         │
                      TaskSpecV1
                         │
        ┌────────────────▼───────────────┐
        │  STAGE 3: RouterPlanner        │
        │  ├─ Extract signals            │
        │  ├─ Select mode (A/B/C/D)     │
        │  ├─ Generate ActionPlan        │
        │  ├─ Validate constraints       │
        │  ├─ Budget management          │
        │  └─ State persistence          │
        └────────────────┬───────────────┘
                         │
                     ActionPlan
                         │
        ┌────────────────▼──────────────────┐
        │  STAGE 4: UnifiedExecutor (4 Modes)
        │                                   │
        │  ┌─ 4.1 Retrieve:                │
        │  │   Hybrid search (BM25+Vector) │
        │  │   Rerank & dedupe             │
        │  │                               │
        │  ├─ 4.2 FetchData:               │
        │  │   HTTP fetch (SSRF guard)     │
        │  │   Parse tables & metadata     │
        │  │                               │
        │  ├─ 4.3 Compute:                 │
        │  │   Score & transform data      │
        │  │   Reasoning (no UI actions)   │
        │  │                               │
        │  └─ 4.4 Act:                     │
        │      Headless browser            │
        │      Click/type/fill (no submit) │
        │      Policy gates & approval     │
        │      Receipt generation          │
        │                                   │
        └────────────────┬──────────────────┘
                         │
               EvidencePack + Receipt
                         │
        ┌────────────────▼──────────────────┐
        │  STAGE 5: Reasoning               │
        │  ├─ Compress evidence            │
        │  ├─ Extract atomic claims        │
        │  ├─ Map citations                │
        │  ├─ Resolve contradictions       │
        │  ├─ Safety validation            │
        │  └─ Open questions               │
        └────────────────┬──────────────────┘
                         │
         AnswerSkeleton + CitationMap
                         │
        ┌────────────────▼──────────────────┐
        │  STAGE 6: AnswerSynthesis         │
        │  ├─ Compose final answer         │
        │  ├─ Insert citations             │
        │  ├─ Personalize format           │
        │  ├─ Post-process (redact, etc)   │
        │  ├─ Safety check                 │
        │  └─ Package response             │
        └────────────────┬──────────────────┘
                         │
                    FinalAnswer
                         │
        ┌────────────────▼──────────────────┐
        │ USER RESPONSE (Markdown + Citations)
        └───────────────────────────────────┘
```

---

## 🎯 Each Module's Responsibility

### Stage 1: UnifiedInputCore
**Input**: RawRequest (text, URL, page context)  
**Output**: NormalizedInput (validated, normalized)  
**Key Modules**:
- `InputAdapter` - Schema validation, idempotency
- `ContextCollector` - Gather browser context
- `Normalizer` - Whitespace, language detection
- `SafetyPrecheck` - Block obvious injection/SSRF

**Latency Target**: <200ms (p95)

---

### Stage 2: QueryUnderstanding
**Input**: NormalizedInput  
**Output**: TaskSpecV1 (intent, slots, constraints)  
**Key Modules**:
- `RuleEngine` - Fast path (A/B/C/D classification)
- `IntentExtractor` - Intent + slot extraction
- `EntityParser` - Budget, time, travel, quantity parsing
- `PolicyEngine` - PII risk, injection, confirmation logic
- `SLMModule` - Fallback for ambiguous cases

**Execution Path**:
- Fast path (>85% confidence): Rule-only
- Slow path (<85% confidence): Rule + SLM call

**Latency Target**: <500ms with rule-only path

---

### Stage 3: RouterPlanner
**Input**: TaskSpecV1  
**Output**: ActionPlan (mode, steps, budgets, policies)  
**Key Modules**:
- `SignalExtractor` - Extract routing hints from TaskSpec
- `ModeSelector` - Choose A/B/C/D mode
- `PlanBuilder` - LLM-powered plan generation
- `PlanValidator` - Policy & capability validation
- `BudgetManager` - Dynamic cost envelope
- `StateManager` - Task FSM & idempotency

**4 Execution Modes**:
- **Mode A (Research-only)**: Perplexity-like, no actions
- **Mode B (Action-only)**: Known workflow, no research
- **Mode C (Research→Action)**: Find info, then execute
- **Mode D (Action→Research)**: Check state, then explain

---

### Stage 4: UnifiedExecutor
**Input**: ActionPlan  
**Output**: EvidencePack + Receipt (if action)  
**Key Modules**:
- `RetrievalEngine` - BM25 + vector hybrid search
- `Reranker` - Cross-encoder ranking & diversity
- `WebFetch` - HTTP client with retry/backoff
- `SSRFGuard` - Block private IP ranges
- `DOMParser` - HTML parsing & extraction
- `TableExtractor` - Structured table parsing
- `ToolSandbox` - Policy enforcement
- `EvidenceBuilder` - Package evidence with citations
- `ExecutionTrace` - Audit trail

**Execution Substeps**:
1. **4.1 Retrieve**: Search for candidates
2. **4.2 FetchData**: Load & parse URLs
3. **4.3 Compute**: Transform/score data
4. **4.4 Act**: Browser automation (optional)

---

### Stage 5: Reasoning
**Input**: EvidencePack + Receipt  
**Output**: AnswerSkeleton + CitationMap  
**Key Modules**:
- `EvidenceSummarizer` - Token reduction
- `ReasoningCore` - LLM-powered reasoning
- `CitationMapper` - Claim ↔ evidence mapping
- `SafetyCheck` - Output validation

**Outputs**:
- Structured answer outline (sections, bullets)
- Atomic claims (each backed by evidence)
- Citation references (url + offset)
- Open questions (missing data indicators)

---

### Stage 6: AnswerSynthesis
**Input**: AnswerSkeleton + CitationMap  
**Output**: FinalAnswer (markdown + citations)  
**Key Modules**:
- `SynthesisComposer` - LLM renders skeleton → text
- `QuickPathSynth` - SLM for simple queries
- `PersonalizationFormatter` - User preference styling
- `PostProcessor` - Cleanup & redaction
- `ResponseBuilder` - API response construction

**Final Checks**:
- Citation format validation
- PII redaction
- Markdown validity
- Length constraints

---

## 🏗️ Directory Structure Map

```
comet-ai-browser/
├── packages/shared/
│   └── src/
│       ├── types/          ← Canonical types across all stages
│       ├── schemas/        ← JSON validation schemas
│       └── utils/          ← Shared utilities (logging, hashing, etc.)
│
├── services/
│   ├── STAGE-1-unified-input-core/     ← 8 sub-modules
│   ├── STAGE-2-query-understanding/    ← 5 sub-modules
│   ├── STAGE-3-router-planner/         ← 7 sub-modules
│   ├── STAGE-4-unified-executor/       ← 9 sub-modules
│   ├── STAGE-5-reasoning/              ← 4 sub-modules
│   ├── STAGE-6-answer-synthesis/       ← 5 sub-modules
│   ├── model-gateway/                  ← LLM/SLM/embeddings adapter
│   ├── retrieval-service/              ← Hybrid search engine
│   └── web-worker/                     ← HTTP fetch + headless browser
│
├── apps/
│   ├── extension/                       ← Browser extension (optional)
│   └── web-ui/                          ← Web interface (optional)
│
├── infra/
│   ├── k8s/                             ← Kubernetes manifests (6 stage deployments)
│   ├── terraform/                       ← Infrastructure as Code
│   └── ci/                              ← GitHub Actions / GitLab CI
│
└── docs/
    ├── ARCHITECTURE.md                  ← System design
    ├── API.md                           ← API specifications
    ├── THREAT-MODEL.md                  ← Security analysis
    ├── RUNBOOK.md                       ← Operations guide
    └── GLOSSARY.md                      ← Terminology
```

---

## 🔄 Data Flow: Types & Objects

| Stage | Input Type | Output Type | Key Decisions |
|-------|-----------|------------|---|
| **1** | RawRequest | UnifiedInputCore | Normalize, validate, language detect |
| **2** | UnifiedInputCore | TaskSpecV1 | Intent, slots, risk, routing |
| **3** | TaskSpecV1 | ActionPlan | Mode (A/B/C/D), steps, budget |
| **4** | ActionPlan | EvidencePack + Receipt | Search, fetch, compute, act |
| **5** | EvidencePack | AnswerSkeleton + CitationMap | Claims, evidence mapping |
| **6** | AnswerSkeleton | FinalAnswer | Render, personalize, package |

---

## 🚀 Deployment Strategy

### Development
- `docker-compose.yml` spins up all 6 stages + Redis + Postgres
- `.env.example` provides defaults

### Staging / Production
- Kubernetes manifests (separate deployment per stage)
- Terraform for cloud infrastructure (AWS/GCP/Azure)
- Persistent state in Redis + Postgres
- Observability: Prometheus + Grafana + OpenTelemetry

---

## 📊 Key Metrics per Stage

| Stage | P95 Latency | Key Metrics |
|-------|------------|---|
| **1** | <200ms | Input length, URL count, language detection |
| **2** | <500ms | Intent confidence, SLM call rate |
| **3** | <1s | Plan validity, policy violations |
| **4** | <5s | Retrieve success rate, fetch latency, action success |
| **5** | <2s | Evidence compression ratio, claim extraction rate |
| **6** | <2s | Citation coverage, synthesis latency |
| **Full** | <12s | End-to-end latency, error rate, cost/request |

---

## 🔐 Security Checkpoints

- **Stage 1**: Input size, URL format, language safety
- **Stage 2**: PII detection, injection pattern filtering
- **Stage 3**: Policy enforcement (no delete/submit in MVP)
- **Stage 4**: SSRF blocking, robots.txt respect, content sanitization
- **Stage 5**: Claim validation, evidence quality checks
- **Stage 6**: PII redaction, system prompt leak prevention

---

## ⚙️ Supporting Services

### model-gateway/
- Abstraction over LLM providers (GPT-4, Claude, Llama, etc.)
- Token budgeting & cost tracking
- Retry policies with exponential backoff
- Model fallback chains (primary → secondary → tertiary)
- Embedding service integration
- Reranking service integration

### retrieval-service/
- Hybrid search combining BM25 (keyword) + vector (semantic)
- Deduplication (URL-based + content-hash)
- Domain scoring (trusted sources prioritization)
- Result caching (session-based)
- Diversity enforcement (avoid monotone results)

### web-worker/
- HTTP client with timeout/retry/size limits
- SSRF protection (blocklist private IPs)
- HTML parsing (jsdom, cheerio, readability)
- Table structure extraction
- Headless browser pool (Playwright/Puppeteer) - P1
- Screenshot & state capture
- Action sandbox with policy gates

---

## 🧪 Testing Strategy

### Per Stage
- **Unit Tests**: Individual module behavior (validators, parsers, extractors)
- **Integration Tests**: Module interactions within stage
- **Golden Tests**: Deterministic outputs for regression prevention
- **E2E Tests**: Full pipeline with test data

### Cross-Stage
- **Contract Tests**: Type compatibility between stages
- **Scenario Tests**: Mode A/B/C/D workflows
- **Security Tests**: SSRF, injection, PII handling
- **Load Tests**: Throughput & latency under stress

---

## 🎓 Implementation Sequence

**Phase 1 (MVP Core)**
1. Stages 1-2 (sync path)
2. Stages 3-4-5-6 (async completion)
3. model-gateway + retrieval + web-worker
4. Local docker-compose setup

**Phase 2 (Production)**
5. Kubernetes manifests
6. Terraform infrastructure
7. CI/CD pipelines
8. Monitoring & observability

**Phase 3 (Advanced)**
9. Headless browser (Stage 4 interactive actions)
10. VLM/PDF pipeline (OCR for documents)
11. Personalization ranking
12. On-device lite models

---

## 📚 Key Documentation Files

Each service has:
- `README.md` - Service overview & quick start
- `src/config.ts` - Configuration schema
- `tests/` - Unit, integration, E2E test suites

Root-level docs:
- `docs/ARCHITECTURE.md` - C4 diagrams, data model
- `docs/API.md` - OpenAPI spec, endpoint schemas
- `docs/THREAT-MODEL.md` - Security analysis
- `docs/RUNBOOK.md` - Deployment, troubleshooting

---

## 🔗 Service Communication

```
API Gateway (WAF, Auth, Rate Limit)
    ↓
Orchestrator Service (Stage 3 router)
    ├── → Stage 1 Service
    ├── → Stage 2 Service
    ├── → Stage 4 Service
    │   ├── → Retrieval Service
    │   ├── → Web Worker Service
    │   └── → Model Gateway
    ├── → Stage 5 Service
    └── → Stage 6 Service
    
All stages ↔ Redis (idempotency, state)
All stages ↔ Postgres (artifacts storage)
All stages → OpenTelemetry (traces/metrics)
```

---

**Status**: Implementation Ready ✅  
**Version**: 1.0 MVP Enterprise  
**Last Updated**: December 2025


----
# AI-Native Browser (Comet-like) - Complete Folder Structure
## 6 Modules Enterprise MVP Architecture

```
comet-ai-browser/
│
├── 📁 docs/
│   ├── README.md                           # Main project documentation
│   ├── ARCHITECTURE.md                     # System architecture overview
│   ├── API.md                              # API specifications (endpoints, schemas)
│   ├── THREAT-MODEL.md                     # Security threat model & mitigations
│   ├── RUNBOOK.md                          # Operations & troubleshooting guide
│   ├── ROADMAP.md                          # Future features & milestones
│   └── GLOSSARY.md                         # Terminology & definitions
│
├── 📁 packages/
│   └── shared/
│       ├── tsconfig.json
│       ├── package.json
│       └── src/
│           ├── types/                      # Shared TypeScript types
│           │   ├── common.ts               # RawRequest, NormalizedInput
│           │   ├── task-spec.ts            # TaskSpecV1, ActionPlan
│           │   ├── evidence.ts             # EvidencePack, EvidenceItem
│           │   ├── answer.ts               # AnswerSkeleton, FinalAnswer
│           │   └── errors.ts               # Error types, exception classes
│           ├── schemas/                    # Validation schemas & serializers
│           │   ├── input.schema.ts         # RawRequestV1 validation
│           │   ├── task.schema.ts          # TaskSpecV1 validation
│           │   ├── evidence.schema.ts      # EvidencePack validation
│           │   ├── answer.schema.ts        # FinalAnswer validation
│           │   └── api.schema.ts           # API response/request schemas
│           └── utils/
│               ├── logger.ts               # Structured logging setup
│               ├── tracer.ts               # OpenTelemetry tracing
│               ├── hashing.ts              # SHA256, payload hashing
│               ├── url-parser.ts           # URL parsing & validation
│               ├── validators.ts           # Common validators
│               └── constants.ts            # Global constants, limits
│
├── 📁 services/
│   │
│   ├── 🔷 STAGE-1-unified-input-core/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts                    # Service entrypoint
│   │       ├── config.ts                   # Configuration & env vars
│   │       ├── constants.ts                # Local constants (MAX_INPUT_LENGTH, etc.)
│   │       ├── exceptions.ts               # Custom exception classes
│   │       ├── api/
│   │       │   ├── routes.ts               # FastAPI/Express route handlers
│   │       │   ├── handlers.ts             # Request/response handlers
│   │       │   ├── middleware.ts           # Auth, CORS, logging middleware
│   │       │   └── schemas.ts              # API request/response schemas
│   │       ├── stages/
│   │       │   └── stage1/                 # Stage 1 pipeline logic
│   │       │       ├── validator.ts        # 1.1 validateRawRequest
│   │       │       ├── env-builder.ts      # 1.2 buildEnv
│   │       │       ├── envelope.ts         # 1.3 initEnvelope
│   │       │       ├── classifier.ts       # 1.4 runInputClassifier
│   │       │       ├── normalizer.ts       # 1.5 runTextNormalizer
│   │       │       ├── context.ts          # 1.6 attachPageContext
│   │       │       ├── safety.ts           # 1.7 computeSafetyFlags
│   │       │       └── telemetry.ts        # 1.8 buildTelemetry
│   │       ├── modules/
│   │       │   ├── input-adapter.ts        # InputAdapter component
│   │       │   ├── context-collector.ts    # ContextCollector component
│   │       │   └── normalizer.ts           # Normalizer component
│   │       ├── integrations/
│   │       │   ├── redis.ts                # Redis client for idempotency
│   │       │   ├── cache.ts                # Caching layer
│   │       │   └── vault.ts                # Secrets management
│   │       └── observability/
│   │           ├── logging.ts              # Structured JSON logging
│   │           ├── metrics.ts              # Prometheus metrics
│   │           └── tracing.ts              # OpenTelemetry spans
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── normalizer.test.ts
│   │       │   ├── classifier.test.ts
│   │       │   ├── safety.test.ts
│   │       │   └── validator.test.ts
│   │       ├── integration/
│   │       │   ├── api.test.ts
│   │       │   ├── redis.test.ts
│   │       │   └── pipeline.test.ts
│   │       └── e2e/
│   │           ├── full-flow.test.ts
│   │           └── idempotency.test.ts
│   │
│   ├── 🔷 STAGE-2-query-understanding/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── constants.ts
│   │       ├── exceptions.ts
│   │       ├── api/
│   │       │   ├── routes.ts
│   │       │   ├── handlers.ts
│   │       │   └── schemas.ts
│   │       ├── stages/
│   │       │   └── stage2/
│   │       │       ├── orchestrator.ts     # runQueryUnderstanding entrypoint
│   │       │       ├── rule-engine.ts      # 2.1 Rule-based classification (A, B, C, D)
│   │       │       ├── intent-extractor.ts # Intent & Slot extraction
│   │       │       ├── entity-parser.ts    # Parse budget, time, travel, quantity
│   │       │       ├── policy-engine.ts    # 2.2 Policy overrides & safety checks
│   │       │       └── slm-module.ts       # 2.3 SLM call for slow path
│   │       ├── modules/
│   │       │   ├── policy-classifier.ts    # Toxicity, PII, injection detection
│   │       │   └── embedding-prep.ts       # Query embedding generation
│   │       ├── rules/
│   │       │   ├── intent-rules.ts         # Intent classification rules
│   │       │   ├── entity-rules.ts         # Entity extraction rules
│   │       │   └── policy-rules.ts         # Policy & safety rules
│   │       ├── integrations/
│   │       │   ├── model-gateway.ts        # SLM model calls
│   │       │   └── embeddings.ts           # Embedding service
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── tracing.ts
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── rule-engine.test.ts
│   │       │   ├── entity-parser.test.ts
│   │       │   └── policy-engine.test.ts
│   │       ├── integration/
│   │       │   ├── slm-call.test.ts
│   │       │   └── end-to-end.test.ts
│   │       └── golden/
│   │           └── golden-tests.ts         # Deterministic outputs
│   │
│   ├── 🔷 STAGE-3-router-planner/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── constants.ts
│   │       ├── exceptions.ts
│   │       ├── api/
│   │       │   ├── routes.ts
│   │       │   ├── handlers.ts
│   │       │   └── schemas.ts
│   │       ├── stages/
│   │       │   └── stage3/
│   │       │       ├── orchestrator.ts     # Main Stage 3 orchestrator
│   │       │       ├── signal-extractor.ts # 3.1 Extract routing signals
│   │       │       ├── mode-selector.ts    # 3.2 Mode selection (A, B, C, D)
│   │       │       ├── plan-builder.ts     # 3.3 PlanBuilder (Planner LLM)
│   │       │       ├── plan-validator.ts   # 3.4 PlanValidator
│   │       │       ├── budget-manager.ts   # 3.5 BudgetManager
│   │       │       ├── state-manager.ts    # 3.6 StateManager & task FSM
│   │       │       └── step-executor.ts    # 3.7 Runtime step execution
│   │       ├── modules/
│   │       │   ├── plan-generator.ts       # ActionPlan generation
│   │       │   ├── policy-enforcer.ts      # Policy constraints enforcement
│   │       │   └── personalization.ts      # User preference adjustments
│   │       ├── integrations/
│   │       │   ├── model-gateway.ts        # LLM/Planner calls
│   │       │   ├── state-store.ts          # Redis/DB state persistence
│   │       │   └── tool-registry.ts        # Capability registry
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── tracing.ts
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── plan-validator.test.ts
│   │       │   ├── budget-manager.test.ts
│   │       │   └── state-manager.test.ts
│   │       ├── integration/
│   │       │   ├── mode-selection.test.ts
│   │       │   └── plan-generation.test.ts
│   │       └── scenario/
│   │           ├── mode-a.scenario.ts
│   │           ├── mode-b.scenario.ts
│   │           ├── mode-c.scenario.ts
│   │           └── mode-d.scenario.ts
│   │
│   ├── 🔷 STAGE-4-unified-executor/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── constants.ts
│   │       ├── exceptions.ts
│   │       ├── api/
│   │       │   ├── routes.ts
│   │       │   ├── handlers.ts
│   │       │   └── schemas.ts
│   │       ├── stages/
│   │       │   └── stage4/
│   │       │       ├── orchestrator.ts     # Stage 4 main executor
│   │       │       ├── 4.1-retrieval.ts    # 4.1 RetrievalEngine
│   │       │       ├── 4.2-fetch.ts        # 4.2 WebFetch & SSRF Guard
│   │       │       ├── 4.3-extract.ts      # 4.3 DOM parsing & extraction
│   │       │       ├── 4.4-action.ts       # 4.4 Action execution
│   │       │       └── evidence-builder.ts # EvidenceBuilder & packaging
│   │       ├── modules/
│   │       │   ├── retrieval-engine.ts     # Hybrid search (BM25 + vector)
│   │       │   ├── reranker.ts             # Cross-encoder reranking
│   │       │   ├── web-fetch.ts            # HTTP client with retries
│   │       │   ├── ssrf-guard.ts           # SSRF protection
│   │       │   ├── dom-parser.ts           # HTML parsing & extraction
│   │       │   ├── table-extractor.ts      # Table structure extraction
│   │       │   ├── content-extractor.ts    # Main content extraction
│   │       │   ├── tool-sandbox.ts         # Tool execution sandbox
│   │       │   ├── action-policy.ts        # Action allowlisting
│   │       │   └── execution-trace.ts      # Trace collection
│   │       ├── integrations/
│   │       │   ├── model-gateway.ts        # VLM/OCR calls
│   │       │   ├── vector-store.ts         # Embedding search
│   │       │   ├── search-provider.ts      # External search API (optional)
│   │       │   ├── headless-browser.ts     # Playwright/Puppeteer
│   │       │   └── http-client.ts          # HTTP fetching
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── tracing.ts
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── ssrf-guard.test.ts
│   │       │   ├── dom-parser.test.ts
│   │       │   └── retrieval.test.ts
│   │       ├── integration/
│   │       │   ├── web-fetch.test.ts
│   │       │   ├── action-execution.test.ts
│   │       │   └── end-to-end.test.ts
│   │       └── security/
│   │           ├── ssrf.test.ts
│   │           └── injection.test.ts
│   │
│   ├── 🔷 STAGE-5-reasoning/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── constants.ts
│   │       ├── exceptions.ts
│   │       ├── api/
│   │       │   ├── routes.ts
│   │       │   ├── handlers.ts
│   │       │   └── schemas.ts
│   │       ├── stages/
│   │       │   └── stage5/
│   │       │       ├── orchestrator.ts     # Stage 5 reasoning orchestrator
│   │       │       ├── 5.1-summarizer.ts   # 5.1 EvidenceSummarizer
│   │       │       ├── 5.2-reasoning.ts    # 5.2 ReasoningCore (Reasoning LLM)
│   │       │       ├── 5.3-citation.ts     # 5.3 CitationMapper
│   │       │       └── 5.4-safety.ts       # 5.4 OutputSafetyCheck
│   │       ├── modules/
│   │       │   ├── evidence-summarizer.ts  # Token reduction & compression
│   │       │   ├── claim-extractor.ts      # Atomic claim extraction
│   │       │   ├── citation-mapper.ts      # Claim-to-evidence mapping
│   │       │   ├── contradiction-resolver.ts # Handle conflicting sources
│   │       │   └── safety-checker.ts       # Output safety validation
│   │       ├── integrations/
│   │       │   ├── model-gateway.ts        # Reasoning LLM calls
│   │       │   └── state-store.ts          # Evidence retrieval
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── tracing.ts
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── claim-extractor.test.ts
│   │       │   └── citation-mapper.test.ts
│   │       ├── integration/
│   │       │   ├── reasoning-flow.test.ts
│   │       │   └── safety-check.test.ts
│   │       └── quality/
│   │           └── citation-quality.test.ts
│   │
│   ├── 🔷 STAGE-6-answer-synthesis/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── constants.ts
│   │       ├── exceptions.ts
│   │       ├── api/
│   │       │   ├── routes.ts
│   │       │   ├── handlers.ts
│   │       │   └── schemas.ts
│   │       ├── stages/
│   │       │   └── stage6/
│   │       │       ├── orchestrator.ts     # Stage 6 main orchestrator
│   │       │       ├── 6.1-composer.ts     # 6.1 SynthesisComposer (LLM)
│   │       │       ├── 6.2-quick.ts        # 6.2 QuickPathSynth (SLM)
│   │       │       ├── 6.3-format.ts       # 6.3 PersonalizationFormatter
│   │       │       ├── 6.4-postproc.ts     # 6.4 PostProcessor
│   │       │       └── 6.5-package.ts      # 6.5 ResponsePackaging
│   │       ├── modules/
│   │       │   ├── composer.ts             # Answer composition
│   │       │   ├── formatter.ts            # Markdown/block formatting
│   │       │   ├── personalizer.ts         # User preference application
│   │       │   ├── post-processor.ts       # Cleanup & validation
│   │       │   └── response-builder.ts     # API response construction
│   │       ├── templates/
│   │       │   ├── answer-template.ts      # Answer structure templates
│   │       │   ├── citation-format.ts      # Citation rendering
│   │       │   └── error-messages.ts       # Standard error responses
│   │       ├── integrations/
│   │       │   ├── model-gateway.ts        # LLM calls (composer)
│   │       │   └── state-store.ts          # Evidence & skeleton retrieval
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── tracing.ts
│   │   └── tests/
│   │       ├── unit/
│   │       │   ├── composer.test.ts
│   │       │   ├── formatter.test.ts
│   │       │   └── post-processor.test.ts
│   │       ├── integration/
│   │       │   ├── synthesis-flow.test.ts
│   │       │   └── response-build.test.ts
│   │       └── output-quality/
│   │           ├── citation-format.test.ts
│   │           └── markdown-validity.test.ts
│   │
│   ├── 🔷 model-gateway/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── adapters/
│   │       │   ├── llm-adapter.ts          # LLM (GPT-4, Claude, etc.)
│   │       │   ├── slm-adapter.ts          # Small LM (Llama, Phi, etc.)
│   │       │   ├── embeddings-adapter.ts   # Embeddings (OpenAI, local)
│   │       │   ├── reranker-adapter.ts     # Cross-encoder reranking
│   │       │   └── vlm-adapter.ts          # Vision-Language Model
│   │       ├── policies/
│   │       │   ├── retry-policy.ts         # Exponential backoff
│   │       │   ├── budget-policy.ts        # Token/cost enforcement
│   │       │   ├── timeout-policy.ts       # Request timeouts
│   │       │   └── fallback-policy.ts      # Model fallback chains
│   │       ├── cache/
│   │       │   ├── embedding-cache.ts
│   │       │   ├── model-response-cache.ts
│   │       │   └── cache-invalidation.ts
│   │       └── observability/
│   │           ├── logging.ts
│   │           ├── metrics.ts
│   │           └── cost-tracking.ts
│   │   └── tests/
│   │       ├── unit/
│   │       └── integration/
│   │
│   ├── 🔷 retrieval-service/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   ├── tsconfig.json
│   │   ├── package.json
│   │   ├── README.md
│   │   └── src/
│   │       ├── index.ts
│   │       ├── config.ts
│   │       ├── hybrid/
│   │       │   ├── hybrid-search.ts        # BM25 + Vector hybrid
│   │       │   ├── bm25-engine.ts
│   │       │   └── vector-engine.ts
│   │       ├── rerank/
│   │       │   ├── cross-encoder.ts
│   │       │   └── diversity-ranker.ts
│   │       ├── cache/
│   │       │   ├── session-cache.ts        # Session-based caching
│   │       │   └── result-cache.ts
│   │       ├── dedup/
│   │       │   ├── url-dedup.ts
│   │       │   └── content-dedup.ts
│   │       └── observability/
│   │           ├── logging.ts
│   │           └── metrics.ts
│   │   └── tests/
│   │
│   └── 🔷 web-worker/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── .env.example
│       ├── tsconfig.json
│       ├── package.json
│       ├── README.md
│       └── src/
│           ├── index.ts
│           ├── config.ts
│           ├── fetch/
│           │   ├── http-client.ts          # HTTP fetching with retries
│           │   ├── ssrf-guard.ts           # SSRF protection
│           │   └── robots-checker.ts       # robots.txt compliance
│           ├── extract/
│           │   ├── dom-parser.ts           # HTML parsing
│           │   ├── content-extractor.ts    # Main content extraction
│           │   ├── table-extractor.ts      # Table structure extraction
│           │   └── metadata-extractor.ts   # Title, author, date, etc.
│           ├── sanitize/
│           │   ├── html-sanitizer.ts       # XSS protection
│           │   ├── pii-redactor.ts         # PII redaction
│           │   └── injection-filter.ts     # Prompt injection filtering
│           ├── sandbox/
│           │   ├── action-sandbox.ts       # Action execution sandbox
│           │   ├── allowlist-manager.ts    # Tool/domain allowlisting
│           │   └── approval-handler.ts     # Human approval workflow
│           ├── headless/
│           │   ├── browser-pool.ts         # Playwright/Puppeteer pool
│           │   ├── screenshot-engine.ts    # Screenshot capture
│           │   └── interaction-handler.ts  # Click, type, fill, submit
│           └── observability/
│               ├── logging.ts
│               └── metrics.ts
│       └── tests/
│
├── 📁 apps/
│   │
│   ├── extension/
│   │   ├── manifest.json
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── popup.html / popup.ts
│   │   │   ├── background.ts               # Service worker
│   │   │   ├── content-script.ts           # Page context capture
│   │   │   └── api-client.ts               # Backend API calls
│   │   └── tests/
│   │
│   └── web-ui/
│       ├── package.json
│       ├── vite.config.ts / next.config.js # Build config
│       ├── public/
│       ├── src/
│       │   ├── pages/
│       │   │   ├── home.tsx
│       │   │   ├── chat.tsx
│       │   │   └── results.tsx
│       │   ├── components/
│       │   │   ├── query-input.tsx
│       │   │   ├── answer-display.tsx
│       │   │   ├── citations.tsx
│       │   │   └── progress.tsx
│       │   ├── api-client.ts
│       │   └── styles/
│       └── tests/
│
├── 📁 infra/
│   ├── k8s/
│   │   ├── namespace.yaml
│   │   ├── stage1-deployment.yaml
│   │   ├── stage2-deployment.yaml
│   │   ├── stage3-deployment.yaml
│   │   ├── stage4-deployment.yaml
│   │   ├── stage5-deployment.yaml
│   │   ├── stage6-deployment.yaml
│   │   ├── model-gateway-deployment.yaml
│   │   ├── retrieval-deployment.yaml
│   │   ├── web-worker-deployment.yaml
│   │   ├── services/
│   │   │   └── *.yaml
│   │   ├── configmaps/
│   │   │   └── *.yaml
│   │   ├── secrets/
│   │   │   └── *.yaml
│   │   └── ingress/
│   │       └── *.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── redis.tf                       # Redis infrastructure
│   │   ├── postgres.tf                    # PostgreSQL for artifacts
│   │   ├── kubernetes.tf                  # K8s cluster
│   │   └── monitoring.tf                  # Prometheus, Grafana
│   ├── docker-compose.yml                 # Local development
│   ├── .env.example
│   └── ci/
│       ├── .github/
│       │   └── workflows/
│       │       ├── test.yml               # Unit & integration tests
│       │       ├── lint.yml               # Code quality checks
│       │       ├── security.yml           # Security scanning
│       │       └── deploy.yml             # CD pipeline
│       └── gitlab-ci.yml                  # Alternative CI/CD
│
├── 📄 .gitignore
├── 📄 .env.example
├── 📄 docker-compose.yml                  # Full stack local dev
├── 📄 package.json                        # Root monorepo config
├── 📄 pnpm-workspace.yaml                 # pnpm monorepo setup
├── 📄 tsconfig.json                       # Root TS config
├── 📄 README.md                           # Project overview
├── 📄 CONTRIBUTING.md                     # Development guidelines
├── 📄 LICENSE                             # License file
└── 📄 CHANGELOG.md                        # Version history
```

---

## 📊 Module Overview

### 🔷 STAGE 1: UnifiedInputCore
**Purpose**: Normalize and validate user input
- **Components**: InputAdapter, ContextCollector, Normalizer, SafetyPrecheck
- **Key Tasks**: 
  - Validate RawRequest schema
  - Normalize text & URL extraction
  - Detect language
  - Attach page context
  - Compute safety flags
- **Output**: `UnifiedInputCoreV1`

### 🔷 STAGE 2: QueryUnderstanding  
**Purpose**: Intent classification and task specification
- **Components**: PolicyClassifiers, IntentExtractor, RuleEngine, EmbeddingPrep
- **Key Tasks**:
  - Classify intent (qa, summarize, extract, etc.)
  - Extract slots & entities (budget, time, travel, etc.)
  - Apply policy overrides (PII, injection, confirmation)
  - Optional SLM call for complex queries
- **Output**: `TaskSpecV1`

### 🔷 STAGE 3: RouterPlanner
**Purpose**: Plan generation and orchestration strategy
- **Components**: SignalExtractor, ModeSelector, PlanBuilder, PlanValidator, BudgetManager, StateManager
- **Key Tasks**:
  - Extract routing signals from TaskSpec
  - Select execution mode (A=Research, B=Action, C=Research+Action, D=Action+Research)
  - Generate ActionPlan with steps, budgets, policy gates
  - Validate against policies & constraints
- **Output**: `ActionPlan` (with mode, steps, budgets)

### 🔷 STAGE 4: UnifiedExecutor
**Purpose**: Execute plan steps (retrieval, fetch, compute, action)
- **Components**: RetrievalEngine, Reranker, WebFetch, DOMParser, TableExtractor, ToolSandbox, EvidenceBuilder
- **Key Tasks**:
  - **4.1 Retrieve**: Hybrid search (BM25 + vector) with dedup
  - **4.2 FetchData**: HTTP fetch with SSRF protection, parse tables
  - **4.3 Compute**: Structured reasoning without UI actions (scoring, recommendations)
  - **4.4 Act**: Headless browser automation with policy gates & receipts
- **Output**: `EvidencePack` + `Receipt` (for actions)

### 🔷 STAGE 5: Reasoning
**Purpose**: Multi-step reasoning over evidence
- **Components**: EvidenceSummarizer, ReasoningCore, CitationMapper, OutputSafetyCheck
- **Key Tasks**:
  - Compress EvidencePack into digest
  - Extract atomic claims (each with evidence backing)
  - Resolve contradictions, flag uncertainties
  - Map claims to evidence (citations)
  - Safety validation
- **Output**: `AnswerSkeleton` + `CitationMap` + `OpenQuestions`

### 🔷 STAGE 6: AnswerSynthesis
**Purpose**: Generate final user-facing answer
- **Components**: SynthesisComposer, QuickPathSynth, PersonalizationFormatter, PostProcessor, ResponsePackaging
- **Key Tasks**:
  - Compose answer from AnswerSkeleton
  - Insert citations (inline + reference list)
  - Apply user personalization (tone, depth)
  - Post-processing (strip leaked system prompts, PII redaction)
  - Package response for FE
- **Output**: `FinalAnswer` + `ResponseV1`

---

## 🔧 Supporting Services

### model-gateway/
- Adapters for LLM, SLM, embeddings, reranker, VLM
- Retry policies, budget enforcement, caching
- Cost tracking & model fallback chains

### retrieval-service/
- Hybrid search engine (BM25 + vector)
- Reranking & diversity enforcement
- Session-based result caching
- URL & content deduplication

### web-worker/
- HTTP fetching with retries & SSRF protection
- HTML parsing & content extraction
- Table structure extraction
- Headless browser automation (P1)
- Sandbox for action execution
- PII redaction & injection filtering

---

## 🚀 Infrastructure & DevOps

### K8s (Kubernetes)
- Separate deployments for each stage service
- ConfigMaps for environment config
- Secrets for API keys & credentials
- Ingress for API Gateway
- Service mesh optional (Istio)

### Terraform
- Infrastructure as Code
- Redis cluster setup
- PostgreSQL database
- K8s cluster provisioning
- Monitoring stack (Prometheus, Grafana)

### CI/CD
- GitHub Actions workflows (test, lint, security, deploy)
- Automated testing on PR
- Security scanning (SAST/dependency)
- Containerized builds & registry push

### Local Development
- `docker-compose.yml` for full stack setup
- `.env.example` for configuration template

---

## 📚 Documentation

- **ARCHITECTURE.md**: System design overview
- **API.md**: Endpoint specs, request/response schemas
- **THREAT-MODEL.md**: Security considerations & mitigations
- **RUNBOOK.md**: Operational procedures, troubleshooting
- **GLOSSARY.md**: Terminology definitions

---

## 🔐 Security & Observability

### Security
- SSRF protection (private IP blocklist)
- Prompt injection filtering
- PII detection & redaction
- Input validation & sanitization
- Action sandbox with policy gates
- Rate limiting & auth

### Observability
- **Logging**: Structured JSON logs (no sensitive data)
- **Metrics**: Prometheus (request count, latency, errors)
- **Tracing**: OpenTelemetry (distributed tracing)
- **Dashboards**: Grafana for monitoring

---

## 📋 Key Files Reference

| File | Purpose |
|------|---------|
| `packages/shared/types/` | Canonical types (TaskSpec, Evidence, Answer) |
| `packages/shared/schemas/` | Validation schemas & serializers |
| `services/*/src/stages/` | Core stage logic (1-6) |
| `services/*/src/modules/` | Individual components per stage |
| `services/*/tests/` | Unit, integration, E2E tests |
| `infra/k8s/*.yaml` | Kubernetes manifests |
| `infra/terraform/` | IaC for cloud infrastructure |
| `docs/*.md` | Architecture, API, operations guides |

---

## 🔄 Data Flow Summary

```
User Input
    ↓
Stage 1: UnifiedInputCore
    ↓ NormalizedInput
Stage 2: QueryUnderstanding
    ↓ TaskSpecV1
Stage 3: RouterPlanner
    ↓ ActionPlan
Stage 4: UnifiedExecutor
    ↓ EvidencePack + Receipt
Stage 5: Reasoning
    ↓ AnswerSkeleton + CitationMap
Stage 6: AnswerSynthesis
    ↓ FinalAnswer (Markdown + Citations)
```

---

**Created**: December 2025  
**Version**: 1.0 (MVP Enterprise)  
**Status**: Implementation Ready

---

# Mỗi stage là 1 con docker compose như này thì nó có đảm bảo response time không?




Có, dùng mỗi stage là một service trong cùng một docker-compose **hoàn toàn có thể đạt được response time tốt**, miễn là thiết kế đúng và máy chủ đủ khỏe. Docker Compose bản chất chỉ là cách khai báo nhiều container trên **cùng một host**, overhead network giữa các container rất nhỏ (bridge network nội bộ, thường vài ms trở xuống).[webkt+1](https://www.webkt.com/article/10356)​

## Khi nào docker-compose vẫn đáp ứng latency tốt

- **Tất cả service chạy trên một máy**: docker-compose được thiết kế cho single-host, nên hop giữa các stage chỉ là internal Docker network, nhanh hơn nhiều so với đi qua internet hay multi-node cluster.[webkt](https://www.webkt.com/article/10356)​
    
- **Số hop hợp lý**: pipeline của bạn 6 stage, nhưng không nhất thiết mỗi stage phải là HTTP hop riêng; có thể group 1–2–3 vào cùng service orchestrator, 4–5–6 trong 1–2 service để giảm network round-trip.
    
- **Resource đủ**: nếu CPU/RAM đủ và không swap, latency chủ yếu đến từ LLM call, web fetch… chứ không phải docker-compose. Với app nhỏ–trung bình, docker-compose thường cho performance rất tốt trong môi trường dev/staging, đôi khi còn nhanh hơn K8s local vì overhead ít hơn.[datacamp+1](https://www.datacamp.com/blog/docker-compose-vs-kubernetes)​
    

## Rủi ro về response time nếu mỗi stage là 1 service

- **Chuỗi HTTP sync dài**: nếu request phải đi qua 6 service sync (Gateway → Stage1 → Stage2 → Stage3 → Stage4 → Stage5 → Stage6), mỗi hop tốn thêm vài–vài chục ms (network + serialization) → p95 dễ bị đội lên. Có case thực tế thêm nhiều hop trong container network làm tăng latency rõ rệt.[github+1](https://github.com/docker/compose/issues/5085)​
    
- **Under-provision / throttling**: nếu mỗi stage chỉ 1 replica, không có queue, khi load tăng thì thời gian chờ trong hàng (queueing delay) sẽ chiếm phần lớn latency.
    
- **Chia quá nhỏ trong khi LLM/web fetch mới là bottleneck**: tối ưu vài ms networking không đáng so với 500–2000ms LLM + web; quan trọng là giảm số lần gọi model/fetch, parallel hóa, chứ không chỉ là chia container.
    

## Gợi ý kiến trúc cho latency

|Lựa chọn|Ưu điểm|Nhược điểm|
|---|---|---|
|1 docker-compose, nhiều service (6 stage tách)**|Dễ scale per-stage, code boundary rõ|Nhiều HTTP hop, phức tạp hóa cho MVP|
|1 docker-compose, 2–3 service lớn (ví dụ: Input+QU, Orchestrator 3–6, Retrieval/WebWorker, Model Gateway)**|Giảm hop, vẫn tách concern|Cần kỷ luật code để giữ boundary trong code, không “monolith lại”|
|1 service monolith cho Stage 1–6 (trong 1 container)|Latency thấp nhất, đơn giản|Khó scale lệch (ví dụ Stage 4 nặng, 1–2 nhẹ)|

Với **MVP và target p95 ~8–12s**, kiến nghị:

- Chạy tất cả trên **một docker-compose stack**, nhưng:
    
    - Gom Stage 1–3 trong **orchestrator service**, Stage 4 trong **retrieval/web-worker**, Stage 5–6 trong **reasoning/synthesis** (tối đa 3–4 service chính).
        
    - Dùng **async pipeline**: Gateway nhận request → trả `task_id` nhanh (Stage 1–2 sync), phần còn lại chạy async, FE poll/stream → giảm yêu cầu 1 request phải chờ full 6 stage.
        
- Đảm bảo:
    
    - LLM calls dùng **model-gateway với retry/budget**.
        
    - Web fetch có timeout p95 hợp lý (2–3s) và limit số URL.
        
    - Đo đạc p50/p95 per-stage qua Prometheus + tracing để biết bottleneck nằm ở đâu.[linkedin+1](https://www.linkedin.com/posts/brijpandeyji_12-microservices-best-practices-1-orchestration-activity-7301449541654896640-BSKX)​
        

## Kết luận ngắn

- **Docker-compose không phải nút thắt cổ chai chính**; nếu chạy trên một host khỏe, hoàn toàn đủ để đạt p95 < 8–12s như spec.[baeldung+1](https://www.baeldung.com/ops/docker-compose-vs-kubernetes)​
    
- Điều quyết định response time là: số HTTP hop giữa stage, cách group service, cách async pipeline, và tối ưu LLM/web-fetch, hơn là việc “mỗi stage là một docker-compose service” hay không.
    

1. [https://www.webkt.com/article/10356](https://www.webkt.com/article/10356)
2. [https://shipyard.build/blog/comparing-docker-kubernetes-local-dev/](https://shipyard.build/blog/comparing-docker-kubernetes-local-dev/)
3. [https://www.datacamp.com/blog/docker-compose-vs-kubernetes](https://www.datacamp.com/blog/docker-compose-vs-kubernetes)
4. [https://github.com/docker/compose/issues/5085](https://github.com/docker/compose/issues/5085)
5. [https://stackoverflow.com/questions/47710883/http-connection-problems-between-services-in-docker-compose](https://stackoverflow.com/questions/47710883/http-connection-problems-between-services-in-docker-compose)
6. [https://www.linkedin.com/posts/brijpandeyji_12-microservices-best-practices-1-orchestration-activity-7301449541654896640-BSKX](https://www.linkedin.com/posts/brijpandeyji_12-microservices-best-practices-1-orchestration-activity-7301449541654896640-BSKX)
7. [https://www.gravitee.io/blog/microservice-orchestration-best-practices](https://www.gravitee.io/blog/microservice-orchestration-best-practices)
8. [https://www.baeldung.com/ops/docker-compose-vs-kubernetes](https://www.baeldung.com/ops/docker-compose-vs-kubernetes)
9. [https://www.reddit.com/r/kubernetes/comments/x413a4/increased_latency_on_a_microservices_application/](https://www.reddit.com/r/kubernetes/comments/x413a4/increased_latency_on_a_microservices_application/)
10. [https://spacelift.io/blog/docker-compose-vs-kubernetes](https://spacelift.io/blog/docker-compose-vs-kubernetes)
11. [https://discuss.kubernetes.io/t/kubernetes-frontend-service-latency-astronomically-higher-than-docker-compose-based-setup/28677](https://discuss.kubernetes.io/t/kubernetes-frontend-service-latency-astronomically-higher-than-docker-compose-based-setup/28677)
12. [https://overcast.blog/optimizing-docker-networking-performance-reducing-latency-and-increasing-throughput-45aba9759af4](https://overcast.blog/optimizing-docker-networking-performance-reducing-latency-and-increasing-throughput-45aba9759af4)
13. [https://blog.devgenius.io/5-docker-compose-mistakes-that-are-killing-your-apps-performance-and-how-to-fix-them-0701a6274530](https://blog.devgenius.io/5-docker-compose-mistakes-that-are-killing-your-apps-performance-and-how-to-fix-them-0701a6274530)
14. [https://www.linkedin.com/pulse/streamlining-microservices-docker-compose-guide-isuru-vithanage-tookc](https://www.linkedin.com/pulse/streamlining-microservices-docker-compose-guide-isuru-vithanage-tookc)
15. [https://www.kaaiot.com/iot-knowledge-base/docker-compose-vs-kubernetes-differences-and-use-cases](https://www.kaaiot.com/iot-knowledge-base/docker-compose-vs-kubernetes-differences-and-use-cases)
16. [https://www.netdata.cloud/academy/docker-compose-networking-mysteries/](https://www.netdata.cloud/academy/docker-compose-networking-mysteries/)
17. [https://www.reddit.com/r/docker/comments/1eso582/using_containers_in_a_high_volume_network_what/](https://www.reddit.com/r/docker/comments/1eso582/using_containers_in_a_high_volume_network_what/)
18. [https://www.reddit.com/r/docker/comments/10wcnpt/is_docker_compose_good_for_microservices/](https://www.reddit.com/r/docker/comments/10wcnpt/is_docker_compose_good_for_microservices/)
19. [https://www.devzero.io/blog/docker-microservices](https://www.devzero.io/blog/docker-microservices)
20. [https://www.reddit.com/r/dataengineering/comments/13s6ugn/docker_compose_vs_kubernetes_understanding_the/](https://www.reddit.com/r/dataengineering/comments/13s6ugn/docker_compose_vs_kubernetes_understanding_the/)