-- Initialize databases for both Langfuse and Log Agent
CREATE DATABASE langfuse;

-- Log Agent tables
CREATE TABLE IF NOT EXISTS analysis_runs (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    analysis_type VARCHAR(20) NOT NULL,
    tier_used VARCHAR(10) NOT NULL,
    total_logs INTEGER DEFAULT 0,
    total_errors INTEGER DEFAULT 0,
    error_rate REAL DEFAULT 0,
    anomaly_detected BOOLEAN DEFAULT FALSE,
    llm_tokens_used INTEGER DEFAULT 0,
    llm_cost_usd REAL DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    summary TEXT,
    result_json JSONB
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_id VARCHAR(32) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    service VARCHAR(100),
    error_type VARCHAR(200),
    error_count INTEGER DEFAULT 0,
    acknowledged_by VARCHAR(100),
    resolved_at TIMESTAMPTZ,
    analysis_run_id VARCHAR(32) REFERENCES analysis_runs(request_id)
);

CREATE TABLE IF NOT EXISTS anomaly_baselines (
    id SERIAL PRIMARY KEY,
    service VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    baseline_mean REAL NOT NULL,
    baseline_stddev REAL NOT NULL,
    sample_count INTEGER NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(service, metric_name)
);

CREATE INDEX idx_analysis_runs_created ON analysis_runs(created_at DESC);
CREATE INDEX idx_alerts_status ON alerts(status, severity);
CREATE INDEX idx_alerts_service ON alerts(service);
CREATE INDEX idx_baselines_service ON anomaly_baselines(service);
