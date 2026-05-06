class LifecycleCache:
    def key(self, strategy_version_id: str) -> str:
        return f"lifecycle:state:{strategy_version_id}"

    def dashboard_key(self) -> str:
        return "lifecycle:dashboard:overview"
