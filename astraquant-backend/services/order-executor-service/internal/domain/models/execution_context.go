package models

type RiskDecision struct {
	Decision          string
	Approved          bool
	ReduceOnly        bool
	SignalID          string
	RiskDecisionID    string
	StrategyID        string
	StrategyVersionID string
	Exchange          string
	InternalSymbol    string
}
type SignalSnapshot struct {
	Side         string
	PositionSide string
	Action       string
	OrderType    string
	Price        string
	Quantity     string
	Leverage     string
}
type AccountStateSnapshot struct {
	Fresh                 bool
	TradingEnabled        bool
	HasTradePermission    bool
	HasWithdrawPermission bool
	Equity                float64
}
type PositionStateSnapshot struct{ Fresh bool }
type OrderStateSnapshot struct{ Fresh bool }
type SimulationAdmissionResult struct {
	Decision         string
	ApprovalRequired bool
	ApprovalStatus   string
}
type ExecutionContext struct {
	SignalID          string
	RiskDecisionID    string
	AccountID         string
	StrategyID        string
	StrategyVersionID string
	Exchange          string
	InternalSymbol    string
	RiskDecision      RiskDecision
	Signal            SignalSnapshot
	AccountState      AccountStateSnapshot
	PositionState     PositionStateSnapshot
	OrderState        OrderStateSnapshot
	AdmissionResult   SimulationAdmissionResult
	KillSwitchState   KillSwitchState
	ExecutionMode     string
	TraceID           string
}
