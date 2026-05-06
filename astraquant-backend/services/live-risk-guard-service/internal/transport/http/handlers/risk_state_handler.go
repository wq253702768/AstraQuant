package handlers

import (
	"github.com/astraquant/live-risk-guard-service/internal/service"
	"github.com/gin-gonic/gin"
)

type RiskStateHandler struct {
	Service *service.EmergencyControlService
}

func (h RiskStateHandler) List(c *gin.Context) { c.JSON(200, gin.H{"items": h.Service.ListStates()}) }
