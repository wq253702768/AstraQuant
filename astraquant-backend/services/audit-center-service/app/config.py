import os
class Settings:
    service_name=os.getenv("SERVICE_NAME","audit-center-service")
    env=os.getenv("ENV","dev")
    http_port=int(os.getenv("HTTP_PORT","8022"))
    database_url=os.getenv("DATABASE_URL","postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url=os.getenv("REDIS_URL","redis://localhost:6379/0")
    nats_url=os.getenv("NATS_URL","nats://localhost:4222")
    audit_export_bucket=os.getenv("AUDIT_EXPORT_BUCKET","audit-exports")
    log_level=os.getenv("LOG_LEVEL","INFO")
settings=Settings()
