package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct {
	EventConsumed         prometheus.Counter
	UpdateTotal           *prometheus.CounterVec
	RedisWriteTotal       prometheus.Counter
	RedisWriteErrorTotal  prometheus.Counter
	StaleTotal            prometheus.Counter
	QueryTotal            prometheus.Counter
	WSConnections         prometheus.Gauge
	WSPushTotal           prometheus.Counter
	NATSConsumeErrorTotal prometheus.Counter
}

func NewMetrics() *Metrics {
	m := &Metrics{EventConsumed: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_event_consumed_total", Help: "events"}), UpdateTotal: prometheus.NewCounterVec(prometheus.CounterOpts{Name: "realtime_state_update_total", Help: "updates"}, []string{"event_type"}), RedisWriteTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_redis_write_total", Help: "redis writes"}), RedisWriteErrorTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_redis_write_error_total", Help: "redis errors"}), StaleTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_stale_total", Help: "stale"}), QueryTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_query_total", Help: "queries"}), WSConnections: prometheus.NewGauge(prometheus.GaugeOpts{Name: "realtime_state_ws_connections", Help: "ws"}), WSPushTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_ws_push_total", Help: "push"}), NATSConsumeErrorTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_state_nats_consume_error_total", Help: "nats errors"})}
	prometheus.MustRegister(m.EventConsumed, m.UpdateTotal, m.RedisWriteTotal, m.RedisWriteErrorTotal, m.StaleTotal, m.QueryTotal, m.WSConnections, m.WSPushTotal, m.NATSConsumeErrorTotal)
	return m
}
