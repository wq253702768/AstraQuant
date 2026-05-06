package models

type Subscription struct {
	Exchange       string `json:"exchange"`
	Channel        string `json:"channel"`
	InternalSymbol string `json:"internal_symbol"`
	ExchangeSymbol string `json:"exchange_symbol"`
	Timeframe      string `json:"timeframe,omitempty"`
	Enabled        bool   `json:"enabled"`
}

func (s Subscription) Key() string {
	return s.Exchange + ":" + s.Channel + ":" + s.InternalSymbol + ":" + s.Timeframe
}
