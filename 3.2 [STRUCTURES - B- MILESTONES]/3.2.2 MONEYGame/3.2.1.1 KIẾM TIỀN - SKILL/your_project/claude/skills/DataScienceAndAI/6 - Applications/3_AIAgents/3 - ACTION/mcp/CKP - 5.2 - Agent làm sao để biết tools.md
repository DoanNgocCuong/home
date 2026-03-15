

# Best Practices: Cơ Chế Tìm MCP và Tools của Agent

Dựa trên tài liệu chính thức và thực tiễn hiện nay, đây là hướng dẫn chi tiết về cách agent tìm kiếm và tương tác với MCP servers và tools:

## 🔍 **Agent Tìm MCP hay Tools Trực Tiếp?**

### **Câu Trả Lời Ngắn:**

Agent **KHÔNG** tìm MCP servers trực tiếp. Thay vào đó:

1. **MCP Host** (ứng dụng AI như Claude Desktop, VS Code) quản lý kết nối đến MCP servers
2. **MCP Client** (một instance cho mỗi server) duy trì kết nối và lấy danh sách tools
3. **Agent/LLM** chỉ tương tác với **tools đã được expose**, không biết về MCP servers

---

## 🏗️ **Kiến Trúc Chuẩn: MCP Host → Client → Server**

```
┌─────────────────────────────────────────────┐
│  MCP Host (Claude Desktop, VS Code, etc.)   │
│  ┌─────────────┐     ┌─────────────┐        │
│  │ MCP Client  │     │ MCP Client  │        │
│  │   (for      │     │   (for      │        │
│  │  Google     │     │ Salesforce) │        │
│  │   Drive)    │     │             │        │
│  └──────┬──────┘     └──────┬──────┘        │
└─────────┼───────────────────┼────────────────┘
          │                   │
          ▼                   ▼
   ┌─────────────┐     ┌─────────────┐
   │  MCP Server │     │  MCP Server │
   │ (Google Dr.)│     │ (Salesforce)│
   └─────────────┘     └─────────────┘
```

**Luồng hoạt động:**

1. MCP Host tạo 1 MCP Client cho mỗi MCP Server cần kết nối
2. Mỗi MCP Client gọi `tools/list` để lấy danh sách tools từ server
3. Agent/LLM chỉ nhìn thấy **danh sách tools tổng hợp** từ tất cả servers

[Model Context Protocol](https://modelcontextprotocol.io/)

---

## 📋 **Cách Khai Báo Tools Chuẩn**

### **1. Server Phải Declare Capability**

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    }
  }
}
```

- `listChanged: true` → Server sẽ gửi notification khi danh sách tools thay đổi

[Tools Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

### **2. Tool Definition Schema**

```json
{
  "name": "get_weather",
  "title": "Weather Information Provider",
  "description": "Get current weather information for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code"
      }
    },
    "required": ["location"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": {"type": "number"},
      "conditions": {"type": "string"}
    }
  }
}
```

**Các thành phần bắt buộc:**

- `name` (required): Unique identifier
- `description` (required): Mô tả rõ ràng cho LLM hiểu khi nào dùng tool
- `inputSchema` (required): JSON Schema định nghĩa parameters
- `outputSchema` (optional): JSON Schema của kết quả trả về

---

## 🔄 **Flow Tìm Kiếm và Sử Dụng Tools**

### **Bước 1: Client Discovers Tools**

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [...],
    "nextCursor": "next-page-cursor"
  }
}
```

### **Bước 2: Agent Calls Tool**

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "location": "New York"
    }
  }
}
```

---

## ⚡ **2 Pattern Chính: Direct vs Code Execution**

### **Pattern 1: Direct Tool Calling (Traditional)**

```
Agent → tools/list → Load ALL tools vào context
      → tools/call → Gọi từng tool riêng lẻ
      → Kết quả trả về context
```

**Nhược điểm:**

- ❌ Hàng trăm tools = hàng trăm ngàn tokens trong context
- ❌ Kết quả trung gian chiếm thêm tokens
- ❌ Chậm và tốn chi phí

[Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

### **Pattern 2: Code Execution with MCP (Modern - Best Practice)**

```
Agent → Filesystem tree of tools → Load only needed tools
      → Write code to call tools
      → Execute in sandbox environment
      → Only final results vào context
```

**Ví dụ filesystem structure:**

```
servers/
  google-drive/
    getDocument.ts
    index.ts
  salesforce/
    updateRecord.ts
    index.ts
```

**Code thay vì direct calls:**

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

const transcript = (await gdrive.getDocument({ 
  documentId: 'abc123' 
})).content;

await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**Ưu điểm:**

- ✅ Giảm token usage 98.7% (từ 150k → 2k tokens)
- ✅ Progressive disclosure: Load tools on-demand
- ✅ Filter data trong execution environment
- ✅ Complex logic (loops, conditionals) trong code
- ✅ Privacy: Sensitive data không qua LLM context

---

## 🎯 **Best Practices Cụ Thể**

### **1. Tool Naming Convention**

- **Chuẩn đề xuất:** 1-64 ký tự, case-sensitive, alphanumeric
- **Format:** `{namespace}_{action}` hoặc `{service}.{action}`
- **Ví dụ:** `gdrive_getDocument`, `salesforce.updateRecord`

### **2. Tool Description**

```json
{
  "name": "search_database",
  "description": "Search the product database. Use when user asks about product availability, pricing, or specifications. Parameters: query (search term), limit (max results, default 10)",
  "inputSchema": {...}
}
```

**Nguyên tắc:**

- Mô tả rõ **khi nào** dùng tool
- Bao gồm **examples** trong description
- List **parameters** với ý nghĩa rõ ràng

### **3. Progressive Tool Discovery**

**Option A: Search Function**

```typescript
// Thêm tool đặc biệt để tìm kiếm tools
{
  "name": "search_tools",
  "description": "Search available tools by keyword",
  "inputSchema": {
    "properties": {
      "keyword": {"type": "string"},
      "detail_level": {
        "enum": ["name_only", "name_and_desc", "full_schema"]
      }
    }
  }
}
```

**Option B: Filesystem Navigation**

```typescript
// Agent explores filesystem để tìm tools
await fs.readdir('./servers/');  // → ['google-drive', 'salesforce']
await fs.readFile('./servers/salesforce/updateRecord.ts');
```

### **4. State Management & Skills**

```typescript
// Lưu intermediate results
const leads = await salesforce.query({...});
await fs.writeFile('./workspace/leads.csv', csvData);

// Lưu reusable functions
// ./skills/save-sheet-as-csv.ts
export async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  // ... convert to CSV
  return csvPath;
}

// Sau này import và dùng lại
import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
```

### **5. Security Best Practices**

**Server-side:**

- ✅ Validate all tool inputs
- ✅ Implement access controls
- ✅ Rate limit tool invocations
- ✅ Sanitize outputs

**Client-side:**

- ✅ User confirmation cho sensitive operations
- ✅ Show tool inputs trước khi call
- ✅ Validate results before passing to LLM
- ✅ Implement timeouts
- ✅ Log tool usage for audit

---

## 📊 **So Sánh 2 Approaches**

|Aspect|Direct Tool Calling|Code Execution with MCP|
|---|---|---|
|**Token Usage**|Tất cả tools vào context|Load on-demand (~98% tiết kiệm)|
|**Latency**|Cao (mỗi tool call qua LLM)|Thấp (batch execution)|
|**Complex Logic**|Khó (chain multiple calls)|Dễ (native code)|
|**Privacy**|Tất cả data qua context|Data ở execution env|
|**Setup Complexity**|Đơn giản|Cần sandboxed environment|
|**Best For**|Few tools, simple workflows|Many tools, complex workflows|

---

## 🚀 **Khuyến Nghị Implementation**

### **Cho Hệ Thống Nhỏ (<20 tools):**

- Dùng **Direct Tool Calling**
- Load tất cả tools vào context
- Đơn giản, dễ implement

### **Cho Hệ Thống Lớn (>50 tools):**

- Dùng **Code Execution with MCP**
- Implement filesystem-based tool discovery
- Build skills library cho reusability
- Setup secure sandbox environment (Docker, gVisor, Firecracker)

### **Hybrid Approach:**

- Frequent tools → Direct calling
- Rare/complex tools → Code execution
- Tool search function để agent tự quyết định

---

## 🔗 **Tài Nguyên Tham Khảo**

- [MCP Specification](https://modelcontextprotocol.io/specification/latest)
- [Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [Anthropic: Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [MCP GitHub Servers](https://github.com/modelcontextprotocol/servers)

---

**Tóm lại:** Agent không tìm MCP servers trực tiếp, mà tương tác với tools đã được MCP Client expose. Best practice hiện đại là dùng **Code Execution pattern** để tiết kiệm tokens và tăng hiệu quả, thay vì load tất cả tools vào context như traditional approach.


---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# có dẫn chứng nào cho việc lý giải kia ko

Có, phần “agent chỉ cần thấy tools, không cần biết server” không phải tự nghĩ ra, mà bám khá sát tài liệu kiến trúc + SDK hiện tại.

## 1. MCP định nghĩa rõ Host quản MCP servers, agent chỉ tương tác tools

- Trang **Architecture overview** mô tả 3 thành phần: *host application*, *MCP clients* và *MCP servers*; host kết nối nhiều server, “discovers tools”, rồi **expose chúng như một tập tools cho model/agent sử dụng**.[^1][^2]
- Phần mô tả tools nêu rõ: tools là “capabilities that MCP servers expose to AI models”, còn việc kết nối server, auth, routing… thuộc về host/client layer, không phải nhiệm vụ của LLM.[^3][^4]

=> Ý này gián tiếp nói: model/agent làm việc ở level “tool”, còn khái niệm “server” là chi tiết triển khai nằm ở lớp dưới.

## 2. OpenAI / VS Code SDK model hóa “servers” ở host, “tools” cho agent

- **OpenAI Agents Python SDK – MCP**: phần docs mô tả bạn cấu hình MCP servers (URL, command) trên **agent host**, SDK sẽ “attach” tools từ servers đó vào agent; phía model chỉ nhận danh sách tools với `name`, `description`, `parameters`, không động đến server name hay URL.[^5]
- **VS Code Copilot MCP docs**: người dùng cấu hình `mcpServers` (per server), Copilot sau đó “makes the tools from those servers available to the agent”; hướng dẫn không có chỗ nào yêu cầu model/agent phải biết server name để gọi tool.[^6]

=> Cả hai đều implement đúng pattern: server là config của host, tool là interface cho agent.

## 3. Bài viết kiến trúc MCP nhấn mạnh “tools = abstraction cho agent”

- Bài giới thiệu MCP của Stytch mô tả kiến trúc với emphasis: “MCP servers expose **tools** that AI agents can call; the hosting application manages server connections and aggregates tools from multiple servers.”[^7]
- Bài phân tích kiến trúc MCP (Kubiya, PingIdentity, v.v.) đều vẽ sơ đồ: nhiều MCP servers → host/registry → **unified tool surface** mà agent tương tác, routing server được xử lý ở host.[^8][^9]

=> Đây chính là lý do nhiều tác giả gọi MCP là “**structured tool abstraction**” chứ không phải API gateway cho LLM.

## 4. Code Execution with MCP: model làm việc với “functions”, routing là việc của runtime

- Bài **“Code execution with MCP”** mô tả pattern: model viết code import modules (tools), rồi runtime map các function đó sang MCP calls đến servers tương ứng; model không giữ knowledge về server endpoints, chỉ biết “gọi hàm nào”.[^10][^11]
- Phần đánh giá lợi ích nhấn mạnh: giảm token, giảm complexity trên phía model bằng cách **ẩn protocol-level chi tiết** (server, JSON-RPC) khỏi reasoning path.[^12][^10]

=> Đây là dẫn chứng trực tiếp cho ý: **càng đẩy chi tiết server xuống dưới, để model chỉ làm việc với API/functions/tools, hệ thống càng dễ scale và ít lỗi hơn.**

***

Tổng hợp: tài liệu chính thức (architecture + tools), SDK (OpenAI, VS Code) và các bài technical blog về MCP/Code Execution đều mô tả cùng một pattern: **Host/Client biết servers, agent biết tools**. Không có câu “agent tuyệt đối không được biết server”, nhưng toàn bộ design + ví dụ code đều đi theo hướng đó, nên mới được xem là best practice kiến trúc.

<div align="center">⁂</div>

[^1]: https://modelcontextprotocol.io/docs/learn/architecture

[^2]: https://modelcontextprotocol.wiki/en/docs/concepts/architecture

[^3]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

[^4]: https://modelcontextprotocol.wiki/en/docs/concepts/tools

[^5]: https://openai.github.io/openai-agents-python/mcp/

[^6]: https://code.visualstudio.com/docs/copilot/customization/mcp-servers

[^7]: https://stytch.com/blog/model-context-protocol-introduction/

[^8]: https://www.kubiya.ai/blog/model-context-protocol-mcp-architecture-components-and-workflow

[^9]: https://developer.pingidentity.com/identity-for-ai/agents/idai-what-is-mcp.html

[^10]: https://www.anthropic.com/engineering/code-execution-with-mcp

[^11]: https://jangwook.net/en/blog/en/anthropic-code-execution-mcp/

[^12]: https://www.hiveresearch.com/post/rethinking-ai-agent-architecture-a-case-study-in-code-execution-over-protocol-abstraction




---
