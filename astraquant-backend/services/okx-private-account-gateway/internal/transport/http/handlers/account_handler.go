package handlers

import "github.com/gin-gonic/gin"

type AccountHandler struct{}

func (h AccountHandler) Handle(c *gin.Context) { c.JSON(200, gin.H{"status": "SUCCESS"}) }
