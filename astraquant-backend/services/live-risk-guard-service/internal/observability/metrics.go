package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct{ BreakerTriggered prometheus.Counter }

func NewMetrics() *Metrics {
	m := &Metrics{BreakerTriggered: prometheus.NewCounter(prometheus.CounterOpts{Name: "live_risk_breaker_triggered_total", Help: "breakers"})}
	prometheus.MustRegister(m.BreakerTriggered)
	return m
}
