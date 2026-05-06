package handlers

import (
	"github.com/astraquant/realtime-state-service/internal/service"
	"github.com/gin-gonic/gin"
	"net/http"
)

type StateHandler struct{ Query *service.StateQueryService }

func notFound(c *gin.Context) {
	c.JSON(http.StatusNotFound, gin.H{"code": "STATE_NOT_FOUND", "message": "状态不存在"})
}
func (h StateHandler) Market(c *gin.Context) {
	v, ok := h.Query.Market(c.Param("exchange"), c.Param("symbol"))
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) BBO(c *gin.Context) {
	v, ok := h.Query.BBO(c.Param("exchange"), c.Param("symbol"))
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) Trade(c *gin.Context) {
	v, ok := h.Query.Trade(c.Param("exchange"), c.Param("symbol"))
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) Kline(c *gin.Context) {
	tf := c.DefaultQuery("timeframe", "1m")
	v, ok := h.Query.Kline(c.Param("exchange"), c.Param("symbol"), tf)
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) MarkPrice(c *gin.Context) {
	v, ok := h.Query.MarkPrice(c.Param("exchange"), c.Param("symbol"))
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) Funding(c *gin.Context) {
	v, ok := h.Query.Funding(c.Param("exchange"), c.Param("symbol"))
	if !ok {
		notFound(c)
		return
	}
	c.JSON(200, v)
}
func (h StateHandler) Snapshot(c *gin.Context) {
	c.JSON(200, h.Query.Snapshot(c.Param("exchange"), c.Param("symbol")))
}
func (h StateHandler) Freshness(c *gin.Context) {
	c.JSON(200, h.Query.Freshness(c.Param("exchange"), c.Param("symbol")))
}
