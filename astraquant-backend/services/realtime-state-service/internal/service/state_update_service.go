package service

import (
	"fmt"
	"github.com/astraquant/realtime-state-service/internal/domain/enums"
	"github.com/astraquant/realtime-state-service/internal/domain/models"
	"github.com/astraquant/realtime-state-service/internal/observability"
	"github.com/astraquant/realtime-state-service/internal/state"
	"strconv"
	"time"
)

type StateUpdateService struct {
	store     *state.MemoryStateStore
	freshness FreshnessService
	metrics   *observability.Metrics
}

func NewStateUpdateService(store *state.MemoryStateStore, freshness FreshnessService, metrics *observability.Metrics) *StateUpdateService {
	return &StateUpdateService{store: store, freshness: freshness, metrics: metrics}
}
func base(e models.UnifiedMarketEvent, fs FreshnessService, kind string) models.BaseState {
	update := time.Now().UnixMilli()
	status, fresh, reason := fs.Status(update, fs.Threshold(kind))
	return models.BaseState{Exchange: e.Exchange, InternalSymbol: e.InternalSymbol, ExchangeSymbol: e.ExchangeSymbol, EventTime: e.EventTime, ReceiveTime: e.ReceiveTime, UpdateTime: update, LatencyMs: e.LatencyMs, FreshnessStatus: status, Fresh: fresh, StaleReason: reason}
}
func str(p map[string]any, k string) string {
	if v, ok := p[k]; ok {
		return fmt.Sprint(v)
	}
	return ""
}
func boolv(p map[string]any, k string) bool { v := fmt.Sprint(p[k]); return v == "true" || v == "1" }
func i64(p map[string]any, k string) int64 {
	v, _ := strconv.ParseInt(fmt.Sprint(p[k]), 10, 64)
	return v
}
func (s *StateUpdateService) Apply(e models.UnifiedMarketEvent) {
	switch e.EventType {
	case enums.EventTicker:
		s.store.SetMarket(models.MarketState{BaseState: base(e, s.freshness, enums.StateTicker), LastPrice: str(e.Payload, "last_price"), Open24h: str(e.Payload, "open_24h"), High24h: str(e.Payload, "high_24h"), Low24h: str(e.Payload, "low_24h"), Volume24h: str(e.Payload, "volume_24h"), QuoteVolume24h: str(e.Payload, "quote_volume_24h")})
	case enums.EventBBO:
		s.store.SetBBO(models.BBOState{BaseState: base(e, s.freshness, enums.StateBBO), BidPrice: str(e.Payload, "bid_price"), BidSize: str(e.Payload, "bid_size"), AskPrice: str(e.Payload, "ask_price"), AskSize: str(e.Payload, "ask_size")})
	case enums.EventTrade:
		s.store.SetTrade(models.TradeState{BaseState: base(e, s.freshness, enums.StateTrade), TradeID: str(e.Payload, "trade_id"), Price: str(e.Payload, "price"), Size: str(e.Payload, "size"), Side: str(e.Payload, "side")})
	case enums.EventKline:
		s.store.SetKline(models.KlineState{BaseState: base(e, s.freshness, enums.StateKline), Timeframe: str(e.Payload, "timeframe"), Open: str(e.Payload, "open"), High: str(e.Payload, "high"), Low: str(e.Payload, "low"), Close: str(e.Payload, "close"), Volume: str(e.Payload, "volume"), QuoteVolume: str(e.Payload, "quote_volume"), Confirmed: boolv(e.Payload, "confirmed")})
	case enums.EventMarkPrice:
		s.store.SetMarkPrice(models.MarkPriceState{BaseState: base(e, s.freshness, enums.StateMarkPrice), MarkPrice: str(e.Payload, "mark_price"), IndexPrice: str(e.Payload, "index_price")})
	case enums.EventFunding:
		s.store.SetFunding(models.FundingState{BaseState: base(e, s.freshness, enums.StateFunding), FundingRate: str(e.Payload, "funding_rate"), NextFundingTime: i64(e.Payload, "next_funding_time"), MarkPrice: str(e.Payload, "mark_price")})
	}
	if s.metrics != nil && s.metrics.UpdateTotal != nil {
		s.metrics.UpdateTotal.WithLabelValues(e.EventType).Inc()
	}
}
