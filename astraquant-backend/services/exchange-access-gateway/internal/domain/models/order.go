package models

type UnifiedOrder struct {
	Exchange        string `json:"exchange"`
	AccountID       string `json:"account_id"`
	InternalSymbol  string `json:"internal_symbol"`
	ExchangeSymbol  string `json:"exchange_symbol"`
	Side            string `json:"side"`
	PositionSide    string `json:"position_side"`
	Action          string `json:"action"`
	OrderType       string `json:"order_type"`
	Price           string `json:"price"`
	Size            string `json:"size"`
	Leverage        string `json:"leverage"`
	ReduceOnly      bool   `json:"reduce_only"`
	ClientOrderID   string `json:"client_order_id"`
	ExchangeOrderID string `json:"exchange_order_id"`
	Status          string `json:"status"`
}

type PlaceOrderRequest struct{ Order UnifiedOrder }
type CancelOrderRequest struct {
	ExchangeOrderID string
	ClientOrderID   string
	Symbol          string
}
type AmendOrderRequest struct {
	ExchangeOrderID string
	ClientOrderID   string
	Symbol          string
	Price           string
	Size            string
}
