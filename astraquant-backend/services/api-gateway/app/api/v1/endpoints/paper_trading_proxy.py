from fastapi import APIRouter, Request
from app.clients.paper_trading_client import PaperTradingClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["paper-trading"])
@router.post("/api/paper-trading/accounts")
async def create_account(payload: dict, request: Request): require_permission(request,"paper_trading:manage"); return await PaperTradingClient().request("POST","/paper-trading/accounts",request,payload)
@router.get("/api/paper-trading/accounts/{account_id}")
async def account(account_id: str, request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET",f"/paper-trading/accounts/{account_id}",request)
@router.get("/api/paper-trading/accounts/{account_id}/positions")
async def positions(account_id: str, request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET",f"/paper-trading/accounts/{account_id}/positions",request)
@router.get("/api/paper-trading/accounts/{account_id}/ledger")
async def ledger(account_id: str, request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET",f"/paper-trading/accounts/{account_id}/ledger",request)
@router.get("/api/paper-trading/orders")
async def orders(request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET","/paper-trading/orders",request,params=dict(request.query_params))
@router.get("/api/paper-trading/trades")
async def trades(request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET","/paper-trading/trades",request,params=dict(request.query_params))
@router.get("/api/paper-trading/performance/strategies/{strategy_version_id}")
async def perf(strategy_version_id: str, request: Request): require_permission(request,"paper_trading:read"); return await PaperTradingClient().request("GET",f"/paper-trading/performance/strategies/{strategy_version_id}",request)
