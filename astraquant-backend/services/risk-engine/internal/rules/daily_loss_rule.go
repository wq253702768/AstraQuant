package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type DailyLossRule struct{}

func (r DailyLossRule) Code() string { return "DAILY_LOSS_RULE" }
func (r DailyLossRule) Name() string { return "日内亏损规则" }
func (r DailyLossRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.RuntimeCounters.DailyLossPct <= riskCtx.StrategyRisk.MaxDailyLossPct {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "日内亏损超过阈值", CurrentValue: fmt.Sprintf("%g", riskCtx.RuntimeCounters.DailyLossPct), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxDailyLossPct)}
}
