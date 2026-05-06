package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct {
	WSConnectionStatus    prometheus.Gauge
	WSReconnectTotal      prometheus.Counter
	WSMessageTotal        prometheus.Counter
	WSMessageErrorTotal   prometheus.Counter
	EventPublishedTotal   *prometheus.CounterVec
	EventLatency          *prometheus.HistogramVec
	SubscriptionTotal     prometheus.Gauge
	NatsPublishErrorTotal prometheus.Counter
	LastMessageTimestamp  prometheus.Gauge
}

func NewMetrics() *Metrics {
	m := &Metrics{WSConnectionStatus: prometheus.NewGauge(prometheus.GaugeOpts{Name: "realtime_ws_connection_status", Help: "WS connection status"}), WSReconnectTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_ws_reconnect_total", Help: "WS reconnect total"}), WSMessageTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_ws_message_total", Help: "WS message total"}), WSMessageErrorTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_ws_message_error_total", Help: "WS parse errors"}), EventPublishedTotal: prometheus.NewCounterVec(prometheus.CounterOpts{Name: "realtime_market_event_published_total", Help: "Published events"}, []string{"event_type"}), EventLatency: prometheus.NewHistogramVec(prometheus.HistogramOpts{Name: "realtime_market_event_latency_ms", Help: "Market event latency"}, []string{"event_type"}), SubscriptionTotal: prometheus.NewGauge(prometheus.GaugeOpts{Name: "realtime_subscription_total", Help: "Subscriptions"}), NatsPublishErrorTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "realtime_nats_publish_error_total", Help: "NATS publish errors"}), LastMessageTimestamp: prometheus.NewGauge(prometheus.GaugeOpts{Name: "realtime_last_message_timestamp", Help: "Last message timestamp"})}
	prometheus.MustRegister(m.WSConnectionStatus, m.WSReconnectTotal, m.WSMessageTotal, m.WSMessageErrorTotal, m.EventPublishedTotal, m.EventLatency, m.SubscriptionTotal, m.NatsPublishErrorTotal, m.LastMessageTimestamp)
	return m
}
