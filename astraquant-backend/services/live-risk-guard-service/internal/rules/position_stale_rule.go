package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type PositionStaleRule struct{ Cfg config.Config }

func (r PositionStaleRule) Evaluate(input models.LiveRiskInput) RuleResult {
	if input.PositionStaleSeconds >= 10 {
		return RuleResult{Triggered: true, RuleCode: "POSITION_STALE_RULE", RuleName: "持仓状态过期规则", Level: "WARNING", Action: "SET_REDUCE_ONLY", Reason: "持仓状态过期", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("POSITION_STALE_RULE", "持仓状态过期规则")
}
