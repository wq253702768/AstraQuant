package service

import (
	"context"
	"net/http"
	"strings"
	"time"

	domainadapter "github.com/astraquant/exchange-access-gateway/internal/domain/adapter"
	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/observability"
	"go.uber.org/zap"
)

type ExchangeAdapter = domainadapter.ExchangeAdapter

type ExchangeGatewayService struct {
	adapters map[string]ExchangeAdapter
	limiter  RateLimiter
	breaker  *CircuitBreaker
	auditor  *RequestAuditService
	metrics  *observability.Metrics
	logger   *zap.Logger
	metadata *MetadataStore
}

func NewExchangeGatewayService(adapters map[string]ExchangeAdapter, limiter RateLimiter, breaker *CircuitBreaker, auditor *RequestAuditService, metrics *observability.Metrics, logger *zap.Logger) *ExchangeGatewayService {
	return &ExchangeGatewayService{adapters: adapters, limiter: limiter, breaker: breaker, auditor: auditor, metrics: metrics, logger: logger, metadata: NewMetadataStore()}
}

func (s *ExchangeGatewayService) adapter(exchange string) (ExchangeAdapter, error) {
	adapter, ok := s.adapters[exchange]
	if !ok {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "exchange not supported", http.StatusNotFound)
	}
	return adapter, nil
}

func (s *ExchangeGatewayService) GetServerTime(ctx context.Context, exchange, traceID string) (int64, error) {
	var result int64
	err := s.call(ctx, exchange, "time", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetServerTime(ctx)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetInstruments(ctx context.Context, exchange string, req models.GetInstrumentsRequest, traceID string) ([]models.UnifiedInstrument, error) {
	var result []models.UnifiedInstrument
	err := s.call(ctx, exchange, "instruments", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetInstruments(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) SyncInstruments(ctx context.Context, exchange string, req models.GetInstrumentsRequest, traceID string) (*models.InstrumentSyncResult, error) {
	items, err := s.GetInstruments(ctx, exchange, req, traceID)
	if err != nil {
		return nil, err
	}
	count := s.metadata.Upsert(items)
	return &models.InstrumentSyncResult{Exchange: exchange, InstType: strings.ToUpper(req.ContractType), Status: "SUCCESS", SuccessCount: count, FailedCount: 0}, nil
}

func (s *ExchangeGatewayService) ListStoredInstruments(exchange string) []models.UnifiedInstrument {
	return s.metadata.List(exchange)
}

func (s *ExchangeGatewayService) GetStoredInstrument(exchange, symbol string) (models.UnifiedInstrument, bool) {
	return s.metadata.Get(exchange, symbol)
}

func (s *ExchangeGatewayService) ListSymbolMappings(exchange string) []models.SymbolMapping {
	return s.metadata.Mappings(exchange)
}

func (s *ExchangeGatewayService) GetKlines(ctx context.Context, exchange string, req models.GetKlinesRequest, traceID string) ([]models.UnifiedKline, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	if !supportedTimeframe(req.Timeframe) {
		return nil, domainerrors.New(domainerrors.TimeframeNotSupported, "timeframe not supported", http.StatusBadRequest)
	}
	if req.Limit > 300 {
		return nil, domainerrors.New(domainerrors.RateLimited, "limit exceeds maximum 300", http.StatusBadRequest)
	}
	var result []models.UnifiedKline
	err := s.call(ctx, exchange, "klines", "P5", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetKlines(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetTicker(ctx context.Context, exchange string, req models.GetTickerRequest, traceID string) (*models.UnifiedTicker, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	var result *models.UnifiedTicker
	err := s.call(ctx, exchange, "ticker", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetTicker(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetFundingRate(ctx context.Context, exchange string, req models.GetFundingRateRequest, traceID string) (*models.UnifiedFundingRate, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	var result *models.UnifiedFundingRate
	err := s.call(ctx, exchange, "funding-rate", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetFundingRate(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetFundingRateHistory(ctx context.Context, exchange string, req models.GetFundingRateHistoryRequest, traceID string) ([]models.UnifiedFundingRate, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	if req.Limit > 100 {
		return nil, domainerrors.New(domainerrors.RateLimited, "limit exceeds maximum 100", http.StatusBadRequest)
	}
	var result []models.UnifiedFundingRate
	err := s.call(ctx, exchange, "funding-rate-history", "P5", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetFundingRateHistory(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetMarkPrice(ctx context.Context, exchange string, req models.GetMarkPriceRequest, traceID string) (*models.UnifiedMarkPrice, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	var result *models.UnifiedMarkPrice
	err := s.call(ctx, exchange, "mark-price", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetMarkPrice(ctx, req)
		result = value
		return err
	})
	return result, err
}

func (s *ExchangeGatewayService) GetOpenInterest(ctx context.Context, exchange string, req models.GetOpenInterestRequest, traceID string) (*models.UnifiedOpenInterest, error) {
	if !IsSupportedSymbol(req.Symbol) {
		return nil, domainerrors.New(domainerrors.SymbolNotSupported, "symbol not supported", http.StatusBadRequest)
	}
	var result *models.UnifiedOpenInterest
	err := s.call(ctx, exchange, "open-interest", "P4", traceID, func(adapter ExchangeAdapter) error {
		value, err := adapter.GetOpenInterest(ctx, req)
		result = value
		return err
	})
	return result, err
}

func supportedTimeframe(timeframe string) bool {
	switch timeframe {
	case "1m", "5m", "15m", "1h", "4h":
		return true
	default:
		return false
	}
}

func (s *ExchangeGatewayService) call(ctx context.Context, exchange, endpoint, priority, traceID string, fn func(ExchangeAdapter) error) error {
	adapter, err := s.adapter(exchange)
	if err != nil {
		return err
	}
	breakerKey := exchange + ":" + endpoint
	if !s.breaker.Allow(breakerKey) {
		s.metrics.CircuitOpenTotal.Inc()
		return domainerrors.New(domainerrors.ExchangeUnavailable, "circuit breaker open", http.StatusServiceUnavailable)
	}
	key := RateLimitKey{Exchange: exchange, Endpoint: endpoint}
	allowed, err := s.limiter.Allow(ctx, key)
	if err != nil {
		return err
	}
	if !allowed {
		s.metrics.RateLimitedTotal.Inc()
		return domainerrors.New(domainerrors.RateLimited, "rate limited", http.StatusTooManyRequests)
	}
	start := time.Now()
	err = fn(adapter)
	latency := time.Since(start)
	internalCode := ""
	responseCode := "0"
	if err != nil {
		s.breaker.RecordFailure(breakerKey)
		responseCode = "ERROR"
		if exchangeErr, ok := err.(*domainerrors.ExchangeError); ok {
			internalCode = string(exchangeErr.Code)
		}
		s.metrics.RequestErrorTotal.WithLabelValues(exchange, endpoint, internalCode).Inc()
	} else {
		s.breaker.RecordSuccess(breakerKey)
	}
	s.metrics.RequestTotal.WithLabelValues(exchange, endpoint).Inc()
	s.metrics.RequestLatency.WithLabelValues(exchange, endpoint).Observe(float64(latency.Milliseconds()))
	s.auditor.Record(AuditRecord{Exchange: exchange, Endpoint: endpoint, Method: "GET", ResponseCode: responseCode, InternalErrorCode: internalCode, LatencyMS: latency.Milliseconds(), Priority: priority, TraceID: traceID, CreatedAt: time.Now()})
	return err
}
