# 1. Cách run với mặc định của dify: 
```bash
docker compose -f docker/docker-compose.yaml up
```
Cách run với image đã build sẵn
```bash
docker compose -f docker/docker-compose.yaml up --build
```

Tuy nhiên với việc run như trên thì sẽ không có api và web mới. 
- Cách 1: build image của api và web mới sau đó run `docker compose -f docker/docker-compose.yaml up`
- Cách 2: Truyền trực tiếp build (thay vì sử dụng image) vào `docker compose -f docker/docker-compose.yaml up`
```bash
image: langgenius/dify-api:0.9.2
```
thành 
```bash
build:
  context: ./api
  dockerfile: Dockerfile
```

# 3. Cách run chạy ngầm 1 file .py

```bash
python .\eval.py --start_row 1 --end_row 4

  

$env:PYTHONIOENCODING="utf-8"

Start-Process python -ArgumentList ".\eval.py", "--start_row", "13", "--end_row", "15" -RedirectStandardOutput "13_15_output.log" -RedirectStandardError "13_15_error.log" -WindowStyle Hidden

  

---

  

# Batch 1: 1001-2000

$env:PYTHONIOENCODING="utf-8"

Start-Process python -ArgumentList ".\eval.py", "--start_row", "1001", "--end_row", "2000" -RedirectStandardOutput "1001_2000_output.log" -RedirectStandardError "1001_2000_error.log" -WindowStyle Hidden

  

python .\eval_v1_onlyApiRAG.py --start_row 1 --end_row 4

  
  

---

python eval_v1_onlyApiRAG.py --start_row 1 --end_row 4

  

---

python eval_v2_ApiRAG_GetID_mapFullNameDB.py --file_name test1_dataset.xlsx --startrow 1 --end_row 1000

python eval_v2_ApiRAG_GetID_mapFullNameDB.py --file_name test1_dataset.xlsx --startrow 8000

python eval_v2_ApiRAG_GetID_mapFullNameDB.py --file_name test2_dataset.xlsx

  

----

  
  

python eval_v2_ApiRAG_GetID_mapFullNameDB.py --file_name test1_dataset.xlsx --startrow 1000 --end_row 8000

nohup python eval_v2_ApiRAG_GetID_mapFullNameDB.py --file_name test1_dataset.xlsx --start_row 1000 --end_row 8000 > eval_test1_embeddingV1_output.log 2>&1 &

  

nohup python eval_v2.2_embeddingv2_ApiRAG_GetID_mapFullNameDB.py --input_file test1_dataset.xlsx > eval_test1_embeddingV2_output.log 2>&1 &

nohup python eval_v2.2_embeddingv2_ApiRAG_GetID_mapFullNameDB.py --input_file test2_dataset.xlsx > eval_test2_embeddingV2_output.log 2>&1 &

  
  

---

python eval_v3_ApiRAG_GetID_mapFullNameDB_andGenerate.py --file_name test1_dataset.xlsx --start_row 1 --end_row 3

nohup python eval_v3_ApiRAG_GetID_mapFullNameDB_andGenerate.py --file_name test1_dataset.xlsx --start_row 1 > eval_test1_v3_output.log 2>&1 &

  
  

--- 19082025

  

python eval_v3_DataV2.2_ApiRAG_GetID_mapFullNameDB_andGenerate.py --file_name test1_dataset_v2_19082025_processed_2000LeanSpeak1000Onion.xlsx --start_row 1 --end_row 3

nohup python eval_v3_DataV2.2_ApiRAG_GetID_mapFullNameDB_andGenerate.py --file_name test1_dataset_v2_19082025_processed_2000LeanSpeak1000Onion.xlsx --start_row 1 > eval_test1_v3_output.log 2>&1 &

  
  
  

---

Muốn kill

  

ps aux | grep "eval_v3_DataV2.2_ApiRAG_GetID_mapFullNameDB_andGenerate.py" | grep -v grep

  

```bash

Lệnh `ps aux` hiển thị thông tin về các tiến trình đang chạy. Ý nghĩa của các ký tự viết tắt:

  

## `ps aux`

- **`a`** = hiển thị tất cả tiến trình của tất cả user (all users)

- **`u`** = hiển thị thông tin chi tiết về user owner và resource usage

- **`x`** = hiển thị cả những tiến trình không có terminal (daemon processes)

  

## `grep -v grep`

- **`grep`** = tìm kiếm dòng chứa pattern "eval_v3_DataV2.2_ApiRAG_GetID_mapFullNameDB_andGenerate.py"

- **`-v`** = invert match, loại bỏ (exclude) các dòng khớp với pattern sau `-v`

- **`grep`** (sau `-v`) = loại bỏ chính dòng chứa lệnh grep

  

## Tổng thể

Lệnh này sẽ:

1. Liệt kê tất cả tiến trình đang chạy

2. Tìm những tiến trình có tên chứa "eval_v3_DataV2.2_ApiRAG_GetID_mapFullNameDB_andGenerate.py"

3. Loại bỏ dòng chứa chính lệnh `grep` (để tránh hiển thị chính lệnh tìm kiếm)

  

Điều này rất hữu ích để kiểm tra xem script Python đó có đang chạy hay không mà không bị nhiễu bởi chính lệnh grep.

```
```
