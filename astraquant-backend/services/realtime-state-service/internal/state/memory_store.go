package state

import (
	"github.com/astraquant/realtime-state-service/internal/domain/models"
	"sync"
)

type MemoryStateStore struct {
	market  sync.Map
	bbo     sync.Map
	trade   sync.Map
	kline   sync.Map
	mark    sync.Map
	funding sync.Map
}

func NewMemoryStateStore() *MemoryStateStore { return &MemoryStateStore{} }
func Key(exchange, symbol string) string     { return exchange + ":" + symbol }
func KlineKey(exchange, symbol, timeframe string) string {
	return exchange + ":" + symbol + ":" + timeframe
}
func newer(oldTime, newTime int64) bool { return newTime >= oldTime }
func (s *MemoryStateStore) SetMarket(v models.MarketState) {
	k := Key(v.Exchange, v.InternalSymbol)
	if old, ok := s.market.Load(k); ok && !newer(old.(models.MarketState).EventTime, v.EventTime) {
		return
	}
	s.market.Store(k, v)
}
func (s *MemoryStateStore) GetMarket(exchange, symbol string) (models.MarketState, bool) {
	v, ok := s.market.Load(Key(exchange, symbol))
	if !ok {
		return models.MarketState{}, false
	}
	return v.(models.MarketState), true
}
func (s *MemoryStateStore) SetBBO(v models.BBOState) {
	k := Key(v.Exchange, v.InternalSymbol)
	if old, ok := s.bbo.Load(k); ok && !newer(old.(models.BBOState).EventTime, v.EventTime) {
		return
	}
	s.bbo.Store(k, v)
}
func (s *MemoryStateStore) GetBBO(exchange, symbol string) (models.BBOState, bool) {
	v, ok := s.bbo.Load(Key(exchange, symbol))
	if !ok {
		return models.BBOState{}, false
	}
	return v.(models.BBOState), true
}
func (s *MemoryStateStore) SetTrade(v models.TradeState) {
	k := Key(v.Exchange, v.InternalSymbol)
	if old, ok := s.trade.Load(k); ok && !newer(old.(models.TradeState).EventTime, v.EventTime) {
		return
	}
	s.trade.Store(k, v)
}
func (s *MemoryStateStore) GetTrade(exchange, symbol string) (models.TradeState, bool) {
	v, ok := s.trade.Load(Key(exchange, symbol))
	if !ok {
		return models.TradeState{}, false
	}
	return v.(models.TradeState), true
}
func (s *MemoryStateStore) SetKline(v models.KlineState) {
	k := KlineKey(v.Exchange, v.InternalSymbol, v.Timeframe)
	if old, ok := s.kline.Load(k); ok && !newer(old.(models.KlineState).EventTime, v.EventTime) {
		return
	}
	s.kline.Store(k, v)
}
func (s *MemoryStateStore) GetKline(exchange, symbol, timeframe string) (models.KlineState, bool) {
	v, ok := s.kline.Load(KlineKey(exchange, symbol, timeframe))
	if !ok {
		return models.KlineState{}, false
	}
	return v.(models.KlineState), true
}
func (s *MemoryStateStore) Klines(exchange, symbol string) []models.KlineState {
	out := []models.KlineState{}
	prefix := Key(exchange, symbol) + ":"
	s.kline.Range(func(k, v any) bool {
		if len(k.(string)) >= len(prefix) && k.(string)[:len(prefix)] == prefix {
			out = append(out, v.(models.KlineState))
		}
		return true
	})
	return out
}
func (s *MemoryStateStore) SetMarkPrice(v models.MarkPriceState) {
	k := Key(v.Exchange, v.InternalSymbol)
	if old, ok := s.mark.Load(k); ok && !newer(old.(models.MarkPriceState).EventTime, v.EventTime) {
		return
	}
	s.mark.Store(k, v)
}
func (s *MemoryStateStore) GetMarkPrice(exchange, symbol string) (models.MarkPriceState, bool) {
	v, ok := s.mark.Load(Key(exchange, symbol))
	if !ok {
		return models.MarkPriceState{}, false
	}
	return v.(models.MarkPriceState), true
}
func (s *MemoryStateStore) SetFunding(v models.FundingState) {
	k := Key(v.Exchange, v.InternalSymbol)
	if old, ok := s.funding.Load(k); ok && !newer(old.(models.FundingState).EventTime, v.EventTime) {
		return
	}
	s.funding.Store(k, v)
}
func (s *MemoryStateStore) GetFunding(exchange, symbol string) (models.FundingState, bool) {
	v, ok := s.funding.Load(Key(exchange, symbol))
	if !ok {
		return models.FundingState{}, false
	}
	return v.(models.FundingState), true
}
