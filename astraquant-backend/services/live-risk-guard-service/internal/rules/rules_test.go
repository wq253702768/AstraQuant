package rules

import (
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
	"testing"
)

func cfg() config.Config {
	return config.Config{AccountDailyLossLimitPct: 0.02, StrategyDailyLossLimitPct: 0.01, AccountMaxDrawdownPct: 0.05, StrategyMaxDrawdownPct: 0.03, MaxConsecutiveLosses: 3, MaxOrderUnknownCountStrategy: 1, OrderFailureCountLimit: 3, MaxSlippagePct: 0.003, MaxAbsFundingRate: 0.0008}
}
func TestAccountDailyLossRule(t *testing.T) {
	if !(AccountDailyLossRule{cfg()}).Evaluate(models.LiveRiskInput{AccountDailyLossPct: -0.03}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestStrategyDailyLossRule(t *testing.T) {
	if !(StrategyDailyLossRule{cfg()}).Evaluate(models.LiveRiskInput{StrategyDailyLossPct: -0.02}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestConsecutiveLossRule(t *testing.T) {
	if !(StrategyConsecutiveLossRule{cfg()}).Evaluate(models.LiveRiskInput{ConsecutiveLosses: 3}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestAccountDrawdownRule(t *testing.T) {
	if !(AccountDrawdownRule{cfg()}).Evaluate(models.LiveRiskInput{AccountDrawdownPct: -0.06}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestStrategyDrawdownRule(t *testing.T) {
	if !(StrategyDrawdownRule{cfg()}).Evaluate(models.LiveRiskInput{StrategyDrawdownPct: -0.04}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestOrderUnknownRule(t *testing.T) {
	if !(OrderUnknownRule{cfg()}).Evaluate(models.LiveRiskInput{UnknownOrderCount: 1}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestOrderFailureRateRule(t *testing.T) {
	if !(OrderFailureRateRule{cfg()}).Evaluate(models.LiveRiskInput{OrderFailureCount: 3}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestAccountStaleRule(t *testing.T) {
	if !(AccountStaleRule{cfg()}).Evaluate(models.LiveRiskInput{AccountStaleSeconds: 10}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestPositionStaleRule(t *testing.T) {
	if !(PositionStaleRule{cfg()}).Evaluate(models.LiveRiskInput{PositionStaleSeconds: 10}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestGatewayDisconnectRule(t *testing.T) {
	if !(GatewayDisconnectRule{cfg()}).Evaluate(models.LiveRiskInput{GatewayDisconnectedSeconds: 15}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestAbnormalSlippageRule(t *testing.T) {
	if !(AbnormalSlippageRule{cfg()}).Evaluate(models.LiveRiskInput{SlippagePct: 0.01}).Triggered {
		t.Fatal("expected trigger")
	}
}
func TestCircuitBreakerPriority(t *testing.T) {
	e := NewCircuitBreakerEngine(cfg())
	if e.Highest(e.Evaluate(models.LiveRiskInput{AccountDailyLossPct: -0.03, ConsecutiveLosses: 3})) != "TRIGGER_KILL_SWITCH" {
		t.Fatal("expected kill switch")
	}
}
func TestReduceOnlyAction(t *testing.T) {
	res := (StrategyConsecutiveLossRule{cfg()}).Evaluate(models.LiveRiskInput{ConsecutiveLosses: 3})
	if res.Action != "SET_REDUCE_ONLY" {
		t.Fatal("expected reduce only")
	}
}
