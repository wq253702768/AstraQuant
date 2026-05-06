from app.application.services.lifecycle_service import lifecycle_service


def sync_strategy_version_created(event: dict) -> dict:
    state = lifecycle_service.init_lifecycle(
        event["strategy_id"],
        event["strategy_version_id"],
        created_by=event.get("created_by"),
        trace_id=event.get("trace_id"),
    )
    return {"strategy_version_id": state.strategy_version_id, "status": state.current_status}
