from dataclasses import dataclass

@dataclass(frozen=True)
class DataValidationResult:
    status: str
    warnings: list[str]
    errors: list[str]

class DataValidator:
    def validate_klines(self, rows: list[dict]) -> DataValidationResult:
        if not rows:
            return DataValidationResult(status="FAILED", warnings=[], errors=["K线数据为空"])
        errors = []
        for row in rows:
            if row["high"] < row["open"] or row["high"] < row["close"] or row["low"] > row["open"] or row["low"] > row["close"]:
                errors.append("OHLC不合法")
                break
        return DataValidationResult(status="FAILED" if errors else "PASS", warnings=[], errors=errors)
