package service

import "sync"

type IdempotencyService struct {
	mu   sync.Mutex
	keys map[string]string
}

func NewIdempotencyService() *IdempotencyService {
	return &IdempotencyService{keys: map[string]string{}}
}
func (s *IdempotencyService) Key(signalID, riskID string) string {
	return "order_executor:" + signalID + ":" + riskID
}
func (s *IdempotencyService) CheckAndSet(key string, orderID string) (string, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if v, ok := s.keys[key]; ok {
		return v, false
	}
	s.keys[key] = orderID
	return orderID, true
}
