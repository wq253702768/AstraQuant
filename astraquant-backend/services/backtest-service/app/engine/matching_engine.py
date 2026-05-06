from decimal import Decimal
from app.domain.entities.backtest_order import BacktestOrder
from app.domain.entities.backtest_trade import BacktestTrade
from app.engine.cost_engine import CostEngine

class MatchingEngine:
    def match(self, order: BacktestOrder, bar: dict, cost_model: dict, equity_after: Decimal) -> BacktestTrade | None:
        high = Decimal(str(bar["high"])); low = Decimal(str(bar["low"])); close = Decimal(str(bar["close"]))
        should_fill = order.order_type == "MARKET" or low <= order.price <= high or order.order_type == "IOC"
        if not should_fill:
            return None
        slippage_rate = Decimal(str(cost_model.get("default_slippage", "0.0003")))
        fill_price, slippage = CostEngine().apply_slippage(close if order.order_type == "MARKET" else order.price, order.side, slippage_rate)
        fee_rate = Decimal(str(cost_model.get("taker_fee_rate", "0.0005")))
        fee = CostEngine().fee(fill_price, order.size, fee_rate)
        return BacktestTrade(trade_time=bar["ts"], symbol=order.symbol, side=order.side, position_side=order.position_side, action=order.action, order_type=order.order_type, order_price=order.price, fill_price=fill_price, size=order.size, leverage=order.leverage, fee=fee, slippage=slippage, funding_fee=Decimal("0"), realized_pnl=Decimal("0"), equity_after=equity_after - fee, cl_ord_id=order.cl_ord_id, reason=order.reason)
