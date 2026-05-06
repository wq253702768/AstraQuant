class DrawdownRepository:
    def __init__(self, client):
        self.client = client
    def insert_many(self, rows: list[dict]) -> None:
        if rows:
            self.client.insert("strategy_drawdown", rows)
    def query_by_task(self, task_id: str, limit: int = 1000):
        return []
