package handlers

import (
	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

type InstrumentsHandler struct {
	Gateway *service.ExchangeGatewayService
}

func (h InstrumentsHandler) GetInstruments(c *gin.Context) {
	items, err := h.Gateway.GetInstruments(c.Request.Context(), c.Param("exchange"), models.GetInstrumentsRequest{ContractType: c.DefaultQuery("contract_type", "swap"), Symbol: c.Query("symbol")}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	Items(c, items)
}
