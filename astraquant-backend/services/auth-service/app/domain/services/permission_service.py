ROLE_PERMISSIONS = {
    "admin": ["*"],
    "strategy_researcher": ["strategy:create", "strategy:read", "strategy:update", "backtest:run", "backtest:read", "ai:run", "ai:read", "market_data:sync", "market_data:read", "market_state:read", "signal:read", "signal:manage", "report:build", "report:read"],
    "trader": ["strategy:read", "signal:read", "signal:manage", "paper_trading:read", "paper_trading:manage", "paper_monitor:read", "paper_monitor:manage", "exchange_account:read", "trade:simulate", "trade:approve_live"],
    "risk_manager": ["strategy:read", "signal:read", "risk:read", "risk:manage", "exchange_account:read", "audit:read", "report:read"],
    "viewer": ["strategy:read", "backtest:read", "ai:read", "market_data:read", "market_state:read", "signal:read", "risk:read", "paper_trading:read", "paper_monitor:read", "exchange_account:read", "report:read"],
}

def permissions_for_roles(roles: list[str]) -> list[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, []))
    return sorted(permissions)
