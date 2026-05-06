class BacktestTradeRepository:
    def __init__(self, client):
        self.client = client
    def insert_many(self, rows: list[dict]) -> None:
        if rows:
            self.client.insert("backtest_trade", rows)
    def query_by_task(self, task_id: str, limit: int = 1000):
        return []
