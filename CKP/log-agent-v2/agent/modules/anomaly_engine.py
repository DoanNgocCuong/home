"""
Anomaly Detection Engine — TIER 1 (Rule-based + Statistical ML)
Runs every scan cycle. ZERO LLM cost.

Inspired by LogAI (Salesforce) patterns:
  - Drain-style log template extraction
  - Statistical anomaly (z-score, IsolationForest concept)
  - Baseline learning (rolling 24h window)
  - Error rate change detection
"""
import logging
import math
import re
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field

from modules.models import NormalizedLog, LogLevel

logger = logging.getLogger(__name__)


# ── Log Template Extraction (Drain-inspired) ─────────────────

# Regex to replace variable parts in log messages
VARIABLE_PATTERNS = [
    (re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), '<IP>'),
    (re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I), '<UUID>'),
    (re.compile(r'\b[0-9a-f]{24,64}\b', re.I), '<HEX>'),
    (re.compile(r'\b\d+\.?\d*\s*(ms|MB|GB|KB|s|bytes|%)\b'), '<NUM>'),
    (re.compile(r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'), '<TIMESTAMP>'),
    (re.compile(r'\b\d+\b'), '<NUM>'),
    (re.compile(r'https?://\S+'), '<URL>'),
]


def extract_template(message: str) -> str:
    """Extract a log template by replacing variable parts with placeholders."""
    template = message
    for pattern, replacement in VARIABLE_PATTERNS:
        template = pattern.sub(replacement, template)
    # Collapse multiple spaces
    template = re.sub(r'\s+', ' ', template).strip()
    return template


def template_signature(template: str) -> str:
    """Create a short hash for a log template."""
    return hashlib.md5(template.encode()).hexdigest()[:12]


# ── Data Structures ──────────────────────────────────────────

@dataclass
class Baseline:
    """Rolling baseline for a metric."""
    service: str
    metric_name: str
    mean: float = 0.0
    stddev: float = 0.0
    sample_count: int = 0
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update(self, new_value: float, alpha: float = 0.1):
        """Exponential moving average update."""
        if self.sample_count == 0:
            self.mean = new_value
            self.stddev = 0.0
        else:
            delta = new_value - self.mean
            self.mean += alpha * delta
            # Welford's online variance
            self.stddev = math.sqrt((1 - alpha) * (self.stddev ** 2 + alpha * delta ** 2))
        self.sample_count += 1
        self.updated_at = datetime.now(timezone.utc)

    def z_score(self, value: float) -> float:
        """Calculate z-score for a value against this baseline."""
        if self.stddev == 0 or self.sample_count < 3:
            return 0.0
        return (value - self.mean) / self.stddev


@dataclass
class AnomalyResult:
    """Result of anomaly detection for a scan cycle."""
    is_anomaly: bool
    severity: str  # "none", "warning", "critical"
    tier_needed: int  # 1 = no AI, 2 = light AI, 3 = deep AI
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    summary: str = ""
    new_templates: List[str] = field(default_factory=list)
    top_errors: List[Dict] = field(default_factory=list)


class AnomalyEngine:
    """
    Tier 1 — Statistical anomaly detection engine.
    Runs every 5 minutes. Zero LLM cost.
    Determines whether to escalate to Tier 2 or Tier 3.
    """

    def __init__(self, z_threshold: float = 2.0, error_rate_warn: float = 1.0, error_rate_crit: float = 5.0):
        self.z_threshold = z_threshold
        self.error_rate_warn = error_rate_warn
        self.error_rate_crit = error_rate_crit

        # In-memory baselines (in production, persist to PostgreSQL)
        self.baselines: Dict[str, Baseline] = {}
        # Known log templates (for new template detection)
        self.known_templates: Dict[str, set] = defaultdict(set)  # service → set of template signatures

    def analyze(self, logs: List[NormalizedLog]) -> AnomalyResult:
        """
        Main analysis entry point — called every scan cycle.
        Returns whether anomaly detected and which tier to escalate to.
        """
        if not logs:
            return AnomalyResult(is_anomaly=False, severity="none", tier_needed=1, summary="No logs to analyze")

        anomalies = []
        tier_needed = 1  # Default: no AI needed

        # ── Check 1: Error rate ──────────────────────────────
        error_rate_result = self._check_error_rate(logs)
        if error_rate_result:
            anomalies.append(error_rate_result)
            tier_needed = max(tier_needed, error_rate_result.get("tier", 1))

        # ── Check 2: Error rate per service ──────────────────
        service_anomalies = self._check_service_error_rates(logs)
        anomalies.extend(service_anomalies)
        for sa in service_anomalies:
            tier_needed = max(tier_needed, sa.get("tier", 1))

        # ── Check 3: New error templates ─────────────────────
        new_templates = self._check_new_templates(logs)
        if new_templates:
            anomalies.append({
                "type": "new_error_templates",
                "count": len(new_templates),
                "templates": new_templates[:5],
                "tier": 2,
                "description": f"{len(new_templates)} new error pattern(s) never seen before",
            })
            tier_needed = max(tier_needed, 2)

        # ── Check 4: Error volume spike ──────────────────────
        volume_spike = self._check_volume_spike(logs)
        if volume_spike:
            anomalies.append(volume_spike)
            tier_needed = max(tier_needed, volume_spike.get("tier", 1))

        # ── Check 5: Cross-service error correlation ─────────
        cascade = self._check_cascading_errors(logs)
        if cascade:
            anomalies.append(cascade)
            tier_needed = max(tier_needed, 3)  # Cascading → always deep RCA

        # ── Update baselines ─────────────────────────────────
        self._update_baselines(logs)

        # ── Build result ─────────────────────────────────────
        is_anomaly = len(anomalies) > 0
        severity = "none"
        if tier_needed >= 3:
            severity = "critical"
        elif tier_needed >= 2:
            severity = "warning"

        # Build top errors summary
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        top_errors = self._get_top_errors(error_logs)

        # Compute metrics
        total = len(logs)
        total_errors = len(error_logs)
        error_rate = round(total_errors / total * 100, 2) if total > 0 else 0

        metrics = {
            "total_logs": total,
            "total_errors": total_errors,
            "error_rate": error_rate,
            "services_count": len({l.service for l in logs}),
            "anomaly_count": len(anomalies),
        }

        summary_parts = []
        if not is_anomaly:
            summary_parts.append(f"Normal operation. {total} logs, {error_rate}% error rate.")
        else:
            summary_parts.append(f"⚠ {len(anomalies)} anomalies detected!")
            for a in anomalies[:3]:
                summary_parts.append(f"  - [{a['type']}] {a.get('description', '')}")

        return AnomalyResult(
            is_anomaly=is_anomaly,
            severity=severity,
            tier_needed=tier_needed,
            anomalies=anomalies,
            metrics=metrics,
            summary="\n".join(summary_parts),
            new_templates=new_templates,
            top_errors=top_errors,
        )

    # ── Individual Checks ────────────────────────────────────

    def _check_error_rate(self, logs: List[NormalizedLog]) -> Optional[Dict]:
        """Check overall error rate against baseline."""
        total = len(logs)
        errors = sum(1 for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))
        rate = errors / total * 100 if total > 0 else 0

        baseline_key = "_global_:error_rate"
        baseline = self.baselines.get(baseline_key)

        if baseline and baseline.sample_count >= 3:
            z = baseline.z_score(rate)
            if abs(z) > self.z_threshold:
                tier = 3 if rate > self.error_rate_crit else 2
                return {
                    "type": "error_rate_anomaly",
                    "current": round(rate, 2),
                    "baseline_mean": round(baseline.mean, 2),
                    "baseline_stddev": round(baseline.stddev, 2),
                    "z_score": round(z, 2),
                    "tier": tier,
                    "description": f"Error rate {rate:.1f}% vs baseline {baseline.mean:.1f}% (z={z:.1f})",
                }
        elif rate > self.error_rate_crit:
            return {
                "type": "error_rate_high",
                "current": round(rate, 2),
                "threshold": self.error_rate_crit,
                "tier": 3,
                "description": f"Error rate {rate:.1f}% exceeds critical threshold {self.error_rate_crit}%",
            }

        return None

    def _check_service_error_rates(self, logs: List[NormalizedLog]) -> List[Dict]:
        """Check error rate per service."""
        by_service: Dict[str, List[NormalizedLog]] = defaultdict(list)
        for log in logs:
            by_service[log.service].append(log)

        anomalies = []
        for service, svc_logs in by_service.items():
            errors = sum(1 for l in svc_logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))
            rate = errors / len(svc_logs) * 100 if svc_logs else 0

            baseline_key = f"{service}:error_rate"
            baseline = self.baselines.get(baseline_key)

            if baseline and baseline.sample_count >= 3:
                z = baseline.z_score(rate)
                if z > self.z_threshold and rate > 1.0:
                    anomalies.append({
                        "type": "service_error_spike",
                        "service": service,
                        "current": round(rate, 2),
                        "baseline_mean": round(baseline.mean, 2),
                        "z_score": round(z, 2),
                        "tier": 3 if rate > self.error_rate_crit else 2,
                        "description": f"{service}: error rate {rate:.1f}% (baseline {baseline.mean:.1f}%, z={z:.1f})",
                    })

        return anomalies

    def _check_new_templates(self, logs: List[NormalizedLog]) -> List[str]:
        """Detect error log templates never seen before."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        new_templates = []

        for log in error_logs:
            template = extract_template(log.message)
            sig = template_signature(template)

            if sig not in self.known_templates.get(log.service, set()):
                new_templates.append(template)
                # Register it
                if log.service not in self.known_templates:
                    self.known_templates[log.service] = set()
                self.known_templates[log.service].add(sig)

        return list(set(new_templates))[:10]

    def _check_volume_spike(self, logs: List[NormalizedLog]) -> Optional[Dict]:
        """Check if error volume has spiked."""
        error_count = sum(1 for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))

        baseline_key = "_global_:error_count"
        baseline = self.baselines.get(baseline_key)

        if baseline and baseline.sample_count >= 3:
            z = baseline.z_score(error_count)
            if z > self.z_threshold * 1.5:  # Higher threshold for volume
                return {
                    "type": "error_volume_spike",
                    "current": error_count,
                    "baseline_mean": round(baseline.mean, 1),
                    "z_score": round(z, 2),
                    "tier": 2,
                    "description": f"Error volume {error_count} vs baseline {baseline.mean:.0f} (z={z:.1f})",
                }
        return None

    def _check_cascading_errors(self, logs: List[NormalizedLog]) -> Optional[Dict]:
        """Detect cascading errors across multiple services via trace correlation."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]

        # Group errors by trace_id
        by_trace: Dict[str, set] = defaultdict(set)
        for log in error_logs:
            if log.trace.trace_id:
                by_trace[log.trace.trace_id].add(log.service)

        # Find traces that span 3+ services with errors
        cascading = {tid: svcs for tid, svcs in by_trace.items() if len(svcs) >= 3}

        if cascading:
            worst_trace = max(cascading.items(), key=lambda x: len(x[1]))
            return {
                "type": "cascading_error",
                "trace_id": worst_trace[0],
                "affected_services": list(worst_trace[1]),
                "cascade_count": len(cascading),
                "tier": 3,
                "description": f"Cascading error across {len(worst_trace[1])} services: {', '.join(worst_trace[1])}. {len(cascading)} cascading traces total.",
            }
        return None

    # ── Baseline Management ──────────────────────────────────

    def _update_baselines(self, logs: List[NormalizedLog]):
        """Update rolling baselines from current scan."""
        total = len(logs)
        if total == 0:
            return

        error_count = sum(1 for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))
        error_rate = error_count / total * 100

        # Global baselines
        self._update_single_baseline("_global_", "error_rate", error_rate)
        self._update_single_baseline("_global_", "error_count", error_count)
        self._update_single_baseline("_global_", "total_logs", total)

        # Per-service baselines
        by_service: Dict[str, List[NormalizedLog]] = defaultdict(list)
        for log in logs:
            by_service[log.service].append(log)

        for service, svc_logs in by_service.items():
            svc_errors = sum(1 for l in svc_logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))
            svc_rate = svc_errors / len(svc_logs) * 100 if svc_logs else 0
            self._update_single_baseline(service, "error_rate", svc_rate)
            self._update_single_baseline(service, "error_count", svc_errors)

    def _update_single_baseline(self, service: str, metric: str, value: float):
        key = f"{service}:{metric}"
        if key not in self.baselines:
            self.baselines[key] = Baseline(service=service, metric_name=metric)
        self.baselines[key].update(value)

    # ── Helpers ───────────────────────────────────────────────

    def _get_top_errors(self, error_logs: List[NormalizedLog], limit: int = 10) -> List[Dict]:
        """Get top N error types with counts."""
        counter = Counter()
        error_details: Dict[str, Dict] = {}

        for log in error_logs:
            key = log.error_type or extract_template(log.message)[:80]
            counter[key] += 1
            if key not in error_details:
                error_details[key] = {
                    "error_type": key,
                    "sample_message": (log.error_message or log.message)[:200],
                    "service": log.service,
                    "services": set(),
                }
            error_details[key]["services"].add(log.service)

        top = []
        for error_type, count in counter.most_common(limit):
            detail = error_details[error_type]
            top.append({
                "error_type": error_type,
                "count": count,
                "sample_message": detail["sample_message"],
                "services": list(detail["services"]),
            })

        return top

    def get_baselines_summary(self) -> Dict[str, Any]:
        """Export baselines for dashboard display."""
        result = {}
        for key, bl in self.baselines.items():
            result[key] = {
                "mean": round(bl.mean, 2),
                "stddev": round(bl.stddev, 2),
                "samples": bl.sample_count,
                "updated": bl.updated_at.isoformat(),
            }
        return result
