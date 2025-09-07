Link: https://github.com/DoanNgocCuong/home/blob/main/3_Learning/4_MLOPs%20v%C3%A0%20Full%20Stack%20Docker/2.%20UV.md

---

> Sau khi ngồi 30min vật lộn với code demo của các sếp xài UV. 
> - Ban đầu em cài: .venv riêng ở ngoài toàn cục, sau đó vào thư mục con. 
>   Rồi pip install uv, sau đó uv run main.py cứ lỗi hoài. (Thậm chí nó còn tự tạo ra .venv riêng???)
> - Sau đó em hiểu là: à nó tự tạo .venv thế thì xoá .venv ở ngoài đi. 
> - Đi thẳng vào: run main.py thôi để cho nó tự tạo .venv trong cùng thư mục => Cũng bug. 
> - AI fix 30min ko ra => Sau đó thì hỏi AI về "**Những Điều Cần Chú Ý Khi Sử Dụng UV:**"


**Những Điều Cần Chú Ý Khi Sử Dụng UV:**

**1. Cài Đặt UV Đúng Cách:**

UV cần được cài đặt ở cấp hệ thống (global), không phải trong virtual environment. Đây là lỗi phổ biến nhất mà nhiều người gặp phải.

```powershell
# Sai - Không cài trong virtual environment
(.venv) > pip install uv  # ❌

# Đúng - Cài ở cấp hệ thống
> deactivate  # Thoát khỏi venv trước
> powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # ✅
```

**2. Không Kích Hoạt Virtual Environment Khi Dùng UV:**

UV tự động quản lý virtual environment, vì vậy bạn không cần và không nên kích hoạt venv thủ công:

```powershell
# Sai - Đang trong virtual environment
(.venv) > uv run main.py  # ❌ Gây lỗi Access Denied

# Đúng - Chạy từ ngoài virtual environment
> uv run main.py  # ✅ UV tự động xử lý
```

**3. File pyproject.toml Hoặc requirements.txt:**

UV cần file cấu hình để biết dependencies của project. Nếu không có, UV sẽ tạo virtual environment trống:


```toml
# pyproject.toml
[project]
name = "demo-rag"
version = "0.1.0"
dependencies = [
    "langchain",
    "chromadb",
    "openai",
]
```

**4. UV Lock File:**

UV tạo file `uv.lock` để đảm bảo tính nhất quán của dependencies. File này nên được commit vào git:

```powershell
# UV tự động tạo uv.lock khi cài dependencies
> uv sync  # Cài đặt dependencies từ pyproject.toml
> git add uv.lock  # Nên commit file này
```

**5. Cấu Trúc Lệnh UV:**

Hiểu rõ các lệnh cơ bản của UV để sử dụng hiệu quả:

```powershell
# Tạo project mới
> uv init my-project

# Thêm dependencies
> uv add pandas numpy

# Xóa dependencies
> uv remove pandas

# Chạy script
> uv run python main.py

# Chạy lệnh trong môi trường UV
> uv run pytest
```

**6. Tương Thích Với IDE:**

Khi dùng VSCode hoặc PyCharm, cần chỉ định đúng Python interpreter:

```powershell
# Tìm đường dẫn Python của UV
> uv run which python
# Output: D:\project\.venv\Scripts\python.exe

# Set interpreter này trong IDE
```

**7. Xử Lý Lỗi Permissions Trên Windows:**

Windows thường có vấn đề với file permissions. Một số cách xử lý:

```powershell
# Chạy PowerShell với quyền Admin nếu cần
> Start-Process powershell -Verb RunAs

# Hoặc dùng --no-cache nếu gặp lỗi cache
> uv run --no-cache main.py
```

**8. Python Version:**

UV có thể quản lý nhiều phiên bản Python. Chỉ định version trong pyproject.toml:

```toml
[project]
requires-python = ">=3.10"
```

**9. Không Mix UV Với Pip:**

Khi đã dùng UV cho project, nên dùng UV cho tất cả operations:

```powershell
# Sai - Mix UV và pip
> uv init
> pip install requests  # ❌

# Đúng - Dùng UV cho tất cả
> uv init
> uv add requests  # ✅
```

**10. Debug Mode:**

Khi gặp lỗi, dùng verbose mode để debug:

```powershell
# Xem chi tiết quá trình UV làm gì
> uv -v run main.py

# Hoặc nhiều chi tiết hơn
> uv -vv run main.py
```

**Workflow Chuẩn Với UV:**

```powershell
# 1. Clone project
> git clone <repo>
> cd project

# 2. Cài đặt dependencies (UV tự tạo venv)
> uv sync

# 3. Chạy code
> uv run python main.py

# 4. Thêm package mới
> uv add new-package

# 5. Update dependencies
> uv lock --upgrade
```

**Lưu Ý Quan Trọng:**

- UV là công cụ mới, có thể có bugs hoặc không tương thích với một số packages cũ
- Documentation của UV đang phát triển, check https://docs.astral.sh/uv/ thường xuyên
- Nếu gặp vấn đề phức tạp, có thể quay lại dùng pip/venv truyền thống