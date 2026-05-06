package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type LeverageRule struct{}

func (r LeverageRule) Code() string { return "LEVERAGE_RULE" }
func (r LeverageRule) Name() string { return "杠杆规则" }
func (r LeverageRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.Signal.Leverage <= riskCtx.StrategyRisk.MaxLeverage {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "信号杠杆超过策略最大杠杆", CurrentValue: fmt.Sprintf("%g", riskCtx.Signal.Leverage), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxLeverage)}
}
