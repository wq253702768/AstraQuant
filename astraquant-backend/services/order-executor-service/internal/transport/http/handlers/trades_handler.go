package handlers

import "github.com/gin-gonic/gin"

func Trades(c *gin.Context) { c.JSON(200, gin.H{"items": []any{}, "total": 0}) }
