class SignalReasonBuilder:
    def trend_breakout(self, timeframe: str, window: int) -> str:
        return f"{timeframe} K线突破过去{window}根K线区间，资金费率正常，盘口价差正常"
