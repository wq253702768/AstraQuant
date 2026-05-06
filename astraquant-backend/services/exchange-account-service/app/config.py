import os
class Settings:
    service_name = os.getenv("SERVICE_NAME", "exchange-account-service")
    env = os.getenv("ENV", "dev")
    http_port = int(os.getenv("HTTP_PORT", "8016"))
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
    okx_private_gateway_url = os.getenv("OKX_PRIVATE_GATEWAY_URL", "http://localhost:8017")
    crypto_provider = os.getenv("CRYPTO_PROVIDER", "LOCAL")
    local_master_key = os.getenv("LOCAL_MASTER_KEY", "change_me_32_bytes_minimum")
    allow_withdraw_permission = os.getenv("ALLOW_WITHDRAW_PERMISSION", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO")
settings = Settings()
