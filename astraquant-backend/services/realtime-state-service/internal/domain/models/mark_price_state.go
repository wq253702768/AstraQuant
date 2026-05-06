package models

type MarkPriceState struct {
	BaseState
	MarkPrice  string `json:"mark_price"`
	IndexPrice string `json:"index_price"`
}
