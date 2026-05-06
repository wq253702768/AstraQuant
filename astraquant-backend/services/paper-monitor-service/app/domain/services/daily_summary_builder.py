from decimal import Decimal
class DailySummaryBuilder:
    def build(self, trades: list[dict], starting_equity: Decimal, ending_equity: Decimal) -> dict:
        wins=[t for t in trades if Decimal(str(t.get("realized_pnl",0)))>0]
        losses=[t for t in trades if Decimal(str(t.get("realized_pnl",0)))<0]
        return {"starting_equity":starting_equity,"ending_equity":ending_equity,"daily_return":(ending_equity-starting_equity)/starting_equity if starting_equity else Decimal("0"),"trade_count":len(trades),"win_trade_count":len(wins),"loss_trade_count":len(losses),"win_rate":Decimal(len(wins))/Decimal(len(trades)) if trades else Decimal("0"),"fee_total":sum((Decimal(str(t.get("fee",0))) for t in trades),Decimal("0")),"slippage_total":sum((Decimal(str(t.get("slippage",0))) for t in trades),Decimal("0")),"funding_fee_total":sum((Decimal(str(t.get("funding_fee",0))) for t in trades),Decimal("0"))}
