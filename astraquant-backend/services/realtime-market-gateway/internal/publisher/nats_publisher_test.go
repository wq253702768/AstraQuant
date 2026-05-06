package publisher

import (
	"github.com/astraquant/realtime-market-gateway/internal/observability"
	"go.uber.org/zap"
	"testing"
)

func TestNatsTopicRouter(t *testing.T) {
	p := NewNATSPublisher("nats://localhost:4222", observability.NewMetrics(), zap.NewNop())
	if p.Topic("TICKER") != "market.ticker" {
		t.Fatal("bad topic")
	}
	if p.Topic("BBO") != "market.bbo" {
		t.Fatal("bad bbo")
	}
}
