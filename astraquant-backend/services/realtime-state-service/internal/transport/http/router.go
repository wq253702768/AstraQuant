package http

import (
	"context"
	"github.com/astraquant/realtime-state-service/internal/config"
	"github.com/astraquant/realtime-state-service/internal/observability"
	"github.com/astraquant/realtime-state-service/internal/service"
	"github.com/astraquant/realtime-state-service/internal/transport/http/handlers"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.uber.org/zap"
)

type Router struct {
	engine *gin.Engine
	cfg    config.Config
}

func NewRouter(cfg config.Config, query *service.StateQueryService, metrics *observability.Metrics, logger *zap.Logger) *Router {
	if cfg.Env != "dev" {
		gin.SetMode(gin.ReleaseMode)
	}
	e := gin.New()
	e.Use(gin.Recovery())
	h := handlers.HealthHandler{ServiceName: cfg.ServiceName}
	sh := handlers.StateHandler{Query: query}
	e.GET("/health", h.Health)
	e.GET("/metrics", gin.WrapH(promhttp.Handler()))
	v := e.Group("/api/v1")
	v.GET("/state/market/:exchange/:symbol", sh.Market)
	v.GET("/state/bbo/:exchange/:symbol", sh.BBO)
	v.GET("/state/trade/:exchange/:symbol", sh.Trade)
	v.GET("/state/kline/:exchange/:symbol", sh.Kline)
	v.GET("/state/mark-price/:exchange/:symbol", sh.MarkPrice)
	v.GET("/state/funding/:exchange/:symbol", sh.Funding)
	v.GET("/state/snapshot/:exchange/:symbol", sh.Snapshot)
	v.GET("/state/freshness/:exchange/:symbol", sh.Freshness)
	v.GET("/ws/realtime", handlers.WebSocket)
	v.GET("/sse/realtime", handlers.SSE)
	return &Router{engine: e, cfg: cfg}
}
func (r *Router) Run(ctx context.Context) error { return r.engine.Run(":" + r.cfg.HTTPPort) }
func (r *Router) Engine() *gin.Engine           { return r.engine }
