package models

type UnifiedMarkPrice struct {
	Exchange       string `json:"exchange"`
	InternalSymbol string `json:"internal_symbol"`
	ExchangeSymbol string `json:"exchange_symbol"`
	MarkPrice      string `json:"mark_price"`
	IndexPrice     string `json:"index_price"`
	Timestamp      int64  `json:"timestamp"`
}

type GetMarkPriceRequest struct{ Symbol string }
