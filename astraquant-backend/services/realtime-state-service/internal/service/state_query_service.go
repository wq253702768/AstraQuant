package service

import (
	"github.com/astraquant/realtime-state-service/internal/domain/enums"
	"github.com/astraquant/realtime-state-service/internal/domain/models"
	"github.com/astraquant/realtime-state-service/internal/state"
	"time"
)

type StateQueryService struct {
	store     *state.MemoryStateStore
	freshness FreshnessService
}

func NewStateQueryService(store *state.MemoryStateStore, freshness FreshnessService) *StateQueryService {
	return &StateQueryService{store: store, freshness: freshness}
}
func (s *StateQueryService) Market(e, sym string) (models.MarketState, bool) {
	return s.store.GetMarket(e, sym)
}
func (s *StateQueryService) BBO(e, sym string) (models.BBOState, bool) { return s.store.GetBBO(e, sym) }
func (s *StateQueryService) Trade(e, sym string) (models.TradeState, bool) {
	return s.store.GetTrade(e, sym)
}
func (s *StateQueryService) Kline(e, sym, tf string) (models.KlineState, bool) {
	return s.store.GetKline(e, sym, tf)
}
func (s *StateQueryService) MarkPrice(e, sym string) (models.MarkPriceState, bool) {
	return s.store.GetMarkPrice(e, sym)
}
func (s *StateQueryService) Funding(e, sym string) (models.FundingState, bool) {
	return s.store.GetFunding(e, sym)
}
func (s *StateQueryService) Snapshot(e, sym string) models.StateSnapshot {
	m, mok := s.Market(e, sym)
	b, bok := s.BBO(e, sym)
	mp, mpok := s.MarkPrice(e, sym)
	f, fok := s.Funding(e, sym)
	t, _ := s.Trade(e, sym)
	kl := s.store.Klines(e, sym)
	fresh := mok && bok && mpok && fok && m.Fresh && b.Fresh && mp.Fresh && f.Fresh
	status := enums.Fresh
	reasons := []string{}
	if !mok || !bok || !mpok || !fok {
		status = enums.Missing
		fresh = false
		reasons = append(reasons, "missing critical state")
	} else if !fresh {
		status = enums.Stale
		reasons = append(reasons, "stale critical state")
	}
	return models.StateSnapshot{Exchange: e, InternalSymbol: sym, Market: ptr(m, mok), BBO: ptr(b, bok), LastTrade: ptr(t, true), Klines: kl, MarkPrice: ptr(mp, mpok), Funding: ptr(f, fok), Fresh: fresh, FreshnessStatus: status, StaleReasons: reasons, SnapshotTime: time.Now().UnixMilli()}
}
func ptr[T any](v T, ok bool) *T {
	if !ok {
		return nil
	}
	return &v
}
func (s *StateQueryService) Freshness(e, sym string) map[string]any {
	snap := s.Snapshot(e, sym)
	return map[string]any{"exchange": e, "internal_symbol": sym, "fresh": snap.Fresh, "freshness_status": snap.FreshnessStatus, "stale_reasons": snap.StaleReasons}
}
