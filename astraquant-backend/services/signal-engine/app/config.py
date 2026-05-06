import os

class Settings:
    def __init__(self):
        self.service_name = os.getenv("SERVICE_NAME", "signal-engine")
        self.env = os.getenv("ENV", "dev")
        self.http_port = int(os.getenv("HTTP_PORT", "8009"))
        self.database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://astra:astra_password@localhost:5432/astraquant")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.nats_url = os.getenv("NATS_URL", "nats://localhost:4222")
        self.strategy_service_url = os.getenv("STRATEGY_SERVICE_URL", "http://localhost:8002")
        self.strategy_score_service_url = os.getenv("STRATEGY_SCORE_SERVICE_URL", "http://localhost:8007")
        self.realtime_state_service_url = os.getenv("REALTIME_STATE_SERVICE_URL", "http://localhost:8012")
        self.default_exchange = os.getenv("DEFAULT_EXCHANGE", "OKX")
        self.default_symbols = [item.strip() for item in os.getenv("DEFAULT_SYMBOLS", "BTC-USDT-SWAP,ETH-USDT-SWAP").split(",") if item.strip()]
        self.default_timeframes = [item.strip() for item in os.getenv("DEFAULT_TIMEFRAMES", "1m,5m").split(",") if item.strip()]
        self.runtime_mode = os.getenv("RUNTIME_MODE", "HYBRID")
        self.state_poll_interval_ms = int(os.getenv("STATE_POLL_INTERVAL_MS", "1000"))
        self.signal_cooldown_seconds = int(os.getenv("SIGNAL_COOLDOWN_SECONDS", "300"))
        self.max_spread_pct = float(os.getenv("MAX_SPREAD_PCT", "0.001"))
        self.max_abs_funding_rate = float(os.getenv("MAX_ABS_FUNDING_RATE", "0.0005"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
settings = Settings()
