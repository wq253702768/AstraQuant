package service

import (
	"github.com/astraquant/realtime-state-service/internal/config"
	"github.com/astraquant/realtime-state-service/internal/domain/models"
	"github.com/astraquant/realtime-state-service/internal/state"
	"testing"
	"time"
)

func cfg() config.Config {
	return config.Config{TickerStaleMs: 5000, BBOStaleMs: 3000, TradeStaleMs: 10000, MarkPriceStaleMs: 5000, FundingStaleMs: 60000}
}
func updater() *StateUpdateService {
	st := state.NewMemoryStateStore()
	return NewStateUpdateService(st, NewFreshnessService(cfg()), nil)
}
func event(t string, ts int64) models.UnifiedMarketEvent {
	return models.UnifiedMarketEvent{EventType: t, Exchange: "OKX", InternalSymbol: "BTC-USDT-SWAP", ExchangeSymbol: "BTC-USDT-SWAP", EventTime: ts, ReceiveTime: time.Now().UnixMilli(), LatencyMs: 1, Payload: map[string]any{"last_price": "1", "bid_price": "1", "ask_price": "2", "trade_id": "t1", "price": "1", "size": "1", "side": "buy", "timeframe": "1m", "open": "1", "high": "2", "low": "1", "close": "2", "mark_price": "1", "index_price": "1", "funding_rate": "0.1"}}
}
func TestUpdateMarketState(t *testing.T) {
	u := updater()
	u.Apply(event("TICKER", 1000))
	v, ok := u.store.GetMarket("OKX", "BTC-USDT-SWAP")
	if !ok || v.LastPrice != "1" {
		t.Fatal("market not updated")
	}
}
func TestUpdateBBOState(t *testing.T) {
	u := updater()
	u.Apply(event("BBO", 1000))
	v, ok := u.store.GetBBO("OKX", "BTC-USDT-SWAP")
	if !ok || v.BidPrice != "1" {
		t.Fatal("bbo not updated")
	}
}
func TestUpdateTradeState(t *testing.T) {
	u := updater()
	u.Apply(event("TRADE", 1000))
	v, ok := u.store.GetTrade("OKX", "BTC-USDT-SWAP")
	if !ok || v.TradeID != "t1" {
		t.Fatal("trade not updated")
	}
}
func TestUpdateKlineState(t *testing.T) {
	u := updater()
	u.Apply(event("KLINE", 1000))
	_, ok := u.store.GetKline("OKX", "BTC-USDT-SWAP", "1m")
	if !ok {
		t.Fatal("kline not updated")
	}
}
func TestUpdateMarkPriceState(t *testing.T) {
	u := updater()
	u.Apply(event("MARK_PRICE", 1000))
	_, ok := u.store.GetMarkPrice("OKX", "BTC-USDT-SWAP")
	if !ok {
		t.Fatal("mark not updated")
	}
}
func TestUpdateFundingState(t *testing.T) {
	u := updater()
	u.Apply(event("FUNDING", 1000))
	_, ok := u.store.GetFunding("OKX", "BTC-USDT-SWAP")
	if !ok {
		t.Fatal("funding not updated")
	}
}
func TestIgnoreOldEvent(t *testing.T) {
	u := updater()
	u.Apply(event("TICKER", 2000))
	u.Apply(event("TICKER", 1000))
	v, _ := u.store.GetMarket("OKX", "BTC-USDT-SWAP")
	if v.EventTime != 2000 {
		t.Fatal("old event overwrote state")
	}
}
