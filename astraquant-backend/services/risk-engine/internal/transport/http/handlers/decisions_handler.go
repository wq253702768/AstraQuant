package handlers

import (
	"github.com/astraquant/risk-engine/internal/domain/models"
	"github.com/astraquant/risk-engine/internal/infrastructure/repositories"
	"github.com/astraquant/risk-engine/internal/service"
	"github.com/gin-gonic/gin"
)

type DecisionsHandler struct {
	Checker *service.RiskCheckService
	Repo    *repositories.RiskDecisionRepository
}

func (h DecisionsHandler) List(c *gin.Context) {
	c.JSON(200, gin.H{"items": h.Repo.List(), "total": len(h.Repo.List())})
}
func (h DecisionsHandler) Get(c *gin.Context) {
	if d, ok := h.Repo.Get(c.Param("id")); ok {
		c.JSON(200, d)
		return
	}
	c.JSON(404, gin.H{"code": "RISK_DECISION_NOT_FOUND"})
}
func (h DecisionsHandler) Check(c *gin.Context) {
	var sig models.SignalInput
	if err := c.BindJSON(&sig); err != nil {
		c.JSON(400, gin.H{"code": "INVALID_REQUEST"})
		return
	}
	d := h.Checker.Check(c.Request.Context(), sig)
	h.Repo.Save(d)
	c.JSON(200, gin.H{"risk_decision_id": d.ID, "decision": d.Decision, "approved": d.Approved})
}
