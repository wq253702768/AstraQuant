package service

import (
	"github.com/astraquant/realtime-market-gateway/internal/domain/enums"
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"sync"
)

type SubscriptionManager struct {
	mu    sync.RWMutex
	items map[string]models.Subscription
}

func NewSubscriptionManager() *SubscriptionManager {
	return &SubscriptionManager{items: map[string]models.Subscription{}}
}
func (m *SubscriptionManager) Add(s models.Subscription) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if s.Exchange == "" {
		s.Exchange = enums.ExchangeOKX
	}
	if s.ExchangeSymbol == "" {
		s.ExchangeSymbol = s.InternalSymbol
	}
	s.Enabled = true
	m.items[s.Key()] = s
}
func (m *SubscriptionManager) Remove(s models.Subscription) {
	m.mu.Lock()
	defer m.mu.Unlock()
	delete(m.items, s.Key())
}
func (m *SubscriptionManager) List() []models.Subscription {
	m.mu.RLock()
	defer m.mu.RUnlock()
	out := make([]models.Subscription, 0, len(m.items))
	for _, v := range m.items {
		out = append(out, v)
	}
	return out
}
func (m *SubscriptionManager) LoadDefaults(symbols []string, timeframes []string) {
	for _, sym := range symbols {
		for _, ch := range []string{enums.ChannelTickers, enums.ChannelBBO, enums.ChannelTrades, enums.ChannelMarkPrice} {
			m.Add(models.Subscription{Exchange: enums.ExchangeOKX, Channel: ch, InternalSymbol: sym, ExchangeSymbol: sym, Enabled: true})
		}
		for _, tf := range timeframes {
			ch := enums.ChannelCandle1m
			if tf == "5m" {
				ch = enums.ChannelCandle5m
			}
			m.Add(models.Subscription{Exchange: enums.ExchangeOKX, Channel: ch, InternalSymbol: sym, ExchangeSymbol: sym, Timeframe: tf, Enabled: true})
		}
	}
}
