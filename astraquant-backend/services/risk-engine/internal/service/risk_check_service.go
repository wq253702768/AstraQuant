package service

import (
	"context"
	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"github.com/astraquant/risk-engine/internal/observability"
	"github.com/astraquant/risk-engine/internal/rules"
	"go.uber.org/zap"
)

type RiskCheckService struct {
	engine  *rules.RuleEngine
	builder RiskContextBuilder
	metrics *observability.Metrics
	logger  *zap.Logger
}

func NewRiskCheckService(engine *rules.RuleEngine, cfg config.Config, metrics *observability.Metrics, logger *zap.Logger) *RiskCheckService {
	return &RiskCheckService{engine: engine, builder: NewRiskContextBuilder(cfg), metrics: metrics, logger: logger}
}
func (s *RiskCheckService) Check(ctx context.Context, signal models.SignalInput) models.RiskDecision {
	riskCtx := s.builder.Build(signal)
	results := s.engine.Evaluate(ctx, riskCtx)
	decision := RiskDecisionBuilder{}.Build(riskCtx, results)
	if s.metrics != nil {
		s.metrics.CheckTotal.Inc()
		s.metrics.DecisionTotal.WithLabelValues(decision.Decision).Inc()
	}
	return decision
}
