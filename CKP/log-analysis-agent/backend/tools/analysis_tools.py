"""
Analysis Tools for the Log Analysis Agent.
These are callable tools that the OpenAI agent invokes for specific analysis tasks.
"""
import logging
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import statistics

from modules.models import (
    NormalizedLog, ErrorPattern, ServiceStatus, ServiceDependency,
    MetricsSnapshot, TimeSeriesPoint, AlertSeverity, ServiceHealth,
    RCATimelineEvent, RootCauseHypothesis, LogLevel,
)

logger = logging.getLogger(__name__)


class ErrorDetector:
    """Detect error patterns, classify errors, and identify anomalies."""

    def detect_error_patterns(self, logs: List[NormalizedLog]) -> List[ErrorPattern]:
        """Group errors by type and detect patterns."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        if not error_logs:
            return []

        # Group by error_type + error_message signature
        groups: Dict[str, List[NormalizedLog]] = defaultdict(list)
        for log in error_logs:
            key = f"{log.error_type or 'Unknown'}::{log.error_message or log.message[:100]}"
            groups[key].append(log)

        patterns = []
        for key, group_logs in groups.items():
            error_type, _, error_msg = key.partition("::")
            services = list({l.service for l in group_logs})
            timestamps = [l.timestamp for l in group_logs]

            # Determine trend
            trend = self._calculate_trend(timestamps)

            # Determine severity based on count and services affected
            severity = self._score_severity(len(group_logs), len(services), trend)

            patterns.append(ErrorPattern(
                error_type=error_type,
                error_message=error_msg,
                count=len(group_logs),
                first_seen=min(timestamps),
                last_seen=max(timestamps),
                affected_services=services,
                severity=severity,
                sample_log_ids=[l.id for l in group_logs[:5]],
                trend=trend,
            ))

        # Sort by count descending
        patterns.sort(key=lambda p: p.count, reverse=True)
        return patterns

    def classify_errors(self, logs: List[NormalizedLog]) -> Dict[str, int]:
        """Classify errors by type."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        counter = Counter(l.error_type or "Unknown" for l in error_logs)
        return dict(counter.most_common(20))

    def calculate_error_rate(
        self, logs: List[NormalizedLog], total_logs: Optional[int] = None
    ) -> float:
        """Calculate error rate as a percentage."""
        if not logs and not total_logs:
            return 0.0
        error_count = sum(1 for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL))
        total = total_logs or len(logs)
        if total == 0:
            return 0.0
        return round((error_count / total) * 100, 2)

    def identify_anomalies(
        self, logs: List[NormalizedLog], window_minutes: int = 5
    ) -> List[Dict]:
        """Identify anomalous spikes in error rates."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        if len(error_logs) < 5:
            return []

        # Bucket errors into time windows
        buckets: Dict[str, int] = defaultdict(int)
        for log in error_logs:
            bucket_key = log.timestamp.strftime(f"%Y-%m-%dT%H:{log.timestamp.minute // window_minutes * window_minutes:02d}")
            buckets[bucket_key] = buckets.get(bucket_key, 0) + 1

        if len(buckets) < 3:
            return []

        values = list(buckets.values())
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0

        anomalies = []
        if stdev > 0:
            for bucket_time, count in buckets.items():
                z_score = (count - mean) / stdev
                if z_score > 2.0:  # More than 2 standard deviations
                    anomalies.append({
                        "time_bucket": bucket_time,
                        "error_count": count,
                        "z_score": round(z_score, 2),
                        "expected": round(mean, 1),
                        "severity": "critical" if z_score > 3 else "warning",
                    })

        return anomalies

    def _calculate_trend(self, timestamps: List[datetime]) -> str:
        """Calculate if errors are increasing, decreasing, or stable."""
        if len(timestamps) < 3:
            return "stable"

        sorted_ts = sorted(timestamps)
        mid = len(sorted_ts) // 2
        first_half = len(sorted_ts[:mid])
        second_half = len(sorted_ts[mid:])

        if second_half > first_half * 1.5:
            return "increasing"
        elif first_half > second_half * 1.5:
            return "decreasing"

        # Check for spike: if most errors concentrated in short window
        time_span = (sorted_ts[-1] - sorted_ts[0]).total_seconds()
        if time_span > 0:
            max_gap = max(
                (sorted_ts[i+1] - sorted_ts[i]).total_seconds()
                for i in range(len(sorted_ts) - 1)
            )
            if max_gap / time_span > 0.5:
                return "spike"

        return "stable"

    def _score_severity(self, count: int, service_count: int, trend: str) -> AlertSeverity:
        """Score error severity."""
        score = 0
        if count > 100:
            score += 3
        elif count > 20:
            score += 2
        elif count > 5:
            score += 1

        if service_count > 3:
            score += 2
        elif service_count > 1:
            score += 1

        if trend in ("increasing", "spike"):
            score += 1

        if score >= 5:
            return AlertSeverity.CRITICAL
        elif score >= 3:
            return AlertSeverity.HIGH
        elif score >= 2:
            return AlertSeverity.WARNING
        return AlertSeverity.MEDIUM


class ServiceAnalyzer:
    """Analyze service health and dependencies."""

    def analyze_services(self, logs: List[NormalizedLog]) -> List[ServiceStatus]:
        """Analyze health status for each service."""
        by_service: Dict[str, List[NormalizedLog]] = defaultdict(list)
        for log in logs:
            by_service[log.service].append(log)

        services = []
        error_detector = ErrorDetector()

        for service_name, svc_logs in by_service.items():
            error_logs = [l for l in svc_logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
            error_rate = error_detector.calculate_error_rate(svc_logs)

            # Calculate latency stats
            latencies = [
                l.http.response_time_ms for l in svc_logs
                if l.http.response_time_ms is not None and l.http.response_time_ms > 0
            ]
            avg_latency = statistics.mean(latencies) if latencies else 0
            p95_latency = self._percentile(latencies, 95) if latencies else 0
            p99_latency = self._percentile(latencies, 99) if latencies else 0

            # Determine health
            health = ServiceHealth.HEALTHY
            if error_rate > 5.0 or p95_latency > 5000:
                health = ServiceHealth.UNHEALTHY
            elif error_rate > 1.0 or p95_latency > 2000:
                health = ServiceHealth.DEGRADED

            # Find dependencies
            deps = set()
            for log in svc_logs:
                called = log.attributes.get("called_service")
                if called and called != service_name:
                    deps.add(called)

            # Top errors for this service
            top_errors = error_detector.detect_error_patterns(svc_logs)[:5]

            services.append(ServiceStatus(
                service_name=service_name,
                health=health,
                error_rate=error_rate,
                avg_latency_ms=round(avg_latency, 1),
                p95_latency_ms=round(p95_latency, 1),
                p99_latency_ms=round(p99_latency, 1),
                request_count=len(svc_logs),
                error_count=len(error_logs),
                top_errors=top_errors,
                dependencies=list(deps),
            ))

        services.sort(key=lambda s: s.error_rate, reverse=True)
        return services

    def build_dependency_graph(self, logs: List[NormalizedLog]) -> List[ServiceDependency]:
        """Build service dependency graph from trace data."""
        edges: Dict[Tuple[str, str], Dict] = defaultdict(
            lambda: {"call_count": 0, "error_count": 0, "latencies": []}
        )

        for log in logs:
            called = log.attributes.get("called_service")
            if called and called != log.service:
                key = (log.service, called)
                edges[key]["call_count"] += 1
                if log.level in (LogLevel.ERROR, LogLevel.CRITICAL):
                    edges[key]["error_count"] += 1
                if log.http.response_time_ms:
                    edges[key]["latencies"].append(log.http.response_time_ms)

        dependencies = []
        for (source, target), data in edges.items():
            latencies = data["latencies"]
            avg_latency = statistics.mean(latencies) if latencies else 0

            dependencies.append(ServiceDependency(
                source=source,
                target=target,
                call_count=data["call_count"],
                error_count=data["error_count"],
                avg_latency_ms=round(avg_latency, 1),
            ))

        return dependencies

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        index = min(index, len(sorted_data) - 1)
        return sorted_data[index]


class MetricsAggregator:
    """Aggregate metrics from logs."""

    def aggregate_metrics(
        self, logs: List[NormalizedLog], time_bucket_minutes: int = 5
    ) -> MetricsSnapshot:
        """Create a comprehensive metrics snapshot."""
        if not logs:
            now = datetime.now(timezone.utc)
            return MetricsSnapshot(
                time_range_start=now, time_range_end=now,
                total_logs=0, total_errors=0, error_rate=0.0,
                avg_response_time_ms=0.0, p50_latency_ms=0.0,
                p95_latency_ms=0.0, p99_latency_ms=0.0,
            )

        timestamps = [l.timestamp for l in logs]
        time_start = min(timestamps)
        time_end = max(timestamps)

        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
        error_rate = round(len(error_logs) / len(logs) * 100, 2) if logs else 0.0

        # Latency stats
        latencies = [
            l.http.response_time_ms for l in logs
            if l.http.response_time_ms is not None and l.http.response_time_ms > 0
        ]
        avg_latency = statistics.mean(latencies) if latencies else 0
        p50 = ServiceAnalyzer._percentile(latencies, 50) if latencies else 0
        p95 = ServiceAnalyzer._percentile(latencies, 95) if latencies else 0
        p99 = ServiceAnalyzer._percentile(latencies, 99) if latencies else 0

        # Error rate time series
        error_trend = self._build_time_series(error_logs, time_bucket_minutes, "errors")
        latency_trend = self._build_latency_series(logs, time_bucket_minutes)

        # Error patterns
        detector = ErrorDetector()
        top_errors = detector.detect_error_patterns(logs)[:10]

        # Service status
        analyzer = ServiceAnalyzer()
        services = analyzer.analyze_services(logs)

        return MetricsSnapshot(
            time_range_start=time_start,
            time_range_end=time_end,
            total_logs=len(logs),
            total_errors=len(error_logs),
            error_rate=error_rate,
            avg_response_time_ms=round(avg_latency, 1),
            p50_latency_ms=round(p50, 1),
            p95_latency_ms=round(p95, 1),
            p99_latency_ms=round(p99, 1),
            error_rate_trend=error_trend,
            latency_trend=latency_trend,
            top_errors=top_errors,
            services=services,
        )

    def _build_time_series(
        self, logs: List[NormalizedLog], bucket_minutes: int, label: str
    ) -> List[TimeSeriesPoint]:
        """Build time series from logs."""
        if not logs:
            return []

        buckets: Dict[datetime, int] = defaultdict(int)
        for log in logs:
            bucket = log.timestamp.replace(
                minute=(log.timestamp.minute // bucket_minutes) * bucket_minutes,
                second=0, microsecond=0
            )
            buckets[bucket] += 1

        return [
            TimeSeriesPoint(timestamp=ts, value=count, label=label)
            for ts, count in sorted(buckets.items())
        ]

    def _build_latency_series(
        self, logs: List[NormalizedLog], bucket_minutes: int
    ) -> List[TimeSeriesPoint]:
        """Build average latency time series."""
        buckets: Dict[datetime, List[float]] = defaultdict(list)
        for log in logs:
            if log.http.response_time_ms and log.http.response_time_ms > 0:
                bucket = log.timestamp.replace(
                    minute=(log.timestamp.minute // bucket_minutes) * bucket_minutes,
                    second=0, microsecond=0
                )
                buckets[bucket].append(log.http.response_time_ms)

        return [
            TimeSeriesPoint(
                timestamp=ts,
                value=round(statistics.mean(vals), 1),
                label="avg_latency_ms"
            )
            for ts, vals in sorted(buckets.items())
        ]


class RootCauseAnalyzer:
    """Analyze root causes of incidents by correlating logs across services."""

    def build_incident_timeline(
        self, logs: List[NormalizedLog]
    ) -> List[RCATimelineEvent]:
        """Build a timeline of events during an incident."""
        error_logs = sorted(
            [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)],
            key=lambda l: l.timestamp,
        )

        timeline = []
        for log in error_logs:
            severity = (
                AlertSeverity.CRITICAL
                if log.level == LogLevel.CRITICAL
                else AlertSeverity.HIGH
            )
            timeline.append(RCATimelineEvent(
                timestamp=log.timestamp,
                service=log.service,
                event_type="error",
                description=f"[{log.error_type or 'Error'}] {log.error_message or log.message[:200]}",
                severity=severity,
                related_trace_ids=[log.trace.trace_id] if log.trace.trace_id else [],
            ))

        return timeline

    def find_error_propagation(
        self, logs: List[NormalizedLog]
    ) -> List[Dict]:
        """Find error propagation chains across services."""
        # Group by trace_id
        by_trace: Dict[str, List[NormalizedLog]] = defaultdict(list)
        for log in logs:
            if log.trace.trace_id:
                by_trace[log.trace.trace_id].append(log)

        chains = []
        for trace_id, trace_logs in by_trace.items():
            error_logs = [l for l in trace_logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]
            if len(error_logs) > 1:
                sorted_errors = sorted(error_logs, key=lambda l: l.timestamp)
                chain = {
                    "trace_id": trace_id,
                    "services": [l.service for l in sorted_errors],
                    "errors": [l.error_type or l.message[:50] for l in sorted_errors],
                    "start_time": sorted_errors[0].timestamp.isoformat(),
                    "end_time": sorted_errors[-1].timestamp.isoformat(),
                    "duration_ms": (sorted_errors[-1].timestamp - sorted_errors[0].timestamp).total_seconds() * 1000,
                }
                chains.append(chain)

        # Sort by duration (longest propagation first)
        chains.sort(key=lambda c: c["duration_ms"], reverse=True)
        return chains[:20]

    def generate_rca_context(self, logs: List[NormalizedLog]) -> Dict:
        """Generate context for OpenAI to analyze root cause."""
        error_logs = [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)]

        # Error distribution by service
        by_service = Counter(l.service for l in error_logs)

        # First error per service (likely origin)
        first_errors = {}
        for log in sorted(error_logs, key=lambda l: l.timestamp):
            if log.service not in first_errors:
                first_errors[log.service] = {
                    "timestamp": log.timestamp.isoformat(),
                    "error_type": log.error_type,
                    "error_message": (log.error_message or log.message)[:300],
                    "trace_id": log.trace.trace_id,
                }

        # Error propagation chains
        propagation = self.find_error_propagation(logs)

        # Stack traces (unique, limited)
        unique_stacks = {}
        for log in error_logs:
            if log.stack_trace and log.error_type not in unique_stacks:
                unique_stacks[log.error_type or "unknown"] = log.stack_trace[:500]

        return {
            "total_errors": len(error_logs),
            "total_logs": len(logs),
            "error_distribution_by_service": dict(by_service),
            "first_error_per_service": first_errors,
            "error_propagation_chains": propagation[:5],
            "unique_stack_traces": unique_stacks,
            "time_range": {
                "start": min(l.timestamp for l in logs).isoformat() if logs else None,
                "end": max(l.timestamp for l in logs).isoformat() if logs else None,
            },
        }
