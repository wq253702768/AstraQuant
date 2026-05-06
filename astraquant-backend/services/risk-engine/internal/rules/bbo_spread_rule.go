package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type BboSpreadRule struct{}

func (r BboSpreadRule) Code() string { return "BBO_SPREAD_RULE" }
func (r BboSpreadRule) Name() string { return "盘口价差规则" }
func (r BboSpreadRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.MarketSnapshot.SpreadPct <= riskCtx.StrategyRisk.MaxSpreadPct {
		return pass(r.Code(), r.Name())
	}
	if riskCtx.Signal.IsCloseOrReduce() {
		return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REDUCE_ONLY", Severity: "ACTION_LIMIT", Message: "盘口价差过大，只允许减仓或平仓", CurrentValue: fmt.Sprintf("%g", riskCtx.MarketSnapshot.SpreadPct), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxSpreadPct)}
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "盘口价差超过阈值", CurrentValue: fmt.Sprintf("%g", riskCtx.MarketSnapshot.SpreadPct), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxSpreadPct)}
}
