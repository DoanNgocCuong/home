
# 3H THANH XUÂN ĐỂ FIX BUG `Client.__init__() got an unexpected keyword argument 'proxies'` Phân tích và Khắc phục Lỗi Tương thích giữa OpenAI và Langchain

  

## Vấn đề

  

Trong quá trình phát triển hệ thống RAG, tôi gặp phải lỗi `Client.__init__() got an unexpected keyword argument 'proxies'` khi khởi tạo OpenAI client. Lỗi này xuất hiện khi hệ thống cố gắng tích hợp OpenAI với Langchain.

  

## Hành trình Khắc phục

  

### Các nỗ lực ban đầu:

1. **Sử dụng AI để tự động sửa lỗi:**

   - Thử nhiều cách tiếp cận khác nhau với AI

   - Nhận được nhiều gợi ý khác nhau nhưng không giải quyết được vấn đề

  

2. **Thay thế Langchain bằng OpenAI trực tiếp:**

   - Cố gắng bypass Langchain và sử dụng OpenAI API trực tiếp

   - Vẫn gặp lỗi tương tự do các thư viện phụ thuộc

  

3. **Thử nghiệm các phiên bản khác nhau:**

   - Downgrade/upgrade các phiên bản thư viện

   - Thử các phiên bản khác nhau của OpenAI và Langchain

   - Vẫn không tìm được sự kết hợp hoạt động

  

### Phát hiện quan trọng:

Sau nhiều nỗ lực không thành công, tôi mới nhận ra rằng vấn đề nằm ở sự tương tác giữa các phiên bản thư viện. Đây là một bài học quý giá về việc hiểu sâu về cách các thư viện tương tác với nhau.

  

## Phân tích Nguyên nhân

  

Sau khi phân tích kỹ lưỡng, tôi xác định được nguyên nhân chính:

  

1. **Xung đột phiên bản thư viện:**

   - Hệ thống đang sử dụng OpenAI SDK phiên bản 1.76.0 (theo requirements.txt)

   - Các phiên bản Langchain đang sử dụng:

     - langchain==0.3.24

     - langchain-community==0.0.38

     - langchain-core==0.3.56

     - langchain-openai==0.3.14

  

2. **Thay đổi API:**

   - OpenAI SDK mới đã loại bỏ hỗ trợ tham số `proxies` trong hàm khởi tạo

   - Langchain vẫn đang cố gắng sử dụng tham số này theo cách cũ

  

3. **Cơ chế hoạt động:**

   - Langchain hoạt động như một wrapper cho OpenAI

   - Khi khởi tạo client, Langchain tự động truyền tham số `proxies`

   - Điều này gây xung đột với API mới của OpenAI

  

## Các Giải pháp Đã Thử

  

1. **Cập nhật phiên bản thư viện:**

   ```bash

   pip install "openai==1.76.0" "langchain==0.3.24" "langchain-community==0.0.38" "langchain-core==0.3.56" "langchain-openai==0.3.14"

   ```

  

2. **Sửa đổi cách khởi tạo client:**

   ```python

   # Initialize OpenAI client with minimal configuration

   self.client = OpenAI(

       api_key=os.getenv("OPENAI_API_KEY")

   )

   ```

  
  

## Kiểm thử Giải pháp

  

1. **Kiểm tra khởi tạo client:**

   - Xác nhận không còn lỗi `proxies`

   - Kiểm tra kết nối với OpenAI API

  

2. **Kiểm tra tính năng:**

   - Thử nghiệm các chức năng cơ bản

   - Xác nhận hoạt động của Langchain wrapper

  

3. **Kiểm tra hiệu suất:**

   - Đo lường thời gian phản hồi

   - Kiểm tra tính ổn định của hệ thống

  

## Kết quả

  

- ✅ Lỗi `Client.__init__() got an unexpected keyword argument 'proxies'` đã được khắc phục

- ✅ Hệ thống hoạt động ổn định với các phiên bản thư viện mới

- ✅ Tất cả chức năng hoạt động như mong đợi

  

## Bài học Kinh nghiệm

  

1. **Quản lý phiên bản:**

   - Luôn kiểm tra tính tương thích giữa các phiên bản thư viện

   - Cập nhật `requirements.txt` khi thay đổi phiên bản

  

2. **Phân tích lỗi:**

   - Đọc kỹ thông báo lỗi để hiểu nguyên nhân gốc rễ

   - Kiểm tra các phụ thuộc giữa các thư viện

  

3. **Phát triển:**

   - Sử dụng các phiên bản thư viện ổn định

   - Đặt tên biến rõ ràng và nhất quán

   - Kiểm tra kỹ các thay đổi API của thư viện

  

4. **Tài liệu:**

   - Cập nhật tài liệu khi thay đổi phiên bản

   - Ghi lại các vấn đề và giải pháp đã thử

  

5. **Quá trình debug:**

   - Đôi khi cần thời gian để hiểu đúng vấn đề

   - Không nên chỉ dựa vào AI để sửa lỗi

   - Cần hiểu sâu về cách các thư viện tương tác với nhau