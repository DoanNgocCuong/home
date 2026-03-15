"""
Datadog Log Fetcher Module.
Handles all interactions with Datadog API for log retrieval and analytics.
"""
import time
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any

import httpx

from config.settings import get_config, DatadogConfig
from modules.models import (
    NormalizedLog, LogLevel, TraceContext, HttpInfo, KubernetesInfo
)

logger = logging.getLogger(__name__)


class DatadogLogFetcher:
    """Fetch and normalize logs from Datadog API."""

    def __init__(self, config: Optional[DatadogConfig] = None):
        self.config = config or get_config().datadog
        self._headers = {
            "DD-API-KEY": self.config.api_key,
            "DD-APPLICATION-KEY": self.config.app_key,
            "Content-Type": "application/json",
        }
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            headers=self._headers,
            timeout=30.0,
        )
        self._last_request_time = 0.0

    async def close(self):
        await self._client.aclose()

    async def _rate_limit(self):
        """Simple rate limiting."""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self.config.rate_limit_per_second
        if elapsed < min_interval:
            await _async_sleep(min_interval - elapsed)
        self._last_request_time = time.time()

    # ── Core API Methods ────────────────────────────────────────────

    async def search_logs(
        self,
        query: str,
        time_from: datetime,
        time_to: datetime,
        limit: int = 1000,
        sort: str = "timestamp",
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search logs via Datadog Log Search API v2."""
        await self._rate_limit()

        body = {
            "filter": {
                "query": query,
                "from": time_from.isoformat(),
                "to": time_to.isoformat(),
            },
            "sort": sort,
            "page": {"limit": min(limit, self.config.max_logs_per_request)},
        }
        if cursor:
            body["page"]["cursor"] = cursor

        try:
            response = await self._client.post(
                "/api/v2/logs/events/search", json=body
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Datadog API error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Datadog request failed: {e}")
            raise

    async def aggregate_logs(
        self,
        query: str,
        time_from: datetime,
        time_to: datetime,
        group_by: Optional[List[str]] = None,
        compute_type: str = "count",
        interval: str = "5m",
    ) -> Dict[str, Any]:
        """Aggregate logs via Datadog Log Analytics API."""
        await self._rate_limit()

        body = {
            "filter": {
                "query": query,
                "from": time_from.isoformat(),
                "to": time_to.isoformat(),
            },
            "compute": [
                {"aggregation": compute_type, "type": "timeseries", "interval": interval}
            ],
        }
        if group_by:
            body["group_by"] = [{"facet": facet, "limit": 20} for facet in group_by]

        try:
            response = await self._client.post(
                "/api/v2/logs/analytics/aggregate", json=body
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Datadog Analytics API error: {e.response.status_code}")
            raise

    # ── High-Level Fetch Methods ────────────────────────────────────

    async def fetch_error_logs(
        self,
        minutes: int = 60,
        services: Optional[List[str]] = None,
        extra_query: Optional[str] = None,
    ) -> List[NormalizedLog]:
        """Fetch error logs from the last N minutes."""
        now = datetime.now(timezone.utc)
        time_from = now - timedelta(minutes=minutes)

        query_parts = ["(status:error OR status:critical OR level:ERROR OR level:CRITICAL)"]

        if self.config.cluster_name:
            query_parts.append(f"@kubernetes.cluster.name:{self.config.cluster_name}")

        if services:
            svc_filter = " OR ".join(f"service:{s}" for s in services)
            query_parts.append(f"({svc_filter})")

        if extra_query:
            query_parts.append(extra_query)

        query = " AND ".join(query_parts)
        logger.info(f"Fetching error logs: {query}")

        return await self._fetch_all_logs(query, time_from, now)

    async def fetch_all_logs(
        self,
        minutes: int = 60,
        services: Optional[List[str]] = None,
        query: Optional[str] = None,
    ) -> List[NormalizedLog]:
        """Fetch all logs (any level) from the last N minutes."""
        now = datetime.now(timezone.utc)
        time_from = now - timedelta(minutes=minutes)

        query_parts = ["*"]
        if self.config.cluster_name:
            query_parts = [f"@kubernetes.cluster.name:{self.config.cluster_name}"]

        if services:
            svc_filter = " OR ".join(f"service:{s}" for s in services)
            query_parts.append(f"({svc_filter})")

        if query:
            query_parts.append(query)

        final_query = " AND ".join(query_parts)
        return await self._fetch_all_logs(final_query, time_from, now)

    async def fetch_logs_by_trace(self, trace_id: str) -> List[NormalizedLog]:
        """Fetch all logs for a specific trace ID."""
        now = datetime.now(timezone.utc)
        time_from = now - timedelta(hours=24)
        query = f"trace_id:{trace_id}"
        return await self._fetch_all_logs(query, time_from, now)

    async def fetch_error_metrics(
        self,
        minutes: int = 60,
        services: Optional[List[str]] = None,
        interval: str = "5m",
    ) -> Dict[str, Any]:
        """Fetch error rate time-series metrics."""
        now = datetime.now(timezone.utc)
        time_from = now - timedelta(minutes=minutes)

        query = "status:error OR status:critical"
        if services:
            svc_filter = " OR ".join(f"service:{s}" for s in services)
            query += f" AND ({svc_filter})"

        group_by = ["service"]
        return await self.aggregate_logs(query, time_from, now, group_by, "count", interval)

    # ── Internal Helpers ────────────────────────────────────────────

    async def _fetch_all_logs(
        self, query: str, time_from: datetime, time_to: datetime
    ) -> List[NormalizedLog]:
        """Fetch all logs with pagination."""
        all_logs = []
        cursor = None
        max_pages = 10  # Safety limit

        for _ in range(max_pages):
            result = await self.search_logs(query, time_from, time_to, cursor=cursor)
            raw_logs = result.get("data", [])

            if not raw_logs:
                break

            for raw_log in raw_logs:
                try:
                    normalized = self._normalize_log(raw_log)
                    all_logs.append(normalized)
                except Exception as e:
                    logger.warning(f"Failed to normalize log: {e}")

            # Check for next page
            cursor = result.get("meta", {}).get("page", {}).get("after")
            if not cursor:
                break

        logger.info(f"Fetched {len(all_logs)} logs total")
        return all_logs

    def _normalize_log(self, raw_log: Dict[str, Any]) -> NormalizedLog:
        """Normalize a raw Datadog log entry into our model."""
        attrs = raw_log.get("attributes", {})
        tags_list = attrs.get("tags", [])
        tags = self._parse_tags(tags_list)

        # Extract nested attributes
        log_attrs = attrs.get("attributes", {})

        # Parse level
        status = attrs.get("status", "info").lower()
        level = self._parse_level(status)

        # Parse timestamp
        timestamp_str = attrs.get("timestamp", "")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            timestamp = datetime.now(timezone.utc)

        # Build trace context
        trace = TraceContext(
            trace_id=log_attrs.get("dd", {}).get("trace_id")
                or log_attrs.get("trace_id")
                or tags.get("trace_id"),
            span_id=log_attrs.get("dd", {}).get("span_id")
                or log_attrs.get("span_id"),
            parent_span_id=log_attrs.get("parent_span_id"),
        )

        # Build HTTP info
        http_attrs = log_attrs.get("http", {})
        http_info = HttpInfo(
            method=http_attrs.get("method"),
            status_code=http_attrs.get("status_code"),
            response_time_ms=http_attrs.get("response_time") or log_attrs.get("duration_ms"),
            url=http_attrs.get("url"),
            path=http_attrs.get("path"),
        )

        # Build Kubernetes info
        k8s = KubernetesInfo(
            cluster_name=log_attrs.get("kubernetes", {}).get("cluster", {}).get("name")
                or tags.get("kube_cluster_name"),
            namespace=log_attrs.get("kubernetes", {}).get("namespace")
                or tags.get("kube_namespace"),
            pod_name=log_attrs.get("kubernetes", {}).get("pod", {}).get("name")
                or tags.get("pod_name"),
            pod_id=log_attrs.get("kubernetes", {}).get("pod", {}).get("uid"),
            container_name=log_attrs.get("kubernetes", {}).get("container", {}).get("name")
                or tags.get("kube_container_name"),
            container_id=log_attrs.get("container_id"),
            node_name=log_attrs.get("kubernetes", {}).get("node", {}).get("name"),
            docker_image=log_attrs.get("docker", {}).get("image"),
        )

        return NormalizedLog(
            id=raw_log.get("id", ""),
            timestamp=timestamp,
            level=level,
            service=attrs.get("service", tags.get("service", "unknown")),
            message=attrs.get("message", ""),
            host=attrs.get("host", ""),
            error_type=log_attrs.get("error", {}).get("kind")
                or log_attrs.get("error_type"),
            error_code=log_attrs.get("error_code"),
            error_message=log_attrs.get("error", {}).get("message")
                or log_attrs.get("error_message"),
            stack_trace=log_attrs.get("error", {}).get("stack")
                or log_attrs.get("stack_trace"),
            trace=trace,
            http=http_info,
            kubernetes=k8s,
            attributes=log_attrs,
        )

    @staticmethod
    def _parse_level(status: str) -> LogLevel:
        mapping = {
            "debug": LogLevel.DEBUG,
            "info": LogLevel.INFO,
            "ok": LogLevel.INFO,
            "warn": LogLevel.WARNING,
            "warning": LogLevel.WARNING,
            "error": LogLevel.ERROR,
            "err": LogLevel.ERROR,
            "critical": LogLevel.CRITICAL,
            "fatal": LogLevel.CRITICAL,
            "emergency": LogLevel.CRITICAL,
        }
        return mapping.get(status, LogLevel.INFO)

    @staticmethod
    def _parse_tags(tags_list: List[str]) -> Dict[str, str]:
        """Parse Datadog tag list into key-value dict."""
        tags = {}
        for tag in tags_list:
            if ":" in tag:
                key, _, value = tag.partition(":")
                tags[key] = value
        return tags


async def _async_sleep(seconds: float):
    """Async sleep helper."""
    import asyncio
    await asyncio.sleep(seconds)
