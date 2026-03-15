ko # CCPoke Setup Guide - Linux (Server)

  

## Quick Start

  

### Bước 1: Cài Claude CLI

  

```bash

curl -fsSL https://claude.ai/install.sh | bash

```

  

### Bước 2: Cài Node.js 20+ (nếu cần)

  

```bash

# Cài nvm (nếu chưa có)

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  

# Cài Node.js 20

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install 20

```

  

### Bước 3: Cài tmux

  

```bash

sudo apt update && sudo apt install tmux

```

  

### Bước 4: Tạo TMUX session với Claude CLI

  

```bash

# Tạo session mới

tmux new-session -d -s claude-session

  

# Chạy Claude CLI trong tmux (quan trọng: unset CLAUDECODE để tránh lỗi nested session)

tmux send-keys -t claude-session 'unset CLAUDECODE && export PATH=$HOME/.local/bin:$PATH && claude' C-m

```

  

### Bước 5: Chạy CCPoke

  

```bash

# Chạy CCPoke (để nó nhận diện Claude session trong tmux)

npx -y ccpoke

```

  

### Bước 6: Verify

  

```bash

# Kiểm tra sessions

curl http://localhost:9377/sessions

  

# Hoặc xem file

cat ~/.ccpoke/sessions.json

```

  

Nếu thấy session trong danh sách → Đã thành công!

  

| Hạng mục | Windows (Git Bash) | Linux |

|----------|-------------------|-------|

| Yêu cầu Node.js | ≥ 20 | ≥ 20 |

| File hook | `.sh` (Unix shell) | `.sh` (Unix shell) |

| Path format | `/c/Users/...` (Unix-style) | `/home/username/...` |

| Cần convert path | ✅ Có (do Git Bash) | ❌ Không |

| Cần tmux | ❌ Không | ✅ Có (cho 2-way chat) |

  

## Các bước setup trên Linux

  

### Bước 1: Nâng cấp Node.js (nếu cần)

  

```bash

# Cài nvm (nếu chưa có)

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

  

# Cài Node.js 20

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install 20

nvm alias default 20

```

  

### Bước 2: Cài tmux (cho 2-way chat)

  

```bash

# Ubuntu/Debian

sudo apt update && sudo apt install tmux

  

# CentOS/RHEL

sudo yum install tmux

```

  

### Bước 3: Tạo config

  

```bash

mkdir -p ~/.ccpoke

  

cat > ~/.ccpoke/config.json << 'EOF'

{

  "channel": "telegram",

  "telegram_bot_token": "YOUR_TOKEN",

  "user_id": YOUR_USER_ID,

  "hook_port": 9377,

  "hook_secret": "YOUR_SECRET",

  "locale": "en",

  "agents": ["claude-code"],

  "projects": []

}

EOF

```

  

### Bước 4: Chạy CCPoke

  

```bash

# Cách 1: Chạy trực tiếp (mỗi lần)

npx -y ccpoke

  

# Cách 2: Cài đặt toàn cục (chạy bất kỳ đâu)

npm i -g ccpoke

ccpoke

```

  

### Bước 5: Tạo hook thủ công

  

CCPoke sẽ tự tạo hook, nhưng có thể tạo thủ công nếu cần:

  

```bash

mkdir -p ~/.ccpoke/hooks

  

cat > ~/.ccpoke/hooks/claude-code-stop.sh << 'EOF'

#!/bin/bash

INPUT=$(cat | tr -d '\n\r')

echo "$INPUT" | grep -q '"session_id"' || exit 0

  

echo "$INPUT" | curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \

  -H "Content-Type: application/json" \

  -H "X-CCPoke-Secret: YOUR_SECRET" \

  --data-binary @- > /dev/null 2>&1 || true

EOF

  

chmod +x ~/.ccpoke/hooks/claude-code-stop.sh

```

  

### Bước 6: Cập nhật Claude Settings

  

```bash

# Thêm vào ~/.claude/settings.json

{

  "hooks": {

    "Stop": [{

      "hooks": [{

        "type": "command",

        "command": "/home/YOUR_USERNAME/.ccpoke/hooks/claude-code-stop.sh",

        "timeout": 10

      }]

    }]

  }

}

```

  

## Các lỗi thường gặp

  

### Lỗi: "node: command not found"

- **Nguyên nhân**: Node.js version quá cũ

- **Fix**: Nâng cấp Node.js lên version 20+

  

### Lỗi: "Conflict: terminated by other getUpdates request"

- **Nguyên nhân**: Có process CCPoke khác đang chạy

- **Fix**: Kill process cũ

```bash

pkill -f ccpoke

```

  

### Lỗi: Port 9377 bị chiếm

- **Fix**:

```bash

lsof -i :9377

kill -9 <PID>

```

  

## Commands hữu ích

  

```bash

# Kiểm tra CCPoke có đang chạy không

curl http://localhost:9377/health

  

# Xem logs

tail -f ~/.ccpoke/ccpoke.log

  

# Xem responses đã nhận

ls -la ~/.ccpoke/responses/

  

# Kill và chạy lại

pkill -f ccpoke && npx -y ccpoke

```

  

## Khác biệt chính so với Windows

  

1. **Không cần convert path**: Linux dùng Unix path trực tiếp, không cần fix như Windows + Git Bash

2. **Cần tmux**: Để dùng tính năng 2-way chat

3. **Node.js**: Phải nâng cấp từ v10 lên v20+ (v10 không tương thích với CCPoke)

  

## Security

  

Giống như Windows:

- Token lưu trong `~/.ccpoke/config.json`

- hook_secret dùng để xác thực request

- Không gửi code ra ngoài, chỉ gửi summary

  
  

---

  

## Vấn đề kỹ thuật - Root Cause Analysis

  

### Vấn đề gặp phải

CCPoke không gửi notification Telegram dù đã setup đúng.

  

### Nguyên nhân sâu xa

  

**Server Linux đang chạy Claude Opus ở 2 "tầng" khác nhau:**

  

1. **Tầng 1 - VSCode Extension** (hiện tại đang dùng):

   - Claude Opus Extension trong VSCode Remote

   - Extension này kết nối đến Claude API, KHÔNG phải Claude CLI local

   - CCPoke không nhận diện được vì không có process Claude CLI local

  

2. **Tầng 2 - Claude CLI** (cần cài thêm):

   - Claude CLI thực sự (`~/.local/bin/claude`)

   - CCPoke cần process này để track session

  

### Cơ chế vận hành của CCPoke

  

```

┌─────────────────────────────────────────────────────────────────┐

│                        CCPoke Flow                               │

├─────────────────────────────────────────────────────────────────┤

│                                                                  │

│  1. Claude CLI chạy trong tmux                                  │

│     ↓                                                            │

│  2. CCPoke scan tmux sessions → tìm thấy "claude-session"      │

│     ↓                                                            │

│  3. Lưu vào sessions.json:                                       │

│     { "sessionId": "xxx", "tmuxTarget": "claude-session:0.0" }  │

│     ↓                                                            │

│  4. Khi Claude Stop → gọi hook /hook/stop                      │

│     ↓                                                            │

│  5. CCPoke gửi notification đến Telegram                       │

│                                                                  │

└─────────────────────────────────────────────────────────────────┘

```

  

**Điều kiện bắt buộc:** CCPoke phải nhìn thấy Claude CLI process trong tmux

  

### Tại sao Windows vẫn hoạt động?

  

| Yếu tố | Windows | Linux Server |

|--------|---------|---------------|

| Claude CLI | Thường đã cài sẵn khi dùng VSCode | Chưa cài |

| Terminal | Git Bash + Claude Opus Extension | VSCode Remote |

| Session detection | Extension tự detect CLI | Cần tmux + CLI riêng |

  

**Windows** thường đã cài Claude CLI khi setup VSCode + Extension, nên CCPoke nhận diện được.

  

**Linux Server** (như server này) đang chạy VSCode Remote - Extension kết nối API bên ngoài, không có local CLI → CCPoke không thấy session.

  

### Hai giai đoạn hoạt động

  

**Giai đoạn 1: Chỉ cài Claude CLI (không chạy trong tmux)**

  

```

VSCode Extension chat → Claude CLI (đã cài nhưng không chạy) →

→ Telegram nhận được notification (1-way) ✅

→ Telegram reply → Linux không nhận được ❌

```

  

**Giai đoạn 2: Claude CLI chạy trong tmux**

  

```

VSCode Extension chat → Claude CLI → CCPoke → Telegram nhận notification (1-way) ✅

Telegram reply → Linux nhận được → Claude CLI xử lý → Response về Telegram (2-way) ✅

```

  

### Tại sao cần cả 2?

  

| Giai đoạn | Cài Claude CLI | Chạy trong tmux | 1-way (Notification) | 2-way (Chat) |

|-----------|----------------|-----------------|---------------------|--------------|

| 1 | ✅ | ❌ | ✅ | ❌ |

| 2 | ✅ | ✅ | ✅ | ✅ |

  

**Lý do:**

- Cài Claude CLI → Extension gọi được CLI → CCPoke nhận signal → Telegram notification

- Chạy trong tmux → Tạo session active → CCPoke có thể gửi message ngược lại

  

### Lưu ý về Windows

- Windows đang có bug ở tính năng 2-way (Telegram → Windows)

- Dev đang fix, nên chỉ hoạt động 1-way

  

## Lỗi thường gặp

  

### Lỗi: "Claude Opus cannot be launched inside another Claude Opus session"

- **Nguyên nhân**: Đang chạy Claude trong VSCode Extension rồi, CLI trong tmux bị conflict

- **Fix**: Tắt VSCode Extension hoặc dùng:

  ```bash

  unset CLAUDECODE && export PATH=$HOME/.local/bin:$PATH && claude

  ```

  

### Lỗi: "node: command not found"

- **Nguyên nhân**: Node.js version quá cũ

- **Fix**: Nâng cấp Node.js lên version 20+

  

### Lỗi: Sessions trống

- **Nguyên nhân**: CCPoke không nhận diện được Claude session

- **Fix**: Đảm bảo Claude CLI chạy trong tmux TRƯỚC KHI chạy CCPoke







---


Nhận được rùi bro ạ, ra là phải cài Claude CLI bằng : ```bash curl -fsSL https://claude.ai/install.sh | bash ``` Xong cho con CCpokemon này chạy trên tmux thì mới được. Còn lúc nãy lỗi là do chạy trên Claude Code Extension trong VSCode (chọc vào .claude/setting.json)


---

Đúng rồi! Claude Opus extension trong VSCode hoạt động độc lập với Claude CLI. So sánh: Component Kết nối qua Cách config Claude Opus Extension (trong VSCode) Settings.json ~/.claude/settings.json hoặc VSCode settings Claude CLI (command line) CLI binary claude auth Trong settings.json của bạn: { "env": { "ANTHROPIC_AUTH_TOKEN": "94FC8C8...", "ANTHROPIC_BASE_URL": "http://zeno360.click", ... } } → Extension đang dùng custom auth token và base URL (có vẻ là proxy/custom endpoint). Còn CCPoke kết nối với: Claude Opus (chạy qua extension hoặc CLI) → thông qua hooks trong settings.json Telegram Bot → qua API Nên: Extension connect trực tiếp với API (qua settings.json) CCPoke connect với extension thông qua hook system Bạn có muốn tìm hiểu thêm về cách này không? === 1. Mình để ý thấy là: khi linux server chưa cài claude cli thì khi mình chat trên extension thì Telegram ko nhận được. Sau khi mình cài Claude CLI thì : Claude chat vs code nó tương tác với claude CLI -> tiếp tục tương tác lan đến CCPokmon và Telegram nhận được outptu cuối (giống hệt trên local window) nhưng đều ko tương tác lại được gì cả. 2. Cho đến khi cài Claude CLI trên Linux, lúc này tmux bật lên và dùng claude CLI chính thức thì mới tương tác được từ phía Telegram ngược lại Linux (window thì bị lỗi này bên phát triển họ đang fix ý bro).


---

```
# Upgrade Node qua nvm (đã có sẵn trên máy)
nvm install 20
nvm use 20
nvm alias default 20

# Verify
node -v   # → v20.x.x

# Cài lại
npm i -g ccpoke
ccpoke
```


# NHỜ CHẠY LẠI THEO DOCS GỐC + FIX VẤN ĐỀ NODEJS 20+ VÀ THEO DÕI LOG KHI CHẠY THEO DOCS (THAY VÌ ĐỂ AI CLAUDE CLI TỰ THEO DÕI) + COPY LOG ĐÓ VÀO CLAUDE DESKTOP VÀ NÓ ĐÃ DỰ ĐOÁN RA VIỆC PHẢI CHECK LOG TRONG : tmux attach -t claude-session => CÁI NÀY ĐƯỢC CHECK 1 CÁI LÀ RA LỖI LUÔN RỒI. Thế mà cái thằng kia: cái thằng Claude CLI lậu lại ko tìm được. Chắc context length bị đầy 100% nên lag rồi.


![](image/Pasted%20image%2020260307013945.png)


```bash
# Xem tmux sessions hiện tại 
tmux ls 
# Attach vào xem bên trong có gì 
tmux attach -t claude-session
```


Thấy lỗi rồi — góc dưới phải:

> **Error: Claude Code cannot be launched inside another Claude Code session.** Nested sessions share runtime resources and will crash all active sessions.

ccpoke tạo pane mới trong tmux nhưng environment variable `CLAUDECODE` đã được set từ session cũ → Claude Code từ chối launch vì nghĩ đang bị nest.

**Fix:**

Thêm vào `~/.bashrc` hoặc `~/.zshrc` để tmux pane mới không kế thừa biến đó:

```bash
# Cho phép ccpoke tạo session mới trong tmux
unset CLAUDECODE
```

Hoặc fix nhanh ngay lập tức:

```bash
# Kill hết session cũ
tmux kill-session -t claude-session

# Unset biến
unset CLAUDECODE

# Khởi động lại ccpoke
ccpoke
```

Sau đó vào Telegram gửi `/projects` → chọn project → lúc này Claude Code sẽ launch được trong pane mới vì không còn biến `CLAUDECODE` conflict.


---
Giải thích đơn giản:

Bạn đang **chạy Claude Code sẵn** trong tmux `claude-session`. Khi ccpoke tạo pane mới từ Telegram, pane đó **kế thừa biến môi trường** `CLAUDECODE` từ session cũ. Claude Code thấy biến này → nghĩ bạn đang mở Claude Code lồng trong Claude Code → **từ chối khởi động** để tránh crash.

**Fix đơn giản — chạy 2 lệnh:**

```bash
# Bước 1: thêm dòng này vào bashrc để lần sau không bị nữa
echo 'unset CLAUDECODE' >> ~/.bashrc

# Bước 2: apply ngay
source ~/.bashrc
```

Sau đó restart ccpoke, vào Telegram tạo lại session từ `/projects` là được.


---
`~/.bashrc` là file cấu hình của terminal. Mỗi lần bạn mở terminal mới, Linux tự động chạy các lệnh trong file này.

Thêm `unset CLAUDECODE` vào đó nghĩa là: **mỗi lần mở terminal mới, tự động xóa biến `CLAUDECODE`** → Claude Code không còn nghĩ bị nest nữa.

Chạy 2 lệnh này là xong:

```bash
echo 'unset CLAUDECODE' >> ~/.bashrc
source ~/.bashrc
```

Rồi restart ccpoke và thử lại từ Telegram.


---

```bash
d [ubuntu@mgc-dev2-3090:~/.ccpoke] $ kill $(lsof -ti:9377)  
7d [ubuntu@mgc-dev2-3090:~/.ccpoke] $ ccpoke
[3/7/2026, 1:34:47 AM] tmux: found 1 Claude Code session(s)
[3/7/2026, 1:34:47 AM] 📱 2-way chat: enabled
[3/7/2026, 1:34:47 AM] hook server listening on localhost:9377
[3/7/2026, 1:34:47 AM] ccpoke: started (hook port: 9377)
[3/7/2026, 1:34:47 AM] installing cloudflared binary...
[3/7/2026, 1:34:50 AM] cloudflared binary installed
[3/7/2026, 1:34:55 AM] 🌐 public URL: https://substitute-whose-hiring-communicate.trycloudflare.com
[3/7/2026, 1:34:56 AM] commands registered
[3/7/2026, 1:34:56 AM] commands menu button registered
[3/7/2026, 1:34:56 AM] telegram bot started
[3/7/2026, 1:35:37 AM] [Projects] started claude-code in claude-session:0.6 for robot-lesson-workflow
[3/7/2026, 1:35:55 AM] [Projects] started claude-code in claude-session:0.7 for robot-lesson-workflow
[3/7/2026, 1:38:25 AM] session linked: dec92e02-a314-4f38-bfda-beb0a9a69a6d (robot-parents-lesson-builder)
[3/7/2026, 1:39:24 AM] session linked by tmux_target: dec92e02-a314-4f38-bfda-beb0a9a69a6d (claude-session:0.0)
[3/7/2026, 1:42:40 AM] [Projects] started claude-code in claude-session:0.8 for robot-parents-lesson-builder
[3/7/2026, 1:42:47 AM] Session discovered: claude-session:0.8 (robot-parents-lesson-builder)
[3/7/2026, 1:42:47 AM] Scan: 2 active, +1 new, -0 removed


```

---


  

[

Search

](https://www.perplexity.ai/)[

Computer

](https://www.perplexity.ai/computer/tasks)

[

](https://www.perplexity.ai/library)[

](https://www.perplexity.ai/discover)[

](https://www.perplexity.ai/spaces)[

](https://www.perplexity.ai/finance)

[View All](https://www.perplexity.ai/library)

# 

)* ± claude --dangerously-skip-permissions │ev2-3090:~/cuong_dn/Continuous_Traning_Pipeline]└2 <usr Error: Claude Code cannot be launched inside another Claude Code session. │> maste4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Continuous_T Nested sessions share runtime resources and will crash all active sessions. │raning_Pipeline]└4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Co To bypass this check, unset the CLAUDECODE environment variable. │ntinuous_Traning_Pipeline]└2 <usr> m4d [ubuntu@mgc-dev2 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/robo4d [ubuntu@mgc-dev2-3090:~/cuong_dn/robo4d [ubu│-3090:~/cuong_dn/Continuous_Traning_Pipeline]└2 <usr> m ntu@mgc-dev2-3090:~/cuong_dn/robot-parents-lesson-builder]└2 <usr> ma4d [ubuntu@mgc-dev│4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Continuous_Traning_ 2-3090:~/cuong_dn/robot-parents-lesson-builder]└2 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/4│4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Continuous_Traning_ 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-parents-lesson-builder]└2 <usr> main(+ │Pipeline]└2 <usr> master 0/-8567)* 1 ± │1 ± ───────────────────────────────────────────────┬───────────────────────────────────────┴───────┬─────────────────────────────────────────────── l crash all active sessions. │ronment variable. │l crash all active sessions. To bypass this check, unset the CLAUDECODE envi│4d [ubuntu@mgc-dev2-3090:~/cuong_dn/rob4d [ubun│To bypass this check, unset the CLAUDECODE envi ronment variable. │tu@mgc-dev2-3090:~/cuong_dn/robot-lesson-workfl│ronment variable. 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont │ow]└2 <usr4d [ubuntu@mgc-dev2-3090:~/cuong_dn/r│7d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont │obot-lesson-workflo4d [ubuntu@mgc-dev2-3090:~/c│7d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont │uong_dn/robot-lesson-workflow]└2 <usr> main(+14│7d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont 4d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont │4d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesso│7d [ubuntu@mgc-dev2-3090:~/cuong_dn/Cont inuous_Traning_Pipeline]└2 <usr> master │n-workflow]└2 <usr> main(+147/-89 │inuous_Traning_Pipeline]└2 <usr> master 1 ± │)+* 1 ± │1 ± ───────────────────────────────────────────────┼───────────────────────────────────────────────┼─────────────────────────────────────────────── To bypass this check, unset the CLAUDECODE envi│ronment variable. │ en/security ronment variable. │7d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesso│ 7d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesso│n-work │ ❯ 1. No, exit n-wor7d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-│flow]└2 <usr> main(+147/-89)+* 1 ± ^C │ 2. Yes, I accept lesson-workflo7d [ubuntu@mgc-dev2-3090:~/cuong_│ │ dn/robot-lesson-wor7d [ubuntu@mgc-dev2-3090:~/c│^C │ Enter to confirm · Esc to uong_dn/robot-lesson-workflow]└2 <usr> main(+14│7d [ubuntu@mgc-dev2-3090:~/cuong7d [ubuntu@mgc-│ cancel 7d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesso│7d [ubuntu@mgc-dev2-3090:~/cuong_dn/robot-lesso│7d [ubuntu@mgc-dev2-3090:~/cuong_ n-workflow]└2 <usr> main(+147/-89 │n-workflow]└2 < │dn/robot-parents-lesson-builder]└ )+* 1 ± │usr> main(+147/-89)+* ± │2 <usr> main(+0/-8567)* 20s 1 ± [claude-se0:bash* "" 21:04 07-Mar-26

Bạn đang gặp lỗi **"Claude Code cannot be launched inside another Claude Code session"** vì Claude Code tự set biến môi trường `CLAUDECODE=1`, và các pane tmux con kế thừa biến này, khiến session mới bị block.

## Nguyên nhân

Khi Claude Code chạy, nó set `CLAUDECODE=1` trong môi trường shell hiện tại. Tất cả các pane tmux được mở từ session đó đều **kế thừa** biến này, nên khi bạn cố chạy `claude` ở pane khác, nó detect nested session và từ chối khởi động.

## Cách Fix

**Fix nhanh — unset biến trước khi chạy:**

bash

`unset CLAUDECODE && claude --dangerously-skip-permissions`

**Fix cho từng pane tmux mới:**

bash

`# Tạo alias tiện lợi alias claude-new='unset CLAUDECODE && claude'`

**Fix vĩnh viễn trong `.bashrc` hoặc `.zshrc`:**

bash

`# Không để CLAUDECODE kế thừa sang shell mới unset CLAUDECODE`

## Multi-Agent Approach (Khuyến nghị)

Thay vì chạy nested, Claude Code có tính năng **Experimental Agent Teams** cho phép orchestrate nhiều session hợp lệ:[](https://code.claude.com/docs/en/agent-teams)​

bash

`# Trong ~/.claude/settings.json {   "env": {    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"  } }`

Hoặc export trực tiếp:

bash

`export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude --dangerously-skip-permissions`

## Quản lý nhiều dự án trong tmux

Nhìn vào terminal của bạn, bạn đang chạy song song `Continuous_Traning_Pipeline`, `robot-parents-lesson-builder`, và `robot-lesson-workflow`. Cách tốt nhất là mỗi dự án chạy trong **tmux window riêng biệt** (không phải pane con từ session đang có Claude):[](https://code.claude.com/docs/en/agent-teams)​

bash

`# Mở window tmux hoàn toàn mới (không kế thừa env) tmux new-window # Rồi mới chạy claude`

Điều này đảm bảo mỗi window có môi trường shell sạch, không mang `CLAUDECODE` từ session cha.

Prepared using Claude Sonnet 4.6 Thinking

ướng dẫn cài đặt ccpoke — Telegram Notification cho Claude Code ccpoke là cầu nối 2 chiều giữa AI agent (Claude Code, Codex CLI, Cursor CLI) và Telegram. Nhận thông báo khi Claude Code trả lời xong, gửi yêu cầu, quản lý nhiều phiên làm việc — tất cả từ điện thoại. Repo: https://github.com/kaida-palooza/ccpoke Yêu cầu Node.js ≥ 20 tmux (cần cho tương tác 2 chiều) Telegram Bot Token (tạo từ @BotFather) Bước 1: Upgrade Node.js ccpoke yêu cầu Node ≥ 20. Nếu đang dùng Node cũ (ví dụ v16), cần upgrade qua nvm: nvm install 20 nvm use 20 nvm alias default 20 node -v # Xác nhận → v20.x.x Nếu không upgrade, sẽ gặp lỗi better-sqlite3 build fail (g++ không hỗ trợ -std=c++20) và node:util thiếu export styleText. Bước 2: Cài đặt ccpoke npm i -g ccpoke Các warning deprecated (har-validator, prebuild-install, uuid, request) là từ dependency cũ, không ảnh hưởng. Bước 3: Chạy setup lần đầu ccpoke Trình hướng dẫn sẽ yêu cầu: Chọn ngôn ngữ Nhập Telegram Bot Token (lấy từ @BotFather) Quét QR hoặc mở link để kết nối bot Gửi /start tới bot trên Telegram Chọn AI agents (Claude Code, Codex CLI, Cursor CLI) Bước 4: Fix lỗi "Cannot be launched inside another Claude Code session" Nếu ccpoke tạo session từ Telegram nhưng Claude Code báo lỗi: Error: Claude Code cannot be launched inside another Claude Code session. Nguyên nhân: biến môi trường CLAUDECODE bị kế thừa từ session cũ. Fix: echo 'unset CLAUDECODE' >> ~/.bashrc source ~/.bashrc Bước 5: Accept Terms (1 lần duy nhất) Nếu session mới bị kẹt ở prompt "Yes, I accept", cần accept terms 1 lần trong terminal thường: cd ~/path/to/your/project claude # Chọn "2. Yes, I accept" → Enter # Sau đó thoát: /exit hoặc Ctrl+C Sau khi accept, các session mới từ Telegram sẽ không hỏi lại. Bước 6: Chạy ccpoke ngầm trong tmux Nếu chạy ccpoke trực tiếp, Ctrl+C sẽ tắt luôn. Để chạy ngầm: # Tạo session riêng cho ccpoke tmux new -s ccpoke -d 'ccpoke' Các lệnh quản lý: # Xem log tmux attach -t ccpoke # Thoát ra mà không tắt (detach) # Nhấn: Ctrl+B rồi D # Restart ccpoke tmux kill-session -t ccpoke tmux new -s ccpoke -d 'ccpoke' Bước 7: Đăng ký project ccpoke project Chọn "Thêm dự án mới" → nhập đường dẫn và tên project. Sau đó vào Telegram gửi /projects → chọn project → chọn agent → session Claude Code tự khởi chạy trong tmux pane mới. Lệnh Telegram LệnhChức năng /start Đăng ký lại cuộc trò chuyện /sessions Xem danh sách phiên đang hoạt động /projects Xem danh sách dự án và mở phiên mới Xem phiên làm việc # Attach vào tmux session của ccpoke tmux attach -t ccpoke # Hoặc nếu dùng iTerm2 tmux -CC attach Mỗi pane trong tmux là 1 session Claude Code cho 1 project. Di chuyển giữa các pane bằng Ctrl+B rồi phím mũi tên. Gỡ cài đặt ccpoke uninstall Troubleshooting Vấn đềNguyên nhânGiải pháp npm ERR! better-sqlite3 build fail Node < 20 hoặc g++ cũ nvm install 20 && nvm use 20 styleText not exported Node < 20 Upgrade Node ≥ 20 "Cannot be launched inside another Claude Code session" Biến CLAUDECODE kế thừa echo 'unset CLAUDECODE' >> ~/.bashrc && source ~/.bashrc Session kẹt ở "Yes, I accept" Chưa accept terms Chạy claude trong terminal, accept 1 lần Ctrl+C tắt ccpoke Chạy foreground Dùng tmux new -s ccpoke -d 'ccpoke' "failed to register commands" Lỗi mạng tạm thời Restart ccpoke "callback_query too old" Callback cũ còn sót Vô hại, bỏ qua Ghi chú Server: mgc-dev2-3090 (Ubuntu, nvm) Node version: v20.20.1 ccpoke version: 1.6.27 Ngày cài đặt: 2026-03-07 === NÃY MÌNH ĐÃ FIX LỖI NÀY RỒI MÀ NHỈ , (mình còn note lại đây nè)

Đúng rồi! 🎯 Bạn đã tự fix và document lại rất rõ ràng luôn.

Nhìn lại flow của cuộc hội thoại:

1. **Terminal screenshot trước** → bạn đang gặp lỗi `Claude Code cannot be launched inside another Claude Code session` live trên server `mgc-dev2-3090`
    
2. **Note ccpoke của bạn** → **Bước 4** đã ghi đúng fix:
    
    bash
    
    `echo 'unset CLAUDECODE' >> ~/.bashrc source ~/.bashrc`
    
3. **Câu trả lời mình vừa đưa** → cũng khớp với fix đó (`unset CLAUDECODE`)
    

Vậy là lúc nãy bạn có thể đang thao tác trực tiếp trên server và quên mất rằng bước fix đã được note sẵn trong doc ccpoke rồi 😄

Note của bạn về ccpoke khá đầy đủ và production-ready — đặc biệt phần **Troubleshooting table** và flow **tmux + ccpoke background** rất thực tế cho môi trường multi-project như `Continuous_Traning_Pipeline`, `robot-parents-lesson-builder`, `robot-lesson-workflow` bạn đang chạy song song.

Prepared using Claude Sonnet 4.6 Thinking

đây là trên linux bro ạ

Ah đúng rồi! Mình để ý trong note ccpoke của bạn có dòng này:

bash

`# Hoặc nếu dùng iTerm2 tmux -CC attach`

**iTerm2 là macOS only** — trên Linux server `mgc-dev2-3090` (Ubuntu) thì bỏ qua dòng đó, chỉ dùng:

bash

`tmux attach -t ccpoke`

Ngoài ra mọi thứ khác trong note vẫn đúng hoàn toàn cho Linux/Ubuntu. Bạn muốn update lại note để bỏ phần iTerm2 đi cho khỏi nhầm sau này không?

Prepared using Claude Sonnet 4.6 Thinking

Mình hỏi chút, bạn đọc kỹ : https://github.com/kaida-palooza/ccpoke xem repo này hướng dẫn gì về việc chạy song song. tại sao khi chạy khởi tạo 1 project mới xong rồi tạo session mới trên telegram thì nó lại phải xác thực trong claude. ko để mặc định auto accept được à

Đọc kỹ source code xong, đây là phân tích thực tế:

## ccpoke không hỗ trợ auto-accept permissions

Nhìn vào `claude-code-provider.ts`, ccpoke chỉ xử lý **phía nhận event** (Stop Hook → Telegram notification). Phần **launch session từ Telegram** (`/projects`) chỉ đơn giản spawn `claude` trong tmux pane mới — **không có cơ chế pass `--dangerously-skip-permissions`** hay bất kỳ flag nào vào lệnh claude.[](https://github.com/anthropics/claude-agent-sdk-python/issues/573)​

## Tại sao vẫn bị hỏi xác thực?

Có 2 loại prompt khác nhau:

|Prompt|Trigger|Fix|
|---|---|---|
|**ToS acceptance** ("Yes, I accept")|Lần đầu tiên trên máy|Accept 1 lần trong terminal → lưu vào `~/.claude/` → không hỏi lại|
|**Permission prompts** (approve actions)|Mỗi khi Claude muốn edit file, run command...|Cần `--dangerously-skip-permissions`|

Bạn nói "xác thực trong claude" — khả năng cao là **permission prompts**, không phải ToS. ToS chỉ hỏi đúng 1 lần rồi thôi.

## Workaround: Wrapper script

Vì ccpoke gọi `claude` trực tiếp từ PATH, bạn có thể tạo wrapper ghi đè:

bash

`# Tạo wrapper script sudo nano /usr/local/bin/claude #!/bin/bash unset CLAUDECODE exec /path/to/real/claude --dangerously-skip-permissions "$@" # Phân quyền sudo chmod +x /usr/local/bin/claude # Verify which claude  # phải trỏ vào wrapper trước`

Kiểm tra path claude thật:

bash

`npm root -g  # tìm path npm global # thường là: /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude`

Ví dụ hoàn chỉnh:

bash

`cat > ~/.local/bin/claude << 'EOF' #!/bin/bash unset CLAUDECODE exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" EOF chmod +x ~/.local/bin/claude # Đảm bảo ~/.local/bin đứng trước trong PATH echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc source ~/.bashrc`

Như vậy mọi lần ccpoke launch `claude` từ Telegram đều tự động có `--dangerously-skip-permissions` mà không cần sửa source code ccpoke.[](https://github.com/anthropics/claude-code/issues/25803)​

Prepared using Claude Sonnet 4.6 Thinking

8d [ubuntu@mgc-dev2-3090:~] $ cat > ~/.local/bin/claude << 'EOF' > #!/bin/bash > unset CLAUDECODE > exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" > EOF bash: /home/ubuntu/.local/bin/claude: Text file busy 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ chmod +x ~/.local/bin/claude 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ # Đảm bảo ~/.local/bin đứng trước trong PATH 9d [ubuntu@mgc-dev2-3090:~] $ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 9d [ubuntu@mgc-dev2-3090:~] $ source ~/.bashrc 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $

Lỗi `Text file busy` nghĩa là file `~/.local/bin/claude` đang được **một process đang chạy dùng**. Không thể ghi đè file executable đang chạy trực tiếp.

## Fix: Dùng temp file rồi mv

`mv` là atomic — không bị lỗi text file busy:

bash

`# Ghi vào file tạm trước cat > /tmp/claude-wrapper << 'EOF' #!/bin/bash unset CLAUDECODE exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" EOF chmod +x /tmp/claude-wrapper # Atomic replace mv /tmp/claude-wrapper ~/.local/bin/claude`

## Verify

bash

`# Kiểm tra nội dung wrapper đúng chưa cat ~/.local/bin/claude # Kiểm tra PATH ưu tiên đúng chưa which claude # Phải ra: /home/ubuntu/.local/bin/claude # Test thử claude --version`

Nếu `which claude` vẫn trỏ vào path cũ thì cần:

bash

`source ~/.bashrc # hoặc mở tmux pane mới để PATH reload`

Prepared using Claude Sonnet 4.6 Thinking

8d [ubuntu@mgc-dev2-3090:~] $ cat > ~/.local/bin/claude << 'EOF' > #!/bin/bash > unset CLAUDECODE > exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" > EOF bash: /home/ubuntu/.local/bin/claude: Text file busy 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ chmod +x ~/.local/bin/claude 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ # Đảm bảo ~/.local/bin đứng trước trong PATH 9d [ubuntu@mgc-dev2-3090:~] $ echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 9d [ubuntu@mgc-dev2-3090:~] $ source ~/.bashrc 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ # Ghi vào file tạm trước 9d [ubuntu@mgc-dev2-3090:~] $ cat > /tmp/claude-wrapper << 'EOF' > #!/bin/bash > unset CLAUDECODE > exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" > EOF 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ chmod +x /tmp/claude-wrapper 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ # Atomic replace 9d [ubuntu@mgc-dev2-3090:~] $ mv /tmp/claude-wrapper ~/.local/bin/claude 9d [ubuntu@mgc-dev2-3090:~] $ 9d [ubuntu@mgc-dev2-3090:~] $ cat ~/.local/bin/claude #!/bin/bash unset CLAUDECODE exec /home/ubuntu/.nvm/versions/node/v20.20.1/bin/claude --dangerously-skip-permissions "$@" 9d [ubuntu@mgc-dev2-3090:~] $ which claude /home/ubuntu/.local/bin/claude 9d [ubuntu@mgc-dev2-3090:~] $ claude --version 2.1.70 (Claude Code) 9d [ubuntu@mgc-dev2-3090:~] $

✅ **Hoàn thành!** Mọi thứ đều đúng:

- `cat ~/.local/bin/claude` → nội dung wrapper chính xác
    
- `which claude` → `/home/ubuntu/.local/bin/claude` (wrapper được ưu tiên)
    
- `claude --version` → `2.1.70` chạy được bình thường
    

Từ giờ mỗi khi ccpoke launch Claude từ Telegram, nó sẽ gọi wrapper này → tự động `unset CLAUDECODE` + `--dangerously-skip-permissions` → **không còn bị kẹt permission prompt nữa**.

Bước tiếp theo là test thực tế: vào Telegram → `/projects` → chọn project → tạo session mới, xem có còn bị hỏi xác thực không nhé.

Prepared using Claude Sonnet 4.6 Thinking