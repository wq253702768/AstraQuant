package service

import (
	"github.com/astraquant/realtime-state-service/internal/config"
	"github.com/astraquant/realtime-state-service/internal/domain/enums"
	"time"
)

type FreshnessService struct{ cfg config.Config }

func NewFreshnessService(cfg config.Config) FreshnessService { return FreshnessService{cfg: cfg} }
func (s FreshnessService) Status(updateTime int64, staleMs int64) (string, bool, string) {
	if updateTime == 0 {
		return enums.Missing, false, "missing"
	}
	age := time.Now().UnixMilli() - updateTime
	if age <= 1000 {
		return enums.Fresh, true, ""
	}
	if age <= 3000 {
		return enums.Normal, true, ""
	}
	if age <= staleMs {
		return enums.Slow, true, ""
	}
	return enums.Stale, false, "stale"
}
func (s FreshnessService) Threshold(kind string) int64 {
	switch kind {
	case enums.StateBBO:
		return s.cfg.BBOStaleMs
	case enums.StateTrade:
		return s.cfg.TradeStaleMs
	case enums.StateMarkPrice:
		return s.cfg.MarkPriceStaleMs
	case enums.StateFunding:
		return s.cfg.FundingStaleMs
	default:
		return s.cfg.TickerStaleMs
	}
}
