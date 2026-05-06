import os
class Settings:
    service_name = os.getenv("SERVICE_NAME", "alert-center-service")
    env = os.getenv("ENV", "dev")
    http_port = int(os.getenv("HTTP_PORT", "8021"))
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    default_dedup_window_seconds = int(os.getenv("DEFAULT_DEDUP_WINDOW_SECONDS", "300"))
    webhook_default_url = os.getenv("WEBHOOK_DEFAULT_URL", "http://localhost:9000/mock-alert-webhook")
    log_level = os.getenv("LOG_LEVEL", "INFO")
settings = Settings()
