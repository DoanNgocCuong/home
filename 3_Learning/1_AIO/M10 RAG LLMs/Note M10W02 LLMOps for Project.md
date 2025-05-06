https://youtu.be/ts4wMuPIrus?feature=shared

0:19:00 tổng quan: Llama3, Adapter, OpenWebUI, Langchain, LangSmith, Gradio + 2 tool Monitoring 

Serving: Time to inference, token per second, GPU memory. 

1. Khi inference tức là mình làm g? 
-> nhân số từ input * parameters của model -> ra ouput. 
(Y = w*X +b) (X là input, w là trọng số, b là bias => Y là output)

2. model = torch.compile (model)
Tối ưu đồ thị tính toán => Kết quả cho thấy  ko thay đổi gì lắm
3. flash_attention_2 
tuy nhiên tùy phiên bản phần cứng nó ko hỗ trợ 
=> TĂNG 1/2 HIỆU NĂNG, GIẢM 1/2 MEMORY

4. W càng nhỏ, tính toán càng nhanh => Quantization + Flash_attention_2 
=> memmory giảm thêm so với v3 là 1GB khoảng 30%

---
0:29:00 serving thành API giống như API trên Playground của OpenAI, của DeepSeek
- 0:31:00 FastAPI (async - bất đồng bộ: async, await), DJ (đồng bộ)
Dùng FastAPI lâu thế rồi mà giờ mới biết là: nó chạy bất đồng bộ tức là: await 1 cái file thì API tiếp theo nó call, file được xử lý xong thì cái tiếp theo kia lại wait để cho nó chạy cái này 


Tuy nhiên chủ yếu time đến từ: đoạn INFERENCE nên cho dù cả async thì vẫn mất quá nhiều time. 
=> 0:34:00 Tritonserver - Dynamic Batching
 chờ cho đủ bacth nó chạy 

![[Pasted image 20250506124312.png]]

