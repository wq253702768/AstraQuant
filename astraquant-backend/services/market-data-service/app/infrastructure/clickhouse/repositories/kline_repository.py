class KlineRepository:
    def __init__(self, client):
        self.client = client

    def insert_many(self, rows: list[dict]) -> None:
        if not rows:
            return
        self.client.insert("market_kline", rows)

    def query(self, exchange: str, symbol: str, timeframe: str, start_time, end_time, limit: int) -> list[dict]:
        query = """
        SELECT exchange, internal_symbol, exchange_symbol, timeframe, ts, open, high, low, close, volume, quote_volume
        FROM market_kline
        WHERE exchange = %(exchange)s AND internal_symbol = %(symbol)s AND timeframe = %(timeframe)s AND ts >= %(start)s AND ts < %(end)s
        ORDER BY ts ASC
        LIMIT %(limit)s
        """
        return self.client.query(query, parameters={"exchange": exchange, "symbol": symbol, "timeframe": timeframe, "start": start_time, "end": end_time, "limit": limit}).result_rows
