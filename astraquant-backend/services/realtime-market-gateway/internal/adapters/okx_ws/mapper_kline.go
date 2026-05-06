package okx_ws

import "github.com/astraquant/realtime-market-gateway/internal/domain/models"

func MapKline(channel string, exchangeSymbol string, row []any) models.UnifiedMarketEvent {
	data := map[string]any{"instId": exchangeSymbol, "ts": row[0]}
	event := base("KLINE", channel, data, map[string]any{"timeframe": TimeframeFromChannel(channel), "open": row[1], "high": row[2], "low": row[3], "close": row[4], "volume": row[5], "quote_volume": row[7], "confirmed": row[8] == "1"})
	return event
}
