package service

import (
	"github.com/astraquant/realtime-state-service/internal/config"
	"github.com/astraquant/realtime-state-service/internal/state"
	"testing"
)

func TestBuildSnapshot(t *testing.T) {
	st := state.NewMemoryStateStore()
	f := NewFreshnessService(config.Config{TickerStaleMs: 5000, BBOStaleMs: 3000, MarkPriceStaleMs: 5000, FundingStaleMs: 60000})
	u := NewStateUpdateService(st, f, nil)
	u.Apply(event("TICKER", 1000))
	u.Apply(event("BBO", 1001))
	u.Apply(event("MARK_PRICE", 1002))
	u.Apply(event("FUNDING", 1003))
	snap := NewStateQueryService(st, f).Snapshot("OKX", "BTC-USDT-SWAP")
	if !snap.Fresh {
		t.Fatal("snapshot should be fresh")
	}
}
