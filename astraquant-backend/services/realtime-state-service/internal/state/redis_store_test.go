package state

import "testing"

func TestRedisKeyBuilder(t *testing.T) {
	s := NewRedisStore("localhost:6379", 0)
	if s.Key("market", "OKX", "BTC-USDT-SWAP", "") != "realtime:market:OKX:BTC-USDT-SWAP" {
		t.Fatal("bad key")
	}
}
