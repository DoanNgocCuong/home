
1. Google Apps Script là một phiên bản của JavaScript chạy trên máy chủ của Google, được thiết kế để tương tác với các dịch vụ như Google Sheets, Drive, và Gmail. Dù dựa trên JavaScript ES5, Apps Script không hỗ trợ đầy đủ các tính năng mới của JavaScript hiện đại và không thể truy cập trực tiếp vào DOM như JavaScript trong trình duyệt. Điểm mạnh của Apps Script là các thư viện tích hợp sẵn giúp tự động hóa các tác vụ với hệ sinh thái Google dễ dàng hơn.

  

2. Google Apps Script không hỗ trợ trực tiếp cấu trúc thư mục khi làm việc trên trình duyệt, nhưng bạn có thể làm điều này bằng cách sử dụng `clasp` (Command Line Apps Script Projects) và làm việc trên máy tính bằng Visual Studio Code (VS Code). Dưới đây là cách thực hiện:

  

    1. **Cài đặt `clasp`**: Sử dụng lệnh `npm install -g @google/clasp` để cài đặt và `clasp login` để đăng nhập vào tài khoản Google.

    2. **Tạo và quản lý dự án**: Sử dụng `clasp create` để tạo dự án và tổ chức mã trong các thư mục như `src/`, `utils/`, `services/`.

    3. **Cập nhật `appsscript.json`**: Đảm bảo cấu hình chính xác để `clasp` nhận diện và tải lên các tệp.

    4. **Đẩy mã lên Google Apps Script**: Sử dụng `clasp push` để đồng bộ mã từ máy tính lên Google Apps Script.

  

Điều này giúp bạn tổ chức mã tốt hơn, dễ quản lý và phát triển chuyên nghiệp bằng cách tận dụng các công cụ như VS Code và Git.

```

- clasp login

- clasp create

- clasp push

- clasp pull

- clasp run

- clasp list

```

-----------

3. SIÊU BUG, `git push` mãi ko được, ra là chưa bật Google Apps Script API

- Truy cập vào trang cài đặt người dùng của Apps Script: https://script.google.com/home/usersettings

Tại đây, tìm và bật tùy chọn "Google Apps Script API".

- Phải lưu dự án trên google apps script thì mới pull, push từ local VSCode/Cursor lên được.

- Khi pull xuống thì các file cùng tên dưới local sẽ đcợc update, các file ko có tên trên cloud thì sẽ giữ nguyên, các file bị xoá trên cloud thì local không ảnh hưởng.  

- Còn khi push lên thì data trên Google Apps Script bị mất.

  

4. KHI PUSH LÊN GITHUB:

- API KEY KO ĐƯỢC PUSH

- File .clasp.json cũng KO THỂ PUSH LÊN GITHUB (((chứa ID của repo trên Google Apps Script, nó được tạo khi bạn đăng nhập vào Google Apps Script và chọn "Publish > Deploy as API executable"))).

=> Need enter scriptID in file `.clasp.json` để đồng bộ: VSCode với Google Apps Script.