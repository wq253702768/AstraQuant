from dataclasses import dataclass
from app.domain.entities.replay_event import ReplayEvent

@dataclass(frozen=True)
class ReplayTimeline:
    events: list[ReplayEvent]
    next_cursor: str | None = None
