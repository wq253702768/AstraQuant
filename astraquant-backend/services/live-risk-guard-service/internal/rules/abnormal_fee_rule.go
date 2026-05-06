package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type AbnormalFeeRule struct{ Cfg config.Config }

func (r AbnormalFeeRule) Evaluate(input models.LiveRiskInput) RuleResult {
	if input.FeeMultiplier > 1.5 {
		return RuleResult{Triggered: true, RuleCode: "ABNORMAL_FEE_RULE", RuleName: "异常手续费规则", Level: "WARNING", Action: "WARNING_ONLY", Reason: "手续费异常", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ABNORMAL_FEE_RULE", "异常手续费规则")
}
