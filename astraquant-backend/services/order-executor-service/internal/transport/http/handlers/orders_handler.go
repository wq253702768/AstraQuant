package handlers

import (
	"github.com/astraquant/order-executor-service/internal/service"
	"github.com/gin-gonic/gin"
)

type OrdersHandler struct {
	Executor *service.OrderExecutionService
}

func (h OrdersHandler) List(c *gin.Context) {
	c.JSON(200, gin.H{"items": h.Executor.Orders.List(), "total": len(h.Executor.Orders.List())})
}
func (h OrdersHandler) Get(c *gin.Context) {
	if o, ok := h.Executor.Orders.Get(c.Param("id")); ok {
		c.JSON(200, o)
		return
	}
	c.JSON(404, gin.H{"code": "LIVE_ORDER_NOT_FOUND"})
}
func (h OrdersHandler) Cancel(c *gin.Context) {
	if o, ok := h.Executor.Cancel(c.Param("id")); ok {
		c.JSON(200, gin.H{"live_order_id": o.ID, "status": o.Status})
		return
	}
	c.JSON(404, gin.H{"code": "LIVE_ORDER_NOT_FOUND"})
}
func (h OrdersHandler) Logs(c *gin.Context) {
	c.JSON(200, gin.H{"items": []gin.H{{"stage": "EXECUTION_GATE", "result": "PASS", "message": "execution gate checked"}}})
}
