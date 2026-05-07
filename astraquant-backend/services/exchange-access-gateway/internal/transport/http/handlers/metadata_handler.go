package handlers

import (
	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"github.com/astraquant/exchange-access-gateway/internal/domain/models"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

type MetadataHandler struct {
	Gateway *service.ExchangeGatewayService
}

type SyncInstrumentsRequest struct {
	Exchange string `json:"exchange"`
	InstType string `json:"inst_type"`
}

func (h MetadataHandler) SyncInstruments(c *gin.Context) {
	var req SyncInstrumentsRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		Error(c, domainerrors.New(domainerrors.BadResponse, "invalid sync payload", 400))
		return
	}
	if req.Exchange == "" {
		req.Exchange = "OKX"
	}
	if req.InstType == "" {
		req.InstType = "SWAP"
	}
	result, err := h.Gateway.SyncInstruments(c.Request.Context(), req.Exchange, models.GetInstrumentsRequest{ContractType: req.InstType}, middleware.TraceID(c))
	if err != nil {
		Error(c, err)
		return
	}
	OK(c, result)
}

func (h MetadataHandler) ListInstruments(c *gin.Context) {
	exchange := c.DefaultQuery("exchange", "OKX")
	Items(c, h.Gateway.ListStoredInstruments(exchange))
}

func (h MetadataHandler) GetInstrument(c *gin.Context) {
	exchange := c.DefaultQuery("exchange", "OKX")
	item, ok := h.Gateway.GetStoredInstrument(exchange, c.Param("symbol"))
	if !ok {
		Error(c, domainerrors.New(domainerrors.SymbolNotSupported, "instrument not found", 404))
		return
	}
	OK(c, item)
}

func (h MetadataHandler) SymbolMappings(c *gin.Context) {
	exchange := c.DefaultQuery("exchange", "OKX")
	Items(c, h.Gateway.ListSymbolMappings(exchange))
}
