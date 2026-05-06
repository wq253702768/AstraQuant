package rules

import (
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type RuleResult struct {
	Triggered      bool
	RuleCode       string
	RuleName       string
	Level          string
	Action         string
	Reason         string
	CurrentValue   string
	ThresholdValue string
}
type Rule interface {
	Evaluate(input models.LiveRiskInput) RuleResult
}

func pass(code, name string) RuleResult {
	return RuleResult{Triggered: false, RuleCode: code, RuleName: name}
}
