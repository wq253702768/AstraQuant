package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type AccountDrawdownRule struct{ Cfg config.Config }

func (r AccountDrawdownRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.AccountDrawdownPct <= -cfg.AccountMaxDrawdownPct {
		return RuleResult{Triggered: true, RuleCode: "ACCOUNT_DRAWDOWN_RULE", RuleName: "账户回撤规则", Level: "CRITICAL", Action: "TRIGGER_KILL_SWITCH", Reason: "账户回撤超限", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ACCOUNT_DRAWDOWN_RULE", "账户回撤规则")
}
