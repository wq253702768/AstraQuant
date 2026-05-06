from typing import Generic, TypeVar
from fastapi import Request
from pydantic import BaseModel
from .errors import ErrorCode

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: str = ErrorCode.SUCCESS.value
    message: str = "OK"
    trace_id: str | None = None
    data: T | None = None

def get_trace_id(request: Request | None) -> str | None:
    return getattr(request.state, "trace_id", None) if request else None

def success_response(data: T | None = None, request: Request | None = None, message: str = "OK") -> ApiResponse[T]:
    return ApiResponse[T](code=ErrorCode.SUCCESS.value, message=message, trace_id=get_trace_id(request), data=data)

def error_response(code: str, message: str, trace_id: str | None, data: object | None = None) -> ApiResponse[object]:
    return ApiResponse[object](code=code, message=message, trace_id=trace_id, data=data)
