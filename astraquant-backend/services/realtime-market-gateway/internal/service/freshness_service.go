package service

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

type FreshnessService struct{}

func (s FreshnessService) Calculate(eventTime, receiveTime int64) models.Freshness {
	latency := receiveTime - eventTime
	level := models.Stale
	if latency <= 100 {
		level = models.Fresh
	} else if latency <= 500 {
		level = models.Normal
	} else if latency <= 2000 {
		level = models.Slow
	}
	return models.Freshness{LatencyMs: latency, Level: level}
}
