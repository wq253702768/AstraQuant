from enum import StrEnum

class StrategyType(StrEnum):
    TREND_BREAKOUT = "trend_breakout"
    PULLBACK_FOLLOW = "pullback_follow"
    GRID_STRATEGY = "grid_strategy"
    DEFENSE_STRATEGY = "defense_strategy"
