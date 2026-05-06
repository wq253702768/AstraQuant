from astra_common.errors import AppError

SUPPORTED_EXCHANGES = {"OKX"}
SUPPORTED_SYMBOLS = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"}
SUPPORTED_TIMEFRAMES = {"1m", "5m", "15m", "1h"}

class BacktestValidationService:
    def validate_request(self, exchange: str, symbols: list[str], timeframe: str, start_time, end_time, initial_capital) -> None:
        if exchange not in SUPPORTED_EXCHANGES:
            raise AppError("INVALID_BACKTEST_REQUEST", "不支持的交易所", 422)
        if not symbols or any(symbol not in SUPPORTED_SYMBOLS for symbol in symbols):
            raise AppError("INVALID_BACKTEST_REQUEST", "不支持的交易品种", 422)
        if timeframe not in SUPPORTED_TIMEFRAMES:
            raise AppError("INVALID_BACKTEST_REQUEST", "不支持的K线周期", 422)
        if end_time <= start_time:
            raise AppError("INVALID_BACKTEST_REQUEST", "end_time 必须大于 start_time", 422)
        if initial_capital <= 0:
            raise AppError("INVALID_BACKTEST_REQUEST", "initial_capital 必须大于0", 422)
