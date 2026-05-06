package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct {
	RequestTotal      *prometheus.CounterVec
	RequestLatency    *prometheus.HistogramVec
	RequestErrorTotal *prometheus.CounterVec
	RateLimitedTotal  prometheus.Counter
	CircuitOpenTotal  prometheus.Counter
}

func NewMetrics() *Metrics {
	m := &Metrics{
		RequestTotal:      prometheus.NewCounterVec(prometheus.CounterOpts{Name: "exchange_request_total", Help: "Total exchange requests"}, []string{"exchange", "endpoint"}),
		RequestLatency:    prometheus.NewHistogramVec(prometheus.HistogramOpts{Name: "exchange_request_latency_ms", Help: "Exchange request latency in milliseconds", Buckets: []float64{10, 50, 100, 300, 500, 1000, 3000, 5000}}, []string{"exchange", "endpoint"}),
		RequestErrorTotal: prometheus.NewCounterVec(prometheus.CounterOpts{Name: "exchange_request_error_total", Help: "Total exchange request errors"}, []string{"exchange", "endpoint", "code"}),
		RateLimitedTotal:  prometheus.NewCounter(prometheus.CounterOpts{Name: "exchange_rate_limited_total", Help: "Total rate limited requests"}),
		CircuitOpenTotal:  prometheus.NewCounter(prometheus.CounterOpts{Name: "exchange_circuit_open_total", Help: "Total circuit open rejections"}),
	}
	prometheus.MustRegister(m.RequestTotal, m.RequestLatency, m.RequestErrorTotal, m.RateLimitedTotal, m.CircuitOpenTotal)
	return m
}
