package service

import (
	"context"
	"sync"
	"time"
)

type RateLimitKey struct {
	Exchange  string
	Endpoint  string
	AccountID string
	Symbol    string
}

type RateLimiter interface {
	Allow(ctx context.Context, key RateLimitKey) (bool, error)
	Wait(ctx context.Context, key RateLimitKey) error
}

type bucket struct {
	tokens     float64
	lastRefill time.Time
}

type InMemoryTokenBucketLimiter struct {
	mu         sync.Mutex
	capacity   float64
	refillRate float64
	buckets    map[string]*bucket
}

func NewInMemoryTokenBucketLimiter(capacity int, refillPerSecond int) *InMemoryTokenBucketLimiter {
	return &InMemoryTokenBucketLimiter{capacity: float64(capacity), refillRate: float64(refillPerSecond), buckets: map[string]*bucket{}}
}

func (l *InMemoryTokenBucketLimiter) Allow(ctx context.Context, key RateLimitKey) (bool, error) {
	l.mu.Lock()
	defer l.mu.Unlock()
	bucketKey := key.String()
	b, ok := l.buckets[bucketKey]
	now := time.Now()
	if !ok {
		b = &bucket{tokens: l.capacity, lastRefill: now}
		l.buckets[bucketKey] = b
	}
	elapsed := now.Sub(b.lastRefill).Seconds()
	b.tokens += elapsed * l.refillRate
	if b.tokens > l.capacity {
		b.tokens = l.capacity
	}
	b.lastRefill = now
	if b.tokens < 1 {
		return false, nil
	}
	b.tokens -= 1
	return true, nil
}

func (l *InMemoryTokenBucketLimiter) Wait(ctx context.Context, key RateLimitKey) error {
	for {
		allowed, err := l.Allow(ctx, key)
		if err != nil {
			return err
		}
		if allowed {
			return nil
		}
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(50 * time.Millisecond):
		}
	}
}

func (k RateLimitKey) String() string {
	return k.Exchange + ":" + k.Endpoint + ":" + k.AccountID + ":" + k.Symbol
}
