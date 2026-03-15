"""
OpenTelemetry setup for distributed tracing and metrics.

Best Practices:
- Initialize tracing early in app lifecycle
- Add trace context to all requests
- Export to observability platform (Datadog, Jaeger, etc.)
- Use instrumented libraries where available
"""

from contextlib import asynccontextmanager
from typing import Any

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from app.core.config import get_settings


def setup_telemetry(app: Any = None) -> None:
    """
    Initialize OpenTelemetry tracing and metrics.

    Args:
        app: Optional FastAPI app to instrument
    """
    settings = get_settings()

    # Create resource with service name
    resource = Resource(attributes={
        SERVICE_NAME: settings.APP_NAME,
        "service.version": settings.APP_VERSION,
        "deployment.environment": settings.ENVIRONMENT,
    })

    # Configure tracing
    tracer_provider = TracerProvider(resource=resource)

    # Add exporters based on environment
    if settings.ENVIRONMENT == "development":
        # Console exporter for local dev
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        # OTLP exporter for production (Datadog, Jaeger, etc.)
        # In production, configure with actual OTLP endpoint
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://localhost:4317",  # Configure for your OTLP collector
            insecure=True,
        )
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    trace.set_tracer_provider(tracer_provider)

    # Configure metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint="http://localhost:4317",
            insecure=True,
        )
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    # Instrument FastAPI if provided
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)


def get_tracer(name: str = "app") -> trace.Tracer:
    """
    Get a tracer for creating spans.

    Usage:
        tracer = get_tracer("api")
        with tracer.start_as_current_span("request") as span:
            span.set_attribute("http.method", "GET")
            # ... do work
    """
    return trace.get_tracer(name)


# ============== Common Span Attributes ==============

class SpanAttributes:
    """Standard OpenTelemetry attribute keys."""

    # HTTP
    HTTP_METHOD = "http.method"
    HTTP_URL = "http.url"
    HTTP_STATUS_CODE = "http.status_code"
    HTTP_REQUEST_CONTENT_LENGTH = "http.request.content_length"
    HTTP_RESPONSE_CONTENT_LENGTH = "http.response.content_length"

    # Database
    DB_SYSTEM = "db.system"
    DB_STATEMENT = "db.statement"
    DB_OPERATION = "db.operation"

    # LLM (Langfuse/OpenAI)
    LLM_MODEL = "llm.model"
    LLM_REQUEST_TOKENS = "llm.request.tokens"
    LLM_RESPONSE_TOKENS = "llm.response.tokens"
    LLM_TOTAL_TOKENS = "llm.total_tokens"

    # Custom
    USER_ID = "user.id"
    REQUEST_ID = "request.id"
    TRACE_ID = "trace.id"


@asynccontextmanager
async def traced_async_context(tracer_name: str = "app", span_name: str = "operation"):
    """
    Context manager for creating spans in async code.

    Usage:
        async with traced_async_context("api", "process_request"):
            await do_work()
    """
    tracer = get_tracer(tracer_name)
    with tracer.start_as_current_span(span_name) as span:
        yield span
