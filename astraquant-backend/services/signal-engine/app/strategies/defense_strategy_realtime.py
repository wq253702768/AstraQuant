from app.strategies.base import RealtimeStrategy
class DefenseStrategyRealtime(RealtimeStrategy):
    def generate(self, snapshot: dict, params: dict) -> list[dict]:
        if not snapshot.get("fresh", True):
            return [{"signal_type":"NO_TRADE","side":None,"position_side":None,"action":"NOOP","reference_price":0,"leverage":1,"suggested_position_pct":0,"indicator_snapshot":{},"reason":"行情数据不新鲜，防御策略禁止交易","bar_id":None}]
        return []
