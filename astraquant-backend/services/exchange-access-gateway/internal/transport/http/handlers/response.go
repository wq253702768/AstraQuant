package handlers

import (
	"net/http"

	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

func OK(c *gin.Context, data any) {
	c.JSON(http.StatusOK, gin.H{"code": "SUCCESS", "message": "OK", "trace_id": middleware.TraceID(c), "data": data})
}

func Items(c *gin.Context, items any) { OK(c, gin.H{"items": items}) }

func Error(c *gin.Context, err error) {
	if exchangeErr, ok := err.(*domainerrors.ExchangeError); ok {
		status := exchangeErr.StatusCode
		if status == 0 {
			status = http.StatusBadGateway
		}
		c.JSON(status, gin.H{"code": domainerrors.PublicCode(exchangeErr.Code), "message": domainerrors.PublicMessage(exchangeErr.Code, exchangeErr.Message), "trace_id": middleware.TraceID(c), "data": nil})
		return
	}
	c.JSON(http.StatusInternalServerError, gin.H{"code": "EXCHANGE_REQUEST_FAILED", "message": err.Error(), "trace_id": middleware.TraceID(c), "data": nil})
}
