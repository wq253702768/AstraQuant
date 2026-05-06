from fastapi import FastAPI, Request
from astra_common.logger import configure_logging
from astra_common.response import success_response
from astra_common.tracing import TraceMiddleware
from app.api.v1.router import api_router
from app.config import settings
from app.middleware.auth import AuthMiddleware
from app.middleware.error_handler import install_error_handlers

configure_logging(settings.log_level)
app = FastAPI(title="AstraQuant API Gateway", version="0.1.0")
app.add_middleware(AuthMiddleware)
app.add_middleware(TraceMiddleware)
install_error_handlers(app)
app.include_router(api_router)

@app.get("/health")
async def health(request: Request):
    return success_response({"status": "ok", "service": settings.service_name}, request)
