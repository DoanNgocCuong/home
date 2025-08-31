### 

  

nohup python3 youtube_video_crawler.py > crawler_output.log 2>&1 &

Giải thích từng phần:

- nohup = "no hang up" - Giữ cho tiến trình chạy ngay cả khi bạn đóng terminal

- python3 youtube_video_crawler.py = Chạy script Python

- > = Chuyển hướng output (stdout)

- crawler_output.log = File để lưu output

- 2>&1 = Chuyển hướng stderr (lỗi) vào cùng file với stdout

- & = Chạy ở background (không block terminal)

```
nohup python main.py --start_situation 10001 --end_situation 11000000956 --input_file "31082025_HocThu_Work.xlsx" --max_workers 20 --batch_size 1 > hocthu_work.log 2> err_hocthu_nonwork.log &


```


```
nohup python main.py --start_situation 1 --end_situation 111000000956 --input_file "31082025_HocThu_Work.xlsx" --max_workers 20 --batch_size 1 > hocthu_work.log 2>&1 &

```