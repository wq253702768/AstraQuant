from enum import StrEnum


class LifecycleStage(StrEnum):
    DRAFT = "DRAFT"
    BACKTEST = "BACKTEST"
    AI_REVIEW = "AI_REVIEW"
    SCORING = "SCORING"
    SIMULATION = "SIMULATION"
    SMALL_LIVE = "SMALL_LIVE"
    LIVE = "LIVE"
    SCALE_UP = "SCALE_UP"
    REVIEW = "REVIEW"
    GOVERNANCE = "GOVERNANCE"
    RETIRED = "RETIRED"
