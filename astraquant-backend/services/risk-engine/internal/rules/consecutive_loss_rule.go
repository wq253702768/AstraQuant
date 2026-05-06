package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type ConsecutiveLossRule struct{}

func (r ConsecutiveLossRule) Code() string { return "CONSECUTIVE_LOSS_RULE" }
func (r ConsecutiveLossRule) Name() string { return "连续亏损规则" }
func (r ConsecutiveLossRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.RuntimeCounters.ConsecutiveLosses <= riskCtx.StrategyRisk.MaxConsecutiveLosses {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "PAUSE_STRATEGY", Severity: "HARD_BLOCK", Message: "连续亏损超过阈值，暂停策略", CurrentValue: fmt.Sprintf("%d", riskCtx.RuntimeCounters.ConsecutiveLosses), LimitValue: fmt.Sprintf("%d", riskCtx.StrategyRisk.MaxConsecutiveLosses)}
}
