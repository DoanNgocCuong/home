"""
Configuration for Log Analysis Agent v2.
Loads from environment variables with sensible defaults.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class DatadogConfig:
    api_key: str = ""
    app_key: str = ""
    site: str = "datadoghq.com"
    cluster_name: str = ""
    max_logs_per_request: int = 1000
    rate_limit_per_second: float = 2.0

    @property
    def base_url(self) -> str:
        return f"https://api.{self.site}"

    @property
    def enabled(self) -> bool:
        return bool(self.api_key and self.app_key)


@dataclass
class LLMConfig:
    """Tiered LLM configuration."""
    # Tier 2: Cheap model for classify + summarize
    tier2_provider: str = "deepseek"      # "deepseek" | "openai"
    tier2_model: str = "deepseek-chat"
    tier2_api_key: str = ""
    tier2_base_url: str = "https://api.deepseek.com/v1"
    tier2_max_tokens: int = 2000
    tier2_temperature: float = 0.1

    # Tier 3: Expensive model for deep RCA
    tier3_provider: str = "openai"        # "openai" | "deepseek"
    tier3_model: str = "gpt-4o"
    tier3_api_key: str = ""
    tier3_base_url: str = "https://api.openai.com/v1"
    tier3_max_tokens: int = 4000
    tier3_temperature: float = 0.2

    @property
    def tier2_enabled(self) -> bool:
        return bool(self.tier2_api_key)

    @property
    def tier3_enabled(self) -> bool:
        return bool(self.tier3_api_key)


@dataclass
class LangfuseConfig:
    secret_key: str = ""
    public_key: str = ""
    host: str = "http://localhost:3000"

    @property
    def enabled(self) -> bool:
        return bool(self.secret_key and self.public_key)


@dataclass
class AgentConfig:
    scan_interval_seconds: int = 300     # 5 minutes
    anomaly_z_threshold: float = 2.0     # z-score threshold for anomaly
    error_rate_warning: float = 1.0      # % — trigger tier 2
    error_rate_critical: float = 5.0     # % — trigger tier 3
    baseline_window_hours: int = 24      # rolling baseline
    max_logs_per_analysis: int = 500
    use_sample_data: bool = True


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class AppConfig:
    datadog: DatadogConfig = field(default_factory=DatadogConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    langfuse: LangfuseConfig = field(default_factory=LangfuseConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "sqlite:///log_analysis.db"


_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    global _config
    if _config is None:
        _config = AppConfig(
            datadog=DatadogConfig(
                api_key=os.getenv("DATADOG_API_KEY", ""),
                app_key=os.getenv("DATADOG_APP_KEY", ""),
                site=os.getenv("DATADOG_SITE", "datadoghq.com"),
                cluster_name=os.getenv("DATADOG_CLUSTER", ""),
            ),
            llm=LLMConfig(
                tier2_api_key=os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", "")),
                tier2_model=os.getenv("LLM_TIER2_MODEL", "deepseek-chat"),
                tier2_base_url=os.getenv("LLM_TIER2_BASE_URL", "https://api.deepseek.com/v1"),
                tier3_api_key=os.getenv("OPENAI_API_KEY", ""),
                tier3_model=os.getenv("LLM_TIER3_MODEL", "gpt-4o"),
            ),
            langfuse=LangfuseConfig(
                secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
                host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
            ),
            agent=AgentConfig(
                scan_interval_seconds=int(os.getenv("SCAN_INTERVAL_SECONDS", "300")),
                anomaly_z_threshold=float(os.getenv("ANOMALY_THRESHOLD", "2.0")),
                use_sample_data=os.getenv("USE_SAMPLE_DATA", "true").lower() == "true",
            ),
            server=ServerConfig(
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8000")),
                debug=os.getenv("DEBUG", "false").lower() == "true",
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///log_analysis.db"),
        )
    return _config
