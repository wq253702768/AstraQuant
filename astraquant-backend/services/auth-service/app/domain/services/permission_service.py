ROLE_PERMISSIONS = {
    "admin": ["*"],
    "strategy_researcher": ["strategy:create", "strategy:read", "strategy:update", "backtest:run", "backtest:read", "ai:run", "ai:read", "market_data:sync", "market_data:read"],
    "trader": ["strategy:read", "trade:simulate", "trade:approve_live"],
    "risk_manager": ["strategy:read", "risk:manage", "audit:read"],
    "viewer": ["strategy:read", "backtest:read", "ai:read", "market_data:read"],
}

def permissions_for_roles(roles: list[str]) -> list[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, []))
    return sorted(permissions)
