package models

type LiveTrade struct {
	ID           string `json:"id"`
	LiveOrderID  string `json:"live_order_id"`
	AccountID    string `json:"account_id"`
	FillPrice    string `json:"fill_price"`
	FillQuantity string `json:"fill_quantity"`
	Fee          string `json:"fee"`
	CreatedAt    int64  `json:"created_at"`
}
