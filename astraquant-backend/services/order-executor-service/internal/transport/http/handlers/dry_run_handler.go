package handlers

import (
	"github.com/astraquant/order-executor-service/internal/domain/models"
	"github.com/astraquant/order-executor-service/internal/service"
	"github.com/gin-gonic/gin"
)

type DryRunHandler struct {
	Executor *service.OrderExecutionService
}

func (h DryRunHandler) DryRun(c *gin.Context) {
	var req map[string]string
	_ = c.BindJSON(&req)
	ctx := models.ExecutionContext{SignalID: req["signal_id"], RiskDecisionID: req["risk_decision_id"], AccountID: "00000000-0000-0000-0000-000000000001", StrategyID: "00000000-0000-0000-0000-000000000002", StrategyVersionID: "00000000-0000-0000-0000-000000000003", Exchange: "OKX", InternalSymbol: "BTC-USDT-SWAP", RiskDecision: models.RiskDecision{Decision: "APPROVE", Approved: true}, Signal: models.SignalSnapshot{Side: "buy", PositionSide: "long", Action: "OPEN", OrderType: "ioc", Price: "1", Quantity: "0.01", Leverage: "1"}, AccountState: models.AccountStateSnapshot{Fresh: true, TradingEnabled: false, HasTradePermission: true}, PositionState: models.PositionStateSnapshot{Fresh: true}, OrderState: models.OrderStateSnapshot{Fresh: true}, AdmissionResult: models.SimulationAdmissionResult{Decision: "ALLOW_SMALL_LIVE_APPLICATION", ApprovalStatus: "APPROVED"}, ExecutionMode: "DRY_RUN"}
	order := h.Executor.DryRun(ctx)
	c.JSON(200, gin.H{"live_order_id": order.ID, "status": order.Status, "order_request": gin.H{"inst_id": order.InternalSymbol, "side": order.Side, "ord_type": order.OrderType, "sz": order.Quantity}})
}
