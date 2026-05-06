package observability

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct {
	SignalConsumed    prometheus.Counter
	CheckTotal        prometheus.Counter
	DecisionTotal     *prometheus.CounterVec
	RejectTotal       prometheus.Counter
	RuleTriggerTotal  *prometheus.CounterVec
	ContextBuildError prometheus.Counter
	NatsPublishError  prometheus.Counter
	DBWriteError      prometheus.Counter
}

func NewMetrics() *Metrics {
	m := &Metrics{SignalConsumed: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_signal_consumed_total", Help: "signals"}), CheckTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_check_total", Help: "checks"}), DecisionTotal: prometheus.NewCounterVec(prometheus.CounterOpts{Name: "risk_decision_total", Help: "decisions"}, []string{"decision"}), RejectTotal: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_reject_total", Help: "rejects"}), RuleTriggerTotal: prometheus.NewCounterVec(prometheus.CounterOpts{Name: "risk_rule_trigger_total", Help: "rule triggers"}, []string{"rule"}), ContextBuildError: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_context_build_error_total", Help: "context errors"}), NatsPublishError: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_nats_publish_error_total", Help: "nats errors"}), DBWriteError: prometheus.NewCounter(prometheus.CounterOpts{Name: "risk_db_write_error_total", Help: "db errors"})}
	prometheus.MustRegister(m.SignalConsumed, m.CheckTotal, m.DecisionTotal, m.RejectTotal, m.RuleTriggerTotal, m.ContextBuildError, m.NatsPublishError, m.DBWriteError)
	return m
}
