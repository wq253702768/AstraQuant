package models

type UnifiedBalance struct {
	AccountID      string `json:"account_id"`
	Exchange       string `json:"exchange"`
	InternalSymbol string `json:"internal_symbol,omitempty"`
	EventTime      int64  `json:"event_time"`
}
