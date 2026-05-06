package models

type UnifiedPosition struct {
	Exchange       string `json:"exchange"`
	AccountID      string `json:"account_id"`
	InternalSymbol string `json:"internal_symbol"`
	PositionSide   string `json:"position_side"`
	Quantity       string `json:"quantity"`
}
