package service

import (
	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type RiskContextBuilder struct{ cfg config.Config }

func NewRiskContextBuilder(cfg config.Config) RiskContextBuilder { return RiskContextBuilder{cfg: cfg} }
func (b RiskContextBuilder) Build(signal models.SignalInput) models.RiskContext {
	ms := models.MarketSnapshot{Fresh: true, FreshnessStatus: "FRESH", SpreadPct: 0.0001, FundingRate: 0.0001, MarkPrice: "1"}
	if v, ok := signal.FreshnessSnapshot["fresh"].(bool); ok {
		ms.Fresh = v
	}
	if v, ok := signal.FreshnessSnapshot["freshness_status"].(string); ok {
		ms.FreshnessStatus = v
	}
	if v, ok := signal.MarketSnapshot["spread_pct"].(float64); ok {
		ms.SpreadPct = v
	}
	if v, ok := signal.MarketSnapshot["funding_rate"].(float64); ok {
		ms.FundingRate = v
	}
	if v, ok := signal.MarketSnapshot["mark_price"].(string); ok {
		ms.MarkPrice = v
	}
	return models.RiskContext{Signal: signal, StrategyRisk: models.StrategyRiskConfig{MaxSpreadPct: b.cfg.MaxSpreadPct, MaxAbsFundingRate: b.cfg.MaxAbsFundingRate, MaxLeverage: b.cfg.DefaultMaxLeverage, MaxPositionPct: b.cfg.DefaultMaxPositionPct, MaxSingleTradeLossPct: b.cfg.DefaultMaxSingleTradeLossPct, MaxDailyLossPct: b.cfg.DefaultMaxDailyLossPct, MaxConsecutiveLosses: b.cfg.DefaultMaxConsecutiveLosses, MaxStrategyDrawdownPct: b.cfg.DefaultMaxStrategyDrawdownPct, StopLossPct: 0.01, OpenCooldownSeconds: b.cfg.DefaultOpenCooldownSeconds}, MarketSnapshot: ms, AccountSnapshot: models.AccountSnapshot{}, PositionSnapshot: models.PositionSnapshot{}, RuntimeCounters: models.RuntimeCounters{}, RuleVersion: b.cfg.RuleVersion}
}
