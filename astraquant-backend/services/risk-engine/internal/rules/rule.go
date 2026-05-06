package rules

import (
	"context"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

type Rule interface {
	Code() string
	Name() string
	Evaluate(ctx context.Context, riskCtx models.RiskContext) models.RuleResult
}

func pass(code, name string) models.RuleResult {
	return models.RuleResult{RuleCode: code, RuleName: name, Passed: true, Decision: "APPROVE", Severity: "SOFT_WARNING", Message: "passed"}
}
