package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type StrategyConsecutiveLossRule struct{ Cfg config.Config }

func (r StrategyConsecutiveLossRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.ConsecutiveLosses >= cfg.MaxConsecutiveLosses {
		return RuleResult{Triggered: true, RuleCode: "STRATEGY_CONSECUTIVE_LOSS_RULE", RuleName: "连续亏损规则", Level: "WARNING", Action: "SET_REDUCE_ONLY", Reason: "连续亏损达到阈值", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("STRATEGY_CONSECUTIVE_LOSS_RULE", "连续亏损规则")
}
