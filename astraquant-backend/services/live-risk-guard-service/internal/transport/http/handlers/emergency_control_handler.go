package handlers

import (
	"github.com/astraquant/live-risk-guard-service/internal/service"
	"github.com/gin-gonic/gin"
)

type EmergencyControlHandler struct {
	Service *service.EmergencyControlService
}

func (h EmergencyControlHandler) Trigger(c *gin.Context) {
	var req map[string]string
	_ = c.BindJSON(&req)
	ctrl := h.Service.Trigger(req["scope"], req["account_id"], req["strategy_version_id"], req["action"], req["reason"], "manual")
	c.JSON(200, gin.H{"emergency_control_id": ctrl.ID, "enabled": ctrl.Enabled, "action": ctrl.Action})
}
func (h EmergencyControlHandler) Release(c *gin.Context) {
	ctrl, ok := h.Service.Release(c.Param("id"), "manual")
	if !ok {
		c.JSON(404, gin.H{"code": "EMERGENCY_CONTROL_NOT_FOUND"})
		return
	}
	c.JSON(200, gin.H{"emergency_control_id": ctrl.ID, "enabled": ctrl.Enabled})
}
