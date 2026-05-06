package tracing

import (
	"crypto/rand"
	"encoding/hex"
	"net/http"
)

const Header = "X-Trace-Id"

func TraceID(r *http.Request) string {
	if value := r.Header.Get(Header); value != "" {
		return value
	}
	bytes := make([]byte, 16)
	_, _ = rand.Read(bytes)
	return "trace_" + hex.EncodeToString(bytes)
}
