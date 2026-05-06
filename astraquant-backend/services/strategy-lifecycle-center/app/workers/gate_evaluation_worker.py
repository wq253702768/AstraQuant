from app.application.services.lifecycle_service import lifecycle_service


def evaluate_gate(strategy_version_id: str, gate_code: str) -> dict:
    return lifecycle_service.evaluate_gate(strategy_version_id, gate_code).to_dict()
