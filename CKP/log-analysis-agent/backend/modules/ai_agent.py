"""
AI Agent Module - OpenAI Integration for Intelligent Log Analysis.
Uses OpenAI's function calling to orchestrate analysis tools.
"""
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from openai import AsyncOpenAI

from config.settings import get_config
from modules.models import (
    NormalizedLog, AnalysisResponse, MetricsSnapshot, RCAReport,
    Alert, AlertSeverity, AlertStatus, RootCauseHypothesis,
)
from tools.analysis_tools import (
    ErrorDetector, ServiceAnalyzer, MetricsAggregator, RootCauseAnalyzer,
)

logger = logging.getLogger(__name__)

# ── Tool Definitions for OpenAI Function Calling ────────────────

ANALYSIS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "detect_error_patterns",
            "description": "Detect and classify error patterns from logs. Returns grouped errors with counts, affected services, severity, and trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_anomalies": {
                        "type": "boolean",
                        "description": "Whether to also check for anomalous error spikes",
                        "default": True,
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_service_health",
            "description": "Analyze health status of each service including error rates, latency percentiles, and dependencies.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "aggregate_metrics",
            "description": "Aggregate metrics: error rates, response times, top errors as time series data for charts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bucket_minutes": {
                        "type": "integer",
                        "description": "Time bucket size in minutes for aggregation",
                        "default": 5,
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_root_cause",
            "description": "Perform root cause analysis: build incident timeline, find error propagation chains across services, identify the origin of failures.",
            "parameters": {
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "Specific trace ID to analyze. If empty, analyzes all error traces.",
                        "default": "",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_dependency_graph",
            "description": "Build service dependency graph showing how services call each other, with call counts and error rates per edge.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

# ── System Prompt ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert DevOps/SRE log analyst. Your job is to analyze structured logs from containerized services running on Rancher (Kubernetes) and monitored via Datadog.

Your capabilities:
1. **Error Detection**: Identify error patterns, classify them, detect anomalous spikes
2. **Service Health**: Assess health of each microservice based on error rates and latency
3. **Root Cause Analysis**: Trace errors across service boundaries, find the origin of cascading failures
4. **Metrics**: Aggregate key performance metrics and identify trends
5. **Recommendations**: Provide actionable remediation suggestions

Analysis guidelines:
- Always start by detecting error patterns to understand the landscape
- Check service health to see which services are affected
- If multiple services have errors, perform root cause analysis to find propagation chains
- Look for common infrastructure issues: timeout cascades, connection pool exhaustion, memory leaks
- Consider Kubernetes-specific issues: pod restarts, resource limits, network policies
- Provide severity assessment and prioritized recommendations

Output format:
- Be concise but thorough
- Prioritize by severity and impact
- Include specific error types, services, and timestamps
- Provide actionable recommendations (not generic advice)
"""


class LogAnalysisAgent:
    """AI-powered log analysis agent using OpenAI function calling."""

    def __init__(self):
        config = get_config()
        self.client = AsyncOpenAI(api_key=config.openai.api_key)
        self.model = config.openai.model
        self.max_tokens = config.openai.max_tokens
        self.temperature = config.openai.temperature

        # Analysis tools
        self.error_detector = ErrorDetector()
        self.service_analyzer = ServiceAnalyzer()
        self.metrics_aggregator = MetricsAggregator()
        self.rca_analyzer = RootCauseAnalyzer()

        # Current analysis context
        self._current_logs: List[NormalizedLog] = []
        self._tool_results: Dict[str, Any] = {}

    async def run_full_analysis(
        self,
        logs: List[NormalizedLog],
        analysis_type: str = "full",
        trace_id: Optional[str] = None,
    ) -> AnalysisResponse:
        """Run a complete analysis using the AI agent loop."""
        self._current_logs = logs
        self._tool_results = {}
        request_id = str(uuid.uuid4())[:8]

        logger.info(f"Starting {analysis_type} analysis on {len(logs)} logs [req:{request_id}]")

        # Build initial user message with log summary
        user_message = self._build_analysis_prompt(logs, analysis_type, trace_id)

        # Run the agent loop
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]

        max_iterations = 8
        for iteration in range(max_iterations):
            logger.info(f"Agent iteration {iteration + 1}/{max_iterations}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=ANALYSIS_TOOLS,
                tool_choice="auto" if iteration < max_iterations - 1 else "none",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            choice = response.choices[0]

            # If the agent wants to call tools
            if choice.message.tool_calls:
                messages.append(choice.message)

                for tool_call in choice.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments or "{}")

                    logger.info(f"Agent calling tool: {tool_name}({tool_args})")
                    result = await self._execute_tool(tool_name, tool_args)
                    self._tool_results[tool_name] = result

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, default=str, ensure_ascii=False),
                    })
            else:
                # Agent finished - extract final summary
                ai_summary = choice.message.content or ""
                break
        else:
            ai_summary = "Analysis completed but reached maximum iterations."

        # Build response from collected tool results
        return self._build_response(request_id, analysis_type, ai_summary)

    async def _execute_tool(self, tool_name: str, args: Dict) -> Any:
        """Execute an analysis tool and return results."""
        logs = self._current_logs

        if tool_name == "detect_error_patterns":
            patterns = self.error_detector.detect_error_patterns(logs)
            anomalies = []
            if args.get("include_anomalies", True):
                anomalies = self.error_detector.identify_anomalies(logs)

            return {
                "error_patterns": [p.model_dump() for p in patterns[:15]],
                "total_patterns": len(patterns),
                "anomalies": anomalies,
                "error_classification": self.error_detector.classify_errors(logs),
                "overall_error_rate": self.error_detector.calculate_error_rate(logs),
            }

        elif tool_name == "analyze_service_health":
            services = self.service_analyzer.analyze_services(logs)
            return {
                "services": [s.model_dump() for s in services],
                "total_services": len(services),
                "unhealthy_count": sum(1 for s in services if s.health == "unhealthy"),
                "degraded_count": sum(1 for s in services if s.health == "degraded"),
            }

        elif tool_name == "aggregate_metrics":
            bucket = args.get("bucket_minutes", 5)
            snapshot = self.metrics_aggregator.aggregate_metrics(logs, bucket)
            return snapshot.model_dump()

        elif tool_name == "analyze_root_cause":
            target_trace = args.get("trace_id", "")
            if target_trace:
                relevant_logs = [l for l in logs if l.trace.trace_id == target_trace]
            else:
                relevant_logs = logs

            timeline = self.rca_analyzer.build_incident_timeline(relevant_logs)
            propagation = self.rca_analyzer.find_error_propagation(relevant_logs)
            context = self.rca_analyzer.generate_rca_context(relevant_logs)

            return {
                "timeline": [e.model_dump() for e in timeline[:30]],
                "error_propagation_chains": propagation,
                "rca_context": context,
            }

        elif tool_name == "build_dependency_graph":
            deps = self.service_analyzer.build_dependency_graph(logs)
            return {
                "dependencies": [d.model_dump() for d in deps],
                "total_edges": len(deps),
            }

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _build_analysis_prompt(
        self,
        logs: List[NormalizedLog],
        analysis_type: str,
        trace_id: Optional[str],
    ) -> str:
        """Build the initial analysis prompt with log summary."""
        error_count = sum(1 for l in logs if l.level.value in ("error", "critical"))
        services = list({l.service for l in logs})
        time_range = ""
        if logs:
            start = min(l.timestamp for l in logs)
            end = max(l.timestamp for l in logs)
            time_range = f"from {start.isoformat()} to {end.isoformat()}"

        prompt = f"""Analyze the following log data:

- **Total logs**: {len(logs)}
- **Error/Critical logs**: {error_count}
- **Services**: {', '.join(services[:20])}
- **Time range**: {time_range}
- **Analysis type**: {analysis_type}
"""
        if trace_id:
            prompt += f"- **Focus trace ID**: {trace_id}\n"

        prompt += """
Please use the available tools to:
1. First, detect error patterns to understand the error landscape
2. Analyze service health to identify which services are affected
3. Aggregate metrics for trend analysis
4. If there are cross-service errors, perform root cause analysis
5. Build the dependency graph

After gathering all data, provide:
- A clear summary of the situation
- The most critical issues found
- Root cause analysis (if applicable)
- Prioritized recommendations for remediation
"""
        return prompt

    def _build_response(
        self, request_id: str, analysis_type: str, ai_summary: str,
    ) -> AnalysisResponse:
        """Build the final AnalysisResponse from collected tool results."""
        now = datetime.now(timezone.utc)

        # Extract error patterns
        error_data = self._tool_results.get("detect_error_patterns", {})
        from modules.models import ErrorPattern
        errors = []
        for p in error_data.get("error_patterns", []):
            try:
                errors.append(ErrorPattern(**p))
            except Exception:
                pass

        # Extract metrics
        metrics = None
        metrics_data = self._tool_results.get("aggregate_metrics")
        if metrics_data:
            try:
                metrics = MetricsSnapshot(**metrics_data)
            except Exception as e:
                logger.warning(f"Failed to parse metrics: {e}")

        # Extract service statuses
        from modules.models import ServiceStatus, ServiceDependency
        services = []
        svc_data = self._tool_results.get("analyze_service_health", {})
        for s in svc_data.get("services", []):
            try:
                services.append(ServiceStatus(**s))
            except Exception:
                pass

        # Extract dependencies
        dependencies = []
        dep_data = self._tool_results.get("build_dependency_graph", {})
        for d in dep_data.get("dependencies", []):
            try:
                dependencies.append(ServiceDependency(**d))
            except Exception:
                pass

        # Build RCA report if available
        rca = None
        rca_data = self._tool_results.get("analyze_root_cause")
        if rca_data:
            from modules.models import RCATimelineEvent
            timeline = []
            for evt in rca_data.get("timeline", []):
                try:
                    timeline.append(RCATimelineEvent(**evt))
                except Exception:
                    pass

            rca = RCAReport(
                incident_id=request_id,
                title="Automated Incident Analysis",
                summary=ai_summary[:500] if ai_summary else "Analysis completed",
                severity=AlertSeverity.HIGH if errors else AlertSeverity.MEDIUM,
                started_at=timeline[0].timestamp if timeline else now,
                detected_at=now,
                timeline=timeline,
                root_causes=[],
                recommendations=[],
                affected_services=list({e.service for e in timeline}),
                total_errors=len([l for l in self._current_logs if l.level.value in ("error", "critical")]),
            )

        # Generate alerts for critical patterns
        alerts = self._generate_alerts(errors, services)

        # Extract recommendations from AI summary
        recommendations = self._extract_recommendations(ai_summary)

        return AnalysisResponse(
            request_id=request_id,
            timestamp=now,
            analysis_type=analysis_type,
            metrics=metrics,
            errors=errors,
            alerts=alerts,
            rca=rca,
            services=services,
            dependencies=dependencies,
            ai_summary=ai_summary,
            ai_recommendations=recommendations,
        )

    def _generate_alerts(
        self, errors: List, services: List,
    ) -> List[Alert]:
        """Generate alerts from analysis results."""
        alerts = []
        now = datetime.now(timezone.utc)

        for error in errors:
            if error.severity in (AlertSeverity.CRITICAL, AlertSeverity.HIGH):
                alerts.append(Alert(
                    id=str(uuid.uuid4())[:8],
                    created_at=now,
                    title=f"{error.severity.value.upper()}: {error.error_type} ({error.count} occurrences)",
                    description=f"{error.error_message[:200]}. Affected services: {', '.join(error.affected_services)}",
                    severity=error.severity,
                    status=AlertStatus.ACTIVE,
                    service=error.affected_services[0] if error.affected_services else "unknown",
                    error_type=error.error_type,
                    error_count=error.count,
                ))

        for svc in services:
            if svc.health.value == "unhealthy":
                alerts.append(Alert(
                    id=str(uuid.uuid4())[:8],
                    created_at=now,
                    title=f"Service Unhealthy: {svc.service_name}",
                    description=f"Error rate: {svc.error_rate}%, P95 latency: {svc.p95_latency_ms}ms",
                    severity=AlertSeverity.CRITICAL,
                    status=AlertStatus.ACTIVE,
                    service=svc.service_name,
                    error_rate=svc.error_rate,
                ))

        return alerts

    @staticmethod
    def _extract_recommendations(ai_summary: str) -> List[str]:
        """Extract recommendation items from AI summary."""
        recommendations = []
        lines = ai_summary.split("\n")
        in_rec_section = False

        for line in lines:
            lower = line.lower().strip()
            if "recommendation" in lower or "suggest" in lower or "remediation" in lower:
                in_rec_section = True
                continue
            if in_rec_section and line.strip().startswith(("-", "*", "•", "1", "2", "3", "4", "5")):
                rec = line.strip().lstrip("-*•0123456789. ")
                if rec and len(rec) > 10:
                    recommendations.append(rec)
            elif in_rec_section and not line.strip():
                in_rec_section = False

        return recommendations[:10]
