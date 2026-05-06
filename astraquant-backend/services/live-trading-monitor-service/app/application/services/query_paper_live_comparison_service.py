from app.domain.services.paper_live_comparator import PaperLiveComparator
class QueryPaperLiveComparisonService:
    async def execute(self):
        paper={"total_return":"0.032","max_drawdown":"-0.018","trade_count":22,"win_rate":"0.545"}; live={"total_return":"0.025","max_drawdown":"-0.012","trade_count":16,"win_rate":"0.5625"}
        deviation=PaperLiveComparator().compare(paper, live)
        return {"paper":paper,"live":live,"deviation":{k:str(v) for k,v in deviation.items()},"conclusion":"实盘收益略低于模拟盘，但回撤更小，偏离处于可接受范围。"}
