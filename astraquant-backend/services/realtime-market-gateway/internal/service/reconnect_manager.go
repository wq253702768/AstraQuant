package service

import "time"

type ReconnectManager struct{ MaxBackoff time.Duration }

func NewReconnectManager(max time.Duration) *ReconnectManager {
	return &ReconnectManager{MaxBackoff: max}
}
func (m *ReconnectManager) Backoff(attempt int) time.Duration {
	if attempt <= 0 {
		return time.Second
	}
	d := time.Duration(1<<min(attempt-1, 5)) * time.Second
	if d > m.MaxBackoff {
		return m.MaxBackoff
	}
	return d
}
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
