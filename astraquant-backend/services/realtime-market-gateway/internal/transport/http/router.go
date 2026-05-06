package http

import (
	"context"
	"github.com/astraquant/realtime-market-gateway/internal/config"
	"github.com/astraquant/realtime-market-gateway/internal/observability"
	"github.com/astraquant/realtime-market-gateway/internal/service"
	"github.com/astraquant/realtime-market-gateway/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, subs *service.SubscriptionManager, runtime *service.RuntimeStateService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	if cfg.Env != "dev" {
		gin.SetMode(gin.ReleaseMode)
	}
	engine := gin.New()
	engine.Use(gin.Recovery())
	health := handlers.HealthHandler{ServiceName: cfg.ServiceName}
	sub := handlers.SubscriptionsHandler{Manager: subs}
	rt := handlers.RuntimeHandler{Runtime: runtime}
	engine.GET("/health", health.Health)
	engine.GET("/metrics", gin.WrapH(promhttp.Handler()))
	v1 := engine.Group("/api/v1")
	v1.GET("/runtime/status", rt.Status)
	v1.GET("/subscriptions", sub.List)
	v1.POST("/subscriptions", sub.Add)
	v1.DELETE("/subscriptions", sub.Remove)
	return &Router{engine: engine, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
func (r *Router) Engine() *gin.Engine           { return r.engine }
