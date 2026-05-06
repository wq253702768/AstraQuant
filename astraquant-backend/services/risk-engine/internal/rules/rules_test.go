package rules

import (
	"context"
	"testing"

	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/domain/enums"
	"github.com/astraquant/risk-engine/internal/domain/models"
)

func ctx() models.RiskContext {
	return models.RiskContext{
		Signal:         models.SignalInput{Action: "OPEN", SignalType: "OPEN_LONG", Leverage: 3, SuggestedPositionPct: 0.05},
		StrategyRisk:   models.StrategyRiskConfig{MaxSpreadPct: 0.001, MaxAbsFundingRate: 0.0005, MaxLeverage: 3, MaxPositionPct: 0.2, MaxSingleTradeLossPct: 0.005, MaxDailyLossPct: 0.02, MaxConsecutiveLosses: 3, MaxStrategyDrawdownPct: 0.06, StopLossPct: 0.01},
		MarketSnapshot: models.MarketSnapshot{Fresh: true, FreshnessStatus: "FRESH", SpreadPct: 0.0001, FundingRate: 0.0001, MarkPrice: "1"},
	}
}

func TestMarketFreshnessRulePass(t *testing.T) {
	if !(MarketFreshnessRule{}).Evaluate(context.Background(), ctx()).Passed {
		t.Fatal("expected pass")
	}
}
func TestMarketFreshnessRuleReject(t *testing.T) {
	c := ctx()
	c.MarketSnapshot.Fresh = false
	c.MarketSnapshot.FreshnessStatus = "STALE"
	if (MarketFreshnessRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestBBOSpreadRuleReject(t *testing.T) {
	c := ctx()
	c.MarketSnapshot.SpreadPct = 0.002
	if (BboSpreadRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestFundingRateRuleReject(t *testing.T) {
	c := ctx()
	c.MarketSnapshot.FundingRate = 0.01
	if (FundingRateRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestMarkPriceRuleRejectMissing(t *testing.T) {
	c := ctx()
	c.MarketSnapshot.MarkPrice = ""
	if (MarkPriceRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestLeverageRuleReject(t *testing.T) {
	c := ctx()
	c.Signal.Leverage = 5
	if (LeverageRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestSingleTradeRiskRuleReject(t *testing.T) {
	c := ctx()
	c.Signal.SuggestedPositionPct = 0.5
	if (SingleTradeRiskRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestPositionSizeRuleReject(t *testing.T) {
	c := ctx()
	c.Signal.SuggestedPositionPct = 0.3
	if (PositionSizeRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestCooldownRuleReject(t *testing.T) {
	c := ctx()
	c.RuntimeCounters.CooldownActive = true
	if (CooldownRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReject {
		t.Fatal("expected reject")
	}
}
func TestDecisionPriorityPause(t *testing.T) {
	c := ctx()
	c.RuntimeCounters.ConsecutiveLosses = 5
	results := NewDefaultRuleEngine(config.Config{DefaultMaxConsecutiveLosses: 3}).Evaluate(context.Background(), c)
	decision := enums.DecisionApprove
	for _, result := range results {
		if result.Decision == enums.DecisionPauseStrategy {
			decision = enums.DecisionPauseStrategy
		}
	}
	if decision != enums.DecisionPauseStrategy {
		t.Fatal("expected pause")
	}
}
func TestReduceOnlyForClose(t *testing.T) {
	c := ctx()
	c.Signal.Action = "CLOSE"
	c.MarketSnapshot.Fresh = false
	if (MarketFreshnessRule{}).Evaluate(context.Background(), c).Decision != enums.DecisionReduceOnly {
		t.Fatal("expected reduce only")
	}
}
