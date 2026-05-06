class FundingRateRepository:
    def __init__(self, client):
        self.client = client
    def insert_many(self, rows: list[dict]) -> None:
        if rows: self.client.insert("funding_rate_history", rows)
