package models

type ExecutionLog struct {
	Stage   string
	Result  string
	Message string
	TraceID string
}
