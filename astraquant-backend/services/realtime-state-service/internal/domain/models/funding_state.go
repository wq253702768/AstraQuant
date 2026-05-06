package models

type FundingState struct {
	BaseState
	FundingRate     string `json:"funding_rate"`
	NextFundingTime int64  `json:"next_funding_time"`
	MarkPrice       string `json:"mark_price"`
}
