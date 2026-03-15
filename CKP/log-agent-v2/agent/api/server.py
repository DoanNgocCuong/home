"""
FastAPI Server v2 — REST API for the 3-Tier Log Analysis Agent.
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import get_config
from modules.models import AnalysisResponse, AlertStatus
from modules.scan_scheduler import ScanScheduler

logger = logging.getLogger(__name__)
config = get_config()

scheduler = ScanScheduler()
_scheduler_task: Optional[asyncio.Task] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start/stop the scan scheduler with the app."""
    global _scheduler_task
    logger.info("Starting scan scheduler in background...")
    _scheduler_task = asyncio.create_task(scheduler.start())
    yield
    scheduler.stop()
    if _scheduler_task:
        _scheduler_task.cancel()


app = FastAPI(
    title="Log Analysis Agent v2",
    description="3-Tier AI Log Analysis: Rule-based → DeepSeek → GPT-4o",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ───────────────────────────────────────────────────

class RunAnalysisRequest(BaseModel):
    time_range_minutes: int = 60
    services: Optional[List[str]] = None
    use_sample_data: Optional[bool] = None


class AlertUpdateRequest(BaseModel):
    status: AlertStatus
    note: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────

@app.get("/api/v1/health")
async def health():
    cost = scheduler.get_cost_summary()
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "architecture": "3-tier",
        "scan_count": scheduler.scan_count,
        "scheduler_running": scheduler._running,
        "datadog_enabled": config.datadog.enabled,
        "tier2_model": config.llm.tier2_model if config.llm.tier2_enabled else "disabled",
        "tier3_model": config.llm.tier3_model if config.llm.tier3_enabled else "disabled",
        "langfuse_enabled": config.langfuse.enabled,
        "total_llm_cost": f"${cost['total_cost']:.4f}",
    }


@app.post("/api/v1/analysis/run", response_model=AnalysisResponse)
async def run_analysis(request: RunAnalysisRequest):
    """Manually trigger a single analysis scan."""
    try:
        result = await scheduler.run_single_scan(
            force_sample=request.use_sample_data,
            time_range_minutes=request.time_range_minutes,
        )
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(500, detail=str(e))


@app.get("/api/v1/analysis/latest", response_model=Optional[AnalysisResponse])
async def get_latest():
    """Get the latest analysis result."""
    if scheduler.last_result:
        return scheduler.last_result
    raise HTTPException(404, "No analysis has been run yet")


@app.get("/api/v1/analysis/history")
async def get_history():
    """Get scan history with tier usage and cost."""
    return {
        "scans": scheduler.history,
        "total": len(scheduler.history),
    }


@app.get("/api/v1/cost")
async def get_cost():
    """Get LLM cost summary — the money question."""
    return scheduler.get_cost_summary()


@app.get("/api/v1/baselines")
async def get_baselines():
    """Get current anomaly baselines."""
    return scheduler.anomaly_engine.get_baselines_summary()


@app.get("/api/v1/alerts")
async def list_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
):
    alerts = scheduler.alerts
    if status:
        alerts = [a for a in alerts if a.status.value == status]
    if severity:
        alerts = [a for a in alerts if a.severity.value == severity]

    return {
        "alerts": [a.model_dump() for a in alerts],
        "total": len(alerts),
        "active": sum(1 for a in scheduler.alerts if a.status == AlertStatus.ACTIVE),
    }


@app.put("/api/v1/alerts/{alert_id}")
async def update_alert(alert_id: str, request: AlertUpdateRequest):
    for alert in scheduler.alerts:
        if alert.id == alert_id:
            alert.status = request.status
            alert.updated_at = datetime.now(timezone.utc)
            return alert.model_dump()
    raise HTTPException(404, "Alert not found")


@app.get("/api/v1/services")
async def list_services():
    if not scheduler.last_result:
        return {"services": [], "dependencies": []}
    r = scheduler.last_result
    return {
        "services": [s.model_dump() for s in r.services],
        "dependencies": [d.model_dump() for d in r.dependencies],
    }


# ── Main ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    uvicorn.run(app, host=config.server.host, port=config.server.port)
