package models

type StateSnapshot struct {
	Exchange        string          `json:"exchange"`
	InternalSymbol  string          `json:"internal_symbol"`
	Market          *MarketState    `json:"market"`
	BBO             *BBOState       `json:"bbo"`
	LastTrade       *TradeState     `json:"last_trade"`
	Klines          []KlineState    `json:"klines"`
	MarkPrice       *MarkPriceState `json:"mark_price"`
	Funding         *FundingState   `json:"funding"`
	Fresh           bool            `json:"fresh"`
	FreshnessStatus string          `json:"freshness_status"`
	StaleReasons    []string        `json:"stale_reasons"`
	SnapshotTime    int64           `json:"snapshot_time"`
}

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
