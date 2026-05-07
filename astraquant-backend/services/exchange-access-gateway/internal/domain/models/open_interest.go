package models

type UnifiedOpenInterest struct {
	Exchange        string `json:"exchange"`
	InternalSymbol  string `json:"internal_symbol"`
	ExchangeSymbol  string `json:"exchange_symbol"`
	OpenInterest    string `json:"open_interest"`
	OpenInterestCcy string `json:"open_interest_ccy"`
	ExchangeTime    int64  `json:"exchange_time"`
	ReceivedAt      int64  `json:"received_at"`
}

type GetOpenInterestRequest struct{ Symbol string }
