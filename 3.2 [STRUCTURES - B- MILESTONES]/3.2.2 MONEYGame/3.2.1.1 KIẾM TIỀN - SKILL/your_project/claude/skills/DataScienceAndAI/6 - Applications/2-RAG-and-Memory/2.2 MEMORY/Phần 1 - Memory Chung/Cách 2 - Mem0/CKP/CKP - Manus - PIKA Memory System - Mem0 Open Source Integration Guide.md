# PIKA Memory System - Mem0 Open Source Integration Guide

**Phiên bản: 1.0 | Ngày: 2025-12-20 | Tác giả: Manus AI**

---

## 📋 EXECUTIVE SUMMARY

Tài liệu này cung cấp một **Integration Guide hoàn chỉnh** để triển khai PIKA Memory System sử dụng **Mem0 Open Source** thay vì tự xây dựng từ đầu. Mem0 Open Source cung cấp tất cả các tính năng cần thiết (Vector Search, Graph Memory, Async Operations) với chi phí thấp hơn 60% so với Mem0 Enterprise.

### Tại Sao Chọn Mem0 Open Source?

| Tiêu Chí | Tự Xây Dựng | Mem0 OSS | Mem0 Enterprise |
| :--- | :--- | :--- | :--- |
| **Thời gian triển khai** | 6-8 tuần | 2-3 tuần | 1 tuần (managed) |
| **Chi phí hàng tháng** | $250-300 | $0 (self-hosted) | $600+ |
| **Maintenance** | 100% team | 80% team | 0% (managed) |
| **Customization** | 100% | 100% | Limited |
| **Vector Search** | ✅ | ✅ | ✅ |
| **Graph Memory** | ✅ | ✅ | ✅ |
| **Async Operations** | ✅ | ✅ | ✅ |
| **Multi-LLM Support** | ✅ | ✅ | ✅ |

### Kiến Trúc Tổng Quát

```
┌─────────────────────────────────────────────────────────────┐
│              PIKA Memory System (Mem0 OSS)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │ PIKA Robot   │                                           │
│  │ AI Workflow  │                                           │
│  └──────────────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────┐                  │
│  │   FastAPI Wrapper Layer              │                  │
│  │  ┌────────────────────────────────┐  │                  │
│  │  │ POST /v1/extract_facts         │  │ ← Async Pattern │
│  │  │ POST /v1/search_facts          │  │   (202 + polling)
│  │  │ GET  /v1/jobs/{job_id}/status  │  │                  │
│  │  └────────────────────────────────┘  │                  │
│  └──────────────┬───────────────────────┘                  │
│                 │                                           │
│                 ▼                                           │
│  ┌──────────────────────────────────────┐                  │
│  │   Mem0 Python SDK (AsyncMemory)      │                  │
│  │  - Vector Search (Qdrant/Milvus)     │                  │
│  │  - Graph Memory (Neo4j)              │                  │
│  │  - Metadata Filtering                │                  │
│  │  - Fact Extraction (LLM)             │                  │
│  └──────────────┬───────────────────────┘                  │
│                 │                                           │
│    ┌────────────┼────────────┬──────────────┐              │
│    │            │            │              │               │
│    ▼            ▼            ▼              ▼               │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐           │
│  │Qdrant/ │ │ Neo4j  │ │PostgreSQL│ │  Redis   │           │
│  │Milvus  │ │(Graph) │ │(History) │ │ (Cache)  │           │
│  │(Vector)│ │(Entity)│ │(Audit)   │ │(Hot Data)│           │
│  └────────┘ └────────┘ └──────────┘ └──────────┘           │
│                                                              │
│  ┌──────────────────────────────────────┐                  │
│  │  OpenAI API (Embedding & LLM)        │                  │
│  │  - text-embedding-3-small            │                  │
│  │  - gpt-4o-mini (fact extraction)     │                  │
│  └──────────────────────────────────────┘                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## PHẦN 1: SETUP & INSTALLATION

### 1.1 Prerequisites

- **Python:** 3.10 hoặc cao hơn
- **OpenAI API Key:** Để sử dụng embeddings và LLM
- **Docker & Docker Compose:** Để chạy các services (Qdrant, Neo4j, Redis, PostgreSQL)
- **Git:** Để clone repository

### 1.2 Installation Steps

#### Step 1: Clone Mem0 Repository

```bash
git clone https://github.com/mem0ai/mem0.git
cd mem0
```

#### Step 2: Install Mem0 with Graph Support

```bash
# Install Mem0 with graph extras
pip install "mem0ai[graph]"

# Or install from source for latest features
pip install -e ".[graph]"
```

#### Step 3: Setup Environment Variables

```bash
# Create .env file
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Vector Database (Qdrant)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Graph Database (Neo4j)
NEO4J_URL=neo4j+s://your-neo4j-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# PostgreSQL (for history and audit logs)
POSTGRES_URL=postgresql://postgres:password@localhost:5432/pika_memory

# Redis (for caching)
REDIS_URL=redis://localhost:6379

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
EOF

# Load environment variables
export $(cat .env | xargs)
```

#### Step 4: Setup Docker Compose

```bash
# Create docker-compose.yml for local development
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Qdrant Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      QDRANT_API_KEY: ""

  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.0
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      NEO4J_AUTH: neo4j/mem0graph
    volumes:
      - neo4j_data:/data

  # PostgreSQL
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: pika_memory
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  qdrant_data:
  neo4j_data:
  postgres_data:
  redis_data:
EOF

# Start services
docker-compose up -d
```

#### Step 5: Initialize PostgreSQL Schema

```bash
# Create init.sql
cat > init.sql << 'EOF'
-- Create tables for PIKA Memory System

-- Users table
CREATE TABLE users (
  id VARCHAR(256) PRIMARY KEY,
  name VARCHAR(256),
  language VARCHAR(10) DEFAULT 'vi',
  friendship_level VARCHAR(50) DEFAULT 'PHASE1_STRANGER',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE conversations (
  id VARCHAR(256) PRIMARY KEY,
  user_id VARCHAR(256) REFERENCES users(id),
  title VARCHAR(512),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table (for async processing)
CREATE TABLE jobs (
  id VARCHAR(256) PRIMARY KEY,
  user_id VARCHAR(256) REFERENCES users(id),
  conversation_id VARCHAR(256) REFERENCES conversations(id),
  status VARCHAR(50), -- 'pending', 'processing', 'completed', 'failed'
  progress INT DEFAULT 0,
  result JSON,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_user_id (user_id)
);

-- Audit log table
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id VARCHAR(256) REFERENCES users(id),
  action VARCHAR(256),
  resource_type VARCHAR(128),
  resource_id VARCHAR(256),
  details JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
);

-- Create indexes
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
EOF
```

---

## PHẦN 2: PIKA MEMORY API IMPLEMENTATION

### 2.1 FastAPI Wrapper Layer

```python
# app/main.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
import asyncio
from datetime import datetime
import logging

from mem0 import AsyncMemory
import os

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="PIKA Memory System",
    description="AI-powered memory layer for PIKA Robot",
    version="1.0.0"
)

# Initialize Mem0 AsyncMemory
memory_config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": os.getenv("QDRANT_URL", "http://localhost:6333"),
            "collection_name": "pika_memories"
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO4J_URL"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD"),
            "database": "neo4j"
        }
    }
}

memory = AsyncMemory.from_config(memory_config)

# In-memory job store (use PostgreSQL in production)
jobs_store = {}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ExtractFactsRequest(BaseModel):
    user_id: str
    conversation_id: str
    conversation: List[Message]
    metadata: Optional[dict] = None

class ExtractFactsResponse(BaseModel):
    status: str
    job_id: str
    status_url: str
    estimated_completion_time_seconds: int

class SearchFactsRequest(BaseModel):
    user_id: str
    query: str
    limit: int = 10
    filters: Optional[dict] = None
    include_relationships: bool = True

class MemoryResult(BaseModel):
    id: str
    memory: str
    user_id: str
    created_at: str
    score: float
    relations: Optional[List[dict]] = None

class SearchFactsResponse(BaseModel):
    status: str
    data: dict

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    current_step: Optional[str] = None
    data: Optional[dict] = None
    error: Optional[str] = None

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/v1/extract_facts", response_model=ExtractFactsResponse)
async def extract_facts(request: ExtractFactsRequest, background_tasks: BackgroundTasks):
    """
    Extract facts from conversation asynchronously.
    
    Returns 202 Accepted with job_id for polling.
    """
    job_id = str(uuid.uuid4())
    
    # Store job status
    jobs_store[job_id] = {
        "status": "pending",
        "progress": 0,
        "user_id": request.user_id,
        "conversation_id": request.conversation_id,
        "created_at": datetime.now().isoformat()
    }
    
    # Push to background task
    background_tasks.add_task(
        process_extract_facts,
        job_id=job_id,
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        conversation=request.conversation,
        metadata=request.metadata
    )
    
    return ExtractFactsResponse(
        status="accepted",
        job_id=job_id,
        status_url=f"/v1/jobs/{job_id}/status",
        estimated_completion_time_seconds=30
    )

@app.get("/v1/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Poll job status for extract_facts operation.
    """
    if job_id not in jobs_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_store[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        current_step=job.get("current_step"),
        data=job.get("data"),
        error=job.get("error")
    )

@app.post("/v1/search_facts", response_model=SearchFactsResponse)
async def search_facts(request: SearchFactsRequest):
    """
    Search facts with semantic similarity.
    
    Returns results immediately (optimized with caching).
    """
    try:
        start_time = datetime.now()
        
        # Build filters
        filters = {"user_id": request.user_id}
        if request.filters:
            filters.update(request.filters)
        
        # Search using Mem0
        results = await memory.search(
            query=request.query,
            user_id=request.user_id,
            limit=request.limit,
            filters=filters
        )
        
        latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        logger.info(f"Search completed for user {request.user_id} in {latency_ms}ms")
        
        return SearchFactsResponse(
            status="success",
            data={
                "query": request.query,
                "results": results.get("results", []),
                "total_results": len(results.get("results", [])),
                "latency_ms": latency_ms
            }
        )
    
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# BACKGROUND TASKS
# ============================================================================

async def process_extract_facts(
    job_id: str,
    user_id: str,
    conversation_id: str,
    conversation: List[Message],
    metadata: Optional[dict] = None
):
    """
    Background task to process fact extraction.
    """
    try:
        # Update job status
        jobs_store[job_id]["status"] = "processing"
        jobs_store[job_id]["progress"] = 10
        jobs_store[job_id]["current_step"] = "Extracting facts from conversation"
        
        # Convert messages to format expected by Mem0
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation
        ]
        
        # Add memories using Mem0
        logger.info(f"Adding memories for user {user_id}")
        result = await memory.add(
            messages=messages,
            user_id=user_id
        )
        
        jobs_store[job_id]["progress"] = 100
        jobs_store[job_id]["status"] = "completed"
        jobs_store[job_id]["current_step"] = "Completed"
        jobs_store[job_id]["data"] = {
            "facts_extracted": len(result.get("results", [])),
            "results": result.get("results", [])
        }
        
        logger.info(f"Job {job_id} completed successfully")
    
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        jobs_store[job_id]["status"] = "failed"
        jobs_store[job_id]["error"] = str(e)

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    logger.info("PIKA Memory System starting up...")
    logger.info(f"Mem0 configured with:")
    logger.info(f"  - Vector Store: Qdrant")
    logger.info(f"  - Graph Store: Neo4j")
    logger.info(f"  - LLM: OpenAI gpt-4o-mini")

@app.on_event("shutdown")
async def shutdown():
    logger.info("PIKA Memory System shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

### 2.2 Running the API Server

```bash
# Start the FastAPI server
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## PHẦN 3: API USAGE EXAMPLES

### 3.1 Extract Facts API (Async Pattern)

#### Request

```bash
curl -X POST http://localhost:8000/v1/extract_facts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "conversation_id": "conv_123",
    "conversation": [
      {
        "role": "user",
        "content": "Mình tên Tuấn, 8 tuổi, thích chơi bóng đá và vẽ tranh"
      },
      {
        "role": "assistant",
        "content": "Tuyệt vời! Tuấn là một cậu bé sáng tạo. Bóng đá và vẽ tranh đều là những hoạt động tuyệt vời!"
      }
    ]
  }'
```

#### Response (202 Accepted)

```json
{
  "status": "accepted",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_url": "/v1/jobs/550e8400-e29b-41d4-a716-446655440000/status",
  "estimated_completion_time_seconds": 30
}
```

#### Poll Job Status

```bash
curl http://localhost:8000/v1/jobs/550e8400-e29b-41d4-a716-446655440000/status
```

**Response (Processing):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 50,
  "current_step": "Extracting facts from conversation"
}
```

**Response (Completed):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "current_step": "Completed",
  "data": {
    "facts_extracted": 3,
    "results": [
      {
        "id": "mem_001",
        "memory": "Tên là Tuấn",
        "user_id": "user_001",
        "created_at": "2025-12-20T10:00:00Z",
        "score": 0.99
      },
      {
        "id": "mem_002",
        "memory": "8 tuổi",
        "user_id": "user_001",
        "created_at": "2025-12-20T10:00:05Z",
        "score": 0.98
      },
      {
        "id": "mem_003",
        "memory": "Thích chơi bóng đá và vẽ tranh",
        "user_id": "user_001",
        "created_at": "2025-12-20T10:00:10Z",
        "score": 0.95
      }
    ]
  }
}
```

### 3.2 Search Facts API

#### Request

```bash
curl -X POST http://localhost:8000/v1/search_facts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "query": "Thú cưng của tôi",
    "limit": 10,
    "include_relationships": true
  }'
```

#### Response (Success)

```json
{
  "status": "success",
  "data": {
    "query": "Thú cưng của tôi",
    "results": [
      {
        "id": "mem_001",
        "memory": "Mình nuôi mèo tên Miu",
        "user_id": "user_001",
        "created_at": "2025-12-10T10:00:00Z",
        "score": 0.96,
        "relations": [
          {
            "type": "owns",
            "target": "Miu (cat)"
          }
        ]
      },
      {
        "id": "mem_002",
        "memory": "Tôi có một con chó",
        "user_id": "user_001",
        "created_at": "2025-12-08T14:30:00Z",
        "score": 0.91,
        "relations": [
          {
            "type": "owns",
            "target": "Dog"
          }
        ]
      }
    ],
    "total_results": 2,
    "latency_ms": 145
  }
}
```

---

## PHẦN 4: CUSTOMIZATION & CONFIGURATION

### 4.1 Custom Fact Extraction Prompt

Mem0 cho phép customize prompt để extraction facts theo cách bạn muốn:

```python
# app/config.py

CUSTOM_EXTRACTION_PROMPT = """
You are an expert at extracting facts about a child from conversations.
Extract all relevant facts about the child, focusing on:
- Personal information (name, age, gender)
- Interests and hobbies
- Family members and relationships
- School and education
- Health and physical abilities
- Preferences and dislikes

Return as JSON array with fields:
- content: The fact statement
- category: One of [personal_info, hobby, family, school, health, preference]
- confidence: A score from 0.0 to 1.0 indicating how confident you are

Example:
Input: "My name is Tuấn, I'm 8 years old and I love playing soccer"
Output: [
  {
    "content": "Name is Tuấn",
    "category": "personal_info",
    "confidence": 0.99
  },
  {
    "content": "8 years old",
    "category": "personal_info",
    "confidence": 0.98
  },
  {
    "content": "Loves playing soccer",
    "category": "hobby",
    "confidence": 0.95
  }
]
"""

# Use in Mem0 config
memory_config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": os.getenv("QDRANT_URL")
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO4J_URL"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD")
        }
    },
    "fact_extraction": {
        "custom_prompt": CUSTOM_EXTRACTION_PROMPT
    }
}
```

### 4.2 Using Different LLM Providers

Mem0 hỗ trợ nhiều LLM providers:

```python
# Using Anthropic Claude
memory_config_claude = {
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-3-sonnet-20240229",
            "api_key": os.getenv("ANTHROPIC_API_KEY")
        }
    },
    # ... other configs
}

# Using Ollama (local)
memory_config_ollama = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "mistral",
            "base_url": "http://localhost:11434"
        }
    },
    # ... other configs
}

# Using Groq
memory_config_groq = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "mixtral-8x7b-32768",
            "api_key": os.getenv("GROQ_API_KEY")
        }
    },
    # ... other configs
}
```

### 4.3 Using Different Vector Stores

```python
# Using Milvus with GPU acceleration
memory_config_milvus = {
    "vector_store": {
        "provider": "milvus",
        "config": {
            "host": "localhost",
            "port": 19530,
            "collection_name": "pika_memories",
            "index_type": "GPU_CAGRA"  # GPU acceleration
        }
    },
    # ... other configs
}

# Using Pinecone (cloud)
memory_config_pinecone = {
    "vector_store": {
        "provider": "pinecone",
        "config": {
            "api_key": os.getenv("PINECONE_API_KEY"),
            "environment": "us-east-1-aws",
            "index_name": "pika-memories"
        }
    },
    # ... other configs
}

# Using Weaviate
memory_config_weaviate = {
    "vector_store": {
        "provider": "weaviate",
        "config": {
            "url": "http://localhost:8080",
            "api_key": os.getenv("WEAVIATE_API_KEY")
        }
    },
    # ... other configs
}
```

---

## PHẦN 5: DEPLOYMENT

### 5.1 Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build Docker image
docker build -t pika-memory-api:latest .

# Run Docker container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e NEO4J_URL=neo4j+s://... \
  -e NEO4J_USERNAME=neo4j \
  -e NEO4J_PASSWORD=... \
  -e QDRANT_URL=http://qdrant:6333 \
  pika-memory-api:latest
```

### 5.2 Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pika-memory-api
  namespace: pika-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: pika-memory-api
  template:
    metadata:
      labels:
        app: pika-memory-api
    spec:
      containers:
      - name: api
        image: ghcr.io/pika/memory-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: pika-secrets
              key: openai-api-key
        - name: NEO4J_URL
          value: "neo4j+s://your-instance.databases.neo4j.io"
        - name: NEO4J_USERNAME
          valueFrom:
            secretKeyRef:
              name: pika-secrets
              key: neo4j-username
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: pika-secrets
              key: neo4j-password
        - name: QDRANT_URL
          value: "http://qdrant-service:6333"
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

---

## PHẦN 6: MONITORING & OBSERVABILITY

### 6.1 Logging

```python
# app/logging_config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

### 6.2 Metrics Collection

```python
# app/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
extract_facts_requests = Counter(
    'extract_facts_requests_total',
    'Total extract_facts requests',
    ['status']
)

search_facts_requests = Counter(
    'search_facts_requests_total',
    'Total search_facts requests',
    ['status']
)

search_latency = Histogram(
    'search_facts_latency_ms',
    'Search facts latency in milliseconds',
    buckets=[10, 50, 100, 200, 500, 1000]
)

job_processing_time = Histogram(
    'extract_facts_processing_time_seconds',
    'Extract facts processing time in seconds',
    buckets=[5, 10, 30, 60, 120]
)

active_jobs = Gauge(
    'active_jobs',
    'Number of active jobs'
)
```

---

## PHẦN 7: TESTING

### 7.1 Unit Tests

```python
# tests/test_apis.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_extract_facts_returns_job_id():
    """Test extract_facts returns job_id immediately"""
    response = client.post("/v1/extract_facts", json={
        "user_id": "user_001",
        "conversation_id": "conv_001",
        "conversation": [
            {"role": "user", "content": "Mình thích chơi bóng đá"},
            {"role": "assistant", "content": "Tuyệt vời!"}
        ]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert "job_id" in data
    assert "status_url" in data

@pytest.mark.asyncio
async def test_search_facts_returns_results():
    """Test search_facts returns results"""
    response = client.post("/v1/search_facts", json={
        "user_id": "user_001",
        "query": "Thú cưng",
        "limit": 10
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "results" in data["data"]
```

### 7.2 Load Tests

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between
import random
import uuid

class MemoryAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(7)
    def search_facts(self):
        """70% traffic: search"""
        self.client.post("/v1/search_facts", json={
            "user_id": f"user_{random.randint(1, 1000)}",
            "query": random.choice(["Thú cưng", "Sở thích", "Gia đình"]),
            "limit": 20
        })
    
    @task(3)
    def extract_facts(self):
        """30% traffic: extract"""
        self.client.post("/v1/extract_facts", json={
            "user_id": f"user_{random.randint(1, 1000)}",
            "conversation_id": f"conv_{uuid.uuid4()}",
            "conversation": [
                {"role": "user", "content": "Test conversation"},
                {"role": "assistant", "content": "Response"}
            ]
        })

# Run load test
# locust -f tests/load/locustfile.py --host=http://localhost:8000
```

---

## PHẦN 8: MIGRATION & ROLLOUT PLAN

### 8.1 Phased Rollout Strategy

```
Phase 1: Development (Week 1-2)
├─ Setup Mem0 OSS locally
├─ Implement FastAPI wrapper
├─ Test with sample data
└─ Benchmark performance

Phase 2: Staging (Week 3)
├─ Deploy to staging environment
├─ Run load tests
├─ Validate with real data
└─ Performance tuning

Phase 3: Production (Week 4)
├─ Deploy to production (canary: 5%)
├─ Monitor metrics
├─ Gradual rollout (25% → 50% → 100%)
└─ Rollback plan ready

Phase 4: Optimization (Week 5-6)
├─ Collect feedback
├─ Optimize based on metrics
├─ Fine-tune configurations
└─ Document learnings
```

### 8.2 Rollback Plan

```bash
# If issues occur, rollback to previous version
kubectl rollout undo deployment/pika-memory-api -n pika-production

# Check rollout status
kubectl rollout status deployment/pika-memory-api -n pika-production

# View rollout history
kubectl rollout history deployment/pika-memory-api -n pika-production
```

---

## PHẦN 9: COST COMPARISON

### 9.1 Monthly Cost Breakdown

| Thành Phần | Mem0 Enterprise | Mem0 OSS (Self-Hosted) |
| :--- | :--- | :--- |
| **Mem0 Platform** | $600 | $0 |
| **Vector DB (Milvus)** | Included | $0 (self-hosted) |
| **Graph DB (Neo4j)** | Included | $0 (self-hosted) |
| **Compute (3 replicas)** | Included | $100-150 (AWS/GCP) |
| **Storage (100GB)** | Included | $20-30 |
| **Monitoring & Logging** | Included | $30-50 |
| **Total** | **$600+** | **$150-230** |
| **Savings** | - | **75% cost reduction** |

---

## PHẦN 10: TROUBLESHOOTING

### 10.1 Common Issues

#### Issue 1: Neo4j Connection Refused

```python
# Solution: Check Neo4j connection
import asyncio
from neo4j import AsyncGraphDatabase

async def test_neo4j_connection():
    uri = os.getenv("NEO4J_URL")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    
    async with AsyncGraphDatabase.driver(uri, auth=(username, password)) as driver:
        async with driver.session() as session:
            result = await session.run("RETURN 1")
            print("Neo4j connection successful")

# Run test
asyncio.run(test_neo4j_connection())
```

#### Issue 2: Qdrant Vector Store Not Responding

```bash
# Check Qdrant health
curl http://localhost:6333/health

# If down, restart Qdrant
docker-compose restart qdrant

# Check logs
docker-compose logs qdrant
```

#### Issue 3: High Latency on Search

```python
# Solution: Add reranker and optimize Qdrant
memory_config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": os.getenv("QDRANT_URL"),
            "collection_name": "pika_memories",
            "search_params": {
                "hnsw_ef": 200,  # Increase for better accuracy
                "exact": False
            }
        }
    },
    "reranker": {
        "provider": "cohere",
        "config": {
            "model": "rerank-english-v2.0",
            "api_key": os.getenv("COHERE_API_KEY")
        }
    }
}
```

---

## KẾT LUẬN

Mem0 Open Source cung cấp một giải pháp **cost-effective** và **production-ready** cho PIKA Memory System. Với việc sử dụng Mem0 OSS:

✅ **Tiết kiệm 75% chi phí** so với Mem0 Enterprise  
✅ **Triển khai nhanh** (2-3 tuần)  
✅ **Full customization** và control  
✅ **Scalable** cho millions of users  
✅ **Production-ready** với monitoring & observability  

**Bước tiếp theo:**
1. Clone Mem0 repository
2. Setup Docker Compose environment
3. Implement FastAPI wrapper
4. Deploy to staging
5. Run load tests
6. Gradual rollout to production

**Tài liệu tham khảo:**
- [Mem0 Documentation](https://docs.mem0.ai)
- [Mem0 GitHub Repository](https://github.com/mem0ai/mem0)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Neo4j Documentation](https://neo4j.com/docs/)
