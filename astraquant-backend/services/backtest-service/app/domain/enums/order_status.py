from enum import StrEnum
class OrderStatus(StrEnum):
    CREATED = "CREATED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
