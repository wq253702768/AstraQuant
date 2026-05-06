from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "api-gateway")
    env: str = os.getenv("ENV", "dev")
    auth_service_url: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    strategy_service_url: str = os.getenv("STRATEGY_SERVICE_URL", "http://localhost:8002")
    market_data_service_url: str = os.getenv("MARKET_DATA_SERVICE_URL", "http://localhost:8003")
    backtest_service_url: str = os.getenv("BACKTEST_SERVICE_URL", "http://localhost:8004")
    replay_service_url: str = os.getenv("REPLAY_SERVICE_URL", "http://localhost:8005")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
