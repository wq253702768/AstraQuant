package main

import (
	"context"
	"github.com/astraquant/realtime-market-gateway/internal/config"
	"github.com/astraquant/realtime-market-gateway/internal/observability"
	"github.com/astraquant/realtime-market-gateway/internal/publisher"
	"github.com/astraquant/realtime-market-gateway/internal/service"
	httptransport "github.com/astraquant/realtime-market-gateway/internal/transport/http"
	"go.uber.org/zap"
	"log"
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
	subMgr := service.NewSubscriptionManager()
	subMgr.LoadDefaults(cfg.DefaultSymbols, cfg.DefaultTimeframes)
	runtime := service.NewRuntimeStateService(cfg.ServiceName)
	pub := publisher.NewNATSPublisher(cfg.NATSURL, metrics, logger)
	_ = pub
	router := httptransport.NewRouter(cfg, subMgr, runtime, metrics, logger)
	if err := router.Run(context.Background()); err != nil {
		logger.Fatal("realtime market gateway stopped", zap.Error(err))
	}
}
