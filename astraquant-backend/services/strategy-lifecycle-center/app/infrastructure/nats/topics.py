CONSUME_TOPICS = [
    "strategy.version.created",
    "backtest.completed",
    "backtest.failed",
    "ai_analysis.completed",
    "strategy_score.calculated",
    "simulation.admission.calculated",
    "live_monitor.admission.calculated",
    "live_risk.breaker.triggered",
    "kill_switch.triggered",
    "alert.created",
    "audit.event",
]

STATE_CHANGED = "lifecycle.state.changed"
GATE_EVALUATED = "lifecycle.gate.evaluated"
APPROVAL_CREATED = "lifecycle.approval.created"
APPROVAL_APPROVED = "lifecycle.approval.approved"
APPROVAL_REJECTED = "lifecycle.approval.rejected"
SMALL_LIVE_APPROVED = "lifecycle.small_live.approved"
ROLLBACK_TO_PAPER = "lifecycle.rollback_to_paper"
STRATEGY_PAUSED = "lifecycle.strategy.paused"
STRATEGY_RETIRED = "lifecycle.strategy.retired"
SCALE_UP_APPROVED = "lifecycle.scale_up.approved"
ALERT_EVENT = "alert.event"
AUDIT_EVENT = "audit.event"
