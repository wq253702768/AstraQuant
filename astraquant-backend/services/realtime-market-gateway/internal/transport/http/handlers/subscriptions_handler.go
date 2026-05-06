package handlers

import (
	"github.com/astraquant/realtime-market-gateway/internal/domain/models"
	"github.com/astraquant/realtime-market-gateway/internal/service"
	"github.com/gin-gonic/gin"
)

type SubscriptionsHandler struct{ Manager *service.SubscriptionManager }

func (h SubscriptionsHandler) List(c *gin.Context) { c.JSON(200, gin.H{"items": h.Manager.List()}) }
func (h SubscriptionsHandler) Add(c *gin.Context) {
	var req models.Subscription
	if err := c.BindJSON(&req); err != nil {
		c.JSON(400, gin.H{"code": "INVALID_REQUEST"})
		return
	}
	h.Manager.Add(req)
	c.JSON(200, gin.H{"status": "SUBSCRIBED"})
}
func (h SubscriptionsHandler) Remove(c *gin.Context) {
	var req models.Subscription
	if err := c.BindJSON(&req); err != nil {
		c.JSON(400, gin.H{"code": "INVALID_REQUEST"})
		return
	}
	h.Manager.Remove(req)
	c.JSON(200, gin.H{"status": "UNSUBSCRIBED"})
}
