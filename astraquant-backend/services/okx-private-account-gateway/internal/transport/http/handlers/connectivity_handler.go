package handlers

import "github.com/gin-gonic/gin"

type ConnectivityHandler struct{}

func (h ConnectivityHandler) Handle(c *gin.Context) { c.JSON(200, gin.H{"status": "SUCCESS"}) }
