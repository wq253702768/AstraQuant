package main

import (
	"context"
	"github.com/astraquant/realtime-state-service/internal/config"
	"github.com/astraquant/realtime-state-service/internal/observability"
	"github.com/astraquant/realtime-state-service/internal/service"
	"github.com/astraquant/realtime-state-service/internal/state"
	httptransport "github.com/astraquant/realtime-state-service/internal/transport/http"
	"go.uber.org/zap"
	"log"
)

func main() {
	cfg := config.Load()
	logger, err := zap.NewDevelopment()
	if cfg.Env != "dev" {
		logger, err = zap.NewProduction()
	}
	if err != nil {
		log.Fatal(err)
	}
	defer logger.Sync()
	metrics := observability.NewMetrics()
	store := state.NewMemoryStateStore()
	freshness := service.NewFreshnessService(cfg)
	updater := service.NewStateUpdateService(store, freshness, metrics)
	query := service.NewStateQueryService(store, freshness)
	_ = updater
	router := httptransport.NewRouter(cfg, query, metrics, logger)
	if err := router.Run(context.Background()); err != nil {
		logger.Fatal("realtime state stopped", zap.Error(err))
	}
}
