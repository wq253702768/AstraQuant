package service

import "testing"

func TestCircuitBreaker(t *testing.T) {
	breaker := NewCircuitBreaker(2)
	key := "OKX:klines"
	if !breaker.Allow(key) {
		t.Fatal("initial state should allow")
	}
	breaker.RecordFailure(key)
	if !breaker.Allow(key) {
		t.Fatal("one failure should still allow")
	}
	breaker.RecordFailure(key)
	if breaker.Allow(key) {
		t.Fatal("threshold failures should open circuit")
	}
	if breaker.State(key) != CircuitOpen {
		t.Fatal("expected OPEN")
	}
}
