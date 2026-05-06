package models

type TradeState struct {
	BaseState
	TradeID string `json:"trade_id"`
	Price   string `json:"price"`
	Size    string `json:"size"`
	Side    string `json:"side"`
}
