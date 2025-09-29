
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

# 2. MCP for AI Engineer 

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