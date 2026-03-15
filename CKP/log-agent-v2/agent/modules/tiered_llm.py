"""
Tiered LLM Engine — Intelligent cost management.

Tier 1: Rule-based (anomaly_engine.py) — $0
Tier 2: Cheap LLM (DeepSeek) — classify, summarize, quick alert
Tier 3: Expensive LLM (GPT-4o) — deep RCA, cross-service analysis, recommendations

Includes Langfuse tracing for full cost visibility.
"""
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

from openai import AsyncOpenAI

from config.settings import get_config, LLMConfig
from modules.models import NormalizedLog, LogLevel
from modules.anomaly_engine import AnomalyResult

logger = logging.getLogger(__name__)


# ── Langfuse Integration (optional) ─────────────────────────

_langfuse = None


def get_langfuse():
    """Lazy init Langfuse client."""
    global _langfuse
    if _langfuse is None:
        config = get_config()
        if config.langfuse.enabled:
            try:
                from langfuse import Langfuse
                _langfuse = Langfuse(
                    secret_key=config.langfuse.secret_key,
                    public_key=config.langfuse.public_key,
                    host=config.langfuse.host,
                )
                logger.info("Langfuse connected for LLM tracing")
            except ImportError:
                logger.warning("langfuse package not installed, tracing disabled")
                _langfuse = False
            except Exception as e:
                logger.warning(f"Langfuse init failed: {e}")
                _langfuse = False
        else:
            _langfuse = False
    return _langfuse if _langfuse else None


# ── Prompts ──────────────────────────────────────────────────

TIER2_SYSTEM_PROMPT = """You are a concise log analyst. Your job is to quickly classify and summarize error patterns.

Rules:
- Be brief: max 200 words
- Output JSON format
- Focus on: error classification, severity, affected scope
- Do NOT provide detailed root cause analysis (that's for tier 3)

Output schema:
{
  "severity": "low|medium|high|critical",
  "classification": "brief error classification",
  "summary": "1-2 sentence summary",
  "alert_title": "short alert title for notification",
  "should_escalate": true/false,
  "escalation_reason": "why tier 3 is needed (if should_escalate)"
}"""

TIER3_SYSTEM_PROMPT = """You are an expert SRE/DevOps engineer performing deep incident analysis on containerized services running on Rancher/Kubernetes.

Your analysis must include:
1. **Root Cause**: Identify the most likely root cause with confidence level
2. **Error Chain**: Map how errors propagated across services
3. **Impact**: What's affected (services, users, business functions)
4. **Timeline**: When did it start, progression, current state
5. **Remediation**: Specific, actionable steps (not generic advice)
6. **Prevention**: How to prevent recurrence

Consider Kubernetes-specific issues: pod OOM, connection pool exhaustion, DNS resolution failures, certificate expiry, resource limits, node pressure.

Output JSON format:
{
  "root_cause": {"description": "...", "confidence": 0.0-1.0, "service_origin": "..."},
  "error_chain": ["service_a → service_b → service_c"],
  "impact": {"affected_services": [...], "estimated_users": "...", "business_impact": "..."},
  "timeline": [{"time": "...", "event": "..."}],
  "remediation": [{"priority": 1, "action": "...", "service": "...", "risk": "low|medium|high"}],
  "prevention": ["..."],
  "severity": "low|medium|high|critical",
  "summary": "2-3 sentence executive summary"
}"""


class TieredLLM:
    """
    Tiered LLM engine with Langfuse cost tracking.
    """

    def __init__(self):
        self.config = get_config().llm
        self._stats = {
            "tier2_calls": 0, "tier2_tokens": 0, "tier2_cost": 0.0,
            "tier3_calls": 0, "tier3_tokens": 0, "tier3_cost": 0.0,
        }

        # Init tier 2 client (DeepSeek or OpenAI mini)
        if self.config.tier2_enabled:
            self._tier2_client = AsyncOpenAI(
                api_key=self.config.tier2_api_key,
                base_url=self.config.tier2_base_url,
            )
        else:
            self._tier2_client = None

        # Init tier 3 client (GPT-4o)
        if self.config.tier3_enabled:
            self._tier3_client = AsyncOpenAI(
                api_key=self.config.tier3_api_key,
                base_url=self.config.tier3_base_url,
            )
        else:
            self._tier3_client = None

    async def run_tier2(
        self,
        anomaly_result: AnomalyResult,
        logs: List[NormalizedLog],
    ) -> Dict[str, Any]:
        """
        Tier 2: Quick classify + summarize using cheap LLM.
        Input: Anomaly context + top errors (NOT raw logs)
        Expected cost: ~$0.01-0.05 per call
        """
        if not self._tier2_client:
            return self._fallback_tier2(anomaly_result)

        # Build compact context (minimize tokens)
        context = self._build_tier2_context(anomaly_result, logs)

        trace_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Langfuse trace
        langfuse = get_langfuse()
        trace = None
        if langfuse:
            trace = langfuse.trace(
                name="tier2_analysis",
                id=trace_id,
                metadata={"tier": 2, "model": self.config.tier2_model},
            )

        try:
            response = await self._tier2_client.chat.completions.create(
                model=self.config.tier2_model,
                messages=[
                    {"role": "system", "content": TIER2_SYSTEM_PROMPT},
                    {"role": "user", "content": context},
                ],
                temperature=self.config.tier2_temperature,
                max_tokens=self.config.tier2_max_tokens,
                response_format={"type": "json_object"},
            )

            result_text = response.choices[0].message.content or "{}"
            tokens_used = response.usage.total_tokens if response.usage else 0
            cost = self._estimate_cost(tokens_used, tier=2)

            # Track stats
            self._stats["tier2_calls"] += 1
            self._stats["tier2_tokens"] += tokens_used
            self._stats["tier2_cost"] += cost

            # Langfuse generation
            if trace:
                trace.generation(
                    name="tier2_classify",
                    model=self.config.tier2_model,
                    input=context[:500],
                    output=result_text[:500],
                    usage={"input": response.usage.prompt_tokens, "output": response.usage.completion_tokens} if response.usage else None,
                    metadata={"cost_usd": cost},
                )

            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                result = {"summary": result_text, "severity": "medium", "should_escalate": False}

            result["_meta"] = {
                "tier": 2,
                "model": self.config.tier2_model,
                "tokens": tokens_used,
                "cost_usd": round(cost, 4),
                "duration_ms": int((time.time() - start_time) * 1000),
                "trace_id": trace_id,
            }
            return result

        except Exception as e:
            logger.error(f"Tier 2 LLM call failed: {e}")
            if trace:
                trace.generation(name="tier2_error", metadata={"error": str(e)})
            return self._fallback_tier2(anomaly_result)

    async def run_tier3(
        self,
        anomaly_result: AnomalyResult,
        logs: List[NormalizedLog],
        tier2_result: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Tier 3: Deep RCA using expensive LLM.
        Input: Full anomaly context + error logs + tier 2 findings
        Expected cost: ~$0.30-1.00 per call
        """
        if not self._tier3_client:
            return self._fallback_tier3(anomaly_result, tier2_result)

        context = self._build_tier3_context(anomaly_result, logs, tier2_result)

        trace_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        langfuse = get_langfuse()
        trace = None
        if langfuse:
            trace = langfuse.trace(
                name="tier3_deep_rca",
                id=trace_id,
                metadata={"tier": 3, "model": self.config.tier3_model},
            )

        try:
            response = await self._tier3_client.chat.completions.create(
                model=self.config.tier3_model,
                messages=[
                    {"role": "system", "content": TIER3_SYSTEM_PROMPT},
                    {"role": "user", "content": context},
                ],
                temperature=self.config.tier3_temperature,
                max_tokens=self.config.tier3_max_tokens,
                response_format={"type": "json_object"},
            )

            result_text = response.choices[0].message.content or "{}"
            tokens_used = response.usage.total_tokens if response.usage else 0
            cost = self._estimate_cost(tokens_used, tier=3)

            self._stats["tier3_calls"] += 1
            self._stats["tier3_tokens"] += tokens_used
            self._stats["tier3_cost"] += cost

            if trace:
                trace.generation(
                    name="tier3_rca",
                    model=self.config.tier3_model,
                    input=context[:1000],
                    output=result_text[:1000],
                    usage={"input": response.usage.prompt_tokens, "output": response.usage.completion_tokens} if response.usage else None,
                    metadata={"cost_usd": cost},
                )

            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                result = {"summary": result_text, "severity": "high"}

            result["_meta"] = {
                "tier": 3,
                "model": self.config.tier3_model,
                "tokens": tokens_used,
                "cost_usd": round(cost, 4),
                "duration_ms": int((time.time() - start_time) * 1000),
                "trace_id": trace_id,
            }
            return result

        except Exception as e:
            logger.error(f"Tier 3 LLM call failed: {e}")
            return self._fallback_tier3(anomaly_result, tier2_result)

    # ── Context Builders (token-optimized) ───────────────────

    def _build_tier2_context(self, anomaly: AnomalyResult, logs: List[NormalizedLog]) -> str:
        """Build compact context for tier 2 (~500-1000 tokens)."""
        parts = [
            f"## Anomaly Alert",
            f"Severity: {anomaly.severity}",
            f"Total logs: {anomaly.metrics.get('total_logs', 0)}",
            f"Error rate: {anomaly.metrics.get('error_rate', 0)}%",
            f"Services: {anomaly.metrics.get('services_count', 0)}",
            "",
            "## Anomalies Detected:",
        ]
        for a in anomaly.anomalies[:5]:
            parts.append(f"- [{a['type']}] {a.get('description', '')}")

        parts.append("\n## Top Errors:")
        for e in anomaly.top_errors[:5]:
            parts.append(f"- {e['error_type']} ({e['count']}x) in {', '.join(e['services'][:3])}")
            parts.append(f"  Message: {e['sample_message'][:100]}")

        if anomaly.new_templates:
            parts.append("\n## New Error Patterns (never seen before):")
            for t in anomaly.new_templates[:3]:
                parts.append(f"- {t[:120]}")

        return "\n".join(parts)

    def _build_tier3_context(
        self, anomaly: AnomalyResult, logs: List[NormalizedLog], tier2: Optional[Dict]
    ) -> str:
        """Build detailed context for tier 3 (~2000-4000 tokens)."""
        parts = [
            "## Incident Context for Deep RCA",
            f"Severity: {anomaly.severity}",
            f"Anomaly count: {len(anomaly.anomalies)}",
            "",
        ]

        # Include tier 2 findings
        if tier2:
            parts.append("## Tier 2 Quick Analysis:")
            parts.append(f"Classification: {tier2.get('classification', 'N/A')}")
            parts.append(f"Summary: {tier2.get('summary', 'N/A')}")
            parts.append(f"Escalation reason: {tier2.get('escalation_reason', 'N/A')}")
            parts.append("")

        # Anomaly details
        parts.append("## Detected Anomalies:")
        for a in anomaly.anomalies:
            parts.append(f"- [{a['type']}] {a.get('description', '')}")

        # Error logs (summarized, not raw)
        error_logs = sorted(
            [l for l in logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL)],
            key=lambda l: l.timestamp,
        )

        parts.append(f"\n## Error Logs ({len(error_logs)} total, showing top 20):")
        for log in error_logs[:20]:
            parts.append(
                f"[{log.timestamp.strftime('%H:%M:%S')}] {log.service} | "
                f"{log.error_type or 'Error'}: {(log.error_message or log.message)[:150]}"
            )
            if log.trace.trace_id:
                parts.append(f"  trace: {log.trace.trace_id[:16]}")
            if log.stack_trace:
                parts.append(f"  stack: {log.stack_trace[:200]}")

        # Cross-service trace info
        traces = set()
        for log in error_logs:
            if log.trace.trace_id:
                traces.add(log.trace.trace_id)

        if traces:
            parts.append(f"\n## Distributed Traces with Errors: {len(traces)} unique traces")
            # Show service chains
            from collections import defaultdict
            by_trace = defaultdict(list)
            for log in error_logs:
                if log.trace.trace_id:
                    by_trace[log.trace.trace_id].append(log.service)

            for tid, services in list(by_trace.items())[:5]:
                unique_svcs = list(dict.fromkeys(services))  # preserve order, dedup
                parts.append(f"  {tid[:16]}: {' → '.join(unique_svcs)}")

        # K8s context
        pods = {l.kubernetes.pod_name for l in error_logs if l.kubernetes.pod_name}
        if pods:
            parts.append(f"\n## K8s Pods with Errors: {len(pods)}")
            for pod in list(pods)[:10]:
                parts.append(f"  - {pod}")

        return "\n".join(parts)

    # ── Fallbacks ────────────────────────────────────────────

    def _fallback_tier2(self, anomaly: AnomalyResult) -> Dict:
        """Rule-based fallback when tier 2 LLM unavailable."""
        severity = anomaly.severity
        top = anomaly.top_errors[0] if anomaly.top_errors else {}
        return {
            "severity": severity,
            "classification": top.get("error_type", "Unknown error pattern"),
            "summary": anomaly.summary,
            "alert_title": f"[{severity.upper()}] {top.get('error_type', 'Error detected')} ({top.get('count', 0)}x)",
            "should_escalate": anomaly.tier_needed >= 3,
            "escalation_reason": "Cascading errors detected" if anomaly.tier_needed >= 3 else "",
            "_meta": {"tier": 2, "model": "rule-based-fallback", "tokens": 0, "cost_usd": 0},
        }

    def _fallback_tier3(self, anomaly: AnomalyResult, tier2: Optional[Dict]) -> Dict:
        """Rule-based fallback when tier 3 LLM unavailable."""
        return {
            "root_cause": {
                "description": f"Automated analysis: {anomaly.summary}",
                "confidence": 0.3,
                "service_origin": anomaly.top_errors[0]["services"][0] if anomaly.top_errors else "unknown",
            },
            "error_chain": [],
            "impact": {"affected_services": list({a.get("service", "") for a in anomaly.anomalies if a.get("service")})},
            "remediation": [{"priority": 1, "action": "Investigate top errors manually", "service": "all", "risk": "low"}],
            "prevention": ["Set up proper alerting thresholds", "Implement circuit breakers"],
            "severity": anomaly.severity,
            "summary": f"Rule-based analysis: {anomaly.summary}. Tier 2 said: {tier2.get('summary', 'N/A') if tier2 else 'N/A'}",
            "_meta": {"tier": 3, "model": "rule-based-fallback", "tokens": 0, "cost_usd": 0},
        }

    # ── Cost Estimation ──────────────────────────────────────

    def _estimate_cost(self, tokens: int, tier: int) -> float:
        """Estimate USD cost for token usage."""
        # Approximate pricing per 1M tokens (input+output blended)
        PRICING = {
            2: {"deepseek-chat": 0.35, "gpt-4o-mini": 0.38, "default": 0.35},
            3: {"gpt-4o": 6.25, "claude-sonnet-4-6": 9.0, "default": 6.25},
        }
        model = self.config.tier2_model if tier == 2 else self.config.tier3_model
        tier_pricing = PRICING.get(tier, PRICING[2])
        per_million = tier_pricing.get(model, tier_pricing["default"])
        return tokens / 1_000_000 * per_million

    def get_stats(self) -> Dict:
        """Get cumulative LLM usage stats."""
        return {
            **self._stats,
            "total_cost": round(self._stats["tier2_cost"] + self._stats["tier3_cost"], 4),
            "total_tokens": self._stats["tier2_tokens"] + self._stats["tier3_tokens"],
        }
