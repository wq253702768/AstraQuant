package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

const traceHeader = "X-Trace-Id"

func main() {
	serviceName := getenv("SERVICE_NAME", "go-service-template")
	port := getenv("PORT", "8090")

	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, r, map[string]any{"status": "ok", "service": serviceName})
	})
	mux.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain; version=0.0.4")
		_, _ = w.Write([]byte("astraquant_service_health{service=\"" + serviceName + "\"} 1\n"))
	})

	logJSON("INFO", "starting service", "", map[string]any{"service": serviceName, "port": port})
	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatal(err)
	}
}

func writeJSON(w http.ResponseWriter, r *http.Request, data map[string]any) {
	traceID := r.Header.Get(traceHeader)
	if traceID == "" {
		traceID = fmt.Sprintf("trace_%d", time.Now().UnixNano())
	}
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set(traceHeader, traceID)
	_ = json.NewEncoder(w).Encode(map[string]any{"code": "SUCCESS", "message": "OK", "trace_id": traceID, "data": data})
}

func getenv(key string, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func logJSON(level string, message string, traceID string, fields map[string]any) {
	payload := map[string]any{"timestamp": time.Now().UTC().Format(time.RFC3339Nano), "level": level, "message": message, "trace_id": traceID}
	for key, value := range fields {
		payload[key] = value
	}
	encoded, _ := json.Marshal(payload)
	log.Println(string(encoded))
}
