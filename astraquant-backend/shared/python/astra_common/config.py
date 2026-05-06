from dataclasses import dataclass
import os

@dataclass(frozen=True)
class BaseServiceSettings:
    service_name: str
    env: str
    log_level: str

def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def load_base_settings(default_service_name: str) -> BaseServiceSettings:
    return BaseServiceSettings(
        service_name=get_env("SERVICE_NAME", default_service_name),
        env=get_env("ENV", "dev"),
        log_level=get_env("LOG_LEVEL", "INFO"),
    )
