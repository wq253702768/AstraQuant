from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from astra_common.errors import AppError
from app.domain.services.timeframe import SUPPORTED_EXCHANGES, SUPPORTED_SYMBOLS, SUPPORTED_TIMEFRAMES

@dataclass(frozen=True)
class NormalizedKline:
    exchange: str
    internal_symbol: str
    exchange_symbol: str
    timeframe: str
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    quote_volume: Decimal

class KlineNormalizer:
    def normalize(self, payload: dict) -> NormalizedKline:
        exchange = str(payload["exchange"]).upper()
        symbol = payload["internal_symbol"]
        timeframe = payload["timeframe"]
        if exchange not in SUPPORTED_EXCHANGES:
            raise AppError("UNSUPPORTED_EXCHANGE", "不支持的交易所", 422)
        if symbol not in SUPPORTED_SYMBOLS:
            raise AppError("UNSUPPORTED_SYMBOL", "不支持的品种", 422)
        if timeframe not in SUPPORTED_TIMEFRAMES:
            raise AppError("UNSUPPORTED_TIMEFRAME", "不支持的周期", 422)
        item = NormalizedKline(
            exchange=exchange,
            internal_symbol=symbol,
            exchange_symbol=payload["exchange_symbol"],
            timeframe=timeframe,
            ts=datetime.fromtimestamp(int(payload["timestamp"]) / 1000, tz=UTC),
            open=Decimal(str(payload["open"])),
            high=Decimal(str(payload["high"])),
            low=Decimal(str(payload["low"])),
            close=Decimal(str(payload["close"])),
            volume=Decimal(str(payload.get("volume", "0"))),
            quote_volume=Decimal(str(payload.get("quote_volume", "0"))),
        )
        if item.open <= 0 or item.high <= 0 or item.low <= 0 or item.close <= 0:
            raise AppError("INVALID_MARKET_DATA_REQUEST", "K线价格必须大于0", 422)
        if item.high < item.open or item.high < item.close or item.low > item.open or item.low > item.close:
            raise AppError("INVALID_MARKET_DATA_REQUEST", "OHLC 数据不合法", 422)
        if item.volume < 0:
            raise AppError("INVALID_MARKET_DATA_REQUEST", "成交量不能为负", 422)
        return item
