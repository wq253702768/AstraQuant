from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from uuid import uuid4
from sqlalchemy import insert, select

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
sys.path.insert(0, str(ROOT / "services/auth-service"))

from astra_common.security import hash_password
from app.domain.services.permission_service import ROLE_PERMISSIONS
from app.infrastructure.db.models import PermissionModel, RoleModel, RolePermissionModel, UserAccountModel, UserRoleModel
from app.infrastructure.db.session import SessionLocal

ROLE_NAMES = {
    "admin": "管理员",
    "strategy_researcher": "策略研究员",
    "trader": "交易员",
    "risk_manager": "风控管理员",
    "viewer": "观察员",
}

PERMISSION_NAMES = {
    "strategy:create": "创建策略",
    "strategy:read": "查看策略",
    "strategy:update": "修改策略",
    "strategy:delete": "删除/废弃策略",
    "backtest:run": "运行回测",
    "backtest:read": "查看回测",
    "ai:run": "运行AI分析",
    "ai:read": "查看AI分析",
    "trade:simulate": "启用模拟盘",
    "trade:approve_live": "批准实盘",
    "risk:manage": "管理风控",
    "audit:read": "查看审计",
    "market_data:sync": "同步行情数据",
    "market_data:read": "查看行情数据",
    "report:build": "生成报告",
    "report:read": "查看报告",
    "market_state:read": "查看实时行情状态",
    "signal:read": "查看交易信号",
    "signal:manage": "管理信号运行",
    "risk:read": "查看风控决策",
    "risk:manage": "管理风控",
    "paper_trading:read": "查看模拟盘",
    "paper_trading:manage": "管理模拟盘",
    "paper_monitor:read": "查看模拟盘监控",
    "paper_monitor:manage": "管理模拟盘观察",
    "exchange_account:read": "查看交易所账户",
    "exchange_account:manage": "管理交易所账户",
    "exchange_credential:manage": "管理交易所凭证",
}

async def main() -> None:
    async with SessionLocal() as session:
        permissions: dict[str, PermissionModel] = {}
        for code, name in PERMISSION_NAMES.items():
            permission = (await session.execute(select(PermissionModel).where(PermissionModel.code == code))).scalar_one_or_none()
            if permission is None:
                resource, action = code.split(":", 1)
                permission = PermissionModel(
                    id=str(uuid4()),
                    code=code,
                    name=name,
                    resource=resource,
                    action=action,
                )
                session.add(permission)
                await session.flush()
            permissions[code] = permission

        roles: dict[str, RoleModel] = {}
        for code, permission_codes in ROLE_PERMISSIONS.items():
            role = (await session.execute(select(RoleModel).where(RoleModel.code == code))).scalar_one_or_none()
            if role is None:
                role = RoleModel(id=str(uuid4()), code=code, name=ROLE_NAMES[code], description=f"{ROLE_NAMES[code]}内置角色")
                session.add(role)
                await session.flush()
            roles[code] = role

            if "*" not in permission_codes:
                for permission_code in permission_codes:
                    existing = (
                        await session.execute(
                            select(RolePermissionModel).where(
                                RolePermissionModel.role_id == role.id,
                                RolePermissionModel.permission_id == permissions[permission_code].id,
                            )
                        )
                    ).scalar_one_or_none()
                    if existing is None:
                        await session.execute(
                            insert(RolePermissionModel).values(
                                role_id=role.id,
                                permission_id=permissions[permission_code].id,
                            )
                        )

        user = (await session.execute(select(UserAccountModel).where(UserAccountModel.username == "admin"))).scalar_one_or_none()
        if user is None:
            user = UserAccountModel(id=str(uuid4()), username="admin", password_hash=hash_password("password"), display_name="管理员", status="active")
            session.add(user)
            await session.flush()
            await session.execute(insert(UserRoleModel).values(user_id=user.id, role_id=roles["admin"].id))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
