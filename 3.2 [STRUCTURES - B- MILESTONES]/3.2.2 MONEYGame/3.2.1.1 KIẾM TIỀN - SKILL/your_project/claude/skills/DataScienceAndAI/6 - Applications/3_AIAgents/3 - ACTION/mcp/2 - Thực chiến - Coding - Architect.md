
1. https://dev.to/rajeev_3ce9f280cbae73b234/building-smarter-local-ai-agents-with-mcp-a-simple-client-server-example-4lfm
2. 
![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Felrj904jg9ydlofywwdl.png)



```
ALL IN ONE , MECE, DEEP RESEARCH Hướng dẫn CHI TIẾT về architect, cách dùng, cách triển khai,  mcp tools trong các luồng agent?? 
 MECE tất cả các loại tools, và tất cả các loại cách triển khai - Full code

```

```
Hướng dẫn về cách dùng mcp tools trong các luồng agent?? 
Full code
```


<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Hướng dẫn về cách dùng mcp tools trong các luồng agent??

Full code

Tôi đã tìm hiểu chi tiết về cách sử dụng MCP tools trong các luồng agent và tổng hợp thành hướng dẫn đầy đủ với code hoàn chỉnh dưới đây.

# Hướng Dẫn Đầy Đủ: Sử Dụng MCP Tools Trong Luồng Agent

## Tổng Quan

Model Context Protocol (MCP) là giao thức chuẩn giúp kết nối AI agents với các công cụ và nguồn dữ liệu bên ngoài. MCP hoạt động theo kiến trúc client-server, cho phép LLM động sử dụng tools thông qua một giao thức thống nhất.[^1][^2][^3][^4]

**Kiến trúc MCP:**

- **MCP Server**: Cung cấp tools, resources, prompts cho agents
- **MCP Client**: Nằm trong agent, giao tiếp với server
- **Transport**: stdio (local), HTTP/SSE (remote), Streamable HTTP


## 1. Xây Dựng MCP Server

### Setup Môi Trường

```bash
# Cài đặt UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Tạo project
uv init mcp-agent-demo
cd mcp-agent-demo

# Cài đặt dependencies
uv add "mcp[cli]" httpx
```


### Code MCP Server Hoàn Chỉnh

**File: `mcp_server/agent_tools_server.py`**

```python
from typing import Any
from mcp.server.fastmcp import FastMCP
import httpx

# Khởi tạo FastMCP server
mcp = FastMCP("agent_tools")

# Constants
API_BASE = "https://api.example.com"
USER_AGENT = "mcp-agent/1.0"

# ==================== HELPER FUNCTIONS ====================

async def make_api_request(url: str) -> dict[str, Any] | None:
    """Thực hiện API request với error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return None

# ==================== TOOLS ====================

@mcp.tool()
async def search_data(query: str, limit: int = 10) -> str:
    """Tìm kiếm dữ liệu từ API.
    
    Args:
        query: Từ khóa tìm kiếm
        limit: Số lượng kết quả tối đa
    """
    url = f"{API_BASE}/search?q={query}&limit={limit}"
    data = await make_api_request(url)
    
    if not data:
        return "Không tìm thấy kết quả."
    
    results = []
    for item in data.get("items", []):
        results.append(f"- {item.get('title')}: {item.get('description')}")
    
    return "\n".join(results) if results else "Không có dữ liệu."

@mcp.tool()
async def calculate(expression: str) -> str:
    """Tính toán biểu thức toán học.
    
    Args:
        expression: Biểu thức cần tính (vd: "2 + 2", "10 * 5")
    """
    try:
        # Chỉ cho phép các phép tính an toàn
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Kết quả: {result}"
    except Exception as e:
        return f"Lỗi tính toán: {str(e)}"

@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Lấy thông tin thời tiết cho thành phố.
    
    Args:
        city: Tên thành phố
    """
    url = f"https://api.weatherapi.com/v1/current.json?q={city}"
    data = await make_api_request(url)
    
    if not data:
        return f"Không tìm thấy thông tin thời tiết cho {city}."
    
    current = data.get("current", {})
    return f"""
Thời tiết tại {city}:
- Nhiệt độ: {current.get('temp_c')}°C
- Điều kiện: {current.get('condition', {}).get('text')}
- Độ ẩm: {current.get('humidity')}%
"""

@mcp.tool()
async def get_user_info(user_id: int) -> str:
    """Lấy thông tin người dùng từ database.
    
    Args:
        user_id: ID của người dùng
    """
    # Giả lập database query
    users = {
        1: {"name": "Nguyễn Văn A", "email": "nva@example.com", "role": "Admin"},
        2: {"name": "Trần Thị B", "email": "ttb@example.com", "role": "User"}
    }
    
    user = users.get(user_id)
    if not user:
        return f"Không tìm thấy user với ID {user_id}."
    
    return f"User: {user['name']}\nEmail: {user['email']}\nRole: {user['role']}"

# ==================== PROMPTS ====================

@mcp.prompt()
async def analyst_prompt(task: str) -> str:
    """Prompt cho agent phân tích dữ liệu.
    
    Args:
        task: Nhiệm vụ cần phân tích
    """
    return f"""Bạn là một data analyst chuyên nghiệp. 
Nhiệm vụ của bạn: {task}

Hãy:
1. Phân tích dữ liệu một cách có hệ thống
2. Đưa ra insights quan trọng
3. Đề xuất actions cụ thể"""

@mcp.prompt()
async def researcher_prompt(topic: str) -> str:
    """Prompt cho agent nghiên cứu.
    
    Args:
        topic: Chủ đề nghiên cứu
    """
    return f"""Bạn là một researcher chuyên sâu về {topic}.
Hãy tìm hiểu toàn diện và trình bày:
- Tổng quan
- Phân tích chi tiết
- Xu hướng hiện tại
- Khuyến nghị"""

# ==================== RESOURCES ====================

@mcp.resource("config://settings")
async def get_config() -> str:
    """Resource chứa cấu hình hệ thống."""
    return """
{
  "api_version": "v1",
  "timeout": 30,
  "max_retries": 3,
  "enabled_features": ["search", "weather", "calculate"]
}
"""

# ==================== MAIN ====================

def main():
    """Khởi động MCP server."""
    print("🚀 Starting MCP Agent Tools Server...")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```


### Giải Thích Code Server

1. **FastMCP Framework**: Sử dụng decorator `@mcp.tool()` để tự động generate tool schemas[^5][^6]
2. **Tools**: Các function Python được expose thành MCP tools với type hints và docstrings[^4][^5]
3. **Async Design**: Tất cả tools đều async để xử lý I/O hiệu quả
4. **Error Handling**: Mỗi tool có try-catch để xử lý lỗi gracefully
5. **Prompts \& Resources**: Cung cấp templates và config cho agents[^7][^5]

## 2. Xây Dựng MCP Client + Agent

### Client Với OpenAI Agent

**File: `agent_client/openai_agent.py`**

```python
import asyncio
import os
import sys
from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
import json

class MCPAgentClient:
    """MCP Client tích hợp OpenAI Agent."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        
        # Khởi tạo OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY không được set!")
        
        self.openai = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        self.max_tokens = 2000
    
    # ==================== CONNECTION ====================
    
    async def __aenter__(self):
        """Kết nối đến MCP server khi enter context."""
        return self
    
    async def __aexit__(self, *args):
        """Cleanup khi exit context."""
        await self.exit_stack.aclose()
    
    async def connect_to_server(self, server_path: str):
        """Kết nối đến MCP server.
        
        Args:
            server_path: Đường dẫn đến file server.py
        """
        try:
            # Thiết lập stdio transport
            server_params = StdioServerParameters(
                command="python",
                args=[server_path],
                env=None
            )
            
            # Kết nối đến server
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            
            read, write = stdio_transport
            
            # Tạo client session
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            
            # Initialize session
            await self.session.initialize()
            
            # List available tools
            tools_response = await self.session.list_tools()
            print(f"✅ Đã kết nối! Tools: {[t.name for t in tools_response.tools]}")
            
        except Exception as e:
            raise RuntimeError(f"Lỗi kết nối server: {e}")
    
    # ==================== TOOL HANDLING ====================
    
    async def _get_mcp_tools(self) -> list:
        """Lấy danh sách tools từ MCP server và format cho OpenAI."""
        response = await self.session.list_tools()
        
        openai_tools = []
        for tool in response.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "No description",
                    "parameters": getattr(
                        tool, 
                        "inputSchema", 
                        {"type": "object", "properties": {}}
                    )
                }
            })
        
        return openai_tools
    
    async def _execute_tool(self, tool_call) -> dict:
        """Thực thi MCP tool call.
        
        Args:
            tool_call: Tool call object từ OpenAI
            
        Returns:
            Dict chứa log và message cho OpenAI
        """
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments or "{}")
        
        print(f"🔧 Executing: {tool_name}({tool_args})")
        
        try:
            # Call MCP tool
            result = await self.session.call_tool(tool_name, tool_args)
            
            # Extract content
            content = result.content[^0].text if result.content else ""
            log = f"[✓ {tool_name} completed]"
            
        except Exception as e:
            content = f"Error: {str(e)}"
            log = f"[✗ {tool_name} failed: {e}]"
        
        return {
            "log": log,
            "message": {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": content
            }
        }
    
    # ==================== AGENT WORKFLOW ====================
    
    async def process_query(self, query: str) -> str:
        """Xử lý query với agent workflow hoàn chỉnh.
        
        Workflow:
        1. Gửi query đến LLM với tools
        2. LLM quyết định tool nào cần dùng
        3. Execute tools thông qua MCP
        4. Gửi kết quả về LLM
        5. LLM tạo response cuối cùng
        
        Args:
            query: User query
            
        Returns:
            Final response từ agent
        """
        # Khởi tạo conversation
        messages = [{"role": "user", "content": query}]
        
        # Lấy available tools
        tools = await self._get_mcp_tools()
        
        # ===== BƯỚC 1: Initial LLM Call =====
        print(f"\n💭 Sending to LLM: {query}")
        
        response = self.openai.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
            tools=tools
        )
        
        current_message = response.choices[^0].message
        result_parts = []
        
        # Lưu text response nếu có
        if current_message.content:
            result_parts.append(current_message.content)
        
        # ===== BƯỚC 2: Tool Execution Loop =====
        if tool_calls := current_message.tool_calls:
            print(f"\n🔧 LLM muốn dùng {len(tool_calls)} tool(s)")
            
            # Thêm assistant message vào history
            messages.append({
                "role": "assistant",
                "content": current_message.content or "",
                "tool_calls": tool_calls
            })
            
            # Execute từng tool
            for tool_call in tool_calls:
                tool_result = await self._execute_tool(tool_call)
                result_parts.append(tool_result["log"])
                messages.append(tool_result["message"])
            
            # ===== BƯỚC 3: Final LLM Call với Tool Results =====
            print("\n💭 Sending tool results back to LLM...")
            
            final_response = self.openai.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages
            )
            
            # Lấy final response
            if content := final_response.choices[^0].message.content:
                result_parts.append(content)
        
        return "\n\n".join(result_parts)
    
    # ==================== CHAT INTERFACE ====================
    
    async def chat_loop(self):
        """Interactive chat loop với agent."""
        print("\n" + "="*50)
        print("🤖 MCP Agent Chat Started!")
        print("Commands: 'quit' để thoát, 'help' để xem hướng dẫn")
        print("="*50 + "\n")
        
        while True:
            try:
                # Nhận input từ user
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print("""
📚 Các lệnh có thể dùng:
- search_data: Tìm kiếm dữ liệu
- calculate: Tính toán
- fetch_weather: Xem thời tiết
- get_user_info: Lấy thông tin user

Ví dụ: "Tìm kiếm thông tin về AI" hoặc "Tính 25 * 4"
                    """)
                    continue
                
                # Process query
                print("\n🤔 Agent đang suy nghĩ...")
                response = await self.process_query(user_input)
                
                print(f"\n🤖 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

# ==================== MAIN ====================

async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python openai_agent.py <path_to_server.py>")
        sys.exit(1)
    
    server_path = sys.argv[^1]
    
    print(f"🚀 Starting MCP Agent Client...")
    print(f"📂 Server: {server_path}")
    
    async with MCPAgentClient() as client:
        await client.connect_to_server(server_path)
        await client.chat_loop()

if __name__ == "__main__":
    asyncio.run(main())
```


## 3. Tích Hợp Với Frameworks Phổ Biến

### 3.1 CrewAI Integration

**File: `frameworks/crewai_mcp_agent.py`**

```python
from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerStdio

# ===== Cách 1: String-based (Đơn giản) =====

agent_simple = Agent(
    role="Research Analyst",
    goal="Phân tích dữ liệu và đưa ra insights",
    backstory="Expert researcher with MCP tools access",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key",  # External MCP
        "crewai-amp:financial-data",  # CrewAI marketplace
    ]
)

# ===== Cách 2: Structured Config (Kiểm soát đầy đủ) =====

from crewai.mcp.filters import create_static_tool_filter

agent_advanced = Agent(
    role="Data Engineer", 
    goal="Process và transform data",
    backstory="Senior engineer with full MCP control",
    mcps=[
        # Stdio transport cho local server
        MCPServerStdio(
            command="python",
            args=["mcp_server/agent_tools_server.py"],
            env={"API_KEY": "your_key"},
            tool_filter=create_static_tool_filter(
                allowed_tool_names=["search_data", "calculate"]
            ),
            cache_tools_list=True
        )
    ]
)

# Tạo task và crew
task = Task(
    description="Phân tích dữ liệu thị trường AI trong Q1 2025",
    expected_output="Báo cáo phân tích với insights và recommendations",
    agent=agent_advanced
)

crew = Crew(
    agents=[agent_advanced],
    tasks=[task],
    verbose=True
)

# Chạy crew
result = crew.kickoff()
print(result)
```


### 3.2 AutoGen Integration

**File: `frameworks/autogen_mcp_agent.py`**

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def main():
    # ===== Setup MCP Server =====
    mcp_server = StdioServerParams(
        command="python",
        args=["mcp_server/agent_tools_server.py"],
        read_timeout_seconds=100
    )
    
    # Load MCP tools
    tools = await mcp_server_tools(mcp_server)
    print(f"✅ Loaded {len(tools)} tools from MCP server")
    
    # ===== Create Agent =====
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    
    agent = AssistantAgent(
        name="mcp_agent",
        model_client=model_client,
        tools=tools,  # MCP tools được inject vào agent
        system_message="Bạn là AI agent với quyền truy cập MCP tools.",
        reflect_on_tool_use=True  # Agent tự reflect về cách dùng tools
    )
    
    # ===== Run Agent =====
    await Console(
        agent.run_stream(
            task="Tìm kiếm thông tin về 'Machine Learning' và tính 15 * 23"
        )
    )

if __name__ == "__main__":
    asyncio.run(main())
```


### 3.3 LangGraph Integration

**File: `frameworks/langgraph_mcp_agent.py`**

```python
import asyncio
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_mcp import MCPAdapter
from mcp import StdioServerParameters

# ===== Define State =====

class AgentState(TypedDict):
    messages: list
    next: str

# ===== Setup MCP =====

async def setup_mcp_tools():
    """Load MCP tools vào LangGraph."""
    mcp_adapter = MCPAdapter(
        server_command=["python", "mcp_server/agent_tools_server.py"],
        transport_type="stdio"
    )
    
    await mcp_adapter.connect()
    tools = await mcp_adapter.get_tools()
    
    print(f"✅ Loaded {len(tools)} MCP tools")
    return tools

# ===== Agent Node =====

async def agent_node(state: AgentState):
    """Node chạy agent reasoning."""
    llm = ChatOpenAI(model="gpt-4o")
    tools = await setup_mcp_tools()
    
    llm_with_tools = llm.bind_tools(tools)
    response = await llm_with_tools.ainvoke(state["messages"])
    
    return {
        "messages": state["messages"] + [response],
        "next": "tools" if response.tool_calls else "end"
    }

# ===== Tool Node =====

async def tool_node(state: AgentState):
    """Node execute MCP tools."""
    tool_node = ToolNode(await setup_mcp_tools())
    result = await tool_node.ainvoke(state)
    
    return {
        "messages": result["messages"],
        "next": "agent"
    }

# ===== Build Graph =====

def create_agent_graph():
    """Tạo LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Add edges
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        lambda x: x["next"],
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# ===== Run =====

async def main():
    graph = create_agent_graph()
    
    result = await graph.ainvoke({
        "messages": [{"role": "user", "content": "Tính 100 * 25"}],
        "next": ""
    })
    
    print(result["messages"][-1]["content"])

if __name__ == "__main__":
    asyncio.run(main())
```


## 4. Best Practices \& Patterns

### Security Considerations

```python
# ❌ KHÔNG NÊN: Expose tất cả tools
mcps=["https://untrusted-server.com/mcp"]

# ✅ NÊN: Filter tools cẩn thận
from crewai.mcp.filters import create_dynamic_tool_filter

def safe_filter(context, tool):
    # Chỉ cho phép read operations
    dangerous_keywords = ["delete", "write", "modify", "exec"]
    tool_name = tool.get("name", "").lower()
    
    return not any(keyword in tool_name for keyword in dangerous_keywords)

agent = Agent(
    role="Safe Agent",
    mcps=[
        MCPServerStdio(
            command="python",
            args=["server.py"],
            tool_filter=safe_filter
        )
    ]
)
```


### Error Handling Pattern

```python
async def robust_tool_execution(session, tool_name, args):
    """Execute tool với retry và fallback."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            result = await session.call_tool(tool_name, args)
            return result
        
        except TimeoutError:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            return {"error": "Tool timeout after retries"}
        
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
```


### Performance Optimization

```python
# Cache tools list để giảm latency
MCPServerStdio(
    command="python",
    args=["server.py"],
    cache_tools_list=True,  # ✅ Cache
    connect_timeout=60       # ✅ Tăng timeout cho servers chậm
)
```


## 5. Chạy Ứng Dụng

### Setup

```bash
# Clone và setup
git clone <your-repo>
cd mcp-agent-demo

# Install dependencies
uv add mcp openai anthropic crewai langchain-mcp-adapters autogen-agentchat

# Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```


### Chạy OpenAI Agent

```bash
# Terminal 1: Không cần start server riêng (stdio tự động)

# Terminal 1: Chạy agent
uv run python agent_client/openai_agent.py mcp_server/agent_tools_server.py
```


### Chạy CrewAI

```bash
uv run python frameworks/crewai_mcp_agent.py
```


### Chạy AutoGen

```bash
uv run python frameworks/autogen_mcp_agent.py
```


## 6. Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
| :-- | :-- | :-- |
| `Connection refused` | Server path sai | Kiểm tra đường dẫn tuyệt đối[^8][^9] |
| `Tool not found` | Tool name không khớp | Chạy `--members` để list tools[^9] |
| `Timeout` | Server khởi động chậm | Tăng `connect_timeout=60`[^10][^11] |
| `Import error` | Thiếu dependencies | `uv add <package>`[^4] |

## 7. Tài Nguyên Tham Khảo

- **MCP Specification**: https://modelcontextprotocol.io[^12]
- **FastMCP Docs**: https://github.com/jlowin/fastmcp[^6]
- **CrewAI MCP**: https://docs.crewai.com/en/mcp/overview[^10]
- **AutoGen MCP**: https://microsoft.github.io/autogen[^13][^14]

***

**Kết luận**: Hướng dẫn này cung cấp full code để xây dựng MCP server, client và tích hợp với các framework agent phổ biến. Pattern này cho phép agents động sử dụng tools thông qua giao thức chuẩn, dễ mở rộng và bảo trì.[^2][^3][^1][^4]
<span style="display:none">[^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53]</span>

<div align="center">⁂</div>

[^1]: https://viblo.asia/p/gioi-thieu-ve-model-context-protocol-mcp-BQyJKEOWVMe

[^2]: https://vinbigdata.com/kham-pha/giai-ma-mcp-chuan-ket-noi-moi-cho-ai-agents.html

[^3]: https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools

[^4]: https://openai.github.io/openai-agents-python/mcp/

[^5]: https://modelcontextprotocol.io/docs/develop/build-server

[^6]: https://github.com/jlowin/fastmcp

[^7]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

[^8]: https://mcpcn.com/en/docs/tutorials/building-a-client/

[^9]: https://realpython.com/python-mcp-client/

[^10]: https://docs.crewai.com/en/mcp/overview

[^11]: https://docs.crewai.com/en/mcp/multiple-servers

[^12]: https://modelcontextprotocol.io/specification/2025-11-25

[^13]: https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools

[^14]: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/components/workbench.html

[^15]: https://www.youtube.com/watch?v=x0C003ePDlk

[^16]: https://www.facebook.com/groups/miaigroup/posts/1952211818883414/

[^17]: https://www.youtube.com/watch?v=XKae3FgKZnM

[^18]: https://www.merge.dev/blog/mcp-integration-examples

[^19]: https://superagi.com/mastering-mcp-servers-in-2025-a-beginners-guide-to-model-context-protocol-implementation/

[^20]: https://viblo.asia/p/giao-thuc-model-context-protocol-mcp-trong-net-xay-dung-ai-agent-thong-minh-voi-openai-mcp-3RlL5B9zVbB

[^21]: https://www.bitcot.com/how-to-build-ai-agents-using-mcp-a-complete-guide/

[^22]: https://www.strategysoftware.com/strategyone/whats-new/model-context-protocol-mcp-integration-for-agents

[^23]: https://obot.ai/resources/learning-center/mcp-tools/

[^24]: https://www.reddit.com/r/ChatGPTCoding/comments/1jd9lfa/learn_mcp_by_building_an_sql_ai_agent/

[^25]: https://composio.dev/blog/the-complete-guide-to-building-mcp-agents

[^26]: https://learn.microsoft.com/en-us/dynamics365/release-plan/2025wave2/service/dynamics365-customer-service/connect-ai-agents-using-model-context-protocol-server

[^27]: https://base.vn/blog/model-context-protocol-mcp-la-gi/

[^28]: https://modelcontextprotocol.info/docs/tutorials/writing-effective-tools/

[^29]: https://cyclr.com/resources/ai/model-context-protocol-mcp-for-ai-integration

[^30]: https://latenode.com/blog/ai-frameworks-technical-infrastructure/langchain-setup-tools-agents-memory/langchain-mcp-integration-complete-guide-to-mcp-adapters

[^31]: https://huggingface.co/blog/python-tiny-agents

[^32]: https://www.mintmcp.com/blog/connect-ai-chains-to enterprise-data-source

[^33]: https://github.com/crewAIInc/crewAI-tools

[^34]: https://docs.langchain.com/oss/python/langchain/mcp

[^35]: https://docs.crewai.com/en/concepts/tools

[^36]: https://phucnt.substack.com/p/mcp-truyen-thong-code-execution-va

[^37]: https://realpython.com/python-mcp/

[^38]: https://www.leanware.co/insights/langchain-mcp-integrating-langchain-with-model-context-protocol

[^39]: https://snyk.io/articles/building-interactive-mcp-servers-experience-on-the-terminal-using-python/

[^40]: https://www.leanware.co/insights/langgraph-mcp-building-powerful-agents-with-mcp-integration

[^41]: https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-mcp-integration-complete-model-context-protocol-setup-guide-working-examples-2025

[^42]: https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html

[^43]: https://developers.redhat.com/articles/2025/08/12/how-build-simple-agentic-ai-server-mcp

[^44]: https://github.com/hirokiyn/mcp-langgraph

[^45]: https://www.youtube.com/watch?v=MDBG2MOp4Go

[^46]: https://generect.com/blog/langgraph-mcp/

[^47]: https://skywork.ai/skypage/en/Mastering-AI-Tool-Integration:-A-Deep-Dive-into-the-mcp_autogen_sse_stdio-MCP-Server-Example/1972504582783287296

[^48]: https://dev.to/rajeev_3ce9f280cbae73b234/building-smarter-local-ai-agents-with-mcp-a-simple-client-server-example-4lfm

[^49]: https://gofastmcp.com/tutorials/create-mcp-server

[^50]: https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/agent-as-mcp-tool

[^51]: https://www.youtube.com/watch?v=je6ZW3rWWMw

[^52]: https://towardsdatascience.com/model-context-protocol-mcp-tutorial-build-your-first-mcp-server-in-6-steps/

[^53]: https://modelcontextprotocol.io/docs/develop/build-client


---
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# ko hiểu lắm, giải thích đơn giản hơn và MECE toàn bộ các cách triển khai

Được rồi, mình sẽ giải thích cực kỳ đơn giản và MECE (Mutually Exclusive, Collectively Exhaustive) tất cả các cách triển khai MCP tools.

# Tất Cả Cách Triển Khai MCP Tools (Đơn Giản \& MECE)

## Framework MECE: 2 Chiều Phân Loại

Có **2 câu hỏi** quyết định cách bạn deploy MCP:

### Câu 1: Server chạy ở đâu?

- **Local** (máy agent)
- **Remote** (máy khác/cloud)


### Câu 2: Bao nhiêu user dùng chung?

- **Single-tenant** (1 user = 1 server riêng)
- **Multi-tenant** (nhiều user → 1 server chung)

→ **Tổ hợp = 3 patterns chính** (vì Local không có multi-tenant)

***

## Pattern 1: **Workstation Deployment** (Local + Single-tenant)

### Server chạy ở đâu?

**Chạy trên máy của agent** - như subprocess

### Diagram đơn giản:

```
┌─────────────────────────────┐
│  Máy của bạn                │
│                             │
│  ┌──────────┐               │
│  │  Agent   │               │
│  │          │ spawn         │
│  │    ↓     │               │
│  │ ┌──────┐ │               │
│  │ │Server│ │               │
│  │ └──────┘ │               │
│  └──────────┘               │
└─────────────────────────────┘
```


### Code minh họa:

```python
# Agent TỰ ĐỘNG spawn server process
server_params = StdioServerParameters(
    command="python",
    args=["my_tools.py"]  # File Python local
)

# Khi agent chạy → server tự khởi động
# Khi agent tắt → server tự tắt
```


### Đặc điểm:

| Tiêu chí | Giá trị |
| :-- | :-- |
| **Có cần deploy không?** | ❌ KHÔNG - chỉ cần file Python |
| **Có cần server riêng không?** | ❌ KHÔNG - subprocess tự động |
| **Có cần worker pool không?** | ❌ KHÔNG - mỗi agent tự spawn |
| **Latency** | <1ms (nhanh nhất)[^1][^2] |
| **Nhiều người dùng được không?** | ❌ KHÔNG - mỗi người chạy riêng |
| **Chi phí** | \$0 (chạy cùng máy agent) |

### Khi nào dùng?[^3]

- ✅ Development/testing
- ✅ Bạn code một mình
- ✅ Tools cần truy cập file local (ví dụ: đọc code trên máy)
- ✅ Desktop app (như Claude Desktop)


### Ưu điểm:

- Setup siêu nhanh (không cần deploy gì)
- Nhanh nhất (không qua network)
- Miễn phí hoàn toàn


### Nhược điểm:

- Chỉ bạn dùng được
- Không share tools với team
- Mỗi lần chạy lại phải spawn lại server

***

## Pattern 2: **Remote - Multi-tenant** (Remote + Shared)

### Server chạy ở đâu?

**Chạy trên server riêng (cloud/VPS)** - nhiều agents kết nối đến

### Diagram đơn giản:

```
┌──────────┐           ┌─────────────────┐
│ Agent 1  │──────┐    │  Server riêng   │
│ (Máy A)  │      │    │  (AWS/GCP)      │
└──────────┘      │    │                 │
                  │    │  ┌───────────┐  │
┌──────────┐     HTTP  │  │ MCP Tools │  │
│ Agent 2  │──────┼───▶│  │  Server   │  │
│ (Máy B)  │      │    │  └───────────┘  │
└──────────┘      │    │                 │
                  │    │  (Chạy 24/7)    │
┌──────────┐      │    └─────────────────┘
│ Agent 3  │──────┘
│ (Máy C)  │
└──────────┘
```


### Code minh họa:

```python
# Server: Deploy lên AWS/GCP
# server.py chạy trên cloud
uvicorn server:app --host 0.0.0.0 --port 8080

# Agent: Connect đến remote URL
agent = Agent(
    mcps=["https://mcp-server.mycompany.com/mcp"]
)
```


### Đặc điểm:

| Tiêu chí | Giá trị |
| :-- | :-- |
| **Có cần deploy không?** | ✅ CÓ - cần server riêng |
| **Có cần server riêng không?** | ✅ CÓ - VPS/cloud |
| **Có cần worker pool không?** | ⚠️ TÙY - nếu traffic cao thì cần nhiều workers |
| **Latency** | 10-50ms (có network)[^1] |
| **Nhiều người dùng được không?** | ✅ CÓ - nhiều người dùng chung 1 server |
| **Chi phí** | \$20-200/month[^3] |

### Khi nào dùng?[^3]

- ✅ Team 3+ người cần dùng chung tools
- ✅ Production app với nhiều users
- ✅ Tools cần chạy 24/7
- ✅ Cần scale horizontally (thêm workers khi traffic tăng)
- ✅ Cần monitoring/logging tập trung


### Ưu điểm:

- Team cùng dùng
- Update tools 1 lần → mọi người có ngay
- Dễ monitor/logging
- Scale được khi traffic tăng


### Nhược điểm:

- Tốn tiền server
- Cần biết DevOps (Docker/K8s)
- Chậm hơn local (có network latency)
- Phải lo bảo mật (authentication, rate limit)

***

## Pattern 3: **Remote - Single-tenant** (Remote + Isolated)

### Server chạy ở đâu?

**Mỗi user có 1 container riêng trên cloud**

### Diagram đơn giản:

```
┌──────────┐           ┌─────────────────────────┐
│ Agent 1  │──────────▶│ Container riêng User 1  │
│ (User 1) │   HTTP    │  ┌───────────┐          │
└──────────┘           │  │ MCP Tools │          │
                       │  └───────────┘          │
                       └─────────────────────────┘

┌──────────┐           ┌─────────────────────────┐
│ Agent 2  │──────────▶│ Container riêng User 2  │
│ (User 2) │   HTTP    │  ┌───────────┐          │
└──────────┘           │  │ MCP Tools │          │
                       │  └───────────┘          │
                       └─────────────────────────┘

              (Mỗi user = 1 container độc lập)
```


### Code minh họa:

```python
# Router nhận request → spawn container cho user
@app.post("/mcp")
async def route_to_user_container(user_id: str):
    # Spawn container nếu chưa có
    container = get_or_create_container(user_id)
    
    # Forward request đến container của user đó
    return forward_to_container(container)
```


### Đặc điểm:

| Tiêu chí | Giá trị |
| :-- | :-- |
| **Có cần deploy không?** | ✅ CÓ - cần orchestration platform |
| **Có cần server riêng không?** | ✅ CÓ - nhiều containers |
| **Có cần worker pool không?** | ✅ CÓ - mỗi user = 1 worker (container) |
| **Latency** | 10-50ms |
| **Nhiều người dùng được không?** | ✅ CÓ - nhưng mỗi người container riêng |
| **Chi phí** | \$100-1000/month (tùy users)[^3] |

### Khi nào dùng?[^4][^3]

- ✅ Cần security cao (mỗi user isolated)
- ✅ Tools có state riêng cho từng user (ví dụ: browser session)
- ✅ Compliance regulations (dữ liệu không được share)
- ✅ Tools tốn resource (GPU, heavy computation)


### Ưu điểm:

- Bảo mật tuyệt đối (mỗi user isolated)
- Container không dùng có thể tắt → tiết kiệm tiền
- Scale theo số users


### Nhược điểm:

- Phức tạp nhất (cần K8s/orchestration)
- Chi phí cao nhất
- Cần DevOps skills mạnh

***

## So Sánh MECE 3 Patterns

| Pattern | Nơi chạy | Số users | Deploy | Cost | Use case |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **Workstation** | Local | 1 | ❌ Không | \$0 | Dev/testing |
| **Remote Multi-tenant** | Cloud | Nhiều (shared) | ✅ Cần | \$20-200 | Team/startup |
| **Remote Single-tenant** | Cloud | Nhiều (isolated) | ✅ Cần | \$100-1000 | Enterprise |


***

## Trả Lời Câu Hỏi Cụ Thể Của Bạn

### "Kho tool này mình cho chạy luồng worker riêng hay cần deploy lên server riêng?"

**Tùy mục đích:**

### Nếu bạn đang **development một mình**:

```python
# ❌ KHÔNG cần worker riêng
# ❌ KHÔNG cần deploy lên server
# ✅ Chỉ cần file Python local

# Pattern: Workstation
agent = Agent(
    mcps=[MCPServerStdio(
        command="python",
        args=["tools.py"]  # File trên máy bạn
    )]
)
```


### Nếu **team 3-5 người cần dùng**:

```bash
# ✅ CẦN deploy lên server riêng
# ✅ CẦN chạy như web service (FastAPI/uvicorn)

# Pattern: Remote Multi-tenant
# Deploy lên Railway/Render (đơn giản)
railway up
# hoặc Docker
docker run -p 8080:8080 mcp-server
```


### Nếu **production với 100+ users**:

```yaml
# ✅ CẦN worker pool với load balancer
# ✅ CẦN Kubernetes/ECS

# Pattern: Remote Multi-tenant với nhiều workers
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 5  # 5 workers
```


### Nếu **enterprise với bảo mật cao**:

```python
# ✅ CẦN container riêng cho mỗi user
# ✅ CẦN orchestration platform (K8s)

# Pattern: Remote Single-tenant
# Mỗi user = 1 container Kubernetes pod
```


***

## Decision Tree Đơn Giản

```
Bạn đang ở giai đoạn nào?
│
├─ Development một mình
│  └─ ✅ Workstation (stdio local)
│     └─ Không cần deploy gì cả
│
├─ Team nhỏ (3-10 người)
│  └─ ✅ Remote Multi-tenant
│     └─ Deploy 1 server lên Railway/Render
│     └─ Chi phí: ~$20/month
│
├─ Production (100+ users)
│  └─ ✅ Remote Multi-tenant + Load Balancer
│     └─ Deploy Kubernetes với 3-5 workers
│     └─ Chi phí: $200-500/month
│
└─ Enterprise (bảo mật cao)
   └─ ✅ Remote Single-tenant
      └─ Mỗi user = 1 container
      └─ Chi phí: $1000+/month
```


***

## Khuyến Nghị Cho Bạn (FinTech Startup)

Dựa trên profile bạn (AI Engineer, đang build fintech startup):

### Phase 1: MVP (Hiện tại - 1-2 tuần đầu)

```python
# ✅ Dùng Workstation
# Không cần deploy, không cần worker, không cần server
MCPServerStdio(command="python", args=["tools.py"])
```

**Lý do**: Iterate nhanh, \$0 cost, focus vào product

### Phase 2: Internal Testing (Tháng 1-2)

```python
# ✅ Deploy 1 container lên Railway
# URL: https://mcp-tools.railway.app/mcp
MCPServerHTTP(url="https://...")
```

**Lý do**: Team test được, vẫn đơn giản, ~\$10/month

### Phase 3: Beta Users (Tháng 3-6)

```bash
# ✅ Docker Compose với 3 workers
docker-compose up --scale worker=3
```

**Lý do**: Handle 50-100 users, ~\$50/month

### Phase 4: Scale (Sau product-market fit)

```yaml
# ✅ Kubernetes với autoscaling
replicas: 5-20 (tự động)
```

**Lý do**: Handle 1000+ users, monitoring đầy đủ

***

## Key Takeaway

**"Worker riêng" và "Server riêng" là 2 khái niệm khác nhau:**

1. **Worker riêng** = Process xử lý requests
    - Workstation: Agent tự spawn (không cần setup)
    - Remote: Uvicorn workers hoặc K8s pods
2. **Server riêng** = Máy chủ chạy độc lập
    - Workstation: KHÔNG cần (chạy local)
    - Remote: CẦN (VPS/cloud)

**Với MVP, bạn KHÔNG cần cả hai** - chỉ cần file Python local.[^5][^6][^3]
<span style="display:none">[^10][^11][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://mcpcat.io/guides/comparing-stdio-sse-streamablehttp/

[^2]: https://www.reddit.com/r/mcp/comments/1kssu2g/mcp_server_transports_inmemory_vs_httpsse_vs_stdio/

[^3]: https://mcpmanager.ai/blog/secure-mcp-server-deployment-at-scale-the-complete-guide/

[^4]: https://fly.io/docs/blueprints/remote-mcp-servers/

[^5]: https://modelcontextprotocol.io/docs/learn/architecture

[^6]: https://www.stainless.com/mcp/local-mcp-vs-remote-mcp

[^7]: https://milvus.io/ai-quick-reference/what-deployment-patterns-support-highavailability-in-model-context-protocol-mcp

[^8]: https://www.reddit.com/r/mcp/comments/1k9knt9/how_are_teams_deploying_mcp_servers_for/

[^9]: https://modelcontextprotocol-security.io/patterns/

[^10]: https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch

[^11]: https://workos.com/blog/how-mcp-servers-work

