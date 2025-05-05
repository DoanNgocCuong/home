Gradio cung cấp nhiều loại nút và ô đầu vào để tạo giao diện tương tác. Dưới đây là danh sách các loại nút, ô và thành phần phổ biến trong Gradio:

### Các nút (Buttons):
1. **Button**: Tạo một nút nhấn, có thể được sử dụng để thực thi một hành động.
   - Ví dụ: `gr.Button("Submit")`

### Các ô đầu vào (Inputs):
1. **TextBox**: Một ô để người dùng nhập văn bản.
   - Ví dụ: `gr.Textbox(label="Input Text")`
   
2. **Number**: Ô nhập liệu cho số, cho phép người dùng nhập giá trị số.
   - Ví dụ: `gr.Number(label="Enter a number")`

3. **Slider**: Thanh trượt cho phép người dùng chọn một giá trị trong khoảng nhất định.
   - Ví dụ: `gr.Slider(minimum=0, maximum=100, label="Select a value")`

4. **Checkbox**: Ô kiểm tra cho phép người dùng chọn hoặc bỏ chọn.
   - Ví dụ: `gr.Checkbox(label="Accept terms and conditions")`

5. **Dropdown**: Danh sách thả xuống, cho phép người dùng chọn một mục từ danh sách.
   - Ví dụ: `gr.Dropdown(choices=["Option 1", "Option 2"], label="Select an option")`

6. **Radio**: Nút chọn cho phép người dùng chọn một trong nhiều tùy chọn.
   - Ví dụ: `gr.Radio(choices=["Option A", "Option B"], label="Pick one")`

7. **File**: Ô để tải lên tệp từ máy tính của người dùng.
   - Ví dụ: `gr.File(label="Upload a file")`

8. **Image**: Ô cho phép tải lên hình ảnh hoặc hiển thị hình ảnh.
   - Ví dụ: `gr.Image(label="Upload an image")`

9. **Audio**: Ô để tải lên và phát tệp âm thanh.
   - Ví dụ: `gr.Audio(label="Upload an audio file")`

10. **Video**: Ô để tải lên và phát tệp video.
    - Ví dụ: `gr.Video(label="Upload a video file")`

11. **CheckboxGroup**: Nhóm các ô checkbox cho phép chọn nhiều tùy chọn.
    - Ví dụ: `gr.CheckboxGroup(choices=["Option 1", "Option 2"], label="Pick options")`

12. **TextArea**: Ô nhập liệu văn bản nhiều dòng.
    - Ví dụ: `gr.TextArea(label="Enter a paragraph")`

### Các thành phần bổ sung khác:
1. **Label**: Dùng để hiển thị văn bản hoặc thông tin không thể chỉnh sửa.
   - Ví dụ: `gr.Label(value="This is a label")`

2. **Plot**: Hiển thị biểu đồ, đồ thị trực quan.
   - Ví dụ: `gr.Plot(label="Graph")`

3. **Gallery**: Thư viện để hiển thị nhiều hình ảnh.
   - Ví dụ: `gr.Gallery(label="Image Gallery")`

4. **HTML**: Ô hiển thị nội dung HTML tùy chỉnh.
   - Ví dụ: `gr.HTML(value="<h1>Custom HTML</h1>")`

5. **Markdown**: Dùng để hiển thị nội dung Markdown.
   - Ví dụ: `gr.Markdown(value="# Heading")`

Các thành phần này có thể kết hợp với nhau để tạo ra giao diện người dùng tương tác, thuận tiện cho việc nhập dữ liệu và xử lý tương tác trên Gradio.