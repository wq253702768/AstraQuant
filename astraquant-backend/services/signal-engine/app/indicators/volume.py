from decimal import Decimal
class VolumeIndicator:
    def snapshot(self, klines: list[dict], window: int = 20) -> dict:
        current = Decimal(str(klines[-1].get("volume", "0")))
        history = [Decimal(str(item.get("volume", "0"))) for item in klines[-window-1:-1]]
        avg = sum(history, Decimal("0")) / Decimal(len(history)) if history else current
        multiplier = current / avg if avg else Decimal("0")
        return {"volume_avg": str(avg), "current_volume": str(current), "volume_multiplier": str(multiplier)}
