

| MCP Server                                                                                                                                                       | Maintainer                         | Read | Write/Update                                                                                                                                             | Auto-convert Docs/Sheets                                                                                                                            | Vị thế                                                                                                                                                           | Phù hợp cho bạn                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Anthropic Google Drive MCP (reference)**[](https://www.pulsemcp.com/servers/gdrive)​                                                                           | Anthropic                          | ✅    | ❌ (chủ yếu read-only)                                                                                                                                    | ✅ (Docs/Sheets → text/CSV)[](https://playbooks.com/mcp/modelcontextprotocol-gdrive)​                                                                | Reference, rất phổ biến[](https://modelcontextprotocol.io/faqs)​                                                                                                 | Safe default, đọc/tóm tắt tài liệu fin, research               |
| **`mcp-gdrive` (community full-feature)**[](https://skywork.ai/skypage/en/The-Ultimate-Guide-to-the-mcp-gdrive-MCP-Server-for-AI-Engineers/1971371440002363392)​ | Community (evolved from Anthropic) | ✅    | ✅ (nhiều bản hỗ trợ Sheets write)[](https://skywork.ai/skypage/en/The-Ultimate-Guide-to-the-mcp-gdrive-MCP-Server-for-AI-Engineers/1971371440002363392)​ | ✅ (nhấn mạnh là key feature)[](https://skywork.ai/skypage/en/The-Ultimate-Guide-to-the-mcp-gdrive-MCP-Server-for-AI-Engineers/1971371440002363392)​ | SOTA về tính năng, nhiều guide chuyên sâu[](https://skywork.ai/skypage/en/The-Ultimate-Guide-to-the-mcp-gdrive-MCP-Server-for-AI-Engineers/1971371440002363392)​ | Khi muốn agent đọc + ghi vào Drive/Sheets (workflow tài chính) |
| **`gdrive-mcp-server` (felores)**[](https://github.com/felores/gdrive-mcp-server)​                                                                               | felores                            | ✅    | ❌ (read-focused)                                                                                                                                         | ✅                                                                                                                                                   | Được đánh giá là efficient, high‑performance read bridge[](https://skywork.ai/skypage/en/google-drive-ai-mcp-servers/1981200041361985536)​                       | Khi cần cầu nối đọc Drive rất ổn định, hiệu năng cao           |

https://github.com/taylorwilsdon/google_workspace_mcp


## GENSPARK: ✅ MCP Server được đề xuất

**[Google Workspace MCP Server](https://github.com/taylorwilsdon/google_workspace_mcp)** của Taylor Wilsdon - Đây là giải pháp **hoàn chỉnh nhất** với:

- ✅ **OAuth 2.1 multi-user support** (chính xác là điều bạn cần!)
- ✅ Drive + Sheets + Docs + Gmail + Calendar + Forms + Tasks + Chat
- ✅ FastMCP framework với stateless HTTP mode
- ✅ Bearer token authentication
- ✅ Production-ready


---

# 🔗 Hướng Dẫn Cấu Hình URL cho MCP Server

## 📌 Tóm Tắt Nhanh

**Câu hỏi**: Nên dùng `localhost` hay `<link-server>` trong cấu hình MCP?

**Trả lời**: Phụ thuộc vào **ngữ cảnh kết nối**:

| Ngữ cảnh | URL nên dùng | Ví dụ |
|----------|--------------|-------|
| **Container → Container** (trong Docker network) | ✅ **Service name** | `http://google-workspace-mcp:8000` |
| **Host machine → Container** | `localhost` + port mapped | `http://localhost:30024` |
| **External → Server** | Domain/IP public | `http://your-domain.com:30024` |

---

## 🎯 Chi Tiết Từng Trường Hợp

### 1. Container-to-Container (Trong Docker Network) ⭐ **KHUYẾN NGHỊ**

**Khi nào**: App container (`multi-agent-main`) cần kết nối đến MCP container (`mcp-google-workspace`)

**Cấu hình**:
```env
GOOGLE_WORKSPACE_MCP_URL=http://google-workspace-mcp:8000
```

**Lý do**:
- ✅ Service name (`google-workspace-mcp`) được Docker DNS tự động resolve
- ✅ Không phụ thuộc vào port mapping
- ✅ Hoạt động tốt nhất trong Docker network
- ✅ Không bị ảnh hưởng bởi firewall host

**Kiểm tra**:
```bash
# Từ trong app container
docker exec multi-agent-main python -c "import socket; print(socket.gethostbyname('google-workspace-mcp'))"
# Kết quả: 10.123.0.3 (IP của MCP container)
```

---

### 2. Host Machine → Container

**Khi nào**: Test từ máy host (không phải từ container)

**Cấu hình**:
```env
GOOGLE_WORKSPACE_MCP_URL=http://localhost:30024
```

**Lý do**:
- ✅ `localhost` trỏ đến chính máy host
- ✅ Port `30024` là port đã map từ container ra host (trong docker-compose: `30024:8000`)

**Lưu ý**:
- ⚠️ Chỉ hoạt động khi test từ host machine
- ⚠️ Không hoạt động từ container khác (vì `localhost` trong container = chính container đó)

---

### 3. External/Domain (Production)

**Khi nào**: Truy cập từ bên ngoài server, hoặc từ domain

**Cấu hình**:
```env
# Option 1: Dùng domain
GOOGLE_WORKSPACE_MCP_URL=http://your-domain.com:30024

# Option 2: Dùng IP public
GOOGLE_WORKSPACE_MCP_URL=http://103.253.20.30:30024
```

**Lý do**:
- ✅ Có thể truy cập từ bất kỳ đâu
- ✅ Phù hợp cho production

**Lưu ý**:
- ⚠️ Cần đảm bảo firewall cho phép port `30024`
- ⚠️ Cần cấu hình domain DNS nếu dùng domain

---

## 🔧 Cấu Hình Trong docker-compose-mcp.yml

### WORKSPACE_MCP_BASE_URI

Biến này được MCP server dùng để **tạo callback URLs** cho OAuth. 

**Quy tắc**:
- Nếu MCP server cần callback từ **bên ngoài** (Google OAuth redirect): dùng domain/IP public
- Nếu chỉ dùng trong Docker network: có thể dùng service name

**Ví dụ**:
```yaml
environment:
  # Cho OAuth callback từ Google (cần accessible từ internet)
  - WORKSPACE_MCP_BASE_URI=http://your-domain.com:30024
  
  # Hoặc nếu chỉ dùng internal
  - WORKSPACE_MCP_BASE_URI=http://google-workspace-mcp:8000
```

---

## 📋 Checklist Chọn URL

Chọn URL dựa trên câu hỏi sau:

1. **App và MCP có cùng trong Docker network không?**
   - ✅ Có → Dùng `http://google-workspace-mcp:8000` (service name)
   - ❌ Không → Xem tiếp

2. **Truy cập từ đâu?**
   - Host machine → `http://localhost:30024`
   - External/Internet → `http://<domain>:30024` hoặc `http://<ip>:30024`

3. **Có cần OAuth callback từ Google không?**
   - ✅ Có → `WORKSPACE_MCP_BASE_URI` phải là URL accessible từ internet
   - ❌ Không → Có thể dùng service name

---

## 🧪 Test Kết Nối

### Test từ App Container
```bash
# Kiểm tra service name resolve
docker exec multi-agent-main python -c "
import socket
try:
    ip = socket.gethostbyname('google-workspace-mcp')
    print(f'✅ Service name resolve: {ip}')
except:
    print('❌ Service name không resolve được')
"

# Test HTTP connection
docker exec multi-agent-main python -c "
import urllib.request
try:
    response = urllib.request.urlopen('http://google-workspace-mcp:8000/health', timeout=5)
    print(f'✅ HTTP connection OK: {response.status}')
except Exception as e:
    print(f'❌ HTTP connection failed: {e}')
"
```

### Test từ Host Machine
```bash
# Test localhost
curl http://localhost:30024/health

# Test với IP
curl http://103.253.20.30:30024/health
```

---

## 🎯 Kết Luận

**Cho Multi Agent System (app container → MCP container)**:

✅ **KHUYẾN NGHỊ**: 
```env
GOOGLE_WORKSPACE_MCP_URL=http://google-workspace-mcp:8000
```

**Lý do**:
- Cả app và MCP đều trong Docker network `multi-agent-network`
- Service name được Docker DNS tự động resolve
- Không phụ thuộc port mapping
- Hoạt động ổn định nhất

**Chỉ dùng `localhost` khi**:
- Test từ host machine (không phải từ container)
- Development local
- Không phải production



