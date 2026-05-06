class QueryKlineService:
    def __init__(self, repository):
        self.repository = repository
    def query(self, exchange: str, symbol: str, timeframe: str, start_time, end_time, limit: int):
        return self.repository.query(exchange, symbol, timeframe, start_time, end_time, limit)
