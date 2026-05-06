package subscriber

import (
	"encoding/json"
	"github.com/astraquant/realtime-state-service/internal/domain/models"
	"github.com/astraquant/realtime-state-service/internal/service"
	"github.com/nats-io/nats.go"
	"go.uber.org/zap"
)

type NATSSubscriber struct {
	URL     string
	Updater *service.StateUpdateService
	Logger  *zap.Logger
}

func (s *NATSSubscriber) Start() error {
	nc, err := nats.Connect(s.URL)
	if err != nil {
		return err
	}
	topics := []string{"market.ticker", "market.bbo", "market.trade", "market.kline", "market.mark_price", "market.funding"}
	for _, topic := range topics {
		_, err = nc.Subscribe(topic, func(msg *nats.Msg) {
			var event models.UnifiedMarketEvent
			if err := json.Unmarshal(msg.Data, &event); err != nil {
				if s.Logger != nil {
					s.Logger.Error("parse market event failed", zap.Error(err))
				}
				return
			}
			s.Updater.Apply(event)
		})
		if err != nil {
			return err
		}
	}
	return nil
}
