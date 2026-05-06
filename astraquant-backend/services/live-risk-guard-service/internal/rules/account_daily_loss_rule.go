package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type AccountDailyLossRule struct{ Cfg config.Config }

func (r AccountDailyLossRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.AccountDailyLossPct <= -cfg.AccountDailyLossLimitPct {
		return RuleResult{Triggered: true, RuleCode: "ACCOUNT_DAILY_LOSS_RULE", RuleName: "账户日亏损规则", Level: "CRITICAL", Action: "TRIGGER_KILL_SWITCH", Reason: "账户日内亏损超限", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ACCOUNT_DAILY_LOSS_RULE", "账户日亏损规则")
}
