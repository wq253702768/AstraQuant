from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.bind_credential_service import BindCredentialService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.credential import BindCredentialRequest
router=APIRouter(prefix="/exchange-accounts", tags=["credentials"])
@router.post("/{account_id}/credentials")
async def bind(account_id: str, payload: BindCredentialRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await BindCredentialService(session).execute(account_id,payload,operator_id); await session.commit(); return success_response(result,request)
