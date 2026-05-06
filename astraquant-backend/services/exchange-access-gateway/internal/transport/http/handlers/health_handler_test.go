package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/astraquant/exchange-access-gateway/internal/transport/http/middleware"
	"github.com/gin-gonic/gin"
)

func TestHealthHandler(t *testing.T) {
	gin.SetMode(gin.TestMode)
	router := gin.New()
	router.Use(middleware.Trace())
	router.GET("/health", HealthHandler{ServiceName: "exchange-access-gateway"}.Health)
	recorder := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodGet, "/health", nil)
	request.Header.Set("X-Trace-Id", "trace_test")
	router.ServeHTTP(recorder, request)
	if recorder.Code != http.StatusOK {
		t.Fatalf("unexpected status: %d", recorder.Code)
	}
	if recorder.Header().Get("X-Trace-Id") != "trace_test" {
		t.Fatal("trace header missing")
	}
}
