from decimal import Decimal
class PaperLiveComparator:
    def compare(self, paper: dict, live: dict) -> dict:
        pr = Decimal(str(paper.get("total_return", "0"))); lr = Decimal(str(live.get("total_return", "0")))
        pdd = abs(Decimal(str(paper.get("max_drawdown", "0.0001")))) or Decimal("0.0001"); ldd = abs(Decimal(str(live.get("max_drawdown", "0"))))
        return {"return_deviation": abs(lr-pr)/max(abs(pr), Decimal("0.0001")), "drawdown_deviation": abs(ldd-pdd)/pdd, "trade_count_deviation": abs(live.get("trade_count",0)-paper.get("trade_count",0))/max(abs(paper.get("trade_count",1)),1)}
