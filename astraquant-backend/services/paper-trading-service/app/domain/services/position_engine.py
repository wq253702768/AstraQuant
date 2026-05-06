from decimal import Decimal
from app.domain.entities.paper_position import PaperPosition
class PositionEngine:
    def open_position(self, account_id: str, order, fill: dict) -> PaperPosition:
        margin = fill["notional_value"] / order.leverage
        return PaperPosition(None, account_id, order.strategy_id, order.strategy_version_id, order.exchange, order.internal_symbol, order.position_side, order.quantity, fill["fill_price"], fill["fill_price"], order.leverage, margin, Decimal("0"), Decimal("0"), "OPEN")
    def add(self, position: PaperPosition, quantity: Decimal, fill_price: Decimal) -> PaperPosition:
        new_qty = position.quantity + quantity
        position.entry_price = ((position.entry_price * position.quantity) + (fill_price * quantity)) / new_qty
        position.quantity = new_qty
        return position
    def close_long(self, position: PaperPosition, quantity: Decimal, fill_price: Decimal) -> Decimal:
        qty = min(position.quantity, quantity); pnl=(fill_price-position.entry_price)*qty; position.quantity -= qty; position.realized_pnl += pnl; position.status = "CLOSED" if position.quantity == 0 else "OPEN"; return pnl
    def close_short(self, position: PaperPosition, quantity: Decimal, fill_price: Decimal) -> Decimal:
        qty = min(position.quantity, quantity); pnl=(position.entry_price-fill_price)*qty; position.quantity -= qty; position.realized_pnl += pnl; position.status = "CLOSED" if position.quantity == 0 else "OPEN"; return pnl
