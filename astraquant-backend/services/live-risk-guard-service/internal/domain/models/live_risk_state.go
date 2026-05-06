package models

type LiveRiskState struct {
	ID                 string `json:"id"`
	Scope              string `json:"scope"`
	AccountID          string `json:"account_id"`
	StrategyID         string `json:"strategy_id"`
	StrategyVersionID  string `json:"strategy_version_id"`
	Exchange           string `json:"exchange"`
	InternalSymbol     string `json:"internal_symbol"`
	RiskState          string `json:"risk_state"`
	ReduceOnly         bool   `json:"reduce_only"`
	TradingBlocked     bool   `json:"trading_blocked"`
	EmergencyStopped   bool   `json:"emergency_stopped"`
	DailyLossPct       string `json:"daily_loss_pct"`
	CurrentDrawdownPct string `json:"current_drawdown_pct"`
	ConsecutiveLosses  int    `json:"consecutive_losses"`
	UnknownOrderCount  int    `json:"unknown_order_count"`
	LastTriggeredRule  string `json:"last_triggered_rule"`
	LastReason         string `json:"last_reason"`
	UpdatedAt          int64  `json:"updated_at"`
}
