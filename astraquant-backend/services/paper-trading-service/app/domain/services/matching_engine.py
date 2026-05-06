from decimal import Decimal
from app.config import settings
from app.domain.services.fee_engine import FeeEngine
from app.domain.services.slippage_engine import SlippageEngine
class MatchingEngine:
    def fill(self, order, bbo: dict):
        bid=Decimal(str(bbo.get("bid_price","0"))); ask=Decimal(str(bbo.get("ask_price","0")))
        fill, slip = SlippageEngine().fill_price(order.side, order.action, bid, ask, settings.slippage_pct)
        notional = fill * order.quantity
        fee = FeeEngine().fee(notional, settings.taker_fee_rate)
        return {"fill_price": fill, "notional_value": notional, "fee": fee, "slippage": slip}
