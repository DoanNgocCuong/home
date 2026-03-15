
1. [bmd1905/vietnamese-ocr: This is a project about Optical Character Recognition (OCR) in Vietnamese texts by using PaddleOCR and VietOCR.](https://github.com/bmd1905/vietnamese-ocr)
2. https://github.com/roboflow/notebooks

3. https://github.com/datalab-to/marker


---
Dưới đây là **bảng mô tả quá trình tăng VRAM** khi khởi chạy và thực thi DeepSeek-OCR theo log thực tế của bạn:

---

|**Mốc thời gian/quy trình**|**Tổng VRAM sử dụng**|**Tăng so với trước**|**Diễn giải**|
|---|---|---|---|
|Ban đầu (startup, idle)|~4.5 GB|—|Chỉ Python runtime, driver và module nền|
|Load mô hình (weights)|~10 GB|+5.5 GB|Tải weights model (~6.2 GiB), khởi tạo model structure, buffer cơ bản|
|Tạo KV cache, profiling encoder|~20 GB|+10 GB|Khởi tạo encoder cache (~8.7 GB), sinh cache attention (KV), profiling, tensor input chuẩn bị cho batch|
|Chạy inference/batch lớn|~22 GB|+2 GB|Tạo thêm tensor, attention, buffer ảnh, xử lý lô nhiều/ảnh lớn|

---

## **Diễn giải các bước chính**

- **Ban đầu (4.5GB):** Hệ điều hành, Python, driver, chưa load weights model.
    
- **Sau khi load model (10GB):** Thêm weights mô hình (~6.2GB), Python buffer, cấu trúc mạng.
    
- **Sau khi khởi tạo KV cache, encoder (20GB):** Cache attention, profiling tokenizer, buffer encoding cho việc inference các batch, các tokens dài.
    
- **Khi inference thực tế hoặc batch lớn (22GB):** Thêm buffer input mã hóa, attention context, sinh tensor kết quả của batch lớn.
    

---

## **Kết luận**

- **Quá trình khởi tạo và chạy DeepSeek-OCR sẽ tăng dần VRAM theo đúng logic tải tài nguyên:**
    
    - Idle → Load model → Profiling + KV cache → Chạy batch thực tế lớn.
        
- **Mỗi bước tăng VRAM là hợp lý theo cách các mô hình lớn quản lý bộ nhớ và chuẩn bị pipeline cho batch lớn và sequence length dài.**
    
- **RTX 3090 24GB có thể sử dụng gần hết VRAM khi bạn dùng batch nhiều ảnh hoặc xử lý tài liệu lớn.**
    

---

**Bảng này giúp bạn dễ dàng dự đoán VRAM sử dụng và kiểm soát tài nguyên khi thiết kế pipeline OCR hiệu quả trên GPU.**




## dots.ocr 


Anh có thể xài dots.ocr cho bài OCR tiếng việt ạ, tụi em cũng đang dùng cái này cho OCR  
https://dotsocr.xiaohongshu.com/  
https://github.com/rednote-hilab/dots.ocr  
  
	host về khoảng 10GB VRAM, máy khoảng 16VRAM là dùng được ạ.