package service

import (
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/domain/models"
	"strings"
)

type OrderRequestBuilder struct{ Cfg config.Config }

func (b OrderRequestBuilder) Build(order models.LiveOrder) models.UnifiedOrderRequest {
	return models.UnifiedOrderRequest{AccountID: order.AccountID, Exchange: order.Exchange, InstID: order.InternalSymbol, TdMode: "cross", Side: strings.ToLower(order.Side), PosSide: strings.ToLower(order.PositionSide), OrdType: strings.ToLower(order.OrderType), Px: order.Price, Sz: order.Quantity, ClOrdID: order.ClientOrderID, ReduceOnly: order.ReduceOnly, Tag: b.Cfg.OKXOrderTag}
}
