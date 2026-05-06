package models

type BBOState struct {
	BaseState
	BidPrice  string `json:"bid_price"`
	BidSize   string `json:"bid_size"`
	AskPrice  string `json:"ask_price"`
	AskSize   string `json:"ask_size"`
	Spread    string `json:"spread"`
	SpreadPct string `json:"spread_pct"`
}
