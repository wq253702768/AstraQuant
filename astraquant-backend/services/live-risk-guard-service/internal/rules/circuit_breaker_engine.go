package rules

import (
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type CircuitBreakerEngine struct{ Rules []Rule }

func NewCircuitBreakerEngine(cfg config.Config) *CircuitBreakerEngine {
	return &CircuitBreakerEngine{Rules: []Rule{AccountDailyLossRule{cfg}, StrategyDailyLossRule{cfg}, StrategyConsecutiveLossRule{cfg}, AccountDrawdownRule{cfg}, StrategyDrawdownRule{cfg}, OrderUnknownRule{cfg}, OrderFailureRateRule{cfg}, AccountStaleRule{cfg}, PositionStaleRule{cfg}, GatewayDisconnectRule{cfg}, AbnormalSlippageRule{cfg}, AbnormalFeeRule{cfg}, FundingRateExtremeRule{cfg}}}
}
func (e *CircuitBreakerEngine) Evaluate(input models.LiveRiskInput) []RuleResult {
	out := []RuleResult{}
	for _, r := range e.Rules {
		res := r.Evaluate(input)
		if res.Triggered {
			out = append(out, res)
		}
	}
	return out
}
func (e *CircuitBreakerEngine) Highest(results []RuleResult) string {
	priority := map[string]int{"TRIGGER_KILL_SWITCH": 5, "BLOCK_TRADING": 4, "SET_REDUCE_ONLY": 3, "MANUAL_REVIEW_REQUIRED": 2, "WARNING_ONLY": 1}
	best := "NORMAL"
	score := 0
	for _, r := range results {
		if priority[r.Action] > score {
			score = priority[r.Action]
			best = r.Action
		}
	}
	return best
}
