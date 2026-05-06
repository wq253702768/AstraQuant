from enum import StrEnum

class ErrorCode(StrEnum):
    SUCCESS = "SUCCESS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class AppError(Exception):
    def __init__(self, code: ErrorCode | str, message: str, status_code: int = 400, data: object | None = None):
        super().__init__(message)
        self.code = str(code)
        self.message = message
        self.status_code = status_code
        self.data = data
