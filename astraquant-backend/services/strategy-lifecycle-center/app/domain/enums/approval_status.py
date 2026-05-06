from enum import StrEnum


class ApprovalStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"
