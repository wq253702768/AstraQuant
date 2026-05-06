package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapFunding(data map[string]any) models.UnifiedMarketEvent {
	return base("FUNDING", "funding-rate", data, map[string]any{"funding_rate": str(data, "fundingRate"), "next_funding_time": i64(data, "nextFundingTime"), "mark_price": str(data, "markPx")})
}
