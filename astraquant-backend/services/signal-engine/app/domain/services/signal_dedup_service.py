class SignalDedupService:
    def __init__(self): self.keys=set(); self.bar_keys=set()
    def dedup_key(self, strategy_id: str, strategy_version_id: str, symbol: str, signal_type: str, bar_id: str | None, direction: str | None) -> str:
        return f"{strategy_id}:{strategy_version_id}:{symbol}:{signal_type}:{bar_id}:{direction}"
    def allow(self, key: str) -> bool:
        if key in self.keys: return False
        self.keys.add(key); return True
    def allow_bar(self, strategy_id: str, symbol: str, bar_id: str, signal_type: str) -> bool:
        key=f"{strategy_id}:{symbol}:{bar_id}:{signal_type}"
        if key in self.bar_keys: return False
        self.bar_keys.add(key); return True
