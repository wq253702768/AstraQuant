package service

import (
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"testing"
)

func TestSubscriptionManagerAddRemove(t *testing.T) {
	m := NewSubscriptionManager()
	s := models.Subscription{Exchange: "OKX", Channel: "tickers", InternalSymbol: "BTC-USDT-SWAP"}
	m.Add(s)
	if len(m.List()) != 1 {
		t.Fatal("expected one")
	}
	m.Remove(s)
	if len(m.List()) != 0 {
		t.Fatal("expected none")
	}
}
