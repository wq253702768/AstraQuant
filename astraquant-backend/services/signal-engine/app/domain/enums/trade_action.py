from enum import StrEnum
class TradeAction(StrEnum):
    OPEN="OPEN"
    CLOSE="CLOSE"
    REDUCE="REDUCE"
    NOOP="NOOP"
    PAUSE="PAUSE"
