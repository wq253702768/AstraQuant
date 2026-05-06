package middleware

import (
	"crypto/rand"
	"encoding/hex"

	"github.com/gin-gonic/gin"
)

const TraceHeader = "X-Trace-Id"
const TraceContextKey = "trace_id"

func Trace() gin.HandlerFunc {
	return func(c *gin.Context) {
		traceID := c.GetHeader(TraceHeader)
		if traceID == "" {
			traceID = newTraceID()
		}
		c.Set(TraceContextKey, traceID)
		c.Writer.Header().Set(TraceHeader, traceID)
		c.Next()
	}
}

func TraceID(c *gin.Context) string {
	value, _ := c.Get(TraceContextKey)
	if traceID, ok := value.(string); ok {
		return traceID
	}
	return ""
}

func newTraceID() string {
	bytes := make([]byte, 16)
	_, _ = rand.Read(bytes)
	return "trace_" + hex.EncodeToString(bytes)
}
