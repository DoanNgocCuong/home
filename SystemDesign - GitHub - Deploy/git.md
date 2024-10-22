- git init 
- git remote add origin ...
- `git reset --soft HEAD~1`: Lệnh git mình yêu thích nhất. 

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

### Biến môi trường .env 
	Khi bạn sử dụng **GitHub Secrets** để lưu trữ các biến môi trường trong phần **Secrets** của repository (dành cho GitHub Actions), những biến môi trường này chỉ được sử dụng khi chạy các workflows của **GitHub Actions** và không có trong repository khi bạn **git clone** xuống.
	
	Cụ thể:
	
	- **GitHub Secrets** không ảnh hưởng trực tiếp đến mã nguồn trong repository của bạn. Chúng chỉ được sử dụng trong quá trình GitHub Actions chạy (ví dụ: quá trình build, test, deploy) và không được lưu trữ dưới dạng file `.env` hoặc bất kỳ file nào khác trong repository.
	- Khi bạn **git clone** dự án xuống, những biến môi trường được lưu trong **GitHub Secrets** không tự động được tải về máy của bạn hoặc máy của những người khác. Những secrets này chỉ tồn tại trong môi trường của GitHub Actions khi workflow chạy.
	
	### Vậy làm thế nào để quản lý biến môi trường khi clone dự án?
	
	1. **File `.env.example`:** Tương tự như cách trước, bạn nên tạo một file `.env.example` và thêm hướng dẫn trong tài liệu dự án (ví dụ: README.md) để người dùng tự tạo file `.env` trên máy của họ khi clone dự án xuống.
	    
	2. **Sử dụng các công cụ quản lý secrets khác trong môi trường cục bộ**: Nếu bạn muốn lưu trữ và quản lý các secrets trong môi trường cục bộ (local environment), có thể cân nhắc sử dụng các dịch vụ như:
	    
	    - **AWS Secrets Manager**
	    - **HashiCorp Vault**
	    - **Azure Key Vault**
	    - **Docker secrets** (nếu bạn dùng Docker)
	    
	    Các công cụ này có thể giúp bạn tự động tải các biến môi trường an toàn vào ứng dụng khi khởi chạy trên môi trường cục bộ hoặc môi trường sản xuất.
	    
	
	### Tóm lại:
	
	- **GitHub Secrets** chỉ dùng trong GitHub Actions workflows, và không có liên hệ trực tiếp với quá trình clone mã nguồn.
	- Để quản lý biến môi trường khi clone dự án xuống, bạn vẫn cần dùng các giải pháp khác như tạo file `.env.example` hoặc cung cấp hướng dẫn về cách thiết lập các biến môi trường.



Về đường dẫn quá dài: `git config --system core.longpaths true`