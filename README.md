# doanngoccuong.github.io/home

Bạn nên đặt file `Bai-viet-1-Image-Prompting.md` trong thư mục `_posts` nếu bạn muốn sử dụng hệ thống bài viết của Jekyll (nền tảng GitHub Pages thường sử dụng). Dưới đây là các bước chi tiết:

1. **Tạo Thư Mục `_posts`:**
   - Tại thư mục gốc của repository, tạo một thư mục có tên `_posts` nếu nó chưa tồn tại.

2. **Đặt Tên File Đúng Chuẩn:**
   - Tên file trong thư mục `_posts` cần tuân theo định dạng: `YYYY-MM-DD-title.md`. Ví dụ:
     ```
     2024-07-27-Bai-viet-1-Image-Prompting.md
     ```

3. **Nội Dung File Markdown:**
   - Đảm bảo file Markdown của bạn có chứa front matter ở đầu file. Ví dụ:
     ```markdown
     ---
     layout: post
     title: "Bài 1: Nguyên lý của các mô hình tạo ảnh và so sánh GANs-VAEs"
     date: 2024-07-27
     categories: blog
     ---

     Nội dung bài viết của bạn ở đây...
     ```

4. **Cập Nhật Liên Kết Trong `index.md`:**
   - Trong file `index.md`, cập nhật liên kết để trỏ đến bài viết mới tạo. Ví dụ:
     ```markdown
     [Bài 1: Nguyên lý của các mô hình tạo ảnh và so sánh GANs-VAEs]({{ site.baseurl }}{% post_url 2024-07-27-Bai-viet-1-Image-Prompting %})
     ```

Sau khi hoàn tất, commit và push các thay đổi lên repository của bạn. GitHub Pages sẽ tự động build lại trang web của bạn và bạn sẽ thấy bài viết mới xuất hiện.

Nếu có vấn đề gì, hãy kiểm tra lại các bước trên và chắc chắn rằng bạn đã tuân theo đúng định dạng và cấu trúc thư mục.