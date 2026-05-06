package handlers

import "github.com/gin-gonic/gin"

type RuntimeHandler struct{}

func (h RuntimeHandler) Handle(c *gin.Context) { c.JSON(200, gin.H{"status": "SUCCESS"}) }
