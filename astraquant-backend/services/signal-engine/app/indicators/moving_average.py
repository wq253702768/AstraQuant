class MovingAverage:
    def calculate(self, values: list[float], period: int) -> float:
        return sum(values[-period:]) / min(len(values), period) if values else 0
