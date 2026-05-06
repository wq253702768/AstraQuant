package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type SingleTradeRiskRule struct{}

func (r SingleTradeRiskRule) Code() string { return "SINGLE_TRADE_RISK_RULE" }
func (r SingleTradeRiskRule) Name() string { return "单笔风险规则" }
func (r SingleTradeRiskRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	estimated := riskCtx.Signal.SuggestedPositionPct * riskCtx.StrategyRisk.StopLossPct * riskCtx.Signal.Leverage
	if estimated <= riskCtx.StrategyRisk.MaxSingleTradeLossPct {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "单笔风险超过阈值", CurrentValue: fmt.Sprintf("%g", estimated), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxSingleTradeLossPct)}
}
