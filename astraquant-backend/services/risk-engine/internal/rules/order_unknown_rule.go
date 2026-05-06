package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type OrderUnknownRule struct{}

func (r OrderUnknownRule) Code() string { return "ORDER_UNKNOWN_RULE" }
func (r OrderUnknownRule) Name() string { return "订单未知规则" }
func (r OrderUnknownRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if !riskCtx.RuntimeCounters.OrderUnknown {
		return pass(r.Code(), r.Name())
	}
	if riskCtx.Signal.IsCloseOrReduce() {
		return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REDUCE_ONLY", Severity: "ACTION_LIMIT", Message: "订单状态未知，只允许减仓或平仓", CurrentValue: "unknown", LimitValue: "known"}
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "订单状态未知，禁止新开仓", CurrentValue: "unknown", LimitValue: "known"}
}
