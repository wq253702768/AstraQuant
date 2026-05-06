package service

import (
	"github.com/astraquant/risk-engine/internal/domain/enums"
	"github.com/astraquant/risk-engine/internal/domain/models"
	"github.com/google/uuid"
	"time"
)

type RiskDecisionBuilder struct{}

func (b RiskDecisionBuilder) Build(ctx models.RiskContext, results []models.RuleResult) models.RiskDecision {
	decision := enums.DecisionApprove
	triggered := []models.TriggeredRule{}
	rejects := []string{}
	warnings := []string{}
	for _, r := range results {
		if r.Passed {
			continue
		}
		tr := models.TriggeredRule{RuleCode: r.RuleCode, RuleName: r.RuleName, Severity: r.Severity, Result: "FAILED", Message: r.Message, CurrentValue: r.CurrentValue, LimitValue: r.LimitValue}
		triggered = append(triggered, tr)
		if r.Decision == enums.DecisionPauseStrategy {
			decision = enums.DecisionPauseStrategy
		}
		if decision != enums.DecisionPauseStrategy && r.Decision == enums.DecisionReject {
			decision = enums.DecisionReject
		}
		if decision != enums.DecisionPauseStrategy && decision != enums.DecisionReject && r.Decision == enums.DecisionManualReview {
			decision = enums.DecisionManualReview
		}
		if decision == enums.DecisionApprove && r.Decision == enums.DecisionReduceOnly {
			decision = enums.DecisionReduceOnly
		}
		if r.Decision == enums.DecisionReject || r.Decision == enums.DecisionPauseStrategy {
			rejects = append(rejects, r.Message)
		} else {
			warnings = append(warnings, r.Message)
		}
	}
	return models.RiskDecision{ID: uuid.NewString(), SignalID: ctx.Signal.SignalID, StrategyID: ctx.Signal.StrategyID, StrategyVersionID: ctx.Signal.StrategyVersionID, Exchange: ctx.Signal.Exchange, InternalSymbol: ctx.Signal.InternalSymbol, Decision: decision, Approved: decision == enums.DecisionApprove || decision == enums.DecisionReduceOnly, ReduceOnly: decision == enums.DecisionReduceOnly, PauseStrategy: decision == enums.DecisionPauseStrategy, TriggeredRules: triggered, RejectReasons: rejects, Warnings: warnings, RiskSnapshot: map[string]any{"rule_version": ctx.RuleVersion}, MarketSnapshot: ctx.Signal.MarketSnapshot, AccountSnapshot: map[string]any{}, PositionSnapshot: map[string]any{}, RuleVersion: ctx.RuleVersion, TraceID: ctx.Signal.TraceID, CreatedAt: time.Now().UnixMilli()}
}
