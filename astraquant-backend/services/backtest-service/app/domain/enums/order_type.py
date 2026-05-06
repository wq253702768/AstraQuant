from enum import StrEnum
class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    IOC = "IOC"
    POST_ONLY = "POST_ONLY"
