from dataclasses import dataclass
@dataclass(frozen=True)
class SignalPrecheck:
    allowed: bool
    reason: str
    freshness_snapshot: dict
