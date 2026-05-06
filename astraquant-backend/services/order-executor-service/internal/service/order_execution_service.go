package service

import (
	"github.com/astraquant/order-executor-service/internal/config"
	"github.com/astraquant/order-executor-service/internal/domain/models"
	"github.com/astraquant/order-executor-service/internal/infrastructure/repositories"
	"github.com/astraquant/order-executor-service/internal/observability"
	"github.com/google/uuid"
	"go.uber.org/zap"
	"time"
)

type OrderExecutionService struct {
	Cfg     config.Config
	Gate    ExecutionGateService
	IDGen   ClientOrderIDService
	Idem    *IdempotencyService
	Orders  *repositories.LiveOrderRepository
	Metrics *observability.Metrics
	Logger  *zap.Logger
}

func NewOrderExecutionService(cfg config.Config, metrics *observability.Metrics, logger *zap.Logger) *OrderExecutionService {
	ks := NewKillSwitchService()
	return &OrderExecutionService{Cfg: cfg, Gate: ExecutionGateService{Cfg: cfg, Approval: ApprovalCheckService{}, Kill: ks}, IDGen: ClientOrderIDService{Prefix: cfg.ClientOrderIDPrefix}, Idem: NewIdempotencyService(), Orders: &repositories.LiveOrderRepository{}, Metrics: metrics, Logger: logger}
}
func (s *OrderExecutionService) DryRun(ctx models.ExecutionContext) models.LiveOrder {
	key := s.Idem.Key(ctx.SignalID, ctx.RiskDecisionID)
	id := uuid.NewString()
	if existing, ok := s.Idem.CheckAndSet(key, id); !ok {
		if order, found := s.Orders.Get(existing); found {
			return order
		}
	}
	gate := s.Gate.Check(ctx)
	status := "DRY_RUN_PASSED"
	mode := gate.Mode
	if !gate.Allowed {
		status = "GATED_REJECTED"
		mode = "LIVE_BLOCKED"
	}
	order := models.LiveOrder{ID: id, AccountID: ctx.AccountID, SignalID: ctx.SignalID, RiskDecisionID: ctx.RiskDecisionID, StrategyID: ctx.StrategyID, StrategyVersionID: ctx.StrategyVersionID, Exchange: ctx.Exchange, InternalSymbol: ctx.InternalSymbol, ExchangeSymbol: ctx.InternalSymbol, ClientOrderID: s.IDGen.Generate(ctx.Signal.Side), Side: ctx.Signal.Side, PositionSide: ctx.Signal.PositionSide, Action: ctx.Signal.Action, OrderType: ctx.Signal.OrderType, TradeMode: "cross", Price: ctx.Signal.Price, Quantity: ctx.Signal.Quantity, Leverage: ctx.Signal.Leverage, ReduceOnly: ctx.RiskDecision.ReduceOnly, ExecutionMode: mode, Status: status, IdempotencyKey: key, TraceID: ctx.TraceID, CreatedAt: time.Now().UnixMilli(), UpdatedAt: time.Now().UnixMilli()}
	s.Orders.Save(order)
	return order
}
func (s *OrderExecutionService) Cancel(id string) (models.LiveOrder, bool) {
	order, ok := s.Orders.Get(id)
	if !ok {
		return order, false
	}
	order.Status = "CANCEL_REQUESTED"
	return order, true
}
