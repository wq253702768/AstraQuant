package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type StrategyDrawdownRule struct{ Cfg config.Config }

func (r StrategyDrawdownRule) Evaluate(input models.LiveRiskInput) RuleResult {
	cfg := r.Cfg
	if input.StrategyDrawdownPct <= -cfg.StrategyMaxDrawdownPct {
		return RuleResult{Triggered: true, RuleCode: "STRATEGY_DRAWDOWN_RULE", RuleName: "策略回撤规则", Level: "CRITICAL", Action: "BLOCK_TRADING", Reason: "策略回撤超限", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("STRATEGY_DRAWDOWN_RULE", "策略回撤规则")
}
