package models

type StrategyRiskConfig struct {
	MaxSpreadPct           float64
	MaxAbsFundingRate      float64
	MaxLeverage            float64
	MaxPositionPct         float64
	MaxSingleTradeLossPct  float64
	MaxDailyLossPct        float64
	MaxConsecutiveLosses   int
	MaxStrategyDrawdownPct float64
	StopLossPct            float64
	OpenCooldownSeconds    int
}
type MarketSnapshot struct {
	Fresh           bool
	FreshnessStatus string
	SpreadPct       float64
	FundingRate     float64
	MarkPrice       string
}
type AccountSnapshot struct{ Equity string }
type PositionSnapshot struct{ Quantity string }
type RuntimeCounters struct {
	DailyLossPct       float64
	ConsecutiveLosses  int
	CurrentDrawdownPct float64
	CooldownActive     bool
	OrderUnknown       bool
}
type RiskContext struct {
	Signal           SignalInput
	StrategyRisk     StrategyRiskConfig
	MarketSnapshot   MarketSnapshot
	AccountSnapshot  AccountSnapshot
	PositionSnapshot PositionSnapshot
	RuntimeCounters  RuntimeCounters
	RuleVersion      string
}
