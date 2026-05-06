package service

import (
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/rules"
	"testing"
)

func TestEmergencyStop(t *testing.T) {
	s := NewEmergencyControlService(rules.NewCircuitBreakerEngine(config.Config{}), nil)
	c := s.Trigger("GLOBAL", "", "", "EMERGENCY_STOP", "test", "u")
	if !c.Enabled {
		t.Fatal("expected enabled")
	}
}
func TestEmergencyRelease(t *testing.T) {
	s := NewEmergencyControlService(rules.NewCircuitBreakerEngine(config.Config{}), nil)
	c := s.Trigger("GLOBAL", "", "", "EMERGENCY_STOP", "test", "u")
	r, ok := s.Release(c.ID, "u")
	if !ok || r.Enabled {
		t.Fatal("expected released")
	}
}
