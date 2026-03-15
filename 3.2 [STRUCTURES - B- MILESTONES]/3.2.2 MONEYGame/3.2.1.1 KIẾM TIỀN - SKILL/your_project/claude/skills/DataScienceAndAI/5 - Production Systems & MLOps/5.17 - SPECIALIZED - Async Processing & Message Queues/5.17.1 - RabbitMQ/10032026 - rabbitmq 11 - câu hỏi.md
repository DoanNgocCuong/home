**Best practices: Giữ message <1MB, offload large data ra Redis/S3 thay vì push toàn bộ vào RabbitMQ.**  
**Data lớn lưu Redis trước, queue chỉ chứa reference (key/path + task_id).**docs.aws.amazon+1

## Xử lý data lớn lúc publish

- **Small data (<100KB)**: Push trực tiếp JSON vào message RabbitMQ.[[cloudamqp](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)]​
    
- **Large data (>1MB)**: Producer lưu data vào Redis (với TTL) hoặc S3, message chỉ chứa **reference** (redis_key hoặc s3_url) + metadata.hoop+2  
    Worker đọc reference từ message, fetch data từ Redis/S3 xử lý, lưu result Redis.[[oneuptime](https://oneuptime.com/blog/post/2026-02-02-rabbitmq-large-messages/view)]​
    

## Sample code best practice (producer.py sửa)

python

`import pika, redis, json, uuid, boto3  # S3 ví dụ   r = redis.Redis(...)   s3 = boto3.client('s3')      task_id = str(uuid.uuid4())   data = {'x':5, 'y':10, 'large_prompt': 'very long text...'}  # Large!     # Lưu data lớn   data_key = f'data:{task_id}'   r.set(data_key, json.dumps(data), ex=3600)  # TTL 1h [web:79]     # Message chỉ ref   message = {'task_id': task_id, 'data_key': data_key}   # Hoặc S3: s3.put_object(Bucket='mybucket', Key=f'data/{task_id}.json', Body=json.dumps(data))   # message = {'task_id': task_id, 's3_path': f's3://mybucket/data/{task_id}.json'}     channel.basic_publish(..., body=json.dumps(message))  # <1KB`  

Worker.py sửa: `data = json.loads(r.get(msg['data_key']))`.[[oneuptime](https://oneuptime.com/blog/post/2026-02-02-rabbitmq-large-messages/view)]​

## Lý do best practices

|Kích thước data|Cách lưu|Lý do|
|---|---|---|

|Kích thước data|Cách lưu|Lý do|
|---|---|---|
|**<100KB**|Trực tiếp RabbitMQ [[cloudamqp](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)]​|Đơn giản, low latency|
|**100KB-1MB**|Compress + queue [[oneuptime](https://oneuptime.com/blog/post/2026-02-02-rabbitmq-large-messages/view)]​|Tránh memory alarm|
|**>1MB**|Redis/S3 ref hoop+1|Scale, tránh block broker (128MB max) docs.aws.amazon+1|

**AI/ML: Prompt lớn lưu Redis (hoặc Pinecone), queue ref cho MLOps worker.**[[moldstud](https://moldstud.com/articles/p-celery-configuration-best-practices-enhance-your-task-queue-efficiency)]​


**Producer/Consumer là thuật ngữ của RabbitMQ (message broker), không phải Redis.**  
**Redis dùng Publisher/Subscriber (Pub/Sub) cho pattern khác.**

## Producer/Consumer trong RabbitMQ

- **Producer**: App gửi message vào queue (exchange → queue).[](https://gpcoder.com/6912-work-queues-trong-rabbitmq/)​
    
- **Consumer/Worker**: Poll message từ queue, xử lý, ACK.[](https://gpcoder.com/6912-work-queues-trong-rabbitmq/)​  
    Ví dụ pika code: producer `basic_publish`, consumer `basic_consume`.[](https://dev.to/deepak_mishra_35863517037/the-nervous-system-designing-distributed-signaling-with-redis-and-rabbitmq-176f)​
    

## Redis không dùng Producer/Consumer

Redis List/Streams: Producer **PUSH** (LPUSH/XADD), Consumer **POP** (RPOP/XREAD) - gọi là **Producer-Consumer queue** nhưng không phải thuật ngữ chính thức.  
Redis Pub/Sub: **Publisher** → Channel, **Subscriber** listen - real-time notify, không persistent.[](https://viblo.asia/p/cap-nhat-celery-task-real-time-voi-redis-pubsub-va-websocket-RQqKLqdpZ7z)​

## Trong luồng kết hợp

|Thành phần|RabbitMQ|Redis|
|---|---|---|
|**Gửi data/task**|Producer (publish) [](https://200lab.io/blog/rabbitmq-la-gi/)​|SET key (ref data) [](https://hoop.dev/blog/what-rabbitmq-redis-actually-does-and-when-to-use-it/)​|
|**Nhận**|Consumer/Worker (consume) [](https://gpcoder.com/6912-work-queues-trong-rabbitmq/)​|GET key (result/ref) [](https://stackoverflow.com/questions/34541805/celery-using-redis-as-a-result-backend-and-rabbitmq-as-a-message-broker)​|
|**Pattern**|Queue (durable)|Key-value/PubSub [](https://redis.io/glossary/redis-queue/)​|

---
