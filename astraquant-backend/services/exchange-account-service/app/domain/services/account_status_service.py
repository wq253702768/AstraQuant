class AccountStatusService:
    def enabled_status(self, has_trade: bool) -> tuple[str, bool]: return ("ACTIVE", False) if has_trade else ("READ_ONLY", False)
