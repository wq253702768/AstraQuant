package models

type RiskDecision struct {
	ID                string          `json:"id"`
	SignalID          string          `json:"signal_id"`
	StrategyID        string          `json:"strategy_id"`
	StrategyVersionID string          `json:"strategy_version_id"`
	Exchange          string          `json:"exchange"`
	InternalSymbol    string          `json:"internal_symbol"`
	Decision          string          `json:"decision"`
	Approved          bool            `json:"approved"`
	ReduceOnly        bool            `json:"reduce_only"`
	PauseStrategy     bool            `json:"pause_strategy"`
	TriggeredRules    []TriggeredRule `json:"triggered_rules"`
	RejectReasons     []string        `json:"reject_reasons"`
	Warnings          []string        `json:"warnings"`
	RiskSnapshot      map[string]any  `json:"risk_snapshot"`
	MarketSnapshot    map[string]any  `json:"market_snapshot"`
	AccountSnapshot   map[string]any  `json:"account_snapshot"`
	PositionSnapshot  map[string]any  `json:"position_snapshot"`
	RuleVersion       string          `json:"rule_version"`
	TraceID           string          `json:"trace_id"`
	CreatedAt         int64           `json:"created_at"`
}
