package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type ReduceOnlyRule struct{}

func (r ReduceOnlyRule) Code() string { return "REDUCE_ONLY_RULE" }
func (r ReduceOnlyRule) Name() string { return "ReduceOnly规则" }
func (r ReduceOnlyRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	return pass(r.Code(), r.Name())
}
