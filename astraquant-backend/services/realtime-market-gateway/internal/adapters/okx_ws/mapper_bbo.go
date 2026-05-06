package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapBBO(data map[string]any) models.UnifiedMarketEvent {
	return base("BBO", "bbo-tbt", data, map[string]any{"bid_price": str(data, "bidPx"), "bid_size": str(data, "bidSz"), "ask_price": str(data, "askPx"), "ask_size": str(data, "askSz")})
}
