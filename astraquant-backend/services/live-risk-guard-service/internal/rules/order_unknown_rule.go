package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type OrderUnknownRule struct{ Cfg config.Config }

func (r OrderUnknownRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.UnknownOrderCount >= cfg.MaxOrderUnknownCountStrategy {
		return RuleResult{Triggered: true, RuleCode: "ORDER_UNKNOWN_RULE", RuleName: "订单未知熔断规则", Level: "CRITICAL", Action: "BLOCK_TRADING", Reason: "订单状态未知，禁止继续开仓", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ORDER_UNKNOWN_RULE", "订单未知熔断规则")
}
