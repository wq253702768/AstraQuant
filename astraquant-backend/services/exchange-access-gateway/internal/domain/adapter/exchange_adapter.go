package adapter

import (
	"context"

	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
)

type ExchangeAdapter interface {
	GetExchangeName() string
	GetInstruments(ctx context.Context, req models.GetInstrumentsRequest) ([]models.UnifiedInstrument, error)
	GetTicker(ctx context.Context, req models.GetTickerRequest) (*models.UnifiedTicker, error)
	GetKlines(ctx context.Context, req models.GetKlinesRequest) ([]models.UnifiedKline, error)
	GetFundingRate(ctx context.Context, req models.GetFundingRateRequest) (*models.UnifiedFundingRate, error)
	GetFundingRateHistory(ctx context.Context, req models.GetFundingRateHistoryRequest) ([]models.UnifiedFundingRate, error)
	GetMarkPrice(ctx context.Context, req models.GetMarkPriceRequest) (*models.UnifiedMarkPrice, error)
	GetOpenInterest(ctx context.Context, req models.GetOpenInterestRequest) (*models.UnifiedOpenInterest, error)
	GetServerTime(ctx context.Context) (int64, error)
	PlaceOrder(ctx context.Context, req models.PlaceOrderRequest) (*models.UnifiedOrder, error)
	CancelOrder(ctx context.Context, req models.CancelOrderRequest) (*models.UnifiedOrder, error)
	AmendOrder(ctx context.Context, req models.AmendOrderRequest) (*models.UnifiedOrder, error)
}
