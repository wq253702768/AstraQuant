package models

type LiveOrder struct {
	ID                string `json:"id"`
	AccountID         string `json:"account_id"`
	SignalID          string `json:"signal_id"`
	RiskDecisionID    string `json:"risk_decision_id"`
	StrategyID        string `json:"strategy_id"`
	StrategyVersionID string `json:"strategy_version_id"`
	Exchange          string `json:"exchange"`
	InternalSymbol    string `json:"internal_symbol"`
	ExchangeSymbol    string `json:"exchange_symbol"`
	ClientOrderID     string `json:"client_order_id"`
	ExchangeOrderID   string `json:"exchange_order_id"`
	Side              string `json:"side"`
	PositionSide      string `json:"position_side"`
	Action            string `json:"action"`
	OrderType         string `json:"order_type"`
	TradeMode         string `json:"trade_mode"`
	Price             string `json:"price"`
	Quantity          string `json:"quantity"`
	FilledQuantity    string `json:"filled_quantity"`
	AvgFillPrice      string `json:"avg_fill_price"`
	Leverage          string `json:"leverage"`
	ReduceOnly        bool   `json:"reduce_only"`
	ExecutionMode     string `json:"execution_mode"`
	Status            string `json:"status"`
	ErrorCode         string `json:"error_code"`
	ErrorMessage      string `json:"error_message"`
	IdempotencyKey    string `json:"idempotency_key"`
	TraceID           string `json:"trace_id"`
	CreatedAt         int64  `json:"created_at"`
	SubmittedAt       int64  `json:"submitted_at"`
	UpdatedAt         int64  `json:"updated_at"`
	FilledAt          int64  `json:"filled_at"`
}
