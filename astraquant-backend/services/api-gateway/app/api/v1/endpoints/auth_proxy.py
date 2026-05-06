from fastapi import APIRouter, Request
from app.clients.auth_client import AuthClient

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login(payload: dict, request: Request):
    return await AuthClient().login(payload, request)

@router.post("/refresh")
async def refresh(payload: dict, request: Request):
    return await AuthClient().refresh(payload, request)

@router.post("/logout")
async def logout(payload: dict, request: Request):
    authorization = request.headers.get("Authorization", "")
    token = authorization.removeprefix("Bearer ").strip()
    return await AuthClient().logout(payload, token, request)

@router.put("/password")
async def change_password(payload: dict, request: Request):
    authorization = request.headers.get("Authorization", "")
    token = authorization.removeprefix("Bearer ").strip()
    return await AuthClient().change_password(payload, token, request)

@router.get("/me")
async def me(request: Request):
    authorization = request.headers.get("Authorization", "")
    token = authorization.removeprefix("Bearer ").strip()
    return await AuthClient().me(token, request)
