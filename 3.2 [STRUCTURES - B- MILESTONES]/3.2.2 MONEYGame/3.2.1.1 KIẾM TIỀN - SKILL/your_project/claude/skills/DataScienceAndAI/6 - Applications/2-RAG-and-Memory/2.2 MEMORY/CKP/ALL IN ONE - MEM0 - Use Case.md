curl --location 'http://103.253.20.30:8889/memories' \
--header 'Content-Type: application/json' \
--data '{
"messages": [
{"role": "assistant", "content": "Chào cậu, tớ là Pika đây!"},
{"role": "assistant", "content": "Cậu có muốn Pika hát một bài không?"},
{"role": "assistant", "content": "Pika rất ổn! Cậu có muốn hỏi Pika điều gì khác không?"}
],
"user_id": "Nguyễn Minh Cường",
"agent_id": "agent_conv_456",
"infer": false
}'



curl --location 'http://103.253.20.30:8889/search' \
--header 'Content-Type: application/json' \
--data '{
"query": "Thái độ của tôi",
"user_id": "Nguyễn Minh Cường",
"top_k":3,
"limit": 10,
"score_threshold": 0.4
}'

{
"results": [
{
"id": "f492f40e-1378-4d39-a554-514a4577e56c",
"memory": "Thích hát",
"hash": "f97794dfccd9425157d917633f58d99d",
"metadata": null,
"score": 0.465090811252594,
"created_at": "2025-12-29T22:45:20.890865-08:00",
"updated_at": null,
"user_id": "Nguyễn Minh Cường",
"agent_id": "agent_conv_456"
},
{
"id": "82e74b1e-d5ce-4ff7-a74c-92f8ba17a64b",
"memory": "Tên là Pika",
"hash": "efa7ea9a6f9d4b2649eac651e7ae0497",
"metadata": null,
"score": 0.3765541911125183,
"created_at": "2025-12-29T22:45:20.695088-08:00",
"updated_at": null,
"user_id": "Nguyễn Minh Cường",
"agent_id": "agent_conv_456"
}
]
}

---

Sao cái này bị vấn đề gì vậy ?


curl --location 'http://103.253.20.30:8889/search' \
--header 'Content-Type: application/json' \
--data '{
"query": "Thái độ của tôi",
"user_id": "Nguyễn Minh Cường",
"top_k":3,
"limit": 10,
"score_threshold": 0.4
}'


{
"results": [
{
"id": "f492f40e-1378-4d39-a554-514a4577e56c",
"memory": "Thích hát",
"hash": "f97794dfccd9425157d917633f58d99d",
"metadata": null,
"score": 0.465090811252594,
"created_at": "2025-12-29T22:45:20.890865-08:00",
"updated_at": null,
"user_id": "Nguyễn Minh Cường",
"agent_id": "agent_conv_456"
},
{
"id": "82e74b1e-d5ce-4ff7-a74c-92f8ba17a64b",
"memory": "Tên là Pika",
"hash": "efa7ea9a6f9d4b2649eac651e7ae0497",
"metadata": null,
"score": 0.3765541911125183,
"created_at": "2025-12-29T22:45:20.695088-08:00",
"updated_at": null,
"user_id": "Nguyễn Minh Cường",
"agent_id": "agent_conv_456"
}
]
}


---
Sao hỏi về thái độ của tôi, user_id Nguyễn Minh Cường,
=> Mình tưởng chỉ ra memory của Nguyễn Minh Cường thôi chứ nhỉ???


Deep research memory MEM0 để chỉ rõ cách dùng


---


# 2. ý mình là sao khi mình sử dụng API  
  
```  
curl --location 'http://103.253.20.30:8889/search' \  
--header 'Content-Type: application/json' \  
--data '{  
"query": "Thái độ của tôi",  
"user_id": "Nguyễn Minh Cường",  
"top_k":3,  
"limit": 10,  
"score_threshold": 0.4  
}'  
```  
  
của user_id : Nguyễn Minh Cường  
  
--  
Mà sao output lại ra kết quả là fact của agent_id



---
# 3. 

```bash
curl --location 'http://103.253.20.30:8889/memories' \
--header 'Content-Type: application/json' \
--data '{
  "messages": [
    {"role": "user", "content": "Chào cậu, tớ là Pika đây!"},
    {"role": "user", "content": "Cậu có muốn Pika hát một bài không?"},
    {"role": "user", "content": "Pika rất ổn! Cậu có muốn hỏi Pika điều gì khác không?"}
  ],
  "user_id": "Đoàn Minh Cường"
}'
```

```bash
curl --location 'http://103.253.20.30:8889/search' \
--header 'Content-Type: application/json' \
--data '{
    "query": "Tên của tôi là gì?",
    "user_id": "Đoàn Minh Cường", 
    "top_k":3, 
    "limit": 10,
    "score_threshold": 0.7
}'
```

#### Case 1: Chỉ search với `user_id`

**Filter:** `user_id = "Nguyễn Minh Phúc"`

**Kết quả:** Tìm tất cả memories có `user_id = "Nguyễn Minh Phúc"`:
- Facts về USER: "Tên là Nguyễn Minh Phúc", "Thích ăn pizza"
- Facts về AGENT: "Tên là Pika", "Thích hát" (nếu được lưu với cùng `user_id`)

**Lưu ý:** Trả về cả facts về user và agent (nếu cùng `user_id`)