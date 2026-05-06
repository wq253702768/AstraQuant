from decimal import Decimal
from app.domain.entities.position import Position
from app.domain.entities.backtest_trade import BacktestTrade

class PositionEngine:
    def apply_trade(self, position: Position | None, trade: BacktestTrade) -> Position:
        position = position or Position(symbol=trade.symbol, position_side=trade.position_side)
        if trade.action == "open":
            total_qty = position.quantity + trade.size
            if total_qty > 0:
                position.entry_price = ((position.entry_price * position.quantity) + (trade.fill_price * trade.size)) / total_qty if position.quantity else trade.fill_price
            position.quantity = total_qty
            position.leverage = trade.leverage
        elif trade.action in {"close", "reduce"}:
            closed = min(position.quantity, trade.size)
            if position.position_side == "long":
                pnl = (trade.fill_price - position.entry_price) * closed
            else:
                pnl = (position.entry_price - trade.fill_price) * closed
            position.realized_pnl += pnl
            position.quantity -= closed
        return position

    def unrealized_pnl(self, position: Position, mark_price: Decimal) -> Decimal:
        if position.position_side == "long":
            return (mark_price - position.entry_price) * position.quantity
        return (position.entry_price - mark_price) * position.quantity
