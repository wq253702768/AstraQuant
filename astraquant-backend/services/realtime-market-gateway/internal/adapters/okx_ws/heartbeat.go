package okx_ws

import "time"

type Heartbeat struct {
	LastPong time.Time
	Timeout  time.Duration
}

func NewHeartbeat(timeout time.Duration) *Heartbeat {
	return &Heartbeat{LastPong: time.Now(), Timeout: timeout}
}
func (h *Heartbeat) Pong()          { h.LastPong = time.Now() }
func (h *Heartbeat) TimedOut() bool { return time.Since(h.LastPong) > h.Timeout }
