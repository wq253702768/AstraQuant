package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type AccountStaleRule struct{ Cfg config.Config }

func (r AccountStaleRule) Evaluate(input models.LiveRiskInput) RuleResult {
	if input.AccountStaleSeconds >= 10 {
		return RuleResult{Triggered: true, RuleCode: "ACCOUNT_STALE_RULE", RuleName: "账户状态过期规则", Level: "WARNING", Action: "SET_REDUCE_ONLY", Reason: "账户状态过期", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ACCOUNT_STALE_RULE", "账户状态过期规则")
}
