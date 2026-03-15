# CCPoke Setup Guide - Chi tiết

## Overview

**CCPoke** kết nối AI coding agents (Claude Opus, Codex CLI, Cursor CLI) với Telegram để nhận notification khi agent hoàn thành công việc.

### Tại sao cần CCPoke?

- **Không ngồi máy tính** mà vẫn biết khi nào AI code xong
- **Ra ngoài** mà vẫn nhận notification về bug production cần fix gấp
- **Miễn phí** - không tốn thêm token, không cần server

---

## Tính năng theo Platform

| Tính năng | Windows | macOS/Linux |
|-----------|---------|-------------|
| 🔔 Notification | ✅ | ✅ |
| 💬 2-way Chat | ❌ (cần tmux) | ✅ |
| 🔀 Multi-session | ✅ (chỉ xem) | ✅ |

---

## Cách hoạt động (Technical Flow)

### Luồng dữ liệu khi Claude Opus xong việc

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Claude Opus    │────▶│   CCPoke         │────▶│    Telegram     │
│  (local)       │hook │  (localhost:9377)│ API │    Bot API      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Chi tiết từng bước:

**Bước 1: Claude Opus hoàn thành task**
- User gõ prompt → Claude Opus xử lý → xong
- Lúc này Claude Opus trigger "Stop hook"

**Bước 2: Hook script được gọi**
- File `.sh` được execute:
```bash
#!/bin/bash
curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \
  -H "Content-Type: application/json" \
  -H "X-CCPoke-Secret: ebf4a4c6..." \
  --data-binary @-
```
- Script gửi HTTP POST đến `localhost:9377/hook/stop`
- Kèm theo data: session_id, response summary, git changes,...

**Bước 3: CCPoke nhận request**
- CCPoke đang chạy ở `localhost:9377`
- Nhận POST request từ hook
- Validate `X-CCPoke-Secret` để đảm bảo request hợp lệ
- Lưu response vào `~/.ccpoke/responses/`

**Bước 4: CCPoke gửi notification đến Telegram**
- CCPoke gọi Telegram Bot API:
```
POST https://api.telegram.org/bot<TOKEN>/sendMessage
```
- Body:
```json
{
  "chat_id": "2112467721",
  "text": "🤖 Claude Opus Response\n📂 project | ⏱ 45s\n\nFixed bug in login..."
}
```

**Bước 5: User nhận notification**
- Tin nhắn hiện trên Telegram app
- Hiển thị: agent name, project, thời gian, summary

### Các loại Hook

| Hook | Khi nào được gọi |
|------|------------------|
| `Stop` | Khi agent hoàn thành response |
| `SessionStart` | Khi bắt đầu session mới |
| `Notification` | Khi có notification |
| `PreToolUse` | Trước khi dùng tool |
| `PermissionRequest` | Khi cần xin permission |

### HTTP Request details

**Từ Claude Opus → CCPoke:**
- Method: `POST`
- URL: `http://localhost:9377/hook/stop?agent=claude-code`
- Headers:
  - `Content-Type: application/json`
  - `X-CCPoke-Secret: <secret>`
- Body: JSON chứa response data

**Từ CCPoke → Telegram:**
- Method: `POST`
- URL: `https://api.telegram.org/bot<TOKEN>/sendMessage`
- Body: `chat_id` + `text`

---

## Hướng dẫn chi tiết từng bước

### Bước 1: Lấy Telegram Bot Token

**Để làm gì?**
- Telegram Bot Token là "chìa khóa" để CCPoke gửi tin nhắn đến Telegram của bạn
- Không có token = không thể gửi notification

**Cách làm:**
1. Mở Telegram → tìm **@BotFather**
2. Gửi `/newbot`
3. Đặt tên bot (ví dụ: `MyCodeBot`)
4. BotFather trả token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

**Không làm sao?**
- Không thể gửi tin nhắn đến Telegram
- CCPoke sẽ báo lỗi khi chạy

---

### Bước 2: Lấy Telegram User ID

**Để làm gì?**
- User ID xác định **ai** sẽ nhận notification
- Bot gửi tin nhắn đến đúng người, không phải tất cả mọi người

**Cách 1: Dùng @userinfobot**
- Mở Telegram → tìm **@userinfobot** → gửi /start → lấy ID

**Cách 2: Dùng API (dùng khi không mở được Telegram app)**

```bash
# Gửi tin nhắn cho bot trước (từ Telegram app trên điện thoại)
# Sau đó chạy:
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates"
```

Kết quả:
```json
{"ok":true,"result":[{"update_id":113158155,"message":{"from":{"id":2112467721,"first_name":"Đoàn Ngọc Cường",...
```

Lấy giá trị `id`: `2112467721`

**Tại sao cần cách 2?**
- Nhiều khi không mở được Telegram app (quên đăng nhập, app lỗi,...)
- API method không cần mở app, chỉ cần token

**Lỗi có thể gặp:**
- `Conflict: terminated by other getUpdates request` → Do CCPoke đang chạy và giữ connection. Fix: Kill node processes trước khi gọi API

**Không làm sao?**
- `user_id` sẽ = 0
- CCPoke không biết gửi notification cho ai
- Bot sẽ không gửi được tin nhắn

---

### Bước 3: Tạo Config

**Để làm gì?**
- Config lưu trữ tất cả thông tin cần thiết: token, user_id, port, secret
- Khi CCPoke chạy, nó sẽ đọc config này để hoạt động

**Cách làm:**

Tạo file: `C:\Users\{username}\.ccpoke\config.json`

```json
{
  "channel": "telegram",
  "telegram_bot_token": "8627061191:AAErtOZUVrda5Q6GUR4zQNIXV0DtDDh-75k",
  "user_id": 2112467721,
  "hook_port": 9377,
  "hook_secret": "ebf4a4c6a737caafe50f7fc4f18241a51c145e96f8971de9e2e663f20d035386",
  "locale": "en",
  "agents": ["claude-code"],
  "projects": []
}
```

**Giải thích từng trường:**

| Trường | Ý nghĩa | Tại sao cần |
|---------|----------|--------------|
| `channel` | Nền tảng gửi tin | Telegram/Discord/Slack |
| `telegram_bot_token` | Token từ BotFather | Để gửi tin nhắn |
| `user_id` | ID người nhận | Xác định ai nhận tin |
| `hook_port` | Cổng chờ hook | Mặc định 9377 |
| `hook_secret` | Mật khẩu bảo mật | Đảm bảo chỉ Claude Opus mới gọi được |
| `locale` | Ngôn ngữ | en/vi/zh |
| `agents` | Agent nào được dùng | claude-code/codex/cursor |

**Lưu ý quan trọng:**
- `user_id` phải là **số** (không phải string)
- `hook_secret` sẽ được tạo tự động khi chạy lần đầu

**Không làm sao?**
- CCPoke không biết dùng token nào, gửi cho ai
- Sẽ phải chạy interactive setup mỗi lần

---

### Bước 4: Chạy CCPoke lần đầu

**Để làm gì?**
- CCPoke sẽ tự động **đăng ký hooks** vào Claude Opus
- Hook là đoạn code được gọi khi Claude Opus hoàn thành một task

**Cách làm:**

```bash
npx -y ccpoke
```

**Điều xảy ra:**
- CCPoke tự động tạo hooks trong `~/.claude/settings.json`
- Tạo file `~/.ccpoke/hooks/claude-code-stop.cmd`
- Hiện thông báo đã cài đặt thành công

**Tại sao cần bước này?**
- Không có hook = Claude Opus không biết gọi ai khi xong việc
- CCPoke sẽ không nhận được thông báo khi agent chạy xong

**Không làm sao?**
- Notification sẽ không hoạt động
- Claude Opus chạy xong nhưng không ai biết

---

### Bước 5: Fix Hook cho Windows + Git Bash

**Vấn đề thực tế gặp phải:**

Khi Claude Opus chạy xong, báo lỗi:
```
/usr/bin/bash: line 1: C:Usershls.ccpokehooksclaude-code-stop.cmd: command not found
```

**Tại sao có lỗi này?**

1. **CCPoke tạo file `.cmd`** (Windows batch file)
2. **Nhưng Claude Opus chạy trong Git Bash** (Unix environment)
3. **Path bị convert sai:**
   - Input: `C:\Users\hls\.ccpoke\hooks\claude-code-stop.cmd`
   - Output: `C:Usershls.ccpokehooksclaude-code-stop.cmd` (thiếu `\`)
4. **Bash không hiểu `.cmd`** → báo "command not found"

**Fix đã thực hiện:**

1. **Tạo file `.sh` (Unix shell script):**

```bash
cat > ~/.ccpoke/hooks/claude-code-stop.sh << 'EOF'
#!/bin/bash
curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \
  -H "Content-Type: application/json" \
  -H "X-CCPoke-Secret: ebf4a4c6a737caafe50f7fc4f18241a51c145e96f8971de9e2e663f20d035386" \
  --data-binary @- > /dev/null 2>&1
EOF
chmod +x ~/.ccpoke/hooks/claude-code-stop.sh
```

2. **Cập nhật settings.json với Unix path:**

Mở `C:\Users\{username}\.claude\settings.json`, tìm phần hooks và sửa:

```json
"hooks": {
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "/c/Users/{username}/.ccpoke/hooks/claude-code-stop.sh",
      "timeout": 10
    }]
  }]
}
```

**Tại sao phải làm vậy?**

| Cách | Vấn đề |
|------|---------|
| `.cmd` + Windows path | Bash không chạy được |
| `.sh` + Unix path | ✅ Hoạt động |

**Không làm sao?**
- Hook không được gọi
- Notification không gửi
- Lỗi "command not found" mỗi khi Claude Opus xong

---

### Bước 6: Xác nhận hoạt động

**Để làm gì?**
- Đảm bảo mọi thứ hoạt động trước khi sử dụng thật
- Kích hoạt "chat session" giữa bot và user

**Cách làm:**

1. **Chạy CCPoke:**
```bash
npx -y ccpoke
```
*CCPoke phải chạy liên tục để nhận hooks*

2. **Gửi /start trong Telegram:**
- Mở bot trên Telegram
- Gửi `/start`
- Bot sẽ reply xác nhận đăng ký thành công

**Tại sao cần gửi /start?**
- `/start` là cách để Telegram Bot biết user nào đang tương tác
- Sau khi nhận /start, bot sẽ lưu session và gửi notification cho đúng user đó

3. **Test notification:**
- Dùng Claude Opus bình thường
- Gõ một câu hỏi đơn giản, ví dụ: "Hello"
- Khi agent trả lời xong → xem Telegram có nhận notification không

**Không làm sao?**
- Bot không biết gửi notification cho ai
- Dù config có user_id đúng, vẫn cần "activate" bằng /start

---

## Bugs đã gặp và Fix chi tiết

### Bug 1: Hook path sai trên Windows + Git Bash ✅ ĐÃ FIX

**Lỗi:**
```
/usr/bin/bash: line 1: C:Usershls.ccpokehooksclaude-code-stop.cmd: command not found
```

**Nguyên nhân:**
- CCPoke tạo file `.cmd` (Windows batch)
- Claude Opus chạy trong Git Bash (Unix)
- Path bị convert sai: `C:\` → `C:`

**Fix:**
```bash
# 1. Tạo file .sh (Unix shell)
cat > ~/.ccpoke/hooks/claude-code-stop.sh << 'EOF'
#!/bin/bash
curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \
  -H "Content-Type: application/json" \
  -H "X-CCPoke-Secret: YOUR_SECRET" \
  --data-binary @- > /dev/null 2>&1
EOF

# 2. Cấp quyền execute
chmod +x ~/.ccpoke/hooks/claude-code-stop.sh

# 3. Cập nhật settings.json với Unix path
# "command": "/c/Users/{user}/.ccpoke/hooks/claude-code-stop.sh"
```

---

### Bug 2: Không lấy được user_id ✅ ĐÃ FIX

**Vấn đề:**
- Không thể dùng @userinfobot (không mở được Telegram app)
- Cần cách khác để lấy ID

**Fix - Dùng API:**
```bash
# 1. Gửi tin nhắn cho bot từ Telegram app
# 2. Gọi API
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates"

# 3. Tìm "from":{"id":123456789,...}
```

---

### Bug 3: CCPoke regenerate .cmd mỗi lần chạy ✅ ĐÃ FIX

**Vấn đề:**
- Mỗi khi chạy `ccpoke setup`, nó overwrite lại settings.json
- Settings.json bị đổi về .cmd thay vì .sh

**Fix:**
- Không chạy `ccpoke setup` sau khi đã setup xong
- Nếu bị overwrite, chỉnh sửa lại settings.json thủ công

---

### Bug 4: Notification không gửi ✅ ĐÃ FIX

**Vấn đề:**
- Data được nhận (có file trong `~/.ccpoke/responses/`)
- Nhưng Telegram không nhận được notification

**Nguyên nhân:**
- user_id đã set trong config
- Nhưng "chat session" chưa được activate bằng /start

**Fix:**
1. Chạy CCPoke: `npx -y ccpoke`
2. Gửi `/start` cho bot trong Telegram
3. Test lại với Claude Opus

---

### Bug 5: Port 9377 bị chiếm ✅ ĐÃ FIX

**Lỗi:** `another ccpoke is already running on port 9377`

**Nguyên nhân:** CCPoke đã chạy rồi, không thể chạy thêm instance

**Fix:**
```bash
# Tìm process đang dùng port 9377
netstat -ano | findstr :9377

# Kill process đó
taskkill //F //PID <PID_NUMBER>
```

---

## Troubleshooting

### Kiểm tra CCPoke đang chạy

```bash
# Kill và chạy lại
taskkill //F //IM node.exe
npx -y ccpoke
```

### Kiểm tra hook có chạy không

```bash
ls -la ~/.ccpoke/responses/
```

Nếu có file mới sau khi dùng Claude Opus = hook hoạt động

### Test hook thủ công

```bash
echo '{"session_id": "test", "message": "Hello"}' | \
  curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \
  -H "Content-Type: application/json" \
  -H "X-CCPoke-Secret: YOUR_SECRET" \
  --data-binary @-
```

### Test gửi tin nhắn trực tiếp

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<USER_ID>&text=Test"
```

---

## Commands

| Command | Mô tả |
|---------|-------|
| `npx -y ccpoke` | Chạy bot |
| `npx -y ccpoke setup` | Setup lại (interactive) |
| `npx -y ccpoke project` | Thêm project |
| `npx -y ccpoke channel` | Đổi channel |
| `npx -y ccpoke uninstall` | Gỡ hoàn toàn |

---

## Telegram Bot Commands

| Command | Mô tả |
|---------|-------|
| `/start` | Đăng ký chat |
| `/sessions` | Xem sessions |
| `/projects` | Xem projects |

---

## Files & Locations

| File | Path |
|------|------|
| Config | `C:\Users\{user}\.ccpoke\config.json` |
| Hooks | `C:\Users\{user}\.ccpoke\hooks\` |
| Responses | `C:\Users\{user}\.ccpoke\responses\` |
| Claude Settings | `C:\Users\{user}\.claude\settings.json` |

---

## Quick Setup (TL;DR)

```bash
# 1. Lấy token từ @BotFather
# 2. Lấy user_id bằng API hoặc @userinfobot

# 3. Tạo config
mkdir -p ~/.ccpoke
cat > ~/.ccpoke/config.json << 'EOF'
{
  "channel": "telegram",
  "telegram_bot_token": "YOUR_TOKEN",
  "user_id": YOUR_ID,
  "hook_port": 9377,
  "hook_secret": "",
  "locale": "en",
  "agents": ["claude-code"],
  "projects": []
}
EOF

# 4. Tạo .sh hook
cat > ~/.ccpoke/hooks/claude-code-stop.sh << 'EOF'
#!/bin/bash
curl -s -X POST "http://localhost:9377/hook/stop?agent=claude-code" \
  -H "Content-Type: application/json" \
  -H "X-CCPoke-Secret: YOUR_SECRET" \
  --data-binary @- > /dev/null 2>&1
EOF
chmod +x ~/.ccpoke/hooks/claude-code-stop.sh

# 5. Cập nhật ~/.claude/settings.json với Unix path

# 6. Chạy
npx -y ccpoke

# 7. Gửi /start trong Telegram
```

---

## Security Analysis

### Đánh giá bảo mật

**Những gì CCPoke làm:**

| Hành động | Có vấn đề? |
|------------|-------------|
| Lưu token local | ✅ An toàn - chỉ lưu trong máy |
| Gửi notification đến Telegram API | ✅ An toàn - cần thiết để hoạt động |
| Nhận hook từ Claude Opus | ✅ An toàn - có secret xác thực |
| Gửi code changes/git diffs | ⚠️ Cẩn thận - có thể chứa secrets |

**Những gì CCPoke KHÔNG làm:**
- ❌ Không gửi code của bạn ra server
- ❌ Không lưu trữ data trên cloud
- ❌ Không đọc file không cần thiết

### Các endpoint bảo mật

**Hook endpoints** (Claude Opus gọi):
- `/hook/stop` - khi agent xong
- `/hook/session-start` - khi bắt đầu
- `/hook/notification` - notification
- `/hook/ask-user-question` - hỏi user
- `/hook/permission-request` - xin permission

Mỗi request đều cần header `X-CCPoke-Secret` đúng mới chạy.

### Những điều cần lưu ý

**1. Token Telegram:**
- Lưu trong `~/.ccpoke/config.json`
- Nếu bị lộ → người khác có thể gửi tin nhắn từ bot của bạn
- **Cách protect:** Không share file config

**2. hook_secret:**
- Dùng để xác thực request từ Claude Opus
- Nếu bị lộ → người khác có thể giả mạo notification
- Đã có sẵn trong config, tự động tạo

**3. Data trong notification:**
- Khi gửi notification, CCPoke gửi:
  - Response summary
  - Git changes (nếu có)
  - Project name
  - Session ID
- ⚠️ **Lưu ý:** Không gửi full code, chỉ gửi summary

**4. cloudflared (optional):**
- Package có `cloudflared` - dùng để expose local server ra ngoài
- Theo mặc định, CCPoke chạy **local** (localhost:9377)
- Không cần expose ra ngoài nếu chỉ dùng notification

### Best Practices

1. **Không share config file** - chứa token và secret
2. **Chạy CCPoke local** - không cần expose ra ngoài
3. **Không dùng token chính** - tạo bot riêng cho CCPoke
4. **Revoke token nếu nghi ngờ** - qua @BotFather

---

## Links

- **GitHub:** https://github.com/kaida-palooza/ccpoke
- **Docs:** https://kaida-palooza.github.io/ccpoke/
- **BotFather:** @BotFather
- **UserInfo:** @userinfobot



---

![](image/Pasted%20image%2020260307194131.png)


# Hướng dẫn cài đặt ccpoke — Telegram Notification cho Claude Code

> ccpoke là cầu nối 2 chiều giữa AI agent (Claude Code, Codex CLI, Cursor CLI) và Telegram. Nhận thông báo khi Claude Code trả lời xong, gửi yêu cầu, quản lý nhiều phiên làm việc — tất cả từ điện thoại.

**Repo:** https://github.com/kaida-palooza/ccpoke

---

## Yêu cầu

- Node.js ≥ 20
- tmux (cần cho tương tác 2 chiều)
- Telegram Bot Token (tạo từ @BotFather)

---

## Bước 1: Upgrade Node.js

ccpoke yêu cầu Node ≥ 20. Nếu đang dùng Node cũ (ví dụ v16), cần upgrade qua nvm:

```bash
nvm install 20
nvm use 20
nvm alias default 20
node -v   # Xác nhận → v20.x.x
```

Nếu không upgrade, sẽ gặp lỗi `better-sqlite3` build fail (g++ không hỗ trợ `-std=c++20`) và `node:util` thiếu export `styleText`.

---

## Bước 2: Cài đặt ccpoke

```bash
npm i -g ccpoke
```

Các warning `deprecated` (har-validator, prebuild-install, uuid, request) là từ dependency cũ, không ảnh hưởng.

---

## Bước 3: Chạy setup lần đầu

```bash
ccpoke
```

Trình hướng dẫn sẽ yêu cầu:

1. Chọn ngôn ngữ
2. Nhập Telegram Bot Token (lấy từ @BotFather)
3. Quét QR hoặc mở link để kết nối bot
4. Gửi `/start` tới bot trên Telegram
5. Chọn AI agents (Claude Code, Codex CLI, Cursor CLI)

---

## Bước 4: Fix lỗi "Cannot be launched inside another Claude Code session"

Nếu ccpoke tạo session từ Telegram nhưng Claude Code báo lỗi:

> Error: Claude Code cannot be launched inside another Claude Code session.

Nguyên nhân: biến môi trường `CLAUDECODE` bị kế thừa từ session cũ.

**Fix:**

```bash
echo 'unset CLAUDECODE' >> ~/.bashrc
source ~/.bashrc
```

---

## Bước 5: Accept Terms (1 lần duy nhất)

Nếu session mới bị kẹt ở prompt "Yes, I accept", cần accept terms 1 lần trong terminal thường:

```bash
cd ~/path/to/your/project
claude
# Chọn "2. Yes, I accept" → Enter
# Sau đó thoát: /exit hoặc Ctrl+C
```

Sau khi accept, các session mới từ Telegram sẽ không hỏi lại.

---

## Bước 6: Chạy ccpoke ngầm trong tmux

Nếu chạy `ccpoke` trực tiếp, Ctrl+C sẽ tắt luôn. Để chạy ngầm:

```bash
# Tạo session riêng cho ccpoke
tmux new -s ccpoke -d 'ccpoke'
```

Các lệnh quản lý:

```bash
# Xem log
	tmux attach -t ccpoke

# Thoát ra mà không tắt (detach)
# Nhấn: Ctrl+B rồi D

# Restart ccpoke
tmux kill-session -t ccpoke
tmux new -s ccpoke -d 'ccpoke'
```

---

## Bước 7: Đăng ký project

```bash
ccpoke project
```

Chọn "Thêm dự án mới" → nhập đường dẫn và tên project.

Sau đó vào Telegram gửi `/projects` → chọn project → chọn agent → session Claude Code tự khởi chạy trong tmux pane mới.

---

## Lệnh Telegram

|Lệnh|Chức năng|
|---|---|
|`/start`|Đăng ký lại cuộc trò chuyện|
|`/sessions`|Xem danh sách phiên đang hoạt động|
|`/projects`|Xem danh sách dự án và mở phiên mới|

---

## Xem phiên làm việc

```bash
# Attach vào tmux session của ccpoke
tmux attach -t ccpoke

# Hoặc nếu dùng iTerm2
tmux -CC attach
```

Mỗi pane trong tmux là 1 session Claude Code cho 1 project. Di chuyển giữa các pane bằng `Ctrl+B` rồi phím mũi tên.

---

## Gỡ cài đặt

```bash
ccpoke uninstall
```

---

## Troubleshooting

|Vấn đề|Nguyên nhân|Giải pháp|
|---|---|---|
|`npm ERR! better-sqlite3` build fail|Node < 20 hoặc g++ cũ|`nvm install 20 && nvm use 20`|
|`styleText` not exported|Node < 20|Upgrade Node ≥ 20|
|"Cannot be launched inside another Claude Code session"|Biến `CLAUDECODE` kế thừa|`echo 'unset CLAUDECODE' >> ~/.bashrc && source ~/.bashrc`|
|Session kẹt ở "Yes, I accept"|Chưa accept terms|Chạy `claude` trong terminal, accept 1 lần|
|Ctrl+C tắt ccpoke|Chạy foreground|Dùng `tmux new -s ccpoke -d 'ccpoke'`|
|"failed to register commands"|Lỗi mạng tạm thời|Restart ccpoke|
|"callback_query too old"|Callback cũ còn sót|Vô hại, bỏ qua|

---

## Ghi chú

- **Server:** mgc-dev2-3090 (Ubuntu, nvm)
- **Node version:** v20.20.1
- **ccpoke version:** 1.6.27
- **Ngày cài đặt:** 2026-03-07