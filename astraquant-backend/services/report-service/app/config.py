from dataclasses import dataclass
import os
@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "report-service")
    env: str = os.getenv("ENV", "dev")
    http_port: int = int(os.getenv("HTTP_PORT", "8008"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url: str = os.getenv("NATS_URL", "nats://localhost:4222")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minio")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minio_password")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
settings = Settings()
