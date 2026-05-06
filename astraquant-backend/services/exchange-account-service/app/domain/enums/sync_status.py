from enum import StrEnum
class SyncStatus(StrEnum):
    FRESH = "FRESH"
    NORMAL = "NORMAL"
    SLOW = "SLOW"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"
