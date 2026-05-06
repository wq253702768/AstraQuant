package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type OrderFailureRateRule struct{ Cfg config.Config }

func (r OrderFailureRateRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.OrderFailureCount >= cfg.OrderFailureCountLimit {
		return RuleResult{Triggered: true, RuleCode: "ORDER_FAILURE_RATE_RULE", RuleName: "订单失败率规则", Level: "CRITICAL", Action: "BLOCK_TRADING", Reason: "订单失败次数超限", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ORDER_FAILURE_RATE_RULE", "订单失败率规则")
}
