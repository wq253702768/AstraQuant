package service

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

type MarketEventNormalizer struct{}

func (n MarketEventNormalizer) Normalize(event models.UnifiedMarketEvent) models.UnifiedMarketEvent {
	return event
}
