package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct{ DryRunTotal prometheus.Counter }

func NewMetrics() *Metrics {
	m := &Metrics{DryRunTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "order_executor_dry_run_total", Help: "dry runs"})}
	prometheus.MustRegister(m.DryRunTotal)
	return m
}
