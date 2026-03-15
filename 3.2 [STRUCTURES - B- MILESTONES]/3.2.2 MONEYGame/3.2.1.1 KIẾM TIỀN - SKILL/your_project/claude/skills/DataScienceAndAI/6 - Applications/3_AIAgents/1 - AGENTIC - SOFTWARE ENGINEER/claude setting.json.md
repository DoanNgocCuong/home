## 1. Claude vs VSCode

+, Step 1: Cài Extention Claude Chat trong VSCode. 

vào .claude/setting.json và sửa như này nhé 

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "94FC8C41-03A9-4F95-BB7E-A3DC0B180AB1",
    "ANTHROPIC_BASE_URL": "http://zeno360.click",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-opus-4-6",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-opus-4-6",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-opus-4-6",
    "CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS": "0",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "alwaysThinkingEnabled": "true",
    "API_TIMEOUT_MS": "3000000"
  },
  "permissions": {
    "allow": [
      "Bash(*)",
      "Edit",
      "Write",
      "Read",
      "MultiEdit",
      "NotebookEdit",
      "WebFetch",
      "WebSearch",
      "TodoRead",
      "TodoWrite",
      "mcp__*"
    ],
    "deny": []
  },
  "model": "opus"
}


```



## 2. Claude CLI 

  

### 1. Cách cài “đẹp” trên Linux/Ubuntu

  

1) Chuẩn bị môi trường:

```bash

sudo apt update

sudo apt install -y git curl ripgrep

```

  

`git` và `ripgrep` giúp Claude Code hiểu project và search code nhanh hơn.[^3]

  

2) Cài bằng native installer (khuyến nghị):

```bash

curl -fsSL https://claude.ai/install.sh | bash

```

  

- Đây là cách được Anthropic và nhiều guide recommend cho macOS/Linux.[^2][^4]

- Không dùng `sudo` với lệnh này để tránh lỗi permission và bảo mật.[^5][^3]

  

3) Thêm vào PATH (chỉ cần làm 1 lần):

```bash

echo 'export PATH="$HOME/.claude/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc

source ~/.bashrc

```

  

4) Verify sau cài:

```bash

claude --version

claude doctor   # nếu có, để check sức khỏe setup

```

  

Kiểm tra được version và không lỗi là ổn.[^5]

  

### 2. Cấu hình tài khoản \& bảo mật

  

1) Đăng nhập / auth:

```bash

claude

# hoặc

claude auth login

claude auth status

```

  

Lần đầu sẽ mở trình duyệt OAuth, hoặc dùng API key theo hướng dẫn từng phiên bản.[^6][^3]

  

2) Bảo mật:

  

- Không bao giờ cài hoặc chạy bằng `sudo` (đặc biệt với npm).[^3][^5]

- Nếu dùng API key: để trong env (`ANTHROPIC_API_KEY`), file `.env` được ignore, không hard-code vào repo.[^3]

- Cấu hình ignore cho thư mục sensitive (keys, .git, data thật) qua settings và permission system.[^7][^3]