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