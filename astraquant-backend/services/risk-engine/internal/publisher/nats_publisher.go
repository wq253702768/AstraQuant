package publisher

import (
	"encoding/json"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"github.com/nats-io/nats.go"
)

type NATSPublisher struct{ URL string }

func (p NATSPublisher) PublishDecision(d models.RiskDecision) error {
	nc, err := nats.Connect(p.URL)
	if err != nil {
		return err
	}
	defer nc.Close()
	b, _ := json.Marshal(map[string]any{"event_type": "risk.checked", "risk_decision_id": d.ID, "signal_id": d.SignalID, "decision": d.Decision, "approved": d.Approved, "reduce_only": d.ReduceOnly, "pause_strategy": d.PauseStrategy, "triggered_rules": d.TriggeredRules, "warnings": d.Warnings, "reject_reasons": d.RejectReasons, "created_at": d.CreatedAt})
	return nc.Publish("risk.checked", b)
}
