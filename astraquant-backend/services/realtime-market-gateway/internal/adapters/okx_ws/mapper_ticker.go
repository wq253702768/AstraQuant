package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapTicker(data map[string]any) models.UnifiedMarketEvent {
	return base("TICKER", "tickers", data, map[string]any{"last_price": str(data, "last"), "open_24h": str(data, "open24h"), "high_24h": str(data, "high24h"), "low_24h": str(data, "low24h"), "volume_24h": str(data, "vol24h"), "quote_volume_24h": str(data, "volCcy24h")})
}
