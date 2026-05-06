from fastapi import APIRouter, Request

from astra_common.response import success_response
from app.application.services.lifecycle_service import lifecycle_service

api_router = APIRouter(prefix="/lifecycle", tags=["lifecycle"])


def actor_id(request: Request) -> str | None:
    return request.headers.get("X-User-Id")


@api_router.get("/strategies")
async def list_strategies(request: Request):
    data = lifecycle_service.list_states(dict(request.query_params))
    return success_response(data, request)


@api_router.post("/strategies")
async def init_strategy(payload: dict, request: Request):
    state = lifecycle_service.init_lifecycle(
        payload["strategy_id"],
        payload["strategy_version_id"],
        payload.get("created_by") or actor_id(request),
        getattr(request.state, "trace_id", None),
    )
    return success_response(state, request)


@api_router.get("/strategies/{strategy_version_id}")
async def get_strategy(strategy_version_id: str, request: Request):
    return success_response(lifecycle_service.get_state(strategy_version_id), request)


@api_router.post("/strategies/{strategy_version_id}/transition")
async def transition(strategy_version_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.transition(
            strategy_version_id,
            payload.get("to_status") or payload["target_status"],
            payload.get("reason", "manual transition"),
            "USER_ACTION",
            actor_id(request),
            getattr(request.state, "trace_id", None),
        ),
        request,
    )


@api_router.get("/strategies/{strategy_version_id}/timeline")
async def timeline(strategy_version_id: str, request: Request):
    return success_response(lifecycle_service.timeline(strategy_version_id), request)


@api_router.get("/strategies/{strategy_version_id}/evidence")
async def evidence(strategy_version_id: str, request: Request):
    return success_response(lifecycle_service.evidence(strategy_version_id), request)


@api_router.post("/strategies/{strategy_version_id}/evidence")
async def add_evidence(strategy_version_id: str, payload: dict, request: Request):
    return success_response(lifecycle_service.add_evidence(strategy_version_id, payload), request)


@api_router.post("/events/strategy-version-created")
async def consume_strategy_version_created(payload: dict, request: Request):
    state = lifecycle_service.init_lifecycle(
        payload["strategy_id"],
        payload["strategy_version_id"],
        payload.get("created_by") or actor_id(request),
        getattr(request.state, "trace_id", None),
    )
    return success_response(state, request)


@api_router.post("/events/backtest-completed")
async def consume_backtest_completed(payload: dict, request: Request):
    return success_response(lifecycle_service.consume_backtest_completed(payload, getattr(request.state, "trace_id", None)), request)


@api_router.post("/events/ai-analysis-completed")
async def consume_ai_analysis_completed(payload: dict, request: Request):
    return success_response(lifecycle_service.consume_ai_analysis_completed(payload, getattr(request.state, "trace_id", None)), request)


@api_router.post("/events/strategy-score-calculated")
async def consume_strategy_score_calculated(payload: dict, request: Request):
    return success_response(lifecycle_service.consume_strategy_score_calculated(payload, getattr(request.state, "trace_id", None)), request)


@api_router.post("/events/simulation-admission-calculated")
async def consume_simulation_admission(payload: dict, request: Request):
    return success_response(lifecycle_service.consume_simulation_admission(payload, getattr(request.state, "trace_id", None)), request)


@api_router.post("/events/live-monitor-admission-calculated")
async def consume_live_admission(payload: dict, request: Request):
    state = lifecycle_service.get_state(payload["strategy_version_id"])
    state.live_observation_id = payload.get("live_observation_id")
    lifecycle_service.add_evidence(state.strategy_version_id, {"evidence_type": "LIVE_ADMISSION_RESULT", "resource_type": "live_admission_result", "resource_id": payload.get("live_admission_result_id", "live_admission"), "title": "实盘准入结果", "score": payload.get("score"), "passed": payload.get("passed", True)})
    return success_response(lifecycle_service.apply_live_admission(state.strategy_version_id, payload, getattr(request.state, "trace_id", None)), request)


@api_router.post("/strategies/{strategy_version_id}/gates/evaluate")
async def evaluate_gate(strategy_version_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.evaluate_gate(strategy_version_id, payload["gate_code"], getattr(request.state, "trace_id", None)),
        request,
    )


@api_router.post("/strategies/{strategy_version_id}/applications/small-live")
async def small_live_application(strategy_version_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.create_application(
            strategy_version_id,
            "SMALL_LIVE_APPLICATION",
            payload.get("request_reason"),
            actor_id(request),
            getattr(request.state, "trace_id", None),
        ),
        request,
    )


@api_router.post("/strategies/{strategy_version_id}/applications/scale-up")
async def scale_up_application(strategy_version_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.create_application(
            strategy_version_id,
            "SCALE_UP_APPLICATION",
            payload.get("request_reason"),
            actor_id(request),
            getattr(request.state, "trace_id", None),
        ),
        request,
    )


@api_router.post("/approvals/{approval_id}/approve")
async def approve(approval_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.approve(approval_id, actor_id(request), payload.get("approval_comment"), getattr(request.state, "trace_id", None)),
        request,
    )


@api_router.post("/approvals/{approval_id}/reject")
async def reject(approval_id: str, payload: dict, request: Request):
    return success_response(
        lifecycle_service.reject(approval_id, actor_id(request), payload.get("rejection_reason"), getattr(request.state, "trace_id", None)),
        request,
    )


@api_router.post("/strategies/{strategy_version_id}/rollback-to-paper")
async def rollback(strategy_version_id: str, payload: dict, request: Request):
    return success_response(lifecycle_service.rollback_to_paper(strategy_version_id, payload.get("reason"), actor_id(request), getattr(request.state, "trace_id", None)), request)


@api_router.post("/strategies/{strategy_version_id}/pause")
async def pause(strategy_version_id: str, payload: dict, request: Request):
    return success_response(lifecycle_service.pause(strategy_version_id, payload.get("reason"), actor_id(request), getattr(request.state, "trace_id", None)), request)


@api_router.post("/strategies/{strategy_version_id}/retire")
async def retire(strategy_version_id: str, payload: dict, request: Request):
    return success_response(lifecycle_service.retire(strategy_version_id, payload.get("reason"), actor_id(request), getattr(request.state, "trace_id", None)), request)


@api_router.get("/dashboard/overview")
async def dashboard(request: Request):
    return success_response(lifecycle_service.dashboard(), request)
