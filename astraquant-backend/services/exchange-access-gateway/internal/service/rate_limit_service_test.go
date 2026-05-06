package service

import (
	"context"
	"testing"
)

func TestRateLimiterAllow(t *testing.T) {
	limiter := NewInMemoryTokenBucketLimiter(1, 1)
	allowed, err := limiter.Allow(context.Background(), RateLimitKey{Exchange: "OKX", Endpoint: "klines"})
	if err != nil || !allowed {
		t.Fatalf("expected allowed")
	}
}

func TestRateLimiterReject(t *testing.T) {
	limiter := NewInMemoryTokenBucketLimiter(1, 1)
	key := RateLimitKey{Exchange: "OKX", Endpoint: "klines"}
	_, _ = limiter.Allow(context.Background(), key)
	allowed, err := limiter.Allow(context.Background(), key)
	if err != nil || allowed {
		t.Fatalf("expected rejected")
	}
}
