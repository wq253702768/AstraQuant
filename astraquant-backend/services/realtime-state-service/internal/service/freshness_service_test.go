package service

import (
	"github.com/astraquant/realtime-state-service/internal/config"
	"testing"
	"time"
)

func TestFreshnessFresh(t *testing.T) {
	s := NewFreshnessService(config.Config{TickerStaleMs: 5000})
	status, fresh, _ := s.Status(time.Now().UnixMilli(), 5000)
	if status != "FRESH" || !fresh {
		t.Fatal("expected fresh")
	}
}
func TestFreshnessStale(t *testing.T) {
	s := NewFreshnessService(config.Config{TickerStaleMs: 5000})
	status, fresh, _ := s.Status(time.Now().Add(-10*time.Second).UnixMilli(), 5000)
	if status != "STALE" || fresh {
		t.Fatal("expected stale")
	}
}
