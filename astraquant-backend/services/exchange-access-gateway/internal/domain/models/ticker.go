package models

type UnifiedTicker struct {
	Exchange       string `json:"exchange"`
	InternalSymbol string `json:"internal_symbol"`
	ExchangeSymbol string `json:"exchange_symbol"`
	LastPrice      string `json:"last_price"`
	BestBidPrice   string `json:"best_bid_price"`
	BestAskPrice   string `json:"best_ask_price"`
	BestBidSize    string `json:"best_bid_size"`
	BestAskSize    string `json:"best_ask_size"`
	Open24h        string `json:"open_24h"`
	High24h        string `json:"high_24h"`
	Low24h         string `json:"low_24h"`
	Volume24h      string `json:"volume_24h"`
	VolumeCcy24h   string `json:"volume_ccy_24h"`
	ExchangeTime   int64  `json:"exchange_time"`
	ReceivedAt     int64  `json:"received_at"`
}

type GetTickerRequest struct{ Symbol string }
