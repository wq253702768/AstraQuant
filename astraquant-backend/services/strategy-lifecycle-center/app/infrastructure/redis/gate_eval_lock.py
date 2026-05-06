from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class GateEvalLock:
    ttl_seconds: int = 60

    def __post_init__(self) -> None:
        self._locks: dict[str, datetime] = {}

    def acquire(self, strategy_version_id: str, gate_code: str) -> bool:
        key = f"lifecycle:gate_lock:{strategy_version_id}:{gate_code}"
        now = datetime.now(timezone.utc)
        if self._locks.get(key, now) > now:
            return False
        self._locks[key] = now + timedelta(seconds=self.ttl_seconds)
        return True
