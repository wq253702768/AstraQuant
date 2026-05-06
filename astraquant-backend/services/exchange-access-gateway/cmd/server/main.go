package main

import (
	"context"
	"log"

	"github.com/astraquant/exchange-access-gateway/internal/adapters/okx"
	"github.com/astraquant/exchange-access-gateway/internal/config"
	"github.com/astraquant/exchange-access-gateway/internal/observability"
	"github.com/astraquant/exchange-access-gateway/internal/service"
	httptransport "github.com/astraquant/exchange-access-gateway/internal/transport/http"
	"go.uber.org/zap"
)

func main() {
	cfg := config.Load()
	logger, err := zap.NewProduction()
	if cfg.Env == "dev" {
		logger, err = zap.NewDevelopment()
	}
	if err != nil {
		log.Fatal(err)
	}
	defer logger.Sync()

	metrics := observability.NewMetrics()
	adapter := okx.NewAdapter(okx.AdapterConfig{
		BaseURL:    cfg.OKXRestBaseURL,
		Timeout:    cfg.OKXTimeout,
		EnableDemo: cfg.OKXEnableDemo,
	}, logger)

	rateLimiter := service.NewInMemoryTokenBucketLimiter(20, 20)
	breaker := service.NewCircuitBreaker(5)
	auditor := service.NewRequestAuditService(logger, cfg.AuditEnable)
	gateway := service.NewExchangeGatewayService(map[string]service.ExchangeAdapter{"OKX": adapter}, rateLimiter, breaker, auditor, metrics, logger)

	router := httptransport.NewRouter(cfg, gateway, metrics, logger)
	if err := router.Run(context.Background()); err != nil {
		logger.Fatal("exchange gateway stopped", zap.Error(err))
	}
}
