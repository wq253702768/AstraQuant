from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "market-data-service")
    env: str = os.getenv("ENV", "dev")
    http_port: int = int(os.getenv("HTTP_PORT", "8003"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    clickhouse_host: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    clickhouse_port: int = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    clickhouse_username: str = os.getenv("CLICKHOUSE_USERNAME", "default")
    clickhouse_password: str = os.getenv("CLICKHOUSE_PASSWORD", "")
    clickhouse_database: str = os.getenv("CLICKHOUSE_DATABASE", "astraquant")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url: str = os.getenv("NATS_URL", "nats://localhost:4222")
    exchange_gateway_url: str = os.getenv("EXCHANGE_GATEWAY_URL", "http://localhost:8010")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
