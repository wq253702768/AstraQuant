package okx

import "testing"

func TestOKXSigner(t *testing.T) {
	sig := Sign(SignInput{Timestamp: "2020-12-08T09:08:57.715Z", Method: "GET", RequestPath: "/api/v5/account/balance?ccy=BTC", SecretKey: "22582BD0CFF14C41EDBF1AB98506286D"})
	if sig == "" {
		t.Fatal("empty sign")
	}
}
func TestPrivateWSLoginPayload(t *testing.T) {
	msg := BuildLogin("key", "pass", "ts", "sign")
	if msg.Op != "login" || msg.Args[0].APIKey != "key" {
		t.Fatal("bad login")
	}
}
func TestAccountMapper(t *testing.T) {
	m := MapAccount(map[string]any{"ccy": "USDT", "eq": "1"})
	if m["currency"] != "USDT" {
		t.Fatal("bad account")
	}
}
func TestPositionMapper(t *testing.T) {
	m := MapPosition(map[string]any{"instId": "BTC-USDT-SWAP", "pos": "1"})
	if m["internal_symbol"] != "BTC-USDT-SWAP" {
		t.Fatal("bad position")
	}
}
func TestOrderMapper(t *testing.T) {
	m := MapOrder(map[string]any{"ordId": "1", "state": "filled"})
	if m["exchange_order_id"] != "1" {
		t.Fatal("bad order")
	}
}
func TestTradeMapper(t *testing.T) {
	m := MapTrade(map[string]any{"tradeId": "1"})
	if m["tradeId"] != "1" {
		t.Fatal("bad trade")
	}
}
func TestErrorMapperAuthFailed(t *testing.T) {
	if MapError("50113") != "OKX_AUTH_FAILED" {
		t.Fatal("bad error")
	}
}
