"""
Configuration settings for Log Analysis Agent.
Loads from environment variables with sensible defaults.
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatadogConfig:
    api_key: str = field(default_factory=lambda: os.getenv("DD_API_KEY", ""))
    app_key: str = field(default_factory=lambda: os.getenv("DD_APP_KEY", ""))
    site: str = field(default_factory=lambda: os.getenv("DD_SITE", "datadoghq.com"))
    # Rancher/K8s specific
    cluster_name: str = field(default_factory=lambda: os.getenv("DD_CLUSTER_NAME", ""))
    default_namespace: str = field(default_factory=lambda: os.getenv("DD_NAMESPACE", "production"))
    # API limits
    max_logs_per_request: int = 1000
    rate_limit_per_second: int = 5
    default_time_range_minutes: int = 60

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}"


@dataclass
class OpenAIConfig:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o"))
    max_tokens: int = 4096
    temperature: float = 0.1  # Low temperature for analytical tasks
    max_context_tokens: int = 120000  # GPT-4o context window


@dataclass
class CacheConfig:
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    log_cache_ttl: int = 3600  # 1 hour
    analysis_cache_ttl: int = 1800  # 30 minutes
    metrics_cache_ttl: int = 300  # 5 minutes


@dataclass
class DatabaseConfig:
    url: str = field(default_factory=lambda: os.getenv(
        "DATABASE_URL", "sqlite:///log_analysis.db"
    ))


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", "8000"))
    cors_origins: list = field(default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"])
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


@dataclass
class AlertConfig:
    error_rate_warning: float = 1.0    # % error rate triggers warning
    error_rate_critical: float = 5.0   # % error rate triggers critical
    latency_warning_ms: int = 2000     # ms
    latency_critical_ms: int = 5000    # ms
    anomaly_threshold: float = 2.0     # standard deviations
    # Notification channels
    slack_webhook: Optional[str] = field(default_factory=lambda: os.getenv("SLACK_WEBHOOK_URL"))


@dataclass
class AppConfig:
    datadog: DatadogConfig = field(default_factory=DatadogConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    alerts: AlertConfig = field(default_factory=AlertConfig)


# Singleton config
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    global _config
    if _config is None:
        _config = AppConfig()
    return _config
