# Async Processing & Message Queues — Production Best Practices

> **Domain:** 5.17 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

Message queues decouple producers and consumers, enabling:
- **Asynchronous processing**: Don't wait for expensive operations
- **Scalability**: Scale consumers independently of producers
- **Resilience**: Systems tolerate component failures
- **Load balancing**: Distribute work across multiple workers

**Impact Example:**
```
Without queue (synchronous):
User → API (5s image processing) → Response [User waits 5s]

With queue (asynchronous):
User → API (100ms, queues job) → Response [User sees success immediately]
       ↓
    Worker processes image asynchronously
```

## 2. Core Principles

### 2.1 Message Queue Comparison

| Feature | RabbitMQ | Kafka | Redis Streams | SQS |
|---------|----------|-------|---------------|-----|
| **Model** | Pull/Push | Pull (offset) | Pull/Pub-sub | Pull |
| **Retention** | Until consumed | Weeks | Days | 14 days |
| **Throughput** | 100k msg/s | 1M+ msg/s | 100k msg/s | 100k msg/s |
| **Ordering** | Per queue | Global | Per stream | FIFO option |
| **Complexity** | Medium | High | Low | Low |
| **Use Case** | Task queue | Event streaming | Cache layer | Managed service |

### 2.2 Delivery Semantics
- **At-most-once**: Message may be lost (fastest)
- **At-least-once**: Message never lost, may duplicate (most common)
- **Exactly-once**: No loss, no duplicates (complex)

## 3. Best Practices

### 3.1 Message Queue Selection

**Practice: Choose Based on Use Case**

```python
# Use RabbitMQ for:
# - Task queues (send email, resize image)
# - RPC-style request/reply
# - Small messages, low latency

# Use Kafka for:
# - Event streaming (user clicks, orders)
# - Event sourcing & audit logs
# - High throughput, multiple consumers
# - Replay events from past

# Use Redis Streams for:
# - Real-time messaging
# - Session management
# - Pub/sub with persistence
# - Lower operational overhead

# Use SQS for:
# - AWS-native services
# - Don't want to manage infrastructure
# - Variable load (auto-scaling)
```

### 3.2 Producer-Consumer Pattern

**Practice: Robust Message Handling**

```python
import json
import pika
from datetime import datetime

class MessageProducer:
    def __init__(self, rabbitmq_url):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()

        # Declare queue (tạo hàng đợi) - idempotent
        self.channel.queue_declare(
            queue='tasks',
            durable=True  # Survive broker restart
        )

    def publish_task(self, task_type, payload):
        message = {
            "id": str(uuid.uuid4()),
            "type": task_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat(),
            "retry_count": 0
        }

        # Publish with confirmation
        self.channel.basic_publish(
            exchange='',
            routing_key='tasks',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json'
            )
        )

        return message["id"]

class MessageConsumer:
    def __init__(self, rabbitmq_url):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='tasks', durable=True)

    def process_messages(self):
        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                logger.info(f"Processing: {message['id']}")

                # Process message
                self.handle_task(message)

                # Acknowledge (xác nhận) success
                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error(f"Error processing message: {e}")

                # Negative acknowledgment with requeue
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=True  # Return to queue for retry
                )

        self.channel.basic_qos(prefetch_count=1)  # One message at a time
        self.channel.basic_consume(
            queue='tasks',
            on_message_callback=callback
        )

        self.channel.start_consuming()

    def handle_task(self, message):
        if message["type"] == "send_email":
            send_email(message["payload"])
        elif message["type"] == "resize_image":
            resize_image(message["payload"])
```

**Key Concepts:**
- **Acknowledgment**: Consumer confirms processing
- **Requeue**: Return message if processing fails
- **Prefetch**: Limit messages to prevent overload

### 3.3 Pub/Sub Pattern

**Practice: Publish-Subscribe for Events**

```python
from redis import Redis

class EventBus:
    def __init__(self, redis_url):
        self.redis = Redis.from_url(redis_url)

    def publish(self, event_type, event_data):
        """Publish event to subscribers (xuất bản sự kiện)"""
        channel = f"events:{event_type}"
        self.redis.publish(channel, json.dumps(event_data))

    def subscribe(self, event_type, callback):
        """Subscribe to event type"""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(f"events:{event_type}")

        for message in pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                callback(event)

# Usage
bus = EventBus("redis://localhost:6379")

# Publisher
bus.publish("user.created", {
    "user_id": 123,
    "email": "user@example.com"
})

# Subscribers (multiple services can listen)
def on_user_created(event):
    send_welcome_email(event["email"])
    update_analytics(event["user_id"])
    create_notification(event["user_id"])

bus.subscribe("user.created", on_user_created)
```

**Use Cases:**
- Event broadcasting (hàng loạt phát)
- Real-time notifications
- Cache invalidation
- Analytics/logging

### 3.4 Dead Letter Queues (DLQ)

**Practice: Handle Failed Messages**

```python
import json
from datetime import datetime, timedelta

class RobustConsumer:
    def __init__(self, rabbitmq_url):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()

        # Main queue
        self.channel.queue_declare(queue='tasks', durable=True)

        # Dead letter queue for failed messages
        self.channel.queue_declare(queue='tasks.dlq', durable=True)

        # Bind main queue to DLQ on failure
        self.channel.queue_bind(
            exchange='tasks.dlx',
            queue='tasks.dlq',
            routing_key='#'
        )

    def process_with_retry(self):
        def callback(ch, method, properties, body):
            message = json.loads(body)
            retry_count = message.get("retry_count", 0)
            max_retries = 3

            try:
                process_message(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            except RetryableException as e:
                if retry_count < max_retries:
                    # Increment retry counter
                    message["retry_count"] = retry_count + 1
                    message["last_error"] = str(e)
                    message["last_retry"] = datetime.now().isoformat()

                    # Requeue with updated message
                    ch.basic_nack(delivery_tag=method.delivery_tag)

                    # Republish with delay
                    delay_ms = (2 ** retry_count) * 1000  # Exponential backoff
                    self.channel.basic_publish(
                        exchange='',
                        routing_key='tasks',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                            expiration=str(delay_ms)
                        )
                    )
                else:
                    # Max retries exceeded, send to DLQ
                    message["reason"] = "max_retries_exceeded"
                    ch.basic_publish(
                        exchange='',
                        routing_key='tasks.dlq',
                        body=json.dumps(message)
                    )
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                # Non-retryable error
                logger.error(f"Non-retryable error: {e}")
                message["reason"] = "non_retryable_error"
                ch.basic_publish(
                    exchange='',
                    routing_key='tasks.dlq',
                    body=json.dumps(message)
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue='tasks',
            on_message_callback=callback
        )
        self.channel.start_consuming()

    def monitor_dlq(self):
        """Monitor DLQ for manual intervention"""
        method, properties, body = self.channel.basic_get('tasks.dlq')
        if method:
            message = json.loads(body)
            logger.critical(f"DLQ Message: {message}")
            # Alert ops team to investigate
```

**DLQ Strategy:**
- Retry with exponential backoff (2s, 4s, 8s, 16s)
- Move to DLQ after max retries
- Monitor DLQ for alert/escalation
- Manual review & replay

### 3.5 Message Ordering Guarantees

**Practice: Ensure Order When Required**

```python
# Kafka: Global ordering per partition
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# All messages with same key go to same partition (ordered)
for order in orders:
    producer.send(
        'orders',
        key=f"customer:{customer_id}".encode(),  # Key = partition assignment
        value=json.dumps(order).encode()
    )

# Consumer reads from partition in order
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    group_id='order-processor'
)

for message in consumer:
    process_order(json.loads(message.value))
```

**Ordering Levels:**
- **No guarantee**: Fastest, suitable for analytics
- **Per-key ordering**: Messages with same key ordered
- **Global ordering**: All messages ordered (slower)

### 3.6 Message Versioning & Schema

**Practice: Schema Registry for Message Evolution**

```python
from confluent_kafka import Producer, Consumer
import avro.io
import avro.schema

# Define schema for user events
user_event_schema = avro.schema.parse(json.dumps({
    "type": "record",
    "name": "UserEvent",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "event_type", "type": "string"},
        {"name": "timestamp", "type": "long"},
        # Optional new field (backwards compatible)
        {"name": "region", "type": ["null", "string"], "default": None}
    ]
}))

# Produce
writer = avro.io.DatumWriter(user_event_schema)
encoder = avro.io.BinaryEncoder(BytesIO())
writer.write(user_event, encoder)

# Consume
reader = avro.io.DatumReader(user_event_schema)
decoder = avro.io.BinaryDecoder(BytesIO(message))
event = reader.read(decoder)
```

**Benefits:**
- Detect incompatible changes
- Document message structure
- Enable safe evolution

### 3.7 Worker Concurrency Optimization

**Practice: Tune Concurrency for Throughput**

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

# I/O-bound tasks: use threads
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = []
    for message in queue:
        future = executor.submit(process_io_task, message)
        futures.append(future)

# CPU-bound tasks: use processes
num_workers = multiprocessing.cpu_count()  # Match CPU cores
with ProcessPoolExecutor(max_workers=num_workers) as executor:
    futures = []
    for message in queue:
        future = executor.submit(process_cpu_task, message)
        futures.append(future)

# Concurrency tuning
config = {
    "num_workers": 10,           # Tune based on load
    "queue_depth": 100,          # Buffer messages
    "batch_size": 20,            # Process multiple messages
    "prefetch_count": 5          # RabbitMQ prefetch
}
```

**Throughput Impact:**
- 1 worker: 100 msg/s
- 5 workers: 450 msg/s (sublinear due to contention)
- 10 workers: 800 msg/s (optimal)
- 20 workers: 850 msg/s (diminishing returns)

### 3.8 Backpressure Handling

**Practice: Prevent Queue Overload (kiểm soát áp lực)**

```python
class AdaptiveConsumer:
    def __init__(self, min_workers=2, max_workers=20):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.current_workers = min_workers

    def monitor_queue_depth(self):
        """Adjust workers based on queue depth"""
        while True:
            queue_depth = self.get_queue_depth()
            processing_rate = self.get_processing_rate()

            # Estimate time to empty
            time_to_empty = queue_depth / processing_rate if processing_rate > 0 else float('inf')

            if time_to_empty > 60:  # More than 1 minute to empty
                # Increase workers
                new_workers = min(self.current_workers + 2, self.max_workers)
                self.scale_workers(new_workers)
                self.current_workers = new_workers

            elif time_to_empty < 10:  # Less than 10 seconds to empty
                # Decrease workers
                new_workers = max(self.current_workers - 1, self.min_workers)
                self.scale_workers(new_workers)
                self.current_workers = new_workers

            time.sleep(30)  # Check every 30 seconds

    def get_queue_depth(self):
        return self.channel.method.message_count

    def get_processing_rate(self):
        # Messages processed per second
        return self.metrics.get_counter('processed_per_sec')
```

### 3.9 Event-Driven Architecture

**Practice: Saga Pattern for Distributed Transactions**

```python
class OrderSaga:
    """Coordinate transaction across multiple services"""

    async def create_order(self, user_id, items):
        order = await self.order_service.create(user_id, items)

        try:
            # Step 1: Reserve inventory (đặt hàng)
            await self.inventory_service.reserve(order.id, items)
            order.status = "reserved"

            # Step 2: Process payment
            await self.payment_service.charge(
                user_id=user_id,
                amount=order.total
            )
            order.status = "paid"

            # Step 3: Ship
            await self.shipping_service.ship(order.id)
            order.status = "shipped"

        except PaymentException:
            # Rollback: Release inventory
            await self.inventory_service.release(order.id)
            order.status = "failed"
            raise

        return order

# Event-based alternative (more resilient)
async def create_order_event_driven(user_id, items):
    # Create order
    order = await order_service.create(user_id, items)

    # Publish event - services react asynchronously
    await event_bus.publish("order.created", {
        "order_id": order.id,
        "items": items
    })

    # Inventory service listens and reserves
    # Payment service listens and charges
    # Shipping service listens and ships
    # If any fails, compensating transaction is published
```

### 3.10 Stream Processing

**Practice: Real-Time Data Processing with Kafka Streams**

```python
from kafka import KafkaConsumer, KafkaProducer
import json
from collections import Counter
from datetime import datetime, timedelta

class StreamProcessor:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['localhost:9092'],
            group_id='analytics'
        )
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092']
        )
        self.window_state = Counter()  # Sliding window state

    def process_stream(self):
        """Real-time analytics on stream"""
        for message in self.consumer:
            event = json.loads(message.value)

            # Window aggregation (5-minute window)
            event['hour'] = event['timestamp'] // 3600
            self.window_state[event['event_type']] += 1

            # Emit aggregated metrics every minute
            if message.offset % 100 == 0:
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "event_counts": dict(self.window_state)
                }
                self.producer.send(
                    'analytics-output',
                    json.dumps(metrics).encode()
                )
```

## 4. Decision Frameworks

### Queue Selection Decision Tree
1. **Need event replay?** → Kafka
2. **Complex routing?** → RabbitMQ
3. **Low operational overhead?** → Redis Streams or SQS
4. **High throughput (1M+ msg/s)?** → Kafka

### Async vs Sync
- **Sync**: When you need result immediately
- **Async**: For operations >100ms, non-blocking preferred

## 5. Checklist

- [ ] Message queue selected for use case
- [ ] Delivery semantics defined (at-most/at-least/exactly-once)
- [ ] Dead letter queue implemented
- [ ] Retry strategy with backoff defined
- [ ] Consumer concurrency optimized
- [ ] Message schema versioned
- [ ] Monitoring (queue depth, lag, errors)
- [ ] Backpressure handling implemented
- [ ] Consumer group coordinated
- [ ] Message ordering guaranteed where needed
- [ ] Idempotency implemented (safe retries)
- [ ] Circuit breaker for downstream services

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| No DLQ | Lost messages forever | Implement DLQ + alerting |
| Unbounded retries | Stuck consumers, memory leak | Set max retry count |
| No idempotency | Duplicate operations, corruption | Make message processing idempotent |
| Sync message processing | Slow API responses | Use async with queues |
| No consumer lag monitoring | Unknown delays & backlog | Track consumer lag |
| Single consumer | No parallelism, bottleneck | Scale consumers horizontally |
| Message ordering ignored | Out-of-order processing | Use message keys for ordering |
| No backpressure | Queue explodes, OOM crashes | Implement adaptive scaling |

## 7. Tools & References

**Message Queues:**
- RabbitMQ, Apache Kafka, Redis Streams, AWS SQS
- Apache Pulsar, NATS, ActiveMQ

**Stream Processing:**
- Kafka Streams, Apache Flink, Spark Streaming
- Redis Streams, Kinesis

**Python Async:**
- asyncio, aiohttp, Celery, RQ, Dramatiq
- concurrent.futures

**Monitoring:**
- Burrow (Kafka consumer lag), Datadog, Prometheus
- CloudWatch, Grafana

**Best Practices:**
- "Enterprise Integration Patterns" (Hohpe & Woolf)
- "The Art of Scalability" (Martin & Eklund)
