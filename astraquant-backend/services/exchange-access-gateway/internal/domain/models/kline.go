package models

type UnifiedKline struct {
	Exchange       string `json:"exchange"`
	InternalSymbol string `json:"internal_symbol"`
	ExchangeSymbol string `json:"exchange_symbol"`
	Timeframe      string `json:"timeframe"`
	Timestamp      int64  `json:"timestamp"`
	Open           string `json:"open"`
	High           string `json:"high"`
	Low            string `json:"low"`
	Close          string `json:"close"`
	Volume         string `json:"volume"`
	QuoteVolume    string `json:"quote_volume"`
}

type GetKlinesRequest struct {
	Symbol    string
	Timeframe string
	StartTime int64
	EndTime   int64
	Limit     int
}
