package service

import (
	"crypto/sha256"
	"encoding/hex"
	"time"

	"go.uber.org/zap"
)

type AuditRecord struct {
	Exchange          string
	Endpoint          string
	Method            string
	RequestHash       string
	ResponseCode      string
	InternalErrorCode string
	LatencyMS         int64
	Priority          string
	TraceID           string
	CreatedAt         time.Time
}

type RequestAuditService struct {
	logger  *zap.Logger
	enabled bool
}

func NewRequestAuditService(logger *zap.Logger, enabled bool) *RequestAuditService {
	return &RequestAuditService{logger: logger, enabled: enabled}
}

func (s *RequestAuditService) HashRequest(summary string) string {
	sum := sha256.Sum256([]byte(summary))
	return hex.EncodeToString(sum[:])
}

func (s *RequestAuditService) Record(record AuditRecord) {
	if !s.enabled {
		return
	}
	s.logger.Info("exchange request audit",
		zap.String("exchange", record.Exchange), zap.String("endpoint", record.Endpoint), zap.String("method", record.Method),
		zap.String("response_code", record.ResponseCode), zap.String("internal_error_code", record.InternalErrorCode),
		zap.Int64("latency_ms", record.LatencyMS), zap.String("priority", record.Priority), zap.String("trace_id", record.TraceID),
	)
}
