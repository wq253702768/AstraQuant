package models

type LiveRiskRuleConfig struct {
	RuleCode string
	RuleName string
	Scope    string
	Enabled  bool
	Level    string
	Action   string
	Config   map[string]any
	Version  string
}
type LiveRiskInput struct {
	AccountDailyLossPct        float64
	StrategyDailyLossPct       float64
	AccountDrawdownPct         float64
	StrategyDrawdownPct        float64
	ConsecutiveLosses          int
	UnknownOrderCount          int
	OrderFailureCount          int
	AccountStaleSeconds        int
	PositionStaleSeconds       int
	GatewayDisconnectedSeconds int
	SlippagePct                float64
	FeeMultiplier              float64
	FundingRate                float64
}
