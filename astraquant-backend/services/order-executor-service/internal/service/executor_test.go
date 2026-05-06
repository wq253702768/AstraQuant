package service

import (
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/domain/models"
	"strings"
	"testing"
)

func ctx() models.ExecutionContext {
	return models.ExecutionContext{SignalID: "sig", RiskDecisionID: "rd", AccountID: "acc", StrategyID: "st", StrategyVersionID: "sv", Exchange: "OKX", InternalSymbol: "BTC-USDT-SWAP", RiskDecision: models.RiskDecision{Decision: "APPROVE", Approved: true}, Signal: models.SignalSnapshot{Side: "buy", PositionSide: "long", Action: "OPEN", OrderType: "ioc", Price: "1", Quantity: "0.01", Leverage: "1"}, AccountState: models.AccountStateSnapshot{Fresh: true, TradingEnabled: false, HasTradePermission: true}, PositionState: models.PositionStateSnapshot{Fresh: true}, OrderState: models.OrderStateSnapshot{Fresh: true}, AdmissionResult: models.SimulationAdmissionResult{Decision: "ALLOW_SMALL_LIVE_APPLICATION", ApprovalStatus: "APPROVED"}}
}
func TestExecutionGateLiveDisabled(t *testing.T) {
	g := ExecutionGateService{Cfg: config.Config{ExecutionMode: "DRY_RUN"}, Approval: ApprovalCheckService{}, Kill: NewKillSwitchService()}
	if !g.Check(ctx()).Allowed || g.Check(ctx()).Mode != "DRY_RUN" {
		t.Fatal("dry run should pass")
	}
}
func TestExecutionGateApprovalMissing(t *testing.T) {
	c := ctx()
	c.AdmissionResult.ApprovalStatus = "PENDING"
	g := ExecutionGateService{Cfg: config.Config{LiveTradingEnabled: true, ExecutionMode: "LIVE_SMALL"}, Approval: ApprovalCheckService{}, Kill: NewKillSwitchService()}
	if g.Check(c).Allowed {
		t.Fatal("should reject missing approval")
	}
}
func TestExecutionGateKillSwitch(t *testing.T) {
	ks := NewKillSwitchService()
	ks.TriggerGlobal()
	g := ExecutionGateService{Cfg: config.Config{ExecutionMode: "DRY_RUN"}, Approval: ApprovalCheckService{}, Kill: ks}
	if g.Check(ctx()).Allowed {
		t.Fatal("kill switch should block")
	}
}
func TestExecutionGateAccountStale(t *testing.T) {
	c := ctx()
	c.AccountState.Fresh = false
	g := ExecutionGateService{Cfg: config.Config{ExecutionMode: "DRY_RUN"}, Approval: ApprovalCheckService{}, Kill: NewKillSwitchService()}
	if g.Check(c).Allowed {
		t.Fatal("stale account should block")
	}
}
func TestIdempotencyDuplicated(t *testing.T) {
	i := NewIdempotencyService()
	key := i.Key("s", "r")
	_, ok := i.CheckAndSet(key, "o1")
	if !ok {
		t.Fatal("first ok")
	}
	id, ok := i.CheckAndSet(key, "o2")
	if ok || id != "o1" {
		t.Fatal("duplicate failed")
	}
}
func TestClientOrderIDGenerate(t *testing.T) {
	id := ClientOrderIDService{Prefix: "AQ"}.Generate("buy")
	if !strings.HasPrefix(id, "AQ") || !strings.HasSuffix(id, "L") {
		t.Fatal("bad id")
	}
}
func TestOrderRequestBuildOpenLong(t *testing.T) {
	o := NewOrderExecutionService(config.Config{ClientOrderIDPrefix: "AQ", OKXOrderTag: "ASTRA", ExecutionMode: "DRY_RUN"}, nil, nil).DryRun(ctx())
	req := OrderRequestBuilder{Cfg: config.Config{OKXOrderTag: "ASTRA"}}.Build(o)
	if req.Side != "buy" || req.PosSide != "long" {
		t.Fatal("bad request")
	}
}
func TestReduceOnlyGuard(t *testing.T) {
	if (ReduceOnlyGuard{}).Valid("OPEN", true) {
		t.Fatal("open reduceOnly invalid")
	}
}
func TestOrderStateMachineFilled(t *testing.T) {
	if !(OrderStateMachine{}).Can("ACKNOWLEDGED", "FILLED") {
		t.Fatal("should allow filled")
	}
}
func TestOrderStateMachineUnknown(t *testing.T) {
	if !(OrderStateMachine{}).Can("SUBMITTED", "UNKNOWN") {
		t.Fatal("should allow unknown")
	}
}
func TestKillSwitchRelease(t *testing.T) {
	ks := NewKillSwitchService()
	ks.TriggerGlobal()
	ks.ReleaseGlobal()
	if ks.Enabled(ctx()) {
		t.Fatal("should release")
	}
}
