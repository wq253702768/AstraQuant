package http

import (
	"context"
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/observability"
	"github.com/astraquant/order-executor-service/internal/service"
	"github.com/astraquant/order-executor-service/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, executor *service.OrderExecutionService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/health", handlers.HealthHandler{ServiceName: cfg.ServiceName}.Health)
	e.GET("/metrics", gin.WrapH(promhttp.Handler()))
	oh := handlers.OrdersHandler{Executor: executor}
	dh := handlers.DryRunHandler{Executor: executor}
	e.GET("/order-executor/orders", oh.List)
	e.GET("/order-executor/orders/:id", oh.Get)
	e.GET("/order-executor/trades", handlers.Trades)
	e.POST("/order-executor/dry-run", dh.DryRun)
	e.POST("/order-executor/orders/:id/cancel", oh.Cancel)
	e.GET("/order-executor/orders/:id/logs", oh.Logs)
	e.POST("/order-executor/kill-switch/trigger", handlers.TriggerKillSwitch)
	e.POST("/order-executor/kill-switch/:id/release", handlers.ReleaseKillSwitch)
	return &Router{engine: e, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
func (r *Router) Engine() *gin.Engine           { return r.engine }
