package handlers

import (
	"github.com/astraquant/live-risk-guard-service/internal/service"
	"github.com/gin-gonic/gin"
)

type CircuitBreakerHandler struct {
	Service *service.EmergencyControlService
}

func (h CircuitBreakerHandler) List(c *gin.Context) {
	c.JSON(200, gin.H{"items": h.Service.ListEvents(), "total": len(h.Service.ListEvents())})
}
func (h CircuitBreakerHandler) Get(c *gin.Context) {
	if e, ok := h.Service.GetEvent(c.Param("id")); ok {
		c.JSON(200, e)
		return
	}
	c.JSON(404, gin.H{"code": "CIRCUIT_BREAKER_NOT_FOUND"})
}
