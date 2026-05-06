package handlers

import (
	"github.com/astraquant/realtime-market-gateway/internal/service"
	"github.com/gin-gonic/gin"
)

type RuntimeHandler struct{ Runtime *service.RuntimeStateService }

func (h RuntimeHandler) Status(c *gin.Context) { c.JSON(200, h.Runtime.Status()) }
