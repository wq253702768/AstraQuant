package okx_ws

import (
	"fmt"
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"strconv"
	"time"
)

func str(data map[string]any, key string) string {
	if v, ok := data[key]; ok && v != nil {
		return fmt.Sprint(v)
	}
	return ""
}
func i64(data map[string]any, key string) int64 {
	v, _ := strconv.ParseInt(str(data, key), 10, 64)
	return v
}
func eventID(eventType string, symbol string, eventTime int64) string {
	return fmt.Sprintf("evt_%s_%s_%d", eventType, symbol, eventTime)
}
func base(eventType string, channel string, data map[string]any, payload map[string]any) models.UnifiedMarketEvent {
	exchangeSymbol := str(data, "instId")
	eventTime := i64(data, "ts")
	receive := time.Now().UnixMilli()
	return models.UnifiedMarketEvent{EventID: eventID(eventType, exchangeSymbol, eventTime), EventType: eventType, Exchange: "OKX", InternalSymbol: FromOKXSymbol(exchangeSymbol), ExchangeSymbol: exchangeSymbol, EventTime: eventTime, ReceiveTime: receive, LatencyMs: receive - eventTime, Payload: payload}
}
