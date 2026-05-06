package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type PositionSizeRule struct{}

func (r PositionSizeRule) Code() string { return "POSITION_SIZE_RULE" }
func (r PositionSizeRule) Name() string { return "仓位比例规则" }
func (r PositionSizeRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.Signal.SuggestedPositionPct <= riskCtx.StrategyRisk.MaxPositionPct {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "建议仓位超过上限", CurrentValue: fmt.Sprintf("%g", riskCtx.Signal.SuggestedPositionPct), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxPositionPct)}
}
