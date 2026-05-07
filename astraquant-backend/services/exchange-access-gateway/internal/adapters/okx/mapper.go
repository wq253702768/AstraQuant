package okx

import (
	"strconv"
	"strings"
	"time"

	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
)

func ToOKXSymbol(internalSymbol string) string { return internalSymbol }
func FromOKXSymbol(okxSymbol string) string    { return okxSymbol }

func timeframeToOKXBar(timeframe string) string {
	switch timeframe {
	case "1m", "5m", "15m":
		return timeframe
	case "1h":
		return "1H"
	default:
		return timeframe
	}
}

func contractTypeToOKXInstType(contractType string) string {
	if strings.EqualFold(contractType, "futures") {
		return "FUTURES"
	}
	return "SWAP"
}

func contractTypeFromOKX(instType string) string {
	if strings.EqualFold(instType, "FUTURES") {
		return "futures"
	}
	return "swap"
}

func statusFromOKX(state string) string {
	if strings.EqualFold(state, "live") {
		return "active"
	}
	return strings.ToLower(state)
}

func precisionFromStep(step string) int {
	if !strings.Contains(step, ".") {
		return 0
	}
	trimmed := strings.TrimRight(strings.Split(step, ".")[1], "0")
	return len(trimmed)
}

func str(data map[string]any, key string) string {
	if value, ok := data[key]; ok && value != nil {
		return strings.TrimSpace(toString(value))
	}
	return ""
}

func toString(value any) string {
	switch typed := value.(type) {
	case string:
		return typed
	case float64:
		return strconv.FormatFloat(typed, 'f', -1, 64)
	case int64:
		return strconv.FormatInt(typed, 10)
	case int:
		return strconv.Itoa(typed)
	default:
		return ""
	}
}

func int64FromString(value string) int64 {
	parsed, _ := strconv.ParseInt(value, 10, 64)
	return parsed
}

func MapInstrument(data map[string]any) models.UnifiedInstrument {
	tickSize := str(data, "tickSz")
	lotSize := str(data, "lotSz")
	exchangeSymbol := str(data, "instId")
	return models.UnifiedInstrument{
		Exchange:       string(models.ExchangeOKX),
		InternalSymbol: FromOKXSymbol(exchangeSymbol),
		ExchangeSymbol: exchangeSymbol,
		BaseAsset:      str(data, "baseCcy"),
		QuoteAsset:     str(data, "quoteCcy"),
		MarginAsset:    str(data, "settleCcy"),
		ContractType:   contractTypeFromOKX(str(data, "instType")),
		TickSize:       tickSize,
		LotSize:        lotSize,
		MinSize:        str(data, "minSz"),
		ContractValue:  str(data, "ctVal"),
		PricePrecision: precisionFromStep(tickSize),
		SizePrecision:  precisionFromStep(lotSize),
		Status:         statusFromOKX(str(data, "state")),
	}
}

func MapTicker(data map[string]any) models.UnifiedTicker {
	exchangeSymbol := str(data, "instId")
	return models.UnifiedTicker{
		Exchange:       string(models.ExchangeOKX),
		InternalSymbol: FromOKXSymbol(exchangeSymbol),
		ExchangeSymbol: exchangeSymbol,
		LastPrice:      str(data, "last"),
		BestBidPrice:   str(data, "bidPx"),
		BestAskPrice:   str(data, "askPx"),
		BestBidSize:    str(data, "bidSz"),
		BestAskSize:    str(data, "askSz"),
		Open24h:        str(data, "open24h"),
		High24h:        str(data, "high24h"),
		Low24h:         str(data, "low24h"),
		Volume24h:      str(data, "vol24h"),
		VolumeCcy24h:   str(data, "volCcy24h"),
		ExchangeTime:   int64FromString(str(data, "ts")),
		ReceivedAt:     time.Now().UnixMilli(),
	}
}

func MapKline(row []any, exchangeSymbol string, timeframe string) models.UnifiedKline {
	value := func(index int) string {
		if index >= len(row) {
			return ""
		}
		return toString(row[index])
	}
	return models.UnifiedKline{
		Exchange:       string(models.ExchangeOKX),
		InternalSymbol: FromOKXSymbol(exchangeSymbol),
		ExchangeSymbol: exchangeSymbol,
		Timeframe:      timeframe,
		Timestamp:      int64FromString(value(0)),
		Open:           value(1),
		High:           value(2),
		Low:            value(3),
		Close:          value(4),
		Volume:         value(5),
		QuoteVolume:    value(7),
	}
}

func MapFundingRate(data map[string]any) models.UnifiedFundingRate {
	exchangeSymbol := str(data, "instId")
	return models.UnifiedFundingRate{
		Exchange:        string(models.ExchangeOKX),
		InternalSymbol:  FromOKXSymbol(exchangeSymbol),
		ExchangeSymbol:  exchangeSymbol,
		FundingRate:     str(data, "fundingRate"),
		RealizedRate:    str(data, "realizedRate"),
		FundingTime:     int64FromString(str(data, "fundingTime")),
		NextFundingTime: int64FromString(str(data, "nextFundingTime")),
		MarkPrice:       str(data, "markPx"),
	}
}

func MapMarkPrice(data map[string]any) models.UnifiedMarkPrice {
	exchangeSymbol := str(data, "instId")
	return models.UnifiedMarkPrice{
		Exchange:       string(models.ExchangeOKX),
		InternalSymbol: FromOKXSymbol(exchangeSymbol),
		ExchangeSymbol: exchangeSymbol,
		MarkPrice:      str(data, "markPx"),
		IndexPrice:     str(data, "idxPx"),
		Timestamp:      int64FromString(str(data, "ts")),
	}
}
