package rules

import (
	"context"
	"fmt"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"math"
)

type FundingRateRule struct{}

func (r FundingRateRule) Code() string { return "FUNDING_RATE_RULE" }
func (r FundingRateRule) Name() string { return "资金费率规则" }
func (r FundingRateRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if math.Abs(riskCtx.MarketSnapshot.FundingRate) <= riskCtx.StrategyRisk.MaxAbsFundingRate {
		return pass(r.Code(), r.Name())
	}
	if riskCtx.Signal.IsCloseOrReduce() {
		return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REDUCE_ONLY", Severity: "ACTION_LIMIT", Message: "资金费率极端，只允许减仓或平仓", CurrentValue: fmt.Sprintf("%g", riskCtx.MarketSnapshot.FundingRate), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxAbsFundingRate)}
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "资金费率超过阈值", CurrentValue: fmt.Sprintf("%g", riskCtx.MarketSnapshot.FundingRate), LimitValue: fmt.Sprintf("%g", riskCtx.StrategyRisk.MaxAbsFundingRate)}
}
