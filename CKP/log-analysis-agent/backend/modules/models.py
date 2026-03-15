"""
Data models for the Log Analysis Agent.
Pydantic models for structured data throughout the pipeline.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SNOOZED = "snoozed"


class ServiceHealth(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


# ── Log Models ─────────────────────────────────────────────────────

class TraceContext(BaseModel):
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    parent_span_id: Optional[str] = None


class HttpInfo(BaseModel):
    method: Optional[str] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    url: Optional[str] = None
    path: Optional[str] = None


class KubernetesInfo(BaseModel):
    cluster_name: Optional[str] = None
    namespace: Optional[str] = None
    pod_name: Optional[str] = None
    pod_id: Optional[str] = None
    container_name: Optional[str] = None
    container_id: Optional[str] = None
    node_name: Optional[str] = None
    docker_image: Optional[str] = None


class NormalizedLog(BaseModel):
    """Normalized log entry from Datadog."""
    id: str
    timestamp: datetime
    level: LogLevel
    service: str
    message: str
    host: Optional[str] = None

    # Error details
    error_type: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None

    # Context
    trace: TraceContext = Field(default_factory=TraceContext)
    http: HttpInfo = Field(default_factory=HttpInfo)
    kubernetes: KubernetesInfo = Field(default_factory=KubernetesInfo)

    # Raw attributes
    attributes: Dict[str, Any] = Field(default_factory=dict)


# ── Analysis Models ────────────────────────────────────────────────

class ErrorPattern(BaseModel):
    """Detected error pattern from log analysis."""
    error_type: str
    error_message: str
    count: int
    first_seen: datetime
    last_seen: datetime
    affected_services: List[str]
    severity: AlertSeverity
    sample_log_ids: List[str] = Field(default_factory=list)
    trend: str = "stable"  # "increasing", "decreasing", "stable", "spike"


class ServiceStatus(BaseModel):
    """Health status for a single service."""
    service_name: str
    health: ServiceHealth
    error_rate: float  # percentage
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    request_count: int
    error_count: int
    top_errors: List[ErrorPattern] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)


class ServiceDependency(BaseModel):
    """Dependency link between services."""
    source: str
    target: str
    call_count: int
    error_count: int
    avg_latency_ms: float


class TimeSeriesPoint(BaseModel):
    """A single data point in time series."""
    timestamp: datetime
    value: float
    label: Optional[str] = None


class MetricsSnapshot(BaseModel):
    """Aggregated metrics for a time period."""
    time_range_start: datetime
    time_range_end: datetime
    total_logs: int
    total_errors: int
    error_rate: float
    avg_response_time_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate_trend: List[TimeSeriesPoint] = Field(default_factory=list)
    latency_trend: List[TimeSeriesPoint] = Field(default_factory=list)
    top_errors: List[ErrorPattern] = Field(default_factory=list)
    services: List[ServiceStatus] = Field(default_factory=list)


# ── Root Cause Analysis Models ─────────────────────────────────────

class RCATimelineEvent(BaseModel):
    """Event in the RCA timeline."""
    timestamp: datetime
    service: str
    event_type: str  # "error", "latency_spike", "deployment", "config_change"
    description: str
    severity: AlertSeverity
    related_trace_ids: List[str] = Field(default_factory=list)


class RootCauseHypothesis(BaseModel):
    """Root cause analysis hypothesis."""
    hypothesis: str
    confidence: float  # 0.0 - 1.0
    supporting_evidence: List[str]
    affected_services: List[str]
    error_propagation_chain: List[str]  # service chain: ["db", "payment-api", "order-api"]


class RCAReport(BaseModel):
    """Complete Root Cause Analysis report."""
    incident_id: str
    title: str
    summary: str
    severity: AlertSeverity
    started_at: datetime
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    timeline: List[RCATimelineEvent] = Field(default_factory=list)
    root_causes: List[RootCauseHypothesis] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    total_errors: int = 0
    impacted_users: Optional[int] = None


# ── Alert Models ───────────────────────────────────────────────────

class Alert(BaseModel):
    """Alert generated by the analysis agent."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.ACTIVE
    service: str
    error_type: Optional[str] = None
    error_count: int = 0
    error_rate: Optional[float] = None
    related_trace_ids: List[str] = Field(default_factory=list)
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    snooze_until: Optional[datetime] = None


# ── API Response Models ────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    """Request to run log analysis."""
    time_range_minutes: int = 60
    services: Optional[List[str]] = None
    query: Optional[str] = None
    analysis_type: str = "full"  # "errors", "metrics", "rca", "full"
    incident_trace_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response from log analysis."""
    request_id: str
    timestamp: datetime
    analysis_type: str
    metrics: Optional[MetricsSnapshot] = None
    errors: List[ErrorPattern] = Field(default_factory=list)
    alerts: List[Alert] = Field(default_factory=list)
    rca: Optional[RCAReport] = None
    services: List[ServiceStatus] = Field(default_factory=list)
    dependencies: List[ServiceDependency] = Field(default_factory=list)
    ai_summary: str = ""
    ai_recommendations: List[str] = Field(default_factory=list)
