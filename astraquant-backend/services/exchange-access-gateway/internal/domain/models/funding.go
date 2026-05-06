package models

type UnifiedFundingRate struct {
	Exchange        string `json:"exchange"`
	InternalSymbol  string `json:"internal_symbol"`
	ExchangeSymbol  string `json:"exchange_symbol"`
	FundingRate     string `json:"funding_rate"`
	RealizedRate    string `json:"realized_rate"`
	FundingTime     int64  `json:"funding_time"`
	NextFundingTime int64  `json:"next_funding_time"`
	MarkPrice       string `json:"mark_price"`
}

type GetFundingRateRequest struct{ Symbol string }

type GetFundingRateHistoryRequest struct {
	Symbol    string
	StartTime int64
	EndTime   int64
	Limit     int
}
