package handlers

import (
	"strconv"

	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

type FundingHandler struct {
	Gateway *service.ExchangeGatewayService
}

func (h FundingHandler) GetFundingRate(c *gin.Context) {
	item, err := h.Gateway.GetFundingRate(c.Request.Context(), c.Param("exchange"), models.GetFundingRateRequest{Symbol: c.Query("symbol")}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	OK(c, item)
}

func (h FundingHandler) GetFundingRateHistory(c *gin.Context) {
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))
	start, _ := strconv.ParseInt(c.DefaultQuery("start_time", "0"), 10, 64)
	end, _ := strconv.ParseInt(c.DefaultQuery("end_time", "0"), 10, 64)
	items, err := h.Gateway.GetFundingRateHistory(c.Request.Context(), c.Param("exchange"), models.GetFundingRateHistoryRequest{Symbol: c.Query("symbol"), StartTime: start, EndTime: end, Limit: limit}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	Items(c, items)
}
