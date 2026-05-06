package service

import (
	"sync"
	"time"
)

type CircuitState string

const (
	CircuitClosed   CircuitState = "CLOSED"
	CircuitOpen     CircuitState = "OPEN"
	CircuitHalfOpen CircuitState = "HALF_OPEN"
)

type CircuitBreaker struct {
	mu        sync.Mutex
	threshold int
	cooldown  time.Duration
	failures  map[string]int
	openedAt  map[string]time.Time
}

func NewCircuitBreaker(threshold int) *CircuitBreaker {
	return &CircuitBreaker{threshold: threshold, cooldown: 30 * time.Second, failures: map[string]int{}, openedAt: map[string]time.Time{}}
}

func (b *CircuitBreaker) Allow(key string) bool {
	b.mu.Lock()
	defer b.mu.Unlock()
	opened, ok := b.openedAt[key]
	if !ok {
		return true
	}
	if time.Since(opened) > b.cooldown {
		delete(b.openedAt, key)
		b.failures[key] = 0
		return true
	}
	return false
}

func (b *CircuitBreaker) RecordSuccess(key string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.failures[key] = 0
	delete(b.openedAt, key)
}

func (b *CircuitBreaker) RecordFailure(key string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.failures[key]++
	if b.failures[key] >= b.threshold {
		b.openedAt[key] = time.Now()
	}
}

func (b *CircuitBreaker) State(key string) CircuitState {
	b.mu.Lock()
	defer b.mu.Unlock()
	opened, ok := b.openedAt[key]
	if !ok {
		return CircuitClosed
	}
	if time.Since(opened) > b.cooldown {
		return CircuitHalfOpen
	}
	return CircuitOpen
}
