package service

import (
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"sync"
	"time"
)

type RuntimeStateService struct {
	mu          sync.RWMutex
	serviceName string
	connections map[string]models.ConnectionState
}

func NewRuntimeStateService(serviceName string) *RuntimeStateService {
	s := &RuntimeStateService{serviceName: serviceName, connections: map[string]models.ConnectionState{}}
	s.connections["OKX:public"] = models.ConnectionState{Exchange: "OKX", ConnectionType: "public", Status: models.StateRunning}
	s.connections["OKX:business"] = models.ConnectionState{Exchange: "OKX", ConnectionType: "business", Status: models.StateRunning}
	return s
}
func (s *RuntimeStateService) Touch(key string, subCount int) {
	s.mu.Lock()
	defer s.mu.Unlock()
	st := s.connections[key]
	st.LastMessageTime = time.Now().UnixMilli()
	st.SubscriptionCount = subCount
	st.Status = models.StateRunning
	s.connections[key] = st
}
func (s *RuntimeStateService) Status() map[string]any {
	s.mu.RLock()
	defer s.mu.RUnlock()
	items := make([]models.ConnectionState, 0, len(s.connections))
	for _, v := range s.connections {
		items = append(items, v)
	}
	return map[string]any{"service": s.serviceName, "connections": items}
}
