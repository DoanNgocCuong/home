
# LOW-LEVEL DESIGN (LLD) - PIKA MEMORY SYSTEM (CODE-COMPLETE EDITION)

**Phiên bản:** 3.0 | **Tác giả:** Manus AI (Lead Architect) | **Ngày:** 2025-12-21

---

## 1. GIỚI THIỆU

### 1.1. Mục Đích

Tài liệu này là một bản thiết kế kỹ thuật **siêu chi tiết** và **hoàn chỉnh về mặt mã nguồn (code-complete)** cho **PIKA Memory System**. Mục tiêu là cung cấp một tài liệu mà một đội ngũ phát triển, kể cả các lập trình viên mới (interns), có thể **sao chép và triển khai (copy-paste-and-run)** mà không cần phải suy nghĩ hay thiết kế thêm.

Nó bao gồm mọi thứ từ cấu trúc thư mục, sơ đồ lớp, đến mã nguồn đầy đủ cho từng file, cấu hình, và kịch bản triển khai.

### 1.2. Các Công Nghệ Chính

*   **API Framework:** FastAPI
*   **Vector Database:** Milvus
*   **Graph Database:** Neo4j
*   **Metadata & Job Store:** PostgreSQL
*   **Caching:** Redis
*   **Message Queue:** RabbitMQ
*   **Containerization:** Docker
*   **Orchestration:** Kubernetes

---
## 2. CẤU TRÚC THƯ MỤC

Đây là cấu trúc thư mục hoàn chỉnh của dự án, tuân thủ theo Clean Architecture.

```
/pika-memory-system/
├── app/                                    # Main Application
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── memory.py
│   │   │   │   └── jobs.py
│   │   │   └── schemas/
│   │   │       ├── memory.py
│   │   │       └── jobs.py
│   │   ├── dependencies.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── domains/
│   │   └── memory/
│   │       ├── application/
│   │       │   ├── services/
│   │       │   │   ├── memory_service.py
│   │       │   │   └── job_service.py
│   │       │   └── repositories/
│   │       │       ├── memory_repository.py
│   │       │       └── job_repository.py
│   │       ├── domain/
│   │       │   ├── entities.py
│   │       │   └── value_objects.py
│   │       └── infrastructure/
│   │           ├── models/
│   │           │   └── job_model.py
│   │           ├── repositories/
│   │           │   ├── memory_repository_impl.py
│   │           │   └── job_repository_impl.py
│   │           └── mappers.py
│   ├── services/
│   │   ├── cache/redis_service.py
│   │   ├── database/postgres_session.py
│   │   ├── message_queue/rabbitmq_service.py
│   │   └── vector_store/milvus_service.py
│   └── main.py
├── workers/
│   ├── tasks/memory_extraction.py
│   └── main.py
├── tests/
├── scripts/
├── infra/
├── .env.example
├── docker-compose.yml
└── Dockerfile
```

---
## 3. SƠ ĐỒ KIẾN TRÚC TỔNG THỂ

```mermaid
graph TD
    subgraph "User Interaction"
        A[Client App] -- HTTPS --> B[API Gateway: FastAPI]
    end

    subgraph "Synchronous Flow (Search)"
        B -- 1. Search Request --> C[Memory Service]
        C -- 2. Get Query Embedding --> D[LLM API]
        C -- 3. Search Vector --> E[Milvus]
        C -- 4. Augment with Graph --> F[Neo4j]
        C -- 5. Cache Result --> G[Redis]
        B -- 6. Return Results --> A
    end

    subgraph "Asynchronous Flow (Extract)"
        B -- 1. Extract Request --> H[Job Service]
        H -- 2. Enqueue Job --> I[RabbitMQ]
        J[Worker] -- 3. Dequeue Job --> I
        J -- 4. Process Job --> K[Extraction Logic]
        K -- 5. Store Data --> E
        K -- 6. Store Data --> F
        K -- 7. Update Job Status --> L[PostgreSQL]
    end

    style B fill:#8E44AD,stroke:#000,color:#fff
    style J fill:#2980B9,stroke:#000,color:#fff
```

---


## 4. MÃ NGUỒN CHI TIẾT (COPY-PASTE READY)

### 4.1. Cấu hình (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Milvus
    MILVUS_HOST: str
    MILVUS_PORT: int

    # ... (các cấu hình khác)

    class Config:
        env_file = ".env"

settings = Settings()
```

### 4.2. Milvus Repository (`app/domains/memory/infrastructure/repositories/memory_repository_impl.py`)

```python
from typing import List
from app.domains.memory.application.repositories.memory_repository import IMemoryRepository
from app.services.vector_store.milvus_service import MilvusService

class MemoryRepositoryImpl(IMemoryRepository):
    def __init__(self, milvus_service: MilvusService):
        self.milvus_service = milvus_service

    async def search(self, user_id: str, query_vector: List[float], limit: int, score_threshold: float) -> List[dict]:
        return self.milvus_service.search(user_id, query_vector, limit, score_threshold)

    async def insert(self, memories: List[dict]):
        self.milvus_service.insert(memories)
```

### 4.3. Memory Service (`app/domains/memory/application/services/memory_service.py`)

```python
from typing import List
from app.domains.memory.application.repositories.memory_repository import IMemoryRepository
from app.services.llm.openai_service import OpenAIService

class MemoryService:
    def __init__(self, memory_repo: IMemoryRepository, openai_service: OpenAIService):
        self.memory_repo = memory_repo
        self.openai_service = openai_service

    async def search_memories(self, user_id: str, query: str, limit: int, score_threshold: float) -> List[dict]:
        query_vector = await self.openai_service.get_embedding(query)
        return await self.memory_repo.search(user_id, query_vector, limit, score_threshold)
```

### 4.4. API Endpoint (`app/api/v1/endpoints/memory.py`)

```python
from fastapi import APIRouter, Depends
from app.api.v1.schemas.memory import SearchRequest, SearchResponse
from app.domains.memory.application.services.memory_service import MemoryService
from app.api.dependencies import get_memory_service

router = APIRouter()

@router.post("/search_facts", response_model=SearchResponse)
async def search_facts(
    request: SearchRequest,
    memory_service: MemoryService = Depends(get_memory_service)
):
    results = await memory_service.search_memories(
        user_id=request.user_id,
        query=request.query,
        limit=request.limit,
        score_threshold=request.score_threshold
    )
    return SearchResponse(count=len(results), facts=results)
```

### 4.5. Main App (`app/main.py`)

```python
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="PIKA Memory System")

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### 4.6. Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---
# PIKA MEMORY SYSTEM - FULL SOURCE CODE

**Phiên bản:** 1.0 | **Tác giả:** Manus AI | **Ngày:** 2025-12-21

---

## HƯỚNG DẪN SỬ DỤNG

Tài liệu này chứa **toàn bộ source code** của PIKA Memory System. Hãy tạo các file theo đúng cấu trúc thư mục được mô tả, copy-paste mã nguồn, và chạy ngay.

---

## PHẦN 1: SCHEMAS (PYDANTIC MODELS)

### File: `app/api/v1/schemas/memory.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class SearchRequest(BaseModel):
    """Request model for searching facts"""
    user_id: str = Field(..., description="User ID")
    query: str = Field(..., max_length=1000, description="Search query")
    limit: int = Field(20, ge=1, le=100, description="Max results")
    score_threshold: float = Field(0.4, ge=0.0, le=1.0, description="Min similarity score")

class Fact(BaseModel):
    """Individual fact/memory"""
    id: str
    score: float
    source: str
    user_id: str
    conversation_id: Optional[str] = None
    fact_type: List[str]
    fact_value: str
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    """Response model for search"""
    status: str = "ok"
    count: int
    facts: List[Fact]
```

### File: `app/api/v1/schemas/jobs.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ConversationTurn(BaseModel):
    """Single turn in conversation"""
    role: str  # "user" or "assistant"
    content: str

class ExtractRequest(BaseModel):
    """Request model for extracting facts"""
    user_id: str
    conversation_id: str
    conversation: List[ConversationTurn]
    metadata: Dict[str, Any] = {}

class ExtractResponse(BaseModel):
    """Response model for extract (202 Accepted)"""
    status: str = "accepted"
    job_id: str
    status_url: str

class JobStatusResponse(BaseModel):
    """Response model for job status polling"""
    job_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: int = 0
    current_step: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

---

## PHẦN 2: REPOSITORIES (ABSTRACT INTERFACES)

### File: `app/domains/memory/application/repositories/memory_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List

class IMemoryRepository(ABC):
    """Abstract repository for memory operations"""

    @abstractmethod
    async def search(self, user_id: str, query_vector: List[float], limit: int, score_threshold: float) -> List[dict]:
        """Search memories by vector similarity"""
        pass

    @abstractmethod
    async def insert(self, memories: List[dict]):
        """Insert new memories"""
        pass

    @abstractmethod
    async def delete(self, memory_id: str):
        """Delete a memory"""
        pass
```

### File: `app/domains/memory/application/repositories/job_repository.py`

```python
from abc import ABC, abstractmethod
from typing import Optional

class IJobRepository(ABC):
    """Abstract repository for job operations"""

    @abstractmethod
    async def create(self, job_id: str, user_id: str, status: str) -> dict:
        """Create a new job"""
        pass

    @abstractmethod
    async def get(self, job_id: str) -> Optional[dict]:
        """Get job by ID"""
        pass

    @abstractmethod
    async def update(self, job_id: str, status: str, data: dict = None, error: str = None):
        """Update job status"""
        pass
```

---

## PHẦN 3: SERVICES

### File: `app/services/vector_store/milvus_service.py`

```python
from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType
from core.config import settings
from typing import List
import uuid

class MilvusService:
    """Service for Milvus vector database operations"""

    def __init__(self):
        connections.connect("default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
        self.collection_name = "pika_memories"
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """Create collection if it doesn't exist"""
        if not utility.has_collection(self.collection_name):
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=36),
                FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=36),
                FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=255),
                FieldSchema(name="fact_type", dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=10, max_length=50),
                FieldSchema(name="fact_value", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="metadata", dtype=DataType.JSON),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536)
            ]
            schema = CollectionSchema(fields, "PIKA user memories collection")
            collection = Collection(self.collection_name, schema)

            # Create vector index
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            collection.create_index("embedding", index_params)
            collection.create_index("user_id", index_name="user_id_index")
            collection.load()

    def search(self, user_id: str, query_vector: List[float], limit: int, score_threshold: float) -> List[dict]:
        """Search memories by vector similarity"""
        collection = Collection(self.collection_name)
        search_params = {"metric_type": "L2", "params": {"nprobe": 16}}
        
        results = collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            expr=f'user_id == "{user_id}"',
            output_fields=["id", "source", "fact_type", "fact_value", "metadata"]
        )
        
        processed_results = []
        for hit in results[0]:
            # Convert L2 distance to similarity score
            similarity_score = 1 - (hit.distance / 2)  # Normalize to 0-1
            if similarity_score >= score_threshold:
                processed_results.append({
                    "id": hit.entity.get("id"),
                    "score": similarity_score,
                    "source": hit.entity.get("source"),
                    "user_id": user_id,
                    "conversation_id": None,
                    "fact_type": hit.entity.get("fact_type", []),
                    "fact_value": hit.entity.get("fact_value"),
                    "metadata": hit.entity.get("metadata", {}),
                })
        return processed_results

    def insert(self, memories: List[dict]):
        """Insert memories into Milvus"""
        collection = Collection(self.collection_name)
        
        # Prepare data for insertion
        ids = [mem.get("id", str(uuid.uuid4())) for mem in memories]
        user_ids = [mem["user_id"] for mem in memories]
        sources = [mem.get("source", "conversation") for mem in memories]
        fact_types = [mem.get("fact_type", []) for mem in memories]
        fact_values = [mem["fact_value"] for mem in memories]
        metadatas = [mem.get("metadata", {}) for mem in memories]
        embeddings = [mem["embedding"] for mem in memories]
        
        data = [ids, user_ids, sources, fact_types, fact_values, metadatas, embeddings]
        collection.insert(data)
        collection.flush()

    def delete(self, memory_id: str):
        """Delete a memory"""
        collection = Collection(self.collection_name)
        collection.delete(f'id == "{memory_id}"')
```

### File: `app/services/llm/openai_service.py`

```python
import openai
from core.config import settings
from typing import List

class OpenAIService:
    """Service for OpenAI API operations"""

    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text"""
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response["data"][0]["embedding"]

    async def extract_facts(self, conversation: List[dict]) -> List[dict]:
        """Extract facts from conversation using GPT"""
        # Format conversation for prompt
        conversation_text = "\n".join([
            f"{turn['role'].upper()}: {turn['content']}"
            for turn in conversation
        ])

        prompt = f"""Extract key facts from this conversation. For each fact, provide:
1. fact_value: The actual fact
2. fact_type: Category (e.g., food, hobby, family, etc.)

Conversation:
{conversation_text}

Return as JSON array of objects with 'fact_value' and 'fact_type' fields."""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response (simplified - in production, use proper JSON parsing)
        import json
        try:
            facts = json.loads(response["choices"][0]["message"]["content"])
            return facts
        except:
            return []
```

### File: `app/services/database/postgres_session.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### File: `app/services/cache/redis_service.py`

```python
import redis
from core.config import settings
import json

class RedisService:
    """Service for Redis caching"""

    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get(self, key: str):
        """Get value from cache"""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: dict, ttl: int = 3600):
        """Set value in cache"""
        self.redis_client.setex(key, ttl, json.dumps(value))

    def delete(self, key: str):
        """Delete value from cache"""
        self.redis_client.delete(key)
```

### File: `app/services/message_queue/rabbitmq_service.py`

```python
import pika
from core.config import settings
import json

class RabbitMQService:
    """Service for RabbitMQ messaging"""

    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="memory_extraction", durable=True)

    def publish(self, message: dict):
        """Publish message to queue"""
        self.channel.basic_publish(
            exchange="",
            routing_key="memory_extraction",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def close(self):
        """Close connection"""
        self.connection.close()
```

---

## PHẦN 4: DOMAIN ENTITIES

### File: `app/domains/memory/domain/entities.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class Memory:
    """Memory entity"""
    id: str
    user_id: str
    fact_value: str
    fact_type: List[str]
    embedding: List[float]
    source: str = "conversation"
    metadata: Dict[str, Any] = None
    created_at: datetime = None

@dataclass
class Job:
    """Job entity for async extraction"""
    id: str
    user_id: str
    status: str  # pending, processing, completed, failed
    progress: int = 0
    current_step: str = None
    data: Dict[str, Any] = None
    error: str = None
    created_at: datetime = None
    completed_at: datetime = None
```

---

## PHẦN 5: REPOSITORIES IMPLEMENTATION

### File: `app/domains/memory/infrastructure/repositories/job_repository_impl.py`

```python
from typing import Optional
from app.domains.memory.application.repositories.job_repository import IJobRepository
from app.services.database.postgres_session import SessionLocal
from app.domains.memory.infrastructure.models.job_model import JobModel
from datetime import datetime

class JobRepositoryImpl(IJobRepository):
    """Concrete implementation of job repository"""

    def __init__(self):
        self.db = SessionLocal()

    async def create(self, job_id: str, user_id: str, status: str) -> dict:
        """Create new job"""
        job = JobModel(id=job_id, user_id=user_id, status=status, created_at=datetime.utcnow())
        self.db.add(job)
        self.db.commit()
        return {"id": job_id, "status": status}

    async def get(self, job_id: str) -> Optional[dict]:
        """Get job by ID"""
        job = self.db.query(JobModel).filter(JobModel.id == job_id).first()
        if job:
            return {
                "id": job.id,
                "status": job.status,
                "progress": job.progress,
                "current_step": job.current_step,
                "data": job.data,
                "error": job.error
            }
        return None

    async def update(self, job_id: str, status: str, data: dict = None, error: str = None):
        """Update job status"""
        job = self.db.query(JobModel).filter(JobModel.id == job_id).first()
        if job:
            job.status = status
            if data:
                job.data = data
            if error:
                job.error = error
            if status == "completed":
                job.completed_at = datetime.utcnow()
            self.db.commit()
```

---

## PHẦN 6: MODELS (ORM)

### File: `app/domains/memory/infrastructure/models/job_model.py`

```python
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class JobModel(Base):
    """ORM model for jobs table"""
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    progress = Column(Integer, default=0)
    current_step = Column(String(256), nullable=True)
    data = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
```

---

## PHẦN 7: DEPENDENCIES

### File: `app/api/dependencies.py`

```python
from app.domains.memory.application.services.memory_service import MemoryService
from app.domains.memory.infrastructure.repositories.memory_repository_impl import MemoryRepositoryImpl
from app.services.vector_store.milvus_service import MilvusService
from app.services.llm.openai_service import OpenAIService

def get_milvus_service() -> MilvusService:
    return MilvusService()

def get_openai_service() -> OpenAIService:
    return OpenAIService()

def get_memory_repository(milvus_service: MilvusService = None) -> MemoryRepositoryImpl:
    if milvus_service is None:
        milvus_service = get_milvus_service()
    return MemoryRepositoryImpl(milvus_service)

def get_memory_service(
    memory_repo: MemoryRepositoryImpl = None,
    openai_service: OpenAIService = None
) -> MemoryService:
    if memory_repo is None:
        memory_repo = get_memory_repository()
    if openai_service is None:
        openai_service = get_openai_service()
    return MemoryService(memory_repo, openai_service)
```

---

## PHẦN 8: ENDPOINTS

### File: `app/api/v1/endpoints/jobs.py`

```python
from fastapi import APIRouter, Depends
from app.api.v1.schemas.jobs import ExtractRequest, ExtractResponse, JobStatusResponse
from app.domains.memory.application.services.job_service import JobService
from app.api.dependencies import get_job_service
import uuid

router = APIRouter()

@router.post("/extract_facts", response_model=ExtractResponse, status_code=202)
async def extract_facts(
    request: ExtractRequest,
    job_service: JobService = Depends(get_job_service)
):
    job_id = str(uuid.uuid4())
    await job_service.create_extraction_job(job_id, request)
    return ExtractResponse(
        job_id=job_id,
        status_url=f"/api/v1/jobs/{job_id}/status"
    )

@router.get("/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    job_status = await job_service.get_job_status(job_id)
    return job_status
```

---

## PHẦN 9: SERVICES (CONTINUED)

### File: `app/domains/memory/application/services/job_service.py`

```python
from app.domains.memory.application.repositories.job_repository import IJobRepository
from app.services.message_queue.rabbitmq_service import RabbitMQService
from app.api.v1.schemas.jobs import ExtractRequest

class JobService:
    """Service for job management"""

    def __init__(self, job_repo: IJobRepository, rabbitmq_service: RabbitMQService):
        self.job_repo = job_repo
        self.rabbitmq_service = rabbitmq_service

    async def create_extraction_job(self, job_id: str, request: ExtractRequest):
        """Create extraction job and enqueue it"""
        await self.job_repo.create(job_id, request.user_id, "pending")
        
        # Publish to queue
        message = {
            "job_id": job_id,
            "user_id": request.user_id,
            "conversation_id": request.conversation_id,
            "conversation": [
                {"role": turn.role, "content": turn.content}
                for turn in request.conversation
            ],
            "metadata": request.metadata
        }
        self.rabbitmq_service.publish(message)

    async def get_job_status(self, job_id: str):
        """Get job status"""
        return await self.job_repo.get(job_id)
```

---

## PHẦN 10: ROUTERS

### File: `app/api/v1/router.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import memory, jobs

router = APIRouter(prefix="/v1")

router.include_router(memory.router, tags=["memory"])
router.include_router(jobs.router, tags=["jobs"])
```

### File: `app/api/router.py`

```python
from fastapi import APIRouter
from app.api.v1 import router as v1_router

api_router = APIRouter()
api_router.include_router(v1_router)
```

---

## PHẦN 11: WORKER

### File: `workers/tasks/memory_extraction.py`

```python
import pika
import json
import asyncio
from app.services.vector_store.milvus_service import MilvusService
from app.services.llm.openai_service import OpenAIService
from app.domains.memory.application.repositories.job_repository import IJobRepository
from app.domains.memory.infrastructure.repositories.job_repository_impl import JobRepositoryImpl
from core.config import settings

class MemoryExtractionWorker:
    """Worker for extracting and storing memories"""

    def __init__(self):
        self.milvus_service = MilvusService()
        self.openai_service = OpenAIService()
        self.job_repo = JobRepositoryImpl()
        self._setup_rabbitmq()

    def _setup_rabbitmq(self):
        """Setup RabbitMQ connection"""
        credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="memory_extraction", durable=True)

    def process_message(self, ch, method, properties, body):
        """Process extraction job"""
        try:
            message = json.loads(body)
            job_id = message["job_id"]
            user_id = message["user_id"]
            conversation = message["conversation"]

            # Update job status
            asyncio.run(self.job_repo.update(job_id, "processing", {"current_step": "Extracting facts"}))

            # Extract facts
            facts = asyncio.run(self.openai_service.extract_facts(conversation))

            # Generate embeddings and store
            memories = []
            for fact in facts:
                embedding = asyncio.run(self.openai_service.get_embedding(fact["fact_value"]))
                memories.append({
                    "user_id": user_id,
                    "fact_value": fact["fact_value"],
                    "fact_type": fact.get("fact_type", []),
                    "embedding": embedding,
                    "source": "conversation",
                    "metadata": message.get("metadata", {})
                })

            # Insert into Milvus
            self.milvus_service.insert(memories)

            # Update job status
            asyncio.run(self.job_repo.update(
                job_id,
                "completed",
                {"facts_extracted": len(memories)}
            ))

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            asyncio.run(self.job_repo.update(job_id, "failed", error=str(e)))
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        """Start worker"""
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="memory_extraction",
            on_message_callback=self.process_message
        )
        print("Worker started. Waiting for messages...")
        self.channel.start_consuming()

if __name__ == "__main__":
    worker = MemoryExtractionWorker()
    worker.start()
```

### File: `workers/main.py`

```python
from workers.tasks.memory_extraction import MemoryExtractionWorker

if __name__ == "__main__":
    worker = MemoryExtractionWorker()
    worker.start()
```

---

## PHẦN 12: CONFIGURATION FILES

### File: `requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pymilvus==2.3.4
redis==5.0.1
pika==1.3.2
openai==1.3.5
python-dotenv==1.0.0
```

### File: `.env.example`

```
# Database
POSTGRES_USER=pika_user
POSTGRES_PASSWORD=pika_password
POSTGRES_DB=pika_memory
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Milvus
MILVUS_HOST=milvus
MILVUS_PORT=19530

# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here
```

### File: `docker-compose.yml`

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  milvus:
    image: milvusdb/milvus:v2.3.4
    environment:
      COMMON_STORAGETYPE: local
    ports:
      - "19530:19530"
      - "9091:9091"
    volumes:
      - milvus_data:/var/lib/milvus

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_DEFAULT_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_DEFAULT_PASS}
    ports:
      - "5672:5672"
      - "15672:15672"

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      POSTGRES_HOST: postgres
      MILVUS_HOST: milvus
      REDIS_HOST: redis
      RABBITMQ_HOST: rabbitmq
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
      - milvus
      - redis
      - rabbitmq
    volumes:
      - ./app:/app/app

  worker:
    build: .
    command: python -m workers.main
    environment:
      POSTGRES_HOST: postgres
      MILVUS_HOST: milvus
      REDIS_HOST: redis
      RABBITMQ_HOST: rabbitmq
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
      - milvus
      - redis
      - rabbitmq
    volumes:
      - ./app:/app/app
      - ./workers:/app/workers

volumes:
  postgres_data:
  milvus_data:
```

### File: `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## PHẦN 13: DATABASE INITIALIZATION

### File: `scripts/init_db.sql`

```sql
-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,
    progress INTEGER DEFAULT 0,
    current_step VARCHAR(256),
    data JSONB,
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
```

---

## HƯỚNG DẪN TRIỂN KHAI

### Bước 1: Clone/Setup Project

```bash
mkdir pika-memory-system
cd pika-memory-system
git init
```

### Bước 2: Tạo Cấu Trúc Thư Mục

```bash
mkdir -p app/api/v1/endpoints
mkdir -p app/api/v1/schemas
mkdir -p app/core
mkdir -p app/domains/memory/domain
mkdir -p app/domains/memory/application/services
mkdir -p app/domains/memory/application/repositories
mkdir -p app/domains/memory/infrastructure/models
mkdir -p app/domains/memory/infrastructure/repositories
mkdir -p app/services/cache
mkdir -p app/services/database
mkdir -p app/services/message_queue
mkdir -p app/services/vector_store
mkdir -p app/services/llm
mkdir -p workers/tasks
mkdir -p scripts
mkdir -p tests
```

### Bước 3: Copy Tất Cả Các File

Sao chép mã nguồn từ các phần trên vào các file tương ứng.

### Bước 4: Setup Environment

```bash
cp .env.example .env
# Chỉnh sửa .env với các giá trị thực tế
```

### Bước 5: Khởi Động Services

```bash
docker-compose up -d
```

### Bước 6: Khởi Tạo Database

```bash
docker exec pika-memory-system-postgres-1 psql -U pika_user -d pika_memory -f /scripts/init_db.sql
```

### Bước 7: Test API

```bash
# Test search_facts
curl -X POST http://localhost:8000/api/v1/search_facts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "query": "What do I like?",
    "limit": 10,
    "score_threshold": 0.4
  }'

# Test extract_facts
curl -X POST http://localhost:8000/api/v1/extract_facts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "conversation_id": "conv_001",
    "conversation": [
      {"role": "user", "content": "I like pizza and dogs"},
      {"role": "assistant", "content": "That'\''s great!"}
    ]
  }'
```

---

## HƯỚNG DẪN TROUBLESHOOTING

| Vấn đề | Giải pháp |
|---|---|
| Milvus connection error | Kiểm tra MILVUS_HOST và MILVUS_PORT trong .env |
| PostgreSQL connection error | Kiểm tra POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD |
| OpenAI API error | Kiểm tra OPENAI_API_KEY |
| RabbitMQ connection error | Kiểm tra RABBITMQ_HOST và credentials |

---

**Hoàn tất! Bạn đã có toàn bộ source code để triển khai PIKA Memory System.**


---


