<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Deep research best practices cho việc dùng Cursor

1. Là dùng các con kia
2. Là rộng hơn toàn bộ hệ thống

Dựa trên nghiên cứu sâu từ 135+ nguồn, tôi đã tổng hợp một báo cáo toàn diện về best practices cho Cursor IDE, bao gồm cả hệ thống multi-agent và toàn bộ workflow phát triển.

***

# CURSOR IDE: DEEP RESEARCH VỀ BEST PRACTICES 2025

## Tổng Quan Executive Summary

Cursor đã trở thành IDE AI-native phát triển nhanh nhất trong lịch sử SaaS, đạt \$500M ARR trong vòng 2 năm, được sử dụng bởi hơn 70% kỹ sư tại các công ty như Stripe, Coinbase, Uber, và NVIDIA. Sự thành công này đến từ việc tích hợp AI sâu vào toàn bộ development workflow thay vì chỉ là plugin bổ sung.[^1]

**Key Metrics từ Thực Tế:**

- **2-5x tăng engineering velocity** tại Coinbase[^1]
- **50% more code shipped** với >25% tăng PR volume tại một số công ty[^1]
- **14 ngày thay vì 4 tuần** để launch platform bất động sản[^2]
- **30% giảm time-to-market** cho MVP[^2]
- **20-25% giảm bug resolution cycles**[^2]

***

## PHẦN 1: HỆ THỐNG MULTI-AGENT (5 VAI AGENT)

### 1.1 Kiến Trúc Tổng Thể

#### Sequential Pipeline Pattern

Pattern phù hợp nhất cho Python pipeline với xử lý tuần tự qua 5 agent:[^3][^4]

**Ưu điểm:**

- Clear dependencies giữa các bước
- Progressive refinement qua từng stage
- Dễ debug từng agent riêng lẻ
- Tracking progress rõ ràng

**Nhược điểm:**

- Không parallel được
- Một agent fail → dừng cả pipeline
- Latency tích lũy qua các stage


#### Cấu Trúc Thư Mục Chuẩn

```
.cursor/
  commands/
    planner.md          # Agent 1
    implementer.md      # Agent 2  
    debugger.md         # Agent 3
    reviewer.md         # Agent 4
    test-writer.md      # Agent 5
  rules/
    python-pipeline.md  # Shared rules
```


### 1.2 Chi Tiết 5 Agent Roles

#### AGENT 1: PLANNER

**System Intent:** Biến yêu cầu thành actionable plan với verification steps

**File: .cursor/commands/planner.md**

```markdown
# Planner Agent

Bạn là Planning Agent cho Python multi-agent pipeline systems.

## Core Responsibilities
- Phân tách user requirements thành 5-10 bước cụ thể
- Xác định chính xác files cần modify/create
- Định nghĩa verification criteria cho mỗi bước
- Surface assumptions và risks ngay từ đầu

## Output Format

### Summary (≤5 dòng)
[Tóm tắt ngắn gọn về change]

### Plan Checklist
1. [ ] Mô tả bước
   - Files: `path/to/file.py`
   - Changes: Thay đổi gì cụ thể
   - Verify: `command to verify` hoặc assertion

2. [ ] Bước tiếp theo...

### Assumptions (≤5)
- Giả định 1
- Giả định 2

### Risks (≤5)  
- Risk 1: Mô tả + cách giảm thiểu
- Risk 2: Mô tả + cách giảm thiểu

## Constraints
- KHÔNG code implementation
- Focus vào WHAT changes, không phải HOW
- Mỗi bước phải independently verifiable
- Reference files bằng @file syntax
```

**Best Practices từ Research:**

- Giữ plan dưới 10 steps để tránh context bloat[^5]
- Pin contracts (types, schemas) vào một file để các agent khác reference[^5]
- Sử dụng checklist format để track progress[^6]
- Include explicit assumptions để avoid scope creep

***

#### AGENT 2: IMPLEMENTER

**System Intent:** Execute plan với minimal diff, không scope creep

**File: .cursor/commands/implementer.md**

```markdown
# Implementer Agent

Bạn là Code Implementation Agent focused on minimal, surgical changes.

## Core Principles
1. **Minimal Diff**: Chỉ thay đổi những gì cần thiết
2. **Scope Discipline**: Follow Plan chính xác, không feature expansion
3. **Pre-flight Check**: List files sẽ sửa TRƯỚC KHI coding

## Workflow

### Step 1: Pre-flight Declaration
Trước mọi code change, state:
- Files tôi sẽ modify: [`file1.py`, `file2.py`]
- Lý do cho mỗi modification
- Expected diff size (lines added/removed)

### Step 2: Implementation  
Cho mỗi file, provide:

```


# File: path/to/file.py

# Change: [Mô tả ngắn]

[Code patch với context]

```

### Step 3: Verification Commands
```


# Commands để verify implementation này

pytest tests/test_specific.py -v
python -m mypy path/to/file.py

```

### Step 4: What I Did NOT Change
Explicitly list:
- Files cố ý skip
- Features cố ý không add
- Scope boundaries tôn trọng

## Anti-Patterns to Avoid
- Thêm "nice-to-have" features
- Refactor unrelated code
- Thay đổi file structure không có trong plan
```

**Engineering Best Practices:**

- JSON schema (Pydantic) để validate tool inputs/outputs[^7]
- OpenTelemetry spans cho distributed tracing[^7]
- Include `run_id` để correlate logs across agents[^7]
- Structured logging với agent_name, trace_id, step

***

#### AGENT 3: DEBUGGER

**System Intent:** Root cause analysis với structured failure diagnosis

**File: .cursor/commands/debugger.md**

```markdown
# Debugger Agent

Bạn là Diagnostic Agent specialized in Python pipeline failures.

## Input Requirements
Provide:
1. Error logs/stack traces
2. @files suspected
3. Recent changes context (nếu có)

## Diagnostic Framework

### Phase 1: Error Classification
Categorize as:
- **Config Error**: Missing env vars, sai settings
- **Runtime Error**: Exception during execution
- **Logic Error**: Wrong output, incorrect behavior  
- **Data Error**: Invalid input/output schema

### Phase 2: Fault Localization
```


# Suspected location

File: path/to/agent_module.py
Function: specific_function_name
Line: 42-50

# Evidence

[Stack trace snippet hoặc log pattern]

```

### Phase 3: Quick Verification Steps
1. **Reproduce**: Minimal command để trigger error
2. **Isolate**: Test specific agent/function riêng lẻ
3. **Validate**: Check input/output tại failure point

### Phase 4: Fix + Enhanced Logging
```


# Minimal diff to fix

[Code patch]

# Enhanced logging để prevent recurrence

import logging
logger.info(
"agent_checkpoint",
extra={
"trace_id": trace_id,
"agent_name": "implementer",
"step": "pre_validation",
"input_schema": str(input_data)
}
)

```

## Debugging Tools Reference
- `pdb`: Set breakpoints cho agent states
- `pytest -vv --tb=long`: Detailed test failures
- `python -m trace`: Execution tracing
- OpenTelemetry: Distributed tracing
```

**Production Debugging Strategy** từ Reddit:[^7]

- Step-level tracing với `run_id` correlation
- Alert trên tool error rates, timeouts, retrieval hit ratios
- Fault-injection simulations để test error handling
- JSON schema validation tại agent boundaries

***

#### AGENT 4: REVIEWER

**System Intent:** Security, edge cases, và maintainability

**File: .cursor/commands/reviewer.md**

```markdown
# Reviewer Agent

Bạn là Code Quality & Security Reviewer cho Python pipelines.

## Review Taxonomy
Classify findings:
- 🔴 **BLOCKER**: Security issue, data loss risk, breaking change
- 🟡 **SHOULD**: Performance concern, maintainability debt
- 🟢 **NICE**: Code style, minor optimization

## Review Checklist

### Security (Priority 1)
- [ ] Input validation tại agent boundaries
- [ ] Không có secrets trong logs hoặc error messages
- [ ] SQL injection / command injection prevention
- [ ] Rate limiting cho external API calls

### Error Handling (Priority 2)
- [ ] Exceptions include context (trace_id, agent_name, step)
- [ ] Graceful degradation cho tool failures
- [ ] Retry logic với exponential backoff
- [ ] Circuit breaker pattern cho external dependencies

### Data Validation (Priority 3)
- [ ] Pydantic models cho agent inputs/outputs
- [ ] JSON schema validation cho tool contracts
- [ ] Type hints cho all public functions
- [ ] Edge case handling (empty lists, None values)

### Performance & Scalability
- [ ] Async operations where applicable
- [ ] Database query optimization (N+1 detection)
- [ ] Memory profiling cho large data processing
- [ ] Caching strategy cho expensive operations

### Code Quality
- [ ] Single Responsibility Principle per agent
- [ ] Clear separation of concerns
- [ ] Docstrings cho agent interfaces
- [ ] Không hardcoded values (use config)

## Output Format

### Critical Issues (🔴 BLOCKER)
```


# Issue: [Mô tả]

# Location: file.py:42

# Risk: [Security/Data integrity concern]

# Fix:

[Suggested code patch]

```

### Recommendations (🟡 SHOULD)
- Issue description
- Why it matters  
- Suggested improvement

### Minor Improvements (🟢 NICE)
- Quick wins cho readability
```

**Modern Code Review Practices**:[^8]

- Focus on correctness, efficiency, readability
- Comment trực tiếp trên code lines với context
- Suggest specific patches, không chỉ point out problems

***

#### AGENT 5: TEST WRITER

**System Intent:** Smoke tests + minimal test harness cho projects chưa có test suite

**File: .cursor/commands/test-writer.md**

```markdown
# Test Writer Agent

Bạn là Test Automation Agent cho Python pipelines without existing test infrastructure.

## Context
Project hiện tại có **no test suite**. Job của bạn là bootstrap minimal, high-value testing.

## Testing Strategy: Smoke Tests First

### Priority 1: Critical Path Smoke Tests (2-4 tests)
Focus on:
- Happy path: End-to-end pipeline execution
- Agent boundaries: Input/output validation
- Error scenarios: Graceful failure handling

### Priority 2: Test Harness Setup
```


# tests/conftest.py

import pytest

@pytest.fixture
def mock_agent_context():
"""Minimal context cho agent testing"""
return {
"trace_id": "test-123",
"config": load_test_config(),
"logger": setup_test_logger()
}

@pytest.fixture
def mock_tool_responses():
"""Mock external tool calls"""
\# Return fixtures for API responses, DB queries, etc.

```

## Test Template: AAA Pattern

```

import pytest
from your_pipeline import PlannerAgent, ImplementerAgent

class TestPlannerAgent:
"""Smoke tests for Planner agent"""

    def test_planner_generates_valid_plan(self, mock_agent_context):
        # Arrange
        user_request = "Add logging to payment processor"
        planner = PlannerAgent(context=mock_agent_context)
        
        # Act
        plan = planner.create_plan(user_request)
        
        # Assert
        assert len(plan.steps) >= 3
        assert len(plan.steps) <= 10
        assert all(hasattr(step, 'verify_command') for step in plan.steps)
        assert plan.summary is not None
    
    def test_planner_handles_vague_requests(self, mock_agent_context):
        # Arrange
        vague_request = "make it better"
        planner = PlannerAgent(context=mock_agent_context)
        
        # Act & Assert
        with pytest.raises(ValueError, match="insufficient context"):
            planner.create_plan(vague_request)
    class TestAgentIntegration:
"""End-to-end smoke test"""

    @pytest.mark.slow
    def test_full_pipeline_execution(self, mock_agent_context):
        # Arrange
        pipeline = AgentPipeline(
            agents=[PlannerAgent, ImplementerAgent, ReviewerAgent]
        )
        
        # Act
        result = pipeline.execute(
            request="Add error handling to data loader",
            context=mock_agent_context
        )
        
        # Assert
        assert result.status == "success"
        assert result.trace_id == mock_agent_context["trace_id"]
        assert len(result.agent_outputs) == 3
    ```

## Verification Commands

### Run tests
```

pytest tests/ -v --tb=short

# Run only smoke tests

pytest tests/ -m smoke -v

# Run with coverage

pytest tests/ --cov=your_pipeline --cov-report=html

```

### Test Configuration
```


# pytest.ini

[pytest]
markers =
smoke: Smoke tests for critical paths
integration: Full pipeline tests
slow: Tests that take >5 seconds

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

```

## Output Deliverables
1. **Test files**: `tests/test_agent_name.py`
2. **Fixtures**: `tests/conftest.py`
3. **Run commands**: Copy-pastable bash commands
4. **Coverage baseline**: Target >60% cho agent logic
```

**Advanced Testing Patterns**:[^9][^10]

- LangSmith/LangFuse cho LLM-specific testing
- Pytest parametrization cho multiple input scenarios
- Automated failure analysis với AI agents analyzing test results

***

### 1.3 Production Best Practices

#### Debugging Strategy trong Production[^7]

**Structured Logging:**

```python
logger.info(
    "agent_execution",
    extra={
        "trace_id": trace_id,
        "run_id": run_id,
        "agent_name": "planner",
        "step": "plan_generation",
        "duration_ms": duration,
        "input_tokens": tokens,
        "output_size": len(plan)
    }
)
```

**Monitoring \& Alerting:**

- Tool error rates > 5%
- Timeouts > 30s
- Retrieval hit ratios < 70%
- Context window utilization > 90%

**Fault Injection Testing:**

```python
@pytest.fixture
def simulate_api_timeout():
    """Simulate external API timeout"""
    with mock.patch('requests.get', side_effect=Timeout()):
        yield

def test_agent_handles_timeout(simulate_api_timeout, agent):
    result = agent.execute(request="task")
    assert result.status == "failed"
    assert "timeout" in result.error_message.lower()
```


***

## PHẦN 2: CURSOR BEST PRACTICES - TOÀN BỘ HỆ THỐNG

### 2.1 Configuration \& Setup

#### 2.1.1 Global AI Rules[^11]

**Location:** Settings → Cursor Settings → Rules → User Rules

**Purpose:** Universal guidelines across tất cả projects

**Example Global Rules:**

```markdown
# Global Cursor Rules

## Code Style
- Prefer functional code over imperative where possible
- TypeScript/JavaScript: omit semi-colons
- Use Tailwind CSS for styling
- British-English spelling over American-English
- date-fns for any date manipulation

## Code Quality
- Always provide proper type annotations
- Do not use `any` unless explicitly allowed
- Comment new logic briefly if not self-explanatory
- Keep function/variable names descriptive

## Safety
- DO NOT remove or break existing code
- DO NOT modify logic unless necessary
- Only extend or add new code with minimal changes
```

**Khi nào cần Global Rules:**

- Code style preferences cá nhân
- Language conventions
- Framework preferences
- Spelling conventions
- Reusable across mọi project

***

#### 2.1.2 .cursorrules File[^12][^13][^11]

**Location:** Project root directory

**Purpose:** Project-specific context và constraints

**Example Structure:**

```markdown
# Project: FinTech Platform - Payment Processing Module

Đây là core payment processing module cho fintech platform, xử lý transactions,
fraud detection, và settlement với các ngân hàng.

## Tech Stack
- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL 15 + Redis 7
- **Message Queue**: RabbitMQ
- **ML**: scikit-learn, TensorFlow
- **Deployment**: Docker + Kubernetes on AWS

## Architecture Patterns
- Microservices architecture
- Event-driven với RabbitMQ
- CQRS pattern cho transaction processing
- Repository pattern cho database access

## Code Conventions

### File Structure
```

src/
api/          \# FastAPI endpoints
services/     \# Business logic
models/       \# Pydantic models
repositories/ \# Database access
events/       \# Event handlers
utils/        \# Helper functions
tests/
unit/
integration/
e2e/

```

### Naming Conventions
- Classes: PascalCase (UserService, PaymentRepository)
- Functions: snake_case (process_payment, validate_user)
- Constants: UPPER_SNAKE_CASE (MAX_RETRY_COUNT)
- Private methods: _snake_case_with_underscore

### Error Handling
- Always use custom exceptions from `exceptions.py`
- Include context: transaction_id, user_id, timestamp
- Log errors với appropriate level (ERROR for failures, WARNING for retries)
- Never expose sensitive data trong error messages

### Security Requirements
- No secrets in code or logs
- Validate all inputs tại API boundaries
- Use parameterized queries (no SQL injection)
- Encrypt sensitive data at rest
- Rate limiting trên all public endpoints

### Testing Requirements
- Minimum 80% coverage cho core business logic
- All API endpoints phải có integration tests
- Mock external services trong unit tests
- Use factories cho test data (factories.py)

### Performance Guidelines
- Database queries: use proper indexes
- Cache frequently accessed data trong Redis (TTL 5 minutes)
- Async operations cho I/O bound tasks
- Pagination cho list endpoints (max 100 items)

### Logging Standards
```

logger.info(
"payment_processed",
extra={
"transaction_id": tx_id,
"amount": amount,
"currency": currency,
"duration_ms": duration
}
)

```

## Business Logic Notes

### Payment Flow
1. Client initiates payment request
2. Validate user and payment method
3. Fraud detection check (ML model)
4. Reserve funds (pending status)
5. Submit to bank/payment gateway
6. Handle async callback
7. Settle or refund based on result

### Fraud Detection
- Model trained trên historical transaction data
- Features: amount, location, time, user history
- Threshold: 0.7 for manual review, 0.9 for auto-block
- Re-train model weekly với new data

### Settlement Rules
- Daily batch at 2 AM UTC
- Retry failed transactions 3 times (exponential backoff)
- Manual review cho amounts >$10,000
- Refunds processed within 24 hours

## Common Commands
```


# Run tests

pytest tests/ -v --cov=src

# Start local dev

docker-compose up -d
uvicorn src.main:app --reload

# Database migrations

alembic upgrade head

# Format code

black src/ tests/
isort src/ tests/

```

## External Dependencies
- Stripe API: Payment processing
- Plaid API: Bank account verification  
- AWS SES: Email notifications
- Sentry: Error tracking
```

**Best Practices cho .cursorrules:**

- Update iteratively khi project evolves[^14]
- Include business logic hints không obvious[^11]
- Reference specific patterns trong codebase
- Document common pitfalls và solutions
- Keep under 1000 lines để avoid context bloat

***

#### 2.1.3 Security Configuration[^15][^16][^17]

**Privacy Mode** - CRITICAL cho Enterprise[^16]

**Location:** Settings → Privacy Mode → Enable

**How it works:**

- Requests route through separate replicas với logging disabled
- Zero data retention agreements với OpenAI, Anthropic, Google
- Team-level enforcement (Business tier)
- Verification every 5 minutes, failsafe to privacy mode

**When to use:**

- Proprietary code
- Financial data
- Healthcare information
- Government projects
- Any sensitive IP

***

**YOLO Mode / Auto-Run**[^18][^19][^20]

**Location:** Settings → Features → Enable Auto Run (formerly YOLO)

**Configuration Example:**

```markdown
# YOLO Mode Settings

## Allow List
- Test commands: vitest, npm test, nr test, pytest
- Build commands: build, tsc, npm run build
- File operations: touch, mkdir, mv, cp
- Linting: eslint, ruff, mypy
- Format: prettier, black

## Deny List  
- Deployment: git push, docker push, kubectl apply
- Database: psql, mysql, mongosh, alembic upgrade
- File deletion: rm -rf, rmdir
- Network: curl, wget, ssh
- Installation: npm install, pip install
```

**Use Cases:**

- Iterative testing until all pass[^18]
- Auto-fix linting errors
- Build verification loops
- Test-driven development workflow

**Warning:** Không bật YOLO cho production deployments hoặc database operations[^15]

***

**Security Best Practices Checklist**[^17][^21][^15]

**1. Secret Management**

- ✅ Use .cursorignore để block .env files
- ✅ Environment variables thay vì hardcode
- ✅ Secret scanners: Secretlint, Gitleaks
- ✅ Pre-commit hooks để prevent leaks
- ✅ AWS Secret Manager / Azure Key Vault

**2. Context Sanitization**

- ✅ Close sensitive files trước khi prompt
- ✅ Redact logs và stack traces
- ✅ Strip customer data từ examples
- ✅ Remove internal URLs và API endpoints

**3. Dependency Validation**

- ✅ Vet every AI-suggested package
- ✅ Check GitHub activity và maintainers
- ✅ Run `npm audit` / `safety check`
- ✅ Use socket.dev cho risk analysis

**4. Workspace Trust**[^22]

- ✅ Enable Workspace Trust trong settings
- ✅ Audit repos trước khi open
- ✅ Check suspicious .vscode/tasks.json files
- ✅ Limit environment secrets available to IDE

**5. Code Review**

- ✅ Never commit AI code without review
- ✅ Branch protection rules
- ✅ PR checklist enforcement
- ✅ Automated security scanning trong CI

***

### 2.2 Workflow Optimization

#### 2.2.1 Mode Selection[^23][^24][^11]

**Chat Mode (Cmd/Ctrl+L)**

**Use cases:**

- High-level questions và brainstorming
- Understanding complex codebases
- Documentation research
- Architecture discussions
- KHÔNG make code changes

**Best for:**

- "Explain how authentication works trong this codebase"
- "What's the best approach to implement caching?"
- "Summarize the payment flow"

***

**Agent Mode (Cmd/Ctrl+I)** - DEFAULT cho coding[^23][^11]

**Use cases:**

- Complex, multi-step tasks
- Cross-file refactoring
- Feature implementation
- Bug fixes with testing
- Autonomous execution

**Best for:**

- "Implement user registration with email verification"
- "Refactor payment service to use async/await"
- "Add error handling across all API endpoints"
- "Migrate from Class components to Hooks"

**Agent Mode Settings:**

- Enable YOLO for auto-testing
- Set appropriate allow/deny lists
- Use with clear, detailed prompts
- Include relevant @file references

***

**Deprecated: Edit Mode**

- Being phased out
- Use Agent mode instead

***

#### 2.2.2 Context Management[^25][^26]

**The @ Symbol System - MASTER THIS**[^27][^28][^25]

**Core @ Symbols:**


| Symbol | Purpose | Example |
| :-- | :-- | :-- |
| `@Files` | Reference specific files | `@src/utils/auth.py` |
| `@Folders` | Include entire directories | `@src/services/` |
| `@Code` | Reference symbols | `@calculateTotal` function |
| `@Docs` | Library documentation | `@docs fastapi` |
| `@Git` | Git history | Recent commits |
| `@Codebase` | Entire project | Use sparingly |
| `@Web` | External docs | `@Web latest Next.js docs` |
| `@Past Chats` | Previous sessions | Summarized history |
| `@Recent Changes` | Latest modifications | Git diff |
| `@Lint Errors` | Linting issues | Current errors |

**Context Best Practices:**

**1. Maximum Context:** 20,000 tokens limit[^29][^30]

**2. Agent Mode Reading:**[^25]

- First 250 lines by default
- Extends to 500 lines if needed
- Max 100 lines per search

**3. Large Files (>600 lines):**[^31][^25]

- Explicitly @ relevant files
- Two-step workaround:

1. Ask simple question first
2. Then paste full file content

**4. Complex Tasks = MORE Context**[^32]

- Mathematical/conceptual/theoretical complexity
- Backend work, database tasks
- Week-long chats possible với Chat Summarization
- Frontend work: more amenable to new chats

**5. Quick File

```
# Instead of @-ing multiple files one by one:
1. Search for relevant files
2. Open them in editor
3. Use: /reference open editors
```


***

**Context Optimization Strategies**

**For Large Codebases:**[^33]

```markdown
# Strategy 1: Master Architecture Doc
Create: docs/ARCHITECTURE.md

Contents:
- System overview diagram (ASCII art)
- Module relationships
- Data flow
- Key design decisions
- Common patterns

Then: Always @docs/ARCHITECTURE.md trong prompts
```

**For Multi-Session Projects:**[^34]

```markdown
# Strategy 2: Project Memory File  
Create: .context/project_memory.md

Contents:
- Current sprint goals
- Completed features
- Known issues
- Technical decisions
- Next steps

Update: After each session
Reference: At start of new session
```

**For Team Projects:**[^34]

```markdown
# Strategy 3: Codebase Structure
Create: docs/codebase_structure.md

Contents:
```

project/
├── src/
│   ├── api/         \# REST endpoints, OpenAPI specs
│   ├── services/    \# Business logic, no DB access
│   ├── models/      \# Pydantic models for validation
│   └── repositories/\# Database access layer only
├── tests/
│   ├── unit/        \# Fast, isolated tests
│   └── integration/ \# DB + external service tests
└── scripts/         \# Deployment, migrations

```

Rules:
- Services never import from repositories directly
- All DB queries through repositories
- Models defined in models/, reused everywhere
```

Update: When files/folders added, modified, removed

```

---

**Summarization**[^12][^94]

**Automatic Summarization:**
- Triggers khi reaching context window limit
- Lossy compression - some details lost[^58]
- Works well for frontend, less ideal for complex backend[^58]

**Manual Summarization:**
```


# In chat:

/summarize

# Frees up context space without new chat

# Useful when mid-flow và don't want to restart

```

**When Summarization Works Well:**
- Long conversations về same feature
- Accumulated decisions và rationale
- Iterative refinement tasks

**When to Start New Chat Instead:**
- Switching to unrelated task
- Stuck in loop với no progress
- After major milestone completion

---

#### 2.2.3 Conversation Management[^44][^54][^58]

**Critical Decision: New Chat vs Continue?**

**START NEW CHAT when:**[^44]
- Context approaching limit (>18K tokens)
- AI stuck in loop, no progress after 3 attempts
- Switching to completely different feature
- After completing và verifying milestone
- Frontend work với clear boundaries

**CONTINUE CHAT when:**[^58]
- Complex mathematical/theoretical work
- Backend with intricate dependencies
- Building up architectural understanding
- Week-long feature development
- Context loss would be expensive

**Data Point:** Một user báo cáo chats kéo dài 1 tuần cho complex database work vẫn effective với Chat Summarization[^58]

---

**Chat Organization Strategies**[^57]

**1. Multiple Specialized Chats:**
```

Chat: "API Development"

- All API-related work
- Reference: @src/api/

Chat: "Database Schema"

- Schema changes
- Migrations
- Reference: @alembic/

Chat: "Frontend Components"

- UI components
- Styling
- Reference: @src/components/

```

**2. Model-Specific Chats:**
```

Chat: "Architecture Planning" - Claude Opus
Chat: "Implementation" - Claude Sonnet
Chat: "Bug Fixing" - GPT-4o
Chat: "Testing" - GPT-3.5 (faster, cheaper)

```

**3. Phase-Based Chats:**
```

Chat: "Sprint 1 - User Auth"
Chat: "Sprint 2 - Payment Integration"
Chat: "Sprint 3 - Admin Dashboard"

```

---

#### 2.2.4 Prompting Strategy[^43][^44]

**Anatomy of Excellent Prompts**

**❌ BAD Prompts:**
```

"Make this better"
"Fix everything"
"Optimize the code"
"Add error handling"

```

**✅ GOOD Prompts:**
```

"Add TypeScript types to the @calculateTotal function in
@src/utils/math.ts. Don't change the existing logic.
Ensure return type matches calling code in @src/api/orders.ts"

"Refactor the @UserService class in @src/services/user.py
to use async/await. Update all calling code in @src/api/users.py.
Run tests after changes and fix until pytest passes."

"Add error handling to @src/api/payments.py for these scenarios:

1. Network timeout (retry 3 times)
2. Invalid payment method (return 400)
3. Insufficient funds (return 402)
Include logging với transaction_id và error details."
```

**Prompt Template Structure:**
```

[CONTEXT]
@relevant/files.py
Current state: [brief description]

[TASK]
What to do: [specific action]
How to do it: [constraints, approach]

[VERIFICATION]
Success criteria: [measurable outcomes]
Commands to verify: [exact commands]

[CONSTRAINTS]
Do NOT: [what to avoid]
Must preserve: [existing behavior]

```

---

**Test-Driven Development Workflow**[^40]

**The Magic Prompt:**
```

Write tests first for this functionality, then implement the code,
then run the tests and iteratively fix until all tests pass.

Functionality: [describe what to build]

Test scenarios:

1. Happy path: [expected behavior]
2. Edge case: [boundary condition]
3. Error case: [failure scenario]

@relevant/files

```

**Why This Works:**
- Forces AI to define expected behavior upfront
- Provides concrete success criteria
- With YOLO mode: Auto-iterates until green
- Guarantees correctness of implementation

**Real Example:**
```

Write tests first for converting Markdown to HTML, then implement,
then run tests until passing.

Test scenarios:

1. Simple text: "Hello" → "<p>Hello</p>"
2. Headers: "\# Title" → "<h1>Title</h1>"
3. Links: "[text](url)" → "<a href='url'>text</a>"
4. Code blocks: ```code```
5. Nested elements: "\# **Bold** title"

Requirements:

- Handle all basic Markdown syntax
- Sanitize HTML to prevent XSS
- Return empty string for null input

```

Result: AI writes 5+ tests, implements, runs, fixes bugs, iterates until 100% pass[^40]

---

**Debugging with Logs Strategy**[^40]

**Step-by-step Workflow:**

**1. Initial Prompt:**
```

Add detailed logging to @src/services/payment.py to help debug
why transactions are failing.

Add logs at these points:

- Input validation
- Before calling external API
- After API response
- Before database commit
- Final result

Format: JSON with timestamp, transaction_id, step, data

```

**2. Run và Collect Logs:**
```

python -m src.main

# Copy log output

```

**3. Feed Back to Cursor:**
```

Here are the logs from a failed transaction:

[paste logs]

Based on these logs:

1. What is the root cause?
2. Which step is failing?
3. What's the fix?
4. Update the code with the fix.
```

**4. Verify:**
```

Run the same transaction again and confirm it works.
If it fails, add more logs and iterate.

```

---

**Multi-Agent Workflow Prompting**[^46][^51]

**Setup: PM/Tech Lead + AI as Developer**

**Step 1: Create PRD**
```


# Product Requirements Document

## Goal

Implement real-time notification system cho user events

## Tech Stack

- FastAPI backend
- WebSocket connections
- Redis pub/sub
- PostgreSQL for persistence


## Stories

1. WebSocket endpoint setup
2. Redis pub/sub integration
3. Notification delivery logic
4. Persistence layer
5. Client reconnection handling

## Success Criteria

- <100ms latency for notifications
- Handle 10K concurrent connections
- Zero message loss
- Full test coverage

```

**Step 2: Agent Creates Story File**
```

Create detailed story file for Story \#1: WebSocket endpoint setup

Include:

- Technical approach
- Files to create/modify
- Dependencies needed
- Testing strategy
- Verification steps

Wait for my approval before implementing.

```

**Step 3: Review và Approve**
```

[Review story file]

Approved. Proceed with implementation using TDD.
Run tests after each change.

```

**Step 4: Push Changes**
```

All tests passing. Push changes with descriptive commit message.
Update story file với status.

```

**Cost Savings:**[^46][^51]
- Detailed PRD → fewer iterations
- Story-by-story → granular control
- Manual simple commands → save tool usage
- Heavy planning phase → reduced execution cost

---

### 2.3 Model Selection Strategy[^97][^99]

#### Model Characteristics

**Claude Family:**

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **Sonnet 4** | Day-to-day coding | Medium | Fast |
| **Opus 4** | Architecture, complex logic | High (8 req/prompt) | Slow |
| **Haiku** | Boilerplate, simple tasks | Low | Very Fast |

**Strengths:**
- Understanding large codebases
- "To the point" vs GPT
- Simplifying complex code
- Following complex instructions

**Weaknesses:**
- May refuse some tasks GPT attempts
- Opus very expensive
- Less factual grounding than GPT

---

**GPT Family:**

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **GPT-4o** | Default cho most tasks | Medium | Fast |
| **GPT-4** | Nuanced refactoring | High | Slow |
| **GPT-3.5** | Boilerplate generation | Low | Very Fast |
| **o1/o3** | Deep reasoning | Very High | Very Slow |

**Strengths:**
- Strong factual grounding
- Deep architectural restructuring
- API documentation
- Design patterns
- Complex logical reasoning

**Weaknesses:**
- Can be "lazy" với incomplete code
- More expensive than Sonnet
- Sometimes verbose

---

**Gemini Family:**

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **2.5 Flash** | Day-to-day alternative | Low | Very Fast |
| **2.5 Pro** | Complex exploration | High | Slow |

**Strengths:**
- Good design capabilities
- Multimodal support
- Strong reasoning

**Weaknesses:**
- Inconsistent code edits reported[^125]
- Sometimes claims completion without doing it

---

#### Selection Decision Tree[^97][^99]

```

START
│
├─ Simple boilerplate? → GPT-3.5 / Haiku
│
├─ Day-to-day feature? → Claude Sonnet / GPT-4.1 / Gemini Flash
│
├─ Multi-file refactor? → Claude Sonnet / GPT-4o + Agent mode
│
├─ Architecture design? → Claude Opus / GPT-4o + @Docs
│
├─ Stuck/spinning? → SWITCH MODELS (Claude ↔ GPT)
│
├─ Privacy-sensitive? → Local model / DeepSeek
│
├─ Docs/screenshots? → GPT-4o (multimodal)
│
└─ Deep reasoning? → o1 / o3 (expensive!)

```

---

#### Auto Mode Considerations[^98]

**How Auto Works:**
- Intelligently picks premium model based on query
- Usually Claude 3.5 or 3.7
- Can switch mid-project (LOSES CONTEXT!)

**Best Practice:**
```

Settings → Models → Unselect unwanted models

This ensures Auto only chooses from your preferred models,
preventing context loss from provider switches.

```

**Cost Consideration:**
- Switching providers = full context resend
- Cached tokens only work with same provider
- Keep related work on same model
- New chat for unrelated small tasks

---

### 2.4 Keyboard Shortcuts[^102][^108][^111]

#### Essential Daily Shortcuts

**Navigation (Use 50+ times/day):**
```

Cmd+P         Quick file open (type few letters, jump)
Cmd+Shift+O   Go to symbol in file
Ctrl+G        Go to line (from stack traces)
Cmd+T         Go to symbol in workspace
Cmd+Shift+E   Explorer focus
Cmd+Shift+F   Global search

```

**AI Interaction (Core workflow):**
```

Cmd+K         Inline edit - FASTEST for small changes
Cmd+L         AI Chat - discussions only
Cmd+I         Agent mode - DEFAULT for coding
Tab           Accept autocomplete
Esc           Close inline edit
Cmd+.         Code actions menu

```

**Editing (Speed up by 2-3x):**
```

Cmd+D             Select next occurrence
Cmd+Shift+L       Select ALL matches
Option+Click      Add cursor
Cmd+D repeatedly  Multi-select same word
Option+Up/Down    Move line
Shift+Option+Up   Copy line
Cmd+/             Toggle comment
Shift+Option+F    Format document
Cmd+]             Indent
Cmd+[             Outdent
F2                Rename symbol everywhere

```

**Context Management:**
```

@                     Start file reference
Cmd+Enter             Attach entire codebase
/reference open       All open files
Cmd+Shift+J           Cursor Settings

```

---

**Productivity Workflow Example:**

**Scenario: Refactor function across 5 files**

```

1. Cmd+Shift+F → Search function name
2. Open all result files
3. Cmd+I → Agent mode
4. Type: "Refactor @functionName in /reference open editors
to use async/await. Update all calling code."
5. Review diffs → Accept
6. Cmd+K in terminal → "run tests"
7. If fail: Agent auto-fixes with YOLO
8. F2 → Rename if needed
9. Cmd+/ → Add comments
10. Shift+Option+F → Format all
```

**Time saved:** 30 minutes → 5 minutes

---

### 2.5 Testing & Verification[^40][^44]

#### Test-First Workflow Pattern

**Standard Workflow:**
```

Prompt:
"Write tests first for [functionality], then implement code,
then run tests and iteratively fix until all pass.

Test cases:

1. [happy path]
2. [edge case]
3. [error case]

@relevant/files

Requirements:

- [specific constraints]
"

With YOLO enabled:
→ AI writes tests
→ AI implements code
→ AI runs tests
→ AI fixes failures
→ AI re-runs
→ Repeats until green ✅

Result: Guaranteed correctness

```

---

#### Pre-PR Verification Flow[^40]

**Setup:**
```

// package.json
{
"scripts": {
"pre-pr": "npm run typecheck \&\& npm run lint \&\& npm run format-check \&\& npm run test:unit"
}
}

```

**End of Session Prompt:**
```

I'm done with my changes. Run `npm run pre-pr` and fix any
issues until everything passes. Iterate automatically.

@modified-files

```

**Result:** Clean PR, no CI failures, saves reviewer time

---

#### Debugging with Logs Pattern[^40]

**Phase 1: Add Instrumentation**
```

Add detailed logging to @problematic/file.py to debug [issue].

Log at these checkpoints:

- Input validation
- Before external calls
- After responses
- Before state changes
- Final output

Format: Structured JSON with trace_id, step, data

```

**Phase 2: Collect Evidence**
```


# Run failing scenario

python src/main.py

# Copy logs

```

**Phase 3: Root Cause Analysis**
```

Here are logs from failed execution:

[paste logs]

Analyze:

1. Which step is failing?
2. What's the root cause?
3. Proposed fix?

Then implement fix and re-run until success.

```

---

### 2.6 Real-World Case Studies

#### Case Study 1: Stripe[^116]

**Scale:**
- 70% of engineers use Cursor
- Company-wide deployment

**Results:**
- Meaningful gains in day-to-day development
- Faster large-scale migrations
- Increased debugging rate
- Faster onboarding

**Quote:** "We spend more on R&D than any other undertaking, and there's significant economic outcomes when making that process more efficient."

---

#### Case Study 2: Coinbase[^116]

**Adoption:**
- Every Coinbase engineer used Cursor by Feb 2025
- Preferred IDE for most developers

**Results:**
- **2-5x increase in engineering velocity**
- Better tech debt handling
- Code refactors faster
- Unit testing improved
- **Single engineers refactoring codebases in days instead of months**

**Impact:** "By February 2025, every Coinbase engineer had utilized Cursor, which has become the preferred IDE for most of our developers."

---

#### Case Study 3: Real Estate Platform[^118]

**Challenge:**
- 14-day deadline thay vì 4 weeks
- Fixed budget
- Busy season launch critical

**Solution:**
- Cursor AI cho tedious tasks
- Product management broke into bite-sized tasks
- Encoded naming, tone, approval criteria

**Results:**
- ✅ **Launched in 14 days** (2 weeks early!)
- ✅ **Tour bookings +18%** month-over-month
- ✅ **60% reduction** in listing time
- ✅ **30% cut in time-to-market** for MVPs
- ✅ **20-25% shorter bug resolution cycles**

**Key Insight:** "Cursor automates repetitive edits while internal team protects brand, compliance, and customer experience."

---

#### Case Study 4: Portfolio Company[^116]

**Metrics:**
- >25% increase in PR volume
- >100% increase in average PR size
- **~50% more code shipped overall**

**Use Cases:**
- Accelerating product roadmaps
- Shipping features faster
- Handling demand surges
- Maintaining quality while scaling

---

### 2.7 Pricing & Cost Management[^101][^104][^107]

#### Pricing Plans Comparison

| Plan | Price | Fast Requests | Auto | Use Case |
|------|-------|---------------|------|----------|
| **Hobby** | Free | 50 slow | Limited | Learning, exploration |
| **Pro** | $20/mo | ~500 | Unlimited | Solo devs |
| **Pro+** | $60/mo | ~1500 | Unlimited | Power users |
| **Ultra** | $200/mo | ~10,000 | Unlimited | Heavy daily use |
| **Teams** | $40/user | ~500 | Unlimited | Team collaboration |
| **Enterprise** | Custom | Custom | Unlimited | Large organizations |

#### Cost Optimization Strategies[^46][^51][^58]

**1. Model Selection:**
```

Simple tasks → GPT-3.5 / Haiku (cheap)
Medium tasks → Sonnet / GPT-4.1 (balanced)
Complex only → Opus / o1 (expensive)

❌ Don't use Opus for "make button bigger"
✅ Use Opus for "design entire payment architecture"

```

**2. Context Management:**
```

❌ Don't: @Codebase for every prompt
✅ Do: @ specific files needed

❌ Don't: Continuous chat for unrelated tasks
✅ Do: New chat for new context

❌ Don't: Minimize context for complex work
✅ Do: Provide full context upfront to avoid re-work

```

**3. Agent Mode Usage:**[^46]
```

Manual: Simple scriptable commands
→ Run in terminal yourself
→ Saves tool usage credits

Agent: Complex multi-step tasks
→ Let Agent automate
→ Worth the credits

```

**4. Planning Phase Investment:**[^51]
```

Spend 20% time on detailed PRD
→ Saves 50% execution credits
→ Fewer iterations needed
→ Better results first try

```

**5. Testing Strategy:**
```

YOLO with allow-list:
→ Tests run automatically
→ Iterates until green
→ But only "safe" commands

Manual verification:
→ For deployment steps
→ Database operations
→ Cost-sensitive operations

```

---

### 2.8 Common Pitfalls & Solutions[^43][^44][^122][^125]

#### Pitfall 1: Huge File All At Once

**Problem:**
```

AI struggles with 2000+ line files
Makes unrelated changes
Loses context mid-edit

```

**Solution:**
```

Break into smaller files:

- services/user_service.py (200 lines)
- services/payment_service.py (200 lines)
- services/notification_service.py (200 lines)

Then:
@services/user_service.py for targeted changes

```

---

#### Pitfall 2: Vague Prompts

**Problem:**
```

"Make this better"
"Fix the bugs"
"Optimize everything"

→ AI guesses wrong
→ Makes unwanted changes
→ Wastes tokens

```

**Solution:**
```

"Optimize @calculateTotal function in @utils/math.py
specifically for:

1. Reduce time complexity from O(n²) to O(n)
2. Add memoization for repeated calculations
3. Use vectorization for numpy arrays

Verify: Run benchmark script and ensure >2x speedup

```

---

#### Pitfall 3: Trusting AI Blindly

**Problem:**
```

AI claims: "I've implemented the feature"
Reality: Half-finished, bugs, wrong approach

```

**Solution:**
```

1. Always review diffs before accepting
2. Run tests immediately
3. Use git commits as checkpoints
4. Ask: "Are you sure? Show me the verification."
```

---

#### Pitfall 4: Long Conversation Hell[^44]

**Problem:**
```

Chat at 18K+ tokens
AI starts forgetting earlier decisions
Makes contradictory changes
Suggests already-implemented code

```

**Solution:**
```

Watch context meter
When >80%:

1. /summarize if continuing same task
2. Start new chat if switching focus
3. Reference @architecture.md for continuity
```

---

#### Pitfall 5: Not Using Version Control[^44]

**Problem:**
```

AI makes breaking changes
No easy way back
Panic ensues

```

**Solution:**
```

Commit early, commit often:

Before starting:
git commit -m "Before AI refactor"

After each working state:
git commit -m "Working: added feature X"

If AI breaks:
git reset --hard HEAD~1

```

---

#### Pitfall 6: Security Ignorance[^60][^68]

**Problem:**
```

.env file open → AI reads secrets
Logs pasted → API keys leaked
Dependency suggested → malware installed

```

**Solution:**
```

Security Checklist:
☑ .cursorignore includes .env*
☑ Close sensitive files before prompting
☑ Redact logs before pasting
☑ Vet every npm package suggested
☑ Enable Privacy Mode for proprietary code
☑ Review diffs for hardcoded secrets

```

---

#### Pitfall 7: Wrong Model for Task[^97]

**Problem:**
```

Using Opus for "fix typo" → Waste \$\$\$
Using GPT-3.5 for "design architecture" → Bad results
```

**Solution:**

```
Quick Reference:

Typo/simple → Haiku/GPT-3.5
Feature → Sonnet/GPT-4o
Refactor → Sonnet/GPT-4o  
Architecture → Opus/GPT-4
Stuck → Switch models
```


---

### 2.9 Cursor vs Competitors

#### Cursor vs GitHub Copilot[^121][^124][^127][^130]

**Copilot Strengths:**

- ✅ Faster inline completions
- ✅ Better VS Code ecosystem compatibility
- ✅ \$10/month (cheaper)
- ✅ Unlimited usage under fair use
- ✅ Sometimes works offline

**Cursor Strengths:**

- ✅ Project-wide context understanding
- ✅ Agent mode for complex tasks
- ✅ Multi-file refactoring
- ✅ Composer for coordinated changes
- ✅ Better for large codebases[^133]

**Performance Comparison:**[^130]


| Task | Cursor | Copilot | Winner |
| :-- | :-- | :-- | :-- |
| Code refactoring | More scalable, declarative | Faster but less elegant | Cursor |
| TypeScript conversion | Clean with comments | Nearly identical | Tie |
| Boilerplate | Good | Excellent | Copilot |
| Multi-file changes | 90% in one pass | Requires babysitting | Cursor |
| Simple edits | Slightly slower | Very fast | Copilot |

**Cost Reality Check:**[^127]

```
Copilot: $10/month unlimited
Cursor: $20/month + $20 credits pool
        → Can exceed $40 if heavy usage
        → Need to manage credits
```

**Verdict:**

- **Copilot for:** File-level tasks, autocomplete, budget-conscious
- **Cursor for:** Large codebases, refactors, complex projects

---

### 2.10 Limitations \& Challenges[^122][^125][^128]

#### Critical Limitations to Understand

**1. Large Codebase Struggles**[^122][^128]

**Problem:**

- Context loss in 100K+ line projects
- Slow processing times
- Misses dependencies
- Requires manual intervention

**Mitigation:**

- Break into modules
- Use architecture docs
- Explicit file references
- Don't rely on @Codebase alone

---

**2. Legacy Project Difficulties**[^125]

**Problem:**

- Trouble maintaining context
- Forgets earlier conversation parts
- Requires repeated clarification
- Less reliable for older systems

**Mitigation:**

- Detailed .cursorrules with legacy patterns
- More specific prompts
- Shorter, focused chats
- Manual documentation

---

**3. Multi-File Coordination**[^122]

**Problem:**

- Modifies one file, forgets dependencies
- Inconsistent logic across files
- Refactoring inefficiencies

**Mitigation:**

- Explicit list of all affected files
- Use Agent mode với @Files for each
- Verification step: "Check all files changed"

---

**4. Inconsistent Code Edits**[^125]

**Problem (especially Gemini 2.5 Pro):**

- Claims completion without doing it
- Requires multiple retries
- Sometimes says "do it yourself"

**Mitigation:**

- Always verify in code
- Ask: "Show me the exact changes made"
- Switch models if persistent
- Use Claude/GPT for critical edits

---

**5. Token Limits**[^122]

**Problem:**

- Stricter than web-based AI
- Can't analyze entire large projects
- Truncated responses

**Mitigation:**

- Break tasks into chunks
- Use /summarize proactively
- Reference summary docs
- New chat for new context

---

**6. Bug Detection Limits**[^122]

**Problem:**

- Misses complex bugs (memory leaks, threading)
- False positives
- Generic fixes

**Mitigation:**

- Combine with manual debugging
- Unit tests essential
- Code review still mandatory
- Don't rely solely on AI

---

**7. Slower VS Code Updates**[^122]

**Problem:**

- Fork of VS Code → delayed features
- Slower bug fixes

**Mitigation:**

- Accept trade-off for AI benefits
- Report bugs to Cursor team
- Check compatibility before updating

---

## PHẦN 3: ADVANCED PATTERNS \& WORKFLOWS

### 3.1 Two-File System[^48]

**Modern Simplified Approach:**

**File 1: project_config.md**

```
# Project Configuration

## Architecture
[System design, patterns, constraints]

## Coding Standards
[Style, naming, structure]

## Technology Choices
[Stack, libraries, versions]

## Security Requirements
[Authentication, authorization, data protection]
```

**File 2: .cursorrules**

```
# Cursor Rules

Reference @project_config.md for all architectural decisions.

## Workflow
1. **Plan Phase**: Analyze request, create detailed plan
2. **Construct Phase**: Execute plan completely
3. **Verify Phase**: Test and confirm

## Construction Rules
- NO TODO comments
- NO placeholders  
- NO incomplete sections
- ALL code must be functional
- Include all imports
- Clear naming conventions

## Verification Required
Every step must include verification command.
```

**Benefits:**

- Simpler than many-file systems
- More autonomous workflow
- Clear separation: architecture vs execution rules
- Easy to maintain

---

### 3.2 Iterative Development Pattern[^69]

**.cursorrules với Step-by-Step:**

```
# Project: E-Commerce Checkout Flow

## General Description
Multi-step checkout với cart, shipping, payment, confirmation.

## Development Approach
Build one step at a time. Do not proceed to next step until current is complete and verified.

## Step 1: Shopping Cart
- Display cart items với images, prices
- Quantity adjustment (+/-)
- Remove item functionality
- Total calculation
- "Proceed to Checkout" button

**Verification:** Cart displays correctly, calculations accurate, all interactions work.

## Step 2: Shipping Information
[Similar detail]

## Step 3: Payment Processing
[Similar detail]
```

**Usage:**

```
Prompt: "Implement Step 1 carefully and beautifully"

[AI implements Step 1]

Verify manually, then:

Prompt: "Implement Step 2 carefully"

[Continues...]
```

**Final Pass:**

```
Prompt: "Implement all remaining steps in full, carefully"
```


---

### 3.3 Project Memory Strategy[^85]

**README-Centric Approach:**

**README.md as Single Source of Truth:**

```
# Project Name

## Current Status
- Sprint 3 of 5
- Features complete: Authentication, User Profile, Post Creation
- In progress: Comment System
- Next: Notification System

## Architecture Decisions

### 2025-01-15: Chose PostgreSQL over MongoDB
Reasoning: Need ACID guarantees for transactions
Impact: All data models use SQL schema
Reference: docs/adr/001-database-choice.md

### 2025-01-20: Implemented Redis caching
Reasoning: Reduce DB load for user sessions
Impact: Session logic in src/cache/sessions.py
TTL: 30 minutes

## Module Overview
```

src/
├── api/           \# REST endpoints, input validation
├── services/      \# Business logic, no direct DB calls
├── repositories/  \# Database access only, no business logic
├── models/        \# Pydantic models, shared across layers
└── utils/         \# Pure functions, no side effects

```

## Coding Patterns

### Error Handling
```python
# Always use custom exceptions
from exceptions import ValidationError, DatabaseError

try:
    result = service.process(data)
except DatabaseError as e:
    logger.error(f"DB Error: {e}", extra={"trace_id": trace_id})
    raise
```


### Testing

- Coverage target: >80%
- Mock external services
- Factories for test data (tests/factories.py)


## Recent Changes

### 2025-01-22

- Added email verification flow
- Files: src/api/auth.py, src/services/email.py
- Tests: tests/integration/test_email_verification.py


## Known Issues

1. Email sending slow in dev (using real SMTP)
    - Workaround: Mock in tests
    - Fix planned: Local mail server

## Next Steps

- [ ] Implement comment threading (nested replies)
- [ ] Add rate limiting to API endpoints
- [ ] Migrate from SQLite to PostgreSQL for staging

```

**Cursor Rule:**
```


# Global Rule

Always reference and update @README.md when:

- Making architectural decisions
- Adding/removing features
- Discovering issues
- Completing milestones

```

**Benefits:**
- Single file to reference
- Always up-to-date
- Natural project documentation
- Easy onboarding

---

### 3.4 Advanced .ai Folder Pattern[^46][^51]

**Structure:**
```

.ai/
prd.md                    \# Product requirements
story-001-websockets.md   \# Detailed stories
story-002-redis.md
story-003-persistence.md
decisions.md              \# ADRs (Architecture Decision Records)
progress.md               \# Current status

```

**PRD Template:**
```


# PRD: Real-Time Notification System

## Goal

Users receive instant notifications for events without polling.

## Tech Stack

- WebSockets (Socket.IO)
- Redis Pub/Sub
- PostgreSQL persistence
- React client


## User Stories

1. As a user, I see notifications immediately when events occur
2. As a user, I receive notifications even if temporarily offline
3. As a developer, I can emit notifications from any service

## Non-Functional Requirements

- <100ms latency
- 10K concurrent connections
- Zero message loss
- 99.9% uptime


## Success Criteria

- Load test: 10K concurrent users
- Latency test: p99 <100ms
- Failover test: Redis restart with no message loss


## Stories

1. WebSocket endpoint setup
2. Redis pub/sub integration
3. Notification delivery
4. Persistence layer
5. Client reconnection handling
```

**Story Template:**
```


# Story: WebSocket Endpoint Setup

## Goal

Create FastAPI WebSocket endpoint for client connections.

## Technical Approach

- Use FastAPI WebSocketRoute
- Connection manager class for active connections
- Heartbeat every 30s to detect disconnects
- Authentication via JWT in query params


## Files to Create

- src/api/websocket.py: Endpoint and routes
- src/services/connection_manager.py: Connection tracking
- src/models/websocket.py: Message schemas


## Files to Modify

- src/main.py: Mount WebSocket routes
- requirements.txt: Add websockets library


## Testing Strategy

- Unit: Connection manager add/remove
- Integration: Connect/disconnect flows
- Load: 1000 concurrent connections


## Verification

```bash
# Start server
uvicorn src.main:app

# Test connection
python scripts/test_websocket.py

# Expected: Connection successful, heartbeat received
```


## Story Status

- [ ] Created files
- [ ] Tests written
- [ ] Tests passing
- [ ] Verified manually
- [ ] Committed


## Commit Message

feat(websocket): add WebSocket endpoint with connection management

- Implement FastAPI WebSocket route
- Add ConnectionManager for tracking active connections
- Heartbeat mechanism for detecting disconnects
- JWT authentication for WebSocket connections
- Unit and integration tests with 100% coverage

Closes \#123

```

**Workflow:**
```


# Start new chat

Cursor: "Hello"

AI: "Hi! I see PRD in .ai/prd.md.
Would you like me to generate story-001-websockets.md?"

You: "Yes, create detailed story file and wait for approval."

[AI creates story file]

You: [Review story-001-websockets.md]

You: "Approved. Implement using TDD."

[AI implements, tests, iterates]

You: "Tests passing. Push changes and update story."

[AI commits with good message, updates story status]

You: "Start story-002."

[Repeat...]

```

---

## PHẦN 4: TEAM & ENTERPRISE

### 4.1 Team Collaboration[^43][^54]

**Shared Configuration:**

**Team .cursorrules (in version control):**
```


# Team Coding Standards

## Applies to All Team Members

### Code Style (Non-negotiable)

- Black formatter with 88 char line length
- isort for imports (black profile)
- Type hints required for all functions
- Docstrings: Google style


### Architecture Patterns (Enforced)

- Repository pattern for DB access
- Service layer for business logic
- API layer for HTTP handling
- No business logic in API routes


### Testing Requirements

- Minimum 70% coverage
- All API endpoints tested
- No mocks in integration tests
- Factories for test data


### Security Rules

- No secrets in code
- All inputs validated
- SQL injection prevention (use ORM)
- Rate limiting on public endpoints


### Review Process

- All AI-generated code requires human review
- At least one approval before merge
- Run full test suite before PR
- Update architecture docs if patterns change

```

**Individual Global Rules (personal preference):**
```


# My Personal Preferences

## Code Style

- Prefer list comprehensions over map/filter
- Type aliases for complex types
- Early returns over nested ifs


## AI Interaction

- Always explain reasoning in comments
- Show verification commands
- Prefer functional patterns

```

**Separation:**
- Team rules: In `.cursorrules` (version controlled)
- Personal rules: In Global Settings (not shared)

---

**Team Workflows:**

**Workflow 1: Pair Programming dengan Cursor**[^133]
```

1. Cursor có real-time sharing (Figma-style)
2. One person drives, others can see changes live
3. AI suggestions visible to all
4. Good for knowledge transfer và complex problems
```

**Workflow 2: Story-Based Development**[^46]
```

Team Lead:

- Creates detailed PRD
- Reviews story files
- Approves implementations

Developers:

- Use Cursor Agent mode
- Generate story files for approval
- Implement after approval
- Push with descriptive commits

Benefits:

- Clear accountability
- Detailed audit trail
- Consistent code quality

```

---

### 4.2 Enterprise Features[^110]

**Teams Plan ($40/user/month):**
- Centralized team billing
- Usage analytics và reporting
- Org-wide privacy mode controls
- Role-based access control (RBAC)
- SAML/OIDC SSO

**Enterprise Plan (Custom pricing):**
- Pooled usage across organization
- Invoice/PO billing
- SCIM seat management
- AI code tracking API
- Audit logs
- Granular admin controls
- Model restrictions
- Priority support

**Admin Controls:**
```

Settings → Organization Settings

Admin can:

- Enforce Privacy Mode
- Restrict models available
- Set usage limits per user
- View usage analytics
- Audit all AI interactions
- Export logs for compliance

```

---

### 4.3 Compliance & Governance[^60][^61]

**Privacy Mode for Enterprise:**[^61]

**Technical Guarantees:**
- `x-ghost-mode` header on all requests
- Separate server replicas với logging disabled
- Zero data retention agreements with all AI providers
- Team-level enforcement
- Server verification every 5 minutes
- Failsafe defaults to privacy mode

**For Regulated Industries:**
- Finance (PCI-DSS, SOX)
- Healthcare (HIPAA)
- Government (FedRAMP)
- Legal (attorney-client privilege)

**Audit Trail:**
```

Enterprise API provides:

- All AI interactions logged
- Timestamp, user, model used
- Input/output captured (if not in Privacy Mode)
- File access logs
- Model usage metrics
- Cost tracking per user/team

```

---

## SUMMARY & ACTION PLAN

### Immediate Actions (Week 1)

**1. Setup Configuration:**
```

☐ Create .cursorrules for current project
☐ Set Global AI Rules
☐ Configure YOLO allow/deny lists
☐ Enable Privacy Mode if sensitive code
☐ Create .cursorignore for secrets

```

**2. Learn Essential Shortcuts:**
```

☐ Cmd+P (quick open)
☐ Cmd+K (inline edit)
☐ Cmd+I (agent mode)
☐ @ symbol (file references)
☐ Tab (accept autocomplete)

```

**3. Create Multi-Agent System:**
```

☐ Setup .cursor/commands/ directory
☐ Create planner.md
☐ Create implementer.md
☐ Create debugger.md
☐ Create reviewer.md
☐ Create test-writer.md
☐ Test with simple workflow

```

---

### Short-Term (Week 2-4)

**4. Establish Workflows:**
```

☐ Test-first workflow với YOLO
☐ Pre-PR verification script
☐ Context management strategy
☐ Chat organization system
☐ Model selection for different tasks

```

**5. Document Project:**
```

☐ Create docs/ARCHITECTURE.md
☐ Setup README.md as memory
☐ Document coding patterns
☐ Note common pitfalls
☐ Create troubleshooting guide

```

**6. Team Adoption (if applicable):**
```

☐ Share .cursorrules with team
☐ Team training session
☐ Establish review process
☐ Set up analytics
☐ Create team best practices doc

```

---

### Long-Term Optimization

**7. Measure & Iterate:**
```

☐ Track velocity improvements
☐ Monitor code quality metrics
☐ Collect team feedback
☐ Refine prompts based on results
☐ Update .cursorrules regularly

```

**8. Advanced Patterns:**
```

☐ Implement two-file system
☐ Story-based development
☐ Project memory strategy
☐ Advanced testing automation
☐ Custom slash commands

```

---

## Kết Luận

Cursor đại diện cho paradigm shift trong software development - không phải AI như một tool bên cạnh, mà AI được integrate sâu vào toàn bộ workflow. Với best practices từ research này:

**Key Takeaways:**

1. **Multi-Agent System:** 5 agent roles (Planner, Implementer, Debugger, Reviewer, Test Writer) tạo structured workflow với clear responsibilities

2. **Context is King:** Master @ symbol system, understand token limits, strategic use of .cursorrules và architecture docs

3. **Security First:** Privacy Mode, .cursorignore, secret scanning, và careful prompt sanitization là mandatory

4. **Model Selection Matters:** Right model cho right task - don't waste Opus on typos, don't use GPT-3.5 for architecture

5. **Test-Driven Development:** "Tests first, code second, iterate until green" pattern với YOLO mode = guaranteed correctness

6. **Real ROI:** Companies achieving 2-5x velocity, 50% more code shipped, 14-day launches thay vì 4 weeks

7. **Limitations Awareness:** Struggles với very large codebases (>100K lines), legacy systems, requires human oversight

**Future Outlook:**
Cursor đã đạt $500M ARR trong 2 năm, với trajectory tiếp tục tăng mạnh. Các công ty như Stripe, Coinbase, Uber đang bet heavily vào AI-native development. Trend rõ ràng: AI sẽ không thay thế developers, nhưng developers using AI sẽ thay thế developers không dùng AI.

**Your Next Steps:**
1. Implement 5-agent system cho Python pipeline
2. Setup comprehensive .cursorrules
3. Practice keyboard shortcuts
4. Start with small projects, scale up
5. Measure và iterate based on results

Chúc bạn thành công với Cursor và AI-augmented development workflow! 🚀
<span style="display:none">[^100][^103][^105][^35][^36][^37][^38][^39][^41][^42][^45][^47][^49][^50][^52][^53][^55][^56][^59][^62][^63][^64][^65][^66][^67][^70][^71][^72][^73][^74][^75][^76][^77][^78][^79][^80][^81][^82][^83][^84][^86][^87][^88][^89][^90][^91][^92][^93][^95][^96]</span>

<div align="center">⁂</div>

[^1]: https://cursor.com/customers
[^2]: https://inoxoft.com/blog/cursor-ai-examples-and-workflows/
[^3]: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
[^4]: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns/
[^5]: https://skywork.ai/blog/vibecoding/cursor-2-0-multi-agent-suite/
[^6]: https://cursor.com/changelog/1-6
[^7]: https://www.reddit.com/r/LangChain/comments/1nsm96e/how_do_you_actually_debug_multiagent_systems_in/
[^8]: https://graphite.com/guides/code-review-best-practices
[^9]: https://mbrenndoerfer.com/writing/testing-ai-agents-with-examples
[^10]: https://skywork.ai/skypage/en/A-Deep-Dive-into-pytest-mcp-server-Bridging-Pytest-with-AI-Agents/1972858335256047616
[^11]: https://stronglytyped.uk/articles/practical-cursor-editor-tips
[^12]: https://cursorrules.org/blog/comprehensive-guide-cursorrules-optimized-ai-programming
[^13]: https://corti.com/using-the-cursorrules-file-when-working-with-the-cursor-ide/
[^14]: https://dev.to/mayank_tamrkar/-mastering-cursor-ai-the-ultimate-guide-for-developers-2025-edition-2ihh
[^15]: https://www.reco.ai/learn/cursor-security
[^16]: https://www.mintmcp.com/blog/cursor-security
[^17]: https://skywork.ai/blog/vibecoding/cursor-2-0-security-privacy/
[^18]: https://www.builder.io/blog/cursor-tips
[^19]: https://www.youtube.com/watch?v=C8Xtek55ERk
[^20]: https://www.youtube.com/watch?v=gC49uM7iSCg
[^21]: https://dev.to/tawe/cursor-ai-security-deep-dive-into-risk-policy-and-practice-4epp
[^22]: https://www.oasis.security/resources/cursor-workspace-trust-vulnerability
[^23]: https://skywork.ai/blog/cursor-ai-comprehensive-guide-2025-everything-you-need-to-know/
[^24]: https://docs.cursor.com/en/guides/advanced/large-codebases
[^25]: https://stevekinney.com/courses/ai-development/cursor-context
[^26]: https://gtinfotech.co.in/blogs/how-does-cursor-ide-understand-analyze-context-of-codebase/
[^27]: https://olwiba.com/posts/2025/mastering-cursor
[^28]: https://docs.cursor.com/en/context/@-symbols/overview
[^29]: https://forum.cursor.com/t/best-practices-for-medium-large-projects/21206
[^30]: https://forum.cursor.com/t/context-and-large-codebases/50750
[^31]: https://www.vincentschmalbach.com/force-full-context-in-cursor-ide-workaround-for-large-files/
[^32]: https://forum.cursor.com/t/10-pro-tips-for-working-with-cursor-agent/137212
[^33]: https://getstream.io/blog/cursor-ai-large-projects/
[^34]: https://www.reddit.com/r/cursor/comments/1l4w5bz/how_can_i_download_or_prepare_a_summary_of_the/
[^35]: https://www.backslash.security/blog/cursor-ide-security-best-practices
[^36]: https://www.sidetool.co/post/optimizing-your-workflow-troubleshooting-cursor-ai-integrations-in-vs-code
[^37]: https://forum.cursor.com/t/composer-agent-refined-workflow-detailed-instructions-and-example-repo-for-practice/47180
[^38]: https://forum.cursor.com/t/guide-a-simpler-more-autonomous-ai-workflow-for-cursor-new-update/70688
[^39]: https://www.reddit.com/r/cursor/comments/1iisxvz/new_favorite_way_to_use_composer_agent/
[^40]: https://cursor.com
[^41]: https://www.reddit.com/r/cursor/comments/1ipqiyg/maximizing_cursor_ai_whats_your_best_workflow_hack/
[^42]: https://www.reddit.com/r/cursor/comments/1iga00x/refined_workflow_for_cursor_composer_agent_mode/
[^43]: https://pub.towardsai.net/cursor-ide-complete-guide-2025-8d8d25407b97
[^44]: https://dev.to/codebucks/cursor-ai-crash-course-boost-your-productivity-with-ai-powered-coding-57c9
[^45]: https://www.reddit.com/r/cursor/comments/1hqcp03/a_few_tips_for_using_composer_effectively/
[^46]: https://www.youtube.com/watch?v=3289vhOUdKA
[^47]: https://www.youtube.com/watch?v=Jem2yqhXFaU
[^48]: https://forum.cursor.com/t/add-the-best-practices-section-to-the-documentation/129131
[^49]: https://cursor.com/security
[^50]: https://www.tothenew.com/blog/the-developers-cursor-checklist-secure-and-smart-practices-for-using-cursor-ai/
[^51]: https://www.youtube.com/watch?v=KPqU4hQ2fCg
[^52]: https://github.com/Mawla/cursor_rules
[^53]: https://www.reddit.com/r/cursor/comments/1jqep65/yolo_auto/
[^54]: https://www.stackhawk.com/blog/secure-code-with-cursor/
[^55]: https://forum.cursor.com/t/optimal-structure-for-mdc-rules-files/52260
[^56]: https://forum.cursor.com/t/where-is-the-yolo-mode-configuration-in-1-0/101754
[^57]: https://apiiro.com/blog/securing-code-with-cursor-and-windsurf/
[^58]: https://www.reddit.com/r/neovim/comments/1ijgamd/what_is_open_sources_answer_to_cursors_codebase/
[^59]: https://www.reddit.com/r/cursor/comments/1jqdcn8/experience_with_larger_codebases/
[^60]: https://forum.cursor.com/t/how-to-properly-reference-files-when-using-cursor-ides-ai-features/60678
[^61]: https://igorstechnoclub.com/cursor-composer-a-practical-guide-with-best-practices/
[^62]: https://prismic.io/blog/cursor-ai
[^63]: https://www.youtube.com/watch?v=3KAI__5dUn0
[^64]: https://forum.cursor.com/t/let-us-summarize-the-current-chat-at-wish/102864
[^65]: https://cursor.com/docs/context/mentions
[^66]: https://cursor.com/docs/agent/chat/summarization
[^67]: https://www.linkedin.com/pulse/ai-dev-clinecursor-efficient-context-management-key-hassan-syed-4ufte
[^68]: https://cursor.com/docs/models
[^69]: https://stevekinney.com/courses/ai-development/cursor-model-selection
[^70]: https://forum.cursor.com/t/cursor-4-7-auto-model-selection/70488
[^71]: https://frontendmasters.com/blog/choosing-the-right-model-in-cursor/
[^72]: https://blog.laozhang.ai/ai/cursor-claude-opus-4-complete-guide-2025/
[^73]: https://www.eesel.ai/blog/cursor-pricing
[^74]: https://skywork.ai/blog/vibecoding/cursor-2-0-workflow-tips/
[^75]: https://pub.towardsai.net/my-cursor-custom-mode-setup-building-the-perfect-ai-development-toolkit-10554ea7568e
[^76]: https://skywork.ai/blog/vibecoding/cursor-2-0-pricing/
[^77]: https://deepsense.ai/blog/a-developers-guide-to-peak-productivity-in-cursor-vs-code/
[^78]: https://www.youtube.com/watch?v=CcWL3qr-4K8
[^79]: https://flexprice.io/blog/cursor-pricing-guide
[^80]: https://mehmetbaykar.com/posts/top-15-cursor-shortcuts-to-speed-up-development/
[^81]: https://www.reddit.com/r/cursor/comments/1j6zo7q/which_ai_model_is_the_best_performing_model_in/
[^82]: https://cursor.com/pricing
[^83]: https://www.mehmetbaykar.com/posts/top-15-cursor-shortcuts-to-speed-up-development/
[^84]: https://forum.cursor.com/t/how-to-choose-optimal-model/117358
[^85]: https://uibakery.io/blog/cursor-ai-pricing-explained
[^86]: https://cursor101.com/en/cursor/cheat-sheet
[^87]: https://northflank.com/blog/claude-code-vs-cursor-comparison
[^88]: https://www.arsturn.com/blog/success-stories-how-cursor-improved-developer-workflows
[^89]: https://www.productgrowth.blog/p/how-cursor-ai-hacked-growth
[^90]: https://cursorideguide.com/use-cases
[^91]: https://www.builder.io/blog/cursor-vs-github-copilot
[^92]: https://fatcatremote.com/it-glossary/cursor-ai/limitations-of-cursor-ai
[^93]: https://newsletter.pragmaticengineer.com/p/cursor
[^94]: https://www.qodo.ai/blog/cursor-vs-github-copilot/
[^95]: https://www.altexsoft.com/blog/cursor-pros-and-cons/
[^96]: https://www.youtube.com/watch?v=En5cSXgGvZM
[^97]: https://community.latenode.com/t/cursor-vs-github-copilot-2025-same-functionality-but-double-the-cost/20812
[^98]: https://docs.kanaries.net/topics/AICoding/cursor-review
[^99]: https://www.reddit.com/r/learnprogramming/comments/1j6k7f8/i_just_tried_cursor_my_motivation_to_learn/
[^100]: https://techpoint.africa/guide/cursor-vs-github-copilot/
[^101]: https://digitaldefynd.com/IQ/pros-cons-of-cursor-ai/
[^102]: https://collabnix.com/top-5-reasons-to-switch-to-cursor-ai-in-2025-the-complete-comparison-guide/
[^103]: https://skywork.ai/blog/vibecoding/cursor-2-0-vs-github-copilot/
[^104]: https://blog.enginelabs.ai/cursor-ai-an-in-depth-review
[^105]: https://www.stryv.ai/blog/ai-coding-assistants-cursor-ai-and-github-copilot-what-worked-what-didn-t```

