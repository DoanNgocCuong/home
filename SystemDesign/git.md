- git init 
- git remote add origin ...


- KHI BẠN GIT PUSH trong terminal. Nó sẽ báo lỗi: 
```
Lỗi này xuất phát từ việc GitHub phát hiện có **API key** (cụ thể là **OpenAI API Key**) trong mã nguồn của bạn và từ chối push do vi phạm các quy tắc bảo mật. Để giải quyết vấn đề này, bạn cần xóa hoặc ẩn thông tin nhạy cảm (như API key) trước khi tiếp tục push. Dưới đây là các bước cụ thể để xử lý:

### 1. **Xóa API Key khỏi mã nguồn**

- Mở các file đã được chỉ ra trong thông báo lỗi:
    
    - `QuizApp_deploy2.3_MulTopic/app.py` tại dòng 63
    - `QuizApp_deploy2.2_Change_Backend_JSONPrompt/app.py` tại dòng 63
- Xóa hoặc thay thế OpenAI API Key bằng biến môi trường hoặc file cấu hình không được đẩy lên GitHub. Ví dụ:

### 2. **Xóa API Key khỏi lịch sử commit**

Nếu API Key đã bị commit trước đó, bạn cần xóa nó khỏi lịch sử commit bằng cách sử dụng **BFG Repo-Cleaner** hoặc **git filter-repo**. Dưới đây là cách làm với `git filter-repo`:

- **Cài đặt `git filter-repo`**:
    
    - Trên Windows, bạn có thể cài đặt thông qua Python pip:
        
        bash
        
        Copy code
        
        `pip install git-filter-repo`
        
- **Chạy lệnh để xóa API Key khỏi lịch sử commit**:
    
    bash
    
    Copy code
    
    `git filter-repo --path QuizApp_deploy2.3_MulTopic/app.py --invert-paths git filter-repo --path QuizApp_deploy2.2_Change_Backend_JSONPrompt/app.py --invert-paths`
    
    Lệnh này sẽ xóa các file chứa API Key khỏi lịch sử commit.
    
```

