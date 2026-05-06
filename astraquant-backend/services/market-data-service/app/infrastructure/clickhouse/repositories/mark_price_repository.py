class MarkPriceRepository:
    def __init__(self, client):
        self.client = client
    def insert_many(self, rows: list[dict]) -> None:
        if rows: self.client.insert("mark_price_history", rows)
