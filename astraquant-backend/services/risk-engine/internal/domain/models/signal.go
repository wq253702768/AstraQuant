package models

type SignalInput struct {
	SignalID             string         `json:"signal_id"`
	StrategyID           string         `json:"strategy_id"`
	StrategyVersionID    string         `json:"strategy_version_id"`
	Exchange             string         `json:"exchange"`
	InternalSymbol       string         `json:"internal_symbol"`
	SignalType           string         `json:"signal_type"`
	Side                 string         `json:"side"`
	PositionSide         string         `json:"position_side"`
	Action               string         `json:"action"`
	ReferencePrice       string         `json:"reference_price"`
	SuggestedPositionPct float64        `json:"suggested_position_pct"`
	Leverage             float64        `json:"leverage"`
	MarketSnapshot       map[string]any `json:"market_snapshot"`
	FreshnessSnapshot    map[string]any `json:"freshness_snapshot"`
	TraceID              string         `json:"trace_id"`
}

func (s SignalInput) IsOpen() bool {
	return s.Action == "OPEN" || s.SignalType == "OPEN_LONG" || s.SignalType == "OPEN_SHORT"
}
func (s SignalInput) IsCloseOrReduce() bool { return s.Action == "CLOSE" || s.Action == "REDUCE" }
