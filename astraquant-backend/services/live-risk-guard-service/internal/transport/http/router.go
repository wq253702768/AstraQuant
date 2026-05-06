package http

import (
	"context"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/observability"
	"github.com/astraquant/live-risk-guard-service/internal/service"
	"github.com/astraquant/live-risk-guard-service/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, svc *service.EmergencyControlService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/health", handlers.HealthHandler{ServiceName: cfg.ServiceName}.Health)
	e.GET("/metrics", gin.WrapH(promhttp.Handler()))
	sh := handlers.RiskStateHandler{Service: svc}
	cb := handlers.CircuitBreakerHandler{Service: svc}
	ec := handlers.EmergencyControlHandler{Service: svc}
	e.GET("/live-risk/states", sh.List)
	e.GET("/live-risk/circuit-breakers", cb.List)
	e.GET("/live-risk/circuit-breakers/:id", cb.Get)
	e.POST("/live-risk/emergency-controls/trigger", ec.Trigger)
	e.POST("/live-risk/emergency-controls/:id/release", ec.Release)
	e.GET("/live-risk/rules", handlers.Rules)
	return &Router{engine: e, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
func (r *Router) Engine() *gin.Engine           { return r.engine }
