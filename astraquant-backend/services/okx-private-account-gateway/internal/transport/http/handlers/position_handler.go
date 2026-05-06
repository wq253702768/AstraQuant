package handlers

import "github.com/gin-gonic/gin"

type PositionHandler struct{}

func (h PositionHandler) Handle(c *gin.Context) { c.JSON(200, gin.H{"status": "SUCCESS"}) }
