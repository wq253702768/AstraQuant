package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type DrawdownRule struct{}

func (r DrawdownRule) Code() string { return "DRAWDOWN_RULE" }
func (r DrawdownRule) Name() string { return "回撤规则" }
func (r DrawdownRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.RuntimeCounters.CurrentDrawdownPct <= riskCtx.StrategyRisk.MaxStrategyDrawdownPct {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "策略回撤超过阈值", CurrentValue: fmt.Sprintf("%g", riskCtx.RuntimeCounters.CurrentDrawdownPct), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxStrategyDrawdownPct)}
}
