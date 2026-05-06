import os


class Settings:
    service_name = os.getenv("SERVICE_NAME", "strategy-lifecycle-center")
    env = os.getenv("ENV", "dev")
    http_port = int(os.getenv("HTTP_PORT", "8023"))
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    strategy_service_url = os.getenv("STRATEGY_SERVICE_URL", "http://localhost:8002")
    backtest_service_url = os.getenv("BACKTEST_SERVICE_URL", "http://localhost:8004")
    ai_analysis_service_url = os.getenv("AI_ANALYSIS_SERVICE_URL", "http://localhost:8006")
    strategy_score_service_url = os.getenv("STRATEGY_SCORE_SERVICE_URL", "http://localhost:8007")
    paper_monitor_service_url = os.getenv("PAPER_MONITOR_SERVICE_URL", "http://localhost:8015")
    live_monitor_service_url = os.getenv("LIVE_MONITOR_SERVICE_URL", "http://localhost:8020")
    order_executor_service_url = os.getenv("ORDER_EXECUTOR_SERVICE_URL", "http://localhost:8018")
    live_risk_guard_service_url = os.getenv("LIVE_RISK_GUARD_SERVICE_URL", "http://localhost:8019")
    alert_center_service_url = os.getenv("ALERT_CENTER_SERVICE_URL", "http://localhost:8021")
    audit_center_service_url = os.getenv("AUDIT_CENTER_SERVICE_URL", "http://localhost:8022")
    default_small_live_approval_expire_days = int(os.getenv("DEFAULT_SMALL_LIVE_APPROVAL_EXPIRE_DAYS", "7"))
    default_scale_up_approval_expire_days = int(os.getenv("DEFAULT_SCALE_UP_APPROVAL_EXPIRE_DAYS", "7"))
    gate_eval_lock_ttl_seconds = int(os.getenv("GATE_EVAL_LOCK_TTL_SECONDS", "60"))
    dashboard_cache_ttl_seconds = int(os.getenv("DASHBOARD_CACHE_TTL_SECONDS", "30"))
    auto_transition_enabled = os.getenv("AUTO_TRANSITION_ENABLED", "true").lower() == "true"
    auto_approval_enabled = os.getenv("AUTO_APPROVAL_ENABLED", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
