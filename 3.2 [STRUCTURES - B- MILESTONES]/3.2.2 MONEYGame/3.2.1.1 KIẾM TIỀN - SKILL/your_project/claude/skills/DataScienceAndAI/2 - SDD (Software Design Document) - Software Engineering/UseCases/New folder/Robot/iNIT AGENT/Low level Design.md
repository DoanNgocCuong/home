# Thiết kế Hệ thống Cấp thấp (Low-Level Design) - Robot AI Workflow

**Tác giả:** Manus AI
**Ngày tạo:** 12/12/2025
**Phiên bản:** 1.0

## 1. Giới thiệu

Tài liệu này cung cấp chi tiết kỹ thuật về các thành phần, module, class, và function trong hệ thống Robot AI Workflow. Nó là bổ sung chi tiết cho thiết kế cấp cao, giúp các developer hiểu rõ cách các thành phần tương tác với nhau ở mức độ code.

## 2. Cấu trúc Thư mục và Tổ chức Code

### 2.1. Cấu trúc Tổng thể

```
robot-ai-workflow/
├── app/                              # Ứng dụng chính (FastAPI)
│   ├── api/                          # API routes và services
│   │   ├── routes/
│   │   │   ├── agent.py             # Agent execution endpoints
│   │   │   ├── workflow.py          # Workflow management endpoints
│   │   │   ├── custom_logic.py      # Custom logic endpoints
│   │   │   └── robot_v2_routes.py   # Robot v2 specific routes
│   │   ├── services/
│   │   │   ├── perform.py           # Agent execution service
│   │   │   ├── models.py            # Pydantic request/response models
│   │   │   ├── robot_v2_services.py # Robot v2 services
│   │   │   └── database_service.py  # Database operations
│   │   ├── deps.py                  # Dependency injection setup
│   │   └── main.py                  # API router configuration
│   ├── common/                       # Shared utilities
│   │   ├── agent/
│   │   │   ├── base.py              # BaseAgent with LangGraph
│   │   │   ├── factory.py           # Agent factory pattern
│   │   │   ├── registry.py          # Agent registry
│   │   │   ├── decorators.py        # Agent decorators
│   │   │   ├── models.py            # BaseState and agent models
│   │   │   └── __init__.py
│   │   ├── kafka/                   # Kafka integration
│   │   ├── redis/                   # Redis utilities
│   │   ├── database/                # Database utilities
│   │   ├── config.py                # Configuration management
│   │   ├── log.py                   # Logging setup
│   │   └── async_utils.py           # Async utilities
│   ├── module/                       # Business logic modules
│   │   ├── agents/                  # Agent implementations
│   │   │   ├── base_tool_loop_agent/
│   │   │   ├── demo_agent/
│   │   │   └── extract_document_agent/
│   │   ├── tools/                   # Tool implementations
│   │   ├── workflows/               # Workflow definitions
│   │   ├── utils/                   # Module utilities
│   │   └── run/                     # Execution runners
│   ├── server.py                    # FastAPI app entry point
│   ├── container.py                 # Dependency injection container
│   └── middleware.py                # Request/response middleware
│
├── src/                              # Legacy source code (Robot v1)
│   ├── channel/                     # Infrastructure connectors
│   │   ├── mysql_bot.py            # MySQL bot configuration
│   │   ├── mysql_connector.py      # MySQL connection manager
│   │   ├── redis_client.py         # Redis client wrapper
│   │   ├── rabbitmq_client.py      # RabbitMQ producer
│   │   └── rabbitmq_consumer.py    # RabbitMQ consumer
│   ├── chatbot/                    # Chatbot core logic
│   │   ├── llm_base.py            # LLM provider interface
│   │   ├── pipeline_task.py       # Pipeline task processor
│   │   ├── policies.py            # Workflow policies
│   │   ├── prompt.py              # Prompt management
│   │   ├── regex_classifier.py    # Intent classification
│   │   └── scenario.py            # Scenario management
│   ├── tools/                      # Tool implementations
│   │   ├── tool_config.py         # Tool registry
│   │   ├── tool_interface.py      # Tool base interface
│   │   └── tool_pronunciation_checker.py
│   └── utils/                      # Utility functions
│       └── utils.py               # Common utilities
│
├── config.yml                       # Configuration file
├── requirement.txt                  # Python dependencies
├── Dockerfile                       # Main app container
├── Dockerfile.worker               # Worker container
├── docker-compose.yml              # Service orchestration
├── app.py                          # Legacy entry point
└── worker_tools.py                 # Worker process entry point
```

### 2.2. Nguyên tắc Tổ chức

**Separation of Concerns:** Mỗi module chịu trách nhiệm cho một khía cạnh cụ thể của hệ thống. API routes không chứa logic nghiệp vụ, mà thay vào đó gọi các services. Services gọi các module business logic.

**Layered Architecture:** Hệ thống tuân theo kiến trúc phân lớp với ba lớp chính: Presentation (API routes), Business Logic (services, agents, workflows), và Data Access (channel modules).

**Dependency Injection:** Sử dụng `dependency-injector` library để quản lý các phụ thuộc, giúp code dễ kiểm thử và tái sử dụng.

## 3. Chi tiết Các Module Chính

### 3.1. Module `app/api` - API Layer

#### 3.1.1. Routes - Định nghĩa Endpoints

**File: `app/api/routes/agent.py`**

Định nghĩa các endpoint liên quan đến agent execution:

```python
@router.post("/agents/runs")
@inject
async def run_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    payload: AgentRequest,
    service: AgentPerformService = Depends(Provide[Container.perform_service]),
):
    """
    Khởi chạy agent ở chế độ nền (non-blocking).
    
    Tham số:
    - payload: Yêu cầu chứa input_state và agent configuration
    
    Trả về:
    - run_id: Mã định danh duy nhất cho lượt chạy này
    """
    background_tasks.add_task(service.perform, request=request, payload=payload)
    return {"run_id": "some-unique-run-id"}
```

**Các endpoint chính:**

| Endpoint | Phương thức | Mục đích | Tham số | Trả về |
| :--- | :--- | :--- | :--- | :--- |
| `/agents/runs` | POST | Chạy agent ở chế độ nền | `AgentRequest` | `{"run_id": str}` |
| `/agents/runs/wait` | POST | Chạy agent và chờ kết quả | `AgentRequest` | `{"run_id": str, "result": dict}` |
| `/agents/runs/{run_id}` | GET | Lấy trạng thái của một lượt chạy | `run_id` | `{"status": str, "result": dict}` |
| `/agents/runs/{run_id}/cancel` | POST | Hủy một lượt chạy | `run_id` | `{"status": str}` |

#### 3.1.2. Services - Logic Nghiệp vụ

**File: `app/api/services/perform.py`**

Chứa `AgentPerformService` - dịch vụ thực thi agent:

```python
class AgentPerformService:
    def __init__(self, agent_registry: AgentRegistry, ...):
        self.agent_registry = agent_registry
        # Các phụ thuộc khác
    
    async def perform(
        self, 
        request: Request, 
        payload: AgentRequest
    ) -> Dict[str, Any]:
        """
        Thực thi agent dựa trên payload.
        
        Quy trình:
        1. Lấy agent từ registry dựa trên agent_name
        2. Chuyển đổi payload thành input_state
        3. Gọi agent.run_async()
        4. Xử lý kết quả và lỗi
        5. Trả về kết quả chuẩn hóa
        """
        agent = self.agent_registry.get(payload.agent_name)
        input_state = payload.to_state()
        result = await agent.run_async(input_state)
        return result
```

**File: `app/api/services/models.py`**

Định nghĩa Pydantic models cho request/response:

```python
class AgentRequest(BaseModel):
    """Request model cho agent execution"""
    agent_name: str              # Tên agent cần chạy
    user_input: str              # Input từ người dùng
    context: Optional[Dict] = None  # Ngữ cảnh bổ sung
    metadata: Optional[Dict] = None # Metadata
    
    def to_state(self) -> BaseState:
        """Chuyển đổi request thành BaseState"""
        return BaseState(
            user_input=self.user_input,
            context=self.context or {},
            metadata=self.metadata or {}
        )
```

### 3.2. Module `app/common/agent` - Agent Framework

#### 3.2.1. BaseAgent - Lớp Cơ sở

**File: `app/common/agent/base.py`**

Định nghĩa `BaseAgent` - lớp cơ sở cho tất cả các agent:

```python
class BaseAgent(Generic[T]):
    """
    Lớp cơ sở cho tất cả agents, tích hợp với LangGraph.
    
    Thuộc tính:
    - graph: CompiledStateGraph - LangGraph workflow
    - name: str - Tên agent
    - recursion_limit: int - Giới hạn độ sâu đệ quy
    - trace_enabled: bool - Bật/tắt tracing
    """
    
    graph: CompiledStateGraph
    name: str
    recursion_limit: int = 600
    trace_enabled = True
    
    def __init__(self, **kwargs):
        """Khởi tạo agent với dependency injection"""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    async def run_async(
        self,
        input_state: T,
        on_error_callback: Optional[Callable] = None,
        callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Thực thi graph bất đồng bộ.
        
        Quy trình:
        1. Ghi log input state
        2. Stream các sự kiện từ graph
        3. Xử lý các sự kiện (output, metadata, error)
        4. Trả về kết quả chuẩn hóa
        
        Trả về:
        {
            "status": "success" | "error",
            "output": Any,
            "error": Optional[str],
            "metadata": Optional[Dict]
        }
        """
        try:
            logger.info(f"Agent {self.__class__.__name__} starting")
            output = None
            metadata = None
            
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
                        elif event.get("name") == "metadata":
                            metadata = event.get("data")
            
            return {
                "status": "success",
                "output": output,
                "error": None,
                "metadata": metadata
            }
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {
                "status": "error",
                "output": None,
                "error": str(e),
                "metadata": None
            }
    
    async def set_output(self, data):
        """Gửi sự kiện output"""
        return await adispatch_custom_event("output", data)
    
    async def set_metadata(self, data):
        """Gửi sự kiện metadata"""
        return await adispatch_custom_event("metadata", data)
```

#### 3.2.2. BaseState - Định nghĩa Trạng thái

**File: `app/common/agent/models.py`**

```python
class BaseState(BaseModel):
    """
    Trạng thái cơ sở cho tất cả agents.
    
    Các trường:
    - user_input: Đầu vào từ người dùng
    - context: Ngữ cảnh của cuộc hội thoại
    - metadata: Metadata bổ sung
    - output: Kết quả đầu ra
    - error: Thông báo lỗi (nếu có)
    """
    user_input: str
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    output: Optional[str] = None
    error: Optional[str] = None
```

#### 3.2.3. AgentRegistry - Quản lý Agents

**File: `app/common/agent/registry.py`**

```python
class AgentRegistry:
    """
    Registry để quản lý và tìm kiếm các agent instances.
    
    Chức năng:
    - Đăng ký agent mới
    - Tìm kiếm agent theo tên
    - Liệt kê tất cả agents
    """
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
    
    def register(self, name: str, agent: BaseAgent):
        """Đăng ký một agent mới"""
        self._agents[name] = agent
    
    def get(self, name: str) -> BaseAgent:
        """Lấy agent theo tên"""
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' not found")
        return self._agents[name]
    
    def list_agents(self) -> List[str]:
        """Liệt kê tất cả tên agents"""
        return list(self._agents.keys())
```

#### 3.2.4. AgentFactory - Tạo Agents

**File: `app/common/agent/factory.py`**

```python
class AgentFactory:
    """
    Factory pattern để tạo agent instances.
    
    Chức năng:
    - Tạo agent từ cấu hình
    - Inject phụ thuộc
    - Xây dựng LangGraph
    """
    
    @staticmethod
    def create_agent(
        agent_class: Type[BaseAgent],
        config: Dict[str, Any],
        **dependencies
    ) -> BaseAgent:
        """
        Tạo một agent instance.
        
        Tham số:
        - agent_class: Lớp agent cần tạo
        - config: Cấu hình agent
        - **dependencies: Các phụ thuộc cần inject
        
        Trả về:
        - Agent instance đã được khởi tạo
        """
        return agent_class(
            name=config.get("name"),
            **dependencies
        )
```

### 3.3. Module `src/channel` - Infrastructure Layer

#### 3.3.1. MySQL Bot - Quản lý Cấu hình Bot

**File: `src/channel/mysql_bot.py`**

```python
class LLMBot:
    """
    Quản lý các thao tác CRUD cho bot configuration trong MySQL.
    
    Thuộc tính:
    - connection: MySQL connection object
    """
    
    def __init__(self, host: str, port: int, username: str, 
                 password: str, database: str):
        self.connection = self._create_connection(
            host, port, username, password, database
        )
    
    def insert_bot(
        self,
        name: str,
        description: str,
        scenario: List[dict],
        generation_params: dict,
        provider_name: str,
        system_prompt: str = None,
        **kwargs
    ) -> int:
        """
        Thêm bot mới vào database.
        
        Trả về:
        - ID của bot vừa được tạo
        """
        query = """
        INSERT INTO llm_bot 
        (name, description, scenario, generation_params, provider_name, 
         system_prompt, create_at, update_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (
            name, description, json.dumps(scenario),
            json.dumps(generation_params), provider_name,
            system_prompt, int(time.time()), int(time.time())
        ))
        self.connection.commit()
        return cursor.lastrowid
    
    def get_bot_from_id(self, id: int) -> Dict:
        """Lấy thông tin bot theo ID"""
        query = "SELECT * FROM llm_bot WHERE id = %s"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (id,))
        return cursor.fetchone()
    
    def get_all_bot_config(self) -> List[Dict]:
        """Lấy tất cả cấu hình bot"""
        query = "SELECT * FROM llm_bot"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    
    def insert_llm_history(
        self,
        conversation_id: str,
        input_text: str,
        output_text: str,
        process_time: float,
        bot_id: int
    ):
        """Lưu lịch sử hội thoại"""
        query = """
        INSERT INTO llm_history 
        (conversation_id, input, output, process_time, create_at, bot_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (
            conversation_id, input_text, output_text,
            process_time, int(time.time()), bot_id
        ))
        self.connection.commit()
```

#### 3.3.2. Redis Client - Cache và Session

**File: `src/channel/redis_client.py`**

```python
class RedisClient:
    """
    Wrapper cho Redis client, cung cấp các thao tác cơ bản.
    
    Thuộc tính:
    - client: Redis connection object
    """
    
    def __init__(self, host: str, port: int, password: str):
        self.client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )
    
    def set(
        self,
        key: str,
        value: Any,
        expire_time: int = 1800,
        pre_fix: str = None
    ):
        """
        Lưu dữ liệu vào Redis.
        
        Tham số:
        - key: Khóa lưu trữ
        - value: Giá trị (sẽ được JSON serialize nếu là dict)
        - expire_time: Thời gian hết hạn (giây, mặc định 30 phút)
        - pre_fix: Tiền tố cho key
        """
        full_key = f"{pre_fix}:{key}" if pre_fix else key
        if isinstance(value, dict):
            value = json.dumps(value)
        self.client.setex(full_key, expire_time, value)
    
    def get(self, key: str, pre_fix: str = None) -> Any:
        """
        Lấy dữ liệu từ Redis.
        
        Trả về:
        - Giá trị hoặc None nếu không tồn tại
        """
        full_key = f"{pre_fix}:{key}" if pre_fix else key
        value = self.client.get(full_key)
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    def delete(self, key: str, pre_fix: str = None):
        """Xóa dữ liệu khỏi Redis"""
        full_key = f"{pre_fix}:{key}" if pre_fix else key
        self.client.delete(full_key)
```

#### 3.3.3. RabbitMQ Client - Message Queue

**File: `src/channel/rabbitmq_client.py`**

```python
class RabbitMQClient:
    """
    Gửi message qua RabbitMQ để xử lý bất đồng bộ.
    
    Thuộc tính:
    - host, port, username, password: Cấu hình kết nối
    - exchange, queue_name: Tên exchange và queue
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        exchange: str,
        queue_name: str,
        **kwargs
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange = exchange
        self.queue_name = queue_name
    
    def send_task(self, message: str):
        """
        Gửi task message đến queue.
        
        Tham số:
        - message: JSON string chứa task data
        
        Quy trình:
        1. Tạo kết nối đến RabbitMQ
        2. Declare exchange và queue
        3. Bind queue với exchange
        4. Gửi message với delivery mode persistent
        5. Đóng kết nối
        """
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
        )
        channel = connection.channel()
        
        channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct',
            durable=True
        )
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue_name
        )
        
        channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        
        connection.close()
```

### 3.4. Module `src/chatbot` - Chatbot Core Logic

#### 3.4.1. LLM Base - Giao tiếp với LLM

**File: `src/chatbot/llm_base.py`**

```python
class BaseLLM:
    """
    Interface thống nhất để tương tác với các nhà cung cấp LLM khác nhau.
    
    Hỗ trợ: OpenAI, Groq, Gemini
    """
    
    def __init__(self, provider_setting: dict, provider_name: str = None):
        self.provider_setting = provider_setting
        self.provider_name = provider_name
        self._init_client()
    
    def _init_client(self):
        """Khởi tạo client cho provider tương ứng"""
        if self.provider_name == "openai":
            self.client = OpenAI(
                api_key=self.provider_setting.get("api_key"),
                base_url=self.provider_setting.get("base_url")
            )
        elif self.provider_name == "groq":
            self.client = Groq(
                api_key=self.provider_setting.get("api_key")
            )
        elif self.provider_name == "gemini":
            genai.configure(api_key=self.provider_setting.get("api_key"))
            self.client = genai
    
    async def get_response(
        self,
        messages: List[dict],
        conversation_id: str = None,
        **params
    ) -> str:
        """
        Gửi request đến LLM và nhận response.
        
        Tham số:
        - messages: Danh sách tin nhắn theo format OpenAI
        - conversation_id: ID cuộc hội thoại (để logging)
        - **params: Các tham số khác (model, temperature, max_tokens)
        
        Trả về:
        - Nội dung response từ LLM
        
        Đặc điểm:
        - Hỗ trợ timeout (5 giây)
        - Retry mechanism (tối đa 3 lần)
        - Xử lý riêng cho từng provider
        """
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                if self.provider_name == "openai":
                    response = await asyncio.wait_for(
                        self._openai_request(messages, **params),
                        timeout=5.0
                    )
                elif self.provider_name == "groq":
                    response = await asyncio.wait_for(
                        self._groq_request(messages, **params),
                        timeout=5.0
                    )
                elif self.provider_name == "gemini":
                    response = await asyncio.wait_for(
                        self._gemini_request(messages, **params),
                        timeout=5.0
                    )
                
                return response
            except asyncio.TimeoutError:
                retry_count += 1
                if retry_count >= max_retries:
                    raise
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"LLM error: {str(e)}")
                raise
    
    def parsing_json(self, data: str) -> dict:
        """
        Parse JSON từ response LLM.
        
        Xử lý:
        - Loại bỏ markdown code blocks (```json)
        - Parse JSON an toàn
        - Fallback về string gốc nếu lỗi
        """
        try:
            # Loại bỏ markdown code blocks
            if data.startswith("```"):
                data = data.split("```")[1]
                if data.startswith("json"):
                    data = data[4:]
            
            return json.loads(data.strip())
        except:
            return {"raw": data}
```

#### 3.4.2. Scenario Management - Quản lý Kịch bản

**File: `src/chatbot/scenario.py`**

```python
class ScenarioExcel:
    """
    Quản lý các kịch bản hội thoại được định nghĩa trong Excel.
    
    Chức năng:
    - Load kịch bản từ Excel
    - Truy vấn bước tiếp theo dựa trên intent và trạng thái
    - Validate kịch bản
    """
    
    def __init__(self):
        self.scenarios = {}
    
    def load_scenario(self, scenario_data: List[dict]):
        """
        Load kịch bản từ dữ liệu Excel.
        
        Format dữ liệu:
        [
            {
                "id": 1,
                "intent": "greeting",
                "current_state": "START",
                "next_state": "INTRO",
                "action": "send_message",
                "message": "Hello!"
            },
            ...
        ]
        """
        for item in scenario_data:
            key = f"{item['intent']}_{item['current_state']}"
            self.scenarios[key] = item
    
    def get_next_action(
        self,
        intent: str,
        current_state: str
    ) -> Optional[dict]:
        """
        Lấy hành động tiếp theo dựa trên intent và trạng thái.
        
        Trả về:
        - Dictionary chứa next_state, action, và các tham số khác
        """
        key = f"{intent}_{current_state}"
        return self.scenarios.get(key)
```

#### 3.4.3. Policies Workflow - Luồng Xử lý Chính

**File: `src/chatbot/policies.py`**

```python
class PoliciesWorkflow:
    """
    Định nghĩa các chính sách và luồng xử lý chính của hệ thống.
    
    Chức năng:
    - Phân loại ý định
    - Xác định hành động tiếp theo
    - Quản lý trạng thái cuộc hội thoại
    """
    
    async def process_message(
        self,
        message: str,
        conversation_state: dict,
        llm_base: BaseLLM,
        scenario: ScenarioExcel,
        **kwargs
    ) -> dict:
        """
        Xử lý một tin nhắn từ người dùng.
        
        Quy trình:
        1. Phân loại ý định từ tin nhắn
        2. Lấy hành động tiếp theo từ kịch bản
        3. Thực thi hành động
        4. Cập nhật trạng thái
        5. Trả về phản hồi
        
        Trả về:
        {
            "response": str,
            "next_state": str,
            "actions": List[dict]
        }
        """
        # 1. Phân loại ý định
        intent = await self._classify_intent(
            message, llm_base, **kwargs
        )
        
        # 2. Lấy hành động tiếp theo
        current_state = conversation_state.get("state", "START")
        action_config = scenario.get_next_action(intent, current_state)
        
        if not action_config:
            return {
                "response": "Xin lỗi, tôi không hiểu.",
                "next_state": current_state,
                "actions": []
            }
        
        # 3. Thực thi hành động
        response = await self._execute_action(
            action_config, message, llm_base, **kwargs
        )
        
        # 4. Cập nhật trạng thái
        next_state = action_config.get("next_state", current_state)
        
        return {
            "response": response,
            "next_state": next_state,
            "actions": action_config.get("actions", [])
        }
    
    async def _classify_intent(
        self,
        message: str,
        llm_base: BaseLLM,
        **kwargs
    ) -> str:
        """Phân loại ý định từ tin nhắn"""
        # Có thể sử dụng regex hoặc LLM
        # ...
        pass
    
    async def _execute_action(
        self,
        action_config: dict,
        message: str,
        llm_base: BaseLLM,
        **kwargs
    ) -> str:
        """Thực thi hành động"""
        action_type = action_config.get("action")
        
        if action_type == "send_message":
            return action_config.get("message")
        elif action_type == "generate_response":
            return await self._generate_response(
                message, llm_base, **kwargs
            )
        # ...
```

### 3.5. Module `src/tools` - Tool Integration

#### 3.5.1. Tool Config - Registry

**File: `src/tools/tool_config.py`**

```python
class ToolsPronunciationChecker:
    """Tool để kiểm tra phát âm"""
    
    async def process(
        self,
        input: dict,
        tool: dict,
        timeout: int = 5
    ) -> dict:
        """
        Kiểm tra phát âm của một từ hoặc câu.
        
        Tham số:
        - input: Chứa audio_url hoặc text
        - tool: Cấu hình tool
        - timeout: Thời gian chờ (giây)
        
        Trả về:
        {
            "score": float,  # Điểm phát âm (0-100)
            "feedback": str, # Nhận xét chi tiết
            "status": str    # "success" hoặc "error"
        }
        """
        # Logic kiểm tra phát âm
        pass

# Registry tất cả tools
TOOL_OBJECTS = {
    "tool_pronunciation_checker": ToolsPronunciationChecker()
}
```

## 4. Luồng Xử lý Chi tiết

### 4.1. Luồng Khởi tạo Hội thoại

```
POST /agents/runs/wait
    ↓
AgentPerformService.perform()
    ↓
AgentRegistry.get(agent_name)
    ↓
AgentRequest.to_state() → BaseState
    ↓
BaseAgent.run_async(input_state)
    ↓
graph.astream_events()
    ↓
[Xử lý các node trong graph]
    ↓
Collect output từ custom events
    ↓
Return {"status": "success", "output": ..., "metadata": ...}
    ↓
HTTP Response 200
```

### 4.2. Luồng Xử lý Tin nhắn (Legacy Robot v1)

```
POST /webhook
    ↓
FastAPI app.py
    ↓
Load conversation_state từ Redis
    ↓
PoliciesWorkflow.process_message()
    ├─ Phân loại ý định (RegexClassifier hoặc LLM)
    ├─ Lấy hành động từ ScenarioExcel
    └─ Thực thi hành động
        ├─ Synchronous: Gọi LLM trực tiếp
        └─ Asynchronous: Gửi task vào RabbitMQ
    ↓
Update conversation_state trong Redis
    ↓
Return response
```

### 4.3. Luồng Xử lý Tác vụ Bất đồng bộ

```
RabbitMQ Consumer (worker_tools.py)
    ↓
Lắng nghe queue
    ↓
Nhận task từ RabbitMQ
    ↓
Phân loại task type
    ├─ PRONUNCIATION_CHECK → ToolsPronunciationChecker
    ├─ EXTRACT_PROFILE → API call
    └─ ...
    ↓
Thực thi task
    ↓
Lưu kết quả vào Redis
    ↓
Gửi callback (nếu có)
```

## 5. Database Schema

### 5.1. MySQL Tables

#### llm_bot Table

```sql
CREATE TABLE llm_bot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    scenario JSON,
    generation_params JSON,
    provider_name VARCHAR(100),
    system_prompt TEXT,
    system_extraction_variables TEXT,
    system_prompt_generation TEXT,
    system_extraction_profile TEXT,
    data_excel JSON,
    create_at INT,
    update_at INT,
    INDEX idx_provider (provider_name),
    INDEX idx_create_at (create_at)
);
```

**Mô tả các cột:**

| Cột | Kiểu | Mô tả |
| :--- | :--- | :--- |
| `id` | INT | Primary key, auto increment |
| `name` | VARCHAR(255) | Tên bot |
| `description` | TEXT | Mô tả chi tiết |
| `scenario` | JSON | Kịch bản hội thoại |
| `generation_params` | JSON | Tham số generation (temperature, max_tokens, ...) |
| `provider_name` | VARCHAR(100) | Tên LLM provider (openai, groq, gemini) |
| `system_prompt` | TEXT | System prompt cho LLM |
| `system_extraction_variables` | TEXT | Prompt trích xuất biến |
| `system_prompt_generation` | TEXT | Prompt sinh câu trả lời |
| `system_extraction_profile` | TEXT | Prompt trích xuất profile người dùng |
| `data_excel` | JSON | Dữ liệu Excel gốc |
| `create_at` | INT | Unix timestamp tạo |
| `update_at` | INT | Unix timestamp cập nhật |

#### llm_history Table

```sql
CREATE TABLE llm_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL,
    input TEXT,
    output TEXT,
    process_time FLOAT,
    create_at INT,
    bot_id INT,
    FOREIGN KEY (bot_id) REFERENCES llm_bot(id),
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_bot_id (bot_id),
    INDEX idx_create_at (create_at)
);
```

### 5.2. Redis Keys Structure

#### Conversation State

```
Key: {conversation_id}
Value: JSON
{
    "conversation_id": "conv_123",
    "bot_id": 1,
    "user_id": "user_456",
    "state": "INTRO",
    "input_slots": {...},
    "bot_config": {...},
    "history": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ],
    "metadata": {...}
}
TTL: 30 minutes
```

#### Task Results

```
Key: task_{task_id}
Value: JSON
{
    "status": "completed",
    "result": {...},
    "error": null
}
TTL: 5-30 minutes (tùy loại task)
```

## 6. Error Handling và Logging

### 6.1. Error Handling Strategy

Hệ thống sử dụng một chiến lược xử lý lỗi phân cấp:

1. **Try-Catch Block:** Mỗi function chính đều có try-catch để bắt các exception.
2. **Custom Exceptions:** Định nghĩa các exception tùy chỉnh cho các loại lỗi khác nhau.
3. **Graceful Degradation:** Khi có lỗi, hệ thống cố gắng cung cấp một phản hồi hữu ích thay vì crash.
4. **Logging:** Tất cả lỗi đều được ghi log chi tiết để debug.

### 6.2. Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

**Log Levels:**

- **DEBUG:** Thông tin chi tiết cho debug
- **INFO:** Thông tin chung về luồng xử lý
- **WARNING:** Cảnh báo về các vấn đề tiềm tàng
- **ERROR:** Lỗi xảy ra nhưng hệ thống vẫn hoạt động
- **CRITICAL:** Lỗi nghiêm trọng, hệ thống có thể không hoạt động

## 7. Configuration Management

### 7.1. Environment Variables

Hệ thống sử dụng các biến môi trường để cấu hình:

```bash
# API Configuration
HOST=0.0.0.0
PORT=9403
WORKERS=4

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USERNAME=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=robot_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=password

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest

# LLM Providers
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=...

# Application
LOG_LEVEL=INFO
PATH_FILE_CONFIG=config.yml
```

### 7.2. Configuration File (config.yml)

```yaml
PROVIDER_MODELS:
  openai:
    provider_setting:
      api_key: ${OPENAI_API_KEY}
      base_url: https://api.openai.com/v1
    generation_params:
      model: gpt-4o-mini
      temperature: 0.0
      max_tokens: 1024
  
  groq:
    provider_setting:
      api_key: ${GROQ_API_KEY}
      base_url: https://api.groq.com/openai/v1
    generation_params:
      model: mixtral-8x7b-32768
      temperature: 0.0
      max_tokens: 1024
  
  gemini:
    provider_setting:
      api_key: ${GEMINI_API_KEY}
    generation_params:
      model: gemini-2.5-flash
      temperature: 0.0
      max_tokens: 1024
```

## 8. Performance Optimization

### 8.1. Caching Strategy

- **Redis Cache:** Lưu trữ conversation state, bot config, và task results.
- **TTL Management:** Đặt TTL phù hợp cho từng loại dữ liệu.
- **Cache Invalidation:** Khi dữ liệu được cập nhật, cache tương ứng được xóa.

### 8.2. Async Processing

- **Async/Await:** Sử dụng async/await cho các I/O operations.
- **Background Tasks:** Các tác vụ nặng được xử lý ở background thông qua RabbitMQ.
- **Connection Pooling:** Sử dụng connection pooling cho database và Redis.

### 8.3. Database Optimization

- **Indexing:** Tạo indexes trên các cột thường xuyên được query.
- **Query Optimization:** Sử dụng efficient queries, tránh N+1 problem.
- **Pagination:** Khi truy vấn danh sách lớn, sử dụng pagination.

## 9. Testing Strategy

### 9.1. Unit Tests

Mỗi module chính nên có unit tests:

```python
import pytest

class TestBaseAgent:
    @pytest.mark.asyncio
    async def test_run_async_success(self):
        """Test BaseAgent.run_async() thành công"""
        # Setup
        agent = BaseAgent(name="test_agent")
        input_state = BaseState(user_input="Hello")
        
        # Mock graph
        agent.graph = Mock()
        agent.graph.astream_events = AsyncMock()
        
        # Execute
        result = await agent.run_async(input_state)
        
        # Assert
        assert result["status"] == "success"
```

### 9.2. Integration Tests

Kiểm thử tương tác giữa các module:

```python
@pytest.mark.asyncio
async def test_conversation_flow():
    """Test toàn bộ luồng hội thoại"""
    # Setup database, redis, rabbitmq
    # ...
    
    # Khởi tạo hội thoại
    # Gửi tin nhắn
    # Kiểm tra kết quả
```

### 9.3. Load Tests

Kiểm thử hiệu suất dưới tải cao:

```python
from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def send_message(self):
        self.client.post("/webhook", json={
            "conversation_id": "test_conv",
            "message": "Hello"
        })
```

## 10. Deployment Considerations

### 10.1. Docker Deployment

**Dockerfile cho Main App:**

```dockerfile
FROM python:3.10

WORKDIR /opt

COPY requirement.txt /opt/
RUN pip install -r requirement.txt

EXPOSE 9403

COPY app /opt/app
COPY src /opt/src
COPY config.yml /opt/

CMD ["python", "-u", "app/server.py"]
```

**Dockerfile cho Worker:**

```dockerfile
FROM python:3.10

WORKDIR /opt

COPY requirement.txt /opt/
RUN pip install -r requirement.txt

COPY app /opt/app
COPY src /opt/src
COPY config.yml /opt/

CMD ["python", "-u", "worker_tools.py"]
```

### 10.2. Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "9403:9403"
    environment:
      - MYSQL_HOST=mysql
      - REDIS_HOST=redis
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - mysql
      - redis
      - rabbitmq
  
  worker:
    build:
      dockerfile: Dockerfile.worker
    environment:
      - MYSQL_HOST=mysql
      - REDIS_HOST=redis
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - mysql
      - redis
      - rabbitmq
    deploy:
      replicas: 5
  
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=robot_db
    volumes:
      - mysql_data:/var/lib/mysql
  
  redis:
    image: redis:7.2.4
    command: redis-server --requirepass password
    volumes:
      - redis_data:/data
  
  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest
    ports:
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  mysql_data:
  redis_data:
  rabbitmq_data:
```

---

**Kết luận:** Tài liệu này cung cấp chi tiết kỹ thuật toàn diện về cấu trúc, thiết kế, và triển khai hệ thống Robot AI Workflow. Nó phục vụ như một hướng dẫn tham khảo cho các developer khi phát triển, bảo trì, và mở rộng hệ thống.
