package service

import (
	"strings"
	"sync"
	"time"

	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
)

var supportedSymbols = map[string]bool{
	"BTC-USDT-SWAP": true,
	"ETH-USDT-SWAP": true,
}

type MetadataStore struct {
	mu          sync.RWMutex
	instruments map[string]models.UnifiedInstrument
	syncedAt    map[string]int64
}

func NewMetadataStore() *MetadataStore {
	return &MetadataStore{instruments: map[string]models.UnifiedInstrument{}, syncedAt: map[string]int64{}}
}

func IsSupportedSymbol(symbol string) bool {
	return supportedSymbols[strings.ToUpper(symbol)]
}

func (s *MetadataStore) Upsert(instruments []models.UnifiedInstrument) int {
	s.mu.Lock()
	defer s.mu.Unlock()
	count := 0
	now := time.Now().UnixMilli()
	for _, item := range instruments {
		if !IsSupportedSymbol(item.InternalSymbol) {
			continue
		}
		s.instruments[item.Exchange+":"+item.InternalSymbol] = item
		s.syncedAt[item.Exchange+":"+item.InternalSymbol] = now
		count++
	}
	return count
}

func (s *MetadataStore) List(exchange string) []models.UnifiedInstrument {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := []models.UnifiedInstrument{}
	prefix := exchange + ":"
	for key, item := range s.instruments {
		if strings.HasPrefix(key, prefix) {
			items = append(items, item)
		}
	}
	return items
}

func (s *MetadataStore) Get(exchange, symbol string) (models.UnifiedInstrument, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	item, ok := s.instruments[exchange+":"+symbol]
	return item, ok
}

func (s *MetadataStore) Mappings(exchange string) []models.SymbolMapping {
	items := s.List(exchange)
	mappings := make([]models.SymbolMapping, 0, len(items))
	for _, item := range items {
		mappings = append(mappings, models.SymbolMapping{
			InternalSymbol: item.InternalSymbol,
			Exchange:       item.Exchange,
			ExchangeSymbol: item.ExchangeSymbol,
			InstrumentType: item.ContractType,
			BaseCurrency:   item.BaseAsset,
			QuoteCurrency:  item.QuoteAsset,
			SettleCurrency: item.MarginAsset,
			Enabled:        true,
		})
	}
	return mappings
}
