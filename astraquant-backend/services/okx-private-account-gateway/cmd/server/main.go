package main

import (
	"context"
	"github.com/astraquant/okx-private-account-gateway/internal/config"
	httptransport "github.com/astraquant/okx-private-account-gateway/internal/transport/http"
	"go.uber.org/zap"
)

func main() {
	cfg := config.Load()
	logger, _ := zap.NewDevelopment()
	router := httptransport.NewRouter(cfg, logger)
	_ = router.Run(context.Background())
}
