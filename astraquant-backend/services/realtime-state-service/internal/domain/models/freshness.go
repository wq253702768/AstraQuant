package models

type BaseState struct {
	Exchange        string `json:"exchange"`
	InternalSymbol  string `json:"internal_symbol"`
	ExchangeSymbol  string `json:"exchange_symbol"`
	EventTime       int64  `json:"event_time"`
	ReceiveTime     int64  `json:"receive_time"`
	UpdateTime      int64  `json:"update_time"`
	LatencyMs       int64  `json:"latency_ms"`
	FreshnessStatus string `json:"freshness_status"`
	Fresh           bool   `json:"fresh"`
	StaleReason     string `json:"stale_reason,omitempty"`
}
