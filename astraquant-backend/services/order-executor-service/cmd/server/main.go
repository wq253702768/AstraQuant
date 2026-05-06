package main

import (
	"context"
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/observability"
	"github.com/astraquant/order-executor-service/internal/service"
	httptransport "github.com/astraquant/order-executor-service/internal/transport/http"
	"go.uber.org/zap"
)

func main() {
	cfg := config.Load()
	logger, _ := zap.NewDevelopment()
	metrics := observability.NewMetrics()
	executor := service.NewOrderExecutionService(cfg, metrics, logger)
	router := httptransport.NewRouter(cfg, executor, metrics, logger)
	_ = router.Run(context.Background())
}
