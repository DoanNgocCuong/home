1. FastAPI - SSE - Websocket 
2. Cơ chế fallback ? 
- retry 3 lần? 

1. tenacity 
2. ![[Pasted image 20250603210649.png]]

```bash
**Sang Nguyễn Thanh** 8:40 PM  
v SSE có upgrade từ http/1.1 sang dạng upgrade ko anh  
Messages addressed to "meeting group chat" will also appear in the meeting group chat in Team Chat  
Due to the large number of participants in this meeting, system messages for those who joined or left have been disabled  
  
**Sang Nguyễn Thanh** 8:41 PM  
oke anh  
  
**Trần Quang Minh** 8:42 PM  
chắc chắn là sse ạ:))) vì websocket bị lặp từ  
  
**Lê Sỹ Thăng** 8:43 PM  
em thì websoket ạ.  
  
**Nam** 8:43 PM  
websocket a  
  
**Kien** 8:43 PM  
SSE ạ  
  
**Quang Dũng Lương** 8:44 PM  
SSE có bị giới hạn connections đồng thời không ạ?  
  
**Lê Sỹ Thăng** 8:44 PM  
tại chatbot giờ chủ yếu dùng websoket nên chắc sẽ tận dụng luôn  
em lôn các ứng dụng web ạ  
  
**Trần Quang Minh** 8:46 PM  
SSE ạ  
  
**Lê Sỹ Thăng** 8:46 PM  
em nghỉ là websoket  
  
**dao nghia** 8:46 PM  
SSE  
  
**Hung Nguyen** 8:46 PM  
SSE ạ, vì mình chat mới gửi response  
  
**Sang Nguyễn Thanh** 8:46 PM  
em nghĩ cả 2  
bản web thì SSE  
  
**Hung Nguyen** 8:57 PM  
Em hay dùng 3-5 ạ  
  
**You** 8:57 PM  
3 ạ  
  
**dao nghia** 8:58 PM  
overload  
  
**Hung Nguyen** 8:59 PM  
Tăng cost ạ  
  
**Hung Nguyen** 9:03 PM  
dạ em có đang xài  
  
**Trần Quang Minh** 9:12 PM  
btap có các phần này kh ạ  
  
**Nam** 9:13 PM  
sao zoom mình ko xem được, nó hiện `Không thể xem nội dung này ở đây` nhỉ?  
  
**FSDS** 9:14 PM  
https://docs.celeryq.dev/en/latest/getting-started/introduction.html  
  
**Sang Nguyễn Thanh** 9:15 PM  
tại sao ko xài kafka ạ  
  
**dao nghia** 9:16 PM  
rabitmq cung dc a  
  
**Nam** 9:16 PM  
tin này cũng bị vậy ạ, 'Không thể xem nội dung này ở đây`  
  
**Hung Nguyen** 9:17 PM  
Cái Batch API của OpenAI cũng dùng dạng queue như này đúng không ạ  
mình gửi 1 file input rồi sét completion window là 24h mới nhận được output ạ  
  
**Trần Quang Minh** 9:18 PM  
tại sao lại có long run này vậy a. e chưa hiểu định nghĩa serving lắm ạ  
  
**Hung Nguyen** 9:20 PM (Edited)  
Async process 1000 requests đó thì sẽ xảy ra vấn đề gì ạ  
  
**dao nghia** 9:21 PM  
Trong trường hợp mình có nhiều task khác nhau, thì có thể đưa vào nhiều queue ko ạ  
có khác gì đưa vào 1 queue không ạ nếu dùng với celery  
  
**Trần Quang Minh** 9:23 PM  
vây lưu ở hang đợi gọi là broker ạ? , là broker là 1 db thì db đó sẽ lưu gì ạ  
  
**Sang Nguyễn Thanh** 9:24 PM  
có pattern nào sử dụng load balancer với message queue ko ạ  
dạ đúng rùi ạ, hosting thường sẽ gặp  
  
**Trần Quang Minh** 9:27 PM  
mấy cái này sử dung vllm thì có kv cached đk a nhỉ  
ủa vậy cái a đang nói có khác gì kv cached hay mấy cái cached khác trong vllm kh a
```