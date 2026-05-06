package service

import (
	"github.com/astraquant/risk-engine/internal/domain/enums"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"testing"
)

func TestDecisionPriorityPause(t *testing.T) {
	ctx := models.RiskContext{Signal: models.SignalInput{SignalID: "s1"}}
	results := []models.RuleResult{{Passed: false, Decision: enums.DecisionReject, Message: "reject"}, {Passed: false, Decision: enums.DecisionPauseStrategy, Message: "pause"}}
	decision := RiskDecisionBuilder{}.Build(ctx, results)
	if decision.Decision != enums.DecisionPauseStrategy {
		t.Fatalf("expected pause, got %s", decision.Decision)
	}
}

func TestDecisionPriorityReject(t *testing.T) {
	ctx := models.RiskContext{Signal: models.SignalInput{SignalID: "s1"}}
	results := []models.RuleResult{{Passed: false, Decision: enums.DecisionReduceOnly, Message: "reduce"}, {Passed: false, Decision: enums.DecisionReject, Message: "reject"}}
	decision := RiskDecisionBuilder{}.Build(ctx, results)
	if decision.Decision != enums.DecisionReject {
		t.Fatalf("expected reject, got %s", decision.Decision)
	}
}
