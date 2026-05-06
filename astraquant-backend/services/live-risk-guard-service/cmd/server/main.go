package main

import (
	"context"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/observability"
	"github.com/astraquant/live-risk-guard-service/internal/rules"
	"github.com/astraquant/live-risk-guard-service/internal/service"
	httptransport "github.com/astraquant/live-risk-guard-service/internal/transport/http"
	"go.uber.org/zap"
)

func main() {
	cfg := config.Load()
	logger, _ := zap.NewDevelopment()
	metrics := observability.NewMetrics()
	engine := rules.NewCircuitBreakerEngine(cfg)
	svc := service.NewEmergencyControlService(engine, metrics)
	router := httptransport.NewRouter(cfg, svc, metrics, logger)
	_ = router.Run(context.Background())
}
