package handlers

import (
	"strconv"

	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

type MarketDataHandler struct {
	Gateway *service.ExchangeGatewayService
}

func (h MarketDataHandler) GetTime(c *gin.Context) {
	serverTime, err := h.Gateway.GetServerTime(c.Request.Context(), c.Param("exchange"), middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	OK(c, gin.H{"exchange": c.Param("exchange"), "server_time": serverTime})
}

func (h MarketDataHandler) GetKlines(c *gin.Context) {
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))
	start, _ := strconv.ParseInt(c.DefaultQuery("start_time", "0"), 10, 64)
	end, _ := strconv.ParseInt(c.DefaultQuery("end_time", "0"), 10, 64)
	items, err := h.Gateway.GetKlines(c.Request.Context(), c.Param("exchange"), models.GetKlinesRequest{Symbol: c.Query("symbol"), Timeframe: c.DefaultQuery("timeframe", "5m"), StartTime: start, EndTime: end, Limit: limit}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	Items(c, items)
}
