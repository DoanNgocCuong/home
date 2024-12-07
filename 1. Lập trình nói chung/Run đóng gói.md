
```
npm install
npm start
```

- package.json 
- Tương tự như 
```
yarn install
yarn start
```

```
pip install poetry
poetry install
```

- Tạo xong sẽ có file `pyproject.toml`

- Run `poetry install` để cài đặt các dependencies sẽ có file `poetry.lock`

- Run `poetry shell` để kích hoạt môi trường

- Run `poetry run streamlit run src/main.py` để chạy ứng dụng



Tôi thấy bạn đã kích hoạt môi trường ảo nhưng chưa cài đặt các package cần thiết. Hãy làm theo các bước sau:

1. Đầu tiên, đảm bảo bạn đang ở thư mục gốc của project:
````bash
cd ~/GIT/Build-An-LLM-RAG-Chatbot-With-LangChain-Python
````

2. Cài đặt các dependencies cần thiết bằng Poetry:
````bash
# Cài đặt streamlit
poetry add streamlit

# Cài đặt các package khác
poetry add langchain python-dotenv
````

3. Sau khi cài đặt xong, thử chạy lại:
````bash
poetry run streamlit run src/main.py
````

Nếu vẫn gặp lỗi, bạn có thể thử:
````bash
# Kiểm tra xem các package đã được cài đặt chưa
poetry show

# Hoặc cài đặt lại tất cả dependencies
poetry install
````

Cho tôi biết nếu bạn vẫn gặp vấn đề!





Tôi thấy bạn đang nhập sai cú pháp trong quá trình khởi tạo Poetry. Hãy làm theo các bước sau:

1. Đầu tiên, di chuyển về thư mục gốc của project:
```bash
cd ~/GIT/Build-An-LLM-RAG-Chatbot-With-LangChain-Python
```

2. Khởi tạo Poetry project với thông tin cơ bản:
```bash
poetry init

# Trả lời các câu hỏi như sau:
Package name: llm-rag-chatbot  # hoặc tên bạn muốn
Version: 0.1.0
Description: A LLM RAG Chatbot  # mô tả ngắn gọn
Author: n  # bỏ qua phần này
License: n  # bỏ qua phần này
Compatible Python versions: ^3.11  # phiên bản Python của bạn
Would you like to define your dependencies interactively: no
Would you like to define your dev dependencies interactively: no
```

3. Sau khi khởi tạo xong, thêm các dependencies:
```bash
# Thêm streamlit
poetry add streamlit

# Thêm langchain
poetry add langchain

# Thêm các package khác cần thiết
poetry add python-dotenv
```

4. Kích hoạt môi trường và chạy ứng dụng:
```bash
# Kích hoạt môi trường
poetry shell

# Chạy ứng dụng
poetry run streamlit run src/main.py
```

Lưu ý: Đừng nhập "poetry add streamlit" làm tên package hay version. Đây là các lệnh riêng biệt sau khi bạn đã khởi tạo xong project.


- Tạo xong sẽ có file `pyproject.toml`
- Run `poetry install` để cài đặt các dependencies sẽ có file `poetry.lock`
- Run `poetry shell` để kích hoạt môi trường
- Run `poetry run streamlit run src/main.py` để chạy ứng dụng
