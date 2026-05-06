package http

import (
	"context"
	"github.com/astraquant/risk-engine/internal/config"
	"github.com/astraquant/risk-engine/internal/infrastructure/repositories"
	"github.com/astraquant/risk-engine/internal/observability"
	"github.com/astraquant/risk-engine/internal/service"
	"github.com/astraquant/risk-engine/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, checker *service.RiskCheckService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	if cfg.Env != "dev" {
		gin.SetMode(gin.ReleaseMode)
	}
	e := gin.New()
	e.Use(gin.Recovery())
	repo := &repositories.RiskDecisionRepository{}
	h := handlers.HealthHandler{ServiceName: cfg.ServiceName}
	d := handlers.DecisionsHandler{Checker: checker, Repo: repo}
	e.GET("/health", h.Health)
	e.GET("/metrics", gin.WrapH(promhttp.Handler()))
	e.GET("/risk/decisions", d.List)
	e.GET("/risk/decisions/:id", d.Get)
	e.POST("/risk/check", d.Check)
	e.GET("/risk/rules", handlers.Rules)
	e.GET("/risk/runtime", handlers.Runtime)
	return &Router{engine: e, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
func (r *Router) Engine() *gin.Engine           { return r.engine }
