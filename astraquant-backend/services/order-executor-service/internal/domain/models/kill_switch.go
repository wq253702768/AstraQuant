package models

type KillSwitchState struct {
	Scope       string `json:"scope"`
	AccountID   string `json:"account_id"`
	StrategyID  string `json:"strategy_id"`
	Enabled     bool   `json:"enabled"`
	Reason      string `json:"reason"`
	TriggeredBy string `json:"triggered_by"`
	TriggeredAt int64  `json:"triggered_at"`
}
