package okx

import "testing"

func TestOKXInstrumentMapper(t *testing.T) {
	item := MapInstrument(map[string]any{"instId": "BTC-USDT-SWAP", "baseCcy": "BTC", "quoteCcy": "USDT", "settleCcy": "USDT", "instType": "SWAP", "tickSz": "0.1", "lotSz": "0.01", "minSz": "0.01", "ctVal": "0.01", "state": "live"})
	if item.InternalSymbol != "BTC-USDT-SWAP" || item.PricePrecision != 1 || item.SizePrecision != 2 || item.Status != "active" {
		t.Fatalf("bad instrument mapping: %+v", item)
	}
}

func TestOKXKlineMapper(t *testing.T) {
	item := MapKline([]any{"1760000000000", "81000", "81200", "80900", "81150", "123.45", "1", "10000000", "1"}, "BTC-USDT-SWAP", "5m")
	if item.Timestamp != 1760000000000 || item.Close != "81150" || item.QuoteVolume != "10000000" {
		t.Fatalf("bad kline mapping: %+v", item)
	}
}

func TestOKXFundingMapper(t *testing.T) {
	item := MapFundingRate(map[string]any{"instId": "BTC-USDT-SWAP", "fundingRate": "0.0001", "realizedRate": "0.0001", "fundingTime": "1760000000000", "nextFundingTime": "1760028800000", "markPx": "81420.1"})
	if item.FundingTime != 1760000000000 || item.MarkPrice != "81420.1" {
		t.Fatalf("bad funding mapping: %+v", item)
	}
}

func TestOKXMarkPriceMapper(t *testing.T) {
	item := MapMarkPrice(map[string]any{"instId": "BTC-USDT-SWAP", "markPx": "81420.1", "idxPx": "81418.9", "ts": "1760000000000"})
	if item.IndexPrice != "81418.9" || item.Timestamp != 1760000000000 {
		t.Fatalf("bad mark mapping: %+v", item)
	}
}
