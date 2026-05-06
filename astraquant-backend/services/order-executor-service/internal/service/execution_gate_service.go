package service

import (
	"fmt"
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/domain/models"
)

type GateResult struct {
	Allowed bool
	Reason  string
	Mode    string
}
type ExecutionGateService struct {
	Cfg      config.Config
	Approval ApprovalCheckService
	Kill     *KillSwitchService
}

func (s ExecutionGateService) Check(ctx models.ExecutionContext) GateResult {
	if s.Kill != nil && s.Kill.Enabled(ctx) {
		return GateResult{false, "kill switch enabled", "LIVE_BLOCKED"}
	}
	if ctx.RiskDecision.Decision != "APPROVE" && ctx.RiskDecision.Decision != "REDUCE_ONLY" {
		return GateResult{false, "risk decision not approved", "LIVE_BLOCKED"}
	}
	if ctx.RiskDecision.ReduceOnly && ctx.Signal.Action == "OPEN" {
		return GateResult{false, "reduceOnly violation", "LIVE_BLOCKED"}
	}
	if !ctx.AccountState.Fresh {
		return GateResult{false, "account state stale", "LIVE_BLOCKED"}
	}
	if !ctx.PositionState.Fresh {
		return GateResult{false, "position state stale", "LIVE_BLOCKED"}
	}
	if !ctx.OrderState.Fresh {
		return GateResult{false, "order state stale", "LIVE_BLOCKED"}
	}
	if !ctx.AccountState.HasTradePermission && s.Cfg.ExecutionMode == "LIVE_SMALL" {
		return GateResult{false, "api key trade permission missing", "LIVE_BLOCKED"}
	}
	if ctx.AccountState.HasWithdrawPermission {
		return GateResult{false, "api key has withdraw permission", "LIVE_BLOCKED"}
	}
	if !s.Cfg.LiveTradingEnabled || s.Cfg.ExecutionMode == "DRY_RUN" {
		return GateResult{true, "dry run allowed", "DRY_RUN"}
	}
	if !s.Approval.Approved(ctx) {
		return GateResult{false, "simulation admission approval is missing", "LIVE_BLOCKED"}
	}
	if ctx.Signal.Leverage != "" && ctx.Signal.Leverage > fmt.Sprintf("%g", s.Cfg.SmallMaxLeverage) {
		return GateResult{false, "small live leverage exceeded", "LIVE_BLOCKED"}
	}
	return GateResult{true, "live small allowed", "LIVE_SMALL"}
}
