"""
Sample Data Generator for demo/testing.
Generates realistic container log data mimicking Rancher/K8s deployments.
"""
import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from modules.models import (
    NormalizedLog, LogLevel, TraceContext, HttpInfo, KubernetesInfo
)

# ── Service definitions ─────────────────────────────────────────

SERVICES = [
    {"name": "api-gateway", "deps": ["order-api", "user-api", "product-api"]},
    {"name": "order-api", "deps": ["payment-api", "inventory-api", "notification-api"]},
    {"name": "payment-api", "deps": ["bank-connector", "fraud-detector"]},
    {"name": "user-api", "deps": ["auth-service", "profile-db"]},
    {"name": "product-api", "deps": ["search-service", "product-db"]},
    {"name": "inventory-api", "deps": ["warehouse-api", "inventory-db"]},
    {"name": "notification-api", "deps": ["email-service", "sms-service"]},
    {"name": "auth-service", "deps": ["redis-session"]},
    {"name": "search-service", "deps": ["elasticsearch"]},
    {"name": "bank-connector", "deps": []},
]

ERROR_SCENARIOS = [
    {
        "type": "ConnectionTimeoutException",
        "message": "Connection to {service} timed out after 30000ms",
        "code": "CONN_TIMEOUT",
        "services": ["payment-api", "bank-connector"],
        "weight": 30,
    },
    {
        "type": "DatabaseConnectionPoolExhausted",
        "message": "Cannot acquire connection from pool. Active: {active}/Max: 50",
        "code": "DB_POOL_EXHAUSTED",
        "services": ["order-api", "user-api", "product-api"],
        "weight": 20,
    },
    {
        "type": "OutOfMemoryError",
        "message": "Java heap space exhausted. Used: {used}MB / Max: 512MB",
        "code": "OOM",
        "services": ["search-service", "order-api"],
        "weight": 5,
    },
    {
        "type": "NullPointerException",
        "message": "Cannot invoke method on null object at {location}",
        "code": "NPE",
        "services": ["api-gateway", "order-api", "user-api"],
        "weight": 15,
    },
    {
        "type": "RateLimitExceeded",
        "message": "Rate limit exceeded: {current}/{limit} requests per minute",
        "code": "RATE_LIMIT",
        "services": ["api-gateway", "payment-api"],
        "weight": 10,
    },
    {
        "type": "ServiceUnavailable",
        "message": "{service} returned 503: Service temporarily unavailable",
        "code": "SVC_UNAVAILABLE",
        "services": ["payment-api", "notification-api", "bank-connector"],
        "weight": 10,
    },
    {
        "type": "SSLHandshakeException",
        "message": "SSL handshake failed with {service}: certificate expired",
        "code": "SSL_ERROR",
        "services": ["bank-connector"],
        "weight": 5,
    },
    {
        "type": "KafkaProducerException",
        "message": "Failed to send message to topic {topic}: broker not available",
        "code": "KAFKA_ERROR",
        "services": ["order-api", "notification-api"],
        "weight": 5,
    },
]

STACK_TRACES = {
    "ConnectionTimeoutException": """java.net.SocketTimeoutException: Connect timed out
\tat sun.nio.ch.NioSocketImpl.timedFinishConnect(NioSocketImpl.java:546)
\tat com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:466)
\tat com.example.service.PaymentClient.processPayment(PaymentClient.java:123)
\tat com.example.controller.OrderController.createOrder(OrderController.java:87)""",
    "DatabaseConnectionPoolExhausted": """com.zaxxer.hikari.pool.HikariPool$PoolEntryCreator
\tat com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:443)
\tat com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:128)
\tat org.springframework.jdbc.datasource.DataSourceUtils.fetchConnection(DataSourceUtils.java:159)
\tat com.example.repository.OrderRepository.findById(OrderRepository.java:45)""",
    "OutOfMemoryError": """java.lang.OutOfMemoryError: Java heap space
\tat java.util.Arrays.copyOf(Arrays.java:3210)
\tat com.example.service.SearchService.indexDocuments(SearchService.java:234)
\tat com.example.scheduler.ReindexJob.execute(ReindexJob.java:56)""",
    "NullPointerException": """java.lang.NullPointerException
\tat com.example.service.UserService.getUserProfile(UserService.java:89)
\tat com.example.controller.UserController.getProfile(UserController.java:34)
\tat org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:897)""",
}

ENDPOINTS = [
    "/api/v1/orders", "/api/v1/orders/{id}", "/api/v1/orders/{id}/pay",
    "/api/v1/users/{id}", "/api/v1/users/{id}/profile",
    "/api/v1/products", "/api/v1/products/search",
    "/api/v1/inventory/{id}", "/api/v1/notifications/send",
    "/api/v1/auth/login", "/api/v1/auth/token/refresh",
    "/health", "/ready",
]


def generate_sample_logs(
    count: int = 500,
    minutes: int = 60,
    error_ratio: float = 0.15,
    include_incident: bool = True,
) -> List[NormalizedLog]:
    """Generate realistic sample logs for demo."""
    logs = []
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)

    # Generate base trace IDs for correlated requests
    trace_ids = [uuid.uuid4().hex[:32] for _ in range(count // 3)]

    # If incident, create a concentrated error burst
    incident_start = start + timedelta(minutes=random.randint(20, 40))
    incident_duration = timedelta(minutes=random.randint(5, 15))
    incident_trace_ids = [uuid.uuid4().hex[:32] for _ in range(20)]

    for i in range(count):
        # Random timestamp within range
        ts = start + timedelta(seconds=random.uniform(0, minutes * 60))

        # Determine if this is an error log
        is_incident_window = include_incident and incident_start <= ts <= incident_start + incident_duration
        is_error = random.random() < (0.6 if is_incident_window else error_ratio)

        # Pick service
        svc = random.choice(SERVICES)
        service_name = svc["name"]

        # Pick trace
        if is_incident_window:
            trace_id = random.choice(incident_trace_ids)
        else:
            trace_id = random.choice(trace_ids)

        span_id = uuid.uuid4().hex[:16]

        if is_error:
            # Pick error scenario
            scenario = _weighted_choice(ERROR_SCENARIOS)
            if scenario["services"]:
                service_name = random.choice(scenario["services"])
                svc = next((s for s in SERVICES if s["name"] == service_name), svc)

            error_type = scenario["type"]
            error_msg = scenario["message"].format(
                service=random.choice(svc["deps"]) if svc["deps"] else "external",
                active=random.randint(45, 50),
                used=random.randint(480, 512),
                limit=1000,
                current=random.randint(1001, 1500),
                location=f"Line {random.randint(50, 300)}",
                topic=f"orders-{random.choice(['created', 'updated', 'cancelled'])}",
            )
            level = random.choice([LogLevel.ERROR, LogLevel.ERROR, LogLevel.ERROR, LogLevel.CRITICAL])
            status_code = random.choice([500, 502, 503, 504, 408, 429])
            response_time = random.uniform(5000, 30000)
            stack_trace = STACK_TRACES.get(error_type, "")
        else:
            error_type = None
            error_msg = None
            level = random.choice([LogLevel.INFO, LogLevel.INFO, LogLevel.INFO, LogLevel.WARNING])
            status_code = random.choice([200, 200, 200, 201, 204, 301, 404])
            response_time = random.uniform(10, 500) if random.random() > 0.3 else random.uniform(500, 2000)
            stack_trace = None

        endpoint = random.choice(ENDPOINTS)
        method = random.choice(["GET", "GET", "POST", "PUT", "DELETE"])
        called_service = random.choice(svc["deps"]) if svc["deps"] and random.random() > 0.5 else None

        # Pod name
        pod_suffix = uuid.uuid4().hex[:6]
        pod_name = f"{service_name}-deployment-{pod_suffix}"

        message = error_msg if is_error else f"{method} {endpoint} -> {status_code} ({response_time:.0f}ms)"

        log = NormalizedLog(
            id=str(uuid.uuid4())[:12],
            timestamp=ts,
            level=level,
            service=service_name,
            message=message,
            host=f"rancher-worker-{random.randint(1, 5):02d}",
            error_type=error_type,
            error_code=scenario["code"] if is_error else None,
            error_message=error_msg,
            stack_trace=stack_trace,
            trace=TraceContext(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=uuid.uuid4().hex[:16] if random.random() > 0.3 else None,
            ),
            http=HttpInfo(
                method=method,
                status_code=status_code,
                response_time_ms=round(response_time, 1),
                url=f"http://{service_name}.production.svc.cluster.local{endpoint}",
                path=endpoint,
            ),
            kubernetes=KubernetesInfo(
                cluster_name="prod-rancher-01",
                namespace="production",
                pod_name=pod_name,
                pod_id=str(uuid.uuid4()),
                container_name=service_name,
                container_id=uuid.uuid4().hex[:12],
                node_name=f"rancher-worker-{random.randint(1, 5):02d}",
                docker_image=f"registry.internal/{service_name}:v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,20)}",
            ),
            attributes={
                "called_service": called_service,
                "environment": "production",
                "version": f"v{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,20)}",
            },
        )
        logs.append(log)

    # Sort by timestamp
    logs.sort(key=lambda l: l.timestamp)
    return logs


def _weighted_choice(items: List[dict]) -> dict:
    """Select an item based on weight."""
    total = sum(item["weight"] for item in items)
    r = random.uniform(0, total)
    cumulative = 0
    for item in items:
        cumulative += item["weight"]
        if r <= cumulative:
            return item
    return items[-1]
