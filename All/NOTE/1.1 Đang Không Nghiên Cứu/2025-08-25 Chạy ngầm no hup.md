Bạn có thể chạy lệnh đó với `nohup` và redirect log như sau:

`nohup python api_processing_pipeline.py \   --start-row 0 \   --end-row 5 \   --batch-size 5 \   --max-workers 5 \   --parallel \   > pipeline.log 2>&1 &`

### Giải thích:

- `nohup`: giúp process chạy ngầm, không bị kill khi bạn thoát terminal.
    
- `> pipeline.log 2>&1`: redirect toàn bộ output (stdout + stderr) vào file `pipeline.log`.
    
- `&`: chạy process ở background.
    

### Kiểm tra tiến trình

`ps aux | grep api_processing_pipeline.py`

### Theo dõi log realtime

`tail -f pipeline.log`

👉 Bạn có muốn mình viết luôn thêm 1 script shell nhỏ (ví dụ `run_pipeline.sh`) để bạn chỉ cần gõ `sh run_pipeline.sh` là chạy kèm log luôn không?

##### You said:

ps aux là viết tắt của ?? grep là viét tắt của ?

###### ChatGPT said:

Hay câu hỏi 👍

### `ps aux`

- **ps** = _process status_ → lệnh liệt kê các tiến trình đang chạy.
    
- Tùy chọn:
    
    - **a** (_all users_): hiển thị tiến trình của tất cả user, không chỉ riêng của bạn.
        
    - **u** (_user-oriented_): hiển thị chi tiết như user, CPU, RAM, thời gian chạy.
        
    - **x** (_without controlling terminal_): hiển thị cả tiến trình không gắn với terminal (daemon, background jobs).
        

👉 Vậy `ps aux` nghĩa là: _hiển thị danh sách chi tiết tất cả tiến trình, của mọi user, kể cả tiến trình chạy ngầm._

---

### `grep`

- **grep** = _Global Regular Expression Print_.
    
- Công dụng: tìm dòng khớp với mẫu (pattern) trong văn bản hoặc output.
    

Ví dụ:

`ps aux | grep python`

→ Lọc ra chỉ những tiến trình có chữ `python`.

---

👉 Nói vui thì `ps aux | grep ...` là combo “hiển thị tất cả tiến trình và lọc ra cái mình quan tâm”.

Bạn có muốn mình làm một bảng tóm tắt mấy lệnh Unix cơ bản thường dùng khi chạy script Python dài hạn (ps, top, tail, kill, nohup) không?