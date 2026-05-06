package okx_ws

import "testing"

func TestOKXTickerMapper(t *testing.T) {
	e := MapTicker(map[string]any{"instId": "BTC-USDT-SWAP", "last": "81426.3", "ts": "1760000000000"})
	if e.EventType != "TICKER" || e.Payload["last_price"] != "81426.3" {
		t.Fatalf("bad ticker: %+v", e)
	}
}
func TestOKXBBOMapper(t *testing.T) {
	e := MapBBO(map[string]any{"instId": "BTC-USDT-SWAP", "bidPx": "1", "askPx": "2", "ts": "1760000000000"})
	if e.EventType != "BBO" || e.Payload["bid_price"] != "1" {
		t.Fatalf("bad bbo")
	}
}
func TestOKXTradeMapper(t *testing.T) {
	e := MapTrade(map[string]any{"instId": "BTC-USDT-SWAP", "tradeId": "t1", "px": "1", "sz": "2", "side": "buy", "ts": "1760000000000"})
	if e.Payload["trade_id"] != "t1" {
		t.Fatalf("bad trade")
	}
}
func TestOKXKlineMapper(t *testing.T) {
	e := MapKline("candle1m", "BTC-USDT-SWAP", []any{"1760000000000", "1", "2", "1", "2", "10", "0", "20", "0"})
	if e.EventType != "KLINE" || e.Payload["timeframe"] != "1m" {
		t.Fatalf("bad kline")
	}
}
func TestOKXMarkPriceMapper(t *testing.T) {
	e := MapMarkPrice(map[string]any{"instId": "BTC-USDT-SWAP", "markPx": "1", "idxPx": "2", "ts": "1760000000000"})
	if e.Payload["index_price"] != "2" {
		t.Fatalf("bad mark")
	}
}
func TestOKXFundingMapper(t *testing.T) {
	e := MapFunding(map[string]any{"instId": "BTC-USDT-SWAP", "fundingRate": "0.1", "nextFundingTime": "1760000000000", "ts": "1760000000000"})
	if e.EventType != "FUNDING" {
		t.Fatalf("bad funding")
	}
}
