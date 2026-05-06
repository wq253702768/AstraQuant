package handlers

import "github.com/gin-gonic/gin"

type HealthHandler struct{ ServiceName string }

func (h HealthHandler) Health(c *gin.Context) { OK(c, gin.H{"status": "ok", "service": h.ServiceName}) }
