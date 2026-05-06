from datetime import timedelta

TIMEFRAME_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
}

SUPPORTED_TIMEFRAMES = set(TIMEFRAME_SECONDS)
SUPPORTED_SYMBOLS = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"}
SUPPORTED_EXCHANGES = {"OKX"}

def timeframe_delta(timeframe: str) -> timedelta:
    if timeframe not in TIMEFRAME_SECONDS:
        raise ValueError(f"unsupported timeframe: {timeframe}")
    return timedelta(seconds=TIMEFRAME_SECONDS[timeframe])
