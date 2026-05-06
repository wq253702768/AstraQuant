package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapTrade(data map[string]any) models.UnifiedMarketEvent {
	return base("TRADE", "trades", data, map[string]any{"trade_id": str(data, "tradeId"), "price": str(data, "px"), "size": str(data, "sz"), "side": str(data, "side")})
}
