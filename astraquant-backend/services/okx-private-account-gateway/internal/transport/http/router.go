package http

import (
	"context"
	"github.com/astraquant/okx-private-account-gateway/internal/config"
	"github.com/astraquant/okx-private-account-gateway/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, logger *zap.Logger) *Router {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/health", handlers.HealthHandler{ServiceName: cfg.ServiceName}.Health)
	e.GET("/api/v1/runtime/status", handlers.RuntimeHandler{}.Handle)
	e.POST("/api/v1/accounts/:account_id/sync", handlers.AccountHandler{}.Handle)
	e.POST("/api/v1/accounts/:account_id/test-connectivity", handlers.ConnectivityHandler{}.Handle)
	return &Router{engine: e, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
