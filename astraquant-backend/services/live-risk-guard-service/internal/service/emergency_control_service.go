package service

import (
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
	"github.com/astraquant/live-risk-guard-service/internal/observability"
	"github.com/astraquant/live-risk-guard-service/internal/rules"
	"github.com/google/uuid"
	"time"
)

type EmergencyControlService struct {
	Engine   *rules.CircuitBreakerEngine
	Metrics  *observability.Metrics
	Controls []models.EmergencyControl
	Events   []models.CircuitBreakerEvent
	State    LiveRiskStateService
}

func NewEmergencyControlService(engine *rules.CircuitBreakerEngine, metrics *observability.Metrics) *EmergencyControlService {
	return &EmergencyControlService{Engine: engine, Metrics: metrics}
}
func (s *EmergencyControlService) Evaluate(input models.LiveRiskInput) []models.CircuitBreakerEvent {
	results := s.Engine.Evaluate(input)
	events := []models.CircuitBreakerEvent{}
	for _, r := range results {
		state := s.State.Apply("STRATEGY", r)
		e := models.CircuitBreakerEvent{ID: uuid.NewString(), Scope: state.Scope, Level: r.Level, RuleCode: r.RuleCode, RuleName: r.RuleName, CurrentValue: r.CurrentValue, ThresholdValue: r.ThresholdValue, Action: r.Action, Reason: r.Reason, AutoCancelRequested: r.Action == "BLOCK_TRADING" || r.Action == "TRIGGER_KILL_SWITCH", KillSwitchTriggered: r.Action == "TRIGGER_KILL_SWITCH", Status: "ACTIVE", TriggeredAt: time.Now().UnixMilli()}
		s.Events = append(s.Events, e)
		events = append(events, e)
	}
	return events
}
func (s *EmergencyControlService) Trigger(scope, accountID, strategyVersionID, action, reason, user string) models.EmergencyControl {
	c := models.EmergencyControl{ID: uuid.NewString(), Scope: scope, AccountID: accountID, StrategyVersionID: strategyVersionID, Action: action, Enabled: true, Reason: reason, TriggeredBy: user, TriggeredAt: time.Now().UnixMilli()}
	s.Controls = append(s.Controls, c)
	return c
}
func (s *EmergencyControlService) Release(id, user string) (models.EmergencyControl, bool) {
	for i, c := range s.Controls {
		if c.ID == id {
			c.Enabled = false
			c.ReleasedBy = user
			c.ReleasedAt = time.Now().UnixMilli()
			s.Controls[i] = c
			return c, true
		}
	}
	return models.EmergencyControl{}, false
}
func (s *EmergencyControlService) ListStates() []models.LiveRiskState       { return s.State.List() }
func (s *EmergencyControlService) ListEvents() []models.CircuitBreakerEvent { return s.Events }
func (s *EmergencyControlService) GetEvent(id string) (models.CircuitBreakerEvent, bool) {
	for _, e := range s.Events {
		if e.ID == id {
			return e, true
		}
	}
	return models.CircuitBreakerEvent{}, false
}
