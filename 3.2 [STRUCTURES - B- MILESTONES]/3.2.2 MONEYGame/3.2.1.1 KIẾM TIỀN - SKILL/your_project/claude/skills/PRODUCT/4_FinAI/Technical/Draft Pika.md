# PIKA ROBOT - HYBRID AGENT ARCHITECTURE

## KIẾN TRÚC CHỐT: HYBRID (Travel Agent + Cursor Agent)

**Lý do chọn:**
1. ✅ Safety-first: Governance layer bảo vệ children
2. ✅ Performance: Multi-agent parallel processing
3. ✅ Scalability: Horizontal scaling với agents
4. ✅ Maintainability: Clear structure, easy debug
5. ✅ Cost-effective: Optimize LLM calls

---

## FOLDER STRUCTURE HOÀN CHỈNH

```
pika_robot/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                           # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py                   # Settings, env vars
│   │   ├── logger.py                   # Centralized logging
│   │   ├── exceptions.py               # Custom exceptions
│   │   └── constants.py                # Constants (age ranges, etc)
│   │
│   ├── models/                         # Data models
│   │   ├── __init__.py
│   │   ├── base.py                     # Base models
│   │   ├── child.py                    # Child profile model
│   │   ├── story.py                    # Story model
│   │   ├── quiz.py                     # Quiz model
│   │   ├── session.py                  # Learning session
│   │   └── analytics.py                # Analytics models
│   │
│   ├── agent/                          # MAIN AGENT SYSTEM
│   │   ├── __init__.py
│   │   │
│   │   ├── entrypoint.py              # 🎯 MAIN ENTRY POINT
│   │   │
│   │   ├── layer_0_governance/        # ⭐ Safety & Validation
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── input_gate/            # Input validation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── validator.py       # Input validation logic
│   │   │   │   ├── safety_checker.py  # Content safety (violence, adult)
│   │   │   │   ├── age_checker.py     # Age-appropriate check
│   │   │   │   └── pii_detector.py    # PII detection (names, addresses)
│   │   │   │
│   │   │   ├── output_gate/           # Output validation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── quality_checker.py # Content quality
│   │   │   │   ├── language_checker.py # Language level check
│   │   │   │   ├── educational_validator.py # Educational value
│   │   │   │   └── safety_filter.py   # Final safety check
│   │   │   │
│   │   │   └── models.py              # Gate result models
│   │   │
│   │   ├── layer_1_perception/        # Context processing
│   │   │   ├── __init__.py
│   │   │   ├── child_profiler.py      # Analyze child profile
│   │   │   ├── context_builder.py     # Build learning context
│   │   │   └── intent_detector.py     # Detect learning intent
│   │   │
│   │   ├── layer_2_cognition/         # ⭐ Multi-Agent Core
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── base/                  # Base classes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_agent.py      # Abstract agent class
│   │   │   │   └── agent_state.py     # Agent state management
│   │   │   │
│   │   │   ├── message_bus/           # Communication
│   │   │   │   ├── __init__.py
│   │   │   │   ├── bus.py             # Message bus implementation
│   │   │   │   ├── message.py         # Message models
│   │   │   │   └── topics.py          # Topic definitions
│   │   │   │
│   │   │   ├── chief_agent/           # Orchestrator
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chief.py           # Chief agent logic
│   │   │   │   └── prompts.py         # Chief prompts
│   │   │   │
│   │   │   ├── story_agent/           # Story generation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── story_agent.py     # Story generation logic
│   │   │   │   ├── prompts.py         # Story prompts
│   │   │   │   └── templates.py       # Story templates
│   │   │   │
│   │   │   ├── audio_agent/           # Audio generation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── audio_agent.py     # TTS logic
│   │   │   │   └── voice_selector.py  # Voice selection
│   │   │   │
│   │   │   ├── quiz_agent/            # Quiz generation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── quiz_agent.py      # Quiz generation
│   │   │   │   ├── prompts.py         # Quiz prompts
│   │   │   │   └── question_types.py  # Question templates
│   │   │   │
│   │   │   ├── voice_agent/           # Speech recognition
│   │   │   │   ├── __init__.py
│   │   │   │   ├── voice_agent.py     # STT logic
│   │   │   │   └── pronunciation_checker.py # Pronunciation check
│   │   │   │
│   │   │   └── moderator_agent/       # Content moderation
│   │   │       ├── __init__.py
│   │   │       ├── moderator.py       # Moderation logic
│   │   │       └── rules.py           # Moderation rules
│   │   │
│   │   ├── layer_3_action/            # External integrations
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── llm/                   # LLM providers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── openai_client.py   # OpenAI integration
│   │   │   │   ├── anthropic_client.py # Claude integration
│   │   │   │   └── gemini_client.py   # Google Gemini
│   │   │   │
│   │   │   ├── tts/                   # Text-to-Speech
│   │   │   │   ├── __init__.py
│   │   │   │   ├── elevenlabs.py      # ElevenLabs TTS
│   │   │   │   └── google_tts.py      # Google TTS
│   │   │   │
│   │   │   ├── stt/                   # Speech-to-Text
│   │   │   │   ├── __init__.py
│   │   │   │   ├── whisper.py         # Whisper STT
│   │   │   │   └── google_stt.py      # Google STT
│   │   │   │
│   │   │   └── storage/               # File storage
│   │   │       ├── __init__.py
│   │   │       ├── s3_client.py       # AWS S3
│   │   │       └── local_storage.py   # Local dev
│   │   │
│   │   └── utils/                     # Agent utilities
│   │       ├── __init__.py
│   │       ├── prompt_builder.py      # Dynamic prompt building
│   │       ├── cost_tracker.py        # Track LLM costs
│   │       └── metrics.py             # Performance metrics
│   │
│   ├── api/                           # API layer
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Main router
│   │   │   │
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── learning.py        # Learning endpoints
│   │   │   │   ├── story.py           # Story generation
│   │   │   │   ├── quiz.py            # Quiz endpoints
│   │   │   │   ├── voice.py           # Voice interaction
│   │   │   │   └── analytics.py       # Analytics endpoints
│   │   │   │
│   │   │   └── dependencies.py        # API dependencies
│   │   │
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py                # Authentication
│   │       ├── rate_limit.py          # Rate limiting
│   │       └── error_handler.py       # Error handling
│   │
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── learning_service.py        # Learning workflow
│   │   ├── content_service.py         # Content management
│   │   ├── analytics_service.py       # Analytics
│   │   └── child_service.py           # Child profile management
│   │
│   ├── db/                            # Database
│   │   ├── __init__.py
│   │   ├── session.py                 # DB session
│   │   ├── base.py                    # Base model
│   │   │
│   │   ├── repositories/              # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── child_repo.py
│   │   │   ├── story_repo.py
│   │   │   ├── quiz_repo.py
│   │   │   └── session_repo.py
│   │   │
│   │   └── migrations/                # Alembic migrations
│   │       └── versions/
│   │
│   └── monitoring/                    # Observability
│       ├── __init__.py
│       ├── tracing.py                 # Distributed tracing
│       ├── metrics.py                 # Prometheus metrics
│       └── alerts.py                  # Alert definitions
│
├── tests/                             # Tests
│   ├── __init__.py
│   │
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_governance/
│   │   ├── test_agents/
│   │   └── test_services/
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_agent_workflows/
│   │   └── test_api/
│   │
│   └── e2e/
│       ├── __init__.py
│       └── test_learning_flow.py
│
├── scripts/                           # Utility scripts
│   ├── init_db.py                     # Initialize database
│   ├── seed_data.py                   # Seed test data
│   ├── benchmark.py                   # Performance benchmarks
│   └── cost_analysis.py               # Cost analysis
│
├── docs/                              # Documentation
│   ├── architecture.md                # Architecture overview
│   ├── agent_design.md                # Agent design decisions
│   ├── api_docs.md                    # API documentation
│   └── deployment.md                  # Deployment guide
│
├── docker/                            # Docker configs
│   ├── Dockerfile.api                 # API service
│   ├── Dockerfile.agents              # Agent workers
│   └── docker-compose.yml             # Local development
│
├── k8s/                               # Kubernetes manifests
│   ├── api-deployment.yaml
│   ├── agents-deployment.yaml
│   ├── redis-deployment.yaml
│   └── ingress.yaml
│
├── .env.example                       # Environment template
├── .gitignore
├── requirements.txt                   # Python dependencies
├── requirements-dev.txt               # Dev dependencies
├── pyproject.toml                     # Poetry config
├── pytest.ini                         # Pytest config
├── README.md                          # Project README
└── main.py                            # Application entry point
```

---

## KEY FILES EXPLAINED

### 1. Main Entry Point
```
app/agent/entrypoint.py
```
**Chức năng:** Entry point cho toàn bộ agent system

### 2. Governance Layer
```
app/agent/layer_0_governance/
├── input_gate/    # Validate ALL inputs
└── output_gate/   # Validate ALL outputs
```
**Critical cho children safety!**

### 3. Multi-Agent System
```
app/agent/layer_2_cognition/
├── chief_agent/       # Orchestrator
├── story_agent/       # Story generation
├── audio_agent/       # TTS
├── quiz_agent/        # Quiz creation
├── voice_agent/       # STT
└── moderator_agent/   # Content safety
```

### 4. Message Bus
```
app/agent/layer_2_cognition/message_bus/
```
**Handles all agent communication**

---

## TECH STACK

```yaml
Language: Python 3.11+
Framework: FastAPI
Agent Framework: LangChain + Custom
Message Bus: Redis (with in-memory fallback)
Database: PostgreSQL
LLM: OpenAI GPT-4, Claude, Gemini
TTS: ElevenLabs, Google TTS
STT: Whisper, Google STT
Observability: Langfuse, Prometheus, Grafana
Testing: Pytest
CI/CD: GitHub Actions
Deployment: Kubernetes (AWS EKS)
```

---

## ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
│              (FastAPI + Rate Limit)                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            LAYER 0: Governance                       │
│  ┌──────────────────┐    ┌──────────────────┐      │
│  │   Input Gate     │    │   Output Gate    │      │
│  │  - Safety check  │    │  - Quality check │      │
│  │  - Age check     │    │  - Language check│      │
│  │  - PII detect    │    │  - Safety filter │      │
│  └──────────────────┘    └──────────────────┘      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         LAYER 1: Perception                          │
│  - Child profiler                                    │
│  - Context builder                                   │
│  - Intent detector                                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         LAYER 2: Cognition (Multi-Agent)             │
│                                                       │
│              ┌─────────────────┐                     │
│              │  Message Bus    │                     │
│              │    (Redis)      │                     │
│              └────────┬────────┘                     │
│                       │                              │
│       ┌───────────────┼───────────────┐             │
│       │               │               │             │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐        │
│  │ Chief   │    │ Story   │    │ Audio   │        │
│  │ Agent   │    │ Agent   │    │ Agent   │        │
│  └────┬────┘    └────┬────┘    └────┬────┘        │
│       │              │              │              │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐        │
│  │ Quiz    │    │ Voice   │    │Moderator│        │
│  │ Agent   │    │ Agent   │    │ Agent   │        │
│  └─────────┘    └─────────┘    └─────────┘        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         LAYER 3: Action (External APIs)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   LLM    │  │   TTS    │  │   STT    │         │
│  │ (GPT-4)  │  │(ElevenLab)│  │(Whisper) │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │   Storage   │
              │   (S3/DB)   │
              └─────────────┘
```

---

## NEXT STEPS

Bạn muốn mình:
1. ✅ Tạo skeleton code cho từng module?
2. ✅ Viết template cho base_agent.py?
3. ✅ Setup docker-compose cho local dev?
4. ✅ Tạo init scripts?
5. ✅ Viết example workflows?

Chọn 1 hoặc nhiều, mình sẽ generate code chi tiết! 🚀




# 🤖 PIKA ROBOT - HYBRID AGENT SYSTEM

**Kiến trúc Hybrid** kết hợp ưu điểm của:
- ✅ **Travel Agent** (Q3): Governance layer (safety-first)
- ✅ **Cursor Agent** (Q4): Multi-agent system (performance + scalability)

---

## 📋 MỤC LỤC

1. [Tổng quan](#-tổng-quan)
2. [Kiến trúc](#-kiến-trúc)
3. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
4. [Cài đặt](#-cài-đặt)
5. [Chạy local](#-chạy-local)
6. [API Documentation](#-api-documentation)
7. [Testing](#-testing)
8. [Deployment](#-deployment)
9. [Monitoring](#-monitoring)
10. [Troubleshooting](#-troubleshooting)

---

## 🎯 TỔNG QUAN

**PIKA Robot** là nền tảng học tiếng Anh cho trẻ em 6-10 tuổi, sử dụng AI agents để:
- 📖 Tạo câu chuyện giáo dục
- 🎤 Tương tác giọng nói
- 📝 Tạo bài quiz
- 🔊 Text-to-speech chất lượng cao
- 🛡️ Bảo vệ trẻ em (content moderation)

### Tại sao Hybrid Architecture?

| Feature | Travel Agent | Cursor Agent | **PIKA Hybrid** |
|---------|--------------|--------------|-----------------|
| Safety | ✅ Excellent | ❌ None | ✅ Excellent |
| Performance | ❌ Slow | ✅ Fast | ✅ Fast |
| Scalability | ❌ Limited | ✅ Excellent | ✅ Excellent |
| Debugging | ✅ Easy | ❌ Hard | ⚠️ Medium |
| Cost | ✅ Low | ❌ High | ⚠️ Medium |

---

## 🏗️ KIẾN TRÚC

```
┌─────────────────────────────────────────────┐
│         FastAPI Gateway (Port 8000)         │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│      LAYER 0: Governance (Safety)           │
│  ┌──────────────┐    ┌──────────────┐      │
│  │ Input Gate   │    │ Output Gate  │      │
│  │ - Safety ✓   │    │ - Quality ✓  │      │
│  │ - Age ✓      │    │ - Language ✓ │      │
│  │ - PII ✓      │    │ - Safety ✓   │      │
│  └──────────────┘    └──────────────┘      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│    LAYER 2: Multi-Agent (Performance)       │
│                                             │
│           ┌──────────────┐                  │
│           │ Message Bus  │                  │
│           │   (Redis)    │                  │
│           └──────┬───────┘                  │
│                  │                          │
│      ┌───────────┼──────────┐              │
│      │           │          │              │
│  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐          │
│  │Chief  │  │Story  │  │Audio  │          │
│  │Agent  │  │Agent  │  │Agent  │          │
│  └───────┘  └───────┘  └───────┘          │
│                                             │
│  ┌───────┐  ┌───────┐  ┌───────┐          │
│  │Quiz   │  │Voice  │  │Moder- │          │
│  │Agent  │  │Agent  │  │ator   │          │
│  └───────┘  └───────┘  └───────┘          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│    LAYER 3: External APIs & Storage         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ OpenAI  │ │ElevenLab│ │ Whisper │       │
│  │ GPT-4   │ │  TTS    │ │  STT    │       │
│  └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────────────────────────────┘
```

---

## 💻 YÊU CẦU HỆ THỐNG

### Minimum Requirements
- **Python:** 3.11+
- **RAM:** 4GB
- **CPU:** 2 cores
- **Disk:** 10GB

### Recommended (Production)
- **Python:** 3.11+
- **RAM:** 16GB
- **CPU:** 4+ cores
- **Disk:** 50GB SSD

### Dependencies
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- API Keys:
  - OpenAI (GPT-4)
  - ElevenLabs (TTS)
  - AWS S3 (storage)
  - Langfuse (monitoring)

---

## 🚀 CÀI ĐẶT

### 1. Clone Repository

```bash
git clone https://github.com/your-org/pika-robot.git
cd pika-robot
```

### 2. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit với API keys của bạn
nano .env
```

**.env example:**
```bash
# Database
DATABASE_URL=postgresql://pika_user:pika_password@localhost:5432/pika_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
MESSAGE_BUS_USE_REDIS=true

# OpenAI
OPENAI_API_KEY=sk-xxxxx

# ElevenLabs
ELEVENLABS_API_KEY=xxxxx

# AWS S3
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
S3_BUCKET=pika-robot-storage

# Langfuse (optional)
LANGFUSE_PUBLIC_KEY=pk-xxxxx
LANGFUSE_SECRET_KEY=sk-xxxxx

# App
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 3. Install Python Dependencies

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Run migrations
alembic upgrade head

# Seed test data (optional)
python scripts/seed_data.py
```

---

## 🏃 CHẠY LOCAL

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api

# Check agent logs
docker-compose logs -f story_agent

# Stop all services
docker-compose down
```

**Services available:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Redis: localhost:6379
- PostgreSQL: localhost:5432
- Prometheus: http://localhost:9090 (with monitoring profile)
- Grafana: http://localhost:3000 (with monitoring profile)

### Option 2: Manual (Development)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - PostgreSQL:**
```bash
# Nếu chưa có, cài PostgreSQL hoặc dùng Docker:
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=pika_password \
  postgres:15-alpine
```

**Terminal 3 - API:**
```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 4 - Chief Agent:**
```bash
source venv/bin/activate
python -m app.agent.layer_2_cognition.chief_agent.chief
```

**Terminal 5 - Story Agent:**
```bash
source venv/bin/activate
python -m app.agent.layer_2_cognition.story_agent.story_agent
```

*Repeat for other agents (Audio, Quiz, Voice, Moderator)*

---

## 📚 API DOCUMENTATION

### Start Learning Session

**POST** `/api/v1/learning/start`

```bash
curl -X POST http://localhost:8000/api/v1/learning/start \
  -H "Content-Type: application/json" \
  -d '{
    "child_id": "child_001",
    "age": 7,
    "topic": "friendship",
    "activity_type": "story",
    "difficulty": "medium",
    "child_name": "Emma"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "story": {
      "story_id": "story_abc123",
      "title": "Emma and the Magic Garden",
      "story_text": "Once upon a time...",
      "vocabulary_used": ["friend", "kind", "share"],
      "learning_objectives": ["Understanding friendship"],
      "estimated_reading_time": 180
    },
    "audio": {
      "audio_url": "https://s3.../story_abc123.mp3",
      "duration_seconds": 120
    },
    "quiz": {
      "questions": [...]
    }
  },
  "metadata": {
    "execution_time_seconds": 2.5,
    "quality_score": 0.92,
    "timestamp": "2025-12-18T10:00:00Z"
  }
}
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

**Full API docs:** http://localhost:8000/docs

---

## 🧪 TESTING

### Run Unit Tests

```bash
pytest tests/unit -v
```

### Run Integration Tests

```bash
pytest tests/integration -v
```

### Run E2E Tests

```bash
pytest tests/e2e -v
```

### Run All Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Test Specific Agent

```bash
# Test Story Agent
python -m app.agent.layer_2_cognition.story_agent.story_agent

# Test Input Gate
python -m app.agent.layer_0_governance.input_gate.validator
```

---

## 🚢 DEPLOYMENT

### Production Checklist

- [ ] Set all API keys in production .env
- [ ] Update `ENVIRONMENT=production`
- [ ] Enable Redis persistence
- [ ] Setup database backups
- [ ] Configure CDN for audio files
- [ ] Enable monitoring (Prometheus + Grafana)
- [ ] Setup alerts
- [ ] Configure auto-scaling
- [ ] SSL certificates
- [ ] Rate limiting
- [ ] DDoS protection

### Kubernetes Deployment

```bash
# Build images
docker build -t pika-api:latest -f docker/Dockerfile.api .
docker build -t pika-agents:latest -f docker/Dockerfile.agents .

# Push to registry
docker push your-registry/pika-api:latest
docker push your-registry/pika-agents:latest

# Deploy to Kubernetes
kubectl apply -f k8s/
```

### Scale Agents

```bash
# Scale Story Agents (handle more requests)
kubectl scale deployment story-agent --replicas=5

# Scale Audio Agents
kubectl scale deployment audio-agent --replicas=3
```

---

## 📊 MONITORING

### Logs

```bash
# View all logs
tail -f logs/pika.log

# View agent-specific logs
tail -f logs/story_agent.log

# Docker logs
docker-compose logs -f
```

### Metrics (Prometheus)

Access: http://localhost:9090

**Key metrics:**
- `pika_story_generation_seconds` - Story generation latency
- `pika_content_blocks_total` - Content moderation blocks
- `pika_requests_total` - Total requests
- `pika_agent_errors_total` - Agent errors

### Dashboards (Grafana)

Access: http://localhost:3000 (admin/admin)

**Dashboards:**
- System Overview
- Agent Performance
- API Latency
- Content Safety

### Langfuse Tracing

Access: https://cloud.langfuse.com

View detailed traces of:
- LLM calls
- Agent workflows
- Cost tracking

---

## 🔧 TROUBLESHOOTING

### Common Issues

**1. Agents not receiving messages**
```bash
# Check Redis connection
redis-cli ping

# Check agent subscriptions
docker-compose logs story_agent | grep "subscribed"
```

**2. High latency**
```bash
# Check agent queue sizes
curl http://localhost:8000/health

# Scale agents
docker-compose up -d --scale story_agent=3
```

**3. Content blocked by Input Gate**
```bash
# Check logs
tail -f logs/input_gate.log

# Review blocked content list
cat app/agent/layer_0_governance/input_gate/validator.py
```

**4. Database connection errors**
```bash
# Test connection
psql postgresql://pika_user:pika_password@localhost:5432/pika_db

# Check migrations
alembic current
```

**5. Out of memory**
```bash
# Check Docker stats
docker stats

# Limit agent memory
docker-compose up -d --scale story_agent=1
```

---

## 📖 DOCUMENTATION

- [Architecture Deep Dive](docs/architecture.md)
- [Agent Design Decisions](docs/agent_design.md)
- [API Reference](docs/api_docs.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing](CONTRIBUTING.md)

---

## 🤝 CONTRIBUTING

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 LICENSE

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 ACKNOWLEDGMENTS

- LangChain for agent frameworks
- Microsoft AutoGen for multi-agent patterns
- Anthropic for Claude API
- OpenAI for GPT-4

---

## 📞 SUPPORT

- **Email:** support@pika-robot.com
- **Discord:** https://discord.gg/pika-robot
- **GitHub Issues:** https://github.com/your-org/pika-robot/issues

---

**Built with ❤️ by PIKA Team**
