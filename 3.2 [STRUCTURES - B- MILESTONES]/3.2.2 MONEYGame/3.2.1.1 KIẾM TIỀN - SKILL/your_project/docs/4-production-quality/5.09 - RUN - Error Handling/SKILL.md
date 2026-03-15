# Error Handling — Production Best Practices

> **Domain:** 5.09 | **Group:** RUN | **Lifecycle:** Run Time
> **Last Updated:** 2026-03-13

---

## 1. Overview

Error handling is the difference between a system that fails silently (worse) and one that fails predictably, debuggably, and recovers gracefully. Production systems must classify errors (transient vs permanent), respond differently to each, and maintain observability even when things go wrong.

**Tiếng Việt:** Xử lý lỗi phân loại các lỗi (tạm thời vs vĩnh viễn), phản hồi khác nhau cho mỗi loại, và duy trì khả năng quan sát khi sự cố xảy ra.

---

## 2. Core Principles

1. **Fail Fast, Fail Loudly** — Don't hide errors; surface them immediately
2. **Classify Errors** — Distinguish transient from permanent; retry-worthy from fatal
3. **Error Budgets** — Same as uptime SLOs; know how many failures you can afford
4. **Partial Failure** — Some requests succeed, some fail; handle both
5. **Observability** — Every error must be traceable (logs, traces, metrics)
6. **User-Facing Errors** — Don't expose stack traces or internal details to users

---

## 3. Best Practices

### 3.1 Error Handling Philosophy

**Fail Fast vs Fail Safe:**
- **Fail Fast:** Detect errors immediately, don't hide in background
  - Example: Validate input at API boundary, return error immediately
  - **Benefit:** Users know immediately, faster debugging

- **Fail Safe:** Continue operation with degraded functionality
  - Example: Cache stale user profile if service down
  - **Benefit:** Better UX, less downtime perceived

**When to use each:**
- **Fail Fast:** Payment processing (wrong amount is worse than no payment)
- **Fail Safe:** Recommendations (stale is better than missing)

---

### 3.2 Error Classification

**Transient Errors (retry-worthy):**
- Network timeout, connection refused
- 503 Service Unavailable, 429 Too Many Requests
- Database connection pool exhausted (temporary)
- **Action:** Retry with exponential backoff

**Permanent Errors (don't retry):**
- 400 Bad Request, 401 Unauthorized, 403 Forbidden
- Invalid JSON, malformed request
- Database constraint violation (duplicate key)
- **Action:** Fail immediately, return error to user

**Example (Classification):**
```python
def should_retry(error):
    transient_status_codes = {408, 429, 500, 502, 503, 504}
    transient_exceptions = (ConnectionError, TimeoutError)

    if isinstance(error, transient_exceptions):
        return True
    if hasattr(error, 'status_code') and error.status_code in transient_status_codes:
        return True
    return False
```

---

### 3.3 Exception Hierarchy Design

**Practice:** Create semantic exception classes for different error types

**Anti-pattern:** Everything inherits from base Exception; can't distinguish at caller

**Good Hierarchy:**
```python
class ApplicationError(Exception):
    """Base for all app errors"""
    pass

class ValidationError(ApplicationError):
    """User input invalid"""
    pass

class TransientError(ApplicationError):
    """Retry-worthy errors"""
    pass

class PermanentError(ApplicationError):
    """Don't retry"""
    pass

class TimeoutError(TransientError):
    """Request took too long"""
    pass

class DatabaseError(TransientError):
    """Database unavailable (transient)"""
    pass

class InvalidCreditCard(PermanentError):
    """Card declined (permanent)"""
    pass
```

---

### 3.4 Error Response Formats (RFC 7807 Problem Details)

**Practice:** Standardize error responses for APIs

**Standard Format:**
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Failed",
  "status": 400,
  "detail": "Field 'email' is invalid: not a valid email address",
  "instance": "/orders/12345",
  "errorCode": "INVALID_EMAIL",
  "timestamp": "2026-03-13T10:30:00Z",
  "traceId": "abc123xyz789"
}
```

**Fields:**
- `type`: URL to documentation about this error class
- `title`: Human-readable error type
- `status`: HTTP status code
- `detail`: Specific error message
- `errorCode`: Machine-readable code for client logic
- `traceId`: For debugging (correlate with logs)

**Anti-pattern:**
```json
{"error": "something went wrong"}  // Useless
```

---

### 3.5 Error Codes Taxonomy

**Create consistent error codes for your system:**

```
AUTH_*         # Authentication/authorization
  AUTH_INVALID_CREDENTIALS
  AUTH_TOKEN_EXPIRED
  AUTH_PERMISSION_DENIED

PAYMENT_*      # Payment errors
  PAYMENT_CARD_DECLINED
  PAYMENT_INSUFFICIENT_FUNDS
  PAYMENT_PROCESSING_ERROR (transient)

VALIDATION_*   # Input validation
  VALIDATION_FIELD_REQUIRED
  VALIDATION_FIELD_INVALID
  VALIDATION_FIELD_OUT_OF_RANGE

INTERNAL_*     # Server errors
  INTERNAL_DATABASE_ERROR (transient)
  INTERNAL_TIMEOUT (transient)
  INTERNAL_SERVER_ERROR
```

**Benefit:** Clients can retry on specific codes intelligently

---

### 3.6 Graceful Error Recovery

**Practice:** Recover from errors without losing state

**Compensation Patterns (Saga Pattern):**
- Order created → Payment processed
- If inventory fails, compensate by reversing payment
- Each step has rollback capability

**Idempotency:**
- Same request twice = same result
- Prevent duplicate charges via idempotency keys

**Example (Idempotent Payment):**
```python
@app.post("/payments")
def process_payment(request: PaymentRequest):
    idempotency_key = request.headers["Idempotency-Key"]

    # Check if already processed
    existing = db.payments.find_one(idempotency_key=idempotency_key)
    if existing:
        return existing.result

    # Process payment
    result = charge_card(request.card, request.amount)
    db.payments.insert(idempotency_key=idempotency_key, result=result)
    return result
```

---

### 3.7 Dead Letter Queues (DLQ)

**Practice:** Handle messages that fail all retries

- **Message Queue:** SQS, RabbitMQ, Kafka
- **Process:** Pull from queue, process, delete on success
- **Failure:** Retry N times with backoff
- **DLQ:** If still failing, move to dead letter queue
- **Manual:** Ops team investigates and processes manually

**Benefit:** Failed messages don't clog main queue; visibility into failures

**Example (AWS SQS):**
```python
from boto3 import client

sqs = client('sqs')

# Configure queue with DLQ
sqs.set_queue_attributes(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/123/main-queue',
    Attributes={
        'RedrivePolicy': json.dumps({
            'deadLetterTargetArn': 'arn:aws:sqs:us-east-1:123:dlq',
            'maxReceiveCount': 3  # Move to DLQ after 3 failures
        })
    }
)
```

---

### 3.8 Error Aggregation & Deduplication

**Practice:** Group similar errors to prevent alert noise

**Aggregation:**
- Same error type from multiple sources → one alert
- "Payment service failing in us-east-1" + "Payment service failing in us-west-2" = one alert

**Deduplication:**
- Don't alert twice on same error
- Use error fingerprint (hash of error type + relevant context)
- Keep hash in alert system to deduplicate

**Benefit:** Reduces alert fatigue; captures true failures

---

### 3.9 User-Facing vs Internal Errors

**Practice:** Never expose stack traces or internal details to users

**User-Facing (Simple, Non-Technical):**
```json
{
  "message": "Your payment couldn't be processed. Please try again or contact support."
}
```

**Internal (Detailed, Debuggable):**
```json
{
  "message": "Payment gateway connection timeout after 30s",
  "exception": "TimeoutError: requests.ConnectionError",
  "stacktrace": "...",
  "context": {"service": "payment-gateway", "attempt": 3}
}
```

**Best Practice:**
- Always log full error with stack trace to internal system
- Return generic message to user, reference trace ID for support team

---

### 3.10 Error Rate Alerting

**Practice:** Alert on error rates, not just error count

**Anti-pattern:** Alert if 10 errors → triggers immediately for small services

**Good:** Alert if 1% of requests failed for 5 minutes
```yaml
alert: HighErrorRate
expr: rate(http_requests_failed[5m]) / rate(http_requests_total[5m]) > 0.01
for: 5m
```

**Considerations:**
- Small services: adjust threshold (0.05 for 1 RPS service)
- Large services: stricter threshold (0.001 for 10k RPS service)

---

### 3.11 Stack Trace Management

**Practice:** Collect stack traces in production, but don't expose them

**Guidelines:**
- Log full stack trace to centralized logging (ELK, Loki)
- Return error code + trace ID to client
- Client includes trace ID in support request
- Support uses trace ID to pull logs and stack trace

**Anti-pattern:** Returning stack trace in HTTP response; exposing code paths to attackers

**Example:**
```python
import traceback
import logging

logger = logging.getLogger(__name__)

def api_endpoint():
    try:
        return process_request()
    except Exception as e:
        trace_id = generate_trace_id()
        logger.error(f"Request failed: {traceback.format_exc()}", extra={"trace_id": trace_id})
        return {"error": "Processing failed", "trace_id": trace_id}, 500
```

---

### 3.12 Panic Recovery (Go/Rust)

**Go — Recover from Panic:**
```go
defer func() {
    if r := recover(); r != nil {
        log.Error("Recovered from panic", "panic", r)
        // Don't crash; log and continue
    }
}()

// Code that might panic
```

**Rust — Error Handling:**
```rust
// Rust forces error handling (no panic recovery)
match risky_operation() {
    Ok(result) => println!("Success: {}", result),
    Err(error) => {
        eprintln!("Error: {}", error);
        // Handle gracefully
    }
}
```

---

### 3.13 Global Exception Handlers

**Practice:** Catch unhandled errors at top level

**Framework Examples:**
```python
# Flask
@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"Unhandled exception: {error}", exc_info=True)
    return {
        "error": "Internal Server Error",
        "trace_id": generate_trace_id()
    }, 500

# Express.js
app.use((error, req, res, next) => {
    logger.error("Unhandled error", {error: error.message, stack: error.stack});
    res.status(500).json({error: "Internal Server Error", traceId: req.id});
});
```

---

### 3.14 Partial Failure Handling in Distributed Systems

**Practice:** Handle cases where some operations succeed, others fail

**Scenario:** User payment succeeds, but email notification fails
- Don't roll back payment (irreversible)
- Retry email with dead letter queue
- Monitor for missing notifications

**Pattern: Eventual Consistency**
- Payment → Queue email task
- Email task fails → Retry later
- Same request twice → Idempotent, so safe

---

### 3.15 Compensation Patterns (Saga)

**Choreography Saga:**
- Service A publishes event "OrderCreated"
- Service B listens, publishes "PaymentProcessed"
- Service C listens, publishes "OrderConfirmed"
- If C fails, B compensates (refund)

**Orchestration Saga:**
- Central orchestrator coordinates steps
- "Order" → "Payment" → "Inventory"
- If inventory fails, orchestrator triggers "RefundPayment" and "CancelOrder"

**Benefit:** Maintains consistency without distributed transactions

---

## 4. Decision Frameworks

**Should I retry this error?**
1. Is it transient? (timeout, 503) → YES
2. Is it idempotent? → YES, retry
3. Is it permanent? (401, 400) → NO
4. Is it partial failure? (email failed but charge succeeded) → Compensate

**Should I expose this error to the user?**
1. Is it user's fault? (bad input) → YES, explain
2. Is it server's fault? (500 error) → NO, show generic message

---

## 5. Checklist

- [ ] Exception hierarchy designed (Transient, Permanent, Validation, etc.)
- [ ] Error responses follow RFC 7807 format
- [ ] Error codes taxonomy documented
- [ ] Error classification implemented (transient vs permanent)
- [ ] Retry logic uses exponential backoff with jitter
- [ ] Idempotency keys supported for critical operations
- [ ] Dead letter queues configured for async operations
- [ ] Error aggregation/deduplication configured
- [ ] Global exception handlers deployed
- [ ] Stack traces logged internally but not exposed to users
- [ ] Error rate alerting (not count-based) configured
- [ ] Compensation/Saga patterns for distributed transactions
- [ ] Partial failure handling documented
- [ ] Error codes returned in API responses

---

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Stack trace in HTTP response | Security risk, confuses users | Return generic message + trace ID |
| Retry non-idempotent ops | Duplicate charges | Add idempotency key check |
| Catch all exceptions as same type | Can't handle differently | Use exception hierarchy |
| Alert on error count | Noisy for low-traffic services | Alert on error rate % |
| No error codes in API | Client can't handle intelligently | Add error code to response |
| Silent failures | Invisible bugs | Log all errors with trace |
| No DLQ for queues | Failed messages clog queue | Add DLQ with reprocess mechanism |
| Retry with no backoff | Thundering herd | Always use exponential backoff |

---

## 7. Tools & References

**Error Tracking:** Sentry, Rollbar, Datadog, Bugsnag
**APM/Tracing:** Jaeger, DataDog, New Relic (includes error tracking)
**Queues:** SQS, RabbitMQ, Kafka (with DLQ support)
**Documentation:** Google SRE Book (Ch. 13: Emergency Response), RFC 7807

---

**Next:** → 5.10 Production Readiness
