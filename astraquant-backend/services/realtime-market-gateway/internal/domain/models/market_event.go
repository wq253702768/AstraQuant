package models

type UnifiedMarketEvent struct {
	EventID        string         `json:"event_id"`
	EventType      string         `json:"event_type"`
	Exchange       string         `json:"exchange"`
	InternalSymbol string         `json:"internal_symbol"`
	ExchangeSymbol string         `json:"exchange_symbol"`
	EventTime      int64          `json:"event_time"`
	ReceiveTime    int64          `json:"receive_time"`
	LatencyMs      int64          `json:"latency_ms"`
	Payload        map[string]any `json:"payload"`
}
