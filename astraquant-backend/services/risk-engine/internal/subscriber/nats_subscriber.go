package subscriber

import (
	"context"
	"encoding/json"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"github.com/astraquant/risk-engine/internal/service"
	"github.com/nats-io/nats.go"
)

type NATSSubscriber struct {
	URL     string
	Checker *service.RiskCheckService
}

func (s NATSSubscriber) Start() error {
	nc, err := nats.Connect(s.URL)
	if err != nil {
		return err
	}
	_, err = nc.Subscribe("signal.generated", func(msg *nats.Msg) {
		var signal models.SignalInput
		if json.Unmarshal(msg.Data, &signal) == nil {
			s.Checker.Check(context.Background(), signal)
		}
	})
	return err
}
