from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_lifecycle_full_happy_path_api():
    payload = {"strategy_id": "11111111-1111-1111-1111-111111111111", "strategy_version_id": "22222222-2222-2222-2222-222222222222"}
    created = client.post("/lifecycle/events/strategy-version-created", json=payload).json()["data"]
    assert created["current_status"] == "DRAFT"

    bt = client.post("/lifecycle/events/backtest-completed", json={**payload, "backtest_id": "bt_001"}).json()["data"]
    assert bt["current_status"] == "BACKTEST_COMPLETED"

    ai = client.post("/lifecycle/events/ai-analysis-completed", json={**payload, "ai_analysis_id": "ai_001"}).json()["data"]
    assert ai["current_status"] == "AI_REVIEW_COMPLETED"

    score = client.post("/lifecycle/events/strategy-score-calculated", json={**payload, "strategy_score_id": "score_001", "score": 86.5, "passed": True}).json()["data"]
    assert score["current_status"] == "SIMULATION_READY"

    client.post("/lifecycle/strategies/22222222-2222-2222-2222-222222222222/transition", json={"target_status": "SIMULATION_RUNNING", "reason": "开始模拟盘"})
    client.post("/lifecycle/strategies/22222222-2222-2222-2222-222222222222/transition", json={"target_status": "SIMULATION_COMPLETED", "reason": "模拟盘完成"})
    admission = client.post("/lifecycle/events/simulation-admission-calculated", json={**payload, "simulation_admission_result_id": "adm_001", "score": 88.0, "passed": True}).json()["data"]
    assert admission["current_status"] == "SIMULATION_ADMISSION_PASSED"

    approval = client.post("/lifecycle/strategies/22222222-2222-2222-2222-222222222222/applications/small-live", json={"request_reason": "模拟盘达标"}).json()["data"]
    approved = client.post(f"/lifecycle/approvals/{approval['approval_id']}/approve", json={"approval_comment": "同意"}).json()["data"]
    assert approved["new_status"] == "SMALL_LIVE_APPROVED"

    detail = client.get("/lifecycle/strategies/22222222-2222-2222-2222-222222222222").json()["data"]
    assert detail["live_enabled"] is True
    assert client.get("/lifecycle/strategies/22222222-2222-2222-2222-222222222222/timeline").json()["data"]["items"]
    assert client.get("/lifecycle/strategies/22222222-2222-2222-2222-222222222222/evidence").json()["data"]["items"]
    assert client.get("/lifecycle/dashboard/overview").json()["data"]["total_strategy_versions"] >= 1
