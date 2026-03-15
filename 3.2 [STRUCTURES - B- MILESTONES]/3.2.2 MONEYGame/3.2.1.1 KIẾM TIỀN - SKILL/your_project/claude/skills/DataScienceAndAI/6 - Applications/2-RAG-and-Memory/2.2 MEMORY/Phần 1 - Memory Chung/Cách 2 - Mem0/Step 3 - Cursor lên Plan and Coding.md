---
name: Triển khai PIKA Memory System - Clean Architecture + Caching 5 lớp
overview: Triển khai PIKA Memory System theo Clean Architecture với caching 5 lớp (L0-L4), async job processing, và tối ưu performance để đạt P95 latency < 200ms. Refactor code hiện tại từ `src/` sang cấu trúc `app/` theo template SDD.
todos:
  - id: setup-structure
    content: Tạo cấu trúc folder Clean Architecture theo template SDD (app/, workers/, tests/)
    status: completed
  - id: core-config
    content: Implement core configuration (config.py, logging.py, exceptions.py)
    status: completed
    dependencies:
      - setup-structure
  - id: domain-entities
    content: Tạo domain entities và value objects (Memory, Job)
    status: completed
    dependencies:
      - setup-structure
  - id: database-setup
    content: Setup PostgreSQL với SQLAlchemy async và Alembic migrations
    status: completed
    dependencies:
      - core-config
  - id: mem0-integration
    content: Refactor Mem0 client vào infrastructure/mem0/mem0_client.py
    status: completed
    dependencies:
      - setup-structure
  - id: repository-impl
    content: Implement repository interfaces (memory_repository_impl, job_repository_impl)
    status: completed
    dependencies:
      - domain-entities
      - database-setup
      - mem0-integration
  - id: cache-l0-l1
    content: Implement L0 (session cache) và L1 (Redis cache)
    status: completed
    dependencies:
      - core-config
  - id: cache-l2-l3
    content: Implement L2 (materialized view) và L3 (embedding cache)
    status: completed
    dependencies:
      - database-setup
      - cache-l0-l1
  - id: proactive-cache
    content: Implement proactive caching service và worker
    status: completed
    dependencies:
      - cache-l2-l3
      - repository-impl
  - id: application-services
    content: Implement application services (memory_service, extraction_service, job_service)
    status: completed
    dependencies:
      - repository-impl
      - cache-l0-l1
  - id: api-refactor
    content: Refactor API endpoints sang Clean Architecture structure
    status: in_progress
    dependencies:
      - application-services
  - id: rabbitmq-setup
    content: Setup RabbitMQ service và message queue infrastructure
    status: completed
    dependencies:
      - core-config
  - id: extraction-worker
    content: Implement async extraction worker với RabbitMQ
    status: pending
    dependencies:
      - rabbitmq-setup
      - application-services
  - id: performance-optimization
    content: Optimize performance với async parallelism và connection pooling
    status: pending
    dependencies:
      - api-refactor
  - id: testing
    content: Viết unit tests, integration tests và load tests
    status: pending
    dependencies:
      - api-refactor
      - extraction-worker
---

# Plan Triển

Khai PIKA Memory System

## Mục tiêu

- Refactor code hiện tại sang Clean Architecture (DDD)
- Implement caching 5 lớp (L0-L4) với proactive caching
- Implement async extraction với RabbitMQ
- Optimize performance đạt P95 < 200ms
- Tuân thủ SOLID principles

## Phân tích hiện trạng

- Code hiện tại: `src/main.py`, `src/memory/mem_client.py`
- Đã có: FastAPI app, MemoryInterface wrapper, 3 endpoints cơ bản
- Chưa có: Clean Architecture structure, caching, async processing, workers

## Cấu trúc folder mới (theo template SDD)

```javascript
app/
├── __init__.py
├── main.py                          # FastAPI app entry point
├── core/                            # Configuration & cross-cutting
│   ├── __init__.py
│   ├── config.py                    # Settings (Pydantic BaseSettings)
│   ├── logging.py                   # Structured logging
│   ├── exceptions.py                # Custom exceptions
│   └── security.py                  # Auth & security utilities
├── api/                             # Presentation layer
│   ├── __init__.py
│   ├── dependencies.py              # Dependency injection
│   └── v1/                          # API versioning
│       ├── __init__.py
│       ├── router.py                # Main router
│       ├── endpoints/               # Endpoints
│       │   ├── __init__.py
│       │   ├── memory.py            # search_facts, extract_facts
│       │   └── jobs.py              # Job status polling
│       └── schemas/                 # Pydantic models
│           ├── __init__.py
│           ├── memory.py
│           └── jobs.py
├── domains/                         # Domain layer (DDD)
│   └── memory/                      # Memory bounded context
│       ├── __init__.py
│       ├── domain/                  # Entities, Value Objects
│       │   ├── __init__.py
│       │   ├── entities.py          # Memory, Job entities
│       │   └── value_objects.py
│       ├── application/             # Use cases, Services
│       │   ├── __init__.py
│       │   ├── services/
│       │   │   ├── __init__.py
│       │   │   ├── memory_service.py        # Search orchestration
│       │   │   ├── extraction_service.py    # Fact extraction logic
│       │   │   └── job_service.py           # Job management
│       │   └── repositories/                # Repository interfaces
│       │       ├── __init__.py
│       │       ├── memory_repository.py
│       │       └── job_repository.py
│       └── infrastructure/           # Implementations
│           ├── __init__.py
│           ├── repositories/
│           │   ├── __init__.py
│           │   ├── memory_repository_impl.py  # Mem0 integration
│           │   └── job_repository_impl.py     # PostgreSQL
│           └── models/              # ORM models
│               ├── __init__.py
│               └── job_model.py
├── infrastructure/                   # Technical infrastructure
│   ├── __init__.py
│   ├── cache/                       # Caching layer
│   │   ├── __init__.py
│   │   ├── cache_service.py         # Cache abstraction
│   │   ├── l0_session_cache.py     # In-memory LRU cache
│   │   ├── l1_redis_cache.py       # Redis cache
│   │   ├── l2_materialized_view.py # PostgreSQL materialized view
│   │   └── proactive_cache.py      # Proactive caching service
│   ├── database/                    # Database connections
│   │   ├── __init__.py
│   │   ├── postgres_session.py     # PostgreSQL session
│   │   └── migrations/              # Alembic migrations
│   ├── messaging/                   # Message queue
│   │   ├── __init__.py
│   │   └── rabbitmq_service.py     # RabbitMQ client
│   └── mem0/                        # Mem0 integration
│       ├── __init__.py
│       └── mem0_client.py          # Mem0 client wrapper
├── middleware/                      # HTTP middleware
│   ├── __init__.py
│   ├── logging_middleware.py
│   └── error_handler.py
├── resilience/                      # Resilience patterns
│   ├── __init__.py
│   ├── circuit_breaker.py
│   └── retry.py
└── utils/                           # Utilities
    ├── __init__.py
    └── helpers.py

workers/                             # Background workers
├── __init__.py
├── main.py                          # Worker entry point
└── tasks/
    ├── __init__.py
    ├── extraction_task.py           # Async extraction worker
    └── proactive_cache_task.py      # Proactive caching worker
```



## Các bước triển khai

### Phase 1: Setup Clean Architecture Structure (Tuần 1)

#### 1.1. Tạo cấu trúc folder

- Tạo toàn bộ folder structure theo template
- Tạo các file `__init__.py` cho tất cả packages

#### 1.2. Core Configuration

- **File**: `app/core/config.py`
- Migrate settings từ environment variables
- Thêm settings cho caching (TTL, intervals)
- Thêm settings cho RabbitMQ, Redis, PostgreSQL
- **File**: `app/core/logging.py`
- Structured logging (JSON format)
- Request ID tracking
- **File**: `app/core/exceptions.py`
- Custom exceptions: `MemoryNotFoundError`, `JobNotFoundError`, `CacheError`

#### 1.3. Domain Layer - Entities & Value Objects

- **File**: `app/domains/memory/domain/entities.py`
- `Memory` entity (id, user_id, content, embedding, metadata)
- `Job` entity (id, user_id, status, progress, data, error)
- **File**: `app/domains/memory/domain/value_objects.py`
- `SearchQuery`, `ExtractionRequest`

### Phase 2: Infrastructure Layer - Database & External Services (Tuần 1-2)

#### 2.1. Database Setup

- **File**: `app/infrastructure/database/postgres_session.py`
- SQLAlchemy async session factory
- Connection pooling configuration
- **File**: `app/domains/memory/infrastructure/models/job_model.py`
- SQLAlchemy model cho `jobs` table
- Migration script với Alembic

#### 2.2. Mem0 Integration

- **File**: `app/infrastructure/mem0/mem0_client.py`
- Refactor `src/memory/mem_client.py` vào đây
- Wrap Mem0 client với error handling
- Add retry logic và circuit breaker

#### 2.3. Repository Implementations

- **File**: `app/domains/memory/infrastructure/repositories/memory_repository_impl.py`
- Implement `IMemoryRepository` interface
- Delegate to Mem0 client
- Add caching layer integration
- **File**: `app/domains/memory/infrastructure/repositories/job_repository_impl.py`
- Implement `IJobRepository` interface
- PostgreSQL operations (create, get, update job status)

### Phase 3: Caching 5 Lớp Implementation (Tuần 2-3)

#### 3.1. Cache Abstraction

- **File**: `app/infrastructure/cache/cache_service.py`
- Abstract cache interface
- Cache key generation strategy
- Cache invalidation logic

#### 3.2. L0: Session Cache (In-Memory)

- **File**: `app/infrastructure/cache/l0_session_cache.py`
- Python `@lru_cache` decorator
- Per-request cache với request ID
- TTL: 1 request lifetime

#### 3.3. L1: Redis Cache

- **File**: `app/infrastructure/cache/l1_redis_cache.py`
- Redis client wrapper
- Cache key: `search:{user_id}:{query_hash}`
- TTL: 1 hour (configurable)
- Serialization: JSON

#### 3.4. L2: Materialized View (PostgreSQL)

- **File**: `app/infrastructure/cache/l2_materialized_view.py`
- Table: `user_favorite_summary`
- Pre-computed results cho "user favorite" queries
- Update strategy: Proactive worker

#### 3.5. L3: Embedding Cache

- **File**: `app/infrastructure/cache/l3_embedding_cache.py`
- Cache query embeddings trong Redis
- Key: `embedding:{query_hash}`
- TTL: 24 hours

#### 3.6. L4: Vector Search (Fallback)

- Integrated trong `memory_repository_impl.py`
- Chỉ được gọi khi tất cả cache layers miss

#### 3.7. Proactive Caching Service

- **File**: `app/infrastructure/cache/proactive_cache.py`
- Service để pre-compute "user favorite" results
- Update L2 materialized view
- Warm up L1 Redis cache

### Phase 4: Application Services Layer (Tuần 3)

#### 4.1. Memory Service

- **File**: `app/domains/memory/application/services/memory_service.py`
- `search_memories()` method
- Cache layer orchestration (L0 → L1 → L2 → L3 → L4)
- Response time optimization với `asyncio.gather()` cho parallel calls

#### 4.2. Extraction Service

- **File**: `app/domains/memory/application/services/extraction_service.py`
- `extract_facts()` method
- Integration với Mem0 client
- Cache invalidation sau extraction

#### 4.3. Job Service

- **File**: `app/domains/memory/application/services/job_service.py`
- `create_extraction_job()` - Enqueue to RabbitMQ
- `get_job_status()` - Poll job status
- Job lifecycle management

### Phase 5: API Layer Refactoring (Tuần 3-4)

#### 5.1. Schemas

- **File**: `app/api/v1/schemas/memory.py`
- `SearchRequest`, `SearchResponse`
- `ExtractRequest`, `ExtractResponse`
- **File**: `app/api/v1/schemas/jobs.py`
- `JobStatusResponse`

#### 5.2. Endpoints

- **File**: `app/api/v1/endpoints/memory.py`
- Refactor `/search_facts` endpoint
    - Inject `MemoryService` via dependency
    - Add caching layer calls
    - Add metrics tracking
- Refactor `/extract_facts` endpoint
    - Return 202 Accepted với job_id
    - Enqueue job to RabbitMQ
- **File**: `app/api/v1/endpoints/jobs.py`
- `GET /jobs/{job_id}/status` endpoint

#### 5.3. Dependencies

- **File**: `app/api/dependencies.py`
- Dependency injection functions
- `get_memory_service()`, `get_job_service()`, `get_db_session()`

#### 5.4. Router

- **File**: `app/api/v1/router.py`
- Include memory và jobs routers
- **File**: `app/main.py`
- FastAPI app initialization
- Include API router
- Add middleware (logging, error handling)

### Phase 6: Async Workers Implementation (Tuần 4)

#### 6.1. RabbitMQ Setup

- **File**: `app/infrastructure/messaging/rabbitmq_service.py`
- RabbitMQ connection và channel management
- Queue declaration: `memory_extraction`
- Message publishing và consuming

#### 6.2. Extraction Worker

- **File**: `workers/tasks/extraction_task.py`
- Consume messages từ RabbitMQ
- Call `ExtractionService` để extract facts
- Update job status trong PostgreSQL
- Error handling và retry logic

#### 6.3. Proactive Caching Worker

- **File**: `workers/tasks/proactive_cache_task.py`
- Scheduled job (mỗi 30 phút)
- Query tất cả users
- Pre-compute "user favorite" results
- Update L2 materialized view và L1 Redis

#### 6.4. Worker Entry Point

- **File**: `workers/main.py`
- Celery hoặc custom worker setup
- Register tasks
- Health check endpoint

### Phase 7: Performance Optimization (Tuần 4-5)

#### 7.1. Async Parallelism

- Sử dụng `asyncio.gather()` trong `memory_service.py`
- Parallel calls: Embedding generation, Vector search, Graph augmentation

#### 7.2. Connection Pooling

- PostgreSQL: SQLAlchemy connection pool tuning
- Redis: Connection pool configuration
- Mem0: HTTP client connection pooling

#### 7.3. Query Optimization

- Vector search: Tune Milvus/Qdrant index parameters
- PostgreSQL: Add indexes cho `jobs` table
- Cache key optimization

#### 7.4. Monitoring & Metrics

- Add Prometheus metrics
- Track cache hit rates (L0, L1, L2, L3)
- Track latency percentiles (P50, P95, P99)

### Phase 8: Testing & Documentation (Tuần 5-6)

#### 8.1. Unit Tests

- Test domain services
- Test repository implementations
- Test cache layers
- Coverage target: > 80%

#### 8.2. Integration Tests

- Test API endpoints với test containers
- Test worker tasks
- Test cache invalidation flow

#### 8.3. Load Testing

- Locust scripts cho load testing
- Target: 500 concurrent users
- Verify P95 latency < 200ms

#### 8.4. Documentation

- API documentation (OpenAPI/Swagger)
- Architecture diagrams
- Runbooks cho operations

## Migration Strategy

### Bước 1: Parallel Run

- Giữ code cũ trong `src/` hoạt động
- Deploy code mới trong `app/` song song
- Route một phần traffic đến version mới

### Bước 2: Data Migration

- Migrate job data từ old schema sang new schema (nếu có)
- Setup database migrations với Alembic

### Bước 3: Cutover

- Switch 100% traffic sang version mới
- Monitor metrics và error rates
- Rollback plan sẵn sàng

## Dependencies cần thêm

```txt
# Message Queue
pika==1.3.2
celery==5.3.4  # Optional, có thể dùng custom worker

# Scheduling
apscheduler==3.10.4  # Cho proactive caching worker

# Resilience
tenacity==8.2.3  # Retry logic
circuitbreaker==2.0.0  # Circuit breaker pattern

# Monitoring
prometheus-client==0.19.0
```



## Risk Mitigation

1. **Breaking Changes**: Giữ backward compatibility trong API contracts
2. **Performance Regression**: Load testing trước khi deploy
3. **Cache Invalidation Bugs**: Comprehensive testing cho cache invalidation logic
4. **Worker Failures**: Implement dead letter queue cho failed jobs

## Success Criteria

- ✅ Code refactored sang Clean Architecture
- ✅ Caching 5 lớp hoạt động với hit rate > 40%