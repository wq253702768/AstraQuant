package models

const (
	Fresh  = "FRESH"
	Normal = "NORMAL"
	Slow   = "SLOW"
	Stale  = "STALE"
)

type Freshness struct {
	LatencyMs int64  `json:"latency_ms"`
	Level     string `json:"level"`
}
