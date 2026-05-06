package models

type CircuitBreakerEvent struct {
	ID                  string         `json:"id"`
	Scope               string         `json:"scope"`
	Level               string         `json:"level"`
	AccountID           string         `json:"account_id"`
	StrategyID          string         `json:"strategy_id"`
	StrategyVersionID   string         `json:"strategy_version_id"`
	InternalSymbol      string         `json:"internal_symbol"`
	RuleCode            string         `json:"rule_code"`
	RuleName            string         `json:"rule_name"`
	CurrentValue        string         `json:"current_value"`
	ThresholdValue      string         `json:"threshold_value"`
	Action              string         `json:"action"`
	Reason              string         `json:"reason"`
	Snapshot            map[string]any `json:"snapshot"`
	AutoCancelRequested bool           `json:"auto_cancel_requested"`
	KillSwitchTriggered bool           `json:"kill_switch_triggered"`
	Status              string         `json:"status"`
	TriggeredAt         int64          `json:"triggered_at"`
	ResolvedAt          int64          `json:"resolved_at"`
	ResolvedBy          string         `json:"resolved_by"`
}
