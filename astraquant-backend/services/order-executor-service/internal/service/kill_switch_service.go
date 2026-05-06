package service

import "github.com/astraquant/order-executor-service/internal/domain/models"

type KillSwitchService struct {
	Global     bool
	Accounts   map[string]bool
	Strategies map[string]bool
}

func NewKillSwitchService() *KillSwitchService {
	return &KillSwitchService{Accounts: map[string]bool{}, Strategies: map[string]bool{}}
}
func (s *KillSwitchService) Enabled(ctx models.ExecutionContext) bool {
	return s.Global || s.Accounts[ctx.AccountID] || s.Strategies[ctx.StrategyVersionID] || ctx.KillSwitchState.Enabled
}
func (s *KillSwitchService) TriggerGlobal() { s.Global = true }
func (s *KillSwitchService) ReleaseGlobal() { s.Global = false }
