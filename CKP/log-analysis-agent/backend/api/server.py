"""
FastAPI Server - REST API for the Log Analysis Agent.
Serves both the analysis backend and the React frontend.
"""
import logging
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config.settings import get_config
from modules.models import (
    AnalysisRequest, AnalysisResponse, Alert, AlertStatus,
)
from modules.ai_agent import LogAnalysisAgent
from modules.datadog_fetcher import DatadogLogFetcher
from modules.sample_data import generate_sample_logs

logger = logging.getLogger(__name__)
config = get_config()

app = FastAPI(
    title="Log Analysis Agent",
    description="AI-powered log analysis for Rancher/K8s containers via Datadog",
    version="1.0.0",
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.cors_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo
_analysis_cache: dict = {}
_alerts_store: List[Alert] = []


# ── Request/Response Models ─────────────────────────────────────

class RunAnalysisRequest(BaseModel):
    time_range_minutes: int = 60
    services: Optional[List[str]] = None
    query: Optional[str] = None
    analysis_type: str = "full"
    trace_id: Optional[str] = None
    use_sample_data: bool = True  # Use sample data if Datadog not configured


class AlertUpdateRequest(BaseModel):
    status: AlertStatus
    note: Optional[str] = None


class AnalysisHistoryItem(BaseModel):
    request_id: str
    timestamp: datetime
    analysis_type: str
    total_logs: int
    total_errors: int
    alert_count: int


# ── API Endpoints ───────────────────────────────────────────────

@app.get("/api/v1/health")
async def health_check():
    """Service health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "datadog_configured": bool(config.datadog.api_key),
        "openai_configured": bool(config.openai.api_key),
    }


@app.post("/api/v1/analysis/run", response_model=AnalysisResponse)
async def run_analysis(request: RunAnalysisRequest):
    """Run a new log analysis."""
    try:
        # Fetch logs
        if request.use_sample_data or not config.datadog.api_key:
            logger.info("Using sample data for analysis")
            logs = generate_sample_logs(
                count=500,
                minutes=request.time_range_minutes,
                error_ratio=0.15,
                include_incident=True,
            )
        else:
            fetcher = DatadogLogFetcher()
            try:
                logs = await fetcher.fetch_error_logs(
                    minutes=request.time_range_minutes,
                    services=request.services,
                    extra_query=request.query,
                )
                # Also fetch non-error logs for metrics
                all_logs = await fetcher.fetch_all_logs(
                    minutes=request.time_range_minutes,
                    services=request.services,
                )
                logs = all_logs  # Use all logs for comprehensive analysis
            finally:
                await fetcher.close()

        if not logs:
            raise HTTPException(status_code=404, detail="No logs found for the given criteria")

        # Run AI analysis (or rule-based if OpenAI not configured)
        if config.openai.api_key:
            agent = LogAnalysisAgent()
            response = await agent.run_full_analysis(
                logs=logs,
                analysis_type=request.analysis_type,
                trace_id=request.trace_id,
            )
        else:
            # Fallback: rule-based analysis without AI
            response = await _run_rule_based_analysis(logs, request)

        # Cache results
        _analysis_cache[response.request_id] = response
        _alerts_store.extend(response.alerts)

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/v1/analysis/{request_id}", response_model=AnalysisResponse)
async def get_analysis(request_id: str):
    """Get a cached analysis result."""
    if request_id not in _analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return _analysis_cache[request_id]


@app.get("/api/v1/analysis/history", response_model=List[AnalysisHistoryItem])
async def get_analysis_history():
    """List all past analyses."""
    items = []
    for req_id, resp in _analysis_cache.items():
        items.append(AnalysisHistoryItem(
            request_id=req_id,
            timestamp=resp.timestamp,
            analysis_type=resp.analysis_type,
            total_logs=resp.metrics.total_logs if resp.metrics else 0,
            total_errors=resp.metrics.total_errors if resp.metrics else 0,
            alert_count=len(resp.alerts),
        ))
    return sorted(items, key=lambda x: x.timestamp, reverse=True)


@app.get("/api/v1/alerts")
async def list_alerts(
    status: Optional[AlertStatus] = None,
    severity: Optional[str] = None,
    service: Optional[str] = None,
):
    """List all alerts with optional filters."""
    alerts = _alerts_store.copy()

    if status:
        alerts = [a for a in alerts if a.status == status]
    if severity:
        alerts = [a for a in alerts if a.severity.value == severity]
    if service:
        alerts = [a for a in alerts if a.service == service]

    return {
        "alerts": [a.model_dump() for a in alerts],
        "total": len(alerts),
        "active": sum(1 for a in _alerts_store if a.status == AlertStatus.ACTIVE),
    }


@app.put("/api/v1/alerts/{alert_id}")
async def update_alert(alert_id: str, request: AlertUpdateRequest):
    """Update an alert status."""
    for alert in _alerts_store:
        if alert.id == alert_id:
            alert.status = request.status
            alert.updated_at = datetime.now(timezone.utc)
            if request.status == AlertStatus.RESOLVED:
                alert.resolved_at = datetime.now(timezone.utc)
            return alert.model_dump()

    raise HTTPException(status_code=404, detail="Alert not found")


@app.get("/api/v1/services")
async def list_services():
    """List monitored services from the latest analysis."""
    if not _analysis_cache:
        return {"services": [], "dependencies": []}

    latest = max(_analysis_cache.values(), key=lambda r: r.timestamp)
    return {
        "services": [s.model_dump() for s in latest.services],
        "dependencies": [d.model_dump() for d in latest.dependencies],
    }


@app.post("/api/v1/demo/generate")
async def generate_demo_data(
    count: int = Query(500, ge=50, le=5000),
    minutes: int = Query(60, ge=5, le=1440),
    error_ratio: float = Query(0.15, ge=0.0, le=1.0),
):
    """Generate sample log data for demo purposes."""
    logs = generate_sample_logs(count=count, minutes=minutes, error_ratio=error_ratio)
    return {
        "generated": len(logs),
        "sample": [l.model_dump() for l in logs[:5]],
        "summary": {
            "total": len(logs),
            "errors": sum(1 for l in logs if l.level.value in ("error", "critical")),
            "services": list({l.service for l in logs}),
        },
    }


# ── Fallback Rule-Based Analysis ────────────────────────────────

async def _run_rule_based_analysis(logs, request) -> AnalysisResponse:
    """Run analysis without AI - uses rule-based tools directly."""
    import uuid
    from tools.analysis_tools import (
        ErrorDetector, ServiceAnalyzer, MetricsAggregator, RootCauseAnalyzer,
    )

    request_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc)

    detector = ErrorDetector()
    svc_analyzer = ServiceAnalyzer()
    metrics_agg = MetricsAggregator()
    rca_analyzer = RootCauseAnalyzer()

    errors = detector.detect_error_patterns(logs)
    services = svc_analyzer.analyze_services(logs)
    dependencies = svc_analyzer.build_dependency_graph(logs)
    metrics = metrics_agg.aggregate_metrics(logs)

    # Build RCA
    timeline = rca_analyzer.build_incident_timeline(logs)
    propagation = rca_analyzer.find_error_propagation(logs)

    from modules.models import RCAReport, AlertSeverity

    rca = RCAReport(
        incident_id=request_id,
        title="Rule-Based Analysis",
        summary=f"Found {len(errors)} error patterns across {len(services)} services. "
                f"Error rate: {metrics.error_rate}%. "
                f"Detected {len(propagation)} cross-service error chains.",
        severity=AlertSeverity.HIGH if metrics.error_rate > 5 else AlertSeverity.MEDIUM,
        started_at=metrics.time_range_start,
        detected_at=now,
        timeline=timeline[:30],
        affected_services=list({s.service_name for s in services if s.health.value != "healthy"}),
        total_errors=metrics.total_errors,
    )

    # Generate alerts
    from modules.models import Alert, AlertStatus
    alerts = []
    for err in errors:
        if err.severity.value in ("critical", "high"):
            alerts.append(Alert(
                id=str(uuid.uuid4())[:8],
                created_at=now,
                title=f"{err.error_type} ({err.count}x)",
                description=err.error_message[:200],
                severity=err.severity,
                service=err.affected_services[0] if err.affected_services else "unknown",
                error_type=err.error_type,
                error_count=err.count,
            ))

    summary = (
        f"## Analysis Summary\n\n"
        f"Analyzed {metrics.total_logs} logs over the past {request.time_range_minutes} minutes.\n\n"
        f"**Key Findings:**\n"
        f"- Error rate: {metrics.error_rate}%\n"
        f"- Total errors: {metrics.total_errors}\n"
        f"- Affected services: {len([s for s in services if s.health.value != 'healthy'])}\n"
        f"- Critical alerts: {len([a for a in alerts if a.severity.value == 'critical'])}\n\n"
        f"**Top Error:**\n"
        f"- {errors[0].error_type}: {errors[0].count} occurrences across {', '.join(errors[0].affected_services)}\n" if errors else ""
    )

    return AnalysisResponse(
        request_id=request_id,
        timestamp=now,
        analysis_type=request.analysis_type,
        metrics=metrics,
        errors=errors,
        alerts=alerts,
        rca=rca,
        services=services,
        dependencies=dependencies,
        ai_summary=summary,
        ai_recommendations=[
            "Investigate connection timeout issues in payment-api → bank-connector",
            "Scale database connection pool for services hitting DB_POOL_EXHAUSTED",
            "Set up circuit breakers for external service calls",
            "Review memory allocation for search-service pods",
            "Configure rate limiting at api-gateway level",
        ],
    )


# ── Main ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host=config.server.host, port=config.server.port)
