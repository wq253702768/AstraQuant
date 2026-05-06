package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type MarketFreshnessRule struct{}

func (r MarketFreshnessRule) Code() string { return "MARKET_FRESHNESS_RULE" }
func (r MarketFreshnessRule) Name() string { return "行情新鲜度规则" }
func (r MarketFreshnessRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.MarketSnapshot.Fresh {
		return pass(r.Code(), r.Name())
	}
	if riskCtx.Signal.IsCloseOrReduce() {
		return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REDUCE_ONLY", Severity: "ACTION_LIMIT", Message: "行情数据过期，只允许减仓或平仓", CurrentValue: riskCtx.MarketSnapshot.FreshnessStatus, LimitValue: "FRESH"}
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "行情数据已过期，禁止新开仓", CurrentValue: riskCtx.MarketSnapshot.FreshnessStatus, LimitValue: "FRESH"}
}
