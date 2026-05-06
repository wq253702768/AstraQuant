from app.strategies.defense_strategy_realtime import DefenseStrategyRealtime
from app.strategies.grid_strategy_realtime import GridStrategyRealtime
from app.strategies.pullback_follow_realtime import PullbackFollowRealtime
from app.strategies.trend_breakout_realtime import TrendBreakoutRealtime
class StrategyRegistry:
    strategies={"trend_breakout":TrendBreakoutRealtime,"pullback_follow":PullbackFollowRealtime,"grid_strategy":GridStrategyRealtime,"defense_strategy":DefenseStrategyRealtime}
    def get(self, strategy_type: str): return self.strategies.get(strategy_type, TrendBreakoutRealtime)()
