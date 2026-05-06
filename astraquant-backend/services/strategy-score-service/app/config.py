from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "strategy-score-service")
    env: str = os.getenv("ENV", "dev")
    http_port: int = int(os.getenv("HTTP_PORT", "8007"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url: str = os.getenv("NATS_URL", "nats://localhost:4222")
    backtest_service_url: str = os.getenv("BACKTEST_SERVICE_URL", "http://localhost:8004")
    ai_analysis_service_url: str = os.getenv("AI_ANALYSIS_SERVICE_URL", "http://localhost:8006")
    strategy_service_url: str = os.getenv("STRATEGY_SERVICE_URL", "http://localhost:8002")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
