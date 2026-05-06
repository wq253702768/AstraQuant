from contextvars import ContextVar
import logging
import time
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

TRACE_HEADER = "X-Trace-Id"
_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)
logger = logging.getLogger("astra_common.request")

def new_trace_id() -> str:
    return f"trace_{uuid4().hex}"

def get_current_trace_id() -> str | None:
    return _trace_id.get()

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get(TRACE_HEADER) or new_trace_id()
        request.state.trace_id = trace_id
        token = _trace_id.set(trace_id)
        started_at = time.perf_counter()
        try:
            response = await call_next(request)
            response.headers[TRACE_HEADER] = trace_id
            elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
            logger.info(
                "request completed method=%s path=%s status_code=%s latency_ms=%s",
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
            )
            return response
        finally:
            _trace_id.reset(token)
