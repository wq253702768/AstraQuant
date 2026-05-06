package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
	"math"
)

type FundingRateExtremeRule struct{ Cfg config.Config }

func (r FundingRateExtremeRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if math.Abs(input.FundingRate) > cfg.MaxAbsFundingRate {
		return RuleResult{Triggered: true, RuleCode: "FUNDING_RATE_EXTREME_RULE", RuleName: "资金费率异常规则", Level: "WARNING", Action: "SET_REDUCE_ONLY", Reason: "资金费率极端", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("FUNDING_RATE_EXTREME_RULE", "资金费率异常规则")
}
