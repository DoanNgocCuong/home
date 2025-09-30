
# 1. MCP Chorm Broswer 

Cách cài rất đơn giản: Trong cursor vào MCP và set up JSON 

```jsonc
"chrome-devtools": {
  "command": "npx",
  "args": ["chrome-devtools-mcp@latest"],
  "autoApprove": ["*"]
}
```

`autoApprove: ["*"]` sẽ cho phép tất cả tools chạy mà không cần hỏi.


- Chú ý: Yêu cầu nodeJS >=v19-22 (lúc cài version nodeJS của mình 18 nên mình cần down bản mới hơn)

**Download Node.js v22 LTS:**

- Vào: [https://nodejs.org/](https://nodejs.org/)
- Click nút **"Download Node.js (LTS)"** màu xanh
- Chọn file Windows Installer (.msi)

---
Cài xong thì xem bên `chrome devtools` nó xanh màu chưa là oke ạ. 

![](image/Pasted%20image%2020250930004253.png)
---

- Testing để trải nghiệm: 
```bash
Use the chrome-devtools MCP tool to open https://web.dev in Chrome and measure its LCP performance metric.
```

# Cài 1 loạt 


```bash
{

  "mcpServers": {

    "fetch": {

      "command": "uvx",

      "args": ["mcp-server-fetch"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "GitKraken": {

      "command": "c:\\Users\\User\\AppData\\Roaming\\Cursor\\User\\globalStorage\\eamodio.gitlens\\gk.exe",

      "type": "stdio",

      "name": "GitKraken",

      "args": [

        "mcp",

        "--host=cursor",

        "--source=gitlens",

        "--scheme=cursor"

      ],

      "env": {}

    },

    "chrome-devtools": {

      "command": "npx",

      "args": ["chrome-devtools-mcp@latest"],

      "autoApprove": ["*"]

    },

    "github-npx": {

      "command": "npx",

      "args": ["-y", "@modelcontextprotocol/server-github"],

      "env": {

        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"

      },

      "disabled": false,

      "autoApprove": []

    },

    "filesystem": {

      "command": "uvx",

      "args": ["mcp-server-filesystem", "/path/to/your/projects"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "sqlite": {

      "command": "uvx",

      "args": ["mcp-server-sqlite", "--db-path", "/path/to/your/database.db"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "postgres": {

      "command": "uvx",

      "args": ["mcp-server-postgres", "postgresql://user:password@localhost:5432/dbname"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "github": {

      "command": "uvx",

      "args": ["mcp-server-github"],

      "env": {

        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token"

      },

      "disabled": false,

      "autoApprove": []

    },

    "pandas": {

      "command": "uvx",

      "args": ["mcp-pandas"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "jupyter": {

      "command": "uvx",

      "args": ["mcp-jupyter"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "neo4j": {

      "command": "uvx",

      "args": ["mcp-server-neo4j"],

      "env": {

        "NEO4J_URI": "bolt://localhost:7687",

        "NEO4J_USERNAME": "neo4j",

        "NEO4J_PASSWORD": "password"

      },

      "disabled": false,

      "autoApprove": []

    },

    "aws": {

      "command": "uvx",

      "args": ["mcp-server-aws"],

      "env": {

        "AWS_ACCESS_KEY_ID": "your_access_key",

        "AWS_SECRET_ACCESS_KEY": "your_secret_key",

        "AWS_DEFAULT_REGION": "us-west-2"

      },

      "disabled": false,

      "autoApprove": []

    },

    "gcp": {

      "command": "uvx",

      "args": ["mcp-server-gcp"],

      "env": {

        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"

      },

      "disabled": false,

      "autoApprove": []

    },

    "kubernetes": {

      "command": "uvx",

      "args": ["mcp-server-kubernetes"],

      "env": {

        "KUBECONFIG": "/path/to/kubeconfig"

      },

      "disabled": false,

      "autoApprove": []

    },

    "docker": {

      "command": "uvx",

      "args": ["mcp-server-docker"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "git": {

      "command": "uvx",

      "args": ["mcp-server-git"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "prometheus": {

      "command": "uvx",

      "args": ["mcp-server-prometheus"],

      "env": {

        "PROMETHEUS_URL": "http://localhost:9090"

      },

      "disabled": false,

      "autoApprove": []

    },

    "grafana": {

      "command": "uvx",

      "args": ["mcp-server-grafana"],

      "env": {

        "GRAFANA_URL": "http://localhost:3000",

        "GRAFANA_API_KEY": "your_api_key"

      },

      "disabled": false,

      "autoApprove": []

    },

    "mlflow": {

      "command": "uvx",

      "args": ["mcp-server-mlflow"],

      "env": {

        "MLFLOW_TRACKING_URI": "http://localhost:5000"

      },

      "disabled": false,

      "autoApprove": []

    },

    "wandb": {

      "command": "uvx",

      "args": ["mcp-server-wandb"],

      "env": {

        "WANDB_API_KEY": "your_wandb_api_key"

      },

      "disabled": false,

      "autoApprove": []

    },

    "web-search": {

      "command": "uvx",

      "args": ["mcp-server-web-search"],

      "env": {

        "GOOGLE_API_KEY": "your_google_api_key",

        "GOOGLE_CSE_ID": "your_cse_id"

      },

      "disabled": false,

      "autoApprove": []

    },

    "slack": {

      "command": "uvx",

      "args": ["mcp-server-slack"],

      "env": {

        "SLACK_BOT_TOKEN": "xoxb-your-bot-token"

      },

      "disabled": false,

      "autoApprove": []

    },

    "openapi": {

      "command": "uvx",

      "args": ["mcp-server-openapi", "https://api.example.com/openapi.json"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "notion": {

      "command": "uvx",

      "args": ["mcp-server-notion"],

      "env": {

        "NOTION_API_KEY": "your_notion_integration_token"

      },

      "disabled": false,

      "autoApprove": []

    },

    "obsidian": {

      "command": "uvx",

      "args": ["mcp-server-obsidian", "/path/to/obsidian/vault"],

      "env": {},

      "disabled": false,

      "autoApprove": []

    },

    "confluence": {

      "command": "uvx",

      "args": ["mcp-server-confluence"],

      "env": {

        "CONFLUENCE_URL": "https://your-domain.atlassian.net",

        "CONFLUENCE_USERNAME": "your_username",

        "CONFLUENCE_API_TOKEN": "your_api_token"

      },

      "disabled": false,

      "autoApprove": []

    },

    "huggingface": {

      "command": "uvx",

      "args": ["mcp-server-huggingface"],

      "env": {

        "HUGGINGFACE_API_TOKEN": "your_hf_token"

      },

      "disabled": false,

      "autoApprove": []

    },

    "openai": {

      "command": "uvx",

      "args": ["mcp-server-openai"],

      "env": {

        "OPENAI_API_KEY": "your_openai_api_key"

      },

      "disabled": false,

      "autoApprove": []

    },

    "anthropic": {

      "command": "uvx",

      "args": ["mcp-server-anthropic"],

      "env": {

        "ANTHROPIC_API_KEY": "your_anthropic_api_key"

      },

      "disabled": false,

      "autoApprove": []

    },

    "vectordb": {

      "command": "uvx",

      "args": ["mcp-server-vectordb"],

      "env": {

        "PINECONE_API_KEY": "your_pinecone_key",

        "PINECONE_ENVIRONMENT": "your_environment"

      },

      "disabled": false,

      "autoApprove": []

    }

  }

}
```

# 2. Cài docs Langchain langgraph 
```bash
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "langgraph-docs": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt",
        "LangChain:https://python.langchain.com/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

Nếu chưa có `uv`, cài trước:

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## **Bonus: Thêm Rules để Cursor tự động dùng docs**

Sau khi config xong, vào **Cursor Settings** → **Rules** → **User Rules** và thêm:

```
For ANY question about LangGraph or LangChain:
1. ALWAYS use the langgraph-docs server first
2. Call list_doc_sources tool to see available documentation
3. Use fetch_docs tool to get specific documentation
4. Reference the docs when suggesting code or fixes
```

LẠ GHÊ, CÁC CÁI KHÁC KO CẦN TẮT CURSOR, còn cái này thì cần 

Test được chưa 

Mở Cursor Chat và thử:

```
List all documentation sources available
```

```output example
I'll check all doc sources from the configured LangGraph/LangChain docs server.

[1 tool called]

### Available documentation sources

- LangGraph: `https://langchain-ai.github.io/langgraph/llms.txt`
- LangChain: `https://python.langchain.com/llms.txt`
```

Hoặc:

```
How do I create a LangGraph agent? Check the docs first.
```

---
#### Nếu vẫn bug thì check 

Bước 1: Test xem uvx có hoạt động không
```
uvx --version
```

Bước 2: Test mcpdoc
```
uvx --from mcpdoc mcpdoc --help
```

Nếu nó hiện help menu → **Thành công!** ✅

```bash
Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

PS C:\Users\User> uvx --version
uvx 0.8.22 (ade2bdbd2 2025-09-23)
PS C:\Users\User> uvx --from mcpdoc mcpdoc --help
Installed 40 packages in 393ms
usage: mcpdoc [-h] [--yaml YAML] [--json JSON] [--urls URLS [URLS ...]] [--follow-redirects]
              [--allowed-domains [ALLOWED_DOMAINS ...]] [--timeout TIMEOUT] [--transport {stdio,sse}]
              [--log-level LOG_LEVEL] [--host HOST] [--port PORT] [--version]

MCP LLMS-TXT Documentation Server

options:
  -h, --help            show this help message and exit
  --yaml, -y YAML       Path to YAML config file with doc sources (default: None)
  --json, -j JSON       Path to JSON config file with doc sources (default: None)
  --urls, -u URLS [URLS ...]
                        List of llms.txt URLs or file paths with optional names (format: 'url_or_path' or
                        'name:url_or_path') (default: None)
  --follow-redirects    Whether to follow HTTP redirects (default: False)
  --allowed-domains [ALLOWED_DOMAINS ...]
                        Additional allowed domains to fetch documentation from. Use '*' to allow all domains.
                        (default: None)
  --timeout TIMEOUT     HTTP request timeout in seconds (default: 10.0)
  --transport {stdio,sse}
                        Transport protocol for MCP server (default: stdio)
  --log-level LOG_LEVEL
                        Log level for the server. Use one on the following: DEBUG, INFO, WARNING, ERROR. (only used
                        with --transport sse) (default: INFO)
  --host HOST           Host to bind the server to (only used with --transport sse) (default: 127.0.0.1)
  --port PORT           Port to bind the server to (only used with --transport sse) (default: 8000)
  --version, -V         Show version information and exit

Examples:
  # Directly specifying llms.txt URLs with optional names
  mcpdoc --urls LangGraph:https://langchain-ai.github.io/langgraph/llms.txt

  # Using a local file (absolute or relative path)
  mcpdoc --urls LocalDocs:/path/to/llms.txt --allowed-domains '*'

  # Using a YAML config file
  mcpdoc --yaml sample_config.yaml

  # Using a JSON config file
  mcpdoc --json sample_config.json

  # Combining multiple documentation sources
  mcpdoc --yaml sample_config.yaml --json sample_config.json --urls LangGraph:https://langchain-ai.github.io/langgraph/llms.txt

  # Using SSE transport with default host (127.0.0.1) and port (8000)
  mcpdoc --yaml sample_config.yaml --transport sse

  # Using SSE transport with custom host and port
  mcpdoc --yaml sample_config.yaml --transport sse --host 0.0.0.0 --port 9000

  # Using SSE transport with additional HTTP options
  mcpdoc --yaml sample_config.yaml --follow-redirects --timeout 15 --transport sse --host localhost --port 8080

  # Allow fetching from additional domains. The domains hosting the llms.txt files are always allowed.
  mcpdoc --yaml sample_config.yaml --allowed-domains https://example.com/ https://another-example.com/

  # Allow fetching from any domain
  mcpdoc --yaml sample_config.yaml --allowed-domains '*'
PS C:\Users\User>

```


2. MCP for AI Engineer 

Dựa trên nhu cầu làm việc với Langchain, Langgraph, AI Agents, LLMs, System Design, Design Architecture, MLOps và LLMOps, đây là danh sách các MCP servers cần thiết được tổ chức theo từng lĩnh vực:

## **🤖 AI/ML Development & LLMs**

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/path/to/your/projects"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "sqlite": {
      "command": "uvx", 
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/your/database.db"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://user:password@localhost:5432/dbname"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **📊 Data & Analytics**

```json
{
  "mcpServers": {
    "pandas": {
      "command": "uvx",
      "args": ["mcp-pandas"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "jupyter": {
      "command": "uvx", 
      "args": ["mcp-jupyter"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "neo4j": {
      "command": "uvx",
      "args": ["mcp-server-neo4j"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "password"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **☁️ Cloud & Infrastructure**

```json
{
  "mcpServers": {
    "aws": {
      "command": "uvx",
      "args": ["mcp-server-aws"],
      "env": {
        "AWS_ACCESS_KEY_ID": "your_access_key",
        "AWS_SECRET_ACCESS_KEY": "your_secret_key",
        "AWS_DEFAULT_REGION": "us-west-2"
      },
      "disabled": false,
      "autoApprove": []
    },
    "gcp": {
      "command": "uvx",
      "args": ["mcp-server-gcp"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/service-account-key.json"
      },
      "disabled": false,
      "autoApprove": []
    },
    "kubernetes": {
      "command": "uvx",
      "args": ["mcp-server-kubernetes"],
      "env": {
        "KUBECONFIG": "/path/to/kubeconfig"
      },
      "disabled": false,
      "autoApprove": []
    },
    "docker": {
      "command": "uvx",
      "args": ["mcp-server-docker"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **🔧 DevOps & MLOps**

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "prometheus": {
      "command": "uvx",
      "args": ["mcp-server-prometheus"],
      "env": {
        "PROMETHEUS_URL": "http://localhost:9090"
      },
      "disabled": false,
      "autoApprove": []
    },
    "grafana": {
      "command": "uvx",
      "args": ["mcp-server-grafana"],
      "env": {
        "GRAFANA_URL": "http://localhost:3000",
        "GRAFANA_API_KEY": "your_api_key"
      },
      "disabled": false,
      "autoApprove": []
    },
    "mlflow": {
      "command": "uvx",
      "args": ["mcp-server-mlflow"],
      "env": {
        "MLFLOW_TRACKING_URI": "http://localhost:5000"
      },
      "disabled": false,
      "autoApprove": []
    },
    "wandb": {
      "command": "uvx",
      "args": ["mcp-server-wandb"],
      "env": {
        "WANDB_API_KEY": "your_wandb_api_key"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **🌐 Web & API Integration**

```json
{
  "mcpServers": {
    "web-search": {
      "command": "uvx",
      "args": ["mcp-server-web-search"],
      "env": {
        "GOOGLE_API_KEY": "your_google_api_key",
        "GOOGLE_CSE_ID": "your_cse_id"
      },
      "disabled": false,
      "autoApprove": []
    },
    "slack": {
      "command": "uvx",
      "args": ["mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token"
      },
      "disabled": false,
      "autoApprove": []
    },
    "openapi": {
      "command": "uvx",
      "args": ["mcp-server-openapi", "https://api.example.com/openapi.json"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **📝 Documentation & Knowledge Management**

```json
{
  "mcpServers": {
    "notion": {
      "command": "uvx",
      "args": ["mcp-server-notion"],
      "env": {
        "NOTION_API_KEY": "your_notion_integration_token"
      },
      "disabled": false,
      "autoApprove": []
    },
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-server-obsidian", "/path/to/obsidian/vault"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "confluence": {
      "command": "uvx",
      "args": ["mcp-server-confluence"],
      "env": {
        "CONFLUENCE_URL": "https://your-domain.atlassian.net",
        "CONFLUENCE_USERNAME": "your_username",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **🎯 Specialized AI/LLM Tools**

```json
{
  "mcpServers": {
    "huggingface": {
      "command": "uvx",
      "args": ["mcp-server-huggingface"],
      "env": {
        "HUGGINGFACE_API_TOKEN": "your_hf_token"
      },
      "disabled": false,
      "autoApprove": []
    },
    "openai": {
      "command": "uvx",
      "args": ["mcp-server-openai"],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key"
      },
      "disabled": false,
      "autoApprove": []
    },
    "anthropic": {
      "command": "uvx",
      "args": ["mcp-server-anthropic"],
      "env": {
        "ANTHROPIC_API_KEY": "your_anthropic_api_key"
      },
      "disabled": false,
      "autoApprove": []
    },
    "vectordb": {
      "command": "uvx",
      "args": ["mcp-server-vectordb"],
      "env": {
        "PINECONE_API_KEY": "your_pinecone_key",
        "PINECONE_ENVIRONMENT": "your_environment"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## **⚙️ Configuration cho từng use case cụ thể:**

### **Langchain/Langgraph Development:**
- `filesystem` (để quản lý code)
- `github` (version control)
- `jupyter` (experimentation)
- `openai/anthropic` (LLM providers)
- `vectordb` (embeddings storage)

### **AI Agents & System Design:**
- `kubernetes` (deployment)
- `docker` (containerization)
- `prometheus/grafana` (monitoring)
- `slack` (notifications)
- `notion/obsidian` (documentation)

### **MLOps/LLMOps:**
- `mlflow/wandb` (experiment tracking)
- `aws/gcp` (cloud infrastructure)
- `git` (version control)
- `postgres/sqlite` (metadata storage)

## **📋 Cách cài đặt và sử dụng:**

1. **Cài đặt uvx** (nếu chưa có):
```bash
pip install uvx
```

2. **Tạo file cấu hình** `mcp_servers.json` với các servers cần thiết

3. **Cập nhật biến môi trường** với API keys và credentials tương ứng

4. **Test kết nối** từng server để đảm bảo hoạt động đúng

5. **Tùy chỉnh `autoApprove`** cho các actions an toàn để tăng tốc workflow

**Lưu ý:** Hãy bắt đầu với một số servers cơ bản như `filesystem`, `github`, và `jupyter`, sau đó từ từ thêm các servers khác theo nhu cầu cụ thể của dự án.


# 3. Cài Exdraw 

```
    "excalidraw": {

      "command": "npx",

      "args": ["-y", "mcp-excalidraw-server"]

    },
```

Ko được, check nó no prompt
```
npx -y mcp-excalidraw-server
```

```
npx -y @fromsko/excalidraw-mcp-server
```