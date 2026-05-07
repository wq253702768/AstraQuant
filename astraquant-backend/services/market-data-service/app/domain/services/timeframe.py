from datetime import timedelta

TIMEFRAME_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "4h": 14400,
}

SUPPORTED_TIMEFRAMES = set(TIMEFRAME_SECONDS)
SUPPORTED_SYMBOLS = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"}
SUPPORTED_EXCHANGES = {"OKX"}

def timeframe_delta(timeframe: str) -> timedelta:
    if timeframe not in TIMEFRAME_SECONDS:
        raise ValueError(f"unsupported timeframe: {timeframe}")
    return timedelta(seconds=TIMEFRAME_SECONDS[timeframe])

def timeframe_milliseconds(timeframe: str) -> int:
    return int(timeframe_delta(timeframe).total_seconds() * 1000)
