import hashlib

class ReplayCacheKeyBuilder:
    def page(self, drawdown_id: str) -> str:
        return f"replay:page:{drawdown_id}"
    def events(self, drawdown_id: str, start_time, end_time, event_type: str | None = None, marker_type: str | None = None) -> str:
        raw = f"{start_time}:{end_time}:{event_type}:{marker_type}"
        return f"replay:events:{drawdown_id}:{hashlib.sha1(raw.encode()).hexdigest()}"
    def klines(self, drawdown_id: str, start_time, end_time, timeframe: str | None = None) -> str:
        raw = f"{start_time}:{end_time}:{timeframe}"
        return f"replay:klines:{drawdown_id}:{hashlib.sha1(raw.encode()).hexdigest()}"
    def curves(self, drawdown_id: str) -> str:
        return f"replay:curves:{drawdown_id}"
