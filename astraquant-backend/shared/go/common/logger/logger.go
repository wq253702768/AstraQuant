package logger

import (
	"encoding/json"
	"log"
	"time"
)

type Entry struct {
	Timestamp string `json:"timestamp"`
	Level     string `json:"level"`
	Message   string `json:"message"`
	TraceID   string `json:"trace_id,omitempty"`
}

func Info(message string, traceID string) {
	payload, _ := json.Marshal(Entry{Timestamp: time.Now().UTC().Format(time.RFC3339Nano), Level: "INFO", Message: message, TraceID: traceID})
	log.Println(string(payload))
}
