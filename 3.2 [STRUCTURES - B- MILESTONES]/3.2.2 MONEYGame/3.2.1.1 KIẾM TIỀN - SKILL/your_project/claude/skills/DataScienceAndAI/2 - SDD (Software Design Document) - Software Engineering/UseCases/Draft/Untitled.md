# Low-Level Design Document
## Robot Workflow Orchestration System - Implementation Details

**Prepared by:** Manus AI  
**Date:** December 13, 2025  
**Version:** 1.0  
**Classification:** Technical Implementation Document

---

## Executive Summary

This Low-Level Design (LLD) document provides detailed implementation specifications for the Robot Workflow Orchestration System. It covers class hierarchies, method signatures, database schemas, API specifications, and code-level design decisions. This document serves as the blueprint for developers implementing the system components.

---

## 1. Class Hierarchy and Component Design

### 1.1 BaseAgent Class

**Location:** `app/common/agent/base.py`

**Purpose:** Abstract base class for all agents, providing core execution and messaging capabilities.

**Class Definition:**
```python
class BaseAgent(Generic[T]):
    graph: CompiledStateGraph
    name: str
    recursion_limit: int = 600
    trace_enabled: bool = True
    
    def __init__(self, **kwargs):
        """Inject dependencies via kwargs"""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def run(self, input_state: T) -> Dict[str, Any]:
        """Synchronous wrapper around run_async"""
        return asyncio.run(self.run_async(input_state))
    
    @observe(capture_input=False, capture_output=False)
    async def run_async(
        self,
        input_state: T,
        on_error_callback: Optional[Callable] = None,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Execute the agent's LangGraph and handle events"""
        try:
            output = None
            async for event in self.graph.astream_events(
                input_state,
                version="v2",
                config={"recursion_limit": self.recursion_limit}
            ):
                event_type = event.get("event")
                match event_type:
                    case "error":
                        raise Exception(event.get("data"))
                    case "on_custom_event":
                        if event.get("name") == "output":
                            output = event.get("data")
            return {"status": "success", "output": output}
        except Exception as e:
            # Error handling and Kafka notification
            logger.error(f"Error executing graph: {str(e)}")
            # ... error processing ...
            return {"status": "error", "error": error_message}
    
    async def send_kafka_one(
        self,
        value: KafkaMessage,
        topic: str | None = None
    ) -> None:
        """Send a message to Kafka if configured"""
        if not hasattr(self, "kafka"):
            logger.warning("Kafka not configured")
            return
        
        kafka_producer = getattr(self, "kafka")
        target_topic = topic or getattr(self, "kafka_topic", None)
        await kafka_producer.send_kafka_one(value, target_topic)
```

**Key Design Decisions:**

The class uses Python's Generic type parameter to maintain type safety for the state object. The `@observe` decorator from Langfuse automatically captures execution traces without requiring explicit instrumentation.

The `run_async` method implements an event-driven loop that processes events emitted by LangGraph. This allows the agent to react to intermediate steps, capture custom events, and handle errors gracefully.

The dependency injection pattern in `__init__` allows agents to receive any dependencies they need without tight coupling. This is crucial for testability and flexibility.

### 1.2 AgentRegistry Class

**Location:** `app/common/agent/registry.py`

**Purpose:** Central registry for agent discovery and metadata management.

**Class Definition:**
```python
@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    description: str
    input_model: Type[BaseModel]
    state_model: Type[BaseState]
    input_to_state: Callable[[BaseModel], BaseState]
    kafka_topic: Optional[str] = None
    dependency_specs: Dict[str, str] = None

class AgentRegistry:
    """Central registry for all agents (Singleton)"""
    _instance: Optional["AgentRegistry"] = None
    _agents: Dict[str, Type[BaseAgent]] = {}
    _configs: Dict[str, AgentConfig] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, agent_id: str, config: AgentConfig):
        """Register an agent"""
        def decorator(agent_class: Type[BaseAgent]):
            if not issubclass(agent_class, BaseAgent):
                raise ValueError("Agent must inherit from BaseAgent")
            
            cls._agents[agent_id] = agent_class
            cls._configs[agent_id] = config
            agent_class.agent_id = agent_id
            agent_class.kafka_topic = config.kafka_topic
            
            return agent_class
        return decorator
    
    @classmethod
    def get_agent_class(cls, agent_id: str) -> Type[BaseAgent]:
        """Get agent class by ID"""
        if agent_id not in cls._agents:
            raise ValueError(f"Agent '{agent_id}' not found")
        return cls._agents[agent_id]
    
    @classmethod
    def get_agent_config(cls, agent_id: str) -> AgentConfig:
        """Get agent configuration"""
        if agent_id not in cls._configs:
            raise ValueError(f"Config for '{agent_id}' not found")
        return cls._configs[agent_id]
    
    @classmethod
    def list_agent_ids(cls) -> List[str]:
        """Get all registered agent IDs"""
        return list(cls._agents.keys())
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents"""
        result = {}
        for agent_id in cls._agents:
            config = cls._configs[agent_id]
            result[agent_id] = {
                "name": config.name,
                "description": config.description,
                "input_model": config.input_model.__name__,
                "kafka_topic": config.kafka_topic,
                "class": cls._agents[agent_id].__name__
            }
        return result
```

**Key Design Decisions:**

The singleton pattern ensures only one registry exists globally. The dataclass `AgentConfig` provides type-safe configuration storage.

The registry stores both agent classes and their configurations separately, allowing efficient lookups and metadata queries.

### 1.3 AgentFactory Class

**Location:** `app/common/agent/factory.py`

**Purpose:** Factory for creating and managing agent instances.

**Class Definition:**
```python
class AgentFactory:
    """Factory for creating and managing agent instances"""
    
    def __init__(self, dependency_resolver: DependencyResolver):
        self.dependency_resolver = dependency_resolver
        self._agent_instances: Dict[str, BaseAgent] = {}
        
        logger.info("Initializing AgentFactory...")
        self._auto_discover_agents()
        self._preload_all_agents()
    
    def _auto_discover_agents(self):
        """Automatically discover and import all agent modules"""
        try:
            agent_package_path = "app.module.agent"
            package = importlib.import_module(agent_package_path)
            
            for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                if is_pkg and not module_name.startswith("_"):
                    try:
                        agent_module_path = f"{agent_package_path}.{module_name}.agent"
                        importlib.import_module(agent_module_path)
                        logger.info(f"Discovered: {agent_module_path}")
                    except ImportError as e:
                        logger.debug(f"Could not import {agent_module_path}: {e}")
        except Exception as e:
            logger.error(f"Error during auto-discovery: {e}")
    
    def _preload_all_agents(self):
        """Preload all discovered agents"""
        logger.info("Starting agent preloading...")
        start_time = time.time()
        
        success_count = 0
        failed_count = 0
        
        agent_ids = AgentRegistry.list_agent_ids()
        if not agent_ids:
            logger.info("No agents found to preload")
            return
        
        for agent_id in agent_ids:
            try:
                logger.info(f"Preloading agent: {agent_id}")
                agent_start_time = time.time()
                
                self.get_agent(agent_id)
                
                agent_time = time.time() - agent_start_time
                success_count += 1
                logger.info(f"✓ Preloaded '{agent_id}' in {agent_time:.2f}s")
            except Exception as e:
                failed_count += 1
                logger.error(f"✗ Failed to preload '{agent_id}': {e}")
        
        total_time = time.time() - start_time
        logger.info(f"Preloading completed in {total_time:.2f}s")
        logger.info(f"Results: {success_count} successful, {failed_count} failed")
    
    def get_agent(self, agent_id: str) -> BaseAgent:
        """Get or create an agent instance"""
        if agent_id in self._agent_instances:
            return self._agent_instances[agent_id]
        
        try:
            agent_class = AgentRegistry.get_agent_class(agent_id)
            config = AgentRegistry.get_agent_config(agent_id)
        except ValueError as e:
            logger.error(f"Agent not found: {e}")
            raise
        
        try:
            dependencies = self.dependency_resolver.resolve(
                config.dependency_specs or {}
            )
        except Exception as e:
            logger.error(f"Failed to resolve dependencies: {e}")
            raise
        
        try:
            agent_instance = agent_class(**dependencies)
            self._agent_instances[agent_id] = agent_instance
            logger.info(f"Created agent: {agent_id}")
            return agent_instance
        except Exception as e:
            logger.error(f"Failed to create agent {agent_id}: {e}")
            raise
    
    def list_available_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all available agents"""
        return AgentRegistry.get_all_agents()
    
    def clear_cache(self):
        """Clear all cached agent instances"""
        self._agent_instances.clear()
        logger.info("Cleared agent instance cache")
```

**Key Design Decisions:**

The factory implements eager loading, initializing all agents during construction. This ensures the first request doesn't experience cold-start latency.

Auto-discovery uses Python's `importlib` and `pkgutil` to dynamically find and import agent modules. This is completely automatic and requires no configuration.

Caching of agent instances ensures that the same instance is reused for all requests, reducing memory overhead and initialization time.

### 1.4 DependencyResolver Class

**Location:** `app/common/dependency_resolver.py`

**Purpose:** Resolve and inject dependencies for agents.

**Class Definition:**
```python
@dataclass
class DependencySpec:
    """Specification for a dependency"""
    factory: Optional[Callable[[], Any]] = None
    singleton: Optional[Any] = None
    
    def __post_init__(self):
        if self.factory and self.singleton:
            raise ValueError("Cannot specify both")
        if not self.factory and self.singleton is None:
            raise ValueError("Must specify either factory or singleton")

class DependencyResolver:
    """Resolves dependencies for agents"""
    
    def __init__(self):
        self._registry: Dict[str, DependencySpec] = {}
        self._cache: Dict[str, Any] = {}
    
    def register(
        self,
        key: str,
        factory: Optional[Callable] = None,
        singleton: Optional[Any] = None
    ):
        """Register a dependency"""
        self._registry[key] = DependencySpec(factory=factory, singleton=singleton)
        logger.info(f"Registered dependency: {key}")
    
    def resolve(self, dependency_specs: Dict[str, str]) -> Dict[str, Any]:
        """Resolve dependencies based on specs"""
        resolved = {}
        
        for param_name, dep_key in dependency_specs.items():
            if dep_key not in self._registry:
                raise ValueError(f"Unknown dependency: {dep_key}")
            
            spec = self._registry[dep_key]
            
            if spec.singleton is not None:
                resolved[param_name] = spec.singleton
            elif spec.factory:
                if dep_key in self._cache:
                    resolved[param_name] = self._cache[dep_key]
                else:
                    instance = spec.factory()
                    self._cache[dep_key] = instance
                    resolved[param_name] = instance
        
        return resolved
    
    def clear_cache(self):
        """Clear the dependency cache"""
        self._cache.clear()
```

**Key Design Decisions:**

The resolver supports both singleton instances (shared across all agents) and factory functions (creating new instances as needed).

Caching of factory-created instances ensures that factories are called only once, even if multiple agents request the same dependency.

---

## 2. API Specifications

### 2.1 Request/Response Models

**Location:** `app/api/services/models.py`

```python
class AgentRequest(BaseModel):
    """Request to execute an agent"""
    agent_id: str = Field(..., description="Agent ID")
    payload: dict = Field(..., description="Payload for the agent")
    
    @model_validator(mode="after")
    def validate_models(self) -> "AgentRequest":
        """Validate agent exists and payload matches schema"""
        agent_ids = AgentRegistry.list_agent_ids()
        if self.agent_id not in agent_ids:
            raise ValueError(
                f"Invalid agent_id: {self.agent_id}. "
                f"Available: {agent_ids}"
            )
        
        input_models = AgentRegistry.get_all_agent_inputs()
        try:
            input_model = input_models[self.agent_id]
            input_model(**self.payload)
        except Exception as e:
            raise ValueError(f"Payload validation error: {e}")
        
        return self

class AgentResponse(BaseModel):
    """Response from agent execution"""
    run_id: str = Field(..., description="Execution ID")
    result: Dict[str, Any] = Field(..., description="Agent result")
```

### 2.2 API Endpoints

**Location:** `app/api/routes/agent.py`

```python
@router.post("/runs")
@inject
async def run_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: AgentRequest,
    service: AgentPerformService = Depends(Provide[Container.perform_service])
):
    """Execute agent asynchronously"""
    background_tasks.add_task(service.perform, request=request, payload=payload)
    return {"run_id": "some-unique-run-id"}

@router.post("/runs/wait")
@inject
async def run_agent_and_wait(
    request: Request,
    payload: AgentRequest,
    service: AgentPerformService = Depends(Provide[Container.perform_service])
):
    """Execute agent and wait for result"""
    result = await service.perform(request=request, payload=payload)
    return {"run_id": "some-unique-run-id", "result": result}

@router.get("/runs/{run_id}")
def get_agent_run_status(run_id: str):
    """Get status of an agent run"""
    return {
        "run_id": run_id,
        "status": "in_progress",
        "result": None
    }

@router.post("/runs/{run_id}/cancel")
def cancel_agent_run(run_id: str):
    """Cancel an agent run"""
    return {
        "message": f"Cancellation requested for {run_id}",
        "run_id": run_id,
        "status": "cancelling"
    }
```

**API Specifications:**

| Endpoint | Method | Request Body | Response | Status Codes |
|----------|--------|--------------|----------|--------------|
| `/agents/runs` | POST | AgentRequest | `{run_id: string}` | 200, 400, 403 |
| `/agents/runs/wait` | POST | AgentRequest | `{run_id: string, result: object}` | 200, 400, 403 |
| `/agents/runs/{run_id}` | GET | - | `{run_id, status, result}` | 200, 404 |
| `/agents/runs/{run_id}/cancel` | POST | - | `{message, status}` | 200, 404 |

---

## 3. Data Models and Schemas

### 3.1 BaseState Model

**Location:** `app/common/agent/models.py`

```python
class BaseState(BaseModel):
    """Base state for all agents"""
    status: Literal["success", "running", "error"] = Field(
        default="running",
        description="Execution status"
    )
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
```

### 3.2 Kafka Message Models

**Location:** `app/common/kafka/models.py`

```python
class KafkaMessage(BaseModel):
    """Base message for Kafka"""
    requestId: str = Field(..., description="Request ID")
    status: Literal["success", "error"] = Field(...)
    message: str = Field(...)

class RefinedDocumentMessage(KafkaMessage):
    """Message for document refinement completion"""
    document_id: Optional[str] = None
    output_path: Optional[str] = None
```

### 3.3 Example Agent Models

**Location:** `app/module/agent/demo_agent/models.py`

```python
class DemoAgentInput(BaseModel):
    """API input model"""
    message: str = Field(..., description="Input message")
    operation: str = Field(
        default="uppercase",
        description="Operation: uppercase, lowercase, reverse"
    )

class DemoAgentState(BaseState):
    """Internal state model"""
    message: str = Field(...)
    operation: str = Field(...)
    result: str = Field(default="", description="Processing result")
    processing_time: float = Field(default=0.0)

def demo_input_to_state(input_data: DemoAgentInput) -> DemoAgentState:
    """Convert input to state"""
    return DemoAgentState(
        message=input_data.message,
        operation=input_data.operation
    )
```

---

## 4. Service Layer Implementation

### 4.1 AgentPerformService

**Location:** `app/api/services/perform.py`

```python
class AgentPerformService:
    """Orchestrates agent execution"""
    
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
    
    async def perform(
        self,
        request: Request,
        payload: AgentRequest
    ) -> Dict[str, Any]:
        """Execute an agent with given payload"""
        try:
            # Get agent instance
            agent = self.agent_factory.get_agent(payload.agent_id)
            
            # Get configuration
            config = self.agent_factory.get_agent_config(payload.agent_id)
            
            # Parse input
            if isinstance(payload.payload, dict):
                input_data = config.input_model(**payload.payload)
            else:
                input_data = payload.payload
            
            # Convert to state
            state = config.input_to_state(input_data)
            
            # Execute agent
            result = await agent.run_async(state)
            
            logger.info(f"Agent {payload.agent_id} completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Error running agent {payload.agent_id}: {e}")
            raise ValueError(f"Failed to run agent: {str(e)}")
```

**Key Design Decisions:**

The service handles the complete orchestration: agent retrieval, input validation, state conversion, and execution. It abstracts away the complexity from the API layer.

Error handling is comprehensive, with detailed logging for debugging.

---

## 5. Dependency Injection Container

**Location:** `app/container.py`

```python
class Container(DeclarativeContainer):
    """Dependency injection container"""
    
    config = WiringConfiguration()
    mock_config = Configuration()
    
    # Core services
    kafka = Singleton(KafkaProducer)
    redis = Resource(
        init_redis_pool,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_AUTH
    )
    
    # Dependency resolver
    dependency_resolver = Factory(
        lambda kafka_inst, redis_inst: _create_dependency_resolver(
            kafka_inst, redis_inst
        ),
        kafka_inst=kafka,
        redis_inst=redis
    )
    
    # Agent factory
    agent_factory = Singleton(
        AgentFactory,
        dependency_resolver=dependency_resolver
    )
    
    # Services
    perform_service = Singleton(
        AgentPerformService,
        agent_factory=agent_factory
    )

def _create_dependency_resolver(kafka_instance, redis_instance):
    """Create and configure dependency resolver"""
    resolver = DependencyResolver()
    resolver.register("kafka_producer", singleton=kafka_instance)
    resolver.register("redis", singleton=redis_instance)
    return resolver
```

**Key Design Decisions:**

The container uses `Singleton` providers for services that should be created once and reused. The `Resource` provider handles proper initialization and cleanup of resources like Redis connections.

The factory function `_create_dependency_resolver` builds the resolver with all registered dependencies, making it easy to add new dependencies in one place.

---

## 6. Middleware and Request Handling

### 6.1 RequestLoggingMiddleware

**Location:** `app/middleware.py`

```python
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs all HTTP requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = generate_short_id()
        request.state.request_id = request_id
        
        # Log incoming request
        client_ip = request.client.host if request.client else "unknown"
        body = await request.body()
        
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {client_ip}"
        )
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log outgoing response
        logger.info(
            f"Outgoing response: Status {response.status_code}, "
            f"Time: {process_time:.4f}s"
        )
        
        return response
```

### 6.2 Authentication Dependency

**Location:** `app/api/deps.py`

```python
API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

def get_api_key(
    api_key_header: str = Security(api_key_header),
    api_key_query: str = Security(api_key_query)
):
    """Validate API key from header or query parameter"""
    if settings.ENVIRONMENT == "local":
        return "local-dev-key"
    
    if api_key_header == settings.SECRET_KEY:
        return api_key_header
    
    if api_key_query == settings.SECRET_KEY:
        return api_key_query
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid credentials"
    )

AuthDep = Depends(get_api_key)
```

---

## 7. Kafka Integration

### 7.1 KafkaProducer Implementation

**Location:** `app/common/kafka/producer.py`

```python
class KafkaProducer:
    """Produces messages to Kafka topics"""
    
    started = False
    
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            security_protocol=settings.KAFKA_SECURITY_PROTOCOL,
            sasl_mechanism="PLAIN" if settings.KAFKA_SECURITY_PROTOCOL == "SASL_PLAINTEXT" else None,
            sasl_plain_username=settings.KAFKA_USERNAME,
            sasl_plain_password=settings.KAFKA_PASSWORD
        )
    
    async def send_and_wait(self, topic: str, message: Any):
        """Send message and wait for confirmation"""
        await self.start()
        await self.producer.send(topic, message)
    
    async def start(self):
        """Start the producer"""
        if self.started:
            return
        logger.info("Starting Kafka producer")
        await self.producer.start()
        self.started = True
    
    async def stop(self):
        """Stop the producer"""
        logger.info("Stopping Kafka producer")
        await self.producer.stop()
    
    async def send_kafka_one(self, value: KafkaMessage, topic: str):
        """Send a single Kafka message"""
        logger.info(f"Sending message to {topic}")
        await self.send_and_wait(topic, value.model_dump_json().encode("utf-8"))

class KafkaProducerMock(KafkaProducer):
    """Mock producer for testing"""
    
    async def send_and_wait(self, topic: str, message: Any):
        logger.info(f"Mock: Sending to {topic}: {message}")
    
    async def start(self):
        pass
    
    async def stop(self):
        pass
```

---

## 8. Logging and Observability

### 8.1 Logger Configuration

**Location:** `app/common/log.py`

```python
class CustomerFormatter(logging.Formatter):
    """Custom formatter with colors"""
    
    FORMATS = {
        logging.DEBUG: "%(asctime)s - [DEBUG] - %(message)s",
        logging.INFO: "%(asctime)s - [INFO] - %(message)s",
        logging.WARNING: "%(asctime)s - [WARNING] - %(message)s",
        logging.ERROR: "%(asctime)s - [ERROR] - %(message)s",
        logging.CRITICAL: "%(asctime)s - [CRITICAL] - %(message)s"
    }

def setup_logger(name="app"):
    """Configure logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOGGING_LEVEL)
    logger.propagate = False
    
    # File handler with rotation
    os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        settings.LOG_FILE_PATH,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(settings.LOGGING_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOGGING_LEVEL)
    
    # Set formatters
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    console_handler.setFormatter(CustomerFormatter())
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

---

## 9. Configuration Management

**Location:** `app/common/config.py`

```python
class Settings(BaseSettings):
    """Application settings from environment"""
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    )
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agent Core"
    
    # Logging
    LOGGING_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "temp/logs"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    OPENAI_API_KEY: str = ""
    
    # Langfuse
    LANGFUSE_HOST: str | None = None
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_AUTH: str = ""
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = ""
    KAFKA_TOPIC: str = ""
    KAFKA_SECURITY_PROTOCOL: str = "PLAIN"
    KAFKA_USERNAME: Optional[str] = None
    KAFKA_PASSWORD: Optional[str] = None
    
    # Environment
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DEBUG: bool = False
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

settings = Settings()
```

---

## 10. Testing Framework

### 10.1 Unit Test Example

```python
# tests/unit/test_agent_registry.py

import pytest
from app.common.agent.registry import AgentRegistry, AgentConfig
from app.common.agent.base import BaseAgent
from app.common.agent.models import BaseState
from pydantic import BaseModel

class TestAgentInput(BaseModel):
    test_field: str

class TestAgentState(BaseState):
    test_field: str

def test_agent_registration():
    """Test agent registration"""
    AgentRegistry.clear_registry()
    
    config = AgentConfig(
        name="Test Agent",
        description="Test",
        input_model=TestAgentInput,
        state_model=TestAgentState,
        input_to_state=lambda x: TestAgentState(test_field=x.test_field)
    )
    
    @AgentRegistry.register("test_agent", config)
    class TestAgent(BaseAgent):
        pass
    
    assert AgentRegistry.is_registered("test_agent")
    assert AgentRegistry.get_agent_class("test_agent") == TestAgent
```

---

## 11. Database and Persistence

### 11.1 Redis Integration

**Location:** `app/common/redis/redis.py`

```python
async def init_redis_pool(**kwargs):
    """Initialize Redis connection pool"""
    logger.info("Initializing Redis")
    redis = Redis(**kwargs)
    yield redis
    logger.info("Closing Redis")
    await redis.close()
```

---

## 12. Error Handling

### 12.1 Exception Hierarchy

```python
# app/common/exceptions/base.py

class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class AgentNotFoundError(AppException):
    """Agent not found in registry"""
    def __init__(self, agent_id: str):
        super().__init__(
            f"Agent '{agent_id}' not found",
            code="AGENT_NOT_FOUND"
        )

class AgentExecutionError(AppException):
    """Error during agent execution"""
    def __init__(self, agent_id: str, error: str):
        super().__init__(
            f"Agent '{agent_id}' execution failed: {error}",
            code="AGENT_EXECUTION_ERROR"
        )
```

---

## 13. Conclusion

This Low-Level Design document provides the detailed specifications needed for implementation. It covers class hierarchies, method signatures, API contracts, data models, and integration patterns. Combined with the High-Level Design document, it provides a complete blueprint for the Robot Workflow Orchestration System.

---

## References

1. Python Type Hints: https://docs.python.org/3/library/typing.html
2. Pydantic Documentation: https://docs.pydantic.dev/
3. FastAPI Advanced Features: https://fastapi.tiangolo.com/advanced/
4. dependency-injector: https://dependency-injector.ets-labs.org/
5. aiokafka: https://aiokafka.readthedocs.io/
6. redis-py: https://redis-py.readthedocs.io/
7. LangGraph: https://langchain-ai.github.io/langgraph/

---

**Document End**


---

## Phụ lục A: Triển khai Agent Phức tạp - `ExtractDocumentAgent`

Để cung cấp một ví dụ thực tế và phức tạp hơn, chúng ta sẽ phân tích chi tiết `ExtractDocumentAgent`. Agent này có nhiệm vụ nhận một file tài liệu (PDF, DOCX), trích xuất nội dung text, hình ảnh, bảng biểu và sau đó dùng LLM để tóm tắt.

### A.1. Sơ đồ Logic của Agent

```mermaid
graph TD
    A[START] --> B{Kiểm tra loại file};
    B -- PDF --> C[Trích xuất text & hình ảnh từ PDF];
    B -- DOCX --> D[Trích xuất text & hình ảnh từ DOCX];
    C --> E{Nội dung có bảng không?};
    D --> E;
    E -- Có --> F[Xử lý Bảng -> HTML];
    E -- Không --> G[Tổng hợp Text];
    F --> G;
    G --> H[Gọi LLM để tóm tắt];
    H --> I[Xử lý hình ảnh (nếu có)];
    I --> J[Tạo kết quả cuối cùng];
    J --> K[FINISH];
```

### A.2. Phân tích các Node chính

1.  **`_extract_content` (Node B, C, D):**
    -   Sử dụng các thư viện như `PyMuPDF` cho PDF và `python-docx` cho DOCX.
    -   Logic sẽ đọc file, lặp qua các trang/đoạn văn, và trích xuất các khối text và hình ảnh.
    -   Hình ảnh được lưu tạm thời vào một thư mục và đường dẫn được lưu vào state.
    -   Text được ghép lại thành một chuỗi lớn.

2.  **`_process_tables` (Node E, F):**
    -   Sử dụng các kỹ thuật nhận dạng bảng (có thể là heuristic hoặc một model AI nhỏ) để tìm các bảng trong text.
    -   Chuyển đổi các bảng này sang định dạng Markdown hoặc HTML để LLM có thể hiểu được cấu trúc.

3.  **`_summarize_text` (Node H):**
    -   Đây là node gọi đến LLM.
    -   Nó sẽ lấy toàn bộ text đã được xử lý từ state.
    -   Sử dụng một `prompt template` được định nghĩa sẵn để yêu cầu LLM tóm tắt nội dung.
    -   **Xử lý lỗi:** Node này cần có cơ chế `retry` nếu LLM bị lỗi hoặc timeout.

    ```python
    # Đoạn code minh họa trong agent.py
    from app.common.llm import get_llm

    async def _summarize_text(self, state: ExtractDocumentState):
        llm = get_llm() # Lấy instance LLM đã được cấu hình
        prompt = f"""Vui lòng tóm tắt nội dung sau:

        {state.extracted_text}

        Tóm tắt:"""

        # Gọi LLM với retry
        summary = await llm.ainvoke(prompt, config={"retries": 3})

        return {"summary": summary.content}
    ```

4.  **`_process_images` (Node I):**
    -   Nếu người dùng yêu cầu, node này có thể sử dụng một model Vision (như GPT-4 Vision) để tạo mô tả cho các hình ảnh đã được trích xuất.
    -   Các mô tả này sau đó được thêm vào kết quả cuối cùng.

### A.3. Thiết kế State (`ExtractDocumentState`)

State của agent này sẽ rất phức tạp, chứa nhiều thông tin:

```python
# app/module/agents/extract_document_agent/models.py

class ExtractDocumentState(BaseState):
    file_path: str  # Đường dẫn đến file đầu vào
    file_type: str  # Loại file (pdf, docx)

    # Dữ liệu được trích xuất
    raw_text: str
    images: List[str] = [] # Danh sách đường dẫn đến các file ảnh
    tables: List[str] = [] # Danh sách các bảng (dạng HTML/Markdown)

    # Dữ liệu đã xử lý
    processed_text: str
    summary: str
    image_descriptions: Dict[str, str] = {}

    # Trạng thái lỗi
    error_message: Optional[str] = None
```

Việc thiết kế một State chi tiết như thế này giúp cho việc debug trở nên cực kỳ dễ dàng, vì tại bất kỳ bước nào, chúng ta cũng có thể xem toàn bộ dữ liệu đang được xử lý.

---

## Phụ lục B: Tích hợp Nâng cao

### B.1. Tích hợp Langfuse để Tracing

Langfuse là công cụ cực kỳ mạnh mẽ để theo dõi các ứng dụng LLM. Để tích hợp, chúng ta cần:

1.  **Cấu hình Biến Môi trường:**
    Trong file `.env`, thêm các biến sau:

    ```
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_HOST="https://cloud.langfuse.com"
    ```

2.  **Tích hợp vào `BaseAgent`:**
    Hệ thống đã được thiết kế để có thể dễ dàng thêm các `callback` vào quá trình chạy graph. Chúng ta có thể sửa đổi `BaseAgent.run_async` để tự động thêm `LangfuseCallbackHandler`.

    ```python
    # app/common/agent/base.py
    from langfuse.callback import CallbackHandler as LangfuseCallbackHandler

    class BaseAgent(Generic[T]):
        async def run_async(self, input_state: T, ...):
            # ...
            # Tạo Langfuse handler
            langfuse_callback = LangfuseCallbackHandler(
                session_id=input_state.session_id, # Giả sử state có session_id
                user_id=input_state.user_id      # Giả sử state có user_id
            )

            # Thêm callback vào config của graph
            config = {
                "recursion_limit": self.recursion_limit,
                "callbacks": [langfuse_callback]
            }

            async for event in self.graph.astream_events(input_state, config=config, ...):
                # ...
    ```

    Với thay đổi nhỏ này, tất cả các agent kế thừa từ `BaseAgent` sẽ tự động gửi trace về Langfuse, bao gồm:
    -   Toàn bộ input/output của graph.
    -   Từng bước chạy của các node.
    -   Các lần gọi LLM, bao gồm cả prompt, response, thời gian, và chi phí.

### B.2. Cơ chế Timeout Toàn cục

Để đảm bảo một request không bị treo vô thời hạn, chúng ta có thể áp dụng timeout ở nhiều cấp độ.

1.  **Timeout ở Gunicorn/Uvicorn:** Cấu hình worker timeout. Nếu một request xử lý quá lâu (ví dụ 30 giây), worker sẽ bị kill và khởi động lại. Đây là lớp bảo vệ cuối cùng.

2.  **Timeout trong `asyncio`:** Chúng ta có thể bọc lời gọi `agent.run_async` trong `asyncio.wait_for`.

    ```python
    # app/api/services/perform.py
    import asyncio

    class AgentPerformService:
        async def perform(...):
            try:
                # ... (tạo agent và state)

                # Bọc lời gọi trong timeout 8 giây
                result = await asyncio.wait_for(
                    agent.run_async(input_state),
                    timeout=8.0
                )

                return result
            except asyncio.TimeoutError:
                logger.error(f"Agent {payload.agent_id} timed out after 8 seconds.")
                return {"status": "error", "error": "Request timed out"}
            except Exception as e:
                # ... (xử lý lỗi khác)
    ```

    Cách này cho phép chúng ta bắt được lỗi timeout một cách tường minh và trả về một thông báo lỗi thân thiện cho người dùng, thay vì chỉ bị rớt kết nối.

### B.3. Mở rộng Dependency Resolver

`DependencyResolver` có thể được mở rộng để hỗ trợ các dependency được khởi tạo "lười biếng" (lazy initialization) hoặc có scope theo request.

**Ví dụ: Thêm một dependency chỉ tồn tại trong một request.**

Chúng ta có thể tạo một `RequestScopedDependencyResolver` kế thừa từ `DependencyResolver` và truyền nó vào context của request thông qua một middleware.

1.  **Tạo Middleware:**

    ```python
    # app/middleware.py
    from starlette.middleware.base import BaseHTTPMiddleware

    class DependencyMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # Tạo một resolver mới cho mỗi request
            request.state.dependency_resolver = DependencyResolver()
            # Đăng ký các dependency chỉ dùng cho request này, ví dụ thông tin user
            request.state.dependency_resolver.register("current_user", request.user)
            
            response = await call_next(request)
            return response
    ```

2.  **Sử dụng trong Service:**

    ```python
    # app/api/services/perform.py

    class AgentPerformService:
        async def perform(self, request: Request, ...):
            # Lấy resolver của request
            request_resolver = request.state.dependency_resolver
            # ...
    ```

Cách tiếp cận này rất mạnh mẽ để quản lý các dependency có vòng đời phức tạp.

---

## Kết luận

Tài liệu Low-Level Design này đã cung cấp một cái nhìn chi tiết và sâu sắc vào từng ngóc ngách của hệ thống **Robot Lesson Workflow**. Từ cấu trúc của một API endpoint, luồng thực thi của một service, cho đến cách một agent được xây dựng và đăng ký, mọi thứ đều được giải thích một cách tường minh với các đoạn code mẫu cụ thể.

Phần hướng dẫn từng bước để tạo một agent mới là kim chỉ nam cho các lập trình viên mới, giúp họ có thể nhanh chóng tham gia và đóng góp cho dự án mà không cảm thấy bị choáng ngợp. Các quy ước và thực hành tốt nhất về coding, logging, và testing đảm bảo rằng chất lượng code của dự án sẽ được duy trì ở mức cao khi đội ngũ phát triển lớn mạnh.

Bằng cách tuân thủ các thiết kế và quy ước trong tài liệu này, dự án không chỉ dễ dàng để bảo trì và mở rộng, mà còn là một môi trường làm việc hiệu quả và thú vị cho các lập trình viên.

