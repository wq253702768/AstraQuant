from enum import StrEnum


class GateResult(StrEnum):
    PASS = "PASS"
    REJECT = "REJECT"
    WAITING = "WAITING"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
