package models

type KlineState struct {
	BaseState
	Timeframe   string `json:"timeframe"`
	Open        string `json:"open"`
	High        string `json:"high"`
	Low         string `json:"low"`
	Close       string `json:"close"`
	Volume      string `json:"volume"`
	QuoteVolume string `json:"quote_volume"`
	Confirmed   bool   `json:"confirmed"`
}
