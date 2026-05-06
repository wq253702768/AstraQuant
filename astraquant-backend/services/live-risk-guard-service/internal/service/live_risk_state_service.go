package service

import (
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
	"github.com/astraquant/live-risk-guard-service/internal/rules"
	"github.com/google/uuid"
	"time"
)

type LiveRiskStateService struct{ States []models.LiveRiskState }

func (s *LiveRiskStateService) Apply(scope string, result rules.RuleResult) models.LiveRiskState {
	state := models.LiveRiskState{ID: uuid.NewString(), Scope: scope, RiskState: "NORMAL", UpdatedAt: time.Now().UnixMilli(), LastTriggeredRule: result.RuleCode, LastReason: result.Reason}
	switch result.Action {
	case "TRIGGER_KILL_SWITCH":
		state.RiskState = "EMERGENCY_STOPPED"
		state.EmergencyStopped = true
		state.TradingBlocked = true
	case "BLOCK_TRADING":
		state.RiskState = "TRADING_BLOCKED"
		state.TradingBlocked = true
	case "SET_REDUCE_ONLY":
		state.RiskState = "REDUCE_ONLY"
		state.ReduceOnly = true
	case "WARNING_ONLY":
		state.RiskState = "WARNING"
	}
	s.States = append(s.States, state)
	return state
}
func (s *LiveRiskStateService) List() []models.LiveRiskState { return s.States }
