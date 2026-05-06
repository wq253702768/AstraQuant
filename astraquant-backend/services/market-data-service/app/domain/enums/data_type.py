from enum import StrEnum

class DataType(StrEnum):
    INSTRUMENT = "instrument"
    KLINE = "kline"
    FUNDING_RATE = "funding_rate"
    MARK_PRICE = "mark_price"
