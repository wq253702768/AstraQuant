package http

import (
	"context"

	"github.com/astraquant/exchange-access-gateway/internal/config"
	"github.com/astraquant/exchange-access-gateway/internal/observability"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/handlers"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, gateway *service.ExchangeGatewayService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	if cfg.Env != "dev" {
		gin.SetMode(gin.ReleaseMode)
	}
	engine := gin.New()
	engine.Use(middleware.Trace(), middleware.Recover(logger), middleware.Logging(logger))

	health := handlers.HealthHandler{ServiceName: cfg.ServiceName}
	market := handlers.MarketDataHandler{Gateway: gateway}
	instruments := handlers.InstrumentsHandler{Gateway: gateway}
	funding := handlers.FundingHandler{Gateway: gateway}
	mark := handlers.MarkPriceHandler{Gateway: gateway}

	engine.GET("/health", health.Health)
	engine.GET("/metrics", gin.WrapH(promhttp.Handler()))

	v1 := engine.Group("/api/v1/exchanges/:exchange")
	v1.GET("/time", market.GetTime)
	v1.GET("/instruments", instruments.GetInstruments)
	v1.GET("/klines", market.GetKlines)
	v1.GET("/funding-rate", funding.GetFundingRate)
	v1.GET("/funding-rate-history", funding.GetFundingRateHistory)
	v1.GET("/mark-price", mark.GetMarkPrice)

	return &Router{engine: engine, cfg: cfg}
}

func (r *Router) Run(ctx context.Context) error {
	return r.engine.Run(":" + r.cfg.HTTPPort)
}

func (r *Router) Engine() *gin.Engine { return r.engine }
