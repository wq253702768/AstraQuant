package okx

import (
	"context"
	"strconv"
	"time"

	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"go.uber.org/zap"
)

type AdapterConfig struct {
	BaseURL    string
	Timeout    time.Duration
	EnableDemo bool
}

type Adapter struct {
	client *RestClient
	logger *zap.Logger
}

func NewAdapter(cfg AdapterConfig, logger *zap.Logger) *Adapter {
	return &Adapter{client: NewRestClient(cfg.BaseURL, cfg.Timeout, cfg.EnableDemo), logger: logger}
}

func (a *Adapter) GetExchangeName() string { return string(models.ExchangeOKX) }

func (a *Adapter) GetServerTime(ctx context.Context) (int64, error) {
	payload, _, err := a.client.Get(ctx, EndpointTime, nil)
	if err != nil {
		return 0, err
	}
	rows, err := payload.DataObjects()
	if err != nil {
		return 0, err
	}
	if len(rows) == 0 {
		return 0, domainerrors.New(domainerrors.BadResponse, "empty time response", 502)
	}
	return int64FromString(str(rows[0], "ts")), nil
}

func (a *Adapter) GetInstruments(ctx context.Context, req models.GetInstrumentsRequest) ([]models.UnifiedInstrument, error) {
	query := map[string]string{"instType": contractTypeToOKXInstType(req.ContractType)}
	if req.Symbol != "" {
		query["instId"] = ToOKXSymbol(req.Symbol)
	}
	payload, _, err := a.client.Get(ctx, EndpointInstruments, query)
	if err != nil {
		return nil, err
	}
	rows, err := payload.DataObjects()
	if err != nil {
		return nil, err
	}
	items := make([]models.UnifiedInstrument, 0, len(rows))
	for _, row := range rows {
		items = append(items, MapInstrument(row))
	}
	return items, nil
}

func (a *Adapter) GetKlines(ctx context.Context, req models.GetKlinesRequest) ([]models.UnifiedKline, error) {
	exchangeSymbol := ToOKXSymbol(req.Symbol)
	query := map[string]string{"instId": exchangeSymbol, "bar": timeframeToOKXBar(req.Timeframe)}
	if req.Limit > 0 {
		query["limit"] = strconv.Itoa(req.Limit)
	}
	if req.StartTime > 0 {
		query["before"] = strconv.FormatInt(req.StartTime, 10)
	}
	if req.EndTime > 0 {
		query["after"] = strconv.FormatInt(req.EndTime, 10)
	}
	payload, _, err := a.client.Get(ctx, EndpointHistoryCandles, query)
	if err != nil {
		return nil, err
	}
	rows, err := payload.DataArrays()
	if err != nil {
		return nil, err
	}
	items := make([]models.UnifiedKline, 0, len(rows))
	for _, row := range rows {
		items = append(items, MapKline(row, exchangeSymbol, req.Timeframe))
	}
	return items, nil
}

func (a *Adapter) GetFundingRate(ctx context.Context, req models.GetFundingRateRequest) (*models.UnifiedFundingRate, error) {
	payload, _, err := a.client.Get(ctx, EndpointFundingRate, map[string]string{"instId": ToOKXSymbol(req.Symbol)})
	if err != nil {
		return nil, err
	}
	rows, err := payload.DataObjects()
	if err != nil {
		return nil, err
	}
	if len(rows) == 0 {
		return nil, domainerrors.New(domainerrors.BadResponse, "empty funding response", 502)
	}
	item := MapFundingRate(rows[0])
	return &item, nil
}

func (a *Adapter) GetFundingRateHistory(ctx context.Context, req models.GetFundingRateHistoryRequest) ([]models.UnifiedFundingRate, error) {
	query := map[string]string{"instId": ToOKXSymbol(req.Symbol)}
	if req.Limit > 0 {
		query["limit"] = strconv.Itoa(req.Limit)
	}
	if req.StartTime > 0 {
		query["before"] = strconv.FormatInt(req.StartTime, 10)
	}
	if req.EndTime > 0 {
		query["after"] = strconv.FormatInt(req.EndTime, 10)
	}
	payload, _, err := a.client.Get(ctx, EndpointFundingRateHistory, query)
	if err != nil {
		return nil, err
	}
	rows, err := payload.DataObjects()
	if err != nil {
		return nil, err
	}
	items := make([]models.UnifiedFundingRate, 0, len(rows))
	for _, row := range rows {
		items = append(items, MapFundingRate(row))
	}
	return items, nil
}

func (a *Adapter) GetMarkPrice(ctx context.Context, req models.GetMarkPriceRequest) (*models.UnifiedMarkPrice, error) {
	payload, _, err := a.client.Get(ctx, EndpointMarkPrice, map[string]string{"instType": "SWAP", "instId": ToOKXSymbol(req.Symbol)})
	if err != nil {
		return nil, err
	}
	rows, err := payload.DataObjects()
	if err != nil {
		return nil, err
	}
	if len(rows) == 0 {
		return nil, domainerrors.New(domainerrors.BadResponse, "empty mark price response", 502)
	}
	item := MapMarkPrice(rows[0])
	return &item, nil
}

func (a *Adapter) PlaceOrder(ctx context.Context, req models.PlaceOrderRequest) (*models.UnifiedOrder, error) {
	return nil, domainerrors.ErrNotImplemented
}
func (a *Adapter) CancelOrder(ctx context.Context, req models.CancelOrderRequest) (*models.UnifiedOrder, error) {
	return nil, domainerrors.ErrNotImplemented
}
func (a *Adapter) AmendOrder(ctx context.Context, req models.AmendOrderRequest) (*models.UnifiedOrder, error) {
	return nil, domainerrors.ErrNotImplemented
}
