# Cấu hình MCP Servers cho Technical Writer

## Giới thiệu

MCP (Model Context Protocol) servers mở rộng khả năng của Claude Opus bằng cách kết nối với các công cụ bên ngoài.

## Các MCP Servers được khuyến nghị

### 1. Document Checking MCPs

#### markdownlint
- **Mục đích**: Kiểm tra lỗi markdown
- **Cài đặt**: Sử dụng npm
```bash
npm install -g @modelcontextprotocol/server-markdownlint
```

#### spell-check
- **Mục đích**: Kiểm tra chính tả
- **Có sẵn**: VSCode built-in (Code Spell Checker)

### 2. Writing Support MCPs

#### Document Format
- Hỗ trợ định dạng tài liệu
- Convert giữa các format (markdown, HTML, PDF)

#### Table of Contents Generator
- Tự động tạo mục lục cho tài liệu dài

## Cách cấu hình trong VSCode

### Bước 1: Mở Settings
- VSCode → Settings (Ctrl+,)
- Tìm "mcpServers"

### Bước 2: Thêm MCP Server

```json
{
  "mcpServers": {
    "markdownlint": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-markdownlint"]
    }
  }
}
```

## MCP Servers phổ biến khác

| Tên | Mục đích | Cài đặt |
|-----|----------|---------|
| GitHub | Quản lý repo | npm |
| Memory | Lưu trữ kiến thức | Built-in |
| Web Fetch | Lấy nội dung web | Built-in |
| Web Search | Tìm kiếm web | Built-in |

## Lưu ý

- Không phải tất cả MCP đều cần thiết - chỉ cài đặt những thứ bạn thực sự cần
- Một số MCP yêu cầu cài đặt thêm dependencies
- Kiểm tra compatibility với phiên bản Claude Opus bạn đang dùng
