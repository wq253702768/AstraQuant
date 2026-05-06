package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type StrategyDailyLossRule struct{ Cfg config.Config }

func (r StrategyDailyLossRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.StrategyDailyLossPct <= -cfg.StrategyDailyLossLimitPct {
		return RuleResult{Triggered: true, RuleCode: "STRATEGY_DAILY_LOSS_RULE", RuleName: "策略日亏损规则", Level: "CRITICAL", Action: "BLOCK_TRADING", Reason: "策略日内亏损超限", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("STRATEGY_DAILY_LOSS_RULE", "策略日亏损规则")
}
