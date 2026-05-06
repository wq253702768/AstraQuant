package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type CooldownRule struct{}

func (r CooldownRule) Code() string { return "COOLDOWN_RULE" }
func (r CooldownRule) Name() string { return "冷却规则" }
func (r CooldownRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if !riskCtx.RuntimeCounters.CooldownActive {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "开仓冷却期内禁止重复开仓", CurrentValue: "active", LimitValue: "inactive"}
}
