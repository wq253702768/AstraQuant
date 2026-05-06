package service

import (
	"testing"
	"time"
)

func TestReconnectBackoff(t *testing.T) {
	r := NewReconnectManager(30 * time.Second)
	if r.Backoff(1) != time.Second {
		t.Fatal("bad first")
	}
	if r.Backoff(10) != 30*time.Second {
		t.Fatal("bad max")
	}
}
