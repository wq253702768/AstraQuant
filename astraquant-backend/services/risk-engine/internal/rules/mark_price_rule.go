package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type MarkPriceRule struct{}

func (r MarkPriceRule) Code() string { return "MARK_PRICE_RULE" }
func (r MarkPriceRule) Name() string { return "标记价格规则" }
func (r MarkPriceRule) Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult {
	if riskCtx.MarketSnapshot.MarkPrice != "" && riskCtx.MarketSnapshot.MarkPrice != "0" {
		return pass(r.Code(), r.Name())
	}
	return models.RuleResult{RuleCode: r.Code(), RuleName: r.Name(), Passed: false, Decision: "REJECT", Severity: "HARD_BLOCK", Message: "标记价格缺失或异常", CurrentValue: riskCtx.MarketSnapshot.MarkPrice, LimitValue: ">0"}
}
