package handlers

import "github.com/gin-gonic/gin"

type OrderHandler struct{}

func (h OrderHandler) Handle(c *gin.Context) { c.JSON(200, gin.H{"status": "SUCCESS"}) }
