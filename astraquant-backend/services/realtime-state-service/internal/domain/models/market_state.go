package models

type MarketState struct {
	BaseState
	LastPrice      string `json:"last_price"`
	Open24h        string `json:"open_24h"`
	High24h        string `json:"high_24h"`
	Low24h         string `json:"low_24h"`
	Volume24h      string `json:"volume_24h"`
	QuoteVolume24h string `json:"quote_volume_24h"`
}
