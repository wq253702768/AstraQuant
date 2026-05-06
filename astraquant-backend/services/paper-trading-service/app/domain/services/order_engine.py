from decimal import Decimal
from app.domain.entities.paper_order import PaperOrder
class OrderEngine:
    def create_market_order(self, risk: dict, account_id: str) -> PaperOrder:
        key = f"paper_order:{risk['risk_decision_id']}:{risk['signal_id']}"
        return PaperOrder(None, account_id, risk["signal_id"], risk["risk_decision_id"], risk["strategy_id"], risk["strategy_version_id"], risk.get("exchange","OKX"), risk["internal_symbol"], risk["side"], risk["position_side"], risk["action"], "MARKET", Decimal(str(risk.get("reference_price", "0"))), Decimal(str(risk.get("quantity", "0.01"))), Decimal(str(risk.get("leverage", "1"))), "CREATED", key)
