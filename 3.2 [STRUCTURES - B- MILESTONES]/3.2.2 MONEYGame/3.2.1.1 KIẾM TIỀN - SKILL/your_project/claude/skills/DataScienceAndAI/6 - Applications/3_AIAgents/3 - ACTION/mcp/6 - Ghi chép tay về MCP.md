## Naming Best Practices cho Tool/MCP/Agent System

### Phân biệt các khái niệm

```
┌─────────────────────────────────────────────────────────────────┐
│                        TERMINOLOGY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MCP Server    = Process cung cấp tools (gdrive-mcp, notion-mcp)│
│  Tool          = Function có thể gọi (search_drive, create_page)│
│  Agent         = AI entity sử dụng tools để hoàn thành task     │
│                                                                 │
│  MCP Server 1:N Tool                                            │
│  Agent N:N Tool                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Naming Patterns

|Pattern|Mục đích|Ví dụ|
|---|---|---|
|**Registry**|Store & lookup by key|`ToolRegistry`, `ServerRegistry`|
|**Manager**|Lifecycle management (start/stop/health)|`MCPManager`, `ConnectionManager`|
|**Catalog**|Read-only listing & metadata|`ToolCatalog`|
|**Executor**|Execute/invoke actions|`ToolExecutor`|
|**Factory**|Create instances|`ClientFactory`|

### Đề xuất cho hệ thống của bạn

```
action_layer/
├── mcp/
│   ├── mcp_manager.py        # Quản lý MCP server connections
│   │                         # - start/stop servers
│   │                         # - health check
│   │                         # - connection pooling
│   │
│   ├── tool_registry.py      # Đăng ký & lookup tools
│   │                         # - register tool
│   │                         # - get tool by name
│   │                         # - list all tools
│   │
│   ├── tool_executor.py      # Thực thi tools
│   │                         # - call tool
│   │                         # - handle errors
│   │                         # - retry logic
│   │
│   └── clients/
│       ├── stdio_client.py
│       └── http_client.py
```

### Class Design

```python
class MCPManager:
    """Quản lý lifecycle của MCP servers"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
    
    async def start_server(self, name: str, config: ServerConfig): ...
    async def stop_server(self, name: str): ...
    async def health_check(self, name: str) -> bool: ...
    def list_servers(self) -> List[str]: ...
    def get_server(self, name: str) -> MCPServer: ...


class ToolRegistry:
    """Registry cho tất cả available tools"""
    
    def __init__(self, mcp_manager: MCPManager):
        self.mcp_manager = mcp_manager
        self._tools_cache: Dict[str, ToolDefinition] = {}
    
    async def refresh(self): 
        """Fetch tools từ tất cả MCP servers"""
        ...
    
    def list_tools(self) -> List[str]: ...
    def get_tool(self, name: str) -> ToolDefinition: ...
    def get_tools_by_server(self, server_name: str) -> List[ToolDefinition]: ...
    def search_tools(self, query: str) -> List[ToolDefinition]: ...


class ToolExecutor:
    """Execute tool calls"""
    
    def __init__(self, mcp_manager: MCPManager):
        self.mcp_manager = mcp_manager
    
    async def execute(self, tool_name: str, arguments: Dict) -> Any: ...
    async def execute_batch(self, calls: List[ToolCall]) -> List[Any]: ...
```

### Flow

```
Cognition Layer
      │
      │ get available tools
      ▼
┌─────────────┐      ┌─────────────┐
│ ToolRegistry│◄─────│ MCPManager  │
│             │      │             │
│ - list      │      │ - servers   │
│ - search    │      │ - lifecycle │
└─────────────┘      └─────────────┘
      │
      │ plan uses tool names
      ▼
┌─────────────┐      ┌─────────────┐
│ToolExecutor │─────►│ MCP Clients │──► MCP Servers
│             │      │             │
│ - execute   │      │ - stdio     │
│ - retry     │      │ - http      │
└─────────────┘      └─────────────┘
```

### Tóm lại

|Đặt tên|Responsibility|
|---|---|
|`MCPManager`|Server lifecycle (start/stop/health)|
|`ToolRegistry`|Tool metadata (list/search/get)|
|`ToolExecutor`|Tool invocation (execute/retry)|

**Không cần `MCPRegistry`** - vì:

- "Registry" nên dành cho **Tools** (thứ được dùng)
- **Servers** nên dùng "Manager" (vì cần quản lý lifecycle)

Xóa `MCPRegistry`, giữ `ToolRegistry` + thêm `MCPManager` nếu cần tách concerns.