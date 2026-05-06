from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "strategy-service")
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url: str = os.getenv("NATS_URL", "nats://localhost:4222")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    system_max_leverage: int = int(os.getenv("SYSTEM_MAX_LEVERAGE", "10"))
    system_max_risk_per_trade_pct: float = float(os.getenv("SYSTEM_MAX_RISK_PER_TRADE_PCT", "0.02"))

settings = Settings()
