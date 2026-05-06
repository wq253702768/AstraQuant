package publisher

import (
	"encoding/json"
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"github.com/astraquant/realtime-market-gateway/internal/observability"
	"github.com/nats-io/nats.go"
	"go.uber.org/zap"
)

type NATSPublisher struct {
	url     string
	metrics *observability.Metrics
	logger  *zap.Logger
}

func NewNATSPublisher(url string, metrics *observability.Metrics, logger *zap.Logger) *NATSPublisher {
	return &NATSPublisher{url: url, metrics: metrics, logger: logger}
}
func (p *NATSPublisher) Topic(eventType string) string {
	switch eventType {
	case "TICKER":
		return "market.ticker"
	case "BBO":
		return "market.bbo"
	case "TRADE":
		return "market.trade"
	case "KLINE":
		return "market.kline"
	case "MARK_PRICE":
		return "market.mark_price"
	case "FUNDING":
		return "market.funding"
	default:
		return "market.gateway.error"
	}
}
func (p *NATSPublisher) Publish(event models.UnifiedMarketEvent) error {
	nc, err := nats.Connect(p.url)
	if err != nil {
		p.metrics.NatsPublishErrorTotal.Inc()
		return err
	}
	defer nc.Close()
	data, _ := json.Marshal(event)
	if err := nc.Publish(p.Topic(event.EventType), data); err != nil {
		p.metrics.NatsPublishErrorTotal.Inc()
		return err
	}
	p.metrics.EventPublishedTotal.WithLabelValues(event.EventType).Inc()
	return nil
}
