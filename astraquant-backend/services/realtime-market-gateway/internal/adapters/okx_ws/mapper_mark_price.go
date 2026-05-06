package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapMarkPrice(data map[string]any) models.UnifiedMarketEvent {
	return base("MARK_PRICE", "mark-price", data, map[string]any{"mark_price": str(data, "markPx"), "index_price": str(data, "idxPx")})
}
