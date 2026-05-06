package models

type EmergencyControl struct {
	ID                string `json:"id"`
	Scope             string `json:"scope"`
	AccountID         string `json:"account_id"`
	StrategyID        string `json:"strategy_id"`
	StrategyVersionID string `json:"strategy_version_id"`
	Action            string `json:"action"`
	Enabled           bool   `json:"enabled"`
	Reason            string `json:"reason"`
	TriggeredBy       string `json:"triggered_by"`
	TriggeredAt       int64  `json:"triggered_at"`
	ReleasedBy        string `json:"released_by"`
	ReleasedAt        int64  `json:"released_at"`
}
