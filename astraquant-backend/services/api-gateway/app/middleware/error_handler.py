from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from astra_common.errors import AppError, ErrorCode
from astra_common.response import error_response

def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.code, exc.message, trace_id, exc.data).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=422,
            content=error_response(
                ErrorCode.VALIDATION_ERROR.value,
                "参数校验失败",
                trace_id,
                {"errors": exc.errors()},
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        trace_id = getattr(request.state, "trace_id", None)
        return JSONResponse(
            status_code=500,
            content=error_response(
                ErrorCode.INTERNAL_ERROR.value,
                "系统内部错误",
                trace_id,
            ).model_dump(),
        )
