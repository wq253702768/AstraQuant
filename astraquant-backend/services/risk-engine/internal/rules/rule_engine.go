package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type RuleEngine struct{ Rules []Rule }

func NewDefaultRuleEngine(cfg config.Config) *RuleEngine {
	return &RuleEngine{Rules: []Rule{MarketFreshnessRule{}, BboSpreadRule{}, FundingRateRule{}, MarkPriceRule{}, LeverageRule{}, SingleTradeRiskRule{}, PositionSizeRule{}, DailyLossRule{}, ConsecutiveLossRule{}, DrawdownRule{}, CooldownRule{}, OrderUnknownRule{}, ReduceOnlyRule{}}}
}
func (e *RuleEngine) Evaluate(ctx context.Context, riskCtx models.RiskContext) []models.RuleResult {
	out := make([]models.RuleResult, 0, len(e.Rules))
	for _, r := range e.Rules {
		out = append(out, r.Evaluate(ctx, riskCtx))
	}
	return out
}
