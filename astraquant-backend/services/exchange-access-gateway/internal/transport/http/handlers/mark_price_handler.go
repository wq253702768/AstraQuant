package handlers

import (
	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

type MarkPriceHandler struct {
	Gateway *service.ExchangeGatewayService
}

func (h MarkPriceHandler) GetMarkPrice(c *gin.Context) {
	item, err := h.Gateway.GetMarkPrice(c.Request.Context(), c.Param("exchange"), models.GetMarkPriceRequest{Symbol: c.Query("symbol")}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	OK(c, item)
}
