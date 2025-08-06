### 

  

nohup python3 youtube_video_crawler.py > crawler_output.log 2>&1 &

Giải thích từng phần:

- nohup = "no hang up" - Giữ cho tiến trình chạy ngay cả khi bạn đóng terminal

- python3 youtube_video_crawler.py = Chạy script Python

- > = Chuyển hướng output (stdout)

- crawler_output.log = File để lưu output

- 2>&1 = Chuyển hướng stderr (lỗi) vào cùng file với stdout

- & = Chạy ở background (không block terminal)