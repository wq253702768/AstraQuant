from app.application.services.lifecycle_service import lifecycle_service


def collect_lifecycle_evidence(strategy_version_id: str) -> dict:
    return {"strategy_version_id": strategy_version_id, "evidence_count": len(lifecycle_service.store.list_evidence(strategy_version_id))}
