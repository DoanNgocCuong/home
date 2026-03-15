"""
Scan Scheduler — The heart of the agent.
Runs every N seconds, orchestrates the 3-tier pipeline.

Flow:
  1. Fetch logs (Datadog API or OTel)
  2. Tier 1: Anomaly Engine (rule-based, $0)
  3. If anomaly → Tier 2: Light LLM (DeepSeek, ~$0.01)
  4. If cascading/critical → Tier 3: Deep LLM (GPT-4o, ~$0.50)
  5. Generate alerts, persist results
"""
import asyncio
import logging
import uuid
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from config.settings import get_config
from modules.models import NormalizedLog, AnalysisResponse, Alert, AlertSeverity, AlertStatus
from modules.anomaly_engine import AnomalyEngine, AnomalyResult
from modules.tiered_llm import TieredLLM
from modules.sample_data import generate_sample_logs
from tools.analysis_tools import ErrorDetector, ServiceAnalyzer, MetricsAggregator, RootCauseAnalyzer

logger = logging.getLogger(__name__)


class ScanScheduler:
    """
    Main orchestrator — runs the 3-tier analysis pipeline on schedule.
    """

    def __init__(self):
        self.config = get_config()
        self.anomaly_engine = AnomalyEngine(
            z_threshold=self.config.agent.anomaly_z_threshold,
            error_rate_warn=self.config.agent.error_rate_warning,
            error_rate_crit=self.config.agent.error_rate_critical,
        )
        self.tiered_llm = TieredLLM()

        # Analysis tools
        self.error_detector = ErrorDetector()
        self.service_analyzer = ServiceAnalyzer()
        self.metrics_aggregator = MetricsAggregator()
        self.rca_analyzer = RootCauseAnalyzer()

        # State
        self._running = False
        self._scan_count = 0
        self._last_result: Optional[AnalysisResponse] = None
        self._history: List[Dict[str, Any]] = []
        self._alerts: List[Alert] = []

    async def start(self):
        """Start the scheduled scanning loop."""
        self._running = True
        interval = self.config.agent.scan_interval_seconds
        logger.info(f"Scan scheduler started. Interval: {interval}s")

        while self._running:
            try:
                await self.run_single_scan()
            except Exception as e:
                logger.error(f"Scan failed: {e}", exc_info=True)

            await asyncio.sleep(interval)

    def stop(self):
        """Stop the scanning loop."""
        self._running = False

    async def run_single_scan(
        self,
        force_sample: Optional[bool] = None,
        time_range_minutes: int = 0,
    ) -> AnalysisResponse:
        """
        Run a single scan cycle through the 3-tier pipeline.
        Can be called manually or by the scheduler.
        """
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        self._scan_count += 1

        minutes = time_range_minutes or (self.config.agent.scan_interval_seconds // 60) or 5
        use_sample = force_sample if force_sample is not None else self.config.agent.use_sample_data

        logger.info(f"═══ Scan #{self._scan_count} [req:{request_id}] ═══")

        # ──────────────────────────────────────────────────────
        # STEP 1: Fetch logs
        # ──────────────────────────────────────────────────────
        if use_sample or not self.config.datadog.enabled:
            logs = generate_sample_logs(
                count=self.config.agent.max_logs_per_analysis,
                minutes=minutes,
                error_ratio=0.12,
                include_incident=self._scan_count % 5 == 0,  # Incident every 5th scan
            )
            logger.info(f"Generated {len(logs)} sample logs")
        else:
            # Pull from Datadog
            from modules.datadog_fetcher import DatadogLogFetcher
            fetcher = DatadogLogFetcher()
            try:
                logs = await fetcher.fetch_all_logs(minutes=minutes)
            finally:
                await fetcher.close()

        if not logs:
            logger.info("No logs found, skipping analysis")
            return self._empty_response(request_id)

        # ──────────────────────────────────────────────────────
        # STEP 2: TIER 1 — Anomaly Detection ($0)
        # ──────────────────────────────────────────────────────
        logger.info(f"Tier 1: Analyzing {len(logs)} logs...")
        anomaly_result = self.anomaly_engine.analyze(logs)

        tier_used = 1
        tier2_result = None
        tier3_result = None
        llm_tokens = 0
        llm_cost = 0.0

        logger.info(
            f"Tier 1 result: anomaly={anomaly_result.is_anomaly}, "
            f"severity={anomaly_result.severity}, tier_needed={anomaly_result.tier_needed}"
        )

        # ──────────────────────────────────────────────────────
        # STEP 3: TIER 2 — Light LLM (if anomaly detected)
        # ──────────────────────────────────────────────────────
        if anomaly_result.tier_needed >= 2:
            logger.info(f"Tier 2: Escalating to {self.config.llm.tier2_model}...")
            tier2_result = await self.tiered_llm.run_tier2(anomaly_result, logs)
            tier_used = 2

            meta = tier2_result.get("_meta", {})
            llm_tokens += meta.get("tokens", 0)
            llm_cost += meta.get("cost_usd", 0)

            logger.info(
                f"Tier 2 result: severity={tier2_result.get('severity')}, "
                f"escalate={tier2_result.get('should_escalate')}, "
                f"tokens={meta.get('tokens', 0)}, cost=${meta.get('cost_usd', 0):.4f}"
            )

        # ──────────────────────────────────────────────────────
        # STEP 4: TIER 3 — Deep RCA (if critical/cascading)
        # ──────────────────────────────────────────────────────
        should_tier3 = (
            anomaly_result.tier_needed >= 3
            or (tier2_result and tier2_result.get("should_escalate"))
        )

        if should_tier3:
            logger.info(f"Tier 3: Deep RCA with {self.config.llm.tier3_model}...")
            tier3_result = await self.tiered_llm.run_tier3(anomaly_result, logs, tier2_result)
            tier_used = 3

            meta = tier3_result.get("_meta", {})
            llm_tokens += meta.get("tokens", 0)
            llm_cost += meta.get("cost_usd", 0)

            logger.info(
                f"Tier 3 result: severity={tier3_result.get('severity')}, "
                f"tokens={meta.get('tokens', 0)}, cost=${meta.get('cost_usd', 0):.4f}"
            )

        # ──────────────────────────────────────────────────────
        # STEP 5: Build response + generate alerts
        # ──────────────────────────────────────────────────────
        duration_ms = int((time.time() - start_time) * 1000)

        response = self._build_response(
            request_id=request_id,
            logs=logs,
            anomaly_result=anomaly_result,
            tier2_result=tier2_result,
            tier3_result=tier3_result,
            tier_used=tier_used,
            llm_tokens=llm_tokens,
            llm_cost=llm_cost,
            duration_ms=duration_ms,
        )

        self._last_result = response
        self._history.append({
            "request_id": request_id,
            "timestamp": response.timestamp.isoformat(),
            "tier_used": tier_used,
            "is_anomaly": anomaly_result.is_anomaly,
            "severity": anomaly_result.severity,
            "total_logs": len(logs),
            "total_errors": anomaly_result.metrics.get("total_errors", 0),
            "error_rate": anomaly_result.metrics.get("error_rate", 0),
            "llm_tokens": llm_tokens,
            "llm_cost": llm_cost,
            "duration_ms": duration_ms,
        })

        # Keep last 100 scans
        self._history = self._history[-100:]

        logger.info(
            f"═══ Scan #{self._scan_count} complete: "
            f"tier={tier_used}, anomaly={anomaly_result.is_anomaly}, "
            f"tokens={llm_tokens}, cost=${llm_cost:.4f}, "
            f"duration={duration_ms}ms ═══"
        )

        return response

    def _build_response(
        self,
        request_id: str,
        logs: List[NormalizedLog],
        anomaly_result: AnomalyResult,
        tier2_result: Optional[Dict],
        tier3_result: Optional[Dict],
        tier_used: int,
        llm_tokens: int,
        llm_cost: float,
        duration_ms: int,
    ) -> AnalysisResponse:
        """Build unified AnalysisResponse from all tiers."""
        now = datetime.now(timezone.utc)

        # Compute metrics
        metrics = self.metrics_aggregator.aggregate_metrics(logs)

        # Error patterns
        errors = self.error_detector.detect_error_patterns(logs)

        # Service analysis
        services = self.service_analyzer.analyze_services(logs)
        dependencies = self.service_analyzer.build_dependency_graph(logs)

        # RCA
        from modules.models import RCAReport, RCATimelineEvent, RootCauseHypothesis
        rca = None

        if tier3_result and "root_cause" in tier3_result:
            rc = tier3_result["root_cause"]
            timeline_events = []
            for evt in tier3_result.get("timeline", []):
                try:
                    timeline_events.append(RCATimelineEvent(
                        timestamp=now,
                        service=evt.get("service", "unknown"),
                        event_type="error",
                        description=evt.get("event", ""),
                        severity=AlertSeverity.HIGH,
                    ))
                except Exception:
                    pass

            hypotheses = [RootCauseHypothesis(
                hypothesis=rc.get("description", ""),
                confidence=rc.get("confidence", 0.5),
                supporting_evidence=[],
                affected_services=tier3_result.get("impact", {}).get("affected_services", []),
                error_propagation_chain=tier3_result.get("error_chain", []),
            )]

            rca = RCAReport(
                incident_id=request_id,
                title=tier3_result.get("summary", "Incident Analysis")[:200],
                summary=tier3_result.get("summary", ""),
                severity=AlertSeverity.CRITICAL if tier3_result.get("severity") == "critical" else AlertSeverity.HIGH,
                started_at=min(l.timestamp for l in logs),
                detected_at=now,
                timeline=timeline_events,
                root_causes=hypotheses,
                recommendations=[r.get("action", r) if isinstance(r, dict) else r for r in tier3_result.get("remediation", [])],
                affected_services=tier3_result.get("impact", {}).get("affected_services", []),
                total_errors=anomaly_result.metrics.get("total_errors", 0),
            )
        elif anomaly_result.is_anomaly:
            # Basic RCA from tier 1
            timeline = self.rca_analyzer.build_incident_timeline(logs)
            rca = RCAReport(
                incident_id=request_id,
                title="Anomaly Detected",
                summary=anomaly_result.summary,
                severity=AlertSeverity.WARNING,
                started_at=min(l.timestamp for l in logs),
                detected_at=now,
                timeline=timeline[:20],
                affected_services=list({a.get("service", "") for a in anomaly_result.anomalies if a.get("service")}),
                total_errors=anomaly_result.metrics.get("total_errors", 0),
            )

        # Generate alerts
        alerts = self._generate_alerts(anomaly_result, tier2_result, tier3_result, now)
        self._alerts.extend(alerts)
        self._alerts = self._alerts[-200:]  # Keep last 200

        # Build summary
        summary_parts = [f"## Scan Result (Tier {tier_used})"]
        summary_parts.append(anomaly_result.summary)

        if tier2_result:
            summary_parts.append(f"\n### AI Classification (Tier 2 — {self.config.llm.tier2_model})")
            summary_parts.append(tier2_result.get("summary", ""))

        if tier3_result:
            summary_parts.append(f"\n### Deep RCA (Tier 3 — {self.config.llm.tier3_model})")
            summary_parts.append(tier3_result.get("summary", ""))

        summary_parts.append(f"\n---\nTokens: {llm_tokens} | Cost: ${llm_cost:.4f} | Duration: {duration_ms}ms")

        # Recommendations
        recommendations = []
        if tier3_result:
            for r in tier3_result.get("remediation", []):
                if isinstance(r, dict):
                    recommendations.append(f"[P{r.get('priority', '?')}] {r.get('action', '')} ({r.get('service', '')})")
                else:
                    recommendations.append(str(r))
            for p in tier3_result.get("prevention", []):
                recommendations.append(f"[Prevention] {p}")
        elif tier2_result and tier2_result.get("should_escalate"):
            recommendations.append("Manual investigation recommended — AI escalation triggered")

        return AnalysisResponse(
            request_id=request_id,
            timestamp=now,
            analysis_type=f"tier{tier_used}",
            metrics=metrics,
            errors=errors,
            alerts=alerts,
            rca=rca,
            services=services,
            dependencies=dependencies,
            ai_summary="\n".join(summary_parts),
            ai_recommendations=recommendations,
        )

    def _generate_alerts(
        self,
        anomaly: AnomalyResult,
        tier2: Optional[Dict],
        tier3: Optional[Dict],
        now: datetime,
    ) -> List[Alert]:
        """Generate alerts from analysis results."""
        alerts = []

        if not anomaly.is_anomaly:
            return alerts

        # Main alert
        title = "Anomaly Detected"
        description = anomaly.summary
        severity = AlertSeverity.WARNING

        if tier2:
            title = tier2.get("alert_title", title)
            sev_map = {"critical": AlertSeverity.CRITICAL, "high": AlertSeverity.HIGH, "warning": AlertSeverity.WARNING}
            severity = sev_map.get(tier2.get("severity", ""), severity)

        if tier3:
            rc = tier3.get("root_cause", {})
            title = f"RCA: {rc.get('description', 'Incident')[:100]}"
            description = tier3.get("summary", description)
            severity = AlertSeverity.CRITICAL if tier3.get("severity") == "critical" else AlertSeverity.HIGH

        service = "multiple"
        for a in anomaly.anomalies:
            if a.get("service"):
                service = a["service"]
                break

        alerts.append(Alert(
            id=str(uuid.uuid4())[:8],
            created_at=now,
            title=title,
            description=description[:500],
            severity=severity,
            service=service,
            error_count=anomaly.metrics.get("total_errors", 0),
            error_rate=anomaly.metrics.get("error_rate"),
        ))

        return alerts

    def _empty_response(self, request_id: str) -> AnalysisResponse:
        from modules.models import MetricsSnapshot
        now = datetime.now(timezone.utc)
        return AnalysisResponse(
            request_id=request_id,
            timestamp=now,
            analysis_type="empty",
            metrics=MetricsSnapshot(
                time_range_start=now, time_range_end=now,
                total_logs=0, total_errors=0, error_rate=0,
                avg_response_time_ms=0, p50_latency_ms=0, p95_latency_ms=0, p99_latency_ms=0,
            ),
            ai_summary="No logs found in the specified time range.",
        )

    # ── Public State Access ──────────────────────────────────

    @property
    def last_result(self) -> Optional[AnalysisResponse]:
        return self._last_result

    @property
    def alerts(self) -> List[Alert]:
        return self._alerts

    @property
    def history(self) -> List[Dict]:
        return self._history

    @property
    def scan_count(self) -> int:
        return self._scan_count

    def get_cost_summary(self) -> Dict:
        """Get LLM cost summary."""
        llm_stats = self.tiered_llm.get_stats()
        tier1_scans = sum(1 for h in self._history if h.get("tier_used") == 1)
        tier2_scans = sum(1 for h in self._history if h.get("tier_used") == 2)
        tier3_scans = sum(1 for h in self._history if h.get("tier_used") == 3)

        return {
            "total_scans": self._scan_count,
            "tier1_scans": tier1_scans,
            "tier2_scans": tier2_scans,
            "tier3_scans": tier3_scans,
            "tier1_pct": round(tier1_scans / max(self._scan_count, 1) * 100, 1),
            "tier2_pct": round(tier2_scans / max(self._scan_count, 1) * 100, 1),
            "tier3_pct": round(tier3_scans / max(self._scan_count, 1) * 100, 1),
            **llm_stats,
            "savings_vs_always_tier3": f"${(self._scan_count * 0.50 - llm_stats['total_cost']):.2f}",
        }
