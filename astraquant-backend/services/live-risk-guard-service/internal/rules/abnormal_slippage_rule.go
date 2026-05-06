package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type AbnormalSlippageRule struct{ Cfg config.Config }

func (r AbnormalSlippageRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.SlippagePct > cfg.MaxSlippagePct {
		return RuleResult{Triggered: true, RuleCode: "ABNORMAL_SLIPPAGE_RULE", RuleName: "异常滑点规则", Level: "WARNING", Action: "WARNING_ONLY", Reason: "滑点异常", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("ABNORMAL_SLIPPAGE_RULE", "异常滑点规则")
}
