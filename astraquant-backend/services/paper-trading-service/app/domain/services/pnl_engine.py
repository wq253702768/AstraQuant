class PnLEngine:
    def unrealized(self, position, mark_price):
        if position.position_side.upper() == "LONG": return (mark_price - position.entry_price) * position.quantity
        return (position.entry_price - mark_price) * position.quantity
