from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "auth-service")
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    jwt_access_expire_seconds: int = int(os.getenv("JWT_ACCESS_EXPIRE_SECONDS", "7200"))
    jwt_refresh_expire_seconds: int = int(os.getenv("JWT_REFRESH_EXPIRE_SECONDS", "604800"))
    login_failed_limit: int = int(os.getenv("LOGIN_FAILED_LIMIT", "5"))
    login_failed_window_seconds: int = int(os.getenv("LOGIN_FAILED_WINDOW_SECONDS", "300"))
    login_lock_seconds: int = int(os.getenv("LOGIN_LOCK_SECONDS", "900"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
