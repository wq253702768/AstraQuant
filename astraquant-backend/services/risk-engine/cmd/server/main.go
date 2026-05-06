package main

import (
	"context"
	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/observability"
	"github.com/astraquant/risk-engine/internal/rules"
	"github.com/astraquant/risk-engine/internal/service"
	httptransport "github.com/astraquant/risk-engine/internal/transport/http"
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
	engine := rules.NewDefaultRuleEngine(cfg)
	checker := service.NewRiskCheckService(engine, cfg, metrics, logger)
	router := httptransport.NewRouter(cfg, checker, metrics, logger)
	if err := router.Run(context.Background()); err != nil {
		logger.Fatal("risk engine stopped", zap.Error(err))
	}
}
