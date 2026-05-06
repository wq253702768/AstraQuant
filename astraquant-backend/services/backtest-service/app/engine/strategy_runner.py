from app.strategies.defense_strategy import DefenseStrategy
from app.strategies.grid_strategy import GridStrategy
from app.strategies.pullback_follow import PullbackFollowStrategy
from app.strategies.trend_breakout import TrendBreakoutStrategy

class StrategyRunner:
    strategies = {
        "trend_breakout": TrendBreakoutStrategy,
        "pullback_follow": PullbackFollowStrategy,
        "grid_strategy": GridStrategy,
        "defense_strategy": DefenseStrategy,
    }
    def run(self, strategy_type: str, rows: list[dict], params: dict):
        strategy_cls = self.strategies.get(strategy_type, TrendBreakoutStrategy)
        return strategy_cls().generate_signals(rows, params)
